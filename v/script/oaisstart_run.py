#!/usr/bin/env python3
"""
oaisstart_run.py

This script implements the session start workflow as defined in v/oaisstart.md.
It checks the status of key documentation files and prints a checklist for the user.
"""

import sys
import datetime
from pathlib import Path
from oais_common import show_help_if_no_args

# Configuration
DOC_DIR = Path("doc")
GUIDE_DIR = Path("v/guide")
COMMON_GUIDE = "common_guide.md"
DOCS_TO_CHECK = [
    "d0001_prd.md",
    "d0004_todo.md",
    "d0010_history.md"
]

def check_file_status(file_path):
    """
    Checks if a file exists and returns its last modified time.
    """
    if not file_path.exists():
        return "Not Found", None

    mtime = file_path.stat().st_mtime
    dt = datetime.datetime.fromtimestamp(mtime)
    return "Exists", dt.strftime("%Y-%m-%d %H:%M:%S")

def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisstart", sys.argv[1:]):
        return

    print("# oaisstart Session Start Workflow\n")
    print(f"Current Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("## 0. Common Guide Load (Required)\n")
    guide_path = GUIDE_DIR / COMMON_GUIDE
    status, mtime = check_file_status(guide_path)
    if status == "Exists":
        print(f"[OK] {guide_path} - Last Modified: {mtime}")
        print(f"     -> Read this file first for project standards\n")
    else:
        print(f"[WARNING] {guide_path} - Not Found")
        print(f"     -> Create common_guide.md for project standards\n")

    print("## 1. Document Status Check\n")
    print("| Document | Status | Last Modified |")
    print("|----------|--------|---------------|")

    for doc_name in DOCS_TO_CHECK:
        file_path = DOC_DIR / doc_name
        status, mtime = check_file_status(file_path)
        print(f"| {doc_name} | {status} | {mtime if mtime else '-'} |")
    print("\n")

    print("## 2. Sync Checklist (Action Required)\n")
    print("### d0001_prd.md (Requirements)")
    print("- [ ] Check for new requirements")
    print("- [ ] Check for modified features")
    print("- [ ] Check for deleted features\n")

    print("### d0004_todo.md (Tasks & Issues)")
    print("- [ ] Check completed tasks")
    print("- [ ] Register new issues")
    print("- [ ] Update progress status\n")

    print("### d0010_history.md (History)")
    print("- [ ] Add recent change history")
    print("- [ ] Update version information\n")

    print("## 3. oaischeck Preparation\n")
    print("- [ ] Run `oaischeck run` to verify code quality")
    print("  - [ ] Check for CRITICAL issues (Must fix immediately)")
    print("  - [ ] Check for ERROR issues (Fix in this session)")
    print("- [ ] Run `oaischeck update` to organize documents\n")

    print("## 4. Session Ready Report Template\n")
    print("Copy and fill this section when ready:\n")
    print("```markdown")
    print("## 세션 준비 완료")
    print("")
    print("### 문서 동기화")
    print("- d0001_prd.md: [변경없음/업데이트됨]")
    print("- d0004_todo.md: [변경없음/업데이트됨]")
    print("- d0010_history.md: [변경없음/업데이트됨]")
    print("")
    print("### oaischeck 결과")
    print("- CRITICAL: 0건")
    print("- ERROR: X건")
    print("- WARNING: Y건")
    print("- INFO: Z건")
    print("")
    print("### 다음 작업")
    print("- [ ] 우선 처리할 이슈")
    print("- [ ] 예정된 기능 구현")
    print("```")

if __name__ == "__main__":
    main()
