# d0002_plan.md - AI 기반 주식 자동매매 시스템 (StokAI) 구현 계획

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.3 | 2026-03-17 | 전체 T001~T104 상태를 완료로 업데이트 |
| v1.2 | 2026-03-16 | PRD v1.3 반영 - 로컬 LLM(Ollama) 제거, 클라우드 LLM 전용 구성 (GPT-4o-mini Primary + DeepSeek V3 Fallback) |
| v1.1 | 2026-03-16 | PRD v1.2 반영 - 3-Panel 레이아웃, 다크 테마, 글래스모피즘 카드, Explainable AI UX, 킬 스위치 강화 UX 태스크 추가 (T098~T104), T012/T060/T075 설명 갱신 |
| v1.0 | 2026-03-16 | 신규 작성 - PRD v1.1 기준 전체 Epic/Feature/Task 계획 수립 |

---

## 1. 구현 개요

### 1.1 프로젝트 요약

키움증권 Open API+와 AI(LLM)를 결합하여 뉴스 감성분석 + 기술적 차트 분석 기반의 자동 매수/매도를 수행하는 PyQt6 데스크탑 프로그램을 개발한다. 로컬 암호화 DB(SQLCipher)로 데이터를 영속 저장하고, Windows 자격증명 관리자(keyring)로 민감 정보를 보호한다.

### 1.2 핵심 목표

1. 키움증권 Open API+ 32bit 브릿지 연동 (KOAPY gRPC)
2. PyQt6 기반 트레이딩 대시보드 UI
3. AI 뉴스 감성분석 (클라우드 LLM: GPT-4o-mini + DeepSeek V3 Fallback)
4. pandas-ta 기반 기술적 지표 분석 (150+ 지표)
5. 자동매매 전략 엔진 + 4단계 리스크 관리
6. SQLCipher 암호화 DB + keyring 자격증명 관리
7. 세션 영속성 (프로그램 재시작 시 완전 복원)
8. PyInstaller 데스크탑 배포

### 1.3 기술 스택 요약

| 분류 | 기술 | 버전 | 용도 |
|------|------|------|------|
| 언어 | Python | 3.10+ | 메인(64bit) + 브릿지(32bit) |
| UI | PyQt6 | 6.6+ | 데스크탑 GUI |
| 차트 | lightweight-charts-python | latest | TradingView 캔들차트 |
| 키움 API | KOAPY | latest | gRPC 브릿지 (64bit 호환) |
| 기술분석 | pandas-ta | 0.3.x | 150+ 지표 |
| DB | SQLCipher (sqlcipher3) | 4.x | AES-256 암호화 DB |
| 보안 | keyring, cryptography | latest | 자격증명/설정 암호화 |
| AI (Primary) | GPT-4o-mini | latest | 뉴스 감성분석, 한국어 우수 |
| AI (Fallback) | DeepSeek V3 | latest | GPT 장애 시 자동 전환 |
| 백테스팅 | Backtrader | 1.9.x | 전략 검증 |
| 뉴스 수집 | requests, BS4, feedparser | latest | 크롤링/RSS |
| 배포 | PyInstaller | 6.x | exe 패키징 |
| 패키지 관리 | uv | latest | 의존성 관리 |
| 테스트 | pytest | 7.0+ | 단위/통합 테스트 |

### 1.4 실행 환경

| 항목 | 사양 |
|------|------|
| OS | Windows 10/11 64bit (키움 API 필수) |
| CPU | 4+ cores |
| RAM | 8GB (최소), 16GB (권장) |
| GPU | 불필요 (클라우드 LLM 사용) |
| 네트워크 | 유선 인터넷 (실시간 시세 필수) |
| 키움 계좌 | Open API+ 신청 완료 |

---

## 2. WBS (Epic / Feature / Task)

### E01. 프로젝트 기반 구축

**목표**: 개발 환경, DB, 보안 인프라, 앱 골격 구성

#### F01-01: 개발 환경 설정

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T001 | pyproject.toml 갱신 (PyQt6, keyring, sqlcipher3, pandas-ta, cryptography 등 의존성 추가) | pyproject.toml | 완료 |
| T002 | 프로젝트 디렉토리 구조 생성 (PRD 3.4 기준: src/, src/ui/, src/engine/, src/ai/, src/bridge/, src/security/, src/db/ 등) | 디렉토리 트리 | 완료 |
| T003 | 로깅 모듈 구현 (파일 + 콘솔 동시 출력, 일별 로테이션, UTF-8) | src/utils/logger.py | 완료 |
| T004 | 상수 정의 (서비스명, 경로, 기본값, 색상 코드 등) | src/utils/constants.py | 완료 |

#### F01-02: 암호화 DB 구축 (SQLCipher)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T005 | SQLCipher DB 연결 매니저 구현 (AES-256-CBC, PBKDF2 256K 반복, WAL 모드) | src/db/database.py | 대기 |
| T006 | 데이터 모델 정의 (PRD 7.2 전체 17개 테이블 스키마) | src/db/models.py | 대기 |
| T007 | 스키마 마이그레이션 모듈 (버전 관리, 자동 업그레이드) | src/db/migrations.py | 대기 |
| T008 | DB 초기화 스크립트 (첫 실행 시 테이블 자동 생성) | src/db/database.py 내 init_db() | 대기 |

#### F01-03: 보안 인프라 (keyring + Fernet)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T009 | 자격증명 매니저 구현 (keyring: 저장/조회/삭제, 서비스명 "StokAI") | src/security/credential_manager.py | 완료 |
| T010 | 암호화 유틸리티 (Fernet 대칭키 암호화/복호화, 키 생성/관리) | src/security/encryption.py | 완료 |
| T011 | 앱 잠금 기능 (PIN/비밀번호, 30분 미사용 자동잠금) | src/security/app_lock.py | 완료 |

