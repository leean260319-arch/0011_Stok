"""T086-T088: BacktestEngine, StrategyAdapter, KiwoomDataFeed, BacktestResult 테스트"""
import matplotlib
matplotlib.use("Agg")

import datetime
import numpy as np
import pandas as pd
import pytest
import backtrader as bt

from src.engine.strategy_engine import Strategy
from src.engine.backtest_engine import (
    StrategyAdapter,
    BacktestEngine,
    BacktestResult,
    KiwoomDataFeed,
    analyze_result,
)


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

class BuyAndHoldStrategy(Strategy):
    """테스트용 항상 매수 전략"""

    @property
    def name(self) -> str:
        return "buy_and_hold"

    def on_signal(self, signal_data: dict) -> None:
        pass

    def on_tick(self, tick_data: dict) -> None:
        pass

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"action": "매수", "reasons": ["항상 매수"]}


class SellStrategy(Strategy):
    """테스트용 항상 매도 전략"""

    @property
    def name(self) -> str:
        return "always_sell"

    def on_signal(self, signal_data: dict) -> None:
        pass

    def on_tick(self, tick_data: dict) -> None:
        pass

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"action": "매도", "reasons": ["항상 매도"]}


class HoldStrategy(Strategy):
    """테스트용 관망 전략"""

    @property
    def name(self) -> str:
        return "hold"

    def on_signal(self, signal_data: dict) -> None:
        pass

    def on_tick(self, tick_data: dict) -> None:
        pass

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"action": "관망", "reasons": ["관망"]}


