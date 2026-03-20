# oaiscommand - 명령어 집계 및 문서화

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-17 | 출력 정렬 규칙 섹션 추가 (스킬명 알파벳 순) |
| v01 | 2026-01-06 | 초기 버전 생성, 명령어 표기법 가이드 추가 |

---

> 프로젝트 명령어/스킬 통합 집계 및 문서화 | ref: `v/guide/common_guide.md`

## 개요

프로젝트에서 사용 가능한 모든 명령어, 스킬, 플러그인을 자동으로 스캔하여 `doc/d0007_command.md` 문서로 집계합니다.

## 명령어

| 명령어 | 설명 |
|--------|------|
| `oaiscommand status` | 서브명령어 리스트, 현재 상태 |
| `oaiscommand version` | 스킬 버전 정보 (v02) |
| `oaiscommand run` | 전체 명령어 집계 및 문서화 (기본) |
| `oaiscommand update` | d0007_command.md 업데이트 |
| `oaiscommand list` | v/command/ 명령어 목록 조회 |
| `oaiscommand compare` | 외부 소스와 비교 (sc/) |
| `oaiscommand sync` | 외부 소스 변경사항 동기화 |
| `oaiscommand adopt [명령어]` | 특정 외부 명령어 채택 |

실행: `uv run python v/script/oaiscommand_run.py [subcommand] [args]`

## 집계 대상

| 카테고리 | 소스 위치 | 설명 |
|----------|----------|------|
| OAIS 스킬 | `v/oais*.md` | 프로젝트 전용 스킬 |
| Built-in 명령어 | (내장) | Claude Code 기본 슬래시 명령어 |
| Project Skills | `.claude/commands/*.md` | 프로젝트 커스텀 스킬 |
| Plugin Skills | `.claude/commands/sc/*.md` | SuperClaude 플러그인 |
| MCP Servers | `.mcp.json` | MCP 서버 설정 |

## 명령어 표기법 규칙

### 필수 규칙: 스킬명 접두사

모든 서브명령어는 **스킬명을 접두사로 포함**해야 합니다.

**올바른 표기**:
```
| `oaistest run` | 전체 테스트 실행 |
| `oaistest status` | 상태 확인 |
| `oaissync list` | 프로젝트 목록 |
```

**잘못된 표기**:
```
| `run` | 전체 테스트 실행 |      ← 스킬명 누락
| `status` | 상태 확인 |          ← 스킬명 누락
```

### 자동 정규화

`oaiscommand run` 실행 시 스킬명이 누락된 명령어는 자동으로 정규화됩니다:
- `run` → `oaistest run`
- `status` → `oaischeck status`

### 표기 형식

| 요소 | 형식 | 예시 |
|------|------|------|
| 기본 명령 | `스킬명 서브명령` | `oaistest run` |
| 인자 포함 | `스킬명 서브명령 [인자]` | `oaissync view [project]` |
| 옵션 포함 | `스킬명 서브명령 --옵션` | `oaistest run --unit` |
| 대체 명령 | `스킬명 서브명령1 / 서브명령2` | `oaiscommit status / preview` |

## 출력 파일

- **d0007_command.md**: 명령어/스킬 통합 집계 문서
  - 섹션 1: 개요 및 통계
  - 섹션 2: Built-in 명령어
  - 섹션 3: OAIS 스킬 (요약 + 상세)
  - 섹션 4: Project Skills
  - 섹션 5: Plugin Skills
  - 섹션 6: MCP Servers

## 출력 정렬 규칙

모든 테이블 및 섹션은 **스킬명 알파벳 순**으로 정렬됩니다.

| 대상 | 정렬 기준 |
|------|----------|
| OAIS 스킬 요약 | 스킬명 알파벳 순 |
| OAIS 스킬 상세 | 스킬명 알파벳 순 |
| Plugin Skills | 플러그인명 알파벳 순 |
| MCP Servers | 서버명 알파벳 순 |

## 서브에이전트

| 단계 | 에이전트 | 역할 | 병렬 |
|------|----------|------|:----:|
| 스캔 | Explore | 명령어 파일 탐색 | O |
| 집계 | task-executor | 문서 생성/업데이트 | O |
| 검증 | task-checker | 명령어 정규화 검증 | - |

## 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/document.md` | 문서화 작업 |

## 관련 경로

- 스크립트: `v/script/oaiscommand_run.py`
- 출력: `doc/d0007_command.md`
- OAIS 스킬: `v/oais*.md`
- Project Skills: `.claude/commands/`
