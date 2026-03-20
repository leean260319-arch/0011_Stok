# oaisstop - 세션 종료 워크플로우

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

## 1. 개요

**목적**: 세션 종료 시 문서 자동 업데이트
**트리거**: `oaisstop`, `세션 종료`, `작업 종료`

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisstop status` | 서브명령어 리스트, 현재 상태 |
| `oaisstop version` | 스킬 버전 정보 (v01) |
| `oaisstop run` | **2단계 종료 실행 (기본)** |
| `oaisstop readme` | README.md만 (1단계) |
| `oaisstop sync` | doc/*.md만 (2단계) |

---

## 3. 서브에이전트

| 단계 | 에이전트 | 병렬 조합 |
|------|----------|----------|
| 검증 | `task-checker` | + `oaisqa` (다수 파일) |
| 품질 | `oaisqa` | + `task-checker` |
| 탐색 | `Explore` | + `task-executor` (문서 갱신) |
| 갱신 | `task-executor` | + `Explore` |

> 에이전트 정의: `v/agent/`

---

## 4. 종료 워크플로우

```
1단계: README.md → 2단계: doc/*.md
(작업내역, 다음작업)  (d0001~d0010)
```

### 4.1 README.md 템플릿

```markdown
## 최근 작업 내역
- 날짜: YYYY-MM-DD
- 작업: [요약]
- 변경: [파일]
- 다음: [후속]
```

### 4.2 doc/*.md 동기화

| 문서 | 조건 |
|------|------|
| d{SP}0001_prd.md | 기능 추가/변경 |
| d{SP}0004_todo.md | 완료/새 이슈 |
| d0005_lib.md | 라이브러리 추가 |
| d{SP}0010_history.md | 모든 변경 |

---

## 5. 체크리스트

**사전**: 문법 오류 없음 | 테스트 통과 | tmp/ 정리

**문서**:
- [ ] README.md: 개요, 구조, 설치, 변경
- [ ] d{SP}0004_todo.md: 완료/이슈
- [ ] d{SP}0010_history.md: 버전 이력

---

## 6. 커밋

> Git 규칙: `v/guide/common_guide.md` 3.2절

```
docs: 세션 종료 - [요약]

- README.md 업데이트
- doc/*.md 동기화

Generated with Claude Code
```

| 타입 | 형식 |
|------|------|
| feat | `feat: [기능] 완료` |
| fix | `fix: [버그] 수정` |
| refactor | `refactor: [대상] 개선` |

---

## 7. 주의사항

- 테스트 필수: 변경 후 통과 확인
- 문서 일관성: 코드-문서 불일치 방지
- 커밋 원자성: 관련 변경만
- 임시 제외: tmp/, __pycache__/

---

## 8. 관련 문서

- `v/oaisstart.md` - 세션 시작
- `doc/d{SP}0004_todo.md` - 할 일/디버깅
- `doc/d{SP}0010_history.md` - 변경 이력
