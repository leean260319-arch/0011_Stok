# oaistest_guide - 테스트 통합 가이드

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v09 | 2026-01-25 | 파일명 변경: test_guide.md → oaistest_guide.md (네이밍 규칙 통일) |
| v08 | 2026-01-05 | Part D 정합성: 43개 모듈, 11개 카테고리 (Config 추가) |
| v07 | 2026-01-05 | Part E 런타임 검증 섹션 추가 (섹션 7) |
| v06 | 2026-01-03 | Part D 중복 방지: SP≠00일 때 d0003 참조 방식 |
| v05 | 2026-01-03 | oaiscontext 연동 명시 (d{SP}0003 생성) |

---

## 1. 개요

### 1.1 문서 목적

테스트 **방법론(How)**을 정의하는 통합 가이드입니다.

### 1.2 역할 분리

| 문서 유형 | 역할 | 예시 |
|----------|------|------|
| `d*003_test.md` | **무엇을(What)** 테스트할 것인가 | TC 목록, 체크리스트, 시나리오 항목 |
| `v/guide/oaistest_guide.md` | **어떻게(How)** 테스트할 것인가 | 방법론, 워크플로우, 도구 사용법 |
| `v/oaistest.md` | 테스트 실행 스킬 | 명령어, 자동화 |
| `v/oaisdev.md` | 테스트 문서 생성 | 개발 첫 실행 시 d0003 자동 생성 |

### 1.2.1 문서 생성 워크플로우

> **컨텍스트 적용**: `oaiscontext.md` 규칙에 따라 SP별 문서 생성
> - SP=00: `d0003_test.md` ← `d0001_prd.md`
> - SP=02: `d20003_test.md` ← `d20001_prd.md`

```
oaisprd run (신규 프로젝트)
    ↓
d{SP}0001_prd.md 생성
    ↓
oaisdev run (첫 실행)
    ↓
d{SP}0003_test.md 존재? → 없음: 자동 생성
    ├── Part A: 공통 에러체크 (고정 항목)
    ├── Part B: PRD 기능에서 시나리오 도출
    ├── Part C: 빈 테이블 (TDD RED에서 등록)
    └── Part D: oais 모듈 스캔하여 자동 생성
    ↓
TDD 사이클 시작 (RED → GREEN → REFACTOR)
```

**스킬별 d0003 조작:**

| 스킬 | 역할 | Part |
|------|------|------|
| oaisdev | **생성** | 전체 (첫 실행 시) |
| oaisdev | **등록** | Part C (TDD RED) |
| oaistest | **갱신** | 실행 결과 테이블 |
| oaistest refresh | **재스캔** | Part D 모듈 목록 |

### 1.3 테스트 구조 (5 Part)

| Part | 이름 | 목적 | 주요 도구 |
|------|------|------|----------|
| A | 에러체크 | 정적 분석, 코드 품질 | pylint, mypy, Serena MCP |
| B | 시나리오 테스트 | E2E/UI 검증 | Playwright MCP |
| C | 단위 테스트 | TDD 기반 함수/클래스 검증 | pytest |
| D | oais 모듈 테스트 | oais 모듈 전체 검증 | pytest |
| **E** | **런타임 검증** | **import 시 런타임 에러 감지** | **pytest (필수)** |

---

## 2. 공통 정의

### 2.1 우선순위

| 우선순위 | 설명 | 테스트 시점 |
|----------|------|-------------|
| P0-Critical | 핵심 기능, 시스템 장애 유발 가능 | 즉시/매 빌드 |
| P1-High | 주요 기능, 사용자 영향 큼 | 24시간 내/매일 |
| P2-Medium | 일반 기능, 사용자 영향 보통 | 1주일 내/주간 |
| P3-Low | 부가 기능, 사용자 영향 적음 | 백로그/릴리스 전 |

### 2.2 상태 표기

