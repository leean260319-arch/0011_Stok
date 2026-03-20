# oaisrun - TDD 기반 자율 실행 스킬 (Builder)

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-26 | version 서브명령어 추가, 문서 이력 관리 섹션 추가 |
| v01 | 2026-01-01 | 초기 문서 작성 |

---

## 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisrun version` | 스킬 버전 정보 (v02) |
| `oaisrun status` | 실행 큐 상태 확인 |
| `oaisrun [태스크ID]` | 특정 태스크 실행 |
| `oaisrun --auto` | 자동 TDD 사이클 실행 |

---

## 1. 개요

이 문서는 프로젝트의 **시공자(Builder)**로서, 설계자(Architect)가 수립한 상세 실행 계획을 받아 **자율적인 TDD(Test-Driven Development) 사이클**을 수행하는 스킬을 정의합니다.

**핵심 역할:**

- **자율 실행**: 실행 큐(Execution Queue)에 등록된 태스크 순차/병렬 처리
- **TDD 사이클**: Red → Green → Refactor 반복
- **자동 검증**: 테스트 통과 및 코드 품질 기준 충족 시까지 반복

**Architect vs Builder:**

- **Architect (`oaisplan`)**: 무엇을 어떻게 만들지 결정(상세 설계)하여 실행 큐에 등록
- **Builder (`oaisrun`)**: 실행 큐의 작업을 고민 없이 수행하고 결과 도출

**입력:**

- `실행 큐(Execution Queue)` (from `oaisplan detail`)
- `doc/d0002_plan.md` (참조)

**출력:**

- 구현된 소스 코드
- 통과된 테스트 코드
- 업데이트된 문서 (`doc/d0004_todo.md`, `doc/d0010_history.md`)

---

## 2. 전문 에이전트 활용

### 2.1 TDD 단계별 서브에이전트 매핑

| TDD 단계 | 서브에이전트 | 정의 파일 | 용도 |
|----------|--------------|-----------|------|
| 사전 분석 (선택적) | `codebase-investigator` | `v/agent/codebase_investigator.md` | 복잡한 구현 전 의존성/영향 분석 |
| RED (테스트 작성) | `task-executor` | `v/agent/task-executor.md` | 실패하는 테스트 코드 작성 |
| GREEN (구현) | `task-executor` | `v/agent/task-executor.md` | 테스트 통과를 위한 최소 구현 |
| REFACTOR (개선) | `python-code-reviewer` | `v/agent/python-code-reviewer.md` | 코드 품질 리뷰 및 개선 제안 |
| 검증 | `task-checker` | `v/agent/task-checker.md` | 태스크 완료 여부 검증 |
| 품질 보증 | `oaisqa` | `v/agent/oaisqa.md` | 중복 검사, 의존성 분석 |
| 에스컬레이션 분석 | `codebase-investigator` | `v/agent/codebase_investigator.md` | TDD 실패 시 근본 원인 심층 분석 |

> **Note**: `codebase-investigator`는 복잡한 태스크의 사전 분석, 또는 TDD 사이클이 반복 실패할 때 근본 원인 분석에 활용합니다.

### 2.2 서브에이전트 실행 예시

```python

# RED 단계: 실패하는 테스트 작성
Task(
    subagent_type="task-executor",
    prompt="""
    태스크 ID: {task_id}
    단계: RED (테스트 작성)

    요구사항:
    - {task_description}

    수행할 작업:
    1. 요구사항을 검증하는 pytest 테스트 작성
    2. 테스트가 명확히 실패하는지 확인
    3. 기존 테스트를 깨뜨리지 않는지 검증
    """
)

# GREEN 단계: 최소 구현
Task(
    subagent_type="task-executor",
    prompt="""
    태스크 ID: {task_id}
    단계: GREEN (구현)

    작성된 테스트: {test_file_path}

    수행할 작업:
    1. 테스트를 통과하는 최소한의 코드 작성
    2. 모든 테스트가 통과하는지 확인
    3. 회귀 없음 검증
    """
)

# REFACTOR 단계: 코드 리뷰
Task(
    subagent_type="python-code-reviewer",
    prompt="""
    태스크 ID: {task_id}
    단계: REFACTOR (코드 리뷰)

    구현 파일: {implementation_file}
    테스트 파일: {test_file}

    리뷰 항목:
    1. 코드 품질 (pylint, flake8 기준)
    2. 타입 힌트 완성도 (mypy 기준)
    3. 중복 코드 제거
    4. 가독성 개선

    --lang ko --confirm
    """
)

# 완료 검증
Task(
    subagent_type="task-checker",
    prompt="""
    태스크 ID: {task_id}

    검증 항목:
    1. 모든 테스트 통과 여부
    2. 코드 품질 기준 충족 여부
    3. 문서화 완료 여부
    """
)
```

