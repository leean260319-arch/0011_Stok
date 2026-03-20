"""서비스 컨테이너 - 앱 전체 서비스 생성/관리/주입"""

# v1.0 - 2026-03-17: 신규 작성

import os

from src.utils.logger import get_logger

logger = get_logger("service_container")


class ServiceContainer:
    """앱 전체 서비스의 생명주기를 관리한다."""

    def __init__(self, config_manager):
        """
        Args:
            config_manager: ConfigManager 인스턴스 (get/set 메서드 제공)
        """
        self._config = config_manager
        self._db = None
        self._bridge = None
        self._llm_service = None
        self._news_analyzer = None
        self._sentiment_scorer = None
        self._strategy_engine = None
        self._risk_manager = None
        self._ai_scorer = None
        self._trade_logger = None
        self._alert_manager = None
        self._news_scheduler = None
        self._market_data_provider = None
        self._stock_screener = None
        self._virtual_portfolio = None

    # ------------------------------------------------------------------
    # 초기화 메서드
    # ------------------------------------------------------------------

    def init_db(self):
        """DB 초기화 (SQLCipher) - init_db 함수로 테이블 자동 생성."""
        from src.db.database import init_db
        from src.utils.constants import DB_PATH

        password = self._config.get("db.password", "")
        if not password:
            import secrets
            password = secrets.token_urlsafe(16)
            self._config.set("db.password", password)
            from src.utils.constants import CONFIG_PATH
            self._config.save(CONFIG_PATH, self._config.get_all())
            logger.info("DB 비밀번호 자동 생성됨")
        self._db = init_db(db_path=DB_PATH, password=password)
        logger.info("DB 초기화 완료")

    def init_bridge(self):
        """키움 API 브릿지 초기화 + 내장 gRPC 서버 시작."""
        from src.bridge.kiwoom_bridge import KiwoomBridge
        from src.bridge.kiwoom_server import serve as start_grpc_server

        # 내장 gRPC 서버 시작 (개발/테스트용 stub 서버)
        self._grpc_server = start_grpc_server()
        logger.info("내장 gRPC 서버 시작 (stub)")

        # 브릿지 생성 + 자동 연결
        self._bridge = KiwoomBridge()
        self._bridge.connect()
        logger.info("KiwoomBridge 연결 완료")

    def init_ai(self):
        """LLM 서비스 + 뉴스 분석기 + 감성 점수 집계기 초기화."""
        from src.ai.llm_service import LLMService, CloudLLMProvider
        from src.ai.news_analyzer import NewsAnalyzer
        from src.ai.sentiment_scorer import SentimentScorer

        primary_key = self._config.get("ai.primary_api_key", "")
        primary = CloudLLMProvider(
            api_key=primary_key,
            model=self._config.get("ai.primary_model", "gpt-4o-mini"),
            base_url=self._config.get("ai.primary_base_url", "https://api.openai.com/v1"),
        )

        fallback_key = self._config.get("ai.fallback_api_key", "")
        fallback = None
        if fallback_key:
            fallback = CloudLLMProvider(
                api_key=fallback_key,
                model=self._config.get("ai.fallback_model", "deepseek-chat"),
                base_url=self._config.get("ai.fallback_base_url", "https://api.deepseek.com/v1"),
            )

        self._llm_service = LLMService(primary=primary, fallback=fallback)
        self._news_analyzer = NewsAnalyzer(llm_service=self._llm_service)
        self._sentiment_scorer = SentimentScorer()
        logger.info("AI 서비스 초기화 완료")

    def init_engine(self):
        """매매 엔진 컴포넌트들 초기화."""
        from src.engine.strategy_engine import (
            StrategyEngine,
            MomentumStrategy,
            MeanReversionStrategy,
            AICompositeStrategy,
        )
        from src.engine.risk_manager import RiskManager
        from src.engine.ai_scorer import AIScorer
        from src.engine.trade_logger import TradeLogger

        # StrategyEngine + 기본 전략 등록
        self._strategy_engine = StrategyEngine()
        self._strategy_engine.register_strategy(MomentumStrategy())
        self._strategy_engine.register_strategy(MeanReversionStrategy())

        # RiskManager
        self._risk_manager = RiskManager()

        # AIScorer
        self._ai_scorer = AIScorer()

        # AICompositeStrategy - AIScorer 생성 후 등록
        self._strategy_engine.register_strategy(AICompositeStrategy(self._ai_scorer))

        # TradeLogger (기본 경로 사용)
        self._trade_logger = TradeLogger()

        logger.info("매매 엔진 초기화 완료")

    def init_scheduler(self):
        """뉴스 수집 스케줄러 초기화."""
        from src.crawler.news_scheduler import NewsScheduler
        from src.crawler.news_manager import NewsManager
        from src.crawler.naver_crawler import NaverNewsCrawler
        from src.crawler.rss_crawler import RSSCrawler

        naver_crawler = NaverNewsCrawler()
        rss_feeds = self._config.get("news.rss_feeds", [
            "https://news.google.com/rss/search?q=주식&hl=ko&gl=KR&ceid=KR:ko",
        ])
        rss_crawler = RSSCrawler(feed_urls=rss_feeds)
        news_manager = NewsManager(naver_crawler, rss_crawler)
        interval = self._config.get("news.interval_minutes", 10)
        self._news_scheduler = NewsScheduler(news_manager, interval_minutes=interval)
        logger.info("NewsScheduler 초기화 완료")

    def init_market_data(self):
        """시장 데이터 프로바이더 + 가상 포트폴리오 초기화."""
        from src.data.market_data_provider import MarketDataProvider
        from src.engine.virtual_portfolio import VirtualPortfolio

        cache_ttl = self._config.get("market.cache_ttl_seconds", 60)
        self._market_data_provider = MarketDataProvider(cache_ttl_seconds=cache_ttl)

        initial_cash = self._config.get("virtual_portfolio.initial_cash", 10_000_000)
        self._virtual_portfolio = VirtualPortfolio(initial_cash=initial_cash)

        logger.info("MarketDataProvider + VirtualPortfolio 초기화 완료")

    def init_screener(self):
        """AI 종목 스크리너 초기화. init_ai, init_engine, init_market_data 이후 호출."""
        from src.ai.stock_screener import StockScreener

        news_manager = None
        if self._news_scheduler and hasattr(self._news_scheduler, '_manager'):
            news_manager = self._news_scheduler._manager

        self._stock_screener = StockScreener(
            market_data_provider=self._market_data_provider,
            news_analyzer=self._news_analyzer,
            sentiment_scorer=self._sentiment_scorer,
            ai_scorer=self._ai_scorer,
            llm_service=self._llm_service,
            news_manager=news_manager,
        )
        logger.info("StockScreener 초기화 완료")

    def init_alerts(self):
        """알림 매니저 초기화."""
        from src.ui.alert_manager import AlertManager

        self._alert_manager = AlertManager()
        logger.info("AlertManager 초기화 완료")

    def init_all(self):
        """모든 서비스 초기화 (순서 보장)."""
        self.init_db()
        self.init_bridge()
        self.init_market_data()
        self.init_ai()
        self.init_engine()
        self.init_alerts()
        self.init_scheduler()
        self.init_screener()
        logger.info("전체 서비스 초기화 완료")

    # ------------------------------------------------------------------
    # 종료
    # ------------------------------------------------------------------

    def shutdown(self):
        """모든 서비스를 안전하게 종료한다."""
        if self._news_scheduler and self._news_scheduler.is_running:
            self._news_scheduler.stop()
            logger.info("NewsScheduler 종료")

        if self._llm_service and hasattr(self._llm_service, '_cache'):
            self._llm_service._cache.close()
            logger.info("LLMCache 종료")

        if self._trade_logger:
            self._trade_logger.close()
            logger.info("TradeLogger 종료")

        if self._db:
            self._db.close()
            logger.info("DB 연결 종료")

        if self._bridge and self._bridge.is_connected:
            self._bridge.disconnect()
            logger.info("KiwoomBridge 연결 종료")

        if hasattr(self, '_grpc_server') and self._grpc_server:
            self._grpc_server.stop(grace=2)
            logger.info("내장 gRPC 서버 종료")

        logger.info("전체 서비스 종료 완료")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def db(self):
        return self._db

    @property
    def bridge(self):
        return self._bridge

    @property
    def llm_service(self):
        return self._llm_service

    @property
    def news_analyzer(self):
        return self._news_analyzer

    @property
    def sentiment_scorer(self):
        return self._sentiment_scorer

    @property
    def strategy_engine(self):
        return self._strategy_engine

    @property
    def risk_manager(self):
        return self._risk_manager

    @property
    def ai_scorer(self):
        return self._ai_scorer

    @property
    def trade_logger(self):
        return self._trade_logger

    @property
    def alert_manager(self):
        return self._alert_manager

    @property
    def news_scheduler(self):
        return self._news_scheduler

    @property
    def market_data_provider(self):
        return self._market_data_provider

    @property
    def virtual_portfolio(self):
        return self._virtual_portfolio

    @property
    def stock_screener(self):
        return self._stock_screener

    @property
    def config(self):
        return self._config
