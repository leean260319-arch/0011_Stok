"""MainWindow 통합 테스트 - 뷰 전환, 패널 배치, 설정 다이얼로그"""
import pytest
from PyQt6.QtWidgets import QStackedWidget, QDialog


class TestMainWindowIntegration:
    """MainWindow 뷰 통합 테스트."""

    def test_has_view_stack(self, qapp):
        """center panel에 QStackedWidget이 있어야 한다."""
        from src.app import MainWindow
        win = MainWindow()
        assert isinstance(win.view_stack, QStackedWidget)

    def test_view_stack_has_8_views(self, qapp):
        """QStackedWidget에 8개 뷰가 등록되어야 한다."""
        from src.app import MainWindow
        win = MainWindow()
        assert win.view_stack.count() == 8

    def test_initial_view_is_dashboard(self, qapp):
        """초기 표시 뷰가 대시보드(인덱스 0)여야 한다."""
        from src.app import MainWindow
        win = MainWindow()
        assert win.view_stack.currentIndex() == 0

    def test_switch_view_changes_stack(self, qapp):
        """switch_view()로 뷰를 전환할 수 있어야 한다."""
        from src.app import MainWindow
        win = MainWindow()
        win.switch_view("chart")
        assert win.view_stack.currentIndex() == 1

    def test_switch_view_to_all_views(self, qapp):
        """모든 뷰 키로 전환이 가능해야 한다."""
        from src.app import MainWindow, _VIEW_KEYS
        win = MainWindow()
        for idx, key in enumerate(_VIEW_KEYS):
            win.switch_view(key)
            assert win.view_stack.currentIndex() == idx

    def test_left_panel_is_left_panel_class(self, qapp):
        """왼쪽 패널이 LeftPanel 인스턴스여야 한다."""
        from src.app import MainWindow
        from src.ui.panels.left_panel import LeftPanel
        win = MainWindow()
        assert isinstance(win.left_panel, LeftPanel)

    def test_right_panel_is_right_panel_class(self, qapp):
        """오른쪽 패널이 RightPanel 인스턴스여야 한다."""
        from src.app import MainWindow
        from src.ui.panels.right_panel import RightPanel
        win = MainWindow()
        assert isinstance(win.right_panel, RightPanel)

    def test_nav_click_switches_view(self, qapp):
        """LeftPanel nav_clicked 시그널이 뷰를 전환해야 한다."""
        from src.app import MainWindow
        win = MainWindow()
        win.left_panel.nav_clicked.emit("portfolio")
        assert win.view_stack.currentIndex() == 4

    def test_has_dashboard_view(self, qapp):
        """dashboard_view 속성이 존재해야 한다."""
        from src.app import MainWindow
        from src.ui.dashboard import DashboardView
        win = MainWindow()
        assert isinstance(win.dashboard_view, DashboardView)

    def test_has_chart_view(self, qapp):
        """chart_view 속성이 존재해야 한다."""
        from src.app import MainWindow
        from src.ui.chart_view import ChartView
        win = MainWindow()
        assert isinstance(win.chart_view, ChartView)

    def test_has_backtest_view(self, qapp):
        """backtest_view 속성이 존재해야 한다."""
        from src.app import MainWindow
        from src.ui.backtest_view import BacktestView
        win = MainWindow()
        assert isinstance(win.backtest_view, BacktestView)

    def test_theme_uses_load_dark_theme(self, qapp):
        """테마가 load_dark_theme()으로 적용되어야 한다."""
        from src.app import MainWindow
        from src.ui.themes.dark_theme import load_dark_theme
        win = MainWindow()
        qss = win.styleSheet()
        # load_dark_theme()에만 있는 QGroupBox 스타일 확인
        assert "QGroupBox" in qss

    def test_right_panel_has_kill_switch(self, qapp):
        """오른쪽 패널에 킬스위치가 있어야 한다."""
        from src.app import MainWindow
        from src.ui.widgets.kill_switch import KillSwitchButton
        win = MainWindow()
        assert isinstance(win.right_panel.kill_switch, KillSwitchButton)

    def test_right_panel_has_ai_signal_card(self, qapp):
        """오른쪽 패널에 AI 시그널 카드가 있어야 한다."""
        from src.app import MainWindow
        from src.ui.widgets.ai_signal_card import AISignalCard
        win = MainWindow()
        assert isinstance(win.right_panel.ai_signal_card, AISignalCard)


class TestSettingsDialog:
    """SettingsDialog 테스트."""

    def test_settings_dialog_created(self, qapp):
        """SettingsDialog가 QDialog를 상속해야 한다."""
        from src.app import SettingsDialog
        dlg = SettingsDialog()
        assert isinstance(dlg, QDialog)

    def test_settings_dialog_has_tabs(self, qapp):
        """SettingsDialog에 5개 탭이 있어야 한다."""
        from src.app import SettingsDialog
        dlg = SettingsDialog()
        assert dlg.tab_widget.count() == 5

    def test_settings_dialog_tab_titles(self, qapp):
        """탭 제목이 올바라야 한다."""
        from src.app import SettingsDialog
        dlg = SettingsDialog()
        titles = [dlg.tab_widget.tabText(i) for i in range(dlg.tab_widget.count())]
        assert "계정 설정" in titles
        assert "AI 설정" in titles
        assert "매매 설정" in titles

    def test_settings_dialog_has_settings_view(self, qapp):
        """SettingsDialog에 SettingsView가 있어야 한다."""
        from src.app import SettingsDialog
        from src.ui.settings_view import SettingsView
        dlg = SettingsDialog()
        assert isinstance(dlg.settings_view, SettingsView)

    def test_settings_dialog_has_ai_settings_view(self, qapp):
        """SettingsDialog에 AISettingsView가 있어야 한다."""
        from src.app import SettingsDialog
        from src.ui.ai_settings_view import AISettingsView
        dlg = SettingsDialog()
        assert isinstance(dlg.ai_settings_view, AISettingsView)

    def test_settings_dialog_has_trade_settings_view(self, qapp):
        """SettingsDialog에 TradeSettingsView가 있어야 한다."""
        from src.app import SettingsDialog
        from src.ui.trade_settings_view import TradeSettingsView
        dlg = SettingsDialog()
        assert isinstance(dlg.trade_settings_view, TradeSettingsView)
