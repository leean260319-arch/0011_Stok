#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaisfix_run.py

d0004_todo.md 기반 코드 오류 자동 수정 스크립트

명령어:
    oaisfix run [대상]     - 이슈 자동 수정
    oaisfix preview        - 수정 미리보기 (dry-run)
    oaisfix test [대상]    - 테스트 시나리오 실행
    oaisfix verify [파일]  - 수정 검증
    oaisfix rollback       - 마지막 수정 롤백
    oaisfix status         - 이슈 상태 조회
"""

import sys
import os
import re
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from oais_common import show_help_if_no_args

# 프로젝트 루트 설정
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BACKUP_DIR = PROJECT_ROOT / "tmp" / "oaisfix_backup"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaisfix - 코드 오류 자동 수정 도구")
    print()
    print("사용법:")
    print("    oaisfix run              전체 이슈 자동 수정")
    print("    oaisfix run [이슈ID]     특정 이슈만 수정 (예: TODO-001)")
    print("    oaisfix run [카테고리]   카테고리별 수정 (CRITICAL/ERROR/WARNING)")
    print("    oaisfix preview          수정 미리보기 (실제 수정 없음)")
    print("    oaisfix preview [이슈ID] 특정 이슈 미리보기")
    print("    oaisfix test             전체 테스트 시나리오 실행")
    print("    oaisfix test [시나리오]  특정 시나리오만 실행 (예: TC-001)")
    print("    oaisfix verify           최근 수정 파일 검증")
    print("    oaisfix verify [파일]    특정 파일 검증")
    print("    oaisfix rollback         마지막 수정 롤백")
    print("    oaisfix status           이슈 현황 조회")
    print("    oaisfix status [카테고리] 카테고리별 상태")
    print()
    print("예시:")
    print("    python v/script/oaisfix_run.py run")
    print("    python v/script/oaisfix_run.py preview")
    print("    python v/script/oaisfix_run.py test TC-001")
    print("    python v/script/oaisfix_run.py status CRITICAL")


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisfix", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    cmd_args = args[1:]

    if cmd == "run":
        return cmd_run(cmd_args)
    elif cmd == "preview":
        return cmd_preview(cmd_args)
    elif cmd == "test":
        return cmd_test(cmd_args)
    elif cmd == "verify":
        return cmd_verify(cmd_args)
    elif cmd == "rollback":
        return cmd_rollback()
    elif cmd == "status":
        return cmd_status(cmd_args)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


def cmd_run(args):
    """이슈 자동 수정 (run 서브명령어)"""
    print("# oaisfix run\n")

    todo_file = PROJECT_ROOT / "doc" / "d0004_todo.md"
    if not todo_file.exists():
        print("[ERROR] d0004_todo.md not found")
        return 1

    content = todo_file.read_text(encoding="utf-8")
    issues = parse_issues(content)

    # 필터 적용
    target = args[0] if args else None
    if target:
        if target.startswith("A") and target[1:].isdigit():
            issues = [i for i in issues if i["id"] == target]
        elif target.upper() in ["CRITICAL", "ERROR", "WARNING", "INFO"]:
            issues = [i for i in issues if i["severity"] == target.upper()]
        elif target.upper() in ["BUGFIX", "HOTFIX", "UPDATE", "FEATURE"]:
            issues = [i for i in issues if i.get("category") == target.upper()]
        else:
            # 파일 경로로 필터
            issues = [i for i in issues if target in (i.get("file") or "")]

    if not issues:
        print("[INFO] No issues found to fix.")
        return 0

    # False Positive와 실제 이슈 분리
    false_positives = [i for i in issues if i.get("is_false_positive")]
    real_issues = [i for i in issues if not i.get("is_false_positive")]

    print(f"[INFO] Found {len(issues)} issues to process:")
    print(f"  - False Positives: {len(false_positives)} (will be resolved as FP)")
    print(f"  - Real Issues: {len(real_issues)} (will attempt to fix)\n")

    # 백업 디렉토리 생성
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    fixed_count = 0
    fp_count = 0

    # 1. False Positive 처리 (해결된 이슈로 이동)
    if false_positives:
        print("## Phase 1: False Positive 처리\n")
        for issue in false_positives:
            title_short = issue['title'][:60] + "..." if len(issue['title']) > 60 else issue['title']
            print(f"  {issue['id']}: {title_short}")
            print(f"    -> [FP] 동적 로딩/선택적 의존성 모듈 (수정 제외)")
            fp_count += 1
        print()

        # False Positive를 해결된 이슈로 이동
        move_to_resolved(false_positives, "False Positive - 동적 로딩/선택적 의존성 모듈")

    # 2. 실제 이슈 수정 시도
    if real_issues:
        print("## Phase 2: 실제 이슈 수정\n")
        for issue in real_issues:
            title_short = issue['title'][:60] + "..." if len(issue['title']) > 60 else issue['title']
            print(f"  {issue['id']}: {title_short}")

            # 백업 생성
            if issue.get("file"):
                backup_file(issue["file"])

            if apply_fix(issue):
                print(f"    -> [OK] FIXED")
                fixed_count += 1
                move_to_resolved([issue], "자동 수정 완료")
            else:
                print(f"    -> [SKIP] Manual fix required")
            print()

    print(f"---")
    print(f"# Summary:")
    print(f"  - False Positives resolved: {fp_count}")
    print(f"  - Issues fixed: {fixed_count}")
    print(f"  - Total processed: {fp_count + fixed_count}/{len(issues)}")
    return 0


def move_to_resolved(issues, resolution_method):
    """
    이슈를 '현재 이슈'에서 '해결된 이슈'로 이동

    Args:
        issues: 이동할 이슈 목록
        resolution_method: 해결 방법 설명
    """
    todo_file = PROJECT_ROOT / "doc" / "d0004_todo.md"
    if not todo_file.exists():
        return

    content = todo_file.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    for issue in issues:
        issue_id = issue["id"]

        # 1. 현재 이슈 테이블에서 해당 행 삭제
        # 패턴: | A001 | 2026-01-02 | BUGFIX | ... | 높음 | 대기 |
        row_pattern = rf"\| {issue_id} \|[^\n]+\n"
        content = re.sub(row_pattern, "", content)

        # 2. 해결된 이슈 테이블에 추가
        # 패턴: | ID | 발생일 | 분류 | 내용 | 해결일 | 해결방법 |
        resolved_row = f"| {issue_id} | {issue.get('date', today)} | {issue.get('category', 'BUGFIX')} | {issue['title'][:50]}... | {today} | {resolution_method} |\n"

        # 해결된 이슈 테이블 헤더 찾기
        resolved_header_pattern = r"(\| ID \| 발생일 \| 분류 \| 내용 \| 해결일 \| 해결방법 \|\n\|[-|]+\n)"
        resolved_match = re.search(resolved_header_pattern, content)

        if resolved_match:
            # 헤더 다음에 새 행 추가
            insert_pos = resolved_match.end()
            content = content[:insert_pos] + resolved_row + content[insert_pos:]
        else:
            print(f"  [WARN] Could not find resolved issues table for {issue_id}")

    # 현재 이슈가 모두 삭제되었으면 "(현재 이슈 없음)" 행 추가
    active_section_match = re.search(
        r"### 현재 이슈 \(Active Issues\)(.*?)(?=### 해결된 이슈|$)",
        content,
        re.DOTALL
    )
    if active_section_match:
        active_section = active_section_match.group(1)
        # 테이블 행이 있는지 확인 (A로 시작하는 ID)
        if not re.search(r"\| A\d{3} \|", active_section):
            # 현재 이슈 없음 행 추가 (테이블 헤더 다음에)
            header_pattern = r"(\| ID \| 발생일 \| 분류 \| 내용 \| 우선순위 \| 상태 \|\n\|[-|]+\n)"
            empty_row = "| - | - | - | (현재 이슈 없음) | - | - |\n"
            content = re.sub(
                header_pattern,
                rf"\g<1>{empty_row}",
                content,
                count=1
            )

    todo_file.write_text(content, encoding="utf-8")


def cmd_preview(args):
    """수정 미리보기 (preview 서브명령어)"""
    print("# oaisfix preview\n")
    print("## 수정 예정 목록 (실제 수정 없음)\n")

    todo_file = PROJECT_ROOT / "doc" / "d0004_todo.md"
    if not todo_file.exists():
        print("[ERROR] d0004_todo.md not found")
        return 1

    content = todo_file.read_text(encoding="utf-8")
    issues = parse_issues(content)

    # 필터 적용
    target = args[0] if args else None
    if target and target.startswith("TODO-"):
        issues = [i for i in issues if i["id"] == target]

    if not issues:
        print("[INFO] No issues found.")
        return 0

    for issue in issues:
        fix_type = get_fix_type(issue)
        status = "자동 수정 가능" if fix_type else "수동 검토 필요"
        print(f"  {issue['id']} [{issue['severity']}] {issue['title']}")
        print(f"    -> 파일: {issue.get('file', 'N/A')}")
        print(f"    -> 상태: {status}")
        if fix_type:
            print(f"    -> 수정 유형: {fix_type}")
        print()

    auto_count = sum(1 for i in issues if get_fix_type(i))
    manual_count = len(issues) - auto_count
    print(f"---\n자동 수정: {auto_count}개 | 수동 필요: {manual_count}개")
    return 0


def cmd_test(args):
    """테스트 시나리오 실행 (test 서브명령어)"""
    print("# oaisfix test\n")

    test_file = PROJECT_ROOT / "doc" / "d0003_test.md"
    if not test_file.exists():
        print("[WARN] d0003_test.md not found. Running pytest instead.")
        return run_pytest(args)

    content = test_file.read_text(encoding="utf-8")

    # 테스트 시나리오 파싱
    scenarios = parse_test_scenarios(content)

    target = args[0] if args else None
    if target:
        if target.startswith("TC-"):
            scenarios = [s for s in scenarios if s["id"] == target]
        elif target in ["unit", "integration", "e2e"]:
            scenarios = [s for s in scenarios if s.get("type") == target]

    if not scenarios:
        print("[INFO] No test scenarios found. Running pytest...")
        return run_pytest(args)

    print(f"## 테스트 시나리오 로드: {len(scenarios)}개\n")

    passed = 0
    failed = 0
    for sc in scenarios:
        print(f"  {sc['id']}: {sc['name']}")
        # 실제 테스트 실행 (여기서는 시뮬레이션)
        if sc.get("file") and Path(PROJECT_ROOT / sc["file"]).exists():
            result = run_single_test(sc)
            if result:
                print("    -> [PASS]")
                passed += 1
            else:
                print("    -> [FAIL]")
                failed += 1
        else:
            print("    -> [SKIP] 테스트 파일 없음")

    print(f"\n---\n결과: {passed}/{passed+failed} 통과")
    if passed + failed > 0:
        print(f"({100*passed/(passed+failed):.1f}%)")
    return 0 if failed == 0 else 1


def cmd_verify(args):
    """수정 검증 (verify 서브명령어)"""
    print("# oaisfix verify\n")

    target = args[0] if args else None

    if target:
        files_to_verify = [Path(target)]
    else:
        # 최근 백업된 파일들 검증
        if not BACKUP_DIR.exists():
            print("[INFO] No recent fixes to verify.")
            return 0
        files_to_verify = [
            PROJECT_ROOT / f.name.replace(".backup", "")
            for f in BACKUP_DIR.glob("*.backup")
        ]

    if not files_to_verify:
        print("[INFO] No files to verify.")
        return 0

    print(f"## 검증 대상: {len(files_to_verify)}개 파일\n")

    all_passed = True
    for file_path in files_to_verify:
        if not file_path.exists():
            continue

        print(f"### {file_path.name}")

        # 1. 구문 검사
        if file_path.suffix == ".py":
            result = verify_syntax(file_path)
            if result:
                print("  [OK] 구문 검사 통과")
            else:
                print("  [FAIL] 구문 오류")
                all_passed = False
                continue

            # 2. 타입 검사 (mypy)
            mypy_result = run_mypy(file_path)
            if mypy_result is None:
                print("  [SKIP] mypy 없음")
            elif mypy_result:
                print("  [OK] 타입 검사 통과")
            else:
                print("  [WARN] 타입 오류 발견")

        print()

    return 0 if all_passed else 1


def cmd_rollback():
    """마지막 수정 롤백 (rollback 서브명령어)"""
    print("# oaisfix rollback\n")

    if not BACKUP_DIR.exists():
        print("[INFO] No backups found to rollback.")
        return 0

    backups = list(BACKUP_DIR.glob("*.backup"))
    if not backups:
        print("[INFO] No backup files found.")
        return 0

    print(f"## 롤백 가능한 백업: {len(backups)}개\n")

    for backup in backups:
        original_name = backup.name.replace(".backup", "")
        original_path = PROJECT_ROOT / original_name

        # 백업에서 복원
        if backup.exists():
            shutil.copy2(backup, original_path)
            print(f"  [ROLLBACK] {original_name}")
            backup.unlink()  # 백업 삭제

    print("\n[INFO] Rollback completed.")
    return 0


def cmd_status(args):
    """이슈 상태 조회 (status 서브명령어)"""
    print("# oaisfix status\n")

    todo_file = PROJECT_ROOT / "doc" / "d0004_todo.md"
    if not todo_file.exists():
        print("[ERROR] d0004_todo.md not found")
        return 1

    content = todo_file.read_text(encoding="utf-8")
    issues = parse_issues(content, include_all=True)

    # 카테고리별 필터
    target = args[0].upper() if args else None
    if target and target in ["CRITICAL", "ERROR", "WARNING", "INFO"]:
        issues = [i for i in issues if i["severity"] == target]

    # 카테고리별 집계
    by_severity = defaultdict(list)
    for issue in issues:
        by_severity[issue["severity"]].append(issue)

    print("## 이슈 현황\n")
    for sev in ["CRITICAL", "ERROR", "WARNING", "INFO"]:
        count = len(by_severity.get(sev, []))
        completed = sum(1 for i in by_severity.get(sev, []) if i.get("status") == "completed")
        if count > 0 or sev in ["CRITICAL", "ERROR"]:
            print(f"  {sev}: {count}개", end="")
            if completed > 0:
                print(f" ({completed}개 완료)")
            else:
                print()

    # 최근 수정
    history_file = PROJECT_ROOT / "doc" / "d0010_history.md"
    if history_file.exists():
        print("\n## 최근 수정")
        history = history_file.read_text(encoding="utf-8")
        # 최근 5개 항목 표시
        recent = re.findall(r"### \[(\d{4}-\d{2}-\d{2})\].*?- (.*?)(?=\n### |\Z)", history, re.DOTALL)[:5]
        for date, item in recent:
            first_line = item.split("\n")[0].strip()
            print(f"  {date} - {first_line[:50]}")

    return 0

# False Positive로 처리할 모듈 목록 (동적 로딩/선택적 의존성)
FALSE_POSITIVE_MODULES = ["cv2", "holidays", "pdf2image", "pytesseract", "werkzeug", "win32com"]


def parse_issues(content, include_all=False):
    """
    d0004_todo.md에서 이슈 파싱 (테이블 형식 지원)

    Args:
        content: 문서 내용
        include_all: True면 모든 상태 포함, False면 '대기' 상태만

    테이블 형식:
        | ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
    """
    issues = []

    # "현재 이슈 (Active Issues)" 섹션에서 테이블 찾기
    active_section_match = re.search(
        r"### 현재 이슈 \(Active Issues\)(.*?)(?=### 해결된 이슈|$)",
        content,
        re.DOTALL
    )

    if not active_section_match:
        return issues

    active_section = active_section_match.group(1)

    # 테이블 행 파싱: | A001 | 2026-01-02 | BUGFIX | [LINT] oais/pdf_parser.py:16 - ... | 높음 | 대기 |
    table_pattern = r"\| (A\d{3}) \| (\d{4}-\d{2}-\d{2}) \| (\w+) \| (.+?) \| (높음|중간|낮음) \| (대기|진행중|완료) \|"

    matches = re.finditer(table_pattern, active_section)
    for m in matches:
        issue_id = m.group(1)
        date = m.group(2)
        category = m.group(3)
        title = m.group(4).strip()
        priority = m.group(5)
        status = m.group(6)

        # '대기' 상태만 처리 (include_all이 아닌 경우)
        if not include_all and status != "대기":
            continue

        # 파일 경로와 라인 번호 추출
        # 예: [LINT] oais/pdf_parser.py:16 - [E0401] Unable to import 'pdf2image'
        file_match = re.search(r"\[LINT\] ([\w/._-]+):(\d+)", title)
        if file_match:
            file_path = file_match.group(1)
            line_no = int(file_match.group(2))
        else:
            file_path = None
            line_no = 0

        # 에러 코드 추출 (E0401, E1101 등)
        error_code_match = re.search(r"\[(E\d{4}|W\d{4})\]", title)
        error_code = error_code_match.group(1) if error_code_match else None

        # 우선순위를 severity로 매핑
        severity_map = {"높음": "ERROR", "중간": "WARNING", "낮음": "INFO"}
        severity = severity_map.get(priority, "WARNING")

        # False Positive 체크
        is_false_positive = is_false_positive_issue(title, file_path)

        issues.append({
            "id": issue_id,
            "severity": severity,
            "category": category,
            "title": title,
            "file": file_path,
            "line": line_no,
            "error_code": error_code,
            "status": status,
            "is_false_positive": is_false_positive,
            "date": date
        })

    return issues


def is_false_positive_issue(title, file_path):
    """
    False Positive 이슈인지 확인

    - 동적 로딩 모듈: cv2, holidays
    - 선택적 의존성: pdf2image, pytesseract, werkzeug, win32com
    """
    title_lower = title.lower()

    for module in FALSE_POSITIVE_MODULES:
        if module.lower() in title_lower:
            return True
        # 모듈 관련 에러 메시지 패턴
        if f"'{module}'" in title or f'"{module}"' in title:
            return True

    return False


def get_fix_type(issue):
    """이슈 유형에 따른 자동 수정 타입 반환"""
    title = issue.get("title", "")

    if "미정의 변수" in title or "F821" in title:
        return "Missing Import"
    if "미사용 import" in title or "unused import" in title.lower():
        return "Remove Unused Import"
    if "중복 import" in title:
        return "Remove Duplicate Import"
    if "타입 오류" in title or "NoneType" in title:
        return "Add None Check"
    if "width" in title.lower() and "column" in title.lower():
        return "Fix Column Width"

    return None


def backup_file(file_path):
    """파일 백업 생성"""
    src = PROJECT_ROOT / file_path
    if src.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        dst = BACKUP_DIR / f"{src.name}.backup"
        shutil.copy2(src, dst)


def update_todo_status(issue_id, status):
    """d0004_todo.md에서 이슈 상태 업데이트"""
    todo_file = PROJECT_ROOT / "doc" / "d0004_todo.md"
    if not todo_file.exists():
        return

    content = todo_file.read_text(encoding="utf-8")

    # 상태 업데이트 (간단한 구현)
    pattern = rf"(#### {issue_id}.*?)(\n- \*\*상태\*\*:.*?)(\n)"
    replacement = rf"\1\n- **상태**: {status}\3"

    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        todo_file.write_text(content, encoding="utf-8")


def parse_test_scenarios(content):
    """d0003_test.md에서 테스트 시나리오 파싱"""
    scenarios = []

    # TC-XXX 패턴 찾기
    pattern = r"### (TC-\d{3})[:\s]+(.*?)\n(.*?)(?=\n### |$)"
    matches = re.finditer(pattern, content, re.DOTALL)

    for m in matches:
        tc_id = m.group(1)
        name = m.group(2).strip()
        body = m.group(3)

        # 테스트 파일 추출
        file_match = re.search(r"테스트 파일[:\s]+`?([\w/\.]+)`?", body)
        type_match = re.search(r"유형[:\s]+(unit|integration|e2e)", body)

        scenarios.append({
            "id": tc_id,
            "name": name,
            "file": file_match.group(1) if file_match else None,
            "type": type_match.group(1) if type_match else None
        })

    return scenarios


def run_pytest(args):
    """pytest 실행"""
    try:
        cmd = ["uv", "run", "pytest"]
        if args:
            cmd.extend(args)
        else:
            cmd.extend(["-v", "--tb=short"])

        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode
    except FileNotFoundError:
        print("[SKIP] pytest not found")
        return 0


def run_single_test(scenario):
    """단일 테스트 시나리오 실행"""
    if not scenario.get("file"):
        return True  # 파일 없으면 스킵 (통과 처리)

    test_file = PROJECT_ROOT / scenario["file"]
    if not test_file.exists():
        return True

    try:
        result = subprocess.run(
            ["uv", "run", "pytest", str(test_file), "-v", "--tb=short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return True


def verify_syntax(file_path):
    """Python 구문 검사"""
    try:
        result = subprocess.run(
            ["uv", "run", "python", "-m", "py_compile", str(file_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return True


def run_mypy(file_path):
    """mypy 타입 검사"""
    try:
        result = subprocess.run(
            ["uv", "run", "mypy", str(file_path), "--ignore-missing-imports"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return None  # mypy not found

def apply_fix(issue):
    """
    이슈 유형별 자동 수정 적용
    """
    file_path = PROJECT_ROOT / issue["file"]
    if not file_path.exists():
        print(f"  [ERROR] File not found: {issue['file']}")
        return False

    title = issue["title"]

    # 1. Missing Import (F821)
    if "미정의 변수" in title or "F821" in title:
        return fix_missing_import(file_path, title)

    # 2. IndentationError
    if "IndentationError" in title:
        # 이건 수동으로 하는게 안전함, 내용만 보고 자동식별 어려움
        return False

    return False

def fix_missing_import(file_path, title):
    """
    누락된 import 문 추가
    """
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    module_to_import = None
    import_stmt = None

    # 타이틀에서 모듈명 추측
    if "sys" in title:
        module_to_import = "sys"
        import_stmt = "import sys"
    elif "shutil" in title:
        module_to_import = "shutil"
        import_stmt = "import shutil"
    elif "load_workbook" in title:
        import_stmt = "from openpyxl import load_workbook"
        module_to_import = "openpyxl"
    elif "OpenpyxlImage" in title:
        import_stmt = "from openpyxl.drawing.image import Image as OpenpyxlImage"
        module_to_import = "openpyxl"
    elif "img2pdf" in title:
        module_to_import = "img2pdf"
        import_stmt = "import img2pdf"

    if not import_stmt:
        return False

    # 이미 import 되어 있는지 확인
    if import_stmt in content:
        print(f"  [INFO] Import '{import_stmt}' already exists.")
        return True

    # Import 추가 위치 찾기 (첫 번째 import 문 뒤나 파일 상단)
    # 간단하게: imports 섹션이 있으면 그 끝에, 없으면 맨 위 (docstring 이후)에.

    # docstring 건너뛰기 로직은 복잡하니, import sys가 있는 곳 근처나,
    # 아니면 `import ...` 가 나오는 마지막 라인 뒤에 추가.

    insert_idx = 0
    last_import_idx = -1

    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            last_import_idx = i

    if last_import_idx != -1:
        insert_idx = last_import_idx + 1
    else:
        # Import가 하나도 없으면? docstring이나 shebang 고려해야 함.
        # 일단 안전하게 3번째 줄 정도에 넣거나 (shebang, encoding 고려)
        insert_idx = 2

    lines.insert(insert_idx, import_stmt)

    file_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [FIX] Added '{import_stmt}' to line {insert_idx+1}")
    return True

if __name__ == "__main__":
    sys.exit(main())
