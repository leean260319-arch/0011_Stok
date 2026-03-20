"""알림 매니저 테스트
v1.0 - 2026-03-17: 신규 작성
"""

from src.ui.alert_manager import AlertManager


class TestAlertManager:
    def test_creation(self, qapp):
        """AlertManager 인스턴스 생성"""
        mgr = AlertManager()
        assert mgr is not None
        assert mgr.get_alerts() == []

    def test_add_alert(self, qapp):
        """알림 추가"""
        mgr = AlertManager()
        mgr.add_alert("system", "테스트", "테스트 메시지", "info")
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert alerts[0]["category"] == "system"
        assert alerts[0]["title"] == "테스트"
        assert alerts[0]["message"] == "테스트 메시지"
        assert alerts[0]["level"] == "info"

    def test_add_alert_emits_signal(self, qapp):
        """알림 추가 시 alert_added 시그널 발행"""
        mgr = AlertManager()
        received = []
        mgr.alert_added.connect(lambda alert: received.append(alert))
        mgr.add_alert("system", "제목", "내용")
        assert len(received) == 1
        assert received[0]["title"] == "제목"

    def test_default_level_info(self, qapp):
        """기본 알림 레벨은 info"""
        mgr = AlertManager()
        mgr.add_alert("system", "제목", "내용")
        assert mgr.get_alerts()[0]["level"] == "info"

    def test_on_trade_executed(self, qapp):
        """매매 체결 알림"""
        mgr = AlertManager()
        trade = {
            "action": "매수",
            "stock_code": "005930",
            "quantity": 10,
            "price": 70000,
        }
        mgr.on_trade_executed(trade)
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert alerts[0]["category"] == "trade"
        assert "매수 체결" in alerts[0]["title"]
        assert "005930" in alerts[0]["message"]
        assert "10주" in alerts[0]["message"]

    def test_on_kill_switch(self, qapp):
        """킬 스위치 발동 알림"""
        mgr = AlertManager()
        mgr.on_kill_switch()
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert alerts[0]["level"] == "critical"
        assert alerts[0]["category"] == "system"
        assert "긴급 정지" in alerts[0]["title"]

    def test_on_connection_lost(self, qapp):
        """연결 끊김 알림"""
        mgr = AlertManager()
        mgr.on_connection_lost()
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert alerts[0]["level"] == "warning"
        assert "연결 끊김" in alerts[0]["title"]

    def test_on_risk_rejected(self, qapp):
        """리스크 거부 알림"""
        mgr = AlertManager()
        mgr.on_risk_rejected("최대 매수금액 초과")
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert "주문 거부" in alerts[0]["title"]
        assert "최대 매수금액 초과" in alerts[0]["message"]

    def test_on_news_sentiment_high_positive(self, qapp):
        """긍정 감성 점수 0.7 이상이면 알림"""
        mgr = AlertManager()
        mgr.on_news_sentiment("005930", "positive", 0.85)
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert "긍정" in alerts[0]["title"]
        assert alerts[0]["level"] == "info"

    def test_on_news_sentiment_high_negative(self, qapp):
        """부정 감성 점수 -0.7 이하이면 알림"""
        mgr = AlertManager()
        mgr.on_news_sentiment("005930", "negative", -0.8)
        alerts = mgr.get_alerts()
        assert len(alerts) == 1
        assert "부정" in alerts[0]["title"]
        assert alerts[0]["level"] == "warning"

    def test_on_news_sentiment_low_score_ignored(self, qapp):
        """감성 점수 절댓값 0.7 미만이면 알림 무시"""
        mgr = AlertManager()
        mgr.on_news_sentiment("005930", "neutral", 0.3)
        assert mgr.get_alerts() == []

    def test_get_unread_count(self, qapp):
        """알림 수 반환"""
        mgr = AlertManager()
        mgr.add_alert("system", "1", "msg1")
        mgr.add_alert("system", "2", "msg2")
        assert mgr.get_unread_count() == 2

    def test_clear(self, qapp):
        """알림 초기화"""
        mgr = AlertManager()
        mgr.add_alert("system", "1", "msg1")
        mgr.add_alert("system", "2", "msg2")
        mgr.clear()
        assert mgr.get_alerts() == []
        assert mgr.get_unread_count() == 0

    def test_multiple_events(self, qapp):
        """여러 이벤트를 순서대로 처리"""
        mgr = AlertManager()
        mgr.on_kill_switch()
        mgr.on_connection_lost()
        mgr.on_trade_executed({"action": "매도", "stock_code": "035420", "quantity": 5, "price": 200000})
        assert len(mgr.get_alerts()) == 3
        categories = [a["category"] for a in mgr.get_alerts()]
        assert categories == ["system", "system", "trade"]
