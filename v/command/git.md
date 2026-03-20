# git - Git 작업

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |

---

## 1. 개요

지능적인 커밋 메시지, 브랜치 관리, 워크플로우 최적화와 함께 Git 작업을 실행합니다.

## 2. 사용법

```
git [operation] [args] [--smart-commit] [--branch-strategy]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `operation` | Git 작업 (add, commit, push, pull, merge, branch, status) |
| `args` | 작업별 인자 |
| `--smart-commit` | 지능적인 커밋 메시지 생성 |
| `--branch-strategy` | 브랜치 명명 규칙 적용 |
| `--interactive` | 복잡한 작업을 위한 대화형 모드 |

## 4. 실행 단계

1. 현재 Git 상태 및 저장소 컨텍스트 분석
2. 검증과 함께 요청된 Git 작업 실행
3. 지능적인 커밋 메시지 생성 적용
4. 머지 충돌 및 브랜치 관리 처리
5. 명확한 피드백 및 다음 단계 제공

## 5. 도구 연동

### Claude
- **allowed-tools**: Bash, Read, Glob, TodoWrite, Edit

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 관련 스킬

- `v/oaiscommit.md` - 커밋 + 이력 정리 통합

---
