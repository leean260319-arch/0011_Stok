"""RAG(Retrieval-Augmented Generation) 엔진
Version: 1.0.0

d0012 P3-01: 뉴스 + 재무 데이터를 검색하여 LLM 분석에 맥락으로 제공.
SQLite 기반 TF-IDF 키워드 매칭으로 관련 문서 검색.
"""

import json
import os
import sqlite3
import time
import uuid
from dataclasses import dataclass

from src.utils.logger import get_logger

logger = get_logger("ai.rag_engine")

SOURCE_LABEL = {
    "news": "뉴스",
    "financial": "재무",
    "report": "리포트",
}


@dataclass
class RAGDocument:
    """RAG 검색 결과 문서."""

    doc_id: str
    content: str
    source: str          # "news", "financial", "report"
    metadata: dict       # title, date, stock_code 등
    score: float = 0.0   # 검색 관련도 점수


class RAGEngine:
    """TF-IDF 기반 RAG 엔진. SQLite + 순수 Python 매칭."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    # ------------------------------------------------------------------
    # DB 초기화
    # ------------------------------------------------------------------

    def _init_db(self):
        """RAG 문서 저장 테이블 생성."""
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS rag_documents ("
            "  doc_id TEXT PRIMARY KEY,"
            "  content TEXT NOT NULL,"
            "  source TEXT NOT NULL,"
            "  metadata TEXT NOT NULL DEFAULT '{}',"
            "  keywords TEXT NOT NULL DEFAULT '',"
            "  created_at REAL NOT NULL"
            ")"
        )
        self._conn.commit()
        logger.debug("RAG DB 초기화 완료: %s", self._db_path)

    # ------------------------------------------------------------------
    # 토큰화
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> list[str]:
        """한국어 공백 기반 토큰화. 1글자 토큰 제거."""
        if not text:
            return []
        tokens = text.split()
        return [t for t in tokens if len(t) > 1]

    # ------------------------------------------------------------------
    # 스코어 계산
    # ------------------------------------------------------------------

    def _calculate_score(self, query_tokens: list[str], doc_keywords: str) -> float:
        """쿼리 토큰과 문서 키워드 간 매칭 스코어 계산."""
        if not query_tokens:
            return 0.0
        doc_tokens = doc_keywords.split()
        if not doc_tokens:
            return 0.0
        matches = sum(1 for qt in query_tokens if qt in doc_tokens)
        return matches / len(query_tokens)

    # ------------------------------------------------------------------
    # 문서 추가
    # ------------------------------------------------------------------

    def add_document(self, content: str, source: str, metadata: dict) -> str:
        """문서를 RAG DB에 추가. doc_id 반환."""
        doc_id = str(uuid.uuid4())
        keywords = " ".join(self._tokenize(content))
        metadata_json = json.dumps(metadata, ensure_ascii=False)
        self._conn.execute(
            "INSERT INTO rag_documents (doc_id, content, source, metadata, keywords, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (doc_id, content, source, metadata_json, keywords, time.time()),
        )
        self._conn.commit()
        logger.debug("RAG 문서 추가: doc_id=%s, source=%s", doc_id, source)
        return doc_id

    def add_documents(self, documents: list[dict]) -> list[str]:
        """여러 문서를 한번에 추가."""
        ids = []
        for doc in documents:
            doc_id = self.add_document(
                content=doc["content"],
                source=doc["source"],
                metadata=doc.get("metadata", {}),
            )
            ids.append(doc_id)
        return ids

    # ------------------------------------------------------------------
    # 검색
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 5, source_filter: str = None) -> list[RAGDocument]:
        """쿼리와 관련된 문서를 검색.

        TF-IDF 기반 키워드 매칭으로 관련 문서 검색.
        source_filter로 특정 소스만 필터링 가능.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        sql = "SELECT doc_id, content, source, metadata, keywords FROM rag_documents"
        params: tuple = ()
        if source_filter:
            sql += " WHERE source = ?"
            params = (source_filter,)

        rows = self._conn.execute(sql, params).fetchall()

        scored: list[tuple[float, dict]] = []
        for row in rows:
            doc_id, content, source, metadata_json, keywords = row
            score = self._calculate_score(query_tokens, keywords)
            if score > 0.0:
                scored.append((score, {
                    "doc_id": doc_id,
                    "content": content,
                    "source": source,
                    "metadata": json.loads(metadata_json),
                    "score": score,
                }))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, doc_data in scored[:top_k]:
            results.append(RAGDocument(**doc_data))

        return results

    # ------------------------------------------------------------------
    # 컨텍스트 조합
    # ------------------------------------------------------------------

    def build_context(self, query: str, top_k: int = 3) -> str:
        """검색 결과를 LLM에 전달할 컨텍스트 문자열로 조합."""
        docs = self.search(query, top_k=top_k)
        if not docs:
            return ""

        parts = []
        for i, doc in enumerate(docs, 1):
            source_label = SOURCE_LABEL.get(doc.source, doc.source)
            date_str = doc.metadata.get("date", "")
            if date_str:
                header = f"[관련 문서 {i}] ({source_label}, {date_str})"
            else:
                header = f"[관련 문서 {i}] ({source_label})"
            parts.append(f"{header}\n{doc.content}")

        return "\n\n".join(parts)

    # ------------------------------------------------------------------
    # 통계
    # ------------------------------------------------------------------

    def get_stats(self) -> dict:
        """RAG DB 통계 반환. {total_docs, by_source, last_updated}"""
        total = self._conn.execute(
            "SELECT COUNT(*) FROM rag_documents"
        ).fetchone()[0]

        by_source_rows = self._conn.execute(
            "SELECT source, COUNT(*) FROM rag_documents GROUP BY source"
        ).fetchall()
        by_source = {row[0]: row[1] for row in by_source_rows}

        last_updated_row = self._conn.execute(
            "SELECT MAX(created_at) FROM rag_documents"
        ).fetchone()
        last_updated = last_updated_row[0] if last_updated_row[0] else None

        return {
            "total_docs": total,
            "by_source": by_source,
            "last_updated": last_updated,
        }

    # ------------------------------------------------------------------
    # 정리
    # ------------------------------------------------------------------

    def clear_old(self, days: int = 30):
        """오래된 문서 삭제."""
        cutoff = time.time() - (days * 86400)
        self._conn.execute(
            "DELETE FROM rag_documents WHERE created_at < ?",
            (cutoff,),
        )
        self._conn.commit()
        logger.info("RAG 오래된 문서 삭제 완료: %d일 이전", days)

    def close(self):
        """DB 연결 종료."""
        self._conn.close()
        logger.debug("RAG DB 연결 종료")
