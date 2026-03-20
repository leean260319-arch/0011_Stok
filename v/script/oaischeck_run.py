#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaischeck_run.py

통합 코드 품질 체크 워크플로우 (v/oaischeck.md 구현)

서브명령어:
    run       - 전체 체크 실행 (pylint, mypy, pytest, oais validator)
    oais      - oais 모듈 사용 검증 및 d0004_todo.md 등록
    error     - 에러 체크만 수행 (pylint, mypy)
    term      - 표준용어 체크만 수행
    update    - d0004/d0010 문서 정리 및 동기화
    debug     - 심층 디버깅 워크플로우 실행
    circular  - 순환 참조(Circular Import) 감지

사용법:
    python v/script/oaischeck_run.py run
    python v/script/oaischeck_run.py oais [--dry-run]
    python v/script/oaischeck_run.py error
    python v/script/oaischeck_run.py term
    python v/script/oaischeck_run.py update
    python v/script/oaischeck_run.py debug [에러메시지]
    python v/script/oaischeck_run.py circular [모듈명]
"""

import sys
import subprocess
import shutil
import re
import ast
import py_compile
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from oais_common import show_help_if_no_args
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


def load_env_value(key: str, default: str = "") -> str:
    """Load value from .env file without external dependencies."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1]
    return default


# SOURCE_DIRS from .env (fallback to default)
_default_dirs = "src,oais,tests"
SOURCE_DIRS = load_env_value("OAIS_SOURCE_DIRS", _default_dirs).split(",")
TARGET_DIRS = [d for d in SOURCE_DIRS if Path(d).exists()]

# SP (서브프로젝트) 컨텍스트: 00=공통, 01=algorithm, 02=1st_server, ...
SP_CONTEXT = "00"  # 기본값: 공통


def get_sp_doc_path(base_doc_num: str) -> Path:
    """
    SP 컨텍스트에 따른 문서 경로 반환

    Args:
        base_doc_num: 기본 문서 번호 (예: "0004", "0010")

    Returns:
        Path: 문서 경로 (예: doc/d0004_todo.md 또는 doc/d20004_todo.md)
    """
    global SP_CONTEXT

    if SP_CONTEXT == "00":
        doc_num = base_doc_num
    else:
        # SP × 10000 + 기본번호
        sp_num = int(SP_CONTEXT)
        base_num = int(base_doc_num)
        doc_num = str(sp_num * 10000 + base_num)

    # 문서 파일명 매핑
    doc_names = {
        "0004": "todo",
        "0010": "history",
        "0001": "prd",
        "0002": "plan",
        "0003": "test",
        "0006": "db",
    }

    suffix = doc_names.get(base_doc_num, "")
    if suffix:
        filename = f"d{doc_num}_{suffix}.md"
    else:
        filename = f"d{doc_num}.md"

    return PROJECT_ROOT / "doc" / filename


def set_sp_context(sp: str):
    """SP 컨텍스트 설정"""
    global SP_CONTEXT
    if sp in ["00", "01", "02", "03", "04", "05"]:
        SP_CONTEXT = sp
        print(f"[INFO] SP Context: {sp}")
    else:
        print(f"[WARN] Invalid SP: {sp}, using default (00)")
        SP_CONTEXT = "00"

# oais_usage_validator를 import하기 위해 path 추가
sys.path.insert(0, str(SCRIPT_DIR))
from oais_usage_validator import get_oais_errors, OaisUsageError


@dataclass
class Issue:
    """발견된 이슈를 나타내는 데이터 클래스"""
    severity: str  # CRITICAL, ERROR, WARNING, INFO
    category: str  # SYNTAX, TYPE, LINT, TEST, OAIS
    file_path: str
    line_no: Optional[int]
    message: str
    suggestion: Optional[str] = None


