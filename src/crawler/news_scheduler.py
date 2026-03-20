"""뉴스 수집 스케줄러 - 주기적 뉴스 크롤링 및 감성분석
v1.0 - 2026-03-17: 신규 작성
v1.1 - 2026-03-17: H5 QThread 기반 워커로 메인 스레드 블로킹 방지
"""

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QThread
from src.crawler.news_manager import NewsManager
from src.utils.logger import get_logger

logger = get_logger("crawler.scheduler")


class _FetchWorker(QThread):
    """백그라운드에서 뉴스를 수집하는 워커."""

    finished = pyqtSignal(list)

    def __init__(self, manager: NewsManager, stock_codes: list[str]):
        super().__init__()
        self._manager = manager
        self._codes = list(stock_codes)

    def run(self):
        all_articles = []
        for code in self._codes:
            articles = self._manager.collect_news(code)
            all_articles.extend(articles)
        self.finished.emit(all_articles)


class NewsScheduler(QObject):
    """주기적으로 뉴스를 수집하고 결과를 시그널로 발행한다.

    Signals:
        news_fetched: 새 뉴스 수집 완료 시 (list[dict])
        fetch_error: 수집 중 에러 발생 시 (str)
    """

    news_fetched = pyqtSignal(list)
    fetch_error = pyqtSignal(str)

    def __init__(self, news_manager: NewsManager, interval_minutes: int = 10):
        super().__init__()
        self._manager = news_manager
        self._interval = interval_minutes * 60 * 1000  # ms
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._fetch)
        self._stock_codes: list[str] = []
        self._running = False

    def set_stock_codes(self, codes: list[str]):
        """수집 대상 종목 코드 설정"""
        self._stock_codes = list(codes)

    def start(self):
        """스케줄러 시작"""
        if self._running:
            return
        self._running = True
        self._timer.start(self._interval)
        self._fetch()  # 즉시 1회 실행
        logger.info("뉴스 스케줄러 시작: %d분 간격", self._interval // 60000)

    def stop(self):
        """스케줄러 중지"""
        self._running = False
        self._timer.stop()
        logger.info("뉴스 스케줄러 중지")

    @property
    def is_running(self) -> bool:
        return self._running

    def _fetch(self):
        """뉴스 수집 실행 - 백그라운드 워커로 위임."""
        if not self._stock_codes:
            return

        if hasattr(self, "_worker") and self._worker.isRunning():
            return  # 이전 수집이 아직 실행 중이면 건너뜀

        self._worker = _FetchWorker(self._manager, self._stock_codes)
        self._worker.finished.connect(self._on_fetch_done)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.start()

    def _on_fetch_done(self, articles: list):
        """워커 완료 콜백."""
        if articles:
            self.news_fetched.emit(articles)
            logger.info("뉴스 수집 완료: %d건", len(articles))
