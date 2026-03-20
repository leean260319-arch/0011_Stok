"""T080-T081 관심 종목 뷰
버전: v2.0
설명: 관심 종목 그룹 관리, 실시간 시세 테이블 통합
변경: v1.0 -> v2.0: WatchlistView에 RealtimeTable 위젯을 실제로 통합
"""

from PyQt6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.utils.constants import Colors


class RealtimeTable(QWidget):
    """T081 실시간 시세 테이블 위젯."""

    _COLUMNS = ["종목코드", "현재가", "등락률", "거래량", "AI점수"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stock_rows: dict[str, int] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("실시간 시세")
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

    def update_stock(
        self,
        code: str,
        price: int,
        change_rate: float,
        volume: int,
        ai_score: float,
    ) -> None:
        """종목 데이터 추가 또는 갱신."""
        if code in self._stock_rows:
            row = self._stock_rows[code]
        else:
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._stock_rows[code] = row

        values = [
            code,
            f"{price:,}",
            f"{change_rate}%",
            f"{volume:,}",
            f"{ai_score}",
        ]
        for col, value in enumerate(values):
            self._table.setItem(row, col, QTableWidgetItem(value))

    def get_stock_count(self) -> int:
        """등록된 종목 수 반환."""
        return self._table.rowCount()

    def clear(self) -> None:
        """테이블 초기화."""
        self._table.setRowCount(0)
        self._stock_rows.clear()


class WatchlistView(QWidget):
    """T080 관심 종목 뷰 - 그룹 관리 + RealtimeTable 통합."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._groups: dict[str, list[str]] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("관심 종목")
        title.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        # 실시간 시세 테이블 통합
        self._realtime_table = RealtimeTable(self)
        layout.addWidget(self._realtime_table)

    @property
    def realtime_table(self) -> RealtimeTable:
        """통합된 RealtimeTable 접근."""
        return self._realtime_table

    def create_group(self, name: str) -> None:
        """그룹 생성."""
        if name not in self._groups:
            self._groups[name] = []

    def delete_group(self, name: str) -> None:
        """그룹 삭제."""
        self._groups.pop(name, None)

    def add_stock(self, group: str, code: str) -> None:
        """그룹에 종목 추가."""
        if group in self._groups and code not in self._groups[group]:
            self._groups[group].append(code)

    def remove_stock(self, group: str, code: str) -> None:
        """그룹에서 종목 제거."""
        if group in self._groups and code in self._groups[group]:
            self._groups[group].remove(code)

    def get_groups(self) -> dict:
        """그룹 목록 반환."""
        return {k: list(v) for k, v in self._groups.items()}

    def update_realtime(
        self, code: str, price: int, change_rate: float, volume: int, ai_score: float
    ) -> None:
        """실시간 시세를 RealtimeTable에 전달한다."""
        self._realtime_table.update_stock(code, price, change_rate, volume, ai_score)
