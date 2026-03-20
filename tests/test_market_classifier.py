"""T-MC: MarketClassifier 테스트 - ADX + SMA + 볼린저밴드 기반 시장 레짐 분류

버전: 1.0.0
작성일: 2026-03-17
"""
import numpy as np
import pandas as pd
import pytest

from src.engine.chart_analyzer import ChartAnalyzer
from src.engine.market_classifier import MarketClassifier, MarketRegime


# ---------------------------------------------------------------------------
# 헬퍼: OHLCV 데이터 생성
# ---------------------------------------------------------------------------

def make_sample_ohlcv(n: int = 100) -> pd.DataFrame:
    np.random.seed(42)
    close = 50000 + np.cumsum(np.random.randn(n) * 500)
    return pd.DataFrame({
        "open": close + np.random.randn(n) * 100,
        "high": close + abs(np.random.randn(n) * 300),
        "low": close - abs(np.random.randn(n) * 300),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


def make_strong_uptrend_ohlcv(n: int = 100) -> pd.DataFrame:
    """강한 상승추세 데이터 (높은 ADX, SMA20 > SMA50)"""
    np.random.seed(10)
    close = 10000 + np.cumsum(abs(np.random.randn(n) * 1000))
    return pd.DataFrame({
        "open": close - abs(np.random.randn(n) * 50),
        "high": close + abs(np.random.randn(n) * 200),
        "low": close - abs(np.random.randn(n) * 100),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


def make_strong_downtrend_ohlcv(n: int = 100) -> pd.DataFrame:
    """강한 하락추세 데이터 (높은 ADX, SMA20 < SMA50)"""
    np.random.seed(20)
    close = 100000 - np.cumsum(abs(np.random.randn(n) * 1000))
    close = np.maximum(close, 1000)
    return pd.DataFrame({
        "open": close + abs(np.random.randn(n) * 50),
        "high": close + abs(np.random.randn(n) * 100),
        "low": close - abs(np.random.randn(n) * 200),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


def make_ranging_ohlcv(n: int = 200) -> pd.DataFrame:
    """횡보장 데이터 (낮은 ADX, 좁은 볼린저밴드)"""
    np.random.seed(30)
    # 50000 주변에서 미세한 변동만
    close = 50000 + np.random.randn(n) * 50
    return pd.DataFrame({
        "open": close + np.random.randn(n) * 10,
        "high": close + abs(np.random.randn(n) * 20),
        "low": close - abs(np.random.randn(n) * 20),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


@pytest.fixture
def sample_classifier() -> MarketClassifier:
    ca = ChartAnalyzer(make_sample_ohlcv())
    return MarketClassifier(ca)


@pytest.fixture
def uptrend_classifier() -> MarketClassifier:
    ca = ChartAnalyzer(make_strong_uptrend_ohlcv())
    return MarketClassifier(ca)


@pytest.fixture
def downtrend_classifier() -> MarketClassifier:
    ca = ChartAnalyzer(make_strong_downtrend_ohlcv())
    return MarketClassifier(ca)


@pytest.fixture
def ranging_classifier() -> MarketClassifier:
    ca = ChartAnalyzer(make_ranging_ohlcv())
    return MarketClassifier(ca)


# ---------------------------------------------------------------------------
# MarketRegime 상수 테스트
# ---------------------------------------------------------------------------

class TestMarketRegime:
    def test_trending_up_value(self):
        assert MarketRegime.TRENDING_UP == "trending_up"

    def test_trending_down_value(self):
        assert MarketRegime.TRENDING_DOWN == "trending_down"

    def test_ranging_value(self):
        assert MarketRegime.RANGING == "ranging"


# ---------------------------------------------------------------------------
# MarketClassifier 초기화 테스트
# ---------------------------------------------------------------------------

class TestMarketClassifierInit:
    def test_init_stores_analyzer(self):
        ca = ChartAnalyzer(make_sample_ohlcv())
        mc = MarketClassifier(ca)
        assert mc._analyzer is ca

    def test_init_with_chart_analyzer(self, sample_classifier):
        assert sample_classifier._analyzer is not None


# ---------------------------------------------------------------------------
# classify() 반환 구조 테스트
# ---------------------------------------------------------------------------

class TestClassifyStructure:
    def test_classify_returns_dict(self, sample_classifier):
        result = sample_classifier.classify()
        assert isinstance(result, dict)

    def test_classify_has_regime_key(self, sample_classifier):
        result = sample_classifier.classify()
        assert "regime" in result

    def test_classify_has_confidence_key(self, sample_classifier):
        result = sample_classifier.classify()
        assert "confidence" in result

    def test_classify_has_indicators_key(self, sample_classifier):
        result = sample_classifier.classify()
        assert "indicators" in result

    def test_classify_has_recommended_strategies_key(self, sample_classifier):
        result = sample_classifier.classify()
        assert "recommended_strategies" in result

    def test_regime_is_valid_string(self, sample_classifier):
        result = sample_classifier.classify()
        assert result["regime"] in {
            MarketRegime.TRENDING_UP,
            MarketRegime.TRENDING_DOWN,
            MarketRegime.RANGING,
        }

    def test_confidence_is_float(self, sample_classifier):
        result = sample_classifier.classify()
        assert isinstance(result["confidence"], float)

    def test_confidence_in_range(self, sample_classifier):
        result = sample_classifier.classify()
        assert 0.0 <= result["confidence"] <= 1.0

    def test_indicators_is_dict(self, sample_classifier):
        result = sample_classifier.classify()
        assert isinstance(result["indicators"], dict)

    def test_indicators_has_adx(self, sample_classifier):
        result = sample_classifier.classify()
        assert "adx" in result["indicators"]

    def test_indicators_has_bb_width(self, sample_classifier):
        result = sample_classifier.classify()
        assert "bb_width" in result["indicators"]

    def test_indicators_has_sma_direction(self, sample_classifier):
        result = sample_classifier.classify()
        assert "sma_direction" in result["indicators"]

    def test_recommended_strategies_is_list(self, sample_classifier):
        result = sample_classifier.classify()
        assert isinstance(result["recommended_strategies"], list)

    def test_recommended_strategies_not_empty(self, sample_classifier):
        result = sample_classifier.classify()
        assert len(result["recommended_strategies"]) > 0


# ---------------------------------------------------------------------------
# classify() 분류 로직 테스트
# ---------------------------------------------------------------------------

class TestClassifyLogic:
    def test_strong_uptrend_classified_as_trending_up(self, uptrend_classifier):
        """강한 상승추세 데이터 -> trending_up"""
        result = uptrend_classifier.classify()
        assert result["regime"] == MarketRegime.TRENDING_UP

    def test_strong_downtrend_classified_as_trending_down(self, downtrend_classifier):
        """강한 하락추세 데이터 -> trending_down"""
        result = downtrend_classifier.classify()
        assert result["regime"] == MarketRegime.TRENDING_DOWN

    def test_ranging_data_classified_as_ranging(self, ranging_classifier):
        """횡보 데이터 -> ranging"""
        result = ranging_classifier.classify()
        assert result["regime"] == MarketRegime.RANGING

    def test_uptrend_confidence_high(self, uptrend_classifier):
        """강한 추세에서 confidence가 0.25 이상"""
        result = uptrend_classifier.classify()
        assert result["confidence"] >= 0.25

    def test_ranging_confidence_low(self, ranging_classifier):
        """횡보장에서 confidence가 0.25 이하"""
        result = ranging_classifier.classify()
        assert result["confidence"] <= 0.25

    def test_uptrend_sma_direction_up(self, uptrend_classifier):
        """상승추세에서 SMA 방향이 'up'"""
        result = uptrend_classifier.classify()
        assert result["indicators"]["sma_direction"] == "up"

    def test_downtrend_sma_direction_down(self, downtrend_classifier):
        """하락추세에서 SMA 방향이 'down'"""
        result = downtrend_classifier.classify()
        assert result["indicators"]["sma_direction"] == "down"


# ---------------------------------------------------------------------------
# 추천 전략 테스트
# ---------------------------------------------------------------------------

class TestRecommendedStrategies:
    def test_trending_up_strategies(self, uptrend_classifier):
        result = uptrend_classifier.classify()
        assert result["regime"] == MarketRegime.TRENDING_UP
        expected = ["모멘텀 추종", "돌파 매수", "추세 추종"]
        assert result["recommended_strategies"] == expected

    def test_trending_down_strategies(self, downtrend_classifier):
        result = downtrend_classifier.classify()
        assert result["regime"] == MarketRegime.TRENDING_DOWN
        expected = ["공매도", "인버스", "방어적 포지션"]
        assert result["recommended_strategies"] == expected

    def test_ranging_strategies(self, ranging_classifier):
        result = ranging_classifier.classify()
        assert result["regime"] == MarketRegime.RANGING
        expected = ["평균회귀", "볼린저밴드 반전", "RSI 역추세"]
        assert result["recommended_strategies"] == expected


# ---------------------------------------------------------------------------
# get_strategy_weights() 테스트
# ---------------------------------------------------------------------------

class TestGetStrategyWeights:
    def test_returns_dict(self, sample_classifier):
        result = sample_classifier.get_strategy_weights(MarketRegime.TRENDING_UP)
        assert isinstance(result, dict)

    def test_trending_up_weights(self, sample_classifier):
        result = sample_classifier.get_strategy_weights(MarketRegime.TRENDING_UP)
        assert "모멘텀 추종" in result
        assert "돌파 매수" in result
        assert "추세 추종" in result

    def test_trending_down_weights(self, sample_classifier):
        result = sample_classifier.get_strategy_weights(MarketRegime.TRENDING_DOWN)
        assert "공매도" in result
        assert "인버스" in result
        assert "방어적 포지션" in result

    def test_ranging_weights(self, sample_classifier):
        result = sample_classifier.get_strategy_weights(MarketRegime.RANGING)
        assert "평균회귀" in result
        assert "볼린저밴드 반전" in result
        assert "RSI 역추세" in result

    def test_weights_sum_to_one(self, sample_classifier):
        for regime in (MarketRegime.TRENDING_UP, MarketRegime.TRENDING_DOWN, MarketRegime.RANGING):
            weights = sample_classifier.get_strategy_weights(regime)
            total = sum(weights.values())
            assert abs(total - 1.0) < 0.01, f"{regime}: 가중치 합 {total} != 1.0"

    def test_all_weights_positive(self, sample_classifier):
        for regime in (MarketRegime.TRENDING_UP, MarketRegime.TRENDING_DOWN, MarketRegime.RANGING):
            weights = sample_classifier.get_strategy_weights(regime)
            for name, w in weights.items():
                assert w > 0, f"{regime}/{name}: 가중치가 0 이하"

    def test_unknown_regime_raises(self, sample_classifier):
        with pytest.raises(KeyError):
            sample_classifier.get_strategy_weights("unknown_regime")
