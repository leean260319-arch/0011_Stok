"""WebAuth 테스트 - 인증 모듈
버전: v1.1
"""
import time

import pytest

from src.web.auth import WebAuth


@pytest.fixture
def auth() -> WebAuth:
    a = WebAuth()
    a.set_credentials("admin", "test1234")
    return a


@pytest.fixture
def auth_password_only() -> WebAuth:
    """하위 호환: 비밀번호만 설정."""
    a = WebAuth()
    a.set_password("test1234")
    return a


# ---------------------------------------------------------------------------
# set_password / verify_password
# ---------------------------------------------------------------------------

class TestPassword:
    def test_verify_correct_password(self, auth_password_only):
        assert auth_password_only.verify_password("test1234") is True

    def test_verify_wrong_password(self, auth_password_only):
        assert auth_password_only.verify_password("wrong") is False

    def test_verify_empty_password(self):
        a = WebAuth()
        assert a.verify_password("") is False

    def test_change_password(self, auth_password_only):
        auth_password_only.set_password("newpass")
        assert auth_password_only.verify_password("newpass") is True
        assert auth_password_only.verify_password("test1234") is False


# ---------------------------------------------------------------------------
# create_session / validate_session / revoke_session
# ---------------------------------------------------------------------------

class TestSession:
    def test_create_and_validate(self, auth):
        token = auth.create_session()
        assert isinstance(token, str)
        assert len(token) == 64  # hex(32 bytes) = 64 chars
        assert auth.validate_session(token) is True

    def test_invalid_token(self, auth):
        assert auth.validate_session("fake_token") is False

    def test_revoke_session(self, auth):
        token = auth.create_session()
        assert auth.validate_session(token) is True
        auth.revoke_session(token)
        assert auth.validate_session(token) is False

    def test_revoke_nonexistent_token(self, auth):
        # 에러 없이 무시
        auth.revoke_session("nonexistent")

    def test_multiple_sessions(self, auth):
        t1 = auth.create_session()
        t2 = auth.create_session()
        assert t1 != t2
        assert auth.validate_session(t1) is True
        assert auth.validate_session(t2) is True

    def test_session_expiry(self, auth):
        """만료된 세션은 유효하지 않음."""
        token = auth.create_session()
        # 수동으로 만료 시간을 과거로 설정
        auth._sessions[token] = time.time() - 1
        assert auth.validate_session(token) is False
        # 만료된 세션은 삭제됨
        assert token not in auth._sessions


# ---------------------------------------------------------------------------
# is_configured
# ---------------------------------------------------------------------------

class TestIsConfigured:
    def test_configured_after_set_credentials(self, auth):
        assert auth.is_configured() is True

    def test_not_configured_initially(self):
        a = WebAuth()
        assert a.is_configured() is False

    def test_is_configured_requires_both(self):
        """username과 password_hash 둘 다 있어야 True."""
        a = WebAuth()
        a.set_password("test")
        assert a.is_configured() is False  # username 없음

        b = WebAuth()
        b._username = "admin"
        assert b.is_configured() is False  # password_hash 없음

        c = WebAuth()
        c.set_credentials("admin", "test")
        assert c.is_configured() is True


# ---------------------------------------------------------------------------
# set_credentials / verify / lock
# ---------------------------------------------------------------------------

class TestCredentials:
    def test_set_credentials(self):
        a = WebAuth()
        a.set_credentials("user1", "pass1")
        assert a.get_username() == "user1"
        assert a.verify("user1", "pass1") is True

    def test_verify_with_username(self, auth):
        assert auth.verify("admin", "test1234") is True

    def test_verify_wrong_username(self, auth):
        assert auth.verify("wrong_user", "test1234") is False

    def test_verify_wrong_password_with_username(self, auth):
        assert auth.verify("admin", "wrong") is False

    def test_get_username(self, auth):
        assert auth.get_username() == "admin"

    def test_login_lock_after_5_fails(self):
        a = WebAuth()
        a.set_credentials("admin", "secret")
        for _ in range(5):
            a.verify("admin", "wrong")
        assert a.is_locked() is True
        assert a.remaining_lock_seconds() > 0
        # 잠금 상태에서 올바른 비밀번호도 실패
        assert a.verify("admin", "secret") is False

    def test_lock_auto_release(self):
        a = WebAuth()
        a.set_credentials("admin", "secret")
        for _ in range(5):
            a.verify("admin", "wrong")
        assert a.is_locked() is True
        # 수동으로 잠금 시간을 과거로 설정
        a._lock_until = time.time() - 1
        assert a.is_locked() is False
        assert a.remaining_lock_seconds() == 0
        # 잠금 해제 후 정상 로그인 가능
        assert a.verify("admin", "secret") is True

    def test_fail_count_resets_on_success(self):
        a = WebAuth()
        a.set_credentials("admin", "secret")
        a.verify("admin", "wrong")
        a.verify("admin", "wrong")
        assert a._fail_count == 2
        a.verify("admin", "secret")
        assert a._fail_count == 0

    def test_set_credentials_resets_fail_count(self):
        a = WebAuth()
        a.set_credentials("admin", "secret")
        a.verify("admin", "wrong")
        a.verify("admin", "wrong")
        a.set_credentials("admin", "newsecret")
        assert a._fail_count == 0
