# design - 시스템 및 컴포넌트 설계

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

시스템 아키텍처, API, 컴포넌트 인터페이스, 기술 사양을 설계합니다.

## 2. 사용법

```
design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 설계할 시스템, 컴포넌트 또는 기능 |
| `--type` | 설계 유형 (architecture, api, component, database) |
| `--format` | 출력 형식 (diagram, spec, code) |
| `--iterative` | 반복적 설계 개선 활성화 |

## 4. 실행 단계

1. 요구사항 및 설계 제약조건 분석
2. 초기 설계 개념 및 대안 작성
3. 상세 설계 사양 개발
4. 요구사항 및 모범사례 대비 설계 검증
5. 설계 문서 및 구현 가이드 생성

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Write, Edit, TodoWrite

### Gemini
- **MCP 플래그**: --seq, --c7, --magic, --verbose, --quiet

## 6. 관련 스킬

- `v/oaisplan.md` - 구현 계획 생성
- `v/oaisprd.md` - PRD 문서 생성

---
