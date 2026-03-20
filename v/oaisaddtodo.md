# oaisaddtodo - Todo 자동 처리 스킬

> 공통 가이드: `v/guide/common_guide.md` | 컨텍스트: `v/oaiscontext.md`

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-06 | 최초 생성 (command에서 skill로 전환, 자동 처리 기능 추가) |

---

## 1. 개요

d{SP}0004_todo.md 문서의 "대기 중" 섹션을 관리하고, 대기 중인 업무를 자동으로 처리합니다.

**핵심 기능**:
1. **자동 처리**: 인자 없이 실행 시 대기 중 업무를 순차 처리
2. **할 일 추가**: 새로운 할 일을 대기 중 섹션에 추가
3. **상태 조회**: 현재 대기 중인 할 일 목록 표시

**옵션**: `--sp N` (서브프로젝트)

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisaddtodo` | **대기 중 업무 자동 처리** (기본 동작) |
| `oaisaddtodo status` | 현재 대기 중인 할 일 목록 표시 |
| `oaisaddtodo version` | 스킬 버전 정보 (v01) |
| `oaisaddtodo add [text]` | 새 할 일 추가 |

실행: `uv run python v/script/oaisaddtodo_run.py [subcommand] [args]`

---

## 3. 자동 처리 워크플로우

### 3.1 기본 동작 (`oaisaddtodo`)

```
oaisaddtodo 실행
    ↓
d{SP}0004_todo.md "대기 중" 섹션 읽기
    ↓
대기 중 항목 없음? → "처리할 업무가 없습니다" 출력 후 종료
    ↓
대기 중 항목 있음:
    ↓
각 항목에 대해:
    1. 항목을 "진행 중"으로 이동
    2. 업무 유형 분석
    3. 적절한 스킬 호출 (oaisdev, oaissync 등)
    4. 완료 시 "완료" 섹션으로 이동
    ↓
모든 항목 처리 완료까지 반복
```

### 3.2 업무 유형별 처리

| 업무 유형 | 키워드 | 호출 스킬 |
|----------|--------|----------|
| 기능 구현 | 구현, 개발, 추가, 생성 | `oaisdev run` |
| 동기화 | 동기화, sync | `oaissync run` |
| 수정/버그 | 수정, 버그, fix | `oaisfix` |
| 문서 | 문서화, 작성 | `oaisdoc` |
| 기타 | - | 에이전트 직접 처리 |

### 3.3 상태 전이

```
[대기 중] → [진행 중] → [완료]
              ↓ (실패 시)
            [디버깅 섹션에 등록]
```

---

## 4. 사용 예시

### 자동 처리 (기본)
```bash
# 대기 중 업무 전체 처리
oaisaddtodo

# 서브프로젝트 지정
oaisaddtodo --sp 02
```

### 상태 조회
```bash
oaisaddtodo status
```

**출력 예시**:
```
# 대기 중인 Todo 목록

| ID | 등록일 | 내용 | 우선순위 | 비고 |
|----|--------|------|---------|------|
| T004 | 2026-01-06 | oaisaddtodo 명령어 생성 완료 | Medium | v/command/oaisaddtodo.md |
| T005 | 2026-01-06 | oaissync diff 기능 다른 프로젝트 동기화 | High | - |

총 2개 항목
```

### 할 일 추가
```bash
# 기본 추가
oaisaddtodo add "새로운 기능 구현"

# 우선순위 지정
oaisaddtodo add "긴급 버그 수정" --priority high

# 비고 추가
oaisaddtodo add "API 문서화" --note "v2.0용"
```

---

## 5. 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--sp N` | 서브프로젝트 지정 (d{SP}0004 사용) | 00 |
| `--priority [high\|medium\|low]` | 우선순위 지정 (add 시) | medium |
| `--note [text]` | 비고 추가 (add 시) | - |
| `--dry-run` | 실제 처리 없이 계획만 표시 | false |
| `--max-items N` | 최대 처리 항목 수 | 전체 |

---

## 6. 서브에이전트 연동

자동 처리 시 업무 유형에 따라 다음 서브에이전트를 활용:

| 단계 | 에이전트 | 역할 |
|------|----------|------|
| 분석 | `Explore` | 업무 내용 분석, 유형 판별 |
| 구현 | `task-executor` | oaisdev 연동 작업 수행 |
| 검증 | `task-checker` | 완료 검증 |

---

## 7. 서브프로젝트 지원

컨텍스트에 따라 대상 문서가 달라집니다:

| SP | Todo 문서 |
|:--:|----------|
| 00 | doc/d0004_todo.md |
| 01 | doc/d10004_todo.md |
| 02 | doc/d20004_todo.md |

---

## 8. 관련 문서

- `v/oaisdev.md` - TDD 기반 개발 스킬
- `v/oaissync.md` - 프로젝트 동기화
- `v/oaisfix.md` - 버그 수정 스킬
- `v/oaiscontext.md` - 컨텍스트 시스템
- `doc/d{SP}0004_todo.md` - Todo/디버깅 문서
