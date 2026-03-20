"""감성 점수 집계기
Version: 1.0.0
"""

import math
from datetime import datetime, timezone
from src.utils.logger import get_logger

logger = get_logger("ai.sentiment_scorer")

DECAY_FACTOR_PER_HOUR = 0.95


class SentimentScorer:
    """시간 가중 감성 점수 집계기"""

    def calculate_weighted_score(self, scores: list[dict]) -> float:
        """시간 가중 평균 감성 점수 계산

        각 항목의 timestamp를 기준으로 현재 시각에서 경과한 시간(시간 단위)에 따라
        decay_factor=0.95/hour 로 가중치를 적감합니다.

        Args:
            scores: 감성 점수 목록. 각 항목은 score(float)와 timestamp(datetime) 필드 필요

        Returns:
            가중 평균 점수 (float). 항목이 없으면 0.0
        """
        if not scores:
            return 0.0

        now = datetime.now(timezone.utc)
        total_weight = 0.0
        weighted_sum = 0.0

        for item in scores:
            ts: datetime = item["timestamp"]
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            elapsed_hours = (now - ts).total_seconds() / 3600.0
            weight = math.pow(DECAY_FACTOR_PER_HOUR, elapsed_hours)
            weighted_sum += item["score"] * weight
            total_weight += weight

        if total_weight == 0.0:
            return 0.0

        return weighted_sum / total_weight

    def get_stock_sentiment(self, stock_code: str, scores: list[dict]) -> dict:
        """종목별 최종 감성 요약 반환

        Args:
            stock_code: 종목코드
            scores: 감성 점수 목록

        Returns:
            dict with keys: stock_code, score, label, article_count, last_updated
        """
        score = self.calculate_weighted_score(scores)

        if score >= 0.1:
            label = "positive"
        elif score <= -0.1:
            label = "negative"
        else:
            label = "neutral"

        last_updated = datetime.now(timezone.utc).isoformat()

        logger.info("종목 %s 감성: score=%.3f, label=%s, 기사수=%d", stock_code, score, label, len(scores))

        return {
            "stock_code": stock_code,
            "score": score,
            "label": label,
            "article_count": len(scores),
            "last_updated": last_updated,
        }
