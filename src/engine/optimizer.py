"""P3-04: 전략 자동 최적화기 - Optuna 기반 파라미터 탐색

버전: 1.0.0
작성일: 2026-03-17

Optuna를 이용해 전략 파라미터를 자동 탐색하고,
Walk-Forward 교차검증으로 과적합을 방지한다.
목적함수: Sharpe Ratio 최대화
"""

import matplotlib
matplotlib.use("Agg")

from dataclasses import dataclass, field

import backtrader as bt
import optuna
import pandas as pd

from src.engine.backtest_engine import BacktestEngine, KiwoomDataFeed

optuna.logging.set_verbosity(optuna.logging.WARNING)


DEFAULT_PARAM_SPACE = {
    "rsi_period": (7, 21),
    "buy_threshold": (0.1, 0.5),
    "sell_threshold": (-0.5, -0.1),
}


@dataclass
class OptimizationResult:
    """최적화 결과 데이터 클래스."""

    best_params: dict
    best_sharpe: float
    n_trials: int
    optimization_history: list[dict] = field(default_factory=list)


def _make_parameterized_strategy(params: dict) -> type:
    """주어진 파라미터로 Backtrader Strategy 클래스를 동적 생성한다."""

    class ParameterizedStrategy(bt.Strategy):
        _params = params

        def __init__(self):
            self._has_position = False
            data_close = self.data.close
            period = self._params.get("rsi_period", 14)
            self._rsi = bt.indicators.RSI(data_close, period=period)

            macd_fast = self._params.get("macd_fast", 12)
            macd_slow = self._params.get("macd_slow", 26)
            self._macd = bt.indicators.MACD(
                data_close, period_me1=macd_fast, period_me2=macd_slow
            )

            bb_period = self._params.get("bb_period", 20)
            bb_std = self._params.get("bb_std", 2.0)
            self._bb = bt.indicators.BollingerBands(
                data_close, period=bb_period, devfactor=bb_std
            )

        def next(self):
            buy_threshold = self._params.get("buy_threshold", 0.2)
            sell_threshold = self._params.get("sell_threshold", -0.2)

            score = 0.0

            # RSI 시그널
            rsi_val = self._rsi[0]
            if rsi_val < 30:
                score += 0.3
            elif rsi_val > 70:
                score -= 0.3

            # MACD 시그널
            if self._macd.macd[0] > self._macd.signal[0]:
                score += 0.3
            elif self._macd.macd[0] < self._macd.signal[0]:
                score -= 0.3

            # BB 시그널
            if self.data.close[0] < self._bb.bot[0]:
                score += 0.2
            elif self.data.close[0] > self._bb.top[0]:
                score -= 0.2

            if score > buy_threshold and not self._has_position:
                size = int(self.broker.getcash() * 0.95 / self.data.close[0])
                if size > 0:
                    self.buy(size=size)
                    self._has_position = True
            elif score < sell_threshold and self._has_position:
                self.close()
                self._has_position = False

    return ParameterizedStrategy


