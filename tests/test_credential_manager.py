"""T009 CredentialManager 테스트
keyring은 unittest.mock.patch로 모킹 - OS 자격증명 저장소 접근 없음
"""
import json
from unittest.mock import MagicMock, patch

import pytest

from src.security.credential_manager import CredentialManager, _KEYS_INDEX_KEY
from src.utils.constants import KEYRING_SERVICE


@pytest.fixture()
def mock_keyring():
    """keyring 저장소를 dict로 모킹."""
    store: dict[tuple[str, str], str] = {}

    def set_password(service, key, value):
        store[(service, key)] = value

    def get_password(service, key):
        return store.get((service, key))

    def delete_password(service, key):
        store.pop((service, key), None)

    with patch("src.security.credential_manager.keyring") as mk:
        mk.set_password.side_effect = set_password
        mk.get_password.side_effect = get_password
        mk.delete_password.side_effect = delete_password
        yield mk, store


@pytest.fixture()
def manager(mock_keyring):
    mk, store = mock_keyring
    return CredentialManager(), store


class TestCredentialManagerSave:
    def test_save_stores_value(self, manager):
        cm, store = manager
        cm.save("api_key", "secret123")
        assert store[(KEYRING_SERVICE, "api_key")] == "secret123"

    def test_save_updates_index(self, manager):
        cm, store = manager
        cm.save("api_key", "secret123")
        index = json.loads(store[(KEYRING_SERVICE, _KEYS_INDEX_KEY)])
        assert "api_key" in index

    def test_save_multiple_keys(self, manager):
        cm, store = manager
        cm.save("key_a", "val_a")
        cm.save("key_b", "val_b")
        index = json.loads(store[(KEYRING_SERVICE, _KEYS_INDEX_KEY)])
        assert "key_a" in index
        assert "key_b" in index


class TestCredentialManagerGet:
    def test_get_returns_saved_value(self, manager):
        cm, _ = manager
        cm.save("token", "abc")
        assert cm.get("token") == "abc"

    def test_get_returns_none_for_missing(self, manager):
        cm, _ = manager
        assert cm.get("nonexistent") is None


class TestCredentialManagerDelete:
    def test_delete_removes_value(self, manager):
        cm, store = manager
        cm.save("to_delete", "val")
        cm.delete("to_delete")
        assert (KEYRING_SERVICE, "to_delete") not in store

    def test_delete_removes_from_index(self, manager):
        cm, store = manager
        cm.save("to_delete", "val")
        cm.delete("to_delete")
        index = json.loads(store[(KEYRING_SERVICE, _KEYS_INDEX_KEY)])
        assert "to_delete" not in index


class TestCredentialManagerExists:
    def test_exists_true_after_save(self, manager):
        cm, _ = manager
        cm.save("exists_key", "v")
        assert cm.exists("exists_key") is True

    def test_exists_false_for_missing(self, manager):
        cm, _ = manager
        assert cm.exists("no_such_key") is False

    def test_exists_false_after_delete(self, manager):
        cm, _ = manager
        cm.save("del_key", "v")
        cm.delete("del_key")
        assert cm.exists("del_key") is False


class TestCredentialManagerListKeys:
    def test_list_keys_empty_initially(self, manager):
        cm, _ = manager
        assert cm.list_keys() == []

    def test_list_keys_contains_saved_keys(self, manager):
        cm, _ = manager
        cm.save("k1", "v1")
        cm.save("k2", "v2")
        keys = cm.list_keys()
        assert "k1" in keys
        assert "k2" in keys

    def test_list_keys_excludes_index_key(self, manager):
        cm, _ = manager
        cm.save("some_key", "v")
        assert _KEYS_INDEX_KEY not in cm.list_keys()

    def test_list_keys_no_duplicates(self, manager):
        cm, _ = manager
        cm.save("dup_key", "v1")
        cm.save("dup_key", "v2")
        keys = cm.list_keys()
        assert keys.count("dup_key") == 1
