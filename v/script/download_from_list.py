#!/usr/bin/env python3
"""
download_from_list.py
arXiv ID 기반 논문 PDF 다운로드 스크립트
"""

import os
import re
import time
import urllib.request
from pathlib import Path

# 경로 설정
BASE_DIR = Path(__file__).parent.parent.parent
DOWN_DIR = BASE_DIR / "01_down"
TMP_DIR = BASE_DIR / "tmp"


def download_arxiv_pdf(arxiv_id, output_dir):
    """arXiv PDF 다운로드"""
    arxiv_id = arxiv_id.strip()
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    output_path = output_dir / f"{arxiv_id.replace('.', '')}.pdf"

    print(f"  다운로드 중: {arxiv_id}")
    print(f"  URL: {pdf_url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(pdf_url, headers=headers)

        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()

            if not content.startswith(b'%PDF'):
                print(f"  경고: PDF 형식이 아닐 수 있음")

            with open(output_path, 'wb') as f:
                f.write(content)

        print(f"  완료: {output_path.name} ({len(content) / 1024:.1f} KB)")
        return True

    except urllib.error.HTTPError as e:
        print(f"  HTTP 오류: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"  URL 오류: {e.reason}")
        return False
    except Exception as e:
        print(f"  오류: {e}")
        return False


def parse_download_list(list_path):
    """download_list.md에서 arXiv ID 추출"""
    arxiv_ids = []

    with open(list_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'\*\*arXiv\*\*:\s*(\d{4}\.\d{4,5})'
    matches = re.findall(pattern, content)

    for match in matches:
        arxiv_ids.append(match)

    return arxiv_ids


def main():
    """메인 함수"""
    print("=" * 60)
    print("arXiv 논문 다운로드 시작")
    print("=" * 60)

    DOWN_DIR.mkdir(exist_ok=True)

    list_path = DOWN_DIR / "download_list.md"
    if not list_path.exists():
        print(f"오류: {list_path} 파일이 없습니다.")
        return

    arxiv_ids = parse_download_list(list_path)
    print(f"\n발견된 arXiv ID: {len(arxiv_ids)}개")
    for aid in arxiv_ids:
        print(f"  - {aid}")

    print(f"\n다운로드 시작...")
    success_count = 0
    fail_list = []

    for idx, arxiv_id in enumerate(arxiv_ids, 1):
        print(f"\n[{idx}/{len(arxiv_ids)}] arXiv:{arxiv_id}")

        existing = list(DOWN_DIR.glob(f"*{arxiv_id.replace('.', '')}*.pdf"))
        if existing:
            print(f"  건너뜀: 이미 존재 ({existing[0].name})")
            success_count += 1
            continue

        if download_arxiv_pdf(arxiv_id, DOWN_DIR):
            success_count += 1
        else:
            fail_list.append(arxiv_id)

        if idx < len(arxiv_ids):
            print(f"  대기 중 (3초)...")
            time.sleep(3)

    print(f"\n{'=' * 60}")
    print(f"다운로드 완료")
    print(f"{'=' * 60}")
    print(f"  성공: {success_count}/{len(arxiv_ids)}")
    print(f"  실패: {len(fail_list)}")

    if fail_list:
        print(f"\n실패 목록:")
        for aid in fail_list:
            print(f"  - arXiv:{aid}")


if __name__ == "__main__":
    main()
