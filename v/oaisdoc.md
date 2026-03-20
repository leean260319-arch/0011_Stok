# oaisdoc - 문서 생성 통합 가이드

> 공통 가이드라인: `v/guide/common_guide.md` 참조

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v03 | 2026-01-03 | d0007 섹션 8 스크립트 목록 규칙 추가 (v/script/*.py) |
| v02 | 2026-01-03 | validate 서브명령어 상세 추가 (스킬 정합성/파일 누락 검증) |
| v01 | 2026-01-02 | 최초 생성 |

---

## 1. 개요

d0001~d0010 핵심 문서 생성/업데이트 오케스트레이터.
d0007_command.md는 oaisdoc 직접 생성.

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisdoc status` | 서브명령어 리스트, 스킬/문서 현재 상태 |
| `oaisdoc version` | 스킬 버전 정보 (v03) |
| `oaisdoc run` | **d0001~d0010 문서 생성/업데이트 (기본)** |
| `oaisdoc run --doc [문서]` | 특정 문서만 업데이트 |
| `oaisdoc run --required-only` | 필수 문서만 업데이트 |
| `oaisdoc run --dry-run` | 드라이런 (실행 없이 계획만) |
| `oaisdoc create [문서ID]` | 특정 문서 생성 |
| `oaisdoc optimize` | **v/oais*.md 스킬 문서 최적화 (전체)** |
| `oaisdoc optimize [파일명]` | 특정 스킬 문서만 최적화 |
| `oaisdoc optimize --content` | 내용 최적화만 |
| `oaisdoc optimize --size` | 용량 최적화만 |
| `oaisdoc validate` | 품질 검증 (이력/필수섹션/참조/마크다운/스킬정합성) |
| `oaisdoc validate --fix` | 검증 + 자동 수정 |
| `oaisdoc validate --skill` | 스킬 정합성만 검증 (v/oais*.md 간 참조/파일 누락) |
| `oaisdoc validate --doc` | 문서만 검증 (doc/*.md) |

---

## 3. 문서-스킬 매핑

| doc/ 문서 | 용도 | 생성 방법 | 필수 |
|-----------|------|----------|:----:|
| d0001_prd.md | PRD | oaisprd run | O |
| d0002_plan.md | 개발 계획 | oaisplan run | O |
| d0003_test.md | 테스트 케이스 | oaistest run | O |
| d0004_todo.md | TODO/디버깅 | oaischeck | O |
| d0005_lib.md | 라이브러리 | oaislib run | - |
| d0006_db.md | DB 구조 | oaisdb run | - |
| d0007_command.md | 명령어 집계 | **oaisdoc 직접** | - |
| d0008_user.md | 사용자 가이드 | oaisuser run | - |
| d0010_history.md | 변경 이력 | oaishistory run | O |

---

## 4. 문서 생성 순서 및 의존성

### 4.1 Phase별 순서

| Phase | 문서 | 스킬 |
|-------|------|------|
| 1.기획 | d{SP}0001_prd, d{SP}0002_plan | oaisprd, oaisplan |
| 2.관리 | d{SP}0004_todo, d{SP}0010_history | oaischeck, oaishistory |
| 3.기술 | d0006_db, d0005_lib, d{SP}0003_test | oaisdb, oaislib, oaistest |
| 4.사용자 | d{SP}0008_user, d0007_command | oaisuser, oaisdoc 직접 |

### 4.2 의존 관계

- d{SP}0001_prd -> d{SP}0002_plan, d{SP}0003_test, d{SP}0008_user
- d{SP}0004_todo -> d{SP}0010_history
- d0006_db -> d{SP}0003_test

---

## 5. d0007_command.md 생성

### 5.1 스캔 대상

v/oais*.md, Claude Built-in, .claude/commands/, Plugin Skills, .mcp.json, **v/script/*.py**

### 5.2 필수 섹션 (섹션 7, 8)

| 섹션 | 내용 |
|------|------|
| 7.1 체크 항목 | 서브에이전트/병렬처리/optimize/status 확인 방법 |
| 7.2 기능 현황 | 스킬별 기능 지원 테이블 |
| 7.3 스킬별 사용에이전트 | 스킬별 에이전트 용도 상세 |
| 7.4 요약 | 기능별 지원 스킬 수 통계 |
| **8.1 스크립트 목록** | v/script/*.py 스크립트 역할 정리 |
| **8.2 스크립트 분류** | 스킬실행/PPT/검증유틸 카테고리별 분류 |

**7.3 테이블 형식**:
```markdown
| 스킬 | 에이전트 | 용도 | 비고 |
|------|----------|------|------|
| oaischeck | code-error-checker | 구문/타입 에러 | 1차 검사 |
| oaisfix | task-executor | 이슈별 수정 | 병렬 처리 |
```

**8.1 스크립트 테이블 형식**:
```markdown
| 스크립트 | 스킬 | 역할 |
|----------|------|------|
| oaischeck_run.py | oaischeck | 코드 품질 체크 실행 |
| oaisbatch_run.py | oaisbatch | 전체 파이프라인 배치 실행 |
```

**8.2 스크립트 분류**:
- **스킬 실행** (oais*_run.py): 스킬 서브명령어 구현
- **PPT 관련** (oaisppt_*.py, generate_*.py): PPTX 생성/변환
- **검증/유틸** (check_*, cleanup_*, verify_*): 코드 검증, 정리

---

## 6. 프로젝트 설정

### 6.1 새 프로젝트 초기화

```bash
mkdir -p doc v/{command,agent,template}
oaisprd create && oaisplan create && oaishistory create
oaischeck  # d0004_todo.md 자동 생성
```

### 6.2 정기 현행화

- **주간**: d{SP}0004_todo 정리, d{SP}0010_history 동기화
- **릴리스 전**: d{SP}0003_test 결과, d{SP}0008_user 확인, 전체 버전 업데이트

---

## 7. oaisdoc run 상세

### 7.1 실행 순서

1. d{SP}0004_todo (oaischeck)
2. d{SP}0010_history (oaishistory)
3. d0005_lib, d0006_db, d{SP}0003_test (병렬 가능)
4. d0007_command (oaisdoc 직접)
5. d{SP}0008_user, d{SP}0001_prd, d{SP}0002_plan

### 7.2 병렬 실행

독립적 스킬 병렬 호출:
- Phase 3: oaislib, oaisdb, oaistest
- Phase 4: oaisuser, oaisprd

```bash
uv run v/script/oaisdoc_run.py           # 전체
uv run v/script/oaisdoc_run.py --dry-run # 드라이런
```

---

## 8. oaisdoc optimize

### 8.1 개요

v/oais*.md 스킬 문서 최적화 (품질 + 용량)

| 유형 | 작업 |
|------|------|
| 내용 | 모호 표현 수정, 누락 보완, 일관성 확보 |
| 용량 | 중복 제거, 예제 축약, 템플릿->참조 변환 |

### 8.2 최적화 규칙

**삭제**: 템플릿 섹션, 반복 가이드, 과도한 예제, 이모지

**문체**: 경어체->단답형, 장황->핵심

**통합**: 공통 패턴 -> common_guide.md 참조

### 8.3 서브에이전트 병렬 최적화

19개 파일을 파일별 에이전트로 병렬 처리 (순차 대비 60-70% 시간 절감)

### 8.4 스크립트화 규칙

반복 출력 패턴은 스크립트로 분리하여 context 절약:
- 동일 형식 출력 2회 이상 반복 시 스크립트화
- `uv run v/script/oais[스킬]_run.py --json`

---

## 9. 문서 구조 표준

### 9.1 공통 헤더

`# [문서번호]_[문서명]` + 이력 테이블(버전/날짜/변경내용)

### 9.2 문서 번호 체계

| 범위 | 용도 |
|------|------|
| d0001~d0010 | 공통 핵심 문서 |
| d10000~d19999 | 서브프로젝트 01 |
| d20000~d29999 | 서브프로젝트 02 |
| d30000~d59999 | 예약 |

### 9.3 문서별 특화 섹션

| 문서 | 특화 섹션 |
|------|----------|
| d0001_prd | 요구사항, 우선순위, 마일스톤 |
| d0002_plan | 태스크, 상태, 담당자 |
| d0003_test | 케이스, 결과, 커버리지 |
| d0004_todo | 디버깅 (CRITICAL/ERROR/WARNING/INFO) |
| d0005_lib | 모듈, 함수, 예시 |
| d0006_db | ERD, 스키마, 관계 |
| d0007_command | 명령어, 사용법 |
| d0008_user | 설치, FAQ |
| d0010_history | 변경 이력 |

---

## 10. v/ 폴더 구조

### 10.1 스킬 파일 (20개)

oaisprd, oaisplan, oaistest, oaischeck, oaisfix, oaisdb, oaislib, oaisuser, oaishistory, oaisdoc, oaiscommit, oaisenv, oaisppt, oaisreport, **oaisdev**, **oaisbatch**, oaisstart, oaisstop, **oaiscontext**, **oaishelp**

> oaisstreamlit -> v/guide/streamlit_guide.md, oaisuv -> oaisenv 통합

### 10.2 가이드 파일 (v/guide/)

common_guide.md, streamlit_guide.md, debugging_guide.md, todo_format_standard.md

### 10.3 복사 항목

- **필수**: v/*.md, v/guide/, v/agent/, v/template/
- **선택**: .claude/ (SuperClaude)
- **제외**: doc/, data/, tmp/

---

## 11. 스킬 기능 매트릭스

### 11.1 체크 항목

| 항목 | 확인 방법 |
|------|----------|
| 서브에이전트 | `Task(subagent_type=` 패턴 |
| 병렬 처리 | `run_in_background` 패턴 |
| optimize | 서브명령어 테이블 확인 |
| status | 서브명령어 테이블에서 `status` 확인 |

### 11.2 기능 현황

| 스킬 | 서브에이전트 | 병렬 | optimize | status |
|------|:----------:|:---:|:--------:|:------:|
| oaischeck | O | O | - | O |
| oaisfix | O | O | - | O |
| oaislib | O | O | O | O |
| oaisdb | O | O | O | O |
| oaisdoc | O | O | O | O |
| oaistest | O | O | - | O |
| oaisprd | O | O | O | O |
| oaisplan | O | O | O | O |
| oaisuser | O | O | - | O |
| oaishistory | O | O | - | O |
| oaiscommit | O | O | - | O |
| oaisenv | O | O | - | O |
| oaisdev | O | O | O | O |
| oaisbatch | O | O | O | O |
| oaisstart | O | O | - | O |
| oaisstop | O | - | - | O |
| oaisppt | O | O | - | O |
| oaisreport | O | O | - | O |
| oaiscontext | - | - | - | O |
| oaishelp | - | - | - | O |

> oaisuv -> oaisenv 통합
> 모든 스킬 status 지원 (20/20)

---

## 12. 문제 해결

| 증상 | 확인 사항 |
|------|----------|
| 스킬 미발견 | v/ 폴더, 스킬 파일, CLAUDE.md 등록 |
| 문서 미생성 | doc/ 폴더, 쓰기 권한, create 명령 |
| 참조 오류 | 선행 문서, 문서 번호, 경로 |

---

## 13. 관련 문서

CLAUDE.md, .claude/, v/*.md, v/template/

## 16. 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/document.md` | 문서화 |
| `v/command/explain.md` | 설명 |

---

## 14. 주의사항

- Phase 순서 준수 권장
- 의존성 문서 먼저 생성
- 모든 변경 이력 기록
- 대규모 업데이트 전 백업
- --force 없으면 자동 백업
- 롤백: data/00_old/skill_backup/

---

## 15. oaisdoc validate 상세

### 15.1 개요

doc/*.md 및 v/oais*.md 품질 검증. 스킬 간 정합성과 관련 파일 누락을 검증.

```bash
oaisdoc validate              # 전체 검증
oaisdoc validate --skill      # 스킬 정합성만
oaisdoc validate --doc        # 문서만
oaisdoc validate --fix        # 검증 + 자동 수정
```

### 15.2 검증 항목

| 카테고리 | 검증 항목 | 설명 |
|----------|----------|------|
| 이력 | 이력 테이블 존재 | 문서 상단 버전/날짜/변경내용 |
| 이력 | 5개 이력 규칙 | common_guide.md 6.3 준수 |
| 필수섹션 | 문서별 필수 섹션 | PRD: 요구사항, Plan: 태스크 등 |
| 참조 | [[링크]] 유효성 | 참조 문서 존재 여부 |
| 마크다운 | 테이블/코드블록 | 깨진 형식 감지 |
| **스킬정합성** | 스킬 간 참조 | oais*.md 간 상호 참조 유효성 |
| **스킬정합성** | 관련 파일 누락 | agent/, script/, template/ 파일 |

### 15.3 스킬 정합성 검증 (--skill)

#### 15.3.1 스킬 간 참조 검증

```
검사 대상: v/oais*.md 내 참조 패턴

1. 스킬 참조: "oais[name]" 언급 → v/oais[name].md 존재 확인
2. 섹션 참조: "섹션 N.N 참조" → 해당 스킬 내 섹션 존재 확인
3. 관련 스킬: "관련 스킬" 목록 → 각 스킬 파일 존재 확인
```

**검증 예시**:
```
oaisbatch.md → "oaisdev 2.1 기준" 참조
  → v/oaisdev.md 존재? ✅
  → 섹션 2.1 존재? ✅

oaisdoc.md → "관련 스킬: oaisprd, oaisplan..."
  → v/oaisprd.md 존재? ✅
  → v/oaisplan.md 존재? ✅
```

#### 15.3.2 관련 파일 누락 검증

| 참조 유형 | 검색 패턴 | 검증 대상 |
|----------|----------|----------|
| 에이전트 | `v/agent/[name].md` | v/agent/ 폴더 내 파일 |
| 스크립트 | `v/script/[name].py` | v/script/ 폴더 내 파일 |
| 템플릿 | `v/template/[name]` | v/template/ 폴더 내 파일 |
| 가이드 | `v/guide/[name].md` | v/guide/ 폴더 내 파일 |

**검증 예시**:
```
oaisdoc.md → "uv run v/script/oaisdoc_run.py"
  → v/script/oaisdoc_run.py 존재? ❌ 누락

oaischeck.md → "v/agent/code-error-checker.md"
  → v/agent/code-error-checker.md 존재? ✅
```

#### 15.3.3 스킬 메타데이터 검증

| 항목 | 검증 내용 |
|------|----------|
| 버전 이력 | 문서 이력 관리 테이블 존재 |
| 서브명령어 | status 명령어 필수 (섹션 11.2 기준) |
| 개요 섹션 | 섹션 1. 개요 필수 |
| 관련 문서 | 관련 스킬/문서 섹션 존재 |

### 15.4 출력 형식

```
=== oaisdoc validate ===

[스킬 정합성] (21개 스킬)

v/oaisbatch.md
  ✅ 스킬 참조: oaisdev, oaischeck, oaisfix... (9개 유효)
  ✅ 에이전트: task-executor, code-error-checker (2개 유효)
  ⚠️ 스크립트: v/script/oaisbatch_run.py 누락
  ✅ 메타데이터: 이력/서브명령어/개요 정상

v/oaisdoc.md
  ✅ 스킬 참조: oaisprd, oaisplan... (10개 유효)
  ⚠️ 스크립트: v/script/oaisdoc_run.py 누락
  ✅ 메타데이터: 정상

[문서 검증] (10개 문서)
  ✅ d20001_prd.md: 이력/필수섹션/참조/마크다운 정상
  ✅ d20002_plan.md: 정상
  ...

[요약]
  스킬: 21개 검증, 2개 경고, 0개 에러
  문서: 10개 검증, 0개 경고, 0개 에러

  ⚠️ 누락 파일:
    - v/script/oaisbatch_run.py
    - v/script/oaisdoc_run.py
```

### 15.5 자동 수정 (--fix)

| 이슈 유형 | 자동 수정 |
|----------|----------|
| 이력 5개 초과 | 오래된 이력 삭제 |
| 이력 테이블 누락 | 템플릿 추가 |
| 깨진 참조 링크 | ~~삭제~~ → 리포트만 |
| 누락 파일 | ~~생성~~ → 리포트만 (수동 생성 권장) |

> **주의**: 스킬 참조 및 파일 누락은 자동 수정하지 않음. 리포트 후 수동 조치.

### 15.6 스킬 의존성 맵

```
oaisbatch (오케스트레이터)
  ├── oaisprd
  ├── oaisplan
  ├── oaisdev ←── oaischeck, oaisfix
  ├── oaischeck
  ├── oaisfix
  ├── oaislib
  ├── oaisdb
  ├── oaistest
  └── oaiscommit

oaisdoc (문서 오케스트레이터)
  ├── oaisprd, oaisplan
  ├── oaischeck, oaishistory
  ├── oaislib, oaisdb, oaistest
  └── oaisuser
```

### 15.7 사용 예시

```bash
# 전체 검증
oaisdoc validate

# 스킬 정합성만 (빠른 검증)
oaisdoc validate --skill

# 특정 스킬만
oaisdoc validate --skill oaisbatch

# 문서만 검증
oaisdoc validate --doc

# 검증 + 자동 수정
oaisdoc validate --fix
```
