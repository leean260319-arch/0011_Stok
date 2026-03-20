# AI 주식 자동매매 시스템 조사 및 개선 계획

## 문서이력관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-03-17 | 신규 작성 - 경쟁 시스템 조사, Best Practice, Gap 분석, 개선 계획 |

---

## 1. 조사 개요

### 1.1 목적

StokAI 주식 자동매매 시스템의 AI/엔진 모듈을 경쟁 오픈소스 시스템과 비교 분석하고, 업계 Best Practice를 반영한 구체적인 개선 계획을 수립한다.

### 1.2 범위

- **경쟁 시스템**: Freqtrade(FreqAI), FinGPT, QuantConnect/Lean, Jesse, vnpy, Hummingbot, Zipline
- **기술 영역**: LLM 토큰 효율화, AI 전문성 확보, 신호 생성 신뢰성, 리스크 관리, 백테스팅, 매매 기록/보고서
- **대상 코드**: `src/ai/`, `src/engine/` 하위 모듈 전체

### 1.3 방법론

1. StokAI 현재 코드 정적 분석 (11개 핵심 파일)
2. 웹 검색 기반 경쟁 시스템 아키텍처 조사
3. 업계 Best Practice 문헌 조사
4. Gap 분석 및 우선순위 기반 개선 계획 수립

### 1.4 StokAI 현재 아키텍처 요약

```
[뉴스 수집] -> NewsAnalyzer (LLM 감성분석)
                    |
              SentimentScorer (시간 가중 집계)
                    |
              AIScorer (감성 40% + 기술 60% 결합) -> signal
                    |                                   |
              [ChartAnalyzer] -> SignalGenerator --------+
              (RSI, MACD, BB, ADX 등 11개 지표)
                    |
              StrategyEngine (AI종합/모멘텀/평균회귀 3전략)
                    |
              RiskManager (4단계 검증 + 킬스위치)
                    |
              BacktestEngine (Backtrader 통합)
```

**핵심 특성**:
- LLM: OpenAI 호환 API (GPT-4o-mini Primary, DeepSeek Fallback)
- 감성분석: 단순 프롬프트, 시스템 프롬프트 미사용, 캐싱 없음
- 기술지표: pandas-ta 기반 11개 지표 (RSI, MACD, BB, SMA, EMA, Stochastic, Ichimoku, ADX, CCI, Williams %R, OBV)
- 전략: 3개 전략 (AI종합, 모멘텀, 평균회귀), 고정 가중치
- 리스크: 4단계 검증 (주문/포트폴리오/계좌/시스템), MDD 킬스위치
- 백테스트: Backtrader 통합, Sharpe/DD/TradeAnalyzer
- 한국 시장 특화: 호가단위 테이블, 장 마감 전 차단

---

## 2. 경쟁 시스템 상세 분석

### 2.1 Freqtrade (+ FreqAI)

**개요**: GitHub 50,000+ 개발자가 기여하는 최대 규모 오픈소스 암호화폐 트레이딩 봇. 2025 GitHub State of Open Source 보고서 기준 가장 활발한 트레이딩 봇 프로젝트.

**아키텍처**:
- **모듈 구조**: Strategy Engine, FreqAI ML 모듈, Risk/Money Management, Backtesting/Optimization이 독립 모듈로 분리
- **플러그인 시스템**: 각 컴포넌트가 플러그인 가능하며, `config.json`의 environments로 모드 전환

**FreqAI ML 파이프라인**:
```
IFreqaiModel (추상 기반) -> 학습/예측 워크플로우 오케스트레이션
    |
FreqaiDataKitchen -> 데이터 준비, 피처 엔지니어링, 전처리 (페어별 독립)
    |
FreqaiDataDrawer -> 모델/메타데이터/예측 이력 영속 저장 (메모리 상주)
    |
ML Libraries -> CatBoost, LightGBM, PyTorch 등
```

- **주기적 재학습**: 라이브/드라이런 시 백그라운드 스레드에서 상시 재학습 수행
- **피처**: 가격, 펀딩레이트, 소셜 감성 등 다양한 입력 지원
- **백테스팅**: 주기적 재학습을 에뮬레이션하여 현실적 백테스트 제공

**전략 구조**:
- Python 클래스 기반 전략 정의
- `populate_indicators()`, `populate_buy_trend()`, `populate_sell_trend()` 메서드 패턴
- 하이퍼옵트(Hyperopt) 기반 파라미터 자동 최적화

**백테스팅**:
- 전용 백테스트 엔진 내장
- FreqAI 연동 시 주기적 재학습 시뮬레이션 포함
- 수수료, 슬리피지 반영

**리스크 관리**:
- Stoploss, Trailing Stop, Custom Stoploss 함수
- ROI 테이블 (시간 경과에 따른 최소 수익률)
- 포지션 사이징: stake_amount, max_open_trades 제어

**StokAI에 적용 가능한 기법**:
| 기법 | 내용 | 적용 대상 |
|------|------|----------|
| 주기적 재학습 | 백그라운드 스레드에서 모델 갱신 | `src/ai/` 전체 |
| 피처 엔지니어링 분리 | DataKitchen 패턴으로 전처리 독립 | `src/engine/chart_analyzer.py` |
| 하이퍼옵트 | 전략 파라미터 자동 최적화 | `src/engine/strategy_engine.py` |
| Trailing Stop | 동적 손절 메커니즘 | `src/engine/risk_manager.py` |
| 영속 저장 | 모델/예측 이력 관리 | 신규 모듈 필요 |

### 2.2 FinGPT

**개요**: AI4Finance Foundation이 개발한 금융 특화 오픈소스 LLM 프레임워크. 데이터 중심(Data-centric) 접근법으로 금융 NLP 태스크에 특화.

**아키텍처 (4계층)**:
```
[Data Source Layer] - 뉴스, SNS, 공시, 재무제표 수집
        |
[Data Engineering Layer] - 실시간 NLP 처리, 노이즈 필터링
        |
[LLMs Layer] - LoRA/QLoRA 경량 파인튜닝
        |
[Tasks Layer] - 감성분석, 요약, 수치 추론
```

