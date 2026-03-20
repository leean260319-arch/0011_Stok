"""T075 킬 스위치 UI 위젯
버전: v1.0
설명: 2초 long-press로 활성화되는 긴급 정지 버튼
"""

from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QPushButton

from src.utils.constants import Colors


class KillSwitchButton(QPushButton):
    """2초 long-press 활성화 킬 스위치 버튼."""

    activated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("KILL", parent)
        self._activated: bool = False
        self._long_press_ms: int = 2000
        self._press_elapsed: int = 0
        self._pressing: bool = False

        # long-press 타이머 (50ms 간격)
        self._press_timer = QTimer(self)
        self._press_timer.setInterval(50)
        self._press_timer.timeout.connect(self._on_press_tick)

        # 깜박임 타이머
        self._blink_timer = QTimer(self)
        self._blink_timer.setInterval(500)
        self._blink_timer.timeout.connect(self._on_blink)
        self._blink_visible: bool = True

        self.setFixedSize(64, 64)
        self._apply_style()

    def is_activated(self) -> bool:
        """활성화 여부를 반환한다."""
        return self._activated

    def deactivate(self) -> None:
        """킬 스위치를 수동 해제한다."""
        self._activated = False
        self._blink_timer.stop()
        self._blink_visible = True
        self._apply_style()
        self.update()

    # ------------------------------------------------------------------
    # Qt 이벤트
    # ------------------------------------------------------------------

    def mousePressEvent(self, event) -> None:
        """마우스 누르기 시작 - 타이머 시작."""
        if event.button() == Qt.MouseButton.LeftButton and not self._activated:
            self._pressing = True
            self._press_elapsed = 0
            self._press_timer.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """마우스 놓기 - 타이머 중지."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressing = False
            self._press_timer.stop()
            self._press_elapsed = 0
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event) -> None:
        """원형 프로그레스 애니메이션을 그린다."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 원형 프로그레스 (누르는 중)
        if self._pressing and self._press_elapsed > 0:
            progress = min(self._press_elapsed / self._long_press_ms, 1.0)
            span_angle = int(progress * 360 * 16)

            pen = QPen(QColor(Colors.DANGER))
            pen.setWidth(3)
            painter.setPen(pen)

            margin = 4
            rect_size = min(self.width(), self.height()) - margin * 2
            painter.drawArc(
                margin, margin, rect_size, rect_size,
                90 * 16, -span_angle,
            )

        painter.end()

    # ------------------------------------------------------------------
    # 내부 슬롯
    # ------------------------------------------------------------------

    def _on_press_tick(self) -> None:
        """long-press 타이머 틱."""
        self._press_elapsed += 50
        self.update()

        if self._press_elapsed >= self._long_press_ms:
            self._press_timer.stop()
            self._activate()

    def _activate(self) -> None:
        """킬 스위치 활성화."""
        self._activated = True
        self._pressing = False
        self._press_elapsed = 0
        self._blink_timer.start()
        self._apply_style()
        self.activated.emit()

    def _on_blink(self) -> None:
        """깜박임 효과."""
        self._blink_visible = not self._blink_visible
        if self._blink_visible:
            self.setStyleSheet(
                f"QPushButton {{ background-color: {Colors.DANGER};"
                f" color: white; border-radius: 32px;"
                f" font-weight: bold; font-size: 14px; }}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{ background-color: {Colors.SURFACE};"
                f" color: {Colors.DANGER}; border-radius: 32px;"
                f" font-weight: bold; font-size: 14px;"
                f" border: 2px solid {Colors.DANGER}; }}"
            )

    def _apply_style(self) -> None:
        """기본 스타일 적용."""
        if self._activated:
            self.setStyleSheet(
                f"QPushButton {{ background-color: {Colors.DANGER};"
                f" color: white; border-radius: 32px;"
                f" font-weight: bold; font-size: 14px; }}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{ background-color: {Colors.SURFACE_VARIANT};"
                f" color: {Colors.DANGER}; border-radius: 32px;"
                f" font-weight: bold; font-size: 14px;"
                f" border: 2px solid {Colors.DANGER}; }}"
            )
