#!/usr/bin/env python3
"""
01_down 폴더 PDF 처리 스크립트
- 메타데이터 추출
- 02_paper 폴더로 표준 형식 이동
- download_list.md 처리
"""

import os
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
import json

# 경로 설정
BASE_DIR = Path(__file__).parent.parent.parent
DOWN_DIR = BASE_DIR / "01_down"
PAPER_DIR = BASE_DIR / "02_paper"
TMP_DIR = BASE_DIR / "tmp"


def extract_metadata_from_pdf(pdf_path):
    """PDF 파일명에서 메타데이터 추출"""
    filename = pdf_path.name

    # arXiv ID 추출
    arxiv_match = re.search(r"(\d{4}\.\d+)", filename)
    if arxiv_match:
        return {
            "type": "arxiv",
            "id": arxiv_match.group(1),
            "title": filename.replace(arxiv_match.group(0), "")
            .replace(".pdf", "")
            .strip(" _-"),
        }

    # 일반 논문 제목 추정
    title = re.sub(r"\.pdf$", "", filename)
    title = re.sub(r"^[R]?\d{6}-\d{4}_?", "", title)  # RYYMMDD-HHMM prefix 제거
    title = title.replace("_", " ").strip()

    return {"type": "general", "title": title, "filename": filename}


def generate_folder_id():
    """YYMMDD-HHMM 형식 폴더 ID 생성 (1분 단위 고유성)"""
    now = datetime.now()
    folder_id = now.strftime("%y%m%d-%H%M")
    return folder_id


def create_standard_folder(folder_id, metadata, pdf_path):
    """표준 폴더 구조 생성"""
    folder_path = PAPER_DIR / folder_id
    folder_path.mkdir(exist_ok=True)

    # PDF 이동
    title_safe = re.sub(r"[^\w\s-]", "", metadata.get("title", "Unknown"))[:30]
    title_safe = re.sub(r"\s+", "_", title_safe.strip())

    new_pdf_name = f"{folder_id}_01_{title_safe}.pdf"
    new_pdf_path = folder_path / new_pdf_name

    shutil.copy2(pdf_path, new_pdf_path)

    # 기본 파일들 생성
    files_created = []

    # 00_서머리.md
    summary_content = f"""# {metadata.get("title", "Unknown Title")}

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | {datetime.now().strftime("%Y-%m-%d")} | 최초 작성 |

---

## 1. 개요

### 1.1 논문 정보
- **제목**: {metadata.get("title", "Unknown Title")}
- **파일명**: {metadata.get("filename", pdf_path.name)}
- **폴더ID**: {folder_id}
- **등록일**: {datetime.now().strftime("%Y-%m-%d")}

### 1.2 메타데이터
"""

    if metadata.get("type") == "arxiv":
        summary_content += f"""- **arXiv ID**: {metadata.get("id", "Unknown")}
"""

    summary_content += f"""
### 1.3 분류
- **키워드**: 
- **분야**: 
- **연구 방법론**: 

---

## 2. 핵심 내용 요약

### 2.1 연구 목적
[TODO: PDF 내용 분석 후 작성]

### 2.2 주요 기여
[TODO: PDF 내용 분석 후 작성]

### 2.3 실험 결과
[TODO: PDF 내용 분석 후 작성]

---

## 3. 상세 분석

### 3.1 방법론
[TODO: PDF 내용 분석 후 작성]

### 3.2 데이터셋
[TODO: PDF 내용 분석 후 작성]

### 3.3 평가 지표
[TODO: PDF 내용 분석 후 작성]

---

## 4. 평가

### 4.1 장점
[TODO: 분석 후 작성]

### 4.2 단점
[TODO: 분석 후 작성]

### 4.3 응용 가능성
[TODO: 분석 후 작성]

---

## 5. 인용 정보

```bibtex
[TODO: 메타데이터 완성 후 작성]
```
"""

    summary_file = folder_path / f"{folder_id}_00_{title_safe}_서머리.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_content)
    files_created.append(summary_file)

    # 03_전문(영어).md (placeholder)
    english_content = f"""# {metadata.get("title", "Unknown Title")}

*Extracted from PDF - English Text*

[TODO: PDF에서 영문 텍스트 추출 필요]
"""

    english_file = folder_path / f"{folder_id}_03_{title_safe}_전문(영어).md"
    with open(english_file, "w", encoding="utf-8") as f:
        f.write(english_content)
    files_created.append(english_file)

    # 04_전문(한글).md (placeholder)
    korean_content = f"""# {metadata.get("title", "Unknown Title")}

*번역된 한글 전문*

[TODO: 영문 전문 번역 필요]
"""

    korean_file = folder_path / f"{folder_id}_04_{title_safe}_전문(한글).md"
    with open(korean_file, "w", encoding="utf-8") as f:
        f.write(korean_content)
    files_created.append(korean_file)

    return {
        "folder_path": folder_path,
        "files_created": files_created,
        "pdf_moved": new_pdf_path,
    }


