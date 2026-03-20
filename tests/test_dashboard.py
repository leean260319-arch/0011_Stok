"""T060-T064 메인 대시보드 뷰 테스트
버전: v1.0
"""
import pytest

from src.ui.dashboard import (
    AccountSummary,
    AutoTradeStatus,
    DailyPnL,
    DashboardView,
    IndexMiniChart,
    SentimentGauge,
)
from src.utils.constants import Colors


class TestAccountSummary:
    """T060 AccountSummary 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = AccountSummary()
        assert w is not None

    def test_set_data(self, qapp):
        """총자산, 수익률, 예수금 설정."""
        w = AccountSummary()
        w.set_data(total_asset=10_000_000, profit_rate=5.3, deposit=2_000_000)
        assert "10,000,000" in w._total_asset_label.text()
        assert "5.3" in w._profit_rate_label.text()
        assert "2,000,000" in w._deposit_label.text()

    def test_initial_labels_exist(self, qapp):
        """QLabel 위젯들이 존재."""
        w = AccountSummary()
        assert w._total_asset_label is not None
        assert w._profit_rate_label is not None
        assert w._deposit_label is not None


class TestDailyPnL:
    """T061 DailyPnL 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = DailyPnL()
        assert w is not None

    def test_set_data(self, qapp):
        """실현/미실현 손익, 수익률 설정."""
        w = DailyPnL()
        w.set_data(realized=500_000, unrealized=-200_000, rate=3.2)
        assert "500,000" in w._realized_label.text()
        assert "200,000" in w._unrealized_label.text()
        assert "3.2" in w._rate_label.text()

    def test_positive_rate_color(self, qapp):
        """양수 수익률에 BULLISH 색상 적용."""
        w = DailyPnL()
        w.set_data(realized=100, unrealized=0, rate=1.5)
        style = w._rate_label.styleSheet()
        assert Colors.BULLISH in style

    def test_negative_rate_color(self, qapp):
        """음수 수익률에 BEARISH 색상 적용."""
        w = DailyPnL()
        w.set_data(realized=-100, unrealized=0, rate=-2.0)
        style = w._rate_label.styleSheet()
        assert Colors.BEARISH in style


class TestAutoTradeStatus:
    """T062 AutoTradeStatus 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = AutoTradeStatus()
        assert w is not None

    def test_set_status(self, qapp):
        """전략명, 체결건수, 실행상태 설정."""
        w = AutoTradeStatus()
        w.set_status(strategy_name="모멘텀", filled_count=15, is_running=True)
        assert "모멘텀" in w._strategy_label.text()
        assert "15" in w._filled_label.text()

    def test_running_indicator(self, qapp):
        """실행 중 상태 표시."""
        w = AutoTradeStatus()
        w.set_status(strategy_name="평균회귀", filled_count=0, is_running=True)
        assert "실행" in w._status_label.text()

    def test_stopped_indicator(self, qapp):
        """중지 상태 표시."""
        w = AutoTradeStatus()
        w.set_status(strategy_name="평균회귀", filled_count=0, is_running=False)
        assert "중지" in w._status_label.text()


class TestSentimentGauge:
    """T063 SentimentGauge 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = SentimentGauge()
        assert w is not None

    def test_set_score_positive(self, qapp):
        """양수 점수 설정 (-100~+100 -> 0~200)."""
        w = SentimentGauge()
        w.set_score(score=50, reasoning="긍정적")
        assert w._progress.value() == 150  # 50 + 100
        assert "긍정적" in w._reasoning_label.text()

    def test_set_score_negative(self, qapp):
        """음수 점수 설정."""
        w = SentimentGauge()
        w.set_score(score=-80, reasoning="부정적")
        assert w._progress.value() == 20  # -80 + 100

    def test_set_score_zero(self, qapp):
        """0점 설정."""
        w = SentimentGauge()
        w.set_score(score=0, reasoning="중립")
        assert w._progress.value() == 100

    def test_progress_range(self, qapp):
        """QProgressBar 범위 0~200."""
        w = SentimentGauge()
        assert w._progress.minimum() == 0
        assert w._progress.maximum() == 200


class TestIndexMiniChart:
    """T064 IndexMiniChart 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = IndexMiniChart()
        assert w is not None

    def test_set_index(self, qapp):
        """지수 정보 설정."""
        w = IndexMiniChart()
        w.set_index(name="KOSPI", price=2650.5, change_rate=1.2)
        assert "KOSPI" in w._name_label.text()
        assert "2650.5" in w._price_label.text()
        assert "1.2" in w._change_label.text()

    def test_negative_change(self, qapp):
        """음수 등락률."""
        w = IndexMiniChart()
        w.set_index(name="KOSDAQ", price=850.0, change_rate=-0.5)
        assert "KOSDAQ" in w._name_label.text()
        assert "-0.5" in w._change_label.text()


class TestDashboardView:
    """DashboardView 통합 테스트."""

    def test_creation(self, qapp):
        """DashboardView 인스턴스 생성."""
        view = DashboardView()
        assert view is not None

    def test_contains_all_widgets(self, qapp):
        """5개 서브 위젯 포함 확인."""
        view = DashboardView()
        assert isinstance(view._account_summary, AccountSummary)
        assert isinstance(view._daily_pnl, DailyPnL)
        assert isinstance(view._auto_trade_status, AutoTradeStatus)
        assert isinstance(view._sentiment_gauge, SentimentGauge)
        assert isinstance(view._index_mini_chart, IndexMiniChart)
