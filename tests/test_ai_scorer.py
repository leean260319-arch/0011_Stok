"""T049: AIScorer 테스트 - 감성 + 기술적 분석 결합 종합 점수"""
import pytest

from src.engine.ai_scorer import AIScorer


@pytest.fixture
def scorer() -> AIScorer:
    return AIScorer()


# ---------------------------------------------------------------------------
# T049: 초기화 테스트
# ---------------------------------------------------------------------------

class TestAIScorerInit:
    def test_default_weights(self, scorer):
        assert scorer.sentiment_weight == 0.4
        assert scorer.technical_weight == 0.6

    def test_custom_weights(self):
        s = AIScorer(sentiment_weight=0.3, technical_weight=0.7)
        assert s.sentiment_weight == 0.3
        assert s.technical_weight == 0.7

    def test_invalid_weights_raise(self):
        with pytest.raises(ValueError, match="합계는 1.0"):
            AIScorer(sentiment_weight=0.5, technical_weight=0.6)

    def test_equal_weights(self):
        s = AIScorer(sentiment_weight=0.5, technical_weight=0.5)
        assert s.sentiment_weight == 0.5


# ---------------------------------------------------------------------------
# T049: 점수 계산 구조 테스트
# ---------------------------------------------------------------------------

class TestAIScorerStructure:
    def test_calculate_returns_dict(self, scorer):
        result = scorer.calculate_score(0.5, 0.5)
        assert isinstance(result, dict)

    def test_result_has_total_score(self, scorer):
        result = scorer.calculate_score(0.5, 0.5)
        assert "total_score" in result

    def test_result_has_signal(self, scorer):
        result = scorer.calculate_score(0.5, 0.5)
        assert "signal" in result

    def test_result_has_sentiment_contrib(self, scorer):
        result = scorer.calculate_score(0.5, 0.5)
        assert "sentiment_contrib" in result

    def test_result_has_technical_contrib(self, scorer):
        result = scorer.calculate_score(0.5, 0.5)
        assert "technical_contrib" in result

    def test_result_has_confidence(self, scorer):
        result = scorer.calculate_score(0.5, 0.5)
        assert "confidence" in result

    def test_signal_valid_value(self, scorer):
        for s, t in [(0.8, 0.8), (-0.8, -0.8), (0.0, 0.0)]:
            result = scorer.calculate_score(s, t)
            assert result["signal"] in {"매수", "매도", "관망"}


# ---------------------------------------------------------------------------
# T049: 점수 계산 로직 테스트
# ---------------------------------------------------------------------------

class TestAIScorerLogic:
    def test_both_positive_gives_buy(self, scorer):
        result = scorer.calculate_score(0.8, 0.8)
        assert result["signal"] == "매수"
        assert result["total_score"] > 0

    def test_both_negative_gives_sell(self, scorer):
        result = scorer.calculate_score(-0.8, -0.8)
        assert result["signal"] == "매도"
        assert result["total_score"] < 0

    def test_neutral_gives_hold(self, scorer):
        result = scorer.calculate_score(0.0, 0.0)
        assert result["signal"] == "관망"
        assert result["total_score"] == 0.0

    def test_total_score_formula(self, scorer):
        s, t = 0.6, 0.4
        result = scorer.calculate_score(s, t)
        expected = round(s * 0.4 + t * 0.6, 3)
        assert result["total_score"] == expected

    def test_sentiment_contrib_formula(self, scorer):
        result = scorer.calculate_score(0.5, 0.3)
        assert result["sentiment_contrib"] == round(0.5 * 0.4, 3)

    def test_technical_contrib_formula(self, scorer):
        result = scorer.calculate_score(0.5, 0.3)
        assert result["technical_contrib"] == round(0.3 * 0.6, 3)

    def test_contrib_sum_equals_total(self, scorer):
        result = scorer.calculate_score(0.7, -0.2)
        assert abs(result["sentiment_contrib"] + result["technical_contrib"] - result["total_score"]) < 1e-6

    def test_confidence_max_one(self, scorer):
        result = scorer.calculate_score(1.0, 1.0)
        assert result["confidence"] <= 1.0

    def test_confidence_min_zero(self, scorer):
        result = scorer.calculate_score(0.0, 0.0)
        assert result["confidence"] == 0.0

    def test_confidence_proportional(self, scorer):
        low = scorer.calculate_score(0.1, 0.1)
        high = scorer.calculate_score(0.8, 0.8)
        assert high["confidence"] > low["confidence"]

    def test_total_score_rounded(self, scorer):
        result = scorer.calculate_score(0.333, 0.666)
        assert result["total_score"] == round(result["total_score"], 3)

    def test_signal_threshold_buy(self, scorer):
        """score == 0.201 → 매수"""
        # sentiment=0.5, technical=0.0 → 0.5*0.4=0.2 (관망 경계)
        # sentiment=0.6, technical=0.0 → 0.6*0.4=0.24 → 매수
        result = scorer.calculate_score(0.6, 0.0)
        assert result["signal"] == "매수"

    def test_signal_threshold_sell(self, scorer):
        result = scorer.calculate_score(-0.6, 0.0)
        assert result["signal"] == "매도"

    def test_mixed_signals_hold(self, scorer):
        """강한 매수 감성 + 강한 매도 기술적 → 상쇄 후 관망"""
        result = scorer.calculate_score(0.5, -0.3)
        # 0.5*0.4 + (-0.3)*0.6 = 0.2 - 0.18 = 0.02 → 관망
        assert result["signal"] == "관망"

    def test_custom_weight_scorer(self):
        s = AIScorer(sentiment_weight=0.7, technical_weight=0.3)
        result = s.calculate_score(0.5, 0.5)
        expected_total = round(0.5 * 0.7 + 0.5 * 0.3, 3)
        assert result["total_score"] == expected_total
