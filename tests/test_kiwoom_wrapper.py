"""KiwoomWrapper 테스트 - Mock bridge 주입, 스로틀링, 재연결"""
from unittest.mock import MagicMock, call, patch

import pytest

from src.bridge.kiwoom_bridge import Balance, HoldingItem, KiwoomBridge, OrderResult, StockPrice
from src.bridge.kiwoom_wrapper import APIThrottler, KiwoomWrapper, get_tick_size, validate_price


# ------------------------------------------------------------------ #
# 픽스처
# ------------------------------------------------------------------ #

@pytest.fixture
def mock_bridge():
    bridge = MagicMock(spec=KiwoomBridge)
    bridge.is_connected = True
    return bridge


@pytest.fixture
def wrapper(mock_bridge):
    return KiwoomWrapper(mock_bridge)


# ------------------------------------------------------------------ #
# get_tick_size / validate_price
# ------------------------------------------------------------------ #

class TestGetTickSize:
    def test_price_below_2000_tick_1(self):
        assert get_tick_size(1000) == 1
        assert get_tick_size(1999) == 1

    def test_price_2000_to_4999_tick_5(self):
        assert get_tick_size(2000) == 5
        assert get_tick_size(4999) == 5

    def test_price_5000_to_19999_tick_10(self):
        assert get_tick_size(5000) == 10
        assert get_tick_size(19999) == 10

    def test_price_20000_to_49999_tick_50(self):
        assert get_tick_size(20000) == 50
        assert get_tick_size(49999) == 50

    def test_price_50000_to_199999_tick_100(self):
        assert get_tick_size(50000) == 100
        assert get_tick_size(199999) == 100

    def test_price_200000_to_499999_tick_500(self):
        assert get_tick_size(200000) == 500
        assert get_tick_size(499999) == 500

    def test_price_500000_above_tick_1000(self):
        assert get_tick_size(500000) == 1000
        assert get_tick_size(1000000) == 1000


class TestValidatePrice:
    def test_zero_price_is_valid_market_order(self):
        assert validate_price(0) is True

    def test_negative_price_is_valid_market_order(self):
        assert validate_price(-1) is True

    def test_valid_price_multiple_of_tick(self):
        assert validate_price(70000) is True   # 100 단위
        assert validate_price(5000) is True    # 10 단위

    def test_invalid_price_not_multiple_of_tick(self):
        assert validate_price(70050) is False  # 100 단위 어긋남
        assert validate_price(5001) is False   # 10 단위 어긋남


# ------------------------------------------------------------------ #
# APIThrottler
# ------------------------------------------------------------------ #

class TestAPIThrottler:
    def test_acquire_within_rate_does_not_sleep(self):
        throttler = APIThrottler(rate_per_sec=5, rate_per_hour=1000)
        with patch("src.bridge.kiwoom_wrapper.time.sleep") as mock_sleep:
            throttler.acquire()
            mock_sleep.assert_not_called()

    def test_acquire_records_timestamps(self):
        throttler = APIThrottler(rate_per_sec=5, rate_per_hour=1000)
        throttler.acquire()
        assert len(throttler._sec_calls) == 1
        assert len(throttler._hour_calls) == 1

    def test_acquire_multiple_within_limit(self):
        throttler = APIThrottler(rate_per_sec=5, rate_per_hour=1000)
        with patch("src.bridge.kiwoom_wrapper.time.sleep"):
            for _ in range(5):
                throttler.acquire()
        assert len(throttler._sec_calls) == 5

    def test_acquire_sleeps_when_per_sec_exceeded(self):
        throttler = APIThrottler(rate_per_sec=2, rate_per_hour=1000)
        # 두 번 채운 뒤 세 번째에서 sleep 호출됨
        import time as _time
        base = _time.monotonic()

        call_count = 0

        def fake_monotonic():
            nonlocal call_count
            call_count += 1
            # 처음 10번은 동일 시각, 이후에는 2초 후로 이동
            if call_count <= 10:
                return base
            return base + 2.0

        with patch("src.bridge.kiwoom_wrapper.time.monotonic", side_effect=fake_monotonic):
            with patch("src.bridge.kiwoom_wrapper.time.sleep") as mock_sleep:
                throttler.acquire()
                throttler.acquire()
                throttler.acquire()  # 세 번째에서 sleep 발생 기대
        mock_sleep.assert_called()

    def test_throttle_decorator_calls_function(self):
        throttler = APIThrottler(rate_per_sec=5, rate_per_hour=1000)
        mock_fn = MagicMock(return_value=42)
        decorated = throttler.throttle(mock_fn)
        result = decorated("arg1", key="val")
        assert result == 42
        mock_fn.assert_called_once_with("arg1", key="val")


