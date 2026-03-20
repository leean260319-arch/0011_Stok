"""T085 매매 설정 뷰
버전: v1.1
설명: 일일 손실 한도, 최대 포지션, 손절, 이익 실현 설정 UI
"""

from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors, RiskDefaults
from src.utils.logger import get_logger

logger = get_logger("ui.trade_settings")


class TradeSettingsView(QWidget):
    """매매 설정 뷰 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config = None
        self._risk_manager = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("매매 설정")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        # --- 리스크 관리 그룹 ---
        risk_group = QGroupBox("리스크 관리")
        risk_form = QFormLayout(risk_group)

        self._daily_loss_spin = self._make_spin(
            RiskDefaults.DAILY_LOSS_LIMIT_PCT, 0.0, 100.0
        )
        risk_form.addRow("일일 손실 한도 (%):", self._daily_loss_spin)

        self._max_position_spin = self._make_spin(
            RiskDefaults.MAX_POSITION_PCT, 0.0, 100.0
        )
        risk_form.addRow("최대 포지션 (%):", self._max_position_spin)

        self._stop_loss_spin = self._make_spin(
            RiskDefaults.STOP_LOSS_PCT, 0.0, 100.0
        )
        risk_form.addRow("손절 (%):", self._stop_loss_spin)

        self._take_profit_spin = self._make_spin(
            RiskDefaults.TAKE_PROFIT_PCT, 0.0, 100.0
        )
        risk_form.addRow("이익 실현 (%):", self._take_profit_spin)

        layout.addWidget(risk_group)

        # --- 버튼 ---
        btn_layout = QHBoxLayout()

        self._save_button = QPushButton("저장")
        self._save_button.setStyleSheet(
            f"QPushButton {{ background-color: {Colors.PRIMARY};"
            f" color: {Colors.BACKGROUND}; font-weight: bold;"
            f" border-radius: 4px; padding: 8px 16px; }}"
        )
        self._save_button.clicked.connect(self._on_save_clicked)
        btn_layout.addWidget(self._save_button)

        self._load_button = QPushButton("불러오기")
        self._load_button.clicked.connect(self._on_load_clicked)
        btn_layout.addWidget(self._load_button)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

    def set_config(self, config) -> None:
        """ConfigManager 인스턴스를 설정한다."""
        self._config = config
        self._load_from_config()

    def set_risk_manager(self, risk_manager) -> None:
        """RiskManager 인스턴스를 설정한다."""
        self._risk_manager = risk_manager

    def _load_from_config(self) -> None:
        """ConfigManager에서 설정값을 로드한다."""
        if self._config is None:
            return
        self._daily_loss_spin.setValue(
            self._config.get("risk.daily_loss_limit_pct", RiskDefaults.DAILY_LOSS_LIMIT_PCT)
        )
        self._max_position_spin.setValue(
            self._config.get("risk.max_position_pct", RiskDefaults.MAX_POSITION_PCT)
        )
        self._stop_loss_spin.setValue(
            self._config.get("risk.stop_loss_pct", RiskDefaults.STOP_LOSS_PCT)
        )
        self._take_profit_spin.setValue(
            self._config.get("risk.take_profit_pct", RiskDefaults.TAKE_PROFIT_PCT)
        )

    def _on_save_clicked(self) -> None:
        """매매 설정을 저장한다."""
        if self._config is None:
            QMessageBox.warning(self, "저장 실패", "설정 매니저가 초기화되지 않았습니다.")
            return

        self._config.set("risk.daily_loss_limit_pct", self._daily_loss_spin.value())
        self._config.set("risk.max_position_pct", self._max_position_spin.value())
        self._config.set("risk.stop_loss_pct", self._stop_loss_spin.value())
        self._config.set("risk.take_profit_pct", self._take_profit_spin.value())

        from src.utils.constants import CONFIG_PATH
        self._config.save(CONFIG_PATH, self._config.get_all())

        # RiskManager 클래스 변수에 즉시 반영
        if self._risk_manager:
            self._risk_manager.DAILY_LOSS_LIMIT = self._daily_loss_spin.value()
            self._risk_manager.CONCENTRATION_LIMIT = self._max_position_spin.value() / 100.0

        QMessageBox.information(self, "저장 완료", "매매 설정이 저장되었습니다.")
        logger.info("매매 설정 저장 완료")

    def _on_load_clicked(self) -> None:
        """저장된 설정을 다시 불러온다."""
        self._load_from_config()
        QMessageBox.information(self, "불러오기", "저장된 매매 설정을 불러왔습니다.")

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
