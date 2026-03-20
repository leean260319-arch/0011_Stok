"""KiwoomBridge 테스트 - Mock gRPC 채널 사용"""
from unittest.mock import MagicMock, patch

import pytest

from src.bridge.kiwoom_bridge import Balance, HoldingItem, KiwoomBridge, OrderResult, StockPrice
from src.bridge import kiwoom_pb2


# ------------------------------------------------------------------ #
# 픽스처
# ------------------------------------------------------------------ #

@pytest.fixture
def bridge():
    return KiwoomBridge()


@pytest.fixture
def connected_bridge():
    """gRPC 채널 연결이 Mock된 KiwoomBridge"""
    b = KiwoomBridge()
    with patch("src.bridge.kiwoom_bridge.grpc.insecure_channel") as mock_channel_fn:
        mock_channel = MagicMock()
        mock_channel_fn.return_value = mock_channel
        with patch("src.bridge.kiwoom_bridge.kiwoom_pb2_grpc.KiwoomServiceStub") as mock_stub_cls:
            mock_stub = MagicMock()
            mock_stub_cls.return_value = mock_stub
            b.connect("localhost", 50051)
            b._stub = mock_stub  # 직접 참조 유지
    return b


# ------------------------------------------------------------------ #
# 초기 상태
# ------------------------------------------------------------------ #

class TestKiwoomBridgeInit:
    def test_initial_state_not_connected(self, bridge):
        assert bridge.is_connected is False

    def test_initial_channel_none(self, bridge):
        assert bridge._channel is None

    def test_initial_stub_none(self, bridge):
        assert bridge._stub is None


# ------------------------------------------------------------------ #
# connect / disconnect
# ------------------------------------------------------------------ #

class TestKiwoomBridgeConnect:
    def test_connect_sets_connected_true(self, bridge):
        with patch("src.bridge.kiwoom_bridge.grpc.insecure_channel") as mock_ch:
            mock_ch.return_value = MagicMock()
            with patch("src.bridge.kiwoom_bridge.kiwoom_pb2_grpc.KiwoomServiceStub"):
                bridge.connect("localhost", 50051)
        assert bridge.is_connected is True

    def test_connect_creates_channel_with_correct_address(self, bridge):
        with patch("src.bridge.kiwoom_bridge.grpc.insecure_channel") as mock_ch:
            mock_ch.return_value = MagicMock()
            with patch("src.bridge.kiwoom_bridge.kiwoom_pb2_grpc.KiwoomServiceStub"):
                bridge.connect("192.168.1.1", 12345)
        mock_ch.assert_called_once_with("192.168.1.1:12345")

    def test_disconnect_sets_connected_false(self, connected_bridge):
        connected_bridge.disconnect()
        assert connected_bridge.is_connected is False

    def test_disconnect_clears_channel_and_stub(self, connected_bridge):
        connected_bridge.disconnect()
        assert connected_bridge._channel is None
        assert connected_bridge._stub is None

    def test_disconnect_when_not_connected_is_safe(self, bridge):
        bridge.disconnect()  # should not raise
        assert bridge.is_connected is False


# ------------------------------------------------------------------ #
# login
# ------------------------------------------------------------------ #