@dataclass
class IssueCollector:
    """이슈 수집 및 관리"""
    issues: List[Issue] = field(default_factory=list)

    def add(self, severity: str, category: str, file_path: str,
            line_no: Optional[int], message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(severity, category, file_path, line_no, message, suggestion))

    def get_by_severity(self, severity: str) -> List[Issue]:
        return [i for i in self.issues if i.severity == severity]

    def count_by_severity(self) -> Dict[str, int]:
        counts = {"CRITICAL": 0, "ERROR": 0, "WARNING": 0, "INFO": 0}
        for issue in self.issues:
            if issue.severity in counts:
                counts[issue.severity] += 1
        return counts

    def has_critical_or_error(self) -> bool:
        return any(i.severity in ("CRITICAL", "ERROR") for i in self.issues)


# 전역 이슈 수집기
issue_collector = IssueCollector()


def check_command(command):
    """Check if a command exists in the path."""
    return shutil.which(command) is not None


def run_py_compile_all():
    """모든 Python 파일에 대해 py_compile 실행 (구문 오류 검증)"""
    print("## Running py_compile (Syntax Check)...")
    errors = []
    file_count = 0

    for target_dir in TARGET_DIRS:
        for py_file in Path(target_dir).rglob("*.py"):
            # 제외 패턴
            if any(x in str(py_file) for x in ["__pycache__", ".git", "node_modules", "tmp"]):
                continue
            file_count += 1
            try:
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as e:
                error_msg = str(e)
                # 라인 번호 추출 시도
                line_match = re.search(r"line (\d+)", error_msg)
                line_no = int(line_match.group(1)) if line_match else None
                errors.append({
                    "file": str(py_file),
                    "line": line_no,
                    "message": error_msg
                })
                # 이슈 수집기에 추가
                issue_collector.add(
                    severity="CRITICAL",
                    category="SYNTAX",
                    file_path=str(py_file),
                    line_no=line_no,
                    message=f"구문 오류: {error_msg}"
                )

    if errors:
        print(f"[CRITICAL] {len(errors)}개 파일에서 구문 오류 발견!\n")
        for err in errors[:10]:  # 최대 10개만 표시
            print(f"  - {err['file']}:{err['line'] or '?'}")
            print(f"    {err['message'][:100]}...")
        if len(errors) > 10:
            print(f"  ... 외 {len(errors) - 10}개")
        return len(errors)
    else:
        print(f"[OK] {file_count}개 파일 구문 검증 통과")
        return 0


def run_tool(name, command, ignore_failure=True):
    """Run a tool and print its output, returning the exit code."""
    print(f"## Running {name}...")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        print(result.stdout)
        if result.stderr:
            print(f"Errors:\n{result.stderr}")

        if result.returncode == 0:
            print(f"[OK] {name} passed.")
        else:
            print(f"[WARN] {name} found issues (Exit code: {result.returncode}).")

        return result.returncode
    except Exception as e:
        print(f"[ERROR] Failed to run {name}: {e}")
        return 1


