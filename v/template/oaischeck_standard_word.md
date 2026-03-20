# 표준용어집 (Standard Terminology)

> 중앙 안내: 상세한 에이전트 활용 원칙 및 공통 가이드라인은 `v/guide/common_guide.md`의 '2. 에이전트 활용 원칙' 섹션을 참조하십시오.

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성, 범용 샘플 용어집 |

---

## 1. 개요

이 문서는 프로젝트 내 코드, DB, 문서에서 사용하는 **표준 용어**를 정의합니다.
`oaischeck 용어만` 명령 실행 시 이 용어집을 기준으로 검증합니다.

### 사용법

1. 프로젝트에 맞게 용어 추가/수정
2. `oaischeck 용어만` 실행
3. 불일치 항목 확인 및 수정

---

## 2. 공통 용어 (Common Terms)

### 2.1 시스템/아키텍처

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 설정 | config | cfg, conf, setting | 시스템/앱 설정 |
| 환경 | env | environment | 실행 환경 (dev/prod) |
| 모듈 | module | mod | 코드 모듈 단위 |
| 유틸리티 | util | utils, utility | 공통 유틸리티 함수 |
| 헬퍼 | helper | hlpr | 보조 함수 |
| 핸들러 | handler | hdlr | 이벤트/요청 처리기 |
| 서비스 | service | svc, srv | 비즈니스 로직 레이어 |
| 컨트롤러 | controller | ctrl | 요청 처리 레이어 |
| 레포지토리 | repository | repo | 데이터 접근 레이어 |

### 2.2 데이터/DB

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 데이터베이스 | database | db | DB 전체 |
| 테이블 | table | tbl | DB 테이블 |
| 컬럼 | column | col | 테이블 컬럼 |
| 레코드 | record | rec, row | 테이블 행 |
| 쿼리 | query | qry | SQL 쿼리 |
| 연결 | connection | conn | DB 연결 |
| 트랜잭션 | transaction | tx, txn | DB 트랜잭션 |
| 인덱스 | index | idx | DB 인덱스 |

### 2.3 사용자/인증

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 사용자 | user | usr, member | 시스템 사용자 |
| 관리자 | admin | adm, administrator | 관리자 권한 사용자 |
| 권한 | permission | perm | 접근 권한 |
| 역할 | role | - | 사용자 역할 |
| 인증 | auth | authentication | 본인 확인 |
| 인가 | authorization | authz | 권한 확인 |
| 세션 | session | sess | 사용자 세션 |
| 토큰 | token | tok | 인증 토큰 |
| 비밀번호 | password | pwd, pw, passwd | 사용자 비밀번호 |

### 2.4 요청/응답

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 요청 | request | req | HTTP/API 요청 |
| 응답 | response | res, resp | HTTP/API 응답 |
| 메시지 | message | msg | 전달 메시지 |
| 상태 | status | stat | 상태값 |
| 결과 | result | res | 처리 결과 |
| 오류 | error | err | 에러/예외 |
| 성공 | success | succ | 성공 상태 |
| 실패 | failure | fail | 실패 상태 |

### 2.5 시간/날짜

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 생성일시 | created_at | create_dt, crt_dt | 레코드 생성 시간 |
| 수정일시 | updated_at | update_dt, upd_dt | 레코드 수정 시간 |
| 삭제일시 | deleted_at | delete_dt, del_dt | 소프트 삭제 시간 |
| 시작일 | start_date | st_dt, begin_date | 시작 날짜 |
| 종료일 | end_date | ed_dt, finish_date | 종료 날짜 |
| 만료일 | expire_date | exp_dt | 만료 날짜 |
| 타임스탬프 | timestamp | ts | Unix timestamp |

### 2.6 상태/플래그

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 활성 | active | is_active, enabled | 활성 상태 |
| 비활성 | inactive | disabled | 비활성 상태 |
| 삭제됨 | deleted | is_deleted, removed | 삭제 상태 |
| 대기 | pending | wait, waiting | 대기 상태 |
| 진행중 | in_progress | processing | 진행 상태 |
| 완료 | completed | done, finished | 완료 상태 |
| 취소 | canceled | cancelled | 취소 상태 |

---

## 3. 도메인 용어 (Domain Terms)

> 프로젝트별로 이 섹션을 커스터마이즈하세요.

### 3.1 비즈니스 용어

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| 고객 | customer | client, cust | 서비스 이용 고객 |
| 주문 | order | ord | 주문 정보 |
| 결제 | payment | pay | 결제 정보 |
| 상품 | product | prod, item | 판매 상품 |
| 카테고리 | category | cat, ctg | 상품 분류 |
| 가격 | price | prc | 가격 정보 |
| 수량 | quantity | qty | 수량 정보 |
| 재고 | stock | inventory | 재고 정보 |

### 3.2 [프로젝트명] 전용 용어

| 한글 용어 | 권장 영문 | 비권장 표기 | 설명 |
|----------|----------|------------|------|
| (추가) | (추가) | (추가) | (추가) |

---

## 4. 약어 정의 (Abbreviations)

| 약어 | 원래 단어 | 사용 가능 여부 | 설명 |
|------|----------|--------------|------|
| id | identifier | O | 고유 식별자 |
| no | number | O | 번호 (단, `num` 비권장) |
| cnt | count | O | 개수 |
| amt | amount | O | 금액 |
| qty | quantity | O | 수량 |
| dt | date/datetime | X | `_date` 또는 `_at` 사용 권장 |
| nm | name | X | `_name` 전체 사용 권장 |
| cd | code | X | `_code` 전체 사용 권장 |
| yn | yes/no | X | `is_` 또는 `has_` 접두사 권장 |

---

## 5. 네이밍 규칙 (Naming Conventions)

### 5.1 변수/함수명

- **Python**: snake_case (`user_name`, `get_user_list`)
- **JavaScript**: camelCase (`userName`, `getUserList`)
- **클래스**: PascalCase (`UserService`, `OrderController`)
- **상수**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)

### 5.2 DB 테이블/컬럼명

- **테이블**: snake_case, 복수형 (`users`, `orders`)
- **컬럼**: snake_case (`user_id`, `created_at`)
- **PK**: `id` 또는 `{table}_id`
- **FK**: `{참조테이블}_id`

### 5.3 파일명

- **Python**: snake_case (`user_service.py`)
- **JavaScript**: camelCase 또는 kebab-case (`userService.js`, `user-service.js`)
- **설정 파일**: lowercase (`config.py`, `settings.json`)

---

## 6. 체크 예외 목록 (Exceptions)

> 검증 시 제외할 용어를 등록합니다.

| 용어 | 제외 사유 |
|------|----------|
| (예시) tmp | 임시 변수로 허용 |
| (예시) i, j, k | 루프 인덱스로 허용 |
| (예시) e, ex | 예외 변수로 허용 |
| (예시) _ | 미사용 변수 표시로 허용 |

---

## 7. 용어 추가 요청

새로운 용어 등록이 필요한 경우:

1. 이 문서에 직접 추가하거나
2. `doc/d0004_todo.md`에 요청 등록

```markdown
### 용어 추가 요청
- **용어**: [한글 용어]
- **영문 권장**: [영문 표기]
- **비권장 표기**: [피해야 할 표기]
- **설명**: [용어 설명]
- **요청자**: [이름]
- **요청일**: [날짜]
```
