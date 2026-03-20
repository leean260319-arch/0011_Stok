"""StokAI 앱 잠금 모듈
버전: 1.0.0
PIN 기반 잠금/해제, 30분 미사용 자동잠금
해시: hashlib.pbkdf2_hmac (bcrypt 대체, 의존성 최소화)
"""
import hashlib
import os
import time

from src.utils.logger import get_logger

logger = get_logger("security.app_lock")

_PBKDF2_ITERATIONS = 260_000
_HASH_ALGO = "sha256"
_SALT_SIZE = 32  # bytes


class AppLock:
    """PIN 기반 앱 잠금 클래스."""

    def __init__(self) -> None:
        self._pin_hash: bytes | None = None
        self._salt: bytes | None = None
        self._locked: bool = False
        self._last_activity: float = time.monotonic()

    # ------------------------------------------------------------------
    # PIN 관리
    # ------------------------------------------------------------------

    def set_pin(self, pin: str) -> None:
        """PIN을 pbkdf2_hmac으로 해시하여 저장."""
        salt = os.urandom(_SALT_SIZE)
        pin_hash = hashlib.pbkdf2_hmac(
            _HASH_ALGO,
            pin.encode("utf-8"),
            salt,
            _PBKDF2_ITERATIONS,
        )
        self._salt = salt
        self._pin_hash = pin_hash
        logger.debug("PIN 설정 완료")

    def verify_pin(self, pin: str) -> bool:
        """입력된 PIN이 저장된 해시와 일치하는지 확인."""
        if self._pin_hash is None or self._salt is None:
            return False
        candidate = hashlib.pbkdf2_hmac(
            _HASH_ALGO,
            pin.encode("utf-8"),
            self._salt,
            _PBKDF2_ITERATIONS,
        )
        return candidate == self._pin_hash

    # ------------------------------------------------------------------
    # 잠금 상태 관리
    # ------------------------------------------------------------------

    @property
    def is_locked(self) -> bool:
        """현재 잠금 상태 반환."""
        return self._locked

    def lock(self) -> None:
        """앱을 잠금 상태로 전환."""
        self._locked = True
        logger.info("앱 잠금")

    def unlock(self, pin: str) -> bool:
        """PIN 확인 후 잠금 해제. 성공 시 True 반환."""
        if not self.verify_pin(pin):
            logger.warning("잠금 해제 실패: PIN 불일치")
            return False
        self._locked = False
        self.update_activity()
        logger.info("앱 잠금 해제")
        return True

    # ------------------------------------------------------------------
    # 자동 잠금 (타임아웃)
    # ------------------------------------------------------------------

    def update_activity(self) -> None:
        """마지막 활동 시간을 현재 시각으로 갱신."""
        self._last_activity = time.monotonic()

    def check_timeout(self, timeout_minutes: int = 30) -> None:
        """마지막 활동 이후 timeout_minutes 초과 시 자동 잠금."""
        elapsed_minutes = (time.monotonic() - self._last_activity) / 60.0
        if elapsed_minutes >= timeout_minutes:
            logger.info("비활동 타임아웃 (%.1f분) - 자동 잠금", elapsed_minutes)
            self.lock()
