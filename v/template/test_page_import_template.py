"""
test_page_import_template.py - Streamlit 페이지 import 테스트 템플릿

런타임 에러 감지:
- StreamlitDuplicateElementKey
- ImportError
- SyntaxError (동적)
- 기타 모듈 로드 시 발생하는 에러

사용법:
1. 이 템플릿을 tests/test_page_import.py로 복사
2. PAGES_DIR 경로를 프로젝트에 맞게 수정
3. mock_oais_modules에서 프로젝트 특화 모킹 추가
"""
import pytest
import importlib.util
import sys
from pathlib import Path


# ============================================================
# [수정 필요] 페이지 디렉토리 경로 설정
# ============================================================
PAGES_DIR = Path(__file__).parent.parent / "02_1st_server" / "pages"


def get_page_files():
    """페이지 파일 목록 반환"""
    if not PAGES_DIR.exists():
        return []
    return sorted(PAGES_DIR.glob("*.py"))


# ============================================================
# Streamlit 모킹 클래스
# ============================================================
class MockSessionState(dict):
    """st.session_state를 모킹 - dict처럼 동작하면서 속성 접근도 지원"""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)


class MockContextManager:
    """with 문에서 사용할 수 있는 컨텍스트 매니저 모킹"""
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def __call__(self, *args, **kwargs):
        return self


# ============================================================
# DB 모킹 Fixture
# ============================================================
@pytest.fixture(autouse=True)
def mock_oais_modules(monkeypatch):
    """oais 모듈 모킹 - DB 연결 없이 테스트"""
    import unittest.mock as mock

    # oais.db 모킹 - DB 연결 방지
    mock_db = mock.MagicMock()
    mock_db.get_connection = mock.MagicMock(return_value=mock.MagicMock())
    mock_db.execute_query = mock.MagicMock(return_value=[])
    mock_db.fetch_all = mock.MagicMock(return_value=[])
    mock_db.fetch_one = mock.MagicMock(return_value=None)

    # oais.auth 모킹
    mock_auth = mock.MagicMock()
    mock_auth.check_login_status = mock.MagicMock(return_value=True)
    mock_auth.get_current_user = mock.MagicMock(return_value={"id": "test", "name": "Test User"})
    mock_auth.is_admin = mock.MagicMock(return_value=True)

    # oais.config_helper 모킹
    mock_config = mock.MagicMock()
    mock_config.Config = mock.MagicMock()
    mock_config.Config.DB_PATH = ":memory:"

    # sqlite3 모킹 - 실제 DB 연결 방지
    mock_sqlite_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_cursor.fetchall = mock.MagicMock(return_value=[])
    mock_cursor.fetchone = mock.MagicMock(return_value=(0,))
    mock_cursor.execute = mock.MagicMock()
    mock_cursor.description = [("col1",)]
    mock_cursor.rowcount = 0
    mock_sqlite_conn.cursor = mock.MagicMock(return_value=mock_cursor)
    mock_sqlite_conn.commit = mock.MagicMock()
    mock_sqlite_conn.execute = mock.MagicMock(return_value=mock_cursor)
    mock_sqlite_conn.row_factory = None

    original_connect = None
    try:
        import sqlite3 as real_sqlite3
        original_connect = real_sqlite3.connect

        def mock_connect(*args, **kwargs):
            if args and (args[0] == ":memory:" or "test" in str(args[0]).lower()):
                return original_connect(*args, **kwargs)
            return mock_sqlite_conn

        monkeypatch.setattr("sqlite3.connect", mock_connect)
    except Exception:
        pass

    yield


