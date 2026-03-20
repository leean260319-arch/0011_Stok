#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
oais_usage_validator.py - oais 모듈 사용 검증 스크립트

목적: 코드베이스에서 oais 모듈의 잘못된 사용을 감지
- oais.function_name() 형태의 직접 호출 감지 (submodule 거치지 않음)
- 존재하지 않는 oais 속성 접근 감지

사용법:
    # 모듈로 import하여 사용
    from oais_usage_validator import get_oais_errors, OaisUsageError
    errors = get_oais_errors()
"""

import ast
import sys
from pathlib import Path
from dataclasses import dataclass


@dataclass
class OaisUsageError:
    """oais 사용 오류 정보"""
    file_path: str
    line_no: int
    col_offset: int
    attr_name: str
    code_snippet: str
    error_type: str  # 'direct_function_call', 'unknown_attribute'
    suggestion: str = ""


# oais 패키지에서 직접 export되는 항목들
OAIS_DIRECT_EXPORTS = {
    # 설정
    "config", "Config",
    # 함수 exports
    "authenticate_user",
    "get_user_companies",
    "get_posts",
    # DB helpers (backwards-compatible)
    "get_db_connection",
    "exec_cud_query",
    "exec_r_query",
    "table2df",
    "_validate_table_name",
    "_validate_column_name",
    "_sanitize_uid",
}

# oais 서브모듈 목록
OAIS_SUBMODULES = {
    "admin", "agent", "application", "auth", "bizreg", "bizreg_data",
    "book_summary", "card_processor", "chuck_task", "columns", "community",
    "company", "config_helper", "customer", "data_processing", "date_utils",
    "db", "db_meta", "excel_utils", "file_manager", "file_ops", "file_upload",
    "financial", "hyphen_api", "ocr", "pdf_parser", "receipt_parser", "seal",
    "services", "session", "sys_code", "task_attachment", "task_core",
    "task_mgmt", "task_query", "ui", "user", "utils", "validation",
}

# 서브모듈별 주요 함수 매핑 (자동 수정 제안용)
SUBMODULE_FUNCTIONS = {
    "date_utils": {
        "get_date_range", "get_current_date", "get_current_datetime",
        "format_date", "parse_date", "date_to_str", "str_to_date",
        "get_week_range", "get_month_range", "get_year_range",
        "format_datetime",
    },
    "db": {
        "get_db_connection", "exec_cud_query", "exec_r_query", "table2df",
    },
    "utils": {
        "format_number", "parse_number", "clean_string", "truncate_string",
    },
    "ui": {
        "show_error", "show_success", "show_warning", "show_info",
        "create_button", "create_form", "format_company_teams",
    },
    "validation": {
        "validate_email", "validate_phone", "validate_bizno",
    },
    "auth": {
        "authenticate_user", "check_permission", "get_user_role",
    },
    "file_manager": {
        "upload_file", "download_file", "delete_file", "list_files",
        "create_excel_download",
    },
    "data_processing": {
        "match_dataframes_by_columns", "normalize_value",
        "auto_detect_column_mappings",
    },
    "card_processor": {
        "detect_card_column", "is_masked_card", "process_card_data",
        "create_card_excel_output",
    },
    "excel_utils": {
        "generate_coupang_excel",
    },
    "financial": {
        "cms_account_main",
    },
    "bizreg": {
        "search_bubin", "search_result_to_df",
    },
}


class OaisUsageVisitor(ast.NodeVisitor):
    """AST Visitor to find oais module usage patterns"""

    def __init__(self, file_path: str, source_lines: list):
        self.file_path = file_path
        self.source_lines = source_lines
        self.errors: list[OaisUsageError] = []
        self.oais_aliases = {"oais"}  # import oais as xxx 추적

    def visit_Import(self, node: ast.Import):
        """import 문 분석"""
        for alias in node.names:
            if alias.name == "oais":
                if alias.asname:
                    self.oais_aliases.add(alias.asname)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """from import 문 분석"""
        # from oais import xxx 는 괜찮음
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        """속성 접근 분석 (oais.xxx)"""
        # oais.xxx 패턴 찾기
        if isinstance(node.value, ast.Name) and node.value.id in self.oais_aliases:
            attr_name = node.attr

            # 서브모듈 접근은 OK
            if attr_name in OAIS_SUBMODULES:
                pass  # oais.db, oais.utils 등은 정상
            # 직접 export된 항목은 OK
            elif attr_name in OAIS_DIRECT_EXPORTS:
                pass  # oais.config, oais.authenticate_user 등은 정상
            else:
                # 잘못된 접근 감지
                code_snippet = self._get_code_snippet(node.lineno)
                suggestion = self._suggest_fix(attr_name)

                self.errors.append(OaisUsageError(
                    file_path=self.file_path,
                    line_no=node.lineno,
                    col_offset=node.col_offset,
                    attr_name=attr_name,
                    code_snippet=code_snippet,
                    error_type="unknown_attribute",
                    suggestion=suggestion,
                ))

        self.generic_visit(node)

    def _get_code_snippet(self, lineno: int) -> str:
        """해당 라인의 코드 스니펫 반환"""
        if 0 < lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def _suggest_fix(self, attr_name: str) -> str:
        """수정 제안 생성"""
        for submodule, functions in SUBMODULE_FUNCTIONS.items():
            if attr_name in functions:
                return f"oais.{submodule}.{attr_name}"
        return ""


def validate_file(file_path: Path) -> list[OaisUsageError]:
    """단일 파일 검증"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
            source_lines = source.splitlines()

        tree = ast.parse(source, filename=str(file_path))
        visitor = OaisUsageVisitor(str(file_path), source_lines)
        visitor.visit(tree)
        return visitor.errors

    except SyntaxError as e:
        print(f"  [SKIP] 문법 오류: {file_path}: {e}")
        return []
    except Exception as e:
        print(f"  [SKIP] 파일 읽기 오류: {file_path}: {e}")
        return []


