# CCone Project - Product Requirements Document (PRD)

## Project Overview

CCone (척척플랫폼)은 법무/세무 업무 자동화 플랫폼입니다. Streamlit 기반 웹 애플리케이션으로, 사업자등록신청, 법인설립, 세무서비스 등의 기능을 제공합니다.

## Current Status

- 모듈 분리 완료: db.py, auth.py, utils.py, ui.py
- 43개 페이지 initialize_page() 적용 완료
- 기본 보안 점검 완료

---

## Tasks

### Task 1: Password Hashing Security Enhancement
- **Priority**: HIGH
- **Status**: WIP
- **Description**: 비밀번호를 해시할 때 hashlib.sha256을 솔트(salt) 없이 사용 중. passlib 라이브러리를 사용하여 솔트 포함 해싱으로 변경 필요
- **Files**:
  - oais/__init__.py
  - 0_02_유저및업체관리_v01.py
  - 9_91_시스템관리.py
  - 9_93_사용자관리_v01.py
- **Details**:
  - 총 8개 위치에서 unsalted SHA256 사용 중
  - 대규모 마이그레이션 필요 (기존 사용자 비밀번호 재해싱 전략 수립 필요)
  - passlib 의존성 추가 및 전체 코드 일괄 수정 필요
- **Acceptance Criteria**:
  - passlib 라이브러리 설치 및 설정
  - 모든 비밀번호 해싱 코드를 passlib로 교체
  - 기존 사용자 비밀번호 마이그레이션 전략 수립 및 적용
  - 신규 사용자 등록 시 솔트 포함 해싱 적용

### Task 2: SQL Injection Prevention
- **Priority**: MEDIUM
- **Status**: PENDING
- **Description**: 24건의 잠재적 SQL 인젝션 패턴을 parameterized query로 개선
- **Files**:
  - 3_31_사업자등록신청_v05(개선중).py (라인 417)
  - 4_41_척척업무관리_v27.py (라인 2585)
  - 8_개발80_DB정보_v01.py (라인 422, 1188, 1192 외)
- **Details**:
  - f-string이나 format으로 SQL 쿼리에 변수 직접 삽입하는 패턴 제거
  - ? placeholder와 파라미터 튜플로 변경
- **Acceptance Criteria**:
  - 모든 SQL 쿼리가 parameterized query 사용
  - SQL 인젝션 취약점 0건

### Task 3: UPSERT Pattern Standardization
- **Priority**: MEDIUM
- **Status**: HOLD
- **Description**: company.py와 customer.py의 UPSERT 패턴 분석 및 필요시 통합
- **Files**:
  - oais/company.py
  - oais/customer.py
- **Details**:
  - 현재 테이블/필드 차이로 각각 구현되어 있음
  - 제네릭 UPSERT 함수 생성 검토
- **Acceptance Criteria**:
  - 패턴 분석 완료
  - 통합 여부 결정 및 문서화

### Task 4: DB Context Manager Implementation
- **Priority**: MEDIUM
- **Status**: HOLD
- **Description**: 데이터베이스 연결을 컨텍스트 매니저로 관리하여 자원 누수 방지
- **Details**:
  - 전체 모듈에 영향
  - 단계적 적용 필요
- **Acceptance Criteria**:
  - DB 컨텍스트 매니저 클래스/함수 생성
  - 최소 1개 모듈에 적용하여 테스트
  - 전체 적용 계획 수립

### Task 5: Configuration Centralization
- **Priority**: LOW
- **Status**: HOLD
- **Description**: 하드코딩된 설정값들을 config.py로 이동
- **Items**:
  - API 타임아웃 (30초) -> API_TIMEOUT
  - 하이픈 API 딜레이 (130초) -> HYPHEN_API_DELAY
  - 최근 게시물 제한 (5건) -> RECENT_POSTS_LIMIT
  - 댓글 목록 제한 (100건) -> COMMENT_LIST_LIMIT
  - 최대 파일 크기 (100MB) -> MAX_FILE_SIZE
  - 날짜 형식 -> DATE_FORMAT, DATETIME_FORMAT
- **Acceptance Criteria**:
  - config.py에 모든 상수 정의
  - 해당 파일들에서 상수 import하여 사용

### Task 6: Utility Functions Enhancement
- **Priority**: LOW
- **Status**: HOLD
- **Description**: 공통 패턴을 유틸리티 함수로 추출
- **Items**:
  - get_current_timestamp() 함수 생성 (utils.py)
  - format_file_size() 함수 활용 확대
  - create_file_uploader() 공통 컴포넌트
  - preview_dataframe() 공통 컴포넌트
- **Acceptance Criteria**:
  - 각 함수 구현 및 테스트
  - 기존 코드에 적용

### Task 7: Test Automation Setup
- **Priority**: LOW
- **Status**: HOLD
- **Description**: E2E 웹 테스트 자동화 환경 구축
- **Details**:
  - 현재 성공률 60% (6/10)
  - 페이지명 불일치로 4개 테스트 실패
  - 페이지명 표준화 필요
- **Acceptance Criteria**:
  - 테스트 대상 페이지명 매핑 정리
  - 성공률 90% 이상 달성

### Task 8: Performance Optimization
- **Priority**: LOW
- **Status**: HOLD
- **Description**: 페이지 응답 시간 최적화
- **Current**: 평균 4초
- **Target**: 2초 이하
- **Acceptance Criteria**:
  - 병목 지점 분석
  - 최적화 적용
  - 평균 응답 시간 2초 이하 달성

### Task 9: Production Environment Security Check
- **Priority**: LOW
- **Status**: HOLD
- **Description**: 운영 환경에서 AUTO_LOGIN 비활성화 확인
- **Acceptance Criteria**:
  - AUTO_LOGIN 환경변수 확인 로직 추가
  - 운영 환경 배포 시 자동 체크

---

## Dependencies

- Task 2 (SQL Injection) can be done independently
- Task 1 (Password Hashing) requires careful migration strategy
- Tasks 3-6 are refactoring tasks that can be done in parallel
- Tasks 7-9 are optimization/infrastructure tasks

## Tech Stack

- Python 3.11+
- Streamlit
- SQLite
- passlib (to be added)