#### F01-04: PyQt6 앱 골격

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T012 | 메인 윈도우 프레임 (QMainWindow, 3-Panel QSplitter 레이아웃, 메뉴바, 상태바, 패널 접기/펼치기/팝아웃) | src/app.py | 완료 |
| T013 | 앱 진입점 (QApplication 초기화, 이벤트 루프, 시스템 트레이) | src/main.py | 완료 |
| T014 | 설정 관리자 (JSON 설정 파일 읽기/쓰기, 기본값 관리) | src/config.py | 완료 |
| T015 | 세션 영속성 매니저 (창 위치/크기, 열린 탭, 마지막 종목 등 DB 저장/복원) | src/utils/session_manager.py | 완료 |
| T016 | 시스템 트레이 아이콘 (최소화, 백그라운드 실행, 우클릭 메뉴) | src/app.py 내 SystemTray | 완료 |

---

### E02. 키움 API 연동

**목표**: 32bit/64bit 브릿지 구축, 실시간 시세 수신, 주문 실행

#### F02-01: 32bit gRPC 브릿지

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T017 | KOAPY 기반 gRPC 서버 (32bit Python, 키움 OCX 래핑) | src/bridge/kiwoom_server.py | 완료 |
| T018 | gRPC 클라이언트 (64bit Python, 서버와 통신) | src/bridge/kiwoom_bridge.py | 완료 |
| T019 | API 래퍼 (로그인, 시세조회, 주문, 잔고 등 고수준 인터페이스) | src/bridge/kiwoom_wrapper.py | 완료 |
| T020 | API 스로틀러 (초당 5회, 시간당 1,000회 제한 자동 준수) | src/bridge/kiwoom_wrapper.py 내 APIThrottler | 완료 |

#### F02-02: 실시간 데이터 수신

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T021 | 실시간 시세 수신 (체결가, 호가, 거래량) | src/bridge/kiwoom_wrapper.py 내 register_realtime() | 완료 |
| T022 | 이벤트 큐 구현 (asyncio.Queue 기반, 시세→전략 엔진/UI 분배) | src/engine/event_queue.py | 완료 |
| T023 | 자동 재연결 (연결 끊김 감지, 최대 3회 재시도) | src/bridge/kiwoom_wrapper.py 내 auto_reconnect() | 완료 |

#### F02-03: 주문/계좌 관리

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T024 | 주문 실행 (시장가/지정가 매수/매도, 호가 단위 검증) | src/bridge/kiwoom_wrapper.py 내 send_order() | 완료 |
| T025 | 체결 확인 (실시간 체결/미체결 수신, 포지션 자동 업데이트) | src/bridge/kiwoom_wrapper.py 내 on_chejan() | 완료 |
| T026 | 잔고 조회 (예수금, 보유 종목, 평가 금액) | src/bridge/kiwoom_wrapper.py 내 get_balance() | 완료 |

---

### E03. 계정 설정 UI (M15)

**목표**: PRD 5.2.5 기반 계정 설정 페이지 완전 구현

#### F03-01: 계정 설정 페이지 UI

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T027 | 계정 설정 페이지 레이아웃 (PyQt6 QWidget, 4개 섹션 그룹박스) | src/ui/settings_view.py | 대기 |
| T028 | 투자 모드 토글 스위치 (커스텀 QWidget, 애니메이션, 모의=파랑/실전=빨강) | src/ui/widgets/toggle_switch.py | 대기 |
| T029 | 계좌 입력 폼 (계좌번호 QLineEdit + 정규식, 비밀번호/API Key echoMode=Password) | src/ui/settings_view.py 내 AccountForm | 대기 |
| T030 | 비밀번호 보기 토글 (눈 아이콘 QAction, echoMode 전환) | src/ui/settings_view.py 내 PasswordToggle | 대기 |
| T031 | 연결 상태 표시 패널 (API연결/계좌/서버/마지막 연결 시각) | src/ui/settings_view.py 내 StatusPanel | 대기 |
| T032 | 보안 저장소 상태 표시 (keyring 저장 항목 수, 마지막 저장 시각) | src/ui/settings_view.py 내 SecurityPanel | 대기 |

#### F03-02: 연결 테스트 및 자격증명 관리

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T033 | 연결 테스트 로직 (PRD 6단계: 입력 검증→API 초기화→로그인→계좌 조회→성공→해제) | src/ui/settings_view.py 내 test_connection() | 대기 |
| T034 | keyring 저장/불러오기/삭제 (credential_manager 연동, 앱 시작 시 자동 로드) | src/ui/settings_view.py 내 save/load/clear_credentials() | 대기 |
| T035 | 실전투자 전환 재인증 (QDialog 비밀번호 확인 팝업) | src/ui/settings_view.py 내 confirm_live_mode() | 대기 |
| T036 | 에러 처리 (7가지 에러 시나리오: 미설치/로그인실패/계좌불일치/네트워크/타임아웃/keyring실패/중복로그인) | src/ui/settings_view.py 내 에러 핸들링 | 대기 |

---

### E04. 뉴스 수집 및 AI 감성분석

**목표**: 뉴스 크롤링 + LLM 감성분석 파이프라인 구축

#### F04-01: 뉴스 크롤러

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T037 | 네이버 금융 뉴스 크롤러 (requests + BS4, User-Agent 설정, 종목별 뉴스) | src/crawler/naver_crawler.py | 대기 |
| T038 | RSS 피드 크롤러 (한경, 연합뉴스 등 feedparser 기반) | src/crawler/rss_crawler.py | 대기 |
| T039 | 뉴스 통합 관리자 (중복 제거, 갱신 주기 관리, DB 저장) | src/crawler/news_manager.py | 대기 |

