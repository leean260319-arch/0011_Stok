import os
import re
import sys
from pathlib import Path

# Write to a non-ignored location
OUTPUT_FILE = Path("doc/check_refs_report.txt")

def log(msg):
    # print(msg) # Print might be lost
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

PAPER_DIR = Path.cwd() / "02_paper"

def check_refs():
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    log(f"DEBUG: Starting check_refs...")

    if not PAPER_DIR.exists():
        log(f"ERROR: Directory not found: {PAPER_DIR}")
        return

    try:
        folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])
    except Exception as e:
        log(f"ERROR: Failed to list directories: {e}")
        return

    log(f"DEBUG: Found {len(folders)} folders.")

    total = 0
    ok = 0
    empty = 0
    missing = 0
    issues = []

    for folder in folders:
        summaries = list(folder.glob("*_00_*서머리.md"))
        if not summaries:
            continue

        summary_file = summaries[0]
        total += 1

        try:
            text = summary_file.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            issues.append(f"{folder.name}: Read Error ({e})")
            continue

        match = re.search(r'^##\s*(References?|참고\s*문헌|Reference|참고문헌)', text, re.MULTILINE | re.IGNORECASE)

        if match:
            start_idx = match.end()
            remainder = text[start_idx:].strip()
            # Check length or next header
            if len(remainder) < 5:
                # But wait, next header?
                empty += 1
                issues.append(f"[EMPTY] {folder.name}")
            else:
                next_header = re.search(r'^##\s+', remainder, re.MULTILINE)
                if next_header:
                    content = remainder[:next_header.start()].strip()
                    if len(content) < 5:
                        empty += 1
                        issues.append(f"[EMPTY] {folder.name}")
                    else:
                        ok += 1
                else:
                    # No next header, remainder is content
                    ok += 1
        else:
            missing += 1
            issues.append(f"[MISSING] {folder.name}")

    log("-" * 40)
    log(f"Total Papers Checked: {total}")
    log(f"References Found: {ok}")
    log(f"Empty Section: {empty}")
    log(f"Missing Section: {missing}")
    log("-" * 40)

    if issues:
        log("Issues Found:")
        for issue in issues[:50]:
            log(issue)

if __name__ == "__main__":
    check_refs()
