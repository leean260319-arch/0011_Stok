"""TradeLogger 단위 테스트"""

import os
import tempfile
import pytest

from src.engine.trade_logger import TradeLogger, TradeRecord


@pytest.fixture
def tmp_db(tmp_path):
    db_path = str(tmp_path / "test_trade_logs.db")
    logger = TradeLogger(db_path=db_path)
    yield logger
    logger.close()


def _make_record(**kwargs) -> TradeRecord:
    defaults = dict(
        timestamp="2026-03-17 10:00:00",
        stock_code="005930",
        stock_name="삼성전자",
        direction="buy",
        price=70000.0,
        quantity=10,
        signal_score=0.75,
        signal_detail='{"rsi": 28, "macd": 0.5}',
        strategy_name="momentum",
        confidence=0.8,
        reason="RSI 과매도 + MACD 골든크로스",
    )
    defaults.update(kwargs)
    return TradeRecord(**defaults)


def test_trade_logger_init(tmp_path):
    """DB 파일이 생성되고 테이블이 존재해야 한다."""
    db_path = str(tmp_path / "init_test.db")
    logger = TradeLogger(db_path=db_path)
    assert os.path.exists(db_path)
    # trade_logs 테이블 존재 확인
    tables = logger._conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='trade_logs'"
    ).fetchall()
    assert len(tables) == 1
    logger.close()


def test_log_trade(tmp_db):
    """매매 기록 저장 후 양수 ID를 반환해야 한다."""
    record = _make_record()
    row_id = tmp_db.log_trade(record)
    assert isinstance(row_id, int)
    assert row_id > 0


def test_get_trades(tmp_db):
    """저장한 매매 기록이 조회되어야 한다."""
    tmp_db.log_trade(_make_record(direction="buy"))
    tmp_db.log_trade(_make_record(direction="sell", price=72000.0))

    trades = tmp_db.get_trades()
    assert len(trades) == 2
    # 최신순 정렬 확인
    assert trades[0]["direction"] == "sell"
    assert trades[1]["direction"] == "buy"


def test_get_trades_by_stock(tmp_db):
    """종목 코드로 필터링 조회가 동작해야 한다."""
    tmp_db.log_trade(_make_record(stock_code="005930"))
    tmp_db.log_trade(_make_record(stock_code="000660"))
    tmp_db.log_trade(_make_record(stock_code="005930"))

    trades_005930 = tmp_db.get_trades(stock_code="005930")
    assert len(trades_005930) == 2
    for t in trades_005930:
        assert t["stock_code"] == "005930"

    trades_000660 = tmp_db.get_trades(stock_code="000660")
    assert len(trades_000660) == 1


def test_get_trade_stats(tmp_db):
    """매매 통계가 올바르게 집계되어야 한다."""
    tmp_db.log_trade(_make_record(direction="buy"))
    tmp_db.log_trade(_make_record(direction="buy"))
    tmp_db.log_trade(_make_record(direction="sell"))

    stats = tmp_db.get_trade_stats()
    assert stats["total"] == 3
    assert stats["buys"] == 2
    assert stats["sells"] == 1


def test_trade_record_dataclass():
    """TradeRecord dataclass가 정상 생성되어야 한다."""
    record = _make_record()
    assert record.stock_code == "005930"
    assert record.direction == "buy"
    assert record.price == 70000.0
    assert record.quantity == 10
    assert record.signal_score == 0.75
