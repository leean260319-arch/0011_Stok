import os
import re
import sys
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PAPER_DIR = Path.cwd() / "02_paper"

def check_refs():
    print(f"DEBUG: Starting check_refs...", flush=True)
    print(f"DEBUG: Target directory: {PAPER_DIR}", flush=True)

    if not PAPER_DIR.exists():
        print(f"ERROR: Directory not found: {PAPER_DIR}", flush=True)
        return

    print("DEBUG: Listing directories...", flush=True)
    try:
        folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])
    except Exception as e:
        print(f"ERROR: Failed to list directories: {e}", flush=True)
        return

    total = 0
    ok = 0
    empty = 0
    missing = 0
    issues = []

    print(f"DEBUG: Found {len(folders)} folders. Scanning...", flush=True)

    for i, folder in enumerate(folders):
        if i % 50 == 0:
            print(f"DEBUG: Processing {i+1}/{len(folders)} - {folder.name}", flush=True)

        summaries = list(folder.glob("*_00_*서머리.md"))
        if not summaries:
            # print(f"DEBUG: No summary in {folder.name}", flush=True)
            continue

        summary_file = summaries[0]
        total += 1

        try:
            text = summary_file.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            issues.append(f"{folder.name}: Read Error ({e})")
            continue

        # Regex for Reference Header
        match = re.search(r'^##\s*(References?|참고\s*문헌|Reference|참고문헌)', text, re.MULTILINE | re.IGNORECASE)

        if match:
            start_idx = match.end()
            remainder = text[start_idx:].strip()
            next_header = re.search(r'^##\s+', remainder, re.MULTILINE)

            if next_header:
                content = remainder[:next_header.start()].strip()
            else:
                content = remainder

            if len(content) < 5:
                # Check for "References" followed by nothing or just whitespace
                empty += 1
                issues.append(f"[EMPTY] {folder.name}: Header found but content is empty")
            else:
                ok += 1
        else:
            missing += 1
            issues.append(f"[MISSING] {folder.name}: No Reference header found")

    print("-" * 40, flush=True)
    print(f"Total Papers Checked: {total}", flush=True)
    print(f"References Found: {ok}", flush=True)
    print(f"Empty Section: {empty}", flush=True)
    print(f"Missing Section: {missing}", flush=True)
    print("-" * 40, flush=True)

    if issues:
        print("Issues Found:", flush=True)
        for issue in issues[:20]:
            print(issue, flush=True)
        if len(issues) > 20:
            print(f"... and {len(issues)-20} more.", flush=True)

if __name__ == "__main__":
    check_refs()
