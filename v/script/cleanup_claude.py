import os
import shutil
from pathlib import Path

CLAUDE_DIR = Path(".claude")
ARCHIVE_DIR = CLAUDE_DIR / "archive"

FILES_TO_MOVE = [
    "ORCHESTRATOR.md",
    "PERSONAS.md",
    "MODES.md",
    "PRINCIPLES.md",
    "MCP.md",
    "FLAGS.md",
    "TM_COMMANDS_GUIDE.md"
]

def main():
    if not CLAUDE_DIR.exists():
        print(f"Error: {CLAUDE_DIR} does not exist.")
        return

    # Create archive dir
    try:
        ARCHIVE_DIR.mkdir(exist_ok=True)
        print(f"Created/Verified {ARCHIVE_DIR}")
    except Exception as e:
        print(f"Failed to create archive dir: {e}")
        return

    # Move files
    for fname in FILES_TO_MOVE:
        src = CLAUDE_DIR / fname
        dst = ARCHIVE_DIR / fname

        if src.exists():
            try:
                shutil.move(str(src), str(dst))
                print(f"Moved {fname} to archive.")
            except Exception as e:
                print(f"Failed to move {fname}: {e}")
        else:
            print(f"Skipped {fname} (not found)")

if __name__ == "__main__":
    main()
