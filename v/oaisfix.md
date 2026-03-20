# oaisfix - 코드 오류 자동 개선 스킬

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 에이전트 활용: `v/guide/common_guide.md` | 서브프로젝트: `v/oaiscontext.md`

## 1. 개요

`d{SP}0004_todo.md` 이슈를 **서브에이전트 병렬 처리**로 자동 수정 → `d{SP}0010_history.md` 기록.

- **컨텍스트**: `--sp N` 또는 `oaiscontext N`
- **역할 구분**: 에러/버그 → `d{SP}0004_todo.md`, 개발 작업 → `d{SP}0002_plan.md`
- **병행 처리**: SP≠00일 때 **d0004 AND d{SP}0004** 모두 확인/수정
- **3단계**: Phase 1(분석) → Phase 2(병렬 수정) → Phase 3(검증/문서)

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisfix status` | 서브명령어 리스트, 이슈 상태 |
| `oaisfix version` | 스킬 버전 정보 (v01) |
| `oaisfix run` | **이슈 자동 수정 (병렬)** |
| `oaisfix run [대상]` | 특정 이슈/파일/카테고리 |
| `oaisfix preview` | 수정 미리보기 |
| `oaisfix test` | 테스트 실행 |
| `oaisfix verify` | 수정 검증 |
| `oaisfix rollback` | 롤백 |

**옵션**: `--interactive`, `--force`, `--no-history`, `--sequential`

---

## 3. 병렬 처리

### 3.1 구조

```
메인 에이전트 (Phase 1,3: 분석/검증)
    │ Task(run_in_background=true)
    ├── Agent 1~3: 영역별 수정
```

### 3.2 에이전트

| 에이전트 | 역할 |
|---------|------|
| `codebase-investigator` | 영향 범위 분석 |
| `python-code-reviewer` | 코드 품질/버그 |
| `task-executor` (1~3) | 영역별 수정 |
| `task-checker` | 수정 검증 |

### 3.3 병렬화 기준

| 병렬화 | 이슈 |
|--------|------|
| 낮음 | E0611 (export), E0102 (중복) - 우선 순차 처리 |
| 높음 | E0606, E1101, E0704, W0612 - 파일별 독립 |

### 3.4 처리 시간

| 구분 | 순차 | 병렬 |
|------|------|------|
| Phase 2 | 60분+ | **15-20분** |
| **총계** | 75분+ | **30-35분** |

---

## 4. 워크플로우

**Phase 1** (메인): todo 파싱 → False Positive 필터 → 우선순위 → 병렬 계획

**Phase 2** (서브에이전트):
- 우선: `oais/__init__.py` export, E0102
- 병렬: Agent별 영역 수정 → py_compile 검증

**Phase 3** (메인): 검증 → d{SP}0004_todo.md 업데이트 → d{SP}0010_history.md 기록

---

## 5. False Positive

> `v/guide/debugging_guide.md` 섹션 4 참조

---

## 6. 이슈별 수정 전략

| 코드 | 이슈 | 수정 |
|------|------|------|
| E0611 | export 누락 | `__init__.py` import 추가 |
| E0102 | 중복 정의 | 첫 번째만 유지 |
| E0606 | 변수 미할당 | 초기화/로직 수정 |
| E1101 | 멤버 누락 | 올바른 멤버명 |
| E0704 | raise 오류 | except 블록 내 이동 |
| W0611/W0612 | 미사용 | 삭제 또는 `_` prefix |

---

## 7. 검증

**필수**: `uv run python -m py_compile <파일>` (common_guide.md 2.8 참조)

수정 → py_compile → 오류 시 재수정 → pytest → 완료

---

## 8. 완료 조건

| 조건 | 검증 |
|------|------|
| 이슈 해결 | **d0004 AND d{SP}0004** "현재 이슈" 비움 (SP≠00) |
| 구문 정상 | py_compile 통과 |
| 테스트 통과 | pytest 성공 |
| 문서 기록 | **d0010 AND d{SP}0010** history (SP≠00) |

---

## 9. 에러 처리

- **수정 실패**: 원본 유지 → todo 상세 추가
- **검증 실패**: rollback → 대안 제시
- **에이전트 실패**: 3회 재시도 → 메인 직접 처리

---

## 10. 주의사항

- **수정 제한**: 복잡 로직, DB 스키마, 프로덕션 직접 수정 불가
- **안전**: `preview` 사전 확인, `--interactive` 단계별, git 커밋 후 수정

---

## 11. 관련 문서

| 문서 | 용도 |
|------|------|
| v/oaischeck.md | 디버깅 워크플로우 |
| v/oaislib.md | oais 모듈 수정 |
| doc/d{SP}0004_todo.md | TODO/디버깅 |
| doc/d{SP}0010_history.md | 변경 이력 |

## 12. 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/improve.md` | 코드 개선 |
| `v/command/cleanup.md` | 정리/삭제 |
| `v/command/troubleshoot.md` | 트러블슈팅 |
