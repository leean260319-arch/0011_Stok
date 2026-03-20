"""T084 AI 설정 뷰
버전: v1.1
설명: AI 모델 선택, API Key 설정, 연결 테스트 UI
"""

from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors, LLMConfig
from src.utils.logger import get_logger

logger = get_logger("ui.ai_settings")


class AISettingsView(QWidget):
    """AI 설정 뷰 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("AI 설정")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        # --- 모델 설정 그룹 ---
        model_group = QGroupBox("모델 설정")
        model_form = QFormLayout(model_group)

        self._primary_model_combo = QComboBox()
        self._primary_model_combo.addItems([
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "claude-3-5-sonnet",
        ])
        self._primary_model_combo.setCurrentText(LLMConfig.PRIMARY_MODEL)
        model_form.addRow("Primary 모델:", self._primary_model_combo)

        self._fallback_model_combo = QComboBox()
        self._fallback_model_combo.addItems([
            "deepseek-chat",
            "gpt-4o-mini",
            "claude-3-haiku",
        ])
        self._fallback_model_combo.setCurrentText(LLMConfig.FALLBACK_MODEL)
        model_form.addRow("Fallback 모델:", self._fallback_model_combo)

        layout.addWidget(model_group)

        # --- API Key 설정 그룹 ---
        api_group = QGroupBox("API Key")
        api_form = QFormLayout(api_group)

        self._primary_api_key_edit = QLineEdit()
        self._primary_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._primary_api_key_edit.setPlaceholderText("Primary API Key 입력")
        api_form.addRow("Primary Key:", self._primary_api_key_edit)

        self._fallback_api_key_edit = QLineEdit()
        self._fallback_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._fallback_api_key_edit.setPlaceholderText("Fallback API Key 입력")
        api_form.addRow("Fallback Key:", self._fallback_api_key_edit)

        layout.addWidget(api_group)

        # --- 버튼 ---
        btn_layout = QHBoxLayout()

        self._test_button = QPushButton("연결 테스트")
        self._test_button.setStyleSheet(
            f"QPushButton {{ background-color: {Colors.PRIMARY};"
            f" color: {Colors.BACKGROUND}; font-weight: bold;"
            f" border-radius: 4px; padding: 8px 16px; }}"
        )
        self._test_button.clicked.connect(self._on_test_clicked)
        btn_layout.addWidget(self._test_button)

        self._save_button = QPushButton("저장")
        self._save_button.clicked.connect(self._on_save_clicked)
        btn_layout.addWidget(self._save_button)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # --- 상태 표시 ---
        self._status_label = QLabel("")
        self._status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(self._status_label)

        layout.addStretch()

    def set_config(self, config) -> None:
        """ConfigManager 인스턴스를 설정한다."""
        self._config = config
        # 저장된 값 로드
        if config:
            primary_key = config.get("ai.primary_api_key", "")
            fallback_key = config.get("ai.fallback_api_key", "")
            if primary_key:
                self._primary_api_key_edit.setText(primary_key)
            if fallback_key:
                self._fallback_api_key_edit.setText(fallback_key)
            primary_model = config.get("ai.primary_model", LLMConfig.PRIMARY_MODEL)
            fallback_model = config.get("ai.fallback_model", LLMConfig.FALLBACK_MODEL)
            self._primary_model_combo.setCurrentText(primary_model)
            self._fallback_model_combo.setCurrentText(fallback_model)

    def _on_save_clicked(self) -> None:
        """AI 설정을 ConfigManager에 저장한다."""
        if self._config is None:
            QMessageBox.warning(self, "저장 실패", "설정 매니저가 초기화되지 않았습니다.")
            return

        self._config.set("ai.primary_model", self._primary_model_combo.currentText())
        self._config.set("ai.fallback_model", self._fallback_model_combo.currentText())
        self._config.set("ai.primary_api_key", self._primary_api_key_edit.text())
        self._config.set("ai.fallback_api_key", self._fallback_api_key_edit.text())

        from src.utils.constants import CONFIG_PATH
        self._config.save(CONFIG_PATH, self._config.get_all())

        self._status_label.setText("AI 설정 저장 완료")
        self._status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
        QMessageBox.information(self, "저장 완료", "AI 설정이 저장되었습니다.")
        logger.info("AI 설정 저장 완료")

    def _on_test_clicked(self) -> None:
        """AI API 연결 테스트를 수행한다."""
        api_key = self._primary_api_key_edit.text().strip()
        if not api_key:
            QMessageBox.warning(self, "연결 테스트", "Primary API Key를 입력하세요.")
            return

        self._status_label.setText("연결 테스트 중...")
        self._status_label.setStyleSheet(f"color: {Colors.WARNING};")
        self._test_button.setEnabled(False)

        # QTimer로 UI 업데이트 후 테스트 실행
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._run_api_test(api_key))

    def _run_api_test(self, api_key: str) -> None:
        """실제 API 호출 테스트."""
        from openai import OpenAI

        model = self._primary_model_combo.currentText()
        base_url = LLMConfig.PRIMARY_BASE_URL

        client = OpenAI(api_key=api_key, base_url=base_url, timeout=15.0)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
        )
        result = response.choices[0].message.content

        self._status_label.setText(f"연결 성공! 응답: {result[:20]}")
        self._status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
        self._test_button.setEnabled(True)
        QMessageBox.information(self, "연결 성공", f"AI API 연결 테스트 성공\n모델: {model}")
        logger.info("AI API 연결 테스트 성공: model=%s", model)
