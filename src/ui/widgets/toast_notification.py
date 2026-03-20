"""T083 토스트 알림 위젯
버전: v1.0
설명: 화면 우하단 팝업 토스트 알림 (자동 fade-out)
"""

from PyQt6.QtCore import QPropertyAnimation, QTimer, Qt
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QLabel, QVBoxLayout, QWidget

from src.utils.constants import Colors

_TYPE_COLORS = {
    "info": Colors.PRIMARY,
    "warning": Colors.WARNING,
    "error": Colors.DANGER,
}


class ToastNotification(QWidget):
    """토스트 알림 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._toast_type: str = "info"
        self._duration_ms: int = 3000
        self._setup_ui()

        # fade-out 효과
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_animation.setDuration(500)
        self._fade_animation.setStartValue(1.0)
        self._fade_animation.setEndValue(0.0)
        self._fade_animation.finished.connect(self.hide)

        # 자동 숨김 타이머
        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self._start_fade_out)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(300)
        self.hide()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        self._message_label = QLabel("")
        self._message_label.setWordWrap(True)
        self._message_label.setStyleSheet(
            f"color: {Colors.TEXT_PRIMARY}; font-size: 13px;"
        )
        layout.addWidget(self._message_label)

    def show_toast(
        self,
        message: str,
        duration_ms: int = 3000,
        toast_type: str = "info",
    ) -> None:
        """토스트를 표시한다.

        Args:
            message: 표시 메시지
            duration_ms: 표시 지속 시간 (ms)
            toast_type: "info", "warning", "error"
        """
        self._toast_type = toast_type
        self._duration_ms = duration_ms

        color = _TYPE_COLORS.get(toast_type, Colors.PRIMARY)
        self.setStyleSheet(
            f"ToastNotification {{"
            f"  background-color: {Colors.SURFACE};"
            f"  border-left: 4px solid {color};"
            f"  border-radius: 6px;"
            f"  border: 1px solid {Colors.BORDER};"
            f"}}"
        )

        self._message_label.setText(message)
        self._opacity_effect.setOpacity(1.0)
        self.show()

        self._auto_hide_timer.start(duration_ms)

    def _start_fade_out(self) -> None:
        """fade-out 애니메이션 시작."""
        self._fade_animation.start()
