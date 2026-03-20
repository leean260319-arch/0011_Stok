"""T089-T090: BacktestView UI 테스트"""
import pytest
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QLabel,
    QPushButton,
    QSpinBox,
    QWidget,
)
from PyQt6.QtCore import QDate

from src.ui.backtest_view import BacktestView
from src.engine.backtest_engine import BacktestResult


# ---------------------------------------------------------------------------
# T089: BacktestView 레이아웃
# ---------------------------------------------------------------------------
class TestBacktestViewLayout:
    """T089: BacktestView 위젯 구성 검증"""

    def test_is_qwidget(self, qapp):
        view = BacktestView()
        assert isinstance(view, QWidget)

    def test_has_strategy_combo(self, qapp):
        view = BacktestView()
        assert hasattr(view, "strategy_combo")
        assert isinstance(view.strategy_combo, QComboBox)

    def test_has_start_date(self, qapp):
        view = BacktestView()
        assert hasattr(view, "start_date")
        assert isinstance(view.start_date, QDateEdit)

    def test_has_end_date(self, qapp):
        view = BacktestView()
        assert hasattr(view, "end_date")
        assert isinstance(view.end_date, QDateEdit)

    def test_has_initial_cash_spinbox(self, qapp):
        view = BacktestView()
        assert hasattr(view, "initial_cash")
        assert isinstance(view.initial_cash, QSpinBox)

    def test_initial_cash_default(self, qapp):
        view = BacktestView()
        assert view.initial_cash.value() == 10_000_000

    def test_has_run_button(self, qapp):
        view = BacktestView()
        assert hasattr(view, "run_button")
        assert isinstance(view.run_button, QPushButton)

    def test_has_result_labels(self, qapp):
        view = BacktestView()
        assert hasattr(view, "label_total_return")
        assert hasattr(view, "label_max_drawdown")
        assert hasattr(view, "label_win_rate")
        assert hasattr(view, "label_sharpe_ratio")
        assert hasattr(view, "label_total_trades")
        assert isinstance(view.label_total_return, QLabel)
        assert isinstance(view.label_max_drawdown, QLabel)
        assert isinstance(view.label_win_rate, QLabel)
        assert isinstance(view.label_sharpe_ratio, QLabel)
        assert isinstance(view.label_total_trades, QLabel)


# ---------------------------------------------------------------------------
# T089: BacktestView 시그널
# ---------------------------------------------------------------------------
class TestBacktestViewSignal:
    """T089: run_clicked 시그널 검증"""

    def test_run_clicked_signal_emitted(self, qapp):
        view = BacktestView()
        received = []
        view.run_clicked.connect(lambda: received.append(True))
        view.run_button.click()
        assert len(received) == 1


# ---------------------------------------------------------------------------
# T089: set_result
# ---------------------------------------------------------------------------
class TestBacktestViewSetResult:
    """T089: set_result 메서드로 결과 표시"""

    def _make_result(self) -> BacktestResult:
        return BacktestResult(
            initial_cash=10_000_000,
            final_value=11_000_000,
            total_return=10.0,
            max_drawdown=5.5,
            win_rate=65.0,
            sharpe_ratio=1.8,
            total_trades=20,
            trades=[],
        )

    def test_set_result_updates_labels(self, qapp):
        view = BacktestView()
        result = self._make_result()
        view.set_result(result)
        assert "10.0" in view.label_total_return.text()
        assert "5.5" in view.label_max_drawdown.text()
        assert "65.0" in view.label_win_rate.text()
        assert "1.8" in view.label_sharpe_ratio.text()
        assert "20" in view.label_total_trades.text()


# ---------------------------------------------------------------------------
# T090: 결과 시각화 데이터 모델
# ---------------------------------------------------------------------------
class TestBacktestViewVisualization:
    """T090: 누적 수익률 및 매매 포인트 데이터 저장/조회"""

    def test_set_equity_curve(self, qapp):
        view = BacktestView()
        dates = ["2025-01-01", "2025-01-02", "2025-01-03"]
        values = [10_000_000, 10_100_000, 10_200_000]
        view.set_equity_curve(dates, values)
        result_dates, result_values = view.get_equity_data()
        assert result_dates == dates
        assert result_values == values

    def test_set_trade_points(self, qapp):
        view = BacktestView()
        trades = [
            {"date": "2025-01-02", "action": "매수", "price": 50000},
            {"date": "2025-01-05", "action": "매도", "price": 52000},
        ]
        view.set_trade_points(trades)
        result = view.get_trade_points()
        assert len(result) == 2
        assert result[0]["action"] == "매수"

    def test_initial_equity_data_empty(self, qapp):
        view = BacktestView()
        dates, values = view.get_equity_data()
        assert dates == []
        assert values == []

    def test_initial_trade_points_empty(self, qapp):
        view = BacktestView()
        result = view.get_trade_points()
        assert result == []
