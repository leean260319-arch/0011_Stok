"""WebDashboardServer 테스트
버전: v1.0
"""
import pytest

from src.web.app_state import AppState
from src.web.server import WebDashboardServer


@pytest.fixture(autouse=True)
def reset_singleton():
    AppState.reset_instance()
    yield
    AppState.reset_instance()


# ---------------------------------------------------------------------------
# 인스턴스 생성
# ---------------------------------------------------------------------------

class TestServerCreation:
    def test_create_server(self):
        server = WebDashboardServer(host="127.0.0.1", port=9999, password="test")
        assert server.host == "127.0.0.1"
        assert server.port == 9999
        assert server.url == "http://127.0.0.1:9999"

    def test_server_has_app(self):
        server = WebDashboardServer(password="pw")
        assert server.app is not None

    def test_server_auth_configured(self):
        server = WebDashboardServer(username="admin", password="mypass")
        assert server.auth.is_configured() is True
        assert server.auth.verify("admin", "mypass") is True

    def test_server_default_port(self):
        server = WebDashboardServer(password="x")
        assert server.port == 8080

    def test_server_state_is_singleton(self):
        server = WebDashboardServer(password="x")
        assert server.state is AppState.get_instance()


# ---------------------------------------------------------------------------
# start / stop (smoke test - 실제 서버 기동 최소화)
# ---------------------------------------------------------------------------

class TestServerLifecycle:
    def test_start_and_stop(self):
        """서버 시작 후 중지 가능 여부 확인."""
        server = WebDashboardServer(host="127.0.0.1", port=18080, password="test")
        server.start()
        # 잠시 대기 후 중지
        import time
        time.sleep(0.5)
        server.stop()
        # stop 호출이 에러 없이 완료되면 통과

    def test_stop_without_start(self):
        """시작하지 않은 서버 중지 시 에러 없음."""
        server = WebDashboardServer(password="x")
        server.stop()  # 에러 없이 통과
