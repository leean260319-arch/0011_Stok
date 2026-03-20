# d0007_command.md - 명령어/스킬 통합 집계

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v2.2 | 2026-01-07 | oaissync diff/merge 서브명령어 추가 |
| v2.1 | 2026-01-06 | oaistodo 스킬 추가 (oaisaddtodo → oaistodo 변경) |
| v2.0 | 2026-01-06 | Claude Code 통합 집계 추가 (oaiscommand run) |
| v1.0 | 2024-12-31 | 자동 생성됨 |

---

## 1. 개요

이 문서는 프로젝트에서 사용 가능한 모든 명령어, 스킬, 플러그인을 집계합니다.

**자동 갱신**: `oaiscommand run` 실행 시 자동 갱신
**마지막 갱신**: 2026-01-06 18:13:20

### 1.1 통계 요약

| 카테고리 | 개수 |
|----------|------|
| OAIS 스킬 명령어 | 145 |
| Claude Built-in 명령어 | 18 |
| Project Skills | 25 |
| Plugin Skills | 26 |
| MCP Servers | 3 |
| **총계** | **217** |

### 1.2 명령어 표기법

모든 OAIS 스킬 명령어는 **스킬명 접두사**를 포함합니다.

| 형식 | 예시 | 설명 |
|------|------|------|
| `스킬명 서브명령` | `oaistest run` | 기본 형식 |
| `스킬명 서브명령 [인자]` | `oaissync view [project]` | 인자 포함 |
| `스킬명 서브명령 --옵션` | `oaistest run --unit` | 옵션 포함 |

> 상세: `v/oaiscommand.md` 참조

---

## 2. Claude Code Built-in 명령어

기본 제공되는 슬래시 명령어입니다.

| 명령어 | 설명 |
|--------|------|
| `/help` | 도움말 표시 |
| `/clear` | 대화 기록 초기화 |
| `/compact` | 대화 컴팩트 모드 |
| `/config` | 설정 관리 |
| `/cost` | 토큰 사용량/비용 확인 |
| `/doctor` | 환경 진단 |
| `/init` | 프로젝트 초기화 |
| `/login` | 로그인 |
| `/logout` | 로그아웃 |
| `/mcp` | MCP 서버 관리 |
| `/memory` | 메모리/컨텍스트 관리 |
| `/model` | 모델 선택 |
| `/permissions` | 권한 설정 |
| `/pr-comments` | PR 코멘트 확인 |
| `/review` | 코드 리뷰 |
| `/status` | 상태 확인 |
| `/terminal-setup` | 터미널 설정 |
| `/vim` | Vim 모드 토글 |

---

## 3. OAIS 스킬 명령어

`v/oais*.md`에서 정의된 프로젝트 전용 스킬입니다.

### 3.1 요약

| 스킬 | 기본 명령어 | 주요 용도 |
|------|------------|----------|
| oaischeck | `oaischeck status` | 기능 모음 |
| oaiscommand | `oaiscommand run` | 전체 명령어 집계 및 문서화 (기본) |
| oaiscommit | `oaiscommit run` | **커밋 + 이력 정리 통합 (기본)** - `--dry-run` 권장 |
| oaiscontext | `oaiscontext` | 현재 컨텍스트 확인 |
| oaisdb | `oaisdb run` | **validate + 분석 + 수정** (3-Phase 통합) |
| oaisdev | `oaisdev run` | 미완료 Feature 전체 구현 |
| oaisdoc | `oaisdoc run` | **d0001~d0010 문서 생성/업데이트 (기본)** |
| oaisenv | `oaisenv run` | 통합 점검 (플러그인+UV+정합성) |
| oaisfix | `oaisfix run` | **이슈 자동 수정 (병렬)** |
| oaishelp | `oaishelp` | d0007_command.md 전체 표시 |
| oaislib | `oaislib run` | Phase 1+2 (분석→수정→문서) |
| oaispaper | `oaispaper run` | 서머리 기반 분석 → d0100_서베이.md 생성 |
| oaisplan | `oaisplan run` | PRD → Task까지 완전 생성 (`run task`와 동일) |
| oaisppt | `oaisppt status` | 기능 모음 |
| oaisprd | `oaisprd run` | PRD 생성/정합성 검증 |
| oaisreport | `oaisreport run` | 신규 리포트 생성 |
| oaisstart | `oaisstart run` | 세션 시작 실행 (기본) |
| oaisstop | `oaisstop run` | **2단계 종료 실행 (기본)** |
| oaissync | `oaissync list` | 기능 모음 |
| oaistest | `oaistest run` | 전체 테스트 (Part D 재스캔 자동 선행) |
| oaistodo | `oaistodo` | **대기 중 업무 자동 처리** |
| oaisuser | `oaisuser run` | 신규 생성 |

