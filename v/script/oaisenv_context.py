#!/usr/bin/env python3
"""
oaisenv_context.py

oaisenv context 서브명령어 구현
- 토큰/컨텍스트 사용량 모니터링
- MCP memory 서버 연동
- 프로젝트 컨텍스트 파일 관리

Usage:
    uv run python v/script/oaisenv_context.py status
    uv run python v/script/oaisenv_context.py token
    uv run python v/script/oaisenv_context.py files
    uv run python v/script/oaisenv_context.py size
    uv run python v/script/oaisenv_context.py validate
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Windows console UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path.cwd()
CLAUDE_DIR = PROJECT_ROOT / ".claude"
V_DIR = PROJECT_ROOT / "v"

# Context file paths
CONTEXT_FILES = {
    "CLAUDE.md": PROJECT_ROOT / "CLAUDE.md",
    ".claude/settings.json": CLAUDE_DIR / "settings.json",
    ".claude/settings.local.json": CLAUDE_DIR / "settings.local.json",
    ".claude/CLAUDE.md": CLAUDE_DIR / "CLAUDE.md",
}

# Token estimation (rough: 1 token ~ 4 chars for English, ~2 chars for Korean)
CHARS_PER_TOKEN_EN = 4
CHARS_PER_TOKEN_KO = 2

# Memory file for local persistence (backup when MCP unavailable)
MEMORY_FILE = PROJECT_ROOT / "tmp" / "context_memory.json"


# ============================================================
# Token Estimation
# ============================================================

def estimate_tokens(text: str) -> int:
    """Estimate token count for text (rough approximation)."""
    if not text:
        return 0

    # Count Korean characters
    korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7af' or '\u1100' <= c <= '\u11ff')
    other_chars = len(text) - korean_chars

    # Estimate tokens
    korean_tokens = korean_chars / CHARS_PER_TOKEN_KO
    other_tokens = other_chars / CHARS_PER_TOKEN_EN

    return int(korean_tokens + other_tokens)


def get_file_token_size(file_path: Path) -> tuple[int, int]:
    """Get file size in bytes and estimated tokens."""
    if not file_path.exists():
        return 0, 0

    try:
        content = file_path.read_text(encoding='utf-8')
        return len(content), estimate_tokens(content)
    except Exception:
        return file_path.stat().st_size, 0


# ============================================================
# Context File Management
# ============================================================

def collect_context_files() -> list[dict]:
    """Collect all context-related files with their sizes."""
    files = []

    # Main context files
    for name, path in CONTEXT_FILES.items():
        if path.exists():
            size_bytes, tokens = get_file_token_size(path)
            files.append({
                "name": name,
                "path": str(path),
                "exists": True,
                "size_bytes": size_bytes,
                "tokens": tokens,
            })
        else:
            files.append({
                "name": name,
                "path": str(path),
                "exists": False,
                "size_bytes": 0,
                "tokens": 0,
            })

    # .claude/agents/
    agents_dir = CLAUDE_DIR / "agents"
    if agents_dir.exists():
        for f in agents_dir.glob("*.md"):
            size_bytes, tokens = get_file_token_size(f)
            files.append({
                "name": f".claude/agents/{f.name}",
                "path": str(f),
                "exists": True,
                "size_bytes": size_bytes,
                "tokens": tokens,
            })

    # .claude/commands/
    commands_dir = CLAUDE_DIR / "commands"
    if commands_dir.exists():
        for f in commands_dir.glob("*.md"):
            size_bytes, tokens = get_file_token_size(f)
            files.append({
                "name": f".claude/commands/{f.name}",
                "path": str(f),
                "exists": True,
                "size_bytes": size_bytes,
                "tokens": tokens,
            })

    # v/guide/
    guide_dir = V_DIR / "guide"
    if guide_dir.exists():
        for f in guide_dir.glob("*.md"):
            size_bytes, tokens = get_file_token_size(f)
            files.append({
                "name": f"v/guide/{f.name}",
                "path": str(f),
                "exists": True,
                "size_bytes": size_bytes,
                "tokens": tokens,
            })

    return files


def validate_context_files() -> list[dict]:
    """Validate context files for issues."""
    issues = []

    # Check CLAUDE.md exists
    claude_md = PROJECT_ROOT / "CLAUDE.md"
    if not claude_md.exists():
        issues.append({
            "severity": "ERROR",
            "file": "CLAUDE.md",
            "message": "CLAUDE.md not found in project root",
        })

    # Check .claude directory
    if not CLAUDE_DIR.exists():
        issues.append({
            "severity": "ERROR",
            "file": ".claude/",
            "message": ".claude directory not found",
        })

    # Check settings.json
    settings_json = CLAUDE_DIR / "settings.json"
    if settings_json.exists():
        try:
            content = settings_json.read_text(encoding='utf-8')
            json.loads(content)
        except json.JSONDecodeError as e:
            issues.append({
                "severity": "ERROR",
                "file": ".claude/settings.json",
                "message": f"Invalid JSON: {e}",
            })

    # Check for large files (>50K tokens)
    for f in collect_context_files():
        if f["tokens"] > 50000:
            issues.append({
                "severity": "WARNING",
                "file": f["name"],
                "message": f"Large file ({f['tokens']:,} tokens) may consume significant context",
            })

    return issues


# ============================================================
# Memory Management (Local + MCP)
# ============================================================

def load_local_memory() -> dict:
    """Load memory from local file."""
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding='utf-8'))
        except Exception:
            return {"entities": [], "relations": []}
    return {"entities": [], "relations": []}


def save_local_memory(memory: dict) -> None:
    """Save memory to local file."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding='utf-8')


