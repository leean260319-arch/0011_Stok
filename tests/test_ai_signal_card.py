"""T103 AI 시그널 카드 테스트
버전: v1.0
"""
import pytest

from src.ui.widgets.ai_signal_card import AISignalCard
from src.utils.constants import Colors


class TestAISignalCard:
    """AISignalCard 위젯 테스트."""

    def test_creation(self, qapp):
        """AISignalCard 인스턴스 생성."""
        card = AISignalCard()
        assert card is not None

    def test_set_signal_buy(self, qapp):
        """buy 시그널 설정."""
        card = AISignalCard()
        card.set_signal("buy", 0.85, "상승 추세 강함")
        assert card._signal_type == "buy"
        assert card._confidence == 0.85
        assert card._reasoning == "상승 추세 강함"

    def test_set_signal_sell(self, qapp):
        """sell 시그널 설정."""
        card = AISignalCard()
        card.set_signal("sell", 0.7, "하락 추세")
        assert card._signal_type == "sell"

    def test_set_signal_hold(self, qapp):
        """hold 시그널 설정."""
        card = AISignalCard()
        card.set_signal("hold", 0.5, "횡보 중")
        assert card._signal_type == "hold"

    def test_confidence_range(self, qapp):
        """신뢰도 게이지 값은 0~100 범위 퍼센트로 표시."""
        card = AISignalCard()
        card.set_signal("buy", 0.85, "테스트")
        assert card._gauge.value() == 85

    def test_reasoning_text(self, qapp):
        """근거 텍스트가 표시된다."""
        card = AISignalCard()
        card.set_signal("buy", 0.9, "강한 매수 신호")
        assert "강한 매수 신호" in card._reasoning_label.text()

    def test_signal_type_label(self, qapp):
        """시그널 타입 라벨이 표시된다."""
        card = AISignalCard()
        card.set_signal("buy", 0.8, "테스트")
        label_text = card._signal_label.text().upper()
        assert "BUY" in label_text

    def test_is_qframe(self, qapp):
        """QFrame을 상속한다."""
        from PyQt6.QtWidgets import QFrame
        card = AISignalCard()
        assert isinstance(card, QFrame)
