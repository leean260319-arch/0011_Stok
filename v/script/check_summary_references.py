import os
import re
from pathlib import Path

PAPER_DIR = Path(r"c:\Users\oaiskoo\home\3_code\0002_paper\02_paper")

def check_summary_references():
    total_files = 0
    ref_found_count = 0
    ref_empty_count = 0
    no_ref_section_count = 0

    error_details = []

    print(f"Checking summaries in {PAPER_DIR}...")

    if not PAPER_DIR.exists():
        print("Error: Paper directory not found.")
        return

    folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    for folder in folders:
        summary_files = list(folder.glob("*_00_*서머리.md"))

        if not summary_files:
            continue

        summary_file = summary_files[0]
        total_files += 1

        try:
            content = summary_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {summary_file.name}: {e}")
            continue

        # Check for References section
        # Patterns: ## References, ## 참고문헌, ## Reference, ## 참고 문헌
        ref_match = re.search(r'##\s*(References?|참고\s*문헌)', content, re.IGNORECASE)

        if ref_match:
            # Check content after the header
            start_pos = ref_match.end()
            # Find next header or end of file
            next_header = re.search(r'\n##\s+', content[start_pos:])

            if next_header:
                ref_content = content[start_pos:start_pos + next_header.start()].strip()
            else:
                ref_content = content[start_pos:].strip()

            if len(ref_content) > 10: # Minimal length check
                ref_found_count += 1
            else:
                ref_empty_count += 1
                error_details.append(f"[EMPTY] {folder.name}: References section exists but looks empty.")
        else:
            no_ref_section_count += 1
            error_details.append(f"[MISSING] {folder.name}: No 'References' or '참고문헌' section found.")

    print("\n" + "="*50)
    print("Summary Reference Check Report")
    print("="*50)
    print(f"Total Summaries Checked: {total_files}")
    print(f"References Found & Content OK: {ref_found_count}")
    print(f"References Section Empty: {ref_empty_count}")
    print(f"References Section Missing: {no_ref_section_count}")
    print("="*50)

    if error_details:
        print("\nDetails of Issues:")
        for err in error_details:
            print(err)
    else:
        print("\nAll summaries seem to have populated reference sections.")

if __name__ == "__main__":
    check_summary_references()
