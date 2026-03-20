from pathlib import Path
import sys

TARGET = Path(r"c:\Users\oaiskoo\home\3_code\0002_paper\doc\debug_test.txt")
try:
    TARGET.write_text("Hello from python", encoding="utf-8")
    print("Success")
except Exception as e:
    print(f"Error: {e}")
