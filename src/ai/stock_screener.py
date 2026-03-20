"""AI 종목 자동 스크리너 - 3단계 필터링 파이프라인

버전: 1.0.0
작성일: 2026-03-18
설명: KOSPI/KOSDAQ에서 AI 기반 매매 대상 종목 자동 선정
      1단계: 유니버스 필터 (시가총액/거래량/가격)
      2단계: 기술지표 스코어링
      3단계: AI 종합 평가 (감성+기술 결합)
"""

from dataclasses import dataclass, field

from src.utils.logger import get_logger

logger = get_logger("ai.stock_screener")


@dataclass
class ScreenerResult:
    """스크리닝 결과 단일 종목"""

    code: str
    name: str
    total_score: float = 0.0
    technical_score: float = 0.0
    sentiment_score: float = 0.0
    signal: str = "관망"
    reasons: list[str] = field(default_factory=list)


class StockScreener:
    """AI 기반 종목 자동 스크리너.

    파이프라인:
      1단계 - 유니버스 필터: 시가총액/거래량/가격 기본 필터
      2단계 - 기술지표 스코어링: RSI/MACD/BB/ADX/OBV 기반 기술적 점수
      3단계 - AI 종합 평가: 뉴스 감성 + 기술지표 통합 점수로 최종 랭킹
    """

    # 1단계 필터 기본값
    MIN_MARKET_CAP = 100_000_000_000  # 시가총액 최소 1000억원
    MIN_VOLUME = 100_000  # 최소 일 거래량 10만주
    MIN_PRICE = 1_000  # 최소 주가 1000원 (동전주 제외)
    MAX_STOCKS_STAGE1 = 100  # 1단계 통과 최대 종목 수

    # 2단계 기술지표 필터
    MAX_STOCKS_STAGE2 = 30  # 2단계 통과 최대 종목 수

    # 3단계 AI 평가
    MAX_FINAL_PICKS = 10  # 최종 선정 종목 수

    def __init__(
        self,
        market_data_provider,
        news_analyzer=None,
        sentiment_scorer=None,
        ai_scorer=None,
        llm_service=None,
        news_manager=None,
    ):
        self._market_data = market_data_provider
        self._news_analyzer = news_analyzer
        self._sentiment_scorer = sentiment_scorer
        self._ai_scorer = ai_scorer
        self._llm_service = llm_service
        self._news_manager = news_manager
        logger.info("StockScreener 초기화 완료")

    # === 전체 파이프라인 ===

    def screen(
        self,
        market: str = "ALL",
        max_picks: int = 10,
        min_market_cap: int = 0,
        include_sentiment: bool = True,
    ) -> list[ScreenerResult]:
        """3단계 파이프라인으로 종목 스크리닝 실행.

        Args:
            market: "KOSPI" | "KOSDAQ" | "ALL"
            max_picks: 최종 선정 종목 수
            min_market_cap: 최소 시가총액 (0이면 기본값)
            include_sentiment: 뉴스 감성분석 포함 여부

        Returns:
            total_score 내림차순 정렬된 ScreenerResult 리스트
        """
        logger.info(
            "스크리닝 시작: market=%s, max_picks=%d, sentiment=%s",
            market, max_picks, include_sentiment,
        )

        # 1단계: 유니버스 필터
        all_stocks = self._get_stock_universe(market)
        filtered = self._filter_universe(all_stocks, min_market_cap or self.MIN_MARKET_CAP)
        logger.info("1단계 유니버스 필터: %d -> %d종목", len(all_stocks), len(filtered))

        if not filtered:
            logger.warning("1단계 필터 통과 종목 없음")
            return []

        # 2단계: 기술지표 스코어링
        scored = self._filter_by_technical(filtered)
        logger.info("2단계 기술지표 필터: %d -> %d종목", len(filtered), len(scored))

        if not scored:
            logger.warning("2단계 필터 통과 종목 없음")
            return []

        # 3단계: AI 종합 평가
        results = self._rank_final(scored, max_picks, include_sentiment)
        logger.info("3단계 최종 선정: %d종목", len(results))

        for r in results:
            logger.info(
                "  [%s] %s: score=%.3f, signal=%s, reasons=%s",
                r.code, r.name, r.total_score, r.signal, r.reasons[:3],
            )

        return results

    def screen_quick(
        self,
        market: str = "ALL",
        max_picks: int = 5,
    ) -> list[ScreenerResult]:
        """빠른 스크리닝 (뉴스 분석 스킵, 기술지표만).

        LLM API 호출 없이 빠르게 종목 선정.
        """
        return self.screen(
            market=market,
            max_picks=max_picks,
            include_sentiment=False,
        )

    # === 1단계: 유니버스 필터 ===

    def _get_stock_universe(self, market: str) -> list[dict]:
        """시장에 따라 종목 목록 조회."""
        if market == "KOSPI":
            return self._market_data.get_kospi_codes()
        elif market == "KOSDAQ":
            return self._market_data.get_kosdaq_codes()
        else:
            return self._market_data.get_all_codes()

    def _filter_universe(
        self,
        all_stocks: list[dict],
        min_market_cap: int,
    ) -> list[dict]:
        """시가총액, 거래량, 최소가격 기준으로 기본 필터링.

        FDR StockListing 데이터에 이미 close/volume/market_cap 포함되어 있으므로
        추가 API 호출 없이 필터링 가능.
        """
        filtered = []

        for stock in all_stocks:
            # 시가총액 필터
            if stock.get("market_cap", 0) < min_market_cap:
                continue
            # 거래량 필터 (StockListing에 포함)
            if stock.get("volume", 0) < self.MIN_VOLUME:
                continue
            # 최소 가격 필터
            if stock.get("close", 0) < self.MIN_PRICE:
                continue
            filtered.append(stock)

        # 시가총액 내림차순 정렬
        filtered.sort(key=lambda x: x.get("market_cap", 0), reverse=True)

        # 상위 MAX_STOCKS_STAGE1개만
        filtered = filtered[: self.MAX_STOCKS_STAGE1]

        # StockListing 데이터로 snapshot 생성 (추가 API 호출 불필요)
        from src.data.market_data_provider import StockSnapshot
        for stock in filtered:
            stock["snapshot"] = StockSnapshot(
                code=stock["code"],
                name=stock.get("name", ""),
                current_price=stock.get("close", 0),
                open_price=stock.get("open", 0),
                high_price=stock.get("high", 0),
                low_price=stock.get("low", 0),
                volume=stock.get("volume", 0),
                market_cap=stock.get("market_cap", 0),
                change_rate=stock.get("change_rate", 0.0),
            )

        return filtered

    # === 2단계: 기술지표 스코어링 ===

    def _score_technical(self, stock: dict) -> dict | None:
        """단일 종목의 기술지표 점수를 계산."""
        from src.engine.chart_analyzer import ChartAnalyzer
        from src.engine.signal_generator import SignalGenerator

        code = stock["code"]

        df = self._market_data.get_ohlcv_history(code, days=120)
        if df is None or len(df) < 20:
            return None

        analyzer = ChartAnalyzer(df)
        sg = SignalGenerator(analyzer)
        signal_result = sg.generate_signal()

        stock["technical_score"] = signal_result["score"]
        stock["signal"] = signal_result["signal"]
        stock["reasons"] = signal_result["reasons"]
        return stock

    def _filter_by_technical(self, stocks: list[dict]) -> list[dict]:
        """기술지표 점수 기반 필터링."""
        scored = []
        for stock in stocks:
            result = self._score_technical(stock)
            if result is not None:
                scored.append(result)

        # technical_score 내림차순 정렬
        scored.sort(key=lambda x: x.get("technical_score", 0), reverse=True)

        # 상위 MAX_STOCKS_STAGE2개
        return scored[: self.MAX_STOCKS_STAGE2]

    # === 3단계: AI 종합 평가 ===

    def _score_sentiment(self, stock: dict) -> float:
        """종목 뉴스 감성 점수 계산."""
        if not self._news_manager or not self._news_analyzer:
            return 0.0

        name = stock.get("name", "")
        if not name:
            return 0.0

        articles = self._news_manager.collect_news(name)
        if not articles:
            return 0.0

        scores = []
        for article in articles[:5]:  # 최대 5개 뉴스만 분석 (비용 제어)
            result = self._news_analyzer.analyze_sentiment(article)
            if result and "score" in result:
                from datetime import datetime
                scores.append({
                    "score": result["score"],
                    "timestamp": datetime.now().isoformat(),
                })

        if not scores and not self._sentiment_scorer:
            return 0.0

        if scores and self._sentiment_scorer:
            return self._sentiment_scorer.calculate_weighted_score(scores)

        if scores:
            return sum(s["score"] for s in scores) / len(scores)

        return 0.0

    def _rank_final(
        self,
        stocks: list[dict],
        max_picks: int,
        include_sentiment: bool = True,
    ) -> list[ScreenerResult]:
        """감성 + 기술지표 결합으로 최종 랭킹."""
        results = []

        for stock in stocks:
            technical_score = stock.get("technical_score", 0.0)

            # 감성 점수
            sentiment_score = 0.0
            if include_sentiment:
                sentiment_score = self._score_sentiment(stock)

            # AI 종합 점수
            if self._ai_scorer:
                ai_result = self._ai_scorer.calculate_score(
                    sentiment_score=sentiment_score,
                    technical_score=technical_score,
                )
                total_score = ai_result["total_score"]
                signal = ai_result["signal"]
            else:
                total_score = technical_score
                signal = stock.get("signal", "관망")

            snapshot = stock.get("snapshot")
            name = stock.get("name", "")
            if snapshot:
                name = snapshot.name or name

            reasons = list(stock.get("reasons", []))
            if sentiment_score != 0:
                reasons.append(f"뉴스감성: {sentiment_score:+.2f}")
            if snapshot:
                reasons.append(f"현재가: {snapshot.current_price:,}원")
                reasons.append(f"거래량: {snapshot.volume:,}")

            results.append(ScreenerResult(
                code=stock["code"],
                name=name,
                total_score=total_score,
                technical_score=technical_score,
                sentiment_score=sentiment_score,
                signal=signal,
                reasons=reasons,
            ))

        # total_score 내림차순 정렬 (매수 시그널 우선)
        results.sort(key=lambda x: x.total_score, reverse=True)

        return results[:max_picks]