class StrategyOptimizer:
    """Optuna 기반 전략 파라미터 자동 최적화기."""

    def __init__(self, backtest_engine: BacktestEngine):
        self._engine = backtest_engine

    def _run_backtest_with_params(
        self, params: dict, data: pd.DataFrame, cash: float
    ) -> float:
        """주어진 파라미터로 백테스트를 실행하고 Sharpe Ratio를 반환한다."""
        strategy_cls = _make_parameterized_strategy(params)
        result = self._engine.run_with_commission(strategy_cls, data, cash=cash)
        return float(result.sharpe_ratio)

    def optimize(
        self,
        strategy_cls,
        data: pd.DataFrame,
        n_trials: int = 50,
        param_space: dict = None,
        cash: float = 10_000_000,
    ) -> OptimizationResult:
        """Optuna로 전략 파라미터 최적화.

        Args:
            strategy_cls: 사용하지 않음 (내부에서 동적 생성). 인터페이스 호환용.
            data: OHLCV DataFrame
            n_trials: 탐색 횟수
            param_space: 파라미터 범위 dict. None이면 DEFAULT_PARAM_SPACE 사용.
            cash: 초기 자금

        Returns:
            OptimizationResult
        """
        space = param_space or DEFAULT_PARAM_SPACE
        history = []

        def objective(trial: optuna.Trial) -> float:
            params = {}
            for key, (low, high) in space.items():
                if isinstance(low, int) and isinstance(high, int):
                    params[key] = trial.suggest_int(key, low, high)
                else:
                    params[key] = trial.suggest_float(key, float(low), float(high))

            sharpe = self._run_backtest_with_params(params, data, cash)
            history.append({"trial": trial.number, "params": params, "sharpe": sharpe})
            return sharpe

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials)

        best_params = study.best_trial.params
        best_sharpe = float(study.best_value)

        return OptimizationResult(
            best_params=best_params,
            best_sharpe=best_sharpe,
            n_trials=n_trials,
            optimization_history=history,
        )

    def optimize_walk_forward(
        self,
        strategy_cls,
        data: pd.DataFrame,
        n_trials: int = 30,
        n_splits: int = 5,
        train_ratio: float = 0.7,
        cash: float = 10_000_000,
        param_space: dict = None,
    ) -> OptimizationResult:
        """Walk-Forward 기반 최적화 (과적합 방지).

        각 split의 train 구간에서 최적 파라미터를 찾고,
        test 구간에서 성능을 검증한다.
        최종 결과는 모든 split의 평균 Sharpe Ratio로 결정한다.

        Args:
            strategy_cls: 사용하지 않음 (내부에서 동적 생성). 인터페이스 호환용.
            data: OHLCV DataFrame
            n_trials: split당 탐색 횟수
            n_splits: Walk-Forward 분할 수
            train_ratio: 학습 데이터 비율
            cash: 초기 자금
            param_space: 파라미터 범위 dict

        Returns:
            OptimizationResult
        """
        space = param_space or DEFAULT_PARAM_SPACE
        total_len = len(data)
        split_size = total_len // n_splits
        history = []

        best_overall_params = {}
        best_overall_sharpe = float("-inf")

        for i in range(n_splits):
            start = i * split_size
            end = min(start + split_size, total_len)
            window = data.iloc[start:end].copy()

            train_end = int(len(window) * train_ratio)
            train_data = window.iloc[:train_end].copy()
            test_data = window.iloc[train_end:].copy()

            # 지표 계산에 최소 데이터 필요 (MACD slow=26 등)
            if len(train_data) < 60 or len(test_data) < 40:
                continue

            # train 구간에서 최적 파라미터 탐색
            def make_objective(train_df: pd.DataFrame):
                def objective(trial: optuna.Trial) -> float:
                    params = {}
                    for key, (low, high) in space.items():
                        if isinstance(low, int) and isinstance(high, int):
                            params[key] = trial.suggest_int(key, low, high)
                        else:
                            params[key] = trial.suggest_float(
                                key, float(low), float(high)
                            )
                    return self._run_backtest_with_params(params, train_df, cash)

                return objective

            study = optuna.create_study(direction="maximize")
            study.optimize(make_objective(train_data), n_trials=n_trials)

            split_best_params = study.best_trial.params

            # test 구간에서 검증
            test_sharpe = self._run_backtest_with_params(
                split_best_params, test_data, cash
            )

            history.append(
                {
                    "split": i + 1,
                    "train_sharpe": float(study.best_value),
                    "test_sharpe": test_sharpe,
                    "params": split_best_params,
                }
            )

            if test_sharpe > best_overall_sharpe:
                best_overall_sharpe = test_sharpe
                best_overall_params = split_best_params

        # 평균 test sharpe
        if history:
            avg_test_sharpe = sum(h["test_sharpe"] for h in history) / len(history)
        else:
            avg_test_sharpe = 0.0

        return OptimizationResult(
            best_params=best_overall_params,
            best_sharpe=float(avg_test_sharpe),
            n_trials=n_trials,
            optimization_history=history,
        )
