"""T011 AppLock 테스트
time.monotonic은 monkeypatch로 제어
"""
import pytest

from src.security.app_lock import AppLock


@pytest.fixture()
def lock():
    return AppLock()


@pytest.fixture()
def locked_lock():
    al = AppLock()
    al.set_pin("1234")
    al.lock()
    return al


class TestSetVerifyPin:
    def test_verify_correct_pin(self, lock):
        lock.set_pin("9999")
        assert lock.verify_pin("9999") is True

    def test_verify_wrong_pin(self, lock):
        lock.set_pin("9999")
        assert lock.verify_pin("0000") is False

    def test_verify_without_pin_set(self, lock):
        assert lock.verify_pin("1234") is False

    def test_different_pins_dont_match(self, lock):
        lock.set_pin("aaaa")
        assert lock.verify_pin("bbbb") is False

    def test_reset_pin_works(self, lock):
        lock.set_pin("old_pin")
        lock.set_pin("new_pin")
        assert lock.verify_pin("new_pin") is True
        assert lock.verify_pin("old_pin") is False


class TestIsLocked:
    def test_initially_unlocked(self, lock):
        assert lock.is_locked is False

    def test_locked_after_lock(self, lock):
        lock.set_pin("1234")
        lock.lock()
        assert lock.is_locked is True

    def test_unlocked_after_unlock(self, locked_lock):
        locked_lock.unlock("1234")
        assert locked_lock.is_locked is False


class TestUnlock:
    def test_unlock_with_correct_pin(self, locked_lock):
        result = locked_lock.unlock("1234")
        assert result is True
        assert locked_lock.is_locked is False

    def test_unlock_with_wrong_pin(self, locked_lock):
        result = locked_lock.unlock("wrong")
        assert result is False
        assert locked_lock.is_locked is True

    def test_unlock_returns_false_without_pin_set(self, lock):
        lock.lock()
        assert lock.unlock("any") is False


class TestCheckTimeout:
    def test_no_lock_before_timeout(self, lock, monkeypatch):
        base = 1000.0
        monkeypatch.setattr("src.security.app_lock.time.monotonic", lambda: base)
        lock.update_activity()
        # 29분 경과 - 아직 잠금 안됨
        monkeypatch.setattr(
            "src.security.app_lock.time.monotonic", lambda: base + 29 * 60
        )
        lock.check_timeout(timeout_minutes=30)
        assert lock.is_locked is False

    def test_lock_after_timeout(self, lock, monkeypatch):
        base = 1000.0
        monkeypatch.setattr("src.security.app_lock.time.monotonic", lambda: base)
        lock.update_activity()
        # 30분 경과 - 자동 잠금
        monkeypatch.setattr(
            "src.security.app_lock.time.monotonic", lambda: base + 30 * 60
        )
        lock.check_timeout(timeout_minutes=30)
        assert lock.is_locked is True

    def test_lock_after_exceeded_timeout(self, lock, monkeypatch):
        base = 5000.0
        monkeypatch.setattr("src.security.app_lock.time.monotonic", lambda: base)
        lock.update_activity()
        monkeypatch.setattr(
            "src.security.app_lock.time.monotonic", lambda: base + 60 * 60
        )
        lock.check_timeout(timeout_minutes=30)
        assert lock.is_locked is True

    def test_update_activity_resets_timer(self, lock, monkeypatch):
        base = 1000.0
        monkeypatch.setattr("src.security.app_lock.time.monotonic", lambda: base)
        lock.update_activity()
        # 20분 후 활동 갱신
        monkeypatch.setattr(
            "src.security.app_lock.time.monotonic", lambda: base + 20 * 60
        )
        lock.update_activity()
        # 갱신 후 10분 경과 (총 30분이지만 갱신 기준 10분) - 잠금 안됨
        monkeypatch.setattr(
            "src.security.app_lock.time.monotonic", lambda: base + 30 * 60
        )
        lock.check_timeout(timeout_minutes=30)
        assert lock.is_locked is False

    def test_custom_timeout(self, lock, monkeypatch):
        base = 2000.0
        monkeypatch.setattr("src.security.app_lock.time.monotonic", lambda: base)
        lock.update_activity()
        monkeypatch.setattr(
            "src.security.app_lock.time.monotonic", lambda: base + 5 * 60
        )
        lock.check_timeout(timeout_minutes=5)
        assert lock.is_locked is True
