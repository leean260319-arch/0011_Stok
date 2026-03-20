import os
import re
import sys
import argparse
from pathlib import Path

# Force UTF-8 for output
sys.stdout.reconfigure(encoding='utf-8')

PAPER_DIR = Path("02_paper")

def extract_references_from_english_full(eng_file):
    """
    Extracts the references section from the English full text file.
    """
    try:
        content = eng_file.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return None

    # Try to find common Reference headers
    # Case insensitive search
    match = re.search(r'^##\s*(References?|Bibliography|참고\s*문헌)', content, re.MULTILINE | re.IGNORECASE)

    if match:
        start_pos = match.end()
        remainder = content[start_pos:].strip()

        # Check if there are any subsequent headers (Appendices might come after)
        # But usually References are at the end.
        # Sometimes "Appendix" follows.

        # Simple heuristic: take everything until next H1 or H2
        # But H2 ## might be subsections of References or Appendices
        # We'll take everything for now, as truncation is risky.

        return remainder

    # Fallback: Search for "REFERENCES" at start of line if standard markdown header is missing
    match_uc = re.search(r'\nREFERENCES\s*\n', content)
    if match_uc:
        return content[match_uc.end():].strip()

    return None

def update_summary_with_refs(folder_path, dry_run=False):
    """
    Updates the summary file in the folder with references extracted from the English full text.
    """
    summary_files = list(folder_path.glob("*_00_*서머리.md"))
    eng_files = list(folder_path.glob("*_03_*전문(영어).md"))

    if not summary_files:
        return "No summary file"

    summary_file = summary_files[0]

    if not eng_files:
        return "No English full text"

    eng_file = eng_files[0]

    # 1. Check if Summary already has References
    try:
        summary_content = summary_file.read_text(encoding='utf-8')
    except:
        return "Read Error (Summary)"

    if re.search(r'^##\s*(References?|참고\s*문헌)', summary_content, re.MULTILINE | re.IGNORECASE):
        # Additional check: is it empty?
        match = re.search(r'^##\s*(References?|참고\s*문헌)', summary_content, re.MULTILINE | re.IGNORECASE)
        start = match.end()
        end_match = re.search(r'^##\s+', summary_content[start:], re.MULTILINE)

        content = summary_content[start:start+end_match.start()] if end_match else summary_content[start:]
        if len(content.strip()) > 50:
            return "Skipped (Already exists)"

    # 2. Extract References from English Full Text
    refs = extract_references_from_english_full(eng_file)
    if not refs or len(refs) < 50:
        return "Extraction Failed or Too Short"

    # 3. Append to Summary
    # Insert before ## 키워드 if exists, otherwise append

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
    parser = argparse.ArgumentParser(description="Extract and add references to summaries")
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files")
    parser.add_argument("--folder", type=str, help="Target specific folder name")
    args = parser.parse_args()

    if not PAPER_DIR.exists():
        print(f"Error: {PAPER_DIR} not found.")
        return

    folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    total = 0
    updated = 0
    skipped = 0
    failed = 0

    if args.folder:
        target_folders = [d for d in folders if d.name == args.folder]
        if not target_folders:
            print(f"Folder {args.folder} not found.")
            return
        folders = target_folders

    print(f"Processing {len(folders)} folders...")

    for folder in folders:
        result = update_summary_with_refs(folder, args.dry_run)
        print(f"[{result}] {folder.name}")

        if "Updated" in result:
            updated += 1
        elif "Skipped" in result:
            skipped += 1
        else:
            failed += 1

    print("-" * 30)
    print(f"Total: {len(folders)}")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print(f"Failed/NoData: {failed}")

if __name__ == "__main__":
    main()
