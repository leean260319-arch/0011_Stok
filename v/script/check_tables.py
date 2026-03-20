import sqlite3
import os

DB_PATH = r'd:\3_code\0003_CCone\db\sene.sqlite'

if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in DB:", [t[0] for t in tables])
        conn.close()
    except Exception as e:
        print(f"Error reading DB: {e}")
else:
    print(f"DB not found at {DB_PATH}")