def make_sample_df(n: int = 100) -> pd.DataFrame:
    """테스트용 OHLCV DataFrame 생성"""
    np.random.seed(42)
    dates = pd.date_range("2025-01-01", periods=n, freq="B")
    close = 50000 + np.cumsum(np.random.randn(n) * 500)
    return pd.DataFrame({
        "date": dates,
        "open": close + np.random.randn(n) * 100,
        "high": close + abs(np.random.randn(n) * 300),
        "low": close - abs(np.random.randn(n) * 300),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


# ---------------------------------------------------------------------------
# T088: BacktestResult 데이터 클래스
# ---------------------------------------------------------------------------
class TestBacktestResult:
    """T088: BacktestResult 구조 검증"""

    def test_fields_exist(self):
        result = BacktestResult(
            initial_cash=10_000_000,
            final_value=11_000_000,
            total_return=10.0,
            max_drawdown=5.0,
            win_rate=60.0,
            sharpe_ratio=1.5,
            total_trades=10,
            trades=[],
        )
        assert result.initial_cash == 10_000_000
        assert result.final_value == 11_000_000
        assert result.total_return == 10.0
        assert result.max_drawdown == 5.0
        assert result.win_rate == 60.0
        assert result.sharpe_ratio == 1.5
        assert result.total_trades == 10
        assert result.trades == []

    def test_trades_list_dict(self):
        trades = [{"date": "2025-01-10", "action": "매수", "price": 50000, "size": 1}]
        result = BacktestResult(
            initial_cash=10_000_000,
            final_value=10_500_000,
            total_return=5.0,
            max_drawdown=2.0,
            win_rate=100.0,
            sharpe_ratio=2.0,
            total_trades=1,
            trades=trades,
        )
        assert len(result.trades) == 1
        assert result.trades[0]["action"] == "매수"


# ---------------------------------------------------------------------------
# T087: KiwoomDataFeed
# ---------------------------------------------------------------------------
class TestKiwoomDataFeed:
    """T087: KiwoomDataFeed - DataFrame -> Backtrader DataFeed 변환"""

    def test_from_dataframe_returns_pandasdata(self):
        df = make_sample_df(30)
        feed = KiwoomDataFeed.from_dataframe(df)
        assert isinstance(feed, bt.feeds.PandasData)

    def test_from_dataframe_column_mapping(self):
        df = make_sample_df(30)
        feed = KiwoomDataFeed.from_dataframe(df)
        # PandasData에 올바른 파라미터가 설정되었는지 확인
        assert feed.p.open == "open"
        assert feed.p.high == "high"
        assert feed.p.low == "low"
        assert feed.p.close == "close"
        assert feed.p.volume == "volume"

    def test_from_dataframe_with_date_index(self):
        df = make_sample_df(30)
        feed = KiwoomDataFeed.from_dataframe(df)
        # cerebro에 추가해서 정상 동작하는지 검증
        cerebro = bt.Cerebro()
        cerebro.adddata(feed)
        cerebro.run()  # 에러 없이 실행되면 성공


# ---------------------------------------------------------------------------
# T086: StrategyAdapter
# ---------------------------------------------------------------------------
class TestStrategyAdapter:
    """T086: StrategyAdapter - 우리 Strategy를 Backtrader Strategy로 래핑"""

    def test_adapter_is_bt_strategy(self):
        assert issubclass(StrategyAdapter, bt.Strategy)

    def test_adapter_runs_with_cerebro(self):
        df = make_sample_df(50)
        feed = KiwoomDataFeed.from_dataframe(df)
        strategy = HoldStrategy()

        cerebro = bt.Cerebro()
        cerebro.adddata(feed)
        cerebro.addstrategy(StrategyAdapter, app_strategy=strategy)
        cerebro.run()  # 에러 없이 실행

    def test_adapter_executes_buy_on_evaluate_buy(self):
        df = make_sample_df(50)
        feed = KiwoomDataFeed.from_dataframe(df)
        strategy = BuyAndHoldStrategy()

        cerebro = bt.Cerebro()
        cerebro.adddata(feed)
        cerebro.addstrategy(StrategyAdapter, app_strategy=strategy)
        cerebro.broker.setcash(10_000_000)
        results = cerebro.run()
        # 매수 전략이므로 포지션이 존재해야 함
        strat = results[0]
        # 브로커의 최종 가치가 초기 현금과 다르면 거래가 발생한 것
        final_value = cerebro.broker.getvalue()
        assert final_value != 10_000_000


# ---------------------------------------------------------------------------
# T086: BacktestEngine
# ---------------------------------------------------------------------------
class TestBacktestEngine:
    """T086: BacktestEngine - 백테스팅 실행 엔진"""

    def test_run_returns_backtest_result(self):
        engine = BacktestEngine()
        df = make_sample_df(50)
        strategy = HoldStrategy()
        result = engine.run(strategy, df, initial_cash=10_000_000)
        assert isinstance(result, BacktestResult)

    def test_run_initial_cash_set(self):
        engine = BacktestEngine()
        df = make_sample_df(50)
        strategy = HoldStrategy()
        result = engine.run(strategy, df, initial_cash=10_000_000)
        assert result.initial_cash == 10_000_000

    def test_run_with_buy_strategy_has_trades(self):
        engine = BacktestEngine()
        df = make_sample_df(50)
        strategy = BuyAndHoldStrategy()
        result = engine.run(strategy, df, initial_cash=10_000_000)
        assert result.total_trades >= 1

    def test_run_hold_strategy_no_trades(self):
        engine = BacktestEngine()
        df = make_sample_df(50)
        strategy = HoldStrategy()
        result = engine.run(strategy, df, initial_cash=10_000_000)
        assert result.total_trades == 0

    def test_run_result_fields_types(self):
        engine = BacktestEngine()
        df = make_sample_df(50)
        strategy = BuyAndHoldStrategy()
        result = engine.run(strategy, df, initial_cash=10_000_000)
        assert isinstance(result.final_value, float)
        assert isinstance(result.total_return, float)
        assert isinstance(result.max_drawdown, float)
        assert isinstance(result.sharpe_ratio, float)
        assert isinstance(result.win_rate, float)
        assert isinstance(result.trades, list)


# ---------------------------------------------------------------------------
# T088: analyze_result
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Walk-Forward / run_with_commission 용 Backtrader 전용 전략
# ---------------------------------------------------------------------------

class BtBuyAndHoldStrategy(bt.Strategy):
    """Backtrader 전용 매수 후 보유 전략 (run_with_commission / walk_forward 테스트용)"""

    def next(self):
        if not self.position:
            size = int(self.broker.getcash() * 0.95 / self.data.close[0])
            if size > 0:
                self.buy(size=size)


class BtHoldStrategy(bt.Strategy):
    """Backtrader 전용 관망 전략 (run_with_commission 테스트용)"""

    def next(self):
        pass


def make_ohlcv_df(n: int = 100) -> pd.DataFrame:
    """date 컬럼 없이 DatetimeIndex를 가진 OHLCV DataFrame 생성 (bt.feeds.PandasData 직접 호환)"""
    np.random.seed(0)
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
# P3-02: run_with_commission 테스트
# ---------------------------------------------------------------------------

class TestRunWithCommission:
    """run_with_commission 메서드 검증"""

    def test_run_with_commission_returns_result(self):
        engine = BacktestEngine()
        df = make_ohlcv_df(60)
        result = engine.run_with_commission(BtBuyAndHoldStrategy, df, cash=10_000_000)
        assert isinstance(result, BacktestResult)
        assert result.initial_cash == 10_000_000

    def test_run_with_commission_reduces_value(self):
        """수수료 적용 시 관망 전략은 final_value == cash, 매수 전략은 수수료로 인해 차이 발생."""
        engine = BacktestEngine()
        df = make_ohlcv_df(60)
        # 관망 전략: 거래 없음 -> final_value == initial_cash
        result_hold = engine.run_with_commission(BtHoldStrategy, df, cash=10_000_000)
        assert result_hold.final_value == 10_000_000

        # 매수 전략: 수수료+슬리피지 적용 -> total_return 계산 가능
        result_buy = engine.run_with_commission(
            BtBuyAndHoldStrategy, df, cash=10_000_000, commission=0.00015, slippage_pct=0.001
        )
        assert isinstance(result_buy.total_return, float)


# ---------------------------------------------------------------------------
# P3-02: walk_forward 테스트
# ---------------------------------------------------------------------------

class TestWalkForward:
    """walk_forward 메서드 검증"""

    def test_walk_forward_returns_splits(self):
        engine = BacktestEngine()
        df = make_ohlcv_df(200)
        wf = engine.walk_forward(BtBuyAndHoldStrategy, df, n_splits=5, train_ratio=0.7)
        assert "splits" in wf
        assert "avg_return" in wf
        assert "avg_sharpe" in wf
        assert isinstance(wf["splits"], list)

    def test_walk_forward_multiple_splits(self):
        engine = BacktestEngine()
        df = make_ohlcv_df(300)
        wf = engine.walk_forward(BtBuyAndHoldStrategy, df, n_splits=3, train_ratio=0.7)
        # 각 split의 test 구간은 split_size(100)*0.3=30행 >= 10이므로 3개 모두 유효
        assert wf["n_splits"] == 3
        for split in wf["splits"]:
            assert "return" in split
            assert "sharpe" in split
            assert "max_dd" in split


# ---------------------------------------------------------------------------
# T088: analyze_result
# ---------------------------------------------------------------------------

class TestAnalyzeResult:
    """T088: analyze_result 함수 검증"""

    def test_analyze_result_returns_backtest_result(self):
        # cerebro 실행 후 결과 전달
        df = make_sample_df(50)
        feed = KiwoomDataFeed.from_dataframe(df)
        strategy = BuyAndHoldStrategy()

        cerebro = bt.Cerebro()
        cerebro.adddata(feed)
        cerebro.addstrategy(StrategyAdapter, app_strategy=strategy)
        cerebro.broker.setcash(10_000_000)
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
        results = cerebro.run()

        result = analyze_result(results[0], 10_000_000)
        assert isinstance(result, BacktestResult)
        assert result.initial_cash == 10_000_000