| 상태 | 설명 | 표기 |
|------|------|------|
| 대기 | 테스트 미실행 | `[ ]` |
| 진행중 | 테스트 실행 중 | `[~]` |
| 통과 | 테스트 성공 | `[x]` |
| 실패 | 테스트 실패 | `[!]` |
| 스킵 | 테스트 건너뜀 | `[-]` |

### 2.3 에러 분류 체계

| 분류 | 설명 | 우선순위 | 이력 태그 |
|------|------|----------|----------|
| [CRITICAL] | 시스템 장애, 보안 취약점 | P0 - 즉시 | [HOTFIX] |
| [ERROR] | 기능 오작동, 예외 미처리 | P1 - 24시간 | [BUGFIX] |
| [WARNING] | 잠재적 문제, 성능 이슈 | P2 - 1주일 | [IMPROVE] |
| [INFO] | 코드 스타일, 개선 권장 | P3 - 백로그 | [ENHANCE] |

### 2.4 커버리지 목표

| 유형 | 목표 |
|------|------|
| Unit Test | 80% |
| Integration | 70% |
| E2E Critical Path | 100% |

---

## 3. Part A: 에러체크

정적 분석 기반 코드 품질/보안/성능 검증

> **검사 기준**: `v/guide/common_guide.md` (코드 품질, 보안, 성능 표준)
> **결과 기록**: `d*003_test.md` Part A 테이블에 실행 결과만 기록

### 3.1 워크플로우

```
검사 실행 (oaischeck / pylint / flake8 / mypy)
    ↓
결과 기록 (d0003_test.md Part A 테이블)
    ↓
이슈 발견 시 → d0004_todo.md 등록
    ↓
수정 및 재검사
```

### 3.2 결과 기록 형식

```markdown
| 실행일 | 도구 | 대상 | 결과 | 비고 |
|--------|------|------|------|------|
| 2026-01-03 | py_compile | src/ (43개) | PASS | 전체 통과 |
| 2026-01-03 | pylint | src/ | 0 errors | W0621 다수 |
```

### 3.3 도구 및 명령어

**Bash 도구:**
```bash
python -m py_compile <file.py>  # 문법 체크
pylint <file.py>                # 린터
flake8 <file.py>                # 린터
mypy <file.py>                  # 타입 체크
```

**Serena MCP 심볼릭 분석:**
- `mcp__serena__find_symbol` - 심볼 검색
- `mcp__serena__get_symbols_overview` - 파일 심볼 개요
- `mcp__serena__find_referencing_symbols` - 참조 심볼 검색
- `mcp__serena__search_for_pattern` - 패턴 검색

### 3.4 서브에이전트 호출

**정적 분석 (python-code-reviewer)**
```
Task(
  subagent_type="python-code-reviewer",
  prompt="oais/ 모듈 정적 분석: 타입 힌트, 미사용 import, 예외 처리, PEP8"
)
```

**품질 분석 (oaisqa)**
```
Task(
  subagent_type="oaisqa",
  prompt="oais/ 모듈 분석: 중복 정의, 순환 참조, 복잡도, 리팩토링 영역"
)
```

### 3.5 용어체크

표준용어집(`doc/기획/TErm/`) 기준 DB/코드 명명 일관성 검증

**불일치 유형:**
| 유형 | 설명 | 예시 |
|------|------|------|
| 용어 미등록 | 용어집에 없음 | `agent` (용어집: 대리인) |
| 표기 불일치 | 다르게 표기 | `company` vs `corp` |
| 영문/한글 혼용 | 일관성 없음 | `user_업체` |
| 약어 미정의 | 정의 없는 약어 | `biz_no` |

**권장 용어:**
| 한글 | 권장 영문 | 비권장 |
|------|----------|--------|
| 업체 | company | corp, firm |
| 사용자 | user | member |
| 사업자번호 | business_number | biz_no |

---

## 4. Part B: 시나리오 테스트

사용자 관점 E2E/UI/통합 테스트

> **시나리오 항목**: PRD(`d*001_prd.md`) 기능 목록에서 도출
> **결과 기록**: `d*003_test.md` Part B 테이블에 실행 결과만 기록

