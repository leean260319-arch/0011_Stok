#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaispaper 인용매핑 - 논문 코드 매핑 테이블 생성

Usage:
    uv run python v/script/oaispaper_cite_mapping.py [--output FILE] [--group GROUP]
"""

import re
import argparse
from pathlib import Path
from datetime import datetime


def scan_paper_folders(paper_dir: Path) -> list[dict]:
    """02_paper 폴더에서 논문 정보 수집"""
    papers = []

    for folder in sorted(paper_dir.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name.startswith('.'):
            continue
        if folder.name == 'paper_list.md':
            continue

        # 서머리 파일 찾기
        summary_files = list(folder.glob('*_00_*_서머리.md'))
        if not summary_files:
            summary_files = list(folder.glob('*서머리.md'))

        paper_info = {
            'folder_id': folder.name,
            'author': '-',
            'year': '-',
            'code': folder.name,
            'title': '-',
            'group': 'Z'  # 기본 그룹
        }

        # 서머리에서 정보 추출
        if summary_files:
            summary_file = summary_files[0]
            try:
                content = summary_file.read_text(encoding='utf-8')

                # 저자 추출
                author_match = re.search(r'[-*]\s*\*?\*?저자\*?\*?[:\s]+(.+)', content)
                if author_match:
                    paper_info['author'] = author_match.group(1).strip()

                # 연도 추출 (출처에서)
                source_match = re.search(r'[-*]\s*\*?\*?출처\*?\*?[:\s]+(.+)', content)
                if source_match:
                    source = source_match.group(1)
                    year_match = re.search(r'(20\d{2}|19\d{2})', source)
                    if year_match:
                        paper_info['year'] = year_match.group(1)

                # 제목 추출
                title_match = re.search(r'[-*]\s*\*?\*?(제목|논문\s*제목)\*?\*?[:\s]+(.+)', content)
                if title_match:
                    paper_info['title'] = title_match.group(2).strip()

            except Exception as e:
                print(f"[WARN] {folder.name} 서머리 읽기 실패: {e}")

        papers.append(paper_info)

    return papers


def assign_group_codes(papers: list[dict], group_by: str = 'keyword') -> list[dict]:
    """논문에 그룹 코드 부여"""
    # 간단한 그룹 분류 (키워드 기반)
    group_counter = {}

    for paper in papers:
        group = 'Z'  # 기본

        title_lower = paper['title'].lower()
        if 'deep' in title_lower or 'neural' in title_lower or 'cnn' in title_lower:
            group = 'A'  # 딥러닝
        elif 'transformer' in title_lower or 'attention' in title_lower:
            group = 'B'  # 트랜스포머
        elif 'crack' in title_lower or 'defect' in title_lower:
            group = 'C'  # 결함 검출
        elif 'segment' in title_lower or 'detection' in title_lower:
            group = 'D'  # 세그멘테이션/검출
        elif 'blur' in title_lower or 'deblur' in title_lower:
            group = 'E'  # 블러/디블러

        # 그룹 내 번호 부여
        if group not in group_counter:
            group_counter[group] = 0
        group_counter[group] += 1

        paper['group'] = group
        paper['code'] = f"{group}{group_counter[group]:02d}"

    return papers


def generate_mapping_table(papers: list[dict], output_file: Path):
    """매핑 테이블 생성"""
    lines = []
    lines.append("# 인용 매핑 테이블\n")
    lines.append(f"\n생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"총 논문 수: {len(papers)}개\n")
    lines.append("\n---\n")
    lines.append("\n| 번호 | 그룹 | 저자 | 연도 | 코드 | 폴더ID | 비고 |")
    lines.append("\n|------|------|------|------|------|--------|------|")

    for i, paper in enumerate(papers, 1):
        author = paper['author'][:20] + '...' if len(paper['author']) > 20 else paper['author']
        title = paper['title'][:15] + '...' if len(paper['title']) > 15 else paper['title']
        lines.append(f"\n| {i} | {paper['group']} | {author} | {paper['year']} | {paper['code']} | {paper['folder_id']} | {title} |")

    lines.append("\n")

    output_file.write_text(''.join(lines), encoding='utf-8')
    return len(papers)


def main():
    parser = argparse.ArgumentParser(description='논문 코드 매핑 테이블 생성')
    parser.add_argument('--paper-dir', default='02_paper', help='논문 폴더 경로')
    parser.add_argument('--output', '-o', default='doc/citation_mapping_table.md', help='출력 파일')
    parser.add_argument('--group', default='keyword', choices=['keyword', 'year', 'none'], help='그룹 분류 기준')

    args = parser.parse_args()

    paper_dir = Path(args.paper_dir)
    output_file = Path(args.output)

    print("=" * 50)
    print("oaispaper 인용매핑")
    print("=" * 50)

    if not paper_dir.exists():
        print(f"[ERROR] 논문 폴더가 없습니다: {paper_dir}")
        return 1

    # 1. 논문 스캔
    print(f"\n[1/3] 논문 폴더 스캔: {paper_dir}")
    papers = scan_paper_folders(paper_dir)
    print(f"      발견된 논문: {len(papers)}개")

    # 2. 그룹 코드 부여
    print(f"\n[2/3] 그룹 코드 부여 (기준: {args.group})")
    papers = assign_group_codes(papers, args.group)

    # 3. 매핑 테이블 생성
    print(f"\n[3/3] 매핑 테이블 생성")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    count = generate_mapping_table(papers, output_file)

    print(f"\n" + "=" * 50)
    print(f"완료: {output_file}")
    print(f"총 {count}개 논문 매핑")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
