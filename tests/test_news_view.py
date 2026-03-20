"""T070-T072 뉴스 분석 뷰 테스트
버전: v1.0
"""
import pytest
from datetime import datetime

from src.ui.news_view import NewsView, SentimentTrendChart, NewsSummaryPanel
from src.utils.constants import Colors


class TestNewsView:
    """T070 NewsView 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = NewsView()
        assert w is not None

    def test_add_news(self, qapp):
        """뉴스 추가."""
        w = NewsView()
        w.add_news("반도체 호황", "연합뉴스", "positive", "https://example.com")
        assert w._list_widget.count() == 1

    def test_add_multiple_news(self, qapp):
        """여러 뉴스 추가."""
        w = NewsView()
        w.add_news("뉴스1", "소스1", "positive", "url1")
        w.add_news("뉴스2", "소스2", "negative", "url2")
        w.add_news("뉴스3", "소스3", "neutral", "url3")
        assert w._list_widget.count() == 3

    def test_positive_sentiment_color(self, qapp):
        """긍정 뉴스에 BULLISH 색상."""
        w = NewsView()
        w.add_news("호재", "뉴스", "positive", "url")
        item = w._list_widget.item(0)
        color = item.foreground().color().name()
        assert color.upper() == Colors.BULLISH.upper()

    def test_negative_sentiment_color(self, qapp):
        """부정 뉴스에 BEARISH 색상."""
        w = NewsView()
        w.add_news("악재", "뉴스", "negative", "url")
        item = w._list_widget.item(0)
        color = item.foreground().color().name()
        assert color.upper() == Colors.BEARISH.upper()

    def test_neutral_sentiment_color(self, qapp):
        """중립 뉴스에 TEXT_SECONDARY 색상."""
        w = NewsView()
        w.add_news("보통", "뉴스", "neutral", "url")
        item = w._list_widget.item(0)
        color = item.foreground().color().name()
        assert color.upper() == Colors.TEXT_SECONDARY.upper()


class TestSentimentTrendChart:
    """T071 SentimentTrendChart 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = SentimentTrendChart()
        assert w is not None

    def test_add_point(self, qapp):
        """데이터 포인트 추가."""
        w = SentimentTrendChart()
        ts = datetime.now()
        w.add_point(ts, 75.0)
        data = w.get_data()
        assert len(data) == 1
        assert data[0]["timestamp"] == ts
        assert data[0]["score"] == 75.0

    def test_add_multiple_points(self, qapp):
        """여러 데이터 포인트 추가."""
        w = SentimentTrendChart()
        for i in range(5):
            w.add_point(datetime.now(), float(i * 10))
        assert len(w.get_data()) == 5

    def test_get_data_empty(self, qapp):
        """빈 데이터."""
        w = SentimentTrendChart()
        assert w.get_data() == []


class TestNewsSummaryPanel:
    """T072 NewsSummaryPanel 위젯 테스트."""

    def test_creation(self, qapp):
        """인스턴스 생성."""
        w = NewsSummaryPanel()
        assert w is not None

    def test_set_summary(self, qapp):
        """AI 요약 텍스트 설정."""
        w = NewsSummaryPanel()
        w.set_summary("오늘 시장은 반도체 호황으로 상승 마감")
        assert "반도체" in w._summary_label.text()

    def test_set_summary_empty(self, qapp):
        """빈 요약."""
        w = NewsSummaryPanel()
        w.set_summary("")
        assert w._summary_label.text() == ""
