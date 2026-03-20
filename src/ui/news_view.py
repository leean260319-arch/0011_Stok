"""T070-T072 뉴스 분석 뷰
버전: v2.0
설명: 뉴스 피드, 감성 트렌드 차트(matplotlib), AI 요약 패널
변경: v1.0 -> v2.0: SentimentTrendChart QLabel placeholder를
      matplotlib FigureCanvasQTAgg 기반 라인 차트로 교체
"""

import webbrowser
import matplotlib
matplotlib.use("Agg")
# 한국어 폰트 설정 (깨짐 방지)
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

from datetime import datetime

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors

_SENTIMENT_COLORS = {
    "positive": Colors.BULLISH,
    "negative": Colors.BEARISH,
    "neutral": Colors.TEXT_SECONDARY,
}


class NewsView(QWidget):
    """T070 뉴스 피드 위젯 - QListWidget 기반, 감성별 색상."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("뉴스 피드")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._list_widget = QListWidget()
        self._list_widget.setStyleSheet(
            f"QListWidget {{ background-color: {Colors.SURFACE};"
            f" border: 1px solid {Colors.BORDER}; border-radius: 4px; }}"
        )
        # 뉴스 아이템 클릭 시 URL 열기
        self._list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list_widget)

        # 감성 트렌드 차트
        self._sentiment_chart = SentimentTrendChart(self)
        layout.addWidget(self._sentiment_chart)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """뉴스 아이템 클릭 시 URL을 브라우저로 열기."""
        url = item.data(256)
        if url:
            webbrowser.open(url)

    def add_news(self, title: str, source: str, sentiment: str, url: str) -> None:
        """뉴스 추가. sentiment: positive/negative/neutral."""
        text = f"[{source}] {title}"
        item = QListWidgetItem(text)
        color_hex = _SENTIMENT_COLORS.get(sentiment, Colors.TEXT_SECONDARY)
        item.setForeground(QColor(color_hex))
        item.setData(256, url)  # Qt.UserRole = 256
        self._list_widget.addItem(item)


class SentimentTrendChart(FigureCanvasQTAgg):
    """T071 감성 트렌드 차트 위젯 - matplotlib 라인 차트."""

    def __init__(self, parent=None):
        self._fig = Figure(figsize=(4, 2.5), dpi=100)
        self._fig.set_facecolor("#1a1a2e")
        super().__init__(self._fig)
        self._ax = self._fig.add_subplot(111)
        self._data: list[dict] = []
        self._setup_ax()
        self._draw_empty()

    def _setup_ax(self) -> None:
        """축 스타일 설정."""
        self._ax.set_facecolor("#16213e")
        self._ax.tick_params(colors="#8892b0", labelsize=8)
        self._ax.spines["top"].set_visible(False)
        self._ax.spines["right"].set_visible(False)
        self._ax.spines["bottom"].set_color("#2a2a4a")
        self._ax.spines["left"].set_color("#2a2a4a")

    def _draw_empty(self) -> None:
        """빈 상태 표시."""
        self._ax.clear()
        self._setup_ax()
        self._ax.text(
            0.5, 0.5, "데이터 없음",
            ha="center", va="center", color="#8892b0", fontsize=10,
            transform=self._ax.transAxes,
        )
        self.draw()

    def add_point(self, timestamp: datetime, score: float) -> None:
        """데이터 포인트 추가."""
        self._data.append({"timestamp": timestamp, "score": score})

    def get_data(self) -> list[dict]:
        """데이터 반환."""
        return list(self._data)

    def update_chart(self) -> None:
        """저장된 데이터로 감성 트렌드 차트를 갱신한다."""
        self._ax.clear()
        self._setup_ax()

        if not self._data:
            self._draw_empty()
            return

        timestamps = [d["timestamp"] for d in self._data]
        scores = [d["score"] for d in self._data]
        x = range(len(timestamps))

        # 감성 점수 라인
        self._ax.plot(x, scores, color="#ffd700", linewidth=1.5)
        self._ax.fill_between(
            x, scores, 0,
            where=[s >= 0 for s in scores],
            alpha=0.15, color="#00d4aa", interpolate=True,
        )
        self._ax.fill_between(
            x, scores, 0,
            where=[s < 0 for s in scores],
            alpha=0.15, color="#ff6b6b", interpolate=True,
        )

        # 0선
        self._ax.axhline(y=0, color="#8892b0", linewidth=0.5, linestyle="--", alpha=0.5)

        # x축 라벨
        n = len(timestamps)
        if n > 0:
            step = max(1, n // 5)
            tick_pos = list(range(0, n, step))
            tick_labels = []
            for p in tick_pos:
                ts = timestamps[p]
                if hasattr(ts, "strftime"):
                    tick_labels.append(ts.strftime("%m/%d %H:%M"))
                else:
                    tick_labels.append(str(ts)[-5:])
            self._ax.set_xticks(tick_pos)
            self._ax.set_xticklabels(tick_labels, rotation=0)

        self._ax.set_ylabel("감성 점수", color="#8892b0", fontsize=8)
        self._ax.set_ylim(-1.1, 1.1)
        self._fig.tight_layout(pad=0.5)
        self.draw()


class NewsSummaryPanel(QWidget):
    """T072 AI 요약 패널 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("AI 뉴스 요약")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._summary_label = QLabel("")
        self._summary_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        self._summary_label.setWordWrap(True)
        layout.addWidget(self._summary_label)

    def set_summary(self, text: str) -> None:
        """AI 요약 텍스트 설정."""
        self._summary_label.setText(text)
