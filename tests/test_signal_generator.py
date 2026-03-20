"""T048: SignalGenerator 테스트 - 기술적 지표 조합 매매 시그널"""
import numpy as np
import pandas as pd
import pytest

from src.engine.chart_analyzer import ChartAnalyzer
from src.engine.signal_generator import SignalGenerator


# ---------------------------------------------------------------------------
# 헬퍼
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


def make_oversold_ohlcv(n: int = 100) -> pd.DataFrame:
    """RSI 과매도 유도: 연속 하락 시세"""
    np.random.seed(0)
    close = 50000 - np.cumsum(abs(np.random.randn(n) * 800))
    close = np.maximum(close, 1000)
    return pd.DataFrame({
        "open": close + np.random.randn(n) * 50,
        "high": close + abs(np.random.randn(n) * 100),
        "low": close - abs(np.random.randn(n) * 100),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


def make_overbought_ohlcv(n: int = 100) -> pd.DataFrame:
    """RSI 과매수 유도: 연속 상승 시세"""
    np.random.seed(1)
    close = 10000 + np.cumsum(abs(np.random.randn(n) * 800))
    return pd.DataFrame({
        "open": close + np.random.randn(n) * 50,
        "high": close + abs(np.random.randn(n) * 100),
        "low": close - abs(np.random.randn(n) * 100),
        "close": close,
        "volume": np.random.randint(10000, 100000, n).astype(float),
    })


@pytest.fixture
def generator() -> SignalGenerator:
    ca = ChartAnalyzer(make_sample_ohlcv())
    return SignalGenerator(ca)


# ---------------------------------------------------------------------------
# T048: 시그널 생성 테스트
# ---------------------------------------------------------------------------

class TestSignalGeneratorStructure:
    def test_generate_returns_dict(self, generator):
        result = generator.generate_signal()
        assert isinstance(result, dict)

    def test_result_has_signal_key(self, generator):
        result = generator.generate_signal()
        assert "signal" in result

    def test_result_has_score_key(self, generator):
        result = generator.generate_signal()
        assert "score" in result

    def test_result_has_reasons_key(self, generator):
        result = generator.generate_signal()
        assert "reasons" in result

    def test_signal_is_valid_string(self, generator):
        result = generator.generate_signal()
        assert result["signal"] in {"매수", "매도", "관망"}

    def test_score_is_float(self, generator):
        result = generator.generate_signal()
        assert isinstance(result["score"], float)

    def test_score_within_range(self, generator):
        result = generator.generate_signal()
        assert -1.0 <= result["score"] <= 1.0

    def test_reasons_is_list(self, generator):
        result = generator.generate_signal()
        assert isinstance(result["reasons"], list)

    def test_reasons_are_strings(self, generator):
        result = generator.generate_signal()
        for r in result["reasons"]:
            assert isinstance(r, str)


class TestSignalGeneratorLogic:
    def test_oversold_tends_to_buy(self):
        """연속 하락 데이터 → RSI 과매도 → 매수 시그널 경향"""
        ca = ChartAnalyzer(make_oversold_ohlcv())
        gen = SignalGenerator(ca)
        result = gen.generate_signal()
        # 점수가 양수이거나 과매도 이유가 포함되어야 함
        has_oversold_reason = any("과매도" in r for r in result["reasons"])
        assert has_oversold_reason or result["score"] >= 0

    def test_overbought_tends_to_sell(self):
        """연속 상승 데이터 → RSI 과매수 → 매도 시그널 경향"""
        ca = ChartAnalyzer(make_overbought_ohlcv())
        gen = SignalGenerator(ca)
        result = gen.generate_signal()
        has_overbought_reason = any("과매수" in r for r in result["reasons"])
        assert has_overbought_reason or result["score"] <= 0

    def test_signal_matches_score_buy(self, generator):
        """score > 0.2 이면 signal == '매수'"""
        result = generator.generate_signal()
        if result["score"] > 0.2:
            assert result["signal"] == "매수"

    def test_signal_matches_score_sell(self, generator):
        """score < -0.2 이면 signal == '매도'"""
        result = generator.generate_signal()
        if result["score"] < -0.2:
            assert result["signal"] == "매도"

    def test_signal_matches_score_hold(self, generator):
        """-0.2 <= score <= 0.2 이면 signal == '관망'"""
        result = generator.generate_signal()
        if -0.2 <= result["score"] <= 0.2:
            assert result["signal"] == "관망"

    def test_score_is_rounded(self, generator):
        result = generator.generate_signal()
        # 소수 3자리까지 반올림 확인
        assert result["score"] == round(result["score"], 3)

    def test_init_stores_analyzer(self):
        ca = ChartAnalyzer(make_sample_ohlcv())
        gen = SignalGenerator(ca)
        assert gen._analyzer is ca


# ---------------------------------------------------------------------------
# P2-01: 동적 지표 가중치 테스트
# ---------------------------------------------------------------------------

class TestClassifyMarket:
    def test_classify_market_trending(self, generator):
        """ADX > 25 -> trending"""
        result = generator.classify_market({"adx": 30})
        assert result == "trending"

    def test_classify_market_ranging(self, generator):
        """ADX < 25 -> ranging"""
        result = generator.classify_market({"adx": 15})
        assert result == "ranging"

    def test_classify_market_boundary_trending(self, generator):
        """ADX == 26 -> trending"""
        result = generator.classify_market({"adx": 26})
        assert result == "trending"

    def test_classify_market_boundary_ranging(self, generator):
        """ADX == 25 -> ranging (not strictly greater)"""
        result = generator.classify_market({"adx": 25})
        assert result == "ranging"

    def test_classify_market_zero_adx(self, generator):
        """ADX 없음 -> ranging"""
        result = generator.classify_market({})
        assert result == "ranging"


class TestDynamicWeights:
    def test_dynamic_weights_trending(self, generator):
        """추세장(trending)에서 MACD 가중치가 RSI 가중치보다 높은지 확인"""
        w = generator.WEIGHTS["trending"]
        assert w["macd"] > w["rsi"]

    def test_dynamic_weights_ranging(self, generator):
        """횡보장(ranging)에서 BB 가중치가 MACD 가중치보다 높은지 확인"""
        w = generator.WEIGHTS["ranging"]
        assert w["bb"] > w["macd"]

    def test_weights_keys_present(self, generator):
        """WEIGHTS 딕셔너리에 trending/ranging 키 존재"""
        assert "trending" in generator.WEIGHTS
        assert "ranging" in generator.WEIGHTS

    def test_weights_indicators_present(self, generator):
        """각 시장 유형에 rsi, macd, bb, adx, obv 키 존재"""
        for market_type in ("trending", "ranging"):
            w = generator.WEIGHTS[market_type]
            for key in ("rsi", "macd", "bb", "adx", "obv"):
                assert key in w