### 4.1 테스트 유형

| 유형 | 목적 | 도구 | 자동화 |
|------|------|------|--------|
| E2E | 전체 흐름 검증 | Playwright | 권장 |
| UI | 화면/인터페이스 | Playwright | 부분 |
| 통합 | 모듈 간 상호작용 | pytest | 권장 |
| 회귀 | 기존 기능 확인 | 기존 스위트 | 필수 |

### 4.2 워크플로우

```
PRD 기능 목록에서 시나리오 도출
    ↓
테스트 실행 (Playwright MCP / 수동)
    ↓
결과 기록 (d0003_test.md Part B 테이블)
    ↓
실패 시 → d0004_todo.md 등록
```

### 4.3 항목 + 결과 구조

**테스트 항목** (PRD 기반, 변경 적음):
```markdown
| ID | 시나리오 | 우선순위 |
|----|----------|:--------:|
| B1-1 | 정상 로그인 | P0 |
| B1-2 | 로그인 실패 | P1 |
```

**실행 결과** (테스트 시마다 추가):
```markdown
| 실행일 | ID | 결과 | 비고 |
|--------|-----|:----:|------|
| 2026-01-03 | B1-1 | PASS | - |
| 2026-01-03 | B1-2 | FAIL | d20004 등록 |
```

### 4.4 Playwright MCP

| 도구 | 용도 |
|------|------|
| `browser_navigate` | URL 이동 |
| `browser_snapshot` | 페이지 스냅샷 |
| `browser_take_screenshot` | 스크린샷 캡처 |
| `browser_click` | 요소 클릭 |
| `browser_type` | 텍스트 입력 |
| `browser_fill_form` | 폼 전체 입력 |
| `browser_wait_for` | 대기 |

**기본 흐름:** `navigate → snapshot → click/type → screenshot → 검증`

**스크린샷 저장:**
- 경로: `tmp/test_screenshots/`
- 네이밍: `[시나리오ID]_[단계]_[YYYYMMDD_HHMMSS].png`

### 4.5 서브에이전트 호출

**E2E 웹 테스트 (web-test-orchestrator)**
```
Task(
  subagent_type="web-test-orchestrator",
  prompt="02_1st_server E2E 테스트: 로그인, 핵심 기능, 에러 상황"
)
```

### 4.6 테스트 환경 설정

```env
AUTOLOGIN=true  # E2E 테스트용
```

| 환경 | AUTOLOGIN | 용도 |
|------|-----------|------|
| 테스트 | true | E2E/UI 자동화 |
| 개발 | true/false | 편의에 따라 |
| 운영 | false | 실제 로그인 |

---

## 5. Part C: 단위 테스트 (TDD)

TDD(Test-Driven Development) 기반 단위 테스트

### 5.1 TDD 워크플로우

```
oaisdev run [태스크]
    ↓
RED: 테스트 작성 → d0003 Part C 등록
    ↓
GREEN: 구현 → 테스트 통과
    ↓
d0003 Part C 상태 업데이트 ([x])
    ↓
REFACTOR: 코드 정리
```

### 5.2 TC 네이밍 규칙

| 레벨 | 형식 | 예시 |
|------|------|------|
| Epic | `E{순번}` | E002 |
| Feature | `F{Epic}-{순번}` | F002-1 |
| Task | `F{Epic}-{Feature}.{순번}` | F002-1.1 |
| TC | `TC{Epic}-{Feature}.{Task}` | TC002-1.1 |

**Task ↔ TC 1:1 매핑:**
```
Task:  F002-1.1 (보건복지부 탭)
TC:   TC002-1.1_보건복지부탭.py
```

### 5.3 테스트 파일 구조

```
tests/
├── conftest.py                      # 공통 fixture
├── TC001-1.1_로그인성공.py          # F001-1.1
├── TC001-1.2_로그인실패.py          # F001-1.2
├── TC002-1.1_보건복지부탭.py        # F002-1.1
└── TC002-1.2_고용노동부탭.py        # F002-1.2
```