**금융 특화 LLM 접근법**:
- **LoRA/QLoRA 파인튜닝**: 대형 사전학습 모델에 저랭크 어댑터를 추가하여 저비용으로 금융 도메인 적응
- **FinGPT v3 시리즈**: 뉴스+트윗 감성분석 데이터셋으로 파인튜닝, 대부분의 금융 감성분석 벤치마크에서 최고 성능 달성
- **FinGPT-RAG**: 외부 지식 검색을 통한 정보 심도/맥락 최적화

**프롬프트 설계**:
- 주가 변동률을 출력 라벨로 사용 (연속형 -> 3클래스 이산화: positive/negative/neutral)
- 뉴스 기사와 대응하는 주가 변동을 직접 매핑
- 구조화된 출력 포맷 강제 (JSON)

**감성분석 방법**:
- 뉴스/소셜미디어에서 세분화된 감성 신호 추출
- 감성 인사이트 + 기술적 지표 결합으로 매매 시그널 생성
- 정확도, F1, 시뮬레이션 누적수익률에서 실증적 개선 확인

**StokAI에 적용 가능한 기법**:
| 기법 | 내용 | 적용 대상 |
|------|------|----------|
| 시스템 프롬프트 설계 | "금융 분석가" 역할 정의 + 분석 프레임워크 | `src/ai/news_analyzer.py` |
| 구조화된 라벨링 | 주가 변동률 기반 감성 라벨 정의 | `src/ai/news_analyzer.py` |
| RAG 파이프라인 | 뉴스 DB + 재무 데이터 검색 증강 | 신규 모듈 필요 |
| 노이즈 필터링 | 저품질 뉴스 사전 필터링 | `src/ai/news_analyzer.py` |
| Few-shot 예제 | 금융 감성분석 예제 제공 | `src/ai/news_analyzer.py` |

### 2.3 QuantConnect/Lean

**개요**: 2012년 설립, 180+ 엔지니어가 기여하는 오픈소스 알고리즘 트레이딩 엔진. 300+ 헤지펀드가 프로덕션 사용. C# 코어 + Python 3.11 지원.

**아키텍처 (Algorithm Framework)**:
```
[Universe Selection] -> 종목 선정
        |
[Alpha Model] -> 매매 시그널(Insight) 생성
        |
[Portfolio Construction] -> PortfolioTarget 생성 (목표 보유수량)
        |
[Risk Management] -> 안전 파라미터 검증 및 조정
        |
[Execution Model] -> 주문 실행
```

**데이터 파이프라인**:
- **멀티스레드**: 데이터 병렬 로딩 + 동기화하여 최대 CPU 활용
- **이벤트 드리븐**: 10년 주식 백테스트 33초 완료 가능
- **일일 15,000+ 백테스트** 분산 컴퓨팅으로 처리

**알고리즘 프레임워크 특징**:
- Alpha-Portfolio-Risk-Execution 파이프라인이 명확히 분리
- Insight 객체로 시그널 표준화 (방향, 기간, 신뢰도, 크기)
- PortfolioTarget으로 포지션 관리 표준화
- Risk Management 모델이 Portfolio 출력을 검증/조정

**StokAI에 적용 가능한 기법**:
| 기법 | 내용 | 적용 대상 |
|------|------|----------|
| Insight 객체 표준화 | 시그널에 방향/기간/신뢰도/크기 포함 | `src/engine/signal_generator.py` |
| Alpha-Risk 분리 | 시그널 생성과 리스크 검증 완전 분리 | `src/engine/` 전체 |
| 포지션 타겟 | 목표 보유수량 기반 주문 생성 | `src/engine/risk_manager.py` |
| 멀티스레드 데이터 | 데이터 병렬 로딩 | `src/engine/chart_analyzer.py` |

### 2.4 Jesse

**개요**: Python 기반 고급 암호화폐 트레이딩 프레임워크. 전략 연구, 백테스팅, 최적화, 라이브 트레이딩 통합.

**핵심 특징**:
- **Optuna 기반 최적화**: 전략 파라미터를 Optuna 라이브러리로 자동 최적화, 교차검증 지원
- **JesseGPT**: 전용 AI 어시스턴트 - 전략 작성, 최적화, 디버깅 지원
- **멀티 타임프레임/심볼**: look-ahead bias 없이 다중 타임프레임 동시 처리
- **스마트 오더링**: 시장가/지정가/스탑 주문 자동 선택

**전략 최적화**:
- Optuna의 TPE(Tree-structured Parzen Estimator) 알고리즘으로 파라미터 탐색
- 교차검증으로 과적합 방지
- 비기술적 사용자도 AI를 통해 최적화 가능

**보고서 생성**:
- 백테스트 결과 상세 보고서
- 성과 지표 (수익률, MDD, Sharpe 등) 자동 계산

**StokAI에 적용 가능한 기법**:
| 기법 | 내용 | 적용 대상 |
|------|------|----------|
| Optuna 최적화 | 전략 파라미터 자동 탐색 | `src/engine/strategy_engine.py` |
| 교차검증 | 과적합 방지 | `src/engine/backtest_engine.py` |
| AI 어시스턴트 | 전략 작성/디버깅 지원 | 별도 도구 |
| 멀티 타임프레임 | 다중 주기 동시 분석 | `src/engine/chart_analyzer.py` |

### 2.5 기타 참고 시스템 요약

| 항목 | vnpy | Hummingbot | Zipline-reloaded |
|------|------|------------|------------------|
| **언어** | Python | Python | Python |
| **주요 시장** | 중국 국내/해외 전 거래 상품 | 암호화폐 (CEX 19개 + DEX 24개) | 미국 주식 |
| **핵심 강점** | 중국 시장 전문, 풀스택 플랫폼 | 시장 조성(Market Making) 특화, 크로스플랫폼 | Quantopian 엔진, 이벤트 드리븐 |
| **백테스팅** | 내장 | V2 프레임워크에서 지원 | 핵심 기능 |
| **라이브 트레이딩** | 지원 | 지원 | 포크(zipline-live) 필요 |
| **한계** | 한국 시장 직접 지원 없음 | 주식 시장 미지원 | Python 3.5-3.6 의존, 설치 어려움 |
| **StokAI 참고점** | 중국 호가 체계 참고 | 마켓메이킹 전략 참고 | 이벤트 드리븐 설계 참고 |

