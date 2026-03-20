# cleanup - 코드 및 프로젝트 정리

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

체계적으로 코드를 정리하고, 불필요한 코드를 제거하고, import를 최적화하며, 프로젝트 구조를 개선합니다.

## 2. 사용법

```
cleanup [target] [--type code|imports|files|all] [--safe|--aggressive]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 정리할 파일, 디렉토리 또는 전체 프로젝트 |
| `--type` | 정리 유형 (code, imports, files, all) |
| `--safe` | 보수적 정리 (기본값) |
| `--aggressive` | 더 철저한 정리 (위험도 높음) |
| `--dry-run` | 변경사항 미리보기 (적용 안함) |

## 4. 실행 단계

1. 대상의 정리 기회 분석
2. 불필요 코드, 미사용 import, 중복 파일 식별
3. 위험 평가와 함께 정리 계획 수립
4. 적절한 안전 조치와 함께 정리 작업 실행
5. 변경사항 검증 및 정리 결과 보고

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Bash, Edit, MultiEdit

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaisfix.md` - 코드 오류 자동 개선
- `v/oaischeck.md` - 코드 품질 체크
- `v/oaislib.md` - oais 모듈 수정/최적화

---
