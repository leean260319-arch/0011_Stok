"""오른쪽 패널 - 킬스위치, AI 시그널, AI 상태, 자동매매 제어
버전: v1.1
설명: 킬스위치, AI 시그널 카드, AI 상태, 자동매매 시작/중지 + 종목 입력
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.ui.widgets.ai_signal_card import AISignalCard
from src.ui.widgets.ai_status_indicator import AIStatusIndicator
from src.ui.widgets.kill_switch import KillSwitchButton
from src.utils.constants import Colors


class RightPanel(QWidget):
    """오른쪽 사이드바 패널 - 킬스위치, AI 시그널, AI 상태, 자동매매 제어."""

    autotrade_requested = pyqtSignal(bool)  # True=시작, False=중지
    stocks_changed = pyqtSignal(list)       # 종목 코드 리스트

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        # 킬스위치
        kill_label = QLabel("긴급 정지")
        kill_label.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {Colors.DANGER};"
        )
        kill_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(kill_label)

        self.kill_switch = KillSwitchButton()
        kill_container = QWidget()
        kill_layout = QVBoxLayout(kill_container)
        kill_layout.setContentsMargins(0, 0, 0, 0)
        kill_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        kill_layout.addWidget(self.kill_switch)
        layout.addWidget(kill_container)

        # AI 상태 인디케이터
        self.ai_status = AIStatusIndicator()
        layout.addWidget(self.ai_status)

        # AI 시그널 카드
        signal_label = QLabel("AI 매매 시그널")
        signal_label.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(signal_label)

        self.ai_signal_card = AISignalCard()
        layout.addWidget(self.ai_signal_card)

        # 자동매매 제어
        trade_label = QLabel("자동매매")
        trade_label.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(trade_label)

        # 감시 종목 (기본: KOSPI 주요 종목)
        stock_hint = QLabel("감시 종목 (자동 선정, 수정 가능)")
        stock_hint.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(stock_hint)

        self.stock_input = QLineEdit()
        # 기본 KOSPI 주요 종목 (삼성전자, SK하이닉스, LG에너지솔루션, 삼성바이오, 현대차)
        self.stock_input.setText("005930, 000660, 373220, 207940, 005380")
        layout.addWidget(self.stock_input)

        # 시작/중지 버튼
        self.btn_autotrade = QPushButton("자동매매 시작")
        self.btn_autotrade.setStyleSheet(
            f"QPushButton {{ background-color: {Colors.SUCCESS}; color: #000000;"
            f" font-weight: bold; border-radius: 4px; padding: 10px; font-size: 14px; }}"
        )
        self.btn_autotrade.clicked.connect(self._on_toggle_autotrade)
        layout.addWidget(self.btn_autotrade)

        layout.addStretch()

    def _on_apply_stocks(self) -> None:
        """입력된 종목 코드를 파싱하여 시그널로 전달한다."""
        text = self.stock_input.text().strip()
        if not text:
            return
        codes = [c.strip() for c in text.split(",") if c.strip()]
        self.stocks_changed.emit(codes)

    def _on_toggle_autotrade(self) -> None:
        """자동매매 시작/중지 토글."""
        self._is_running = not self._is_running
        self.autotrade_requested.emit(self._is_running)
        self._update_button_style()

    def _update_button_style(self) -> None:
        """버튼 상태에 따라 스타일 변경."""
        if self._is_running:
            self.btn_autotrade.setText("자동매매 중지")
            self.btn_autotrade.setStyleSheet(
                f"QPushButton {{ background-color: {Colors.DANGER}; color: #FFFFFF;"
                f" font-weight: bold; border-radius: 4px; padding: 10px; font-size: 14px; }}"
            )
        else:
            self.btn_autotrade.setText("자동매매 시작")
            self.btn_autotrade.setStyleSheet(
                f"QPushButton {{ background-color: {Colors.SUCCESS}; color: #000000;"
                f" font-weight: bold; border-radius: 4px; padding: 10px; font-size: 14px; }}"
            )

    def set_autotrade_running(self, running: bool) -> None:
        """외부에서 자동매매 상태를 반영한다."""
        self._is_running = running
        self._update_button_style()
