# spawn - 태스크 분할 및 병렬 실행

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

복잡한 태스크를 조율된 서브태스크로 분할하여 효율적으로 실행합니다.

## 2. 사용법

```
spawn [mode] [--parallel] [--sequential] [--max-agents <n>]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `mode` | 실행 모드 (parallel, sequential, adaptive) |
| `--parallel` | 병렬 실행 활성화 |
| `--sequential` | 순차 실행 강제 |
| `--max-agents` | 최대 동시 에이전트 수 |
| `--timeout` | 태스크별 타임아웃 설정 |

## 4. 실행 단계

1. 태스크 복잡도 분석
2. 의존성 기반 서브태스크 분할
3. 실행 전략 결정 (병렬/순차)
4. 에이전트 할당 및 실행
5. 결과 수집 및 통합
6. 최종 결과 보고

## 5. 도구 연동

### Claude
- **allowed-tools**: Task, Read, Glob, Grep, Bash, TodoWrite

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaisbatch.md` - 전체 파이프라인 배치 실행

---
