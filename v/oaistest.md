# oaistest - 통합 테스트 스킬

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v05 | 2026-01-25 | checklist 서브명령어 추가 (요구사항 품질 검증, speckit 통합) |
| v04 | 2026-01-05 | refresh 제거, run 시 Part D 재스캔 자동 선행 |
| v03 | 2026-01-05 | 정합성 수정: 에이전트 매핑 Part D/E 추가, 워크플로우 Part E 추가, 모듈 수 43개로 수정 |
| v02 | 2026-01-05 | 필수 테스트 유형 섹션 추가 (Part E: 런타임 검증) |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 참조: common_guide.md (에이전트) | oaiscontext.md (SP)

## 1. 개요

테스트 실행 스킬. 컨텍스트: `--sp N` 또는 `oaiscontext N`

**문서 역할 분리:**

| 스킬 | 역할 | 문서 |
|------|------|------|
| oaisdev | d{SP}0003 **생성** | 첫 실행 시 자동 생성 (INIT) |
| oaisdev | Part C **등록** | TDD RED 단계에서 TC 등록 |
| oaistest | 결과 **갱신** | 테스트 실행 후 상태 업데이트 |
| oaistest | Part D **재스캔** | `run` 실행 시 자동 선행 |

문서연계: 실패→d{SP}0004 | 개발→d{SP}0002 | 항목→d{SP}0003

## 2. 가이드

**통합 가이드**: `v/guide/oaistest_guide.md` (방법론 How)

| 파트 | 내용 |
|------|------|
| 공통 | 우선순위/상태/에러분류 |
| A | 정적분석, 용어체크 |
| B | E2E/UI, Playwright |
| C | pytest, TDD |
| D | oais 모듈 전체 검증 |
| **E** | **런타임 검증 (import 테스트)** ← 필수 |

## 3. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaistest version` | 스킬 버전 정보 (v05) |
| `status` | 서브명령어 리스트, 상태 요약 |
| `run` | 전체 테스트 (Part D 재스캔 자동 선행) |
| `run --unit` | Part C pytest |
| `run --e2e` | Part B 시나리오 |
| `run --module` | Part D oais 모듈 (재스캔 자동 선행) |
| `run --runtime` | Part E 런타임 검증 (import 테스트) |
| `run [ID]` | 특정 시나리오 |
| `run [P0-P3]` | 우선순위별 |
| `preview` | 계획 출력 |
| `checklist [domain]` | 요구사항 품질 체크리스트 생성 |

옵션: `--screenshot` `--fail-fast` `--verbose`

> **Note**: d{SP}0003 신규 생성은 `oaisdev run` 첫 실행에서 수행. Part D 재스캔은 `run` 시 자동 선행.

## 4. 에이전트 매핑

| 유형 | 에이전트 | 병렬 |
|------|----------|:----:|
| Part A 정적 | python-code-reviewer | O |
| Part A 품질 | oaisqa | O |
| Part B E2E | web-test-orchestrator | - |
| Part C 단위 | task-executor | - |
| Part D oais | task-executor | - |
| Part E 런타임 | task-executor | - |

병렬: A(reviewer+qa) | B설계(qa+Explore, run_in_background=true)

## 5. 워크플로우

### 5.1 전체 (run)
가이드→**Part D 재스캔**→Part A→B→C→D→E→d{SP}0003→d{SP}0004

### 5.2 단위 (--unit)
d{SP}0003 Part C→TC매칭→pytest→상태갱신

TC규칙: `TC[번호]_[모듈].py`

### 5.3 E2E (--e2e)
d{SP}0003 Part B→Playwright→상태갱신→스크린샷(tmp/test_screenshots/)

### 5.4 oais 모듈 (--module)