def process_download_list():
    """download_list.md 처리"""
    download_list_path = DOWN_DIR / "download_list.md"
    if not download_list_path.exists():
        return {"status": "no_list", "processed": 0}

    print("download_list.md 처리 시작...")
    # TODO: 실제 다운로드 로직 구현
    return {"status": "processed", "processed": 0}  # 임시


def main():
    """메인 처리 함수"""
    print("01_down 폴더 PDF 처리 시작...")

    # 디렉토리 확인
    if not DOWN_DIR.exists():
        print(f"{DOWN_DIR} 폴더가 존재하지 않습니다.")
        return

    PAPER_DIR.mkdir(exist_ok=True)

    # PDF 파일 찾기
    pdf_files = list(DOWN_DIR.glob("*.pdf"))
    print(f"PDF 파일 {len(pdf_files)}개 발견")

    processed_pdfs = []

    for idx, pdf_path in enumerate(pdf_files):
        print(f"\n처리 중 ({idx + 1}/{len(pdf_files)}): {pdf_path.name}")

        # 메타데이터 추출
        metadata = extract_metadata_from_pdf(pdf_path)
        print(f"   타입: {metadata['type']}")
        print(f"   제목: {metadata.get('title', 'Unknown')}")

        # 폴더 ID 생성
        folder_id = generate_folder_id()
        print(f"   폴더ID: {folder_id}")

        # 표준 폴더 생성
        try:
            result = create_standard_folder(folder_id, metadata, pdf_path)
            processed_pdfs.append(
                {"folder_id": folder_id, "metadata": metadata, "result": result}
            )
            print(f"   성공: {result['folder_path']}")
        except Exception as e:
            print(f"   실패: {e}")
            continue

        # 마지막 PDF가 아니면 60초 대기 (폴더 ID 중복 방지)
        if idx < len(pdf_files) - 1:
            print(f"   다음 PDF 처리를 위해 60초 대기 중...")
            time.sleep(60)

    # download_list.md 처리
    print(f"\ndownload_list.md 처리...")
    list_result = process_download_list()

    # 결과 요약
    print(f"\n처리 결과:")
    print(f"   PDF 처리: {len(processed_pdfs)}개 성공")
    print(f"   리스트 처리: {list_result.get('processed', 0)}개")

    # paper_list.md 업데이트
    update_paper_list(processed_pdfs)

    print(f"\n처리 완료!")


def update_paper_list(processed_pdfs):
    """paper_list.md 업데이트"""
    paper_list_path = PAPER_DIR / "paper_list.md"

    # 기존 내용 읽기
    if paper_list_path.exists():
        with open(paper_list_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = """# d0014_논문리스트.md - 논문 목록

## 문서 이력
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-21 | 최초 작성 |

---

## 총 논문수
**N개** (완료: X개, 미완료: Y개)

---

## 논문리스트

"""

    # 새로운 논문 추가
    new_entries = []
    for pdf_info in processed_pdfs:
        folder_id = pdf_info["folder_id"]
        metadata = pdf_info["metadata"]
        title = metadata.get("title", "Unknown")

        entry = f"""### {folder_id} - {title}
- **저자**: - | **연도**: - | **출처**: -
- **등록일**: {datetime.now().strftime("%Y-%m-%d")} | **완료**: X

"""
        new_entries.append(entry)

    # 업데이트
    if new_entries:
        content += "\n".join(new_entries)

        with open(paper_list_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"paper_list.md 업데이트 완료 ({len(new_entries)}개 추가)")


if __name__ == "__main__":
    main()
