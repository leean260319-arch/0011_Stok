# CLAUDE.md

## Project Guidelines

> **세션 시작 시 필수**: 아래 파일을 먼저 읽고 지침을 따를 것

1. `v/guide/common_guide.md` - 프로젝트 공통 개발 표준, 디렉토리 구조, 에이전트 워크플로우 원칙

## most important references(MIR)

### 핵심 문서 (d*.md)

@d0001_prd.md
@d0004_todo.md
@d0003_test.md
@d0005_lib.md
@d0006_db.md
@d0008_user.md
@d0009_env.md
@d0010_history.md

### 스킬/워크플로우 문서 (v/oais*.md)

- v/oaischeck.md - 코드 에러 체크
- v/oaisfix.md - 코드 오류 수정
- v/oaistest.md - 테스트 관리
- v/oaislib.md - oais 모듈 관리
- v/oaisdb.md - DB 관리
- v/oaisuser.md - 사용자 관리
- v/oaiscommand.md - 명령어 관리
- v/oaisprd.md - PRD 생성
- v/oaisplan.md - 구현 계획
- v/oaisdev.md - TDD 기반 개발
- v/oaiscommit.md - Git 커밋

### MIR 참조 가이드

- **디버깅/에러 관리**: d0004_todo.md의 "디버깅" 섹션 참조
  - 에러 발생 시 해당 섹션에 기록 및 추적
  - 해결된 이슈는 해결된 이슈 섹션에 보관

### 핵심 문서 템플릿 (d*.md)

프로젝트 핵심 문서 생성 시 아래 템플릿을 참조:

| 문서 | 용도 | 설명 |
|------|------|------|
| d0001_prd.md | PRD | 프로젝트 요구사항 정의서 |
| d0004_todo.md | TODO/디버깅 | 할 일 관리 및 디버깅 추적 |
| d0003_test.md | 테스트 | 테스트 시나리오 가이드라인 |
| d0005_lib.md | 라이브러리 | 사용된 라이브러리 및 종속성 문서 |
| d0006_db.md | 데이터베이스 | DB 구조, 스키마, 쿼리 가이드 |
| d0008_user.md | 사용자 | 사용자 가이드/매뉴얼 |
| d0009_env.md | 환경 | 개발 환경 현황 (oaisenv run 자동 생성) |
| d0010_history.md | 이력 | 프로젝트 변경 이력 관리 |

### oais 스킬 매핑 (v/oais*.md)

| 스킬 | 용도 | 연동 문서 |
|------|------|----------|
| oaischeck | 코드 에러 체크 | → d0004_todo.md |
| oaisfix | 코드 오류 수정 | ← d0004_todo.md |
| oaistest | 테스트 관리 | ↔ d0003_test.md |
| oaislib | oais 모듈 관리 | → d0005_lib.md |
| oaisdb | DB 관리 | → d0006_db.md |
| oaisuser | 사용자 관리 | → d0008_user.md |
| oaisprd | PRD 생성/정제 | → d0001_prd.md |
| oaisplan | 구현 계획 | → d0002_plan.md |
| oaisdev | TDD 기반 개발 | - |
| oaiscommit | Git 커밋 | → d0010_history.md |

#### 문서 워크플로우

```
오류 발생 → d0004_todo.md (디버깅 섹션에 등록/추적) → d0010_history.md (이력)
```

#### 디버깅 워크플로우

- 모든 에러/디버깅 사항은 **d0004_todo.md의 "디버깅" 섹션**에서 통합 관리
- 에러 분류: `[CRITICAL]`, `[ERROR]`, `[WARNING]`, `[INFO]`
- 해결된 이슈는 날짜 및 해결방법과 함께 보관

#### 테스트 워크플로우

```
테스트 계획 (d0003_test.md 가이드라인 참조)
    ↓
테스트 시나리오 작성 (oaistest 스킬 실행)
    ↓
테스트 실행 (Playwright/수동)
    ↓
결과 기록 (d0003_test.md 업데이트)
    ↓
문제점 등록 (d0004_todo.md 디버깅 섹션)
```

- 테스트 가이드라인: **d0003_test.md** 참조
- 테스트 시나리오 생성: **oaistest** 스킬 실행
- 테스트 실패 시 반드시 d0004_todo.md에 이슈 등록

#### 문서 생성 규칙

- 새 문서 생성 시 해당 템플릿 구조 준수
- 문서이력관리 섹션을 문서 상단에 필수 포함
- 문서 번호 체계:
  - **d0001~d0010**: 핵심 문서 (PRD, TODO, 테스트, DB, 라이브러리, 사용자, 이력)
  - **a0001~a0009**: 스킬/워크플로우 문서 (체크, 수정, 테스트, 분석, 명령어, 템플릿, 스크립트)

### 서브프로젝트 구조 및 문서 번호 체계

> 프로젝트별 서브프로젝트 구조는 `doc/d0001_prd.md` 참조

#### 문서 번호 체계 (공통)

| 범위 | 용도 |
|------|------|
| d0001~d9999 | 00_공통 (전체 프로젝트 공통 문서) |
| d10000~ | 서브프로젝트별 문서 (PRD에서 정의) |

- 문서 번호 형식: `d[서브프로젝트번호][4자리문서번호]`
- 예시: `d20001` = 02번 서브프로젝트의 0001번 문서

## most important guidelines(MIG)

