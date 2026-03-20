"""T055-T059: RiskManager 테스트 - 4단계 리스크 검증 + 킬 스위치"""
import pytest

from src.engine.risk_manager import RiskManager


@pytest.fixture
def rm() -> RiskManager:
    return RiskManager()


# ---------------------------------------------------------------------------
# T055: 리스크 1단계 - validate_order
# ---------------------------------------------------------------------------

class TestValidateOrder:
    def test_valid_order_passes(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        ok, msg = rm.validate_order(order)
        assert ok is True
        assert msg == ""

    def test_order_exceeds_max_amount(self, rm):
        """최대 주문 금액 초과"""
        order = {"symbol": "005930", "price": 70000, "quantity": 100000}
        ok, msg = rm.validate_order(order)
        assert ok is False
        assert "최대 주문 금액" in msg

    def test_zero_quantity_rejected(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 0}
        ok, msg = rm.validate_order(order)
        assert ok is False

    def test_negative_price_rejected(self, rm):
        order = {"symbol": "005930", "price": -1000, "quantity": 10}
        ok, msg = rm.validate_order(order)
        assert ok is False

    def test_tick_size_validation_passes(self, rm):
        """호가 단위 검증 - 올바른 호가"""
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        ok, _ = rm.validate_order(order)
        assert ok is True

    def test_tick_size_validation_fails(self, rm):
        """호가 단위 검증 - 잘못된 호가 (70000원대는 100원 단위)"""
        order = {"symbol": "005930", "price": 70050, "quantity": 10}
        ok, msg = rm.validate_order(order)
        assert ok is False
        assert "호가 단위" in msg

    def test_returns_tuple(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        result = rm.validate_order(order)
        assert isinstance(result, tuple)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# T056: 리스크 2단계 - validate_portfolio
# ---------------------------------------------------------------------------

class TestValidatePortfolio:
    def test_valid_portfolio_passes(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        portfolio = {
            "total_value": 100_000_000,
            "positions": {"005930": {"value": 10_000_000}},
            "sectors": {"IT": 0.3},
        }
        ok, msg = rm.validate_portfolio(order, portfolio)
        assert ok is True

    def test_concentration_exceeds_30pct(self, rm):
        """종목 집중도 30% 초과"""
        order = {"symbol": "005930", "price": 70000, "quantity": 500}
        portfolio = {
            "total_value": 100_000_000,
            "positions": {"005930": {"value": 29_000_000}},
            "sectors": {"IT": 0.3},
        }
        ok, msg = rm.validate_portfolio(order, portfolio)
        assert ok is False
        assert "종목 집중도" in msg

    def test_sector_exceeds_50pct(self, rm):
        """섹터 편중 50% 초과"""
        order = {"symbol": "005930", "price": 70000, "quantity": 100}
        portfolio = {
            "total_value": 100_000_000,
            "positions": {"005930": {"value": 5_000_000}},
            "sectors": {"IT": 0.45},
            "order_sector": "IT",
        }
        # 기존 IT 45% + 주문 7,000,000/100M = 7% → 52% > 50%
        ok, msg = rm.validate_portfolio(order, portfolio)
        assert ok is False
        assert "섹터" in msg

    def test_new_position_within_limit(self, rm):
        """신규 종목 매수 - 한도 내"""
        order = {"symbol": "035720", "price": 50000, "quantity": 10}
        portfolio = {
            "total_value": 100_000_000,
            "positions": {},
            "sectors": {"게임": 0.1},
        }
        ok, _ = rm.validate_portfolio(order, portfolio)
        assert ok is True

    def test_returns_tuple(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        portfolio = {
            "total_value": 100_000_000,
            "positions": {},
            "sectors": {},
        }
        result = rm.validate_portfolio(order, portfolio)
        assert isinstance(result, tuple)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# T057: 리스크 3단계 - validate_account
# ---------------------------------------------------------------------------

class TestValidateAccount:
    def test_valid_account_passes(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 50_000_000,
            "daily_pnl_pct": -1.0,
            "weekly_pnl_pct": -2.0,
            "monthly_pnl_pct": -5.0,
        }
        ok, msg = rm.validate_account(order, account)
        assert ok is True

    def test_daily_loss_exceeds_3pct(self, rm):
        """일일 손실 3% 초과"""
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 50_000_000,
            "daily_pnl_pct": -3.5,
            "weekly_pnl_pct": -2.0,
            "monthly_pnl_pct": -5.0,
        }
        ok, msg = rm.validate_account(order, account)
        assert ok is False
        assert "일일 손실" in msg

    def test_weekly_loss_exceeds_5pct(self, rm):
        """주간 손실 5% 초과"""
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 50_000_000,
            "daily_pnl_pct": -1.0,
            "weekly_pnl_pct": -5.5,
            "monthly_pnl_pct": -5.0,
        }
        ok, msg = rm.validate_account(order, account)
        assert ok is False
        assert "주간 손실" in msg

    def test_monthly_loss_exceeds_10pct(self, rm):
        """월간 손실 10% 초과"""
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 50_000_000,
            "daily_pnl_pct": -1.0,
            "weekly_pnl_pct": -2.0,
            "monthly_pnl_pct": -11.0,
        }
        ok, msg = rm.validate_account(order, account)
        assert ok is False
        assert "월간 손실" in msg

    def test_insufficient_cash(self, rm):
        """최소 예수금 20% 미달"""
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 15_000_000,  # 15% < 20%
            "daily_pnl_pct": -1.0,
            "weekly_pnl_pct": -2.0,
            "monthly_pnl_pct": -5.0,
        }
        ok, msg = rm.validate_account(order, account)
        assert ok is False
        assert "예수금" in msg

    def test_returns_tuple(self, rm):
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 50_000_000,
            "daily_pnl_pct": 0.0,
            "weekly_pnl_pct": 0.0,
            "monthly_pnl_pct": 0.0,
        }
        result = rm.validate_account(order, account)
        assert isinstance(result, tuple)


