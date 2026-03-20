"""알림 매니저 - 앱 이벤트를 알림으로 변환
v1.0 - 2026-03-17: 신규 작성
"""

from PyQt6.QtCore import QObject, pyqtSignal
from src.utils.logger import get_logger

logger = get_logger("ui.alert_manager")


class AlertManager(QObject):
    """앱 이벤트를 수신하여 알림을 생성한다.

    Signals:
        alert_added: 새 알림 추가 시 (dict with keys: category, title, message, level)
    """

    alert_added = pyqtSignal(dict)

    # 알림 레벨
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

    def __init__(self):
        super().__init__()
        self._alerts: list[dict] = []

    def add_alert(self, category: str, title: str, message: str, level: str = "info"):
        """알림 추가"""
        alert = {
            "category": category,
            "title": title,
            "message": message,
            "level": level,
        }
        self._alerts.append(alert)
        self.alert_added.emit(alert)
        logger.info("[%s] %s: %s", level.upper(), title, message)

    def on_trade_executed(self, trade_data: dict):
        """매매 체결 알림"""
        action = trade_data.get("action", "")
        stock = trade_data.get("stock_code", "")
        qty = trade_data.get("quantity", 0)
        price = trade_data.get("price", 0)
        self.add_alert(
            category="trade",
            title=f"{action} 체결",
            message=f"{stock} {qty}주 @ {price:,}원",
            level=self.INFO,
        )

    def on_kill_switch(self):
        """킬 스위치 발동 알림"""
        self.add_alert(
            category="system",
            title="긴급 정지",
            message="킬 스위치가 발동되었습니다. 모든 자동매매가 중지됩니다.",
            level=self.CRITICAL,
        )

    def on_connection_lost(self):
        """연결 끊김 알림"""
        self.add_alert(
            category="system",
            title="연결 끊김",
            message="키움 API 연결이 끊어졌습니다.",
            level=self.WARNING,
        )

    def on_risk_rejected(self, reason: str):
        """리스크 거부 알림"""
        self.add_alert(
            category="system",
            title="주문 거부",
            message=reason,
            level=self.WARNING,
        )

    def on_news_sentiment(self, stock_code: str, sentiment: str, score: float):
        """뉴스 감성 알림 (극단적 감성만)"""
        if abs(score) < 0.7:
            return
        direction = "긍정" if score > 0 else "부정"
        self.add_alert(
            category="analysis",
            title=f"{stock_code} 감성 {direction}",
            message=f"감성 점수: {score:.2f}",
            level=self.INFO if score > 0 else self.WARNING,
        )

    def get_alerts(self) -> list[dict]:
        """전체 알림 목록 반환"""
        return list(self._alerts)

    def get_unread_count(self) -> int:
        """알림 수"""
        return len(self._alerts)

    def clear(self):
        """알림 초기화"""
        self._alerts.clear()
