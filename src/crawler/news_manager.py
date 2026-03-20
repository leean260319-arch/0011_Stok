"""뉴스 통합 관리자
Version: 1.0.0
"""

from src.utils.logger import get_logger

logger = get_logger("crawler.news_manager")


class NewsManager:
    """여러 뉴스 소스를 통합 관리하는 클래스"""

    def __init__(self, naver_crawler, rss_crawler):
        """
        Args:
            naver_crawler: NaverNewsCrawler 인스턴스
            rss_crawler: RSSCrawler 인스턴스
        """
        self._naver = naver_crawler
        self._rss = rss_crawler

    def collect_news(self, stock_code: str) -> list[dict]:
        """모든 소스에서 뉴스 수집 후 중복 제거

        Args:
            stock_code: 종목코드

        Returns:
            중복 제거된 뉴스 목록
        """
        naver_news = self._naver.fetch_news(stock_code)
        rss_news = self._rss.fetch_all()
        combined = naver_news + rss_news
        result = self.deduplicate(combined)
        logger.info("종목 %s 뉴스 수집 완료: %d건 (중복 제거 후)", stock_code, len(result))
        return result

    def deduplicate(self, news_list: list[dict]) -> list[dict]:
        """URL 기반 중복 제거

        Args:
            news_list: 뉴스 목록

        Returns:
            중복 제거된 뉴스 목록 (첫 번째 등장 항목 유지)
        """
        seen_urls: set[str] = set()
        result = []
        for item in news_list:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                result.append(item)
            elif not url:
                result.append(item)
        return result
