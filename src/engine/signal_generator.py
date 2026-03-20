"""기술적 시그널 생성기 - 지표 조합으로 매수/매도/관망 시그널 산출

버전: 1.1.0
작성일: 2026-03-17
"""
from src.engine.chart_analyzer import ChartAnalyzer


class SignalGenerator:
    """기술적 지표 조합 기반 매매 시그널 생성기"""

    BUY_THRESHOLD = 0.2
    SELL_THRESHOLD = -0.2

    WEIGHTS = {
        "trending": {"rsi": 0.15, "macd": 0.35, "bb": 0.10, "adx": 0.25, "obv": 0.15},
        "ranging": {"rsi": 0.30, "macd": 0.15, "bb": 0.30, "adx": 0.10, "obv": 0.15},
    }

    def __init__(self, chart_analyzer: ChartAnalyzer):
        self._analyzer = chart_analyzer

    def classify_market(self, indicators: dict) -> str:
        """ADX 기반 시장 상황 분류. trending/ranging 반환."""
        adx = indicators.get("adx", 0)
        if adx > 25:
            return "trending"
        return "ranging"

    def generate_signal(self) -> dict:
        """기술적 지표 조합으로 매수/매도/관망 시그널 생성

        Returns:
            {
                signal: str,          # "매수" | "매도" | "관망"
                score: float,         # -1.0 ~ +1.0
                reasons: list[str],
            }
        """
        score = 0.0
        reasons = []

        # --- ADX 값 먼저 수집 (시장 분류에 필요) ---
        adx_df = self._analyzer.calc_adx()
        adx_col = [c for c in adx_df.columns if c.startswith("ADX_")]
        dmp_col = [c for c in adx_df.columns if c.startswith("DMP_")]
        dmn_col = [c for c in adx_df.columns if c.startswith("DMN_")]

        adx_val = 0.0
        dmp_val = 0.0
        dmn_val = 0.0
        if adx_col and dmp_col and dmn_col:
            valid_adx = adx_df[[adx_col[0], dmp_col[0], dmn_col[0]]].dropna()
            if len(valid_adx) > 0:
                adx_val = float(valid_adx.iloc[-1][adx_col[0]])
                dmp_val = float(valid_adx.iloc[-1][dmp_col[0]])
                dmn_val = float(valid_adx.iloc[-1][dmn_col[0]])

        # --- OBV 값 수집 ---
        obv_series = self._analyzer.calc_obv() if hasattr(self._analyzer, "calc_obv") else None
        obv_val = None
        obv_prev_val = None
        if obv_series is not None:
            obv_clean = obv_series.dropna()
            if len(obv_clean) >= 2:
                obv_val = float(obv_clean.iloc[-1])
                obv_prev_val = float(obv_clean.iloc[-2])

        # --- 시장 분류 및 가중치 선택 ---
        market_type = self.classify_market({"adx": adx_val})
        w = self.WEIGHTS[market_type]

        # --- RSI 과매수/과매도 ---
        rsi_series = self._analyzer.calc_rsi()
        latest_rsi = float(rsi_series.dropna().iloc[-1])
        if latest_rsi < 30:
            score += w["rsi"]
            reasons.append(f"RSI 과매도({latest_rsi:.1f})")
        elif latest_rsi > 70:
            score -= w["rsi"]
            reasons.append(f"RSI 과매수({latest_rsi:.1f})")

        # --- MACD 골든크로스 / 데드크로스 ---
        macd_df = self._analyzer.calc_macd()
        macd_col = [c for c in macd_df.columns if c.startswith("MACD_") and "h" not in c.lower() and "s" not in c.lower()]
        signal_col = [c for c in macd_df.columns if "MACDs_" in c]
        if macd_col and signal_col:
            valid = macd_df[[macd_col[0], signal_col[0]]].dropna()
            if len(valid) >= 2:
                prev_macd, prev_sig = float(valid.iloc[-2][macd_col[0]]), float(valid.iloc[-2][signal_col[0]])
                curr_macd, curr_sig = float(valid.iloc[-1][macd_col[0]]), float(valid.iloc[-1][signal_col[0]])
                if prev_macd < prev_sig and curr_macd >= curr_sig:
                    score += w["macd"]
                    reasons.append("MACD 골든크로스")
                elif prev_macd > prev_sig and curr_macd <= curr_sig:
                    score -= w["macd"]
                    reasons.append("MACD 데드크로스")

        # --- 볼린저밴드 하단/상단 이탈 ---
        bb_df = self._analyzer.calc_bollinger()
        lower_col = [c for c in bb_df.columns if "BBL_" in c]
        upper_col = [c for c in bb_df.columns if "BBU_" in c]
        close_series = self._analyzer.df["close"]
        if lower_col and upper_col:
            valid_bb = bb_df[[lower_col[0], upper_col[0]]].dropna()
            if len(valid_bb) > 0:
                last_idx = valid_bb.index[-1]
                last_close = float(close_series.loc[last_idx])
                last_lower = float(valid_bb.iloc[-1][lower_col[0]])
                last_upper = float(valid_bb.iloc[-1][upper_col[0]])
                if last_close < last_lower:
                    score += w["bb"]
                    reasons.append("볼린저밴드 하단 이탈(과매도 구간)")
                elif last_close > last_upper:
                    score -= w["bb"]
                    reasons.append("볼린저밴드 상단 이탈(과매수 구간)")

        # --- ADX 추세 강도 (방향 강화용) ---
        if adx_col and dmp_col and dmn_col and adx_val > 0:
            if adx_val > 25:
                if dmp_val > dmn_val:
                    score += w["adx"]
                    reasons.append(f"ADX 강한 상승추세({adx_val:.1f})")
                else:
                    score -= w["adx"]
                    reasons.append(f"ADX 강한 하락추세({adx_val:.1f})")

        # --- OBV 방향 확인 ---
        if obv_val is not None and obv_prev_val is not None:
            if obv_val > obv_prev_val:
                score += w["obv"]
                reasons.append("OBV 상승(매수세 강화)")
            elif obv_val < obv_prev_val:
                score -= w["obv"]
                reasons.append("OBV 하락(매도세 강화)")

        # score 범위 클리핑 -1.0 ~ +1.0
        score = max(-1.0, min(1.0, score))

        if score > self.BUY_THRESHOLD:
            signal = "매수"
        elif score < self.SELL_THRESHOLD:
            signal = "매도"
        else:
            signal = "관망"

        return {
            "signal": signal,
            "score": round(score, 3),
            "reasons": reasons,
        }