**한국 시장 특화 오픈소스**:
- **한국투자증권 Open API**: OAuth 2.0 인증, REST + WebSocket, 파이썬 공식 지원
- **키움증권 Open API**: COM 기반, PyQt5와 연동
- **WikiDocs 자동매매 시스템**: 한국/미국 주식 자동매매 실전 가이드

---

## 3. 업계 Best Practice

### 3.1 토큰 효율화 기법

#### 3.1.1 응답 캐싱

**방법**: 동일하거나 유사한 프롬프트에 대한 LLM 응답을 캐시하여 중복 API 호출 방지.

| 캐시 방식 | 장점 | 단점 | 적합 상황 |
|----------|------|------|----------|
| **SQLite** | 설치 불필요, 파일 기반, 간단 구현 | 고동시성 부적합, 디스크 I/O | StokAI처럼 단일 프로세스 |
| **Redis** | 인메모리, 고속, 시맨틱 캐싱 가능 | 별도 서버 필요, 메모리 비용 | 대규모 서비스 |
| **파일 기반** | 가장 간단 | 관리 어려움, 검색 느림 | 프로토타입 |

- **시맨틱 캐싱**: 벡터 검색으로 유사 쿼리 매칭, 캐시 히트율 30-60% 달성 가능
- **TTL 설정**: 뉴스 감성분석은 24시간, 재무 데이터는 분기별로 차등 적용
- **비용 절감**: 적절한 캐싱으로 API 비용 60-80% 절감 가능

**StokAI 현재 상태**: `src/ai/llm_service.py`에 캐싱 메커니즘 전무. 동일 뉴스 기사를 반복 분석하면 매번 API 호출 발생.

#### 3.1.2 프롬프트 압축

- **뉴스 요약 후 분석**: 긴 뉴스 본문을 먼저 요약(저비용 모델) -> 요약본으로 감성분석(고비용 모델)
- **LLMLingua**: 프롬프트 압축 라이브러리, 10배 압축 시 90%+ 태스크 성능 유지
- **불필요한 컨텍스트 제거**: 프롬프트에서 반복적/장황한 설명 최소화

**StokAI 현재 상태**: `news_analyzer.py`의 `SENTIMENT_PROMPT`는 뉴스 전문(`content_preview`)을 그대로 전송. 긴 기사일수록 토큰 낭비.

#### 3.1.3 배치 처리

- **다건 동시 분석**: 여러 뉴스 기사를 하나의 프롬프트로 묶어 분석
- **현재 문제**: `analyze_batch()`가 기사별 개별 API 호출 (N건 = N회 호출)

#### 3.1.4 토큰 예산 관리

- 일/월별 토큰 사용량 추적
- 예산 초과 시 저비용 모델로 자동 전환
- 프롬프트별 토큰 수 사전 계산

**StokAI 현재 상태**: `constants.py`에 API_RATE_PER_SEC/HOUR만 정의. 토큰 사용량 추적/로깅 없음.

### 3.2 AI 전문성 확보 기법

#### 3.2.1 시스템 프롬프트 설계

**Best Practice 구조**:
```
[역할 정의] "당신은 25년 경력의 한국 주식시장 전문 금융 분석가입니다."
[분석 프레임워크] "다음 관점에서 분석하세요: 1) 기업 실적 영향, 2) 산업 트렌드..."
[출력 형식] "반드시 JSON 형식으로..."
[제약 조건] "추측하지 말고, 근거가 불충분하면 neutral로 판단하세요."
```

- 역할(Role) 정의: 전문가 페르소나 부여로 분석 품질 향상
- 분석 프레임워크: 기본적 분석(실적, 매출, 마진, 현금흐름), 기술적 요인(시장 심리, 기관 매매, 거시경제), 촉매 이벤트(실적발표, 신제품, 규제 변화)
- 한국 시장 특수성 반영: KOSPI/KOSDAQ 구분, 외국인/기관 수급, 한국 공시 체계

**StokAI 현재 상태**: `news_analyzer.py`에서 시스템 프롬프트 미사용. `messages=[{"role": "user", "content": prompt}]`로만 전송.

#### 3.2.2 Few-shot Learning

**구현 방법**:
```json
[시스템] "다음은 금융 뉴스 감성분석 예시입니다."
[예시1] 제목: "삼성전자 3분기 영업이익 40% 증가" -> {"score": 0.8, "label": "positive", ...}
[예시2] 제목: "반도체 업황 하반기 둔화 전망" -> {"score": -0.5, "label": "negative", ...}
[예시3] 제목: "한국은행 기준금리 동결" -> {"score": 0.0, "label": "neutral", ...}
[실제 분석 대상] ...
```

- 3-5개의 대표 예제로 출력 형식/판단 기준 학습 유도
- 한국 주식 시장에 맞는 예제 선정 (삼성전자, KOSPI, 금통위 등)
- 토큰 추가 비용 대비 분석 일관성/정확도 크게 향상

**StokAI 현재 상태**: Few-shot 예제 없음. 프롬프트에 출력 형식만 정의.

#### 3.2.3 Chain-of-Thought (단계별 추론)

```
1단계: 뉴스 핵심 내용 파악 (어떤 기업/산업에 대한 뉴스인가?)
2단계: 단기 영향 분석 (1-5일 주가에 미칠 영향)
3단계: 수급 영향 분석 (외국인/기관 매매에 미칠 영향)
4단계: 종합 판단 (score, label 결정)
```

- 단계별 추론을 유도하면 분석 깊이와 정확도 향상
- 각 단계의 근거가 명시되어 판단 투명성 확보

#### 3.2.4 RAG (Retrieval-Augmented Generation)