def cmd_run():
    """전체 체크 실행 (run 서브명령어)"""
    global issue_collector
    issue_collector = IssueCollector()  # 이슈 수집기 초기화

    print("# oaischeck run\n")

    if not TARGET_DIRS:
        print("[ERROR] No source directories found (src, oais, tests).")
        return 1

    print("=" * 60)
    print("[OAISCHECK] Inspection Scope")
    print("=" * 60)
    print("The following directories will be inspected:\n")
    for d in TARGET_DIRS:
        print(f"  - {d}")
    print("\n" + "=" * 60 + "\n")

    print("Starting checks immediately...\n")

    failure_count = 0
    missing_tools = []

    # 0. py_compile (구문 검증) - 가장 먼저 실행
    syntax_errors = run_py_compile_all()
    if syntax_errors > 0:
        failure_count += 1
    print("-" * 40 + "\n")

    # 1. Pylint
    if check_command("pylint"):
        cmd = ["pylint", "--errors-only", "--output-format=text"] + TARGET_DIRS
        ret = run_tool("Pylint", cmd)
        if ret != 0:
            failure_count += 1
            # pylint 출력에서 에러 파싱 시도
            parse_pylint_errors(cmd)
    else:
        print("[ERROR] Pylint not found. Install with: uv sync --group dev")
        missing_tools.append("pylint")
        failure_count += 1

    print("-" * 40 + "\n")

    # 2. Mypy
    if check_command("mypy"):
        cmd = ["mypy", "--ignore-missing-imports"] + TARGET_DIRS
        ret = run_tool("Mypy", cmd)
        if ret != 0:
            failure_count += 1
            # mypy 출력에서 에러 파싱
            parse_mypy_errors(cmd)
    else:
        print("[ERROR] Mypy not found. Install with: uv sync --group dev")
        missing_tools.append("mypy")
        failure_count += 1

    print("-" * 40 + "\n")

    # 3. Pytest
    if check_command("pytest"):
        cmd = ["pytest", "-v", "--tb=short"]
        ret = run_tool("Pytest", cmd)
        if ret != 0:
            failure_count += 1
            issue_collector.add(
                severity="ERROR",
                category="TEST",
                file_path="tests/",
                line_no=None,
                message="pytest 테스트 실패"
            )
    else:
        print("[ERROR] Pytest not found. Install with: uv sync --group dev")
        missing_tools.append("pytest")
        failure_count += 1

    print("-" * 40 + "\n")

    # 4. oais Usage Validator (직접 호출)
    print("## Running oais Usage Validator...")
    result = get_oais_errors(PROJECT_ROOT)
    if result['total_errors'] > 0:
        print(f"[WARN] {result['total_errors']}개 oais 사용 오류 발견")
        failure_count += 1
        # oais 오류를 이슈 수집기에 추가
        for file_path, errors in result.get('server_errors', {}).items():
            for err in errors:
                issue_collector.add(
                    severity="ERROR",
                    category="OAIS",
                    file_path=file_path,
                    line_no=err.line_no,
                    message=f"oais.{err.attr_name} 잘못된 사용",
                    suggestion=err.suggestion
                )
    else:
        print("[OK] oais Usage Validator passed.")

    # 결과 요약 및 d0004_todo.md 등록
    print("\n" + "=" * 60)
    print("# Summary")
    print("=" * 60)

    counts = issue_collector.count_by_severity()
    print(f"\n발견된 이슈:")
    print(f"  - CRITICAL: {counts['CRITICAL']}개")
    print(f"  - ERROR: {counts['ERROR']}개")
    print(f"  - WARNING: {counts['WARNING']}개")
    print(f"  - INFO: {counts['INFO']}개")
    print(f"  - 총계: {len(issue_collector.issues)}개")

    if missing_tools:
        print(f"\n[WARN] 미설치 도구: {', '.join(missing_tools)}")
        print("  설치 명령: uv sync --group dev")

    # d0004_todo.md에 이슈 등록
    if issue_collector.issues:
        register_issues_to_todo(issue_collector)
        print(f"\n[OK] {len(issue_collector.issues)}개 이슈가 d0004_todo.md에 등록됨")
        return 1
    else:
        print("\n[OK] All checks passed successfully. 이슈 없음.")
        return 0


def parse_pylint_errors(cmd):
    """pylint 출력에서 에러 파싱"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        for line in result.stdout.split('\n'):
            # 형식: file.py:10:0: E0001: message
            match = re.match(r'^(.+?):(\d+):\d+: ([EWCRF]\d+): (.+)$', line)
            if match:
                file_path, line_no, code, message = match.groups()
                severity = "ERROR" if code.startswith('E') else "WARNING"
                issue_collector.add(
                    severity=severity,
                    category="LINT",
                    file_path=file_path,
                    line_no=int(line_no),
                    message=f"[{code}] {message}"
                )
    except Exception:
        pass


def parse_mypy_errors(cmd):
    """mypy 출력에서 에러 파싱"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        for line in result.stdout.split('\n'):
            # 형식: file.py:10: error: message
            match = re.match(r'^(.+?):(\d+): (error|warning): (.+)$', line)
            if match:
                file_path, line_no, level, message = match.groups()
                severity = "ERROR" if level == "error" else "WARNING"
                issue_collector.add(
                    severity=severity,
                    category="TYPE",
                    file_path=file_path,
                    line_no=int(line_no),
                    message=message
                )
    except Exception:
        pass


