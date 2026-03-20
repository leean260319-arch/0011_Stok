#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaistest_run.py

통합 테스트 실행 스크립트

명령어:
    oaistest run              전체 테스트 실행
    oaistest run [시나리오ID] 특정 시나리오 실행 (예: TC-001, UI-LOGIN-001)
    oaistest run [카테고리]   카테고리별 실행 (예: 로그인, API, E2E)
    oaistest run [우선순위]   우선순위별 실행 (P0, P1, P2, P3)
    oaistest preview          테스트 계획 출력 (실행 안함)
"""

import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from oais_common import show_help_if_no_args

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaistest - 통합 테스트 도구")
    print()
    print("사용법:")
    print("    oaistest run              전체 테스트 실행")
    print("    oaistest run [시나리오ID] 특정 시나리오 실행 (예: TC-001)")
    print("    oaistest run [카테고리]   카테고리별 실행 (예: 로그인, API)")
    print("    oaistest run [우선순위]   우선순위별 실행 (P0, P1, P2, P3)")
    print("    oaistest preview          테스트 계획 출력 (실행 안함)")
    print("    oaistest preview [필터]   필터링된 테스트 계획")
    print()
    print("옵션:")
    print("    --verbose                 상세 로그 출력")
    print("    --fail-fast               첫 실패 시 중단")
    print("    --screenshot              스크린샷 저장 (E2E)")
    print()
    print("예시:")
    print("    python v/script/oaistest_run.py run")
    print("    python v/script/oaistest_run.py run TC-001")
    print("    python v/script/oaistest_run.py run P0")
    print("    python v/script/oaistest_run.py preview")


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaistest", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    cmd_args = args[1:]

    # 옵션 파싱
    options = {
        "verbose": "--verbose" in cmd_args,
        "fail_fast": "--fail-fast" in cmd_args,
        "screenshot": "--screenshot" in cmd_args
    }
    # 옵션 제거
    cmd_args = [a for a in cmd_args if not a.startswith("--")]

    if cmd == "run":
        return cmd_run(cmd_args, options)
    elif cmd == "preview":
        return cmd_preview(cmd_args)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


def cmd_run(args, options):
    """테스트 실행 (run 서브명령어)"""
    print("# oaistest run\n")

    # 테스트 문서에서 시나리오 로드
    test_file = PROJECT_ROOT / "doc" / "d0003_test.md"
    scenarios = []

    if test_file.exists():
        content = test_file.read_text(encoding="utf-8")
        scenarios = parse_test_scenarios(content)

    target = args[0] if args else None

    if target:
        filtered = filter_scenarios(scenarios, target)
        if filtered:
            return run_scenarios(filtered, options)
        else:
            print(f"[INFO] No matching scenarios for: {target}")
            print("[INFO] Falling back to pytest...")

    # pytest 실행
    return run_pytest(args, options)


def cmd_preview(args):
    """테스트 계획 출력 (preview 서브명령어)"""
    print("# oaistest preview\n")

    test_file = PROJECT_ROOT / "doc" / "d0003_test.md"

    if not test_file.exists():
        print("[WARN] d0003_test.md not found.")
        print("[INFO] Available: pytest tests/")
        return 0

    content = test_file.read_text(encoding="utf-8")
    scenarios = parse_test_scenarios(content)

    target = args[0] if args else None
    if target:
        scenarios = filter_scenarios(scenarios, target)

    if not scenarios:
        print("[INFO] No test scenarios found.")
        return 0

    # 카테고리별 그룹화
    by_category = defaultdict(list)
    for sc in scenarios:
        cat = sc.get("category", "기타")
        by_category[cat].append(sc)

    print("## 테스트 계획\n")

    # 우선순위별 집계
    priority_counts = defaultdict(int)
    for sc in scenarios:
        priority_counts[sc.get("priority", "P3")] += 1

    print("### 우선순위별 현황")
    for p in ["P0", "P1", "P2", "P3"]:
        count = priority_counts.get(p, 0)
        if count > 0:
            print(f"  {p}: {count}개")
    print()

    # 카테고리별 상세
    print("### 카테고리별 시나리오")
    for cat, items in sorted(by_category.items()):
        print(f"\n#### {cat} ({len(items)}개)")
        for sc in items:
            status_icon = get_status_icon(sc.get("status", "pending"))
            print(f"  {status_icon} {sc['id']}: {sc['name']}")
            if sc.get("priority"):
                print(f"      우선순위: {sc['priority']}")

    print(f"\n---\n총 {len(scenarios)}개 시나리오")
    return 0


def parse_test_scenarios(content):
    """d0003_test.md에서 테스트 시나리오 파싱"""
    scenarios = []

    # 패턴 1: TC-XXX 또는 UI-XXX-001 형식
    pattern = r"###\s+(TC-\d+|[A-Z]+-[A-Z]+-\d+)[:\s]+(.*?)\n(.*?)(?=\n### |\Z)"

    matches = re.finditer(pattern, content, re.DOTALL)
    for m in matches:
        sc_id = m.group(1)
        name = m.group(2).strip()
        body = m.group(3)

        # 카테고리 추출 (ID에서)
        parts = sc_id.split("-")
        if len(parts) >= 2:
            category = parts[0]
        else:
            category = "기타"

        # 우선순위 추출
        priority_match = re.search(r"\*\*우선순위\*\*:\s*(P[0-3])", body)
        priority = priority_match.group(1) if priority_match else "P2"

        # 상태 추출
        status_match = re.search(r"\*\*상태\*\*:\s*(\[.\])\s*(\w+)", body)
        if status_match:
            status = status_match.group(2).lower()
        else:
            # 체크박스로 상태 확인
            if "[x]" in body[:100]:
                status = "pass"
            elif "[!]" in body[:100]:
                status = "fail"
            else:
                status = "pending"

        # 테스트 유형 추출
        type_match = re.search(r"\*\*테스트 유형\*\*:\s*(\w+)", body)
        test_type = type_match.group(1) if type_match else "unit"

        scenarios.append({
            "id": sc_id,
            "name": name,
            "category": category,
            "priority": priority,
            "status": status,
            "type": test_type,
            "body": body
        })

    # 패턴 2: 체크리스트 형식 - [ ] 또는 [x] 패턴
    checklist_pattern = r"- \[([ x!~-])\]\s+(.*?)(?:\n|$)"
    for m in re.finditer(checklist_pattern, content):
        check = m.group(1)
        item = m.group(2).strip()

        # 이미 파싱된 시나리오와 중복 방지
        if any(item in sc["name"] for sc in scenarios):
            continue

        status = {
            " ": "pending",
            "x": "pass",
            "!": "fail",
            "~": "in_progress",
            "-": "skip"
        }.get(check, "pending")

        # ID 생성
        sc_id = f"CL-{len(scenarios)+1:03d}"

        scenarios.append({
            "id": sc_id,
            "name": item[:50],
            "category": "체크리스트",
            "priority": "P2",
            "status": status,
            "type": "checklist",
            "body": ""
        })

    return scenarios


def filter_scenarios(scenarios, target):
    """시나리오 필터링"""
    target_upper = target.upper()

    # 시나리오 ID로 필터
    if target_upper.startswith("TC-") or "-" in target_upper:
        return [s for s in scenarios if target_upper in s["id"].upper()]

    # 우선순위로 필터
    if target_upper in ["P0", "P1", "P2", "P3"]:
        return [s for s in scenarios if s.get("priority") == target_upper]

    # 카테고리/키워드로 필터
    return [s for s in scenarios
            if target.lower() in s.get("category", "").lower()
            or target.lower() in s.get("name", "").lower()]


def run_scenarios(scenarios, options):
    """시나리오 기반 테스트 실행"""
    print(f"## 테스트 시나리오 실행: {len(scenarios)}개\n")

    passed = 0
    failed = 0
    skipped = 0

    for sc in scenarios:
        print(f"### {sc['id']}: {sc['name']}")

        # 이미 통과/실패된 시나리오는 상태만 표시
        if sc["status"] == "pass":
            print("    -> [PASS] (이전 실행)")
            passed += 1
            continue
        elif sc["status"] == "skip":
            print("    -> [SKIP]")
            skipped += 1
            continue

        # 실제 테스트 실행 (여기서는 시뮬레이션)
        if sc["type"] == "checklist":
            print("    -> [INFO] 수동 확인 필요")
            skipped += 1
        else:
            # pytest 파일이 있으면 실행
            test_path = find_test_file(sc)
            if test_path:
                result = run_single_pytest(test_path, options)
                if result == 0:
                    print("    -> [PASS]")
                    passed += 1
                else:
                    print("    -> [FAIL]")
                    failed += 1
                    if options.get("fail_fast"):
                        print("\n[FAIL-FAST] 중단됨")
                        break
            else:
                print("    -> [SKIP] 테스트 파일 없음")
                skipped += 1

        print()

    print(f"---\n## 결과 요약")
    print(f"  통과: {passed}")
    print(f"  실패: {failed}")
    print(f"  스킵: {skipped}")

    total = passed + failed
    if total > 0:
        print(f"  성공률: {100*passed/total:.1f}%")

    return 0 if failed == 0 else 1


def find_test_file(scenario):
    """시나리오에 해당하는 테스트 파일 찾기"""
    tests_dir = PROJECT_ROOT / "tests"
    if not tests_dir.exists():
        return None

    # 시나리오 ID 기반 검색
    sc_id = scenario["id"].lower().replace("-", "_")
    for test_file in tests_dir.rglob("test_*.py"):
        if sc_id in test_file.stem.lower():
            return test_file

    return None


def run_single_pytest(test_path, options):
    """단일 테스트 파일 실행"""
    cmd = ["uv", "run", "pytest", str(test_path)]

    if options.get("verbose"):
        cmd.append("-v")
    if options.get("fail_fast"):
        cmd.append("-x")

    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.returncode
    except FileNotFoundError:
        return 1


def run_pytest(args, options):
    """pytest 실행"""
    print("## pytest 실행\n")

    cmd = ["uv", "run", "pytest"]

    # 대상 추가
    if args:
        target = args[0]
        # 경로 지정
        if "/" in target or "\\" in target:
            cmd.append(target)
        else:
            cmd.extend(["tests", "-k", target])
    else:
        cmd.append("tests")

    # 옵션 추가
    if options.get("verbose"):
        cmd.append("-v")
    if options.get("fail_fast"):
        cmd.append("-x")

    cmd.append("--tb=short")

    print(f"실행: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=False,
            text=True
        )
        return result.returncode
    except FileNotFoundError:
        print("[ERROR] pytest not found")
        return 1


def get_status_icon(status):
    """상태에 따른 아이콘 반환"""
    icons = {
        "pass": "[x]",
        "fail": "[!]",
        "skip": "[-]",
        "in_progress": "[~]",
        "pending": "[ ]"
    }
    return icons.get(status.lower(), "[ ]")


if __name__ == "__main__":
    sys.exit(main())
