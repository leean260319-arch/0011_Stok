"""T082 알림 센터 테스트
버전: v1.0
"""
import pytest
from datetime import datetime

from src.ui.alert_view import AlertView


class TestAlertView:
    """AlertView 위젯 테스트."""

    def test_creation(self, qapp):
        """AlertView 인스턴스 생성."""
        view = AlertView()
        assert view is not None

    def test_add_alert(self, qapp):
        """알림 추가."""
        view = AlertView()
        ts = datetime.now()
        view.add_alert("trade", "매수 체결", ts)
        alerts = view.get_alerts()
        assert len(alerts) == 1
        assert alerts[0]["category"] == "trade"
        assert alerts[0]["message"] == "매수 체결"

    def test_add_multiple_alerts(self, qapp):
        """여러 알림 추가."""
        view = AlertView()
        ts = datetime.now()
        view.add_alert("trade", "매수 체결", ts)
        view.add_alert("analysis", "분석 완료", ts)
        view.add_alert("system", "시스템 알림", ts)
        assert len(view.get_alerts()) == 3

    def test_mark_read(self, qapp):
        """알림 읽음 처리."""
        view = AlertView()
        ts = datetime.now()
        view.add_alert("trade", "매수 체결", ts)
        alerts = view.get_alerts()
        alert_id = alerts[0]["id"]
        view.mark_read(alert_id)
        alerts = view.get_alerts()
        assert alerts[0]["read"] is True

    def test_unread_count(self, qapp):
        """읽지 않은 알림 개수."""
        view = AlertView()
        ts = datetime.now()
        view.add_alert("trade", "매수1", ts)
        view.add_alert("trade", "매수2", ts)
        assert view.unread_count() == 2
        alerts = view.get_alerts()
        view.mark_read(alerts[0]["id"])
        assert view.unread_count() == 1

    def test_clear_all(self, qapp):
        """모든 알림 삭제."""
        view = AlertView()
        ts = datetime.now()
        view.add_alert("trade", "매수", ts)
        view.add_alert("system", "시스템", ts)
        view.clear_all()
        assert len(view.get_alerts()) == 0
        assert view.unread_count() == 0

    def test_alert_categories(self, qapp):
        """알림 카테고리: trade, analysis, system."""
        view = AlertView()
        ts = datetime.now()
        view.add_alert("trade", "매매", ts)
        view.add_alert("analysis", "분석", ts)
        view.add_alert("system", "시스템", ts)
        categories = [a["category"] for a in view.get_alerts()]
        assert "trade" in categories
        assert "analysis" in categories
        assert "system" in categories