# ---------------------------------------------------------------------------
# T058: 리스크 4단계 - system_safeguard
# ---------------------------------------------------------------------------

class TestSystemSafeguard:
    def test_normal_market_passes(self, rm):
        market_info = {
            "mdd_pct": 10.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        ok, msg = rm.system_safeguard(market_info)
        assert ok is True

    def test_mdd_exceeds_15pct(self, rm):
        """MDD 15% 초과 → 킬 스위치"""
        market_info = {
            "mdd_pct": 16.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        ok, msg = rm.system_safeguard(market_info)
        assert ok is False
        assert "MDD" in msg

    def test_api_disconnected(self, rm):
        """API 연결 끊김"""
        market_info = {
            "mdd_pct": 10.0,
            "api_connected": False,
            "market_open": True,
            "minutes_to_close": 60,
        }
        ok, msg = rm.system_safeguard(market_info)
        assert ok is False
        assert "API" in msg

    def test_market_closed(self, rm):
        """장 마감"""
        market_info = {
            "mdd_pct": 10.0,
            "api_connected": True,
            "market_open": False,
            "minutes_to_close": 0,
        }
        ok, msg = rm.system_safeguard(market_info)
        assert ok is False
        assert "장" in msg or "마감" in msg

    def test_near_close_blocked(self, rm):
        """장 마감 전 차단 (마감 10분 전)"""
        market_info = {
            "mdd_pct": 10.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 5,
        }
        ok, msg = rm.system_safeguard(market_info)
        assert ok is False
        assert "마감" in msg

    def test_mdd_triggers_kill_switch(self, rm):
        """MDD 15% 초과 시 킬 스위치 자동 발동"""
        market_info = {
            "mdd_pct": 16.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        rm.system_safeguard(market_info)
        assert rm.is_killed() is True

    def test_returns_tuple(self, rm):
        market_info = {
            "mdd_pct": 10.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        result = rm.system_safeguard(market_info)
        assert isinstance(result, tuple)


# ---------------------------------------------------------------------------
# T059: 킬 스위치 테스트
# ---------------------------------------------------------------------------

class TestKillSwitch:
    def test_default_off(self, rm):
        assert rm.is_killed() is False

    def test_kill_switch_on(self, rm):
        rm.kill_switch_on()
        assert rm.is_killed() is True

    def test_kill_switch_off(self, rm):
        rm.kill_switch_on()
        rm.kill_switch_off()
        assert rm.is_killed() is False

    def test_kill_blocks_orders(self, rm):
        """킬 스위치 발동 시 validate_order 차단"""
        rm.kill_switch_on()
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        ok, msg = rm.validate_order(order)
        assert ok is False
        assert "킬 스위치" in msg

    def test_kill_blocks_portfolio(self, rm):
        """킬 스위치 발동 시 validate_portfolio 차단"""
        rm.kill_switch_on()
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        portfolio = {"total_value": 100_000_000, "positions": {}, "sectors": {}}
        ok, msg = rm.validate_portfolio(order, portfolio)
        assert ok is False
        assert "킬 스위치" in msg

    def test_kill_blocks_account(self, rm):
        """킬 스위치 발동 시 validate_account 차단"""
        rm.kill_switch_on()
        order = {"symbol": "005930", "price": 70000, "quantity": 10}
        account = {
            "total_equity": 100_000_000,
            "available_cash": 50_000_000,
            "daily_pnl_pct": 0.0,
            "weekly_pnl_pct": 0.0,
            "monthly_pnl_pct": 0.0,
        }
        ok, msg = rm.validate_account(order, account)
        assert ok is False
        assert "킬 스위치" in msg

    def test_auto_kill_on_mdd(self, rm):
        """MDD 15% 초과 시 자동 발동"""
        market_info = {
            "mdd_pct": 16.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        rm.system_safeguard(market_info)
        assert rm.is_killed() is True

    def test_manual_release_only(self, rm):
        """자동 발동 후 수동 해제만 허용"""
        market_info = {
            "mdd_pct": 16.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        rm.system_safeguard(market_info)
        assert rm.is_killed() is True
        # 정상 시장 조건이 되어도 자동 해제되지 않음
        normal_market = {
            "mdd_pct": 5.0,
            "api_connected": True,
            "market_open": True,
            "minutes_to_close": 60,
        }
        rm.system_safeguard(normal_market)
        assert rm.is_killed() is True  # 여전히 킬 상태
        # 수동 해제
        rm.kill_switch_off()
        assert rm.is_killed() is False


# ---------------------------------------------------------------------------
# P2-02: Kelly Criterion 포지션 사이징
# ---------------------------------------------------------------------------

class TestKellyPositionSize:
    def test_kelly_position_size_basic(self, rm):
        """승률 60%, 손익비 2:1 시 적절한 포지션"""
        result = rm.calculate_position_size(
            account_balance=10_000_000,
            win_rate=0.6,
            avg_win=0.1,
            avg_loss=0.05,
        )
        # Half-Kelly: b=2, p=0.6, q=0.4 → kelly=(2*0.6-0.4)/2=0.4 → half=0.2
        # fraction=0.2, 범위 내 → 10_000_000 * 0.2 = 2_000_000
        assert result == 2_000_000.0

    def test_kelly_position_size_low_confidence(self, rm):
        """신뢰도 낮으면 포지션 축소"""
        result_full = rm.calculate_position_size(
            account_balance=10_000_000,
            win_rate=0.6,
            avg_win=0.1,
            avg_loss=0.05,
            signal_confidence=1.0,
        )
        result_low = rm.calculate_position_size(
            account_balance=10_000_000,
            win_rate=0.6,
            avg_win=0.1,
            avg_loss=0.05,
            signal_confidence=0.3,
        )
        assert result_low < result_full

    def test_kelly_position_size_zero_loss(self, rm):
        """avg_loss=0일 때 최소 5%"""
        result = rm.calculate_position_size(
            account_balance=10_000_000,
            win_rate=0.6,
            avg_win=0.1,
            avg_loss=0.0,
        )
        assert result == 10_000_000 * 0.05

    def test_kelly_position_size_max_cap(self, rm):
        """max_position_pct 초과하지 않음"""
        result = rm.calculate_position_size(
            account_balance=10_000_000,
            win_rate=0.9,
            avg_win=0.5,
            avg_loss=0.01,
            signal_confidence=1.0,
            max_position_pct=0.3,
        )
        assert result <= 10_000_000 * 0.3


# ---------------------------------------------------------------------------
# P2-03: ATR 기반 동적 손절 + 트레일링 스탑
# ---------------------------------------------------------------------------

class TestDynamicStopLoss:
    def test_dynamic_stop_loss_long(self, rm):
        """매수 포지션 손절가 < 진입가"""
        stop = rm.calculate_dynamic_stop_loss(
            entry_price=50000,
            atr=500,
            multiplier=2.5,
            direction="long",
        )
        assert stop < 50000

    def test_dynamic_stop_loss_short(self, rm):
        """매도 포지션 손절가 > 진입가"""
        stop = rm.calculate_dynamic_stop_loss(
            entry_price=50000,
            atr=500,
            multiplier=2.5,
            direction="short",
        )
        assert stop > 50000

    def test_dynamic_stop_loss_zero_atr(self, rm):
        """ATR=0이면 고정 2% 손절"""
        stop = rm.calculate_dynamic_stop_loss(
            entry_price=50000,
            atr=0,
            direction="long",
        )
        assert stop == round(50000 * 0.98, 0)

    def test_trailing_stop_basic(self, rm):
        """최고가 - ATR * 배수"""
        stop = rm.calculate_trailing_stop(
            highest_price=60000,
            atr=500,
            multiplier=2.0,
        )
        assert stop == round(60000 - 500 * 2.0, 0)

    def test_trailing_stop_zero_atr(self, rm):
        """ATR=0이면 2% 기본값"""
        stop = rm.calculate_trailing_stop(
            highest_price=60000,
            atr=0,
        )
        assert stop == round(60000 * 0.98, 0)
