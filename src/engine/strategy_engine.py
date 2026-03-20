"""매매 전략 엔진 - 전략 기반 클래스 및 개별 전략 구현

버전: 1.0.0
작성일: 2026-03-17
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.engine.event_queue import Event


class Strategy(ABC):
    """매매 전략 추상 기반 클래스"""

    @property
    @abstractmethod
    def name(self) -> str:
        """전략 이름"""
        ...

    @abstractmethod
    def on_signal(self, signal_data: dict) -> None:
        """시그널 수신 처리"""
        ...

    @abstractmethod
    def on_tick(self, tick_data: dict) -> None:
        """틱 데이터 수신 처리"""
        ...

    @abstractmethod
    def evaluate(self, market_data: dict | None = None) -> dict:
        """전략 평가 실행 -> 결과 dict 반환"""
        ...


class StrategyEngine:
    """전략 등록/제거/평가/실행 엔진"""

    def __init__(self):
        self._strategies: dict[str, Strategy] = {}

    @property
    def strategies(self) -> list[Strategy]:
        """등록된 전략 목록"""
        return list(self._strategies.values())

    def register_strategy(self, strategy: Strategy) -> None:
        """전략 등록 (이름 중복 불가)"""
        if strategy.name in self._strategies:
            raise ValueError(f"이미 등록된 전략입니다: {strategy.name}")
        self._strategies[strategy.name] = strategy

    def remove_strategy(self, name: str) -> None:
        """전략 제거"""
        if name not in self._strategies:
            raise KeyError(f"존재하지 않는 전략입니다: {name}")
        del self._strategies[name]

    def evaluate_all(self, market_data: dict) -> list[dict]:
        """모든 전략의 evaluate 결과 수집"""
        results = []
        for name, strategy in self._strategies.items():
            result = strategy.evaluate(market_data)
            result["strategy_name"] = name
            results.append(result)
        return results

    def ensemble_evaluate(self, data: dict) -> dict:
        """등록된 전략들의 다수결 투표로 종합 신호 생성.

        Returns:
            {"signal": str, "confidence": float, "agreement": float, "details": list}
        """
        votes = {"buy": 0.0, "sell": 0.0, "hold": 0.0}
        details = []
        for name, strategy in self._strategies.items():
            result = strategy.evaluate(data)
            signal = result.get("signal", result.get("action", "hold"))
            confidence = result.get("confidence", 0.5)
            if signal in ("매수", "buy"):
                votes["buy"] += confidence
            elif signal in ("매도", "sell"):
                votes["sell"] += confidence
            else:
                votes["hold"] += confidence
            details.append({"strategy": name, "signal": signal, "confidence": confidence})

        total = sum(votes.values()) or 1
        winner = max(votes, key=votes.get)
        agreement = votes[winner] / total

        signal_map = {"buy": "매수", "sell": "매도", "hold": "관망"}
        n = len(self._strategies)
        return {
            "signal": signal_map[winner],
            "confidence": votes[winner] / n if n else 0,
            "agreement": round(agreement, 3),
            "details": details,
        }

    def run(self, events: list[Event]) -> list[list[dict]]:
        """이벤트 리스트에서 데이터 수신 -> 전략 평가 -> 결과 반환 (동기)"""
        all_results = []
        for event in events:
            market_data = event.data if event.data else {}
            results = self.evaluate_all(market_data)
            all_results.append(results)
        return all_results


# ---------------------------------------------------------------------------
# T051: AI 종합 전략
# ---------------------------------------------------------------------------

class AICompositeStrategy(Strategy):
    """AI 종합 점수 기반 전략 - AIScorer 활용"""

    BUY_THRESHOLD = 0.6
    SELL_THRESHOLD = -0.3

    def __init__(self, ai_scorer: Any):
        self._scorer = ai_scorer
        self._last_signal = {}
        self._last_tick = {}

    @property
    def name(self) -> str:
        return "ai_composite"

    def on_signal(self, signal_data: dict) -> None:
        """시그널 수신 (저장용)"""
        self._last_signal = signal_data

    def on_tick(self, tick_data: dict) -> None:
        """틱 데이터 수신 (저장용)"""
        self._last_tick = tick_data

    def evaluate(self, market_data: dict | None = None) -> dict:
        """AI 종합 점수 기반 매수/매도/관망 판단

        market_data에 sentiment_score, technical_score 필요
        """
        market_data = market_data or {}
        sentiment = market_data.get("sentiment_score", 0.0)
        technical = market_data.get("technical_score", 0.0)

        score_result = self._scorer.calculate_score(sentiment, technical)
        total_score = score_result["total_score"]

        if total_score >= self.BUY_THRESHOLD:
            action = "매수"
        elif total_score <= self.SELL_THRESHOLD:
            action = "매도"
        else:
            action = "관망"

        return {
            "action": action,
            "score": total_score,
            "confidence": score_result.get("confidence", 0.0),
            "reasons": [f"AI 종합 점수: {total_score}"],
        }


# ---------------------------------------------------------------------------
# T052: 모멘텀 전략
# ---------------------------------------------------------------------------

class MomentumStrategy(Strategy):
    """RSI + MACD 기반 모멘텀 전략"""

    def __init__(self):
        self._last_signal = {}
        self._last_tick = {}

    @property
    def name(self) -> str:
        return "momentum"

    def on_signal(self, signal_data: dict) -> None:
        self._last_signal = signal_data

    def on_tick(self, tick_data: dict) -> None:
        self._last_tick = tick_data

    def evaluate(self, market_data: dict | None = None) -> dict:
        """RSI < 30 + MACD 골든크로스 -> 매수 / RSI > 70 + MACD 데드크로스 -> 매도"""
        market_data = market_data or {}
        rsi = market_data.get("rsi", 50)
        macd_cross = market_data.get("macd_cross", "none")

        reasons = []
        confidence = 0.0

        # 매수 조건: RSI < 30 AND MACD 골든크로스
        if rsi < 30 and macd_cross == "golden":
            action = "매수"
            reasons.append(f"RSI 과매도({rsi})")
            reasons.append("MACD 골든크로스")
            # RSI가 낮을수록 + MACD 크로스 -> 신뢰도 높음
            rsi_strength = min(1.0, (30 - rsi) / 30)
            confidence = 0.5 + 0.5 * rsi_strength
        # 매도 조건: RSI > 70 AND MACD 데드크로스
        elif rsi > 70 and macd_cross == "dead":
            action = "매도"
            reasons.append(f"RSI 과매수({rsi})")
            reasons.append("MACD 데드크로스")
            # RSI가 높을수록 + MACD 크로스 -> 신뢰도 높음
            rsi_strength = min(1.0, (rsi - 70) / 30)
            confidence = 0.5 + 0.5 * rsi_strength
        else:
            action = "관망"
            reasons.append("모멘텀 조건 미충족")
            confidence = 0.3

        return {
            "action": action,
            "confidence": round(confidence, 3),
            "reasons": reasons,
        }


# ---------------------------------------------------------------------------
# T053: 평균 회귀 전략
# ---------------------------------------------------------------------------

class MeanReversionStrategy(Strategy):
    """볼린저밴드 기반 평균 회귀 전략"""

    def __init__(self):
        self._last_signal = {}
        self._last_tick = {}

    @property
    def name(self) -> str:
        return "mean_reversion"

    def on_signal(self, signal_data: dict) -> None:
        self._last_signal = signal_data

    def on_tick(self, tick_data: dict) -> None:
        self._last_tick = tick_data

    def evaluate(self, market_data: dict | None = None) -> dict:
        """볼린저밴드 하단 터치 -> 매수 / 상단 터치 -> 매도"""
        market_data = market_data or {}
        close = market_data.get("close", 0)
        bb_lower = market_data.get("bb_lower", 0)
        bb_upper = market_data.get("bb_upper", 0)

        if close <= 0 or bb_lower <= 0 or bb_upper <= 0:
            return {"action": "관망", "confidence": 0.0, "reasons": ["데이터 부족"]}

        reasons = []
        confidence = 0.0
        bb_width = bb_upper - bb_lower

        if close <= bb_lower:
            action = "매수"
            reasons.append("볼린저밴드 하단 터치")
            # 하단 아래로 벗어난 정도에 비례하여 신뢰도 상승
            deviation = (bb_lower - close) / bb_width if bb_width > 0 else 0
            confidence = min(1.0, 0.5 + deviation)
        elif close >= bb_upper:
            action = "매도"
            reasons.append("볼린저밴드 상단 터치")
            # 상단 위로 벗어난 정도에 비례하여 신뢰도 상승
            deviation = (close - bb_upper) / bb_width if bb_width > 0 else 0
            confidence = min(1.0, 0.5 + deviation)
        else:
            action = "관망"
            reasons.append("볼린저밴드 범위 내")
            confidence = 0.3

        return {
            "action": action,
            "confidence": round(confidence, 3),
            "reasons": reasons,
        }