# ============================================================
# Streamlit 모킹 Fixture
# ============================================================
@pytest.fixture(autouse=True)
def mock_streamlit(monkeypatch):
    """Streamlit 모킹 - 실제 UI 렌더링 없이 import만 테스트"""
    import unittest.mock as mock

    # key 중복 검사를 위한 key 저장소
    used_keys = set()

    # Streamlit 모듈 모킹
    mock_st = mock.MagicMock()
    mock_st.session_state = MockSessionState()
    mock_st.set_page_config = mock.MagicMock()
    mock_st.sidebar = mock.MagicMock()

    # columns - 요청된 수만큼 반환
    def mock_columns(spec, **kwargs):
        if isinstance(spec, int):
            return [MockContextManager() for _ in range(spec)]
        elif isinstance(spec, (list, tuple)):
            return [MockContextManager() for _ in range(len(spec))]
        return [MockContextManager(), MockContextManager()]

    mock_st.columns = mock_columns

    # tabs - 요청된 수만큼 반환
    def mock_tabs(labels, **kwargs):
        return [MockContextManager() for _ in range(len(labels))]

    mock_st.tabs = mock_tabs

    # ========== 위젯 key 중복 검사 함수들 ==========
    def check_key(*args, key=None, **kwargs):
        """위젯의 key 중복 검사"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        return mock.MagicMock()

    def check_key_return_value(*args, key=None, **kwargs):
        """값을 반환하는 위젯 - options의 첫 번째 값 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        options = kwargs.get("options", args[1] if len(args) > 1 else None)
        if options and len(options) > 0:
            return options[0]
        return ""

    def check_key_return_false(*args, key=None, **kwargs):
        """checkbox - False 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        return False

    def check_key_return_empty_string(*args, key=None, **kwargs):
        """text_input/text_area - 빈 문자열 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        return ""

    def check_key_return_list(*args, key=None, **kwargs):
        """multiselect - 빈 리스트 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        return []

    def check_key_slider(*args, key=None, value=None, **kwargs):
        """slider - 단일값 또는 범위(튜플) 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        if value is not None and isinstance(value, (list, tuple)):
            return tuple(value)
        min_val = kwargs.get("min_value", 0)
        if value is not None:
            return value
        return min_val

    def check_key_number_input(*args, key=None, value=None, **kwargs):
        """number_input - 기본값 또는 0 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        if value is not None:
            return value
        return kwargs.get("min_value", 0)

    def check_key_select_slider(*args, key=None, value=None, options=None, **kwargs):
        """select_slider - 범위 반환"""
        if key is not None:
            if key in used_keys:
                raise ValueError(f"Duplicate key detected: {key}")
            used_keys.add(key)
        if value is not None:
            if isinstance(value, (list, tuple)):
                return tuple(value)
            return value
        if options and len(options) >= 2:
            return (options[0], options[-1])
        return (0, 100)

    # key를 사용하는 위젯들에 중복 검사 적용
    mock_st.button = check_key
    mock_st.text_input = check_key_return_empty_string
    mock_st.text_area = check_key_return_empty_string
    mock_st.selectbox = check_key_return_value
    mock_st.multiselect = check_key_return_list
    mock_st.checkbox = check_key_return_false
    mock_st.radio = check_key_return_value
    mock_st.slider = check_key_slider
    mock_st.select_slider = check_key_select_slider
    mock_st.number_input = check_key_number_input
    mock_st.date_input = check_key
    mock_st.time_input = check_key
    mock_st.file_uploader = check_key
    mock_st.data_editor = check_key
    mock_st.form = lambda key=None, **kwargs: MockContextManager()
    mock_st.form_submit_button = check_key

    # expander - 컨텍스트 매니저로 동작
    def mock_expander(label, expanded=False, **kwargs):
        return MockContextManager()

    mock_st.expander = mock_expander

    # container, empty - 컨텍스트 매니저
    mock_st.container = lambda **kwargs: MockContextManager()
    mock_st.empty = lambda: mock.MagicMock()

    # spinner - 컨텍스트 매니저
    mock_st.spinner = lambda text="": MockContextManager()

    # cache 데코레이터
    mock_st.cache_data = lambda *args, **kwargs: lambda f: f
    mock_st.cache_resource = lambda *args, **kwargs: lambda f: f
    mock_st.cache = lambda *args, **kwargs: lambda f: f

    # experimental 함수들
    mock_st.experimental_rerun = mock.MagicMock()

    # query_params
    mock_st.query_params = mock.MagicMock()

    monkeypatch.setitem(sys.modules, "streamlit", mock_st)

    yield mock_st

    # 테스트 후 key 저장소 초기화
    used_keys.clear()


# ============================================================
# 테스트 케이스
# ============================================================
@pytest.mark.parametrize("page_file", get_page_files(), ids=lambda x: x.name)
def test_page_import(page_file):
    """각 페이지 파일이 import 가능한지 테스트"""
    module_name = f"page_{page_file.stem}"

    spec = importlib.util.spec_from_file_location(module_name, page_file)
    assert spec is not None, f"Cannot create spec for {page_file}"

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        # 이 시점에서 런타임 에러 발생 가능
        # - DuplicateKey
        # - ImportError
        # - 기타 초기화 에러
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"Failed to import {page_file.name}: {type(e).__name__}: {e}")
    finally:
        # 모듈 정리
        if module_name in sys.modules:
            del sys.modules[module_name]


def test_pages_directory_exists():
    """pages 디렉토리 존재 확인"""
    assert PAGES_DIR.exists(), f"Pages directory not found: {PAGES_DIR}"


def test_pages_count():
    """최소 페이지 수 확인"""
    pages = get_page_files()
    # [수정 필요] 프로젝트에 맞게 최소 페이지 수 조정
    assert len(pages) >= 1, f"Expected at least 1 page, found {len(pages)}"