#### F04-02: LLM 감성분석 엔진

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T040 | LLM 서비스 추상화 (API/로컬 공통 인터페이스, 모델 전환) | src/ai/llm_service.py | 대기 |
| T041 | 클라우드 LLM 연동 (GPT-4o-mini Primary + DeepSeek V3 Fallback, 자동 전환 로직) | src/ai/llm_service.py 내 CloudLLMProvider | 대기 |
| T043 | 뉴스 감성분석기 (프롬프트 설계, JSON 파싱, 감성 점수 -1.0~+1.0) | src/ai/news_analyzer.py | 대기 |
| T044 | 감성 점수 집계 (종목별 시간 가중 평균, 최근 뉴스 가중치 부여) | src/ai/sentiment_scorer.py | 대기 |

---

### E05. 기술적 분석 엔진

**목표**: pandas-ta 기반 기술적 지표 계산 및 시그널 생성

#### F05-01: 기술적 지표 계산

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T045 | 차트 분석기 (pandas-ta 래퍼, OHLCV DataFrame 입력, 지표 일괄 계산) | src/ai/chart_analyzer.py | 대기 |
| T046 | 기본 지표 구현 (SMA, EMA, RSI, MACD, 볼린저 밴드, 스토캐스틱, 거래량 MA) | src/ai/chart_analyzer.py 내 calc_basic_indicators() | 대기 |
| T047 | 확장 지표 구현 (ADX, ATR, OBV, 일목균형표, 피봇 포인트) | src/ai/chart_analyzer.py 내 calc_extended_indicators() | 대기 |

#### F05-02: AI 종합 점수 산출

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T048 | 기술적 시그널 생성 (RSI/MACD/볼린저/거래량/이평선 → +1/-1/0 시그널) | src/engine/signal_generator.py | 대기 |
| T049 | AI 종합 점수 엔진 (감성 30% + 기술 70% 가중 합산, -1.0~+1.0 정규화) | src/engine/signal_generator.py 내 calc_composite_score() | 대기 |

---

### E06. 매매 전략 엔진

**목표**: 자동매매 전략 실행 + 4단계 리스크 관리

#### F06-01: 전략 엔진

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T050 | 전략 기반 클래스 (Strategy 추상 클래스, on_signal/on_tick/on_order 인터페이스) | src/engine/strategy_engine.py | 대기 |
| T051 | AI 종합 전략 (종합 점수 >= 0.6 매수, <= -0.3 매도) | src/engine/strategy_engine.py 내 AICompositeStrategy | 대기 |
| T052 | 모멘텀 전략 (RSI < 30 + MACD 골든크로스 진입) | src/engine/strategy_engine.py 내 MomentumStrategy | 대기 |
| T053 | 평균 회귀 전략 (볼린저 밴드 하단 터치 진입) | src/engine/strategy_engine.py 내 MeanReversionStrategy | 대기 |
| T054 | 전략 실행 루프 (이벤트 큐 수신 → 전략 평가 → 리스크 검증 → 주문) | src/engine/strategy_engine.py 내 run() | 대기 |

#### F06-02: 리스크 관리 4단계

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T055 | 1단계: 개별 주문 검증 (최대 주문 금액, 슬리피지, 호가 단위) | src/engine/risk_manager.py 내 validate_order() | 대기 |
| T056 | 2단계: 포트폴리오 검증 (종목 집중도 30%, 섹터 편중 50%) | src/engine/risk_manager.py 내 validate_portfolio() | 대기 |
| T057 | 3단계: 계좌 검증 (일일 손실 3%, 주간 5%, 월간 10%, 최소 예수금 20%) | src/engine/risk_manager.py 내 validate_account() | 대기 |
| T058 | 4단계: 시스템 안전장치 (MDD 15% 킬 스위치, API 끊김 차단, 장 마감 전 차단) | src/engine/risk_manager.py 내 system_safeguard() | 대기 |
| T059 | 킬 스위치 (수동/자동 발동, 미체결 전 취소, 수동 해제만 허용) | src/engine/risk_manager.py 내 kill_switch() | 대기 |

---

### E07. UI 대시보드

**목표**: PyQt6 기반 트레이딩 대시보드 전체 UI 구현

#### F07-01: 메인 대시보드 (M01)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T060 | 계좌 요약 글래스모피즘 카드 (총자산, 수익률, 예수금, 반투명 블러 효과) | src/ui/dashboard.py 내 AccountSummary | 대기 |
| T061 | 당일 손익 글래스모피즘 카드 (실현/미실현 손익, 미니 차트, 수익률 컬러 코딩) | src/ui/dashboard.py 내 DailyPnL | 대기 |
| T062 | 자동매매 상태 표시 (실행 중 전략, 체결 현황) | src/ui/dashboard.py 내 AutoTradeStatus | 대기 |
| T063 | AI 시장 심리 게이지 (뉴스 감성 게이지 차트, Explainable AI 근거 툴팁) | src/ui/dashboard.py 내 SentimentGauge | 대기 |
| T064 | 주요 지수 미니 차트 (KOSPI/KOSDAQ 실시간) | src/ui/dashboard.py 내 IndexMiniChart | 대기 |

