"""T089-T090: 백테스팅 뷰 - 전략 선택, 기간 설정, 결과 표시, 시각화 데이터, 에퀴티 커브 차트
버전: v2.0
변경: v1.0 -> v2.0: 에퀴티 커브 matplotlib 차트 추가, run_backtest 슬롯 추가
"""

import matplotlib
matplotlib.use("Agg")
# 한국어 폰트 설정 (깨짐 방지)
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors


class EquityCurveCanvas(FigureCanvasQTAgg):
    """백테스트 에퀴티 커브 차트."""

    def __init__(self, parent=None):
        self._fig = Figure(figsize=(6, 3), dpi=100)
        self._fig.set_facecolor("#1a1a2e")
        super().__init__(self._fig)
        self._ax = self._fig.add_subplot(111)
        self._setup_ax()

    def _setup_ax(self) -> None:
        self._ax.set_facecolor("#16213e")
        self._ax.tick_params(colors="#8892b0", labelsize=8)
        self._ax.spines["top"].set_visible(False)
        self._ax.spines["right"].set_visible(False)
        self._ax.spines["bottom"].set_color("#2a2a4a")
        self._ax.spines["left"].set_color("#2a2a4a")

    def update_chart(self, dates: list, values: list, trade_points: list[dict] | None = None) -> None:
        """에퀴티 커브와 매매 포인트를 그린다."""
        self._ax.clear()
        self._setup_ax()

        if not dates or not values:
            self._ax.text(
                0.5, 0.5, "백테스트를 실행하세요",
                ha="center", va="center", color="#8892b0", fontsize=10,
                transform=self._ax.transAxes,
            )
            self.draw()
            return

        x = range(len(dates))
        self._ax.plot(x, values, color="#00d4aa", linewidth=1.2)
        self._ax.fill_between(x, values, values[0], alpha=0.08, color="#00d4aa")

        # 매매 포인트
        if trade_points:
            for tp in trade_points:
                idx = tp.get("index")
                val = tp.get("value")
                action = tp.get("action", "")
                if idx is not None and val is not None:
                    if action == "매수":
                        self._ax.scatter(idx, val, marker="^", color="#00d4aa", s=40, zorder=5)
                    elif action == "매도":
                        self._ax.scatter(idx, val, marker="v", color="#ff6b6b", s=40, zorder=5)

        # x축 라벨
        n = len(dates)
        step = max(1, n // 5)
        tick_pos = list(range(0, n, step))
        tick_labels = [str(dates[p])[-5:] for p in tick_pos]
        self._ax.set_xticks(tick_pos)
        self._ax.set_xticklabels(tick_labels, rotation=0)

        self._ax.set_ylabel("자산 (원)", color="#8892b0", fontsize=8)
        self._fig.tight_layout(pad=0.5)
        self.draw()


class BacktestView(QWidget):
    """백테스팅 뷰 위젯.

    Signals:
        run_clicked: 실행 버튼 클릭 시그널
    """

    run_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._equity_dates: list = []
        self._equity_values: list = []
        self._trade_points: list[dict] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 구성."""
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # 설정 그룹
        settings_box = QGroupBox("백테스팅 설정")
        form = QFormLayout(settings_box)

        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["AI 종합 전략", "모멘텀 전략", "평균 회귀 전략"])
        form.addRow("전략 선택", self.strategy_combo)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate(2025, 1, 1))
        form.addRow("시작일", self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        form.addRow("종료일", self.end_date)

        self.initial_cash = QSpinBox()
        self.initial_cash.setRange(1_000_000, 1_000_000_000)
        self.initial_cash.setSingleStep(1_000_000)
        self.initial_cash.setValue(10_000_000)
        self.initial_cash.setSuffix(" 원")
        form.addRow("초기 자금", self.initial_cash)

        self.run_button = QPushButton("백테스팅 실행")
        self.run_button.clicked.connect(self.run_clicked.emit)
        form.addRow(self.run_button)

        root.addWidget(settings_box)

        # 결과 그룹
        result_box = QGroupBox("백테스팅 결과")
        result_layout = QFormLayout(result_box)

        self.label_total_return = QLabel("-")
        self.label_max_drawdown = QLabel("-")
        self.label_win_rate = QLabel("-")
        self.label_sharpe_ratio = QLabel("-")
        self.label_total_trades = QLabel("-")

        result_layout.addRow("총 수익률 (%)", self.label_total_return)
        result_layout.addRow("최대 낙폭 (%)", self.label_max_drawdown)
        result_layout.addRow("승률 (%)", self.label_win_rate)
        result_layout.addRow("샤프 비율", self.label_sharpe_ratio)
        result_layout.addRow("총 거래 수", self.label_total_trades)

        root.addWidget(result_box)

        # 에퀴티 커브 차트
        self._equity_canvas = EquityCurveCanvas(self)
        self._equity_canvas.setMinimumHeight(150)
        root.addWidget(self._equity_canvas)

        root.addStretch()

    def set_result(self, result) -> None:
        """BacktestResult로 결과 라벨을 업데이트한다."""
        self.label_total_return.setText(f"{result.total_return:.1f}%")
        self.label_max_drawdown.setText(f"{result.max_drawdown:.1f}%")
        self.label_win_rate.setText(f"{result.win_rate:.1f}%")
        self.label_sharpe_ratio.setText(f"{result.sharpe_ratio:.1f}")
        self.label_total_trades.setText(str(result.total_trades))

    def set_equity_curve(self, dates: list, values: list) -> None:
        """누적 수익률 데이터를 저장하고 차트를 갱신한다."""
        self._equity_dates = dates
        self._equity_values = values
        self._equity_canvas.update_chart(dates, values, self._trade_points)

    def get_equity_data(self) -> tuple[list, list]:
        """누적 수익률 데이터를 반환한다."""
        return self._equity_dates, self._equity_values

    def set_trade_points(self, trades: list[dict]) -> None:
        """매매 포인트 데이터를 저장한다."""
        self._trade_points = trades

    def get_trade_points(self) -> list[dict]:
        """매매 포인트 데이터를 반환한다."""
        return self._trade_points

    def run_backtest(self, strategy, df) -> None:
        """BacktestEngine을 사용하여 백테스트를 실행하고 결과를 표시한다.

        Args:
            strategy: Strategy 인스턴스
            df: OHLCV pd.DataFrame
        """
        from src.engine.backtest_engine import BacktestEngine

        cash = self.initial_cash.value()
        engine = BacktestEngine()
        result = engine.run(strategy=strategy, df=df, initial_cash=float(cash))
        self.set_result(result)

    @property
    def equity_canvas(self) -> EquityCurveCanvas:
        """에퀴티 커브 캔버스 접근."""
        return self._equity_canvas
