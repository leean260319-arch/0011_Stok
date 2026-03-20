#!/usr/bin/env python3
"""
oaispaper_trans.py

PDF 텍스트 추출 및 번역 스크립트
- PDF에서 영문 전문 추출
- 영문 전문에서 한글 번역 생성
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import PyPDF2

# 경로 설정
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = PROJECT_ROOT / "02_paper"


def extract_text_from_pdf(pdf_path):
    """
    PDF 파일에서 텍스트 추출

    Args:
        pdf_path (Path): PDF 파일 경로

    Returns:
        str: 추출된 텍스트
    """
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            return text
    except Exception as e:
        print(f"[Error] PDF 추출 실패: {e}", file=sys.stderr)
        return None


def create_english_full_text(folder_path, pdf_path, title):
    """
    03_전문(영어).md 파일 생성

    Args:
        folder_path (Path): 논문 폴더 경로
        pdf_path (Path): PDF 파일 경로
        title (str): 논문 제목

    Returns:
        tuple: (성공 여부, 파일 경로, 오류 메시지)
    """
    text = extract_text_from_pdf(pdf_path)

    if text is None:
        return False, None, "PDF 추출 실패"

    if len(text.strip()) < 1000:
        return False, None, f"추출된 텍스트 부족 ({len(text)} bytes < 1000)"

    # 폴더 ID 추출
    folder_id = folder_path.name

    # 파일명 생성 (기존 형식 준수)
    title_safe = title.replace(" ", "_")[:30]
    english_file = folder_path / f"{folder_id}_03_{title_safe}_전문(영어).md"

    # 파일 쓰기
    content = f"""# {title}

*Extracted from PDF - English Text*

---

{text}
"""

    try:
        english_file.write_text(content, encoding="utf-8")
        return True, english_file, None
    except Exception as e:
        return False, None, f"파일 쓰기 실패: {e}"


def create_korean_translation(folder_path, english_file, title):
    """
    04_전문(한글).md 파일 생성 (영문 전문 기반 번역)

    Args:
        folder_path (Path): 논문 폴더 경로
        english_file (Path): 영문 전문 파일 경로
        title (str): 논문 제목

    Returns:
        tuple: (성공 여부, 파일 경로, 오류 메시지)
    """
    if not english_file.exists():
        return False, None, "영문 전문 파일 없음"

    # 영문 텍스트 읽기
    try:
        english_text = english_file.read_text(encoding="utf-8")
    except Exception as e:
        return False, None, f"영문 전문 읽기 실패: {e}"

    # 폴더 ID 추출
    folder_id = folder_path.name

    # 파일명 생성
    title_safe = title.replace(" ", "_")[:30]
    korean_file = folder_path / f"{folder_id}_04_{title_safe}_전문(한글).md"

    # 번역 프레임워크 생성 (실제 번역은 추후 작업)
    content = f"""# {title}

*번역된 한글 전문*

---

[TODO: 영문 전문 번역 필요]

아래는 영문 전문입니다:

