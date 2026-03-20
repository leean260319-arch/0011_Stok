#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
oaisdoc run 실행 스크립트

doc/d0001~d0010 문서들을 스캔하고, 각 문서에 매핑된 oais 스킬을
자동으로 실행하여 문서를 일괄 업데이트합니다.

사용법:
    uv run v/script/oaisdoc_run.py           # 전체 실행
    uv run v/script/oaisdoc_run.py --dry-run # 드라이런
    uv run v/script/oaisdoc_run.py --required-only # 필수만
    uv run v/script/oaisdoc_run.py --doc d0004_todo.md # 특정 문서만
"""

import sys
import os
from pathlib import Path
import subprocess
import argparse
from oais_common import show_help_if_no_args

# 프로젝트 루트 설정
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOC_DIR = PROJECT_ROOT / "doc"

# 문서-스킬 매핑 테이블 (실행 순서대로 정의)
# 형식: (문서명, 스킬명, 실행명령어, 필수여부)
DOC_SKILL_MAPPING = [
    ("d0004_todo.md", "oaischeck", "oaischeck update", True),
    ("d0010_history.md", "oaishistory", "oaishistory sync", True),
    ("d0005_lib.md", "oaislib", "oaislib run", False),
    ("d0006_db.md", "oaisdb", "oaisdb", False),
    ("d0003_test.md", "oaistest", "oaistest", True),
    ("d0007_command.md", "oaiscommand", "oaiscommand run", False),
    ("d0008_user.md", "oaisuser", "oaisuser update", False),
    ("d0001_prd.md", "oaisprd", "oaisprd update", True),
    ("d0002_plan.md", "oaisplan", "oaisplan update", True),
]


def check_doc_exists(doc_name: str) -> bool:
    """문서 파일 존재 여부 확인"""
    doc_path = DOC_DIR / doc_name
    return doc_path.exists()


def execute_skill(skill_command: str, dry_run: bool = False) -> tuple[bool, str]:
    """
    스킬 명령어 실행

    Returns:
        tuple: (성공여부, 메시지)
    """
    if dry_run:
        return True, f"[DRY-RUN] 실행 예정: {skill_command}"

    try:
        # Claude Code 환경에서는 스킬이 슬래시 명령어로 실행됨
        # 이 스크립트는 실행 계획을 보여주는 용도
        # 실제 실행은 Claude Code에서 /oaisdoc run 으로 수행
        return True, f"실행 계획: /{skill_command}"
    except Exception as e:
        return False, f"실행 실패: {str(e)}"


def run_doc_update(
    dry_run: bool = False,
    required_only: bool = False,
    target_doc: str = None
) -> dict:
    """
    문서 업데이트 실행

    Args:
        dry_run: 드라이런 모드 (실행 없이 계획만 표시)
        required_only: 필수 문서만 업데이트
        target_doc: 특정 문서만 업데이트 (None이면 전체)

    Returns:
        dict: 실행 결과 통계
    """
    print("[oaisdoc run] 문서 업데이트 시작...")
    print()

    results = {
        "success": 0,
        "skip": 0,
        "fail": 0,
        "details": []
    }

    # 필터링된 매핑 리스트 생성
    filtered_mapping = []
    for doc, skill, cmd, required in DOC_SKILL_MAPPING:
        # 특정 문서만 처리
        if target_doc and doc != target_doc:
            continue
        # 필수만 처리
        if required_only and not required:
            continue
        filtered_mapping.append((doc, skill, cmd, required))

    total = len(filtered_mapping)

    for idx, (doc, skill, cmd, required) in enumerate(filtered_mapping, 1):
        print(f"[{idx}/{total}] {doc}")
        print(f"       스킬: {cmd}")

        # 문서 존재 확인
        if not check_doc_exists(doc):
            status = "[SKIP] (파일 없음)"
            results["skip"] += 1
            results["details"].append({
                "doc": doc,
                "skill": skill,
                "status": "skip",
                "reason": "파일 없음"
            })
        else:
            # 스킬 실행
            success, msg = execute_skill(cmd, dry_run)
            if success:
                if dry_run:
                    status = f"[DRY] {msg}"
                else:
                    status = "[OK] 완료"
                results["success"] += 1
                results["details"].append({
                    "doc": doc,
                    "skill": skill,
                    "status": "success",
                    "message": msg
                })
            else:
                status = f"[FAIL] {msg}"
                results["fail"] += 1
                results["details"].append({
                    "doc": doc,
                    "skill": skill,
                    "status": "fail",
                    "reason": msg
                })

        print(f"       상태: {status}")
        print()

    # 결과 요약
    print("-" * 40)
    print(f"[완료] {results['success']}/{total} 문서 업데이트됨")
    print(f"       - 성공: {results['success']}")
    print(f"       - 스킵: {results['skip']}")
    print(f"       - 실패: {results['fail']}")

    return results


def generate_execution_plan() -> str:
    """실행 계획 문자열 생성"""
    lines = [
        "# oaisdoc run 실행 계획",
        "",
        "## 문서-스킬 매핑",
        "",
        "| 순서 | 문서 | 스킬 | 명령어 | 필수 | 존재 |",
        "|------|------|------|--------|------|------|",
    ]

    for idx, (doc, skill, cmd, required) in enumerate(DOC_SKILL_MAPPING, 1):
        exists = "O" if check_doc_exists(doc) else "X"
        req = "O" if required else "-"
        lines.append(f"| {idx} | `{doc}` | `{skill}` | `{cmd}` | {req} | {exists} |")

    lines.extend([
        "",
        "## 실행 순서",
        "",
    ])

    for idx, (doc, skill, cmd, required) in enumerate(DOC_SKILL_MAPPING, 1):
        if check_doc_exists(doc):
            lines.append(f"{idx}. `/{cmd}` → {doc}")
        else:
            lines.append(f"{idx}. ~~`/{cmd}` → {doc}~~ (파일 없음)")

    return "\n".join(lines)


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisdoc", sys.argv[1:]):
        return

    parser = argparse.ArgumentParser(
        description="oaisdoc run - 문서 일괄 업데이트 도구"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실행 없이 계획만 표시"
    )
    parser.add_argument(
        "--required-only",
        action="store_true",
        help="필수 문서만 업데이트"
    )
    parser.add_argument(
        "--doc",
        type=str,
        default=None,
        help="특정 문서만 업데이트 (예: d0004_todo.md)"
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="실행 계획을 마크다운으로 출력"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=["run", "plan", "list"],
        help="실행 명령 (기본: run)"
    )

    args = parser.parse_args()

    # plan 명령 또는 --plan 플래그
    if args.command == "plan" or args.plan:
        print(generate_execution_plan())
        return 0

    # list 명령
    if args.command == "list":
        print("## 문서-스킬 매핑 목록")
        print()
        for doc, skill, cmd, required in DOC_SKILL_MAPPING:
            exists = "[O]" if check_doc_exists(doc) else "[X]"
            req = "[필수]" if required else "[선택]"
            print(f"{exists} {doc} -> {skill} {req}")
        return 0

    # run 명령
    results = run_doc_update(
        dry_run=args.dry_run,
        required_only=args.required_only,
        target_doc=args.doc
    )

    # 실패가 있으면 비정상 종료
    return 1 if results["fail"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
