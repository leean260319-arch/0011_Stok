"""T050-T054: StrategyEngine 테스트 - 전략 기반 클래스, 개별 전략, 실행 루프"""
import numpy as np
import pandas as pd
import pytest
from unittest.mock import MagicMock

from src.engine.strategy_engine import (
    Strategy,
    StrategyEngine,
    AICompositeStrategy,
    MomentumStrategy,
    MeanReversionStrategy,
)
from src.engine.event_queue import Event


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


class DummyStrategy(Strategy):
    """테스트용 더미 전략"""

    @property
    def name(self) -> str:
        return "dummy"

    def on_signal(self, signal_data: dict) -> None:
        self._last_signal = signal_data

    def on_tick(self, tick_data: dict) -> None:
        self._last_tick = tick_data

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"action": "관망", "reason": "더미"}


class DummyStrategy2(Strategy):
    """테스트용 더미 전략 2"""

    @property
    def name(self) -> str:
        return "dummy2"

    def on_signal(self, signal_data: dict) -> None:
        pass

    def on_tick(self, tick_data: dict) -> None:
        pass

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"action": "매수", "reason": "테스트"}


# ---------------------------------------------------------------------------
# T050: Strategy 추상 클래스 테스트
# ---------------------------------------------------------------------------

class TestStrategyABC:
    def test_cannot_instantiate_abstract(self):
        """Strategy 추상 클래스는 직접 인스턴스화 불가"""
        with pytest.raises(TypeError):
            Strategy()

    def test_dummy_strategy_instantiable(self):
        """구현체는 인스턴스화 가능"""
        s = DummyStrategy()
        assert s is not None

    def test_name_property(self):
        s = DummyStrategy()
        assert s.name == "dummy"

    def test_on_signal_callable(self):
        s = DummyStrategy()
        s.on_signal({"signal": "매수"})
        assert s._last_signal == {"signal": "매수"}

    def test_on_tick_callable(self):
        s = DummyStrategy()
        s.on_tick({"price": 50000})
        assert s._last_tick == {"price": 50000}

    def test_evaluate_returns_dict(self):
        s = DummyStrategy()
        result = s.evaluate()
        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# T050: StrategyEngine 등록/제거 테스트
# ---------------------------------------------------------------------------

