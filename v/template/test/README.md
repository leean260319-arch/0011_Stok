# 테스트 문서 템플릿

## 개요

`d*003_test.md` 문서 생성용 템플릿.

## 템플릿 목록

| 템플릿 | 용도 |
|--------|------|
| `common_test_template.md` | 범용 테스트 문서 |

## 플레이스홀더

| 변수 | 설명 | 예시 |
|------|------|------|
| `{SP}` | 서브프로젝트 번호 | 0, 20 |
| `{프로젝트명}` | 프로젝트 이름 | 시니어포탈 |
| `{서브프로젝트명}` | 서브프로젝트 이름 | 02_1st_server |
| `{날짜}` | 생성 날짜 | 2026-01-03 |

## 생성 워크플로우

> **컨텍스트 적용**: `oaiscontext.md` 규칙에 따라 SP별 문서 생성

```
oaisprd run (신규)
    ↓
d{SP}0001_prd.md 생성
    ↓
oaisdev run (첫 실행)
    ↓
d{SP}0003_test.md 존재? → 없음: 템플릿 기반 생성
    - Part A: 공통 에러체크 (고정)
    - Part B: PRD 기능에서 시나리오 도출
    - Part C: 빈 테이블 (TDD RED에서 등록)
    - Part D: oais 모듈 스캔하여 자동 생성
    ↓
TDD 사이클 시작
```

**예시:**
- SP=00: `d0003_test.md` ← `d0001_prd.md`
- SP=02: `d20003_test.md` ← `d20001_prd.md`

## 자동 생성 규칙

### Part B (시나리오)

PRD의 기능 요구사항에서 도출:

| PRD 우선순위 | 시나리오 우선순위 |
|-------------|------------------|
| Must | P0 |
| Should | P1 |
| Could | P2 |
| Won't | 제외 |

### Part D (oais 모듈)

```bash
# oais 모듈 스캔
Grep pattern: "^def [a-z]" in oais/*.py
```

10개 카테고리로 자동 분류:
- Core, Entity, Task, Data, Application
- File, External, Document, Utility, UI

## 관련 스킬

- `oaisprd`: PRD 생성
- `oaisdev`: 테스트 문서 생성 (INIT) + Part C 등록 (TDD)
- `oaistest`: 테스트 실행 및 결과 갱신, Part D 재스캔 (refresh)
