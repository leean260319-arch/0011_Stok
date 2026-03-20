# oaisstart - 세션 시작 워크플로우

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-21 | common_guide.md 자동 로드 추가 |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 세션 시작 시 공통 가이드 로드, 문서 동기화 및 품질 검사 | ref: `v/guide/common_guide.md`

## 명령어

| 명령어 | 설명 |
|--------|------|
| `oaisstart status` | 서브명령어 리스트, 스킬/문서 상태 |
| `oaisstart version` | 스킬 버전 정보 (v02) |
| `oaisstart run` | 세션 시작 실행 (기본) |

실행: `uv run python v/script/oaisstart_run.py`

## 워크플로우

**common_guide.md 로드** → 문서 상태 점검 (PRD/TODO/HISTORY) → 동기화 체크리스트 → oaischeck 연동 → 준비 완료

## 서브에이전트

| 단계 | 에이전트 | 용도 |
|------|----------|------|
| 스캔 | Explore | 프로젝트 구조 (병렬) |
| 검증 | task-checker | 환경/설정 (병렬) |

## 관련

`v/script/oaisstart_run.py` | `v/oaischeck.md` | `doc/d{SP}0004_todo.md`
