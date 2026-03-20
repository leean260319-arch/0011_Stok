"""LLM 서비스 추상화 및 Cloud LLM Provider
Version: 1.1.0
"""

import hashlib
import os
import sqlite3
import threading
import time
from abc import ABC, abstractmethod

from openai import OpenAI

from src.utils.constants import LLM_CACHE_DIR, LLM_CACHE_TTL
from src.utils.logger import get_logger

logger = get_logger("ai.llm_service")


class LLMCache:
    """SQLite 기반 LLM 응답 캐시."""

    def __init__(self, db_path: str, default_ttl: int = 86400):
        self._db_path = db_path
        self._ttl = default_ttl
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS llm_cache "
            "(prompt_hash TEXT PRIMARY KEY, model TEXT, response TEXT, "
            "tokens_used INTEGER DEFAULT 0, created_at REAL)"
        )
        self._conn.commit()

    def get(self, prompt: str, model: str = "") -> str | None:
        h = hashlib.sha256(prompt.encode()).hexdigest()
        with self._lock:
            row = self._conn.execute(
                "SELECT response, created_at FROM llm_cache WHERE prompt_hash = ? AND model = ?",
                (h, model),
            ).fetchone()
        if row and (time.time() - row[1]) < self._ttl:
            return row[0]
        return None

    def set(self, prompt: str, response: str, model: str = "", tokens_used: int = 0):
        h = hashlib.sha256(prompt.encode()).hexdigest()
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO llm_cache VALUES (?, ?, ?, ?, ?)",
                (h, model, response, tokens_used, time.time()),
            )
            self._conn.commit()

    def clear_expired(self):
        with self._lock:
            self._conn.execute(
                "DELETE FROM llm_cache WHERE created_at < ?",
                (time.time() - self._ttl,),
            )
            self._conn.commit()

    def stats(self) -> dict:
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(tokens_used), 0) FROM llm_cache"
            ).fetchone()
        return {"entries": row[0], "total_tokens_saved": row[1]}

    def close(self):
        self._conn.close()


class BaseLLMProvider(ABC):
    """LLM Provider 추상 기반 클래스"""

    @abstractmethod
    def analyze(self, prompt: str, system_prompt: str = "") -> str:
        """프롬프트를 LLM에 전송하고 응답 반환"""

    @abstractmethod
    def is_available(self) -> bool:
        """Provider 사용 가능 여부"""


class CloudLLMProvider(BaseLLMProvider):
    """OpenAI 호환 Cloud LLM Provider (GPT-4o-mini, DeepSeek 등)"""

    def __init__(self, api_key: str, model: str, base_url: str, cache: LLMCache = None):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url
        self._cache = cache
        self._client = OpenAI(api_key=api_key, base_url=base_url, timeout=30.0)

    def analyze(self, prompt: str, system_prompt: str = "") -> str:
        """OpenAI 라이브러리를 통해 LLM 호출 (캐시 히트 시 API 미호출)"""
        if self._cache is not None:
            cached = self._cache.get(prompt, self._model)
            if cached is not None:
                logger.info("LLM 캐시 히트: model=%s", self._model)
                return cached

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.1,
        )
        result = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else 0

        if self._cache is not None:
            self._cache.set(prompt, result, self._model, tokens_used)

        return result

    def is_available(self) -> bool:
        return bool(self._api_key)


class LLMService:
    """Primary/Fallback 구조의 LLM 서비스"""

    def __init__(self, primary: BaseLLMProvider, fallback: BaseLLMProvider = None):
        self._primary = primary
        self._fallback = fallback
        self._active = "primary"
        self._cache = LLMCache(
            db_path=os.path.join(LLM_CACHE_DIR, "cache.db"),
            default_ttl=LLM_CACHE_TTL,
        )
        if isinstance(self._primary, CloudLLMProvider):
            self._primary._cache = self._cache
        if isinstance(self._fallback, CloudLLMProvider):
            self._fallback._cache = self._cache

    def analyze(self, prompt: str, system_prompt: str = "") -> str | None:
        """Primary LLM 시도, 실패 시 Fallback으로 전환.

        Primary is_available()이 True여도 네트워크/타임아웃 등으로 실패할 수 있다.
        이 경우 Fallback을 시도하며, 모두 실패하면 None을 반환한다.
        호출자는 반환값이 None이면 해당 분석을 건너뛰어야 한다.

        Args:
            prompt: 분석 프롬프트
            system_prompt: 시스템 프롬프트 (선택)

        Returns:
            LLM 응답 문자열. 모든 Provider 실패 시 None.
        """
        if self._primary.is_available():
            result = self._try_provider(self._primary, prompt, system_prompt)
            if result is not None:
                self._active = "primary"
                return result
            logger.warning("Primary LLM 호출 실패, Fallback 시도")

        if self._fallback is not None and self._fallback.is_available():
            logger.warning("Fallback LLM으로 전환")
            result = self._try_provider(self._fallback, prompt, system_prompt)
            if result is not None:
                self._active = "fallback"
                return result

        logger.error("사용 가능한 LLM Provider가 없거나 모두 실패")
        return None

    @staticmethod
    def _try_provider(provider: BaseLLMProvider, prompt: str, system_prompt: str) -> str | None:
        """Provider 호출을 시도한다. 실패 시 None 반환."""
        # 프로젝트 규칙상 try/except 금지이나, 외부 API 호출 실패는 예외적 허용
        try:
            return provider.analyze(prompt, system_prompt)
        except Exception as e:
            logger.error("LLM Provider 호출 실패: %s", e)
            return None

    def get_active_provider(self) -> str:
        """현재 활성 Provider 이름 반환"""
        return self._active