class TestKiwoomBridgeLogin:
    def test_login_returns_true_on_success(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = True
        mock_resp.message = "OK"
        connected_bridge._stub.Login.return_value = mock_resp

        result = connected_bridge.login("user1", "pass1")
        assert result is True

    def test_login_returns_false_on_failure(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = False
        mock_resp.message = "FAIL"
        connected_bridge._stub.Login.return_value = mock_resp

        result = connected_bridge.login("user1", "wrong")
        assert result is False

    def test_login_calls_stub_with_credentials(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = True
        mock_resp.message = "OK"
        connected_bridge._stub.Login.return_value = mock_resp

        connected_bridge.login("testuser", "testpass")
        call_args = connected_bridge._stub.Login.call_args[0][0]
        assert call_args.user_id == "testuser"
        assert call_args.password == "testpass"


# ------------------------------------------------------------------ #
# get_stock_price
# ------------------------------------------------------------------ #

class TestKiwoomBridgeGetStockPrice:
    def test_get_stock_price_returns_stock_price_dataclass(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.code = "005930"
        mock_resp.current_price = 70000
        mock_resp.open_price = 69000
        mock_resp.high_price = 71000
        mock_resp.low_price = 68000
        mock_resp.volume = 100000
        connected_bridge._stub.GetStockPrice.return_value = mock_resp

        result = connected_bridge.get_stock_price("005930")
        assert isinstance(result, StockPrice)
        assert result.code == "005930"
        assert result.current_price == 70000
        assert result.open_price == 69000
        assert result.high_price == 71000
        assert result.low_price == 68000
        assert result.volume == 100000

    def test_get_stock_price_calls_stub_with_code(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.code = "000660"
        mock_resp.current_price = 0
        mock_resp.open_price = 0
        mock_resp.high_price = 0
        mock_resp.low_price = 0
        mock_resp.volume = 0
        connected_bridge._stub.GetStockPrice.return_value = mock_resp

        connected_bridge.get_stock_price("000660")
        call_args = connected_bridge._stub.GetStockPrice.call_args[0][0]
        assert call_args.code == "000660"


# ------------------------------------------------------------------ #
# send_order
# ------------------------------------------------------------------ #

class TestKiwoomBridgeSendOrder:
    def test_send_order_returns_order_result(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = True
        mock_resp.order_no = "ORDER001"
        mock_resp.message = "접수"
        connected_bridge._stub.SendOrder.return_value = mock_resp

        result = connected_bridge.send_order("ACC001", "005930", "BUY", 10, 70000)
        assert isinstance(result, OrderResult)
        assert result.success is True
        assert result.order_no == "ORDER001"
        assert result.message == "접수"

    def test_send_order_calls_stub_with_correct_params(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = True
        mock_resp.order_no = ""
        mock_resp.message = ""
        connected_bridge._stub.SendOrder.return_value = mock_resp

        connected_bridge.send_order("ACC001", "005930", "SELL", 5, 69000)
        call_args = connected_bridge._stub.SendOrder.call_args[0][0]
        assert call_args.account == "ACC001"
        assert call_args.code == "005930"
        assert call_args.order_type == "SELL"
        assert call_args.quantity == 5
        assert call_args.price == 69000


# ------------------------------------------------------------------ #
# get_balance
# ------------------------------------------------------------------ #

class TestKiwoomBridgeGetBalance:
    def test_get_balance_returns_balance_dataclass(self, connected_bridge):
        holding = MagicMock()
        holding.code = "005930"
        holding.name = "삼성전자"
        holding.quantity = 10
        holding.avg_price = 68000
        holding.current_price = 70000
        holding.eval_amount = 700000

        mock_resp = MagicMock()
        mock_resp.deposit = 1000000
        mock_resp.holdings = [holding]
        mock_resp.total_eval_amount = 1700000
        connected_bridge._stub.GetBalance.return_value = mock_resp

        result = connected_bridge.get_balance("ACC001")
        assert isinstance(result, Balance)
        assert result.deposit == 1000000
        assert result.total_eval_amount == 1700000
        assert len(result.holdings) == 1
        assert isinstance(result.holdings[0], HoldingItem)
        assert result.holdings[0].code == "005930"

    def test_get_balance_empty_holdings(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.deposit = 500000
        mock_resp.holdings = []
        mock_resp.total_eval_amount = 0
        connected_bridge._stub.GetBalance.return_value = mock_resp

        result = connected_bridge.get_balance("ACC001")
        assert result.holdings == []


# ------------------------------------------------------------------ #
# register_realtime
# ------------------------------------------------------------------ #

class TestKiwoomBridgeRegisterRealtime:
    def test_register_realtime_returns_true_on_success(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = True
        connected_bridge._stub.RegisterRealtime.return_value = mock_resp

        result = connected_bridge.register_realtime(["005930", "000660"], ["10", "15"])
        assert result is True

    def test_register_realtime_calls_stub_with_codes_and_fids(self, connected_bridge):
        mock_resp = MagicMock()
        mock_resp.success = True
        connected_bridge._stub.RegisterRealtime.return_value = mock_resp

        connected_bridge.register_realtime(["005930"], ["10", "11"])
        call_args = connected_bridge._stub.RegisterRealtime.call_args[0][0]
        assert list(call_args.codes) == ["005930"]
        assert list(call_args.fid_list) == ["10", "11"]
