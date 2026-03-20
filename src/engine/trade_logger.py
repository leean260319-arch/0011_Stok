"""매매 근거 자동 기록 모듈
버전: v1.0
설명: 매매 시점의 시그널, 지표값, 감성 점수 등을 SQLite에 자동 저장
"""

import os
import sqlite3
import threading
from dataclasses import dataclass

from src.utils.constants import DATA_DIR
from src.utils.logger import get_logger

logger = get_logger("engine.trade_logger")

TRADE_LOG_DB = os.path.join(DATA_DIR, "trade_logs.db")


@dataclass
class TradeRecord:
    """매매 기록 데이터클래스."""
    timestamp: str
    stock_code: str
    stock_name: str
    direction: str  # "buy" / "sell"
    price: float
    quantity: int
    signal_score: float
    signal_detail: str  # JSON 문자열: 지표값, 감성 점수 등
    strategy_name: str
    confidence: float
    reason: str
    pnl: float = 0.0


class TradeLogger:
    """매매 근거를 SQLite에 자동 기록한다."""

    def __init__(self, db_path: str = TRADE_LOG_DB):
        self._db_path = db_path
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS trade_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                stock_code TEXT NOT NULL,
                stock_name TEXT DEFAULT '',
                direction TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                signal_score REAL DEFAULT 0,
                signal_detail TEXT DEFAULT '{}',
                strategy_name TEXT DEFAULT '',
                confidence REAL DEFAULT 0,
                reason TEXT DEFAULT '',
                pnl REAL DEFAULT 0
            )
        """)
        # 기존 테이블에 pnl 컬럼이 없으면 추가
        existing_cols = [
            row[1] for row in self._conn.execute("PRAGMA table_info(trade_logs)").fetchall()
        ]
        if "pnl" not in existing_cols:
            self._conn.execute("ALTER TABLE trade_logs ADD COLUMN pnl REAL DEFAULT 0")
        self._conn.commit()
        logger.info("TradeLogger 초기화: %s", db_path)

    def log_trade(self, record: TradeRecord) -> int:
        """매매 기록을 저장하고 ID를 반환한다."""
        pnl = record.pnl
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO trade_logs "
                "(timestamp, stock_code, stock_name, direction, price, quantity, "
                "signal_score, signal_detail, strategy_name, confidence, reason, pnl) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    record.timestamp, record.stock_code, record.stock_name,
                    record.direction, record.price, record.quantity,
                    record.signal_score, record.signal_detail,
                    record.strategy_name, record.confidence, record.reason,
                    pnl,
                ),
            )
            self._conn.commit()
        logger.info(
            "매매 기록: %s %s %s %d주 @ %.0f",
            record.timestamp, record.direction, record.stock_code,
            record.quantity, record.price,
        )
        return cur.lastrowid

    def get_trades(self, limit: int = 100, stock_code: str = "") -> list[dict]:
        """매매 기록을 조회한다."""
        with self._lock:
            if stock_code:
                rows = self._conn.execute(
                    "SELECT * FROM trade_logs WHERE stock_code = ? ORDER BY id DESC LIMIT ?",
                    (stock_code, limit),
                ).fetchall()
            else:
                rows = self._conn.execute(
                    "SELECT * FROM trade_logs ORDER BY id DESC LIMIT ?", (limit,),
                ).fetchall()
            cols = [d[0] for d in self._conn.execute("SELECT * FROM trade_logs LIMIT 0").description]
        return [dict(zip(cols, row)) for row in rows]

    def get_trade_stats(self) -> dict:
        """매매 통계를 반환한다.

        매매 쌍(buy->sell) 기반으로 수익률을 계산하여
        win_rate, avg_win, avg_loss를 포함한다.
        """
        with self._lock:
            total = self._conn.execute("SELECT COUNT(*) FROM trade_logs").fetchone()[0]
            buys = self._conn.execute(
                "SELECT COUNT(*) FROM trade_logs WHERE direction = 'buy'"
            ).fetchone()[0]
            sells = self._conn.execute(
                "SELECT COUNT(*) FROM trade_logs WHERE direction = 'sell'"
            ).fetchone()[0]

            # 매매 쌍 기반 수익률 계산
            buy_rows = self._conn.execute(
                "SELECT stock_code, price, timestamp FROM trade_logs "
                "WHERE direction = 'buy' ORDER BY id ASC"
            ).fetchall()
            sell_rows = self._conn.execute(
                "SELECT stock_code, price, timestamp FROM trade_logs "
                "WHERE direction = 'sell' ORDER BY id ASC"
            ).fetchall()

        # 종목별 buy 큐를 만들어 sell과 FIFO 매칭
        buy_queue: dict[str, list[float]] = {}
        for code, price, _ in buy_rows:
            buy_queue.setdefault(code, []).append(price)

        returns = []
        for code, sell_price, _ in sell_rows:
            if code in buy_queue and buy_queue[code]:
                buy_price = buy_queue[code].pop(0)
                if buy_price > 0:
                    ret = (sell_price - buy_price) / buy_price
                    returns.append(ret)

        if not returns:
            return {
                "total": total, "buys": buys, "sells": sells,
                "win_rate": 0.5, "avg_win": 0.03, "avg_loss": 0.02,
            }

        wins = [r for r in returns if r > 0]
        losses = [r for r in returns if r <= 0]
        win_rate = len(wins) / len(returns)
        avg_win = (sum(wins) / len(wins)) if wins else 0.0
        avg_loss = (abs(sum(losses) / len(losses))) if losses else 0.0

        return {
            "total": total, "buys": buys, "sells": sells,
            "win_rate": win_rate, "avg_win": avg_win, "avg_loss": avg_loss,
        }

    def close(self):
        self._conn.close()
