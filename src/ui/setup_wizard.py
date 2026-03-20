"""T096 최초 실행 설정 마법사
버전: v1.0
설명: 4단계 설정 마법사 (비밀번호, 키움 API, AI, 매매 설정)
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors, RiskDefaults


class SetupWizard(QWidget):
    """최초 실행 설정 마법사 위젯 (4단계)."""

    wizard_completed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._completed = False
        self._setup_ui()

    def current_step(self) -> int:
        """현재 단계 인덱스(0-3)를 반환한다."""
        return self._stack.currentIndex()

    def next_step(self) -> None:
        """다음 단계로 이동한다."""
        idx = self._stack.currentIndex()
        if idx < self._stack.count() - 1:
            self._stack.setCurrentIndex(idx + 1)

    def prev_step(self) -> None:
        """이전 단계로 이동한다."""
        idx = self._stack.currentIndex()
        if idx > 0:
            self._stack.setCurrentIndex(idx - 1)

    def get_step_data(self, step: int) -> dict:
        """각 단계의 입력 데이터를 반환한다."""
        if step == 0:
            return {
                "password": self._pw_input.text(),
                "password_confirm": self._pw_confirm_input.text(),
            }
        if step == 1:
            return {
                "account_number": self._account_number_input.text(),
                "account_password": self._account_password_input.text(),
                "api_key": self._kiwoom_api_key_input.text(),
            }
        if step == 2:
            return {
                "openai_api_key": self._openai_key_input.text(),
                "deepseek_api_key": self._deepseek_key_input.text(),
            }
        if step == 3:
            return {
                "daily_loss_limit": self._daily_loss_spin.value(),
                "max_position": self._max_position_spin.value(),
                "stop_loss": self._stop_loss_spin.value(),
                "take_profit": self._take_profit_spin.value(),
            }
        return {}

    def is_complete(self) -> bool:
        """모든 단계가 완료되었는지 반환한다."""
        return self._completed

    # ---- UI 구성 ----

    def _setup_ui(self) -> None:
        """UI를 초기화한다."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("StokAI 초기 설정")
        title.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._create_step1())
        self._stack.addWidget(self._create_step2())
        self._stack.addWidget(self._create_step3())
        self._stack.addWidget(self._create_step4())
        layout.addWidget(self._stack)

        # 버튼
        btn_layout = QHBoxLayout()

        self._prev_button = QPushButton("이전")
        self._prev_button.clicked.connect(self.prev_step)
        btn_layout.addWidget(self._prev_button)

        btn_layout.addStretch()

        self._next_button = QPushButton("다음")
        self._next_button.clicked.connect(self.next_step)
        btn_layout.addWidget(self._next_button)

        self._complete_button = QPushButton("완료")
        self._complete_button.clicked.connect(self._on_complete)
        btn_layout.addWidget(self._complete_button)

        layout.addLayout(btn_layout)

    def _create_step1(self) -> QWidget:
        """1단계: 앱 비밀번호 설정."""
        widget = QWidget()
        form = QFormLayout(widget)

        group = QGroupBox("앱 비밀번호 설정")
        group_form = QFormLayout(group)

        self._pw_input = QLineEdit()
        self._pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._pw_input.setPlaceholderText("비밀번호 입력")
        group_form.addRow("비밀번호:", self._pw_input)

        self._pw_confirm_input = QLineEdit()
        self._pw_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._pw_confirm_input.setPlaceholderText("비밀번호 확인")
        group_form.addRow("비밀번호 확인:", self._pw_confirm_input)

        form.addRow(group)
        return widget

    def _create_step2(self) -> QWidget:
        """2단계: 키움 API 설정."""
        widget = QWidget()
        form = QFormLayout(widget)

        group = QGroupBox("키움 API 설정")
        group_form = QFormLayout(group)

        self._account_number_input = QLineEdit()
        self._account_number_input.setPlaceholderText("계좌번호")
        group_form.addRow("계좌번호:", self._account_number_input)

        self._account_password_input = QLineEdit()
        self._account_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._account_password_input.setPlaceholderText("계좌 비밀번호")
        group_form.addRow("비밀번호:", self._account_password_input)

        self._kiwoom_api_key_input = QLineEdit()
        self._kiwoom_api_key_input.setPlaceholderText("API Key")
        group_form.addRow("API Key:", self._kiwoom_api_key_input)

        form.addRow(group)
        return widget

    def _create_step3(self) -> QWidget:
        """3단계: AI 설정."""
        widget = QWidget()
        form = QFormLayout(widget)

        group = QGroupBox("AI 설정")
        group_form = QFormLayout(group)

        self._openai_key_input = QLineEdit()
        self._openai_key_input.setPlaceholderText("OpenAI API Key")
        group_form.addRow("OpenAI API Key:", self._openai_key_input)

        self._deepseek_key_input = QLineEdit()
        self._deepseek_key_input.setPlaceholderText("DeepSeek API Key")
        group_form.addRow("DeepSeek API Key:", self._deepseek_key_input)

        form.addRow(group)
        return widget

    def _create_step4(self) -> QWidget:
        """4단계: 매매 설정."""
        widget = QWidget()
        form = QFormLayout(widget)

        group = QGroupBox("매매 설정")
        group_form = QFormLayout(group)

        self._daily_loss_spin = self._make_spin(
            RiskDefaults.DAILY_LOSS_LIMIT_PCT, 0.0, 100.0
        )
        group_form.addRow("일일 손실 한도 (%):", self._daily_loss_spin)

        self._max_position_spin = self._make_spin(
            RiskDefaults.MAX_POSITION_PCT, 0.0, 100.0
        )
        group_form.addRow("최대 포지션 (%):", self._max_position_spin)

        self._stop_loss_spin = self._make_spin(
            RiskDefaults.STOP_LOSS_PCT, 0.0, 100.0
        )
        group_form.addRow("손절 (%):", self._stop_loss_spin)

        self._take_profit_spin = self._make_spin(
            RiskDefaults.TAKE_PROFIT_PCT, 0.0, 100.0
        )
        group_form.addRow("이익 실현 (%):", self._take_profit_spin)

        form.addRow(group)
        return widget

    def _on_complete(self) -> None:
        """완료 버튼 클릭 처리."""
        self._completed = True
        self.wizard_completed.emit()

    @staticmethod
    def _make_spin(default: float, min_val: float, max_val: float) -> QDoubleSpinBox:
        """QDoubleSpinBox를 생성한다."""
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setSingleStep(0.5)
        spin.setDecimals(1)
        spin.setSuffix(" %")
        return spin
