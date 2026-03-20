"""뉴스 수집 스케줄러 테스트
v1.0 - 2026-03-17: 신규 작성
v1.1 - 2026-03-17: QThread 기반 비동기 워커 대응
"""

from unittest.mock import MagicMock, patch
from src.crawler.news_scheduler import NewsScheduler


def _wait_worker(scheduler):
    """워커 스레드가 존재하면 완료를 대기한다."""
    if hasattr(scheduler, "_worker") and scheduler._worker is not None:
        scheduler._worker.wait()


def _make_manager(news_by_code=None):
    """테스트용 NewsManager 목 생성"""
    manager = MagicMock()
    if news_by_code is None:
        news_by_code = {}
    manager.collect_news.side_effect = lambda code: news_by_code.get(code, [])
    return manager


class TestNewsScheduler:
    def test_creation(self, qapp):
        """NewsScheduler 인스턴스 생성"""
        manager = _make_manager()
        scheduler = NewsScheduler(manager, interval_minutes=5)
        assert scheduler is not None
        assert not scheduler.is_running

    def test_set_stock_codes(self, qapp):
        """종목 코드 설정"""
        manager = _make_manager()
        scheduler = NewsScheduler(manager)
        scheduler.set_stock_codes(["005930", "035420"])
        assert scheduler._stock_codes == ["005930", "035420"]

    def test_start_sets_running(self, qapp):
        """start 호출 시 is_running True"""
        manager = _make_manager()
        scheduler = NewsScheduler(manager)
        scheduler.set_stock_codes(["005930"])
        scheduler.start()
        _wait_worker(scheduler)
        assert scheduler.is_running
        scheduler.stop()

    def test_stop_sets_not_running(self, qapp):
        """stop 호출 시 is_running False"""
        manager = _make_manager()
        scheduler = NewsScheduler(manager)
        scheduler.set_stock_codes(["005930"])
        scheduler.start()
        _wait_worker(scheduler)
        scheduler.stop()
        assert not scheduler.is_running

    def test_start_calls_fetch_immediately(self, qapp):
        """start 시 즉시 1회 수집 실행"""
        news = {"005930": [{"title": "뉴스1", "url": "https://a.com/1"}]}
        manager = _make_manager(news)
        scheduler = NewsScheduler(manager, interval_minutes=60)
        scheduler.set_stock_codes(["005930"])
        scheduler.start()
        _wait_worker(scheduler)

        manager.collect_news.assert_called_with("005930")
        scheduler.stop()

    def test_fetch_emits_news_fetched(self, qapp):
        """수집 결과가 news_fetched 시그널로 발행"""
        news = {"005930": [{"title": "뉴스1", "url": "https://a.com/1"}]}
        manager = _make_manager(news)
        scheduler = NewsScheduler(manager, interval_minutes=60)
        scheduler.set_stock_codes(["005930"])

        received = []
        scheduler.news_fetched.connect(lambda articles: received.extend(articles))
        scheduler.start()
        _wait_worker(scheduler)
        qapp.processEvents()

        assert len(received) == 1
        assert received[0]["title"] == "뉴스1"
        scheduler.stop()

    def test_fetch_multiple_codes(self, qapp):
        """여러 종목 수집 시 결과가 합쳐짐"""
        news = {
            "005930": [{"title": "삼성", "url": "https://a.com/1"}],
            "035420": [{"title": "네이버", "url": "https://b.com/1"}],
        }
        manager = _make_manager(news)
        scheduler = NewsScheduler(manager, interval_minutes=60)
        scheduler.set_stock_codes(["005930", "035420"])

        received = []
        scheduler.news_fetched.connect(lambda articles: received.extend(articles))
        scheduler.start()
        _wait_worker(scheduler)
        qapp.processEvents()

        assert len(received) == 2
        scheduler.stop()

    def test_fetch_no_codes_skips(self, qapp):
        """종목 코드 미설정 시 수집 건너뜀"""
        manager = _make_manager()
        scheduler = NewsScheduler(manager, interval_minutes=60)
        scheduler.start()
        _wait_worker(scheduler)

        manager.collect_news.assert_not_called()
        scheduler.stop()

    def test_fetch_empty_result_no_signal(self, qapp):
        """수집 결과가 비어있으면 시그널 미발행"""
        manager = _make_manager({"005930": []})
        scheduler = NewsScheduler(manager, interval_minutes=60)
        scheduler.set_stock_codes(["005930"])

        received = []
        scheduler.news_fetched.connect(lambda articles: received.extend(articles))
        scheduler.start()
        _wait_worker(scheduler)
        qapp.processEvents()

        assert len(received) == 0
        scheduler.stop()

    def test_start_twice_no_duplicate(self, qapp):
        """start 두 번 호출해도 중복 실행 안 됨"""
        news = {"005930": [{"title": "뉴스1", "url": "https://a.com/1"}]}
        manager = _make_manager(news)
        scheduler = NewsScheduler(manager, interval_minutes=60)
        scheduler.set_stock_codes(["005930"])
        scheduler.start()
        _wait_worker(scheduler)
        scheduler.start()  # 두 번째 호출

        # collect_news는 start에서 1회만 호출
        assert manager.collect_news.call_count == 1
        scheduler.stop()

    def test_default_interval(self, qapp):
        """기본 간격은 10분(600000ms)"""
        manager = _make_manager()
        scheduler = NewsScheduler(manager)
        assert scheduler._interval == 600000
