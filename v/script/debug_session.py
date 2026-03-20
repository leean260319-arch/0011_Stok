import sqlite3
import pandas as pd
import os
import sys

# Ensure we can import oais if needed, though we are using direct sqlite here
sys.path.append(os.getcwd())

db_path = 'db/user.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)

with open('d:/3_code/0003_CCone/tmp_debug_out.txt', 'w', encoding='utf-8') as f:
    f.write("--- USER ADMIN ---\n")
    try:
        df_user = pd.read_sql("SELECT no, id, name FROM common_user WHERE id='admin'", conn)
        f.write(str(df_user) + "\n")
        admin_no = df_user.iloc[0]['no'] if not df_user.empty else None
    except Exception as e:
        f.write(f"Error querying user: {e}\n")

    f.write("\n--- COMPANY 이마이닝 ---\n")
    try:
        df_comp = pd.read_sql("SELECT no, company_name, company_type FROM common_company WHERE company_name LIKE '%이마이닝%'", conn)
        f.write(str(df_comp) + "\n")

        if not df_comp.empty:
            comp_no = df_comp.iloc[0]['no']
            f.write(f"\n--- TAX AGENCY (company_no={comp_no}) ---\n")
            df_agency = pd.read_sql(f"SELECT * FROM tax_agency WHERE company_no={comp_no}", conn)
            f.write(str(df_agency) + "\n")

            f.write(f"\n--- TAX AGENT (agency_no link check) ---\n")
            if not df_agency.empty:
                agency_no = df_agency.iloc[0]['no']
                f.write(f"Agency No: {agency_no}\n")
                f.write(str(pd.read_sql(f"SELECT * FROM tax_agent WHERE agency_no={agency_no}", conn)) + "\n")
            else:
                f.write("No Tax Agency record found for this company.\n")

            f.write("\n--- ADMIN USER RELATIONS ---\n")
            f.write(str(pd.read_sql(f"SELECT * FROM common_user_company_relation WHERE user_id='admin'", conn)) + "\n")

            f.write("\n--- TAX AGENT TABLE (All) ---\n")
            f.write(str(pd.read_sql(f"SELECT * FROM tax_agent", conn)) + "\n")

    except Exception as e:
        f.write(f"Error querying company: {e}\n")

conn.close()
