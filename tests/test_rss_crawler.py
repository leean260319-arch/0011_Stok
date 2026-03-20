"""T038: RSS 피드 크롤러 테스트"""

from unittest.mock import patch, MagicMock
from src.crawler.rss_crawler import RSSCrawler


def _make_feed(title, entries):
    """feedparser 응답 형태의 mock 객체 생성"""
    feed_obj = MagicMock()
    feed_obj.feed.get = lambda key, default="": title if key == "title" else default
    feed_obj.entries = entries
    return feed_obj


def _make_entry(title, link, published, summary):
    entry = MagicMock()
    entry.get = lambda key, default="": {
        "title": title,
        "link": link,
        "published": published,
        "summary": summary,
    }.get(key, default)
    return entry


class TestRSSCrawler:
    def test_fetch_all_returns_list(self):
        """fetch_all이 리스트를 반환하는지 확인"""
        entries = [_make_entry("테스트 뉴스", "https://example.com/1", "Mon, 15 Jan 2024", "내용")]
        mock_feed = _make_feed("테스트 피드", entries)

        with patch("feedparser.parse", return_value=mock_feed):
            crawler = RSSCrawler(["https://rss.example.com"])
            result = crawler.fetch_all()

        assert isinstance(result, list)

    def test_fetch_all_dict_keys(self):
        """반환 dict가 필수 키를 모두 포함하는지 확인"""
        entries = [_make_entry("테스트 뉴스", "https://example.com/1", "Mon, 15 Jan 2024", "내용")]
        mock_feed = _make_feed("테스트 피드", entries)

        with patch("feedparser.parse", return_value=mock_feed):
            crawler = RSSCrawler(["https://rss.example.com"])
            result = crawler.fetch_all()

        assert len(result) == 1
        item = result[0]
        for key in ("title", "url", "date", "source", "summary"):
            assert key in item, f"키 '{key}' 누락"

    def test_fetch_all_multiple_feeds(self):
        """여러 피드에서 뉴스를 수집하는지 확인"""
        entry1 = _make_entry("뉴스1", "https://a.com/1", "2024-01-15", "내용1")
        entry2 = _make_entry("뉴스2", "https://b.com/2", "2024-01-15", "내용2")
        feed1 = _make_feed("피드A", [entry1])
        feed2 = _make_feed("피드B", [entry2])

        with patch("feedparser.parse", side_effect=[feed1, feed2]):
            crawler = RSSCrawler(["https://rss.a.com", "https://rss.b.com"])
            result = crawler.fetch_all()

        assert len(result) == 2

    def test_fetch_all_empty_feed(self):
        """항목 없는 피드는 빈 결과 반환"""
        mock_feed = _make_feed("빈 피드", [])

        with patch("feedparser.parse", return_value=mock_feed):
            crawler = RSSCrawler(["https://rss.example.com"])
            result = crawler.fetch_all()

        assert result == []

    def test_fetch_all_no_feeds(self):
        """피드 URL이 없으면 빈 리스트 반환"""
        crawler = RSSCrawler([])
        result = crawler.fetch_all()
        assert result == []

    def test_fetch_all_source_from_feed_title(self):
        """source 필드가 피드 제목으로 설정되는지 확인"""
        entries = [_make_entry("뉴스", "https://example.com/1", "2024-01-15", "내용")]
        mock_feed = _make_feed("한국경제TV", entries)

        with patch("feedparser.parse", return_value=mock_feed):
            crawler = RSSCrawler(["https://rss.example.com"])
            result = crawler.fetch_all()

        assert result[0]["source"] == "한국경제TV"