### 3.2 상세

#### oaischeck

| 명령어 | 설명 |
|--------|------|
| `oaischeck status` | 서브명령어 리스트, 체크 대상 현황, 최근 이슈 |
| `oaischeck / oaischeck [대상]` | 전체 또는 특정 대상 체크 |
| `oaischeck oais / error / term` | oais모듈 / 에러 / 표준용어 체크 |
| `oaischeck debug [에러]` | 심층 디버깅 |
| `oaischeck circular [모듈]` | 순환 참조 감지 |

#### oaiscommand

| 명령어 | 설명 |
|--------|------|
| `oaiscommand status` | 서브명령어 리스트, 현재 상태 |
| `oaiscommand run` | 전체 명령어 집계 및 문서화 (기본) |
| `oaiscommand update` | d0007_command.md 업데이트 |
| `oaiscommand list` | v/command/ 명령어 목록 조회 |
| `oaiscommand compare` | 외부 소스와 비교 (sc/) |
| `oaiscommand sync` | 외부 소스 변경사항 동기화 |

#### oaiscommit

| 명령어 | 설명 |
|--------|------|
| `oaiscommit run` | **커밋 + 이력 정리 통합 (기본)** - `--dry-run` 권장 |
| `oaiscommit commit` | Git 커밋만 |
| `oaiscommit sync` | 이력 정리만 (d{SP}0004 → d{SP}0010) |
| `oaiscommit status / preview` | 서브명령어 리스트, 상태/변경사항 |

#### oaiscontext

| 명령어 | 설명 |
|--------|------|
| `oaiscontext` | 현재 컨텍스트 확인 |
| `oaiscontext [N]` | SP N으로 설정 (00~05) |
| `oaiscontext clear` | 공통(00) 초기화 |
| `oaiscontext list` | SP 목록 표시 |

#### oaisdb

| 명령어 | 설명 |
|--------|------|
| `oaisdb status` | 서브명령어 리스트, DB 상태/미해결 이슈 |
| `oaisdb run` | **validate + 분석 + 수정** (3-Phase 통합) |
| `oaisdb validate` | SQL 쿼리 스키마 검증만 (EXPLAIN) |
| `oaisdb optimize` | run + 최적화 |
| `oaisdb doc` | d0006_db.md 문서화 |
| `oaisdb design` | **DB 설계**: PRD/Plan 기반 테이블/컬럼 설계 → d{SP}0006_db.md |
| `oaisdb dev` | **DB 개발**: 설계된 스키마 마이그레이션 (백업 필수) |

#### oaisdev

| 명령어 | 설명 |
|--------|------|
| `oaisdev status` | 서브명령어 리스트, 진행 상태 |
| `oaisdev run` | 미완료 Feature 전체 구현 |
| `oaisdev run [ID]` | 특정 Feature 구현 (F002-1 등) |
| `oaisdev queue` | 대기 큐 처리 |
| `oaisdev optimize` | 코드 최적화 |

#### oaisdoc

| 명령어 | 설명 |
|--------|------|
| `oaisdoc status` | 서브명령어 리스트, 스킬/문서 현재 상태 |
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

#### oaisenv

| 명령어 | 설명 |
|--------|------|
| `oaisenv status` | 서브명령어 리스트, 상태 요약 |
| `oaisenv run` | 통합 점검 (플러그인+UV+정합성) |
| `oaisenv run --fix` | 통합 점검 + 자동 수정 |
| `oaisenv run --verbose` | 상세 출력 |
| `oaisenv plugin` | 플러그인 상태 확인 |
| `oaisenv validate` | 스킬 정합성 검증 |
| `oaisenv validate --full` | oais*.md 스킬 스캔 → 에이전트/커맨드/MCP 참조 검증 |
| `oaisenv agent` | 에이전트 경로 검증 |
| `oaisenv structure` | 문서 구조 검증 |
| `oaisenv reflect` | 설정 파일 반영 검증 |
| `oaisenv command` | v/command/ 연동 검증 |
| `oaisenv sync-agents` | 에이전트 폴더 동기화 |
| `oaisenv sync-skills` | 스킬 폴더 동기화 |
| `oaisenv install` | 누락 환경 요소 설치 |
| `oaisenv uv check` | UV 의존성 상태 체크 |
| `oaisenv uv update` | UV 의존성 업데이트 |

