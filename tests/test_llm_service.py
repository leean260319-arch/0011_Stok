"""T040+T041: LLM 서비스 추상화 및 CloudLLMProvider 테스트"""

import os
import time
from unittest.mock import MagicMock, patch

import pytest

from src.ai.llm_service import BaseLLMProvider, CloudLLMProvider, LLMCache, LLMService


class ConcreteProvider(BaseLLMProvider):
    """테스트용 구체 Provider"""

    def __init__(self, response: str, available: bool = True):
        self._response = response
        self._available = available

    def analyze(self, prompt: str, system_prompt: str = "") -> str:
        return self._response

    def is_available(self) -> bool:
        return self._available


class TestCloudLLMProvider:
    def test_is_available_true_with_key(self):
        """API 키가 있으면 is_available True"""
        with patch("src.ai.llm_service.OpenAI"):
            provider = CloudLLMProvider(api_key="sk-test", model="gpt-4o-mini", base_url="https://api.openai.com/v1")
        assert provider.is_available() is True

    def test_is_available_false_without_key(self):
        """API 키가 없으면 is_available False"""
        with patch("src.ai.llm_service.OpenAI"):
            provider = CloudLLMProvider(api_key="", model="gpt-4o-mini", base_url="https://api.openai.com/v1")
        assert provider.is_available() is False

    def test_analyze_calls_openai(self):
        """analyze가 OpenAI client를 호출하는지 확인"""
        mock_message = MagicMock()
        mock_message.content = "분석 결과"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.ai.llm_service.OpenAI", return_value=mock_client):
            provider = CloudLLMProvider(api_key="sk-test", model="gpt-4o-mini", base_url="https://api.openai.com/v1")
            result = provider.analyze("테스트 프롬프트")

        assert result == "분석 결과"

    def test_analyze_passes_prompt_as_user_message(self):
        """프롬프트가 user role로 전달되는지 확인"""
        mock_message = MagicMock()
        mock_message.content = "결과"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.ai.llm_service.OpenAI", return_value=mock_client):
            provider = CloudLLMProvider(api_key="sk-test", model="gpt-4o-mini", base_url="https://api.openai.com/v1")
            provider.analyze("내 프롬프트")

        call_kwargs = mock_client.chat.completions.create.call_args
        messages = call_kwargs.kwargs.get("messages") or call_kwargs.args[0] if call_kwargs.args else call_kwargs.kwargs["messages"]
        # kwargs로 전달된 경우
        kwargs = call_kwargs.kwargs
        assert kwargs["messages"][0]["role"] == "user"
        assert kwargs["messages"][0]["content"] == "내 프롬프트"


class TestLLMService:
    def test_analyze_uses_primary_when_available(self):
        """Primary 사용 가능 시 primary가 호출되는지 확인"""
        primary = ConcreteProvider("primary 응답")
        fallback = ConcreteProvider("fallback 응답")
        service = LLMService(primary, fallback)

        result = service.analyze("프롬프트")
        assert result == "primary 응답"

    def test_analyze_uses_fallback_when_primary_unavailable(self):
        """Primary 불가 시 fallback이 호출되는지 확인"""
        primary = ConcreteProvider("primary 응답", available=False)
        fallback = ConcreteProvider("fallback 응답")
        service = LLMService(primary, fallback)

        result = service.analyze("프롬프트")
        assert result == "fallback 응답"

    def test_get_active_provider_primary(self):
        """primary 사용 후 active가 'primary'인지 확인"""
        primary = ConcreteProvider("응답")
        service = LLMService(primary)
        service.analyze("프롬프트")
        assert service.get_active_provider() == "primary"

    def test_get_active_provider_fallback(self):
        """fallback 사용 후 active가 'fallback'인지 확인"""
        primary = ConcreteProvider("응답", available=False)
        fallback = ConcreteProvider("fallback 응답")
        service = LLMService(primary, fallback)
        service.analyze("프롬프트")
        assert service.get_active_provider() == "fallback"

    def test_returns_none_when_no_provider_available(self):
        """사용 가능한 provider 없으면 None 반환"""
        primary = ConcreteProvider("응답", available=False)
        fallback = ConcreteProvider("fallback", available=False)
        service = LLMService(primary, fallback)

        result = service.analyze("프롬프트")
        assert result is None

    def test_returns_none_without_fallback_when_primary_unavailable(self):
        """fallback 없고 primary 불가 시 None 반환"""
        primary = ConcreteProvider("응답", available=False)
        service = LLMService(primary)

        result = service.analyze("프롬프트")
        assert result is None

    def test_base_provider_is_abstract(self):
        """BaseLLMProvider를 직접 인스턴스화할 수 없는지 확인"""
        with pytest.raises(TypeError):
            BaseLLMProvider()


class TestLLMCache:
    def _make_cache(self, tmp_path, ttl=86400):
        db_path = os.path.join(str(tmp_path), "test_cache.db")
        return LLMCache(db_path=db_path, default_ttl=ttl)

    def test_llm_cache_set_and_get(self, tmp_path):
        """저장 후 동일 프롬프트/모델로 조회 시 캐시된 응답 반환"""
        cache = self._make_cache(tmp_path)
        cache.set("테스트 프롬프트", "응답 텍스트", model="gpt-4o-mini", tokens_used=50)
        result = cache.get("테스트 프롬프트", model="gpt-4o-mini")
        assert result == "응답 텍스트"
        cache.close()

    def test_llm_cache_expired(self, tmp_path):
        """TTL 만료 시 None 반환"""
        cache = self._make_cache(tmp_path, ttl=1)
        cache.set("만료 프롬프트", "만료 응답", model="gpt-4o-mini")
        time.sleep(1.1)
        result = cache.get("만료 프롬프트", model="gpt-4o-mini")
        assert result is None
        cache.close()

    def test_llm_cache_stats(self, tmp_path):
        """통계 확인: entries 수 및 tokens_saved 합산"""
        cache = self._make_cache(tmp_path)
        cache.set("프롬프트1", "응답1", model="gpt-4o-mini", tokens_used=30)
        cache.set("프롬프트2", "응답2", model="gpt-4o-mini", tokens_used=70)
        stats = cache.stats()
        assert stats["entries"] == 2
        assert stats["total_tokens_saved"] == 100
        cache.close()

    def test_cloud_provider_uses_cache(self, tmp_path):
        """캐시 히트 시 OpenAI API 미호출 확인"""
        db_path = os.path.join(str(tmp_path), "test_cache.db")
        cache = LLMCache(db_path=db_path)
        cache.set("캐시된 프롬프트", "캐시 응답", model="gpt-4o-mini")

        mock_client = MagicMock()
        with patch("src.ai.llm_service.OpenAI", return_value=mock_client):
            provider = CloudLLMProvider(
                api_key="sk-test",
                model="gpt-4o-mini",
                base_url="https://api.openai.com/v1",
                cache=cache,
            )
            result = provider.analyze("캐시된 프롬프트")

        assert result == "캐시 응답"
        mock_client.chat.completions.create.assert_not_called()
        cache.close()
