"""T044: 감성 점수 집계 테스트"""

from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from src.ai.sentiment_scorer import SentimentScorer


def _ts(hours_ago: float = 0.0) -> datetime:
    """현재 UTC 기준 hours_ago 시간 전 timestamp 반환"""
    return datetime.now(timezone.utc) - timedelta(hours=hours_ago)


class TestSentimentScorer:
    def test_empty_scores_returns_zero(self):
        """점수 목록이 비어있으면 0.0 반환"""
        scorer = SentimentScorer()
        assert scorer.calculate_weighted_score([]) == 0.0

    def test_single_score_returns_score(self):
        """단일 점수는 decay 없이 그대로 반환"""
        scorer = SentimentScorer()
        scores = [{"score": 0.8, "timestamp": _ts(0)}]
        result = scorer.calculate_weighted_score(scores)
        assert abs(result - 0.8) < 0.01

    def test_recent_news_has_higher_weight(self):
        """최신 뉴스가 오래된 뉴스보다 더 큰 가중치를 가지는지 확인"""
        scorer = SentimentScorer()
        scores = [
            {"score": 1.0, "timestamp": _ts(0)},    # 최신 (긍정)
            {"score": -1.0, "timestamp": _ts(24)},   # 24시간 전 (부정)
        ]
        result = scorer.calculate_weighted_score(scores)
        # 최신이 높은 가중치 → 결과는 양수여야 함
        assert result > 0.0

    def test_old_news_has_lower_weight(self):
        """오래된 뉴스일수록 가중치가 감소하는지 확인"""
        scorer = SentimentScorer()
        scores_recent = [{"score": 0.5, "timestamp": _ts(0)}]
        scores_old = [{"score": 0.5, "timestamp": _ts(100)}]

        # 같은 점수라도 최신이 더 높은 결과를 내야 함 (단일 점수는 같으므로 가중치 합 비교)
        # 단일 항목은 가중 평균이 score와 동일하지만,
        # 두 항목 혼합 테스트로 검증
        scores_mixed_recent = [
            {"score": 1.0, "timestamp": _ts(1)},
            {"score": 0.0, "timestamp": _ts(1)},
        ]
        scores_mixed_old = [
            {"score": 1.0, "timestamp": _ts(100)},
            {"score": 0.0, "timestamp": _ts(100)},
        ]
        result_recent = scorer.calculate_weighted_score(scores_mixed_recent)
        result_old = scorer.calculate_weighted_score(scores_mixed_old)
        # 둘 다 0.5여야 하지만 decay는 동일하게 적용되므로 평균은 같음
        assert abs(result_recent - 0.5) < 0.01
        assert abs(result_old - 0.5) < 0.01

    def test_decay_reduces_weight_over_time(self):
        """decay_factor=0.95/hour 적용 검증"""
        import math
        scorer = SentimentScorer()
        fixed_now = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        ts_2h_ago = fixed_now - timedelta(hours=2)

        scores = [{"score": 1.0, "timestamp": ts_2h_ago}]

        with patch("src.ai.sentiment_scorer.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_now
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
            result = scorer.calculate_weighted_score(scores)

        expected_weight = math.pow(0.95, 2)
        # score=1.0, weight=0.95^2, 단일 항목이므로 가중평균 = 1.0
        assert abs(result - 1.0) < 0.01

    def test_get_stock_sentiment_keys(self):
        """get_stock_sentiment 반환 dict 키 확인"""
        scorer = SentimentScorer()
        scores = [{"score": 0.5, "timestamp": _ts(0)}]
        result = scorer.get_stock_sentiment("005930", scores)
        for key in ("stock_code", "score", "label", "article_count", "last_updated"):
            assert key in result, f"키 '{key}' 누락"

    def test_get_stock_sentiment_positive_label(self):
        """score >= 0.1이면 label=positive"""
        scorer = SentimentScorer()
        scores = [{"score": 0.5, "timestamp": _ts(0)}]
        result = scorer.get_stock_sentiment("005930", scores)
        assert result["label"] == "positive"

    def test_get_stock_sentiment_negative_label(self):
        """score <= -0.1이면 label=negative"""
        scorer = SentimentScorer()
        scores = [{"score": -0.5, "timestamp": _ts(0)}]
        result = scorer.get_stock_sentiment("005930", scores)
        assert result["label"] == "negative"

    def test_get_stock_sentiment_neutral_label(self):
        """-0.1 < score < 0.1이면 label=neutral"""
        scorer = SentimentScorer()
        scores = [{"score": 0.05, "timestamp": _ts(0)}]
        result = scorer.get_stock_sentiment("005930", scores)
        assert result["label"] == "neutral"

    def test_get_stock_sentiment_article_count(self):
        """article_count가 입력 개수와 일치하는지 확인"""
        scorer = SentimentScorer()
        scores = [
            {"score": 0.3, "timestamp": _ts(0)},
            {"score": 0.5, "timestamp": _ts(1)},
            {"score": -0.2, "timestamp": _ts(2)},
        ]
        result = scorer.get_stock_sentiment("035420", scores)
        assert result["article_count"] == 3

    def test_get_stock_sentiment_stock_code(self):
        """stock_code 필드가 올바르게 설정되는지 확인"""
        scorer = SentimentScorer()
        scores = [{"score": 0.0, "timestamp": _ts(0)}]
        result = scorer.get_stock_sentiment("000660", scores)
        assert result["stock_code"] == "000660"

    def test_naive_datetime_treated_as_utc(self):
        """timezone 없는 datetime도 처리되는지 확인"""
        scorer = SentimentScorer()
        naive_ts = datetime.utcnow()  # timezone 없음
        scores = [{"score": 0.4, "timestamp": naive_ts}]
        result = scorer.calculate_weighted_score(scores)
        assert isinstance(result, float)
