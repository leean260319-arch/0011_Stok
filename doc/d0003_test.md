# d0003_test.md - AI 기반 주식 자동매매 시스템 (StokAI) 테스트 케이스

## 문서 정보
- **문서번호**: d0003
- **서브프로젝트**: StokAI (SP=00)
- **작성일**: 2026-03-16
- **관련 문서**: d0001_prd.md, d0004_todo.md

## 문서이력관리

| 버전 | 날짜 | 변경내용 |
|------|------|----------|
| v02 | 2026-03-16 | E01 F01-01 TDD 완료: TC01-01.T003 (logger 7 PASS), TC01-01.T004 (constants 9 PASS), 총 16 PASS |
| v01 | 2026-03-16 | 초기 생성 (oaisdev run) - PRD v1.3 기준 Part A/B/C/D 구성 |

---

## 1. 개요

이 문서는 AI 기반 주식 자동매매 시스템(StokAI)의 테스트 항목과 결과를 정의합니다.

- **테스트 방법론**: TDD (Red->Green->Refactor->Verify)
- **테스트 실행**: `uv run pytest tests/ -v`
- **관련 문서**: `doc/d0001_prd.md`, `doc/d0004_todo.md`

---

# Part A: 에러체크

> **검사 기준**: `v/guide/common_guide.md` (코드 품질, 보안, 성능 표준)

## 테스트 항목

| ID | 검사 항목 | 도구 |
|----|----------|------|
| A1 | Python 문법 오류 | py_compile |
| A2 | 코드 품질 (PEP8) | pylint, black |
| A3 | 타입 체크 | mypy |
| A4 | 보안 취약점 | 코드 리뷰 |
| A5 | src 모듈 import | import 검사 |

## 실행 결과

| 실행일 | ID | 결과 | 비고 |
|--------|-----|:----:|------|
| - | - | - | (검사 기록 없음) |

**실패 시**: `d0004_todo.md`에 등록

---

# Part B: 시나리오 테스트

> **실행 방법**: `uv run pytest tests/ -m e2e` 또는 수동 테스트

## 테스트 항목

| ID | 시나리오 | PRD 기능 | 우선순위 |
|----|----------|----------|:--------:|
| B1-1 | 키움 API 로그인 및 연결 상태 확인 | F001 | P0 |
| B1-2 | 실시간 시세 수신 (관심종목 등록 후 체결가 수신 확인) | F002 | P0 |
| B1-3 | 시장가/지정가 주문 실행 및 체결 확인 | F003, F005 | P0 |
| B1-4 | 계좌 잔고/예수금/보유 종목 조회 | F004 | P0 |
| B2-1 | 뉴스 크롤링 (네이버 금융/RSS 수집) | F006 | P0 |
| B2-2 | 뉴스 감성분석 (GPT-4o-mini API 호출, 점수 반환) | F007 | P0 |
| B2-3 | 기술적 지표 계산 (RSI, MACD, 볼린저 밴드) | F008 | P0 |
| B2-4 | AI 종합 점수 산출 (감성 + 기술 결합) | F009 | P0 |
| B3-1 | 자동매매 전략 실행 (시그널 발생 -> 주문) | F010 | P0 |
| B3-2 | 리스크 관리 (손절/익절/일일한도/킬스위치) | F011 | P0 |
| B3-3 | 포지션 추적 (보유수량/평균단가/수익률) | F012 | P0 |
| B4-1 | 메인 대시보드 렌더링 (3-Panel 레이아웃) | F013 | P0 |
| B4-2 | 실시간 캔들차트 (시간프레임 전환, 지표 오버레이) | F014 | P0 |
| B4-3 | 뉴스 감성 대시보드 (피드 + 트렌드 차트) | F015 | P0 |
| B5-1 | 세션 영속성 (재시작 후 설정/데이터 복원) | F016 | P0 |
| B5-2 | SQLCipher DB 암호화 저장/복호화 조회 | F017 | P0 |
| B5-3 | keyring 자격증명 저장/조회/삭제 | F018 | P0 |
| B5-4 | 설정 파일 Fernet 암호화/복호화 | F019 | P0 |
| B6-1 | 매매 알림 (체결/시그널/리스크 이벤트) | F020 | P0 |
| B6-2 | 시스템 트레이 (최소화, 백그라운드 실행) | F021 | P0 |
| B7-1 | 계정 설정 UI (계좌번호/비밀번호/API Key 입력) | F022 | P0 |
| B7-2 | 연결 테스트 (6단계 검증) | F023 | P0 |
| B7-3 | 투자 모드 토글 (모의/실전 전환 + 재인증) | F024 | P0 |
| B7-4 | 자격증명 자동 로드 (앱 시작 시) | F025 | P0 |