### 2.3 병렬 실행 권장 케이스

| 조건 | 병렬 실행 방식 | 효과 |
|------|----------------|------|
| 복잡한 태스크 사전 분석 | `codebase-investigator` + `Explore` | 아키텍처 분석과 패턴 탐색 동시 수행 |
| 독립된 태스크 다수 | 여러 `task-executor` 동시 실행 | TDD 사이클 처리 시간 단축 |
| REFACTOR 단계 | `python-code-reviewer` + `oaisqa` 병렬 | 코드 리뷰와 품질 분석 동시 수행 |
| 전체 점검 (`oaisrun all`) | 각 스킬별 에이전트 병렬 | oaischeck, oaistest, oaislib 동시 실행 |
| 에스컬레이션 분석 | `codebase-investigator` + `python-code-reviewer` | 근본 원인 분석과 코드 품질 검토 동시 수행 |

### 2.4 에스컬레이션 시 에이전트 활용

반복 한계 도달 또는 모호한 요구사항 시:

```python

# 심층 분석을 위한 코드베이스 조사 에이전트
Task(
    subagent_type="codebase-investigator",
    prompt="""
    TDD 실패 근본 원인 분석:

    실패 정보:
    - 태스크: {task_id}
    - 반복 횟수: {iteration_count}
    - 마지막 에러: {last_error}

    분석 항목:
    1. 관련 코드의 의존성 체인 추적
    2. 유사한 구현 패턴 및 성공 사례 탐색
    3. 잠재적 충돌 또는 Side Effect 식별
    4. 구체적 해결 방안 및 우회책 제시

    --depth deep --format markdown --lang ko
    """
)

# 간단한 패턴 탐색 (경량 분석용)
Task(
    subagent_type="Explore",
    prompt="""
    TDD 실패 패턴 탐색

    실패 정보:
    - 태스크: {task_id}
    - 마지막 에러: {last_error}

    분석 요청:
    1. 유사한 구현 패턴 탐색
    2. 의존성 문제 확인
    3. 해결 방안 제시
    """
)

---

## 3. 명령어 체계

### 3.1 기본 명령어

| 명령어 | 설명 | 역할 |
|--------|------|------|
| `oaisrun` | **대기 중인 실행 큐 처리 (기본)** | **구현 실행** |
| `oaisrun execute [ID]` | 특정 태스크 즉시 실행 | 단일 실행 |
| `oaisrun all` | 프로젝트 전체 점검 (oaischeck + oaistest + ...) | 유지보수 |
| `oaisrun status` | 현재 진행 상태 및 큐 확인 | 모니터링 |
| `oaisrun resume` | 중단된 작업 재개 | 실행 제어 |

> **Note:** 기존의 `oaisrun plan` 명령어는 **`oaisplan detail`**로 이동되었습니다.

### 3.2 옵션

| 옵션 | 설명 |
|------|------|
| `--max-iterations N` | TDD 반복 최대 횟수 (기본: 10) |
| `--timeout M` | 태스크당 최대 시간(분) (기본: 30) |
| `--interactive` | 각 단계(Red/Green/Refactor)마다 사용자 승인 대기 |
| `--skip-refactor` | Refactor 단계 건너뛰기 (빠른 프로토타이핑용) |
| `--report` | 실행 리포트 생성 (`tmp/oaisrun_report.md`) |

---

## 4. TDD 실행 사이클 (The Loop)

`oaisrun`은 하나의 태스크에 대해 다음 루프를 **완료될 때까지(또는 한계 도달 시까지)** 반복합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    TDD 자율 실행 루프                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. RED (테스트 작성)                                       │
│     - 입력: 태스크 요구사항 (`oaisplan detail` 산출물)       │
│     - 행동: 실패하는 테스트 코드 작성 (pytest)               │
│     - 검증: 테스트가 **실패**하는지 확인                     │
│                                                             │
│  2. GREEN (구현)                                            │
│     - 입력: 실패하는 테스트                                  │
│     - 행동: 테스트를 통과하는 최소한의 코드 작성             │
│     - 검증: 테스트가 **통과**하는지 확인                     │
│                                                             │
│  3. REFACTOR (개선)                                         │
│     - 입력: 통과한 코드                                      │
│     - 행동: 중복 제거, 가독성 향상, 주석 추가                │
│     - 검증: 테스트 통과 유지, Lint/Type Check 통과           │
│                                                             │
│  4. COMPLETE (완료 처리)                                    │
│     - 행동: 문서 업데이트, 커밋, 다음 태스크로 이동          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 단계별 상세 로직

#### 1. RED (Clean Fail)

- **목표**: 구현되지 않음을 증명하는 테스트 작성.
- **성공 기준**:
  - 테스트 코드가 문법적으로 올바름.
  - 실행 시 `ImportError` 또는 `AssertionError` 등으로 명확히 실패함.
  - 기존의 다른 테스트를 깨뜨리지 않음.

#### 2. GREEN (Clean Pass)

- **목표**: 테스트를 통과시키는 가장 단순한 구현.
- **성공 기준**:
  - 작성된 테스트가 통과함.
  - 기존 모든 테스트가 여전히 통과함 (회귀 없음).

#### 3. REFACTOR (Clean Code)

- **목표**: 코드 품질 표준 준수.
- **체크리스트**:
  - `pylint`, `flake8` 검사 통과.
  - `mypy` 타입 체크 통과.
  - `v/guide/common_guide.md`의 코딩 컨벤션 준수.

---

## 5. 자동 반복 및 에스컬레이션

### 5.1 반복(Iteration) 제한

무한 루프 방지를 위해 각 태스크는 설정된 횟수(`--max-iterations`) 내에 완료되어야 합니다.

```python

