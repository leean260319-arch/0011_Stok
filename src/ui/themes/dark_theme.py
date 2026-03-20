"""T101 다크 테마 QSS 모듈
버전: v1.1
설명: Colors 상수를 사용하여 다크 테마 QSS 문자열을 생성
변경: v1.1 - font_size 파라미터 추가 (폰트 크기 동적 적용)
"""

from src.utils.constants import Colors


def load_dark_theme(font_size: int = 12) -> str:
    """다크 테마 QSS 문자열을 반환한다."""
    return f"""
/* === 기본 위젯 === */
QMainWindow {{
    background-color: {Colors.BACKGROUND};
    color: {Colors.TEXT_PRIMARY};
}}
QWidget {{
    background-color: {Colors.BACKGROUND};
    color: {Colors.TEXT_PRIMARY};
    font-family: "Malgun Gothic", sans-serif;
    font-size: {font_size}px;
}}

/* === 메뉴바 === */
QMenuBar {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border-bottom: 1px solid {Colors.BORDER};
}}
QMenuBar::item:selected {{
    background-color: {Colors.SURFACE_VARIANT};
}}
QMenu {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
}}
QMenu::item:selected {{
    background-color: {Colors.SURFACE_VARIANT};
}}

/* === 상태바 === */
QStatusBar {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_SECONDARY};
    border-top: 1px solid {Colors.BORDER};
}}

/* === 스플리터 === */
QSplitter::handle {{
    background-color: {Colors.BORDER};
    width: 2px;
}}

/* === 그룹박스 === */
QGroupBox {{
    background-color: {Colors.SURFACE};
    border: 1px solid {Colors.BORDER};
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
    color: {Colors.TEXT_PRIMARY};
    font-weight: bold;
    font-size: {font_size + 1}px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: {Colors.PRIMARY};
}}

/* === 버튼 === */
QPushButton {{
    background-color: {Colors.SURFACE_VARIANT};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    border-radius: 4px;
    padding: 6px 16px;
    min-height: {font_size * 2}px;
}}
QPushButton:hover {{
    background-color: {Colors.BORDER};
}}
QPushButton:pressed {{
    background-color: {Colors.PRIMARY};
    color: {Colors.BACKGROUND};
}}

/* === 텍스트 입력 === */
QLineEdit {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: {Colors.PRIMARY};
    selection-color: {Colors.BACKGROUND};
}}
QLineEdit:focus {{
    border: 1px solid {Colors.PRIMARY};
}}

/* === 콤보박스 === */
QComboBox {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    border-radius: 4px;
    padding: 4px 8px;
}}
QComboBox:hover {{
    border: 1px solid {Colors.PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    selection-background-color: {Colors.SURFACE_VARIANT};
}}

/* === 테이블 === */
QTableWidget {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    gridline-color: {Colors.BORDER};
    selection-background-color: {Colors.SURFACE_VARIANT};
}}
QTableWidget::item {{
    padding: 4px;
}}
QHeaderView::section {{
    background-color: {Colors.SURFACE_VARIANT};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    padding: 4px;
    font-weight: bold;
    font-size: {font_size}px;
}}

/* === 스크롤바 === */
QScrollBar:vertical {{
    background-color: {Colors.BACKGROUND};
    width: 10px;
    border: none;
}}
QScrollBar::handle:vertical {{
    background-color: {Colors.BORDER};
    border-radius: 5px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {Colors.TEXT_SECONDARY};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background-color: {Colors.BACKGROUND};
    height: 10px;
    border: none;
}}
QScrollBar::handle:horizontal {{
    background-color: {Colors.BORDER};
    border-radius: 5px;
    min-width: 20px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {Colors.TEXT_SECONDARY};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""
