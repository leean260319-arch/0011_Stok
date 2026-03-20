import sqlite3
import os

# 설정
DB_PATH = r'd:\3_code\0003_CCone\db\sene.sqlite'
OUTPUT_FILE = r'd:\3_code\0003_CCone\v\template\db_standard_word.md'

def to_markdown_table(headers, rows):
    if not headers:
        return ""

    # 헤더 생성
    header_line = "| " + " | ".join(str(h) for h in headers) + " |"
    separator_line = "| " + " | ".join("---" for _ in headers) + " |"

    lines = [header_line, separator_line]

    # 데이터 행 생성
    for row in rows:
        line = "| " + " | ".join(str(item) if item is not None else "" for item in row) + " |"
        lines.append(line)

    return "\n".join(lines)

def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: DB file not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM sys_standard_word")
            rows = cursor.fetchall()

            # 컬럼명 가져오기
            headers = [description[0] for description in cursor.description]

        except sqlite3.OperationalError as e:
            print(f"Query error: {e}")
            conn.close()
            return

        conn.close()

        if not rows:
            print("Warning: sys_standard_word table is empty.")
            content = "# 표준용어집 (sys_standard_word)\n\n데이터가 없습니다."
        else:
            # 마크다운 변환
            markdown_table = to_markdown_table(headers, rows)

            # 현재 시간 (pandas 없이)
            import datetime
            now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            content = f"# 표준용어집 (sys_standard_word)\n\n업데이트: {now_str}\n\n{markdown_table}"

        # 파일 저장
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Successfully exported sys_standard_word to {OUTPUT_FILE}")
        print(f"Row count: {len(rows)}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
