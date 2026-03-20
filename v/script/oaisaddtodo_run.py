#!/usr/bin/env python3
"""
oaisaddtodo_run.py

Todo 자동 처리 스킬 스크립트
- 기본 실행: 대기 중 업무 자동 처리
- status: 대기 중 목록 표시
- add [text]: 새 할 일 추가

Usage:
    uv run python v/script/oaisaddtodo_run.py              # 자동 처리
    uv run python v/script/oaisaddtodo_run.py status       # 상태 조회
    uv run python v/script/oaisaddtodo_run.py add [text]   # 할 일 추가
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path.cwd()
DOC_DIR = PROJECT_ROOT / "doc"

# 기본 todo 문서
DEFAULT_TODO_FILE = "d0004_todo.md"


# ============================================================
# Helper Functions
# ============================================================

def get_todo_file(sp: str = "00") -> Path:
    """Get todo file path based on subproject context."""
    if sp == "00":
        return DOC_DIR / DEFAULT_TODO_FILE
    else:
        # d20004_todo.md for SP=02
        doc_num = int(sp) * 10000 + 4
        return DOC_DIR / f"d{doc_num}_todo.md"


def get_today() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def find_last_todo_id(content: str) -> int:
    """Find the last todo ID number from the content."""
    # Match patterns like T001, T002, etc.
    matches = re.findall(r'\| T(\d+) \|', content)
    if matches:
        return max(int(m) for m in matches)
    return 0


def parse_waiting_todos(content: str) -> list[dict]:
    """Parse waiting todos from the document."""
    todos = []

    # Find the '대기 중' section
    waiting_pattern = r'### 대기 중\s*\n\s*\n((?:\|[^\n]+\n)+)'
    match = re.search(waiting_pattern, content)

    if match:
        table = match.group(1)
        lines = table.strip().split('\n')

        for line in lines:
            # Skip header and separator
            if line.startswith('| ID |') or line.startswith('|----'):
                continue
            # Skip empty placeholder
            if '(대기 중인 작업 없음)' in line:
                continue

            # Parse actual todo rows: | T004 | 2026-01-06 | 내용 | Medium | 비고 |
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and parts[1].startswith('T'):
                todos.append({
                    'id': parts[1],
                    'date': parts[2],
                    'content': parts[3],
                    'priority': parts[4],
                    'note': parts[5]
                })

    return todos


def analyze_task_type(content: str) -> tuple[str, str]:
    """
    Analyze task content to determine type and recommended skill.
    Returns: (task_type, skill_name)
    """
    content_lower = content.lower()

    # 동기화 관련
    if any(kw in content_lower for kw in ['동기화', 'sync', '동기']):
        return 'sync', 'oaissync'

    # 구현/개발 관련
    if any(kw in content_lower for kw in ['구현', '개발', '추가', '생성', '만들기']):
        return 'develop', 'oaisdev'

    # 수정/버그 관련
    if any(kw in content_lower for kw in ['수정', '버그', 'fix', '고치', '오류']):
        return 'fix', 'oaisfix'

    # 문서화 관련
    if any(kw in content_lower for kw in ['문서', '작성', '정리', 'doc']):
        return 'document', 'oaisdoc'

    # 기타
    return 'general', 'agent'


def add_todo_to_waiting(content: str, text: str, priority: str = "Medium", note: str = "-") -> tuple[str, str]:
    """
    Add a new todo item to the '대기 중' section.

    Returns:
        Tuple of (modified_content, new_todo_id)
    """
    # Find the last ID
    last_id = find_last_todo_id(content)
    new_id = f"T{last_id + 1:03d}"
    today = get_today()

    # Create new row
    new_row = f"| {new_id} | {today} | {text} | {priority} | {note} |"

    # Find the '대기 중' section and its table
    # Pattern: ### 대기 중 ... table header ... empty row or data rows
    waiting_section_pattern = r'(### 대기 중\s*\n\s*\n\s*\| ID \| 등록일 \| 내용 \| 우선순위 \| 비고 \|\s*\n\s*\|[-|]+\|\s*\n)(\| - \| - \| \(대기 중인 작업 없음\) \| - \| - \||\| T\d+ \|[^\n]*)'

    match = re.search(waiting_section_pattern, content)

    if match:
        header = match.group(1)
        existing_row = match.group(2)

        # Check if it's the empty placeholder
        if "(대기 중인 작업 없음)" in existing_row:
            # Replace the placeholder with new row
            new_content = content.replace(
                header + existing_row,
                header + new_row
            )
        else:
            # Add new row after existing rows
            # Find all rows in 대기 중 section
            section_start = match.start()
            section_content = content[section_start:]

            # Find where the table ends (next section or empty line after table)
            lines = section_content.split('\n')
            table_end_idx = 0
            in_table = False
            for i, line in enumerate(lines):
                if line.startswith('| ID |') or line.startswith('|----'):
                    in_table = True
                    continue
                if in_table and line.startswith('|'):
                    table_end_idx = i
                elif in_table and not line.startswith('|'):
                    break

            # Insert new row after last table row
            lines.insert(table_end_idx + 1, new_row)
            new_section = '\n'.join(lines)
            new_content = content[:section_start] + new_section
    else:
        # Fallback: try simpler pattern
        simple_pattern = r'(\| - \| - \| \(대기 중인 작업 없음\) \| - \| - \|)'
        if re.search(simple_pattern, content):
            new_content = re.sub(simple_pattern, new_row, content)
        else:
            # Just append after the table header in 대기 중
            header_pattern = r'(### 대기 중\s*\n\s*\n\s*\| ID \| 등록일 \| 내용 \| 우선순위 \| 비고 \|\s*\n\s*\|[-|]+\|\s*\n)'
            match = re.search(header_pattern, content)
            if match:
                insert_pos = match.end()
                new_content = content[:insert_pos] + new_row + "\n" + content[insert_pos:]
            else:
                print("오류: '대기 중' 섹션을 찾을 수 없습니다.")
                return content, ""

    return new_content, new_id


def move_to_in_progress(content: str, todo_id: str, todo_text: str) -> str:
    """Move a todo from 대기 중 to 진행 중."""
    today = get_today()

    # Pattern for the specific todo row
    todo_pattern = rf'\| {todo_id} \| [^\|]+ \| [^\|]+ \| [^\|]+ \| [^\|]+ \|'

    # Remove from 대기 중
    new_content = re.sub(todo_pattern + r'\n?', '', content)

    # Find 진행 중 section and add there
    in_progress_header = r'(### 진행 중\s*\n\s*\n\s*\| ID \| 등록일 \| 내용 \| 담당 \| 상태 \|\s*\n\s*\|[-|]+\|\s*\n)'
    match = re.search(in_progress_header, new_content)

    if match:
        # Check if placeholder exists
        placeholder_pattern = r'\| - \| - \| \(진행 중인 작업 없음\) \| - \| - \|'
        if re.search(placeholder_pattern, new_content):
            new_row = f"| {todo_id} | {today} | {todo_text} | Agent | 처리중 |"
            new_content = re.sub(placeholder_pattern, new_row, new_content)
        else:
            # Add new row
            insert_pos = match.end()
            new_row = f"| {todo_id} | {today} | {todo_text} | Agent | 처리중 |\n"
            new_content = new_content[:insert_pos] + new_row + new_content[insert_pos:]

    return new_content


def move_to_completed(content: str, todo_id: str, todo_text: str) -> str:
    """Move a todo from 진행 중 to 완료."""
    today = get_today()

    # Pattern for the specific todo row in 진행 중
    todo_pattern = rf'\| {todo_id} \| [^\|]+ \| [^\|]+ \| [^\|]+ \| [^\|]+ \|'

    # Remove from 진행 중
    new_content = re.sub(todo_pattern + r'\n?', '', content)

    # Find 완료 section and add there
    completed_header = r'(### 완료\s*\n\s*\n\s*\| ID \| 등록일 \| 내용 \| 완료일 \| 비고 \|\s*\n\s*\|[-|]+\|\s*\n)'
    match = re.search(completed_header, new_content)

    if match:
        insert_pos = match.end()
        new_row = f"| {todo_id} | {today} | {todo_text} | {today} | 자동 처리 |\n"
        new_content = new_content[:insert_pos] + new_row + new_content[insert_pos:]

    return new_content


# ============================================================
# Commands
# ============================================================

def cmd_status(sp: str = "00"):
    """Show current waiting todos."""
    todo_file = get_todo_file(sp)

    if not todo_file.exists():
        print(f"오류: {todo_file} 파일이 존재하지 않습니다.")
        return

    content = todo_file.read_text(encoding='utf-8')
    todos = parse_waiting_todos(content)

    print("# oaisaddtodo status - 대기 중인 Todo 목록\n")

    if not todos:
        print("(대기 중인 항목 없음)")
        return

    print("| ID | 등록일 | 내용 | 우선순위 | 비고 |")
    print("|----|--------|------|---------|------|")
    for todo in todos:
        print(f"| {todo['id']} | {todo['date']} | {todo['content']} | {todo['priority']} | {todo['note']} |")

    print(f"\n총 {len(todos)}개 항목")

    # Show recommended actions
    print("\n## 처리 권장 순서")
    high_priority = [t for t in todos if t['priority'].lower() == 'high']
    for todo in high_priority:
        task_type, skill = analyze_task_type(todo['content'])
        print(f"- [{todo['id']}] {todo['content']} → {skill} 사용 권장")


def cmd_add(text: str, priority: str = "Medium", note: str = "-", sp: str = "00"):
    """Add a new todo item."""
    todo_file = get_todo_file(sp)

    if not todo_file.exists():
        print(f"오류: {todo_file} 파일이 존재하지 않습니다.")
        return

    content = todo_file.read_text(encoding='utf-8')
    new_content, new_id = add_todo_to_waiting(content, text, priority, note)

    if not new_id:
        return

    # Write back
    todo_file.write_text(new_content, encoding='utf-8')

    # Display result
    print("# oaisaddtodo add - Todo 추가 완료\n")
    print(f"[OK] {new_id} 추가됨\n")
    print("| ID | 등록일 | 내용 | 우선순위 | 비고 |")
    print("|----|--------|------|---------|------|")
    print(f"| {new_id} | {get_today()} | {text} | {priority} | {note} |")
    print(f"\n파일: {todo_file.relative_to(PROJECT_ROOT)}")


def cmd_run(sp: str = "00", dry_run: bool = False, max_items: int = 0):
    """Process pending todos automatically."""
    todo_file = get_todo_file(sp)

    if not todo_file.exists():
        print(f"오류: {todo_file} 파일이 존재하지 않습니다.")
        return

    content = todo_file.read_text(encoding='utf-8')
    todos = parse_waiting_todos(content)

    print("# oaisaddtodo - 대기 중 업무 자동 처리\n")

    if not todos:
        print("[OK] 처리할 대기 중 업무가 없습니다.")
        return

    # Apply max_items limit
    if max_items > 0:
        todos = todos[:max_items]

    print(f"## 처리 대상: {len(todos)}개 항목\n")

    # Analyze each todo
    for todo in todos:
        task_type, skill = analyze_task_type(todo['content'])
        priority_marker = "[!]" if todo['priority'].lower() == 'high' else ""
        print(f"- {priority_marker}[{todo['id']}] {todo['content']}")
        print(f"  유형: {task_type} | 권장 스킬: {skill}")

    if dry_run:
        print("\n[DRY-RUN] 실제 처리는 수행하지 않습니다.")
        return

    print("\n" + "="*50)
    print("## 처리 시작")
    print("="*50 + "\n")

    # Process each todo
    for i, todo in enumerate(todos, 1):
        task_type, skill = analyze_task_type(todo['content'])

        print(f"\n### [{i}/{len(todos)}] {todo['id']}: {todo['content']}")
        print(f"유형: {task_type} | 스킬: {skill}\n")

        # Output instruction for agent to process
        print(f">>> 다음 업무를 처리하세요:")
        print(f"    내용: {todo['content']}")
        print(f"    권장 스킬: {skill}")

        if skill == 'oaissync':
            print(f"    실행: oaissync run [project]")
        elif skill == 'oaisdev':
            print(f"    실행: oaisdev run")
        elif skill == 'oaisfix':
            print(f"    실행: oaisfix run")
        else:
            print(f"    직접 처리 필요")

        print(f"\n    완료 후 이 항목을 '완료' 섹션으로 이동하세요.")
        print(f"    - 항목 ID: {todo['id']}")
        print(f"    - 파일: {todo_file.relative_to(PROJECT_ROOT)}")

    print("\n" + "="*50)
    print("## 처리 완료 안내")
    print("="*50)
    print(f"\n총 {len(todos)}개 항목의 처리 지침이 출력되었습니다.")
    print("각 항목을 순차적으로 처리하고, 완료 시 상태를 업데이트하세요.")


def main():
    """Main entry point."""
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisaddtodo", sys.argv[1:]):
        return

    args = sys.argv[1:]

    # Parse global options
    sp = "00"
    dry_run = False
    max_items = 0

    # Extract options
    filtered_args = []
    i = 0
    while i < len(args):
        if args[i] == "--sp" and i + 1 < len(args):
            sp = args[i + 1]
            i += 2
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        elif args[i] == "--max-items" and i + 1 < len(args):
            max_items = int(args[i + 1])
            i += 2
        else:
            filtered_args.append(args[i])
            i += 1

    args = filtered_args

    # No arguments: run auto-process
    if not args:
        cmd_run(sp, dry_run, max_items)
        return

    subcommand = args[0].lower()

    if subcommand == "status":
        cmd_status(sp)
        return

    if subcommand == "add":
        if len(args) < 2:
            print("사용법: oaisaddtodo add [text]")
            print("\n예시:")
            print('  oaisaddtodo add "로그인 페이지 수정"')
            print('  oaisaddtodo add "API 문서화" --priority high')
            return

        # Extract text and options
        text = args[1]
        priority = "Medium"
        note = "-"

        j = 2
        while j < len(args):
            if args[j] == "--priority" and j + 1 < len(args):
                priority = args[j + 1].capitalize()
                j += 2
            elif args[j] == "--note" and j + 1 < len(args):
                note = args[j + 1]
                j += 2
            else:
                j += 1

        cmd_add(text, priority, note, sp)
        return

    # Unknown subcommand - show help
    print("oaisaddtodo - Todo 자동 처리 스킬")
    print("\n사용법:")
    print("  oaisaddtodo              # 대기 중 업무 자동 처리")
    print("  oaisaddtodo status       # 대기 중 목록 표시")
    print('  oaisaddtodo add [text]   # 새 할 일 추가')
    print("\n옵션:")
    print("  --sp N          서브프로젝트 지정")
    print("  --dry-run       실제 처리 없이 계획만 표시")
    print("  --max-items N   최대 처리 항목 수")
    print("\n예시:")
    print("  oaisaddtodo --dry-run")
    print('  oaisaddtodo add "새 기능 구현" --priority high')


if __name__ == "__main__":
    main()