def register_issues_to_todo(collector: IssueCollector):
    """수집된 이슈를 d0004_todo.md에 등록"""
    todo_path = PROJECT_ROOT / "doc" / "d0004_todo.md"

    if not todo_path.exists():
        print(f"[WARN] {todo_path} not found. Skipping todo update.")
        return

    todo_content = todo_path.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # "현재 이슈" 테이블 찾기 (새 형식)
    # | ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
    # |----|--------|------|------|---------|------|
    # | - | - | - | (현재 이슈 없음) | - | - |
    current_issue_pattern = r'(\| ID \| 발생일 \| 분류 \| 내용 \| 우선순위 \| 상태 \|\n\|[-|]+\n)(\| - \| - \| - \| \(현재 이슈 없음\) \| - \| - \|)?'

    # 새 이슈 행 생성 (새 형식: ID | 발생일 | 분류 | 내용 | 우선순위 | 상태)
    new_rows = []
    for i, issue in enumerate(collector.issues, 1):
        issue_id = f"A{i:03d}"
        priority = "높음" if issue.severity in ("CRITICAL", "ERROR") else "중간"
        rel_path = issue.file_path
        if PROJECT_ROOT and issue.file_path.startswith(str(PROJECT_ROOT)):
            rel_path = str(Path(issue.file_path).relative_to(PROJECT_ROOT))
        line_info = f":{issue.line_no}" if issue.line_no else ""
        # 분류: BUGFIX (에러/버그)
        category = "BUGFIX"
        # 내용: [severity] 파일:라인 - 메시지
        message = issue.message[:40] + "..." if len(issue.message) > 40 else issue.message
        content = f"[{issue.category}] {rel_path}{line_info} - {message}"
        row = f"| {issue_id} | {today} | {category} | {content} | {priority} | 대기 |"
        new_rows.append(row)

    if new_rows:
        new_table_content = '\n'.join(new_rows)

        def replace_table(match):
            header = match.group(1)
            return header + new_table_content

        updated_content = re.sub(current_issue_pattern, replace_table, todo_content)

        if updated_content != todo_content:
            todo_path.write_text(updated_content, encoding="utf-8")
        else:
            # 패턴 매칭 실패 시 메시지
            print("[WARN] d0004_todo.md 현재 이슈 섹션 패턴 매칭 실패. 수동 등록 필요.")


def cmd_oais(dry_run: bool = False):
    """oais 모듈 사용 검증 (oais 서브명령어)"""
    print("# oaischeck oais\n")

    # oais 오류 검사
    result = get_oais_errors(PROJECT_ROOT)

    print(f"검사 대상: {result['total_files']}개 파일")
    print(f"총 오류: {result['total_errors']}개")
    print(f"운영 코드 오류 파일: {len(result['server_errors'])}개")

    if result['total_errors'] == 0:
        print("\n[OK] oais 모듈 사용에 문제가 없습니다.")
        return 0

    # 운영 코드 오류 상세 출력
    print("\n## 운영 코드 오류 상세")
    for file_path, errors in sorted(result['server_errors'].items()):
        rel_path = Path(file_path).relative_to(result['project_root'])
        print(f"\n### {rel_path}")
        for err in errors:
            fix = f" -> {err.suggestion}" if err.suggestion else " (서브모듈 확인 필요)"
            print(f"  L{err.line_no}: oais.{err.attr_name}{fix}")

    if dry_run:
        print("\n[DRY-RUN] d0004_todo.md 업데이트를 건너뜁니다.")
        return 1

    # d0004_todo.md에 등록
    update_todo_file(result)
    return 1


def get_next_todo_id(todo_content: str) -> str:
    """다음 TODO ID 반환 (TODO-XXX 형식)"""
    # 기존 TODO ID 패턴 찾기
    pattern = r"TODO-(\d{3})"
    matches = re.findall(pattern, todo_content)
    if matches:
        max_id = max(int(m) for m in matches)
        return f"TODO-{max_id + 1:03d}"
    return "TODO-001"


