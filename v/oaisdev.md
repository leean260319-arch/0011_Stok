# oaisdev - TDD 기반 개발 스킬

> 공통 가이드: `v/guide/common_guide.md` | 컨텍스트: `v/oaiscontext.md`

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v06 | 2026-01-09 | 병행 처리 규칙 삭제 → 단일 문서 처리 (oaiscontext 기준) |
| v05 | 2026-01-05 | VERIFY 단계 추가: import 테스트 의무화 (런타임 에러 감지) |
| v04 | 2026-01-03 | Part D 중복 방지: SP≠00일 때 d0003 참조 방식 |
| v03 | 2026-01-03 | oaiscontext 연동 명시 (d{SP}0003 생성) |
| v02 | 2026-01-03 | d0003_test.md 생성 기능 추가 (INIT 단계) |

---

## 1. 개요

oaisplan 태스크를 TDD 사이클(Red→Green→Refactor)로 구현. **첫 실행 시 테스트 문서 자동 생성.**

**옵션**: `--sp N` (서브프로젝트) | 가이드 자동 참조 (Streamlit→`streamlit_guide.md`)

| 스킬 | 역할 | 문서 |
|------|------|------|
| oaisplan | 설계 | d{SP}0002_plan.md |
| oaisdev | 구현 + **테스트 문서** | d{SP}0002_plan.md, **d{SP}0003_test.md** |
| oaisfix | 수정 | d{SP}0004_todo.md |

> **단일 문서**: 현재 SP의 `d{SP}0004` 사전 검토 (`v/oaiscontext.md` 섹션 8)

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisdev status` | 서브명령어 리스트, 진행 상태 |
| `oaisdev version` | 스킬 버전 정보 (v06) |
| `oaisdev run` | 미완료 Feature 전체 구현 |
| `oaisdev run [ID]` | 특정 Feature 구현 (F002-1 등) |
| `oaisdev queue` | 대기 큐 처리 |
| `oaisdev optimize` | 코드 최적화 |

**옵션**: `--max-iterations N`, `--timeout M`, `--interactive`, `--skip-refactor`

**개발 대상 조건** (d{SP}0002_plan.md 참조):
1. Task까지 세분화 완료 (Task 없으면 TC 매핑 불가 → TDD 불가)
2. 상태가 `완료`가 아님
3. PRD 5.1 페이지 개요에서 `진행=예`인 페이지만 (아니오는 제외)

---

## 3. 서브에이전트

| 단계 | 에이전트 | 병렬 |
|------|----------|:----:|
| 분석 | `codebase-investigator`, `Explore` | O |
| RED/GREEN | `task-executor` | - |
| REFACTOR | `python-code-reviewer`, `oaisqa` | O |
| 검증 | `task-checker` | - |
| 에스컬레이션 | `codebase-investigator` | - |

---

## 4. TDD 사이클

| 단계 | 작업 | 산출물 |
|------|------|--------|
| INIT | 테스트 문서 생성 | d{SP}0003_test.md (첫 실행 시) |
| RED | 실패 테스트 작성 | d{SP}0003 Part C 등록 |
| GREEN | 최소 구현 | 테스트 통과 |
| REFACTOR | 품질 개선 | lint 통과 |
| **VERIFY** | **런타임 검증** | **import 테스트 통과** |
| COMPLETE | 문서 갱신 | d{SP}0003 [x] |

### 네이밍 규칙

| 레벨 | 형식 | 예시 |
|------|------|------|
| Epic | `E{순번}` | E002 |
| Feature | `F{Epic}-{순번}` | F002-1 |
| Task | `F{Epic}-{Feature}.{순번}` | F002-1.1 |
| TC | `TC{Epic}-{Feature}.{Task}` | TC002-1.1 |

**Task ↔ TC 1:1 매핑**: `F002-1.1` → `TC002-1.1_보건복지부탭.py`

### 4.1 테스트 문서 생성 (INIT)

**첫 실행 시 d{SP}0003 존재 여부 확인 → 없으면 자동 생성**

> **컨텍스트 적용**: `oaiscontext.md` 규칙에 따라 `d{SP}0003_test.md` 생성
> - SP=00: `d0003_test.md` (PRD: `d0001_prd.md`)
> - SP=02: `d20003_test.md` (PRD: `d20001_prd.md`)

```
oaisdev run (첫 실행)
    ↓
d{SP}0003_test.md 존재? → 없음: 자동 생성
    ↓
d{SP}0001_prd.md 읽기 → Part B 시나리오 도출
    ↓
