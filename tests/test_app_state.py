"""AppState 테스트 - 공유 상태 객체
버전: v1.0
"""
import threading

import pytest

from src.web.app_state import AppState


@pytest.fixture(autouse=True)
def reset_singleton():
    """각 테스트 전후 싱글톤 초기화."""
    AppState.reset_instance()
    yield
    AppState.reset_instance()


@pytest.fixture
def state() -> AppState:
    return AppState.get_instance()


# ---------------------------------------------------------------------------
# 싱글톤
# ---------------------------------------------------------------------------

class TestSingleton:
    def test_get_instance_returns_same_object(self):
        a = AppState.get_instance()
        b = AppState.get_instance()
        assert a is b

    def test_reset_instance_creates_new(self):
        a = AppState.get_instance()
        AppState.reset_instance()
        b = AppState.get_instance()
        assert a is not b


# ---------------------------------------------------------------------------
# update_account
# ---------------------------------------------------------------------------

class TestUpdateAccount:
    def test_update_single_field(self, state):
        state.update_account(total_asset=10_000_000)
        assert state.account["total_asset"] == 10_000_000

    def test_update_multiple_fields(self, state):
        state.update_account(total_asset=5_000_000, deposit=1_000_000, profit_rate=2.5)
        assert state.account["total_asset"] == 5_000_000
        assert state.account["deposit"] == 1_000_000
        assert state.account["profit_rate"] == 2.5

    def test_update_sets_last_update(self, state):
        state.update_account(total_asset=100)
        assert "last_update" in state.account
        assert state.account["last_update"] is not None


# ---------------------------------------------------------------------------
# update_positions
# ---------------------------------------------------------------------------

class TestUpdatePositions:
    def test_set_positions(self, state):
        positions = [
            {"symbol": "005930", "name": "삼성전자", "quantity": 10},
            {"symbol": "000660", "name": "SK하이닉스", "quantity": 5},
        ]
        state.update_positions(positions)
        assert len(state.positions) == 2
        assert state.positions[0]["symbol"] == "005930"

    def test_replace_positions(self, state):
        state.update_positions([{"symbol": "A"}])
        state.update_positions([{"symbol": "B"}, {"symbol": "C"}])
        assert len(state.positions) == 2
        assert state.positions[0]["symbol"] == "B"


# ---------------------------------------------------------------------------
# add_trade_log
# ---------------------------------------------------------------------------

class TestAddTradeLog:
    def test_add_log(self, state):
        state.add_trade_log({"action": "buy", "symbol": "005930", "amount": 700_000})
        assert len(state.trade_logs) == 1
        assert state.trade_logs[0]["action"] == "buy"
        assert "timestamp" in state.trade_logs[0]

    def test_newest_first(self, state):
        state.add_trade_log({"action": "buy", "symbol": "A"})
        state.add_trade_log({"action": "sell", "symbol": "B"})
        assert state.trade_logs[0]["symbol"] == "B"
        assert state.trade_logs[1]["symbol"] == "A"

    def test_max_100_logs(self, state):
        for i in range(110):
            state.add_trade_log({"action": "buy", "symbol": str(i)})
        assert len(state.trade_logs) == 100
        # 가장 최근 것이 첫 번째
        assert state.trade_logs[0]["symbol"] == "109"


# ---------------------------------------------------------------------------
# add_alert
# ---------------------------------------------------------------------------

class TestAddAlert:
    def test_add_alert(self, state):
        state.add_alert("system", "테스트 알림")
        assert len(state.alerts) == 1
        assert state.alerts[0]["category"] == "system"
        assert state.alerts[0]["message"] == "테스트 알림"
        assert state.alerts[0]["read"] is False

    def test_max_50_alerts(self, state):
        for i in range(60):
            state.add_alert("test", f"알림 {i}")
        assert len(state.alerts) == 50
        assert state.alerts[0]["message"] == "알림 59"


# ---------------------------------------------------------------------------
# get_snapshot
# ---------------------------------------------------------------------------

class TestGetSnapshot:
    def test_snapshot_has_all_keys(self, state):
        snap = state.get_snapshot()
        expected_keys = {
            "account", "positions", "auto_trade", "kill_switch_active",
            "ai_signal", "sentiment", "market_index", "trade_logs",
            "alerts", "system",
        }
        assert set(snap.keys()) == expected_keys

    def test_snapshot_reflects_updates(self, state):
        state.update_account(total_asset=999)
        state.kill_switch_active = True
        snap = state.get_snapshot()
        assert snap["account"]["total_asset"] == 999
        assert snap["kill_switch_active"] is True

    def test_snapshot_trade_logs_max_20(self, state):
        for i in range(30):
            state.add_trade_log({"action": "buy", "symbol": str(i)})
        snap = state.get_snapshot()
        assert len(snap["trade_logs"]) == 20

    def test_snapshot_alerts_only_unread(self, state):
        state.add_alert("a", "msg1")
        state.add_alert("b", "msg2")
        state.alerts[1]["read"] = True  # msg1을 읽음 처리
        snap = state.get_snapshot()
        # 읽지 않은 것만
        assert all(a["read"] is False for a in snap["alerts"])


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_updates(self, state):
        """여러 스레드에서 동시에 업데이트해도 오류 없이 동작."""
        errors = []

        def updater(n):
            for i in range(50):
                state.update_account(total_asset=n * 1000 + i)
                state.add_trade_log({"action": "buy", "symbol": f"{n}-{i}"})
                state.add_alert("thread", f"스레드 {n} 알림 {i}")

        threads = [threading.Thread(target=updater, args=(t,)) for t in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 오류 없이 완료, 제한 초과하지 않음
        assert len(state.trade_logs) <= 100
        assert len(state.alerts) <= 50
        snap = state.get_snapshot()
        assert "account" in snap
