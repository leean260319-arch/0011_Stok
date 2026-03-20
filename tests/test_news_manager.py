"""T039: 뉴스 통합 관리자 테스트"""

from unittest.mock import MagicMock
from src.crawler.news_manager import NewsManager


def _make_naver(news_list):
    crawler = MagicMock()
    crawler.fetch_news.return_value = news_list
    return crawler


def _make_rss(news_list):
    crawler = MagicMock()
    crawler.fetch_all.return_value = news_list
    return crawler


class TestNewsManager:
    def test_collect_news_combines_sources(self):
        """naver + rss 뉴스를 합쳐서 반환하는지 확인"""
        naver = _make_naver([{"title": "N1", "url": "https://n.com/1"}])
        rss = _make_rss([{"title": "R1", "url": "https://r.com/1"}])
        manager = NewsManager(naver, rss)

        result = manager.collect_news("005930")
        assert len(result) == 2

    def test_collect_news_calls_naver_with_stock_code(self):
        """naver_crawler.fetch_news에 종목코드가 전달되는지 확인"""
        naver = _make_naver([])
        rss = _make_rss([])
        manager = NewsManager(naver, rss)

        manager.collect_news("035420")
        naver.fetch_news.assert_called_once_with("035420")

    def test_deduplicate_removes_same_url(self):
        """동일 URL의 중복 항목이 제거되는지 확인"""
        news_list = [
            {"title": "뉴스1", "url": "https://example.com/1"},
            {"title": "뉴스1 복사본", "url": "https://example.com/1"},
            {"title": "뉴스2", "url": "https://example.com/2"},
        ]
        manager = NewsManager(MagicMock(), MagicMock())
        result = manager.deduplicate(news_list)

        assert len(result) == 2
        urls = [item["url"] for item in result]
        assert urls.count("https://example.com/1") == 1

    def test_deduplicate_keeps_first_occurrence(self):
        """중복 시 첫 번째 항목이 유지되는지 확인"""
        news_list = [
            {"title": "원본", "url": "https://example.com/1"},
            {"title": "복사본", "url": "https://example.com/1"},
        ]
        manager = NewsManager(MagicMock(), MagicMock())
        result = manager.deduplicate(news_list)

        assert result[0]["title"] == "원본"

    def test_deduplicate_empty_list(self):
        """빈 리스트 입력 시 빈 리스트 반환"""
        manager = NewsManager(MagicMock(), MagicMock())
        assert manager.deduplicate([]) == []

    def test_collect_news_deduplicates(self):
        """collect_news에서 중복이 제거되는지 확인"""
        shared_url = "https://example.com/shared"
        naver = _make_naver([{"title": "N", "url": shared_url}])
        rss = _make_rss([{"title": "R", "url": shared_url}])
        manager = NewsManager(naver, rss)

        result = manager.collect_news("005930")
        urls = [item["url"] for item in result]
        assert urls.count(shared_url) == 1

    def test_deduplicate_no_url_items_kept(self):
        """url 필드가 없는 항목은 중복 제거 없이 유지"""
        news_list = [
            {"title": "url없음1"},
            {"title": "url없음2"},
        ]
        manager = NewsManager(MagicMock(), MagicMock())
        result = manager.deduplicate(news_list)
        assert len(result) == 2
