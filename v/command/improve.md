# improve - 코드 개선

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

코드 품질, 성능, 유지보수성에 대한 체계적인 개선을 적용합니다.

## 2. 사용법

```
improve [target] [--focus performance|security|quality|readability] [--scope file|module|project]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 개선할 파일 또는 모듈 |
| `--focus` | 개선 초점 (performance, security, quality, readability) |
| `--scope` | 개선 범위 (file, module, project) |
| `--preserve-api` | 외부 API 호환성 유지 |
| `--measure` | 개선 전후 측정 |

## 4. 실행 단계

1. 현재 코드 상태 분석 및 측정
2. 개선 기회 식별 및 우선순위화
3. 개선 계획 수립 (최소 변경 원칙)
4. 단계적 개선 적용
5. 테스트를 통한 기능 검증
6. 개선 결과 측정 및 문서화

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Edit, MultiEdit, Bash

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaischeck.md` - 코드 에러 체크
- `v/oaisfix.md` - 코드 오류 자동 개선

---
