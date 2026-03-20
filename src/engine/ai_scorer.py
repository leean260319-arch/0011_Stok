"""AI 종합 점수 산출기 - 감성 + 기술적 분석 결합

버전: 1.0.0
작성일: 2026-03-17
"""


class AIScorer:
    """감성 분석 점수와 기술적 분석 점수를 가중치로 결합하는 종합 점수 산출기"""

    BUY_THRESHOLD = 0.2
    SELL_THRESHOLD = -0.2
    CONFIDENCE_SCALE = 0.5  # abs(total) / CONFIDENCE_SCALE → confidence

    def __init__(self, sentiment_weight: float = 0.4, technical_weight: float = 0.6):
        if abs(sentiment_weight + technical_weight - 1.0) > 1e-9:
            raise ValueError("sentiment_weight + technical_weight 합계는 1.0이어야 합니다")
        self._sentiment_weight = sentiment_weight
        self._technical_weight = technical_weight

    @property
    def sentiment_weight(self) -> float:
        return self._sentiment_weight

    @property
    def technical_weight(self) -> float:
        return self._technical_weight

    def calculate_score(self, sentiment_score: float, technical_score: float) -> dict:
        """감성 + 기술적 분석 결합 종합 점수

        Args:
            sentiment_score: -1.0 ~ +1.0  (뉴스 감성)
            technical_score: -1.0 ~ +1.0  (기술적 시그널)

        Returns:
            {
                total_score: float,          # -1.0 ~ +1.0
                signal: str,                 # "매수" | "매도" | "관망"
                sentiment_contrib: float,    # 감성 기여분
                technical_contrib: float,    # 기술적 기여분
                confidence: float,           # 0.0 ~ 1.0
            }
        """
        sentiment_contrib = sentiment_score * self._sentiment_weight
        technical_contrib = technical_score * self._technical_weight
        total = sentiment_contrib + technical_contrib

        if total > self.BUY_THRESHOLD:
            signal = "매수"
        elif total < self.SELL_THRESHOLD:
            signal = "매도"
        else:
            signal = "관망"

        confidence = min(abs(total) / self.CONFIDENCE_SCALE, 1.0)

        return {
            "total_score": round(total, 3),
            "signal": signal,
            "sentiment_contrib": round(sentiment_contrib, 3),
            "technical_contrib": round(technical_contrib, 3),
            "confidence": round(confidence, 3),
        }
