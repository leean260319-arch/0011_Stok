"""T014: 설정 관리자 - JSON 설정 파일 읽기/쓰기, 기본값 관리"""

# 버전 정보
# v1.0 - 2026-03-16: 신규 작성

import json
import os
import tempfile

from src.utils.constants import LLMConfig, RiskDefaults
from src.utils.logger import get_logger

logger = get_logger("config")

DEFAULT_CONFIG: dict = {
    "theme": "dark",
    "language": "ko",
    "ai": {
        "primary_model": LLMConfig.PRIMARY_MODEL,
        "fallback_model": LLMConfig.FALLBACK_MODEL,
        "primary_base_url": LLMConfig.PRIMARY_BASE_URL,
        "fallback_base_url": LLMConfig.FALLBACK_BASE_URL,
    },
    "risk": {
        "daily_loss_limit_pct": RiskDefaults.DAILY_LOSS_LIMIT_PCT,
        "max_position_pct": RiskDefaults.MAX_POSITION_PCT,
        "stop_loss_pct": RiskDefaults.STOP_LOSS_PCT,
        "take_profit_pct": RiskDefaults.TAKE_PROFIT_PCT,
        "max_concurrent_strategies": RiskDefaults.MAX_CONCURRENT_STRATEGIES,
    },
    "ui": {
        "left_panel_width": 250,
        "right_panel_width": 300,
        "show_left_panel": True,
        "show_right_panel": True,
        "font_size": 12,
        "ui_scale": 100,
    },
    "auto_trade": {
        "enabled": False,
        "start_time": "09:00",
        "end_time": "15:30",
    },
    "web_dashboard": {
        "enabled": True,
        "port": 8080,
        "username": "admin",
        "password": "",
    },
}


class ConfigManager:
    """JSON 설정 파일 읽기/쓰기 및 기본값 관리 클래스."""

    def __init__(self) -> None:
        import copy
        self._config: dict = copy.deepcopy(DEFAULT_CONFIG)

    def load(self, path: str) -> dict:
        """JSON 파일을 읽어 설정을 로드한다. 파일이 없으면 기본값을 반환한다."""
        import copy
        if not os.path.exists(path):
            self._config = copy.deepcopy(DEFAULT_CONFIG)
            return copy.deepcopy(DEFAULT_CONFIG)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self._config = data
        return data

    def save(self, path: str, config: dict) -> None:
        """설정 딕셔너리를 JSON 파일로 원자적으로 저장한다."""
        dir_path = os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=dir_path or ".", suffix=".tmp", text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)

    def get(self, key: str, default=None):
        """설정값을 조회한다. 점 표기법 지원 (예: 'ai.primary_model')."""
        parts = key.split(".")
        obj = self._config
        for part in parts:
            if not isinstance(obj, dict) or part not in obj:
                return default
            obj = obj[part]
        return obj

    def get_all(self) -> dict:
        """전체 설정 딕셔너리를 반환한다."""
        import copy
        return copy.deepcopy(self._config)

    def set(self, key: str, value) -> None:
        """설정값을 변경한다. 점 표기법 지원 (예: 'ai.primary_model')."""
        parts = key.split(".")
        obj = self._config
        for part in parts[:-1]:
            if part not in obj or not isinstance(obj[part], dict):
                obj[part] = {}
            obj = obj[part]
        obj[parts[-1]] = value