oais/*.py 스캔 → Part D 모듈 목록 생성
    ↓
TDD 사이클 시작 (RED → GREEN → REFACTOR)
```

**Part별 생성 규칙:**

| Part | 생성 방법 | 갱신 시점 |
|------|----------|----------|
| A | 공통 에러체크 (고정) | - |
| B | PRD 기능 → 시나리오 도출 | PRD 변경 시 |
| C | TDD RED 단계에서 등록 | 개발 진행 시 |
| D | SP별 분기 (아래 참조) | `oaistest refresh` |

**Part D 생성 규칙 (중복 방지):**

| SP | Part D 처리 |
|:--:|------------|
| 00 | oais 모듈 스캔하여 직접 생성 |
| ≠00 | `"d0003_test.md Part D 참조"` 링크만 추가 |

> **이유**: oais 모듈은 공통이므로 d0003에만 관리, 중복 방지

**Part B 시나리오 도출:**

| PRD 우선순위 | 시나리오 우선순위 |
|-------------|------------------|
| Must | P0 |
| Should | P1 |
| Could | P2 |
| Won't | 제외 |

**Part D oais 모듈 스캔:**
```bash
Grep: "^def [a-z]" in oais/*.py
```
10개 카테고리: Core, Entity, Task, Data, Application, File, External, Document, Utility, UI

**템플릿**: `v/template/test/common_test_template.md`

### 4.2 런타임 검증 (VERIFY) - 필수

> ⚠️ **필수**: REFACTOR 완료 후, COMPLETE 전에 반드시 실행

**목적**: py_compile/pylint로 감지 불가능한 런타임 에러 사전 감지

**워크플로우**:
```
REFACTOR 완료
    ↓
VERIFY: import 테스트 실행
    ↓
uv run pytest tests/test_page_import.py -v
    ↓
실패? → GREEN으로 돌아가 수정
    ↓
통과 → COMPLETE 진행
```

**감지 대상 에러**:

| 에러 유형 | 원인 | 예시 |
|----------|------|------|
| StreamlitDuplicateElementKey | 동일 key 중복 | `st.button("A", key="btn")` x2 (탭/루프 내) |
| ImportError (조건부) | if문 내 import | `if flag: import module` |
| AttributeError | 런타임 객체 접근 | `st.session_state.undefined` |
| TypeError | 런타임 타입 불일치 | 함수에 잘못된 타입 전달 |

**Streamlit 페이지 개발 시 주의사항**:

1. **탭/루프 내 위젯 key**:
   ```python
   # ❌ 잘못된 예 (DuplicateKey 발생)
   for item in items:
       st.button("Click", key="btn")

   # ✅ 올바른 예
   for i, item in enumerate(items):
       st.button("Click", key=f"btn_{i}")
   ```

2. **다중 탭 위젯 key**:
   ```python
   # ❌ 잘못된 예 (탭 간 key 충돌)
   with tab1:
       st.button("Submit", key="submit")
   with tab2:
       st.button("Submit", key="submit")

   # ✅ 올바른 예
   with tab1:
       st.button("Submit", key="tab1_submit")
   with tab2:
       st.button("Submit", key="tab2_submit")
   ```

**test_page_import.py 요구사항**:
- 모든 pages/*.py import 테스트
- Streamlit 모킹 (위젯 key 중복 추적)
- DB 연결 모킹 (순수 코드 검증)

> 템플릿: `v/template/test_page_import_template.py`

---

## 5. 반복/에스컬레이션

- **반복 제한**: `--max-iterations` (기본 10)
- **에스컬레이션**: 반복 초과, 모호한 요구사항, 환경 문제 시

---

## 6. optimize

```bash
oaisdev optimize              # 전체
oaisdev optimize [파일]       # 특정 파일
oaisdev optimize --dry-run    # 분석만
```

---

## 7. 워크플로우

`oaisplan → oaisdev run → oaisbatch run`

---

## 8. 관련 문서

- `oaisplan.md`: 설계
- `oaistest.md`: 테스트 실행
- `oaischeck.md`: 코드 체크
- `d{SP}0002_plan.md`: 구현 계획
- `d{SP}0003_test.md`: 테스트 케이스 (본 스킬에서 생성)
- `d{SP}0004_todo.md`: 이슈
- `v/template/test/`: 테스트 문서 템플릿

## 9. 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/implement.md` | 기능 구현 |
| `v/command/build.md` | 프로젝트 빌드 |
| `v/command/test.md` | 테스트 실행 |
