"""T075 킬 스위치 UI 테스트
버전: v1.0
"""
import pytest
from PyQt6.QtWidgets import QPushButton

from src.ui.widgets.kill_switch import KillSwitchButton


class TestKillSwitchButton:
    """KillSwitchButton 위젯 테스트."""

    def test_creation(self, qapp):
        """KillSwitchButton 인스턴스 생성."""
        btn = KillSwitchButton()
        assert btn is not None

    def test_is_qpushbutton(self, qapp):
        """QPushButton을 상속한다."""
        btn = KillSwitchButton()
        assert isinstance(btn, QPushButton)

    def test_initial_not_activated(self, qapp):
        """초기 상태는 비활성화."""
        btn = KillSwitchButton()
        assert btn.is_activated() is False

    def test_deactivate(self, qapp):
        """deactivate() 수동 해제."""
        btn = KillSwitchButton()
        btn._activated = True
        btn.deactivate()
        assert btn.is_activated() is False

    def test_has_activated_signal(self, qapp):
        """activated pyqtSignal이 존재한다."""
        btn = KillSwitchButton()
        assert hasattr(btn, "activated")

    def test_long_press_duration(self, qapp):
        """long-press 활성화 시간은 2초."""
        btn = KillSwitchButton()
        assert btn._long_press_ms == 2000
