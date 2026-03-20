"""T065-T069 차트 분석 뷰
버전: v2.0
설명: 캔들스틱 차트(matplotlib), 오버레이, 보조지표 패널, 타임프레임 선택, 매매 마커
변경: v1.0 -> v2.0: QLabel placeholder를 CandlestickCanvas(matplotlib)로 교체,
      볼린저밴드/이동평균선 오버레이, 거래량 바 차트, 매매 마커 실제 렌더링
"""

import matplotlib
matplotlib.use("Agg")
# 한국어 폰트 설정 (깨짐 방지)
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

import numpy as np
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors


class CandlestickCanvas(FigureCanvasQTAgg):
    """OHLCV DataFrame을 캔들스틱 차트로 렌더링하는 matplotlib 캔버스."""

    COLOR_UP = "#00d4aa"
    COLOR_DOWN = "#ff6b6b"
    COLOR_BG = "#1a1a2e"
    COLOR_AXES_BG = "#16213e"
    COLOR_TICK = "#8892b0"
    COLOR_SPINE = "#2a2a4a"
    COLOR_TEXT = "#e0e0e0"

    def __init__(self, parent=None):
        self._fig = Figure(figsize=(8, 6), dpi=100)
        self._fig.set_facecolor(self.COLOR_BG)
        super().__init__(self._fig)
        self._ax_price = self._fig.add_axes([0.08, 0.3, 0.88, 0.65])
        self._ax_volume = self._fig.add_axes([0.08, 0.05, 0.88, 0.2])
        self._setup_axes()
        self._df: pd.DataFrame | None = None
        self._overlays: list[str] = []

    def _setup_axes(self) -> None:
        """축 스타일 설정."""
        for ax in [self._ax_price, self._ax_volume]:
            ax.set_facecolor(self.COLOR_AXES_BG)
            ax.tick_params(colors=self.COLOR_TICK, labelsize=8)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_color(self.COLOR_SPINE)
            ax.spines["left"].set_color(self.COLOR_SPINE)

    def update_chart(self, df: pd.DataFrame | None, overlays: list[str] | None = None) -> None:
        """OHLCV DataFrame으로 캔들스틱 + 거래량 차트 갱신."""
        self._ax_price.clear()
        self._ax_volume.clear()
        self._setup_axes()

        if df is None or df.empty:
            self.draw()
            return

        self._df = df.copy()
        if overlays is not None:
            self._overlays = list(overlays)

        n = len(df)
        x = np.arange(n)

        # 캔들스틱
        for i in range(n):
            row = df.iloc[i]
            o, h, l, c = row["open"], row["high"], row["low"], row["close"]
            color = self.COLOR_UP if c >= o else self.COLOR_DOWN
            body_bottom = min(o, c)
            body_height = abs(c - o)
            if body_height == 0:
                body_height = (h - l) * 0.01 if h != l else 0.1
            self._ax_price.bar(
                i, body_height, bottom=body_bottom,
                width=0.6, color=color, edgecolor=color, linewidth=0.5,
            )
            self._ax_price.vlines(i, l, h, color=color, linewidth=0.8)

        # 오버레이
        closes = df["close"].values
        for ov in self._overlays:
            self._draw_overlay(x, df, ov)

        # 거래량
        vol_colors = [
            self.COLOR_UP if df.iloc[i]["close"] >= df.iloc[i]["open"] else self.COLOR_DOWN
            for i in range(n)
        ]
        self._ax_volume.bar(x, df["volume"].values, color=vol_colors, alpha=0.6, width=0.6)

        # x축 라벨
        if n > 0:
            step = max(1, n // 6)
            tick_positions = list(range(0, n, step))
            tick_labels = []
            for pos in tick_positions:
                idx = df.index[pos] if pos < n else df.index[-1]
                if hasattr(idx, "strftime"):
                    tick_labels.append(idx.strftime("%m/%d"))
                else:
                    tick_labels.append(str(idx)[-5:])
            self._ax_volume.set_xticks(tick_positions)
            self._ax_volume.set_xticklabels(tick_labels, rotation=0)
            self._ax_price.set_xticks([])

        self.draw()

    def _draw_overlay(self, x: np.ndarray, df: pd.DataFrame, overlay_name: str) -> None:
        """오버레이 지표를 가격 차트에 그린다."""
        closes = df["close"].values
        upper_name = overlay_name.upper()

        if upper_name.startswith("MA") or upper_name.startswith("SMA"):
            period = self._extract_period(overlay_name, default=20)
            if len(closes) >= period:
                ma = pd.Series(closes).rolling(window=period).mean().values
                self._ax_price.plot(x, ma, color="#ffd700", linewidth=1.0, alpha=0.8, label=overlay_name)

        elif upper_name.startswith("EMA"):
            period = self._extract_period(overlay_name, default=20)
            if len(closes) >= period:
                ema = pd.Series(closes).ewm(span=period, adjust=False).mean().values
                self._ax_price.plot(x, ema, color="#ff9f43", linewidth=1.0, alpha=0.8, label=overlay_name)

        elif upper_name.startswith("BB") or upper_name.startswith("BOLLINGER"):
            period = self._extract_period(overlay_name, default=20)
            if len(closes) >= period:
                s = pd.Series(closes)
                ma = s.rolling(window=period).mean()
                std = s.rolling(window=period).std()
                upper = (ma + 2 * std).values
                lower = (ma - 2 * std).values
                ma_vals = ma.values
                self._ax_price.plot(x, ma_vals, color="#ffd700", linewidth=0.8, alpha=0.7)
                self._ax_price.plot(x, upper, color="#64b5f6", linewidth=0.6, alpha=0.6)
                self._ax_price.plot(x, lower, color="#64b5f6", linewidth=0.6, alpha=0.6)
                self._ax_price.fill_between(x, lower, upper, alpha=0.05, color="#64b5f6")

        self._ax_price.legend(loc="upper left", fontsize=7, facecolor="#1a1a2e",
                              edgecolor="#2a2a4a", labelcolor="#8892b0")

    @staticmethod
    def _extract_period(name: str, default: int = 20) -> int:
        """오버레이 이름에서 기간 숫자를 추출한다. 예: 'MA20' -> 20."""
        digits = "".join(c for c in name if c.isdigit())
        return int(digits) if digits else default

    def draw_markers(self, markers: list[dict]) -> None:
        """매매 마커를 가격 차트에 표시한다."""
        if self._df is None or self._df.empty or not markers:
            return
        for m in markers:
            price = m.get("price", 0)
            marker_type = m.get("type", "")
            idx = m.get("index")
            if idx is None:
                continue
            if marker_type == "buy":
                self._ax_price.scatter(idx, price, marker="^", color=self.COLOR_UP, s=60, zorder=5)
            elif marker_type == "sell":
                self._ax_price.scatter(idx, price, marker="v", color=self.COLOR_DOWN, s=60, zorder=5)
        self.draw()


class ChartView(QWidget):
    """T065-T066, T069 차트 뷰 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._overlays: list[str] = []
        self._markers: list[dict] = []
        self._df: pd.DataFrame | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self._stock_label = QLabel("-")
        self._stock_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(self._stock_label)

        # 타임프레임 선택 위젯
        self._timeframe_selector = TimeframeSelector(self)
        self._timeframe_selector.timeframe_changed.connect(self._on_timeframe_changed)
        layout.addWidget(self._timeframe_selector)

        # 캔들스틱 차트 캔버스
        self._canvas = CandlestickCanvas(self)
        self._canvas.setMinimumHeight(200)
        layout.addWidget(self._canvas)

        # 보조지표 패널
        self._sub_indicator_panel = SubIndicatorPanel(self)
        layout.addWidget(self._sub_indicator_panel)

    def _on_timeframe_changed(self, timeframe: str) -> None:
        """타임프레임 변경 처리 (외부 연결용 슬롯)."""
        pass

    def set_stock_name(self, name: str) -> None:
        """종목명 설정."""
        self._stock_label.setText(name)

    def set_data(self, df: pd.DataFrame) -> None:
        """OHLCV 데이터를 설정하고 차트를 갱신한다."""
        self._df = df
        self._canvas.update_chart(df, self._overlays)
        if self._markers:
            self._canvas.draw_markers(self._markers)

    def add_overlay(self, indicator_name: str) -> None:
        """T066 오버레이 추가 (중복 무시)."""
        if indicator_name not in self._overlays:
            self._overlays.append(indicator_name)
        if self._df is not None:
            self._canvas.update_chart(self._df, self._overlays)

    def get_overlays(self) -> list[str]:
        """오버레이 목록 반환."""
        return list(self._overlays)

    def add_trade_markers(self, markers: list[dict]) -> None:
        """T069 매매 마커 데이터 저장 및 표시."""
        self._markers.extend(markers)
        if self._df is not None:
            self._canvas.draw_markers(markers)

    def get_markers(self) -> list[dict]:
        """마커 데이터 반환."""
        return list(self._markers)

    @property
    def canvas(self) -> CandlestickCanvas:
        """차트 캔버스 접근."""
        return self._canvas


class SubIndicatorPanel(QWidget):
    """T067 보조지표 패널 - RSI/MACD/스토캐스틱 선택."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        label = QLabel("보조지표")
        label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(label)

        self._combo = QComboBox()
        self._combo.addItems(["RSI", "MACD", "Stochastic"])
        layout.addWidget(self._combo)


class TimeframeSelector(QWidget):
    """T068 타임프레임 선택 위젯."""

    timeframe_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_timeframe: str = "일"
        self._buttons: list[QPushButton] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        for tf in ["1분", "5분", "15분", "일", "주", "월"]:
            btn = QPushButton(tf)
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda checked, t=tf: self._on_clicked(t))
            self._buttons.append(btn)
            layout.addWidget(btn)

    def _on_clicked(self, timeframe: str) -> None:
        """버튼 클릭 처리."""
        self._selected_timeframe = timeframe
        self.timeframe_changed.emit(timeframe)

    @property
    def selected_timeframe(self) -> str:
        """현재 선택된 타임프레임."""
        return self._selected_timeframe
