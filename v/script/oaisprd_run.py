#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaisprd_run.py

PRD 문서 생성 및 관리 스크립트

명령어:
    oaisprd run              새 PRD 문서 생성 (기본)
    oaisprd run [번호]       서브프로젝트 PRD 생성
    oaisprd template         PRD 템플릿 구조 조회
    oaisprd validate         PRD 구조 검증 및 누락 항목 체크
    oaisprd update           PRD 현행화 (실제 프로젝트와 동기화)
    oaisprd section [번호]   특정 섹션만 생성/갱신
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DOC_DIR = PROJECT_ROOT / "doc"
PRD_FILE = DOC_DIR / "d0001_prd.md"

# PRD 필수/권장/선택 섹션
REQUIRED_SECTIONS = [
    "1. 문서 관리",
    "2. 프로젝트 개요",
    "4. 기능 요구사항",
    "5. 기술 요구사항"
]

RECOMMENDED_SECTIONS = [
    "3. 사용자 및 요구사항",
    "6. 비기능 요구사항",
    "7. 테스트 및 품질 관리"
]

OPTIONAL_SECTIONS = [
    "8. 배포 및 운영 가이드",
    "9. 프로젝트 관리",
    "10. 부록"
]


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaisprd - PRD 문서 생성 및 관리")
    print()
    print("사용법:")
    print("    oaisprd run              새 PRD 문서 생성 (기본)")
    print("    oaisprd run [번호]       서브프로젝트 PRD 생성")
    print("    oaisprd template         PRD 템플릿 구조 조회")
    print("    oaisprd validate         PRD 구조 검증 및 누락 항목 체크")
    print("    oaisprd update           PRD 현행화")
    print("    oaisprd section [번호]   특정 섹션만 생성/갱신")
    print()
    print("예시:")
    print("    python v/script/oaisprd_run.py run")
    print("    python v/script/oaisprd_run.py validate")
    print("    python v/script/oaisprd_run.py template")


def get_prd_path(doc_number=None):
    """PRD 파일 경로 반환"""
    if doc_number:
        return DOC_DIR / f"d{doc_number}_prd.md"
    return PRD_FILE


def parse_prd_sections(content):
    """PRD 문서에서 섹션 추출"""
    sections = []

    # ## N. 섹션명 패턴
    pattern = r"^##\s+(\d+)\.\s+(.+?)$"

    for line in content.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            num = match.group(1)
            name = match.group(2).strip()
            sections.append({
                "number": num,
                "name": name,
                "full": f"{num}. {name}"
            })

    return sections


def cmd_run(args):
    """PRD 문서 생성 (run 서브명령어)"""
    print("# oaisprd run\n")

    doc_number = args[0] if args else None
    prd_path = get_prd_path(doc_number)

    if prd_path.exists():
        print(f"[WARN] {prd_path}가 이미 존재합니다.")
        if "--force" not in sys.argv:
            print("[INFO] 덮어쓰려면 --force 옵션을 사용하세요.")
            return 1

    today = datetime.now().strftime("%Y-%m-%d")
    project_name = PROJECT_ROOT.name

    template = f"""# PRD: {project_name}

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| v1.0 | {today} | 최초 작성 | oaisprd |

---

## 1. 문서 관리

### 1.1 문서 정보

| 항목 | 내용 |
|------|------|
| 제목 | {project_name} PRD |
| 버전 | v1.0 |
| 작성일 | {today} |

### 1.2 용어 정의

| 용어 | 정의 |
|------|------|
| PRD | Product Requirements Document |

---

## 2. 프로젝트 개요

### 2.1 배경 및 비즈니스 케이스

**문제 정의:**
- (해결하고자 하는 문제)

### 2.2 비전 및 목표

**비전:**
> (프로젝트 비전)

**목표:**
- (목표 1)
- (목표 2)

### 2.3 범위

**In-Scope:**
- (포함 범위)

**Out-of-Scope:**
- (제외 범위)

---

## 3. 사용자 및 요구사항

### 3.1 타겟 사용자

| 사용자 유형 | 설명 |
|------------|------|
| (유형) | (설명) |

### 3.2 사용자 스토리

- As a (사용자), I want to (행동), so that (목적)

---

## 4. 기능 요구사항

### 4.1 기능 목록

| ID | 기능명 | 설명 | 우선순위 | 상태 |
|----|--------|------|---------|------|
| F001 | (기능명) | (설명) | Must | 계획 |

---

## 5. 기술 요구사항

### 5.1 기술 스택

| 레이어 | 기술 | 버전 |
|--------|------|------|
| Frontend | - | - |
| Backend | Python | 3.10+ |
| Database | SQLite | 3.x |

### 5.2 시스템 아키텍처

(아키텍처 설명)

---

## 6. 비기능 요구사항

### 6.1 성능

| 항목 | 요구사항 |
|------|---------|
| 응답시간 | < 500ms |

### 6.2 보안

- (보안 요구사항)

---

## 7. 테스트 및 품질 관리

### 7.1 테스트 전략

- 단위 테스트
- 통합 테스트
- E2E 테스트

---

## 8. 배포 및 운영 가이드

### 8.1 배포 전략

(배포 방법)

---

## 9. 프로젝트 관리

### 9.1 일정

| 마일스톤 | 일정 | 상태 |
|----------|------|------|
| M1 | (날짜) | 계획 |

---

## 10. 부록

### 10.1 용어집

| 용어 | 정의 |
|------|------|
| - | - |

---
"""

    DOC_DIR.mkdir(parents=True, exist_ok=True)
    prd_path.write_text(template, encoding="utf-8")

    print(f"[OK] PRD 문서 생성됨: {prd_path}")
    return 0