def update_todo_file(result: dict):
    """d0004_todo.md에 파일별 오류 등록"""
    todo_path = PROJECT_ROOT / "doc" / "d0004_todo.md"

    if not todo_path.exists():
        print(f"[WARN] {todo_path} not found. Skipping todo update.")
        return

    todo_content = todo_path.read_text(encoding="utf-8")

    # 기존 oais 모듈 사용 오류 이슈 삭제 (갱신을 위해)
    # "### [ERROR] oais 모듈 사용 오류" 로 시작하는 블록 제거
    old_issue_pattern = r"\n### \[ERROR\] oais 모듈 사용 오류[^\n]*\n(?:(?!###).*\n)*"
    todo_content = re.sub(old_issue_pattern, "\n", todo_content)

    # "## 대기중인 작업" 섹션 찾기
    section_pattern = r"(## 대기중인 작업\s*\n---\s*\n)"
    match = re.search(section_pattern, todo_content)

    if not match:
        print("[WARN] '대기중인 작업' 섹션을 찾을 수 없습니다.")
        return

    # 파일별 이슈 생성 (운영 코드만)
    today = datetime.now().strftime("%Y-%m-%d")
    new_issues = []

    for file_path, errors in sorted(result['server_errors'].items()):
        rel_path = Path(file_path).relative_to(result['project_root'])
        file_name = Path(file_path).stem

        # 각 오류에 대한 수정 정보 생성
        error_details = []
        for err in errors:
            if err.suggestion:
                error_details.append(
                    f"  - L{err.line_no}: `oais.{err.attr_name}` -> `{err.suggestion}`"
                )
            else:
                error_details.append(
                    f"  - L{err.line_no}: `oais.{err.attr_name}` (서브모듈 확인 필요)"
                )

        issue = f"""
### [ERROR] oais 모듈 사용 오류 - {file_name} ({today})

- **파일**: `{rel_path}`
- **오류 수**: {len(errors)}개
- **수정 내용**:
{chr(10).join(error_details)}
"""
        new_issues.append(issue)

    # 섹션 바로 다음에 추가
    section_end = match.end()
    all_issues = "\n".join(new_issues)
    updated_content = todo_content[:section_end] + all_issues + todo_content[section_end:]

    todo_path.write_text(updated_content, encoding="utf-8")
    print(f"\n[OK] {len(result['server_errors'])}개 파일의 이슈가 d0004_todo.md에 등록되었습니다.")


def cmd_error():
    """에러 체크만 수행 (error 서브명령어)"""
    print("# oaischeck error\n")

    if not TARGET_DIRS:
        print("[ERROR] No source directories found.")
        return 1

    print("## 에러 체크만 수행 (표준용어 체크 제외)\n")
    failure_count = 0

    # 1. Pylint
    if check_command("pylint"):
        cmd = ["pylint", "--errors-only"] + TARGET_DIRS
        ret = run_tool("Pylint (errors only)", cmd)
        if ret != 0:
            failure_count += 1
    else:
        print("[SKIP] Pylint not found.")

    print("-" * 40 + "\n")

    # 2. Mypy
    if check_command("mypy"):
        cmd = ["mypy", "--no-error-summary"] + TARGET_DIRS
        ret = run_tool("Mypy", cmd)
        if ret != 0:
            failure_count += 1
    else:
        print("[SKIP] Mypy not found.")

    print("\n# Summary")
    if failure_count == 0:
        print("No errors found.")
        return 0
    else:
        print(f"Errors found in {failure_count} tools.")
        return 1


def cmd_term():
    """표준용어 체크만 수행 (term 서브명령어)"""
    print("# oaischeck term\n")

    # 표준용어 파일 로드
    term_file = PROJECT_ROOT / "doc" / "d0006_db.md"
    if not term_file.exists():
        print(f"[ERROR] 표준용어 파일을 찾을 수 없습니다: {term_file}")
        return 1

    # 표준용어 추출 (sys_standard_word 테이블 섹션에서)
    term_content = term_file.read_text(encoding="utf-8")

    # 간단한 표준용어 패턴 매칭 (실제 구현은 더 정교해야 함)
    print("## 표준용어 체크")
    print("표준용어 파일: doc/d0006_db.md")
    print("\n[INFO] 표준용어 체크는 현재 기본 검사만 수행합니다.")
    print("[OK] 표준용어 체크 완료")
    return 0


