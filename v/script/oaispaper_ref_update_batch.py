import os
import re
import sys
import argparse
from pathlib import Path

# Force UTF-8 for output
sys.stdout.reconfigure(encoding='utf-8')

# Write minimal output to file to debug
LOG_FILE = Path("tmp/ref_update_minimal.txt")

def log(msg):
    # Also print to stdout for interactive use
    print(msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except:
        pass

PAPER_DIR = Path("02_paper")

def extract_references_from_english_full(eng_file):
    try:
        content = eng_file.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return None

    match = re.search(r'^##\s*(References?|Bibliography|참고\s*문헌|참고문헌)', content, re.MULTILINE | re.IGNORECASE)

    if match:
        start_pos = match.end()
        remainder = content[start_pos:].strip()
        return remainder

    match_uc = re.search(r'\nREFERENCES\s*\n', content)
    if match_uc:
        return content[match_uc.end():].strip()

    return None

def update_summary_with_refs(folder_path, dry_run=False):
    summary_files = list(folder_path.glob("*_00_*서머리.md"))
    eng_files = list(folder_path.glob("*_03_*전문(영어).md"))

    if not summary_files:
        return "No summary file"

    summary_file = summary_files[0]

    if not eng_files:
        return "No English full text"

    eng_file = eng_files[0]

    try:
        summary_content = summary_file.read_text(encoding='utf-8')
    except:
        return "Read Error (Summary)"

    if re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', summary_content, re.MULTILINE | re.IGNORECASE):
        match = re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', summary_content, re.MULTILINE | re.IGNORECASE)
        start = match.end()
        end_match = re.search(r'^##\s+', summary_content[start:], re.MULTILINE)
        content = summary_content[start:start+end_match.start()] if end_match else summary_content[start:]
        if len(content.strip()) > 50:
            return "Skipped (Already exists)"

    refs = extract_references_from_english_full(eng_file)
    if not refs or len(refs) < 50:
        return "Extraction Failed or Too Short"

    keyword_match = re.search(r'^##\s*키워드', summary_content, re.MULTILINE)

    new_section = f"\n\n## 참고문헌\n{refs}\n"

    if keyword_match:
        insert_pos = keyword_match.start()
        new_content = summary_content[:insert_pos] + new_section + "\n" + summary_content[insert_pos:]
    else:
        new_content = summary_content + new_section

    if not dry_run:
        summary_file.write_text(new_content, encoding='utf-8')
        return "Updated"
    else:
        return "Updated (Dry Run)"

def main():
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    LOG_FILE.parent.mkdir(exist_ok=True)

    if not PAPER_DIR.exists():
        log(f"Error: {PAPER_DIR} not found.")
        return

    folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    updated = 0
    skipped = 0
    failed = 0

    log(f"Processing {len(folders)} folders...")

    for folder in folders:
        result = update_summary_with_refs(folder, dry_run=False) # Direct execution for now
        log(f"[{result}] {folder.name}")

        if "Updated" in result:
            updated += 1
        elif "Skipped" in result:
            skipped += 1
        else:
            failed += 1

    log("-" * 30)
    log(f"Total: {len(folders)}")
    log(f"Updated: {updated}")
    log(f"Skipped: {skipped}")
    log(f"Failed/NoData: {failed}")

if __name__ == "__main__":
    main()
