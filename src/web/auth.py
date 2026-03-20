"""웹 대시보드 인증 모듈 - 아이디/비밀번호 검증, 세션 토큰 관리, 로그인 잠금
버전: v1.2
"""
import hashlib
import secrets
import threading
import time


class WebAuth:
    """웹 대시보드 인증 관리."""

    def __init__(self):
        self._username: str = ""
        self._password_hash: str = ""
        self._sessions: dict[str, float] = {}  # token -> expiry timestamp
        self._session_timeout = 3600 * 8  # 8시간
        self._fail_count: int = 0
        self._max_fail: int = 5
        self._lock_until: float = 0
        self._lock_duration: int = 600  # 10분
        self._lock = threading.Lock()

    def set_password(self, password: str) -> None:
        """웹 접속 비밀번호 설정 (하위 호환)."""
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()

    def set_credentials(self, username: str, password: str) -> None:
        """아이디와 비밀번호를 설정한다."""
        self._username = username
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()
        self._fail_count = 0

    def get_username(self) -> str:
        """현재 아이디를 반환한다."""
        return self._username

    def _is_locked_unsafe(self) -> bool:
        """잠금 상태를 확인한다 (락 없음, 내부 전용). 시간 초과 시 자동 해제."""
        if self._lock_until <= 0:
            return False
        if time.time() >= self._lock_until:
            self._lock_until = 0
            self._fail_count = 0
            return False
        return True

    def _remaining_lock_seconds_unsafe(self) -> int:
        """잠금 해제까지 남은 초를 반환한다 (락 없음, 내부 전용)."""
        if not self._is_locked_unsafe():
            return 0
        return int(self._lock_until - time.time())

    def is_locked(self) -> bool:
        """잠금 상태를 확인한다. 시간 초과 시 자동 해제."""
        with self._lock:
            return self._is_locked_unsafe()

    def remaining_lock_seconds(self) -> int:
        """잠금 해제까지 남은 초를 반환한다."""
        with self._lock:
            return self._remaining_lock_seconds_unsafe()

    def verify_password(self, password: str) -> bool:
        """비밀번호 검증 (하위 호환)."""
        with self._lock:
            return hashlib.sha256(password.encode()).hexdigest() == self._password_hash

    def verify(self, username: str, password: str) -> bool:
        """아이디와 비밀번호를 검증한다. 5회 실패 시 잠금."""
        with self._lock:
            if self._is_locked_unsafe():
                return False
            if (
                username == self._username
                and hashlib.sha256(password.encode()).hexdigest() == self._password_hash
            ):
                self._fail_count = 0
                return True
            self._fail_count += 1
            if self._fail_count >= self._max_fail:
                self._lock_until = time.time() + self._lock_duration
            return False

    def create_session(self) -> str:
        """세션 토큰 생성."""
        with self._lock:
            token = secrets.token_hex(32)
            self._sessions[token] = time.time() + self._session_timeout
            return token

    def validate_session(self, token: str) -> bool:
        """세션 토큰 유효성 확인."""
        with self._lock:
            expiry = self._sessions.get(token)
            if expiry is None:
                return False
            if time.time() > expiry:
                del self._sessions[token]
                return False
            return True

    def revoke_session(self, token: str) -> None:
        """세션 종료."""
        with self._lock:
            self._sessions.pop(token, None)

    def is_configured(self) -> bool:
        """아이디와 비밀번호가 모두 설정되어 있는지."""
        return bool(self._username and self._password_hash)

    def remaining_attempts(self) -> int:
        """남은 로그인 시도 횟수를 반환한다."""
        with self._lock:
            if self._is_locked_unsafe():
                return 0
            return self._max_fail - self._fail_count

    def cleanup_expired_sessions(self) -> int:
        """만료된 세션을 정리하고 삭제 건수를 반환한다."""
        with self._lock:
            now = time.time()
            expired = [t for t, exp in self._sessions.items() if now > exp]
            for t in expired:
                del self._sessions[t]
            return len(expired)