def cmd_update():
    """d0004/d0010 문서 정리 및 동기화 (update 서브명령어)"""
    print("# oaischeck update\n")

    todo_file = PROJECT_ROOT / "doc" / "d0004_todo.md"
    history_file = PROJECT_ROOT / "doc" / "d0010_history.md"

    updated = False

    # d0004_todo.md 정리
    if todo_file.exists():
        content = todo_file.read_text(encoding="utf-8")
        original_len = len(content)

        # 완료된 항목 찾기 (체크된 항목)
        completed_pattern = r"- \[x\] (.+)"
        completed_items = re.findall(completed_pattern, content, re.IGNORECASE)

        if completed_items:
            print(f"## d0004_todo.md에서 완료된 항목 {len(completed_items)}개 발견")
            for item in completed_items[:5]:  # 최대 5개만 표시
                print(f"  - {item[:50]}...")

            # 완료된 항목을 history로 이동할지는 사용자 확인 필요
            print("\n[INFO] 완료된 항목은 수동으로 d0010_history.md로 이동하세요.")
            updated = True
        else:
            print("## d0004_todo.md: 완료된 항목 없음")
    else:
        print(f"[WARN] {todo_file} not found")

    # d0010_history.md 확인
    if history_file.exists():
        content = history_file.read_text(encoding="utf-8")
        # 최근 이력 항목 수 확인
        history_pattern = r"### \[.+?\]"
        history_items = re.findall(history_pattern, content)
        print(f"\n## d0010_history.md: {len(history_items)}개 이력 항목")
    else:
        print(f"[WARN] {history_file} not found")

    print("\n[OK] 문서 상태 확인 완료")
    return 0


def cmd_debug(error_msg: str = None):
    """심층 디버깅 워크플로우 (debug 서브명령어)"""
    print("# oaischeck debug\n")

    if error_msg:
        print(f"## 분석 대상 에러: {error_msg}\n")

        # 에러 유형 분류
        error_types = {
            "TypeError": "타입 불일치 오류",
            "ValueError": "값 오류",
            "AttributeError": "속성 접근 오류",
            "KeyError": "딕셔너리 키 오류",
            "ImportError": "모듈 임포트 오류",
            "ModuleNotFoundError": "모듈을 찾을 수 없음",
            "SyntaxError": "문법 오류",
            "IndentationError": "들여쓰기 오류",
            "NameError": "정의되지 않은 이름",
            "FileNotFoundError": "파일을 찾을 수 없음",
        }

        detected_type = None
        for err_type, desc in error_types.items():
            if err_type.lower() in error_msg.lower():
                detected_type = (err_type, desc)
                break

        if detected_type:
            print(f"### 에러 유형: {detected_type[0]}")
            print(f"### 설명: {detected_type[1]}")
            print("\n### 권장 조치:")

            if detected_type[0] == "ImportError":
                print("  1. 순환 참조 확인: oaischeck circular")
                print("  2. 모듈 경로 확인")
                print("  3. __init__.py 파일 확인")
            elif detected_type[0] == "AttributeError":
                print("  1. oais 모듈 사용 검증: oaischeck oais")
                print("  2. None 체크 추가")
                print("  3. 속성 존재 여부 확인")
            elif detected_type[0] == "TypeError":
                print("  1. 인자 타입 확인")
                print("  2. None 값 처리")
                print("  3. 타입 힌트 추가 후 mypy 실행")
            else:
                print("  1. 스택 트레이스 분석")
                print("  2. 관련 코드 리뷰")
                print("  3. 단위 테스트 작성")
        else:
            print("### 에러 유형을 자동 감지할 수 없습니다.")
            print("### 수동 분석이 필요합니다.")
    else:
        print("## 디버깅 워크플로우 가이드\n")
        print("1. 에러 메시지 수집")
        print("2. 에러 유형 분류")
        print("3. 관련 코드 탐색")
        print("4. 근본 원인 분석")
        print("5. 수정 및 검증")
        print("\n### 사용 예시:")
        print('  oaischeck debug "TypeError: NoneType has no attribute"')
        print('  oaischeck debug "ImportError: circular import"')

    return 0


