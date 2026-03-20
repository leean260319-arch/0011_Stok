"""UI 차트 위젯 바인딩 테스트
버전: v1.0
설명: matplotlib 기반 차트 위젯의 클래스 생성/메서드 호출 테스트 (렌더링 검증 아님)
"""

import matplotlib
matplotlib.use("Agg")

from datetime import datetime

import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# 1. chart_view.py - CandlestickCanvas, ChartView
# ---------------------------------------------------------------------------
class TestCandlestickCanvas:
    """CandlestickCanvas 생성 및 update_chart 테스트."""

    def test_creation(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        canvas = CandlestickCanvas()
        assert canvas is not None
        assert canvas._fig is not None

    def test_update_chart_with_data(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        canvas = CandlestickCanvas()
        df = _make_ohlcv_df(30)
        canvas.update_chart(df)
        assert canvas._df is not None

    def test_update_chart_empty(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        canvas = CandlestickCanvas()
        canvas.update_chart(pd.DataFrame())

    def test_update_chart_none(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        canvas = CandlestickCanvas()
        canvas.update_chart(None)

    def test_update_chart_with_overlays(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        canvas = CandlestickCanvas()
        df = _make_ohlcv_df(30)
        canvas.update_chart(df, overlays=["MA20", "BB20", "EMA10"])

    def test_draw_markers(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        canvas = CandlestickCanvas()
        df = _make_ohlcv_df(30)
        canvas.update_chart(df)
        markers = [
            {"index": 5, "price": 10500, "type": "buy"},
            {"index": 15, "price": 10800, "type": "sell"},
        ]
        canvas.draw_markers(markers)

    def test_extract_period(self, qapp):
        from src.ui.chart_view import CandlestickCanvas
        assert CandlestickCanvas._extract_period("MA20") == 20
        assert CandlestickCanvas._extract_period("BB") == 20
        assert CandlestickCanvas._extract_period("EMA50") == 50


class TestChartViewIntegration:
    """ChartView의 set_data, overlay, marker 통합 테스트."""

    def test_set_data(self, qapp):
        from src.ui.chart_view import ChartView
        view = ChartView()
        df = _make_ohlcv_df(20)
        view.set_data(df)
        assert view._df is not None

    def test_canvas_property(self, qapp):
        from src.ui.chart_view import ChartView, CandlestickCanvas
        view = ChartView()
        assert isinstance(view.canvas, CandlestickCanvas)

    def test_overlay_triggers_redraw(self, qapp):
        from src.ui.chart_view import ChartView
        view = ChartView()
        df = _make_ohlcv_df(30)
        view.set_data(df)
        view.add_overlay("MA20")
        assert "MA20" in view.get_overlays()

    def test_markers_with_data(self, qapp):
        from src.ui.chart_view import ChartView
        view = ChartView()
        df = _make_ohlcv_df(20)
        view.set_data(df)
        view.add_trade_markers([{"index": 3, "price": 10300, "type": "buy"}])
        assert len(view.get_markers()) == 1


# ---------------------------------------------------------------------------
# 2. portfolio_view.py - AllocationChart, ReturnChart
# ---------------------------------------------------------------------------
class TestAllocationChart:
    """AllocationChart 파이 차트 테스트."""

    def test_creation(self, qapp):
        from src.ui.portfolio_view import AllocationChart
        chart = AllocationChart()
        assert chart is not None

    def test_set_data(self, qapp):
        from src.ui.portfolio_view import AllocationChart
        chart = AllocationChart()
        data = [
            {"name": "삼성전자", "weight": 40.0},
            {"name": "SK하이닉스", "weight": 30.0},
            {"name": "현금", "weight": 30.0},
        ]
        chart.set_data(data)
        assert len(chart.get_data()) == 3

    def test_set_data_empty(self, qapp):
        from src.ui.portfolio_view import AllocationChart
        chart = AllocationChart()
        chart.set_data([])
        assert chart.get_data() == []

    def test_is_figure_canvas(self, qapp):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from src.ui.portfolio_view import AllocationChart
        chart = AllocationChart()
        assert isinstance(chart, FigureCanvasQTAgg)


class TestReturnChart:
    """ReturnChart 라인 차트 테스트."""

    def test_creation(self, qapp):
        from src.ui.portfolio_view import ReturnChart
        chart = ReturnChart()
        assert chart is not None

    def test_add_point(self, qapp):
        from src.ui.portfolio_view import ReturnChart
        chart = ReturnChart()
        chart.add_point("2026-01-01", 1.5)
        chart.add_point("2026-01-02", 2.3)
        assert len(chart.get_data()) == 2

    def test_update_chart(self, qapp):
        from src.ui.portfolio_view import ReturnChart
        chart = ReturnChart()
        chart.add_point("2026-01-01", 1.5)
        chart.add_point("2026-01-02", 2.3)
        chart.add_point("2026-01-03", -0.5)
        chart.update_chart()

    def test_update_chart_empty(self, qapp):
        from src.ui.portfolio_view import ReturnChart
        chart = ReturnChart()
        chart.update_chart()

    def test_set_data_and_draw(self, qapp):
        from src.ui.portfolio_view import ReturnChart
        chart = ReturnChart()
        dates = ["2026-01-01", "2026-01-02", "2026-01-03"]
        returns = [0.5, 1.2, -0.3]
        chart.set_data_and_draw(dates, returns)
        assert len(chart.get_data()) == 3

    def test_is_figure_canvas(self, qapp):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from src.ui.portfolio_view import ReturnChart
        chart = ReturnChart()
        assert isinstance(chart, FigureCanvasQTAgg)


# ---------------------------------------------------------------------------
# 3. backtest_view.py - EquityCurveCanvas, BacktestView.run_backtest
# ---------------------------------------------------------------------------
class TestEquityCurveCanvas:
    """EquityCurveCanvas 테스트."""

    def test_creation(self, qapp):
        from src.ui.backtest_view import EquityCurveCanvas
        canvas = EquityCurveCanvas()
        assert canvas is not None

    def test_update_chart(self, qapp):
        from src.ui.backtest_view import EquityCurveCanvas
        canvas = EquityCurveCanvas()
        dates = ["2026-01-01", "2026-01-02", "2026-01-03"]
        values = [10_000_000, 10_100_000, 10_200_000]
        canvas.update_chart(dates, values)

    def test_update_chart_empty(self, qapp):
        from src.ui.backtest_view import EquityCurveCanvas
        canvas = EquityCurveCanvas()
        canvas.update_chart([], [])

    def test_update_chart_with_trades(self, qapp):
        from src.ui.backtest_view import EquityCurveCanvas
        canvas = EquityCurveCanvas()
        dates = ["01-01", "01-02", "01-03", "01-04"]
        values = [10_000_000, 10_050_000, 10_150_000, 10_100_000]
        trades = [
            {"index": 1, "value": 10_050_000, "action": "매수"},
            {"index": 3, "value": 10_100_000, "action": "매도"},
        ]
        canvas.update_chart(dates, values, trades)


class TestBacktestViewEquityCanvas:
    """BacktestView 에퀴티 캔버스 통합 테스트."""

    def test_has_equity_canvas(self, qapp):
        from src.ui.backtest_view import BacktestView, EquityCurveCanvas
        view = BacktestView()
        assert hasattr(view, "equity_canvas")
        assert isinstance(view.equity_canvas, EquityCurveCanvas)

    def test_set_equity_curve_updates_canvas(self, qapp):
        from src.ui.backtest_view import BacktestView
        view = BacktestView()
        dates = ["2026-01-01", "2026-01-02"]
        values = [10_000_000, 10_100_000]
        view.set_equity_curve(dates, values)
        result_dates, result_values = view.get_equity_data()
        assert result_dates == dates
        assert result_values == values

    def test_has_run_backtest_method(self, qapp):
        from src.ui.backtest_view import BacktestView
        view = BacktestView()
        assert hasattr(view, "run_backtest")
        assert callable(view.run_backtest)


# ---------------------------------------------------------------------------
# 4. news_view.py - SentimentTrendChart
# ---------------------------------------------------------------------------
class TestSentimentTrendChart:
    """SentimentTrendChart 테스트."""

    def test_creation(self, qapp):
        from src.ui.news_view import SentimentTrendChart
        chart = SentimentTrendChart()
        assert chart is not None

    def test_is_figure_canvas(self, qapp):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from src.ui.news_view import SentimentTrendChart
        chart = SentimentTrendChart()
        assert isinstance(chart, FigureCanvasQTAgg)

    def test_add_point(self, qapp):
        from src.ui.news_view import SentimentTrendChart
        chart = SentimentTrendChart()
        chart.add_point(datetime(2026, 1, 1, 9, 0), 0.8)
        chart.add_point(datetime(2026, 1, 1, 10, 0), -0.3)
        data = chart.get_data()
        assert len(data) == 2
        assert data[0]["score"] == 0.8

    def test_update_chart(self, qapp):
        from src.ui.news_view import SentimentTrendChart
        chart = SentimentTrendChart()
        chart.add_point(datetime(2026, 1, 1, 9, 0), 0.5)
        chart.add_point(datetime(2026, 1, 1, 10, 0), -0.2)
        chart.add_point(datetime(2026, 1, 1, 11, 0), 0.7)
        chart.update_chart()

    def test_update_chart_empty(self, qapp):
        from src.ui.news_view import SentimentTrendChart
        chart = SentimentTrendChart()
        chart.update_chart()


# ---------------------------------------------------------------------------
# 5. watchlist_view.py - WatchlistView + RealtimeTable 통합
# ---------------------------------------------------------------------------
class TestWatchlistViewRealtimeIntegration:
    """WatchlistView에 RealtimeTable이 통합되었는지 테스트."""

    def test_has_realtime_table(self, qapp):
        from src.ui.watchlist_view import WatchlistView, RealtimeTable
        view = WatchlistView()
        assert hasattr(view, "realtime_table")
        assert isinstance(view.realtime_table, RealtimeTable)

    def test_update_realtime(self, qapp):
        from src.ui.watchlist_view import WatchlistView
        view = WatchlistView()
        view.update_realtime("005930", 72000, 1.5, 1000000, 85.0)
        assert view.realtime_table.get_stock_count() == 1

    def test_update_realtime_multiple(self, qapp):
        from src.ui.watchlist_view import WatchlistView
        view = WatchlistView()
        view.update_realtime("005930", 72000, 1.5, 1000000, 85.0)
        view.update_realtime("000660", 130000, -0.5, 500000, 70.0)
        assert view.realtime_table.get_stock_count() == 2

    def test_update_realtime_same_code(self, qapp):
        from src.ui.watchlist_view import WatchlistView
        view = WatchlistView()
        view.update_realtime("005930", 72000, 1.5, 1000000, 85.0)
        view.update_realtime("005930", 72500, 2.2, 1200000, 87.0)
        assert view.realtime_table.get_stock_count() == 1

    def test_groups_still_work(self, qapp):
        from src.ui.watchlist_view import WatchlistView
        view = WatchlistView()
        view.create_group("관심1")
        view.add_stock("관심1", "005930")
        groups = view.get_groups()
        assert "관심1" in groups
        assert "005930" in groups["관심1"]


class TestRealtimeTable:
    """RealtimeTable 단독 테스트."""

    def test_creation(self, qapp):
        from src.ui.watchlist_view import RealtimeTable
        table = RealtimeTable()
        assert table is not None

    def test_update_stock(self, qapp):
        from src.ui.watchlist_view import RealtimeTable
        table = RealtimeTable()
        table.update_stock("005930", 72000, 1.5, 1000000, 85.0)
        assert table.get_stock_count() == 1

    def test_clear(self, qapp):
        from src.ui.watchlist_view import RealtimeTable
        table = RealtimeTable()
        table.update_stock("005930", 72000, 1.5, 1000000, 85.0)
        table.clear()
        assert table.get_stock_count() == 0


# ---------------------------------------------------------------------------
# 헬퍼 함수
# ---------------------------------------------------------------------------
def _make_ohlcv_df(n: int = 30) -> pd.DataFrame:
    """테스트용 OHLCV DataFrame 생성."""
    import numpy as np
    dates = pd.date_range("2026-01-01", periods=n, freq="B")
    base = 10000
    close = base + np.cumsum(np.random.randn(n) * 100)
    close = np.maximum(close, 1000)
    data = {
        "open": close + np.random.randn(n) * 50,
        "high": close + abs(np.random.randn(n) * 80),
        "low": close - abs(np.random.randn(n) * 80),
        "close": close,
        "volume": np.random.randint(100000, 1000000, n),
    }
    df = pd.DataFrame(data, index=dates)
    df["high"] = df[["open", "high", "close"]].max(axis=1)
    df["low"] = df[["open", "low", "close"]].min(axis=1)
    return df
