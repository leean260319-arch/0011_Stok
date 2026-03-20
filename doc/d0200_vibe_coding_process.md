# d0200 Vibe Coding 프로세스

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-28 | 최초 작성 - oais 스킬 기반 개발 프로세스 정의 |

---

## 1. 개요

이 문서는 Vibe 코딩 환경에서 **oais 스킬**을 활용한 개발 프로세스를 정의한다. oais 스킬은 AI 에이전트(Claude Code, Gemini 등)가 프로젝트 개발 전 과정을 체계적으로 수행할 수 있도록 설계된 워크플로우 단위이다.

### 1.1 핵심 원칙

- **스킬 우선**: 모든 작업은 해당 oais 스킬이 있는지 먼저 확인하고 활용한다
- **문서 연동**: 각 스킬은 핵심 문서(d0001~d0010)와 자동 연계된다
- **서브에이전트 위임**: 복잡한 작업은 전문 서브에이전트에게 위임한다
- **TDD 기반**: 개발은 Red -> Green -> Refactor 사이클을 따른다

---

## 2. 스킬 전체 구조

### 2.1 스킬 분류

```
oais 스킬 (32개)
  |
  +-- 세션 관리 -------- oaisstart, oaisstop, oaiscontext, oaishelp
  |
  +-- 핵심 개발 -------- oaisprd, oaisplan, oaisdev, oaistest, oaischeck
  |
  +-- 유지보수 --------- oaisfix, oaislib, oaisdb, oaisenv
  |
  +-- 문서/이력 -------- oaistodo, oaiscommit, oaishistory, oaisdoc, oaisuser, oaiscommand
  |
  +-- 실행/유틸 -------- oaisrun, oaisbatch, oaisuv, oaissync, oaisskill
  |
  +-- 콘텐츠 생성 ------ oaisppt, oaisreport, oaisword, oaisbook, oaispaper, oaissurvey
  |
  +-- 특화 ------------- oaisstreamlit, oaisaddtodo
```

### 2.2 스킬-문서 연계 맵

| 핵심 문서 | 역할 | 관련 스킬 |
|-----------|------|----------|
| d0001_prd.md | 요구사항 정의 | oaisprd |
| d0002_plan.md | 구현 계획 | oaisplan |
| d0003_test.md | 테스트 시나리오 | oaisdev(생성), oaistest(갱신) |
| d0004_todo.md | 할일/디버깅 통합 관리 | oaistodo, oaischeck, oaisfix |
| d0005_lib.md | 라이브러리 문서 | oaislib |
| d0006_db.md | DB 구조/스키마 | oaisdb |
| d0007_command.md | 명령어 집계 | oaiscommand |
| d0008_user.md | 사용자 가이드 | oaisuser |
| d0009_env.md | 환경 현황 | oaisenv |
| d0010_history.md | 변경 이력 | oaiscommit, oaishistory |

---

## 3. 개발 프로세스 전체 흐름

### 3.1 전체 파이프라인

```
[세션 시작]
  oaisstart run
  oaisenv run
  oaiscontext [SP번호]
       |
       v
[요구사항 정의]
  oaisprd run          --> d0001_prd.md
  oaisprd clarify      --> 모호성 해소
       |
       v
[구현 계획]
  oaisplan run         --> d0002_plan.md
       |
       v
[TDD 개발]
  oaisdev run          --> 코드 구현 + d0003_test.md 자동 생성
       |
       v
[테스트]
  oaistest run         --> 테스트 실행, 결과 갱신
  oaistest checklist   --> 체크리스트 확인
       |
       v
[품질 검증]
  oaischeck run        --> 에러/중복/순환참조 감지
  oaischeck error      --> d0004_todo.md에 이슈 등록
       |
       v
[오류 수정]
  oaisfix run          --> 병렬 에이전트로 자동 수정
       |
       v
[커밋 및 이력]
  oaiscommit run       --> Git 커밋
  oaiscommit sync      --> d0004 완료항목 -> d0010 이동
       |
       v
[세션 종료]
  oaisstop run
```