### 5.4 테스트 파일 템플릿

```python
"""
TC002-1.1_보건복지부탭.py - 보건복지부 탭 테스트

TC ID: TC002-1.1
Task ID: F002-1.1
Feature: F002-1 중앙정부 정책
"""
import pytest


class TestTC002_1_1_보건복지부탭:
    """TC002-1.1: 보건복지부 탭 테스트"""

    def test_tab_renders_correctly(self):
        """보건복지부 탭 정상 렌더링"""
        # Arrange
        # Act
        # Assert
        assert True
```

### 5.5 d0003 Part C 등록 형식

```markdown
## C2. 등록된 단위 테스트

### E001: 인증/권한 시스템

| TC ID | Task ID | 테스트명 | 파일 | 상태 |
|-------|---------|----------|------|------|
| TC001-1.1 | F001-1.1 | 로그인 성공 | tests/TC001-1.1_로그인성공.py | [x] |
| TC001-1.2 | F001-1.2 | 로그인 실패 | tests/TC001-1.2_로그인실패.py | [ ] |
```

### 5.6 서브에이전트 호출

**TDD 개발 (task-executor)**
```
Task(
  subagent_type="task-executor",
  prompt="TDD 구현: F002-1.1 보건복지부 탭
  1. RED: TC002-1.1 테스트 작성
  2. d0003 Part C 등록
  3. GREEN: 최소 구현
  4. REFACTOR: 정리"
)
```

---

## 6. Part D: oais 모듈 테스트

