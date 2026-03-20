"""RAG Engine 테스트 (TDD)
d0012 P3-01: RAG(Retrieval-Augmented Generation) 엔진
"""

import os
import sqlite3
import time

import pytest

from src.ai.rag_engine import RAGDocument, RAGEngine


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def rag(tmp_path):
    """임시 DB로 RAGEngine 생성 후 반환, 종료 시 close"""
    db_path = os.path.join(str(tmp_path), "test_rag.db")
    engine = RAGEngine(db_path=db_path)
    yield engine
    engine.close()


# ------------------------------------------------------------------
# RAGDocument dataclass
# ------------------------------------------------------------------

class TestRAGDocument:
    def test_create_rag_document(self):
        """RAGDocument 생성 및 필드 확인"""
        doc = RAGDocument(
            doc_id="abc123",
            content="삼성전자 실적 발표",
            source="news",
            metadata={"title": "삼성전자"},
            score=0.85,
        )
        assert doc.doc_id == "abc123"
        assert doc.content == "삼성전자 실적 발표"
        assert doc.source == "news"
        assert doc.metadata == {"title": "삼성전자"}
        assert doc.score == 0.85

    def test_default_score_is_zero(self):
        """score 기본값이 0.0인지 확인"""
        doc = RAGDocument(
            doc_id="id1", content="내용", source="news", metadata={}
        )
        assert doc.score == 0.0


# ------------------------------------------------------------------
# RAGEngine 초기화
# ------------------------------------------------------------------

class TestRAGEngineInit:
    def test_creates_db_file(self, tmp_path):
        """RAGEngine 생성 시 DB 파일이 생성되는지 확인"""
        db_path = os.path.join(str(tmp_path), "rag_init.db")
        engine = RAGEngine(db_path=db_path)
        assert os.path.exists(db_path)
        engine.close()

    def test_creates_rag_documents_table(self, tmp_path):
        """rag_documents 테이블이 생성되는지 확인"""
        db_path = os.path.join(str(tmp_path), "rag_table.db")
        engine = RAGEngine(db_path=db_path)
        conn = sqlite3.connect(db_path)
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='rag_documents'"
        )
        assert cur.fetchone() is not None
        conn.close()
        engine.close()

    def test_close_does_not_raise(self, tmp_path):
        """close 호출이 에러 없이 완료되는지 확인"""
        db_path = os.path.join(str(tmp_path), "rag_close.db")
        engine = RAGEngine(db_path=db_path)
        engine.close()


# ------------------------------------------------------------------
# add_document
# ------------------------------------------------------------------

class TestAddDocument:
    def test_add_document_returns_doc_id(self, rag):
        """add_document가 doc_id(str)를 반환하는지 확인"""
        doc_id = rag.add_document(
            content="삼성전자 3분기 실적 호조",
            source="news",
            metadata={"title": "삼성전자 실적"},
        )
        assert isinstance(doc_id, str)
        assert len(doc_id) > 0

    def test_add_document_unique_ids(self, rag):
        """두 번 추가 시 서로 다른 doc_id가 반환되는지 확인"""
        id1 = rag.add_document(content="내용1", source="news", metadata={})
        id2 = rag.add_document(content="내용2", source="news", metadata={})
        assert id1 != id2

    def test_add_document_stored_in_db(self, rag):
        """추가된 문서가 DB에 저장되는지 확인"""
        doc_id = rag.add_document(
            content="테스트 내용", source="financial", metadata={"key": "value"}
        )
        stats = rag.get_stats()
        assert stats["total_docs"] >= 1


# ------------------------------------------------------------------
# add_documents (batch)
# ------------------------------------------------------------------

class TestAddDocuments:
    def test_add_documents_returns_list_of_ids(self, rag):
        """add_documents가 doc_id 리스트를 반환하는지 확인"""
        docs = [
            {"content": "뉴스1", "source": "news", "metadata": {}},
            {"content": "뉴스2", "source": "news", "metadata": {}},
            {"content": "재무1", "source": "financial", "metadata": {}},
        ]
        ids = rag.add_documents(docs)
        assert isinstance(ids, list)
        assert len(ids) == 3
        assert len(set(ids)) == 3  # 모두 고유

    def test_add_documents_empty_list(self, rag):
        """빈 리스트 입력 시 빈 리스트 반환"""
        ids = rag.add_documents([])
        assert ids == []


# ------------------------------------------------------------------
# search
# ------------------------------------------------------------------

