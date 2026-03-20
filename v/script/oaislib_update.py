#!/usr/bin/env python3
"""
oaislib_update.py

oais 모듈 분석 및 문서화 스크립트

명령어:
    oaislib run              전체 모듈 분석
    oaislib run [모듈명]     특정 모듈 분석 (예: oaislib run company)
    oaislib update           d0005_lib.md 문서 업데이트
"""

import ast
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OAIS_DIR = PROJECT_ROOT / "oais"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaislib - oais 모듈 분석 및 문서화")
    print()
    print("사용법:")
    print("    oaislib run              전체 모듈 분석")
    print("    oaislib run [모듈명]     특정 모듈 분석 (예: company, db)")
    print("    oaislib update           d0005_lib.md 문서 업데이트")
    print()
    print("옵션:")
    print("    --depth [n]              분석 깊이 설정 (기본: 2)")
    print("    --include-private        private 함수 포함")
    print("    --doc-only               문서만 생성, 분석 생략")
    print()
    print("예시:")
    print("    python v/script/oaislib_update.py run")
    print("    python v/script/oaislib_update.py run company")
    print("    python v/script/oaislib_update.py update")

def parse_module(file_path):
    """
    Parses a python file to extract classes and functions with docstrings.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    module_doc = ast.get_docstring(tree)
    functions = []
    classes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_doc = ast.get_docstring(node)
            args = [a.arg for a in node.args.args]
            functions.append({
                "name": node.name,
                "args": args,
                "doc": func_doc
            })
        elif isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node)
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_doc = ast.get_docstring(item)
                    m_args = [a.arg for a in item.args.args]
                    methods.append({
                        "name": item.name,
                        "args": m_args,
                        "doc": method_doc
                    })
            classes.append({
                "name": node.name,
                "doc": class_doc,
                "methods": methods
            })

    return module_doc, classes, functions

def generate_markdown(modules_data):
    """Generates markdown content from parsed module data."""
    md = "# Generated OAIS Library Documentation\n\n"

    for mod_name, data in modules_data.items():
        md += f"## Module: `{mod_name}`\n\n"
        if data['doc']:
            md += f"{data['doc'].strip()}\n\n"

        if data['classes']:
            md += "### Classes\n"
            for cls in data['classes']:
                md += f"- **`{cls['name']}`**\n"
                if cls['doc']:
                    md += f"  - {cls['doc'].strip().splitlines()[0]}\n"
                for method in cls['methods']:
                    if not method['name'].startswith("_"):
                        args_str = ", ".join(method['args'])
                        md += f"  - `.{method['name']}({args_str})`\n"
            md += "\n"

        if data['functions']:
            md += "### Functions\n"
            for func in data['functions']:
                if not func['name'].startswith("_"):
                    args_str = ", ".join(func['args'])
                    md += f"- **`{func['name']}({args_str})`**\n"
                    if func['doc']:
                        md += f"  - {func['doc'].strip().splitlines()[0]}\n"
            md += "\n"

        md += "---\n\n"
    return md

def cmd_run(args, options):
    """모듈 분석 (run 서브명령어)"""
    print("# oaislib run\n")

    if not OAIS_DIR.exists():
        print(f"[ERROR] {OAIS_DIR} directory not found.")
        return 1

    include_private = options.get("include_private", False)
    target_module = args[0] if args else None

    print(f"분석 대상: {OAIS_DIR}")
    if target_module:
        print(f"모듈 필터: {target_module}")
    print()

    modules_data = {}

    for py_file in sorted(OAIS_DIR.glob("*.py")):
        if py_file.name == "__init__.py":
            continue

        # 모듈 필터 적용
        if target_module and target_module.lower() not in py_file.stem.lower():
            continue

        try:
            mod_doc, classes, functions = parse_module(py_file)

            # private 필터
            if not include_private:
                functions = [f for f in functions if not f["name"].startswith("_")]
                for cls in classes:
                    cls["methods"] = [m for m in cls["methods"] if not m["name"].startswith("_")]

            modules_data[py_file.stem] = {
                "doc": mod_doc,
                "classes": classes,
                "functions": functions
            }

            # 분석 결과 출력
            print(f"## {py_file.stem}")
            if mod_doc:
                first_line = mod_doc.strip().split("\n")[0]
                print(f"  {first_line[:60]}")
            print(f"  클래스: {len(classes)}개 | 함수: {len(functions)}개")
            print()

        except Exception as e:
            print(f"[ERROR] Failed to parse {py_file.name}: {e}")

    print(f"---\n총 {len(modules_data)}개 모듈 분석 완료")
    return 0


def cmd_update(options):
    """문서 업데이트 (update 서브명령어)"""
    print("# oaislib update\n")

    if not OAIS_DIR.exists():
        print(f"[ERROR] {OAIS_DIR} directory not found.")
        return 1

    include_private = options.get("include_private", False)

    print("Scanning oais modules...\n")
    modules_data = {}

    for py_file in sorted(OAIS_DIR.glob("*.py")):
        if py_file.name == "__init__.py":
            continue

        try:
            mod_doc, classes, functions = parse_module(py_file)

            # private 필터
            if not include_private:
                functions = [f for f in functions if not f["name"].startswith("_")]
                for cls in classes:
                    cls["methods"] = [m for m in cls["methods"] if not m["name"].startswith("_")]

            modules_data[py_file.stem] = {
                "doc": mod_doc,
                "classes": classes,
                "functions": functions
            }
            print(f"  [OK] {py_file.stem}")

        except Exception as e:
            print(f"  [ERROR] {py_file.name}: {e}")

    md_output = generate_markdown(modules_data)

    out_file = PROJECT_ROOT / "doc" / "d0005_lib.md"
    out_file.parent.mkdir(exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md_output)

    print(f"\n[OK] Documentation generated at {out_file}")
    print(f"총 {len(modules_data)}개 모듈 문서화 완료")
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
    options = {
        "include_private": "--include-private" in cmd_args,
        "doc_only": "--doc-only" in cmd_args
    }

    # depth 옵션
    if "--depth" in cmd_args:
        idx = cmd_args.index("--depth")
        if idx + 1 < len(cmd_args):
            try:
                options["depth"] = int(cmd_args[idx + 1])
            except ValueError:
                pass

    # 옵션 제거
    cmd_args = [a for a in cmd_args if not a.startswith("--") and not a.isdigit()]

    if cmd == "run":
        return cmd_run(cmd_args, options)
    elif cmd == "update":
        return cmd_update(options)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
