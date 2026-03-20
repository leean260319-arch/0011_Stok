#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaisuser_run.py

사용자 가이드 문서 관리 스크립트

명령어:
    oaisuser run              d0008_user.md 신규 생성 (기본)
    oaisuser status           d0008_user.md 현황 조회
    oaisuser add [기능명]     특정 기능 사용법 추가
    oaisuser faq [질문]       FAQ 항목 추가
    oaisuser update           전체 문서 현행화
    oaisuser sync             PRD 기반 기능 목록 동기화
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DOC_DIR = PROJECT_ROOT / "doc"
USER_FILE = DOC_DIR / "d0008_user.md"
PRD_FILE = DOC_DIR / "d0001_prd.md"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaisuser - 사용자 가이드 문서 관리")
    print()
    print("사용법:")
    print("    oaisuser run              d0008_user.md 신규 생성 (기본)")
    print("    oaisuser status           d0008_user.md 현황 조회")
    print("    oaisuser add [기능명]     특정 기능 사용법 추가")
    print("    oaisuser faq [질문]       FAQ 항목 추가")
    print("    oaisuser update           전체 문서 현행화")
    print("    oaisuser sync             PRD 기반 기능 목록 동기화")
    print()
    print("예시:")
    print("    python v/script/oaisuser_run.py run")
    print("    python v/script/oaisuser_run.py add \"로그인\"")
    print("    python v/script/oaisuser_run.py faq \"비밀번호 분실\"")
    print("    python v/script/oaisuser_run.py sync")


def parse_user_sections(content):
    """d0008_user.md에서 섹션 추출"""
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


def parse_features(content):
    """d0008_user.md에서 기능 목록 추출"""
    features = []

    # ### N.N [기능명] 패턴
    pattern = r"^###\s+(\d+\.\d+)\s+(.+?)$"

    for line in content.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            num = match.group(1)
            name = match.group(2).strip()
            features.append({
                "number": num,
                "name": name
            })

    return features


def parse_faq(content):
    """d0008_user.md에서 FAQ 추출"""
    faqs = []

    # #### Q: 질문 패턴
    pattern = r"^####\s+Q:\s+(.+?)$"

    for line in content.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            question = match.group(1).strip()
            faqs.append(question)

    return faqs


def extract_prd_features():
    """d0001_prd.md에서 기능 요구사항 추출"""
    if not PRD_FILE.exists():
        return []

    content = PRD_FILE.read_text(encoding="utf-8")
    features = []

    # | F001 | 기능명 | 설명 | 우선순위 | 상태 | 패턴
    pattern = r"\|\s*(F\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"

    for match in re.finditer(pattern, content):
        fid = match.group(1).strip()
        name = match.group(2).strip()
        desc = match.group(3).strip()
        if name and name != "(기능명)":
            features.append({
                "id": fid,
                "name": name,
                "description": desc
            })

    return features


def cmd_run():
    """d0008_user.md 신규 생성 (run 서브명령어)"""
    print("# oaisuser run\n")

    if USER_FILE.exists():
        print(f"[WARN] {USER_FILE}가 이미 존재합니다.")
        if "--force" not in sys.argv:
            print("[INFO] 덮어쓰려면 --force 옵션을 사용하세요.")
            return 1

    today = datetime.now().strftime("%Y-%m-%d")
    project_name = PROJECT_ROOT.name

    template = f"""# d0008_user.md - 사용자 가이드

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | {today} | 최초 생성 (oaisuser) |

---

## 1. 개요

### 1.1 시스템 소개
{project_name}은 [목적/기능 요약]을 위한 시스템입니다.

### 1.2 대상 사용자
- **관리자**: 시스템 설정, 사용자 관리
- **일반 사용자**: 주요 기능 이용
- **게스트**: 제한된 기능 이용

### 1.3 시스템 요구사항
- **브라우저**: Chrome, Edge, Firefox (최신 버전)
- **화면 해상도**: 1280x720 이상 권장
- **네트워크**: 인터넷 연결 필수

---

## 2. 시작하기

### 2.1 접속 방법
1. 브라우저에서 [URL] 접속
2. 로그인 화면에서 계정 정보 입력
3. 메인 화면으로 이동

### 2.2 계정 생성
[계정 생성 절차 설명]

### 2.3 로그인/로그아웃
[로그인/로그아웃 절차 설명]

---

## 3. 주요 기능

### 3.1 [기능1명]

#### 3.1.1 기능 설명
[기능 설명]

#### 3.1.2 사용 방법
1. [단계 1]
2. [단계 2]
3. [단계 3]

#### 3.1.3 주의사항
- [주의사항 1]
- [주의사항 2]

---

## 4. 화면별 안내

### 4.1 메인 화면
[메인 화면 구성 요소 및 사용법]

---

## 5. FAQ

### 5.1 계정/로그인

#### Q: 비밀번호를 잊어버렸습니다.
A: [해결 방법]

#### Q: 로그인이 되지 않습니다.
A: [해결 방법]

### 5.2 기능 사용

#### Q: [자주 묻는 질문 1]
A: [답변]

---

## 6. 트러블슈팅

### 6.1 일반 문제

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| 페이지가 로드되지 않음 | 네트워크 문제 | 인터넷 연결 확인 |
| 버튼이 동작하지 않음 | 브라우저 캐시 | 캐시 삭제 후 재시도 |

### 6.2 오류 메시지

| 오류 메시지 | 의미 | 조치 방법 |
|-------------|------|----------|
| "세션 만료" | 로그인 시간 초과 | 재로그인 |

---

## 7. 용어 설명

| 용어 | 설명 |
|------|------|
| [용어1] | [설명] |
| [용어2] | [설명] |

---

## 8. 문의 및 지원

### 8.1 기술 지원
- **담당자**: [이름/부서]
- **연락처**: [이메일/전화]

### 8.2 피드백
- [피드백 제출 방법]

---
"""

    DOC_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILE.write_text(template, encoding="utf-8")

    print(f"[OK] 사용자 가이드 생성됨: {USER_FILE}")
    return 0