### 3.2 간략 사이클 (빠른 개발)

```
oaisprd run -> oaisplan run -> oaisdev run -> oaischeck run -> oaiscommit run
```

### 3.3 배치 실행 (전체 자동화)

```
oaisbatch run          --> PRD부터 커밋까지 일괄 처리
oaisbatch unitdev      --> 단위 개발 파이프라인
```

---

## 4. 단계별 상세 프로세스

### 4.1 세션 시작

| 순서 | 스킬 | 명령어 | 동작 |
|------|------|--------|------|
| 1 | oaisstart | `oaisstart run` | common_guide.md 로드, 문서 상태 점검 |
| 2 | oaisenv | `oaisenv run` | 환경 정합성 검증, d0009_env.md 생성 |
| 3 | oaiscontext | `oaiscontext [N]` | 서브프로젝트 컨텍스트 설정 (SP 00~05) |

**세션 시작 시 확인 사항:**
- common_guide.md 최신 여부
- d0001_prd.md, d0004_todo.md, d0010_history.md 존재 여부
- 미해결 CRITICAL/ERROR 이슈 유무

### 4.2 요구사항 정의 (oaisprd)

```
oaisprd run      --> PRD 초안 생성/갱신
oaisprd clarify  --> 모호한 요구사항 해소 (질문-답변 기반)
oaisprd unitdev  --> 단위 기능 개발용 PRD 작성
```

**출력:** `doc/d{SP}0001_prd.md`

**핵심 규칙:**
- PRD에는 구현 상태(완료/진행중)를 포함하지 않는다
- 기능의 우선순위(Must/Should/Could)까지만 정의한다
- 구현 상태는 d0002_plan.md에서 관리한다

### 4.3 구현 계획 (oaisplan)

```
oaisplan run     --> PRD 기반 구현 계획 수립
```

**출력:** `doc/d{SP}0002_plan.md`

**포함 내용:**
- Epic 및 작업 분해(WBS)
- 스프린트 계획, 마일스톤
- 각 기능의 구현 상태 추적

### 4.4 TDD 기반 개발 (oaisdev)

```
oaisdev run      --> Red -> Green -> Refactor 사이클 실행
```

**출력:** 구현 코드 + `doc/d{SP}0003_test.md` (첫 실행 시 자동 생성)

**TDD 사이클:**
```
[RED]       테스트 작성 (실패하는 테스트)
   |
   v
[GREEN]     최소한의 코드로 테스트 통과
   |
   v
[REFACTOR]  코드 정리, 중복 제거
   |
   v
[VERIFY]    py_compile 구문 검증 (필수)
```

**필수 검증 명령어:**
```bash
uv run python -m py_compile <수정된파일.py>
```

### 4.5 테스트 (oaistest)

```
oaistest run       --> 테스트 실행
oaistest checklist --> 체크리스트 기반 확인
oaistest refresh   --> 테스트 시나리오 갱신
```

**출력:** `doc/d{SP}0003_test.md` 갱신

**테스트 실패 시:**
- d0004_todo.md 디버깅 섹션에 이슈 자동 등록
- 에러 분류: `[CRITICAL]`, `[ERROR]`, `[WARNING]`, `[INFO]`

### 4.6 품질 검증 (oaischeck)

```
oaischeck run      --> 전체 코드 품질 체크
oaischeck oais     --> oais 모듈 전용 체크
oaischeck error    --> 에러만 집중 체크
oaischeck debug    --> 디버깅 모드
oaischeck circular --> 순환 참조 감지
```

**출력:** d0004_todo.md에 발견된 이슈 등록

**병렬 에이전트 구성 (고급):**
- `code-error-checker` - 구문/런타임 에러
- `python-code-reviewer` - 코드 품질/패턴
- `oais-qa` - 중복/의존성 분석

### 4.7 오류 수정 (oaisfix)

```
oaisfix run        --> d0004_todo.md 기반 자동 수정
```