## 실행 결과

| 실행일 | ID | 결과 | 비고 |
|--------|-----|:----:|------|
| - | - | - | (테스트 기록 없음) |

**실패 시**: `d0004_todo.md`에 등록

---

# Part C: 단위 테스트

> **TC 규칙**: Task <-> TC 1:1 매핑 (F01-01.T001 -> TC01-01.T001)
> **TDD 가이드**: RED -> GREEN -> REFACTOR -> VERIFY

## 테스트 항목

| ID | 테스트명 | 파일 | Task | 상태 |
|----|----------|------|------|:----:|
| TC01-01.T003 | 로깅 모듈 (get_logger, setup_logging, 포맷, UTF-8) | tests/test_logger.py | T003 | PASS |
| TC01-01.T004 | 상수 정의 (APP_NAME, Colors, LLMConfig, RiskDefaults) | tests/test_constants.py | T004 | PASS |

## 실행 결과

| 실행일 | ID | 결과 | 비고 |
|--------|-----|:----:|------|
| - | - | - | (테스트 기록 없음) |

**실패 시**: `d0004_todo.md`에 등록

---

# Part D: src 모듈 테스트

> **실행 방법**: `uv run pytest tests/ -m module` 또는 pytest
> **대상**: src/ 전체 모듈
> **목적**: 모듈 기능 전체 검증

## 테스트 항목

| ID | 모듈 | 함수 수 | 테스트 파일 | 설명 |
|----|------|:-------:|-------------|------|
| D01 | src/db/database.py | - | tests/test_database.py | SQLCipher DB 연결/관리 |
| D02 | src/db/models.py | - | tests/test_models.py | 데이터 모델 (17 테이블) |
| D03 | src/security/credential_manager.py | - | tests/test_credential.py | keyring 자격증명 관리 |
| D04 | src/security/encryption.py | - | tests/test_encryption.py | Fernet 암호화 유틸 |
| D05 | src/bridge/kiwoom_wrapper.py | - | tests/test_kiwoom.py | 키움 API 래퍼 |
| D06 | src/ai/llm_service.py | - | tests/test_llm.py | 클라우드 LLM 연동 |
| D07 | src/ai/news_analyzer.py | - | tests/test_news_analyzer.py | 뉴스 감성분석 |
| D08 | src/engine/strategy_engine.py | - | tests/test_strategy.py | 매매 전략 엔진 |
| D09 | src/engine/risk_manager.py | - | tests/test_risk.py | 4단계 리스크 관리 |
| D10 | src/utils/logger.py | - | tests/test_logger.py | 로깅 모듈 |
| D11 | src/config.py | - | tests/test_config.py | 설정 관리자 |

## 실행 결과

| 실행일 | ID | 결과 | 비고 |
|--------|-----|:----:|------|
| - | - | - | (테스트 기록 없음) |

**실패 시**: `d0004_todo.md`에 등록

---

## 관련 문서

- `doc/d0001_prd.md`: 요구사항 정의서
- `doc/d0002_plan.md`: 구현 계획
- `doc/d0004_todo.md`: TODO 및 디버깅
