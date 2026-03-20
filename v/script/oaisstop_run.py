#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oaisstop_run.py - 세션 종료 워크플로우 (상세: doc/a0009_script.md)"""

import sys
import re
import subprocess
from datetime import datetime
from oais_common import (
    show_help_if_no_args, PROJECT_ROOT, DOC_DIR, TODO_FILE, HISTORY_FILE,
    log_ok, log_warn, log_info, log_tip
)

README_FILE = PROJECT_ROOT / "README.md"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaisstop - 세션 종료 워크플로우")
    print()
    print("사용법:")
    print("    oaisstop run        2단계 종료 워크플로우 실행 (기본)")
    print("    oaisstop readme     README.md 업데이트만 수행 (1단계)")
    print("    oaisstop sync       doc/*.md 동기화만 수행 (2단계)")
    print()
    print("옵션:")
    print("    --dry-run           실제 파일 수정 없이 미리보기")
    print("    --no-commit         자동 커밋 생략")
    print("    --message [msg]     작업 내역 메시지 지정")
    print()
    print("예시:")
    print("    python v/script/oaisstop_run.py run")
    print("    python v/script/oaisstop_run.py readme --message \"로그인 기능 구현\"")


def get_git_status():
    """Git 상태 조회"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            return [l for l in lines if l]
        return []
    except Exception:
        return []


def get_recent_commits(count=3):
    """최근 커밋 조회"""
    try:
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
        return []
    except Exception:
        return []


def cmd_readme(options):
    """README.md 업데이트 (readme 서브명령어)"""
    dry_run = options.get("dry_run", False)
    print("# oaisstop readme\n")
    if dry_run:
        print("[DRY-RUN] 실제 파일 수정 없이 미리보기만 실행\n")
    print("=== 1단계: README.md 업데이트 ===\n")

    today = datetime.now().strftime("%Y-%m-%d")
    message = options.get("message", "(작업 내역)")

    # 변경된 파일 확인
    changed_files = get_git_status()
    print(f"변경된 파일: {len(changed_files)}개")

    if changed_files:
        for f in changed_files[:5]:
            print(f"  - {f}")
        if len(changed_files) > 5:
            print(f"  ... 외 {len(changed_files) - 5}개")

    # README.md 업데이트 섹션 생성
    update_section = f"""
## 최근 작업 내역

- **날짜**: {today}
- **작업 내용**: {message}
- **변경된 파일**: {len(changed_files)}개
- **다음 작업**: (권장 후속 작업)

"""

    print()
    print("## 업데이트 내용 미리보기\n")
    print(update_section)

    if README_FILE.exists():
        content = README_FILE.read_text(encoding="utf-8")

        # 기존 최근 작업 내역 섹션이 있으면 교체
        pattern = r"## 최근 작업 내역\n[\s\S]*?(?=\n## |\Z)"
        if re.search(pattern, content):
            content = re.sub(pattern, update_section.strip() + "\n\n", content)
            action = "기존 섹션 업데이트"
        else:
            # 없으면 맨 아래 추가
            content = content.rstrip() + "\n\n" + update_section
            action = "신규 섹션 추가"

        if dry_run:
            print(f"[DRY-RUN] {action} 예정: {README_FILE}")
        else:
            README_FILE.write_text(content, encoding="utf-8")
            print(f"[OK] {action}")
    else:
        print("[WARN] README.md가 없습니다.")
        print("[INFO] 수동으로 생성이 필요합니다.")

    return 0


def cmd_sync(options):
    """doc/*.md 동기화 (sync 서브명령어)"""
    print("# oaisstop sync\n")
    print("=== 2단계: doc/*.md 동기화 ===\n")

    today = datetime.now().strftime("%Y-%m-%d")
    docs_to_check = [
        ("d0004_todo.md", "할 일 관리"),
        ("d0010_history.md", "변경 이력"),
        ("d0005_lib.md", "라이브러리 문서"),
        ("d0006_db.md", "DB 구조"),
        ("d0001_prd.md", "PRD")
    ]

    print("## 문서 동기화 상태\n")

    for doc_name, description in docs_to_check:
        doc_path = DOC_DIR / doc_name
        if doc_path.exists():
            stat = doc_path.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            age = (datetime.now() - mtime).days

            if age > 7:
                status = "[WARN] 7일 이상 미갱신"
            else:
                status = "[OK]"

            print(f"  {status} {doc_name}: {description}")
            print(f"      마지막 수정: {mtime.strftime('%Y-%m-%d')}")
        else:
            print(f"  [SKIP] {doc_name}: 파일 없음")

    # d0010_history.md 업데이트
    print()
    print("## 이력 문서 업데이트\n")

    if HISTORY_FILE.exists():
        content = HISTORY_FILE.read_text(encoding="utf-8")

        # 버전 히스토리 섹션에 오늘 항목 추가 확인
        if today not in content:
            print(f"  [INFO] {today} 이력이 없습니다.")
            print("  [TIP] oaishistory run 으로 이력을 추가하세요.")
        else:
            print(f"  [OK] {today} 이력 존재")
    else:
        print("  [WARN] d0010_history.md가 없습니다.")

    print()
    print("---")
    print("[INFO] 문서 동기화는 서브에이전트를 통해 수행됩니다.")
    print("[TIP] Task tool로 task-executor, Explore 에이전트를 활용하세요.")

    return 0


def cmd_run(options):
    """2단계 종료 워크플로우 실행 (run 서브명령어)"""
    dry_run = options.get("dry_run", False)
    print("# oaisstop run\n")
    if dry_run:
        print("[DRY-RUN] 실제 파일 수정 없이 미리보기만 실행\n")
    print("=== 세션 종료 워크플로우 ===\n")

    # 1단계: README.md 업데이트
    print("[1/3] README.md 업데이트...")
    cmd_readme(options)

    print()

    # 2단계: doc/*.md 동기화
    print("[2/3] doc/*.md 동기화...")
    cmd_sync(options)

    print()

    # 3단계: 체크리스트
    print("[3/3] 종료 체크리스트\n")

    checklist = [
        "미완료 태스크 -> d0004_todo.md 기록",
        "완료 태스크 -> 히스토리 이동",
        "변경 파일 -> 커밋 여부 확인",
        "문서 -> 버전 히스토리 갱신",
        "README.md -> 오늘/다음 작업 정리"
    ]

    for item in checklist:
        print(f"  [ ] {item}")

    print()
    print("---")
    print("[INFO] 세션 종료 워크플로우 가이드 출력 완료")
    print("[TIP] 실제 문서 업데이트는 서브에이전트를 활용하세요.")
    print()

    # 커밋 안내
    changed = get_git_status()
    if changed and not options.get("no_commit"):
        print("## 커밋 안내\n")
        print(f"  변경된 파일: {len(changed)}개")
        print("  권장 커밋 메시지:")
        print(f'    docs: 세션 종료 - {options.get("message", "작업 정리")}')

    return 0


def parse_options(args):
    """옵션 파싱"""
    options = {
        "no_commit": "--no-commit" in args,
        "dry_run": "--dry-run" in args,
        "message": None
    }

    # --message
    if "--message" in args:
        idx = args.index("--message")
        if idx + 1 < len(args):
            options["message"] = args[idx + 1]

    return options


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisstop", sys.argv[1:]):
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
    elif cmd == "readme":
        return cmd_readme(options)
    elif cmd == "sync":
        return cmd_sync(options)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
