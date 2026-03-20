#!/usr/bin/env python3
"""oaissync_run.py - Vibe 환경 동기화 (상세: doc/a0009_script.md)"""

import os
import sys
import shutil
import filecmp
from datetime import datetime
from pathlib import Path
from oais_common import (
    show_help_if_no_args, log_ok, log_warn, log_info, log_error, log_dry_run
)

# ============================================================
# Configuration
# ============================================================

CURRENT_PROJECT = Path.cwd()
PARENT_DIR = CURRENT_PROJECT.parent
TEMPLATE_DIR = CURRENT_PROJECT / "v" / "template"

# 동기화 대상 파일/폴더
SYNC_TARGETS = [
    "v/",
    ".claude/",
    "CLAUDE.md",
    "run_claude.bat",
    "run_claude.sh",
]

# 동기화 제외 패턴
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".git",
    "tmp",
    ".venv",
    "node_modules",
    "v/0_claude미사용",
    ".claude/settings.local.json",  # 프로젝트별 로컬 설정
    ".claude\\settings.local.json",  # Windows 경로
    "settings.local.json",  # 파일명 직접 매칭
]

# Vibe 환경 판별 기준
VIBE_INDICATORS = {
    "claude_dir": ".claude",
    "v_dir": "v",
}


# ============================================================
# Helper Functions
# ============================================================

def is_excluded(path: Path) -> bool:
    """Check if path should be excluded from sync."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if path_str.endswith(pattern[1:]):
                return True
        elif pattern in path_str:
            return True
    return False


def get_file_mtime(file_path: Path) -> datetime | None:
    """Get file modification time."""
    if file_path.exists():
        return datetime.fromtimestamp(file_path.stat().st_mtime)
    return None


def compare_files(source: Path, target: Path) -> str:
    """
    Compare two files and return status.

    Returns:
        ONLY_SOURCE: Only exists in source
        ONLY_TARGET: Only exists in target
        NEWER_SOURCE: Source is newer
        NEWER_TARGET: Target is newer
        SAME: Files are identical
    """
    source_exists = source.exists()
    target_exists = target.exists()

    if source_exists and not target_exists:
        return "ONLY_SOURCE"
    elif not source_exists and target_exists:
        return "ONLY_TARGET"
    elif source_exists and target_exists:
        if source.is_file() and target.is_file():
            if filecmp.cmp(source, target, shallow=False):
                return "SAME"
            source_mtime = get_file_mtime(source)
            target_mtime = get_file_mtime(target)
            if source_mtime and target_mtime:
                if source_mtime > target_mtime:
                    return "NEWER_SOURCE"
                else:
                    return "NEWER_TARGET"
        return "DIFFERENT"
    return "NONE"


def get_status_symbol(status: str) -> str:
    """Get display symbol for status."""
    symbols = {
        "ONLY_SOURCE": "->",
        "ONLY_TARGET": "<-",
        "NEWER_SOURCE": ">>",
        "NEWER_TARGET": "<<",
        "SAME": "==",
        "DIFFERENT": "!=",
        "NONE": "--",
    }
    return symbols.get(status, "?")


# ============================================================
# Template System
# ============================================================

import re


def load_template_block(template_path: Path) -> str:
    """템플릿 파일에서 ```template ... ``` 블록 추출"""
    if not template_path.exists():
        return ""
    content = template_path.read_text(encoding='utf-8')
    match = re.search(r'```template\n(.*?)\n```', content, re.DOTALL)
    if match:
        return match.group(1)
    return ""


# 템플릿 파일 경로
TEMPLATE_LIST_PATH = TEMPLATE_DIR / "oaissync_list.md"

# 템플릿 문자열 정의
TEMPLATE_VIEW_HEADER = """# oaissync view - 차이점 비교

## 비교 대상

| 항목 | 값 |
|------|-----|
| 소스 (현재) | `{source_project}` |
| 대상 | `{target_project}` |
| 대상 Vibe 상태 | {env_status} |
| .claude/ | {has_claude} |
| v/ | {has_v} |
"""

TEMPLATE_VIEW_SUMMARY_HEADER = """
## 요약

| 상태 | 기호 | 설명 | 개수 |
|------|------|------|------|
| SAME | == | 동일 | {same_count} |
"""

TEMPLATE_VIEW_SUMMARY_ROW = "| {status} | {symbol} | {desc} | {count} |"

TEMPLATE_VIEW_TOTAL = """
**총 {total_files}개 파일 중 {diff_count}개 차이**
"""

TEMPLATE_VIEW_DETAIL_HEADER = """
## 상세 차이점

