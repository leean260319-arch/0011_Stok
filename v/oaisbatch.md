# oaisbatch - 전체 파이프라인 배치 실행

> 참조: v/guide/common_guide.md (에이전트 원칙), v/oaiscontext.md (서브프로젝트)

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v09 | 2026-01-09 | d0004 규칙 변경: 병행 처리 → 단일 문서 (oaiscontext 기준) |
| v08 | 2026-01-05 | test 단계를 oaistest run 호출로 변경 (pytest 직접 → oaistest 스킬) |
| v07 | 2026-01-04 | test 단계 강화: 테스트 0개 시 경고, 페이지 import 테스트 필수 |
| v06 | 2026-01-03 | unitdev 서브명령어 추가 (단위개발문서 기준 페이지 단위 파이프라인) |
| ~~v05~~ | ~~2026-01-03~~ | ~~d0004 병행 처리 규칙 추가~~ (v09에서 변경됨) |
| v04 | 2026-01-03 | dev 단계에 d0004 사전 검토 추가 (기존 이슈 확인) |
| v03 | 2026-01-03 | check 단계 스코프 명확화 (서브프로젝트 루트 + pages/ 전체) |
| v02 | 2026-01-03 | sql-check를 db 단계로 통합 (oaisdb run = validate + 분석 + 수정) |
| v01 | 2026-01-02 | 최초 생성 |

---

## 1. 개요

PRD→커밋 전체 파이프라인 일괄 실행. `--sp N` 또는 `oaiscontext N`으로 서브프로젝트 지정.

## 2. 명령어

| 명령어 | 설명 |
|--------|------|
| `oaisbatch version` | 스킬 버전 정보 (v09) |
| status | 서브명령어 리스트, 진행 상태 |
| run | 전체 실행 |
| run --from/--to/--skip/--only [단계] | 부분 실행 |
| unitdev [문서번호] | 단위개발문서 기준 페이지 단위 파이프라인 |
| optimize | 전체 + 최적화 |

**단계**: prd, plan, dev, check, fix, lib, db, test, commit
**옵션**: --interactive (단계별 확인), --report (리포트)

## 3. 파이프라인 흐름

```
prd → plan → dev ←─────────┐
                ↓          │
        check → fix        │
                ↓          │
        lib → db → test ───┘ (실패 시 dev로, 최대 3회)
               ↑      ↓
     (oaisdb run)  commit
```

> **db 단계**: `oaisdb run` = validate(코드-DB) + 분석(무결성) + 수정

## 4. 단계별 조건

| 단계 | 완료 조건 |
|------|-----------|
| prd | PRD(d{SP}0001) 유효 |
| plan | d{SP}0002에 실행 가능 태스크 존재 |
| dev | **d{SP}0004 사전 검토** + Feature TDD 완료 (기준: oaisdev 2.1) |
| check | py_compile, pylint, mypy → d{SP}0004 등록 (스코프: 섹션 4.1 참조) |
| fix | d{SP}0004 현재 이슈=0 |
| lib | oais 모듈 이슈=0 |
| db | **oaisdb run** (validate + 분석 + 수정) → 이슈=0 |
| test | **oaistest run** 실행 → Part A~E 통과 (섹션 4.4 참조) |
| commit | 커밋 완료, d{SP}0010 동기화 |

> **db 단계 상세**: 코드-DB 정합성(EXPLAIN) + 무결성(integrity_check) + FK 검증 + 수정

### 4.1 check 단계 스코프

서브프로젝트(SP) 설정 시, **루트 + 하위 전체** 검사:

```
SP=02 (02_1st_server) 예시:
  02_1st_server/
  ├── *.py          ← [필수] 루트 .py 파일 (login.py, config.py 등)
  └── pages/*.py    ← [필수] 페이지 파일
```

**검사 명령어**:
```bash
# py_compile (전체)
uv run python -m py_compile 02_1st_server/*.py 02_1st_server/pages/*.py

# pylint (전체, E0602 undefined-variable 포함)
uv run pylint 02_1st_server/*.py 02_1st_server/pages/*.py --enable=E0602
```