**동작 방식:**
1. d0004_todo.md에서 미해결 이슈 읽기
2. 이슈별 서브에이전트 위임 (병렬 처리)
3. 수정 후 py_compile 검증
4. 해결된 이슈 상태 업데이트

### 4.8 커밋 및 이력 (oaiscommit)

```
oaiscommit run       --> Git 커밋 실행
oaiscommit commit    --> 커밋만 실행
oaiscommit sync      --> d0004 완료항목 -> d0010 이동
oaiscommit github    --> GitHub 연동 (PR 등)
```

**커밋 규칙:**
- Conventional Commits 형식 사용
- 원자적 커밋 (단일 변경사항에 집중)
- 커밋 시 d0004_todo.md 완료 항목을 d0010_history.md로 이동

---

## 5. 보조 프로세스

### 5.1 모듈 관리 (oaislib)

```
oaislib run        --> oais/ 모듈 문제점 발견 및 수정
```
- d0005_lib.md와 연동
- 모듈 간 의존성 분석, 중복 감지

### 5.2 DB 관리 (oaisdb)

```
oaisdb run         --> DB 현황 분석
oaisdb design      --> DB 설계
oaisdb dev         --> DB 개발 (마이그레이션 등)
oaisdb validate    --> DB 정합성 검증
```
- d0006_db.md와 연동

### 5.3 환경 관리 (oaisenv)

```
oaisenv run        --> 환경 정합성 검증 (Python, 플러그인, 스킬)
oaisenv context    --> 현재 컨텍스트 출력
```
- d0009_env.md 자동 생성/갱신

### 5.4 TODO 관리 (oaistodo)

```
oaistodo run       --> Todo 상태 점검
oaistodo add       --> 새 항목 추가
oaistodo clear     --> 완료 항목 정리
```
- d0004_todo.md 직접 관리

### 5.5 이력 관리 (oaishistory)

```
oaishistory run    --> d0004 완료 항목을 d0010으로 이동
```

### 5.6 사용자 가이드 (oaisuser)

```
oaisuser run       --> 사용자 가이드 생성
oaisuser add       --> 가이드 항목 추가
oaisuser faq       --> FAQ 생성
oaisuser sync      --> 가이드 동기화
```
- d0008_user.md와 연동

---

## 6. 서브프로젝트(SP) 관리

### 6.1 컨텍스트 설정

```
oaiscontext 00     --> 공통 프로젝트 (d0001~d0010)
oaiscontext 01     --> 서브프로젝트 01 (d10001~d10010)
oaiscontext 02     --> 서브프로젝트 02 (d20001~d20010)
...
oaiscontext 05     --> 서브프로젝트 05 (d50001~d50010)
```

### 6.2 문서 번호 체계

| 범위 | 용도 |
|------|------|
| d0001~d0010 | SP 00 공통 문서 |
| d10001~d10010 | SP 01 문서 |
| d20001~d20010 | SP 02 문서 |
| d0200~ | 프로세스/가이드 문서 (이 문서) |

### 6.3 SP 전환 시 동작

컨텍스트를 변경하면 모든 oais 스킬이 해당 SP의 문서를 자동 참조한다.

```
oaiscontext 01 실행 후:
  oaisprd run   --> doc/d10001_prd.md 참조
  oaischeck run --> doc/d10004_todo.md에 이슈 기록
  oaiscommit    --> doc/d10010_history.md에 이력 기록
```

---

## 7. 에이전트 활용

### 7.1 서브에이전트 매핑

| 작업 유형 | 서브에이전트 | 관련 스킬 |
|----------|-------------|----------|
| 코드베이스 탐색 | Explore | oaischeck |
| 코드 구현/수정 | task-executor | oaisdev, oaisfix |
| Python 코드 리뷰 | python-code-reviewer | oaischeck |
| 구현 검증 | task-checker | oaistest |
| 품질 분석 | oais-qa | oaischeck |
| 웹앱 E2E 테스트 | web-test-orchestrator | oaistest |