**금융 RAG 파이프라인**:
```
[쿼리] "삼성전자 관련 뉴스 감성 분석"
        |
[검색] 뉴스 DB (최근 7일) + 재무 DB (최근 실적) + 애널리스트 리포트
        |
[증강] 검색 결과를 컨텍스트로 프롬프트에 추가
        |
[생성] LLM이 풍부한 맥락으로 정확한 감성 판단
```

- SSRN 연구: RAG 기반 금융 감성분석이 기존 방법 대비 정확도 향상
- 실용적 구현: SQLite/MySQL로 뉴스 저장 + 벡터 검색으로 관련 기사 탐색
- **한계**: 감성분석만으로 익일 주가 예측력은 R-Square 0.010 수준으로 제한적 -> 기술적 지표와 결합 필수

**StokAI 현재 상태**: RAG 미구현. 뉴스 기사를 개별로만 분석, 과거 뉴스/재무 맥락 미제공.

### 3.3 신호 생성 신뢰성

#### 3.3.1 다중 지표 앙상블

- 단일 지표 의존 대신 다수 지표 투표/가중합
- QuantConnect의 Insight 패턴: 각 Alpha 모델이 독립 시그널 생성 -> 합산
- **현재 StokAI**: `signal_generator.py`에서 RSI, MACD, BB, ADX 4개 지표를 고정 점수로 합산. 가중치 조절 불가, 시장 상황 미반영.

#### 3.3.2 시장 상황별 동적 가중치

```python
# 개념 예시
if market_regime == "trending":
    weights = {"macd": 0.4, "adx": 0.3, "rsi": 0.2, "bb": 0.1}
elif market_regime == "ranging":
    weights = {"bb": 0.4, "rsi": 0.3, "macd": 0.2, "adx": 0.1}
```

- 상승장/횡보장/하락장에 따라 지표 가중치 동적 조절
- ADX로 추세 강도 판별 -> 추세 지표/역추세 지표 가중치 조절

#### 3.3.3 거래량 확인 신호

- 가격 시그널 + 거래량 확인으로 신뢰도 향상
- OBV(On-Balance Volume) 방향과 가격 방향 일치 확인
- **StokAI**: `chart_analyzer.py`에 OBV 계산 메서드 있으나 `signal_generator.py`에서 미사용

#### 3.3.4 시그널 컨피던스 레벨

- QuantConnect Insight 패턴: 시그널에 confidence(0-1) 첨부
- **StokAI**: `ai_scorer.py`에 confidence 계산 있으나 단순한 `abs(total)/0.5` 공식. 지표 합의도(agreement) 미반영.

### 3.4 리스크 관리 고급 기법

#### 3.4.1 Kelly Criterion 포지션 사이징

**공식**: `f* = (bp - q) / b`
- f* = 최적 투자 비율
- b = 평균 수익/손실 비율 (payoff ratio)
- p = 승률
- q = 패률 (1-p)

**실전 적용**:
- Full Kelly는 과도한 변동성 유발 -> **Half-Kelly(50%)** 또는 **Quarter-Kelly(25%)** 사용 권장
- 과거 매매 기록에서 승률, 평균 수익/손실 비율 계산
- 종목별 독립적 Kelly 비율 산출 가능

**StokAI 현재 상태**: `risk_manager.py`에 포지션 사이징 로직 없음. `backtest_engine.py`에서 단순히 `현금의 95%` 투입.

#### 3.4.2 ATR 기반 동적 손절

```python
# 개념 예시
atr = calc_atr(period=14)
stop_loss = entry_price - (atr * 2.5)  # ATR 2.5배 손절
trailing_stop = highest_price - (atr * 2.0)  # ATR 2.0배 트레일링
```

- 고정 퍼센트 손절 대신 변동성(ATR) 기반 동적 설정
- 변동성 큰 종목: 넓은 손절 / 변동성 작은 종목: 좁은 손절
- **StokAI 현재 상태**: `RiskDefaults.STOP_LOSS_PCT = 2.0` 고정. 변동성 미반영.

#### 3.4.3 트레일링 스탑

- Freqtrade의 Trailing Stop: 가격 상승에 따라 손절가 자동 상향
- ATR 기반 트레일링: `trailing_stop = highest_since_entry - (ATR * multiplier)`
- **StokAI 현재 상태**: 트레일링 스탑 미구현.

#### 3.4.4 변동성 기반 포지션 조절

- ATR로 변동성 측정 -> 변동성 높을수록 포지션 축소
- `position_size = risk_amount / (ATR * multiplier)`
- 역변동성(Inverse Volatility) 가중으로 포트폴리오 안정성 향상

### 3.5 백테스팅 신뢰성

#### 3.5.1 Walk-Forward Analysis

```
[전체 데이터]
|--학습1--|--검증1--|
     |--학습2--|--검증2--|
          |--학습3--|--검증3--|
```

- 학습(In-Sample) 구간에서 파라미터 최적화 -> 검증(Out-of-Sample) 구간에서 성능 측정
- 여러 윈도우를 순차 적용하여 과적합 위험 감소
- **주의**: 단일 가격 경로만 테스트하므로 Monte Carlo와 병행 필요

**StokAI 현재 상태**: `backtest_engine.py`에서 단일 기간 백테스트만 지원. Walk-Forward 미구현.

#### 3.5.2 슬리피지/수수료 반영

- Backtrader 엔진이 수수료(commission) 설정 지원
- 슬리피지: 한국 시장 호가 단위 기반 1-2 틱 슬리피지 반영 필요
- **StokAI 현재 상태**: `backtest_engine.py`에서 수수료/슬리피지 설정 미반영.

#### 3.5.3 Monte Carlo 시뮬레이션

- 매매 순서를 무작위로 재배열하여 다수의 가상 자산 곡선 생성
- 실제 백테스트보다 높은 중앙값 드로다운 노출 -> 숨겨진 리스크 발견
- 드로다운/수익 확률 분포로 전략 강건성 평가
- Bootstrap 방법: 실제 매매 목록에서 복원추출로 새 자산 곡선 생성

