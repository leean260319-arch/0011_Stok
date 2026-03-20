"""왼쪽 패널 - 네비게이션 메뉴
버전: v1.0
설명: 사이드바 네비게이션 버튼으로 center panel 뷰 전환
"""

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel

from src.utils.constants import Colors

# 네비게이션 항목: (키, 표시명)
NAV_ITEMS = [
    ("dashboard", "대시보드"),
    ("chart", "차트 분석"),
    ("news", "뉴스 분석"),
    ("trade", "자동매매"),
    ("portfolio", "포트폴리오"),
    ("watchlist", "관심종목"),
    ("backtest", "백테스팅"),
    ("alert", "알림센터"),
]


class LeftPanel(QWidget):
    """왼쪽 사이드바 네비게이션 패널.

    Signals:
        nav_clicked(str): 네비게이션 키 클릭 시그널
    """

    nav_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: dict[str, QPushButton] = {}
        self._current_key: str = "dashboard"
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(2)

        title = QLabel("StokAI")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {Colors.PRIMARY};"
            " padding: 8px 4px;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        for key, label in NAV_ITEMS:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._button_style(False))
            btn.clicked.connect(lambda checked, k=key: self._on_nav_clicked(k))
            self._buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # 초기 선택
        self._update_selection("dashboard")

    def _on_nav_clicked(self, key: str) -> None:
        """네비게이션 버튼 클릭 처리."""
        self._update_selection(key)
        self.nav_clicked.emit(key)

    def _update_selection(self, key: str) -> None:
        """선택 상태 UI 갱신."""
        self._current_key = key
        for k, btn in self._buttons.items():
            is_selected = (k == key)
            btn.setChecked(is_selected)
            btn.setStyleSheet(self._button_style(is_selected))

    def select(self, key: str) -> None:
        """프로그래밍 방식으로 네비게이션 선택."""
        if key in self._buttons:
            self._update_selection(key)

    @property
    def current_key(self) -> str:
        """현재 선택된 네비게이션 키."""
        return self._current_key

    @staticmethod
    def _button_style(selected: bool) -> str:
        """버튼 스타일시트를 반환한다."""
        if selected:
            return (
                f"QPushButton {{ background-color: {Colors.PRIMARY};"
                f" color: {Colors.BACKGROUND}; font-weight: bold;"
                f" border: none; border-radius: 4px;"
                f" padding: 10px 12px; text-align: left; }}"
            )
        return (
            f"QPushButton {{ background-color: transparent;"
            f" color: {Colors.TEXT_PRIMARY}; border: none;"
            f" border-radius: 4px; padding: 10px 12px; text-align: left; }}"
            f"QPushButton:hover {{ background-color: {Colors.SURFACE_VARIANT}; }}"
        )