| 상태 | 파일 | 소스 수정일 | 대상 수정일 |
|:----:|------|------------|------------|
"""

TEMPLATE_VIEW_DETAIL_ROW = "| {symbol} | `{file_path}` | {source_mtime} | {target_mtime} |"

TEMPLATE_VIEW_NO_DIFF = """
모든 파일이 동일합니다.
"""

# 상태 정보 매핑
STATUS_INFO = {
    "ONLY_SOURCE": ("->", "대상에 없음 -> 복사 필요"),
    "ONLY_TARGET": ("<-", "현재에 없음 <- 가져오기"),
    "NEWER_SOURCE": (">>", "현재가 최신 -> 덮어쓰기"),
    "NEWER_TARGET": ("<<", "대상이 최신 <- 가져오기"),
}

# Diff 상태 설명 (더 명확한 버전)
DIFF_STATUS_DESC = {
    "ONLY_SOURCE": ("->", "대상에 없음"),
    "ONLY_TARGET": ("<-", "소스에 없음"),
    "NEWER_SOURCE": (">>", "소스가 최신"),
    "NEWER_TARGET": ("<<", "대상이 최신"),
}

# ============================================================
# Diff Template System
# ============================================================

TEMPLATE_DIFF_ALL_HEADER = """# oaissync diff - 전체 차이점 비교

## 비교 대상

| 항목 | 값 |
|------|-----|
| 소스 (현재) | `{source_project}` |
| 대상 | `{target_project}` |
| 차이 파일 수 | {total_count}개 |

---
"""

TEMPLATE_DIFF_FILE_HEADER = """
## [{current_index}/{total_count}] {file_path}

| 항목 | 값 |
|------|-----|
| 소스 (현재) | `{source_project}` - {source_mtime} |
| 대상 | `{target_project}` - {target_mtime} |
| 비교 결과 | **{status_desc}** ({status_symbol}) |
| 변경 내용 | {change_summary} |
"""

TEMPLATE_DIFF_CONTENT = """
### 차이점

```diff
{diff_content}
```
"""

TEMPLATE_DIFF_SEPARATOR = """
---
"""

TEMPLATE_DIFF_ONLY_SOURCE = """
### 파일 내용 (소스에만 존재)

```
{file_content}
```
"""

TEMPLATE_DIFF_ONLY_TARGET = """
### 파일 내용 (대상에만 존재)

