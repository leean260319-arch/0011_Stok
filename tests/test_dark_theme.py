"""T101 다크 테마 QSS 테스트
버전: v1.0
"""
from src.ui.themes.dark_theme import load_dark_theme
from src.utils.constants import Colors


class TestLoadDarkTheme:
    """load_dark_theme() 함수 테스트."""

    def test_returns_string(self):
        """QSS 문자열을 반환한다."""
        qss = load_dark_theme()
        assert isinstance(qss, str)
        assert len(qss) > 0

    def test_contains_qmainwindow(self):
        """QMainWindow 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QMainWindow" in qss

    def test_contains_qwidget(self):
        """QWidget 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QWidget" in qss

    def test_contains_qmenubar(self):
        """QMenuBar 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QMenuBar" in qss

    def test_contains_qmenu(self):
        """QMenu 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QMenu" in qss

    def test_contains_qstatusbar(self):
        """QStatusBar 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QStatusBar" in qss

    def test_contains_qsplitter(self):
        """QSplitter 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QSplitter" in qss

    def test_contains_qgroupbox(self):
        """QGroupBox 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QGroupBox" in qss

    def test_contains_qpushbutton(self):
        """QPushButton 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QPushButton" in qss

    def test_contains_qlineedit(self):
        """QLineEdit 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QLineEdit" in qss

    def test_contains_qcombobox(self):
        """QComboBox 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QComboBox" in qss

    def test_contains_qtablewidget(self):
        """QTableWidget 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QTableWidget" in qss

    def test_contains_qscrollbar(self):
        """QScrollBar 스타일이 포함된다."""
        qss = load_dark_theme()
        assert "QScrollBar" in qss

    def test_uses_colors_constants(self):
        """Colors 상수 값들이 QSS에 포함된다."""
        qss = load_dark_theme()
        assert Colors.BACKGROUND in qss
        assert Colors.SURFACE in qss
        assert Colors.PRIMARY in qss
        assert Colors.TEXT_PRIMARY in qss
        assert Colors.TEXT_SECONDARY in qss
        assert Colors.BORDER in qss