#### oaisfix

| 명령어 | 설명 |
|--------|------|
| `oaisfix status` | 서브명령어 리스트, 이슈 상태 |
| `oaisfix run` | **이슈 자동 수정 (병렬)** |
| `oaisfix run [대상]` | 특정 이슈/파일/카테고리 |
| `oaisfix preview` | 수정 미리보기 |
| `oaisfix test` | 테스트 실행 |
| `oaisfix verify` | 수정 검증 |
| `oaisfix rollback` | 롤백 |

#### oaishelp

| 명령어 | 설명 |
|--------|------|
| `oaishelp` | d0007_command.md 전체 표시 |
| `oaishelp [섹션]` | 특정 섹션만 표시 (예: oais, claude, plugin) |
| `oaishelp [스킬명]` | 특정 스킬 상세 (해당 v/oais*.md 참조) |

#### oaislib

| 명령어 | 설명 |
|--------|------|
| `oaislib status` | 서브명령어 리스트, 상태/미해결 이슈 |
| `oaislib run` | Phase 1+2 (분석→수정→문서) |
| `oaislib optimize` | run + 최적화 |
| `oaislib doc` | d0005_lib.md 문서화만 |

#### oaispaper

| 명령어 | 설명 |
|--------|------|
| `oaispaper status` | paper 폴더 현황, d0100 상태, 미분석 논문 |
| `oaispaper list` | 분석 대상 논문 목록 (서머리 유무 구분) |
| `oaispaper run` | 서머리 기반 분석 → d0100_서베이.md 생성 |
| `oaispaper deeprun` | PDF 포함 정밀 분석 → d0100_서베이.md 생성 |
| `oaispaper compare` | 논문 간 비교 분석 (모델, 성능, 방법론) |
| `oaispaper cite` | 인용 형식 생성 (APA, IEEE, BibTeX) |
| `oaispaper add [폴더]` | 새 논문 추가 분석 → 기존 d0100에 병합 |
| `oaispaper --topic` | 연구 주제 오버라이드 |
| `oaispaper --keywords` | 키워드 오버라이드 (콤마 구분) |
| `oaispaper --threshold` | 관련성 임계값 (기본 2) |
| `oaispaper --dry-run` | 실행 없이 계획만 출력 |
| `oaispaper --verbose` | 상세 로그 출력 |

#### oaisplan

| 명령어 | 설명 |
|--------|------|
| `oaisplan status` | 서브명령어 리스트, 상태 요약 |
| `oaisplan run` | PRD → Task까지 완전 생성 (`run task`와 동일) |
| `oaisplan run epic` | PRD → Epic까지 생성 |
| `oaisplan run feature` | PRD → Feature까지 생성 |
| `oaisplan run task` | PRD → Task까지 생성 (기본값) |
| `oaisplan detail` | 실행 전 상세 설계 (→oaisdev) |
| `oaisplan optimize` | 현재 Plan 검토 및 개선 |
| `oaisplan sync` | PRD 변경사항 동기화 |

#### oaisppt

| 명령어 | 설명 |
|--------|------|
| `oaisppt status` | 서브명령어 리스트, 상태 요약 |
| `oaisppt run [경로]` | PPTX 생성 |
| `oaisppt preview` | 미리보기 |

#### oaisprd

| 명령어 | 설명 |
|--------|------|
| `oaisprd status` | 서브명령어 리스트, 상태 요약 |
| `oaisprd run` | PRD 생성/정합성 검증 |
| `oaisprd run --template [type]` | 템플릿 지정 생성 |
| `oaisprd optimize` | PRD 최적화 |
| `oaisprd template` | 템플릿 목록 조회 |
| `oaisprd template [type]` | 특정 템플릿 조회 |
| `oaisprd validate` | 구조 검증 |
| `oaisprd section [N]` | 특정 섹션 갱신 |
| `oaisprd unitdev` | 전체 단위개발문서 현행화 |
| `oaisprd unitdev [문서명]` | 특정 단위개발문서 현행화 |

#### oaisreport

