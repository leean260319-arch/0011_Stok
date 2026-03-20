"""T077-T079 포트폴리오 뷰 테스트
버전: v1.0
"""
import pytest
from datetime import date

from src.ui.portfolio_view import PortfolioView, AllocationChart, ReturnChart


class TestPortfolioView:
    """T077 PortfolioView 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = PortfolioView()
        assert w is not None

    def test_columns(self, qapp):
        """6개 컬럼 확인."""
        w = PortfolioView()
        assert w._table.columnCount() == 6

    def test_add_stock(self, qapp):
        """종목 추가."""
        w = PortfolioView()
        w.add_stock("삼성전자", 10, 70000, 72000)
        assert w._table.rowCount() == 1
        assert w.get_stock_count() == 1

    def test_add_multiple_stocks(self, qapp):
        """여러 종목 추가."""
        w = PortfolioView()
        w.add_stock("삼성전자", 10, 70000, 72000)
        w.add_stock("SK하이닉스", 5, 150000, 145000)
        assert w.get_stock_count() == 2

    def test_stock_data_display(self, qapp):
        """종목 데이터 표시 확인."""
        w = PortfolioView()
        w.add_stock("삼성전자", 10, 70000, 72000)
        assert w._table.item(0, 0).text() == "삼성전자"
        assert w._table.item(0, 1).text() == "10"

    def test_profit_rate_calculation(self, qapp):
        """수익률 계산."""
        w = PortfolioView()
        w.add_stock("삼성전자", 10, 70000, 72000)
        rate_text = w._table.item(0, 4).text()
        # (72000 - 70000) / 70000 * 100 = 2.86%
        assert "2.86" in rate_text

    def test_eval_amount_calculation(self, qapp):
        """평가금액 계산."""
        w = PortfolioView()
        w.add_stock("삼성전자", 10, 70000, 72000)
        eval_text = w._table.item(0, 5).text()
        assert "720,000" in eval_text


class TestAllocationChart:
    """T078 AllocationChart 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = AllocationChart()
        assert w is not None

    def test_set_data(self, qapp):
        """비중 데이터 설정."""
        w = AllocationChart()
        data = [
            {"name": "삼성전자", "ratio": 40.0},
            {"name": "SK하이닉스", "ratio": 30.0},
            {"name": "현금", "ratio": 30.0},
        ]
        w.set_data(data)
        result = w.get_data()
        assert len(result) == 3
        assert result[0]["name"] == "삼성전자"

    def test_get_data_empty(self, qapp):
        """빈 데이터."""
        w = AllocationChart()
        assert w.get_data() == []


class TestReturnChart:
    """T079 ReturnChart 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = ReturnChart()
        assert w is not None

    def test_add_point(self, qapp):
        """수익률 데이터 포인트 추가."""
        w = ReturnChart()
        w.add_point("2026-01-01", 1.5)
        data = w.get_data()
        assert len(data) == 1
        assert data[0]["date"] == "2026-01-01"
        assert data[0]["cumulative_return"] == 1.5

    def test_add_multiple_points(self, qapp):
        """여러 포인트 추가."""
        w = ReturnChart()
        w.add_point("2026-01-01", 1.5)
        w.add_point("2026-01-02", 2.3)
        w.add_point("2026-01-03", -0.5)
        assert len(w.get_data()) == 3

    def test_get_data_empty(self, qapp):
        """빈 데이터."""
        w = ReturnChart()
        assert w.get_data() == []
