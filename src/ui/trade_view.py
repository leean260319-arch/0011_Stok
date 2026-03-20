"""T073-T074, T076 자동매매 관리 뷰
버전: v1.0
설명: 전략 목록, 거래 로그, 손실 한도 바
"""

from PyQt6.QtWidgets import (
    QHeaderView,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors


class StrategyList(QWidget):
    """T073 전략 목록 위젯."""

    # 전략 이름 -> 설명 매핑
    _STRATEGY_DESCRIPTIONS: dict[str, str] = {
        "momentum": "RSI/MACD 기반 추세 추종",
        "mean_reversion": "볼린저밴드 기반 평균 회귀",
        "ai_composite": "AI 종합 분석",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._strategies: dict[str, bool] = {}
        self._descriptions: dict[str, str] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("전략 목록")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._list_widget = QListWidget()
        self._list_widget.setStyleSheet(
            f"QListWidget {{ background-color: {Colors.SURFACE};"
            f" border: 1px solid {Colors.BORDER}; }}"
        )
        # 아이템 클릭 시 전략 활성/비활성 토글
        self._list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list_widget)

    def _on_item_clicked(self, item) -> None:
        """리스트 아이템 클릭 시 전략 토글 처리."""
        # 아이템에 저장된 전략 이름으로 토글 (UserRole=256)
        name = item.data(256)
        if name and name in self._strategies:
            self.toggle_strategy(name)

    def add_strategy(self, name: str, is_active: bool, description: str = "") -> None:
        """전략 추가. description이 없으면 내장 매핑에서 자동 조회."""
        self._strategies[name] = is_active
        # 인자로 전달된 설명 우선, 없으면 내장 매핑, 없으면 빈 문자열
        self._descriptions[name] = description or self._STRATEGY_DESCRIPTIONS.get(name, "")
        self._refresh_list()

    def toggle_strategy(self, name: str) -> None:
        """전략 활성/비활성 토글."""
        if name in self._strategies:
            self._strategies[name] = not self._strategies[name]
            self._refresh_list()

    def get_active_strategies(self) -> list[str]:
        """활성 전략 목록 반환."""
        return [name for name, active in self._strategies.items() if active]

    def _refresh_list(self) -> None:
        """리스트 UI 갱신."""
        self._list_widget.clear()
        for name, active in self._strategies.items():
            status = "[ON]" if active else "[OFF]"
            desc = self._descriptions.get(name, "")
            # 설명이 있으면 "상태 전략명 - 설명" 형식으로 표시
            if desc:
                display_text = f"{status} {name} - {desc}"
            else:
                display_text = f"{status} {name}"
            item = QListWidgetItem(display_text)
            # 전략 이름을 UserRole에 저장해 토글 시 정확히 식별
            item.setData(256, name)
            self._list_widget.addItem(item)


class TradeLog(QWidget):
    """T074 거래 로그 위젯 - QTableWidget."""

    _COLUMNS = ["시간", "유형", "종목", "가격", "수량"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("거래 로그")
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

    def add_log(
        self, timestamp: str, event_type: str, stock: str, price: int, quantity: int
    ) -> None:
        """거래 로그 추가."""
        row = self._table.rowCount()
        self._table.insertRow(row)
        for col, value in enumerate(
            [timestamp, event_type, stock, str(price), str(quantity)]
        ):
            self._table.setItem(row, col, QTableWidgetItem(value))


class LossLimitBar(QWidget):
    """T076 손실 한도 바 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("손실 한도")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        self._progress = QProgressBar()
        self._progress.setMinimum(0)
        self._progress.setMaximum(100)
        self._progress.setValue(0)
        layout.addWidget(self._progress)

        self._info_label = QLabel("")
        self._info_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(self._info_label)

    def set_limit(self, current_loss: int, max_limit: int) -> None:
        """손실 한도 설정."""
        if max_limit == 0:
            pct = 0
        else:
            pct = int(current_loss / max_limit * 100)
        self._progress.setValue(pct)
        self._info_label.setText(f"{current_loss:,} / {max_limit:,} ({pct}%)")
