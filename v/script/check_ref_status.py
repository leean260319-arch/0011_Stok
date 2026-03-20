import os
import re
from pathlib import Path
import sys

# Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = PROJECT_ROOT / "02_paper"
REPORT_FILE = PROJECT_ROOT / "doc" / "reference_status_report.txt"

def check_references():
    sys.stdout.reconfigure(encoding='utf-8')
    print("Checking reference status in summaries...", flush=True)

    if not PAPER_DIR.exists():
        print(f"Error: {PAPER_DIR} does not exist.", flush=True)
        return

    folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    total = 0
    has_ref = 0
    missing_ref = 0
    missing_list = []

    for folder in folders:
        summary_files = list(folder.glob("*_00_*서머리.md"))

        if not summary_files:
            continue

        summary_file = summary_files[0]
        total += 1

        try:
            content = summary_file.read_text(encoding='utf-8')
        except:
            continue

        # Check for References section
        if re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', content, re.MULTILINE | re.IGNORECASE):
            # strict check: content length
            match = re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', content, re.MULTILINE | re.IGNORECASE)
            start = match.end()
            end_match = re.search(r'^##\s+', content[start:], re.MULTILINE)
            ref_content = content[start:start+end_match.start()] if end_match else content[start:]

            if len(ref_content.strip()) > 10:
                has_ref += 1
            else:
                missing_ref += 1
                missing_list.append(f"{folder.name} (Empty Section)")
        else:
            missing_ref += 1
            missing_list.append(f"{folder.name} (Missing Header)")

    # Generate Report
    lines = []
    lines.append("## Summary Reference Status Report")
    lines.append(f"Total Summaries Checked: {total}")
    lines.append(f"With References: {has_ref} ({(has_ref/total)*100:.1f}%)")
    lines.append(f"Missing References: {missing_ref} ({(missing_ref/total)*100:.1f}%)")
    lines.append("-" * 30)

    if missing_list:
        lines.append("\n### Missing References List")
        for item in missing_list[:50]: # Show top 50
            lines.append(f"- {item}")
        if len(missing_list) > 50:
            lines.append(f"... and {len(missing_list) - 50} more.")
    else:
        lines.append("\nAll summaries have references!")

    report_content = "\n".join(lines)
    print(report_content)

    REPORT_FILE.write_text(report_content, encoding='utf-8')
    print(f"\nReport saved to {REPORT_FILE}")

if __name__ == "__main__":
    check_references()