oais/*.py 전체 모듈 기능 검증 (43개 모듈, 11개 카테고리)

### 6.0 SP별 Part D 처리 (중복 방지)

> oais 모듈은 공통이므로 **d0003에서만 관리**, 서브프로젝트는 참조

| SP | Part D 처리 |
|:--:|------------|
| 00 | oais 모듈 스캔하여 직접 생성 (`d0003_test.md`) |
| ≠00 | `"d0003_test.md Part D 참조"` 링크만 추가 |

**d20003_test.md Part D 예시:**
```markdown
## Part D: oais 모듈 테스트

> **참조**: `d0003_test.md` Part D 참조
> oais 모듈은 공통이므로 d0003에서 통합 관리합니다.
```

### 6.1 테스트 대상

| 카테고리 | 모듈 수 | 함수 수 | 검증 내용 |
|----------|:-------:|:-------:|----------|
| Core | 5 | - | DB 연결, 인증, 세션, 관리자 |
| Config | 2 | - | 기본 설정, 설정 헬퍼 |
| Entity | 5 | - | 사용자, 업체, 대리인, 고객, 커뮤니티 |
| Task | 5 | - | 업무 핵심, 조회, 첨부, 관리 |
| Data | 4 | - | 컬럼, 시스템 코드, DB 메타, 데이터 처리 |
| Application | 3 | - | 신청, 사업자등록, 사업자 데이터 |
| File | 5 | - | 파일 연산, 업로드, 관리, OCR, 도장 |
| External | 3 | - | 하이픈 API, 뉴스 API, 서비스 |
| Document | 4 | - | PDF, 영수증, 카드, 도서 요약 |
| Utility | 5 | - | 유틸리티, 날짜, 엑셀, 검증, 재무 |
| UI | 2 | - | UI 렌더링, 모바일 CSS |

### 6.2 테스트 패턴

**DB 함수 테스트:**
```python
import pytest
from oais.db import get_db_connection

@pytest.fixture
def test_db():
    """테스트용 DB 연결"""
    conn = get_db_connection(":memory:")
    yield conn
    conn.close()

def test_get_user_companies(test_db):
    """사용자 업체 조회 테스트"""
    from oais.user import get_user_companies
    result = get_user_companies("test_user")
    assert isinstance(result, pd.DataFrame)
```

**유틸리티 함수 테스트:**
```python
def test_validate_business_number():
    """사업자번호 검증 테스트"""
    from oais.validation import validate_business_number
    assert validate_business_number("123-45-67890") == True
    assert validate_business_number("invalid") == False
```

**UI 함수 테스트:**
```python
def test_render_sidebar():
    """사이드바 렌더링 테스트"""
    from oais.ui import render_sidebar
    result = render_sidebar()
    assert result is not None
```

---

## 7. Part E: 런타임 검증 (필수)

페이지 import 시 발생하는 런타임 에러 사전 감지

> **필수 테스트**: py_compile/pylint로 감지 불가능한 런타임 에러 검증
> **결과 기록**: `d*003_test.md` Part E 테이블에 실행 결과 기록

### 7.1 테스트 목적

정적 분석(Part A)으로 감지할 수 없는 런타임 에러를 사전에 발견합니다.

| 에러 유형 | 원인 | py_compile | pylint | Part E |
|----------|------|:----------:|:------:|:------:|
| StreamlitDuplicateElementKey | 위젯 key 중복 | ❌ | ❌ | ✅ |
| ImportError (조건부) | if문 내 import | ❌ | ❌ | ✅ |
| AttributeError | 런타임 객체 접근 | ❌ | ❌ | ✅ |
| TypeError | 런타임 타입 불일치 | ❌ | ❌ | ✅ |
| NameError (동적) | 동적 변수 참조 | ❌ | ❌ | ✅ |

### 7.2 워크플로우

```
Part A~D 완료
    ↓
Part E: test_page_import.py 실행
    ↓
pages/*.py 동적 import (모킹 환경)
    ↓
런타임 에러 감지 (DuplicateKey, ImportError 등)
    ↓
실패 시 → d{SP}0004 등록
```

### 7.3 테스트 파일 구조

```
tests/
├── test_page_import.py    ← [필수] Part E 런타임 검증
└── conftest.py            ← 공통 fixture
```

**테스트 대상**: `{서브프로젝트}/pages/*.py` 전체

### 7.4 도구 및 명령어

```bash
# Part E만 실행
oaistest run --runtime

# pytest 직접 실행
uv run pytest tests/test_page_import.py -v

# 특정 페이지만 테스트
uv run pytest tests/test_page_import.py -k "7_74" -v
```

### 7.5 테스트 핵심 기능

**test_page_import.py 주요 모킹:**

| 모킹 대상 | 목적 | 구현 |
|----------|------|------|
| Streamlit 위젯 | UI 함수 호출 허용 | MockSessionState, MockContextManager |
| 위젯 key 추적 | 중복 key 감지 | used_keys set + DuplicateElementKey 예외 |
| DB 연결 | 순수 코드 검증 | sqlite3.connect 모킹 |
| 세션 상태 | st.session_state 접근 | dict 기반 모킹 |

### 7.6 테스트 패턴

**기본 import 테스트:**
```python
import importlib.util
import sys

def test_page_import(page_file):
    """페이지 파일 import 테스트"""
    spec = importlib.util.spec_from_file_location("page_module", page_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules["page_module"] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"Import failed: {page_file} - {e}")
```

**DuplicateElementKey 감지:**
```python
class MockStreamlit:
    used_keys = set()

    def _check_key(self, key):
        if key in self.used_keys:
            raise DuplicateElementKey(f"Duplicate key: {key}")
        self.used_keys.add(key)
```

### 7.7 결과 기록 형식

```markdown
## Part E: 런타임 검증 결과

| 실행일 | 대상 | 전체 | 통과 | 실패 | 비고 |
|--------|------|:----:|:----:|:----:|------|
| 2026-01-05 | pages/*.py (49개) | 49 | 49 | 0 | 전체 통과 |
```

### 7.8 실패 시 처리

```markdown
# d{SP}0004_todo.md 등록 예시

| ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
|----|--------|------|------|---------|------|
| T030 | 2026-01-05 | [RUNTIME] | 7_74_앱_시니어복지.py DuplicateElementKey | 높음 | 대기 |
```

> **템플릿**: `v/template/test_page_import_template.py`

---

## 8. 에이전트/도구 매핑

### 8.1 단계별 권장 에이전트

| 단계 | 작업 유형 | 권장 에이전트 | 도구 |
|------|----------|--------------|------|
| Part A 정적 분석 | 코드 분석 | `python-code-reviewer` | Serena MCP |
| Part A 품질 분석 | 중복/의존성 | `oaisqa` | Serena MCP |
| Part B 시나리오 | E2E 웹 테스트 | `web-test-orchestrator` | Playwright MCP |
| Part B 설계 | 테스트 시나리오 | `qa` | Sequential MCP |
| Part C 단위 | TDD 개발 | `task-executor` | pytest |
| Part D oais 모듈 | 모듈 전체 검증 | `task-executor` | pytest |
| **Part E 런타임** | **import 검증** | `task-executor` | **pytest** |
| 결과 검증 | 문서화 | `task-executor` | - |
| 코드 탐색 | 구조 파악 | `Explore` | - |

### 8.2 병렬/순차 실행 가이드

**병렬 실행 (의존성 없음):**
- `python-code-reviewer` + `oaisqa` (Part A)
- 여러 모듈 독립 테스트

**순차 실행 (의존성 있음):**
1. Part A 에러체크 → 수정
2. Part A 완료 → Part B 시나리오
3. 결과 → 문서 업데이트

---

## 9. 결과 기록

### 9.1 테스트 사이클 기록

```markdown
### 테스트 사이클: 2026-01-03
**실행자**: [이름] | **대상**: Part A + WEB-1ST-010~030 | **결과**: 25/30 (83%)

**실패**: 에러체크-보안-03, WEB-1ST-010-02 → d0004_todo.md 등록
**스킵**: 호환성-03 (별도 스프린트)
```

### 9.2 테스트 결과 리포트

```
=== 테스트 결과 ===
서버: [URL] | 일시: YYYY-MM-DD HH:MM:SS
총: XX개 | 통과: XX (XX%) | 실패: XX (XX%) | 스킵: XX (XX%)

| 카테고리 | 전체 | 통과 | 실패 |
|----------|------|------|------|
| 에러체크 | 15 | 14 | 1 |
| 로그인 | 5 | 4 | 1 |

실패: [P0] 에러체크-보안-03, [P1] UI-LOGIN-002
→ X개 이슈 d0004_todo.md 등록
```

### 9.3 에러 결과 기록 (d0004_todo.md)

```markdown
| ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
|----|--------|------|------|---------|------|
| T020 | 2026-01-03 | [TEST] | test_login.py::test_invalid FAILED | 중간 | 대기 |
| T021 | 2026-01-03 | [ERR] | conftest.py:23 - fixture 'db' not found | 높음 | 대기 |
```

---

## 10. 명령어 참조

### 10.1 oaistest 명령어

| 명령어 | 설명 |
|--------|------|
| `oaistest run` | 전체 테스트 실행 |
| `oaistest run --unit` | Part C 단위 테스트만 |
| `oaistest run --e2e` | Part B 시나리오만 |
| `oaistest run --module` | Part D oais 모듈만 |
| `oaistest run [시나리오ID]` | 특정 시나리오 |
| `oaistest run [P0]` | 우선순위별 |
| `oaistest preview` | 테스트 계획만 출력 |

### 10.2 옵션

| 옵션 | 설명 |
|------|------|
| `--screenshot` | 각 단계 스크린샷 |
| `--fail-fast` | 첫 실패 시 중단 |
| `--verbose` | 상세 로그 |

---

## 11. 관련 문서

| 문서 | 용도 |
|------|------|
| d0003_test.md | 공통 테스트 항목 (What) |
| d20003_test.md | 02_1st_server 테스트 항목 (What) |
| v/oaistest.md | 테스트 실행 스킬 |
| v/oaisdev.md | TDD 개발 스킬 |
| v/oaischeck.md | 코드 체크 스킬 |
| d0004_todo.md | 이슈 등록/추적 |
| d0010_history.md | 변경 이력 |
