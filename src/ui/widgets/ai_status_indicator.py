"""T104 AI 상태 표시 위젯
버전: v1.0
설명: AI 처리 상태(idle/processing/complete/error)를 표시
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget

from src.utils.constants import Colors

_STATUS_CONFIG = {
    "idle": {"text": "AI 대기", "color": Colors.TEXT_SECONDARY},
    "processing": {"text": "AI 분석 중...", "color": Colors.PRIMARY},
    "complete": {"text": "AI 분석 완료", "color": Colors.SUCCESS},
    "error": {"text": "AI 오류", "color": Colors.DANGER},
}


class AIStatusIndicator(QWidget):
    """AI 처리 상태 표시 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._status: str = "idle"
        self._setup_ui()
        self.set_status("idle")

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(8)

        self._status_label = QLabel("")
        self._status_label.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;"
        )
        layout.addWidget(self._status_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedWidth(80)
        self._progress_bar.setFixedHeight(12)
        self._progress_bar.setRange(0, 0)  # indeterminate
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setStyleSheet(
            f"QProgressBar {{ background-color: {Colors.SURFACE_VARIANT};"
            f"  border-radius: 6px; border: none; }}"
            f"QProgressBar::chunk {{ background-color: {Colors.PRIMARY};"
            f"  border-radius: 6px; }}"
        )
        self._progress_bar.hide()
        layout.addWidget(self._progress_bar)

    def set_status(self, status: str) -> None:
        """상태를 설정한다.

        Args:
            status: "idle", "processing", "complete", "error"
        """
        self._status = status
        cfg = _STATUS_CONFIG.get(status, _STATUS_CONFIG["idle"])

        self._status_label.setText(cfg["text"])
        self._status_label.setStyleSheet(
            f"color: {cfg['color']}; font-size: 12px;"
        )

        if status == "processing":
            self._progress_bar.setRange(0, 0)
            self._progress_bar.show()
        else:
            self._progress_bar.hide()
