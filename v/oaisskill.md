# oaisskill - 스킬 최적화 검증

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-25 | 초기 작성 |

---

> 공통: `v/guide/common_guide.md` | 에이전트 참조: `agents.md`

## 1. 개요

`v/oais*.md` 스킬 파일들이 서브에이전트 위임 및 명령어 활용을 최적화하고 있는지 검증/개선하는 스킬.

**검증 항목**:
1. `v/agent/` 서브에이전트 적절한 활용 여부
2. `v/command/` 명령어 적절한 활용 여부

---

## 2. 서브명령어

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `oaisskill status` | 서브명령어 목록, 스킬 현황, 최적화 요약 | - |
| `oaisskill version` | 스킬 버전 정보 (v01) | 터미널 |
| `oaisskill validate` | 현재 상황 검토 후 최적안 제안 | 개선 권장사항 |
| `oaisskill run` | 자동 최적화 수행 (1,2번 항목 적용) | 수정된 스킬 파일 |
| `oaisskill run [스킬명]` | 특정 스킬만 최적화 | 수정된 스킬 파일 |

---

## 3. 검증 기준

### 3.1 서브에이전트 위임 검증

**원칙**: 단일 에이전트 작업보다 멀티 에이전트 병렬 처리 우선

**검증 항목**:

| 체크 | 기준 | 권장 |
|------|------|------|
| 병렬 처리 | 독립 작업이 2개 이상인가? | `Task(run_in_background=true)` 활용 |
| 적절한 위임 | 작업 유형에 맞는 에이전트 사용? | 아래 매핑 테이블 참조 |
| 과도한 위임 | 단순 작업에 불필요한 위임? | 직접 처리 권장 |

**작업-에이전트 매핑**:

| 작업 유형 | 권장 에이전트 | 비고 |
|----------|-------------|------|
| 코드 구현/수정 | `task-executor` | 기능 구현, 버그 수정 |
| Python 리뷰 | `python-code-reviewer` | 품질/성능/버그 검토 |
| 구현 검증 | `task-checker` | 완료 작업 QA |
| 품질/중복 분석 | `oaisqa` | 중복 감지, 의존성 분석 |
| 에러 분석 | `code-error-checker` | 에러 메시지 분석 |
| E2E 웹 테스트 | `oais-web-test-orchestrator` | Playwright 테스트 |
| 데이터 분석 | `data-analyst` | 통계, 트렌드 |
| Streamlit 구현 | `streamlit-implementer` | UI 페이지 구현 |
| 웹 디자인 | `web-design-expert` | Bootstrap 기반 UI |
| 학술 연구 | `academic-researcher` | 논문/문헌 분석 |
| 번역 | `translator` | 다국어 번역 |
| PPT 생성 | `oaisppt-agent` | 프레젠테이션 |

### 3.2 명령어 활용 검증

**원칙**: `v/command/` 명령어로 표준화된 워크플로우 활용

**검증 항목**:

| 체크 | 기준 | 권장 |
|------|------|------|
| 명령어 활용 | 해당 작업에 맞는 명령어 존재? | 명령어 연동 추가 |
| 중복 구현 | 명령어로 대체 가능한 로직? | 명령어 호출로 변경 |
| 워크플로우 연결 | 연관 명령어 체인 정의? | 관련 명령어 참조 추가 |

**명령어 목록**:

| 명령어 | 용도 | 연관 스킬 |
|--------|------|----------|
| `analyze` | 코드 분석 | oaischeck, oaislib |
| `build` | 프로젝트 빌드 | oaisdev |
| `cleanup` | 정리/삭제 | oaisfix |
| `design` | 설계 | oaisprd, oaisplan |
| `document` | 문서화 | oaisdoc |
| `estimate` | 추정 | oaisplan |
| `explain` | 설명 | oaishelp |
| `git` | Git 작업 | oaiscommit |
| `implement` | 구현 | oaisdev |
| `improve` | 개선 | oaisfix |
| `load` | 로드 | oaiscontext |
| `spawn` | 멀티태스킹 | oaisbatch |
| `task` | 작업 관리 | oaisplan |
| `test` | 테스트 | oaischeck |
| `troubleshoot` | 트러블슈팅 | oaischeck, oaisfix |
| `workflow` | 워크플로우 | oaisbatch |

---

## 4. 워크플로우

### 4.1 validate 워크플로우

