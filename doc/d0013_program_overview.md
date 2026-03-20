# StokAI v0.1.0 - 프로그램 개요 및 사용법

## 문서이력관리

| 버전 | 날짜 | 변경내용 |
|------|------|---------|
| v1.0 | 2026-03-18 | 최초 작성 |

---

## 1. 프로그램 개요

StokAI는 **AI 기반 주식 자동매매 시스템**으로, KOSPI/KOSDAQ 시장에서 기술적 분석과 뉴스 감성분석을 결합하여 자동으로 매매 시그널을 생성하고 주문을 실행합니다.

### 핵심 특징

- **AI 종목 자동 선정**: 951+ 종목에서 3단계 필터링으로 최적 매매 대상 자동 선정
- **실시간 기술적 분석**: RSI, MACD, 볼린저밴드, ADX, OBV 등 11개 지표 조합
- **다중 전략 앙상블**: Momentum + Mean Reversion + AI Composite 전략 동시 운영
- **리스크 관리**: Kelly 포지션사이징, 일일 손실한도, 집중도 제한, 킬스위치
- **가상 포트폴리오**: 실제 증권사 연결 없이도 시뮬레이션 매매 + 수익률 추적
- **웹 대시보드**: 원격 모니터링 (FastAPI + WebSocket)
- **뉴스 감성분석**: LLM 기반 실시간 뉴스 분석 (OpenAI API)

---

## 2. 시스템 구성

```
+-------------------------------------------------------------------+
|                        StokAI Desktop App                          |
|  +-------------+  +--------------------+  +--------------------+  |
|  | Left Panel  |  | Center Panel       |  | Right Panel        |  |
|  | (네비게이션) |  | (대시보드/차트/뉴스)|  | (킬스위치/AI시그널)|  |
|  +-------------+  +--------------------+  +--------------------+  |
+-------------------------------------------------------------------+
         |                    |                       |
+--------v--------------------v-----------------------v---------+
|                     Service Container (DI)                     |
|  +--------+ +-------+ +----------+ +---------+ +----------+  |
|  |Market  | |  AI   | | Engine   | | Bridge  | | Crawler  |  |
|  |DataProv| |Screener| |Orchestr. | | (gRPC)  | | (News)   |  |
|  +--------+ +-------+ +----------+ +---------+ +----------+  |
+---------------------------------------------------------------+
         |                    |                       |
   FinanceDataReader     OpenAI API            Kiwoom OCX
   (KRX 시세 데이터)    (뉴스 감성분석)       (실제 주문 실행)
```

### 모듈별 역할

| 모듈 | 파일 | 역할 |
|------|------|------|
| **MarketDataProvider** | `src/data/market_data_provider.py` | FinanceDataReader 기반 실시간 시세/OHLCV/종목목록 |
| **StockScreener** | `src/ai/stock_screener.py` | 3단계 AI 종목 자동 선정 |
| **ChartAnalyzer** | `src/engine/chart_analyzer.py` | pandas-ta 기반 11개 기술지표 계산 |
| **SignalGenerator** | `src/engine/signal_generator.py` | 기술지표 조합 매수/매도/관망 시그널 |
| **StrategyEngine** | `src/engine/strategy_engine.py` | Momentum, MeanReversion, AIComposite 전략 |
| **RiskManager** | `src/engine/risk_manager.py` | 4단계 리스크 검증 + 킬스위치 |
| **TradingOrchestrator** | `src/engine/orchestrator.py` | 자동매매 파이프라인 총괄 |
| **VirtualPortfolio** | `src/engine/virtual_portfolio.py` | 가상 포트폴리오 (시뮬레이션 매매 추적) |
| **NewsAnalyzer** | `src/ai/news_analyzer.py` | LLM 기반 뉴스 감성분석 |
| **BacktestEngine** | `src/engine/backtest_engine.py` | Backtrader 기반 백테스팅 |

---

## 3. 자동매매 파이프라인

```
[자동매매 시작 버튼 클릭]
       |
       v
1단계: AI 종목 선정 (StockScreener)
       |  - KOSPI/KOSDAQ 951+ 종목 조회
       |  - 시가총액 1000억+, 거래량 10만+, 주가 1000원+ 필터 -> 100종목
       |  - 기술지표(RSI/MACD/BB/ADX/OBV) 스코어링 -> 30종목
       |  - AIScorer 종합 평가 -> 최종 5종목 자동 선정
       v
2단계: 실시간 모니터링 (5초 간격)
       |  - FinanceDataReader로 현재가/OHLCV 조회
       |  - ChartAnalyzer로 11개 기술지표 계산
       |  - SignalGenerator로 매수/매도/관망 시그널 산출
       v
3단계: 전략 앙상블 평가 (StrategyEngine)
       |  - Momentum 전략: RSI/MACD 추세 추종
       |  - MeanReversion 전략: 볼린저밴드 평균 회귀
       |  - AIComposite 전략: 감성+기술 결합
       |  - 3개 전략 가중평균 -> 최종 시그널
       v
4단계: 리스크 검증 (RiskManager)
       |  - 주문 유효성 (가격/수량)
       |  - Kelly 포지션사이징 (승률 기반)
       |  - 포트폴리오 집중도 제한
       |  - 일일 손실한도 체크
       v
5단계: 주문 실행
       |  - 키움 API 연결 시: 실제 주문 실행
       |  - 미연결 시: 가상 포트폴리오에 시뮬레이션 매매
       v
6단계: 결과 반영
       - 매매 기록 저장 (TradeLogger)
       - 포트폴리오 갱신 (보유종목/잔고/수익률)
       - UI 실시간 업데이트
```

