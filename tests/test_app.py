"""T012/T016: MainWindow 및 SystemTray 테스트"""
import pytest
from PyQt6.QtWidgets import QMainWindow, QSplitter, QMenuBar, QStatusBar, QSystemTrayIcon
from PyQt6.QtCore import Qt


class TestMainWindow:
    """MainWindow 기본 구조 테스트"""

    def test_mainwindow_is_qmainwindow(self, qapp):
        """MainWindow가 QMainWindow를 상속해야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        assert isinstance(win, QMainWindow)

    def test_has_splitter_with_three_panels(self, qapp):
        """QSplitter에 3개 패널이 있어야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        splitter = win.splitter
        assert isinstance(splitter, QSplitter)
        assert splitter.count() == 3

    def test_left_panel_initial_width(self, qapp):
        """왼쪽 패널 초기 크기 설정이 250px여야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        # offscreen 환경에서는 실제 픽셀 크기가 다를 수 있으므로 내부 설정값 확인
        assert win._left_panel_width == 250

    def test_right_panel_initial_width(self, qapp):
        """오른쪽 패널 초기 크기 설정이 300px여야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        assert win._right_panel_width == 300

    def test_has_menubar(self, qapp):
        """메뉴바가 존재해야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        mb = win.menuBar()
        assert mb is not None
        assert isinstance(mb, QMenuBar)

    def test_menubar_has_required_menus(self, qapp):
        """메뉴바에 파일/보기/도구/도움말 메뉴가 있어야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        mb = win.menuBar()
        titles = [a.text() for a in mb.actions()]
        assert any("파일" in t for t in titles)
        assert any("보기" in t for t in titles)
        assert any("도구" in t for t in titles)
        assert any("도움말" in t for t in titles)

    def test_has_statusbar(self, qapp):
        """상태바가 존재해야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        sb = win.statusBar()
        assert sb is not None
        assert isinstance(sb, QStatusBar)

    def test_toggle_left_panel_hides(self, qapp):
        """toggle_left_panel() 호출 시 왼쪽 패널이 숨겨져야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        win.show()
        initial_sizes = win.splitter.sizes()
        win.toggle_left_panel()
        sizes_after = win.splitter.sizes()
        assert sizes_after[0] == 0

    def test_toggle_left_panel_shows(self, qapp):
        """toggle_left_panel() 두 번 호출 시 패널이 복원되어야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        win.show()
        win.toggle_left_panel()
        win.toggle_left_panel()
        sizes = win.splitter.sizes()
        assert sizes[0] > 0

    def test_toggle_right_panel_hides(self, qapp):
        """toggle_right_panel() 호출 시 오른쪽 패널이 숨겨져야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        win.show()
        win.toggle_right_panel()
        sizes = win.splitter.sizes()
        assert sizes[2] == 0

    def test_toggle_right_panel_shows(self, qapp):
        """toggle_right_panel() 두 번 호출 시 패널이 복원되어야 한다"""
        from src.app import MainWindow
        win = MainWindow()
        win.show()
        win.toggle_right_panel()
        win.toggle_right_panel()
        sizes = win.splitter.sizes()
        assert sizes[2] > 0

    def test_window_title_contains_appname(self, qapp):
        """윈도우 타이틀에 APP_NAME이 포함되어야 한다"""
        from src.app import MainWindow
        from src.utils.constants import APP_NAME
        win = MainWindow()
        assert APP_NAME in win.windowTitle()

    def test_dark_theme_stylesheet_applied(self, qapp):
        """다크 테마 스타일시트가 적용되어야 한다"""
        from src.app import MainWindow
        from src.utils.constants import Colors
        win = MainWindow()
        qss = win.styleSheet()
        assert Colors.BACKGROUND in qss


class TestSystemTray:
    """SystemTray 기본 동작 테스트"""

    def test_system_tray_created(self, qapp):
        """SystemTray 인스턴스가 생성되어야 한다"""
        from src.app import SystemTray
        tray = SystemTray(parent=None)
        assert isinstance(tray, QSystemTrayIcon)

    def test_system_tray_has_context_menu(self, qapp):
        """SystemTray에 컨텍스트 메뉴가 있어야 한다"""
        from src.app import SystemTray
        tray = SystemTray(parent=None)
        menu = tray.contextMenu()
        assert menu is not None

    def test_system_tray_menu_has_quit_action(self, qapp):
        """트레이 메뉴에 종료 액션이 있어야 한다"""
        from src.app import SystemTray
        tray = SystemTray(parent=None)
        menu = tray.contextMenu()
        titles = [a.text() for a in menu.actions()]
        assert any("종료" in t for t in titles)

    def test_system_tray_menu_has_show_action(self, qapp):
        """트레이 메뉴에 창 열기 액션이 있어야 한다"""
        from src.app import SystemTray
        tray = SystemTray(parent=None)
        menu = tray.contextMenu()
        titles = [a.text() for a in menu.actions()]
        assert any("창 열기" in t for t in titles)