#### F07-02: 차트 분석 뷰 (M02)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T065 | 실시간 캔들차트 (lightweight-charts-python + PyQt6 WebEngine 임베드) | src/ui/chart_view.py | 대기 |
| T066 | 기술적 지표 오버레이 (MA, 볼린저 밴드, 일목균형표) | src/ui/chart_view.py 내 add_overlay() | 대기 |
| T067 | 보조 지표 패널 (RSI, MACD, 스토캐스틱 하단 차트) | src/ui/chart_view.py 내 SubIndicatorPanel | 대기 |
| T068 | 시간 프레임 전환 (1분/5분/15분/일/주/월 탭) | src/ui/chart_view.py 내 TimeframeSelector | 대기 |
| T069 | 매매 시그널 마커 (차트 위 매수/매도 삼각형 오버레이) | src/ui/chart_view.py 내 add_trade_markers() | 대기 |

#### F07-03: 뉴스 분석 뷰 (M03)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T070 | 실시간 뉴스 피드 리스트 (종목별/전체 필터, 감성 컬러 뱃지) | src/ui/news_view.py | 대기 |
| T071 | 감성 트렌드 차트 (시간별 감성 점수 변화 라인 차트) | src/ui/news_view.py 내 SentimentTrendChart | 대기 |
| T072 | 뉴스 요약 패널 (AI 3줄 요약 표시) | src/ui/news_view.py 내 NewsSummaryPanel | 대기 |

#### F07-04: 자동매매 관리 뷰 (M05)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T073 | 전략 목록 + 실행 토글 (등록된 전략 리스트, on/off 스위치) | src/ui/trade_view.py 내 StrategyList | 대기 |
| T074 | 실시간 매매 로그 (시그널/주문/체결 이벤트 실시간 로그) | src/ui/trade_view.py 내 TradeLog | 대기 |
| T075 | 킬 스위치 강화 UI (2초 길게 누르기/슬라이드 활성화, 원형 프로그래스 애니메이션, 깜박이는 펄스, Ctrl+Shift+K 단축키) | src/ui/widgets/kill_switch.py | 대기 |
| T076 | 일일 손실 한도 프로그래스 바 (현재 손실/한도 비율 표시) | src/ui/trade_view.py 내 LossLimitBar | 대기 |

#### F07-05: 포트폴리오 뷰 (M08)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T077 | 보유 종목 테이블 (종목명, 수량, 평균단가, 현재가, 수익률, 평가금액) | src/ui/portfolio_view.py | 대기 |
| T078 | 자산 배분 파이차트 (종목별/섹터별 비중) | src/ui/portfolio_view.py 내 AllocationChart | 대기 |
| T079 | 수익률 추이 차트 (일별/월별 누적 수익률) | src/ui/portfolio_view.py 내 ReturnChart | 대기 |

#### F07-06: 관심 종목 뷰 (M13)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T080 | 관심 종목 그룹 관리 (그룹 생성/삭제, 종목 추가/제거) | src/ui/watchlist_view.py | 대기 |
| T081 | 실시간 모니터링 테이블 (현재가, 등락률, 거래량, AI 점수 실시간 갱신) | src/ui/watchlist_view.py 내 RealtimeTable | 대기 |

#### F07-07: 알림 센터 (M14)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T082 | 알림 센터 뷰 (매매/분석/시스템 알림 분류, 읽음/안읽음) | src/ui/alert_view.py | 대기 |
| T083 | 팝업 알림 (체결/킬스위치 등 긴급 이벤트 토스트 알림) | src/ui/widgets/toast_notification.py | 대기 |

#### F07-08: AI/매매 설정 뷰 (M16, M17)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T084 | AI 설정 페이지 (GPT-4o-mini/DeepSeek V3 전환, API 키 관리, 연결 테스트) | src/ui/ai_settings_view.py | 대기 |
| T085 | 매매 설정 페이지 (리스크 한도, 매매 규칙, 알림 설정) | src/ui/trade_settings_view.py | 대기 |

#### F07-09: 3-Panel 레이아웃 및 UI 테마 (신규)

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T098 | 3-Panel QSplitter 레이아웃 프레임 (L-Panel 250px/Center 가변/R-Panel 300px, 패널 접기/펼치기, 크기 비율 세션 저장) | src/ui/panels/panel_layout.py | 대기 |
| T099 | L-Panel 네비게이션 위젯 (아이콘+텍스트 메뉴, 관심종목 리스트, 종목 인크리멘털 검색, 시장 지수 스파크라인) | src/ui/panels/left_panel.py | 대기 |
| T100 | R-Panel 컨트롤 위젯 (킬 스위치 상단 고정, 주문 폼, AI 시그널 카드, 매매 로그, 계좌 요약) | src/ui/panels/right_panel.py | 대기 |
| T101 | 다크 테마 QSS 스타일시트 (PRD 13.3 컬러 팔레트 적용, 테마 변수 관리 구조) | src/ui/themes/dark_theme.qss | 대기 |
| T102 | 글래스모피즘 카드 베이스 위젯 (반투명 배경, 블러 효과, 둥근 모서리, 그림자) | src/ui/widgets/glass_card.py | 대기 |
| T103 | Explainable AI 시그널 카드 (매수/매도/관망 판단 + 근거 요약 + 신뢰도 게이지 + 호버 상세 팝업) | src/ui/widgets/ai_signal_card.py | 대기 |
| T104 | AI 처리 상태 표시 위젯 (스피너, 진행률 바, 상태바 통합, 에러 시 재시도 버튼) | src/ui/widgets/ai_status_indicator.py | 대기 |

---

### E08. 백테스팅

**목표**: 과거 데이터로 매매 전략 수익률 검증

#### F08-01: 백테스팅 엔진

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T086 | Backtrader 통합 (전략 클래스를 Backtrader Strategy로 변환) | src/engine/backtest_engine.py | 대기 |
| T087 | 과거 데이터 로더 (키움 API 일봉/분봉 데이터 → Backtrader DataFeed) | src/engine/backtest_engine.py 내 KiwoomDataFeed | 대기 |
| T088 | 백테스팅 결과 분석 (수익률, MDD, 승률, 샤프비율, DB 저장) | src/engine/backtest_engine.py 내 analyze_result() | 대기 |