#### 3.5.4 벤치마크 대비 비교

- KOSPI/KOSDAQ 지수 대비 초과수익률 측정
- 매수후보유(Buy-and-Hold) 전략 대비 비교
- **StokAI 현재 상태**: 벤치마크 비교 미구현.

### 3.6 매매 기록 및 보고서

#### 3.6.1 매매 근거 자동 기록

- 매매 시점의 시그널, 지표값, 뉴스 감성 등을 자동 저장
- 사후 분석(post-mortem)을 위한 데이터 축적
- **StokAI 현재 상태**: 매매 근거 기록 메커니즘 없음.

#### 3.6.2 성과 보고서 자동 생성

**quantstats 라이브러리**:
- 수익률 시각화, 드로다운 차트, 롤링 통계, 월간 수익률
- HTML 티어시트(tear sheet) 자동 생성
- 벤치마크 대비 비교 기능 내장

**보고서 주기**:
- 일간: 당일 매매 요약, 손익, 시그널 적중률
- 주간: 주간 성과, 전략별 기여도
- 월간: 월간 종합, 벤치마크 대비, 리스크 지표

**StokAI 현재 상태**: 보고서 생성 기능 없음.

#### 3.6.3 전략 비교 리포트

- 동시 운용 전략별 성과 비교
- 전략간 상관관계 분석 (분산투자 효과 측정)
- **StokAI 현재 상태**: `strategy_engine.py`에 `evaluate_all()`은 있으나 전략간 비교/분석 기능 없음.

---

## 4. StokAI Gap 분석

| 기능 영역 | Freqtrade | FinGPT | QuantConnect | Jesse | StokAI 현재 | Gap 심각도 |
|----------|-----------|--------|-------------|-------|------------|-----------|
| **토큰 캐싱** | N/A (ML 기반) | N/A (파인튜닝) | N/A | N/A | 미구현 | **높음** - API 비용 낭비 |
| **시스템 프롬프트** | N/A | 역할+프레임워크 정의 | N/A | JesseGPT 활용 | 미사용 | **높음** - 분석 품질 저하 |
| **Few-shot 예제** | N/A | 감성분석 예제 포함 | N/A | 전략 예제 제공 | 미구현 | **높음** - 출력 불일관 |
| **배치 분석** | 배치 피처 계산 | 배치 처리 | 배치 데이터 | 멀티 심볼 | 개별 호출만 | **중간** - 비용/속도 비효율 |
| **토큰 추적** | 모델 학습 로깅 | 비용 모니터링 | 리소스 모니터링 | 리소스 추적 | 미구현 | **중간** - 비용 관리 불가 |
| **동적 가중치** | 하이퍼옵트 | 학습 기반 | Alpha 앙상블 | Optuna 최적화 | 고정 가중치 | **높음** - 시장 대응 부족 |
| **Kelly 포지션** | stake_amount | N/A | 포트폴리오 모델 | 포지션 관리 | 고정 95% | **높음** - 리스크 과다 |
| **ATR 손절** | Custom Stoploss | N/A | Risk Model | 스마트 오더 | 고정 2% | **높음** - 변동성 미반영 |
| **트레일링 스탑** | 내장 지원 | N/A | Risk Model | 지원 | 미구현 | **중간** - 수익 극대화 불가 |
| **매매 근거 기록** | 전략 로그 | 분석 로그 | Insight 기록 | 매매 로그 | 미구현 | **중간** - 사후 분석 불가 |
| **성과 보고서** | 내장 보고서 | 성과 대시보드 | 상세 분석기 | 보고서 생성 | 미구현 | **중간** - 성과 파악 불가 |
| **Walk-Forward** | FreqAI 재학습 | N/A | 내장 지원 | 교차검증 | 미구현 | **중간** - 과적합 위험 |
| **수수료/슬리피지** | 설정 지원 | N/A | 정밀 시뮬레이션 | 지원 | 미반영 | **높음** - 비현실적 백테스트 |
| **벤치마크 비교** | 기준 비교 | 벤치마크 | 벤치마크 | 비교 기능 | 미구현 | **중간** - 성과 맥락 부족 |
| **시장 분류기** | 하이퍼옵트 | 시장 상황 분석 | 유니버스 선정 | 필터 기능 | 미구현 | **중간** - 전략 전환 불가 |
| **전략 최적화** | Hyperopt | LoRA 튜닝 | 파라미터 최적화 | Optuna | 수동 조정만 | **중간** - 비효율 |
| **RAG 시스템** | N/A | FinGPT-RAG | N/A | N/A | 미구현 | **낮음** - 장기 과제 |
| **거래량 확인** | 지표 활용 | N/A | 다중 데이터 | 지원 | OBV 미활용 | **중간** - 신호 신뢰도 부족 |

---

## 5. StokAI 개선 구현 계획

### 5.1 Phase 1: 즉시 구현 (1주)

> AI 분석 품질 향상 + 비용 절감에 집중

#### P1-01: LLM 응답 캐싱

- **파일**: `src/ai/llm_service.py`
- **내용**:
  - SQLite 기반 프롬프트-응답 캐시 테이블 생성 (`llm_cache`)
  - 캐시 키: 프롬프트 해시(SHA256)
  - TTL: 뉴스 감성분석 24시간, 기타 분석 1시간
  - `LLMService.analyze()` 메서드에 캐시 조회/저장 로직 추가
  - 캐시 히트/미스 로깅
- **구현 예시**:
  ```python
  # llm_service.py에 추가
  import hashlib, sqlite3, time

  class LLMCache:
      def __init__(self, db_path: str, default_ttl: int = 86400):
          self._conn = sqlite3.connect(db_path)
          self._ttl = default_ttl
          self._conn.execute("""
              CREATE TABLE IF NOT EXISTS llm_cache (
                  prompt_hash TEXT PRIMARY KEY,
                  response TEXT,
                  created_at REAL
              )""")

      def get(self, prompt: str) -> str | None:
          h = hashlib.sha256(prompt.encode()).hexdigest()
          row = self._conn.execute(
              "SELECT response, created_at FROM llm_cache WHERE prompt_hash = ?", (h,)
          ).fetchone()
          if row and (time.time() - row[1]) < self._ttl:
              return row[0]
          return None

      def set(self, prompt: str, response: str):
          h = hashlib.sha256(prompt.encode()).hexdigest()
          self._conn.execute(
              "INSERT OR REPLACE INTO llm_cache VALUES (?, ?, ?)",
              (h, response, time.time())
          )
          self._conn.commit()
  ```
