# explain - 코드 및 개념 설명

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

코드 기능, 개념 또는 시스템 동작에 대한 명확하고 종합적인 설명을 제공합니다.

## 2. 사용법

```
explain [target] [--level basic|intermediate|advanced] [--format text|diagram|examples]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 설명할 코드 파일, 함수, 개념 또는 시스템 |
| `--level` | 설명 복잡도 (basic, intermediate, advanced) |
| `--format` | 출력 형식 (text, diagram, examples) |
| `--context` | 설명을 위한 추가 컨텍스트 |

## 4. 실행 단계

1. 대상 코드 또는 개념을 철저히 분석
2. 핵심 컴포넌트 및 관계 식별
3. 복잡도 수준에 따른 설명 구조화
4. 관련 예시 및 사용 사례 제공
5. 적절한 형식으로 명확하고 접근 가능한 설명 제시

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Bash

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaislib.md` - 모듈 분석 및 문서화

---
