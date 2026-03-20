"""ServiceContainer 테스트"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch


class FakeConfigManager:
    """테스트용 ConfigManager 대역."""

    def __init__(self, data=None):
        self._data = data or {}

    def get(self, key, default=None):
        parts = key.split(".")
        obj = self._data
        for part in parts:
            if not isinstance(obj, dict) or part not in obj:
                return default
            obj = obj[part]
        return obj

    def set(self, key, value):
        parts = key.split(".")
        obj = self._data
        for part in parts[:-1]:
            if part not in obj:
                obj[part] = {}
            obj = obj[part]
        obj[parts[-1]] = value


class TestServiceContainerInit:
    """ServiceContainer 초기화 테스트."""

    def test_init_stores_config(self):
        from src.service_container import ServiceContainer

        cfg = FakeConfigManager()
        sc = ServiceContainer(cfg)
        assert sc.config is cfg

    def test_all_properties_none_before_init(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())
        assert sc.db is None
        assert sc.bridge is None
        assert sc.llm_service is None
        assert sc.news_analyzer is None
        assert sc.sentiment_scorer is None
        assert sc.strategy_engine is None
        assert sc.risk_manager is None
        assert sc.ai_scorer is None
        assert sc.trade_logger is None


class TestServiceContainerBridge:
    """init_bridge 테스트."""

    def test_init_bridge_creates_instance(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())
        sc.init_bridge()
        assert sc.bridge is not None
        assert sc.bridge.is_connected is False


class TestServiceContainerEngine:
    """init_engine 테스트."""

    def test_init_engine_creates_all_components(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())
        sc.init_engine()
        assert sc.strategy_engine is not None
        assert sc.risk_manager is not None
        assert sc.ai_scorer is not None
        assert sc.trade_logger is not None

    def test_strategy_engine_has_default_strategies(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())
        sc.init_engine()
        names = [s.name for s in sc.strategy_engine.strategies]
        assert "momentum" in names
        assert "mean_reversion" in names


class TestServiceContainerAI:
    """init_ai 테스트."""

    def test_init_ai_creates_services(self):
        from src.service_container import ServiceContainer

        cfg = FakeConfigManager({"ai": {"primary_api_key": "test-key"}})
        sc = ServiceContainer(cfg)
        sc.init_ai()
        assert sc.llm_service is not None
        assert sc.news_analyzer is not None
        assert sc.sentiment_scorer is not None

    def test_init_ai_no_fallback_when_no_key(self):
        from src.service_container import ServiceContainer

        cfg = FakeConfigManager({"ai": {}})
        sc = ServiceContainer(cfg)
        sc.init_ai()
        assert sc.llm_service._fallback is None

    def test_init_ai_with_fallback(self):
        from src.service_container import ServiceContainer

        cfg = FakeConfigManager({
            "ai": {
                "primary_api_key": "pk",
                "fallback_api_key": "fk",
                "fallback_model": "deepseek-chat",
            }
        })
        sc = ServiceContainer(cfg)
        sc.init_ai()
        assert sc.llm_service._fallback is not None


class TestServiceContainerDB:
    """init_db 테스트."""

    def test_init_db_creates_manager(self, tmp_path):
        from src.service_container import ServiceContainer

        cfg = FakeConfigManager({"db": {"password": "test123"}})
        sc = ServiceContainer(cfg)

        mock_db = MagicMock()
        with patch("src.db.database.init_db", return_value=mock_db) as mock_init:
            sc.init_db()

        assert sc.db is mock_db
        mock_init.assert_called_once()


class TestServiceContainerShutdown:
    """shutdown 테스트."""

    def test_shutdown_closes_services(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())

        mock_trade_logger = MagicMock()
        mock_db = MagicMock()
        mock_bridge = MagicMock()
        mock_bridge.is_connected = True

        sc._trade_logger = mock_trade_logger
        sc._db = mock_db
        sc._bridge = mock_bridge

        sc.shutdown()

        mock_trade_logger.close.assert_called_once()
        mock_db.close.assert_called_once()
        mock_bridge.disconnect.assert_called_once()

    def test_shutdown_skips_none_services(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())
        # 모든 서비스가 None인 상태에서 shutdown 호출 - 에러 없어야 함
        sc.shutdown()

    def test_shutdown_skips_disconnected_bridge(self):
        from src.service_container import ServiceContainer

        sc = ServiceContainer(FakeConfigManager())
        mock_bridge = MagicMock()
        mock_bridge.is_connected = False
        sc._bridge = mock_bridge

        sc.shutdown()
        mock_bridge.disconnect.assert_not_called()