> ⚠️ **주의**: pages/ 폴더만 검사하면 login.py 등 루트 파일의 런타임 에러를 놓침

### 4.2 dev 단계 d{SP}0004 사전 검토

dev 단계 시작 시 **d{SP}0004 현재 이슈**를 먼저 확인:

```
dev 단계 시작
    ↓
d{SP}0004 "현재 이슈" 섹션 읽기
    ↓
이슈 있음? → 이슈 목록 출력 + 처리 여부 확인
    ↓
이슈 없음 → Feature TDD 진행
```

**검토 내용**:
- 기존 등록된 버그/에러 확인
- 커스텀 TODO 항목 확인
- 우선순위 높은 이슈 먼저 처리 권고

> ⚠️ **주의**: d{SP}0004를 읽지 않으면 이미 알려진 버그를 무시하고 진행하게 됨

### 4.3 문서 등록 규칙 (단일 문서)

> **규칙**: 현재 SP의 todo 문서에만 등록/확인 (파일 없으면 자동 생성)

```
# context 미지정 (SP=00)
모든 단계에서 doc/d0004_todo.md 사용

# oaiscontext 02 설정 시
dev 단계:
  → doc/d20004_todo.md 현재 이슈 확인

check 단계:
  → 에러 발견 시 doc/d20004_todo.md 등록

fix 단계:
  → d20004 현재 이슈 = 0 확인

history 단계:
  → d20004 해결된 이슈 → d20010 아카이브
```

**적용 단계**: dev, check, fix, history

> 상세: `v/oaiscontext.md` 섹션 8 참조

### 4.4 test 단계: oaistest run 호출

> ⚠️ **필수**: test 단계에서 `oaistest run` 스킬을 호출하여 전체 테스트 실행

**oaistest run 실행 내용**:

| Part | 내용 | 검사 항목 |
|------|------|----------|
| Part A | 정적분석 | py_compile, pylint, 품질 |
| Part B | E2E/UI | Playwright 시나리오 |
| Part C | pytest | TDD 단위 테스트 |
| Part D | oais 모듈 | 453개 함수 검증 |
| Part E | 런타임 | test_page_import.py (필수) |

**테스트 단계 흐름**:
```
oaistest run 실행
    ↓
Part A~E 순차 실행
    ↓
실패 있음? → d{SP}0004 등록 → fix 단계로
    ↓
Part A~E 통과 → commit 단계로
```

**Part E (런타임 검증) 필수 이유**:
| 에러 유형 | 원인 | Part E로 감지 |
|----------|------|:-------------:|
| DuplicateElementKey | 동일 key 중복 | ✅ |
| ImportError (조건부) | if문 내 import | ✅ |
| AttributeError | 런타임 객체 접근 | ✅ |
| TypeError | 런타임 타입 불일치 | ✅ |

> **참조**: oaistest.md (Part A~E 상세), oaistest_guide.md (방법론)

## 5. 예시

```bash
oaisbatch run                        # 전체
oaisbatch run --from dev             # dev부터
oaisbatch run --from check --to test # 검증만
oaisbatch optimize                   # run + optimize
```

## 6. 서브에이전트

| 단계 | 에이전트 |
|------|----------|
| dev | task-executor, codebase-investigator |
| check | code-error-checker, python-code-reviewer |
| fix/lib/db | task-executor (lib: +python-code-reviewer) |
| test | **oaistest** (Part A~E 전체 실행) |

모든 단계 병렬 실행 지원.

## 7. 관련 스킬

oaisprd, oaisplan, oaisdev, oaischeck, oaisfix, oaislib, oaisdb, oaistest, oaiscommit

## 8. unitdev - 페이지 단위 파이프라인

### 8.1 개요

단위개발문서(d{SP}1{YY}0) 기준으로 **단일 페이지**에 대해 전체 파이프라인 실행.

```
oaisbatch unitdev d21700    # 7_70 페이지 대상 전체 파이프라인
oaisbatch unitdev d21710    # 7_71 페이지 대상 전체 파이프라인
```

