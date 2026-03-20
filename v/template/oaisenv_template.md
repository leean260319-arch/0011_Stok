# d0009_env.md - 개발 환경 현황

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | {{DATE}} | oaisenv run 자동 생성 |

---

## 목차

1. [시스템 환경](#1-시스템-환경)
2. [MCP 서버 현황](#2-mcp-서버-현황)
3. [Claude 플러그인](#3-claude-플러그인)
4. [Claude 스킬](#4-claude-스킬)
5. [oais 스킬](#5-oais-스킬)
6. [에이전트 현황](#6-에이전트-현황)
7. [커맨드 현황](#7-커맨드-현황)
8. [Python 패키지](#8-python-패키지)
9. [검증 결과](#9-검증-결과)

---

> 스킬: `v/oaisenv.md` | 마지막 업데이트: {{DATETIME}}

## 1. 시스템 환경

### 1.1 런타임 버전

| 항목 | 버전 |
|------|------|
| Python | {{PYTHON_VERSION}} |
| UV | {{UV_VERSION}} |
| Node.js | {{NODE_VERSION}} |
| npm | {{NPM_VERSION}} |
| Git | {{GIT_VERSION}} |
| Pandoc | {{PANDOC_VERSION}} |

### 1.2 개발 도구 상태

| 도구 | 상태 |
|------|------|
{{DEV_TOOLS_TABLE}}

---

## 2. MCP 서버 현황 ({{MCP_INSTALLED_COUNT}}/{{MCP_TOTAL_COUNT}}개 설치)

| MCP 서버 | 역할 | 설치 | 설치 방법 |
|---------|------|:----:|----------|
{{MCP_STATUS_TABLE}}

---

## 3. Claude 플러그인 ({{PLUGINS_INSTALLED_COUNT}}/12개 설치)

| 플러그인 | 역할 | 설치 | 설치 방법 |
|---------|------|:----:|----------|
| code-review | PR/코드 리뷰 자동화 | {{P_code-review}} | `/plugin install code-review@claude-plugins-official` |
| commit-commands | Git 커밋 메시지 생성 | {{P_commit-commands}} | `/plugin install commit-commands@claude-plugins-official` |
| frontend-design | 프론트엔드 UI/UX 디자인 | {{P_frontend-design}} | `/plugin install frontend-design@claude-plugins-official` |
| feature-dev | 기능 개발 워크플로우 | {{P_feature-dev}} | `/plugin install feature-dev@claude-plugins-official` |
| context7 | 라이브러리 문서 조회 | {{P_context7}} | `/plugin install context7@claude-plugins-official` |
| serena | 심볼릭 코드 분석/편집 | {{P_serena}} | `/plugin install serena@claude-plugins-official` |
| playwright | E2E 테스트 자동화 | {{P_playwright}} | `/plugin install playwright@claude-plugins-official` |
| typescript-lsp | TypeScript 언어 서버 | {{P_typescript-lsp}} | `/plugin install typescript-lsp@claude-plugins-official` |
| pyright-lsp | Python 타입 체크 (Pyright) | {{P_pyright-lsp}} | `/plugin install pyright-lsp@claude-plugins-official` |
| security-guidance | 보안 가이드라인 제공 | {{P_security-guidance}} | `/plugin install security-guidance@claude-plugins-official` |
| paper-search-tools | 논문 검색 MCP & Skills | {{P_paper-search-tools}} | `/plugin marketplace add fcakyon/claude-codex-settings` → `/plugin install paper-search-tools@fcakyon-claude-plugins` |
| oh-my-claudecode | Claude Code 확장 (omc) | {{P_oh-my-claudecode}} | `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode` → `/plugin install oh-my-claudecode` → `/oh-my-claudecode:omc-setup` |

---

## 4. Claude 스킬 ({{CLAUDE_SKILLS_INSTALLED_COUNT}}/15개 설치)

> 스킬 디렉토리: https://skills.sh/ | 설치: `npx skills add <url> --skill <name>`

| 스킬 | 역할 | 설치 | 설치 방법 |
|------|------|:----:|----------|
| algorithmic-art | 알고리즘 아트 생성 (p5.js) | {{S_algorithmic-art}} | `npx skills add https://github.com/anthropics/skills --skill algorithmic-art` |
| brand-guidelines | 브랜드 가이드라인 적용 | {{S_brand-guidelines}} | `npx skills add https://github.com/anthropics/skills --skill brand-guidelines` |
| canvas-design | 비주얼 아트 생성 (.png, .pdf) | {{S_canvas-design}} | `npx skills add https://github.com/anthropics/skills --skill canvas-design` |
| doc-coauthoring | 문서 공동 작성 워크플로우 | {{S_doc-coauthoring}} | `npx skills add https://github.com/anthropics/skills --skill doc-coauthoring` |
| docx | Word 문서 생성/편집 | {{S_docx}} | `npx skills add https://github.com/anthropics/skills --skill docx` |
| internal-comms | 내부 커뮤니케이션 작성 | {{S_internal-comms}} | `npx skills add https://github.com/anthropics/skills --skill internal-comms` |
| mcp-builder | MCP 서버 구축 가이드 | {{S_mcp-builder}} | `npx skills add https://github.com/anthropics/skills --skill mcp-builder` |
| pdf | PDF 조작/생성/분석 | {{S_pdf}} | `npx skills add https://github.com/anthropics/skills --skill pdf` |
| pptx | PowerPoint 생성/편집 | {{S_pptx}} | `npx skills add https://github.com/anthropics/skills --skill pptx` |
| skill-creator | 스킬 생성 가이드 | {{S_skill-creator}} | `npx skills add https://github.com/anthropics/skills --skill skill-creator` |
| slack-gif-creator | Slack용 GIF 생성 | {{S_slack-gif-creator}} | `npx skills add https://github.com/anthropics/skills --skill slack-gif-creator` |
| theme-factory | 아티팩트 테마 적용 | {{S_theme-factory}} | `npx skills add https://github.com/anthropics/skills --skill theme-factory` |
| webapp-testing | 웹앱 테스팅 (Playwright) | {{S_webapp-testing}} | `npx skills add https://github.com/anthropics/skills --skill webapp-testing` |
| web-artifacts-builder | 복합 웹 아티팩트 구축 | {{S_web-artifacts-builder}} | `npx skills add https://github.com/anthropics/skills --skill web-artifacts-builder` |
| xlsx | Excel 스프레드시트 생성/편집 | {{S_xlsx}} | `npx skills add https://github.com/anthropics/skills --skill xlsx` |

> **일괄 설치**: `npx skills add https://github.com/anthropics/skills` (전체 Anthropic 공식 스킬)

---

## 5. oais 스킬 ({{OAIS_SKILLS_COUNT}}개)

{{SKILLS_TABLE}}

---

## 6. 에이전트 현황 ({{AGENTS_INSTALLED_COUNT}}/{{AGENTS_TOTAL_COUNT}}개 사용)

> 설치: `v/unuse/agent/xxx.md` → `v/agent/` | 삭제: `v/agent/xxx.md` → `v/unuse/agent/`

| 에이전트 | 사용 | 역할 |
|---------|:----:|------|
{{AGENTS_TABLE}}

---

## 7. 커맨드 현황 ({{COMMANDS_INSTALLED_COUNT}}/{{COMMANDS_TOTAL_COUNT}}개 사용)

> 설치: `v/unuse/command/xxx.md` → `v/command/` | 삭제: `v/command/xxx.md` → `v/unuse/command/`

| 커맨드 | 사용 | 역할 |
|--------|:----:|------|
{{COMMANDS_TABLE}}

---

## 8. Python 패키지

| 항목 | 값 |
|------|---|
| 설치된 패키지 | {{PACKAGES_COUNT}}개 |
| PyTorch | {{PYTORCH_VERSION}} |
| CUDA | {{CUDA_AVAILABLE}} |

---

## 9. 검증 결과

| 항목 | 결과 |
|------|------|
| 발견된 이슈 | {{ISSUES_FOUND}} |
| 수정된 이슈 | {{ISSUES_FIXED}} |
| 남은 이슈 | {{ISSUES_REMAINING}} |
| 검증 상태 | {{VALIDATION_STATUS}} |

{{VALIDATION_ISSUES_SECTION}}

---

*이 문서는 `oaisenv run` 명령으로 자동 생성됩니다.*
