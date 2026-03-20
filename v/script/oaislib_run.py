#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaislib_run.py

oais 모듈 수정 및 최적화 스크립트

명령어:
    oaislib run              현재 문제점 수정 (d0004 이슈 기반)
    oaislib optimize         문제점 수정 + 최적화
    oaislib status           상태 및 이슈 요약
    oaislib doc              문서화만 수행 (d0005_lib.md)
"""

import ast
import re
import sys
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OAIS_DIR = PROJECT_ROOT / "oais"
DOC_DIR = PROJECT_ROOT / "doc"
TMP_DIR = PROJECT_ROOT / "tmp"
TODO_FILE = DOC_DIR / "d0004_todo.md"
LIB_DOC_FILE = DOC_DIR / "d0005_lib.md"

# ID prefix for oaislib tasks
ID_PREFIX = "L"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaislib - oais 모듈 수정 및 최적화")
    print()
    print("사용법:")
    print("    oaislib run              현재 문제점 수정 (d0004 이슈 기반)")
    print("    oaislib optimize         문제점 수정 + 최적화")
    print("    oaislib status           상태 및 이슈 요약")
    print("    oaislib doc              문서화만 수행 (d0005_lib.md)")
    print()
    print("옵션:")
    print("    --module [name]          특정 모듈만 대상")
    print("    --dry-run                실제 수정 없이 분석만")
    print("    --interactive            각 단계마다 사용자 승인")
    print("    --report                 리포트 생성 (tmp/)")
    print()
    print("예시:")
    print("    uv run python v/script/oaislib_run.py run")
    print("    uv run python v/script/oaislib_run.py optimize --module config")
    print("    uv run python v/script/oaislib_run.py status")


def extract_oais_issues_from_todo():
    """d0004_todo.md에서 oais 관련 이슈 추출"""
    if not TODO_FILE.exists():
        return []

    content = TODO_FILE.read_text(encoding="utf-8")
    issues = []

    # 테이블 형식 파싱: | ID | 날짜 | 내용 | 우선순위 | 상태 |
    pattern = r"\|\s*(A\d+|L\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"

    for match in re.finditer(pattern, content):
        issue_id = match.group(1).strip()
        date = match.group(2).strip()
        desc = match.group(3).strip()
        priority = match.group(4).strip()
        status = match.group(5).strip()

        # oais/ 관련 이슈만 필터링
        if "oais/" in desc or "oais\\" in desc:
            issues.append({
                "id": issue_id,
                "date": date,
                "description": desc,
                "priority": priority,
                "status": status
            })

    return issues


def analyze_module(file_path):
    """Python 모듈 분석"""
    issues = []

    # 1. py_compile 검증
    import py_compile
    try:
        py_compile.compile(str(file_path), doraise=True)
    except py_compile.PyCompileError as e:
        issues.append({
            "type": "SYNTAX",
            "file": str(file_path),
            "message": str(e)
        })
        return issues  # 구문 오류면 추가 분석 불가

    # 2. AST 분석
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))

        # 미사용 import 탐지 (간단한 버전)
        imports = []
        names_used = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append(alias.asname or alias.name)
            elif isinstance(node, ast.Name):
                names_used.add(node.id)

        # 간단한 미사용 import 체크 (정확하지 않음, 참고용)
        for imp in imports:
            base_name = imp.split(".")[0]
            if base_name not in names_used and not imp.startswith("_"):
                # 너무 많은 false positive 방지를 위해 기록만
                pass

    except SyntaxError as e:
        issues.append({
            "type": "SYNTAX",
            "file": str(file_path),
            "message": str(e)
        })

    return issues


def analyze_oais_modules(target_module=None):
    """oais/ 전체 모듈 분석"""
    if not OAIS_DIR.exists():
        print(f"[ERROR] {OAIS_DIR} 디렉토리를 찾을 수 없습니다.")
        return []

    all_issues = []

    for py_file in sorted(OAIS_DIR.glob("*.py")):
        if py_file.name == "__init__.py":
            continue

        # 모듈 필터
        if target_module and target_module.lower() not in py_file.stem.lower():
            continue

        issues = analyze_module(py_file)
        all_issues.extend(issues)

    return all_issues


def get_next_todo_id():
    """다음 TODO ID 생성"""
    if not TODO_FILE.exists():
        return f"{ID_PREFIX}001"

    content = TODO_FILE.read_text(encoding="utf-8")
    pattern = rf"\|\s*{ID_PREFIX}(\d+)\s*\|"
    matches = re.findall(pattern, content)

    if not matches:
        return f"{ID_PREFIX}001"

    max_num = max(int(m) for m in matches)
    return f"{ID_PREFIX}{max_num + 1:03d}"


def cmd_status(options):
    """상태 및 이슈 요약"""
    print("# oaislib status\n")

    # 1. oais 모듈 현황
    print("## oais 모듈 현황\n")

    if not OAIS_DIR.exists():
        print(f"[ERROR] {OAIS_DIR} 디렉토리를 찾을 수 없습니다.")
        return 1

    py_files = list(OAIS_DIR.glob("*.py"))
    py_files = [f for f in py_files if f.name != "__init__.py"]

    print(f"총 모듈 수: {len(py_files)}개\n")

    for py_file in sorted(py_files)[:10]:
        size = py_file.stat().st_size
        print(f"  {py_file.name:<30} ({size:,} bytes)")

    if len(py_files) > 10:
        print(f"  ... 외 {len(py_files) - 10}개")

    print()

    # 2. d0004 이슈 현황
    print("## d0004_todo.md oais 관련 이슈\n")

    issues = extract_oais_issues_from_todo()

    if not issues:
        print("  oais 관련 이슈가 없습니다.")
    else:
        pending = [i for i in issues if i["status"] in ["대기", "pending"]]
        in_progress = [i for i in issues if i["status"] in ["진행중", "in_progress"]]

        print(f"  대기 중: {len(pending)}개")
        print(f"  진행 중: {len(in_progress)}개")
        print()

        # 상위 5개 이슈 표시
        print("### 주요 이슈 (상위 5개)")
        for issue in issues[:5]:
            print(f"  [{issue['id']}] {issue['description'][:50]}...")
            print(f"       우선순위: {issue['priority']} | 상태: {issue['status']}")

    print()
    print("---")
    print("[TIP] 'oaislib run'으로 문제점 수정을 시작하세요.")

    return 0


def cmd_run(options):
    """현재 문제점 수정 (d0004 이슈 기반)"""
    print("# oaislib run\n")
    print("=== oais 모듈 문제점 수정 ===\n")

    dry_run = options.get("dry_run", False)
    target_module = options.get("module")

    if dry_run:
        print("[DRY-RUN] 실제 수정 없이 분석만 수행합니다.\n")

    # 1. d0004에서 oais 관련 이슈 추출
    print("## 1단계: d0004_todo.md 이슈 확인\n")

    issues = extract_oais_issues_from_todo()
    pending_issues = [i for i in issues if i["status"] in ["대기", "pending"]]

    if target_module:
        pending_issues = [i for i in pending_issues if target_module.lower() in i["description"].lower()]

    print(f"  oais 관련 대기 이슈: {len(pending_issues)}개\n")

    # 2. 모듈 분석 (신규 이슈 탐지)
    print("## 2단계: 모듈 분석 (신규 이슈 탐지)\n")

    new_issues = analyze_oais_modules(target_module)
    print(f"  분석 완료. 신규 탐지 이슈: {len(new_issues)}개\n")

    # 3. 이슈 목록 출력
    print("## 3단계: 수정 대상 이슈\n")

    all_issues_count = len(pending_issues) + len(new_issues)

    if all_issues_count == 0:
        print("  수정할 이슈가 없습니다. oais 모듈이 정상입니다.")
        return 0

    print(f"  총 {all_issues_count}개 이슈 발견\n")

    # 기존 이슈
    if pending_issues:
        print("### d0004 기존 이슈")
        for issue in pending_issues[:10]:
            print(f"  [{issue['id']}] {issue['description'][:60]}")
        if len(pending_issues) > 10:
            print(f"  ... 외 {len(pending_issues) - 10}개")
        print()

    # 신규 이슈
    if new_issues:
        print("### 신규 탐지 이슈")
        for issue in new_issues[:5]:
            print(f"  [{issue['type']}] {issue['file']}")
            print(f"       {issue['message'][:60]}")
        if len(new_issues) > 5:
            print(f"  ... 외 {len(new_issues) - 5}개")
        print()

    # 4. 수정 가이드
    print("## 4단계: 수정 가이드\n")
    print("  [INFO] oaislib는 서브에이전트 기반으로 동작합니다.")
    print("  [TIP] Task tool로 task-executor, python-code-reviewer를 사용하세요.")
    print()
    print("### 수정 워크플로우")
    print("  1. 이슈별로 TODO 상태를 '진행중'으로 변경")
    print("  2. 코드 수정 수행")
    print("  3. py_compile 검증")
    print("  4. 수정 완료 시 '해결된 이슈' 섹션으로 이동")
    print()

    if dry_run:
        print("[DRY-RUN] 완료. 실제 수정은 수행되지 않았습니다.")

    return 0


def cmd_optimize(options):
    """문제점 수정 + 최적화"""
    print("# oaislib optimize\n")
    print("=== oais 모듈 수정 + 최적화 ===\n")

    dry_run = options.get("dry_run", False)
    target_module = options.get("module")

    if dry_run:
        print("[DRY-RUN] 실제 수정 없이 분석만 수행합니다.\n")

    # 1. run 워크플로우 먼저 실행
    print("## Phase 1: 문제점 수정 (run)\n")
    cmd_run(options)

    print("\n" + "=" * 50 + "\n")

    # 2. 최적화 분석
    print("## Phase 2: 최적화 분석\n")

    if not OAIS_DIR.exists():
        print(f"[ERROR] {OAIS_DIR} 디렉토리를 찾을 수 없습니다.")
        return 1

    optimization_candidates = []

    for py_file in sorted(OAIS_DIR.glob("*.py")):
        if py_file.name == "__init__.py":
            continue

        if target_module and target_module.lower() not in py_file.stem.lower():
            continue

        size = py_file.stat().st_size
        lines = len(py_file.read_text(encoding="utf-8").splitlines())

        # 최적화 대상 판단 기준
        candidates = []

        # 큰 파일 (500줄 이상)
        if lines > 500:
            candidates.append(f"대형 파일 ({lines}줄) - 모듈 분리 검토")

        # 큰 용량 (50KB 이상)
        if size > 50000:
            candidates.append(f"대용량 파일 ({size:,} bytes) - 최적화 필요")

        if candidates:
            optimization_candidates.append({
                "file": py_file.name,
                "lines": lines,
                "size": size,
                "suggestions": candidates
            })

    # 3. 최적화 대상 출력
    print("### 최적화 대상 모듈\n")

    if not optimization_candidates:
        print("  최적화가 필요한 모듈이 없습니다.")
    else:
        for item in optimization_candidates:
            print(f"  **{item['file']}** ({item['lines']}줄, {item['size']:,} bytes)")
            for suggestion in item["suggestions"]:
                print(f"    - {suggestion}")
            print()

    # 4. 최적화 체크리스트
    print("### 최적화 체크리스트\n")
    print("  [ ] 중복 코드 제거")
    print("  [ ] 미사용 import 정리")
    print("  [ ] 미사용 함수/클래스 삭제")
    print("  [ ] 타입 힌트 추가")
    print("  [ ] 모듈 분리 (큰 파일)")
    print()

    # 5. 가이드
    print("## 최적화 가이드\n")
    print("  [INFO] oaislib optimize는 서브에이전트 기반으로 동작합니다.")
    print("  [TIP] python-code-reviewer로 상세 리뷰를 받으세요.")
    print()
    print("### TODO 등록 형식")
    print(f"  | {get_next_todo_id()} | {datetime.now().strftime('%Y-%m-%d')} | [OPT] oais/module.py - 설명 | 중간 | 대기 |")
    print()

    if dry_run:
        print("[DRY-RUN] 완료. 실제 수정은 수행되지 않았습니다.")

    return 0


def cmd_doc(options):
    """문서화만 수행"""
    print("# oaislib doc\n")
    print("=== d0005_lib.md 문서 업데이트 ===\n")

    if not OAIS_DIR.exists():
        print(f"[ERROR] {OAIS_DIR} 디렉토리를 찾을 수 없습니다.")
        return 1

    # 기존 oaislib_update.py의 문서화 로직 호출
    from oaislib_update import cmd_update
    return cmd_update(options)


def parse_options(args):
    """옵션 파싱"""
    options = {
        "dry_run": "--dry-run" in args,
        "interactive": "--interactive" in args,
        "report": "--report" in args,
        "module": None
    }

    # --module [name]
    if "--module" in args:
        idx = args.index("--module")
        if idx + 1 < len(args) and not args[idx + 1].startswith("--"):
            options["module"] = args[idx + 1]

    return options


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaislib", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    options = parse_options(args)

    if cmd == "run":
        return cmd_run(options)
    elif cmd == "optimize":
        return cmd_optimize(options)
    elif cmd == "status":
        return cmd_status(options)
    elif cmd == "doc":
        return cmd_doc(options)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
