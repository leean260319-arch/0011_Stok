"""T102 글래스모피즘 카드 위젯
버전: v1.0
설명: 반투명 배경과 둥근 모서리를 가진 카드 위젯
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class GlassCard(QFrame):
    """글래스모피즘 스타일의 카드 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._content_widget: QWidget | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            "GlassCard {"
            "  background: rgba(255,255,255,0.05);"
            "  border-radius: 12px;"
            "  border: 1px solid rgba(255,255,255,0.1);"
            "}"
        )

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(8)

        self._title_label = QLabel("")
        self._title_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #E0E0E0;"
            "background: transparent; border: none;"
        )
        self._layout.addWidget(self._title_label)

    def setTitle(self, title: str) -> None:
        """카드 타이틀을 설정한다."""
        self._title_label.setText(title)

    def setContent(self, widget: QWidget) -> None:
        """카드 콘텐츠 위젯을 설정한다. 기존 콘텐츠는 제거된다."""
        if self._content_widget is not None:
            self._layout.removeWidget(self._content_widget)
            self._content_widget.setParent(None)
        self._content_widget = widget
        self._layout.addWidget(widget)

    def paintEvent(self, event) -> None:
        """둥근 모서리와 반투명 배경을 그린다."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5, self.width() - 1, self.height() - 1, 12, 12)

        # 반투명 배경
        painter.fillPath(path, QColor(255, 255, 255, 13))

        # 테두리
        pen = QPen(QColor(255, 255, 255, 26))
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.end()
        super().paintEvent(event)
