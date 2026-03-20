"""차트 분석기 - pandas-ta 기반 기술적 지표 계산

버전: 1.0.0
작성일: 2026-03-17
"""
import pandas as pd
import pandas_ta as ta


class ChartAnalyzer:
    """OHLCV DataFrame 기반 기술적 지표 계산기"""

    REQUIRED_COLUMNS = {"open", "high", "low", "close", "volume"}

    def __init__(self, df: pd.DataFrame):
        """df는 OHLCV 컬럼 필수: open, high, low, close, volume"""
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"필수 컬럼 누락: {missing}")
        self._df = df.copy()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    # ------------------------------------------------------------------
    # 기본 지표 6종
    # ------------------------------------------------------------------

    def calc_rsi(self, period: int = 14) -> pd.Series:
        """RSI (Relative Strength Index)"""
        return ta.rsi(self._df["close"], length=period)

    def calc_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """MACD (Moving Average Convergence Divergence)"""
        return ta.macd(self._df["close"], fast=fast, slow=slow, signal=signal)

    def calc_bollinger(self, period: int = 20, std: float = 2) -> pd.DataFrame:
        """볼린저밴드 (Bollinger Bands)"""
        return ta.bbands(self._df["close"], length=period, std=std)

    def calc_sma(self, period: int = 20) -> pd.Series:
        """단순이동평균 (Simple Moving Average)"""
        return ta.sma(self._df["close"], length=period)

    def calc_ema(self, period: int = 20) -> pd.Series:
        """지수이동평균 (Exponential Moving Average)"""
        return ta.ema(self._df["close"], length=period)

    def calc_stochastic(self, k: int = 14, d: int = 3) -> pd.DataFrame:
        """스토캐스틱 (Stochastic Oscillator)"""
        return ta.stoch(self._df["high"], self._df["low"], self._df["close"], k=k, d=d)

    # ------------------------------------------------------------------
    # 확장 지표 5종
    # ------------------------------------------------------------------

    def calc_ichimoku(self) -> pd.DataFrame:
        """일목균형표 (Ichimoku Cloud)"""
        return ta.ichimoku(self._df["high"], self._df["low"], self._df["close"])[0]

    def calc_adx(self, period: int = 14) -> pd.DataFrame:
        """ADX (Average Directional Index)"""
        return ta.adx(self._df["high"], self._df["low"], self._df["close"], length=period)

    def calc_cci(self, period: int = 20) -> pd.Series:
        """CCI (Commodity Channel Index)"""
        return ta.cci(self._df["high"], self._df["low"], self._df["close"], length=period)

    def calc_williams_r(self, period: int = 14) -> pd.Series:
        """Williams %R"""
        return ta.willr(self._df["high"], self._df["low"], self._df["close"], length=period)

    def calc_obv(self) -> pd.Series:
        """OBV (On-Balance Volume)"""
        return ta.obv(self._df["close"], self._df["volume"])

    def calc_atr(self, df: "pd.DataFrame", period: int = 14) -> float:
        """ATR(Average True Range) 계산.

        Args:
            df: OHLCV DataFrame (open, high, low, close 컬럼 필요)
            period: ATR 기간 (기본 14)

        Returns:
            최신 ATR 값. 데이터 부족 시 0.0
        """
        if len(df) < period + 1:
            return 0.0
        atr_series = ta.atr(df["high"], df["low"], df["close"], length=period)
        if atr_series is None or atr_series.empty:
            return 0.0
        latest = atr_series.iloc[-1]
        if latest != latest:  # NaN check
            return 0.0
        return float(latest)

    # ------------------------------------------------------------------
    # 전체 지표 계산
    # ------------------------------------------------------------------

    def calc_all(self) -> pd.DataFrame:
        """모든 기본+확장 지표를 계산하여 원본 df와 합쳐 반환"""
        parts = [
            self._df,
            self.calc_macd(),
            self.calc_bollinger(),
            self.calc_stochastic(),
            self.calc_ichimoku(),
            self.calc_adx(),
        ]
        scalar_series = {
            "RSI_14": self.calc_rsi(),
            "SMA_20": self.calc_sma(),
            "EMA_20": self.calc_ema(),
            "CCI_20": self.calc_cci(),
            "WILLR_14": self.calc_williams_r(),
            "OBV": self.calc_obv(),
        }
        result = pd.concat(parts, axis=1)
        for name, series in scalar_series.items():
            result[name] = series
        return result