class TestStrategyEngineRegistration:
    def test_register_strategy(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        assert len(engine.strategies) == 1

    def test_register_multiple_strategies(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        engine.register_strategy(DummyStrategy2())
        assert len(engine.strategies) == 2

    def test_register_duplicate_name_raises(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        with pytest.raises(ValueError, match="이미 등록"):
            engine.register_strategy(DummyStrategy())

    def test_remove_strategy(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        engine.remove_strategy("dummy")
        assert len(engine.strategies) == 0

    def test_remove_nonexistent_raises(self):
        engine = StrategyEngine()
        with pytest.raises(KeyError, match="존재하지 않"):
            engine.remove_strategy("nonexistent")

    def test_strategies_property_returns_list(self):
        engine = StrategyEngine()
        assert isinstance(engine.strategies, list)


# ---------------------------------------------------------------------------
# T050: StrategyEngine.evaluate_all 테스트
# ---------------------------------------------------------------------------

class TestStrategyEngineEvaluateAll:
    def test_evaluate_all_returns_list(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        results = engine.evaluate_all({})
        assert isinstance(results, list)

    def test_evaluate_all_collects_all_results(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        engine.register_strategy(DummyStrategy2())
        results = engine.evaluate_all({})
        assert len(results) == 2

    def test_evaluate_all_result_has_strategy_name(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        results = engine.evaluate_all({})
        assert results[0]["strategy_name"] == "dummy"

    def test_evaluate_all_empty_engine(self):
        engine = StrategyEngine()
        results = engine.evaluate_all({})
        assert results == []


# ---------------------------------------------------------------------------
# T051: AICompositeStrategy 테스트
# ---------------------------------------------------------------------------

class TestAICompositeStrategy:
    def test_name(self):
        scorer = MagicMock()
        s = AICompositeStrategy(scorer)
        assert s.name == "ai_composite"

    def test_evaluate_buy_signal(self):
        """ai_score >= 0.6 이면 매수"""
        scorer = MagicMock()
        scorer.calculate_score.return_value = {
            "total_score": 0.7,
            "signal": "매수",
            "confidence": 0.9,
        }
        s = AICompositeStrategy(scorer)
        result = s.evaluate({"sentiment_score": 0.8, "technical_score": 0.7})
        assert result["action"] == "매수"

    def test_evaluate_sell_signal(self):
        """ai_score <= -0.3 이면 매도"""
        scorer = MagicMock()
        scorer.calculate_score.return_value = {
            "total_score": -0.4,
            "signal": "매도",
            "confidence": 0.8,
        }
        s = AICompositeStrategy(scorer)
        result = s.evaluate({"sentiment_score": -0.5, "technical_score": -0.5})
        assert result["action"] == "매도"

    def test_evaluate_hold_signal(self):
        """그 외 관망"""
        scorer = MagicMock()
        scorer.calculate_score.return_value = {
            "total_score": 0.3,
            "signal": "관망",
            "confidence": 0.5,
        }
        s = AICompositeStrategy(scorer)
        result = s.evaluate({"sentiment_score": 0.3, "technical_score": 0.3})
        assert result["action"] == "관망"

    def test_evaluate_returns_score(self):
        scorer = MagicMock()
        scorer.calculate_score.return_value = {
            "total_score": 0.7,
            "signal": "매수",
            "confidence": 0.9,
        }
        s = AICompositeStrategy(scorer)
        result = s.evaluate({"sentiment_score": 0.8, "technical_score": 0.7})
        assert "score" in result

    def test_on_signal(self):
        scorer = MagicMock()
        s = AICompositeStrategy(scorer)
        s.on_signal({"signal": "매수"})  # 예외 없이 호출

    def test_on_tick(self):
        scorer = MagicMock()
        s = AICompositeStrategy(scorer)
        s.on_tick({"price": 50000})  # 예외 없이 호출

    def test_boundary_buy_060(self):
        """정확히 0.6 → 매수"""
        scorer = MagicMock()
        scorer.calculate_score.return_value = {
            "total_score": 0.6,
            "signal": "매수",
            "confidence": 0.8,
        }
        s = AICompositeStrategy(scorer)
        result = s.evaluate({"sentiment_score": 0.6, "technical_score": 0.6})
        assert result["action"] == "매수"

    def test_boundary_sell_minus030(self):
        """정확히 -0.3 → 매도"""
        scorer = MagicMock()
        scorer.calculate_score.return_value = {
            "total_score": -0.3,
            "signal": "매도",
            "confidence": 0.6,
        }
        s = AICompositeStrategy(scorer)
        result = s.evaluate({"sentiment_score": -0.3, "technical_score": -0.3})
        assert result["action"] == "매도"


# ---------------------------------------------------------------------------
# T052: MomentumStrategy 테스트
# ---------------------------------------------------------------------------

class TestMomentumStrategy:
    def test_name(self):
        s = MomentumStrategy()
        assert s.name == "momentum"

    def test_evaluate_returns_dict(self):
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 25, "macd_cross": "golden"})
        assert isinstance(result, dict)

    def test_buy_rsi_low_macd_golden(self):
        """RSI < 30 + MACD 골든크로스 → 매수"""
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 25, "macd_cross": "golden"})
        assert result["action"] == "매수"

    def test_sell_rsi_high_macd_dead(self):
        """RSI > 70 + MACD 데드크로스 → 매도"""
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 75, "macd_cross": "dead"})
        assert result["action"] == "매도"

    def test_hold_rsi_normal(self):
        """RSI 30~70, 크로스 없음 → 관망"""
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 50, "macd_cross": "none"})
        assert result["action"] == "관망"

    def test_rsi_low_no_macd_golden(self):
        """RSI < 30 but MACD 크로스 없음 → 관망 (두 조건 모두 필요)"""
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 25, "macd_cross": "none"})
        assert result["action"] == "관망"

    def test_rsi_high_no_macd_dead(self):
        """RSI > 70 but MACD 크로스 없음 → 관망"""
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 75, "macd_cross": "none"})
        assert result["action"] == "관망"

    def test_result_has_reasons(self):
        s = MomentumStrategy()
        result = s.evaluate({"rsi": 25, "macd_cross": "golden"})
        assert "reasons" in result

    def test_on_signal(self):
        s = MomentumStrategy()
        s.on_signal({"signal": "매수"})

    def test_on_tick(self):
        s = MomentumStrategy()
        s.on_tick({"price": 50000})


# ---------------------------------------------------------------------------
# T053: MeanReversionStrategy 테스트
# ---------------------------------------------------------------------------

class TestMeanReversionStrategy:
    def test_name(self):
        s = MeanReversionStrategy()
        assert s.name == "mean_reversion"

    def test_evaluate_returns_dict(self):
        s = MeanReversionStrategy()
        result = s.evaluate({"close": 49000, "bb_lower": 49500, "bb_upper": 51000})
        assert isinstance(result, dict)

    def test_buy_at_lower_band(self):
        """볼린저밴드 하단 터치 → 매수"""
        s = MeanReversionStrategy()
        result = s.evaluate({"close": 49000, "bb_lower": 49500, "bb_upper": 51000})
        assert result["action"] == "매수"

    def test_sell_at_upper_band(self):
        """볼린저밴드 상단 터치 → 매도"""
        s = MeanReversionStrategy()
        result = s.evaluate({"close": 51500, "bb_lower": 49500, "bb_upper": 51000})
        assert result["action"] == "매도"

    def test_hold_in_band(self):
        """밴드 내부 → 관망"""
        s = MeanReversionStrategy()
        result = s.evaluate({"close": 50000, "bb_lower": 49500, "bb_upper": 51000})
        assert result["action"] == "관망"

    def test_result_has_reasons(self):
        s = MeanReversionStrategy()
        result = s.evaluate({"close": 49000, "bb_lower": 49500, "bb_upper": 51000})
        assert "reasons" in result

    def test_on_signal(self):
        s = MeanReversionStrategy()
        s.on_signal({"signal": "매수"})

    def test_on_tick(self):
        s = MeanReversionStrategy()
        s.on_tick({"price": 50000})


