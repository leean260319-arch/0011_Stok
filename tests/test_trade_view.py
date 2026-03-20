"""T073-T074, T076 자동매매 관리 뷰 테스트
버전: v1.0
"""
import pytest

from src.ui.trade_view import StrategyList, TradeLog, LossLimitBar


class TestStrategyList:
    """T073 StrategyList 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = StrategyList()
        assert w is not None

    def test_add_strategy(self, qapp):
        """전략 추가."""
        w = StrategyList()
        w.add_strategy("모멘텀", is_active=True)
        w.add_strategy("평균회귀", is_active=False)
        assert w._list_widget.count() == 2

    def test_get_active_strategies(self, qapp):
        """활성 전략 목록."""
        w = StrategyList()
        w.add_strategy("모멘텀", is_active=True)
        w.add_strategy("평균회귀", is_active=False)
        w.add_strategy("AI복합", is_active=True)
        active = w.get_active_strategies()
        assert "모멘텀" in active
        assert "AI복합" in active
        assert "평균회귀" not in active

    def test_toggle_strategy(self, qapp):
        """전략 활성/비활성 토글."""
        w = StrategyList()
        w.add_strategy("모멘텀", is_active=True)
        w.toggle_strategy("모멘텀")
        assert "모멘텀" not in w.get_active_strategies()
        w.toggle_strategy("모멘텀")
        assert "모멘텀" in w.get_active_strategies()

    def test_toggle_nonexistent(self, qapp):
        """존재하지 않는 전략 토글 시 무시."""
        w = StrategyList()
        w.toggle_strategy("없는전략")  # 에러 없이 통과


class TestTradeLog:
    """T074 TradeLog 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = TradeLog()
        assert w is not None

    def test_columns(self, qapp):
        """5개 컬럼 확인 (시간/유형/종목/가격/수량)."""
        w = TradeLog()
        assert w._table.columnCount() == 5

    def test_add_log(self, qapp):
        """거래 로그 추가."""
        w = TradeLog()
        w.add_log("09:01:00", "매수", "삼성전자", 70000, 10)
        assert w._table.rowCount() == 1

    def test_add_multiple_logs(self, qapp):
        """여러 로그 추가."""
        w = TradeLog()
        w.add_log("09:01:00", "매수", "삼성전자", 70000, 10)
        w.add_log("09:05:00", "매도", "SK하이닉스", 150000, 5)
        assert w._table.rowCount() == 2

    def test_log_content(self, qapp):
        """로그 내용 확인."""
        w = TradeLog()
        w.add_log("09:01:00", "매수", "삼성전자", 70000, 10)
        assert w._table.item(0, 0).text() == "09:01:00"
        assert w._table.item(0, 1).text() == "매수"
        assert w._table.item(0, 2).text() == "삼성전자"


class TestLossLimitBar:
    """T076 LossLimitBar 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = LossLimitBar()
        assert w is not None

    def test_set_limit(self, qapp):
        """손실 한도 설정."""
        w = LossLimitBar()
        w.set_limit(current_loss=150_000, max_limit=500_000)
        assert w._progress.value() == 30  # 150000/500000 * 100

    def test_set_limit_zero(self, qapp):
        """최대 한도 0일 때."""
        w = LossLimitBar()
        w.set_limit(current_loss=0, max_limit=0)
        assert w._progress.value() == 0

    def test_set_limit_full(self, qapp):
        """한도 100% 도달."""
        w = LossLimitBar()
        w.set_limit(current_loss=500_000, max_limit=500_000)
        assert w._progress.value() == 100
