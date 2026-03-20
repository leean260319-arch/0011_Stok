# oaisenv - 개발 환경 및 스킬 정합성 검증

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v07 | 2026-01-26 | 섹션 6/7 에이전트/커맨드 사용 상태 관리 추가 (v/unuse/ 폴더 활용) |
| v06 | 2026-01-25 | `oaisenv run` 통합 (--fix, --verbose 제거, 항상 자동수정+상세출력) |
| v05 | 2026-01-25 | `oaisenv context` 서브명령어 추가 (토큰 모니터링, Memory 연동, 파일 관리) |
| v04 | 2026-01-23 | `oaisenv run` 실행 시 `doc/d0009_env.md` 환경 리포트 자동 생성 |
| v03 | 2026-01-15 | uv cleanup 기능 추가 (미사용 패키지 탐지 및 삭제) |
| v02 | 2026-01-05 | validate --full 기능 추가 (에이전트/커맨드/MCP 정합성 검증) |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

## 1. 개요

개발 전 환경 점검 통합 스킬 - 플러그인, Python 의존성, 스킬 정합성 일괄 점검/수정

**관련:** `v/oaisstart.md`, `v/oaischeck.md`, `v/guide/common_guide.md`

---

## 2. 서브명령어

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `oaisenv status` | 서브명령어 리스트, 상태 요약 | 터미널 |
| `oaisenv version` | 스킬 버전 정보 (v07) | 터미널 |
| `oaisenv run` | 통합 점검 + 자동 수정 + 상세 출력 | **d0009_env.md** + 터미널 |
| `oaisenv run --dry-run` | 점검만 (수정 안 함) | 터미널 |
| `oaisenv plugin` | 플러그인 상태 확인 | 설치 가이드 |
| `oaisenv validate` | 스킬 정합성 검증 | d{SP}0004 업데이트 |
| `oaisenv validate --full` | oais*.md 스킬 스캔 → 에이전트/커맨드/MCP 참조 검증 | 터미널 + d{SP}0004 |
| `oaisenv agent` | 에이전트 경로 검증 | 터미널 + d{SP}0004 |
| `oaisenv structure` | 문서 구조 검증 | 터미널 |
| `oaisenv reflect` | 설정 파일 반영 검증 | 터미널 + d{SP}0004 |
| `oaisenv command` | v/command/ 연동 검증 | 터미널 + d{SP}0004 |
| `oaisenv sync-agents` | 에이전트 폴더 동기화 | 파일 동기화 |
| `oaisenv sync-skills` | 스킬 폴더 동기화 | 파일 동기화 |
| `oaisenv install` | 누락 환경 요소 설치 | 설치 실행 |
| `oaisenv uv check` | UV 의존성 상태 체크 | 터미널 + d{SP}0004 |
| `oaisenv uv update` | UV 의존성 업데이트 | 패키지 업데이트 |
| `oaisenv uv cleanup` | **미사용 패키지 탐지 및 삭제** | 터미널 (대화형) |
| `oaisenv context status` | **컨텍스트 전체 상태** | 터미널 |
| `oaisenv context token` | **토큰 사용량 추정** | 터미널 |
| `oaisenv context files` | **컨텍스트 파일 목록** | 터미널 |
| `oaisenv context size` | **파일별 토큰 크기** | 터미널 |
| `oaisenv context validate` | **컨텍스트 파일 검증** | 터미널 |
| `oaisenv context save "msg"` | **메모리에 정보 저장** | tmp/context_memory.json |
| `oaisenv context load` | **메모리에서 로드** | 터미널 |
| `oaisenv context list` | **저장된 엔티티 목록** | 터미널 |
| `oaisenv context clear` | **메모리 초기화** | 터미널 |

---

## 3. 에이전트 활용

> 에이전트 원칙: `v/guide/common_guide.md` 섹션 2 참조

| 단계 | 작업 | 에이전트 |
|------|------|----------|
| 1 | 환경 구조 탐색 | `Explore` (내장) |
| 2 | 정합성 분석 | `oais-qa` |
| 3-4 | 동기화/기록 | `task-executor` |

Task() 예시:
```
Task(subagent_type="oaisqa", prompt="v/oais*.md 정합성 검증 → [VALIDATION] 태그")
Task(subagent_type="task-executor", prompt="v/agent/ → .claude/agents/ 섹션 병합")
```

---

## 4. 환경 관리

### 4.1 superpowers 플러그인

설치: `/plugin marketplace add obra/superpowers-marketplace` → `/plugin install superpowers@superpowers-marketplace`

### 4.2 UV 의존성

> Python 실행: `uv run` 필수 (common_guide.md 4.1 참조)

