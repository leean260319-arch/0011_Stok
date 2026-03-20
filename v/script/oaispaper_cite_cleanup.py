#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaispaper 인용정리 - 검증 불가 인용 제거 및 재번호

Usage:
    uv run python v/script/oaispaper_cite_cleanup.py [--input FILE] [--output FILE] [--dry-run]
"""

import re
import argparse
from pathlib import Path
from datetime import datetime


def identify_missing_citations(content: str, paper_dir: Path) -> list[str]:
    """검증 불가능한 인용 번호 식별"""
    # 모든 인용 번호 추출
    citation_pattern = r'\[(\d{3})\]'
    all_citations = set(re.findall(citation_pattern, content))

    # 논문 파일 존재하는 폴더 목록
    existing_folders = set()
    if paper_dir.exists():
        for folder in paper_dir.iterdir():
            if folder.is_dir():
                # 서머리 파일이 있으면 유효한 논문
                if list(folder.glob('*서머리.md')) or list(folder.glob('*.pdf')):
                    existing_folders.add(folder.name)

    # 매핑 테이블 로드 시도
    mapping_file = Path('doc/citation_mapping_table.md')
    citation_to_folder = {}

    if mapping_file.exists():
        map_content = mapping_file.read_text(encoding='utf-8')
        for line in map_content.split('\n'):
            if line.startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 7 and parts[1].isdigit():
                    citation_to_folder[parts[1].zfill(3)] = parts[6]

    # 검증 불가 목록
    missing = []
    for num in all_citations:
        folder_id = citation_to_folder.get(num)
        if folder_id and folder_id not in existing_folders:
            missing.append(num)

    return sorted(missing, key=int)


def remove_unverified_citations(content: str, missing_numbers: list[str]) -> tuple[str, int]:
    """검증 불가능한 인용 제거"""
    removed_count = 0

    for num in missing_numbers:
        # 패턴: Author... (Year)[NUMBER]
        pattern = rf'([A-Z][^\(]*?\(\d{{4}}\))\[{num}\]'

        matches = list(re.finditer(pattern, content))
        removed_count += len(matches)

        # 뒤에서부터 제거
        for match in reversed(matches):
            start, end = match.span()
            content = content[:start] + content[end:]

    return content, removed_count


def renumber_citations(content: str) -> tuple[str, int]:
    """남은 인용 순차 재번호"""
    citation_pattern = r'\[(\d{3})\]'

    # 모든 인용 위치와 현재 번호 수집
    matches = list(re.finditer(citation_pattern, content))

    # 위치별 새 번호 매핑 (등장 순서대로)
    seen_numbers = {}
    position_to_new_number = {}
    new_number = 1

    for match in matches:
        old_num = match.group(1)
        if old_num not in seen_numbers:
            seen_numbers[old_num] = new_number
            new_number += 1
        position_to_new_number[(match.start(), match.end())] = seen_numbers[old_num]

    # 뒤에서부터 교체
    for (start, end), num in reversed(sorted(position_to_new_number.items())):
        new_citation = f"[{num:03d}]"
        content = content[:start] + new_citation + content[end:]

    return content, len(seen_numbers)


def main():
    parser = argparse.ArgumentParser(description='검증 불가 인용 제거 및 재번호')
    parser.add_argument('--input', '-i', required=True, help='보고서 파일')
    parser.add_argument('--output', '-o', help='출력 파일 (기본: 입력파일_v02.md)')
    parser.add_argument('--paper-dir', default='02_paper', help='논문 폴더 경로')
    parser.add_argument('--dry-run', action='store_true', help='실행 없이 미리보기')

    args = parser.parse_args()

    input_file = Path(args.input)
    paper_dir = Path(args.paper_dir)

    if args.output:
        output_file = Path(args.output)
    else:
        stem = input_file.stem
        if '_v' in stem:
            # 버전 증가
            base, ver = stem.rsplit('_v', 1)
            new_ver = int(ver) + 1 if ver.isdigit() else 2
            output_file = input_file.with_name(f"{base}_v{new_ver:02d}{input_file.suffix}")
        else:
            output_file = input_file.with_name(f"{stem}_v02{input_file.suffix}")

    print("=" * 50)
    print("oaispaper 인용정리")
    print("=" * 50)

    if not input_file.exists():
        print(f"[ERROR] 파일이 없습니다: {input_file}")
        return 1

    content = input_file.read_text(encoding='utf-8')

    # 1. 검증 불가 인용 식별
    print(f"\n[1/3] 검증 불가 인용 식별")
    missing = identify_missing_citations(content, paper_dir)
    print(f"      검증 불가: {len(missing)}개")
    if missing:
        print(f"      번호: {', '.join(missing)}")

    # 2. 인용 제거
    print(f"\n[2/3] 인용 제거")
    content, removed = remove_unverified_citations(content, missing)
    print(f"      제거됨: {removed}개")

    # 3. 재번호
    print(f"\n[3/3] 인용 재번호")
    content, final_count = renumber_citations(content)
    print(f"      최종 인용 수: {final_count}개")

    if args.dry_run:
        print(f"\n[DRY-RUN] 실제 저장하지 않음")
        print(f"출력 예정: {output_file}")
    else:
        output_file.write_text(content, encoding='utf-8')
        print(f"\n" + "=" * 50)
        print(f"완료: {output_file}")
        print("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