def find_python_files(root_dir: Path, exclude_dirs: set = None) -> list[Path]:
    """Python 파일 목록 반환"""
    if exclude_dirs is None:
        exclude_dirs = {"__pycache__", "venv", "node_modules", "tmp"}

    python_files = []
    for path in root_dir.rglob("*.py"):
        # .으로 시작하는 폴더 제외 (.git, .venv, .yoyo 등)
        if any(part.startswith(".") for part in path.parts):
            continue
        if any(excluded in path.parts for excluded in exclude_dirs):
            continue
        python_files.append(path)
    return python_files


def get_oais_errors(project_root: Path = None, server_only: bool = False) -> dict:
    """
    oais 모듈 사용 오류 검사 및 결과 반환

    Args:
        project_root: 프로젝트 루트 경로 (None이면 자동 탐지)
        server_only: True면 02_1st_server만 검사

    Returns:
        dict: {
            "total_files": int,
            "total_errors": int,
            "errors_by_file": {file_path: [OaisUsageError, ...]},
            "server_errors": {file_path: [OaisUsageError, ...]},
        }
    """
    if project_root is None:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent

    # oais 패키지 자체는 제외, 그리고 old/data 폴더 제외
    exclude_dirs = {"__pycache__", "venv", "node_modules", "tmp", "oais", "00_old", "data"}

    # Python 파일 검색
    python_files = find_python_files(project_root, exclude_dirs)

    all_errors: list[OaisUsageError] = []

    for py_file in python_files:
        errors = validate_file(py_file)
        if errors:
            all_errors.extend(errors)

    # 파일별로 그룹화
    errors_by_file = {}
    for error in all_errors:
        if error.file_path not in errors_by_file:
            errors_by_file[error.file_path] = []
        errors_by_file[error.file_path].append(error)

    # 02_1st_server만 필터 (실제 운영 코드)
    server_errors = {k: v for k, v in errors_by_file.items() if "02_1st_server" in k}

    return {
        "project_root": project_root,
        "total_files": len(python_files),
        "total_errors": len(all_errors),
        "errors_by_file": errors_by_file,
        "server_errors": server_errors,
    }


def main():
    """CLI 실행 (독립 실행용)"""
    result = get_oais_errors()

    print(f"검사 대상: {result['total_files']}개 파일")
    print(f"총 오류: {result['total_errors']}개")
    print(f"운영 코드 오류 파일: {len(result['server_errors'])}개")

    if result['total_errors'] > 0:
        print("\n운영 코드 오류 상세:")
        for file_path, errors in sorted(result['server_errors'].items()):
            rel_path = Path(file_path).relative_to(result['project_root'])
            print(f"\n  {rel_path}:")
            for err in errors:
                fix = f" -> {err.suggestion}" if err.suggestion else ""
                print(f"    L{err.line_no}: oais.{err.attr_name}{fix}")

    return 1 if result['total_errors'] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