# 의사 코드
failures = 0
while failures < MAX_RETRIES:
    try:
        run_cycle()
        if verification_passed():
            return SUCCESS
    except Exception:
        failures += 1
        analyze_and_fix() # 자율 수정 시도

escalate_to_user() # 한계 도달 시 사용자에게 위임
```

### 5.2 에스컬레이션 조건

다음 경우 `oaisrun`은 멈추고 **사용자 개입(Interactive Mode)**을 요청합니다.

1. **반복 횟수 초과**: 10회 이상 시도해도 테스트를 통과하지 못함.
2. **모호한 요구사항**: `oaisplan`이 제공한 정보로 구현 불가.
3. **환경 문제**: 패키지 설치 실패, API 연결 불가 등.

---

## 6. oaisrun all (프로젝트 건강검진)

`oaisrun all`은 프로젝트 전체의 상태를 점검하는 유지보수 명령입니다.

```bash
oaisrun all
```

**실행 순서:**

1. **oaischeck**: 정적 분석 및 에러 체크
2. **oaisfix run**: 발견된 단순 에러 자동 수정
3. **oaistest**: 전체 테스트 스위트 실행
4. **oaislib**: 모듈 문서 현행화
5. **oaisdb**: DB 스키마 문서 현행화

---

## 7. 관련 문서

| 문서 | 용도 |
|------|------|
| `v/oaisplan.md` | **Architect** - 상세 설계 및 태스크 공급 |
| `v/oaischeck.md` | 코드 품질 기준 정의 |
| `v/oaistest.md` | 테스트 실행 가이드 |
| `doc/d0002_plan.md` | 전체 구현 계획 |
| `doc/d0004_todo.md` | 이슈 및 완료 처리 |

---