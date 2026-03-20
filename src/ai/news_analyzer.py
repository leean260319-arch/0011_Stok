"""뉴스 감성분석기
Version: 1.1.0
"""

import json
from src.utils.logger import get_logger
from src.utils.constants import NEWS_CONTENT_MAX_CHARS

logger = get_logger("ai.news_analyzer")

SENTIMENT_SYSTEM_PROMPT = """당신은 25년 경력의 한국 주식시장 전문 금융 분석가입니다.
KOSPI/KOSDAQ 시장의 뉴스가 단기(1-5일) 주가에 미치는 영향을 분석합니다.
다음 관점에서 종합적으로 판단하세요:
1) 기업 실적/재무 영향
2) 산업/섹터 트렌드
3) 외국인/기관 수급 영향
4) 거시경제/정책 영향
근거가 불충분하면 neutral(0.0)로 판단하세요.
반드시 JSON 형식만 반환하세요."""

FEW_SHOT_EXAMPLES = """
[예시 1]
제목: 삼성전자, 3분기 영업이익 12조원... 전년비 40% 증가
내용: 반도체 수요 회복과 AI 칩 판매 호조로 역대급 실적 달성
결과: {"score": 0.8, "label": "positive", "reason": "영업이익 40% 증가는 강한 실적 모멘텀"}

[예시 2]
제목: 반도체 업황, 하반기 둔화 본격화 전망
내용: 글로벌 수요 감소와 재고 조정으로 하반기 업황 악화 우려
결과: {"score": -0.5, "label": "negative", "reason": "업황 둔화 전망은 섹터 전체 부정적 영향"}

[예시 3]
제목: 한국은행, 기준금리 3.25% 동결 결정
내용: 시장 예상에 부합하는 동결 결정, 향후 인하 가능성 시사
결과: {"score": 0.1, "label": "neutral", "reason": "예상 부합 동결로 시장 영향 제한적"}
"""

SENTIMENT_PROMPT = """다음 뉴스 기사를 분석하여 주식 투자 관점에서 감성 점수를 JSON 형식으로 반환하세요.

아래 예시를 참고하세요:
{few_shot_examples}
제목: {title}
내용: {content}

응답 형식 (JSON만 반환, 다른 텍스트 없음):
{{
  "score": <-1.0 ~ +1.0 사이의 실수. -1.0=매우 부정, 0.0=중립, +1.0=매우 긍정>,
  "label": <"positive" | "neutral" | "negative">,
  "reason": <감성 판단 근거 한 문장>
}}"""


class NewsAnalyzer:
    """LLM 기반 뉴스 감성분석기"""

    def __init__(self, llm_service):
        """
        Args:
            llm_service: LLMService 인스턴스
        """
        self._llm = llm_service

    def _extract_json(self, raw: str) -> dict:
        """LLM 응답에서 JSON을 추출한다. 코드블록 래핑 제거."""
        text = raw.strip()
        # 마크다운 코드블록 제거
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [line for line in lines if not line.strip().startswith("```")]
            text = "\n".join(lines).strip()
        # JSON 객체 부분만 추출 (첫 { 부터 마지막 } 까지)
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return {"score": 0, "label": "neutral", "reason": "분석 실패"}
        text = text[start:end + 1]
        result = json.loads(text)
        return result

    def analyze_sentiment(self, article: dict) -> dict:
        """단일 뉴스 기사 감성 분석

        Args:
            article: 뉴스 기사 dict (title, content_preview 또는 summary 포함)

        Returns:
            dict with keys: score (float), label (str), reason (str)
        """
        title = article.get("title", "")
        content_preview = article.get("content_preview", article.get("summary", ""))

        # 뉴스 내용 토큰 절약을 위한 절단
        if len(content_preview) > NEWS_CONTENT_MAX_CHARS:
            logger.debug("뉴스 내용 절단: %d자 -> %d자", len(content_preview), NEWS_CONTENT_MAX_CHARS)
            content_preview = content_preview[:NEWS_CONTENT_MAX_CHARS] + "... (이하 생략)"

        prompt = SENTIMENT_PROMPT.format(
            few_shot_examples=FEW_SHOT_EXAMPLES,
            title=title,
            content=content_preview,
        )
        raw_response = self._llm.analyze(prompt, system_prompt=SENTIMENT_SYSTEM_PROMPT)
        if raw_response is None:
            logger.warning("LLM 응답 없음, 중립 반환")
            return {"score": 0.0, "label": "neutral", "reason": "LLM 응답 없음"}

        parsed = self._extract_json(raw_response)
        score = float(parsed.get("score", 0))
        label = str(parsed.get("label", "neutral"))
        reason = str(parsed.get("reason", ""))

        logger.debug("감성분석 완료: score=%.2f, label=%s", score, label)
        return {"score": score, "label": label, "reason": reason}

    def analyze_batch(self, articles: list[dict]) -> list[dict]:
        """뉴스 기사 목록 일괄 감성 분석

        Args:
            articles: 뉴스 기사 목록

        Returns:
            각 기사의 감성 분석 결과 목록
        """
        results = []
        for article in articles:
            result = self.analyze_sentiment(article)
            results.append(result)
        logger.info("배치 감성분석 완료: %d건", len(results))
        return results
