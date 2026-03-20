"""T065-T069 차트 분석 뷰 테스트
버전: v1.0
"""
import pytest

from src.ui.chart_view import (
    ChartView,
    SubIndicatorPanel,
    TimeframeSelector,
)


class TestChartView:
    """T065 ChartView 기본 프레임 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = ChartView()
        assert w is not None

    def test_stock_label(self, qapp):
        """종목명 라벨 표시."""
        w = ChartView()
        w.set_stock_name("삼성전자")
        assert "삼성전자" in w._stock_label.text()

    def test_add_overlay(self, qapp):
        """T066 오버레이 추가."""
        w = ChartView()
        w.add_overlay("MA20")
        w.add_overlay("BB")
        overlays = w.get_overlays()
        assert "MA20" in overlays
        assert "BB" in overlays
        assert len(overlays) == 2

    def test_add_duplicate_overlay(self, qapp):
        """중복 오버레이 추가 시 무시."""
        w = ChartView()
        w.add_overlay("MA20")
        w.add_overlay("MA20")
        assert len(w.get_overlays()) == 1

    def test_add_trade_markers(self, qapp):
        """T069 매매 마커 추가."""
        w = ChartView()
        markers = [
            {"time": "2026-01-01", "type": "buy", "price": 50000},
            {"time": "2026-01-02", "type": "sell", "price": 52000},
        ]
        w.add_trade_markers(markers)
        result = w.get_markers()
        assert len(result) == 2
        assert result[0]["type"] == "buy"

    def test_get_markers_empty(self, qapp):
        """마커 없을 때 빈 리스트."""
        w = ChartView()
        assert w.get_markers() == []


class TestSubIndicatorPanel:
    """T067 SubIndicatorPanel 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = SubIndicatorPanel()
        assert w is not None

    def test_default_indicators(self, qapp):
        """RSI/MACD/스토캐스틱 항목 존재."""
        w = SubIndicatorPanel()
        items = [w._combo.itemText(i) for i in range(w._combo.count())]
        assert "RSI" in items
        assert "MACD" in items
        assert "Stochastic" in items

    def test_selected_indicator(self, qapp):
        """선택된 지표명 표시."""
        w = SubIndicatorPanel()
        w._combo.setCurrentText("MACD")
        assert w._combo.currentText() == "MACD"


class TestTimeframeSelector:
    """T068 TimeframeSelector 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = TimeframeSelector()
        assert w is not None

    def test_default_timeframes(self, qapp):
        """1분/5분/15분/일/주/월 버튼 존재."""
        w = TimeframeSelector()
        labels = [btn.text() for btn in w._buttons]
        for tf in ["1분", "5분", "15분", "일", "주", "월"]:
            assert tf in labels

    def test_select_timeframe(self, qapp):
        """타임프레임 선택."""
        w = TimeframeSelector()
        w._on_clicked("5분")
        assert w.selected_timeframe == "5분"

    def test_signal_emitted(self, qapp):
        """timeframe_changed 시그널 발생."""
        w = TimeframeSelector()
        received = []
        w.timeframe_changed.connect(lambda tf: received.append(tf))
        w._on_clicked("일")
        assert received == ["일"]