#### F08-02: 백테스팅 UI

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T089 | 백테스팅 뷰 (전략 선택, 기간 설정, 실행 버튼, 결과 차트) | src/ui/backtest_view.py | 대기 |
| T090 | 백테스팅 결과 시각화 (누적 수익률, 드로다운 차트, 매매 포인트) | src/ui/backtest_view.py 내 BacktestChart | 대기 |

---

### E09. 데이터 관리 및 내보내기

**목표**: DB 백업/복원, 데이터 내보내기, 자동 저장

#### F09-01: 데이터 관리

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T091 | DB 백업/복원 (암호화 DB 파일 복사, 복원 시 무결성 검증) | src/db/database.py 내 backup()/restore() | 대기 |
| T092 | 데이터 내보내기 (매매 이력/분석 결과 CSV/Excel 내보내기) | src/utils/exporter.py | 대기 |
| T093 | 자동 저장 (5분 주기 세션 상태 자동 저장, 비정상 종료 대비) | src/utils/session_manager.py 내 auto_save() | 대기 |
| T094 | 데이터 보존 정책 적용 (분봉 90일, 뉴스 180일, AI분석 365일 자동 정리) | src/db/database.py 내 cleanup_old_data() | 대기 |

---

### E10. 배포 및 최초 실행

**목표**: PyInstaller 패키징, 설정 마법사, 자동 업데이트 확인

#### F10-01: 데스크탑 배포

| Task | 설명 | 산출물 | 상태 |
|------|------|--------|------|
| T095 | PyInstaller 빌드 스크립트 (64bit 메인 앱 + 32bit 브릿지 분리 빌드) | build.py / StokAI.spec | 대기 |
| T096 | 최초 실행 설정 마법사 (4단계: 앱 비밀번호 → 키움 API → AI 설정 → 매매 설정) | src/ui/setup_wizard.py | 대기 |
| T097 | 자동 업데이트 확인 (GitHub Releases API, 버전 비교, 다운로드 안내) | src/utils/updater.py | 대기 |

---

## 3. 스프린트 계획

| 스프린트 | 기간 | Epic | Feature | 주요 산출물 | 상태 |
|---------|------|------|---------|-----------|------|
| S01 | 1~2주차 | E01 | F01-01~04 | 개발환경, DB, 보안, 앱 골격 | 대기 |
| S02 | 3~4주차 | E02 | F02-01~03 | 키움 API 브릿지, 시세 수신, 주문 | 대기 |
| S03 | 5주차 | E03 | F03-01~02 | 계정 설정 UI, 연결 테스트, keyring | 대기 |
| S04 | 6~7주차 | E04 | F04-01~02 | 뉴스 크롤러, LLM 감성분석 | 대기 |
| S05 | 8주차 | E05 | F05-01~02 | 기술적 지표, AI 종합 점수 | 대기 |
| S06 | 9~10주차 | E06 | F06-01~02 | 매매 전략 엔진, 리스크 관리 4단계 | 대기 |
| S07 | 11~13주차 | E07 | F07-01~09 | 3-Panel 레이아웃, 다크테마, 대시보드/차트/뉴스/매매/포트폴리오 UI, 글래스모피즘 카드, Explainable AI UX | 대기 |
| S08 | 14주차 | E08 | F08-01~02 | 백테스팅 엔진 + UI | 대기 |
| S09 | 15주차 | E09 | F09-01 | DB 백업, 내보내기, 자동 저장 | 대기 |
| S10 | 16주차 | E10 | F10-01 | PyInstaller 배포, 설정 마법사 | 대기 |

### 크리티컬 패스

```
E01(기반) → E02(키움API) → E03(계정설정) → E05(기술분석) → E06(전략엔진) → E07(UI)
                                              ↑
                              E04(뉴스/AI) ---+
```

- E01 → E02: DB/보안 인프라가 API 연동의 전제
- E02 → E03: API 래퍼가 있어야 연결 테스트 구현 가능
- E04, E05 → E06: 감성 + 기술 분석이 전략 엔진의 입력
- E06 → E07: 전략 엔진이 매매 UI의 백엔드
- E04와 E05는 병렬 진행 가능

---

## 4. 기술 설계

### 4.1 src/ 모듈 설계

