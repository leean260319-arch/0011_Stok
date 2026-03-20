"""성과 보고서 생성 모듈
버전: v1.0
설명: 매매 기록 기반 일간/주간/월간 성과 보고서 생성
"""

import os
import statistics
from datetime import datetime
from dataclasses import dataclass

from src.utils.constants import DATA_DIR
from src.utils.logger import get_logger

logger = get_logger("engine.report_generator")

REPORT_DIR = os.path.join(DATA_DIR, "reports")


@dataclass
class PerformanceReport:
    """성과 보고서 데이터."""
    period: str  # "daily" / "weekly" / "monthly"
    start_date: str
    end_date: str
    total_trades: int
    buy_trades: int
    sell_trades: int
    total_pnl: float
    win_rate: float
    avg_profit: float
    avg_loss: float
    max_drawdown: float
    sharpe_ratio: float
    best_trade: dict
    worst_trade: dict


class ReportGenerator:
    """매매 기록 기반 성과 보고서를 생성한다."""

    def __init__(self, report_dir: str = REPORT_DIR):
        self._report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def generate_summary(self, trades: list[dict]) -> PerformanceReport:
        """매매 기록 리스트에서 성과 요약을 생성한다.

        Args:
            trades: TradeLogger.get_trades()의 반환값

        Returns:
            PerformanceReport
        """
        if not trades:
            return PerformanceReport(
                period="custom", start_date="", end_date="",
                total_trades=0, buy_trades=0, sell_trades=0,
                total_pnl=0.0, win_rate=0.0, avg_profit=0.0, avg_loss=0.0,
                max_drawdown=0.0, sharpe_ratio=0.0,
                best_trade={}, worst_trade={},
            )

        buy_trades = [t for t in trades if t.get("direction") == "buy"]
        sell_trades = [t for t in trades if t.get("direction") == "sell"]

        # 손익 계산
        pnls = [t.get("pnl", 0) for t in trades]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]

        win_rate = len(wins) / len(pnls) if pnls else 0.0
        avg_profit = sum(wins) / len(wins) if wins else 0.0
        avg_loss = sum(losses) / len(losses) if losses else 0.0

        # MDD 계산
        cumulative = 0.0
        peak = 0.0
        max_dd = 0.0
        for p in pnls:
            cumulative += p
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_dd:
                max_dd = dd

        # Sharpe (단순 추정)
        mean_pnl = statistics.mean(pnls) if pnls else 0.0
        std_pnl = statistics.stdev(pnls) if len(pnls) > 1 else 1.0
        sharpe = (mean_pnl / std_pnl) if std_pnl > 0 else 0.0

        # 최고/최저 매매
        sorted_trades = sorted(trades, key=lambda t: t.get("pnl", 0))
        best = sorted_trades[-1] if sorted_trades else {}
        worst = sorted_trades[0] if sorted_trades else {}

        dates = [t.get("timestamp", "") for t in trades if t.get("timestamp")]

        return PerformanceReport(
            period="custom",
            start_date=min(dates) if dates else "",
            end_date=max(dates) if dates else "",
            total_trades=len(trades),
            buy_trades=len(buy_trades),
            sell_trades=len(sell_trades),
            total_pnl=round(sum(pnls), 4),
            win_rate=round(win_rate, 4),
            avg_profit=round(avg_profit, 4),
            avg_loss=round(avg_loss, 4),
            max_drawdown=round(max_dd, 4),
            sharpe_ratio=round(sharpe, 4),
            best_trade=best,
            worst_trade=worst,
        )

    def save_report_text(self, report: PerformanceReport, filename: str = "") -> str:
        """보고서를 텍스트 파일로 저장한다."""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join(self._report_dir, filename)

        lines = [
            "StokAI 성과 보고서",
            f"기간: {report.start_date} ~ {report.end_date}",
            f"유형: {report.period}",
            "",
            "[매매 현황]",
            f"  총 매매: {report.total_trades}건",
            f"  매수: {report.buy_trades}건 / 매도: {report.sell_trades}건",
            "",
            "[수익률]",
            f"  총 손익: {report.total_pnl:+.4f}",
            f"  승률: {report.win_rate:.1%}",
            f"  평균 수익: {report.avg_profit:+.4f}",
            f"  평균 손실: {report.avg_loss:+.4f}",
            "",
            "[리스크]",
            f"  최대 낙폭(MDD): {report.max_drawdown:.4f}",
            f"  Sharpe Ratio: {report.sharpe_ratio:.4f}",
        ]

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        logger.info("보고서 저장: %s", path)
        return path
