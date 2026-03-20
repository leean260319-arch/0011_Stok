"""T086-T088: 백테스팅 엔진 - Backtrader 통합, 데이터 로더, 결과 분석"""

# 버전 정보
# v1.0 - 2026-03-17: 신규 작성

import matplotlib
matplotlib.use("Agg")

from dataclasses import dataclass, field

import backtrader as bt
import pandas as pd

from src.engine.strategy_engine import Strategy


@dataclass
class BacktestResult:
    """백테스팅 결과 데이터 클래스."""

    initial_cash: float
    final_value: float
    total_return: float
    max_drawdown: float
    win_rate: float
    sharpe_ratio: float
    total_trades: int
    trades: list[dict] = field(default_factory=list)


class KiwoomDataFeed(bt.feeds.PandasData):
    """키움 API OHLCV DataFrame을 Backtrader DataFeed로 변환."""

    params = (
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", None),
    )

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "KiwoomDataFeed":
        """pandas DataFrame을 KiwoomDataFeed로 변환한다."""
        data = df.copy()
        if "date" in data.columns:
            data = data.set_index("date")
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        return cls(dataname=data)


class StrategyAdapter(bt.Strategy):
    """우리의 Strategy를 Backtrader Strategy로 래핑하는 어댑터."""

    params = (("app_strategy", None),)

    def __init__(self):
        self._app_strategy: Strategy = self.p.app_strategy
        self._has_position = False

    def next(self):
        market_data = {
            "close": self.data.close[0],
            "open": self.data.open[0],
            "high": self.data.high[0],
            "low": self.data.low[0],
            "volume": self.data.volume[0],
        }
        result = self._app_strategy.evaluate(market_data)
        action = result.get("action", "관망")

        if action == "매수" and not self._has_position:
            size = int(self.broker.getcash() * 0.95 / self.data.close[0])
            if size > 0:
                self.buy(size=size)
                self._has_position = True
        elif action == "매도" and self._has_position:
            self.close()
            self._has_position = False


def analyze_result(strat_result, initial_cash: float) -> BacktestResult:
    """Backtrader 실행 결과를 BacktestResult로 변환한다."""
    final_value = strat_result.broker.getvalue()
    total_return = ((final_value - initial_cash) / initial_cash) * 100

    # DrawDown 분석
    max_drawdown = 0.0
    if hasattr(strat_result, "analyzers"):
        dd = strat_result.analyzers.getbyname("drawdown")
        if dd:
            dd_analysis = dd.get_analysis()
            max_drawdown = dd_analysis.get("max", {}).get("drawdown", 0.0)

    # Sharpe Ratio
    sharpe_ratio = 0.0
    sharpe = strat_result.analyzers.getbyname("sharpe")
    if sharpe:
        sharpe_analysis = sharpe.get_analysis()
        sr = sharpe_analysis.get("sharperatio", None)
        if sr is not None:
            sharpe_ratio = float(sr)

    # Trade 분석
    total_trades = 0
    win_rate = 0.0
    trades_list = []
    trade_analyzer = strat_result.analyzers.getbyname("trades")
    if trade_analyzer:
        ta = trade_analyzer.get_analysis()
        total_obj = ta.get("total", {})
        if isinstance(total_obj, dict):
            closed = total_obj.get("closed", 0)
            opened = total_obj.get("open", 0)
            total_trades = closed + opened
        else:
            total_trades = 0
        if total_trades > 0:
            won = ta.get("won", {}).get("total", 0)
            win_rate = (won / total_trades) * 100

    return BacktestResult(
        initial_cash=initial_cash,
        final_value=float(final_value),
        total_return=total_return,
        max_drawdown=max_drawdown,
        win_rate=win_rate,
        sharpe_ratio=sharpe_ratio,
        total_trades=total_trades,
        trades=trades_list,
    )