| 디렉토리 | 파일 | 역할 |
|---------|------|------|
| src/ | main.py | 앱 진입점 (QApplication, 이벤트 루프) |
| src/ | app.py | 메인 윈도우 (QMainWindow, 탭 네비게이션, 시스템 트레이) |
| src/ | config.py | 설정 관리자 (JSON 읽기/쓰기) |
| src/bridge/ | kiwoom_server.py | 32bit gRPC 서버 (키움 OCX) |
| src/bridge/ | kiwoom_bridge.py | 64bit gRPC 클라이언트 |
| src/bridge/ | kiwoom_wrapper.py | API 고수준 래퍼 (로그인, 시세, 주문, 스로틀러) |
| src/engine/ | event_queue.py | 이벤트 큐 (시세→전략/UI 분배) |
| src/engine/ | strategy_engine.py | 전략 기반 클래스 + 기본 전략 3종 |
| src/engine/ | risk_manager.py | 리스크 관리 4단계 + 킬 스위치 |
| src/engine/ | signal_generator.py | 기술적 시그널 + AI 종합 점수 |
| src/engine/ | backtest_engine.py | Backtrader 통합 |
| src/ai/ | llm_service.py | LLM 서비스 추상화 (API/로컬) |
| src/ai/ | news_analyzer.py | 뉴스 감성분석 (프롬프트, 점수화) |
| src/ai/ | chart_analyzer.py | pandas-ta 기술적 지표 계산 |
| src/ai/ | sentiment_scorer.py | 종목별 감성 점수 집계 |
| src/crawler/ | naver_crawler.py | 네이버 금융 뉴스 크롤링 |
| src/crawler/ | rss_crawler.py | RSS 피드 수집 |
| src/crawler/ | news_manager.py | 뉴스 통합 관리 (중복 제거, DB 저장) |
| src/ui/ | dashboard.py | 메인 대시보드 (M01) |
| src/ui/ | chart_view.py | 차트 분석 (M02) |
| src/ui/ | news_view.py | 뉴스 분석 (M03) |
| src/ui/ | trade_view.py | 자동매매 관리 (M05) |
| src/ui/ | portfolio_view.py | 포트폴리오 (M08) |
| src/ui/ | watchlist_view.py | 관심 종목 (M13) |
| src/ui/ | alert_view.py | 알림 센터 (M14) |
| src/ui/ | settings_view.py | 계정 설정 (M15) |
| src/ui/ | ai_settings_view.py | AI 설정 (M16) |
| src/ui/ | trade_settings_view.py | 매매 설정 (M17) |
| src/ui/ | backtest_view.py | 백테스팅 (M10) |
| src/ui/ | setup_wizard.py | 최초 실행 설정 마법사 |
| src/ui/widgets/ | toggle_switch.py | 커스텀 토글 스위치 위젯 |
| src/ui/widgets/ | toast_notification.py | 토스트 알림 위젯 |
| src/ui/widgets/ | glass_card.py | 글래스모피즘 카드 베이스 위젯 |
| src/ui/widgets/ | kill_switch.py | 킬 스위치 강화 UX 위젯 |
| src/ui/widgets/ | ai_signal_card.py | Explainable AI 시그널 카드 |
| src/ui/widgets/ | ai_status_indicator.py | AI 처리 상태 표시 위젯 |
| src/ui/panels/ | panel_layout.py | 3-Panel QSplitter 레이아웃 프레임 |
| src/ui/panels/ | left_panel.py | L-Panel 네비게이션 (메뉴, 관심종목, 검색) |
| src/ui/panels/ | right_panel.py | R-Panel 컨트롤 (킬스위치, 주문, AI시그널, 로그) |
| src/ui/themes/ | dark_theme.qss | 다크 테마 QSS 스타일시트 |
| src/db/ | database.py | SQLCipher DB 연결/관리 |
| src/db/ | models.py | 17개 테이블 스키마 |
| src/db/ | migrations.py | 스키마 마이그레이션 |
| src/security/ | credential_manager.py | keyring 자격증명 관리 |
| src/security/ | encryption.py | Fernet 암호화 유틸리티 |
| src/security/ | app_lock.py | 앱 잠금 |
| src/utils/ | logger.py | 로깅 |
| src/utils/ | constants.py | 상수 정의 |
| src/utils/ | helpers.py | 헬퍼 함수 |
| src/utils/ | session_manager.py | 세션 영속성 |
| src/utils/ | exporter.py | CSV/Excel 내보내기 |
| src/utils/ | updater.py | 자동 업데이트 확인 |

### 4.2 데이터 흐름

```
[키움 API (32bit)]
       |
       v (gRPC)
[kiwoom_bridge.py] ---> [event_queue.py]
                              |
                    +---------+---------+
                    |                   |
              [strategy_engine.py] [UI 갱신 (PyQt Signal)]
                    |
            +-------+-------+
            |               |
   [risk_manager.py]  [signal_generator.py]
            |               |
            |         +-----+-----+
            |         |           |
            |  [news_analyzer.py] [chart_analyzer.py]
            |  (LLM 감성분석)      (pandas-ta 지표)
            |         |           |
            |  [sentiment_scorer] [기술 시그널]
            |         |           |
            |         +-----+-----+
            |               |
            |     [AI 종합 점수]
            |
   [주문 실행] ---> [kiwoom_wrapper.py]
            |
   [체결 확인] ---> [DB 저장 (SQLCipher)]
```

### 4.3 의존성 방향

```
UI Layer (src/ui/)
    |
    v
Engine Layer (src/engine/)
    |
    +---> AI Layer (src/ai/)
    |
    +---> Crawler Layer (src/crawler/)
    |
    v
Bridge Layer (src/bridge/)
    |
    v
Data Layer (src/db/, src/security/)
    |
    v
Utils Layer (src/utils/)
```

> 하위 레이어는 상위 레이어를 import하지 않음 (단방향 의존)

---

## 5. 리스크 관리

| 리스크 | 확률 | 영향 | 대응 방안 |
|--------|------|------|---------|
| 키움 API 32bit 브릿지 불안정 | 중간 | 높음 | KOAPY 대신 pykiwoom 32bit 직접 사용 대안 준비 |
| PyQt6 + lightweight-charts 통합 이슈 | 중간 | 중간 | QWebEngineView 임베드 또는 Plotly 대안 |
| SQLCipher Windows 빌드 실패 | 중간 | 높음 | SQLite + Fernet 컬럼 암호화 대안 |
| 키움 API 동시 접속 제한 (1대) | 높음 | 중간 | 모의/실전 분리 실행, HTS 동시 사용 불가 안내 |
| LLM API 비용 초과 | 낮음 | 낮음 | DeepSeek V3 Fallback 자동 전환, 일일 호출 한도 설정 |
| 뉴스 크롤링 차단 (네이버) | 중간 | 중간 | RSS 피드 우선 사용, 네이버 검색 API 대안 |
| PyInstaller 빌드 크기 과다 (500MB+) | 높음 | 낮음 | --exclude-module로 불필요 의존성 제거, UPX 압축 |
| 장중 앱 크래시 | 낮음 | 높음 | 자동 저장 5분 주기, WAL 모드 DB 무결성, 킬 스위치 자동 발동 |
| 개인정보 유출 | 낮음 | 매우높음 | 3층 암호화, keyring, 역컴파일 방지(Nuitka 검토) |

