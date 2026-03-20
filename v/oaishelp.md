# oaishelp - 명령어/스킬 도움말

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-04 | 역할 변경: d0007_command.md 표시로 단순화 |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 공통 가이드: `v/guide/common_guide.md`

## 1. 개요

**역할**: `doc/d0007_command.md` 문서 표시

d0007_command.md는 프로젝트의 모든 명령어, 스킬, 플러그인을 집계한 통합 문서입니다.

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaishelp version` | 스킬 버전 정보 (v02) |
| `oaishelp` | d0007_command.md 전체 표시 |
| `oaishelp [섹션]` | 특정 섹션만 표시 (예: oais, claude, plugin) |
| `oaishelp [스킬명]` | 특정 스킬 상세 (해당 v/oais*.md 참조) |

## 3. d0007 문서 구조

| 섹션 | 내용 |
|------|------|
| 1. 개요 | 통계 요약 |
| 2. Claude Built-in | /help, /clear 등 18개 |
| 3. Project Skills | sc:*, update-docs 등 25개 |
| 4. Plugin Skills | code-review, commit 등 26개 |
| 5. MCP Servers | sequential-thinking 등 3개 |
| 6. OAIS 스킬 | oais* 18개 스킬 상세 |
| 7. 스킬 정합성 | 서브에이전트, 병렬처리, status 지원 현황 |
| 8. 스크립트 | v/script/*.py 목록 |

## 4. 실행

```bash
# d0007 전체 표시
oaishelp

# 특정 섹션
oaishelp oais      # OAIS 스킬만
oaishelp claude    # Claude Built-in만
oaishelp plugin    # Plugin Skills만

# 특정 스킬 상세 (→ v/oais*.md 참조)
oaishelp oaisdev   # → v/oaisdev.md 내용 표시
```

## 5. 관련 문서

| 문서 | 용도 |
|------|------|
| `doc/d0007_command.md` | 명령어/스킬 통합 집계 (마스터) |
| `v/oais*.md` | 개별 스킬 상세 정의 |
| `v/guide/common_guide.md` | 공통 가이드라인 |
