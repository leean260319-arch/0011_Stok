"""네이버 금융 뉴스 크롤러
Version: 1.0.0
"""

import requests
from bs4 import BeautifulSoup
from src.utils.logger import get_logger

logger = get_logger("crawler.naver")

NAVER_NEWS_URL = "https://finance.naver.com/item/news_news.nhn"


class NaverNewsCrawler:
    """네이버 금융 종목 뉴스 크롤러"""

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
        )

    def fetch_news(self, stock_code: str, max_count: int = 20) -> list[dict]:
        """종목코드 기준 뉴스 목록 수집

        Args:
            stock_code: 종목코드 (예: '005930')
            max_count: 최대 수집 건수

        Returns:
            list of dict with keys: title, url, date, source, content_preview
        """
        params = {"code": stock_code, "page": 1}
        response = self._session.get(NAVER_NEWS_URL, params=params, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        return self._parse_news(soup, max_count)

    def _parse_news(self, soup: BeautifulSoup, max_count: int) -> list[dict]:
        """BeautifulSoup 객체에서 뉴스 파싱"""
        results = []
        table = soup.find("table", class_="type5")
        if table is None:
            logger.warning("뉴스 테이블을 찾을 수 없습니다.")
            return results

        rows = table.find_all("tr")
        for row in rows:
            if len(results) >= max_count:
                break

            info_td = row.find("td", class_="title")
            if info_td is None:
                continue

            a_tag = info_td.find("a")
            if a_tag is None:
                continue

            title = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            url = f"https://finance.naver.com{href}" if href.startswith("/") else href

            date_td = row.find("td", class_="date")
            date = date_td.get_text(strip=True) if date_td else ""

            source_td = row.find("td", class_="info")
            source = source_td.get_text(strip=True) if source_td else ""

            content_td = row.find("td", class_="summary")
            content_preview = content_td.get_text(strip=True) if content_td else ""

            results.append(
                {
                    "title": title,
                    "url": url,
                    "date": date,
                    "source": source,
                    "content_preview": content_preview,
                }
            )

        logger.info("네이버 뉴스 %d건 수집", len(results))
        return results