---

## 6. 의사결정 기록

| 날짜 | 결정 사항 | 이유 |
|------|---------|------|
| 2026-03-16 | UI 프레임워크: PyQt6 (Streamlit 대신) | 키움 API가 PyQt 기반, 실시간 업데이트 완전 지원, 데스크탑 앱 요구사항 |
| 2026-03-16 | 키움 API 연동: KOAPY gRPC 브릿지 | 64bit Python 호환으로 AI/ML 라이브러리 제약 없음 |
| 2026-03-16 | 차트: lightweight-charts-python | TradingView 스타일, PyQt 통합 지원, 캔들차트 최적화 |
| 2026-03-16 | DB: SQLCipher | 전체 파일 암호화로 개인정보 보호, SQLite API 완전 호환 |
| 2026-03-16 | Primary AI: GPT-4o-mini | 월 $0.23 최저 비용, 한국어 감성분석 우수, API 안정성 99.9% |
| 2026-03-16 | Fallback AI: DeepSeek V3 | GPT 장애 시 자동 전환, 가성비 우수 |
| 2026-03-16 | 기술분석: pandas-ta (TA-Lib 대신) | pip install만으로 설치, C 빌드 불필요, 150+ 지표 동일 |
| 2026-03-16 | 백테스팅: Backtrader | 입문 용이, 라이브 트레이딩 지원, 충분한 기능 |
| 2026-03-16 | 리스크 관리: 4단계 계층형 | 개별 주문→포트폴리오→계좌→시스템 순차 검증으로 중복 안전장치 |
| 2026-03-16 | 배포: PyInstaller (Nuitka 대신) | 빌드 간편, C 툴체인 불필요, 검증된 안정성 |

---

## 7. 진행 추적