---

## 4. 사용법

### 4.1 설치

1. `StokAI_Setup_0.1.0.exe` 실행
2. 설치 경로 선택 (기본: `C:\Program Files\StokAI`)
3. 설치 완료 후 바탕화면 아이콘으로 실행

### 4.2 초기 설정 (설정 마법사)

처음 실행 시 4단계 설정 마법사가 표시됩니다:

1. **계좌 설정**: 키움증권 계좌번호, 비밀번호 입력
2. **API 설정**: OpenAI API 키 입력 (뉴스 감성분석용, 선택)
3. **매매 설정**: 일일 손실한도, 최대 포지션 비중 등
4. **웹 대시보드**: 원격 모니터링 활성화/포트 설정

### 4.3 화면 구성

#### 좌측 패널 (네비게이션)
- 대시보드 / 차트 / 뉴스 / 자동매매 / 포트폴리오 / 관심종목 / 백테스팅 / 알림

#### 중앙 패널 (메인 뷰)
- **대시보드**: 계좌 요약, 자동매매 상태, 시장 현황
- **차트**: 캔들스틱 차트 + 기술지표 오버레이
- **뉴스**: 실시간 뉴스 + 감성 분석 트렌드
- **자동매매**: 전략 목록 + 매매 로그
- **포트폴리오**: 보유종목 테이블 + 비중 차트 + 수익률 차트
- **백테스팅**: 과거 데이터 기반 전략 검증

#### 우측 패널
- **긴급 정지 (킬스위치)**: 2초 long-press로 모든 매매 즉시 중단
- **AI 시그널 카드**: 현재 AI 분석 결과 실시간 표시
- **자동매매 제어**: 시작/중지 버튼 + 감시 종목 입력

#### 상태바
- 모의투자/실전투자 모드 표시
- 연결 상태
- AI 분석 상태
- 시장 상태 (개장/폐장 + 남은 시간)
- 현재 시간

### 4.4 자동매매 시작

1. 우측 패널의 "자동매매 시작" 버튼 클릭
2. **종목 입력란이 비어있으면**: AI가 자동으로 최적 종목 5개 선정 (약 30초)
3. **종목 입력란에 코드가 있으면**: 해당 종목만 감시
4. 5초 간격으로 시세 확인 + 전략 분석 + 시그널 생성
5. 매수/매도 조건 충족 시 자동 주문 실행
6. 포트폴리오에 실시간 반영

### 4.5 킬스위치 (긴급 정지)

- 우측 패널 상단 빨간 버튼을 **2초간 길게 누르면** 발동
- 모든 자동매매 즉시 중단
- RiskManager 킬스위치 활성화 (추가 주문 차단)

### 4.6 모의투자 / 실전투자 전환

- 설정 > 계좌 > "모의투자 / 실전투자" 토글
- 실전투자 전환 시 비밀번호 확인 필수
- 상태바에 현재 모드 표시 (초록=모의, 빨강=실전)

### 4.7 웹 대시보드

- 설정 > 웹 대시보드에서 활성화
- 같은 네트워크의 브라우저에서 `http://[PC IP]:8080` 접속
- 아이디/비밀번호 인증
- WebSocket 기반 실시간 데이터 갱신

---

## 5. 기술 스택

| 분류 | 기술 | 용도 |
|------|------|------|
| GUI | PyQt6 | 데스크톱 UI |
| 데이터 | FinanceDataReader, pandas | KRX 시세 데이터 |
| 기술분석 | pandas-ta | 11개 기술지표 |
| AI/LLM | OpenAI API | 뉴스 감성분석 |
| 전략 | Backtrader, Optuna | 백테스팅, 파라미터 최적화 |
| 웹 | FastAPI, WebSocket, Jinja2 | 원격 대시보드 |
| DB | SQLCipher | 암호화 데이터베이스 |
| 보안 | keyring, Fernet | 자격증명/데이터 암호화 |
| 증권사 | gRPC (Kiwoom OCX) | 실제 주문 실행 |
| 빌드 | PyInstaller, Inno Setup | Windows EXE + 인스톨러 |

---

## 6. 의존성

```
PyQt6>=6.6.0          # GUI 프레임워크
finance-datareader    # KRX 시세 데이터
pandas>=2.1.0         # 데이터 처리
pandas-ta>=0.3.14b    # 기술적 분석 지표
numpy>=1.26.0         # 수치 계산
openai>=1.12.0        # LLM API (뉴스 분석)
matplotlib>=3.10.8    # 차트 시각화
fastapi>=0.135.1      # 웹 대시보드 서버
backtrader>=1.9.78    # 백테스팅 엔진
optuna>=4.8.0         # 하이퍼파라미터 최적화
grpcio>=1.60.0        # Kiwoom gRPC 통신
sqlcipher3>=0.5.0     # 암호화 DB
keyring>=25.0.0       # 자격증명 관리
cryptography>=42.0.0  # 데이터 암호화
```

