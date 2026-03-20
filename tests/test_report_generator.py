"""ReportGenerator 단위 테스트"""

import os
import pytest

from src.engine.report_generator import ReportGenerator, PerformanceReport


@pytest.fixture
def gen(tmp_path):
    return ReportGenerator(report_dir=str(tmp_path / "reports"))


def _make_trades() -> list[dict]:
    return [
        {"timestamp": "2026-03-10 09:00:00", "direction": "buy",  "pnl":  0.8},
        {"timestamp": "2026-03-11 09:00:00", "direction": "sell", "pnl":  0.5},
        {"timestamp": "2026-03-12 09:00:00", "direction": "buy",  "pnl": -0.3},
        {"timestamp": "2026-03-13 09:00:00", "direction": "sell", "pnl":  0.2},
        {"timestamp": "2026-03-14 09:00:00", "direction": "buy",  "pnl": -0.1},
    ]


def test_generate_summary_empty(gen):
    """빈 매매 목록에서 기본 PerformanceReport를 반환해야 한다."""
    report = gen.generate_summary([])
    assert isinstance(report, PerformanceReport)
    assert report.total_trades == 0
    assert report.win_rate == 0.0
    assert report.total_pnl == 0.0
    assert report.best_trade == {}
    assert report.worst_trade == {}


def test_generate_summary_with_trades(gen):
    """매매 기록으로 요약이 올바르게 생성되어야 한다."""
    trades = _make_trades()
    report = gen.generate_summary(trades)

    assert report.total_trades == 5
    assert report.buy_trades == 3
    assert report.sell_trades == 2
    assert report.start_date == "2026-03-10 09:00:00"
    assert report.end_date == "2026-03-14 09:00:00"
    assert report.period == "custom"


def test_win_rate_calculation(gen):
    """승률이 올바르게 계산되어야 한다 (양수 pnl = 승)."""
    trades = _make_trades()
    # wins: 0.8, 0.5, 0.2 = 3개 / total 5 = 0.6
    report = gen.generate_summary(trades)
    assert abs(report.win_rate - 0.6) < 1e-4


def test_max_drawdown_calculation(gen):
    """MDD가 0 이상이어야 한다."""
    trades = _make_trades()
    report = gen.generate_summary(trades)
    assert report.max_drawdown >= 0.0


def test_save_report_text(gen, tmp_path):
    """텍스트 보고서 파일이 저장되어야 한다."""
    trades = _make_trades()
    report = gen.generate_summary(trades)
    path = gen.save_report_text(report, filename="test_report.txt")

    assert os.path.exists(path)
    content = open(path, encoding="utf-8").read()
    assert "StokAI 성과 보고서" in content
    assert "총 매매" in content
    assert "승률" in content
    assert "MDD" in content


def test_performance_report_dataclass():
    """PerformanceReport dataclass가 정상 생성되어야 한다."""
    report = PerformanceReport(
        period="daily",
        start_date="2026-03-17",
        end_date="2026-03-17",
        total_trades=10,
        buy_trades=6,
        sell_trades=4,
        total_pnl=1.5,
        win_rate=0.6,
        avg_profit=0.5,
        avg_loss=-0.2,
        max_drawdown=0.3,
        sharpe_ratio=1.2,
        best_trade={"pnl": 0.8},
        worst_trade={"pnl": -0.3},
    )
    assert report.period == "daily"
    assert report.total_trades == 10
    assert report.win_rate == 0.6
    assert report.sharpe_ratio == 1.2
