import sqlite3
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import Config

def verify():
    db_path = Config.DB_PATH
    output = []
    output.append(f"Connecting to database: {db_path}")

    if not os.path.exists(db_path):
        output.append("Database file not found!")
        return "\n".join(output)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        tables = [
            ("common_company", ["no", "id"], "no"),
            ("common_user", ["no", "id"], "no"),
            ("tax_customer", ["no", "company_no"], "no"),
            ("sys_standard_word", ["no"], "no"),
            ("common_user_company_relation", ["no", "company_no", "user_id"], "no")
        ]

        for table_name, expected_columns, pk_column in tables:
            output.append(f"Checking table: {table_name}...")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            # Check PK
            # col[5] is pk flag (1 or higher)

            if pk_column in column_names:
                pk_col_idx = column_names.index(pk_column)
                if columns[pk_col_idx][5] >= 1:
                     output.append(f"  [OK] PK column '{pk_column}' exists and is PK.")
                else:
                     output.append(f"  [FAIL] PK column '{pk_column}' exists but is NOT PK.")
            else:
                 output.append(f"  [FAIL] PK column '{pk_column}' MISSING!")

            for col in expected_columns:
                if col in column_names:
                    output.append(f"  [OK] Expected column '{col}' exists.")
                else:
                    output.append(f"  [FAIL] Expected column '{col}' MISSING!")

        conn.close()
    except Exception as e:
        output.append(f"Error: {e}")

    return "\n".join(output)

if __name__ == "__main__":
    result = verify()
    print(result)
    with open("tmp/migration_result.txt", "w", encoding="utf-8") as f:
        f.write(result)
