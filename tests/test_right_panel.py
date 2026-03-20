"""RightPanel 테스트"""
import pytest
from PyQt6.QtWidgets import QWidget


class TestRightPanel:
    """RightPanel 기본 동작 테스트."""

    def test_is_qwidget(self, qapp):
        """RightPanel이 QWidget을 상속해야 한다."""
        from src.ui.panels.right_panel import RightPanel
        panel = RightPanel()
        assert isinstance(panel, QWidget)

    def test_has_kill_switch(self, qapp):
        """킬스위치 버튼이 존재해야 한다."""
        from src.ui.panels.right_panel import RightPanel
        from src.ui.widgets.kill_switch import KillSwitchButton
        panel = RightPanel()
        assert isinstance(panel.kill_switch, KillSwitchButton)

    def test_has_ai_signal_card(self, qapp):
        """AI 시그널 카드가 존재해야 한다."""
        from src.ui.panels.right_panel import RightPanel
        from src.ui.widgets.ai_signal_card import AISignalCard
        panel = RightPanel()
        assert isinstance(panel.ai_signal_card, AISignalCard)

    def test_has_ai_status_indicator(self, qapp):
        """AI 상태 인디케이터가 존재해야 한다."""
        from src.ui.panels.right_panel import RightPanel
        from src.ui.widgets.ai_status_indicator import AIStatusIndicator
        panel = RightPanel()
        assert isinstance(panel.ai_status, AIStatusIndicator)

    def test_kill_switch_not_activated_initially(self, qapp):
        """킬스위치가 초기에 비활성 상태여야 한다."""
        from src.ui.panels.right_panel import RightPanel
        panel = RightPanel()
        assert not panel.kill_switch.is_activated()