# ------------------------------------------------------------------ #
# KiwoomWrapper.login
# ------------------------------------------------------------------ #

class TestKiwoomWrapperLogin:
    def test_login_success_resets_reconnect_count(self, wrapper, mock_bridge):
        mock_bridge.login.return_value = True
        wrapper._reconnect_count = 2

        result = wrapper.login("user", "pass")
        assert result is True
        assert wrapper._reconnect_count == 0

    def test_login_failure_does_not_reset_reconnect_count(self, wrapper, mock_bridge):
        mock_bridge.login.return_value = False
        wrapper._reconnect_count = 2

        result = wrapper.login("user", "wrong")
        assert result is False
        assert wrapper._reconnect_count == 2

    def test_login_delegates_to_bridge(self, wrapper, mock_bridge):
        mock_bridge.login.return_value = True
        wrapper.login("u", "p")
        mock_bridge.login.assert_called_once_with("u", "p")


# ------------------------------------------------------------------ #
# KiwoomWrapper.get_stock_price
# ------------------------------------------------------------------ #

class TestKiwoomWrapperGetStockPrice:
    def test_get_stock_price_applies_throttle_and_delegates(self, wrapper, mock_bridge):
        expected = StockPrice("005930", 70000, 69000, 71000, 68000, 100000)
        mock_bridge.get_stock_price.return_value = expected

        with patch.object(wrapper._throttler, "acquire") as mock_acquire:
            result = wrapper.get_stock_price("005930")

        mock_acquire.assert_called_once()
        mock_bridge.get_stock_price.assert_called_once_with("005930")
        assert result is expected


# ------------------------------------------------------------------ #
# KiwoomWrapper.register_realtime
# ------------------------------------------------------------------ #

class TestKiwoomWrapperRegisterRealtime:
    def test_register_realtime_adds_codes_to_list(self, wrapper, mock_bridge):
        mock_bridge.register_realtime.return_value = True

        wrapper.register_realtime(["005930", "000660"])
        assert "005930" in wrapper._realtime_codes
        assert "000660" in wrapper._realtime_codes

    def test_register_realtime_no_duplicate_codes(self, wrapper, mock_bridge):
        mock_bridge.register_realtime.return_value = True

        wrapper.register_realtime(["005930"])
        wrapper.register_realtime(["005930"])
        assert wrapper._realtime_codes.count("005930") == 1

    def test_register_realtime_default_fid_list(self, wrapper, mock_bridge):
        mock_bridge.register_realtime.return_value = True

        wrapper.register_realtime(["005930"])
        call_args = mock_bridge.register_realtime.call_args
        fids = call_args[0][1]
        assert "10" in fids  # 현재가

    def test_register_realtime_custom_fid_list(self, wrapper, mock_bridge):
        mock_bridge.register_realtime.return_value = True

        wrapper.register_realtime(["005930"], fid_list=["10", "15"])
        call_args = mock_bridge.register_realtime.call_args
        assert call_args[0][1] == ["10", "15"]

    def test_register_realtime_returns_false_does_not_add_codes(self, wrapper, mock_bridge):
        mock_bridge.register_realtime.return_value = False

        wrapper.register_realtime(["005930"])
        assert "005930" not in wrapper._realtime_codes


# ------------------------------------------------------------------ #
# KiwoomWrapper.send_order
# ------------------------------------------------------------------ #

class TestKiwoomWrapperSendOrder:
    def test_send_order_valid_buy(self, wrapper, mock_bridge):
        expected = OrderResult(True, "ORD001", "접수")
        mock_bridge.send_order.return_value = expected

        with patch.object(wrapper._throttler, "acquire"):
            result = wrapper.send_order("ACC", "005930", "BUY", 10, 70000)
        assert result is expected

    def test_send_order_invalid_price_raises(self, wrapper, mock_bridge):
        with pytest.raises(ValueError, match="호가 단위"):
            wrapper.send_order("ACC", "005930", "BUY", 10, 70050)

    def test_send_order_zero_quantity_raises(self, wrapper, mock_bridge):
        with pytest.raises(ValueError, match="수량"):
            wrapper.send_order("ACC", "005930", "BUY", 0, 70000)

    def test_send_order_negative_quantity_raises(self, wrapper, mock_bridge):
        with pytest.raises(ValueError, match="수량"):
            wrapper.send_order("ACC", "005930", "BUY", -1, 70000)

    def test_send_order_invalid_order_type_raises(self, wrapper, mock_bridge):
        with pytest.raises(ValueError, match="주문 유형"):
            wrapper.send_order("ACC", "005930", "UNKNOWN", 10, 70000)

    def test_send_order_market_price_zero_is_valid(self, wrapper, mock_bridge):
        expected = OrderResult(True, "ORD002", "접수")
        mock_bridge.send_order.return_value = expected

        with patch.object(wrapper._throttler, "acquire"):
            result = wrapper.send_order("ACC", "005930", "BUY_MARKET", 10, 0)
        assert result.success is True

    def test_send_order_all_valid_types(self, wrapper, mock_bridge):
        mock_bridge.send_order.return_value = OrderResult(True, "", "")
        for otype in ("BUY", "SELL", "BUY_MARKET", "SELL_MARKET"):
            with patch.object(wrapper._throttler, "acquire"):
                wrapper.send_order("ACC", "005930", otype, 1, 0)


