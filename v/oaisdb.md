# oaisdb - DB 수정 및 최적화 스킬

> 공통 원칙: `v/guide/common_guide.md` 참조

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v04 | 2026-01-04 | design/dev 서브명령어 추가 (DB 설계 및 마이그레이션) |
| v03 | 2026-01-04 | 섹션 3 개선: SP별 DB 문서화 규칙 상세화 (사용/미사용 테이블/컬럼 표기 형식) |
| v02 | 2026-01-03 | run에 validate 통합 (코드-DB 정합성 검증 포함) |
| v01 | 2026-01-02 | 최초 생성 |

---

## 1. 개요

DB 문제점 발견 → 기록 → 수정하는 3-Phase 워크플로우.

| 구분 | 문서 | 용도 |
|------|------|------|
| 에러/이슈 | d{SP}0004_todo.md | 이 스킬이 처리 |
| 신규 개발 | d{SP}0002_plan.md | 스키마 확장 |

**Phase 흐름**: validate(코드-DB) → 분석(DB) → d0004 기록 → 수정 → 해결 이동 → 미해결 0개 확인

**DB 유형**: SQLite, PostgreSQL, MySQL | **위치**: `db/*.db`

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisdb status` | 서브명령어 리스트, DB 상태/미해결 이슈 |
| `oaisdb version` | 스킬 버전 정보 (v04) |
| `oaisdb run` | **validate + 분석 + 수정** (3-Phase 통합) |
| `oaisdb validate` | SQL 쿼리 스키마 검증만 (EXPLAIN) |
| `oaisdb optimize` | run + 최적화 |
| `oaisdb doc` | d0006_db.md 문서화 |
| `oaisdb design` | **DB 설계**: PRD/Plan 기반 테이블/컬럼 설계 → d{SP}0006_db.md |
| `oaisdb dev` | **DB 개발**: 설계된 스키마 마이그레이션 (백업 필수) |

**옵션**: `--db <path>`, `--table [name]`, `--dry-run`, `--path <code_path>`, `--sp <num>`

## 3. 서브프로젝트 DB 문서 규칙

**DB는 공통 사용** → 모든 SP에서 전체 DB를 분석하되, SP별 사용 현황을 명시

| SP | 출력 문서 | 분석 범위 | 내용 |
|----|----------|----------|------|
| 00 | d0006_db.md | 전체 DB | 전체 스키마, ERD, 모든 테이블/컬럼 |
| ≠00 | d{SP}0006_db.md | 전체 DB | 전체 스키마 + **SP별 사용 현황 표기** |

### 3.1 SP≠00 문서화 규칙

SP≠00일 때 `oaisdb doc` 실행 시:

1. **전체 DB 분석**: 모든 테이블/컬럼 스키마 포함
2. **사용 현황 표기**: 해당 SP 코드에서 사용/미사용 명확히 구분

**테이블 사용 현황 표기 형식**:

```markdown
| 테이블명 | SP 사용 | 설명 |
|----------|---------|------|
| senior_users | ✅ 사용 | 회원 정보 |
| admin_logs | ❌ 미사용 | 관리자 로그 (SP=00 전용) |
| news_contents | ✅ 사용 | 뉴스 콘텐츠 |
```

**컬럼 사용 현황 표기 형식** (테이블별):

```markdown
### senior_users 테이블
| 컬럼명 | SP 사용 | 타입 | 설명 |
|--------|---------|------|------|
| user_id | ✅ 사용 | INTEGER | PK |
| email | ✅ 사용 | TEXT | 이메일 |
| admin_level | ❌ 미사용 | INTEGER | 관리자 레벨 (SP=00 전용) |
```

### 3.2 사용 판정 기준

| 판정 | 조건 |
|------|------|
| ✅ 사용 | SP 코드에서 SELECT/INSERT/UPDATE/DELETE 참조 |
| ❌ 미사용 | SP 코드에서 참조 없음 (다른 SP 전용) |
| ⚠️ 간접 | FK 관계로 간접 참조 (JOIN 등) |

## 4. 병렬 처리

**아키텍처**: 메인(분석+조율+검증) → Task(background) → Agent1~4(스키마/인덱스/쿼리/데이터)

| Agent | 영역 | 에이전트 |
|-------|------|----------|
| 1 | 스키마/FK | task-executor |
| 2 | 인덱스 | data-analyst |
| 3 | 쿼리 | task-executor |
| 4 | 데이터 | data-analyst |

**병렬화 기준**:
- INTEGRITY: 순차 (의존성)
- FK/INDEX/QUERY/DATA: 병렬 (테이블별 독립)

**처리 시간**: 순차 85분+ → 병렬 35-40분

## 5. 워크플로우

### 5.1 run (3-Phase 통합)

```
Phase 1: validate (코드-DB 정합성)
    ↓
Phase 2: DB 분석 (무결성/FK/스키마)
    ↓
