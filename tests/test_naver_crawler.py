"""T037: 네이버 금융 뉴스 크롤러 테스트"""

from unittest.mock import MagicMock, patch
from src.crawler.naver_crawler import NaverNewsCrawler

SAMPLE_HTML = """
<html><body>
<table class="type5">
  <tr>
    <td class="title"><a href="/item/news_read.nhn?code=005930&arti_id=001">삼성전자 실적 개선 기대</a></td>
    <td class="info">한국경제</td>
    <td class="date">2024.01.15 09:30</td>
    <td class="summary">삼성전자가 올해 실적 개선이 기대된다는 분석이 나왔다.</td>
  </tr>
  <tr>
    <td class="title"><a href="/item/news_read.nhn?code=005930&arti_id=002">반도체 업황 회복 신호</a></td>
    <td class="info">매일경제</td>
    <td class="date">2024.01.15 08:00</td>
    <td class="summary">반도체 시장 업황이 회복세를 보이고 있다.</td>
  </tr>
</table>
</body></html>
"""


class TestNaverNewsCrawler:
    def test_fetch_news_returns_list(self):
        """fetch_news가 리스트를 반환하는지 확인"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930")

        assert isinstance(result, list)

    def test_fetch_news_parses_title(self):
        """뉴스 제목이 올바르게 파싱되는지 확인"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930")

        assert len(result) == 2
        assert result[0]["title"] == "삼성전자 실적 개선 기대"
        assert result[1]["title"] == "반도체 업황 회복 신호"

    def test_fetch_news_dict_keys(self):
        """반환 dict가 필수 키를 모두 포함하는지 확인"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930")

        assert len(result) > 0
        item = result[0]
        for key in ("title", "url", "date", "source", "content_preview"):
            assert key in item, f"키 '{key}' 누락"

    def test_fetch_news_url_is_absolute(self):
        """URL이 절대경로로 변환되는지 확인"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930")

        assert result[0]["url"].startswith("https://finance.naver.com")

    def test_fetch_news_max_count(self):
        """max_count 제한이 적용되는지 확인"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930", max_count=1)

        assert len(result) == 1

    def test_fetch_news_empty_table(self):
        """뉴스 테이블이 없으면 빈 리스트 반환"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>no table</p></body></html>"
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930")

        assert result == []

    def test_fetch_news_source_and_date(self):
        """출처와 날짜가 올바르게 파싱되는지 확인"""
        crawler = NaverNewsCrawler()
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status = MagicMock()

        with patch("requests.Session.get", return_value=mock_response):
            result = crawler.fetch_news("005930")

        assert result[0]["source"] == "한국경제"
        assert result[0]["date"] == "2024.01.15 09:30"
