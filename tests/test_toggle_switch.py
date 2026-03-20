"""T028 ToggleSwitch 위젯 테스트"""
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from src.ui.widgets.toggle_switch import ToggleSwitch


class TestToggleSwitchInit:
    """ToggleSwitch 초기화 테스트"""

    def test_default_unchecked(self, qapp):
        w = ToggleSwitch()
        assert w.checked is False

    def test_init_checked_true(self, qapp):
        w = ToggleSwitch(checked=True)
        assert w.checked is True

    def test_has_toggled_signal(self, qapp):
        w = ToggleSwitch()
        assert hasattr(w, "toggled")

    def test_minimum_size(self, qapp):
        w = ToggleSwitch()
        assert w.minimumWidth() >= 50
        assert w.minimumHeight() >= 24


class TestToggleSwitchBehavior:
    """ToggleSwitch 동작 테스트"""

    def test_set_checked_true(self, qapp):
        w = ToggleSwitch()
        w.set_checked(True)
        assert w.checked is True

    def test_set_checked_false(self, qapp):
        w = ToggleSwitch(checked=True)
        w.set_checked(False)
        assert w.checked is False

    def test_mouse_press_toggles(self, qapp):
        w = ToggleSwitch()
        w.show()
        initial = w.checked
        QTest.mouseClick(w, Qt.MouseButton.LeftButton)
        assert w.checked != initial

    def test_toggled_signal_emitted(self, qapp):
        w = ToggleSwitch()
        received = []
        w.toggled.connect(lambda v: received.append(v))
        w.set_checked(True)
        assert received == [True]

    def test_toggled_signal_false(self, qapp):
        w = ToggleSwitch(checked=True)
        received = []
        w.toggled.connect(lambda v: received.append(v))
        w.set_checked(False)
        assert received == [False]

    def test_mouse_click_emits_signal(self, qapp):
        w = ToggleSwitch()
        w.show()
        received = []
        w.toggled.connect(lambda v: received.append(v))
        QTest.mouseClick(w, Qt.MouseButton.LeftButton)
        assert len(received) == 1


class TestToggleSwitchColors:
    """ToggleSwitch 색상 테스트"""

    def test_unchecked_color_blue(self, qapp):
        w = ToggleSwitch()
        assert w.unchecked_color == "#326AFF"

    def test_checked_color_red(self, qapp):
        w = ToggleSwitch()
        assert w.checked_color == "#F04451"