class TestSearch:
    def test_search_returns_list_of_rag_documents(self, rag):
        """search가 RAGDocument 리스트를 반환하는지 확인"""
        rag.add_document(content="삼성전자 반도체 실적", source="news", metadata={})
        results = rag.search("삼성전자")
        assert isinstance(results, list)
        for doc in results:
            assert isinstance(doc, RAGDocument)

    def test_search_finds_relevant_document(self, rag):
        """관련 키워드로 검색 시 해당 문서가 반환되는지 확인"""
        rag.add_document(
            content="삼성전자 3분기 반도체 실적 호조",
            source="news",
            metadata={"title": "삼성전자 실적"},
        )
        rag.add_document(
            content="현대차 전기차 판매량 증가",
            source="news",
            metadata={"title": "현대차 판매"},
        )
        results = rag.search("삼성전자 반도체")
        assert len(results) > 0
        assert any("삼성전자" in doc.content for doc in results)

    def test_search_top_k_limits_results(self, rag):
        """top_k로 반환 개수가 제한되는지 확인"""
        for i in range(10):
            rag.add_document(content=f"문서 {i} 테스트 키워드", source="news", metadata={})
        results = rag.search("테스트 키워드", top_k=3)
        assert len(results) <= 3

    def test_search_source_filter(self, rag):
        """source_filter로 특정 소스만 검색되는지 확인"""
        rag.add_document(content="삼성전자 뉴스 내용", source="news", metadata={})
        rag.add_document(content="삼성전자 재무 데이터", source="financial", metadata={})
        results = rag.search("삼성전자", source_filter="financial")
        assert all(doc.source == "financial" for doc in results)

    def test_search_empty_query_returns_empty(self, rag):
        """빈 쿼리 시 빈 리스트 반환"""
        rag.add_document(content="내용", source="news", metadata={})
        results = rag.search("")
        assert results == []

    def test_search_no_match_returns_empty(self, rag):
        """매칭 없을 때 빈 리스트 반환"""
        rag.add_document(content="삼성전자 실적", source="news", metadata={})
        results = rag.search("아무관련없는단어XYZQWERTY")
        assert results == []

    def test_search_results_sorted_by_score_desc(self, rag):
        """검색 결과가 score 내림차순으로 정렬되는지 확인"""
        rag.add_document(content="삼성전자", source="news", metadata={})
        rag.add_document(content="삼성전자 반도체 삼성전자", source="news", metadata={})
        rag.add_document(content="삼성전자 반도체 실적 삼성전자 호조", source="news", metadata={})
        results = rag.search("삼성전자 반도체 실적 호조")
        if len(results) >= 2:
            for i in range(len(results) - 1):
                assert results[i].score >= results[i + 1].score


# ------------------------------------------------------------------
# _calculate_score (내부 메서드 직접 테스트)
# ------------------------------------------------------------------

class TestCalculateScore:
    def test_full_match_score(self, rag):
        """모든 쿼리 토큰이 매칭되면 1.0 반환"""
        score = rag._calculate_score(["삼성전자", "실적"], "삼성전자 실적 호조")
        assert score == 1.0

    def test_partial_match_score(self, rag):
        """일부만 매칭되면 0과 1 사이 값 반환"""
        score = rag._calculate_score(["삼성전자", "LG전자"], "삼성전자 실적 호조")
        assert 0.0 < score < 1.0

    def test_no_match_score(self, rag):
        """매칭 없으면 0.0 반환"""
        score = rag._calculate_score(["없는단어"], "삼성전자 실적 호조")
        assert score == 0.0

    def test_empty_query_tokens(self, rag):
        """빈 쿼리 토큰이면 0.0 반환"""
        score = rag._calculate_score([], "삼성전자 실적")
        assert score == 0.0

    def test_empty_doc_keywords(self, rag):
        """빈 문서 키워드면 0.0 반환"""
        score = rag._calculate_score(["삼성전자"], "")
        assert score == 0.0


# ------------------------------------------------------------------
# build_context
# ------------------------------------------------------------------

