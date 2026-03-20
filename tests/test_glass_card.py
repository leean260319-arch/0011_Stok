"""T102 글래스모피즘 카드 테스트
버전: v1.0
"""
import pytest
from PyQt6.QtWidgets import QLabel

from src.ui.widgets.glass_card import GlassCard


class TestGlassCard:
    """GlassCard 위젯 테스트."""

    def test_creation(self, qapp):
        """GlassCard 인스턴스 생성."""
        card = GlassCard()
        assert card is not None

    def test_set_title(self, qapp):
        """setTitle로 타이틀 설정."""
        card = GlassCard()
        card.setTitle("테스트 제목")
        assert card._title_label.text() == "테스트 제목"

    def test_set_content(self, qapp):
        """setContent로 콘텐츠 위젯 설정."""
        card = GlassCard()
        content = QLabel("콘텐츠")
        card.setContent(content)
        assert card._content_widget is content

    def test_default_title_empty(self, qapp):
        """기본 타이틀은 빈 문자열."""
        card = GlassCard()
        assert card._title_label.text() == ""

    def test_replace_content(self, qapp):
        """콘텐츠를 교체하면 이전 콘텐츠는 제거된다."""
        card = GlassCard()
        first = QLabel("첫번째")
        second = QLabel("두번째")
        card.setContent(first)
        card.setContent(second)
        assert card._content_widget is second

    def test_is_qframe(self, qapp):
        """QFrame을 상속한다."""
        from PyQt6.QtWidgets import QFrame
        card = GlassCard()
        assert isinstance(card, QFrame)
