# document - 집중 문서화

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

특정 컴포넌트, 함수 또는 기능에 대한 정확하고 집중된 문서를 생성합니다.

## 2. 사용법

```
document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 문서화할 특정 파일, 함수 또는 컴포넌트 |
| `--type` | 문서 유형 (inline, external, api, guide) |
| `--style` | 문서 스타일 (brief, detailed) |
| `--template` | 특정 문서 템플릿 사용 |

## 4. 실행 단계

1. 대상 컴포넌트 분석 및 핵심 정보 추출
2. 문서화 요구사항 및 대상 독자 식별
3. 유형 및 스타일에 따른 적절한 문서 생성
4. 일관된 형식 및 구조 적용
5. 기존 문서 생태계와 통합

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Write, Edit

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaisdoc.md` - 프로젝트 문서 관리 가이드
- `v/oaisuser.md` - 사용자 가이드 문서 관리

---
