"""RSS 피드 크롤러
Version: 1.0.0
"""

import feedparser
from src.utils.logger import get_logger

logger = get_logger("crawler.rss")


class RSSCrawler:
    """RSS 피드 뉴스 크롤러"""

    def __init__(self, feed_urls: list[str]):
        """
        Args:
            feed_urls: RSS 피드 URL 목록
        """
        self._feed_urls = feed_urls

    def fetch_all(self) -> list[dict]:
        """모든 RSS 피드에서 뉴스 수집

        Returns:
            list of dict with keys: title, url, date, source, summary
        """
        results = []
        for url in self._feed_urls:
            feed = feedparser.parse(url)
            source = feed.feed.get("title", url)
            for entry in feed.entries:
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                summary = entry.get("summary", "")

                results.append(
                    {
                        "title": title,
                        "url": link,
                        "date": published,
                        "source": source,
                        "summary": summary,
                    }
                )

        logger.info("RSS 뉴스 총 %d건 수집 (피드 %d개)", len(results), len(self._feed_urls))
        return results
