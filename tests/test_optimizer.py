"""P3-04: StrategyOptimizer - Optuna 기반 전략 파라미터 자동 최적화 테스트"""

# 버전 정보
# v1.0 - 2026-03-17: 신규 작성

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest

optuna = pytest.importorskip("optuna")

from src.engine.backtest_engine import BacktestEngine, BacktestResult
from src.engine.optimizer import (
    DEFAULT_PARAM_SPACE,
    OptimizationResult,
    StrategyOptimizer,
)


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

def make_ohlcv_df(n: int = 200) -> pd.DataFrame:
    """테스트용 OHLCV DataFrame 생성 (DatetimeIndex)"""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    close = 50000 + np.cumsum(np.random.randn(n) * 500)
    return pd.DataFrame(
        {
            "open": close + np.random.randn(n) * 100,
            "high": close + abs(np.random.randn(n) * 300),
            "low": close - abs(np.random.randn(n) * 300),
            "close": close,
            "volume": np.random.randint(10000, 100000, n).astype(float),
        },
        index=dates,
    )


# ---------------------------------------------------------------------------
# OptimizationResult 데이터 클래스 테스트
# ---------------------------------------------------------------------------

class TestOptimizationResult:
    """OptimizationResult 구조 검증"""

    def test_fields_exist(self):
        result = OptimizationResult(
            best_params={"rsi_period": 14},
            best_sharpe=1.5,
            n_trials=10,
            optimization_history=[],
        )
        assert result.best_params == {"rsi_period": 14}
        assert result.best_sharpe == 1.5
        assert result.n_trials == 10
        assert result.optimization_history == []

    def test_optimization_history_contains_dicts(self):
        history = [{"trial": 0, "params": {"rsi_period": 10}, "sharpe": 0.5}]
        result = OptimizationResult(
            best_params={"rsi_period": 10},
            best_sharpe=0.5,
            n_trials=1,
            optimization_history=history,
        )
        assert len(result.optimization_history) == 1
        assert "sharpe" in result.optimization_history[0]


# ---------------------------------------------------------------------------
# DEFAULT_PARAM_SPACE 검증
# ---------------------------------------------------------------------------

class TestDefaultParamSpace:
    """기본 파라미터 공간 검증"""

    def test_has_required_keys(self):
        assert "rsi_period" in DEFAULT_PARAM_SPACE
        assert "buy_threshold" in DEFAULT_PARAM_SPACE
        assert "sell_threshold" in DEFAULT_PARAM_SPACE

    def test_ranges_are_tuples_of_two(self):
        for key, val in DEFAULT_PARAM_SPACE.items():
            assert isinstance(val, tuple), f"{key}은 tuple이어야 함"
            assert len(val) == 2, f"{key}은 (min, max) 형태여야 함"
            assert val[0] < val[1], f"{key}의 min < max이어야 함"


# ---------------------------------------------------------------------------
# StrategyOptimizer 초기화 테스트
# ---------------------------------------------------------------------------

class TestStrategyOptimizerInit:
    """StrategyOptimizer 생성자 검증"""

    def test_init_with_backtest_engine(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        assert optimizer._engine is engine


# ---------------------------------------------------------------------------
# StrategyOptimizer.optimize 테스트
# ---------------------------------------------------------------------------

class TestOptimize:
    """optimize 메서드 검증"""

    def test_optimize_returns_optimization_result(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=3,
            cash=10_000_000,
        )
        assert isinstance(result, OptimizationResult)

    def test_optimize_best_params_has_keys(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=3,
        )
        # 기본 param_space 키가 best_params에 존재
        for key in DEFAULT_PARAM_SPACE:
            assert key in result.best_params

    def test_optimize_n_trials_matches(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=5,
        )
        assert result.n_trials == 5

    def test_optimize_history_length_matches_trials(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=4,
        )
        assert len(result.optimization_history) == 4

    def test_optimize_best_sharpe_is_float(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=3,
        )
        assert isinstance(result.best_sharpe, float)

    def test_optimize_custom_param_space(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        custom_space = {
            "rsi_period": (10, 20),
            "buy_threshold": (0.2, 0.4),
            "sell_threshold": (-0.4, -0.2),
        }
        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=3,
            param_space=custom_space,
        )
        # 결과 파라미터가 커스텀 범위 내에 있는지 확인
        assert 10 <= result.best_params["rsi_period"] <= 20
        assert 0.2 <= result.best_params["buy_threshold"] <= 0.4
        assert -0.4 <= result.best_params["sell_threshold"] <= -0.2

    def test_optimize_with_extended_param_space(self):
        """MACD, BB 파라미터까지 포함한 확장 파라미터 공간 테스트"""
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(200)

        extended_space = {
            "rsi_period": (7, 21),
            "macd_fast": (8, 16),
            "macd_slow": (20, 30),
            "bb_period": (15, 25),
            "bb_std": (1.5, 3.0),
            "buy_threshold": (0.1, 0.4),
            "sell_threshold": (-0.4, -0.1),
        }
        result = optimizer.optimize(
            strategy_cls=None,
            data=df,
            n_trials=3,
            param_space=extended_space,
        )
        for key in extended_space:
            assert key in result.best_params


# ---------------------------------------------------------------------------
# StrategyOptimizer.optimize_walk_forward 테스트
# ---------------------------------------------------------------------------

class TestOptimizeWalkForward:
    """optimize_walk_forward 메서드 검증 (과적합 방지)"""

    def test_walk_forward_returns_optimization_result(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(600)

        result = optimizer.optimize_walk_forward(
            strategy_cls=None,
            data=df,
            n_trials=3,
            n_splits=3,
        )
        assert isinstance(result, OptimizationResult)

    def test_walk_forward_best_params_exist(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(600)

        result = optimizer.optimize_walk_forward(
            strategy_cls=None,
            data=df,
            n_trials=3,
            n_splits=3,
        )
        assert isinstance(result.best_params, dict)
        assert len(result.best_params) > 0

    def test_walk_forward_n_trials_matches(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(600)

        result = optimizer.optimize_walk_forward(
            strategy_cls=None,
            data=df,
            n_trials=4,
            n_splits=3,
        )
        assert result.n_trials == 4

    def test_walk_forward_history_has_entries(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(600)

        result = optimizer.optimize_walk_forward(
            strategy_cls=None,
            data=df,
            n_trials=3,
            n_splits=3,
        )
        assert len(result.optimization_history) == 3

    def test_walk_forward_best_sharpe_is_float(self):
        engine = BacktestEngine()
        optimizer = StrategyOptimizer(engine)
        df = make_ohlcv_df(600)

        result = optimizer.optimize_walk_forward(
            strategy_cls=None,
            data=df,
            n_trials=3,
            n_splits=2,
        )
        assert isinstance(result.best_sharpe, float)
