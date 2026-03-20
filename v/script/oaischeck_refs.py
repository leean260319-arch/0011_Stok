import os
import re
from pathlib import Path

# Use relative path if CWD is project root
PAPER_DIR = Path("02_paper")

def check_refs():
    print(f"Checking Summaries in {PAPER_DIR.absolute()}")
    if not PAPER_DIR.exists():
        print("02_paper not found!")
        return

    # Count
    total = 0
    ok = 0
    empty = 0
    missing = 0

    issues = []

    # Iterate folders
    # Sort for consistent output
    folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    for folder in folders:
        # Find summary
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

        # Regex for Reference Header
        # Looking for ## References/참고문헌 at start of line
        # Use simple search first
        match = re.search(r'^##\s*(References?|참고\s*문헌|Reference)', text, re.MULTILINE | re.IGNORECASE)

        if match:
            # Check if there is content
            start_idx = match.end()
            remainder = text[start_idx:].strip()

            # Check if there is another header immediately or end of file
            next_header = re.search(r'^##\s+', remainder, re.MULTILINE)

            if next_header:
                content = remainder[:next_header.start()].strip()
            else:
                content = remainder

            if len(content) < 5: # Arbitrary small threshold
                empty += 1
                issues.append(f"[EMPTY] {folder.name}: Header found but content is empty")
            else:
                ok += 1
        else:
            missing += 1
            issues.append(f"[MISSING] {folder.name}: No Reference header found")

    # Verify extraction success in the content
    # Look for [1], (Author, Year) etc within the content?
    # User asked "properly extracted". Usually this means the list exists.

    print("-" * 40)
    print(f"Total Papers Checked: {total}")
    print(f"References OK: {ok}")
    print(f"Empty Section: {empty}")
    print(f"Missing Section: {missing}")
    print("-" * 40)

    if issues:
        print("Issues Found:")
        for i in issues[:20]:
            print(i)
        if len(issues) > 20:
            print(f"... and {len(issues)-20} more.")

if __name__ == "__main__":
    check_refs()
