# debugging_guide - 프로젝트 디버깅 가이드

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v03 | 2026-01-02 | 태그 체계 통일 (BUGFIX, HOTFIX 등 d0010 체계로 변경) |
| v02 | 2026-01-02 | oaislib, oaisdb 스킬 추가, 도메인별 디버깅/DB 에러 유형 추가 |
| v01 | 2026-01-02 | 최초 생성 - d0004_todo.md, oaischeck.md, oaisfix.md에서 디버깅 관련 내용 통합 |

---

## 1. 개요

프로젝트 디버깅 워크플로우, 에러 분류, False Positive 처리 방법 정의.

**범용 디버깅 스킬**:
| 스킬 | 대상 | 역할 |
|------|------|------|
| oaischeck | 전체 코드 | 에러 감지 → d0004 기록 |
| oaisfix | 전체 코드 | d0004 이슈 자동 수정 |

**도메인별 디버깅 스킬**:
| 스킬 | 대상 | 역할 |
|------|------|------|
| oaislib | oais/ 모듈 | 분석 → d0004 기록 → 수정 (2-Phase) |
| oaisdb | db/*.db | 분석 → d0004 기록 → 수정 (2-Phase) |

**관련 문서**:
- doc/d0004_todo.md - 이슈 추적 (현재/해결 이슈 테이블)
- doc/d0010_history.md - 아카이브 이력

---

## 2. 디버깅 워크플로우

### 2.1 기본 흐름

[에러 발생] → [현재 이슈] → 해결 → [해결된 이슈 (1~2주 모니터링)] → [d0010 아카이브]

| 단계 | 설명 | 담당 |
|------|------|------|
| 에러 발생 | d0004_todo.md "현재 이슈" 테이블에 기록 | 개발자/oaischeck |
| 해결 완료 | "해결된 이슈"로 이동 (해결일, 해결방법 기록) | 개발자/oaisfix |
| 안정 확인 | 1~2주 재발 여부 모니터링 | 개발자 |
| 아카이브 | oaishistory run → d0010_history.md 이동 | oaishistory |

### 2.2 도메인별 2-Phase 워크플로우

oaislib, oaisdb 등 도메인별 스킬은 2단계 워크플로우 사용:

Phase 1: 분석 → 문제점 발견 → d0004 "현재 이슈" 기록
Phase 2: d0004 이슈 수정 → "해결된 이슈" 이동

| 단계 | 담당 | 작업 |
|------|------|------|
| Phase 1 | 메인 에이전트 | 분석, 이슈 발견, d0004 등록 |
| Phase 2 | 서브에이전트 (병렬) | 이슈 수정, 검증 |
| 완료 | 메인 에이전트 | 결과 취합, 문서 업데이트 |

**완료 조건**: d0004_todo.md에 해당 도메인 미해결 이슈 0개

### 2.3 이슈 기록 형식

> 표준 형식: v/guide/oaistodo_guide.md 참조

**현재 이슈 테이블:**

| ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
|----|--------|------|------|---------|------|
| T001 | 2026-01-02 | BUGFIX | oais\seal.py:148 - 에러 내용 | 높음 | 대기 |

**해결된 이슈 테이블:**

| ID | 발생일 | 분류 | 내용 | 해결일 | 해결방법 |
|----|--------|------|------|--------|---------|
| T001 | 2026-01-02 | BUGFIX | 에러 내용 | 2026-01-03 | 해결 내용 |

---

## 3. 에러 분류 체계

### 3.1 우선순위별 분류

| 분류 | 설명 | 대응 시간 |
|------|------|----------|
| CRITICAL | 시스템 장애, 보안 취약점 | 즉시 |
| ERROR | 기능 오작동 | 24시간 |
| WARNING | 잠재 문제 | 1주일 |
| INFO | 코드 스타일 | 백로그 |

### 3.2 분류 태그 (통일 체계)

> d0004 ↔ d0010 동일 태그 사용

| 태그 | 의미 |
|------|------|
| BUGFIX | 버그/에러 수정 |
| HOTFIX | 보안/긴급 수정 |
| UPDATE | 의존성 업데이트 |
| FEATURE | 기능 관련 |
| IMPROVE | 최적화/개선 |
| DOCS | 문서 수정 |
| REFACTOR | 코드 리팩토링 |
| CONFIG | 설정 변경 |
| MISC | 미분류/기타 |

### 3.3 Pylint 에러 코드

| 코드 | 유형 | 수정 방법 |
|------|------|----------|
| E0611 | export 누락 | __init__.py에 import 추가 |
| E0102 | 중복 정의 | 첫 번째만 유지 |
| E0606 | 변수 미할당 | 변수 초기화 추가 |
| E0601 | 정의 전 사용 | 정의 순서 수정 |
| E1101 | 멤버 누락 | 올바른 멤버명 사용 |
| E0704 | raise 오류 | except 블록 내로 이동 |
| W0611 | 미사용 import | import 문 삭제 |
| W0612 | 미사용 변수 | 변수 삭제 또는 _ prefix |

### 3.4 DB 에러 유형 (oaisdb)

| 유형 | 설명 | 수정 방법 |
|------|------|----------|
| INTEGRITY | 무결성 오류 | 데이터 정리, 제약조건 수정 |
| FK | 외래키 누락/위반 | FK 제약조건 추가 |
| INDEX | 인덱스 누락/비효율 | 인덱스 추가/수정 |
| QUERY | 느린 쿼리 | 쿼리 최적화, N+1 제거 |
| DATA | 중복/고아 데이터 | 데이터 정리 |

**검증 명령 (SQLite):**
PRAGMA integrity_check;   -- 무결성 검사
PRAGMA foreign_key_check; -- FK 검증

### 3.5 이슈 ID 규칙

| Prefix | 스킬 | 예시 |
|--------|------|------|
| T | 일반 | T001 |
| L | oaislib | L001 |
| D | oaisdb | D001 |

---

## 4. False Positive 처리

### 4.1 제외 대상 모듈

다음 모듈은 **동적 로딩**으로 pylint 오류 발생하나 실제 오류 아님:

| 모듈 | 사유 |
|------|------|
| cv2 | OpenCV C++ 바인딩, 동적 멤버 |
| holidays | 런타임 국가별 로딩 |
| pdf2image | 선택적 의존성 |
| pytesseract | 선택적 의존성 |
| werkzeug | Flask 런타임 의존성 |
| win32com | Windows COM 동적 바인딩 |

### 4.2 필터링 로직

FALSE_POSITIVE_MODULES = ['cv2', 'holidays', 'pdf2image', 'pytesseract', 'werkzeug', 'win32com']

def is_false_positive(issue):
    return any(mod in issue['message'] for mod in FALSE_POSITIVE_MODULES)

---

## 5. 구문 검증

### 5.1 필수 검증 명령

uv run python -m py_compile <파일.py>

### 5.2 주요 구문 오류

| 오류 | 원인 | 해결 |
|------|------|------|
| unterminated string literal | docstring 미닫힘/중복 | 따옴표 쌍 확인 |
| invalid syntax | 구문 오류 | 해당 라인 검토 |
| IndentationError | 들여쓰기 불일치 | 공백/탭 통일 |

### 5.3 검증 흐름

코드 수정 → py_compile (필수) → 오류 시 재수정 → 테스트 → 완료

---

## 6. 디버깅 체크리스트

### 6.1 코드 분석

- [ ] 에러 라인 주변 코드 확인
- [ ] 변수 타입 검증
- [ ] 조건문 분기 확인
- [ ] 예외 처리 누락 여부

### 6.2 데이터 분석

- [ ] 입력값 유효성 확인
- [ ] DB 쿼리 결과 검증
- [ ] NULL/None 처리 확인

### 6.3 환경 분석

- [ ] 라이브러리 버전 확인
- [ ] 환경 변수 설정 확인
- [ ] 파일 권한 확인

### 6.4 Streamlit 특화

- [ ] session_state 키 존재 여부
- [ ] 위젯 key 중복 확인
- [ ] column_config 타입 일치
- [ ] st.rerun() 무한루프 확인

---

## 7. 수정 프로세스

원인 파악 → 최소 변경 → 영향 분석 → 수정 → 테스트 → 유사 패턴 수정

| 단계 | 설명 |
|------|------|
| 원인 파악 | 에러 메시지, 스택 트레이스 분석 |
| 최소 변경 | 필요한 부분만 수정 |
| 영향 분석 | 수정으로 인한 다른 영향 확인 |
| 수정 | 코드 변경 |
| 테스트 | py_compile, pytest 실행 |
| 유사 패턴 | 동일 문제 다른 위치 수정 |

---

## 8. 디버깅 도구 사용법

### 8.1 oaischeck

oaischeck              # 전체 에러 + 표준용어 체크
oaischeck [대상]       # 특정 대상 체크
oaischeck error        # 에러 체크만
oaischeck debug [에러] # 심층 디버깅
oaischeck circular     # 순환 참조 감지

### 8.2 oaisfix

oaisfix status         # 이슈 상태 조회
oaisfix run            # 이슈 자동 수정 (병렬)
oaisfix run [대상]     # 특정 이슈/파일 수정
oaisfix preview        # 수정 미리보기
oaisfix verify         # 수정 검증

### 8.3 oaislib (oais 모듈 전용)

oaislib status         # oais 모듈 상태 및 미해결 이슈 요약
oaislib run            # Phase 1 + Phase 2 실행 (분석 → 수정)
oaislib optimize       # run + 최적화 (성능, 중복제거)
oaislib doc            # d0005_lib.md 문서화만

### 8.4 oaisdb (DB 전용)

oaisdb status          # DB 상태 및 미해결 이슈 요약
oaisdb run             # Phase 1 + Phase 2 실행 (분석 → 수정)
oaisdb optimize        # run + 최적화 (인덱스, 쿼리)
oaisdb doc             # d0006_db.md 문서화만

---

## 9. 관련 문서

| 문서 | 용도 |
|------|------|
| doc/d0004_todo.md | 이슈 추적 |
| doc/d0010_history.md | 아카이브 이력 |
| v/oaischeck.md | 코드 품질 체크 |
| v/oaisfix.md | 자동 오류 수정 |
| v/oaislib.md | oais 모듈 디버깅 |
| v/oaisdb.md | DB 디버깅 |
| v/guide/common_guide.md | 공통 가이드라인 |