- **효과**: 동일 뉴스 재분석 방지, API 비용 50%+ 절감 기대

#### P1-02: 시스템 프롬프트 도입

- **파일**: `src/ai/news_analyzer.py`, `src/ai/llm_service.py`
- **내용**:
  - `CloudLLMProvider.analyze()`에 `system_prompt` 파라미터 추가
  - `messages`에 `{"role": "system", "content": system_prompt}` 삽입
  - 뉴스 감성분석 전용 시스템 프롬프트 정의:
    ```
    당신은 25년 경력의 한국 주식시장 전문 금융 분석가입니다.
    KOSPI/KOSDAQ 시장의 뉴스가 단기(1-5일) 주가에 미치는 영향을 분석합니다.
    다음 관점에서 종합적으로 판단하세요:
    1) 기업 실적/재무 영향
    2) 산업/섹터 트렌드
    3) 외국인/기관 수급 영향
    4) 거시경제/정책 영향
    근거가 불충분하면 neutral(0.0)로 판단하세요.
    ```
- **효과**: 분석 품질 향상, 한국 시장 맥락 반영, 판단 일관성 확보

#### P1-03: Few-shot 예제 추가

- **파일**: `src/ai/news_analyzer.py`
- **내용**:
  - `SENTIMENT_PROMPT`에 3-5개 한국 주식 시장 감성분석 예제 추가
  - 예제 유형: 긍정(실적 호조), 부정(업황 악화), 중립(금리 동결)
  - 각 예제에 score, label, reason 포함
- **구현 예시**:
  ```python
  FEW_SHOT_EXAMPLES = """
  [예시 1]
  제목: 삼성전자, 3분기 영업이익 12조원... 전년비 40% 증가
  내용: 반도체 수요 회복과 AI 칩 판매 호조로 역대급 실적 달성
  결과: {"score": 0.8, "label": "positive", "reason": "영업이익 40% 증가는 강한 실적 모멘텀"}

  [예시 2]
  제목: 반도체 업황, 하반기 둔화 본격화 전망
  내용: 글로벌 수요 감소와 재고 조정으로 하반기 업황 악화 우려
  결과: {"score": -0.5, "label": "negative", "reason": "업황 둔화 전망은 섹터 전체 부정적 영향"}

  [예시 3]
  제목: 한국은행, 기준금리 3.25% 동결 결정
  내용: 시장 예상에 부합하는 동결 결정, 향후 인하 가능성 시사
  결과: {"score": 0.1, "label": "neutral", "reason": "예상 부합 동결로 시장 영향 제한적"}
  """
  ```
- **효과**: 출력 형식 일관성 향상, 판단 기준 명확화

#### P1-04: 뉴스 요약 후 분석 (토큰 절약)

- **파일**: `src/ai/news_analyzer.py`
- **내용**:
  - `content_preview`가 500자 초과 시 먼저 요약 요청 -> 요약본으로 감성분석
  - 요약 단계: 저비용 모델 사용 (또는 Python 텍스트 절단)
  - 대안: 단순 절단 (앞 500자만 사용) - 비용 대비 효율적
- **효과**: 긴 뉴스 기사의 토큰 사용량 50-70% 절감

#### P1-05: 토큰 사용량 추적/로깅

- **파일**: `src/ai/llm_service.py`, `src/utils/constants.py`
- **내용**:
  - `CloudLLMProvider.analyze()` 반환 시 토큰 사용량 파싱 (`response.usage`)
  - 일별 토큰 사용량 SQLite 테이블 저장
  - 일/월 예산 초과 시 경고 로그 + fallback 모델 자동 전환
  - `constants.py`에 토큰 예산 상수 추가
- **효과**: API 비용 가시화, 예산 관리 가능

### 5.2 Phase 2: 단기 개선 (2-4주)

> 매매 신호 신뢰성 + 리스크 관리 고도화

#### P2-01: 동적 지표 가중치

- **파일**: `src/engine/signal_generator.py`
- **내용**:
  - ADX 값으로 시장 상황 분류 (추세/횡보)
  - 추세장: MACD, ADX 가중치 상향 / 횡보장: BB, RSI 가중치 상향
  - 기존 고정 점수(0.3, 0.2) 대신 가중치 딕셔너리 기반 동적 계산
  - OBV 방향 확인을 거래량 확인 신호로 추가
- **효과**: 시장 상황에 맞는 시그널 생성, 거짓 신호 감소

#### P2-02: Kelly Criterion 포지션 사이징

- **파일**: `src/engine/risk_manager.py`
- **내용**:
  - 과거 매매 기록에서 승률(p), 수익/손실 비율(b) 계산
  - Kelly 공식: `f* = (b*p - q) / b`
  - Half-Kelly(50%) 적용으로 보수적 운용
  - `calculate_position_size(account, signal_confidence)` 메서드 추가
  - 기존 `backtest_engine.py`의 95% 고정 투입 대체
- **효과**: 수학적으로 최적화된 포지션 크기, 과도한 리스크 방지

#### P2-03: ATR 기반 동적 손절 + 트레일링 스탑

- **파일**: `src/engine/risk_manager.py`, `src/engine/chart_analyzer.py`
- **내용**:
  - `ChartAnalyzer`에 `calc_atr()` 메서드 추가 (pandas-ta의 `ta.atr()` 활용)
  - ATR 배수 기반 손절가 계산: `stop_loss = entry - (ATR * 2.5)`
  - 트레일링 스탑: `trailing_stop = highest - (ATR * 2.0)`
  - 한국 시장 호가단위 반올림 적용 (`get_tick_size()` 활용)
  - `RiskDefaults.STOP_LOSS_PCT` 고정값을 ATR 기반 동적값으로 대체
