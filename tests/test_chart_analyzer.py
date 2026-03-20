"""T045+T046+T047: ChartAnalyzer 테스트 - 기본 지표 6종 + 확장 지표 5종"""
import numpy as np
import pandas as pd
import pytest

from src.engine.chart_analyzer import ChartAnalyzer


# ---------------------------------------------------------------------------
# 테스트 픽스처
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


@pytest.fixture
def analyzer() -> ChartAnalyzer:
    return ChartAnalyzer(make_sample_ohlcv())


# ---------------------------------------------------------------------------
# T045: 초기화 및 df 프로퍼티
# ---------------------------------------------------------------------------

class TestChartAnalyzerInit:
    def test_init_with_valid_df(self):
        df = make_sample_ohlcv()
        ca = ChartAnalyzer(df)
        assert ca.df is not None
        assert len(ca.df) == len(df)

    def test_df_is_copy(self):
        df = make_sample_ohlcv()
        ca = ChartAnalyzer(df)
        df.loc[df.index[0], "close"] = 999999
        assert ca.df["close"].iloc[0] != 999999

    def test_missing_column_raises(self):
        df = make_sample_ohlcv().drop(columns=["volume"])
        with pytest.raises(ValueError, match="필수 컬럼 누락"):
            ChartAnalyzer(df)

    def test_required_columns_present(self):
        ca = ChartAnalyzer(make_sample_ohlcv())
        assert set(ca.df.columns) >= {"open", "high", "low", "close", "volume"}


# ---------------------------------------------------------------------------
# T046: 기본 지표 6종
# ---------------------------------------------------------------------------

class TestBasicIndicators:
    def test_rsi_returns_series(self, analyzer):
        result = analyzer.calc_rsi()
        assert isinstance(result, pd.Series)

    def test_rsi_range(self, analyzer):
        result = analyzer.calc_rsi().dropna()
        assert (result >= 0).all() and (result <= 100).all()

    def test_rsi_custom_period(self, analyzer):
        result = analyzer.calc_rsi(period=7)
        assert isinstance(result, pd.Series)
        assert result.dropna().iloc[-1] >= 0

    def test_macd_returns_dataframe(self, analyzer):
        result = analyzer.calc_macd()
        assert isinstance(result, pd.DataFrame)

    def test_macd_has_required_columns(self, analyzer):
        result = analyzer.calc_macd()
        cols = result.columns.tolist()
        assert any("MACD_" in c for c in cols)
        assert any("MACDs_" in c for c in cols)
        assert any("MACDh_" in c for c in cols)

    def test_bollinger_returns_dataframe(self, analyzer):
        result = analyzer.calc_bollinger()
        assert isinstance(result, pd.DataFrame)

    def test_bollinger_has_bands(self, analyzer):
        result = analyzer.calc_bollinger()
        cols = result.columns.tolist()
        assert any("BBU_" in c for c in cols), "상단밴드 없음"
        assert any("BBM_" in c for c in cols), "중간밴드 없음"
        assert any("BBL_" in c for c in cols), "하단밴드 없음"

    def test_bollinger_upper_gt_lower(self, analyzer):
        result = analyzer.calc_bollinger().dropna()
        upper_col = [c for c in result.columns if "BBU_" in c][0]
        lower_col = [c for c in result.columns if "BBL_" in c][0]
        assert (result[upper_col] > result[lower_col]).all()

    def test_sma_returns_series(self, analyzer):
        result = analyzer.calc_sma()
        assert isinstance(result, pd.Series)

    def test_sma_length(self, analyzer):
        result = analyzer.calc_sma(period=20)
        assert len(result) == len(analyzer.df)

    def test_ema_returns_series(self, analyzer):
        result = analyzer.calc_ema()
        assert isinstance(result, pd.Series)

    def test_ema_vs_sma_different(self, analyzer):
        sma = analyzer.calc_sma().dropna()
        ema = analyzer.calc_ema().dropna()
        # SMA와 EMA는 값이 다름 (동일하면 버그)
        assert not sma.equals(ema)

    def test_stochastic_returns_dataframe(self, analyzer):
        result = analyzer.calc_stochastic()
        assert isinstance(result, pd.DataFrame)

    def test_stochastic_has_k_d(self, analyzer):
        result = analyzer.calc_stochastic()
        cols = result.columns.tolist()
        assert any("STOCHk_" in c for c in cols)
        assert any("STOCHd_" in c for c in cols)

    def test_stochastic_range(self, analyzer):
        result = analyzer.calc_stochastic().dropna()
        k_col = [c for c in result.columns if "STOCHk_" in c][0]
        assert (result[k_col] >= 0).all() and (result[k_col] <= 100).all()


