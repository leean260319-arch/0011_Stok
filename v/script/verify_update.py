import shutil
from pathlib import Path

def verify():
    # Target file
    target = Path("02_paper/230312-1648/230312-1648_00_Holistically_Nested_Edge_서머리.md")

    # Destination in doc folder (not gitignored for reading)
    dest = Path("doc/check_summary_content.txt")

    if target.exists():
        content = target.read_text(encoding='utf-8')
        dest.write_text(content, encoding='utf-8')
        print("Copied summary to doc/check_summary_content.txt")
    else:
        print("Target file not found")

if __name__ == "__main__":
    verify()
