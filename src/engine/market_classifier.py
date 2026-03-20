"""시장 상황 분류기 - ADX + SMA + 볼린저밴드 기반 시장 레짐 분류

버전: 1.0.0
작성일: 2026-03-17

ADX, 이동평균 방향, 볼린저밴드 폭을 조합하여
시장을 trending_up / trending_down / ranging 3단계로 분류한다.
"""
from src.engine.chart_analyzer import ChartAnalyzer


class MarketRegime:
    """시장 레짐 상수"""

    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    RANGING = "ranging"


# 레짐별 추천 전략
_STRATEGY_MAP = {
    MarketRegime.TRENDING_UP: ["모멘텀 추종", "돌파 매수", "추세 추종"],
    MarketRegime.TRENDING_DOWN: ["공매도", "인버스", "방어적 포지션"],
    MarketRegime.RANGING: ["평균회귀", "볼린저밴드 반전", "RSI 역추세"],
}

# 레짐별 전략 가중치
_STRATEGY_WEIGHTS = {
    MarketRegime.TRENDING_UP: {
        "모멘텀 추종": 0.45,
        "돌파 매수": 0.35,
        "추세 추종": 0.20,
    },
    MarketRegime.TRENDING_DOWN: {
        "공매도": 0.40,
        "인버스": 0.35,
        "방어적 포지션": 0.25,
    },
    MarketRegime.RANGING: {
        "평균회귀": 0.40,
        "볼린저밴드 반전": 0.35,
        "RSI 역추세": 0.25,
    },
}


class MarketClassifier:
    """ADX + SMA 방향 + 볼린저밴드 폭 기반 시장 레짐 분류기"""

    ADX_TREND_THRESHOLD = 25

    def __init__(self, chart_analyzer: ChartAnalyzer):
        self._analyzer = chart_analyzer

    def classify(self) -> dict:
        """시장 상황을 분류한다.

        Returns:
            {
                "regime": str,               # trending_up / trending_down / ranging
                "confidence": float,          # 0.0 ~ 1.0
                "indicators": dict,           # ADX, BB width, SMA direction 등
                "recommended_strategies": list[str],
            }
        """
        adx_val = self._get_adx()
        sma_direction = self._get_sma_direction()
        bb_width = self._get_bb_width()

        # 분류 로직
        if adx_val > self.ADX_TREND_THRESHOLD:
            if sma_direction == "up":
                regime = MarketRegime.TRENDING_UP
            else:
                regime = MarketRegime.TRENDING_DOWN
        else:
            regime = MarketRegime.RANGING

        # confidence = ADX / 100 (0.0 ~ 1.0 범위로 클리핑)
        confidence = min(adx_val / 100.0, 1.0)

        return {
            "regime": regime,
            "confidence": round(confidence, 4),
            "indicators": {
                "adx": round(adx_val, 4),
                "bb_width": round(bb_width, 4),
                "sma_direction": sma_direction,
            },
            "recommended_strategies": _STRATEGY_MAP[regime],
        }

    def get_strategy_weights(self, regime: str) -> dict:
        """레짐별 전략 가중치 반환.

        Args:
            regime: MarketRegime 상수 중 하나

        Returns:
            {전략명: 가중치(float)} 딕셔너리. 가중치 합 = 1.0

        Raises:
            KeyError: 알 수 없는 regime
        """
        return _STRATEGY_WEIGHTS[regime]

    # ------------------------------------------------------------------
    # 내부 지표 추출 메서드
    # ------------------------------------------------------------------

    def _get_adx(self) -> float:
        """최신 ADX 값을 반환한다. 데이터 부족 시 0.0 반환."""
        adx_df = self._analyzer.calc_adx()
        adx_col = [c for c in adx_df.columns if c.startswith("ADX_")]
        if not adx_col:
            return 0.0
        valid = adx_df[adx_col[0]].dropna()
        if len(valid) == 0:
            return 0.0
        return float(valid.iloc[-1])

    def _get_sma_direction(self) -> str:
        """SMA20 vs SMA50 비교로 방향 판단. 'up' 또는 'down' 반환.
        데이터 부족 시 'down' 반환."""
        sma20 = self._analyzer.calc_sma(period=20).dropna()
        sma50 = self._analyzer.calc_sma(period=50).dropna()
        if len(sma20) == 0 or len(sma50) == 0:
            return "down"
        latest_sma20 = float(sma20.iloc[-1])
        latest_sma50 = float(sma50.iloc[-1])
        if latest_sma20 > latest_sma50:
            return "up"
        return "down"

    def _get_bb_width(self) -> float:
        """볼린저밴드 폭 = (BBU - BBL) / BBM 반환.
        데이터 부족 시 0.0 반환."""
        bb_df = self._analyzer.calc_bollinger()
        bbu_cols = [c for c in bb_df.columns if "BBU_" in c]
        bbl_cols = [c for c in bb_df.columns if "BBL_" in c]
        bbm_cols = [c for c in bb_df.columns if "BBM_" in c]
        if not bbu_cols or not bbl_cols or not bbm_cols:
            return 0.0
        bbu_col = bbu_cols[0]
        bbl_col = bbl_cols[0]
        bbm_col = bbm_cols[0]
        valid = bb_df[[bbu_col, bbl_col, bbm_col]].dropna()
        if len(valid) == 0:
            return 0.0
        bbu = float(valid.iloc[-1][bbu_col])
        bbl = float(valid.iloc[-1][bbl_col])
        bbm = float(valid.iloc[-1][bbm_col])
        if bbm == 0:
            return 0.0
        return (bbu - bbl) / bbm
