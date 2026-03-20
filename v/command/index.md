# index - 프로젝트 인덱싱

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

포괄적인 프로젝트 문서 및 지식 기반을 생성합니다.

## 2. 사용법

```
index [query] [--type files|symbols|docs|all] [--format tree|list|json]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `query` | 검색할 키워드 또는 패턴 |
| `--type` | 인덱싱 유형 (files, symbols, docs, all) |
| `--format` | 출력 형식 (tree, list, json) |
| `--depth` | 검색 깊이 제한 |
| `--exclude` | 제외할 패턴 |

## 4. 실행 단계

1. 프로젝트 구조 스캔
2. 파일 및 심볼 인덱싱
3. 문서 및 주석 추출
4. 관계 매핑 생성
5. 검색 가능한 인덱스 구축
6. 결과 형식에 맞게 출력

## 5. 도구 연동

### Claude
- **allowed-tools**: Glob, Grep, Read, Bash

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaislib.md` - 모듈 분석 및 문서화

---