```
1. v/oais*.md 파일 목록 수집
   ↓
2. 각 스킬 파일 분석 (병렬)
   - 서브에이전트 사용 현황 추출
   - 명령어 참조 현황 추출
   ↓
3. 최적화 기회 식별
   - 위임 가능하나 직접 처리 중인 작업
   - 활용 가능하나 미사용 중인 명령어
   - 병렬화 가능하나 순차 처리 중인 작업
   ↓
4. 개선 권장사항 출력
```

### 4.2 run 워크플로우

```
1. validate 워크플로우 실행
   ↓
2. 개선 항목별 수정 계획 생성
   ↓
3. 스킬 파일 수정 (병렬)
   - 에이전트 위임 섹션 추가/수정
   - 명령어 연동 섹션 추가/수정
   - 워크플로우 병렬화 적용
   ↓
4. 수정 결과 검증
   ↓
5. 변경 사항 요약 출력
```

---

## 5. 분석 대상

**포함**: `v/oais*.md` (스킬 파일)

**분석 패턴**:

| 패턴 | 추출 정보 |
|------|----------|
| `에이전트:.*` | 현재 사용 중인 에이전트 |
| `Task\(.*subagent_type=` | Task 도구 에이전트 위임 |
| `run_in_background` | 병렬 처리 여부 |
| `v/command/.*\.md` | 명령어 참조 |
| `## 관련 스킬` | 스킬 간 연동 |

---

## 6. 출력 형식

### 6.1 validate 출력

```markdown
# oaisskill validate 결과

## 분석 대상: N개 스킬

## 에이전트 활용 현황

| 스킬 | 현재 에이전트 | 권장 추가 | 병렬화 |
|------|-------------|----------|--------|
| oaischeck | code-error-checker | oaisqa | O |
| oaisfix | task-executor | task-checker | O |

## 명령어 활용 현황

| 스킬 | 연동 명령어 | 권장 추가 |
|------|-----------|----------|
| oaischeck | analyze | test, troubleshoot |
| oaisdev | implement | build |

## 개선 권장사항

### oaischeck.md
1. [에이전트] `oaisqa` 에이전트 병렬 활용 권장
2. [명령어] `test` 명령어 연동 추가 권장

### oaisfix.md
1. [에이전트] 수정 후 `task-checker` 검증 위임 권장
```

### 6.2 run 출력

```markdown
# oaisskill run 결과

## 수정된 스킬: N개

| 스킬 | 변경 내용 |
|------|----------|
| oaischeck.md | 에이전트 병렬화, 명령어 연동 추가 |
| oaisfix.md | task-checker 검증 단계 추가 |

## 상세 변경 사항

### oaischeck.md
- [+] 에이전트: oaisqa (품질 분석 병렬 실행)
- [+] 명령어 연동: test, troubleshoot
- [~] 워크플로우: Task(run_in_background=true) 적용
```

---

## 7. 서브에이전트 활용

| 단계 | 에이전트 | 역할 | 병렬 |
|------|----------|------|:----:|
| 스킬 분석 | `Explore` | 파일 탐색, 패턴 추출 | O |
| 최적화 검토 | `oaisqa` | 중복/누락 분석 | O |
| 파일 수정 | `task-executor` | 스킬 파일 수정 | O |
| 검증 | `task-checker` | 수정 결과 검증 | - |

---

## 8. 관련 문서

| 문서 | 용도 |
|------|------|
| `agents.md` | 에이전트 검색 경로, 역할, 위임 규칙 |
| `v/agent/*.md` | 서브에이전트 정의 |
| `v/command/*.md` | 명령어 정의 |
| `v/guide/common_guide.md` | 에이전트 활용 원칙 |

---

## 9. 예시

### validate 실행

```bash
oaisskill validate
```

**출력**:
```
# oaisskill validate 결과

## 분석 대상: 22개 스킬

## 개선 권장사항

### oaischeck.md
- [에이전트] oaisqa 추가 권장 (품질 분석 병렬화)
- [명령어] test 연동 추가 권장

### oaisdb.md
- [에이전트] data-engineer 활용 권장 (DB 작업)
- [병렬화] 스키마 분석/데이터 검증 병렬 처리 권장
```

### run 실행

```bash
oaisskill run oaischeck
```

**출력**:
```
# oaisskill run 결과

## 수정된 스킬: 1개

### oaischeck.md
- [+] 에이전트 섹션에 oaisqa 추가
- [+] 명령어 연동 섹션에 test, troubleshoot 추가
- [~] 워크플로우에 병렬 처리 패턴 적용

완료: v/oaischeck.md 업데이트됨
```
