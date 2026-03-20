"""StokAI 상수 정의 모듈"""

import os
import sys

APP_NAME = "StokAI"
APP_VERSION = "0.1.0"
KEYRING_SERVICE = "StokAI"
DB_FILENAME = "stokai.db"

DEFAULT_LOG_DIR = "logs"
DEFAULT_DB_DIR = "db"
DEFAULT_DATA_DIR = "data"
CONFIG_FILENAME = "config.json"


def get_app_dir() -> str:
    """앱 루트 디렉토리를 반환한다. PyInstaller 번들 시에도 동작한다."""
    if getattr(sys, "frozen", False):
        # PyInstaller 번들 exe: exe 파일이 위치한 디렉토리
        return os.path.dirname(sys.executable)
    # 개발 환경: src/utils/constants.py -> 프로젝트 루트
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


APP_DIR = get_app_dir()
DB_DIR = os.path.join(APP_DIR, DEFAULT_DB_DIR)
LOG_DIR = os.path.join(APP_DIR, DEFAULT_LOG_DIR)
DATA_DIR = os.path.join(APP_DIR, DEFAULT_DATA_DIR)
DB_PATH = os.path.join(DB_DIR, DB_FILENAME)
CONFIG_PATH = os.path.join(APP_DIR, CONFIG_FILENAME)

API_RATE_PER_SEC = 5
API_RATE_PER_HOUR = 1000

# LLM 캐시 설정
LLM_CACHE_TTL = 86400  # 24시간 (초)
LLM_CACHE_DIR = os.path.join(DATA_DIR, "cache")

# 뉴스 분석 토큰 절약 설정
NEWS_CONTENT_MAX_CHARS = 500  # 뉴스 내용 최대 글자수

# 토큰 예산 관리
LLM_DAILY_TOKEN_BUDGET = 100000  # 일일 토큰 예산
LLM_MONTHLY_TOKEN_BUDGET = 2000000  # 월간 토큰 예산


def get_local_ip() -> str:
    """로컬 네트워크 IP를 반환한다. 실패 시 127.0.0.1."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()
    except OSError:
        return "127.0.0.1"


def get_public_ip() -> str:
    """공인 IP를 반환한다. 외부 API로 조회. 실패 시 빈 문자열."""
    import urllib.request
    import urllib.error
    services = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com",
    ]
    for url in services:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "StokAI"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.read().decode().strip()
        except (urllib.error.URLError, OSError):
            continue
    return ""


class Colors:
    BACKGROUND = "#121212"
    SURFACE = "#1E1E1E"
    SURFACE_VARIANT = "#2A2A2A"
    PRIMARY = "#FFD700"
    BULLISH = "#F04451"
    BEARISH = "#326AFF"
    TEXT_PRIMARY = "#E0E0E0"
    TEXT_SECONDARY = "#9E9E9E"
    BORDER = "#333333"
    DANGER = "#FF1744"
    SUCCESS = "#00E676"
    WARNING = "#FFAB00"


class LLMConfig:
    PRIMARY_MODEL = "gpt-4o-mini"
    FALLBACK_MODEL = "deepseek-chat"
    PRIMARY_BASE_URL = "https://api.openai.com/v1"
    FALLBACK_BASE_URL = "https://api.deepseek.com/v1"


class RiskDefaults:
    DAILY_LOSS_LIMIT_PCT = 3.0
    MAX_POSITION_PCT = 20.0
    STOP_LOSS_PCT = 2.0
    TAKE_PROFIT_PCT = 5.0
    MAX_CONCURRENT_STRATEGIES = 5