- **효과**: 변동성 반영 손절, 수익 보호 극대화

#### P2-04: 매매 근거 자동 기록

- **파일**: 신규 `src/engine/trade_logger.py`, `src/engine/strategy_engine.py` 수정
- **내용**:
  - `TradeLog` 데이터클래스: 시점, 종목, 방향, 가격, 수량, 시그널 상세, 지표값, 감성 점수
  - SQLite `trade_logs` 테이블 저장
  - `StrategyEngine.evaluate_all()` 실행 시 자동 로깅
  - 사후 분석용 조회 API 제공
- **효과**: 매매 판단 투명성, 전략 개선을 위한 데이터 축적

#### P2-05: 성과 보고서 생성

- **파일**: 신규 `src/engine/report_generator.py`
- **내용**:
  - quantstats 라이브러리 연동 (HTML 티어시트 생성)
  - 일간 보고서: 당일 매매, 손익, 시그널 적중률
  - 주간/월간 보고서: 누적 수익률, MDD, Sharpe, 전략별 기여도
  - KOSPI 벤치마크 대비 초과수익률
  - PDF/HTML 형식 자동 저장 (`data/reports/`)
- **효과**: 성과 가시화, 전략 효과 정량 평가

#### P2-06: 전략 앙상블/투표 메커니즘

- **파일**: `src/engine/strategy_engine.py`
- **내용**:
  - `StrategyEngine`에 `ensemble_evaluate()` 메서드 추가
  - 등록된 전략들의 결과를 다수결(majority voting) 또는 가중합으로 합산
  - 각 전략의 confidence를 가중치로 사용
  - 합의도(agreement ratio) 계산: 전략 일치율이 높을수록 신뢰도 상향
- **효과**: 단일 전략 의존 탈피, 시그널 안정성 향상

### 5.3 Phase 3: 중기 개선 (1-2개월)

> 시스템 고도화 + 자동화

#### P3-01: RAG 시스템 (뉴스 + 재무 DB)

- **파일**: 신규 `src/ai/rag_engine.py`, `src/ai/news_analyzer.py` 수정
- **내용**:
  - 뉴스 기사 SQLite 저장 + 임베딩 벡터 생성
  - 감성분석 시 관련 과거 뉴스/재무 데이터 검색하여 컨텍스트 증강
  - 종목별 최근 7일 뉴스 히스토리 + 최근 분기 실적 데이터 제공
  - 벡터 검색: `sentence-transformers` 또는 OpenAI Embeddings API
- **효과**: 맥락 기반 분석으로 감성분석 정확도 향상, 연속적 뉴스 트렌드 파악

#### P3-02: Walk-Forward 백테스팅

- **파일**: `src/engine/backtest_engine.py`
- **내용**:
  - 데이터를 N개 윈도우로 분할 (학습 + 검증)
  - 각 윈도우에서 전략 파라미터 최적화 -> 다음 윈도우에서 성과 검증
  - 전체 검증 구간 성과를 종합하여 최종 성능 지표 산출
  - 수수료(한국 주식 0.015%) + 슬리피지(1-2 틱) 반영
  - Monte Carlo: 매매 순서 무작위화로 드로다운 분포 생성
  - KOSPI 벤치마크 비교 추가
- **효과**: 과적합 방지, 현실적 성능 평가, 숨겨진 리스크 발견

#### P3-03: 시장 상황 분류기 (상승/횡보/하락)

- **파일**: 신규 `src/engine/market_classifier.py`
- **내용**:
  - ADX + 이동평균 방향 + 볼린저밴드 폭으로 시장 레짐 분류
  - 3단계 분류: `trending_up`, `trending_down`, `ranging`
  - 분류 결과에 따라 전략 활성화/비활성화 자동 전환
  - SignalGenerator, StrategyEngine과 연동
- **효과**: 시장 상황에 부적합한 전략 자동 비활성화, 수익성 향상

#### P3-04: 전략 자동 최적화

- **파일**: 신규 `src/engine/optimizer.py`, `src/engine/backtest_engine.py` 수정
- **내용**:
  - Optuna 연동으로 전략 파라미터 자동 탐색
  - 최적화 대상: RSI 기간, MACD 파라미터, BB 기간/표준편차, 매수/매도 임계값
  - 목적함수: Sharpe Ratio 최대화 또는 Calmar Ratio 최대화
  - Walk-Forward 기반 교차검증으로 과적합 방지
  - 최적화 결과 자동 적용 또는 사용자 승인 후 적용
- **효과**: 수동 파라미터 조정 불필요, 시장 변화에 자동 적응

---

## 6. 결론

### 6.1 핵심 발견

1. **토큰 효율화가 가장 시급**: StokAI는 LLM 호출에 캐싱/배치/예산 관리가 전무하여 운영 비용이 불필요하게 높다. Phase 1에서 즉시 해결 가능.

2. **AI 분석 품질 개선 여지 큼**: 시스템 프롬프트, Few-shot, CoT 등 프롬프트 엔지니어링만으로도 분석 품질을 크게 향상할 수 있다. 코드 변경량 대비 효과가 가장 크다.

3. **리스크 관리 고도화 필요**: 고정 퍼센트 손절/포지션 사이징은 업계 수준에 크게 미달. Kelly Criterion + ATR 기반 동적 관리가 필수.

4. **백테스팅 현실성 부족**: 수수료/슬리피지 미반영, 단일 기간 백테스트만 지원하여 실전과 괴리 발생 가능. Walk-Forward + Monte Carlo로 보완 필요.

5. **매매 기록/보고서 부재**: 사후 분석과 성과 측정이 불가하여 전략 개선 루프가 없다. 자동 기록 + 보고서 생성으로 해결.

### 6.2 구현 우선순위 요약

