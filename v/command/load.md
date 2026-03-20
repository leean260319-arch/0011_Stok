# load - 프로젝트 컨텍스트 로드

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

프로젝트 컨텍스트, 구성 및 종속성을 로드하고 분석합니다.

## 2. 사용법

```
load [path] [--depth shallow|deep|full] [--focus <area>]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `path` | 로드할 프로젝트 경로 |
| `--depth` | 로드 깊이 (shallow, deep, full) |
| `--focus` | 특정 영역에 집중 (api, ui, db, config) |
| `--cache` | 결과 캐싱 활성화 |
| `--refresh` | 캐시 무시하고 새로 로드 |

## 4. 실행 단계

1. 프로젝트 구조 탐색
2. 구성 파일 분석 (package.json, pyproject.toml 등)
3. 종속성 그래프 구축
4. 핵심 모듈 및 진입점 식별
5. 프로젝트 메타데이터 수집
6. 컨텍스트 요약 생성

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Glob, Grep, Bash

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaisstart.md` - 프로젝트 시작 및 초기화

---