def cmd_template():
    """PRD 템플릿 구조 조회 (template 서브명령어)"""
    print("# oaisprd template\n")

    print("## PRD 표준 템플릿 구조\n")

    print("### 필수 섹션 (Must)")
    for s in REQUIRED_SECTIONS:
        print(f"  - {s}")

    print()
    print("### 권장 섹션 (Should)")
    for s in RECOMMENDED_SECTIONS:
        print(f"  - {s}")

    print()
    print("### 선택 섹션 (Could)")
    for s in OPTIONAL_SECTIONS:
        print(f"  - {s}")

    print()
    print("---")
    print("전체 10개 섹션")

    return 0


def cmd_validate():
    """PRD 구조 검증 (validate 서브명령어)"""
    print("# oaisprd validate\n")

    if not PRD_FILE.exists():
        print(f"[ERROR] {PRD_FILE}가 없습니다.")
        print("[TIP] oaisprd run 으로 생성하세요.")
        return 1

    content = PRD_FILE.read_text(encoding="utf-8")
    sections = parse_prd_sections(content)
    section_names = [s['full'] for s in sections]

    print(f"검증 대상: {PRD_FILE}")
    print(f"발견된 섹션: {len(sections)}개")
    print()

    # 필수 섹션 체크
    print("## 필수 섹션 (Must)\n")
    missing_required = []
    for req in REQUIRED_SECTIONS:
        found = any(req in name for name in section_names)
        status = "[OK]" if found else "[MISSING]"
        print(f"  {status} {req}")
        if not found:
            missing_required.append(req)

    # 권장 섹션 체크
    print()
    print("## 권장 섹션 (Should)\n")
    missing_recommended = []
    for rec in RECOMMENDED_SECTIONS:
        found = any(rec in name for name in section_names)
        status = "[OK]" if found else "[WARN]"
        print(f"  {status} {rec}")
        if not found:
            missing_recommended.append(rec)

    # 선택 섹션 체크
    print()
    print("## 선택 섹션 (Could)\n")
    for opt in OPTIONAL_SECTIONS:
        found = any(opt in name for name in section_names)
        status = "[OK]" if found else "[-]"
        print(f"  {status} {opt}")

    # 결과 요약
    print()
    print("---")
    print("## 검증 결과\n")

    if missing_required:
        print(f"[ERROR] 누락된 필수 섹션: {len(missing_required)}개")
        for m in missing_required:
            print(f"  - {m}")
    else:
        print("[OK] 모든 필수 섹션 존재")

    if missing_recommended:
        print(f"[WARN] 누락된 권장 섹션: {len(missing_recommended)}개")

    return 0 if not missing_required else 1


def cmd_update():
    """PRD 현행화 (update 서브명령어)"""
    print("# oaisprd update\n")

    if not PRD_FILE.exists():
        print(f"[ERROR] {PRD_FILE}가 없습니다.")
        return 1

    print(f"대상: {PRD_FILE}")
    print()

    # 프로젝트 분석
    print("## 프로젝트 분석\n")

    # pyproject.toml 확인
    pyproject = PROJECT_ROOT / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8")
        print("  [OK] pyproject.toml 발견")

        # Python 버전 추출
        version_match = re.search(r'requires-python\s*=\s*"([^"]+)"', content)
        if version_match:
            print(f"      Python: {version_match.group(1)}")

    # db 디렉토리 확인
    db_dir = PROJECT_ROOT / "db"
    if db_dir.exists():
        db_files = list(db_dir.glob("*.sqlite"))
        print(f"  [OK] DB 파일: {len(db_files)}개")

    # oais 디렉토리 확인
    oais_dir = PROJECT_ROOT / "oais"
    if oais_dir.exists():
        oais_modules = list(oais_dir.glob("*.py"))
        print(f"  [OK] oais 모듈: {len(oais_modules)}개")

    print()
    print("---")
    print("[INFO] PRD 수동 업데이트를 권장합니다.")
    print("[TIP] 위 분석 결과를 바탕으로 PRD를 갱신하세요.")

    return 0


def cmd_section(args):
    """특정 섹션만 생성/갱신 (section 서브명령어)"""
    print("# oaisprd section\n")

    if not args:
        print("[ERROR] 섹션 번호를 지정하세요.")
        print("사용법: oaisprd section [번호]")
        print()
        print("사용 가능한 섹션:")
        all_sections = REQUIRED_SECTIONS + RECOMMENDED_SECTIONS + OPTIONAL_SECTIONS
        for s in all_sections:
            print(f"  - {s}")
        return 1

    section_num = args[0]

    all_sections = REQUIRED_SECTIONS + RECOMMENDED_SECTIONS + OPTIONAL_SECTIONS
    target = None
    for s in all_sections:
        if s.startswith(f"{section_num}."):
            target = s
            break

    if not target:
        print(f"[ERROR] 섹션 {section_num}를 찾을 수 없습니다.")
        return 1

    print(f"대상 섹션: {target}")
    print()
    print("[INFO] 해당 섹션의 수동 작성을 권장합니다.")
    print("[TIP] oaisprd template 으로 템플릿 구조를 확인하세요.")

    return 0


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisprd", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    cmd_args = args[1:]

    # 옵션 제거
    cmd_args = [a for a in cmd_args if not a.startswith("--")]

    if cmd == "run":
        return cmd_run(cmd_args)
    elif cmd == "template":
        return cmd_template()
    elif cmd == "validate":
        return cmd_validate()
    elif cmd == "update":
        return cmd_update()
    elif cmd == "section":
        return cmd_section(cmd_args)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
