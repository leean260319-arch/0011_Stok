"""T014: ConfigManager 테스트"""
import json
import pytest

from src.config import ConfigManager


class TestConfigManager:
    """ConfigManager 기본 동작 테스트"""

    def test_default_config_exists(self):
        """DEFAULT_CONFIG 딕셔너리가 존재해야 한다"""
        from src.config import DEFAULT_CONFIG
        assert isinstance(DEFAULT_CONFIG, dict)
        assert len(DEFAULT_CONFIG) > 0

    def test_load_missing_file_returns_defaults(self, tmp_path):
        """존재하지 않는 파일 로드 시 기본값 반환"""
        mgr = ConfigManager()
        result = mgr.load(str(tmp_path / "nonexistent.json"))
        from src.config import DEFAULT_CONFIG
        assert result == DEFAULT_CONFIG

    def test_load_existing_file(self, tmp_path):
        """존재하는 JSON 파일을 정상 로드해야 한다"""
        cfg_path = tmp_path / "config.json"
        data = {"theme": "dark", "ai": {"primary_model": "gpt-4o"}}
        cfg_path.write_text(json.dumps(data), encoding="utf-8")
        mgr = ConfigManager()
        result = mgr.load(str(cfg_path))
        assert result["theme"] == "dark"
        assert result["ai"]["primary_model"] == "gpt-4o"

    def test_save_and_reload(self, tmp_path):
        """save() 후 load()하면 동일한 데이터를 반환해야 한다"""
        cfg_path = str(tmp_path / "cfg.json")
        mgr = ConfigManager()
        mgr.load(cfg_path)
        mgr.set("theme", "light")
        mgr.save(cfg_path, mgr._config)

        mgr2 = ConfigManager()
        result = mgr2.load(cfg_path)
        assert result["theme"] == "light"

    def test_get_simple_key(self, tmp_path):
        """단순 키로 설정값 조회"""
        mgr = ConfigManager()
        mgr.load(str(tmp_path / "none.json"))
        mgr.set("theme", "dark")
        assert mgr.get("theme") == "dark"

    def test_get_dot_notation(self, tmp_path):
        """점 표기법으로 중첩 설정값 조회"""
        mgr = ConfigManager()
        mgr.load(str(tmp_path / "none.json"))
        mgr.set("ai.primary_model", "gpt-4o-mini")
        assert mgr.get("ai.primary_model") == "gpt-4o-mini"

    def test_get_missing_key_returns_default(self, tmp_path):
        """존재하지 않는 키는 default 반환"""
        mgr = ConfigManager()
        mgr.load(str(tmp_path / "none.json"))
        assert mgr.get("nonexistent", "fallback") == "fallback"
        assert mgr.get("nonexistent") is None

    def test_set_dot_notation(self, tmp_path):
        """점 표기법으로 중첩 키 설정"""
        mgr = ConfigManager()
        mgr.load(str(tmp_path / "none.json"))
        mgr.set("a.b.c", 42)
        assert mgr.get("a.b.c") == 42

    def test_save_creates_file(self, tmp_path):
        """save()가 파일을 생성해야 한다"""
        cfg_path = str(tmp_path / "out.json")
        mgr = ConfigManager()
        mgr.load(str(tmp_path / "none.json"))
        mgr.save(cfg_path, mgr._config)
        assert (tmp_path / "out.json").exists()

    def test_save_valid_json(self, tmp_path):
        """save()가 유효한 JSON을 저장해야 한다"""
        cfg_path = str(tmp_path / "valid.json")
        mgr = ConfigManager()
        mgr.load(str(tmp_path / "none.json"))
        mgr.set("key", "value")
        mgr.save(cfg_path, mgr._config)
        with open(cfg_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["key"] == "value"
