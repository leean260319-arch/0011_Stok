#!/usr/bin/env python3
"""
oaisdb_update.py

DB 스키마 분석 및 문서화 스크립트

명령어:
    oaisdb run        전체 DB 분석 및 문서화
    oaisdb schema     스키마만 추출 (출력)
    oaisdb update     d0006_db.md 문서 업데이트
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 설정
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# DB 경로 설정
DB_PATH = PROJECT_ROOT / "db" / "sene.sqlite"
DOC_FILE = PROJECT_ROOT / "doc" / "d0006_db.md"
STD_WORD_FILE = PROJECT_ROOT / "v" / "template" / "db_standard_word.md"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaisdb - DB 스키마 분석 및 문서화")
    print()
    print("사용법:")
    print("    oaisdb run        전체 DB 분석 및 문서화")
    print("    oaisdb schema     스키마만 추출 (출력)")
    print("    oaisdb update     d0006_db.md 문서 업데이트")
    print()
    print("옵션:")
    print("    --db [경로]       DB 파일 경로 지정")
    print("    --export-words    표준용어집 내보내기")
    print()
    print("예시:")
    print("    python v/script/oaisdb_update.py run")
    print("    python v/script/oaisdb_update.py schema")
    print("    python v/script/oaisdb_update.py update --export-words")

def get_schema(db_path):
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return {}

    schema = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 테이블 목록 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            # 컬럼 정보 조회 (PRAGMA table_info)
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_data = cursor.fetchall()

            columns = []
            for col in columns_data:
                # cid, name, type, notnull, dflt_value, pk
                columns.append({
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "default": col[4],
                    "pk": bool(col[5])
                })

            # FK 정보 조회 (PRAGMA foreign_key_list)
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            fk_data = cursor.fetchall()

            # FK 매핑: {from_col: to_table.to_col}
            fks = {}
            for fk in fk_data:
                # id, seq, table, from, to, on_update, on_delete, match
                from_col = fk[3]
                to_table = fk[2]
                to_col = fk[4]
                fks[from_col] = f"{to_table}.{to_col}"

            # 컬럼에 FK 정보 병합
            for col in columns:
                if col["name"] in fks:
                    col["fk"] = fks[col["name"]]

            schema[table_name] = columns

        conn.close()
    except Exception as e:
        print(f"Error reading DB schema: {e}")

    return schema

def export_standard_words(db_path, output_file):
    """sys_standard_word 테이블을 별도 마크다운 문서로 내보내기"""
    if not db_path.exists():
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 테이블 존재 여부 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sys_standard_word'")
        if not cursor.fetchone():
            print("Warning: sys_standard_word table not found.")
            conn.close()
            return

        cursor.execute("SELECT * FROM sys_standard_word")
        rows = cursor.fetchall()

        if not rows:
            content = "# 표준용어집 (sys_standard_word)\n\n데이터가 없습니다."
        else:
            headers = [description[0] for description in cursor.description]

            # 마크다운 테이블 생성
            header_line = "| " + " | ".join(str(h) for h in headers) + " |"
            separator_line = "| " + " | ".join("---" for _ in headers) + " |"

            lines = [header_line, separator_line]
            for row in rows:
                lines.append("| " + " | ".join(str(item) if item is not None else "" for item in row) + " |")

            markdown_table = "\n".join(lines)

            # 현재 시간
            from datetime import datetime
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            content = f"# 표준용어집 (sys_standard_word)\n\n업데이트: {now_str}\n\n{markdown_table}"

        # 파일 저장
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Standard word dictionary exported to {output_file}")
        conn.close()

    except Exception as e:
        print(f"Error exporting standard words: {e}")

def generate_db_doc(schema):
    md = "# d0006_db.md - 데이터베이스 구조\n\n"

    # 문서 이력 관리 (자동 생성 시 현재 날짜)
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    md += "## 문서이력관리\n"
    md += "| 버전 | 날짜 | 작성자 | 변경내용 |\n"
    md += "|-----|------|-------|---------|\n"
    md += f"| vAuto | {today} | oaisdb | 자동 업데이트 |\n\n"
    md += "---\n\n"

    md += "## 1. 개요\n\n이 문서는 프로젝트의 데이터베이스 스키마를 정의합니다.\n\n---\n\n"

    md += "## 2. 테이블 목록\n\n"

    # 테이블 목록 요약
    md += f"총 테이블 수: {len(schema)}\n\n"

    for table_name in sorted(schema.keys()):
        md += f"- [{table_name}](#{table_name.lower()})\n"
    md += "\n---\n\n"

    md += "## 3. 상세 스키마\n\n"

    for table_name in sorted(schema.keys()):
        columns = schema[table_name]
        md += f"### {table_name}\n\n"
        md += "| 컬럼명 | 타입 | PK | NULL | 기본값 | FK | 설명 |\n"
        md += "|--------|------|----|------|--------|----|------|\n"

        for col in columns:
            pk = "✅" if col['pk'] else ""
            not_null = "NO" if col['notnull'] else "YES"
            default = f"`{col['default']}`" if col['default'] is not None else ""
            fk = f"`{col['fk']}`" if 'fk' in col else ""

            md += f"| {col['name']} | {col['type']} | {pk} | {not_null} | {default} | {fk} | - |\n"
        md += "\n"

    return md

def cmd_run(db_path, export_words=True):
    """전체 DB 분석 및 문서화 (run 서브명령어)"""
    print("# oaisdb run\n")

    print(f"DB 경로: {db_path}")
    print()

    # 1. DB 스키마 추출
    schema = get_schema(db_path)

    if not schema:
        print("[ERROR] Schema extraction failed or DB empty.")
        return 1

    print(f"총 {len(schema)}개 테이블 발견\n")

    # 2. 테이블 목록 출력
    for table_name in sorted(schema.keys()):
        columns = schema[table_name]
        pk_cols = [c["name"] for c in columns if c["pk"]]
        fk_cols = [c["name"] for c in columns if "fk" in c]
        print(f"  {table_name}")
        print(f"    컬럼: {len(columns)}개 | PK: {pk_cols or '-'} | FK: {len(fk_cols)}개")

    # 3. 문서 생성
    md_output = generate_db_doc(schema)
    DOC_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DOC_FILE, "w", encoding="utf-8") as f:
        f.write(md_output)
    print(f"\n[OK] DB 문서 생성됨: {DOC_FILE}")

    # 4. 표준 용어집 내보내기
    if export_words:
        export_standard_words(db_path, STD_WORD_FILE)

    return 0


def cmd_schema(db_path):
    """스키마 추출 (schema 서브명령어)"""
    print("# oaisdb schema\n")

    print(f"DB 경로: {db_path}")
    print()

    schema = get_schema(db_path)

    if not schema:
        print("[ERROR] Schema extraction failed or DB empty.")
        return 1

    # 스키마 정보 출력
    for table_name in sorted(schema.keys()):
        columns = schema[table_name]
        print(f"## {table_name}")
        print()
        print("| 컬럼명 | 타입 | PK | NULL | 기본값 | FK |")
        print("|--------|------|----|------|--------|---|")

        for col in columns:
            pk = "O" if col['pk'] else ""
            not_null = "N" if col['notnull'] else "Y"
            default = col['default'] if col['default'] else ""
            fk = col.get('fk', "")
            print(f"| {col['name']} | {col['type']} | {pk} | {not_null} | {default} | {fk} |")

        print()

    print(f"---\n총 {len(schema)}개 테이블")
    return 0


def cmd_update(db_path, export_words=False):
    """문서 업데이트 (update 서브명령어)"""
    print("# oaisdb update\n")

    print(f"DB 경로: {db_path}")
    print()

    # 1. DB 스키마 추출
    schema = get_schema(db_path)

    if not schema:
        print("[ERROR] Schema extraction failed or DB empty.")
        return 1

    # 2. 메인 DB 문서 생성
    md_output = generate_db_doc(schema)

    DOC_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DOC_FILE, "w", encoding="utf-8") as f:
        f.write(md_output)
    print(f"[OK] DB 문서 업데이트됨: {DOC_FILE}")
    print(f"테이블 수: {len(schema)}")

    # 3. 표준 용어집 내보내기
    if export_words:
        export_standard_words(db_path, STD_WORD_FILE)

    return 0


def main():
    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    cmd_args = args[1:]

    # 옵션 파싱
    export_words = "--export-words" in cmd_args
    db_path = DB_PATH

    # --db 옵션
    if "--db" in cmd_args:
        idx = cmd_args.index("--db")
        if idx + 1 < len(cmd_args):
            db_path = Path(cmd_args[idx + 1])
            if not db_path.is_absolute():
                db_path = PROJECT_ROOT / db_path

    if cmd == "run":
        return cmd_run(db_path, export_words)
    elif cmd == "schema":
        return cmd_schema(db_path)
    elif cmd == "update":
        return cmd_update(db_path, export_words)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
