"""T082 알림 센터 위젯
버전: v1.0
설명: 카테고리별 알림 관리 (trade/analysis/system)
"""

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors

_CATEGORY_ICONS = {
    "trade": "[Trade]",
    "analysis": "[AI]",
    "system": "[SYS]",
}


class AlertView(QWidget):
    """알림 센터 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._alerts: list[dict] = []
        self._next_id: int = 1
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # 헤더
        header = QHBoxLayout()
        title = QLabel("알림 센터")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        header.addWidget(title)

        self._unread_label = QLabel("0")
        self._unread_label.setStyleSheet(
            f"background-color: {Colors.DANGER}; color: white;"
            " border-radius: 8px; padding: 2px 6px; font-size: 11px;"
        )
        header.addWidget(self._unread_label)
        header.addStretch()

        self._clear_button = QPushButton("모두 삭제")
        self._clear_button.setFixedHeight(24)
        self._clear_button.clicked.connect(self.clear_all)
        header.addWidget(self._clear_button)

        layout.addLayout(header)

        # 알림 리스트
        self._list_widget = QListWidget()
        self._list_widget.setStyleSheet(
            f"QListWidget {{ background-color: {Colors.SURFACE};"
            f" border: 1px solid {Colors.BORDER}; border-radius: 4px; }}"
            f"QListWidget::item {{ padding: 6px; border-bottom: 1px solid {Colors.BORDER}; }}"
        )
        layout.addWidget(self._list_widget)

    def add_alert(self, category: str, message: str, timestamp: datetime) -> None:
        """알림을 추가한다.

        Args:
            category: "trade", "analysis", "system"
            message: 알림 메시지
            timestamp: 알림 시간
        """
        alert = {
            "id": self._next_id,
            "category": category,
            "message": message,
            "timestamp": timestamp,
            "read": False,
        }
        self._next_id += 1
        self._alerts.append(alert)
        self._refresh_list()

    def get_alerts(self) -> list[dict]:
        """전체 알림 목록을 반환한다."""
        return list(self._alerts)

    def mark_read(self, alert_id: int) -> None:
        """알림을 읽음 처리한다."""
        for alert in self._alerts:
            if alert["id"] == alert_id:
                alert["read"] = True
                break
        self._refresh_list()

    def unread_count(self) -> int:
        """읽지 않은 알림 개수를 반환한다."""
        return sum(1 for a in self._alerts if not a["read"])

    def clear_all(self) -> None:
        """모든 알림을 삭제한다."""
        self._alerts.clear()
        self._refresh_list()

    def _refresh_list(self) -> None:
        """알림 리스트 UI를 갱신한다."""
        self._list_widget.clear()
        for alert in reversed(self._alerts):
            prefix = _CATEGORY_ICONS.get(alert["category"], "[?]")
            ts = alert["timestamp"].strftime("%H:%M:%S")
            text = f"{prefix} {ts} - {alert['message']}"
            item = QListWidgetItem(text)
            if alert["read"]:
                item.setForeground(QColor(Colors.TEXT_SECONDARY))
            self._list_widget.addItem(item)

        self._unread_label.setText(str(self.unread_count()))
