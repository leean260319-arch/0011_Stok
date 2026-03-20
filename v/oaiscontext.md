# oaiscontext - 서브프로젝트 컨텍스트 관리

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v03 | 2026-01-09 | oaisfix run 예외 규칙 추가 (SP≠00: d{SP}0004 + d0004 병행) |
| v02 | 2026-01-09 | 섹션 8 규칙 변경: 병행 처리 → 단일 등록 (context 기준) |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

## 1. 개요

서브프로젝트별 문서 컨텍스트 설정. 모든 oais 스킬이 해당 SP 문서 참조.

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaiscontext version` | 스킬 버전 정보 (v03) |
| `oaiscontext` | 현재 컨텍스트 확인 |
| `oaiscontext [N]` | SP N으로 설정 (00~05) |
| `oaiscontext clear` | 공통(00) 초기화 |
| `oaiscontext list` | SP 목록 표시 |

## 3. SP 번호 체계

| SP | 폴더 | 문서 범위 |
|:--:|------|----------|
| 00 | (공통) | d0001~d9999 |
| 01 | 01_algorithm | d10001~d19999 |
| 02 | 02_1st_server | d20001~d29999 |
| 03~05 | 03~05_reserved | d30001~d59999 |

## 4. 문서 매핑

```
문서번호 = SP × 10000 + 기본번호
예) SP=02: d0001→d20001, d0004→d20004
```

## 5. 우선순위

`--sp N` > 세션 컨텍스트 > CWD 감지(`0N_*`) > 기본값(00)

## 6. 사용 예시

```bash
oaiscontext 02     # 02로 전환 → d20001~d20010 참조
oaischeck --sp 01  # 일회성 01 사용
oaiscontext clear  # 00 복귀
```

## 7. 자동 감지

| CWD 패턴 | SP |
|----------|:--:|
| `*/01_*/*`, `01_*` | 01 |
| `*/02_*/*`, `02_*` | 02 |
| 그 외 | 00 |

## 8. 문서 등록 규칙

> **핵심 규칙**: context 설정에 따라 **단일 문서**에만 등록

### 규칙

| 조건 | 등록 대상 |
|------|----------|
| `oaiscontext` 미지정 (SP=00) | **d0004** 에만 등록 |
| `oaiscontext [N]` 지정 (SP≠00) | **d{SP}0004** 에만 등록 |

### 적용 대상

| 스킬 | 처리 방식 |
|------|----------|
| oaischeck | 에러를 현재 SP의 todo 문서에 등록 |
| **oaisfix** | **SP≠00: d{SP}0004 + d0004 둘 다 확인/수정** |
| oaisdev | 현재 SP의 todo 문서 사전 검토 |
| oaishistory | 현재 SP의 todo → history 아카이브 |
| oaisbatch | 모든 단계에서 현재 SP 문서 사용 |

> **oaisfix 예외**: 수정 작업은 공통 모듈(oais)에도 영향을 줄 수 있으므로 d0004도 함께 처리

### 예시

```
# context 미지정 (기본 SP=00)
oaischeck: doc/d0004_todo.md 에 등록
oaisfix:   doc/d0004_todo.md 이슈 처리

# oaiscontext 02 설정 시
oaischeck: doc/d20004_todo.md 에만 등록
oaisfix:   doc/d20004_todo.md + doc/d0004_todo.md 둘 다 처리
```

### 주의사항

- **파일 자동 생성**: d{SP}0004 파일이 없으면 즉시 생성
- **context 전환 시**: 이전 SP 이슈는 해당 SP 문서에서만 관리
- **공통 oais 모듈 이슈**: context 미지정 상태에서 d0004에 등록 권장

## 9. 관련 문서

- `v/guide/common_guide.md`, `CLAUDE.md`
