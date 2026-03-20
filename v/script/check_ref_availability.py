import re
import sys
import requests
from pathlib import Path

# Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = PROJECT_ROOT / "02_paper"

def check_ref_availability(folder_name=None):
    sys.stdout.reconfigure(encoding='utf-8')
    print("Checking reference availability...", flush=True)

    if folder_name:
        target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir() and d.name == folder_name]
    else:
        # Default to first one for demo
        target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir()]
        target_folders = target_folders[:1]

    if not target_folders:
        print("No papers found.")
        return

    folder = target_folders[0]
    print(f"Target Paper: {folder.name}", flush=True)

    eng_files = list(folder.glob("*_03_*전문(영어).md"))
    if not eng_files:
        print("English full text not found.")
        return

    content = eng_files[0].read_text(encoding='utf-8', errors='ignore')

    # Extract References Section
    match = re.search(r'^##\s*(References?|Bibliography|참고\s*문헌|참고문헌)', content, re.MULTILINE | re.IGNORECASE)
    if not match:
        print("References section not found.")
        return

    ref_text = content[match.end():].strip()

    # Simple split by newline (heuristic)
    # Better: split by [n] or number.

    # Try to find pattern [1], [2] etc.
    refs = re.split(r'\[\d+\]', ref_text)
    if len(refs) < 2:
        # Try numbering 1. 2.
        refs = re.split(r'\n\d+\.', ref_text)

    # Filter empty
    refs = [r.strip() for r in refs if len(r.strip()) > 10]

    print(f"Found {len(refs)} references.", flush=True)

    analyzed = []

    for i, ref in enumerate(refs[:10]): # Check top 10
        # Check for ArXiv
        arxiv = re.search(r'arxiv:(\d+\.\d+)', ref, re.IGNORECASE)
        doi = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', ref, re.IGNORECASE)
        url = re.search(r'https?://[^\s]+', ref)

        status = "Unknown"
        link = None

        if arxiv:
            status = "ArXiv (Downloadable)"
            link = f"https://arxiv.org/pdf/{arxiv.group(1)}.pdf"
        elif doi:
            status = "DOI (Requires Access)"
            link = f"https://doi.org/{doi.group(0)}"
        elif url:
            status = "URL Found"
            link = url.group(0)

        analyzed.append({
            "id": i+1,
            "text": ref[:60] + "...",
            "status": status,
            "link": link
        })

    print("\nAnalysis Result (Top 10):")
    print("-" * 60)
    print(f"{'ID':<4} | {'Status':<20} | {'Link/Info'}")
    print("-" * 60)
    for item in analyzed:
        link_str = item['link'] if item['link'] else "-"
        print(f"{item['id']:<4} | {item['status']:<20} | {link_str}")
    print("-" * 60)

    print("\nSummary:")
    downloadable = len([x for x in analyzed if "Downloadable" in x['status']])
    print(f"Directly Downloadable (ArXiv): {downloadable}/{len(analyzed)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str)
    args = parser.parse_args()

    check_ref_availability(args.folder)