### 8.2 문서번호-페이지 매핑

```
문서번호: d{SP}1{YY}0
         ↓
페이지ID: {X}_{YY}

예시:
  d21700 → SP=2, YY=70 → 7_70_앱프로토타입*.py
  d21710 → SP=2, YY=71 → 7_71_*.py
  d21100 → SP=2, YY=10 → 1_10_*.py
```

**페이지 카테고리 (X 값)**:
| YY 범위 | X | 카테고리 |
|---------|---|----------|
| 10-19 | 1 | 메인/로그인 |
| 20-29 | 2 | 서비스 A |
| 30-39 | 3 | 서비스 B |
| 70-79 | 7 | 앱프로토타입 |

### 8.3 단계별 스코프 제한

| 단계 | 전체 파이프라인 | unitdev 스코프 |
|------|----------------|----------------|
| prd | d{SP}0001 전체 | d{SP}0001 내 해당 페이지 섹션 |
| plan | d{SP}0002 전체 | d{SP}0002 내 해당 페이지 태스크 |
| dev | 모든 pages/*.py | {X}_{YY}_*.py만 |
| check | 서브프로젝트 전체 | {X}_{YY}_*.py만 |
| fix | d{SP}0004 전체 | 해당 페이지 관련 이슈만 |
| lib | oais 전체 | 해당 페이지가 import하는 모듈만 |
| db | DB 전체 | 해당 페이지가 사용하는 테이블만 |
| test | pytest 전체 | test_{YY}_*.py만 |
| commit | 전체 커밋 | 해당 페이지 파일만 커밋 |

### 8.4 실행 흐름

```
oaisbatch unitdev d21700
    ↓
1. 문서번호 파싱: d21700 → SP=02, YY=70
    ↓
2. 페이지ID 계산: 7_70
    ↓
3. 파일 패턴: 02_1st_server/pages/7_70_*.py
    ↓
4. 단위개발문서 로드: doc/d21700_*.md
    ↓
5. 파이프라인 실행 (스코프 제한 적용):
   prd(페이지섹션) → plan(페이지태스크) → dev(7_70_*.py)
        ↓
   check(7_70_*.py) → fix(페이지이슈) → lib(사용모듈)
        ↓
   db(사용테이블) → test(test_70_*.py) → commit(7_70_*)
```

### 8.5 옵션

```bash
oaisbatch unitdev d21700                    # 전체 실행
oaisbatch unitdev d21700 --from check       # check부터
oaisbatch unitdev d21700 --only dev,check   # dev, check만
oaisbatch unitdev d21700 --interactive      # 단계별 확인
oaisbatch unitdev d21700 --dry-run          # 실행 계획만 출력
```

### 8.6 출력 예시

```
=== oaisbatch unitdev d21700 ===

[매핑]
  문서번호: d21700
  페이지ID: 7_70
  파일패턴: 02_1st_server/pages/7_70_*.py
  대상파일: 7_70_앱프로토타입.py (1개)
  단위문서: doc/d21700_앱프로토타입_단위개발.md

[파이프라인]
  ✅ prd    - 5.2.2 앱프로토타입 섹션 확인
  ✅ plan   - Epic E07 태스크 확인
  🔄 dev    - 7_70_앱프로토타입.py 개발 중
  ⏳ check  - 대기 중
  ⏳ fix    - 대기 중
  ⏳ lib    - 대기 중
  ⏳ db     - 대기 중
  ⏳ test   - 대기 중
  ⏳ commit - 대기 중
```

### 8.7 주의사항

- **SP 자동 감지**: 문서번호에서 SP 추출 (d21700 → SP=02)
- **oaiscontext 무시**: unitdev는 문서번호로 SP 결정, 기존 컨텍스트 무시
- **단일 문서**: 해당 SP의 d{SP}0004만 처리 (섹션 4.3 참조)
- **단위문서 필수**: d{SP}1{YY}0_*.md 파일 없으면 에러
