import os
from pathlib import Path

def test_access():
    with open("tmp/access_test.txt", "w", encoding="utf-8") as f:
        f.write("Access Test Start\n")

        cwd = Path.cwd()
        f.write(f"CWD: {cwd}\n")

        target = cwd / "02_paper"
        if target.exists():
            f.write(f"02_paper exists. Items: {len(list(target.iterdir()))}\n")
        else:
            f.write("02_paper NOT found\n")

    print("Test finished")

if __name__ == "__main__":
    test_access()
