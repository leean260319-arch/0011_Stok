"""T043: 뉴스 감성분석기 테스트"""

import json
from unittest.mock import MagicMock
from src.ai.news_analyzer import (
    NewsAnalyzer,
    SENTIMENT_PROMPT,
    SENTIMENT_SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
)
from src.utils.constants import NEWS_CONTENT_MAX_CHARS


def _make_llm(response_dict: dict):
    """지정된 JSON을 반환하는 mock LLMService"""
    llm = MagicMock()
    llm.analyze.return_value = json.dumps(response_dict)
    return llm


class TestNewsAnalyzer:
    def test_analyze_sentiment_returns_dict(self):
        """analyze_sentiment가 dict를 반환하는지 확인"""
        llm = _make_llm({"score": 0.5, "label": "positive", "reason": "긍정적 뉴스"})
        analyzer = NewsAnalyzer(llm)
        result = analyzer.analyze_sentiment({"title": "테스트", "content_preview": "내용"})
        assert isinstance(result, dict)

    def test_analyze_sentiment_keys(self):
        """반환 dict가 score, label, reason 키를 포함하는지 확인"""
        llm = _make_llm({"score": 0.5, "label": "positive", "reason": "긍정적 뉴스"})
        analyzer = NewsAnalyzer(llm)
        result = analyzer.analyze_sentiment({"title": "테스트", "content_preview": "내용"})
        assert "score" in result
        assert "label" in result
        assert "reason" in result

    def test_analyze_sentiment_score_is_float(self):
        """score가 float 타입인지 확인"""
        llm = _make_llm({"score": 0.7, "label": "positive", "reason": "상승 기대"})
        analyzer = NewsAnalyzer(llm)
        result = analyzer.analyze_sentiment({"title": "뉴스", "content_preview": "내용"})
        assert isinstance(result["score"], float)

    def test_analyze_sentiment_positive(self):
        """긍정 분석 결과가 올바르게 반환되는지 확인"""
        llm = _make_llm({"score": 0.8, "label": "positive", "reason": "실적 개선"})
        analyzer = NewsAnalyzer(llm)
        result = analyzer.analyze_sentiment({"title": "실적 개선", "content_preview": "이익 증가"})
        assert result["score"] == 0.8
        assert result["label"] == "positive"

    def test_analyze_sentiment_negative(self):
        """부정 분석 결과가 올바르게 반환되는지 확인"""
        llm = _make_llm({"score": -0.6, "label": "negative", "reason": "손실 우려"})
        analyzer = NewsAnalyzer(llm)
        result = analyzer.analyze_sentiment({"title": "손실", "content_preview": "적자"})
        assert result["score"] == -0.6
        assert result["label"] == "negative"

    def test_analyze_sentiment_uses_summary_fallback(self):
        """content_preview 없을 때 summary를 사용하는지 확인"""
        llm = _make_llm({"score": 0.0, "label": "neutral", "reason": "중립"})
        analyzer = NewsAnalyzer(llm)
        analyzer.analyze_sentiment({"title": "뉴스", "summary": "RSS 요약"})
        call_args = llm.analyze.call_args[0][0]
        assert "RSS 요약" in call_args

    def test_analyze_sentiment_prompt_contains_title(self):
        """프롬프트에 기사 제목이 포함되는지 확인"""
        llm = _make_llm({"score": 0.3, "label": "positive", "reason": "이유"})
        analyzer = NewsAnalyzer(llm)
        analyzer.analyze_sentiment({"title": "삼성전자 호실적", "content_preview": "내용"})
        call_args = llm.analyze.call_args[0][0]
        assert "삼성전자 호실적" in call_args

    def test_analyze_batch_returns_list(self):
        """analyze_batch가 리스트를 반환하는지 확인"""
        llm = _make_llm({"score": 0.5, "label": "positive", "reason": "이유"})
        analyzer = NewsAnalyzer(llm)
        articles = [
            {"title": "뉴스1", "content_preview": "내용1"},
            {"title": "뉴스2", "content_preview": "내용2"},
        ]
        result = analyzer.analyze_batch(articles)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_analyze_batch_calls_analyze_for_each(self):
        """batch 처리 시 각 기사마다 LLM이 호출되는지 확인"""
        llm = _make_llm({"score": 0.1, "label": "neutral", "reason": "중립"})
        analyzer = NewsAnalyzer(llm)
        articles = [{"title": f"뉴스{i}", "content_preview": "내용"} for i in range(3)]
        analyzer.analyze_batch(articles)
        assert llm.analyze.call_count == 3

    def test_sentiment_prompt_constant_exists(self):
        """SENTIMENT_PROMPT 상수가 정의되어 있는지 확인"""
        assert isinstance(SENTIMENT_PROMPT, str)
        assert len(SENTIMENT_PROMPT) > 0
        assert "{title}" in SENTIMENT_PROMPT
        assert "{content}" in SENTIMENT_PROMPT

    def test_long_content_truncated(self):
        """1000자 뉴스가 500자로 절단되는지 확인"""
        llm = _make_llm({"score": 0.0, "label": "neutral", "reason": "중립"})
        analyzer = NewsAnalyzer(llm)
        long_content = "가" * 1000
        analyzer.analyze_sentiment({"title": "긴뉴스", "content_preview": long_content})
        call_args = llm.analyze.call_args[0][0]
        truncated = "가" * NEWS_CONTENT_MAX_CHARS + "... (이하 생략)"
        assert truncated in call_args

    def test_short_content_not_truncated(self):
        """200자 뉴스는 절단되지 않는지 확인"""
        llm = _make_llm({"score": 0.0, "label": "neutral", "reason": "중립"})
        analyzer = NewsAnalyzer(llm)
        short_content = "나" * 200
        analyzer.analyze_sentiment({"title": "짧은뉴스", "content_preview": short_content})
        call_args = llm.analyze.call_args[0][0]
        assert short_content in call_args
        assert "... (이하 생략)" not in call_args

    def test_sentiment_system_prompt_used(self):
        """analyze 호출 시 SENTIMENT_SYSTEM_PROMPT가 system_prompt로 전달되는지 확인"""
        llm = _make_llm({"score": 0.5, "label": "positive", "reason": "이유"})
        analyzer = NewsAnalyzer(llm)
        analyzer.analyze_sentiment({"title": "테스트", "content_preview": "내용"})
        _, kwargs = llm.analyze.call_args
        assert kwargs.get("system_prompt") == SENTIMENT_SYSTEM_PROMPT

    def test_few_shot_in_prompt(self):
        """프롬프트에 Few-shot 예제가 포함되는지 확인"""
        llm = _make_llm({"score": 0.0, "label": "neutral", "reason": "중립"})
        analyzer = NewsAnalyzer(llm)
        analyzer.analyze_sentiment({"title": "테스트", "content_preview": "내용"})
        call_args = llm.analyze.call_args[0][0]
        assert "예시 1" in call_args
        assert "예시 2" in call_args
        assert "예시 3" in call_args
