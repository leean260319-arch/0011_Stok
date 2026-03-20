#!/usr/bin/env python3
"""
oaisenv_uv_cleanup.py

pyproject.toml의 의존성과 실제 코드 import를 비교하여 미사용 패키지를 탐지합니다.

Usage:
    uv run python v/script/oaisenv_uv_cleanup.py
    uv run python v/script/oaisenv_uv_cleanup.py --dry-run
    uv run python v/script/oaisenv_uv_cleanup.py --auto
    uv run python v/script/oaisenv_uv_cleanup.py --exclude numpy --exclude pandas
"""

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

# Windows 콘솔 UTF-8 인코딩 설정
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path.cwd()
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"

# 패키지명 -> import명 매핑 (다른 경우만)
PACKAGE_TO_IMPORT = {
    "opencv-python": ["cv2"],
    "opencv-python-headless": ["cv2"],
    "scikit-learn": ["sklearn"],
    "scikit-image": ["skimage"],
    "pillow": ["PIL", "pillow"],
    "python-docx": ["docx"],
    "beautifulsoup4": ["bs4"],
    "pyyaml": ["yaml"],
    "pymupdf": ["fitz"],
    "pypdf2": ["PyPDF2"],
    "pdf2image": ["pdf2image"],
    "pytesseract": ["pytesseract"],
    "webdriver-manager": ["webdriver_manager"],
    "streamlit-cropper": ["streamlit_cropper"],
    "streamlit-quill": ["streamlit_quill"],
    "types-requests": ["requests"],  # stub 패키지
    "pytest-cov": ["pytest_cov", "coverage"],
    "pytest-playwright": ["pytest_playwright"],
}

# 자동 제외 패키지 (런타임/빌드/테스트 전용)
AUTO_EXCLUDE = {
    # 런타임 서버
    "uvicorn", "gunicorn", "daphne", "hypercorn",
    # 테스트 프레임워크
    "pytest", "pytest-cov", "pytest-playwright", "coverage",
    # 타입 힌트
    "mypy", "types-requests", "types-pyyaml",
    # 빌드 도구
    "setuptools", "wheel", "pip", "build",
    # 린터/포매터
    "pylint", "flake8", "black", "isort", "ruff",
    # Jupyter 관련 (노트북에서만 사용)
    "ipykernel", "ipywidgets", "jupyter", "notebook",
}

# 검색 제외 디렉토리
EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".mypy_cache", ".pytest_cache", "dist", "build", "egg-info",
    ".claude", ".gemini", ".taskmaster", "tmp", "data",
}


# ============================================================
# Functions
# ============================================================