class TestBuildContext:
    def test_build_context_returns_string(self, rag):
        """build_context가 문자열을 반환하는지 확인"""
        rag.add_document(
            content="삼성전자 실적 발표", source="news",
            metadata={"title": "삼성 실적", "date": "2026-03-17"},
        )
        ctx = rag.build_context("삼성전자")
        assert isinstance(ctx, str)

    def test_build_context_contains_document_content(self, rag):
        """build_context 결과에 문서 내용이 포함되는지 확인"""
        rag.add_document(
            content="삼성전자 3분기 영업이익 증가",
            source="news",
            metadata={"title": "삼성 실적", "date": "2026-03-17"},
        )
        ctx = rag.build_context("삼성전자 영업이익")
        assert "삼성전자 3분기 영업이익 증가" in ctx

    def test_build_context_format(self, rag):
        """build_context 출력에 [관련 문서 N] 형식이 포함되는지 확인"""
        rag.add_document(
            content="테스트 문서 내용",
            source="news",
            metadata={"date": "2026-03-17"},
        )
        ctx = rag.build_context("테스트 문서")
        assert "[관련 문서 1]" in ctx

    def test_build_context_includes_source_info(self, rag):
        """build_context에 소스 정보가 포함되는지 확인"""
        rag.add_document(
            content="재무 데이터 PER 12.5",
            source="financial",
            metadata={"date": "2026-03-16"},
        )
        ctx = rag.build_context("PER")
        assert "financial" in ctx or "재무" in ctx

    def test_build_context_empty_when_no_match(self, rag):
        """매칭 문서 없으면 빈 문자열 반환"""
        ctx = rag.build_context("없는내용XYZQWERTY")
        assert ctx == ""

    def test_build_context_top_k_limits(self, rag):
        """top_k에 따라 포함 문서 수가 제한되는지 확인"""
        for i in range(10):
            rag.add_document(
                content=f"공통키워드 문서{i}",
                source="news",
                metadata={"date": "2026-03-17"},
            )
        ctx = rag.build_context("공통키워드", top_k=2)
        assert ctx.count("[관련 문서") <= 2


# ------------------------------------------------------------------
# get_stats
# ------------------------------------------------------------------

class TestGetStats:
    def test_get_stats_empty_db(self, rag):
        """빈 DB에서 통계가 올바른지 확인"""
        stats = rag.get_stats()
        assert stats["total_docs"] == 0
        assert isinstance(stats["by_source"], dict)

    def test_get_stats_after_add(self, rag):
        """문서 추가 후 통계가 올바른지 확인"""
        rag.add_document(content="뉴스1", source="news", metadata={})
        rag.add_document(content="뉴스2", source="news", metadata={})
        rag.add_document(content="재무1", source="financial", metadata={})
        stats = rag.get_stats()
        assert stats["total_docs"] == 3
        assert stats["by_source"]["news"] == 2
        assert stats["by_source"]["financial"] == 1

    def test_get_stats_has_last_updated(self, rag):
        """통계에 last_updated 필드가 있는지 확인"""
        rag.add_document(content="내용", source="news", metadata={})
        stats = rag.get_stats()
        assert "last_updated" in stats


# ------------------------------------------------------------------
# clear_old
# ------------------------------------------------------------------

class TestClearOld:
    def test_clear_old_removes_old_documents(self, rag):
        """오래된 문서가 삭제되는지 확인"""
        # 직접 DB에 오래된 문서 삽입
        old_time = time.time() - (31 * 86400)  # 31일 전
        rag._conn.execute(
            "INSERT INTO rag_documents (doc_id, content, source, metadata, keywords, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("old_doc", "오래된 뉴스", "news", "{}", "오래된 뉴스", old_time),
        )
        rag._conn.commit()

        rag.add_document(content="최신 뉴스", source="news", metadata={})
        assert rag.get_stats()["total_docs"] == 2

        rag.clear_old(days=30)
        assert rag.get_stats()["total_docs"] == 1

    def test_clear_old_keeps_recent_documents(self, rag):
        """최근 문서는 삭제되지 않는지 확인"""
        rag.add_document(content="최신 뉴스1", source="news", metadata={})
        rag.add_document(content="최신 뉴스2", source="news", metadata={})
        rag.clear_old(days=30)
        assert rag.get_stats()["total_docs"] == 2


# ------------------------------------------------------------------
# 한국어 토큰화
# ------------------------------------------------------------------

class TestTokenization:
    def test_tokenize_korean(self, rag):
        """한국어 공백 기반 토큰화가 동작하는지 확인"""
        tokens = rag._tokenize("삼성전자 3분기 실적 발표")
        assert "삼성전자" in tokens
        assert "3분기" in tokens
        assert "실적" in tokens
        assert "발표" in tokens

    def test_tokenize_removes_short_tokens(self, rag):
        """1글자 토큰이 제거되는지 확인"""
        tokens = rag._tokenize("나 는 삼성전자 를 좋아한다")
        assert "나" not in tokens
        assert "는" not in tokens
        assert "삼성전자" in tokens

    def test_tokenize_empty_string(self, rag):
        """빈 문자열 토큰화 시 빈 리스트 반환"""
        tokens = rag._tokenize("")
        assert tokens == []