| 명령어 | 설명 |
|--------|------|
| `oaisreport status` | 서브명령어 리스트, 스킬/문서 상태 |
| `oaisreport run` | 신규 리포트 생성 |
| `oaisreport update` | 기존 리포트 업데이트 |
| `oaisreport list` | 리포트 목록 조회 |
| `oaisreport word` | Word 문서(.docx) 생성 (document-skills:docx 활용) |
| `oaisreport quotation` | 견적서 마크다운 → 워드 변환 (quotation_docx.js 템플릿) |

#### oaisstart

| 명령어 | 설명 |
|--------|------|
| `oaisstart status` | 서브명령어 리스트, 스킬/문서 상태 |
| `oaisstart run` | 세션 시작 실행 (기본) |

#### oaisstop

| 명령어 | 설명 |
|--------|------|
| `oaisstop status` | 서브명령어 리스트, 현재 상태 |
| `oaisstop run` | **2단계 종료 실행 (기본)** |
| `oaisstop readme` | README.md만 (1단계) |
| `oaisstop sync` | doc/*.md만 (2단계) |

#### oaissync

| 명령어 | 설명 |
|--------|------|
| `oaissync status` | 서브명령어 리스트, 동기화 대상 현황 |
| `oaissync list` | 동기화 가능한 프로젝트 목록 조회 |
| `oaissync files` | 동기화 대상 파일/폴더 목록 |
| `oaissync view [project]` | 대상 프로젝트와 차이점 비교 (읽기 전용) |
| `oaissync diff [project] [file]` | 특정 파일 내용 비교 (unified diff) |
| `oaissync merge [project] [file]` | **양쪽 파일 병합** (버전 이력 + 섹션 통합) |
| `oaissync run [project]` | 동기화 실행 (대화형) |

#### oaistest

| 명령어 | 설명 |
|--------|------|
| `oaistest status` | 서브명령어 리스트, 상태 요약 |
| `oaistest run` | 전체 테스트 (Part D 재스캔 자동 선행) |
| `oaistest run --unit` | Part C pytest |
| `oaistest run --e2e` | Part B 시나리오 |
| `oaistest run --module` | Part D oais 모듈 (재스캔 자동 선행) |
| `oaistest run --runtime` | Part E 런타임 검증 (import 테스트) |
| `oaistest run [ID]` | 특정 시나리오 |
| `oaistest run [P0-P3]` | 우선순위별 |
| `oaistest preview` | 계획 출력 |

#### oaistodo

| 명령어 | 설명 |
|--------|------|
| `oaistodo status` | 대기 중인 할 일 목록 표시 |
| `oaistodo` | **대기 중 업무 자동 처리 (기본)** |
| `oaistodo add [text]` | 새 할 일 추가 |
| `oaistodo add [text] --priority [high\|medium\|low]` | 우선순위 지정 추가 |
| `oaistodo --dry-run` | 실행 없이 계획만 표시 |
| `oaistodo --sp N` | 서브프로젝트 지정 |

#### oaisuser

| 명령어 | 설명 |
|--------|------|
| `oaisuser run` | 신규 생성 |
| `oaisuser status` | 서브명령어 리스트, 현황 조회 |
| `oaisuser add [기능명]` | 기능 사용법 추가 |
| `oaisuser faq [질문]` | FAQ 추가 |
| `oaisuser sync` | PRD 기반 동기화 |


---

## 4. Project Skills

`.claude/commands/`에 정의된 프로젝트 스킬입니다.

| 스킬 | 설명 | 위치 |
|------|------|------|
| `data-analysis` | Data Analysis Command: 데이터 분석 및 시각화 | .claude/commands/data-analysis.md |
| `env-setup` | Environment Setup Command: 개발 환경 설정 | .claude/commands/env-setup.md |
| `generate-tests` | generate-tests 스킬 | .claude/commands/generate-tests.md |
| `lint` | Python Linter | .claude/commands/lint.md |
| `test` | Test Runner | .claude/commands/test.md |
| `update-docs` | Documentation Update Command: Update Implementation Document | .claude/commands/update-docs.md |
| `daemosan:img-extract` | 고급 디자인 시스템 추출 가이드 | .claude/commands/daemosan/img-extract.md |
| `daemosan:paraller-work` | 고급 UI 변형 생성 가이드 | .claude/commands/daemosan/paraller-work.md |
| `sc:analyze` | sc:analyze 스킬 | .claude/commands/sc/analyze.md |
| `sc:build` | sc:build 스킬 | .claude/commands/sc/build.md |
| `sc:cleanup` | sc:cleanup 스킬 | .claude/commands/sc/cleanup.md |
| `sc:design` | sc:design 스킬 | .claude/commands/sc/design.md |
| `sc:document` | sc:document 스킬 | .claude/commands/sc/document.md |
| `sc:estimate` | sc:estimate 스킬 | .claude/commands/sc/estimate.md |
| `sc:explain` | sc:explain 스킬 | .claude/commands/sc/explain.md |
| `sc:git` | sc:git 스킬 | .claude/commands/sc/git.md |
| `sc:implement` | sc:implement 스킬 | .claude/commands/sc/implement.md |
| `sc:improve` | sc:improve 스킬 | .claude/commands/sc/improve.md |
| `sc:index` | sc:index 스킬 | .claude/commands/sc/index.md |
| `sc:load` | sc:load 스킬 | .claude/commands/sc/load.md |
| `sc:spawn` | sc:spawn 스킬 | .claude/commands/sc/spawn.md |
| `sc:task` | sc:task 스킬 | .claude/commands/sc/task.md |
| `sc:test` | sc:test 스킬 | .claude/commands/sc/test.md |
| `sc:troubleshoot` | sc:troubleshoot 스킬 | .claude/commands/sc/troubleshoot.md |
| `sc:workflow` | sc:workflow 스킬 | .claude/commands/sc/workflow.md |

---

## 5. Plugin Skills

Claude Code 플러그인에서 제공하는 스킬입니다.

#### code-review

| 스킬 | 설명 |
|------|------|
| `code-review:code-review` | Code review a pull request |

#### commit-commands

| 스킬 | 설명 |
|------|------|
| `commit-commands:clean_gone` | Cleans up git branches marked as [gone] |
| `commit-commands:commit-push-pr` | Commit, push, and open a PR |
| `commit-commands:commit` | Create a git commit |

#### document-skills

| 스킬 | 설명 |
|------|------|
| `document-skills:algorithmic-art` | Creating algorithmic art using p5.js |
| `document-skills:brand-guidelines` | Applies brand colors and typography |
| `document-skills:canvas-design` | Create visual art in .png and .pdf |
| `document-skills:doc-coauthoring` | Guide for co-authoring documentation |
| `document-skills:docx` | Document creation, editing, and analysis (.docx) |
| `document-skills:frontend-design` | Create production-grade frontend interfaces |
| `document-skills:internal-comms` | Write internal communications |
| `document-skills:mcp-builder` | Guide for creating MCP servers |
| `document-skills:pdf` | PDF manipulation toolkit |
| `document-skills:pptx` | Presentation creation and editing (.pptx) |
| `document-skills:skill-creator` | Guide for creating effective skills |
| `document-skills:slack-gif-creator` | Create animated GIFs for Slack |
| `document-skills:theme-factory` | Toolkit for styling artifacts with a theme |
| `document-skills:web-artifacts-builder` | Tools for creating web artifacts |
| `document-skills:webapp-testing` | Toolkit for testing web apps with Playwright |
| `document-skills:xlsx` | Spreadsheet creation and analysis (.xlsx) |

#### feature-dev

| 스킬 | 설명 |
|------|------|
| `feature-dev:feature-dev` | Guided feature development with codebase understanding |

#### frontend-design

| 스킬 | 설명 |
|------|------|
| `frontend-design:frontend-design` | Create distinctive frontend interfaces |

#### superpowers

| 스킬 | 설명 |
|------|------|
| `superpowers:brainstorming` | Use before any creative work |
| `superpowers:dispatching-parallel-agents` | Use for 2+ independent tasks |
| `superpowers:executing-plans` | Execute written implementation plan |
| `superpowers:finishing-a-development-branch` | Guide completion of development work |


---

## 6. MCP Servers

`.mcp.json`에 설정된 MCP 서버입니다.

| 서버 | 설명 |
|------|------|
| `mcp:sequential-thinking` | MCP Server: @modelcontextprotocol/server-sequential-thinking |
| `mcp:taskmaster-ai` | MCP Server: task-master-ai |
| `mcp:github` | MCP Server: @modelcontextprotocol/server-github |

---

## 7. 관련 문서

- `v/oaiscommand.md` - 명령어 집계 스킬 정의
- `.claude/COMMANDS.md` - SuperClaude 명령어 프레임워크
- `.mcp.json` - MCP 서버 설정
