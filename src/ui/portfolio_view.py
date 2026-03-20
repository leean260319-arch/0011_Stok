"""T077-T079 포트폴리오 뷰
버전: v2.0
설명: 포트폴리오 테이블, 비중 파이 차트(matplotlib), 수익률 라인 차트(matplotlib)
변경: v1.0 -> v2.0: AllocationChart/ReturnChart QLabel placeholder를
      matplotlib FigureCanvasQTAgg 기반 실제 차트로 교체
"""

import matplotlib
matplotlib.use("Agg")
# 한국어 폰트 설정 (깨짐 방지)
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors


class PortfolioView(QWidget):
    """T077 포트폴리오 뷰 - 종목명/수량/평균단가/현재가/수익률/평가금액."""

    _COLUMNS = ["종목명", "수량", "평균단가", "현재가", "수익률", "평가금액"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("포트폴리오")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._table = QTableWidget(0, len(self._COLUMNS))
        self._table.setHorizontalHeaderLabels(self._COLUMNS)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self._table)

        # 비중 파이 차트
        self._allocation_chart = AllocationChart(self)
        layout.addWidget(self._allocation_chart)

        # 수익률 라인 차트
        self._return_chart = ReturnChart(self)
        layout.addWidget(self._return_chart)

    def add_stock(
        self, name: str, qty: int, avg_price: int, current_price: int
    ) -> None:
        """종목 추가."""
        row = self._table.rowCount()
        self._table.insertRow(row)

        profit_rate = (current_price - avg_price) / avg_price * 100 if avg_price else 0
        eval_amount = current_price * qty

        values = [
            name,
            str(qty),
            f"{avg_price:,}",
            f"{current_price:,}",
            f"{profit_rate:.2f}%",
            f"{eval_amount:,}",
        ]
        for col, value in enumerate(values):
            self._table.setItem(row, col, QTableWidgetItem(value))

    def get_stock_count(self) -> int:
        """종목 수 반환."""
        return self._table.rowCount()


class AllocationChart(FigureCanvasQTAgg):
    """T078 비중 차트 위젯 - matplotlib 파이 차트."""

    _PIE_COLORS = [
        "#00d4aa", "#ff6b6b", "#ffd700", "#64b5f6",
        "#ff9f43", "#a29bfe", "#fd79a8", "#55efc4",
        "#74b9ff", "#dfe6e9",
    ]

    def __init__(self, parent=None):
        self._fig = Figure(figsize=(4, 3), dpi=100)
        self._fig.set_facecolor("#1a1a2e")
        super().__init__(self._fig)
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor("#1a1a2e")
        self._data: list[dict] = []
        self._draw_empty()

    def _draw_empty(self) -> None:
        """빈 상태 표시."""
        self._ax.clear()
        self._ax.set_facecolor("#1a1a2e")
        self._ax.text(
            0.5, 0.5, "데이터 없음",
            ha="center", va="center", color="#8892b0", fontsize=10,
            transform=self._ax.transAxes,
        )
        self._ax.set_xticks([])
        self._ax.set_yticks([])
        for spine in self._ax.spines.values():
            spine.set_visible(False)
        self.draw()

    def set_data(self, allocations: list[dict]) -> None:
        """비중 데이터 설정 및 파이 차트 갱신.

        Args:
            allocations: [{"name": "삼성전자", "weight": 30.0}, ...] 형태
        """
        self._data = list(allocations)
        self._ax.clear()
        self._ax.set_facecolor("#1a1a2e")

        if not self._data:
            self._draw_empty()
            return

        labels = [d.get("name", "") for d in self._data]
        values = [d.get("weight", d.get("ratio", 0)) for d in self._data]
        colors = self._PIE_COLORS[: len(values)]

        wedges, texts, autotexts = self._ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors,
            textprops={"color": "#e0e0e0", "fontsize": 8},
            pctdistance=0.75,
            startangle=90,
        )
        for t in autotexts:
            t.set_fontsize(7)
            t.set_color("#e0e0e0")

        self._fig.tight_layout(pad=0.5)
        self.draw()

    def get_data(self) -> list[dict]:
        """비중 데이터 반환."""
        return list(self._data)


class ReturnChart(FigureCanvasQTAgg):
    """T079 수익률 차트 위젯 - matplotlib 라인 차트."""

    def __init__(self, parent=None):
        self._fig = Figure(figsize=(4, 3), dpi=100)
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

    def add_point(self, date: str, cumulative_return: float) -> None:
        """수익률 데이터 포인트 추가."""
        self._data.append({"date": date, "cumulative_return": cumulative_return})

    def get_data(self) -> list[dict]:
        """수익률 데이터 반환."""
        return list(self._data)

    def update_chart(self) -> None:
        """저장된 데이터로 차트 갱신."""
        self._ax.clear()
        self._setup_ax()

        if not self._data:
            self._draw_empty()
            return

        dates = [d["date"] for d in self._data]
        returns = [d["cumulative_return"] for d in self._data]
        x = range(len(dates))

        self._ax.plot(x, returns, color="#00d4aa", linewidth=1.5)
        self._ax.fill_between(x, returns, alpha=0.1, color="#00d4aa")

        # 0선
        self._ax.axhline(y=0, color="#8892b0", linewidth=0.5, linestyle="--", alpha=0.5)

        # x축 라벨
        n = len(dates)
        if n > 0:
            step = max(1, n // 5)
            tick_pos = list(range(0, n, step))
            tick_labels = [dates[p][-5:] if len(dates[p]) > 5 else dates[p] for p in tick_pos]
            self._ax.set_xticks(tick_pos)
            self._ax.set_xticklabels(tick_labels, rotation=0)

        self._ax.set_ylabel("수익률 (%)", color="#8892b0", fontsize=8)
        self._fig.tight_layout(pad=0.5)
        self.draw()

    def set_data_and_draw(self, dates: list[str], returns: list[float]) -> None:
        """날짜/수익률 리스트를 한번에 설정하고 차트를 그린다."""
        self._data = [
            {"date": d, "cumulative_return": r}
            for d, r in zip(dates, returns)
        ]
        self.update_chart()
