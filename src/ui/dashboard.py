"""T060-T064 메인 대시보드 뷰
버전: v1.0
설명: 계좌 요약, 일일 손익, 자동매매 상태, 감성 게이지, 지수 미니차트
"""

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors


class AccountSummary(QWidget):
    """T060 계좌 요약 위젯 - 총자산, 수익률, 예수금 표시."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("계좌 요약")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._total_asset_label = QLabel("0")
        self._profit_rate_label = QLabel("0")
        self._deposit_label = QLabel("0")

        for label_name, widget in [
            ("총자산", self._total_asset_label),
            ("수익률", self._profit_rate_label),
            ("예수금", self._deposit_label),
        ]:
            row = QHBoxLayout()
            name_label = QLabel(label_name)
            name_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            row.addWidget(name_label)
            row.addStretch()
            widget.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            row.addWidget(widget)
            layout.addLayout(row)

    def set_data(self, total_asset: int, profit_rate: float, deposit: int) -> None:
        """계좌 데이터 설정."""
        self._total_asset_label.setText(f"{total_asset:,}")
        self._profit_rate_label.setText(f"{profit_rate}%")
        self._deposit_label.setText(f"{deposit:,}")


class DailyPnL(QWidget):
    """T061 일일 손익 위젯 - 실현/미실현 손익, 수익률 컬러코딩."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("일일 손익")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._realized_label = QLabel("0")
        self._unrealized_label = QLabel("0")
        self._rate_label = QLabel("0")

        for label_name, widget in [
            ("실현 손익", self._realized_label),
            ("미실현 손익", self._unrealized_label),
            ("수익률", self._rate_label),
        ]:
            row = QHBoxLayout()
            name_label = QLabel(label_name)
            name_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            row.addWidget(name_label)
            row.addStretch()
            widget.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            row.addWidget(widget)
            layout.addLayout(row)

    def set_data(self, realized: int, unrealized: int, rate: float) -> None:
        """손익 데이터 설정."""
        self._realized_label.setText(f"{realized:,}")
        self._unrealized_label.setText(f"{unrealized:,}")
        self._rate_label.setText(f"{rate}%")

        if rate > 0:
            self._rate_label.setStyleSheet(f"color: {Colors.BULLISH};")
        elif rate < 0:
            self._rate_label.setStyleSheet(f"color: {Colors.BEARISH};")
        else:
            self._rate_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")


class AutoTradeStatus(QWidget):
    """T062 자동매매 상태 위젯 - 전략명, 체결 건수, 실행 상태."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("자동매매 상태")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._strategy_label = QLabel("-")
        self._filled_label = QLabel("0")
        self._status_label = QLabel("중지")

        for label_name, widget in [
            ("전략", self._strategy_label),
            ("체결 건수", self._filled_label),
            ("상태", self._status_label),
        ]:
            row = QHBoxLayout()
            name_label = QLabel(label_name)
            name_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            row.addWidget(name_label)
            row.addStretch()
            widget.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
            row.addWidget(widget)
            layout.addLayout(row)

    def set_status(self, strategy_name: str, filled_count: int, is_running: bool) -> None:
        """자동매매 상태 설정."""
        self._strategy_label.setText(strategy_name)
        self._filled_label.setText(str(filled_count))
        if is_running:
            self._status_label.setText("실행 중")
            self._status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
        else:
            self._status_label.setText("중지")
            self._status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")


class SentimentGauge(QWidget):
    """T063 감성 게이지 위젯 - 감성 점수 QProgressBar(-100~+100)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("시장 감성")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._progress = QProgressBar()
        self._progress.setMinimum(0)
        self._progress.setMaximum(200)
        self._progress.setValue(100)
        layout.addWidget(self._progress)

        self._reasoning_label = QLabel("")
        self._reasoning_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        self._reasoning_label.setWordWrap(True)
        layout.addWidget(self._reasoning_label)

    def set_score(self, score: int, reasoning: str) -> None:
        """감성 점수 설정. score: -100~+100 -> 내부 0~200 변환."""
        self._progress.setValue(score + 100)
        self._reasoning_label.setText(reasoning)


class IndexMiniChart(QWidget):
    """T064 지수 미니차트 위젯 - KOSPI/KOSDAQ 라벨 + 현재가 + 등락률."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        self._name_label = QLabel("-")
        self._name_label.setStyleSheet(
            f"font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(self._name_label)

        self._price_label = QLabel("-")
        self._price_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(self._price_label)

        self._change_label = QLabel("-")
        self._change_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(self._change_label)

        layout.addStretch()

    def set_index(self, name: str, price: float, change_rate: float) -> None:
        """지수 정보 설정."""
        self._name_label.setText(name)
        self._price_label.setText(str(price))
        self._change_label.setText(f"{change_rate}%")

        if change_rate > 0:
            self._change_label.setStyleSheet(f"color: {Colors.BULLISH};")
        elif change_rate < 0:
            self._change_label.setStyleSheet(f"color: {Colors.BEARISH};")
        else:
            self._change_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")


class DashboardView(QWidget):
    """메인 대시보드 뷰 - 5개 서브 위젯을 QVBoxLayout으로 조합."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        self._account_summary = AccountSummary()
        self._daily_pnl = DailyPnL()
        self._auto_trade_status = AutoTradeStatus()
        self._sentiment_gauge = SentimentGauge()
        self._index_mini_chart = IndexMiniChart()

        layout.addWidget(self._account_summary)
        layout.addWidget(self._daily_pnl)
        layout.addWidget(self._auto_trade_status)
        layout.addWidget(self._sentiment_gauge)
        layout.addWidget(self._index_mini_chart)
