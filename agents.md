# agents.md - 프로젝트 에이전트 레퍼런스

## 문서이력관리

| 버전 | 날짜 | 변경내용 |
|------|------|----------|
| v01 | 2026-01-21 | 초기 작성 |

---

## 1. 에이전트 검색 경로

에이전트 사용 시 아래 경로 순서로 탐색:

| 우선순위 | 경로 | 설명 |
|---------|------|------|
| 1 | `v/agent/` | 프로젝트 소스 경로 (마스터) |
| 2 | `.claude/agents/` | Claude Code 런타임 경로 (동기화 대상) |
| 3 | `.gemini/agents/` | Gemini 런타임 경로 (동기화 대상) |

### 사용 규칙

- 에이전트 호출 시 위 경로에서 `[name].md` 파일 탐색
- 파일이 없으면 해당 에이전트 사용 불가
- 여러 경로에 있으면 우선순위 높은 것 사용

---

## 2. 에이전트 정의

### 2.1 개발/구현

| 에이전트 | 파일명 | 역할 | 도구 |
|---------|--------|------|------|
| task-executor | `task-executor.md` | 기능 구현, 버그 수정 | Write, Edit, Bash |
| task-checker | `task-checker.md` | 구현 검증, QA | Read, Bash, Task Master |
| frontend-developer | `frontend-developer.md` | React UI 개발 | Write, Edit, Bash |
| code-error-checker | `code-error-checker.md` | 에러 분석 | Read |

### 2.2 검증/테스트

| 에이전트 | 파일명 | 역할 | 도구 |
|---------|--------|------|------|
| python-code-reviewer | `python-code-reviewer.md` | Python 코드 리뷰 | Read, Sequential |
| oaisqa | `oaisqa.md` | 품질/중복 분석 | Grep, Read, Sequential |
| oais-web-test-orchestrator | `oais-web-test-orchestrator.md` | E2E 웹 테스트 | Playwright |
| streamlit-code-reviewer | `streamlit-code-reviewer.md` | Streamlit 코드 리뷰 | Read |

### 2.3 데이터/분석

| 에이전트 | 파일명 | 역할 | 도구 |
|---------|--------|------|------|
| data-analyst | `data-analyst.md` | 데이터 분석 | Python |
| data-engineer | `data-engineer.md` | 데이터 파이프라인 | Python, SQL |
| data-scientist | `data-scientist.md` | ML/통계 분석 | ML libraries |
| jupyter-specialist | `jupyter-specialist.md` | 노트북 개발 | Jupyter |

### 2.4 Streamlit

| 에이전트 | 파일명 | 역할 | 도구 |
|---------|--------|------|------|
| streamlit-page-planner | `streamlit-page-planner.md` | 페이지 계획 | Read, Sequential |
| streamlit-page-designer | `streamlit-page-designer.md` | 페이지 설계 | Read, Sequential |
| streamlit-implementer | `streamlit-implementer.md` | 페이지 구현 | Write, Edit |

### 2.5 특화

| 에이전트 | 파일명 | 역할 | 도구 |
|---------|--------|------|------|
| codebase_investigator | `codebase_investigator.md` | 코드베이스 심층 분석 | Serena, Sequential |
| ai-engineer | `ai-engineer.md` | AI/LLM 시스템 설계 | Context7, Sequential |
| academic-researcher | `academic-researcher.md` | 학술 연구 | WebSearch, Context7 |
| web-design-expert | `web-design-expert.md` | 웹 디자인 | Magic |
| oaiswebdesigner | `oaiswebdesigner.md` | OAIS 웹 디자인 | Magic |
| oaisppt-agent | `oaisppt-agent.md` | PPT 생성 | PPTX skill |

---

## 3. 위임 규칙

### 3.1 작업별 에이전트 매핑

| 작업 유형 | 에이전트 |
|----------|---------|
| 코드 탐색 | Explore (내장) |
| 코드 구현 | task-executor |
| Python 리뷰 | python-code-reviewer |
| 구현 검증 | task-checker |
| 품질 분석 | oaisqa |
| 웹 테스트 | oais-web-test-orchestrator |
| 데이터 분석 | data-analyst |
| 학술 연구 | academic-researcher |

### 3.2 위임 우선순위

1. **항상 위임**: Explore, task-executor
2. **적극 위임**: 리뷰, 분석, 테스트
3. **조율 필요**: oais-leader (다중 작업)

### 3.3 oais-leader 활성화 조건

- 파일 2개 이상 영향
- 리뷰 + 개선 동시 필요
- 다중 도메인 분석
- "종합", "comprehensive" 키워드

---

## 4. MCP 서버 통합

| MCP | 연관 에이전트 | 용도 |
|-----|-------------|------|
| Sequential | python-code-reviewer, oaisqa | 체계적 분석 |
| Context7 | ai-engineer, academic-researcher | 문서/패턴 검색 |
| Magic | frontend-developer, web-design-expert | UI 생성 |
| Playwright | oais-web-test-orchestrator | 브라우저 테스트 |
| Serena | codebase_investigator | 심볼 분석 |

---

## 5. 작업별 에이전트 체인

### 새 기능 구현
```
task-executor -> python-code-reviewer -> task-checker -> oaisqa
```

### 버그 수정
```
code-error-checker -> codebase_investigator -> task-executor -> python-code-reviewer
```

### 성능 최적화
```
python-code-reviewer -> task-executor -> oais-web-test-orchestrator
```

### UI 개발
```
frontend-developer -> web-design-expert -> oais-web-test-orchestrator
```

### 데이터 분석
```
data-analyst -> jupyter-specialist -> data-scientist
```

---

## 6. 운영 규칙

1. 한 번에 1개 에이전트만 활성화
2. 의존 작업은 순차 실행
3. 독립 작업은 병렬 가능
4. Task Master로 모든 작업 추적
5. 컨텍스트 절약 위해 서브에이전트 적극 활용