| 우선순위 | Phase | 항목 | 효과 | 난이도 |
|---------|-------|------|------|--------|
| 1 | P1-01 | LLM 응답 캐싱 | API 비용 50%+ 절감 | 낮음 |
| 2 | P1-02 | 시스템 프롬프트 | 분석 품질 대폭 향상 | 낮음 |
| 3 | P1-03 | Few-shot 예제 | 출력 일관성 향상 | 낮음 |
| 4 | P1-05 | 토큰 추적/로깅 | 비용 가시화 | 낮음 |
| 5 | P1-04 | 뉴스 요약/절단 | 토큰 절약 | 낮음 |
| 6 | P2-03 | ATR 동적 손절 | 변동성 반영 리스크 | 중간 |
| 7 | P2-02 | Kelly 포지션 | 최적 포지션 크기 | 중간 |
| 8 | P2-01 | 동적 가중치 | 시장 적응 시그널 | 중간 |
| 9 | P2-04 | 매매 근거 기록 | 판단 투명성 | 중간 |
| 10 | P2-05 | 성과 보고서 | 성과 가시화 | 중간 |
| 11 | P2-06 | 전략 앙상블 | 시그널 안정성 | 중간 |
| 12 | P3-02 | Walk-Forward | 과적합 방지 | 높음 |
| 13 | P3-03 | 시장 분류기 | 전략 자동 전환 | 높음 |
| 14 | P3-04 | 전략 최적화 | 자동 파라미터 탐색 | 높음 |
| 15 | P3-01 | RAG 시스템 | 맥락 기반 분석 | 높음 |

### 6.3 기대 효과

- **Phase 1 완료 시**: API 비용 50%+ 절감, 감성분석 품질/일관성 대폭 향상
- **Phase 2 완료 시**: 매매 신호 신뢰도 향상, 리스크 관리 체계화, 성과 측정 가능
- **Phase 3 완료 시**: 시장 적응형 자동매매 시스템 완성, 업계 오픈소스 수준 달성

### 6.4 한국 시장 특수 고려사항

- **장 시간**: 09:00-15:30 (StokAI `config.py`에 반영됨)
- **상하한가**: 전일 종가 대비 +-30% (리스크 관리에 반영 필요)
- **호가단위**: 가격대별 차등 호가 (`risk_manager.py`에 구현됨)
- **수수료**: 증권사별 상이 (일반 0.015%, HTS/MTS 할인)
- **세금**: 매도 시 증권거래세 0.18% (KOSPI), 0.18% (KOSDAQ)
- **외국인/기관 수급**: 한국 시장의 핵심 가격 동인, 감성분석에 수급 관점 필수
- **공시 체계**: DART 전자공시 기반, 주요 공시 이벤트 모니터링 필요

---

## 참고 자료

### 경쟁 시스템
- [Freqtrade 공식 문서 - FreqAI](https://www.freqtrade.io/en/stable/freqai/)
- [FreqAI ML System - DeepWiki](https://deepwiki.com/freqtrade/freqtrade/5.1-freqai-machine-learning)
- [FinGPT GitHub](https://github.com/AI4Finance-Foundation/FinGPT)
- [FinGPT 논문 (arXiv)](https://arxiv.org/html/2306.06031v2)
- [QuantConnect Lean GitHub](https://github.com/QuantConnect/Lean)
- [QuantConnect Algorithm Framework](https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/overview)
- [Jesse 공식 사이트](https://jesse.trade/)
- [Jesse GitHub](https://github.com/jesse-ai/jesse)

### 토큰 효율화
- [LLM Token Optimization - Redis Blog](https://redis.io/blog/llm-token-optimization-speed-up-apps/)
- [Reduce LLM Costs - Glukhov](https://www.glukhov.org/post/2025/11/cost-effective-llm-applications)
- [Prompt Caching - Redis Blog](https://redis.io/blog/what-is-prompt-caching/)
- [AWS LLM Caching Guide](https://aws.amazon.com/blogs/database/optimize-llm-response-costs-and-latency-with-effective-caching/)

### 리스크 관리
- [Kelly Criterion - Zerodha Varsity](https://zerodha.com/varsity/chapter/kellys-criterion/)
- [Position Sizing Frameworks - Medium](https://medium.com/@ildiveliu/risk-before-returns-position-sizing-frameworks-fixed-fractional-atr-based-kelly-lite-4513f770a82a)
- [ATR Position Sizing - QuantStrategy.io](https://quantstrategy.io/blog/using-atr-to-adjust-position-size-volatility-based-risk/)
- [AI Trading Bot Risk Management Guide](https://3commas.io/blog/ai-trading-bot-risk-management-guide-2025)

### 백테스팅/신뢰성
- [Robustness Testing Guide - Build Alpha](https://www.buildalpha.com/robustness-testing-guide/)
- [Monte Carlo Methods - StrategyQuant](https://strategyquant.com/blog/new-robustness-tests-on-the-strategyquant-codebase-5-monte-carlo-methods-to-bulletproof-your-trading-strategies/)
- [Monte Carlo Backtesting - Medium](https://medium.com/@kridtapon/monte-carlo-simulations-in-algorithmic-trading-a-deeper-look-73a0136ecfcd)

### RAG/감성분석
- [FinGPT-RAG 감성분석 - SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5145647)
- [Agentic RAG for Stock Analysis - GitHub](https://github.com/bhanup6663/stock_agent_RAG)
- [RAG for Finance - CFA Institute](https://rpc.cfainstitute.org/research/the-automation-ahead-content-series/retrieval-augmented-generation)

### 보고서/성과분석
- [quantstats - GitHub](https://github.com/ranaroussi/quantstats)
- [Automated Market Report - GitHub](https://github.com/hgnx/automated-market-report)

### 한국 시장
- [한국투자증권 API 자동매매 튜토리얼](https://tgparkk.github.io/stock/2025/03/08/auto-stock-1-init.html)
- [파이썬 한국/미국 주식 자동매매 - WikiDocs](https://wikidocs.net/book/7845)
- [키움증권 시스템 트레이딩 - 퀀티랩](https://blog.quantylab.com/systrading.html)
