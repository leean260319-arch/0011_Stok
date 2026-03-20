import sqlite3
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import Config

def verify_table_schema(cursor, table_name, expected_columns, pk_column="no"):
    print(f"Checking table: {table_name}...")
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        # Check PK
        pk_info = next((col for col in columns if col[5] == 1), None) # col[5] is pk flag
        # Note: SQLite PRAGMA table_info: cid, name, type, notnull, dflt_value, pk

        if pk_column in column_names:
             print(f"  [OK] PK column '{pk_column}' exists.")
        else:
             print(f"  [FAIL] PK column '{pk_column}' MISSING!")

        for col in expected_columns:
            if col in column_names:
                print(f"  [OK] Expected column '{col}' exists.")
            else:
                print(f"  [FAIL] Expected column '{col}' MISSING!")

    except Exception as e:
        print(f"  [ERROR] Failed to check table {table_name}: {e}")

def main():
    db_path = Config.DB_PATH
    print(f"Connecting to database: {db_path}")

    if not os.path.exists(db_path):
        print("Database file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verify tables
    verify_table_schema(cursor, "common_company", ["no", "id"], pk_column="no")
    verify_table_schema(cursor, "common_user", ["no", "id"], pk_column="no") # id is logical PK (text) but no is surrogate PK
    verify_table_schema(cursor, "tax_customer", ["no", "company_no"], pk_column="no")
    verify_table_schema(cursor, "sys_standard_word", ["no"], pk_column="no")
    verify_table_schema(cursor, "common_user_company_relation", ["no", "company_no", "user_id"], pk_column="no")

    conn.close()

if __name__ == "__main__":
    main()
