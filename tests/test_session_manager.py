"""T015/T093: SessionManager 테스트"""
import time
from unittest.mock import patch, MagicMock

import pytest

from src.utils.session_manager import SessionManager


class TestSessionManager:
    """SessionManager 기본 동작 테스트"""

    def test_save_and_load_session(self, tmp_path):
        """세션 저장 후 로드하면 동일 데이터 반환"""
        db_path = str(tmp_path / "session.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        data = {
            "window_geometry": {"x": 100, "y": 100, "width": 1280, "height": 800},
            "open_tabs": ["005930", "000660"],
            "last_stock_code": "005930",
            "panel_sizes": [250, 700, 300],
            "splitter_state": "default",
        }
        mgr.save_session(data)
        result = mgr.load_session()
        assert result["last_stock_code"] == "005930"
        assert result["open_tabs"] == ["005930", "000660"]
        assert result["panel_sizes"] == [250, 700, 300]

    def test_load_session_empty_returns_empty_dict(self, tmp_path):
        """세션이 없을 때 빈 딕셔너리 반환"""
        db_path = str(tmp_path / "empty.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        result = mgr.load_session()
        assert result == {}

    def test_save_session_overwrites(self, tmp_path):
        """save_session() 재호출 시 이전 데이터를 덮어써야 한다"""
        db_path = str(tmp_path / "overwrite.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        mgr.save_session({"last_stock_code": "005930"})
        mgr.save_session({"last_stock_code": "000660"})
        result = mgr.load_session()
        assert result["last_stock_code"] == "000660"

    def test_session_stores_window_geometry(self, tmp_path):
        """window_geometry 저장/복원"""
        db_path = str(tmp_path / "geo.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        geo = {"x": 50, "y": 50, "width": 1920, "height": 1080}
        mgr.save_session({"window_geometry": geo})
        result = mgr.load_session()
        assert result["window_geometry"] == geo

    def test_session_stores_splitter_state(self, tmp_path):
        """splitter_state 저장/복원"""
        db_path = str(tmp_path / "split.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        mgr.save_session({"splitter_state": "encoded_bytes_here"})
        result = mgr.load_session()
        assert result["splitter_state"] == "encoded_bytes_here"


class TestSessionAutoSave:
    """T093: 자동 저장 기능 테스트"""

    def test_start_auto_save_calls_save(self, tmp_path):
        """start_auto_save() 시작 후 save_session이 호출되어야 한다"""
        db_path = str(tmp_path / "auto.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        mgr.save_session({"test": "data"})
        # 짧은 간격으로 자동 저장 시작
        mgr.start_auto_save(interval_sec=0.1)
        time.sleep(0.3)
        mgr.stop_auto_save()
        # 자동 저장이 동작했으므로 세션 데이터가 유지됨
        result = mgr.load_session()
        assert result == {"test": "data"}

    def test_stop_auto_save(self, tmp_path):
        """stop_auto_save() 호출 후 자동 저장이 중단되어야 한다"""
        db_path = str(tmp_path / "stop.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        mgr.start_auto_save(interval_sec=0.1)
        mgr.stop_auto_save()
        assert mgr._auto_save_timer is None

    def test_stop_auto_save_without_start(self, tmp_path):
        """start 없이 stop 호출해도 오류가 없어야 한다"""
        db_path = str(tmp_path / "nostop.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        mgr.stop_auto_save()  # 예외 없이 통과해야 함

    def test_auto_save_repeats(self, tmp_path):
        """자동 저장이 반복 실행되어야 한다"""
        db_path = str(tmp_path / "repeat.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        call_count = []
        original_save = mgr.save_session

        def counting_save(data):
            call_count.append(1)
            original_save(data)

        mgr.save_session = counting_save
        mgr._auto_save_data = {"count": "test"}
        mgr.start_auto_save(interval_sec=0.1)
        time.sleep(0.5)
        mgr.stop_auto_save()
        # 0.1초 간격으로 0.5초 동안 -> 최소 2회 이상 호출
        assert len(call_count) >= 2

    def test_start_auto_save_with_custom_interval(self, tmp_path):
        """사용자 지정 간격으로 자동 저장이 동작해야 한다"""
        db_path = str(tmp_path / "custom.db")
        mgr = SessionManager(db_path=db_path, password="testpass")
        mgr.save_session({"interval": "custom"})
        mgr.start_auto_save(interval_sec=600)
        assert mgr._auto_save_timer is not None
        mgr.stop_auto_save()