목적: oais 모듈 기능 전체 검증. 대상: oais/*.py 전체 함수

```
1. oais/*.py 재스캔 → d{SP}0003 Part D 목록 갱신
2. 모듈별 함수 추출 (11개 카테고리, 43개 모듈)
3. TC 존재 확인 → 실행 → 오류 발견
4. 실패 시 d{SP}0004에 MODULE_ERROR 등록
```

**카테고리:**
- Core (5): db, auth, session, admin, check_admin
- Config (2): base_config, config_helper
- Entity (5): user, company, agent, customer, community
- Task (5): task_core, task_query, task_attachment, task_mgmt, chuck_task
- Data (4): columns, sys_code, db_meta, data_processing
- Application (3): application, bizreg, bizreg_data
- File (5): file_ops, file_upload, file_manager, ocr, seal
- External (3): hyphen_api, news_api, services
- Document (4): pdf_parser, receipt_parser, card_processor, book_summary
- Utility (5): utils, date_utils, excel_utils, validation, financial
- UI (2): ui, mobile_css

테스트 패턴:
```python
def test_get_user_companies():
    result = get_user_companies("test_user")
    assert isinstance(result, pd.DataFrame)

def test_render_sidebar():
    result = render_sidebar()
    assert result is not None
```

커버리지: 전체 함수 80% | DB 함수 100% | 유틸리티 70%

### 5.5 런타임 검증 (Part E) - 필수

> ⚠️ **필수**: py_compile/pylint로 감지 불가능한 런타임 에러 검증

**목적**: 페이지 import 시 발생하는 런타임 에러 사전 감지

| 에러 유형 | 원인 | Part E 감지 |
|----------|------|:-----------:|
| StreamlitDuplicateElementKey | 위젯 key 중복 | ✅ |
| ImportError (조건부) | if문 내 import | ✅ |
| AttributeError | 런타임 객체 접근 | ✅ |
| TypeError | 런타임 타입 불일치 | ✅ |

**테스트 파일**:
```
tests/
├── test_page_import.py    ← [필수] Part E 런타임 검증
└── ...
```

**실행 명령어**:
```bash
oaistest run --runtime       # Part E만 실행
uv run pytest tests/test_page_import.py -v
```

**워크플로우**:
```
Part A~D 완료
    ↓
Part E: test_page_import.py 실행
    ↓
DuplicateKey 등 런타임 에러 감지
    ↓
실패 시 d{SP}0004에 등록
```

**test_page_import.py 핵심 기능**:
- Streamlit 모킹 (MockSessionState, MockContextManager)
- 위젯 key 중복 추적 (used_keys set)
- DB 연결 모킹 (순수 코드 검증)
- 모든 pages/*.py 동적 import

> 템플릿: `v/template/test_page_import_template.py`

### 5.6 checklist (요구사항 품질 검증)

> **핵심 개념**: 체크리스트는 "요구사항을 위한 유닛테스트" - 구현이 아닌 요구사항 자체의 품질 검증

**체크리스트 목적**:
- ❌ NOT: "버튼이 올바르게 클릭되는지 확인"
- ✅ YES: "클릭 동작에 대한 요구사항이 명확히 정의되어 있는가?"

**검증 차원**:

| 차원 | 검증 내용 |
|------|----------|
| 완전성 | 필요한 모든 요구사항이 문서화되었는가? |
| 명확성 | 요구사항이 구체적이고 모호하지 않은가? |
| 일관성 | 요구사항 간 충돌이 없는가? |
| 측정가능성 | 성공 기준이 객관적으로 검증 가능한가? |
| 커버리지 | 모든 흐름/케이스가 정의되었는가? |

**도메인별 체크리스트**:

| 도메인 | 파일명 | 주요 검증 항목 |
|--------|--------|---------------|
| ux | `ux.md` | 시각 계층, 상호작용 상태, 접근성 |
| api | `api.md` | 에러 응답, 인증, 버저닝 |
| performance | `performance.md` | 성능 지표, 부하 조건 |
| security | `security.md` | 인증/인가, 데이터 보호, 위협 모델 |

**체크리스트 항목 형식**:
```markdown
- [ ] CHK001 - [영역별] 요구사항 품질 질문? [품질차원, Spec §X.Y]
```

**올바른 예시**:
```markdown
- [ ] CHK001 - 시각 계층 요구사항이 측정 가능한 기준으로 정의되어 있는가? [명확성, Spec §FR-1]
- [ ] CHK002 - 모든 인터랙티브 요소에 대해 hover 상태 요구사항이 일관되게 정의되어 있는가? [일관성]
- [ ] CHK003 - 이미지 로드 실패 시 fallback 동작이 요구사항에 명시되어 있는가? [커버리지, Gap]
```

**잘못된 예시** (구현 검증):
```markdown
- [ ] 랜딩 페이지에 3개의 에피소드 카드가 표시되는지 확인  ← ❌
- [ ] hover 상태가 데스크톱에서 작동하는지 테스트  ← ❌
```

**워크플로우**:
```
oaistest checklist [domain]
    │
    ├─► 1. 문서 로드
    │      ├─ d{SP}0001_prd.md (요구사항)
    │      ├─ d{SP}0002_plan.md (기술 계획)
    │      └─ d{SP}0003_test.md (테스트 항목)
    │
    ├─► 2. 도메인 분석
    │      ├─ 키워드 추출 (auth, latency, UX 등)
    │      └─ 위험 지표 식별
    │
    ├─► 3. 체크리스트 생성
    │      ├─ doc/checklists/ 디렉토리 생성
    │      └─ [domain].md 파일 생성
    │
    └─► 4. 리포트 출력
           ├─ 생성 파일 경로
           ├─ 항목 수
           └─ 포커스 영역
```

**사용법**:
```bash
oaistest checklist ux           # UX 요구사항 품질 체크리스트
oaistest checklist api          # API 요구사항 품질 체크리스트
oaistest checklist security     # 보안 요구사항 품질 체크리스트
oaistest checklist              # 대화형으로 도메인 선택
```

## 6. 관련문서

oaistest_guide.md(통합가이드) | oaisdev.md(TDD) | oaischeck.md(Part A) | d{SP}0003(항목) | d{SP}0004(이슈)

## 7. 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/test.md` | 테스트 실행 |
| `v/command/analyze.md` | 코드 분석 |
