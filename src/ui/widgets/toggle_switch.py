"""T028 ToggleSwitch - 투자 모드 토글 스위치 위젯
버전: 1.0.0
설명: 모의투자(파랑)↔실전투자(빨강) 커스텀 토글 스위치
"""
from PyQt6.QtCore import QRect, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QSizePolicy, QWidget


class ToggleSwitch(QWidget):
    """커스텀 토글 스위치 위젯.

    unchecked(모의투자) = 파랑 #326AFF
    checked(실전투자)  = 빨강 #F04451
    """

    toggled = pyqtSignal(bool)

    unchecked_color = "#326AFF"
    checked_color = "#F04451"

    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self.setMinimumSize(60, 28)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # ------------------------------------------------------------------
    # 공개 API
    # ------------------------------------------------------------------
    @property
    def checked(self) -> bool:
        return self._checked

    def set_checked(self, value: bool) -> None:
        """checked 상태를 설정하고 toggled 시그널을 발행."""
        if self._checked == value:
            return
        self._checked = value
        self.update()
        self.toggled.emit(self._checked)

    # ------------------------------------------------------------------
    # Qt 이벤트
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_checked(not self._checked)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        radius = h / 2

        # 배경 트랙
        color = QColor(self.checked_color if self._checked else self.unchecked_color)
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        track = QPainterPath()
        track.addRoundedRect(0, 0, w, h, radius, radius)
        painter.drawPath(track)

        # 슬라이더 원
        margin = 3
        diameter = h - margin * 2
        x = w - diameter - margin if self._checked else margin
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(int(x), margin, diameter, diameter)

        painter.end()
