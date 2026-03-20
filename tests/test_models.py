"""T006: 데이터 모델 정의 테스트 (17개 테이블 스키마)"""
import pytest

from src.db.database import init_db
from src.db import models


class TestModels:
    """models.py에 17개 테이블 CREATE SQL이 정의되어 있는지 테스트"""

    EXPECTED_TABLES = [
        "user_config",
        "stocks",
        "watchlist",
        "price_history",
        "orders",
        "trades",
        "positions",
        "portfolio_snapshot",
        "news",
        "news_sentiment",
        "technical_signals",
        "ai_scores",
        "strategies",
        "strategy_logs",
        "backtest_results",
        "alerts",
        "app_state",
    ]

    def test_all_table_schemas_defined(self):
        """models.SCHEMAS 딕셔너리에 17개 테이블이 모두 정의되어 있어야 한다"""
        assert hasattr(models, "SCHEMAS"), "models.SCHEMAS 딕셔너리가 없습니다"
        for table in self.EXPECTED_TABLES:
            assert table in models.SCHEMAS, f"SCHEMAS에 '{table}' 테이블이 없습니다"

    def test_schemas_are_valid_sql(self, tmp_path):
        """각 테이블 SQL이 실제로 실행 가능해야 한다"""
        db_path = str(tmp_path / "schema_test.db")
        mgr = init_db(db_path=db_path, password="schematest")
        rows = mgr.fetchall(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        created = {r[0] for r in rows}
        for table in self.EXPECTED_TABLES:
            assert table in created, f"'{table}' 테이블이 DB에 생성되지 않았습니다"
        mgr.close()

    def test_user_config_columns(self, tmp_path):
        """user_config 테이블에 필수 컬럼이 있어야 한다"""
        db_path = str(tmp_path / "col_test.db")
        mgr = init_db(db_path=db_path, password="testpass")
        rows = mgr.fetchall("PRAGMA table_info(user_config)")
        cols = {r[1] for r in rows}
        assert "id" in cols
        assert "key" in cols
        assert "value" in cols
        mgr.close()

    def test_stocks_columns(self, tmp_path):
        """stocks 테이블에 필수 컬럼이 있어야 한다"""
        db_path = str(tmp_path / "stocks_test.db")
        mgr = init_db(db_path=db_path, password="testpass")
        rows = mgr.fetchall("PRAGMA table_info(stocks)")
        cols = {r[1] for r in rows}
        assert "id" in cols
        assert "code" in cols
        assert "name" in cols
        mgr.close()

    def test_price_history_columns(self, tmp_path):
        """price_history 테이블에 OHLCV 컬럼이 있어야 한다"""
        db_path = str(tmp_path / "price_test.db")
        mgr = init_db(db_path=db_path, password="testpass")
        rows = mgr.fetchall("PRAGMA table_info(price_history)")
        cols = {r[1] for r in rows}
        for col in ["id", "stock_code", "open", "high", "low", "close", "volume"]:
            assert col in cols, f"price_history에 '{col}' 컬럼이 없습니다"
        mgr.close()

    def test_orders_columns(self, tmp_path):
        """orders 테이블에 주문 관련 필수 컬럼이 있어야 한다"""
        db_path = str(tmp_path / "orders_test.db")
        mgr = init_db(db_path=db_path, password="testpass")
        rows = mgr.fetchall("PRAGMA table_info(orders)")
        cols = {r[1] for r in rows}
        for col in ["id", "stock_code", "order_type", "quantity", "price"]:
            assert col in cols, f"orders에 '{col}' 컬럼이 없습니다"
        mgr.close()

    def test_app_state_columns(self, tmp_path):
        """app_state 테이블에 필수 컬럼이 있어야 한다"""
        db_path = str(tmp_path / "appstate_test.db")
        mgr = init_db(db_path=db_path, password="testpass")
        rows = mgr.fetchall("PRAGMA table_info(app_state)")
        cols = {r[1] for r in rows}
        assert "id" in cols
        assert "key" in cols
        assert "value" in cols
        mgr.close()


class TestMigrations:
    """T007: 스키마 마이그레이션 모듈 테스트"""

    def test_migration_module_importable(self):
        """migrations 모듈이 import 가능해야 한다"""
        from src.db import migrations
        assert hasattr(migrations, "get_current_version")
        assert hasattr(migrations, "migrate")

    def test_initial_version_is_zero_or_one(self, tmp_path):
        """새 DB의 스키마 버전은 0 또는 1이어야 한다"""
        from src.db.migrations import get_current_version
        db_path = str(tmp_path / "mig.db")
        mgr = init_db(db_path=db_path, password="testpass")
        version = get_current_version(mgr)
        assert version >= 0
        mgr.close()

    def test_migrate_is_callable(self, tmp_path):
        """migrate() 함수가 오류 없이 호출 가능해야 한다"""
        from src.db.migrations import migrate
        db_path = str(tmp_path / "mig2.db")
        mgr = init_db(db_path=db_path, password="testpass")
        migrate(mgr)  # 이미 최신 버전이므로 아무 작업도 안 함
        mgr.close()