---

## 7. 파일 구조

```
StokAI/
├── src/
│   ├── main.py                    # 앱 진입점
│   ├── app.py                     # 메인 윈도우 + 시스템 트레이
│   ├── service_container.py       # 서비스 DI 컨테이너
│   ├── config.py                  # 설정 관리
│   ├── ai/                        # AI 모듈
│   │   ├── llm_service.py         #   LLM 서비스 (Primary/Fallback)
│   │   ├── news_analyzer.py       #   뉴스 감성분석
│   │   ├── sentiment_scorer.py    #   시간가중 감성점수 집계
│   │   ├── rag_engine.py          #   RAG 엔진
│   │   └── stock_screener.py      #   AI 종목 자동 스크리너
│   ├── data/                      # 시장 데이터
│   │   └── market_data_provider.py#   FinanceDataReader 기반
│   ├── engine/                    # 매매 엔진
│   │   ├── orchestrator.py        #   자동매매 파이프라인
│   │   ├── chart_analyzer.py      #   기술지표 계산 (11종)
│   │   ├── signal_generator.py    #   매매 시그널 생성
│   │   ├── strategy_engine.py     #   전략 엔진 (3종)
│   │   ├── risk_manager.py        #   리스크 관리 (4단계)
│   │   ├── ai_scorer.py           #   AI 종합점수 산출
│   │   ├── virtual_portfolio.py   #   가상 포트폴리오
│   │   ├── backtest_engine.py     #   백테스팅
│   │   ├── optimizer.py           #   Optuna 최적화
│   │   ├── trade_logger.py        #   매매 기록
│   │   └── market_classifier.py   #   시장 레짐 분류
│   ├── bridge/                    # Kiwoom gRPC
│   │   ├── kiwoom_bridge.py       #   64bit gRPC 클라이언트
│   │   ├── kiwoom_server.py       #   32bit gRPC 서버 (stub)
│   │   └── kiwoom_wrapper.py      #   고수준 래퍼
│   ├── crawler/                   # 뉴스 수집
│   │   ├── naver_crawler.py       #   네이버 금융 뉴스
│   │   ├── rss_crawler.py         #   RSS 피드
│   │   ├── news_manager.py        #   뉴스 통합 관리
│   │   └── news_scheduler.py      #   자동 수집 스케줄러
│   ├── ui/                        # PyQt6 UI (25개)
│   │   ├── dashboard.py           #   메인 대시보드
│   │   ├── chart_view.py          #   캔들스틱 차트
│   │   ├── portfolio_view.py      #   포트폴리오
│   │   └── ...                    #   기타 뷰/위젯
│   ├── web/                       # FastAPI 웹 서버
│   │   ├── server.py              #   FastAPI + uvicorn
│   │   ├── auth.py                #   인증
│   │   └── api_routes.py          #   REST API
│   ├── security/                  # 보안
│   │   ├── credential_manager.py  #   keyring 자격증명
│   │   └── encryption.py          #   Fernet 암호화
│   └── utils/                     # 유틸리티
│       ├── logger.py              #   로깅
│       └── constants.py           #   상수
├── tests/                         # 테스트 (77개)
├── doc/                           # 문서
├── dist/                          # 빌드 출력
│   ├── StokAI/StokAI.exe         #   실행파일
│   └── StokAI_Setup_0.1.0.exe    #   인스톨러
└── pyproject.toml                 # 프로젝트 설정
```

---

## 8. 현재 상태 및 제한사항

### 작동하는 기능
- AI 종목 자동 선정 (KOSPI 951종목 -> 5종목, 약 30초)
- 실시간 시세 조회 (FinanceDataReader)
- 기술지표 분석 (11개 지표)
- 3개 전략 앙상블 시그널 생성
- 가상 포트폴리오 시뮬레이션 매매
- 시장 상태 실시간 표시 (개장/폐장/남은시간)
- 웹 대시보드 (원격 모니터링)
- 뉴스 수집 (네이버 + RSS)

### 제한사항
- **실제 주문**: 키움증권 API(32bit OCX) 연결 필요 - 현재 stub 서버
- **뉴스 감성분석**: OpenAI API 키 설정 필요 (미설정 시 기술지표만으로 판단)
- **시세 지연**: FinanceDataReader는 실시간이 아닌 15~20분 지연 데이터
- **공휴일 미반영**: 주말만 휴장 처리, 공휴일은 미반영

### 향후 개선 예정
- 키움증권 OCX 실제 연결 (32bit 프로세스 분리)
- 실시간 시세 WebSocket 연동
- 가상 포트폴리오 수익률 차트
- 공휴일 캘린더 반영
- AI 종목 선정에 뉴스 감성분석 통합 (screen 메서드)
