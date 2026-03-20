# estimate - 개발 추정

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

복잡도 분석을 기반으로 태스크, 기능 또는 프로젝트에 대한 정확한 개발 추정을 생성합니다.

## 2. 사용법

```
estimate [target] [--type time|effort|complexity|cost] [--unit hours|days|weeks]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 추정할 태스크, 기능 또는 프로젝트 |
| `--type` | 추정 유형 (time, effort, complexity, cost) |
| `--unit` | 추정 시간 단위 (hours, days, weeks) |
| `--breakdown` | 상세 추정 분석 제공 |

## 4. 실행 단계

1. 대상의 범위 및 요구사항 분석
2. 복잡도 요소 및 의존성 식별
3. 추정 방법론 및 과거 데이터 적용
4. 신뢰 구간과 함께 추정치 생성
5. 위험 요소와 함께 상세 분석 제시

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Bash

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaisplan.md` - 구현 계획 생성

---
