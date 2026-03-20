"""LeftPanel 네비게이션 패널 테스트"""
import pytest
from PyQt6.QtWidgets import QWidget, QPushButton


class TestLeftPanel:
    """LeftPanel 기본 동작 테스트."""

    def test_is_qwidget(self, qapp):
        """LeftPanel이 QWidget을 상속해야 한다."""
        from src.ui.panels.left_panel import LeftPanel
        panel = LeftPanel()
        assert isinstance(panel, QWidget)

    def test_has_nav_buttons(self, qapp):
        """네비게이션 버튼이 존재해야 한다."""
        from src.ui.panels.left_panel import LeftPanel, NAV_ITEMS
        panel = LeftPanel()
        assert len(panel._buttons) == len(NAV_ITEMS)

    def test_default_selection_is_dashboard(self, qapp):
        """초기 선택 항목이 dashboard여야 한다."""
        from src.ui.panels.left_panel import LeftPanel
        panel = LeftPanel()
        assert panel.current_key == "dashboard"

    def test_select_changes_current_key(self, qapp):
        """select() 호출 시 current_key가 변경되어야 한다."""
        from src.ui.panels.left_panel import LeftPanel
        panel = LeftPanel()
        panel.select("chart")
        assert panel.current_key == "chart"

    def test_select_invalid_key_ignored(self, qapp):
        """존재하지 않는 키로 select() 호출 시 변경되지 않아야 한다."""
        from src.ui.panels.left_panel import LeftPanel
        panel = LeftPanel()
        panel.select("nonexistent")
        assert panel.current_key == "dashboard"

    def test_nav_clicked_signal_emitted(self, qapp):
        """버튼 클릭 시 nav_clicked 시그널이 발행되어야 한다."""
        from src.ui.panels.left_panel import LeftPanel
        panel = LeftPanel()
        received = []
        panel.nav_clicked.connect(lambda k: received.append(k))
        panel._on_nav_clicked("news")
        assert received == ["news"]
        assert panel.current_key == "news"

    def test_all_nav_keys_present(self, qapp):
        """모든 NAV_ITEMS 키가 버튼으로 존재해야 한다."""
        from src.ui.panels.left_panel import LeftPanel, NAV_ITEMS
        panel = LeftPanel()
        for key, _label in NAV_ITEMS:
            assert key in panel._buttons

    def test_button_style_changes_on_selection(self, qapp):
        """선택된 버튼은 다른 스타일을 가져야 한다."""
        from src.ui.panels.left_panel import LeftPanel
        panel = LeftPanel()
        dashboard_style = panel._buttons["dashboard"].styleSheet()
        panel.select("chart")
        chart_style = panel._buttons["chart"].styleSheet()
        dashboard_after = panel._buttons["dashboard"].styleSheet()
        # 선택된 버튼과 비선택 버튼의 스타일이 달라야 함
        assert chart_style != dashboard_after
