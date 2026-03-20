# troubleshoot - 문제 해결

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

코드, 빌드 또는 시스템 동작의 문제를 진단하고 해결합니다.

## 2. 사용법

```
troubleshoot [symptoms] [--deep] [--trace] [--fix]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `symptoms` | 문제 증상 또는 에러 메시지 |
| `--deep` | 심층 분석 모드 |
| `--trace` | 실행 추적 활성화 |
| `--fix` | 자동 수정 시도 |
| `--root-cause` | 근본 원인 분석 집중 |

## 4. 실행 단계

1. 증상 수집 및 분석
2. 에러 패턴 식별
3. 관련 코드 및 로그 탐색
4. 근본 원인 추론
5. 해결 방안 제시
6. 수정 적용 및 검증 (--fix 옵션 시)

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Bash, TodoWrite

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaischeck.md` - 코드 에러 체크 (debug 서브명령어)
- `v/oaisfix.md` - 코드 오류 자동 개선

---
