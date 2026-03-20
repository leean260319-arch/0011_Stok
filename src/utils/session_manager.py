"""T015/T093: 세션 영속성 매니저 - 창 위치/크기, 열린 탭, 마지막 종목 등 DB 저장/복원"""

# 버전 정보
# v1.0 - 2026-03-16: 신규 작성
# v1.1 - 2026-03-17: T093 자동 저장 기능 추가

import json
import threading

from src.db.database import DatabaseManager
from src.utils.logger import get_logger

logger = get_logger("utils.session_manager")

_CREATE_SESSION_TABLE = """
    CREATE TABLE IF NOT EXISTS app_session (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        data       TEXT NOT NULL,
        saved_at   TEXT DEFAULT (datetime('now', 'localtime'))
    )
"""


class SessionManager:
    """세션 데이터를 DB에 저장하고 복원하는 클래스.

    저장 항목: window_geometry, open_tabs, last_stock_code,
               panel_sizes, splitter_state
    """

    def __init__(self, db_path: str, password: str) -> None:
        self._db_path = db_path
        self._password = password
        self._auto_save_timer: threading.Timer | None = None
        self._auto_save_data: dict = {}
        self._ensure_table()

    def _ensure_table(self) -> None:
        """app_session 테이블이 없으면 생성한다."""
        with DatabaseManager(db_path=self._db_path, password=self._password) as mgr:
            mgr.conn.execute(_CREATE_SESSION_TABLE)
            mgr.conn.commit()

    def save_session(self, data: dict) -> None:
        """세션 데이터를 JSON 직렬화 후 DB에 저장한다. 기존 레코드는 삭제 후 재삽입."""
        serialized = json.dumps(data, ensure_ascii=False)
        with DatabaseManager(db_path=self._db_path, password=self._password) as mgr:
            mgr.conn.execute("DELETE FROM app_session")
            mgr.conn.execute(
                "INSERT INTO app_session (data) VALUES (?)", (serialized,)
            )
            mgr.conn.commit()
        logger.debug("세션 저장 완료")

    def load_session(self) -> dict:
        """마지막으로 저장된 세션 데이터를 반환한다. 없으면 빈 딕셔너리 반환."""
        with DatabaseManager(db_path=self._db_path, password=self._password) as mgr:
            row = mgr.fetchone(
                "SELECT data FROM app_session ORDER BY id DESC LIMIT 1"
            )
        if row is None:
            return {}
        return json.loads(row[0])

    # ------------------------------------------------------------------
    # T093: 자동 저장
    # ------------------------------------------------------------------

    def start_auto_save(self, interval_sec: float = 300) -> None:
        """주기적 자동 저장을 시작한다.

        Args:
            interval_sec: 저장 주기 (초). 기본 300초(5분).
        """
        self._auto_save_interval = interval_sec
        self._schedule_auto_save()
        logger.info("자동 저장 시작: %s초 간격", interval_sec)

    def stop_auto_save(self) -> None:
        """자동 저장을 중단한다."""
        if self._auto_save_timer is not None:
            self._auto_save_timer.cancel()
            self._auto_save_timer = None
        logger.info("자동 저장 중단")

    def _schedule_auto_save(self) -> None:
        """다음 자동 저장 타이머를 예약한다."""
        self._auto_save_timer = threading.Timer(
            self._auto_save_interval, self._run_auto_save
        )
        self._auto_save_timer.daemon = True
        self._auto_save_timer.start()

    def _run_auto_save(self) -> None:
        """자동 저장 실행 후 다음 타이머를 재예약한다."""
        data = self._auto_save_data if self._auto_save_data else self.load_session()
        self.save_session(data)
        logger.debug("자동 저장 실행 완료")
        self._schedule_auto_save()
