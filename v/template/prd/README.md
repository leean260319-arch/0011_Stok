# PRD 템플릿 가이드

> 프로젝트 유형별 PRD 템플릿 모음

## 템플릿 목록

| 템플릿 | 프로젝트 유형 | 용도 | 예시 |
|--------|-------------|------|------|
| `common_prd_template.md` | 공통/기본 | 범용 PRD 구조 | d0001_prd.md |
| `streamlit_prd_template.md` | Streamlit 웹 | 멀티페이지 웹 앱 | d20001_prd.md |
| `algorithm_prd_template.md` | 알고리즘/분석 | 연산/처리 로직 | d10001_prd.md |
| `agent_prd_template.md` | 에이전트/CLI | 자동화 도구 | - |

## 프로젝트 유형 선택 가이드

| 조건 | 권장 템플릿 |
|------|-----------|
| Streamlit 웹 서버 | `streamlit_prd_template.md` |
| 알고리즘/데이터 분석 | `algorithm_prd_template.md` |
| CLI 도구/에이전트 스킬 | `agent_prd_template.md` |
| 기타/범용 | `common_prd_template.md` |

## 템플릿 선택 규칙

### common_guide.md 프로젝트 유형 매핑

| 유형 | 설명 | PRD 템플릿 |
|------|------|-----------|
| Type A | 알고리즘 위주 (웹서버 없음) | `algorithm_prd_template.md` |
| Type B | 웹서버 포함 (다중 서브프로젝트) | `streamlit_prd_template.md` |
| Type C | 에이전트/CLI 도구 | `agent_prd_template.md` |

## 템플릿 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `{SP}` | 서브프로젝트 번호 (2자리) | 01, 02, 20 |
| `{서브프로젝트명}` | 폴더명 | 02_1st_server |
| `{YYYY-MM-DD}` | 날짜 | 2026-01-03 |

## 사용 방법

### oaisprd 스킬 사용

```bash
# 템플릿 목록 조회
oaisprd template

# 특정 유형 템플릿으로 PRD 생성
oaisprd run --template streamlit
oaisprd run --template algorithm
oaisprd run --template agent
```

### 수동 사용

1. 프로젝트 유형에 맞는 템플릿 선택
2. 템플릿 복사하여 `doc/d{SP}0001_prd.md` 생성
3. 변수 치환 및 내용 작성

## 관련 문서

- `v/oaisprd.md`: PRD 생성 스킬
- `v/guide/common_guide.md`: 프로젝트 유형 정의