def add_entity(name: str, entity_type: str, observations: list[str]) -> dict:
    """Add entity to memory."""
    memory = load_local_memory()

    # Check if entity exists
    for entity in memory["entities"]:
        if entity["name"] == name:
            entity["observations"].extend(observations)
            entity["updated"] = datetime.now().isoformat()
            save_local_memory(memory)
            return {"status": "updated", "entity": entity}

    # Add new entity
    entity = {
        "name": name,
        "type": entity_type,
        "observations": observations,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
    }
    memory["entities"].append(entity)
    save_local_memory(memory)
    return {"status": "created", "entity": entity}


def list_entities() -> list[dict]:
    """List all entities in memory."""
    memory = load_local_memory()
    return memory.get("entities", [])


def clear_memory() -> None:
    """Clear all memory."""
    save_local_memory({"entities": [], "relations": []})


# ============================================================
# Commands
# ============================================================

def cmd_status():
    """Show overall context status."""
    print("# oaisenv context status\n")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. Token summary
    files = collect_context_files()
    total_tokens = sum(f["tokens"] for f in files)
    total_bytes = sum(f["size_bytes"] for f in files)

    print("## 1. Context Token Summary\n")
    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| Total Files | {len([f for f in files if f['exists']])} |")
    print(f"| Total Size | {total_bytes:,} bytes |")
    print(f"| Estimated Tokens | {total_tokens:,} |")
    print()

    # 2. Memory status
    entities = list_entities()
    print("## 2. Memory Status\n")
    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| Saved Entities | {len(entities)} |")
    print(f"| Memory File | {'Exists' if MEMORY_FILE.exists() else 'Not Created'} |")
    print()

    # 3. Validation
    issues = validate_context_files()
    print("## 3. Validation\n")
    if issues:
        print(f"| Severity | File | Issue |")
        print(f"|----------|------|-------|")
        for issue in issues:
            print(f"| {issue['severity']} | {issue['file']} | {issue['message']} |")
    else:
        print("[OK] No issues found")
    print()


def cmd_token():
    """Show token usage estimation."""
    print("# oaisenv context token\n")

    files = collect_context_files()
    existing_files = [f for f in files if f["exists"]]

    # Sort by tokens descending
    existing_files.sort(key=lambda x: x["tokens"], reverse=True)

    print("## Context Files Token Estimation\n")
    print("| File | Size | Tokens |")
    print("|------|------|--------|")

    total_tokens = 0
    for f in existing_files:
        size_kb = f["size_bytes"] / 1024
        print(f"| {f['name']} | {size_kb:.1f} KB | {f['tokens']:,} |")
        total_tokens += f["tokens"]

    print(f"| **Total** | | **{total_tokens:,}** |")
    print()

    # Context window estimate
    print("## Context Window Usage\n")
    context_window = 200000  # Claude's context window
    usage_pct = (total_tokens / context_window) * 100

    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| Context Window | {context_window:,} tokens |")
    print(f"| Used by Files | {total_tokens:,} tokens ({usage_pct:.1f}%) |")
    print(f"| Remaining | {context_window - total_tokens:,} tokens |")

    if usage_pct > 50:
        print(f"\n[WARN] Context files using >{usage_pct:.0f}% of context window")


def cmd_files():
    """List context files."""
    print("# oaisenv context files\n")

    files = collect_context_files()

    print("## Context Files\n")
    print("| Status | File | Size |")
    print("|--------|------|------|")

    for f in files:
        status = "OK" if f["exists"] else "MISSING"
        size = f"{f['size_bytes']:,} bytes" if f["exists"] else "-"
        print(f"| {status} | {f['name']} | {size} |")
    print()