def parse_pyproject() -> tuple[list[str], list[str]]:
    """pyproject.toml에서 의존성 추출"""
    if not PYPROJECT_PATH.exists():
        print(f"오류: {PYPROJECT_PATH} 파일이 없습니다.")
        sys.exit(1)

    content = PYPROJECT_PATH.read_text(encoding='utf-8')

    dependencies = []
    dev_dependencies = []

    # dependencies 섹션 파싱
    dep_match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if dep_match:
        dep_text = dep_match.group(1)
        for line in dep_text.split('\n'):
            line = line.strip().strip(',').strip('"').strip("'")
            if line and not line.startswith('#'):
                # 버전 정보 제거 (>=, ==, ~= 등)
                pkg_name = re.split(r'[><=~!\[]', line)[0].strip().lower()
                if pkg_name:
                    dependencies.append(pkg_name)

    # dev dependencies 섹션 파싱
    dev_match = re.search(r'\[dependency-groups\]\s*dev\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if dev_match:
        dev_text = dev_match.group(1)
        for line in dev_text.split('\n'):
            line = line.strip().strip(',').strip('"').strip("'")
            if line and not line.startswith('#'):
                pkg_name = re.split(r'[><=~!\[]', line)[0].strip().lower()
                if pkg_name:
                    dev_dependencies.append(pkg_name)

    return dependencies, dev_dependencies


def get_import_names(package: str) -> list[str]:
    """패키지명에서 가능한 import 이름들 반환"""
    # 매핑 테이블 확인
    if package in PACKAGE_TO_IMPORT:
        return PACKAGE_TO_IMPORT[package]

    # 기본: 패키지명 그대로 + 하이픈을 언더스코어로
    names = [package]
    if '-' in package:
        names.append(package.replace('-', '_'))

    return names


def scan_imports() -> set[str]:
    """프로젝트 코드에서 모든 import 문 추출"""
    imports = set()

    for py_file in PROJECT_ROOT.rglob("*.py"):
        # 제외 디렉토리 체크
        if any(excluded in py_file.parts for excluded in EXCLUDE_DIRS):
            continue

        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # 최상위 모듈명만 추출
                        top_module = alias.name.split('.')[0]
                        imports.add(top_module.lower())
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        top_module = node.module.split('.')[0]
                        imports.add(top_module.lower())
        except (SyntaxError, UnicodeDecodeError):
            # 파싱 실패 파일은 건너뜀
            continue

    return imports


def find_unused_packages(
    dependencies: list[str],
    imports: set[str],
    exclude: set[str],
    include_dev: bool = False,
    dev_dependencies: list[str] = None
) -> list[str]:
    """미사용 패키지 찾기"""
    unused = []

    packages_to_check = dependencies.copy()
    if include_dev and dev_dependencies:
        packages_to_check.extend(dev_dependencies)

    for package in packages_to_check:
        # 자동 제외 및 사용자 제외 체크
        if package in AUTO_EXCLUDE or package in exclude:
            continue

        # 가능한 import 이름들 가져오기
        import_names = get_import_names(package)

        # import 여부 확인
        is_used = any(name.lower() in imports for name in import_names)

        if not is_used:
            unused.append(package)

    return unused


def remove_packages(packages: list[str]) -> bool:
    """패키지 삭제 실행"""
    if not packages:
        return True

    cmd = ["uv", "remove"] + packages
    print(f"\n실행: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("삭제 완료")
        return True
    else:
        print(f"오류: {result.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="미사용 패키지 탐지 및 삭제")
    parser.add_argument("--dry-run", action="store_true", help="삭제 없이 미리보기")
    parser.add_argument("--auto", action="store_true", help="확인 없이 자동 삭제")
    parser.add_argument("--exclude", action="append", default=[], help="제외할 패키지")
    parser.add_argument("--include-dev", action="store_true", help="dev 의존성도 검사")
    args = parser.parse_args()

    print("# oaisenv uv cleanup - 미사용 패키지 탐지\n")

    # 1. pyproject.toml 파싱
    print("## 1. pyproject.toml 분석\n")
    dependencies, dev_dependencies = parse_pyproject()
    print(f"- 의존성: {len(dependencies)}개")
    print(f"- dev 의존성: {len(dev_dependencies)}개")

    # 2. import 스캔
    print("\n## 2. 프로젝트 import 스캔\n")
    imports = scan_imports()
    print(f"- 발견된 import: {len(imports)}개")

    # 3. 미사용 패키지 찾기
    print("\n## 3. 미사용 패키지 분석\n")
    exclude_set = set(pkg.lower() for pkg in args.exclude)
    unused = find_unused_packages(
        dependencies,
        imports,
        exclude_set,
        args.include_dev,
        dev_dependencies
    )

    if not unused:
        print("미사용 패키지가 없습니다.")
        return

    print(f"미사용 패키지 {len(unused)}개 발견:\n")
    for i, pkg in enumerate(unused, 1):
        print(f"  {i}. {pkg}")

    # 4. 삭제 처리
    if args.dry_run:
        print("\n(--dry-run: 삭제하지 않음)")
        return

    if args.auto:
        print("\n## 4. 자동 삭제 실행\n")
        remove_packages(unused)
        return

    # 대화형 확인
    print("\n## 4. 삭제 확인\n")
    print("삭제할 패키지 번호를 입력하세요 (예: 1,3,5 또는 all 또는 none):")

    try:
        choice = input("> ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n취소됨")
        return

    if choice == "none" or choice == "":
        print("취소됨")
        return

    if choice == "all":
        to_remove = unused
    else:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(",")]
            to_remove = [unused[i] for i in indices if 0 <= i < len(unused)]
        except (ValueError, IndexError):
            print("잘못된 입력")
            return

    if to_remove:
        print(f"\n삭제 대상: {', '.join(to_remove)}")
        remove_packages(to_remove)
    else:
        print("삭제할 패키지가 없습니다.")


if __name__ == "__main__":
    main()