| Task | 담당 | 상태 | 완료일 | 비고 |
|------|------|------|--------|------|
| T001 | - | 완료 | 2026-03-16 | pyproject.toml 갱신 |
| T002 | - | 완료 | 2026-03-16 | 디렉토리 구조 생성 |
| T003 | - | 완료 | 2026-03-16 | 로깅 모듈 (7 PASS) |
| T004 | - | 완료 | 2026-03-16 | 상수 정의 (9 PASS) |
| T005 | - | 완료 | 2026-03-16 | SQLCipher DB 매니저 (19 PASS) |
| T006 | - | 완료 | 2026-03-16 | 17개 테이블 스키마 |
| T007 | - | 완료 | 2026-03-16 | 마이그레이션 모듈 |
| T008 | - | 완료 | 2026-03-16 | DB 초기화 |
| T009 | - | 완료 | 2026-03-16 | keyring 자격증명 (14 PASS) |
| T010 | - | 완료 | 2026-03-16 | Fernet 암호화 유틸 (14 PASS) |
| T011 | - | 완료 | 2026-03-16 | 앱 잠금 (15 PASS) |
| T012 | - | 완료 | 2026-03-16 | 메인 윈도우 3-Panel (13 PASS) |
| T013 | - | 완료 | 2026-03-16 | 앱 진입점 (3 PASS) |
| T014 | - | 완료 | 2026-03-16 | 설정 관리자 |
| T015 | - | 완료 | 2026-03-16 | 세션 영속성 (5 PASS) |
| T016 | - | 완료 | 2026-03-16 | 시스템 트레이 (4 PASS) |
| T017 | - | 완료 | 2026-03-17 | gRPC 서버 (15 PASS) |
| T018 | - | 완료 | 2026-03-17 | gRPC 클라이언트 (19 PASS) |
| T019 | - | 완료 | 2026-03-17 | API 래퍼 |
| T020 | - | 완료 | 2026-03-17 | API 스로틀러 (43 PASS) |
| T021 | - | 완료 | 2026-03-17 | 실시간 시세 수신 |
| T022 | - | 완료 | 2026-03-17 | 이벤트 큐 (21 PASS) |
| T023 | - | 완료 | 2026-03-17 | 자동 재연결 |
| T024 | - | 완료 | 2026-03-17 | 주문 실행 |
| T025 | - | 완료 | 2026-03-17 | 체결 확인 |
| T026 | - | 완료 | 2026-03-17 | 잔고 조회 |
| T027 | - | 완료 | 2026-03-17 | 계정 설정 레이아웃 |
| T028 | - | 완료 | 2026-03-17 | 토글 스위치 위젯 |
| T029 | - | 완료 | 2026-03-17 | 계좌 입력 폼 |
| T030 | - | 완료 | 2026-03-17 | 비밀번호 보기 토글 |
| T031 | - | 완료 | 2026-03-17 | 연결 상태 패널 |
| T032 | - | 완료 | 2026-03-17 | 보안 저장소 상태 |
| T033 | - | 완료 | 2026-03-17 | 연결 테스트 6단계 |
| T034 | - | 완료 | 2026-03-17 | keyring CRUD |
| T035 | - | 완료 | 2026-03-17 | 실전 전환 재인증 |
| T036 | - | 완료 | 2026-03-17 | 에러 처리 7종 |
| T037 | - | 완료 | 2026-03-17 | 네이버 뉴스 크롤러 |
| T038 | - | 완료 | 2026-03-17 | RSS 크롤러 |
| T039 | - | 완료 | 2026-03-17 | 뉴스 통합 관리 |
| T040 | - | 완료 | 2026-03-17 | LLM 서비스 추상화 |
| T041 | - | 완료 | 2026-03-17 | API LLM 연동 |
| T043 | - | 완료 | 2026-03-17 | 뉴스 감성분석기 |
| T044 | - | 완료 | 2026-03-17 | 감성 점수 집계 |
| T045 | - | 완료 | 2026-03-17 | 차트 분석기 |
| T046 | - | 완료 | 2026-03-17 | 기본 지표 6종 |
| T047 | - | 완료 | 2026-03-17 | 확장 지표 5종 |
| T048 | - | 완료 | 2026-03-17 | 기술적 시그널 생성 |
| T049 | - | 완료 | 2026-03-17 | AI 종합 점수 |
| T050 | - | 완료 | 2026-03-17 | 전략 기반 클래스 |
| T051 | - | 완료 | 2026-03-17 | AI 종합 전략 |
| T052 | - | 완료 | 2026-03-17 | 모멘텀 전략 |
| T053 | - | 완료 | 2026-03-17 | 평균 회귀 전략 |
| T054 | - | 완료 | 2026-03-17 | 전략 실행 루프 |
| T055 | - | 완료 | 2026-03-17 | 리스크 1단계: 주문 |
| T056 | - | 완료 | 2026-03-17 | 리스크 2단계: 포트폴리오 |
| T057 | - | 완료 | 2026-03-17 | 리스크 3단계: 계좌 |
| T058 | - | 완료 | 2026-03-17 | 리스크 4단계: 시스템 |
| T059 | - | 완료 | 2026-03-17 | 킬 스위치 |
| T060 | - | 완료 | 2026-03-17 | 계좌 요약 카드 |
| T061 | - | 완료 | 2026-03-17 | 당일 손익 카드 |
| T062 | - | 완료 | 2026-03-17 | 자동매매 상태 |
| T063 | - | 완료 | 2026-03-17 | AI 시장 심리 게이지 |
| T064 | - | 완료 | 2026-03-17 | 지수 미니 차트 |
| T065 | - | 완료 | 2026-03-17 | 캔들차트 |
| T066 | - | 완료 | 2026-03-17 | 지표 오버레이 |
| T067 | - | 완료 | 2026-03-17 | 보조 지표 패널 |
| T068 | - | 완료 | 2026-03-17 | 시간 프레임 전환 |
| T069 | - | 완료 | 2026-03-17 | 매매 시그널 마커 |
| T070 | - | 완료 | 2026-03-17 | 뉴스 피드 리스트 |
| T071 | - | 완료 | 2026-03-17 | 감성 트렌드 차트 |
| T072 | - | 완료 | 2026-03-17 | 뉴스 요약 패널 |
| T073 | - | 완료 | 2026-03-17 | 전략 목록 + 토글 |
| T074 | - | 완료 | 2026-03-17 | 매매 로그 |
| T075 | - | 완료 | 2026-03-17 | 킬 스위치 UI |
| T076 | - | 완료 | 2026-03-17 | 손실 한도 바 |
| T077 | - | 완료 | 2026-03-17 | 보유 종목 테이블 |
| T078 | - | 완료 | 2026-03-17 | 자산 배분 차트 |
| T079 | - | 완료 | 2026-03-17 | 수익률 추이 차트 |
| T080 | - | 완료 | 2026-03-17 | 관심 종목 관리 |
| T081 | - | 완료 | 2026-03-17 | 실시간 모니터링 |
| T082 | - | 완료 | 2026-03-17 | 알림 센터 |
| T083 | - | 완료 | 2026-03-17 | 팝업 알림 |
| T084 | - | 완료 | 2026-03-17 | AI 설정 페이지 |
| T085 | - | 완료 | 2026-03-17 | 매매 설정 페이지 |
| T086 | - | 완료 | 2026-03-17 | Backtrader 통합 |
| T087 | - | 완료 | 2026-03-17 | 과거 데이터 로더 |
| T088 | - | 완료 | 2026-03-17 | 백테스트 결과 분석 |
| T089 | - | 완료 | 2026-03-17 | 백테스팅 뷰 |
| T090 | - | 완료 | 2026-03-17 | 백테스트 시각화 |
| T091 | - | 완료 | 2026-03-17 | DB 백업/복원 |
| T092 | - | 완료 | 2026-03-17 | 데이터 내보내기 |
| T093 | - | 완료 | 2026-03-17 | 자동 저장 5분 |
| T094 | - | 완료 | 2026-03-17 | 데이터 보존 정책 |
| T095 | - | 완료 | 2026-03-17 | PyInstaller 빌드 |
| T096 | - | 완료 | 2026-03-17 | 설정 마법사 |
| T097 | - | 완료 | 2026-03-17 | 자동 업데이트 확인 |
| T098 | - | 완료 | 2026-03-17 | 3-Panel QSplitter 레이아웃 |
| T099 | - | 완료 | 2026-03-17 | L-Panel 네비게이션 |
| T100 | - | 완료 | 2026-03-17 | R-Panel 컨트롤 |
| T101 | - | 완료 | 2026-03-17 | 다크 테마 QSS |
| T102 | - | 완료 | 2026-03-17 | 글래스모피즘 카드 위젯 |
| T103 | - | 완료 | 2026-03-17 | Explainable AI 시그널 카드 |
| T104 | - | 완료 | 2026-03-17 | AI 처리 상태 표시 |

---

## 문서 종료

본 계획서는 PRD v1.1을 기준으로 작성되었으며, PRD 요구사항 변경 시 함께 업데이트한다.
구현 진행 중 발견되는 이슈는 doc/d0004_todo.md 디버깅 섹션에 기록한다.