```
{file_content}
```
"""


def generate_change_summary(status: str, added: int, removed: int, line_count: int = 0) -> str:
    """변경 요약 문자열 생성"""
    if status == "ONLY_SOURCE":
        return f"소스에만 존재 (신규 파일, {line_count}줄)"
    elif status == "ONLY_TARGET":
        return f"대상에만 존재 ({line_count}줄)"
    elif status == "NEWER_SOURCE":
        if added > 0 and removed == 0:
            return f"소스에 +{added}줄 추가 (대상에 없음)"
        elif added == 0 and removed > 0:
            return f"소스에서 -{removed}줄 삭제"
        else:
            return f"소스에 +{added}줄, -{removed}줄 변경"
    elif status == "NEWER_TARGET":
        if added > 0 and removed == 0:
            return f"대상에 +{added}줄 추가 (소스에 없음)"
        elif added == 0 and removed > 0:
            return f"대상에서 -{removed}줄 삭제"
        else:
            return f"대상에 +{added}줄, -{removed}줄 변경"
    return "알 수 없음"


def render_diff_output(data: dict, include_content: bool = True) -> str:
    """
    템플릿을 사용하여 diff 출력 생성

    Args:
        data: 렌더링에 필요한 데이터
        include_content: diff 내용 포함 여부

    Returns:
        렌더링된 출력 문자열
    """
    output = []

    # 파일 헤더
    output.append(TEMPLATE_DIFF_FILE_HEADER.format(
        current_index=data["current_index"],
        total_count=data["total_count"],
        file_path=data["file_path"],
        source_project=data["source_project"],
        target_project=data["target_project"],
        source_mtime=data["source_mtime"],
        target_mtime=data["target_mtime"],
        status_desc=data["status_desc"],
        status_symbol=data["status_symbol"],
        change_summary=data["change_summary"],
    ))

    # diff 내용
    if include_content and data.get("diff_content"):
        if data["status"] == "ONLY_SOURCE":
            output.append(TEMPLATE_DIFF_ONLY_SOURCE.format(
                file_content=data["diff_content"]
            ))
        elif data["status"] == "ONLY_TARGET":
            output.append(TEMPLATE_DIFF_ONLY_TARGET.format(
                file_content=data["diff_content"]
            ))
        else:
            output.append(TEMPLATE_DIFF_CONTENT.format(
                diff_content=data["diff_content"]
            ))

    output.append(TEMPLATE_DIFF_SEPARATOR)

    return "\n".join(output)


def render_view_output(data: dict) -> str:
    """
    템플릿을 사용하여 view 출력 생성

    Args:
        data: 렌더링에 필요한 데이터
            - source_project: 소스 프로젝트명
            - target_project: 대상 프로젝트명
            - env_status: 환경 상태
            - has_claude: .claude/ 존재 여부
            - has_v: v/ 존재 여부
            - same_count: 동일 파일 수
            - status_counts: 상태별 개수 딕셔너리
            - comparison_results: 비교 결과 리스트

    Returns:
        렌더링된 출력 문자열
    """
    output = []

    # 헤더
    output.append(TEMPLATE_VIEW_HEADER.format(
        source_project=data["source_project"],
        target_project=data["target_project"],
        env_status=data["env_status"],
        has_claude=data["has_claude"],
        has_v=data["has_v"],
    ))

    # 요약 테이블
    output.append(TEMPLATE_VIEW_SUMMARY_HEADER.format(same_count=data["same_count"]))

    for status, (symbol, desc) in STATUS_INFO.items():
        count = data["status_counts"].get(status, 0)
        if count > 0:
            output.append(TEMPLATE_VIEW_SUMMARY_ROW.format(
                status=status,
                symbol=symbol,
                desc=desc,
                count=count
            ))

    # 총계
    total_files = data["same_count"] + len(data["comparison_results"])
    diff_count = len(data["comparison_results"])
    output.append(TEMPLATE_VIEW_TOTAL.format(
        total_files=total_files,
        diff_count=diff_count
    ))

    # 상세 차이점
    if data["comparison_results"]:
        output.append(TEMPLATE_VIEW_DETAIL_HEADER)
        for result in data["comparison_results"]:
            source_dt = result["source_mtime"].strftime("%Y-%m-%d %H:%M") if result["source_mtime"] else "-"
            target_dt = result["target_mtime"].strftime("%Y-%m-%d %H:%M") if result["target_mtime"] else "-"
            output.append(TEMPLATE_VIEW_DETAIL_ROW.format(
                symbol=result["symbol"],
                file_path=result["path"],
                source_mtime=source_dt,
                target_mtime=target_dt
            ))
    else:
        output.append(TEMPLATE_VIEW_NO_DIFF)

    return "\n".join(output)


def render_box_table(projects: list) -> str:
    """
    박스 문자를 사용하여 테이블 생성

    Args:
        projects: 프로젝트 리스트 [{name, status, has_claude, has_v, sync}]

    Returns:
        박스 테이블 문자열
    """
    # 컬럼 너비 계산
    col_widths = {
        "idx": 4,
        "name": max(7, max((len(p["name"]) for p in projects), default=7)) + 2,
        "status": 9,
        "claude": 10,
        "v": 5,
        "sync": 6,
    }

    # 테이블 문자
    lines = []

    # 상단 경계
    top = "┌" + "─" * col_widths["idx"] + "┬" + "─" * col_widths["name"] + "┬" + "─" * col_widths["status"] + "┬" + "─" * col_widths["claude"] + "┬" + "─" * col_widths["v"] + "┬" + "─" * col_widths["sync"] + "┐"
    lines.append(top)

    # 헤더
    header = "│" + " # ".center(col_widths["idx"]) + "│" + " Project".ljust(col_widths["name"]) + "│" + " Status ".center(col_widths["status"]) + "│" + " .claude/ ".center(col_widths["claude"]) + "│" + " v/ ".center(col_widths["v"]) + "│" + " Sync ".center(col_widths["sync"]) + "│"
    lines.append(header)

    # 헤더 구분선
    sep = "├" + "─" * col_widths["idx"] + "┼" + "─" * col_widths["name"] + "┼" + "─" * col_widths["status"] + "┼" + "─" * col_widths["claude"] + "┼" + "─" * col_widths["v"] + "┼" + "─" * col_widths["sync"] + "┤"
    lines.append(sep)

    # 데이터 행
    for idx, proj in enumerate(projects, 1):
        row = "│" + str(idx).rjust(col_widths["idx"] - 1) + " " + "│" + " " + proj["name"].ljust(col_widths["name"] - 1) + "│" + proj["status"].center(col_widths["status"]) + "│" + proj["has_claude"].center(col_widths["claude"]) + "│" + proj["has_v"].center(col_widths["v"]) + "│" + proj["sync"].center(col_widths["sync"]) + "│"
        lines.append(row)

    # 하단 경계
    bottom = "└" + "─" * col_widths["idx"] + "┴" + "─" * col_widths["name"] + "┴" + "─" * col_widths["status"] + "┴" + "─" * col_widths["claude"] + "┴" + "─" * col_widths["v"] + "┴" + "─" * col_widths["sync"] + "┘"
    lines.append(bottom)

    return "\n".join(lines)


def render_list_output(data: dict) -> str:
    """
    템플릿을 사용하여 list 출력 생성

    Args:
        data: 렌더링에 필요한 데이터
            - scan_path: 스캔 경로
            - projects: 프로젝트 리스트 [{name, status, has_claude, has_v, sync}]
            - total_count: 총 프로젝트 수

    Returns:
        렌더링된 출력 문자열
    """
    # 템플릿 파일에서 로드 시도
    template = load_template_block(TEMPLATE_LIST_PATH)

    # 템플릿이 없으면 기본 템플릿 사용
    if not template:
        template = """# oaissync list - 프로젝트 목록

스캔 경로: `{scan_path}`

{table_output}

총 {total_count}개 프로젝트 발견

## 상태 설명
- Full: vibe 환경 완전 구축 (.claude/ AND v/)
- Partial: 부분 구축 (.claude/ OR v/)
- None: vibe 환경 없음 (새로 구축 가능)

