import argparse
import sys
import re
from datetime import datetime
from pathlib import Path

# Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = PROJECT_ROOT / "02_paper"
LOG_FILE = PROJECT_ROOT / "tmp" / "ref_update_run.log"

def log(msg):
    # Print to stdout
    print(msg, flush=True)
    # Write to file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception as e:
        print(f"Log write failed: {e}")

def do_ref_update(dry_run=False, folder_name=None):
    sys.stdout.reconfigure(encoding='utf-8')
    LOG_FILE.parent.mkdir(exist_ok=True)
    if LOG_FILE.exists():
        LOG_FILE.unlink() # New run, clear log

    log(f"[{datetime.now()}] Running oaispaper ref-update (standalone)...")
    log(f"Target Directory: {PAPER_DIR}")

    if not PAPER_DIR.exists():
        log(f"Error: {PAPER_DIR} does not exist.")
        return

    if folder_name:
        target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir() and d.name == folder_name]
    else:
        target_folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    log(f"Processing {len(target_folders)} folders...")

    updated = 0
    skipped = 0
    failed = 0

    for i, folder in enumerate(target_folders):
        if i % 20 == 0:
            log(f"Progress: {i}/{len(target_folders)}... (Current: {folder.name})")

        summary_files = list(folder.glob("*_00_*서머리.md"))
        eng_files = list(folder.glob("*_03_*전문(영어).md"))

        if not summary_files:
            failed += 1
            # log(f"- [FAILED] {folder.name}: No summary")
            continue

        summary_file = summary_files[0]

        if not eng_files:
            failed += 1
            # log(f"- [FAILED] {folder.name}: No English full text")
            continue

        eng_file = eng_files[0]

        try:
            summary_content = summary_file.read_text(encoding='utf-8')
        except:
            failed += 1
            log(f"- [FAILED] {folder.name}: Read error")
            continue

        # Check if References already exists and is substantial
        if re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', summary_content, re.MULTILINE | re.IGNORECASE):
            match = re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', summary_content, re.MULTILINE | re.IGNORECASE)
            start = match.end()
            end_match = re.search(r'^##\s+', summary_content[start:], re.MULTILINE)
            content = summary_content[start:start+end_match.start()] if end_match else summary_content[start:]

            if len(content.strip()) > 50:
                skipped += 1
                continue

        # Extract refs from English file
        try:
            eng_content = eng_file.read_text(encoding='utf-8', errors='ignore')
        except:
            failed += 1
            continue

        match = re.search(r'^##\s*(References?|Bibliography|참고\s*문헌|참고문헌)', eng_content, re.MULTILINE | re.IGNORECASE)
        refs = None
        if match:
            start_pos = match.end()
            refs = eng_content[start_pos:].strip()
        else:
            match_uc = re.search(r'\nREFERENCES\s*\n', eng_content)
            if match_uc:
                refs = eng_content[match_uc.end():].strip()

        if not refs or len(refs) < 50:
            failed += 1
            log(f"- [Ref Missing] {folder.name}: Could not extract references")
            continue

        # Update summary
        keyword_match = re.search(r'^##\s*키워드', summary_content, re.MULTILINE)
        new_section = f"\n\n## 참고문헌\n{refs}\n"

        if keyword_match:
            insert_pos = keyword_match.start()
            new_content = summary_content[:insert_pos] + new_section + "\n" + summary_content[insert_pos:]
        else:
            new_content = summary_content + new_section

        if not dry_run:
            try:
                summary_file.write_text(new_content, encoding='utf-8')
                updated += 1
                log(f"- [UPDATED] {folder.name}")
            except Exception as e:
                log(f"- [Write Error] {folder.name}: {e}")
                failed += 1
        else:
            updated += 1
            log(f"- [UPDATED] {folder.name} (Dry Run)")

    log("-" * 30)
    log(f"Result - Total: {len(target_folders)}")
    log(f"Updated: {updated}")
    log(f"Skipped: {skipped}")
    log(f"Failed: {failed}")
    log(f"[{datetime.now()}] Finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--folder', type=str)
    args = parser.parse_args()

    do_ref_update(args.dry_run, args.folder)
