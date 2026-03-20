"""웹 대시보드 설정 페이지
버전: v1.1
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors
from src.utils.logger import get_logger

logger = get_logger("ui.web_settings")


class WebSettingsView(QWidget):
    """웹 대시보드 설정 페이지."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config = None
        self._setup_ui()

    def set_config(self, config) -> None:
        """ConfigManager 인스턴스를 설정하고 UI에 반영한다."""
        self._config = config
        self._load_from_config()

    def _setup_ui(self) -> None:
        """UI를 구성한다."""
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        root.addWidget(self._build_server_group())
        root.addWidget(self._build_credential_group())
        root.addWidget(self._build_info_group())
        root.addStretch()

    # ------------------------------------------------------------------
    # 서버 설정 그룹
    # ------------------------------------------------------------------
    def _build_server_group(self) -> QGroupBox:
        """서버 활성화, 포트 설정 그룹."""
        box = QGroupBox("웹 대시보드 서버")
        form = QFormLayout(box)

        self.enabled_check = QCheckBox("웹 대시보드 활성화")
        self.enabled_check.setChecked(True)
        form.addRow(self.enabled_check)

        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setValue(8080)
        form.addRow("포트 번호", self.port_spin)

        return box

    # ------------------------------------------------------------------
    # 인증 정보 그룹
    # ------------------------------------------------------------------
    def _build_credential_group(self) -> QGroupBox:
        """아이디/비밀번호 설정 그룹."""
        box = QGroupBox("인증 정보")
        form = QFormLayout(box)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("아이디")
        self.username_edit.setText("admin")
        form.addRow("아이디", self.username_edit)

        # 비밀번호 입력
        pw_row = QHBoxLayout()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("새 비밀번호 (변경 시에만 입력)")
        pw_row.addWidget(self.password_edit)
        self._pw_eye_btn = QToolButton()
        self._pw_eye_btn.setText("보기")
        self._pw_eye_btn.setCheckable(True)
        self._pw_eye_btn.toggled.connect(self._toggle_password_visibility)
        pw_row.addWidget(self._pw_eye_btn)
        form.addRow("비밀번호", pw_row)

        # 현재 인증 정보 확인
        form.addRow(QLabel("--- 현재 인증 정보 확인 ---"))

        self.current_username_label = QLabel("")
        form.addRow("현재 아이디", self.current_username_label)

        cur_pw_row = QHBoxLayout()
        self.current_password_label = QLabel("********")
        cur_pw_row.addWidget(self.current_password_label)
        self._cur_pw_eye_btn = QToolButton()
        self._cur_pw_eye_btn.setText("보기")
        self._cur_pw_eye_btn.setCheckable(True)
        self._cur_pw_eye_btn.toggled.connect(self._toggle_current_pw_visibility)
        cur_pw_row.addWidget(self._cur_pw_eye_btn)
        form.addRow("현재 비밀번호", cur_pw_row)

        # 저장 버튼
        btn_save = QPushButton("저장")
        btn_save.clicked.connect(self.save_settings)
        form.addRow(btn_save)

        return box

    # ------------------------------------------------------------------
    # 정보 표시 그룹
    # ------------------------------------------------------------------
    def _build_info_group(self) -> QGroupBox:
        """접속 URL, 접속자 수 표시 그룹."""
        box = QGroupBox("서버 정보")
        form = QFormLayout(box)

        ip = self.get_local_ip()
        port = self.port_spin.value()
        self.url_label = QLabel(f"http://{ip}:{port}")
        self.url_label.setStyleSheet(f"color: {Colors.PRIMARY}; font-weight: bold;")
        # 마우스로 텍스트 선택/복사 허용
        self.url_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        # URL 라벨과 복사 버튼을 가로로 배치
        url_row = QHBoxLayout()
        url_row.addWidget(self.url_label)
        self._copy_btn = QPushButton("복사")
        self._copy_btn.setFixedWidth(60)
        self._copy_btn.clicked.connect(self._copy_url)
        url_row.addWidget(self._copy_btn)
        url_row.addStretch()
        form.addRow("접속 URL", url_row)

        self.port_spin.valueChanged.connect(self._update_url_label)

        self.connection_count_label = QLabel("0")
        form.addRow("현재 접속자 수", self.connection_count_label)

        return box

    def _update_url_label(self) -> None:
        """포트 변경 시 URL 라벨을 갱신한다."""
        ip = self.get_local_ip()
        port = self.port_spin.value()
        self.url_label.setText(f"http://{ip}:{port}")

    def _copy_url(self) -> None:
        """접속 URL을 클립보드에 복사한다."""
        QApplication.clipboard().setText(self.url_label.text())
        self._copy_btn.setText("복사됨")
        # 2초 후 버튼 텍스트 복원 (QTimer 사용)
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self._copy_btn.setText("복사"))

    def _toggle_password_visibility(self, checked: bool) -> None:
        """비밀번호 입력 필드 표시/숨기기."""
        if checked:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self._pw_eye_btn.setText("숨기기")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self._pw_eye_btn.setText("보기")

    def _toggle_current_pw_visibility(self, checked: bool) -> None:
        """현재 비밀번호 라벨 표시/숨기기."""
        if checked:
            stored = ""
            if self._config:
                stored = self._config.get("web_dashboard.password", "")
            self.current_password_label.setText(stored if stored else "(미설정)")
            self._cur_pw_eye_btn.setText("숨기기")
        else:
            self.current_password_label.setText("********")
            self._cur_pw_eye_btn.setText("보기")

    def get_local_ip(self) -> str:
        """로컬 네트워크 IP를 반환한다."""
        from src.utils.constants import get_local_ip
        return get_local_ip()

    def save_settings(self) -> None:
        """설정을 ConfigManager에 저장한다."""
        if self._config is None:
            QMessageBox.warning(self, "저장 실패", "설정 매니저가 초기화되지 않았습니다.")
            return

        from src.utils.constants import CONFIG_PATH

        self._config.set("web_dashboard.enabled", self.enabled_check.isChecked())
        self._config.set("web_dashboard.port", self.port_spin.value())
        self._config.set("web_dashboard.username", self.username_edit.text())
        if self.password_edit.text():
            self._config.set("web_dashboard.password", self.password_edit.text())
        self._config.save(CONFIG_PATH, self._config.get_all())

        # 현재 인증 정보 라벨 갱신
        self.current_username_label.setText(self.username_edit.text())

        QMessageBox.information(self, "저장 완료", "웹 대시보드 설정이 저장되었습니다.")
        logger.info("웹 대시보드 설정 저장 완료")

    def _load_from_config(self) -> None:
        """ConfigManager에서 설정을 읽어 UI에 반영한다."""
        if self._config is None:
            return
        self.enabled_check.setChecked(self._config.get("web_dashboard.enabled", True))
        self.port_spin.setValue(self._config.get("web_dashboard.port", 8080))
        self.username_edit.setText(self._config.get("web_dashboard.username", "admin"))
        self.current_username_label.setText(self._config.get("web_dashboard.username", "admin"))

    def load_settings(self) -> None:
        """외부에서 호출 가능한 설정 로드."""
        self._load_from_config()

    def update_connection_count(self, count: int) -> None:
        """접속자 수 라벨을 갱신한다."""
        self.connection_count_label.setText(str(count))