def cmd_status():
    """d0008_user.md 현황 조회 (status 서브명령어)"""
    print("# oaisuser status\n")

    if not USER_FILE.exists():
        print(f"[ERROR] {USER_FILE}가 없습니다.")
        print("[TIP] oaisuser run 으로 생성하세요.")
        return 1

    content = USER_FILE.read_text(encoding="utf-8")
    sections = parse_user_sections(content)
    features = parse_features(content)
    faqs = parse_faq(content)

    print(f"파일: {USER_FILE}")
    print(f"크기: {len(content)} bytes")
    print()

    print("## 섹션 구조\n")
    for s in sections:
        print(f"  - {s['full']}")

    print()
    print(f"## 통계\n")
    print(f"  섹션: {len(sections)}개")
    print(f"  기능 항목: {len(features)}개")
    print(f"  FAQ: {len(faqs)}개")

    if features:
        print()
        print("## 기능 목록\n")
        for f in features:
            print(f"  [{f['number']}] {f['name']}")

    if faqs:
        print()
        print("## FAQ 목록\n")
        for q in faqs[:5]:
            print(f"  - {q[:40]}...")
        if len(faqs) > 5:
            print(f"  ... 외 {len(faqs) - 5}개")

    return 0


def cmd_add(args):
    """특정 기능 사용법 추가 (add 서브명령어)"""
    print("# oaisuser add\n")

    if not args:
        print("[ERROR] 기능명을 지정하세요.")
        print("사용법: oaisuser add [기능명]")
        return 1

    feature_name = args[0]

    if not USER_FILE.exists():
        print(f"[ERROR] {USER_FILE}가 없습니다.")
        print("[TIP] oaisuser run 으로 먼저 생성하세요.")
        return 1

    content = USER_FILE.read_text(encoding="utf-8")
    features = parse_features(content)

    # 기존 기능 번호 파악
    max_num = 0
    for f in features:
        parts = f['number'].split('.')
        if len(parts) >= 2 and parts[0] == '3':
            try:
                num = int(parts[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass

    new_num = f"3.{max_num + 1}"

    new_section = f"""
### {new_num} {feature_name}

#### {new_num}.1 기능 설명
[{feature_name} 기능의 목적과 주요 역할을 1-2문장으로 설명]

#### {new_num}.2 접근 방법
- **메뉴 경로**: [메뉴] -> [서브메뉴] -> [{feature_name}]
- **단축키**: (있는 경우)

#### {new_num}.3 사용 방법
1. [단계 1]
2. [단계 2]
3. [단계 3]

#### {new_num}.4 주의사항
- [주의사항 1]
- [주의사항 2]

"""

    # "## 4. 화면별 안내" 앞에 삽입
    insert_pattern = r"(---\n\n## 4\. 화면별 안내)"
    match = re.search(insert_pattern, content)

    if match:
        insert_pos = match.start()
        content = content[:insert_pos] + new_section + content[insert_pos:]
        USER_FILE.write_text(content, encoding="utf-8")
        print(f"[OK] 기능 추가됨: {new_num} {feature_name}")
    else:
        print("[WARN] 삽입 위치를 찾을 수 없습니다.")
        print("[INFO] 수동으로 추가하세요.")
        print()
        print(new_section)

    return 0


def cmd_faq(args):
    """FAQ 항목 추가 (faq 서브명령어)"""
    print("# oaisuser faq\n")

    if not args:
        print("[ERROR] 질문을 지정하세요.")
        print("사용법: oaisuser faq [질문]")
        return 1

    question = args[0]

    if not USER_FILE.exists():
        print(f"[ERROR] {USER_FILE}가 없습니다.")
        print("[TIP] oaisuser run 으로 먼저 생성하세요.")
        return 1

    new_faq = f"""
#### Q: {question}
A: [답변]

"""

    content = USER_FILE.read_text(encoding="utf-8")

    # "## 6. 트러블슈팅" 앞에 삽입
    insert_pattern = r"(---\n\n## 6\. 트러블슈팅)"
    match = re.search(insert_pattern, content)

    if match:
        insert_pos = match.start()
        content = content[:insert_pos] + new_faq + content[insert_pos:]
        USER_FILE.write_text(content, encoding="utf-8")
        print(f"[OK] FAQ 추가됨: {question}")
    else:
        print("[WARN] 삽입 위치를 찾을 수 없습니다.")
        print("[INFO] 수동으로 추가하세요.")
        print()
        print(new_faq)

    return 0


def cmd_update():
    """전체 문서 현행화 (update 서브명령어)"""
    print("# oaisuser update\n")

    if not USER_FILE.exists():
        print(f"[ERROR] {USER_FILE}가 없습니다.")
        return 1

    content = USER_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # 문서 이력 업데이트
    version_pattern = r"\| v(\d+) \|"
    versions = re.findall(version_pattern, content)

    if versions:
        max_version = max(int(v) for v in versions)
        new_version = f"v{max_version + 1:02d}"
    else:
        new_version = "v02"

    # 새 버전 행 추가
    history_pattern = r"(\| 버전 \| 날짜 \| 변경 내용 \|\n\|[^\n]+\|)"
    match = re.search(history_pattern, content)

    if match:
        insert_pos = match.end()
        new_row = f"\n| {new_version} | {today} | 문서 현행화 (oaisuser) |"
        content = content[:insert_pos] + new_row + content[insert_pos:]
        USER_FILE.write_text(content, encoding="utf-8")
        print(f"[OK] 문서 이력 업데이트: {new_version}")

    print()
    print("## 현행화 권장 사항\n")
    print("  1. 각 기능별 사용 방법 검토 및 업데이트")
    print("  2. 스크린샷 최신화")
    print("  3. FAQ 항목 추가/수정")
    print("  4. 트러블슈팅 내용 보완")
    print()
    print("[INFO] 수동 검토 후 내용을 업데이트하세요.")

    return 0


def cmd_sync():
    """PRD 기반 기능 목록 동기화 (sync 서브명령어)"""
    print("# oaisuser sync\n")

    if not PRD_FILE.exists():
        print(f"[ERROR] {PRD_FILE}가 없습니다.")
        return 1

    prd_features = extract_prd_features()

    if not prd_features:
        print("[INFO] PRD에서 기능 요구사항을 찾을 수 없습니다.")
        return 0

    print(f"PRD 기능: {len(prd_features)}개 발견\n")

    for f in prd_features:
        print(f"  [{f['id']}] {f['name']}")
        if f['description'] and f['description'] != "(설명)":
            print(f"      {f['description'][:50]}")

    # d0008_user.md 비교
    if USER_FILE.exists():
        content = USER_FILE.read_text(encoding="utf-8")
        user_features = parse_features(content)
        user_feature_names = [f['name'].lower() for f in user_features]

        print()
        print("## 동기화 분석\n")

        missing = []
        for pf in prd_features:
            if pf['name'].lower() not in user_feature_names:
                missing.append(pf)

        if missing:
            print(f"[WARN] 누락된 기능: {len(missing)}개")
            for m in missing:
                print(f"  - {m['name']}")
            print()
            print("[TIP] oaisuser add \"기능명\" 으로 추가하세요.")
        else:
            print("[OK] 모든 PRD 기능이 문서화되어 있습니다.")
    else:
        print()
        print(f"[INFO] {USER_FILE}가 없습니다.")
        print("[TIP] oaisuser run 으로 먼저 생성하세요.")

    return 0


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisuser", sys.argv[1:]):
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
        return cmd_run()
    elif cmd == "status":
        return cmd_status()
    elif cmd == "add":
        return cmd_add(cmd_args)
    elif cmd == "faq":
        return cmd_faq(cmd_args)
    elif cmd == "update":
        return cmd_update()
    elif cmd == "sync":
        return cmd_sync()
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
