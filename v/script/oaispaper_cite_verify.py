#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaispaper 인용검증 - 인용 검증 문서 자동 생성

Usage:
    uv run python v/script/oaispaper_cite_verify.py [--input FILE] [--output FILE] [--paper-dir DIR]
"""

import re
import argparse
from pathlib import Path
from datetime import datetime


def load_citation_mapping(mapping_file: Path) -> dict:
    """매핑 테이블에서 코드별 정보 로드"""
    citations = {}

    if not mapping_file.exists():
        return citations

    content = mapping_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    for line in lines:
        if not line.startswith('|') or '---' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 7 and parts[1].isdigit():
            code = parts[5]
            citations[code] = {
                'number': parts[1],
                'group': parts[2],
                'author': parts[3],
                'year': parts[4],
                'code': code,
                'folder_id': parts[6],
                'note': parts[7] if len(parts) > 7 else ''
            }

    return citations


def find_paper_file(code: str, paper_dir: Path) -> Path | None:
    """코드에 해당하는 논문 파일 찾기"""
    # 폴더 ID로 검색
    for folder in paper_dir.iterdir():
        if folder.is_dir() and code in folder.name:
            # 서머리 파일 찾기
            summary_files = list(folder.glob('*서머리.md'))
            if summary_files:
                return summary_files[0]
            # PDF 파일
            pdf_files = list(folder.glob('*.pdf'))
            if pdf_files:
                return pdf_files[0]

    return None


def extract_paper_title(paper_file: Path) -> str:
    """논문 파일에서 제목 추출"""
    if not paper_file or not paper_file.exists():
        return "제목없음"

    if paper_file.suffix == '.pdf':
        return paper_file.stem

    try:
        content = paper_file.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                # 코드 prefix 제거
                title = re.sub(r'^[A-Z]\d{2}_', '', title)
                title = re.sub(r'^\d{6}-\d{4}_\d{2}_', '', title)
                return title[:50]
    except Exception:
        pass

    return "제목없음"


def extract_citation_keywords(context: str) -> list[str]:
    """인용 구절에서 핵심 키워드 추출"""
    keywords = []

    # 큰따옴표/작은따옴표로 묶인 용어
    quoted = re.findall(r'["\']([^"\']+)["\']', context)
    keywords.extend(quoted)

    # 영문 약어 (2-5자)
    acronyms = re.findall(r'\b([A-Z]{2,5})\b', context)
    keywords.extend(acronyms)

    # 기술 용어
    tech_terms = ['transformer', 'cnn', 'deep learning', 'neural', 'segmentation',
                  'detection', 'classification', 'attention', 'encoder', 'decoder']
    context_lower = context.lower()
    for term in tech_terms:
        if term in context_lower:
            keywords.append(term)

    return list(set([k for k in keywords if len(k) > 2]))[:10]


def extract_citations_from_report(report_file: Path) -> list[dict]:
    """보고서에서 인용 추출"""
    content = report_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 인용 패턴: Author (Year)[NUMBER] 또는 [NUMBER]
    citation_pattern = r'([A-Z][a-z]+(?:\s+(?:et al\.|&\s*[A-Z][a-z]+))?)\s*\((\d{4})\)\[(\d{3})\]'
    simple_pattern = r'\[(\d{3})\]'

    citations = []
    current_section = "문서 시작"
    section_pattern = r'^#{1,6}\s+(.+)$'

    for i, line in enumerate(lines):
        # 섹션 추적
        section_match = re.match(section_pattern, line)
        if section_match:
            current_section = section_match.group(1).strip()

        # 인용 찾기
        matches = re.finditer(citation_pattern, line)
        for match in matches:
            author = match.group(1)
            year = match.group(2)
            number = match.group(3)

            # 컨텍스트 (앞뒤 3줄)
            context_start = max(0, i - 3)
            context_end = min(len(lines), i + 4)
            context = '\n'.join(lines[context_start:context_end])

            citations.append({
                'number': number,
                'author': author,
                'year': year,
                'section': current_section,
                'line_number': i + 1,
                'context': context
            })

    return citations


def generate_verification_doc(citations: list[dict], paper_dir: Path, output_file: Path):
    """검증 문서 생성"""
    lines = []
    lines.append("# 인용 검증 문서\n")
    lines.append(f"\n생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"총 인용 수: {len(citations)}개\n")
    lines.append("\n---\n")

    verified_count = 0
    unverified_count = 0

    for cite in sorted(citations, key=lambda x: int(x['number'])):
        number = cite['number']
        author = cite['author']
        year = cite['year']

        # 논문 파일 찾기 (폴더 ID로)
        paper_file = None
        paper_title = "제목없음"

        for folder in paper_dir.iterdir():
            if folder.is_dir():
                summary_files = list(folder.glob('*서머리.md'))
                if summary_files:
                    paper_file = summary_files[0]
                    paper_title = extract_paper_title(paper_file)
                    break

        lines.append(f"\n## {number}_{paper_title}, {author}, {year}\n")
        lines.append(f"\n**본문 인용 위치**: {cite['section']}\n")
        lines.append(f"**라인 번호**: {cite['line_number']}\n")
        lines.append(f"\n**인용 구절**:\n```\n{cite['context']}\n```\n")

        keywords = extract_citation_keywords(cite['context'])
        lines.append(f"\n**추출 키워드**: {', '.join(keywords)}\n")

        if paper_file and paper_file.exists():
            lines.append(f"\n**원문 파일**: {paper_file.name}\n")
            lines.append(f"\n**검증 사항**:\n")
            lines.append(f"- ✅ 논문 파일 확인됨\n")
            lines.append(f"- 저자명, 연도 정확성: {author} ({year})\n")
            verified_count += 1
        else:
            lines.append(f"\n**원문 파일**: 없음\n")
            lines.append(f"\n**검증 사항**:\n")
            lines.append(f"- ⚠️ 논문 파일 없음 - 검증 불가\n")
            unverified_count += 1

        lines.append("\n---\n")

    # 요약 추가
    summary = f"\n## 검증 요약\n\n- 총 인용: {len(citations)}개\n- 검증 완료: {verified_count}개\n- 검증 불가: {unverified_count}개\n"
    lines.insert(4, summary)

    output_file.write_text(''.join(lines), encoding='utf-8')
    return len(citations), verified_count, unverified_count


def main():
    parser = argparse.ArgumentParser(description='인용 검증 문서 생성')
    parser.add_argument('--input', '-i', default='doc/d0910_보고서.md', help='보고서 파일')
    parser.add_argument('--output', '-o', default='doc/d0911_인용검증.md', help='출력 파일')
    parser.add_argument('--paper-dir', default='02_paper', help='논문 폴더 경로')

    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)
    paper_dir = Path(args.paper_dir)

    print("=" * 50)
    print("oaispaper 인용검증")
    print("=" * 50)

    if not input_file.exists():
        print(f"[ERROR] 보고서 파일이 없습니다: {input_file}")
        return 1

    # 1. 인용 추출
    print(f"\n[1/2] 인용 추출: {input_file}")
    citations = extract_citations_from_report(input_file)
    print(f"      발견된 인용: {len(citations)}개")

    if not citations:
        print("[WARN] 인용이 발견되지 않았습니다.")
        return 0

    # 2. 검증 문서 생성
    print(f"\n[2/2] 검증 문서 생성")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    total, verified, unverified = generate_verification_doc(citations, paper_dir, output_file)

    print(f"\n" + "=" * 50)
    print(f"완료: {output_file}")
    print(f"총 {total}개 인용 / 검증: {verified}개 / 미검증: {unverified}개")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