- `oaisenv uv check`: 오래된/취약점 패키지 감지 → `[DEP]` 태그
- `oaisenv uv update`: 패키지 업데이트
- `oaisenv uv cleanup`: 미사용 패키지 탐지 및 삭제

### 4.3 uv cleanup 상세

pyproject.toml의 의존성과 실제 코드 import를 비교하여 미사용 패키지를 탐지합니다.

**워크플로우:**

```
1. pyproject.toml 의존성 추출
     ↓
2. 프로젝트 코드에서 import 문 스캔
     ↓
3. 미사용 패키지 리스트업
     ↓
4. 사용자 확인 (대화형)
     ↓
5. 선택된 패키지 삭제 (uv remove)
```

**실행:**

```bash
uv run python v/script/oaisenv_uv_cleanup.py
uv run python v/script/oaisenv_uv_cleanup.py --dry-run    # 삭제 없이 미리보기
uv run python v/script/oaisenv_uv_cleanup.py --auto       # 확인 없이 자동 삭제
```

**옵션:**

| 옵션 | 설명 |
|------|------|
| `--dry-run` | 미사용 패키지 목록만 표시 (삭제 안 함) |
| `--auto` | 확인 없이 자동 삭제 |
| `--exclude PKG` | 특정 패키지 제외 (반복 가능) |
| `--include-dev` | dev 의존성도 검사 |

**제외 대상 (자동):**

- 런타임에만 사용되는 패키지 (uvicorn, gunicorn 등)
- 테스트 프레임워크 (pytest, coverage 등)
- 타입 힌트 패키지 (types-* 등)
- 빌드 도구 (setuptools, wheel 등)

---

## 5. 정합성 검증

