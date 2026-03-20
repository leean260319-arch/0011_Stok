"""TC01-01.T004 - 상수 정의 테스트"""
import pytest


class TestConstants:
    """src/utils/constants.py 단위 테스트"""

    def test_app_name_defined(self):
        from src.utils.constants import APP_NAME

        assert APP_NAME == "StokAI"

    def test_app_version_defined(self):
        from src.utils.constants import APP_VERSION

        assert isinstance(APP_VERSION, str)
        assert len(APP_VERSION.split(".")) >= 2

    def test_keyring_service_name(self):
        from src.utils.constants import KEYRING_SERVICE

        assert KEYRING_SERVICE == "StokAI"

    def test_db_filename(self):
        from src.utils.constants import DB_FILENAME

        assert DB_FILENAME.endswith(".db")

    def test_color_constants_defined(self):
        from src.utils.constants import Colors

        assert Colors.BACKGROUND == "#121212"
        assert Colors.SURFACE == "#1E1E1E"
        assert Colors.PRIMARY == "#FFD700"
        assert Colors.BULLISH == "#F04451"
        assert Colors.BEARISH == "#326AFF"
        assert Colors.TEXT_PRIMARY == "#E0E0E0"
        assert Colors.DANGER == "#FF1744"

    def test_api_throttle_limits(self):
        from src.utils.constants import API_RATE_PER_SEC, API_RATE_PER_HOUR

        assert API_RATE_PER_SEC == 5
        assert API_RATE_PER_HOUR == 1000

    def test_default_paths(self):
        from src.utils.constants import DEFAULT_LOG_DIR, DEFAULT_DB_DIR

        assert isinstance(DEFAULT_LOG_DIR, str)
        assert isinstance(DEFAULT_DB_DIR, str)

    def test_llm_config(self):
        from src.utils.constants import LLMConfig

        assert LLMConfig.PRIMARY_MODEL == "gpt-4o-mini"
        assert LLMConfig.FALLBACK_MODEL == "deepseek-chat"

    def test_risk_defaults(self):
        from src.utils.constants import RiskDefaults

        assert 0 < RiskDefaults.DAILY_LOSS_LIMIT_PCT <= 100
        assert 0 < RiskDefaults.MAX_POSITION_PCT <= 100
        assert RiskDefaults.STOP_LOSS_PCT > 0
        assert RiskDefaults.TAKE_PROFIT_PCT > 0
