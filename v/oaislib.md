# oaislib - oais 모듈 수정/최적화

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 공통: `v/guide/common_guide.md` | 컨텍스트: `v/oaiscontext.md`

## 1. 개요

oais 모듈 문제점 발견/수정 2단계 워크플로우.

- **컨텍스트**: `--sp N` 또는 `oaiscontext N`
- **에러/이슈**: d{SP}0004_todo.md | **신규 개발**: d{SP}0002_plan.md
- **워크플로우**: Phase 1(분석→d0004 기록) → Phase 2(수정→해결 이동)
- **완료**: d0004에 oais 미해결 이슈 0개

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaislib status` | 서브명령어 리스트, 상태/미해결 이슈 |
| `oaislib version` | 스킬 버전 정보 (v01) |
| `oaislib run` | Phase 1+2 (분석→수정→문서) |
| `oaislib optimize` | run + 최적화 |
| `oaislib doc` | d0005_lib.md 문서화만 |

옵션: `--module [name]`, `--dry-run`, `--interactive`, `--report`

---

## 3. 병렬 처리

### 3.1 아키텍처

```
메인 에이전트 (분석 + 조율 + 검증)
    ┌────┼────┬────┐
Agent1  Agent2  Agent3  Agent4
core    bizreg  기타    pages
```

### 3.2 역할 분배

| 에이전트 | 담당 | 역할 |
|---------|------|------|
| Agent 1 | __init__.py, config_helper.py | export/중복 |
| Agent 2 | bizreg.py, seal.py, ocr.py | 변수/멤버 |
| Agent 3 | oais 나머지 | 기타 이슈 |
| Agent 4 | 02_1st_server/pages/* | import |

### 3.3 서브에이전트 매핑

| 단계 | 에이전트 | 병렬 |
|------|---------|------|
| 분석 | Explore, python-code-reviewer | O |
| 수정 | task-executor | O |
| 최적화 | python-code-reviewer | O |
| 검증 | task-checker | - |
| 품질 | oaisqa | O |

### 3.4 병렬화 전략

| 이슈 | 병렬화 | 비고 |
|------|--------|------|
| E0611 (export) | 낮음 | __init__.py 먼저 |
| E0606 (미할당) | 높음 | 파일별 독립 |
| E1101 (멤버) | 높음 | 파일별 독립 |

### 3.5 False Positive

> `v/guide/debugging_guide.md` 섹션 4 참조

### 3.6 예상 시간

| 항목 | 순차 | 병렬 |
|------|------|------|
| Phase 1 | 5분 | 5분 |
| Phase 2 | 60분+ | 15-20분 |
| Phase 3 | 30분 | 10분 |
| **총계** | 100분+ | 40-45분 |

---

## 4. 워크플로우

### 4.1 run

**Phase 1**: pylint -E, py_compile 분석 → d0004 기록 → 병렬 계획
**Phase 2**: 병렬 수정 → py_compile 검증 → 결과 수집 → d0004 이동 → pytest

### 4.2 optimize

run + Phase 3: 중복/미사용/성능 분석 → [OPT] 등록 → 병렬 최적화 → d0005 반영

---

## 5. d0004 연동

### 이슈 범위

| 경로 | 포함 |
|------|------|
| oais/*.py, oais/**/*.py | O |
| 02_1st_server/* (oais import) | O |
| tests/test_oais*.py | O |

### ID 규칙

- 기존: A001, A002... | 신규: L prefix + [FIX]/[OPT]
- 예: `| L001 | 2026-01-02 | [FIX] oais/config.py - 중복 | 높음 | 대기 |`

---

## 6. 최적화 체크리스트

- **코드**: 중복제거, 미사용 import/함수 삭제, 타입힌트
- **성능**: 루프/메모리/I/O 최적화
- **구조**: 모듈분리, 순환의존성 제거

---

## 7. 완료 조건

### run

| 조건 | 검증 |
|------|------|
| 미해결 이슈 0개 | d{SP}0004 "현재 이슈" 확인 |
| 구문 오류 없음 | `uv run python -m py_compile oais/*.py` |
| 테스트 통과 | `uv run pytest tests/` |
| 문서 업데이트 | d0005, d{SP}0010 반영 |

### optimize

run 조건 + [OPT] 0개 + pytest 전체 통과

---

## 8. 관련 문서

| 문서 | 용도 |
|------|------|
| v/guide/debugging_guide.md | 디버깅 워크플로우 |
| doc/d{SP}0004_todo.md | TODO/이슈 |
| doc/d0005_lib.md | 라이브러리 |
| v/oaisdb.md, v/oaisbatch.md | 관련 스킬 |

## 9. 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/analyze.md` | 코드 분석 |
| `v/command/improve.md` | 코드 개선 |