# ------------------------------------------------------------------ #
# KiwoomWrapper.on_chejan / get_position
# ------------------------------------------------------------------ #

class TestKiwoomWrapperOnChejan:
    def test_buy_creates_new_position(self, wrapper):
        wrapper.on_chejan("005930", 10, 70000, "BUY")
        pos = wrapper.get_position("005930")
        assert pos["quantity"] == 10
        assert pos["avg_price"] == 70000

    def test_buy_updates_avg_price(self, wrapper):
        wrapper.on_chejan("005930", 10, 70000, "BUY")
        wrapper.on_chejan("005930", 10, 72000, "BUY")
        pos = wrapper.get_position("005930")
        assert pos["quantity"] == 20
        assert pos["avg_price"] == 71000  # (700000+720000)//20

    def test_sell_reduces_quantity(self, wrapper):
        wrapper.on_chejan("005930", 10, 70000, "BUY")
        wrapper.on_chejan("005930", 3, 71000, "SELL")
        pos = wrapper.get_position("005930")
        assert pos["quantity"] == 7

    def test_sell_all_clears_avg_price(self, wrapper):
        wrapper.on_chejan("005930", 10, 70000, "BUY")
        wrapper.on_chejan("005930", 10, 71000, "SELL")
        pos = wrapper.get_position("005930")
        assert pos["quantity"] == 0
        assert pos["avg_price"] == 0

    def test_get_position_unknown_code_returns_default(self, wrapper):
        pos = wrapper.get_position("UNKNOWN")
        assert pos == {"quantity": 0, "avg_price": 0}


# ------------------------------------------------------------------ #
# KiwoomWrapper.get_balance
# ------------------------------------------------------------------ #

class TestKiwoomWrapperGetBalance:
    def test_get_balance_applies_throttle_and_delegates(self, wrapper, mock_bridge):
        expected = Balance(deposit=1000000)
        mock_bridge.get_balance.return_value = expected

        with patch.object(wrapper._throttler, "acquire") as mock_acquire:
            result = wrapper.get_balance("ACC001")

        mock_acquire.assert_called_once()
        mock_bridge.get_balance.assert_called_once_with("ACC001")
        assert result is expected


# ------------------------------------------------------------------ #
# KiwoomWrapper.auto_reconnect
# ------------------------------------------------------------------ #

class TestKiwoomWrapperAutoReconnect:
    def test_reconnect_success_on_first_attempt(self, wrapper, mock_bridge):
        mock_bridge.is_connected = True
        mock_bridge.login.return_value = True

        result = wrapper.auto_reconnect("localhost", 50051, "u", "p")
        assert result is True
        assert wrapper._reconnecting is False

    def test_reconnect_re_registers_realtime_codes(self, wrapper, mock_bridge):
        wrapper._realtime_codes = ["005930", "000660"]
        mock_bridge.is_connected = True
        mock_bridge.login.return_value = True
        mock_bridge.register_realtime.return_value = True

        wrapper.auto_reconnect()
        mock_bridge.register_realtime.assert_called()

    def test_reconnect_fails_after_max_attempts(self, wrapper, mock_bridge):
        mock_bridge.is_connected = True
        mock_bridge.login.return_value = False  # 로그인 항상 실패

        result = wrapper.auto_reconnect()
        assert result is False
        assert wrapper._reconnect_count == KiwoomWrapper.MAX_RECONNECT

    def test_reconnect_not_reentrant(self, wrapper, mock_bridge):
        wrapper._reconnecting = True
        result = wrapper.auto_reconnect()
        assert result is False
        mock_bridge.connect.assert_not_called()

    def test_reconnect_resets_reconnecting_flag_after_completion(self, wrapper, mock_bridge):
        mock_bridge.is_connected = True
        mock_bridge.login.return_value = True

        wrapper.auto_reconnect()
        assert wrapper._reconnecting is False