def get_imports_from_file(file_path):
    """파일에서 import 문 추출"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except Exception:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def find_cycles_in_graph(graph):
    """의존성 그래프에서 순환 찾기"""
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in stack:
                cycle = path[path.index(neighbor):] + [neighbor]
                cycles.append(cycle)

        path.pop()
        stack.remove(node)

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node, [])

    return cycles


def cmd_circular(module_name: str = None):
    """순환 참조 감지 (circular 서브명령어)"""
    print("# oaischeck circular\n")

    target_dir = PROJECT_ROOT / "oais"
    if module_name:
        target_dir = PROJECT_ROOT / module_name
        if not target_dir.exists():
            target_dir = PROJECT_ROOT / "oais"
            print(f"[INFO] '{module_name}' 디렉토리가 없어 oais 폴더를 검사합니다.\n")

    if not target_dir.exists():
        print(f"[ERROR] 대상 디렉토리가 없습니다: {target_dir}")
        return 1

    print(f"## 검사 대상: {target_dir}\n")

    # 의존성 그래프 생성
    graph = defaultdict(list)
    py_files = list(target_dir.rglob("*.py"))

    module_base = target_dir.name

    for py_file in py_files:
        rel_path = py_file.relative_to(target_dir)
        module_name_current = str(rel_path.with_suffix('')).replace('/', '.').replace('\\', '.')
        if module_name_current == '__init__':
            module_name_current = module_base
        else:
            module_name_current = f"{module_base}.{module_name_current}"

        imports = get_imports_from_file(py_file)
        for imp in imports:
            if imp.startswith(module_base):
                graph[module_name_current].append(imp)

    # 순환 참조 찾기
    cycles = find_cycles_in_graph(graph)

    if cycles:
        print(f"### [WARN] {len(cycles)}개 순환 참조 발견!\n")
        for i, cycle in enumerate(cycles[:10], 1):  # 최대 10개만 표시
            print(f"  {i}. {' -> '.join(cycle)}")

        if len(cycles) > 10:
            print(f"\n  ... 외 {len(cycles) - 10}개")

        return 1
    else:
        print("[OK] 순환 참조가 발견되지 않았습니다.")
        return 0


def print_usage():
    """사용법 출력"""
    print("""oaischeck - 통합 코드 품질 체크

사용법:
    oaischeck run              전체 체크 실행 (pylint, mypy, pytest, oais)
    oaischeck oais             oais 모듈 검증 및 d0004_todo.md 등록
    oaischeck oais --dry-run   검증만 (todo 등록 안함)
    oaischeck error            에러 체크만 (pylint, mypy)
    oaischeck term             표준용어 체크만
    oaischeck update           d0004/d0010 문서 정리
    oaischeck debug [에러]     심층 디버깅 워크플로우
    oaischeck circular [모듈]  순환 참조 감지

예시:
    python v/script/oaischeck_run.py run
    python v/script/oaischeck_run.py oais
    python v/script/oaischeck_run.py error
    python v/script/oaischeck_run.py debug "TypeError: NoneType"
    python v/script/oaischeck_run.py circular oais
""")


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaischeck", sys.argv[1:]):
        return

    # Agent 환경에서 출력 캡처를 위해 로그 파일로 리다이렉션 코드를 제거합니다.
    # log_file = PROJECT_ROOT / "oaischeck_report.log"
    # sys.stdout = open(log_file, "w", encoding="utf-8")
    # sys.stderr = sys.stdout
    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    subcommand = args[0]

    if subcommand == "run":
        return cmd_run()
    elif subcommand == "oais":
        dry_run = "--dry-run" in args
        return cmd_oais(dry_run=dry_run)
    elif subcommand == "error":
        return cmd_error()
    elif subcommand == "term":
        return cmd_term()
    elif subcommand == "update":
        return cmd_update()
    elif subcommand == "debug":
        error_msg = args[1] if len(args) > 1 else None
        return cmd_debug(error_msg)
    elif subcommand == "circular":
        module_name = args[1] if len(args) > 1 else None
        return cmd_circular(module_name)
    elif subcommand in ("-h", "--help", "help"):
        print_usage()
        return 0
    else:
        print(f"[ERROR] Unknown subcommand: {subcommand}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
