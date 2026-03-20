"""StokAI 자격증명 매니저 모듈
버전: 1.0.0
keyring을 사용하여 OS 자격증명 저장소에 안전하게 저장
"""
import json
import keyring

from src.utils.constants import KEYRING_SERVICE
from src.utils.logger import get_logger

_KEYS_INDEX_KEY = "__stokai_keys_index__"

logger = get_logger("security.credential_manager")


class CredentialManager:
    """OS keyring을 사용하는 자격증명 매니저."""

    def __init__(self, service: str = KEYRING_SERVICE):
        self.service = service

    def save(self, key: str, value: str) -> None:
        """자격증명을 keyring에 저장."""
        keyring.set_password(self.service, key, value)
        self._add_to_index(key)
        logger.debug("자격증명 저장: %s", key)

    def get(self, key: str) -> str | None:
        """자격증명을 keyring에서 조회."""
        return keyring.get_password(self.service, key)

    def delete(self, key: str) -> None:
        """자격증명을 keyring에서 삭제."""
        keyring.delete_password(self.service, key)
        self._remove_from_index(key)
        logger.debug("자격증명 삭제: %s", key)

    def exists(self, key: str) -> bool:
        """자격증명 존재 여부 확인."""
        return self.get(key) is not None

    def list_keys(self) -> list[str]:
        """저장된 키 목록 반환."""
        raw = keyring.get_password(self.service, _KEYS_INDEX_KEY)
        if raw is None:
            return []
        return json.loads(raw)

    def _add_to_index(self, key: str) -> None:
        """키 목록 인덱스에 키 추가."""
        if key == _KEYS_INDEX_KEY:
            return
        keys = self.list_keys()
        if key not in keys:
            keys.append(key)
            keyring.set_password(self.service, _KEYS_INDEX_KEY, json.dumps(keys))

    def _remove_from_index(self, key: str) -> None:
        """키 목록 인덱스에서 키 제거."""
        if key == _KEYS_INDEX_KEY:
            return
        keys = self.list_keys()
        if key in keys:
            keys.remove(key)
            keyring.set_password(self.service, _KEYS_INDEX_KEY, json.dumps(keys))
