"""T005/T008: SQLCipher DB 연결 매니저 + DB 초기화 테스트"""
import os
import tempfile
import pytest

from src.db.database import DatabaseManager, init_db


class TestDatabaseManager:
    """DatabaseManager 기본 연결 테스트"""

    def test_connect_and_close(self, tmp_path):
        """DB 연결/종료가 정상 동작해야 한다"""
        db_path = str(tmp_path / "test.db")
        mgr = DatabaseManager(db_path=db_path, password="testpass")
        mgr.connect()
        assert mgr.conn is not None
        mgr.close()
        assert mgr.conn is None

    def test_context_manager(self, tmp_path):
        """with 구문으로 사용 가능해야 한다"""
        db_path = str(tmp_path / "ctx.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            assert mgr.conn is not None
        assert mgr.conn is None

    def test_wal_mode_enabled(self, tmp_path):
        """WAL 저널 모드가 활성화되어야 한다"""
        db_path = str(tmp_path / "wal.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            cur = mgr.conn.execute("PRAGMA journal_mode")
            mode = cur.fetchone()[0]
            assert mode == "wal"

    def test_encryption_key_applied(self, tmp_path):
        """암호화 키가 적용되어야 한다 (잘못된 키로 열면 실패)"""
        db_path = str(tmp_path / "enc.db")
        with DatabaseManager(db_path=db_path, password="correct_pass") as mgr:
            mgr.conn.execute("CREATE TABLE t (id INTEGER)")
            mgr.conn.commit()

        # 잘못된 비밀번호로 열면 쿼리 실패
        import sqlcipher3
        conn2 = sqlcipher3.connect(db_path)
        conn2.execute(DatabaseManager._pragma_key_sql("wrong_pass"))
        raised = False
        try:
            conn2.execute("SELECT * FROM t")
        except Exception:
            raised = True
        finally:
            conn2.close()
        assert raised, "잘못된 키로 열었을 때 예외가 발생해야 한다"

    def test_execute_and_fetchall(self, tmp_path):
        """execute / fetchall 헬퍼가 동작해야 한다"""
        db_path = str(tmp_path / "exec.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
            mgr.execute("INSERT INTO items (name) VALUES (?)", ("apple",))
            mgr.execute("INSERT INTO items (name) VALUES (?)", ("banana",))
            rows = mgr.fetchall("SELECT name FROM items ORDER BY id")
            assert len(rows) == 2
            assert rows[0][0] == "apple"
            assert rows[1][0] == "banana"

    def test_db_dir_created_automatically(self, tmp_path):
        """DB 파일의 상위 디렉토리가 자동 생성되어야 한다"""
        db_path = str(tmp_path / "subdir" / "nested" / "test.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            assert os.path.isdir(str(tmp_path / "subdir" / "nested"))


class TestPragmaKeySql:
    """_pragma_key_sql: SQL 인젝션 방지 hex 인코딩 테스트"""

    def test_hex_encoding_format(self):
        """hex 인코딩 형식이 올바른 PRAGMA key SQL을 생성해야 한다"""
        sql = DatabaseManager._pragma_key_sql("testpass")
        expected_hex = "testpass".encode("utf-8").hex()
        assert sql == f"PRAGMA key=\"x'{expected_hex}'\""

    def test_special_chars_password(self, tmp_path):
        """작은따옴표/큰따옴표 등 특수문자가 포함된 비밀번호로 DB를 열 수 있어야 한다"""
        db_path = str(tmp_path / "special.db")
        password = "it's a \"test\" pass!@#$%"
        with DatabaseManager(db_path=db_path, password=password) as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER)")
            mgr.execute("INSERT INTO t VALUES (1)")
            rows = mgr.fetchall("SELECT id FROM t")
            assert rows[0][0] == 1

    def test_special_chars_reopen(self, tmp_path):
        """특수문자 비밀번호로 저장 후 다시 열어도 데이터가 유지되어야 한다"""
        db_path = str(tmp_path / "reopen.db")
        password = "p@ss'w\"ord;--"
        with DatabaseManager(db_path=db_path, password=password) as mgr:
            mgr.execute("CREATE TABLE t (val TEXT)")
            mgr.execute("INSERT INTO t VALUES (?)", ("hello",))
        with DatabaseManager(db_path=db_path, password=password) as mgr:
            rows = mgr.fetchall("SELECT val FROM t")
            assert rows[0][0] == "hello"

    def test_unicode_password(self, tmp_path):
        """한글 등 유니코드 비밀번호도 정상 동작해야 한다"""
        db_path = str(tmp_path / "unicode.db")
        password = "비밀번호123"
        with DatabaseManager(db_path=db_path, password=password) as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER)")
            mgr.execute("INSERT INTO t VALUES (42)")
            rows = mgr.fetchall("SELECT id FROM t")
            assert rows[0][0] == 42

    def test_empty_password(self, tmp_path):
        """빈 문자열 비밀번호도 hex 인코딩 가능해야 한다"""
        sql = DatabaseManager._pragma_key_sql("")
        assert sql == "PRAGMA key=\"x''\""


class TestInitDb:
    """init_db(): 17개 테이블 자동 생성 테스트"""

    def test_init_db_creates_all_tables(self, tmp_path):
        """init_db() 실행 후 17개 테이블이 모두 존재해야 한다"""
        db_path = str(tmp_path / "init.db")
        mgr = init_db(db_path=db_path, password="testpass")

        rows = mgr.fetchall(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        table_names = {r[0] for r in rows}

        expected_tables = {
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
        }
        missing = expected_tables - table_names
        assert not missing, f"누락된 테이블: {missing}"
        mgr.close()

    def test_init_db_idempotent(self, tmp_path):
        """init_db()를 두 번 호출해도 오류 없이 동작해야 한다"""
        db_path = str(tmp_path / "idem.db")
        mgr1 = init_db(db_path=db_path, password="testpass")
        mgr1.close()
        mgr2 = init_db(db_path=db_path, password="testpass")
        rows = mgr2.fetchall(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        assert len(rows) >= 17
        mgr2.close()

    def test_init_db_returns_manager(self, tmp_path):
        """init_db()는 DatabaseManager 인스턴스를 반환해야 한다"""
        from src.db.database import DatabaseManager
        db_path = str(tmp_path / "ret.db")
        mgr = init_db(db_path=db_path, password="testpass")
        assert isinstance(mgr, DatabaseManager)
        mgr.close()


class TestDatabaseBackupRestore:
    """T091: DB 백업/복원/무결성 검증 테스트"""

    def test_backup_creates_file(self, tmp_path):
        """backup()은 백업 파일을 생성해야 한다"""
        db_path = str(tmp_path / "src.db")
        backup_path = str(tmp_path / "backup.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER)")
            mgr.execute("INSERT INTO t VALUES (1)")
            result = mgr.backup(backup_path)
        assert result is True
        assert os.path.exists(backup_path)

    def test_backup_preserves_data(self, tmp_path):
        """backup() 후 백업 파일에 원본 데이터가 보존되어야 한다"""
        db_path = str(tmp_path / "src.db")
        backup_path = str(tmp_path / "backup.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER, name TEXT)")
            mgr.execute("INSERT INTO t VALUES (1, 'hello')")
            mgr.backup(backup_path)
        # 백업 파일을 열어 데이터 확인
        with DatabaseManager(db_path=backup_path, password="testpass") as mgr2:
            rows = mgr2.fetchall("SELECT name FROM t")
            assert rows[0][0] == "hello"

    def test_backup_returns_false_on_invalid_path(self, tmp_path):
        """존재하지 않는 디렉토리로 백업 시 False를 반환해야 한다"""
        db_path = str(tmp_path / "src.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER)")
            result = mgr.backup("/nonexistent/dir/backup.db")
        assert result is False

    def test_restore_recovers_data(self, tmp_path):
        """restore()로 백업에서 데이터를 복원할 수 있어야 한다"""
        db_path = str(tmp_path / "main.db")
        backup_path = str(tmp_path / "backup.db")
        # 원본 DB 생성 및 백업
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER, val TEXT)")
            mgr.execute("INSERT INTO t VALUES (1, 'original')")
            mgr.backup(backup_path)
        # 원본 DB 데이터 변경
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("DELETE FROM t")
            mgr.execute("INSERT INTO t VALUES (2, 'modified')")
        # 복원 (restore 내부에서 close -> copy -> reconnect)
        mgr2 = DatabaseManager(db_path=db_path, password="testpass")
        mgr2.connect()
        result = mgr2.restore(backup_path)
        assert result is True
        # restore 후 mgr2는 재연결 상태 - 복원 데이터 확인
        rows = mgr2.fetchall("SELECT val FROM t")
        assert rows[0][0] == "original"
        mgr2.close()

    def test_restore_returns_false_on_missing_backup(self, tmp_path):
        """존재하지 않는 백업 파일로 복원 시 False를 반환해야 한다"""
        db_path = str(tmp_path / "main.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            result = mgr.restore(str(tmp_path / "nonexistent.db"))
        assert result is False

    def test_verify_integrity_on_valid_db(self, tmp_path):
        """정상 DB에서 verify_integrity()는 True를 반환해야 한다"""
        db_path = str(tmp_path / "good.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            mgr.execute("CREATE TABLE t (id INTEGER)")
            assert mgr.verify_integrity() is True

    def test_verify_integrity_on_new_db(self, tmp_path):
        """빈 DB에서도 verify_integrity()는 True를 반환해야 한다"""
        db_path = str(tmp_path / "empty.db")
        with DatabaseManager(db_path=db_path, password="testpass") as mgr:
            assert mgr.verify_integrity() is True


class TestDatabaseCleanup:
    """T094: 데이터 보존 정책 - 오래된 데이터 삭제 테스트"""

    def _setup_db_with_tables(self, tmp_path):
        """테스트용 DB에 price_history, news, ai_scores 테이블 생성"""
        db_path = str(tmp_path / "cleanup.db")
        mgr = init_db(db_path=db_path, password="testpass")
        return mgr

    def test_cleanup_old_minute_data(self, tmp_path):
        """minute_bars_days 이전의 분봉 데이터가 삭제되어야 한다"""
        mgr = self._setup_db_with_tables(tmp_path)
        # 오래된 분봉 데이터 삽입 (91일 전)
        mgr.execute(
            "INSERT INTO price_history (stock_code, timeframe, date, open, high, low, close, volume) "
            "VALUES (?, ?, datetime('now', '-91 days'), 100, 110, 90, 105, 1000)",
            ("005930", "1m"),
        )
        # 최근 분봉 데이터 삽입
        mgr.execute(
            "INSERT INTO price_history (stock_code, timeframe, date, open, high, low, close, volume) "
            "VALUES (?, ?, datetime('now'), 100, 110, 90, 105, 1000)",
            ("005930", "1m"),
        )
        deleted = mgr.cleanup_old_data(minute_bars_days=90)
        rows = mgr.fetchall("SELECT * FROM price_history WHERE timeframe='1m'")
        assert len(rows) == 1  # 최근 데이터만 남아야 함
        assert deleted["price_history"] == 1
        mgr.close()

    def test_cleanup_old_news(self, tmp_path):
        """news_days 이전의 뉴스가 삭제되어야 한다"""
        mgr = self._setup_db_with_tables(tmp_path)
        # 오래된 뉴스 삽입 (181일 전)
        mgr.execute(
            "INSERT INTO news (source, title, url, crawled_at) "
            "VALUES (?, ?, ?, datetime('now', '-181 days'))",
            ("test", "old news", "http://old.com"),
        )
        # 최근 뉴스 삽입
        mgr.execute(
            "INSERT INTO news (source, title, url, crawled_at) "
            "VALUES (?, ?, ?, datetime('now'))",
            ("test", "new news", "http://new.com"),
        )
        deleted = mgr.cleanup_old_data(news_days=180)
        rows = mgr.fetchall("SELECT * FROM news")
        assert len(rows) == 1
        assert deleted["news"] == 1
        mgr.close()

    def test_cleanup_old_ai_scores(self, tmp_path):
        """ai_analysis_days 이전의 AI 분석이 삭제되어야 한다"""
        mgr = self._setup_db_with_tables(tmp_path)
        # 오래된 AI 분석 삽입 (366일 전)
        mgr.execute(
            "INSERT INTO ai_scores (stock_code, date, created_at) "
            "VALUES (?, ?, datetime('now', '-366 days'))",
            ("005930", "2024-01-01"),
        )
        # 최근 AI 분석 삽입
        mgr.execute(
            "INSERT INTO ai_scores (stock_code, date, created_at) "
            "VALUES (?, ?, datetime('now'))",
            ("005930", "2025-12-01"),
        )
        deleted = mgr.cleanup_old_data(ai_analysis_days=365)
        rows = mgr.fetchall("SELECT * FROM ai_scores")
        assert len(rows) == 1
        assert deleted["ai_scores"] == 1
        mgr.close()

    def test_cleanup_preserves_daily_price(self, tmp_path):
        """cleanup은 일봉(D) 데이터는 삭제하지 않아야 한다"""
        mgr = self._setup_db_with_tables(tmp_path)
        # 오래된 일봉 데이터 (분봉이 아닌 D 타임프레임)
        mgr.execute(
            "INSERT INTO price_history (stock_code, timeframe, date, open, high, low, close, volume) "
            "VALUES (?, ?, datetime('now', '-91 days'), 100, 110, 90, 105, 1000)",
            ("005930", "D"),
        )
        mgr.cleanup_old_data(minute_bars_days=90)
        rows = mgr.fetchall("SELECT * FROM price_history WHERE timeframe='D'")
        assert len(rows) == 1  # 일봉은 보존
        mgr.close()

    def test_cleanup_no_data_returns_zeros(self, tmp_path):
        """삭제할 데이터가 없으면 0을 반환해야 한다"""
        mgr = self._setup_db_with_tables(tmp_path)
        deleted = mgr.cleanup_old_data()
        assert deleted["price_history"] == 0
        assert deleted["news"] == 0
        assert deleted["ai_scores"] == 0
        mgr.close()