def cmd_size():
    """Show file sizes with token estimates."""
    print("# oaisenv context size\n")

    files = collect_context_files()
    existing = [f for f in files if f["exists"]]
    existing.sort(key=lambda x: x["tokens"], reverse=True)

    print("## File Sizes (by token count)\n")
    print("| File | Bytes | Tokens | % |")
    print("|------|-------|--------|---|")

    total_tokens = sum(f["tokens"] for f in existing)

    for f in existing:
        pct = (f["tokens"] / total_tokens * 100) if total_tokens > 0 else 0
        print(f"| {f['name']} | {f['size_bytes']:,} | {f['tokens']:,} | {pct:.1f}% |")

    print(f"| **Total** | | **{total_tokens:,}** | 100% |")


def cmd_validate():
    """Validate context files."""
    print("# oaisenv context validate\n")

    issues = validate_context_files()

    if not issues:
        print("[OK] All context files valid\n")
        return

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARNING"]

    print(f"## Issues Found: {len(errors)} errors, {len(warnings)} warnings\n")

    if errors:
        print("### Errors\n")
        for issue in errors:
            print(f"- **{issue['file']}**: {issue['message']}")
        print()

    if warnings:
        print("### Warnings\n")
        for issue in warnings:
            print(f"- **{issue['file']}**: {issue['message']}")


def cmd_save(message: str):
    """Save information to memory."""
    print("# oaisenv context save\n")

    if not message:
        print("[ERROR] Message required: oaisenv context save \"your message\"")
        return

    # Parse message to create entity
    result = add_entity(
        name=f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        entity_type="note",
        observations=[message]
    )

    print(f"[OK] Saved to memory")
    print(f"- Status: {result['status']}")
    print(f"- Name: {result['entity']['name']}")
    print(f"- Message: {message}")


def cmd_load():
    """Load and display memory contents."""
    print("# oaisenv context load\n")

    entities = list_entities()

    if not entities:
        print("No entities in memory.\n")
        print("Use `oaisenv context save \"message\"` to save information.")
        return

    print(f"## Memory Entities ({len(entities)})\n")

    for entity in entities:
        print(f"### {entity['name']} ({entity['type']})")
        print(f"- Created: {entity.get('created', 'N/A')}")
        print(f"- Updated: {entity.get('updated', 'N/A')}")
        print("- Observations:")
        for obs in entity.get('observations', []):
            print(f"  - {obs}")
        print()


def cmd_list():
    """List saved entities."""
    print("# oaisenv context list\n")

    entities = list_entities()

    if not entities:
        print("No entities in memory.")
        return

    print("| Name | Type | Observations | Updated |")
    print("|------|------|--------------|---------|")

    for entity in entities:
        obs_count = len(entity.get('observations', []))
        updated = entity.get('updated', 'N/A')[:10]
        print(f"| {entity['name']} | {entity['type']} | {obs_count} | {updated} |")


def cmd_clear():
    """Clear memory."""
    print("# oaisenv context clear\n")

    clear_memory()
    print("[OK] Memory cleared")


def cmd_help():
    """Show help."""
    print("# oaisenv context - Context Management\n")
    print("## Commands\n")
    print("| Command | Description |")
    print("|---------|-------------|")
    print("| `context status` | Overall context status |")
    print("| `context token` | Token usage estimation |")
    print("| `context files` | List context files |")
    print("| `context size` | File sizes with tokens |")
    print("| `context validate` | Validate context files |")
    print("| `context save \"msg\"` | Save to memory |")
    print("| `context load` | Load from memory |")
    print("| `context list` | List memory entities |")
    print("| `context clear` | Clear memory |")


def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    subcommand = sys.argv[1].lower()

    if subcommand == "status":
        cmd_status()
    elif subcommand == "token":
        cmd_token()
    elif subcommand == "files":
        cmd_files()
    elif subcommand == "size":
        cmd_size()
    elif subcommand == "validate":
        cmd_validate()
    elif subcommand == "save":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        cmd_save(message)
    elif subcommand == "load":
        cmd_load()
    elif subcommand == "list":
        cmd_list()
    elif subcommand == "clear":
        cmd_clear()
    elif subcommand in ["help", "-h", "--help"]:
        cmd_help()
    else:
        print(f"[ERROR] Unknown command: {subcommand}")
        cmd_help()


if __name__ == "__main__":
    main()