# ---------------------------------------------------------------------------
# T047: 확장 지표 5종
# ---------------------------------------------------------------------------

class TestExtendedIndicators:
    def test_ichimoku_returns_dataframe(self, analyzer):
        result = analyzer.calc_ichimoku()
        assert isinstance(result, pd.DataFrame)

    def test_ichimoku_has_columns(self, analyzer):
        result = analyzer.calc_ichimoku()
        assert len(result.columns) >= 1

    def test_adx_returns_dataframe(self, analyzer):
        result = analyzer.calc_adx()
        assert isinstance(result, pd.DataFrame)

    def test_adx_has_adx_column(self, analyzer):
        result = analyzer.calc_adx()
        cols = result.columns.tolist()
        assert any("ADX_" in c for c in cols)

    def test_adx_non_negative(self, analyzer):
        result = analyzer.calc_adx().dropna()
        adx_col = [c for c in result.columns if "ADX_" in c][0]
        assert (result[adx_col] >= 0).all()

    def test_cci_returns_series(self, analyzer):
        result = analyzer.calc_cci()
        assert isinstance(result, pd.Series)

    def test_cci_has_values(self, analyzer):
        result = analyzer.calc_cci().dropna()
        assert len(result) > 0

    def test_williams_r_returns_series(self, analyzer):
        result = analyzer.calc_williams_r()
        assert isinstance(result, pd.Series)

    def test_williams_r_range(self, analyzer):
        result = analyzer.calc_williams_r().dropna()
        assert (result >= -100).all() and (result <= 0).all()

    def test_obv_returns_series(self, analyzer):
        result = analyzer.calc_obv()
        assert isinstance(result, pd.Series)

    def test_obv_length(self, analyzer):
        result = analyzer.calc_obv()
        assert len(result) == len(analyzer.df)


# ---------------------------------------------------------------------------
# calc_all 통합 테스트
# ---------------------------------------------------------------------------

class TestCalcAll:
    def test_calc_all_returns_dataframe(self, analyzer):
        result = analyzer.calc_all()
        assert isinstance(result, pd.DataFrame)

    def test_calc_all_contains_ohlcv(self, analyzer):
        result = analyzer.calc_all()
        for col in ["open", "high", "low", "close", "volume"]:
            assert col in result.columns

    def test_calc_all_contains_rsi(self, analyzer):
        result = analyzer.calc_all()
        assert "RSI_14" in result.columns

    def test_calc_all_contains_sma(self, analyzer):
        result = analyzer.calc_all()
        assert "SMA_20" in result.columns

    def test_calc_all_contains_ema(self, analyzer):
        result = analyzer.calc_all()
        assert "EMA_20" in result.columns

    def test_calc_all_contains_obv(self, analyzer):
        result = analyzer.calc_all()
        assert "OBV" in result.columns

    def test_calc_all_row_count(self, analyzer):
        result = analyzer.calc_all()
        assert len(result) == len(analyzer.df)


# ---------------------------------------------------------------------------
# P2-03: calc_atr 테스트
# ---------------------------------------------------------------------------

class TestCalcAtr:
    def test_calc_atr_basic(self, analyzer):
        """정상 데이터에서 ATR > 0"""
        df = make_sample_ohlcv(100)
        result = analyzer.calc_atr(df, period=14)
        assert result > 0.0

    def test_calc_atr_insufficient_data(self, analyzer):
        """데이터 부족 시 0.0 반환"""
        df = make_sample_ohlcv(10)  # period=14보다 작음
        result = analyzer.calc_atr(df, period=14)
        assert result == 0.0

    def test_calc_atr_returns_float(self, analyzer):
        """반환 타입은 float"""
        df = make_sample_ohlcv(100)
        result = analyzer.calc_atr(df)
        assert isinstance(result, float)
