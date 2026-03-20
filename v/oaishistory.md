# oaishistory - 완료 항목 이력 이동 스킬

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 공통: v/guide/common_guide.md | 컨텍스트: v/oaiscontext.md

## 1. 개요

d{SP}0004_todo.md 완료 항목 → d{SP}0010_history.md 이동

**컨텍스트**: `--sp N` 또는 `oaiscontext N`

| 기능 | 설명 |
|------|------|
| 이력 이동 | d{SP}0004 → d{SP}0010 |
| **병행 처리** | SP≠00일 때 **d0004→d0010 AND d{SP}0004→d{SP}0010** |
| 자동 요약 | >20K → 10K 축소 |

---

## 2. 서브명령어

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `oaishistory version` | 스킬 버전 정보 (v01) | 터미널 |
| oaishistory status | 서브명령어 리스트, 이동 대상 항목 수, d0010 토큰 상태 | - |
| oaishistory run | 완료 항목 d{SP}0010 이동 | doc/d{SP}0010_history.md |

---

## 3. 워크플로우

**타이밍**: 해결 후 1~2주 안정성 확인

```
d{SP}0004 스캔 → 태그 추론 → d{SP}0010 등록 → 토큰 체크(>20K시 요약) → d{SP}0004 삭제
```

### 자동 요약

| 항목 | 값 |
|------|-----|
| 트리거 | >20K |
| 목표 | 10K |
| 보존 | 최근 30일 상세 |

**방식**: FIFO 1줄 요약 → "## 아카이브 요약" 이동

---

## 4. 형식 처리

**대상**: d{SP}0004 "해결된 이슈" 섹션 (표준/비표준)

| 형식 | 처리 |
|------|------|
| 표준 테이블 | 태그 유지 |
| 마크다운 목록 | 태그 추론 |
| 텍스트/인용 | MISC 적용 |

**태그 추론**:

| 키워드 | 태그 |
|--------|------|
| error, fix, bug | BUGFIX |
| security, 보안 | HOTFIX |
| update, 버전 | UPDATE |
| feature, 기능 | FEATURE |
| refactor, optimize | IMPROVE |
| doc, 문서 | DOCS |
| (없음) | MISC |

---

## 5. d0010 형식

```
#### YYYY-MM-DD - [태그] [제목]
- 파일: 경로 | 원인: 내용 | 해결: 방법
```

**태그**: HOTFIX | BUGFIX | UPDATE | FEATURE | IMPROVE | DOCS | REFACTOR | CONFIG | MISC

---

## 6. 서브에이전트

| 단계 | 에이전트 | 병렬 |
|------|----------|:----:|
| 스캔 | Explore | O |
| 요약 | task-executor | - |
| 검증 | task-checker | - |

---

## 7. 관련 문서

- **입력**: doc/d{SP}0004_todo.md
- **출력**: doc/d{SP}0010_history.md
- **태그**: v/guide/oaistodo_guide.md