| 명령어 | 검증 대상 | 규칙 |
|--------|----------|------|
| `agent` | 에이전트 테이블 | v/agent/ 경로 존재 |
| `structure` | 문서 구조 | 필수 섹션, 번호 연속성 |
| `reflect` | CLAUDE.md/GEMINI.md | MIR 스킬 등록 |
| `command` | v/command/*.md | 통합 명령어 매핑 |
| `validate --full` | oais*.md 전체 스캔 | 에이전트/커맨드/MCP 교차 검증 |

### 5.1 validate --full 상세

oais*.md 스킬 파일을 스캔하여 참조된 리소스가 현재 환경에 존재하는지 검증합니다.

**검증 대상:**

| 리소스 | 추출 패턴 | 검증 경로 |
|--------|----------|----------|
| 에이전트 | `subagent_type="xxx"`, `v/agent/xxx.md` | v/agent/, .claude/agents/ |
| 커맨드 | `v/command/xxx.md` | v/command/, .claude/commands/ |
| MCP | `mcp__xxx__`, 서버명 직접 참조 | .mcp.json mcpServers |

**옵션:**

| 옵션 | 설명 |
|------|------|
| `--verbose`, `-v` | 유효한 참조도 표시 |
| `--sp N` | 서브프로젝트 지정 (기본: 00) |
| `--output-todo` | 누락 항목을 todo 형식으로 출력 |

**실행:**

```bash
uv run python v/script/oaisenv_validate_full.py
uv run python v/script/oaisenv_validate_full.py --verbose
uv run python v/script/oaisenv_validate_full.py --output-todo --sp 02
```

**출력 예시:**

```
[oaisfix.md]
  ❌ 에이전트 누락: some-missing-agent
  ❌ MCP 누락: some-missing-mcp
```

---

## 6. 에이전트 동기화

**Source:** `v/agent/` (우선) → **Target:** `.claude/agents/`, `.gemini/agents/`

| Source | Target | 결과 |
|--------|--------|------|
| 있음 | 없음 | 추가 |
| 없음 | 있음 | 역병합 후보 |
| 다름 | 다름 | Source 우선 |

옵션: `--dry-run`, `--verbose`, `--reverse`, `--section "2.1"`

---

## 7. 스킬 동기화

경로: `v/oaisXXX.md` → `.claude/skills/oaisXXX/SKILL.md`

옵션: 에이전트 동기화와 동일

---

## 8. 워크플로우

### 8.1 oaisenv run 흐름

```
oaisenv run
  ├─ 1. 플러그인 → [ENV]
  ├─ 2. UV 의존성 → [DEP]
  ├─ 3. 정합성 → [VALIDATION]
  ├─ 4. 환경 리포트 생성 → doc/d0009_env.md
  └─ 5. 리포팅/수정 (--fix)
```

### 8.2 d0009_env.md 리포트 내용

`oaisenv run` 실행 시 자동 생성되는 환경 현황 문서:

| 섹션 | 내용 |
|------|------|
| 1. 시스템 환경 | Python, UV, Node.js, npm, Git, Pandoc 버전 |
| 2. MCP 서버 | 설치/미설치 상태, 설치 방법 |
| 3. Claude 플러그인 | 설치/미설치 상태 (O/X), 설치 방법 |
| 4. Claude 스킬 | 설치/미설치 상태 (O/X), 설치 방법 |
| 5. oais 스킬 | v/oais*.md 파일 목록 |
| 6. 에이전트 현황 | **사용/미사용 상태 (O/X)**, 역할 설명 |
| 7. 커맨드 현황 | **사용/미사용 상태 (O/X)**, 역할 설명 |
| 8. Python 패키지 | 패키지 수, PyTorch 버전, CUDA 상태 |
| 9. 검증 결과 | 발견/수정/남은 이슈, 검증 상태 |

### 8.3 에이전트/커맨드 관리

에이전트와 커맨드는 폴더 이동으로 사용 상태를 관리합니다.

**에이전트 관리:**
| 작업 | 경로 이동 |
|------|----------|
| 삭제 (미사용) | `v/agent/xxx.md` → `v/unuse/agent/xxx.md` |
| 설치 (사용) | `v/unuse/agent/xxx.md` → `v/agent/xxx.md` |

**커맨드 관리:**
| 작업 | 경로 이동 |
|------|----------|
| 삭제 (미사용) | `v/command/xxx.md` → `v/unuse/command/xxx.md` |
| 설치 (사용) | `v/unuse/command/xxx.md` → `v/command/xxx.md` |

**레지스트리:**
- 에이전트/커맨드 목록은 `v/script/oaisenv_run.py`의 `AGENT_REGISTRY`, `COMMAND_REGISTRY`에서 관리
- 새 에이전트/커맨드 추가 시 레지스트리에도 등록 필요

### 8.4 --fix 자동 수정

| 문제 | 수정 |
|------|------|
| 플러그인 미설치 | `/plugin install` |
| 취약 패키지 | `uv update` |
| 동기화 필요 | `sync-agents` |

### 8.5 태그

`[ENV]` 환경 | `[DEP]` 의존성 | `[VALIDATION]` 정합성 | `[SYNC]` 동기화

---

## 9. MCP/도구

> 도구 원칙: `v/guide/common_guide.md` 섹션 2 참조

| 항목 | 도구 |
|------|------|
| 심볼 검증 | `mcp__serena__find_symbol` |
| 패턴 검색 | `mcp__grep__search` |
| 품질 분석 | `oais-qa` |

---

## 10. 컨텍스트 관리 (Context Management)

### 10.1 개요

세션 컨텍스트를 효율적으로 관리하기 위한 기능:

| 카테고리 | 기능 | 설명 |
|----------|------|------|
| 토큰 모니터링 | `context token` | 파일별 토큰 사용량 추정 |
| Memory 연동 | `context save/load` | 세션 간 정보 유지 |
| 파일 관리 | `context files/validate` | 컨텍스트 파일 검증 |

### 10.2 토큰 모니터링

컨텍스트 윈도우 사용량을 추정하여 효율적인 세션 관리를 지원합니다.

```bash
uv run python v/script/oaisenv_context.py token
```

**추정 방식:**
- 영문: 4자 = 1토큰
- 한글: 2자 = 1토큰
- 컨텍스트 윈도우: 200,000 토큰 기준

### 10.3 Memory 연동

세션 간 정보를 유지하기 위해 로컬 메모리 파일(`tmp/context_memory.json`)을 사용합니다.

```bash
# 정보 저장
uv run python v/script/oaisenv_context.py save "PRD 변경: 인증 방식 JWT로 결정"

# 저장된 정보 로드
uv run python v/script/oaisenv_context.py load

# 엔티티 목록
uv run python v/script/oaisenv_context.py list

# 메모리 초기화
uv run python v/script/oaisenv_context.py clear
```

**MCP memory 서버 연동:**
- MCP memory 서버가 설치된 경우 자동 연동
- 로컬 파일은 백업용으로 유지

### 10.4 파일 관리

컨텍스트에 로드되는 파일들을 관리합니다.

```bash
# 파일 목록
uv run python v/script/oaisenv_context.py files

# 파일별 토큰 크기
uv run python v/script/oaisenv_context.py size

# 파일 검증
uv run python v/script/oaisenv_context.py validate
```

**관리 대상 파일:**
- `CLAUDE.md` - 프로젝트 지침
- `.claude/settings.json` - 도구 설정
- `.claude/agents/*.md` - 커스텀 에이전트
- `.claude/commands/*.md` - 슬래시 커맨드
- `v/guide/*.md` - 가이드 문서

---

## 11. 관련 문서

- `v/oaisstart.md` - 세션 시작
- `v/oaischeck.md` - 코드 품질 체크
- `v/guide/common_guide.md` - 공통 가이드라인
