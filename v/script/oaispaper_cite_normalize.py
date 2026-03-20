#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaispaper 인용정규화 - 인용 형식 통일 및 중복 제거

Usage:
    uv run python v/script/oaispaper_cite_normalize.py [--input FILE] [--output FILE] [--dry-run]
"""

import re
import argparse
from pathlib import Path
from datetime import datetime


def remove_code_prefix(content: str) -> tuple[str, int]:
    """[CODE][NUMBER] -> [NUMBER] 형식으로 변환"""
    # 패턴: [A01][001] -> [001]
    pattern = r'\[([A-Z]\d{2})\]\[(\d{3})\]'

    matches = list(re.finditer(pattern, content))
    count = len(matches)

    content = re.sub(pattern, r'[\2]', content)

    return content, count


def fix_full_duplicate(content: str) -> tuple[str, int]:
    """전체 중복 제거: Author (Year)Author (Year)[NUMBER] -> Author (Year)[NUMBER]"""
    fixed_count = 0

    # 패턴: 동일한 저자+연도가 연속으로 2번 나오는 경우
    pattern = r'([A-Z][a-zA-Z\s&.,]+?\s*\(\d{4}\))\s*\1(\[\d{3}\])'

    while True:
        match = re.search(pattern, content)
        if not match:
            break
        content = content[:match.start()] + match.group(1) + match.group(2) + content[match.end():]
        fixed_count += 1

    return content, fixed_count


def fix_korean_english_mixed(content: str) -> tuple[str, int]:
    """한글-영문 혼합 중복 제거: Park 등 (2014)Park et al. (2014)[006] -> Park et al. (2014)[006]"""
    fixed_count = 0

    # 패턴: Author 등 (Year)Author et al. (Year)[NUMBER]
    pattern = r'([A-Z][a-z]+)\s+등\s*\((\d{4})\)\s*\1\s+et al\.\s*\(\2\)(\[\d{3}\])'

    while True:
        match = re.search(pattern, content)
        if not match:
            break
        replacement = f"{match.group(1)} et al. ({match.group(2)}){match.group(3)}"
        content = content[:match.start()] + replacement + content[match.end():]
        fixed_count += 1

    return content, fixed_count


def fix_korean_connector(content: str) -> tuple[str, int]:
    """한글 연결사 중복 제거: Zhang과 Wang (2024)Zhang & Wang (2024)[003] -> Zhang & Wang (2024)[003]"""
    fixed_count = 0

    # 패턴: Author1과/와 Author2 (Year)Author1 & Author2 (Year)[NUMBER]
    pattern = r'([A-Z][a-z]+)[과와]\s+([A-Z][a-z]+)\s*\((\d{4})\)\s*\1\s+&\s+\2\s*\(\3\)(\[\d{3}\])'

    while True:
        match = re.search(pattern, content)
        if not match:
            break
        replacement = f"{match.group(1)} & {match.group(2)} ({match.group(3)}){match.group(4)}"
        content = content[:match.start()] + replacement + content[match.end():]
        fixed_count += 1

    return content, fixed_count


def fix_partial_duplicate(content: str) -> tuple[str, int]:
    """부분 중복 제거: Author et al.Author et al. (Year)[NUMBER] -> Author et al. (Year)[NUMBER]"""
    fixed_count = 0

    # 패턴: 저자명이 2번 반복되는 경우
    pattern = r'([A-Z][a-z]+(?:\s+et al\.)?)\s*\1\s*\((\d{4})\)(\[\d{3}\])'

    while True:
        match = re.search(pattern, content)
        if not match:
            break
        replacement = f"{match.group(1)} ({match.group(2)}){match.group(3)}"
        content = content[:match.start()] + replacement + content[match.end():]
        fixed_count += 1

    return content, fixed_count


def normalize_author_format(content: str) -> tuple[str, int]:
    """저자 형식 정규화: 일관된 et al. 사용"""
    fixed_count = 0

    # 패턴: 다양한 et al 변형을 표준화
    variations = [
        (r'et\s+al\s+\(', 'et al. ('),      # et al ( -> et al. (
        (r'et\s+al\.\s+\(', 'et al. ('),    # et al.  ( -> et al. (
        (r'et\.al\.\s*\(', 'et al. ('),     # et.al. ( -> et al. (
    ]

    for pattern, replacement in variations:
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            fixed_count += matches

    return content, fixed_count


def validate_citation_sequence(content: str) -> list[str]:
    """인용 번호 순서 검증"""
    pattern = r'\[(\d{3})\]'
    matches = re.findall(pattern, content)

    warnings = []
    seen = set()
    prev_num = 0

    for num_str in matches:
        num = int(num_str)

        # 첫 등장 확인
        if num not in seen:
            seen.add(num)
            if num != prev_num + 1 and prev_num > 0:
                warnings.append(f"비순차 번호: [{prev_num:03d}] -> [{num:03d}]")
            prev_num = num

    return warnings


def main():
    parser = argparse.ArgumentParser(description='인용 형식 정규화 및 중복 제거')
    parser.add_argument('--input', '-i', required=True, help='보고서 파일')
    parser.add_argument('--output', '-o', help='출력 파일 (기본: 입력파일_normalized.md)')
    parser.add_argument('--dry-run', action='store_true', help='실행 없이 미리보기')
    parser.add_argument('--validate-only', action='store_true', help='검증만 실행')

    args = parser.parse_args()

    input_file = Path(args.input)

    if args.output:
        output_file = Path(args.output)
    else:
        stem = input_file.stem
        output_file = input_file.with_name(f"{stem}_normalized{input_file.suffix}")

    print("=" * 50)
    print("oaispaper 인용정규화")
    print("=" * 50)

    if not input_file.exists():
        print(f"[ERROR] 파일이 없습니다: {input_file}")
        return 1

    content = input_file.read_text(encoding='utf-8')
    original_content = content

    # 검증만 실행
    if args.validate_only:
        print(f"\n[검증] 인용 순서 확인")
        warnings = validate_citation_sequence(content)
        if warnings:
            for w in warnings:
                print(f"      [WARN] {w}")
        else:
            print("      [OK] 인용 순서 정상")
        return 0

    total_fixes = 0

    # 1. 코드 prefix 제거
    print(f"\n[1/5] 코드 prefix 제거")
    content, count = remove_code_prefix(content)
    print(f"      수정: {count}개")
    total_fixes += count

    # 2. 전체 중복 제거
    print(f"\n[2/5] 전체 중복 제거")
    content, count = fix_full_duplicate(content)
    print(f"      수정: {count}개")
    total_fixes += count

    # 3. 한글-영문 혼합 중복 제거
    print(f"\n[3/5] 한글-영문 혼합 중복 제거")
    content, count = fix_korean_english_mixed(content)
    print(f"      수정: {count}개")
    total_fixes += count

    # 4. 한글 연결사 중복 제거
    print(f"\n[4/5] 한글 연결사 중복 제거")
    content, count = fix_korean_connector(content)
    print(f"      수정: {count}개")
    total_fixes += count

    # 5. 저자 형식 정규화
    print(f"\n[5/5] 저자 형식 정규화")
    content, count = normalize_author_format(content)
    print(f"      수정: {count}개")
    total_fixes += count

    # 추가: 부분 중복 제거
    content, count = fix_partial_duplicate(content)
    if count > 0:
        print(f"\n[추가] 부분 중복 제거: {count}개")
        total_fixes += count

    # 검증
    print(f"\n[검증] 인용 순서 확인")
    warnings = validate_citation_sequence(content)
    if warnings:
        for w in warnings:
            print(f"      [WARN] {w}")
    else:
        print("      [OK] 인용 순서 정상")

    print(f"\n총 수정: {total_fixes}개")

    if args.dry_run:
        print(f"\n[DRY-RUN] 실제 저장하지 않음")
        print(f"출력 예정: {output_file}")
    else:
        if content != original_content:
            output_file.write_text(content, encoding='utf-8')
            print(f"\n" + "=" * 50)
            print(f"완료: {output_file}")
            print("=" * 50)
        else:
            print(f"\n[INFO] 변경사항 없음")

    return 0


if __name__ == "__main__":
    exit(main())
