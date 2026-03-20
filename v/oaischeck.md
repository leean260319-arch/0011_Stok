# oaischeck - 코드 품질 체크

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-05 | 런타임 검증 섹션 추가 (import 테스트, DuplicateKey 감지) |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 참조: `v/guide/common_guide.md`, `v/guide/debugging_guide.md`, `v/oaiscontext.md`
> 결과: 에러→**`d0004` AND `d{SP}0004`** | 개발→`d{SP}0002_plan.md` | 이력→`d{SP}0010_history.md`

**옵션**: `--sp N` (서브프로젝트) | **에이전트**: `code-error-checker`, `python-code-reviewer`, `oais-qa`

## 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaischeck status` | 서브명령어 리스트, 체크 대상 현황, 최근 이슈 |
| `oaischeck version` | 스킬 버전 정보 (v02) |
| `oaischeck` / `oaischeck [대상]` | 전체 또는 특정 대상 체크 |
| `oaischeck oais` / `error` / `term` | oais모듈 / 에러 / 표준용어 체크 |
| `oaischeck debug [에러]` | 심층 디버깅 |
| `oaischeck circular [모듈]` | 순환 참조 감지 |

## 체크 대상

**포함**: `src/`, `oais/`, `tests/`, `04_app/`, 루트 `*.py` | **제외**: `data/`, `tmp/`, `db/`, `.git/`, `__pycache__/`, `node_modules/`

## 워크플로우

- **병렬 실행**: Task 도구 `run_in_background=true`
- **Serena MCP**: `find_symbol`, `get_symbols_overview`, `find_referencing_symbols`
- **검증**: `uv run python -m py_compile <file.py>` [필수] → `pylint && mypy`
- **분류**: `[CRITICAL]` 즉시 | `[ERROR]` 24h | `[WARNING]` 1주 | `[INFO]` 백로그

## 결과 기록

`d{SP}0004_todo.md`: `| ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |`
태그: `[ERR]` 에러 | `[SEC]` 보안 | `[OPT]` 최적화

### 병행 등록 규칙 (SP≠00)

> ⚠️ **필수**: SP≠00일 때 에러를 **d0004 AND d{SP}0004** 양쪽에 등록

```
예시: oaiscontext 02 설정 시

에러 발견:
  → doc/d0004_todo.md 에 등록 (공통)
  → doc/d20004_todo.md 에도 등록 (서브프로젝트)
```

> 상세: `v/oaiscontext.md` 섹션 8 참조

## 표준용어 검증

용어집: `v/template/oaischeck_standard_word.md`

## oais 모듈 검증

올바른: `oais.date_utils.get_date_range()` / 잘못된: `oais.get_date_range()`

## 순환 참조 감지

`[CRITICAL]` `__init__.py` 포함 | `[ERROR]` 직접순환 (A↔B) | `[WARNING]` 간접순환 (A→B→C→A)
해결: 함수 내부 import, TYPE_CHECKING 활용

## 런타임 검증 (oaischeck runtime)

> ⚠️ **필수**: py_compile/pylint로 감지 불가능한 런타임 에러를 잡기 위한 검증

### 정적 분석 vs 런타임 검증

| 검증 유형 | 도구 | 감지 가능 | 감지 불가능 |
|----------|------|----------|------------|
| 정적 분석 | py_compile, pylint, mypy | 구문 오류, 타입 힌트, 미정의 변수 | 런타임 초기화 에러 |
| 런타임 검증 | pytest import 테스트 | DuplicateKey, 조건부 ImportError, AttributeError | - |

### 런타임 에러 유형

| 에러 유형 | 원인 | 예시 |
|----------|------|------|
| StreamlitDuplicateElementKey | 동일 key 중복 사용 | `st.button("A", key="btn")` x2 |
| ImportError (조건부) | if문 내 import | `if flag: import module` |
| AttributeError | 런타임 객체 접근 | `st.session_state.undefined` |
| TypeError | 런타임 타입 불일치 | `func(expected_int)` with str |

### 필수 검증 명령어

```bash
# 1. 정적 분석 (기존)
uv run python -m py_compile <file.py>
uv run pylint <file.py>

# 2. 런타임 검증 (추가 필수)
uv run pytest tests/test_page_import.py -v
```

### 페이지 import 테스트 요구사항

```
tests/
├── conftest.py
├── test_page_import.py    ← [필수] 런타임 에러 감지
└── test_*.py
```

**test_page_import.py 역할**:
- 모든 pages/*.py 파일 import 테스트
- Streamlit 위젯 key 중복 감지 (MockSessionState + used_keys 추적)
- DB 연결 모킹으로 순수 코드 검증
- 런타임 초기화 에러 감지

> 템플릿: `v/template/test_page_import_template.py`

### 워크플로우

```
oaischeck 실행
    ↓
1. 정적 분석 (py_compile, pylint)
    ↓
2. 런타임 검증 (pytest test_page_import.py)
    ↓
에러 발견? → d{SP}0004 등록
    ↓
모두 통과 → 완료
```

---

## 디버깅 (`oaischeck debug`)

**체크포인트**: 에러라인 주변, 변수타입, 입력유효성, DB결과, NULL처리, 라이브러리버전
**Streamlit**: session_state 키, 위젯 key 중복, st.rerun() 무한루프
**프로세스**: 원인파악 → 최소변경 → 영향분석 → 수정 → 테스트

---

## 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/analyze.md` | 코드 분석 |
| `v/command/test.md` | 테스트 실행 |
| `v/command/troubleshoot.md` | 트러블슈팅 |