Phase 3: 수정 및 검증
```

**Phase 1 - validate**:
- Python 코드 내 SQL 쿼리 추출
- EXPLAIN으로 스키마 검증
- 오류 시 d0004 등록 (CRITICAL)

| 오류 유형 | 심각도 | 예시 |
|----------|--------|------|
| 테이블 없음 | CRITICAL | `no such table: community_posts` |
| 컬럼 없음 | CRITICAL | `no such column: user_id` |
| 조인 오류 | CRITICAL | FK 불일치 |
| 타입 불일치 | WARNING | INT vs TEXT |

**Phase 2 - 분석**:
- DB 무결성 검사 (`PRAGMA integrity_check`)
- FK 관계 검증 (`foreign_key_check`)
- 스키마/인덱스 분석
- d0004 기록 → 병렬 계획

**Phase 3 - 수정**:
- 에이전트 병렬 수정
- 검증 및 문서 반영

### 5.2 validate (단독)

코드-DB 정합성 검증만 실행 (수정 없음)

**사용**: `oaisdb validate [--path <dir>]`

### 5.3 optimize

run + 인덱스/쿼리/정규화 최적화 → `[OPT]` 태그로 d0004 등록

### 5.4 design (DB 설계)

PRD/Plan 문서와 코드를 분석하여 DB 스키마를 설계하고 문서화합니다.

**사용**: `oaisdb design [--sp <num>]`

**워크플로우**:

```
1. 문서 분석
   - d{SP}0001_prd.md: 기능 요구사항에서 엔티티 추출
   - d{SP}0002_plan.md: 개발 계획에서 데이터 모델 파악
   - 기존 코드: SQL 쿼리에서 사용 패턴 분석

2. 스키마 설계
   - 테이블 정의 (이름, 용도)
   - 컬럼 정의 (타입, 제약조건, 기본값)
   - 관계 정의 (PK, FK, 인덱스)

3. 문서 출력
   - SP=00: d0006_db.md (전체 DB 구조)
   - SP≠00: d{SP}0006_db.md (전체 DB + SP 사용 표시)
```

**설계 테이블 표기 규칙**:

| 구분 | 표기 | 설명 |
|------|------|------|
| 구현 완료 | (없음) | 실제 DB에 존재 |
| 설계 중 | `(설계)` | 아직 미구현, 마이그레이션 필요 |
| 삭제 예정 | `(삭제예정)` | 향후 제거 대상 |

**문서 형식 예시**:

```markdown
### users 테이블
| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| id | INTEGER | PK | 사용자 ID |
| name | TEXT | NOT NULL | 이름 |

### posts 테이블 (설계)
| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| id | INTEGER | PK | 게시글 ID |
| user_id | INTEGER | FK→users.id | 작성자 |
```

### 5.5 dev (DB 마이그레이션)

설계된 스키마를 실제 DB에 반영합니다. 데이터 보존을 위해 백업 필수.

**사용**: `oaisdb dev [--db <path>] [--table <name>]`

**워크플로우**:

```
1. 사전 점검
   - d{SP}0006_db.md에서 (설계) 테이블 목록 추출
   - 현재 DB 스키마와 비교
   - 변경사항 목록 생성

2. 백업 생성 (필수)
   - 형식: db/backup_YYYYMMDD-HHMM.db
   - 예: db/backup_20260104-1530.db

3. 사용자 확인 (기존 데이터 처리)
   - 컬럼 추가: 기본값 또는 NULL 허용?
   - 컬럼 삭제: 데이터 백업 필요?
   - 타입 변경: 데이터 변환 방법?
   - 테이블 삭제: 정말 삭제?

4. 마이그레이션 실행
   - ALTER TABLE / CREATE TABLE 실행
   - 데이터 마이그레이션 (필요시)
   - 인덱스/FK 재생성

5. 검증 및 문서 갱신
   - PRAGMA integrity_check
   - foreign_key_check
   - (설계) 꼬리표 제거
```

**백업 정책**:

| 항목 | 규칙 |
|------|------|
| 위치 | `db/backup_YYYYMMDD-HHMM.db` |
| 보관 | 최근 5개 유지 (자동 정리) |
| 복원 | `oaisdb restore --backup <filename>` |

**사용자 질문 예시**:

```
⚠️ 기존 데이터 처리 확인

[posts] 테이블에 [category] 컬럼 추가:
- 기본값 설정: 'general'
- NULL 허용: 기존 행은 NULL

어떤 방식을 선택하시겠습니까? (1/2)
```

## 6. d0004 연동

**이슈 범위**: `db/*.db`, 스키마/쿼리 관련만
**ID 규칙**: `D` prefix + `[FIX]`/`[OPT]` 태그
**흐름**: 발견 → d0004(대기) → 수정(진행중) → 해결 이동

## 7. 최적화 체크리스트

| 영역 | 항목 |
|------|------|
| 인덱스 | 조회 컬럼, 복합, 미사용 제거 |
| 쿼리 | N+1, JOIN, SELECT *, EXPLAIN |
| 스키마 | 정규화, 타입, NULL, FK |
| 데이터 | 미사용, 고아, 중복 |

## 8. 완료 조건

**run**: 미해결 0개 + `PRAGMA integrity_check` ok + `foreign_key_check` 통과 + 문서 반영
**optimize**: run 조건 + `[OPT]` 0개

## 9. SQL 템플릿

```sql
-- 테이블/인덱스/검증
SELECT name FROM sqlite_master WHERE type='table';
SELECT name, tbl_name FROM sqlite_master WHERE type='index';
PRAGMA integrity_check; PRAGMA foreign_key_check;
```

## 10. 관련 문서

doc/d{SP}0004_todo.md (이슈), doc/d0006_db.md (DB 구조)

## 11. 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/analyze.md` | 코드 분석 |
| `v/command/improve.md` | 최적화 |