# ---------------------------------------------------------------------------
# T054: StrategyEngine.run 실행 루프 테스트
# ---------------------------------------------------------------------------

class TestStrategyEngineRun:
    def test_run_processes_events(self):
        """이벤트 큐에서 데이터 수신 → 전략 평가 → 결과 반환"""
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())

        events = [
            Event(event_type="market_data", data={"price": 50000}),
            Event(event_type="market_data", data={"price": 51000}),
        ]
        results = engine.run(events)
        assert len(results) == 2

    def test_run_returns_list_of_results(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        events = [Event(event_type="market_data", data={"price": 50000})]
        results = engine.run(events)
        assert isinstance(results, list)
        assert isinstance(results[0], list)

    def test_run_empty_events(self):
        engine = StrategyEngine()
        engine.register_strategy(DummyStrategy())
        results = engine.run([])
        assert results == []

    def test_run_no_strategies(self):
        engine = StrategyEngine()
        events = [Event(event_type="market_data", data={"price": 50000})]
        results = engine.run(events)
        assert len(results) == 1
        assert results[0] == []


# ---------------------------------------------------------------------------
# P2-06: 전략 앙상블/투표 테스트
# ---------------------------------------------------------------------------

class BuyStrategy(Strategy):
    """매수 신호 전략 (테스트용)"""

    def __init__(self, strategy_name: str, confidence: float = 0.8):
        self._name = strategy_name
        self._confidence = confidence

    @property
    def name(self) -> str:
        return self._name

    def on_signal(self, signal_data: dict) -> None:
        pass

    def on_tick(self, tick_data: dict) -> None:
        pass

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"signal": "매수", "confidence": self._confidence}


class SellStrategy(Strategy):
    """매도 신호 전략 (테스트용)"""

    def __init__(self, strategy_name: str, confidence: float = 0.8):
        self._name = strategy_name
        self._confidence = confidence

    @property
    def name(self) -> str:
        return self._name

    def on_signal(self, signal_data: dict) -> None:
        pass

    def on_tick(self, tick_data: dict) -> None:
        pass

    def evaluate(self, market_data: dict | None = None) -> dict:
        return {"signal": "매도", "confidence": self._confidence}


class TestEnsembleEvaluate:
    def test_ensemble_evaluate_majority_buy(self):
        """매수 전략 다수일 때 신호는 매수"""
        engine = StrategyEngine()
        engine.register_strategy(BuyStrategy("buy1", confidence=0.8))
        engine.register_strategy(BuyStrategy("buy2", confidence=0.8))
        engine.register_strategy(SellStrategy("sell1", confidence=0.8))
        result = engine.ensemble_evaluate({})
        assert result["signal"] == "매수"

    def test_ensemble_evaluate_agreement(self):
        """agreement ratio: 3개 중 2개 매수 -> agreement >= 0.5"""
        engine = StrategyEngine()
        engine.register_strategy(BuyStrategy("buy1", confidence=1.0))
        engine.register_strategy(BuyStrategy("buy2", confidence=1.0))
        engine.register_strategy(SellStrategy("sell1", confidence=1.0))
        result = engine.ensemble_evaluate({})
        assert result["agreement"] > 0.5

    def test_ensemble_evaluate_empty(self):
        """전략 없을 때 안전 처리 - confidence 0, agreement 1.0"""
        engine = StrategyEngine()
        result = engine.ensemble_evaluate({})
        assert "signal" in result
        assert result["confidence"] == 0
        assert "agreement" in result
        assert "details" in result

    def test_ensemble_evaluate_returns_dict(self):
        """반환값이 dict이고 필수 키 포함"""
        engine = StrategyEngine()
        engine.register_strategy(BuyStrategy("buy1"))
        result = engine.ensemble_evaluate({})
        assert isinstance(result, dict)
        for key in ("signal", "confidence", "agreement", "details"):
            assert key in result

    def test_ensemble_evaluate_details_list(self):
        """details는 전략별 결과 리스트"""
        engine = StrategyEngine()
        engine.register_strategy(BuyStrategy("buy1"))
        engine.register_strategy(SellStrategy("sell1"))
        result = engine.ensemble_evaluate({})
        assert isinstance(result["details"], list)
        assert len(result["details"]) == 2

    def test_ensemble_evaluate_signal_valid(self):
        """신호 값은 매수/매도/관망 중 하나"""
        engine = StrategyEngine()
        engine.register_strategy(BuyStrategy("buy1"))
        result = engine.ensemble_evaluate({})
        assert result["signal"] in {"매수", "매도", "관망"}

    def test_ensemble_evaluate_majority_sell(self):
        """매도 전략 다수일 때 신호는 매도"""
        engine = StrategyEngine()
        engine.register_strategy(SellStrategy("sell1", confidence=0.9))
        engine.register_strategy(SellStrategy("sell2", confidence=0.9))
        engine.register_strategy(BuyStrategy("buy1", confidence=0.9))
        result = engine.ensemble_evaluate({})
        assert result["signal"] == "매도"
