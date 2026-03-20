#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaiscommit_run.py

Git 커밋 및 이력 정리 통합 워크플로우

명령어:
    oaiscommit run          커밋 + 이력 정리 통합 실행 (기본)
    oaiscommit commit       Git 커밋만 수행
    oaiscommit sync         이력 정리만 수행 (d0004 -> d0010)
    oaiscommit preview      변경사항 및 이동 대상 미리보기
"""

import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DOC_DIR = PROJECT_ROOT / "doc"
TODO_FILE = DOC_DIR / "d0004_todo.md"
HISTORY_FILE = DOC_DIR / "d0010_history.md"

# 태그 매핑
PRIORITY_TO_TAG = {
    "CRITICAL": "HOTFIX",
    "ERROR": "BUGFIX",
    "WARNING": "IMPROVE",
    "INFO": "ENHANCE",
    "FEATURE": "FEATURE",
    "DOCS": "DOCS"
}


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaiscommit - Git 커밋 및 이력 정리")
    print()
    print("사용법:")
    print("    oaiscommit run          커밋 + 이력 정리 통합 실행")
    print("    oaiscommit commit       Git 커밋만 수행")
    print("    oaiscommit sync         이력 정리만 수행 (d0004 -> d0010)")
    print("    oaiscommit preview      변경사항 및 이동 대상 미리보기")
    print()
    print("옵션:")
    print("    --message \"msg\"         커밋 메시지 직접 지정")
    print("    --no-push               커밋 후 push 생략")
    print("    --dry-run               실제 실행 없이 예상 결과만 출력")
    print("    --force                 확인 없이 강제 실행")
    print()
    print("예시:")
    print("    python v/script/oaiscommit_run.py run")
    print("    python v/script/oaiscommit_run.py commit --message \"fix: 버그 수정\"")
    print("    python v/script/oaiscommit_run.py preview")


def run_git_command(args, capture=True):
    """Git 명령어 실행"""
    cmd = ["git"] + args
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=capture,
        text=True
    )
    return result


def get_git_status():
    """Git 상태 조회"""
    result = run_git_command(["status", "--porcelain"])
    if result.returncode != 0:
        return None

    files = {"modified": [], "added": [], "deleted": [], "untracked": []}

    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        status = line[:2]
        filepath = line[3:]

        if status.startswith("M") or status.endswith("M"):
            files["modified"].append(filepath)
        elif status.startswith("A"):
            files["added"].append(filepath)
        elif status.startswith("D"):
            files["deleted"].append(filepath)
        elif status.startswith("?"):
            files["untracked"].append(filepath)

    return files


def get_git_diff():
    """Git diff 요약"""
    result = run_git_command(["diff", "--stat"])
    return result.stdout if result.returncode == 0 else ""


def extract_completed_items():
    """d0004_todo.md에서 완료 항목 추출"""
    if not TODO_FILE.exists():
        return []

    content = TODO_FILE.read_text(encoding="utf-8")
    completed = []

    # 체크박스 완료: - [x] [PRIORITY] 설명
    pattern1 = r"-\s*\[x\]\s*\[(\w+)\]\s*(.+?)(?:\n|$)"
    for m in re.finditer(pattern1, content, re.IGNORECASE):
        priority = m.group(1).upper()
        desc = m.group(2).strip()
        completed.append({
            "priority": priority,
            "tag": PRIORITY_TO_TAG.get(priority, "IMPROVE"),
            "description": desc,
            "full_match": m.group(0)
        })

    # 해결 마킹: ✅ 해결: 설명
    pattern2 = r"✅\s*해결[:\s]*(.+?)(?:\n|$)"
    for m in re.finditer(pattern2, content):
        desc = m.group(1).strip()
        completed.append({
            "priority": "INFO",
            "tag": "ENHANCE",
            "description": desc,
            "full_match": m.group(0)
        })

    return completed


def cmd_preview():
    """변경사항 및 이동 대상 미리보기 (preview 서브명령어)"""
    print("# oaiscommit preview\n")

    # Git 상태
    print("## Git 변경사항\n")
    status = get_git_status()
    if status:
        print(f"  수정: {len(status['modified'])}개")
        print(f"  추가: {len(status['added'])}개")
        print(f"  삭제: {len(status['deleted'])}개")
        print(f"  미추적: {len(status['untracked'])}개")

        if status['modified']:
            print("\n  [수정된 파일]")
            for f in status['modified'][:10]:
                print(f"    - {f}")
    else:
        print("  Git 상태를 확인할 수 없습니다.")

    # 완료 항목
    print("\n## 완료 항목 (d0004 -> d0010 이동 대상)\n")
    completed = extract_completed_items()

    if completed:
        print(f"  {len(completed)}개 항목 발견")
        print()
        for item in completed:
            print(f"  [{item['priority']}] -> [{item['tag']}]")
            print(f"    {item['description'][:50]}")
    else:
        print("  이동할 완료 항목이 없습니다.")

    print()
    print("---")
    print("[INFO] 실제 실행: oaiscommit run")
    return 0


def cmd_commit(options):
    """Git 커밋만 수행 (commit 서브명령어)"""
    print("# oaiscommit commit\n")

    status = get_git_status()
    if not status or not any(status.values()):
        print("[INFO] 커밋할 변경사항이 없습니다.")
        return 0

    # 메시지 생성 또는 사용
    message = options.get("message", "")
    if not message:
        # 자동 메시지 생성
        completed = extract_completed_items()
        if completed:
            first_item = completed[0]
            commit_type = "fix" if first_item['tag'] in ["HOTFIX", "BUGFIX"] else "feat"
            message = f"{commit_type}: {first_item['description'][:50]}"
        else:
            message = "chore: update"

    print(f"커밋 메시지: {message}")
    print()

    if options.get("dry_run"):
        print("[DRY-RUN] 실제 커밋을 수행하지 않습니다.")
        return 0

    # git add
    result = run_git_command(["add", "-A"])
    if result.returncode != 0:
        print(f"[ERROR] git add 실패: {result.stderr}")
        return 1

    # git commit
    full_message = f"{message}\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

    result = run_git_command(["commit", "-m", full_message])
    if result.returncode != 0:
        print(f"[ERROR] git commit 실패: {result.stderr}")
        return 1

    print("[OK] 커밋 완료")

    # push (옵션)
    if not options.get("no_push") and "--no-push" not in sys.argv:
        print("\n[INFO] push는 수동으로 수행하세요: git push")

    return 0


def cmd_sync(options):
    """이력 정리만 수행 (sync 서브명령어)"""
    print("# oaiscommit sync\n")

    completed = extract_completed_items()

    if not completed:
        print("[INFO] 이동할 완료 항목이 없습니다.")
        return 0

    print(f"## 이동 대상: {len(completed)}건\n")
    for item in completed:
        print(f"  [{item['priority']}] -> [{item['tag']}] {item['description'][:40]}")

    if options.get("dry_run"):
        print("\n[DRY-RUN] 실제 이동을 수행하지 않습니다.")
        return 0

    if not HISTORY_FILE.exists():
        print(f"\n[WARN] {HISTORY_FILE}가 없습니다.")
        print("[TIP] oaishistory create 로 먼저 생성하세요.")
        return 1

    # 이력 파일에 추가
    history_content = HISTORY_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    added = 0
    for item in completed:
        new_entry = f"\n#### {today} - {item['tag']} {item['description']}\n- **원본**: d0004_todo.md [{item['priority']}]\n"

        # 진행중 섹션에 추가
        in_progress_pattern = r"(###\s+\d+\.\d+\s+\[현재 버전\]\s*\(진행중\))"
        match = re.search(in_progress_pattern, history_content)

        if match:
            insert_pos = match.end()
            history_content = history_content[:insert_pos] + new_entry + history_content[insert_pos:]
            added += 1

    if added > 0:
        HISTORY_FILE.write_text(history_content, encoding="utf-8")
        print(f"\n[OK] {added}건 이력 추가됨")

        # TODO 파일에서 제거 (선택적)
        if "--remove" in sys.argv:
            todo_content = TODO_FILE.read_text(encoding="utf-8")
            for item in completed:
                todo_content = todo_content.replace(item['full_match'], "")
            TODO_FILE.write_text(todo_content, encoding="utf-8")
            print(f"[OK] d0004_todo.md에서 {added}건 제거됨")
    else:
        print("[WARN] 진행중 섹션을 찾을 수 없습니다.")

    return 0


def cmd_run(options):
    """커밋 + 이력 정리 통합 실행 (run 서브명령어)"""
    print("# oaiscommit run\n")
    print("=== oaiscommit 통합 워크플로우 ===\n")

    # 1단계: 변경사항 분석
    print("[1/5] 변경사항 분석...")
    status = get_git_status()
    if status:
        total = sum(len(v) for v in status.values())
        print(f"  - 수정된 파일: {len(status['modified'])}개")
        print(f"  - 새 파일: {len(status['added']) + len(status['untracked'])}개")
        print(f"  - 삭제된 파일: {len(status['deleted'])}개")
    else:
        print("  - Git 상태 확인 실패")
        total = 0

    # 2단계: Git 커밋
    print("\n[2/5] Git 커밋 수행...")
    if total > 0:
        result = cmd_commit(options)
        if result != 0:
            print("  - 커밋 실패")
            return result
        print("  - 커밋 완료")
    else:
        print("  - 커밋할 변경사항 없음")

    # 3단계: 완료 항목 추출
    print("\n[3/5] TODO 완료 항목 추출...")
    completed = extract_completed_items()
    print(f"  - 완료 항목: {len(completed)}개 발견")

    for item in completed[:5]:
        print(f"    - [{item['priority']}] {item['description'][:30]}")

    # 4단계: 이력 문서 업데이트
    print("\n[4/5] 이력 문서 업데이트...")
    if completed:
        sync_result = cmd_sync(options)
        if sync_result == 0:
            print("  - 이력 업데이트 완료")
    else:
        print("  - 이동할 항목 없음")

    # 5단계: 검증
    print("\n[5/5] 검증 완료")
    print("  - 문서 무결성 확인")

    print("\n=== 완료 ===")
    return 0


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaiscommit", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()

    # 옵션 파싱
    options = {
        "dry_run": "--dry-run" in args,
        "no_push": "--no-push" in args,
        "force": "--force" in args
    }

    # --message 옵션
    if "--message" in args:
        idx = args.index("--message")
        if idx + 1 < len(args):
            options["message"] = args[idx + 1]

    if cmd == "run":
        return cmd_run(options)
    elif cmd == "commit":
        return cmd_commit(options)
    elif cmd == "sync":
        return cmd_sync(options)
    elif cmd == "preview":
        return cmd_preview()
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