- 오류 분석/디버깅 작업은 반드시 d0004_todo.md의 '디버깅' 섹션을 참조하고 업데이트할 것
- 새로운 오류 발견 시 d0004_todo.md의 디버깅 섹션에 항목 추가할 것
- 항상 OS를 먼저 확인 후, 해당 OS에 맞는 명령어를 사용하라
- 가장 중요한 가이드는 어떤업무를 요청하던지 우선 적절한 서브에이전트에게 skills를 사용하는 것을 우선 검토하고, 이후 다양한 command와 mcp를 이용해서 아래 내용 진행해라.
- 웹페이지이외에는 스크립트는 이모지 사용금지
- 항상 한국어로 답하기
- 서브에이전트를 항상 이용해서 context를 아낄 것
- 필요한 MCP 서버가 있으면 사용자에게 설치를 요청할 것
- **[필수] 프로젝트 루트에 파일 생성 금지**: 모든 임시/테스트/디버그 파일은 반드시 `tmp/` 폴더에만 생성할 것
- **[필수] tmp/ 폴더 사용 규칙**: 스크립트 테스트, 디버깅, 임시 출력 등 모든 임시 파일은 `tmp/`에 저장
- 메세지가 깨어지지 않도록 utf-8로 출력되도록 할 것
- 파이썬 실행은 uv run 으로 실행
- 절대경로는 사용하지 말라
- 파일 업버전하라고 하기 전까지는 새버전 생성하지 말 것
- 에러가 나면 그대로 프로그램이 멈춰도 되니, try except 구문을 만들지 말라
- doc/*.md 문서에 대해서 이전 버전에서 현재버전에 어떤 내용이 변경되었는지를 문서의 처음 섹션에 문서이력관리 섹션에서 문서가 업버전될때마다 업데이트할 것, 이전 버전의 문서는 project folder/data/00_old로 이동시킴
- **[버전 관리 규칙]**: 스크립트 파일명에는 버전을 포함하지 않고, 파일 내부 헤더에서 버전 관리. 단, `src/ps00/ps0000_python_template_vXX.py` 템플릿 파일은 예외 (버전을 빠르게 확인해야 하므로 파일명에 버전 포함)

### directory

- oais module dir : oais/
- data dir : data/
- document dir : doc/
- temporary dir : tmp/ (모든 임시/테스트/디버그 파일은 여기에만 생성)
- db dir : db/
- **project root** : 설정파일(*.md,*.toml 등)만 허용, py/임시파일 생성 금지

## 업무 처리 우선순위 (최우선 적용)

**모든 업무 요청 시 아래 순서를 따를 것**

### 1단계: oais-leader 우선 검토

- 모든 업무 요청은 **oais-leader 에이전트가 먼저 검토**
- oais-leader가 작업 복잡도, 범위, 필요 도구를 분석
- 적절한 서브에이전트와 Skills 조합 결정

### 2단계: Skills 우선 활용

- 해당 작업에 맞는 **Skills를 우선 검토**
- Skills로 해결 가능하면 Skills 사용
- **프로젝트 스킬** (v/oais*.md):
  - `oaischeck`: 코드 분석 → d0004_todo.md 기입
  - `oaisfix`: d0004_todo.md 기반 오류 수정
  - `oaistest`: 테스트 시나리오 작성/현행화
  - `oaislib`: oais 모듈 분석/문서화
  - `oaisdb`: DB 구조 분석/문서화
  - `oaisuser`: 사용자 계정 관리
- **범용 스킬**: xlsx, docx, pptx, pdf, skill-creator, mcp-builder, canvas-design, webapp-testing 등

### 3단계: MCP 및 도구 활용

- Sequential Thinking: 복잡한 분석 및 계획
- Playwright: 웹 테스트 및 자동화
- TaskMaster: 태스크 관리
- GitHub MCP: GitHub 연동
- 기타 필요한 MCP 서버 및 command 활용

### 4단계: 서브에이전트 위임

- oais-leader가 결정한 서브에이전트에게 작업 위임
- 병렬 처리 가능한 작업은 동시 위임

## Subagent 기본 위임 규칙 (Context 절약)

**원칙**: 메인 컨텍스트 절약을 위해 가능한 모든 작업을 subagent에게 위임

### 기본 위임 매핑

| 작업 유형 | Subagent | 설명 |
|----------|----------|------|
| 코드베이스 탐색/검색 | Explore | 파일 찾기, 코드 검색, 구조 파악 |
| 코드 구현/수정 | task-executor | 기능 구현, 버그 수정, 리팩토링 |
| Python 코드 리뷰 | python-code-reviewer | 품질, 성능, 버그 검토 |
| Python 알고리즘 | python-algorithm-expert | 알고리즘 분석/수정 |
| 구현 검증 | task-checker | 완료된 작업 검증, QA |
| 품질 분석 | oais-qa | 중복 감지, 의존성 분석 |
| 복잡한 다중 작업 | oais-leader | 여러 subagent 조율 |
| 웹앱 테스트 | web-test-orchestrator | E2E 테스트, Playwright |
| 데이터 분석 | data-analyst | 통계, 트렌드 분석 |
| 학술 연구 | academic-researcher | 논문 검색, 문헌 분석 |

### 위임 우선순위

1. **항상 위임**: 코드 탐색(Explore), 코드 구현(task-executor)
2. **적극 위임**: 리뷰, 분석, 테스트 작업
3. **조율 필요시**: oais-leader로 복잡한 작업 조율

### 위임하지 않는 경우

- 단순 질문/답변 (1-2줄 응답)
- 파일 1개 간단 수정
- 사용자와 대화형 확인 필요 시

### oais-leader 자동 활성화 조건

- 파일 2개 이상 영향받는 작업
- 코드 리뷰 + 개선이 함께 필요한 경우
- 다중 도메인 분석 (보안, 성능, 품질 동시 검토)
- "종합", "전체", "comprehensive" 키워드

### 활용 도구

- Sequential Thinking: 복잡한 분석 및 계획
- TaskMaster: 태스크 관리
- GitHub MCP: GitHub 연동

## Task Master AI Instructions

**Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**
@./.taskmaster/CLAUDE.md
