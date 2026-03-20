import sqlite3
import os
import sys

# 설정
DB_PATH = r'd:\3_code\0003_CCone\db\sene.sqlite'
OUTPUT_FILE = r'd:\3_code\0003_CCone\v\template\db_standard_word.md'
LOG_FILE = r'd:\3_code\0003_CCone\v\script\debug.log'

def log(msg):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def to_markdown_table(headers, rows):
    if not headers:
        return ""
    header_line = "| " + " | ".join(str(h) for h in headers) + " |"
    separator_line = "| " + " | ".join("---" for _ in headers) + " |"
    lines = [header_line, separator_line]
    for row in rows:
        line = "| " + " | ".join(str(item) if item is not None else "" for item in row) + " |"
        lines.append(line)
    return "\n".join(lines)

def main():
    try:
        log("Script started")
        if not os.path.exists(DB_PATH):
            log(f"Error: DB file not found at {DB_PATH}")
            return

        log("Connecting to DB...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            log("Executing query...")
            cursor.execute("SELECT * FROM sys_standard_word")
            rows = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            log(f"Query success. Rows: {len(rows)}")

        except sqlite3.OperationalError as e:
            log(f"Query error: {e}")
            conn.close()
            return

        conn.close()

        if not rows:
            content = "# 표준용어집 (sys_standard_word)\n\n데이터가 없습니다."
        else:
            log("Formatting markdown...")
            markdown_table = to_markdown_table(headers, rows)
            import datetime
            now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content = f"# 표준용어집 (sys_standard_word)\n\n업데이트: {now_str}\n\n{markdown_table}"

        log("Writing output file...")
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        log(f"Successfully exported to {OUTPUT_FILE}")

    except Exception as e:
        log(f"Global error: {e}")

if __name__ == "__main__":
    main()
