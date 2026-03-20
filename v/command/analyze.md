# analyze - 코드 분석

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

코드 품질, 보안, 성능, 아키텍처 영역에 걸친 종합적인 코드 분석을 수행합니다.

## 2. 사용법

```
analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `target` | 분석 대상 파일, 디렉토리 또는 프로젝트 |
| `--focus` | 분석 초점 영역 (quality, security, performance, architecture) |
| `--depth` | 분석 깊이 (quick, deep) |
| `--format` | 출력 형식 (text, json, report) |

## 4. 실행 단계

1. 분석 대상 파일을 탐색하고 분류
2. 적절한 분석 도구 및 기술 적용
3. 심각도 등급과 함께 발견사항 생성
4. 우선순위가 지정된 실행 가능한 권장사항 작성
5. 종합적인 분석 보고서 제시

## 5. 도구 연동

### Claude
- **allowed-tools**: Read, Grep, Glob, Bash, TodoWrite

### Gemini
- **MCP 플래그**: --seq, --c7, --magic, --verbose, --quiet

## 6. 관련 스킬

- `v/oaischeck.md` - 프로젝트 특화 코드 에러 체크
- `v/oaisfix.md` - 코드 오류 자동 개선

---
