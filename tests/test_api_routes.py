"""REST API 엔드포인트 테스트 - FastAPI TestClient
버전: v1.0
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.web.app_state import AppState
from src.web.auth import WebAuth
from src.web.ws_manager import WebSocketManager
from src.web.api_routes import router, set_deps, ApiDeps


@pytest.fixture(autouse=True)
def reset_singleton():
    AppState.reset_instance()
    yield
    AppState.reset_instance()


@pytest.fixture
def deps():
    """API 의존성 세트."""
    state = AppState.get_instance()
    auth = WebAuth()
    auth.set_credentials("admin", "testpass")
    ws = WebSocketManager()
    d = ApiDeps(auth=auth, state=state, ws_manager=ws)
    set_deps(d)
    return d


@pytest.fixture
def client(deps) -> TestClient:
    """FastAPI TestClient."""
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.fixture
def auth_header(client) -> dict:
    """로그인 후 인증 헤더."""
    resp = client.post("/api/login", json={"username": "admin", "password": "testpass"})
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# 인증
# ---------------------------------------------------------------------------

class TestAuth:
    def test_login_success(self, client):
        resp = client.post("/api/login", json={"username": "admin", "password": "testpass"})
        assert resp.status_code == 200
        assert "token" in resp.json()

    def test_login_wrong_password(self, client):
        resp = client.post("/api/login", json={"username": "admin", "password": "wrong"})
        assert resp.status_code == 401

    def test_access_without_token(self, client):
        resp = client.get("/api/status")
        assert resp.status_code == 401

    def test_access_with_invalid_token(self, client):
        resp = client.get("/api/status", headers={"Authorization": "Bearer fake"})
        assert resp.status_code == 401

    def test_logout(self, client, auth_header):
        resp = client.post("/api/logout", headers=auth_header)
        assert resp.status_code == 200
        # 로그아웃 후 토큰 무효
        resp2 = client.get("/api/status", headers=auth_header)
        assert resp2.status_code == 401


# ---------------------------------------------------------------------------
# GET 엔드포인트
# ---------------------------------------------------------------------------

class TestGetEndpoints:
    def test_get_status(self, client, auth_header, deps):
        deps.state.update_account(total_asset=5_000_000)
        resp = client.get("/api/status", headers=auth_header)
        assert resp.status_code == 200
        data = resp.json()
        assert data["account"]["total_asset"] == 5_000_000

    def test_get_account(self, client, auth_header, deps):
        deps.state.update_account(deposit=2_000_000)
        resp = client.get("/api/account", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["deposit"] == 2_000_000

    def test_get_positions(self, client, auth_header, deps):
        deps.state.update_positions([{"symbol": "005930", "quantity": 10}])
        resp = client.get("/api/positions", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_get_trade_logs(self, client, auth_header, deps):
        for i in range(5):
            deps.state.add_trade_log({"action": "buy", "symbol": str(i)})
        resp = client.get("/api/trade-logs?limit=3", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) == 3

    def test_get_alerts(self, client, auth_header, deps):
        deps.state.add_alert("test", "알림 1")
        resp = client.get("/api/alerts", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_get_ai_signal(self, client, auth_header):
        resp = client.get("/api/ai-signal", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["signal_type"] == "hold"

    def test_get_sentiment(self, client, auth_header):
        resp = client.get("/api/sentiment", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["label"] == "neutral"

    def test_get_market(self, client, auth_header):
        resp = client.get("/api/market", headers=auth_header)
        assert resp.status_code == 200
        assert "kospi" in resp.json()
        assert "kosdaq" in resp.json()


# ---------------------------------------------------------------------------
# POST 제어 엔드포인트
# ---------------------------------------------------------------------------

class TestControlEndpoints:
    def test_autotrade_start(self, client, auth_header, deps):
        resp = client.post(
            "/api/autotrade/start",
            json={"strategy_name": "momentum"},
            headers=auth_header,
        )
        assert resp.status_code == 200
        assert deps.state.auto_trade["is_running"] is True
        assert deps.state.auto_trade["strategy_name"] == "momentum"

    def test_autotrade_stop(self, client, auth_header, deps):
        deps.state.auto_trade["is_running"] = True
        deps.state.auto_trade["strategy_name"] = "test"
        resp = client.post("/api/autotrade/stop", headers=auth_header)
        assert resp.status_code == 200
        assert deps.state.auto_trade["is_running"] is False

    def test_kill_switch_on(self, client, auth_header, deps):
        resp = client.post("/api/kill-switch/on", headers=auth_header)
        assert resp.status_code == 200
        assert deps.state.kill_switch_active is True

    def test_kill_switch_off(self, client, auth_header, deps):
        deps.state.kill_switch_active = True
        resp = client.post("/api/kill-switch/off", headers=auth_header)
        assert resp.status_code == 200
        assert deps.state.kill_switch_active is False

    def test_kill_switch_creates_alert(self, client, auth_header, deps):
        client.post("/api/kill-switch/on", headers=auth_header)
        assert len(deps.state.alerts) >= 1
        assert deps.state.alerts[0]["category"] == "kill_switch"

    def test_autotrade_start_creates_alert(self, client, auth_header, deps):
        client.post(
            "/api/autotrade/start",
            json={"strategy_name": "test_strat"},
            headers=auth_header,
        )
        assert any("자동매매 시작" in a["message"] for a in deps.state.alerts)
