"""T080-T081 관심 종목 뷰 테스트
버전: v1.0
"""
import pytest

from src.ui.watchlist_view import WatchlistView, RealtimeTable


class TestWatchlistView:
    """T080 WatchlistView 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = WatchlistView()
        assert w is not None

    def test_create_group(self, qapp):
        """그룹 생성."""
        w = WatchlistView()
        w.create_group("반도체")
        groups = w.get_groups()
        assert "반도체" in groups

    def test_delete_group(self, qapp):
        """그룹 삭제."""
        w = WatchlistView()
        w.create_group("반도체")
        w.delete_group("반도체")
        assert "반도체" not in w.get_groups()

    def test_add_stock_to_group(self, qapp):
        """그룹에 종목 추가."""
        w = WatchlistView()
        w.create_group("반도체")
        w.add_stock("반도체", "005930")
        groups = w.get_groups()
        assert "005930" in groups["반도체"]

    def test_remove_stock_from_group(self, qapp):
        """그룹에서 종목 제거."""
        w = WatchlistView()
        w.create_group("반도체")
        w.add_stock("반도체", "005930")
        w.remove_stock("반도체", "005930")
        assert "005930" not in w.get_groups()["반도체"]

    def test_multiple_groups(self, qapp):
        """여러 그룹 관리."""
        w = WatchlistView()
        w.create_group("반도체")
        w.create_group("자동차")
        w.add_stock("반도체", "005930")
        w.add_stock("자동차", "005380")
        groups = w.get_groups()
        assert len(groups) == 2
        assert "005930" in groups["반도체"]
        assert "005380" in groups["자동차"]

    def test_delete_nonexistent_group(self, qapp):
        """존재하지 않는 그룹 삭제 시 무시."""
        w = WatchlistView()
        w.delete_group("없는그룹")  # 에러 없이 통과

    def test_get_groups_empty(self, qapp):
        """빈 그룹."""
        w = WatchlistView()
        assert w.get_groups() == {}


class TestRealtimeTable:
    """T081 RealtimeTable 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = RealtimeTable()
        assert w is not None

    def test_columns(self, qapp):
        """5개 컬럼 (종목코드/현재가/등락률/거래량/AI점수)."""
        w = RealtimeTable()
        assert w._table.columnCount() == 5

    def test_update_stock_new(self, qapp):
        """새 종목 데이터 추가."""
        w = RealtimeTable()
        w.update_stock("005930", 72000, 1.5, 1_000_000, 85.0)
        assert w._table.rowCount() == 1

    def test_update_stock_existing(self, qapp):
        """기존 종목 데이터 갱신."""
        w = RealtimeTable()
        w.update_stock("005930", 72000, 1.5, 1_000_000, 85.0)
        w.update_stock("005930", 73000, 2.9, 1_200_000, 90.0)
        assert w._table.rowCount() == 1
        assert w._table.item(0, 1).text() == "73,000"

    def test_update_multiple_stocks(self, qapp):
        """여러 종목 데이터."""
        w = RealtimeTable()
        w.update_stock("005930", 72000, 1.5, 1_000_000, 85.0)
        w.update_stock("000660", 150000, -0.5, 500_000, 70.0)
        assert w._table.rowCount() == 2