```text
{english_text}
```
"""

    try:
        korean_file.write_text(content, encoding="utf-8")
        return True, korean_file, None
    except Exception as e:
        return False, None, f"파일 쓰기 실패: {e}"


def find_pdf_and_title(folder_path):
    """
    폴더에서 PDF 파일과 제목 추출

    Args:
        folder_path (Path): 논문 폴더 경로

    Returns:
        tuple: (PDF 경로, 제목)
    """
    # PDF 파일 찾기
    pdf_files = list(folder_path.glob("*.pdf"))
    if not pdf_files:
        return None, None

    pdf_path = pdf_files[0]

    # 서머리 파일에서 제목 추출 시도
    summary_files = list(folder_path.glob("*_00_*서머리.md"))
    if summary_files:
        try:
            summary_content = summary_files[0].read_text(encoding="utf-8")
            # 제목 추출 (H1 헤더)
            for line in summary_content.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    return pdf_path, title
        except:
            pass

    # PDF 파일명에서 제목 추출
    pdf_name = pdf_path.stem
    title = pdf_name.replace(f"{folder_path.name}_01_", "").replace("_", " ").strip()

    return pdf_path, title


def process_folder(folder_path, extract_english=True, translate_korean=False):
    """
    단일 폴더 처리

    Args:
        folder_path (Path): 논문 폴더 경로
        extract_english (bool): 영문 추출 여부
        translate_korean (bool): 한글 번역 여부

    Returns:
        dict: 처리 결과
    """
    result = {
        "folder": folder_path.name,
        "english": {"success": False, "path": None, "error": None},
        "korean": {"success": False, "path": None, "error": None},
    }

    # PDF와 제목 찾기
    pdf_path, title = find_pdf_and_title(folder_path)

    if pdf_path is None:
        result["english"]["error"] = "PDF 파일 없음"
        return result

    if title is None:
        title = "Unknown Title"

    # 영문 추출
    if extract_english:
        success, english_file, error = create_english_full_text(
            folder_path, pdf_path, title
        )
        result["english"]["success"] = success
        result["english"]["path"] = str(english_file) if english_file else None
        result["english"]["error"] = error

    # 한글 번역
    if translate_korean:
        # 영문 파일 찾기
        english_files = list(folder_path.glob("*_03_*전문(영어).md"))
        if english_files:
            english_file = english_files[0]
            success, korean_file, error = create_korean_translation(
                folder_path, english_file, title
            )
            result["korean"]["success"] = success
            result["korean"]["path"] = str(korean_file) if korean_file else None
            result["korean"]["error"] = error
        else:
            result["korean"]["error"] = "영문 전문 파일 없음"

    return result


def do_english(args):
    """
    영문 전문 추출 명령어 실행
    """
    sys.stdout.reconfigure(encoding="utf-8")
    print("# oaispaper trans english - 영문 전문 추출\n", flush=True)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    if not PAPER_DIR.exists():
        print(f"Error: Paper directory not found at {PAPER_DIR}", flush=True)
        return

    # 대상 폴더 결정
    if args.folder:
        target_folders = [PAPER_DIR / args.folder]
        if not target_folders[0].exists():
            print(f"Error: Folder {args.folder} not found", flush=True)
            return
    else:
        target_folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    print(f"총 {len(target_folders)}개 폴더 처리 중...\n", flush=True)

    # 처리
    success_count = 0
    failed_count = 0
    skipped_count = 0

    results = []

    for folder in target_folders:
        result = process_folder(folder, extract_english=True, translate_korean=False)
        results.append(result)

        # 기존 파일 존재 체크
        existing_english = list(folder.glob("*_03_*전문(영어).md"))

        if existing_english and not args.force:
            skipped_count += 1
            print(f"- [SKIP] {folder.name}: 이미 존재", flush=True)
            continue

        if result["english"]["success"]:
            success_count += 1
            print(
                f"- [OK] {folder.name}: {Path(result['english']['path']).name}",
                flush=True,
            )
        else:
            failed_count += 1
            error = result["english"]["error"] or "알 수 없는 오류"
            print(f"- [FAIL] {folder.name}: {error}", flush=True)

    # 결과 요약
    print(f"\n## 요약", flush=True)
    print(f"- 성공: {success_count}개", flush=True)
    print(f"- 실패: {failed_count}개", flush=True)
    print(f"- 건너뜀: {skipped_count}개", flush=True)
    print(f"- 총 처리: {len(target_folders)}개", flush=True)

    # 실패 목록 저장
    failed = [r for r in results if not r["english"]["success"]]
    if failed:
        log_file = PROJECT_ROOT / "tmp" / "trans_english_failed.txt"
        log_file.parent.mkdir(exist_ok=True)
        log_content = f"영문 추출 실패 로그 - {datetime.now()}\n\n"
        for r in failed:
            log_content += f"{r['folder']}: {r['english']['error']}\n"
        log_file.write_text(log_content, encoding="utf-8")
        print(f"\n실패 로그: tmp/trans_english_failed.txt", flush=True)


def do_korean(args):
    """
    한글 번역 명령어 실행
    """
    sys.stdout.reconfigure(encoding="utf-8")
    print("# oaispaper trans korean - 한글 번역 생성\n", flush=True)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    if not PAPER_DIR.exists():
        print(f"Error: Paper directory not found at {PAPER_DIR}", flush=True)
        return

    # 대상 폴더 결정
    if args.folder:
        target_folders = [PAPER_DIR / args.folder]
        if not target_folders[0].exists():
            print(f"Error: Folder {args.folder} not found", flush=True)
            return
    else:
        target_folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])

    print(f"총 {len(target_folders)}개 폴더 처리 중...\n", flush=True)

    # 처리
    success_count = 0
    failed_count = 0
    skipped_count = 0

    results = []

    for folder in target_folders:
        result = process_folder(folder, extract_english=False, translate_korean=True)
        results.append(result)

        # 기존 파일 존재 체크
        existing_korean = list(folder.glob("*_04_*전문(한글).md"))

        if existing_korean and not args.force:
            skipped_count += 1
            print(f"- [SKIP] {folder.name}: 이미 존재", flush=True)
            continue

        if result["korean"]["success"]:
            success_count += 1
            print(
                f"- [OK] {folder.name}: {Path(result['korean']['path']).name}",
                flush=True,
            )
        else:
            failed_count += 1
            error = result["korean"]["error"] or "알 수 없는 오류"
            print(f"- [FAIL] {folder.name}: {error}", flush=True)

    # 결과 요약
    print(f"\n## 요약", flush=True)
    print(f"- 성공: {success_count}개", flush=True)
    print(f"- 실패: {failed_count}개", flush=True)
    print(f"- 건너뜀: {skipped_count}개", flush=True)
    print(f"- 총 처리: {len(target_folders)}개", flush=True)

    # 실패 목록 저장
    failed = [r for r in results if not r["korean"]["success"]]
    if failed:
        log_file = PROJECT_ROOT / "tmp" / "trans_korean_failed.txt"
        log_file.parent.mkdir(exist_ok=True)
        log_content = f"한글 번역 실패 로그 - {datetime.now()}\n\n"
        for r in failed:
            log_content += f"{r['folder']}: {r['korean']['error']}\n"
        log_file.write_text(log_content, encoding="utf-8")
        print(f"\n실패 로그: tmp/trans_korean_failed.txt", flush=True)


def main():
    parser = argparse.ArgumentParser(description="PDF 텍스트 추출 및 번역")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # english 명령어
    eng_p = subparsers.add_parser("english", help="영문 전문 추출")
    eng_p.add_argument("--folder", type=str, help="특정 폴더만 처리")
    eng_p.add_argument("--force", action="store_true", help="기존 파일 덮어쓰기")

    # korean 명령어
    kor_p = subparsers.add_parser("korean", help="한글 번역 생성")
    kor_p.add_argument("--folder", type=str, help="특정 폴더만 처리")
    kor_p.add_argument("--force", action="store_true", help="기존 파일 덮어쓰기")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "english":
        do_english(args)
    elif args.command == "korean":
        do_korean(args)
    else:
        print("Not implemented")
        sys.exit(1)


if __name__ == "__main__":
    main()