## Sync 컬럼
- OK: 동기화 완료 (차이 없음)
- 숫자: 동기화 필요 (차이 파일 수)
- -: 비교 불가 (Full 상태 아님)"""

    # 박스 테이블 생성
    table_output = render_box_table(data["projects"])

    # 템플릿 렌더링
    return template.format(
        scan_path=data["scan_path"],
        table_output=table_output,
        total_count=data["total_count"]
    )


def find_project_by_name(name: str) -> Path | None:
    """
    Find project by name or 4-digit prefix.

    Examples:
        "0003" -> "0003_CCone"
        "0003_CCone" -> "0003_CCone"
    """
    # Direct match first
    direct_path = PARENT_DIR / name
    if direct_path.exists():
        return direct_path

    # Try prefix match (4-digit number)
    if len(name) == 4 and name.isdigit():
        for item in PARENT_DIR.iterdir():
            if item.is_dir() and item.name.startswith(name + "_"):
                return item
            # Also match exact 4-digit folder name
            if item.is_dir() and item.name == name:
                return item

    return None


def collect_files(base_path: Path, relative_path: str) -> list[Path]:
    """Collect all files under a path recursively."""
    full_path = base_path / relative_path
    files = []

    if not full_path.exists():
        return files

    if full_path.is_file():
        if not is_excluded(full_path):
            files.append(Path(relative_path))
    elif full_path.is_dir():
        for item in full_path.rglob("*"):
            if item.is_file() and not is_excluded(item):
                rel = item.relative_to(base_path)
                files.append(rel)

    return files


def quick_diff_count(target_project: Path) -> int:
    """Quick count of differences between current and target project."""
    all_files = set()
    for target in SYNC_TARGETS:
        source_files = collect_files(CURRENT_PROJECT, target.rstrip("/"))
        target_files = collect_files(target_project, target.rstrip("/"))
        all_files.update(source_files)
        all_files.update(target_files)

    diff_count = 0
    for rel_path in all_files:
        source_path = CURRENT_PROJECT / rel_path
        target_path = target_project / rel_path
        status = compare_files(source_path, target_path)
        if status != "SAME":
            diff_count += 1

    return diff_count


# ============================================================
# Commands
# ============================================================

def cmd_status():
    """Show status and available subcommands."""
    print("# oaissync - Vibe 환경 동기화\n")
    print("## 서브명령어\n")
    print("| 명령어 | 설명 |")
    print("|--------|------|")
    print("| `oaissync status` | 현재 상태 (이 화면) |")
    print("| `oaissync list` | 동기화 가능한 프로젝트 목록 |")
    print("| `oaissync files` | 동기화 대상 파일/폴더 목록 |")
    print("| `oaissync view [project]` | 차이점 비교 (읽기 전용) |")
    print("| `oaissync run [project]` | 동기화 실행 |")
    print("| `oaissync run --push-only` | **push만 필요한 모든 프로젝트 일괄 동기화** |")
    print("| `oaissync run --push-only --dry-run` | 동기화 미리보기 (실제 복사 안 함) |")
    print("| `oaissync diff [project] [file]` | 파일 내용 비교 |")
    print()
    print(f"## 현재 프로젝트\n")
    print(f"- 경로: `{CURRENT_PROJECT}`")
    print(f"- 상위 폴더: `{PARENT_DIR}`")


def cmd_list():
    """List projects in parent directory with vibe environment status."""
    # 프로젝트 데이터 수집
    projects = []
    for item in sorted(PARENT_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            # Skip current project
            if item.name == CURRENT_PROJECT.name:
                continue

            has_claude = (item / VIBE_INDICATORS["claude_dir"]).exists()
            has_v = (item / VIBE_INDICATORS["v_dir"]).exists()

            if has_claude and has_v:
                status = "Full"
            elif has_claude or has_v:
                status = "Partial"
            else:
                status = "None"

            # Check sync status for Full projects
            if status == "Full":
                diff_count = quick_diff_count(item)
                sync_mark = "OK" if diff_count == 0 else str(diff_count)
            else:
                sync_mark = "-"

            projects.append({
                "name": item.name,
                "status": status,
                "has_claude": "O" if has_claude else "X",
                "has_v": "O" if has_v else "X",
                "sync": sync_mark,
            })

    # 템플릿 기반 출력 생성
    template_data = {
        "scan_path": str(PARENT_DIR),
        "projects": projects,
        "total_count": len(projects),
    }

    output = render_list_output(template_data)
    print(output)


def cmd_files():
    """Show sync target files/folders."""
    print("# oaissync files - 동기화 대상\n")
    print("## 기본 동기화 대상\n")

    for target in SYNC_TARGETS:
        target_path = CURRENT_PROJECT / target
        if target_path.exists():
            status = "[존재]"
        else:
            status = "[없음]"
        print(f"- `{target}` {status}")

    print("\n## v/ 폴더 상세\n")
    v_path = CURRENT_PROJECT / "v"
    if v_path.exists():
        print("```")
        for item in sorted(v_path.iterdir()):
            if is_excluded(item):
                continue
            if item.is_dir():
                count = len(list(item.rglob("*")))
                print(f"  {item.name}/  ({count} files)")
            else:
                print(f"  {item.name}")
        print("```")

    print("\n## .claude/ 폴더 상세\n")
    claude_path = CURRENT_PROJECT / ".claude"
    if claude_path.exists():
        print("```")
        for item in sorted(claude_path.iterdir()):
            if is_excluded(item):
                continue
            if item.is_dir():
                count = len(list(item.rglob("*")))
                print(f"  {item.name}/  ({count} files)")
            else:
                print(f"  {item.name}")
        print("```")

    print("\n## 제외 패턴\n")
    for pattern in EXCLUDE_PATTERNS:
        print(f"- `{pattern}`")


def cmd_view(project_name: str | None = None):
    """View differences with target project (read-only)."""
    if not project_name:
        print("# oaissync view - 차이점 비교\n")
        print("사용법: `oaissync view [project_name]`\n")
        print("프로젝트명 또는 4자리 번호 입력 가능 (예: 0003 또는 0003_CCone)\n")
        print("`oaissync list`로 프로젝트 목록을 먼저 확인하세요.")
        return

    target_project = find_project_by_name(project_name)
    if not target_project:
        print(f"오류: 프로젝트 '{project_name}'를 찾을 수 없습니다.")
        print("4자리 번호 또는 전체 프로젝트명을 입력하세요.")
        return

    # Check vibe environment status
    has_claude = (target_project / VIBE_INDICATORS["claude_dir"]).exists()
    has_v = (target_project / VIBE_INDICATORS["v_dir"]).exists()
    if has_claude and has_v:
        env_status = "Full"
    elif has_claude or has_v:
        env_status = "Partial"
    else:
        env_status = "None"

    # Collect all files to compare
    all_files = set()
    for target in SYNC_TARGETS:
        source_files = collect_files(CURRENT_PROJECT, target.rstrip("/"))
        target_files = collect_files(target_project, target.rstrip("/"))
        all_files.update(source_files)
        all_files.update(target_files)

    # Compare files
    comparison_results = []
    same_count = 0
    for rel_path in sorted(all_files):
        source_path = CURRENT_PROJECT / rel_path
        target_path = target_project / rel_path

        status = compare_files(source_path, target_path)
        if status == "SAME":
            same_count += 1
        else:
            comparison_results.append({
                "path": str(rel_path),
                "status": status,
                "symbol": get_status_symbol(status),
                "source_mtime": get_file_mtime(source_path),
                "target_mtime": get_file_mtime(target_path),
            })

    # Build status counts
    status_counts = {}
    for result in comparison_results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    # Prepare data for template rendering
    template_data = {
        "source_project": CURRENT_PROJECT.name,
        "target_project": target_project.name,
        "env_status": env_status,
        "has_claude": "O" if has_claude else "X",
        "has_v": "O" if has_v else "X",
        "same_count": same_count,
        "status_counts": status_counts,
        "comparison_results": comparison_results,
    }

    # Render and print output using template
    output = render_view_output(template_data)
    print(output)


def check_push_only(target_project: Path, allow_delete: bool = False) -> tuple[bool, int, int]:
    """
    Check if project only needs push (no pull required).

    Args:
        target_project: Target project path
        allow_delete: If True, ONLY_TARGET files are treated as deletable (not pull needed)

    Returns:
        (is_push_only, diff_count, delete_count): True if only push needed, total diff count, and count of files to delete
    """
    all_files = set()
    for target in SYNC_TARGETS:
        source_files = collect_files(CURRENT_PROJECT, target.rstrip("/"))
        target_files = collect_files(target_project, target.rstrip("/"))
        all_files.update(source_files)
        all_files.update(target_files)

    diff_count = 0
    delete_count = 0
    has_pull_needed = False

    for rel_path in all_files:
        source_path = CURRENT_PROJECT / rel_path
        target_path = target_project / rel_path
        status = compare_files(source_path, target_path)

        if status != "SAME":
            diff_count += 1
            if status == "ONLY_TARGET":
                delete_count += 1
                if not allow_delete:
                    has_pull_needed = True
            elif status == "NEWER_TARGET":
                has_pull_needed = True

    return (not has_pull_needed, diff_count, delete_count)


def sync_project(target_project: Path, dry_run: bool = False) -> bool:
    """
    Sync files to target project (push only).

    Args:
        target_project: Target project path
        dry_run: If True, only show what would be done without actual sync

    Returns:
        True if successful
    """
    for target in SYNC_TARGETS:
        source_path = CURRENT_PROJECT / target.rstrip("/")
        target_path = target_project / target.rstrip("/")

        if not source_path.exists():
            continue

        if dry_run:
            if source_path.is_file():
                print(f"    [DRY-RUN] 복사 예정: {source_path.name} -> {target_path}")
            else:
                print(f"    [DRY-RUN] 폴더 복사 예정: {target}/ -> {target_project.name}/{target}/")
        else:
            if source_path.is_file():
                # Single file copy
                shutil.copy2(source_path, target_path)
            else:
                # Directory copy
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.copytree(source_path, target_path,
                              ignore=shutil.ignore_patterns(*[p.replace("*", "") for p in EXCLUDE_PATTERNS if "*" in p]))

    return True


def cmd_run_push_only(dry_run: bool = False, allow_delete: bool = False):
    """Run sync for all Full projects that only need push."""
    print("# oaissync run --push-only\n")
    if dry_run:
        print("[DRY-RUN] 실제 파일 복사 없이 미리보기만 실행\n")
    if allow_delete:
        print("[DELETE] 대상에만 있는 파일 삭제 모드 활성화\n")
    print("push만 필요한 Full 프로젝트 일괄 동기화\n")

    # Collect Full projects
    full_projects = []
    for item in sorted(PARENT_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            if item.name == CURRENT_PROJECT.name:
                continue

            has_claude = (item / VIBE_INDICATORS["claude_dir"]).exists()
            has_v = (item / VIBE_INDICATORS["v_dir"]).exists()

            if has_claude and has_v:  # Full status
                full_projects.append(item)

    if not full_projects:
        print("Full 상태의 프로젝트가 없습니다.")
        return

    # Check each project
    push_only_projects = []
    skip_projects = []
    ok_projects = []

    print("## 프로젝트 검사\n")
    if allow_delete:
        print("| # | Project | 상태 | 차이 | 삭제 | 결과 |")
        print("|---|---------|------|------|------|------|")
    else:
        print("| # | Project | 상태 | 차이 | 결과 |")
        print("|---|---------|------|------|------|")

    for idx, proj in enumerate(full_projects, 1):
        is_push_only, diff_count, delete_count = check_push_only(proj, allow_delete=allow_delete)

        if diff_count == 0:
            ok_projects.append(proj)
            if allow_delete:
                print(f"| {idx} | {proj.name} | OK | 0 | 0 | 동기화 불필요 |")
            else:
                print(f"| {idx} | {proj.name} | OK | 0 | 동기화 불필요 |")
        elif is_push_only:
            push_only_projects.append((proj, diff_count, delete_count))
            if allow_delete:
                print(f"| {idx} | {proj.name} | Push | {diff_count} | {delete_count} | 동기화 대상 |")
            else:
                print(f"| {idx} | {proj.name} | Push | {diff_count} | 동기화 대상 |")
        else:
            skip_projects.append((proj, diff_count, delete_count))
            if allow_delete:
                print(f"| {idx} | {proj.name} | Pull필요 | {diff_count} | {delete_count} | 건너뜀 |")
            else:
                print(f"| {idx} | {proj.name} | Pull필요 | {diff_count} | 건너뜀 |")

    print()

    if not push_only_projects:
        print("## 결과\n")
        print(f"- OK (동기화 불필요): {len(ok_projects)}개")
        print(f"- Pull 필요 (건너뜀): {len(skip_projects)}개")
        print("\npush만 필요한 프로젝트가 없습니다.")
        if skip_projects and not allow_delete:
            print("\n[TIP] 대상에만 있는 파일 삭제 허용: `oaissync run --push-only --delete`")
        return

    # Execute sync
    if dry_run:
        print("## 동기화 미리보기\n")
    else:
        print("## 동기화 실행\n")

    success_count = 0
    total_deleted = 0
    for proj, diff_count, delete_count in push_only_projects:
        if dry_run:
            print(f"- {proj.name} ({diff_count}개 파일, 삭제: {delete_count}개):")
            sync_project(proj, dry_run=True)
            success_count += 1
            total_deleted += delete_count
        else:
            print(f"- {proj.name} ({diff_count}개 파일, 삭제: {delete_count}개)... ", end="", flush=True)
            if sync_project(proj, dry_run=False):
                print("완료")
                success_count += 1
                total_deleted += delete_count
            else:
                print("실패")

    if dry_run:
        print(f"\n## 미리보기 완료\n")
        print(f"- 동기화 대상: {success_count}/{len(push_only_projects)}개")
        print(f"- OK (이미 동기화): {len(ok_projects)}개")
        print(f"- Pull 필요 (건너뜀): {len(skip_projects)}개")
        if allow_delete:
            print(f"- 삭제 예정 파일: {total_deleted}개")
        print("\n[TIP] 실제 동기화: `oaissync run --push-only` (--dry-run 제거)")
    else:
        print(f"\n## 완료\n")
        print(f"- 동기화 성공: {success_count}/{len(push_only_projects)}개")
        print(f"- OK (이미 동기화): {len(ok_projects)}개")
        print(f"- Pull 필요 (건너뜀): {len(skip_projects)}개")
        if allow_delete:
            print(f"- 삭제된 파일: {total_deleted}개")

    if skip_projects:
        print(f"\n### Pull 필요 프로젝트\n")
        print("다음 프로젝트는 수동 동기화가 필요합니다:\n")
        for proj, diff_count, delete_count in skip_projects:
            print(f"- `{proj.name}` ({diff_count}개 차이)")


def cmd_run(project_name: str | None = None):
    """Run sync comparison with target project."""
    print("# oaissync run - 동기화 실행\n")

    if not project_name:
        print("사용법: `oaissync run [project_name]`\n")
        print("프로젝트명 또는 4자리 번호 입력 가능 (예: 0003 또는 0003_CCone)\n")
        print("`oaissync list`로 프로젝트 목록을 먼저 확인하세요.")
        return

    target_project = find_project_by_name(project_name)
    if not target_project:
        print(f"오류: 프로젝트 '{project_name}'를 찾을 수 없습니다.")
        print("4자리 번호 또는 전체 프로젝트명을 입력하세요.")
        return

    print(f"## 비교 대상\n")
    print(f"- 소스 (현재): `{CURRENT_PROJECT.name}`")
    print(f"- 대상: `{target_project.name}`\n")

    # Collect all files to compare
    all_files = set()
    for target in SYNC_TARGETS:
        source_files = collect_files(CURRENT_PROJECT, target.rstrip("/"))
        target_files = collect_files(target_project, target.rstrip("/"))
        all_files.update(source_files)
        all_files.update(target_files)

    # Compare files
    comparison_results = []
    for rel_path in sorted(all_files):
        source_path = CURRENT_PROJECT / rel_path
        target_path = target_project / rel_path

        status = compare_files(source_path, target_path)
        if status != "SAME":  # Only show differences
            comparison_results.append({
                "path": str(rel_path),
                "status": status,
                "symbol": get_status_symbol(status),
                "source_mtime": get_file_mtime(source_path),
                "target_mtime": get_file_mtime(target_path),
            })

    print("## 비교 결과\n")

    if not comparison_results:
        print("모든 파일이 동일합니다. 동기화가 필요하지 않습니다.")
        return

    print("| 상태 | 파일 | 소스 수정일 | 대상 수정일 |")
    print("|------|------|------------|------------|")

    for result in comparison_results:
        source_dt = result["source_mtime"].strftime("%Y-%m-%d %H:%M") if result["source_mtime"] else "-"
        target_dt = result["target_mtime"].strftime("%Y-%m-%d %H:%M") if result["target_mtime"] else "-"
        print(f"| {result['symbol']} | `{result['path']}` | {source_dt} | {target_dt} |")

    print(f"\n총 {len(comparison_results)}개 파일 차이 발견\n")

    # Summary by status
    print("## 상태별 요약\n")
    status_counts = {}
    for result in comparison_results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    print("| 상태 | 설명 | 개수 | 권장 액션 |")
    print("|------|------|------|----------|")

    status_info = {
        "ONLY_SOURCE": ("→", "대상에 없음 → 복사 필요", "push"),
        "ONLY_TARGET": ("←", "현재에 없음 ← 가져오기", "pull"),
        "NEWER_SOURCE": (">>", "현재가 최신 → 덮어쓰기", "push"),
        "NEWER_TARGET": ("<<", "대상이 최신 ← 가져오기", "pull"),
    }

    for status, count in status_counts.items():
        if status in status_info:
            symbol, desc, action = status_info[status]
            print(f"| {symbol} | {desc} | {count} | {action} |")

    print("\n## 동기화 가이드\n")
    print("위 결과를 확인 후, 다음 액션을 선택하세요:\n")
    print("- **push**: 현재 프로젝트 → 대상 프로젝트로 복사")
    print("- **pull**: 대상 프로젝트 → 현재 프로젝트로 복사")
    print("- **skip**: 해당 파일 건너뛰기")
    print("\n### 예시 명령어\n")
    print("```bash")
    print(f"# 대상 프로젝트로 v/ 폴더 전체 복사")
    print(f"cp -r v/ {target_project}/v/")
    print()
    print(f"# 대상 프로젝트에서 특정 파일 가져오기")
    print(f"cp {target_project}/v/oaissync.md v/")
    print("```")


def get_file_diff_data(source_file: Path, target_file: Path, source_project_name: str,
                       target_project_name: str, rel_path: str, status: str,
                       current_index: int, total_count: int) -> dict:
    """단일 파일의 diff 데이터 생성"""
    import difflib

    source_mtime = get_file_mtime(source_file)
    target_mtime = get_file_mtime(target_file)
    source_dt = source_mtime.strftime("%Y-%m-%d %H:%M") if source_mtime else "-"
    target_dt = target_mtime.strftime("%Y-%m-%d %H:%M") if target_mtime else "-"

    symbol, desc = DIFF_STATUS_DESC.get(status, ("?", "알 수 없음"))

    # 파일 내용 및 diff 생성
    diff_content = ""
    added = 0
    removed = 0
    line_count = 0

    if status == "ONLY_SOURCE":
        # 소스에만 존재
        try:
            content = source_file.read_text(encoding='utf-8')
            line_count = len(content.splitlines())
            diff_content = content[:2000] + ("..." if len(content) > 2000 else "")
        except (UnicodeDecodeError, Exception):
            diff_content = "(바이너리 파일 또는 읽기 오류)"
    elif status == "ONLY_TARGET":
        # 대상에만 존재
        try:
            content = target_file.read_text(encoding='utf-8')
            line_count = len(content.splitlines())
            diff_content = content[:2000] + ("..." if len(content) > 2000 else "")
        except (UnicodeDecodeError, Exception):
            diff_content = "(바이너리 파일 또는 읽기 오류)"
    else:
        # 양쪽 모두 존재 - unified diff 생성
        try:
            source_lines = source_file.read_text(encoding='utf-8').splitlines(keepends=True)
            target_lines = target_file.read_text(encoding='utf-8').splitlines(keepends=True)

            diff = difflib.unified_diff(
                target_lines,
                source_lines,
                fromfile=f"[대상] {target_project_name}/{rel_path}",
                tofile=f"[소스] {source_project_name}/{rel_path}",
                lineterm=""
            )
            diff_output = list(diff)

            if diff_output:
                # 추가/삭제 줄 수 계산
                added = sum(1 for line in diff_output if line.startswith('+') and not line.startswith('+++'))
                removed = sum(1 for line in diff_output if line.startswith('-') and not line.startswith('---'))
                # diff 내용 (최대 50줄)
                diff_content = "\n".join(diff_output[:50])
                if len(diff_output) > 50:
                    diff_content += f"\n... (+{len(diff_output) - 50}줄 더)"
        except (UnicodeDecodeError, Exception):
            diff_content = "(바이너리 파일 또는 읽기 오류)"

    change_summary = generate_change_summary(status, added, removed, line_count)

    return {
        "current_index": current_index,
        "total_count": total_count,
        "file_path": rel_path,
        "source_project": source_project_name,
        "target_project": target_project_name,
        "source_mtime": source_dt,
        "target_mtime": target_dt,
        "status": status,
        "status_symbol": symbol,
        "status_desc": desc,
        "change_summary": change_summary,
        "diff_content": diff_content,
        "added": added,
        "removed": removed,
    }


def cmd_diff(project_name: str | None, filename: str | None):
    """Show visual diff between files in current and target project."""
    if not project_name:
        print("# oaissync diff - 파일 비교\n")
        print("사용법: `oaissync diff [project] [filename]`\n")
        print("- filename 생략 시: 모든 차이 파일을 순서대로 표시")
        print("- filename 지정 시: 해당 파일만 비교\n")
        print("`oaissync list`로 프로젝트 목록을 먼저 확인하세요.")
        return

    # Find target project
    target_project = find_project_by_name(project_name)
    if not target_project:
        print(f"오류: 프로젝트 '{project_name}'를 찾을 수 없습니다.")
        return

    # 특정 파일만 비교하는 경우
    if filename:
        filename = filename.replace("\\", "/")
        source_file = CURRENT_PROJECT / filename
        target_file = target_project / filename

        # 파일 상태 확인
        if not source_file.exists() and not target_file.exists():
            print("오류: 양쪽 모두 파일이 존재하지 않습니다.")
            return

        if source_file.exists() and not target_file.exists():
            status = "ONLY_SOURCE"
        elif not source_file.exists() and target_file.exists():
            status = "ONLY_TARGET"
        else:
            source_mtime = get_file_mtime(source_file)
            target_mtime = get_file_mtime(target_file)
            if source_mtime and target_mtime:
                status = "NEWER_SOURCE" if source_mtime > target_mtime else "NEWER_TARGET"
            else:
                status = "NEWER_SOURCE"

        diff_data = get_file_diff_data(
            source_file, target_file,
            CURRENT_PROJECT.name, target_project.name,
            filename, status, 1, 1
        )
        output = render_diff_output(diff_data, include_content=True)
        print(output)
        return

    # 파일명 미지정 - 모든 차이 파일 표시
    # Collect all files to compare
    all_files = set()
    for target in SYNC_TARGETS:
        source_files = collect_files(CURRENT_PROJECT, target.rstrip("/"))
        target_files = collect_files(target_project, target.rstrip("/"))
        all_files.update(source_files)
        all_files.update(target_files)

    # Compare files and collect differences
    comparison_results = []
    for rel_path in sorted(all_files):
        source_path = CURRENT_PROJECT / rel_path
        target_path = target_project / rel_path

        status = compare_files(source_path, target_path)
        if status != "SAME":
            comparison_results.append({
                "path": str(rel_path),
                "status": status,
                "source_path": source_path,
                "target_path": target_path,
            })

    if not comparison_results:
        print("# oaissync diff - 파일 비교\n")
        print("모든 파일이 동일합니다. 비교할 차이점이 없습니다.")
        return

    # 전체 헤더 출력
    print(TEMPLATE_DIFF_ALL_HEADER.format(
        source_project=CURRENT_PROJECT.name,
        target_project=target_project.name,
        total_count=len(comparison_results)
    ))

    # 각 파일별 diff 출력
    total_count = len(comparison_results)
    for idx, result in enumerate(comparison_results, 1):
        diff_data = get_file_diff_data(
            result["source_path"],
            result["target_path"],
            CURRENT_PROJECT.name,
            target_project.name,
            result["path"],
            result["status"],
            idx,
            total_count
        )
        output = render_diff_output(diff_data, include_content=True)
        print(output)


def main():
    """Main entry point."""
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaissync", sys.argv[1:]):
        return

    if len(sys.argv) < 2:
        cmd_status()
        return

    subcommand = sys.argv[1].lower()

    if subcommand == "status":
        cmd_status()
    elif subcommand == "list":
        cmd_list()
    elif subcommand == "files":
        cmd_files()
    elif subcommand == "view":
        project_name = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_view(project_name)
    elif subcommand == "run":
        # Check for --push-only flag
        if "--push-only" in sys.argv:
            dry_run = "--dry-run" in sys.argv
            allow_delete = "--delete" in sys.argv
            cmd_run_push_only(dry_run=dry_run, allow_delete=allow_delete)
        else:
            project_name = sys.argv[2] if len(sys.argv) > 2 else None
            cmd_run(project_name)
    elif subcommand == "diff":
        project_name = sys.argv[2] if len(sys.argv) > 2 else None
        filename = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_diff(project_name, filename)
    else:
        print(f"알 수 없는 명령어: {subcommand}")
        print("'oaissync status'로 사용 가능한 명령어를 확인하세요.")


if __name__ == "__main__":
    main()