### 7.2 병렬 에이전트 활성화 조건

다음 조건 중 하나라도 해당되면 병렬 에이전트를 활성화한다:
- 동시 수정 파일 3개 이상
- 다중 도메인 작업 (frontend + backend + DB)
- 10회 이상 반복 실패
- "종합", "전체" 등의 키워드 포함 요청

---

## 8. 콘텐츠 생성 프로세스

### 8.1 보고서/문서

```
oaisreport run             --> Markdown 리포트 생성
oaisreport pdf             --> PDF 변환
oaisreport pdf --pandoc    --> Pandoc 기반 PDF (수식 지원)
oaisreport algorithm       --> 알고리즘 리포트
```

### 8.2 프레젠테이션

```
oaisppt run                --> PPT 생성
oaisppt preview            --> 미리보기
```
- 슬라이드 10개 이상 시 병렬 생성

### 8.3 Word 문서

```
oaisword convert           --> Markdown -> Word 변환
oaisword quotation         --> 견적서 생성
```

### 8.4 학술 연구

```
oaispaper run              --> 논문 검색/분석
oaispaper trans            --> 논문 번역
oaispaper anal             --> 논문 심층 분석
oaispaper ref              --> 참고문헌 관리
oaissurvey run             --> 논문 서베이
```

### 8.5 도서 요약

```
oaisbook run               --> 도서/유튜브 서머리 생성
```

---

## 9. 운영 규칙

### 9.1 실행 규칙

| 항목 | 규칙 |
|------|------|
| Python 실행 | 반드시 `uv run` 사용 |
| 경로 | 절대경로 금지, 상대경로 사용 |
| 임시 파일 | `tmp/` 폴더에만 생성 |
| 프로젝트 루트 | 설정 파일만 허용, py/임시파일 금지 |
| 에러 처리 | try-except 생성 금지 (즉시 중단) |
| 인코딩 | UTF-8 출력 필수 |
| 언어 | 한국어 응답 |

### 9.2 문서 관리 규칙

- 모든 문서에 **문서 이력 관리** 섹션 포함
- 이력은 **최근 5개만 유지**
- 버전업 시 이전 문서는 `data/00_old/`로 이동
- 스크립트 파일명에 버전 포함하지 않음 (파일 내부 헤더에서 관리)

### 9.3 에러 추적 규칙

```
에러 발생
  --> d{SP}0004_todo.md "디버깅" 섹션에 등록
  --> 분류: [CRITICAL] / [ERROR] / [WARNING] / [INFO]
  --> 해결 시: 날짜 + 해결방법 기록
  --> oaiscommit sync로 d{SP}0010_history.md에 아카이브
```

---

## 10. 프로세스 패턴 요약

### 10.1 신규 기능 개발

```
oaisprd run -> oaisplan run -> oaisdev run -> oaistest run -> oaischeck run -> oaiscommit run
```

### 10.2 버그 수정

```
oaischeck run -> oaisfix run -> oaistest run -> oaiscommit run
```

### 10.3 코드 리뷰 및 개선

```
oaischeck run (병렬: code-error-checker + python-code-reviewer + oais-qa)
  -> oaisfix run -> oaiscommit run
```

### 10.4 환경 점검 및 동기화

```
oaisstart run -> oaisenv run -> oaissync list -> oaissync pull
```

### 10.5 전체 파이프라인 배치

```
oaisbatch run   --> PRD부터 커밋까지 전체 자동 실행
```

---

## 11. 관련 문서

| 문서 | 설명 |
|------|------|
| v/guide/common_guide.md | 프로젝트 공통 가이드라인 |
| CLAUDE.md | Claude Code 에이전트 설정 |
| doc/d0001_prd.md | 프로젝트 요구사항 정의서 |
| doc/d0004_todo.md | 할일 및 디버깅 관리 |
| doc/d0010_history.md | 변경 이력 |
| doc/d0007_command.md | 명령어 집계 |
