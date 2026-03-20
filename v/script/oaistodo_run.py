#!/usr/bin/env python3
"""
oaistodo_run.py

Todo 자동 처리 스킬 스크립트
- oaistodo "내용": 추가 + 즉시 처리
- oaistodo: 대기 중 업무 자동 처리
- oaistodo status: 대기 중 목록 표시
- oaistodo add [text]: 할 일 추가만 (처리 안함)
- oaistodo clear: 완료된 todo를 d0010_history.md로 이동

Usage:
    uv run python v/script/oaistodo_run.py "버그 수정"  # 추가 + 즉시 처리
    uv run python v/script/oaistodo_run.py              # 대기 중 전체 처리
    uv run python v/script/oaistodo_run.py status       # 상태 조회
    uv run python v/script/oaistodo_run.py add [text]   # 할 일 추가만
    uv run python v/script/oaistodo_run.py clear        # 완료 항목 아카이브
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

# Windows 콘솔 UTF-8 인코딩 설정
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

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


def get_history_file(sp: str = "00") -> Path:
    """Get history file path based on subproject context."""
    if sp == "00":
        return DOC_DIR / "d0010_history.md"
    else:
        # d20010_history.md for SP=02
        doc_num = int(sp) * 10000 + 10
        return DOC_DIR / f"d{doc_num}_history.md"


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

    # Find the '커스텀 Todo' or '대기 중' section using string finding (more robust than regex)
    section_map = {
        '## 커스텀 Todo': [],
        '### 대기 중': []
    }

    lines = content.split('\n')
    current_section = None
    table_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped in section_map:
            current_section = stripped
            continue

        if current_section:
            # Detect next section start
            if stripped.startswith('#') and stripped not in section_map:
                current_section = None
                continue

            # Collect table lines
            if stripped.startswith('|'):
                # Skip separators
                if '---' in stripped:
                    continue
                # Skip header
                if ' ID ' in stripped and ' 내용 ' in stripped:
                     continue
                table_lines.append(stripped)

    # Parse collected rows
    for line in table_lines:
        # Skip empty placeholder
        if '(대기 중인 작업 없음)' in line:
            continue

        # Parse actual todo rows: | ID | Date | Content | Priority | Note/Status |
        parts = [p.strip() for p in line.split('|')]
        # Expected format: ['', 'ID', 'Date', 'Content', 'Priority', 'Note', '']
        # Length should be at least 7 (including empty start/end)

        if len(parts) >= 6:
            todo_id = parts[1]
            # ID validation: allow T (Todo), C (Custom), or digits
            if re.match(r'^[TC]\d+$', todo_id) or todo_id.isdigit():
                 todos.append({
                    'id': todo_id,
                    'date': parts[2] if len(parts) > 2 else "",
                    'content': parts[3] if len(parts) > 3 else "",
                    'priority': parts[4] if len(parts) > 4 else "Medium",
                    'note': parts[5] if len(parts) > 5 else "-"
                })

    return todos


def get_processing_skill(tag: str, content: str) -> str:
    """
    Get the skill for processing based on tag and content.

    Strategy:
    1. Explicit Tag Matching
    2. Content Keyword Matching (fallback)
    3. Default to 'oaisdev' (General Purpose)
    """
    tag = tag.upper().strip()
    content = content.lower()

    # 1. Explicit Tag Mapping
    tag_map = {
        'FEATURE': 'oaisdev',
        'BUGFIX': 'oaisfix',
        'HOTFIX': 'oaisfix',
        'DOCS': 'oaisprd',    # oaisdoc is for skill mgmt, not general docs. oaisprd manages docs.
        'UPDATE': 'oaisenv',
        'CONFIG': 'oaisenv',
        'PPT': 'oaisppt',
        'PAPER': 'oaisreport', # Research paper writing
        'IMPROVE': 'oaisdev',  # Optimization often involves dev work
        'REFACTOR': 'oaisdev',
        'TEST': 'oaistest'
    }

    if tag in tag_map:
        return tag_map[tag]

    # 2. Content Analysis (if tag is MISC, unknown, or empty)
    if '문서' in content or 'doc' in content:
        return 'oaisprd'  # General documentation -> oaisprd
    if '에러' in content or 'error' in content or 'fix' in content or '수정' in content:
        return 'oaisfix'
    if '테스트' in content or 'test' in content:
        return 'oaistest'
    if 'ppt' in content or '발표' in content:
        return 'oaisppt'
    if '논문' in content or 'paper' in content or 'report' in content or '리포트' in content:
        return 'oaisreport'
    if '설정' in content or 'config' in content or 'env' in content:
        return 'oaisenv'

    # 3. Default Fallback
    return 'oaisdev'


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

    # Find Section and Table
    search_keywords = ["## 커스텀 Todo", "### 대기 중"]

    match = None
    used_header = ""

    for kw in search_keywords:
        pattern = re.escape(kw) + r'(?:[^|]*\n)*\n(\s*\| ID \| 등록일 \| 내용 \| 우선순위 \| (?:비고|상태) \|\s*\n\s*\|[-|]+\|\s*\n)'
        m = re.search(pattern, content)
        if m:
            match = m
            used_header = kw
            break

    if match:
        table_header_full = match.group(1)
        insert_pos = match.end()

        # Check if placeholder exists right after header
        rest_content = content[insert_pos:]
        placeholder_regex = r'^\| - \| - \| \([^)]+\) \| - \| - \|\s*\n'
        pmatch = re.match(placeholder_regex, rest_content)

        if pmatch:
            # Replace placeholder with new row
            new_content = content[:insert_pos] + new_row + "\n" + rest_content[pmatch.end():]
        else:
            # Append to table
            # Find end of table
            lines = rest_content.split('\n')
            table_rows = []
            for line in lines:
                if line.strip().startswith('|'):
                    table_rows.append(line)
                else:
                    break

            # Insert after last row
            last_row_end_pos = insert_pos + len('\n'.join(table_rows)) + (1 if table_rows else 0)
            if table_rows:
                # Add newline before new row if needed
                new_content = content[:last_row_end_pos] + "\n" + new_row + content[last_row_end_pos:]
            else:
                 # No rows yet (should invoke placeholder logic usually, but just in case)
                new_content = content[:insert_pos] + new_row + "\n" + content[insert_pos:]

    else:
        # If no section found, append '커스텀 Todo' section at the end
        if "## 커스텀 Todo" not in content:
            new_section = f"\n\n## 커스텀 Todo\n\n> `oaistodo add` 명령으로 추가된 항목.\n\n| ID | 등록일 | 내용 | 우선순위 | 비고 |\n|----|--------|------|---------|------|\n{new_row}\n"
            new_content = content + new_section
        else:
            # Section exists but table not found/matched?
            print("오류: Todo 테이블을 찾을 수 없습니다.")
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

    # Find 완료 (Resolved Issues) section
    # Try '해결된 이슈' (new standard), then '완료' (legacy)
    completed_headers = [
        r'### 해결된 이슈 \(Resolved Issues\)',
        r'### 해결된 이슈',
        r'### 완료',
        r'## 3. 해결된 이슈 \(Resolved Issues\)'
    ]

    match = None
    for header in completed_headers:
        pattern = header + r'(?:[^|]*\n)*\n(\s*\| ID \| 발생일 \| 분류 \| 내용 \| 해결일 \| 해결방법 \|\s*\n\s*\|[-|]+\|\s*\n)'
        m = re.search(pattern, new_content)
        if m:
            match = m
            break

    if match:
        insert_pos = match.end()
        # For d0004 Resolved Issues, columns: ID | 발생일 | 분류 | 내용 | 해결일 | 해결방법
        # We need to adapt the new row format.
        # Original todo (from oaistodo add): ID | Date | Content | Priority | Status/Note
        # Target: ID | Date | MISC (auto) | Content | Today | 자동 처리
        today = get_today()
        new_row = f"| {todo_id} | {today} | MISC | {todo_text} | {today} | 자동 처리 |\n"
        new_content = new_content[:insert_pos] + new_row + new_content[insert_pos:]
    else:
        # Try finding simpler table header if section header match failed specifically
        table_header = r'\| ID \| 발생일 \| 분류 \| 내용 \| 해결일 \| 해결방법 \|\s*\n\s*\|[-|]+\|\s*\n'
        match = re.search(table_header, new_content)
        if match:
             insert_pos = match.end()
             today = get_today()
             new_row = f"| {todo_id} | {today} | MISC | {todo_text} | {today} | 자동 처리 |\n"
             new_content = new_content[:insert_pos] + new_row + new_content[insert_pos:]

    return new_content


def parse_resolved_issues(content: str) -> list[dict]:
    """Parse resolved issues from d0004_todo.md."""
    issues = []

    # Find "해결된 이슈" section
    lines = content.split('\n')
    in_section = False
    table_started = False

    for line in lines:
        stripped = line.strip()

        # Detect section start
        if '해결된 이슈' in stripped and stripped.startswith('#'):
            in_section = True
            continue

        # Detect next section (exit)
        if in_section and stripped.startswith('#') and '해결된 이슈' not in stripped:
            break

        if in_section:
            # Skip table header and separator
            if '| ID |' in stripped or '|----' in stripped or '|----|' in stripped:
                table_started = True
                continue

            # Parse table rows
            if table_started and stripped.startswith('|'):
                # Skip placeholder
                if '해결된 이슈 없음' in stripped:
                    continue

                parts = [p.strip() for p in stripped.split('|')]
                # Expected: ['', ID, 발생일, 분류, 내용, 해결일, 해결방법, '']
                if len(parts) >= 7 and parts[1] and parts[1] != '-':
                    issues.append({
                        'id': parts[1],
                        'date': parts[2],
                        'category': parts[3],
                        'content': parts[4],
                        'resolved_date': parts[5],
                        'resolution': parts[6]
                    })

    return issues


def clear_resolved_issues(content: str) -> str:
    """Remove resolved issues from d0004_todo.md, leaving only placeholder."""
    # Find the section and replace table content with placeholder
    lines = content.split('\n')
    result_lines = []
    in_section = False
    table_started = False
    header_written = False

    for line in lines:
        stripped = line.strip()

        # Detect section start
        if '해결된 이슈' in stripped and stripped.startswith('#'):
            in_section = True
            result_lines.append(line)
            continue

        # Detect next section (exit)
        if in_section and stripped.startswith('#') and '해결된 이슈' not in stripped:
            in_section = False
            table_started = False

        if in_section:
            # Keep description lines (not table)
            if not stripped.startswith('|'):
                result_lines.append(line)
                continue

            # Keep table header and separator
            if '| ID |' in stripped or '|----' in stripped or '|----|' in stripped:
                result_lines.append(line)
                if '|----' in stripped or '|----|' in stripped:
                    # Add placeholder after separator
                    if not header_written:
                        result_lines.append('| - | - | - | (해결된 이슈 없음) | - | - |')
                        header_written = True
                        table_started = True
                continue

            # Skip data rows (they will be moved to history)
            if table_started:
                continue

        result_lines.append(line)

    return '\n'.join(result_lines)


def add_to_history_archive(content: str, issues: list[dict]) -> str:
    """Add resolved issues to d0010_history.md archive section."""
    if not issues:
        return content

    # Find "아카이브된 이슈" section
    lines = content.split('\n')
    result_lines = []
    in_section = False
    table_started = False
    placeholder_removed = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect section start
        if '아카이브된 이슈' in stripped and stripped.startswith('#'):
            in_section = True
            result_lines.append(line)
            continue

        # Detect next section (exit)
        if in_section and stripped.startswith('#') and '아카이브된 이슈' not in stripped:
            in_section = False
            table_started = False

        if in_section:
            # Keep description lines
            if not stripped.startswith('|'):
                result_lines.append(line)
                continue

            # Keep table header and separator
            if '| 원본 ID |' in stripped or '|----' in stripped or '|----|' in stripped or '|------' in stripped:
                result_lines.append(line)
                if '|----' in stripped or '|----|' in stripped or '|------' in stripped:
                    table_started = True
                    # Add new issues after separator
                    for issue in issues:
                        new_row = f"| {issue['id']} | {issue['category']} | {issue['content']} | {issue['resolved_date']} | {issue['resolution']} |"
                        result_lines.append(new_row)
                continue

            # Remove placeholder if exists
            if table_started and '아카이브된 이슈 없음' in stripped:
                placeholder_removed = True
                continue

            # Keep existing data rows
            result_lines.append(line)
            continue

        result_lines.append(line)

    return '\n'.join(result_lines)


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

    print("# oaistodo status - 대기 중인 Todo 목록\n")

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
    skill = get_processing_skill()
    for todo in high_priority:
        print(f"- [{todo['id']}] {todo['content']} → {skill} run")


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
    print("# oaistodo add - Todo 추가 완료\n")
    print(f"[OK] {new_id} 추가됨\n")
    print("| ID | 등록일 | 내용 | 우선순위 | 비고 |")
    print("|----|--------|------|---------|------|")
    print(f"| {new_id} | {get_today()} | {text} | {priority} | {note} |")
    print(f"\n파일: {todo_file.relative_to(PROJECT_ROOT)}")


def cmd_add_and_run(text: str, priority: str = "Medium", note: str = "-", sp: str = "00"):
    """Add a new todo item and immediately process it."""
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
    print(f"# oaistodo - Todo 추가 및 즉시 처리\n")
    print(f"## 1. 추가 완료\n")
    print(f"[OK] {new_id} 추가됨\n")
    print("| ID | 등록일 | 내용 | 우선순위 | 비고 |")
    print("|----|--------|------|---------|------|")
    print(f"| {new_id} | {get_today()} | {text} | {priority} | {note} |")

    # Determine skill
    tag = "MISC"
    match = re.match(r'^\[([A-Z]+)\]', text)
    if match:
        tag = match.group(1)
    skill = get_processing_skill(tag, text)

    print(f"\n## 2. 즉시 처리\n")
    print(f">>> 다음 업무를 처리하세요:")
    print(f"    내용: {text}")
    print(f"    권장 실행: {skill} run (또는 적절한 스킬 사용)")
    print(f"\n    완료 후 이 항목을 '완료' 섹션으로 이동하세요.")
    print(f"    - 항목 ID: {new_id}")
    print(f"    - 파일: {todo_file.relative_to(PROJECT_ROOT)}")


def cmd_clear(sp: str = "00", dry_run: bool = False):
    """Clear resolved issues from d0004_todo.md and archive to d0010_history.md."""
    todo_file = get_todo_file(sp)
    history_file = get_history_file(sp)

    if not todo_file.exists():
        print(f"오류: {todo_file} 파일이 존재하지 않습니다.")
        return

    if not history_file.exists():
        print(f"오류: {history_file} 파일이 존재하지 않습니다.")
        return

    # Read todo file
    todo_content = todo_file.read_text(encoding='utf-8')

    # Parse resolved issues
    issues = parse_resolved_issues(todo_content)

    print("# oaistodo clear - 완료 항목 아카이브\n")

    if not issues:
        print("[OK] 아카이브할 해결된 이슈가 없습니다.")
        return

    print(f"## 아카이브 대상: {len(issues)}개 항목\n")
    print("| ID | 분류 | 내용 | 해결일 | 해결방법 |")
    print("|-----|------|------|--------|---------|")
    for issue in issues:
        content_short = issue['content'][:40] + "..." if len(issue['content']) > 40 else issue['content']
        print(f"| {issue['id']} | {issue['category']} | {content_short} | {issue['resolved_date']} | {issue['resolution']} |")

    if dry_run:
        print("\n[DRY-RUN] 실제 이동은 수행하지 않습니다.")
        return

    # Read history file
    history_content = history_file.read_text(encoding='utf-8')

    # Add to history archive
    new_history_content = add_to_history_archive(history_content, issues)

    # Clear from todo file
    new_todo_content = clear_resolved_issues(todo_content)

    # Write files
    history_file.write_text(new_history_content, encoding='utf-8')
    todo_file.write_text(new_todo_content, encoding='utf-8')

    print(f"\n## 완료\n")
    print(f"- {len(issues)}개 항목 아카이브 완료")
    print(f"- 소스: {todo_file.relative_to(PROJECT_ROOT)}")
    print(f"- 대상: {history_file.relative_to(PROJECT_ROOT)}")


def cmd_run(sp: str = "00", dry_run: bool = False, max_items: int = 0):
    """Process pending todos automatically."""
    todo_file = get_todo_file(sp)

    if not todo_file.exists():
        print(f"오류: {todo_file} 파일이 존재하지 않습니다.")
        return

    content = todo_file.read_text(encoding='utf-8')
    todos = parse_waiting_todos(content)

    print("# oaistodo - 대기 중 업무 자동 처리\n")

    if not todos:
        print("[OK] 처리할 대기 중 업무가 없습니다.")
        return

    # Apply max_items limit
    if max_items > 0:
        todos = todos[:max_items]

    print(f"## 처리 대상: {len(todos)}개 항목\n")

    print(f"## 처리 대상: {len(todos)}개 항목\n")

    # Analyze skills for each item
    todo_actions = []
    for todo in todos:
        # Extract tag if present in content or use MISC column
        # In parsed todos, we don't have a separate 'tag' field from parsing function yet
        # The parsing function puts priority in 'priority' field.
        # But wait, standard format: | ID | Date | Tag | Content | Priority | Status |
        # Current parsing function handles: | ID | Date | Content | Priority | Note |
        # We need to adjust parsing logic if we want to use tags properly.
        # However, for now, let's assume the 'priority' or 'note' might contain tag info
        # OR just rely on content analysis.

        # Actually my previous edit to parse_waiting_todos was minimal.
        # Let's check parse_waiting_todos again. It assumes 5 columns.
        # Standard: | ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
        # Let's infer skill from content mainly for now, as column mapping might vary.

        # Try to find a tag at the start of content like "[DOCS] content"
        tag = "MISC"
        content_text = todo['content']
        match = re.match(r'^\[([A-Z]+)\]', content_text)
        if match:
            tag = match.group(1)

        skill = get_processing_skill(tag, content_text)
        todo_actions.append({'todo': todo, 'skill': skill})

    # List each todo with assigned skill
    for item in todo_actions:
        todo = item['todo']
        skill = item['skill']
        priority_marker = "[!]" if todo['priority'].lower() == 'high' else ""
        print(f"- {priority_marker}[{todo['id']}] {todo['content']}")
        print(f"  → 권장 스킬: {skill} run")

    if dry_run:
        print("\n[DRY-RUN] 실제 처리는 수행하지 않습니다.")
        return

    print("\n" + "="*50)
    print("## 처리 시작")
    print("="*50 + "\n")

    # Process each todo
    for i, todo in enumerate(todos, 1):
        print(f"\n### [{i}/{len(todos)}] {todo['id']}: {todo['content']}")

        # Output instruction for agent to process
        skill = todo_actions[i-1]['skill']
        print(f"\n>>> 다음 업무를 처리하세요:")
        print(f"    내용: {todo['content']}")
        print(f"    권장 실행: {skill} run (또는 적절한 스킬 사용)")
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
    if show_help_if_no_args("oaistodo", sys.argv[1:]):
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

    first_arg = args[0]
    subcommand = first_arg.lower()

    # Check if it's a known subcommand
    if subcommand == "status":
        cmd_status(sp)
        return

    if subcommand == "clear":
        cmd_clear(sp, dry_run)
        return

    if subcommand == "add":
        if len(args) < 2:
            print("사용법: oaistodo add [text]")
            print("\n예시:")
            print('  oaistodo add "로그인 페이지 수정"')
            print('  oaistodo add "API 문서화" --priority high')
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

    # If first arg is not a known subcommand, treat it as content for add+run
    # This handles: oaistodo "버그 수정"
    if first_arg and not first_arg.startswith("-"):
        text = first_arg
        priority = "Medium"
        note = "-"

        j = 1
        while j < len(args):
            if args[j] == "--priority" and j + 1 < len(args):
                priority = args[j + 1].capitalize()
                j += 2
            elif args[j] == "--note" and j + 1 < len(args):
                note = args[j + 1]
                j += 2
            else:
                j += 1

        cmd_add_and_run(text, priority, note, sp)
        return

    # Unknown or invalid - show help
    print("oaistodo - Todo 자동 처리 스킬")
    print("\n사용법:")
    print('  oaistodo "내용"       # 추가 + 즉시 처리')
    print("  oaistodo              # 대기 중 업무 전체 처리")
    print("  oaistodo status       # 대기 중 목록 표시")
    print('  oaistodo add [text]   # 할 일 추가만 (처리 안함)')
    print("  oaistodo clear        # 완료 항목 → d0010_history.md 아카이브")
    print("\n옵션:")
    print("  --sp N          서브프로젝트 지정")
    print("  --dry-run       실제 처리 없이 계획만 표시")
    print("  --max-items N   최대 처리 항목 수")
    print("\n예시:")
    print('  oaistodo "버그 수정"')
    print("  oaistodo --dry-run")
    print('  oaistodo add "새 기능 구현" --priority high')
    print("  oaistodo clear --dry-run")


if __name__ == "__main__":
    main()