class BacktestEngine:
    """백테스팅 실행 엔진."""

    def run(
        self,
        strategy: Strategy,
        df: pd.DataFrame,
        initial_cash: float = 10_000_000,
    ) -> BacktestResult:
        """백테스팅을 실행하고 결과를 반환한다."""
        cerebro = bt.Cerebro()

        feed = KiwoomDataFeed.from_dataframe(df)
        cerebro.adddata(feed)

        cerebro.addstrategy(StrategyAdapter, app_strategy=strategy)
        cerebro.broker.setcash(initial_cash)

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")

        results = cerebro.run()
        return analyze_result(results[0], initial_cash)

    def run_with_commission(
        self,
        strategy_cls,
        data: pd.DataFrame,
        cash: float = 10_000_000,
        commission: float = 0.00015,
        slippage_pct: float = 0.001,
    ) -> BacktestResult:
        """수수료 + 슬리피지를 반영한 백테스트.

        Args:
            strategy_cls: Backtrader Strategy 클래스
            data: OHLCV DataFrame
            cash: 초기 자금
            commission: 수수료율 (기본 0.015%)
            slippage_pct: 슬리피지 비율 (기본 0.1%)

        Returns:
            BacktestResult
        """
        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy_cls)

        bt_data = KiwoomDataFeed.from_dataframe(data)
        cerebro.adddata(bt_data)

        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission=commission)
        cerebro.broker.set_slippage_perc(slippage_pct)

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")

        results = cerebro.run()
        strat = results[0]

        final_value = cerebro.broker.getvalue()
        total_return = (final_value - cash) / cash

        sharpe_analysis = strat.analyzers.sharpe.get_analysis()
        dd_analysis = strat.analyzers.drawdown.get_analysis()
        trade_analysis = strat.analyzers.trades.get_analysis()

        sharpe_ratio = sharpe_analysis.get("sharperatio", 0) or 0
        max_drawdown = dd_analysis.get("max", {}).get("drawdown", 0) / 100

        total_trades = trade_analysis.get("total", {}).get("total", 0)
        won = trade_analysis.get("won", {}).get("total", 0)
        win_rate = won / total_trades if total_trades > 0 else 0

        return BacktestResult(
            initial_cash=cash,
            final_value=round(final_value, 0),
            total_return=round(total_return, 6),
            max_drawdown=round(max_drawdown, 6),
            win_rate=round(win_rate, 4),
            sharpe_ratio=round(sharpe_ratio, 4),
            total_trades=total_trades,
            trades=[],
        )

    def walk_forward(
        self,
        strategy_cls,
        data: pd.DataFrame,
        n_splits: int = 5,
        train_ratio: float = 0.7,
        cash: float = 10_000_000,
        commission: float = 0.00015,
    ) -> dict:
        """Walk-Forward Analysis - 다중 윈도우 백테스트.

        Args:
            strategy_cls: Backtrader Strategy 클래스
            data: OHLCV DataFrame
            n_splits: 분할 수
            train_ratio: 학습 데이터 비율
            cash: 초기 자금
            commission: 수수료율

        Returns:
            {"splits": list[dict], "avg_return": float, "avg_sharpe": float}
        """
        total_len = len(data)
        split_size = total_len // n_splits
        results = []

        for i in range(n_splits):
            start = i * split_size
            end = min(start + split_size, total_len)
            window = data.iloc[start:end].copy()

            train_end = int(len(window) * train_ratio)
            test_data = window.iloc[train_end:].copy()

            if len(test_data) < 10:
                continue

            result = self.run_with_commission(
                strategy_cls, test_data, cash=cash, commission=commission
            )
            results.append({
                "split": i + 1,
                "test_start": str(test_data.index[0]),
                "test_end": str(test_data.index[-1]),
                "return": result.total_return,
                "sharpe": result.sharpe_ratio,
                "max_dd": result.max_drawdown,
                "trades": result.total_trades,
            })

        avg_return = sum(r["return"] for r in results) / len(results) if results else 0
        avg_sharpe = sum(r["sharpe"] for r in results) / len(results) if results else 0

        return {
            "splits": results,
            "n_splits": len(results),
            "avg_return": round(avg_return, 6),
            "avg_sharpe": round(avg_sharpe, 4),
        }
