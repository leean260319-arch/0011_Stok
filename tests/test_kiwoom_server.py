"""KiwoomServer 테스트 - 클래스/메서드 존재 및 stub 응답 확인"""
from unittest.mock import MagicMock, patch

import pytest


# ------------------------------------------------------------------ #
# KiwoomServicer 클래스/메서드 존재 확인
# ------------------------------------------------------------------ #

class TestKiwoomServicerExists:
    def test_kiwoom_servicer_importable(self):
        from src.bridge.kiwoom_server import KiwoomServicer
        assert KiwoomServicer is not None

    def test_serve_function_importable(self):
        from src.bridge.kiwoom_server import serve
        assert callable(serve)

    def test_kiwoom_servicer_has_login(self):
        from src.bridge.kiwoom_server import KiwoomServicer
        assert hasattr(KiwoomServicer, "Login")

    def test_kiwoom_servicer_has_get_stock_price(self):
        from src.bridge.kiwoom_server import KiwoomServicer
        assert hasattr(KiwoomServicer, "GetStockPrice")

    def test_kiwoom_servicer_has_send_order(self):
        from src.bridge.kiwoom_server import KiwoomServicer
        assert hasattr(KiwoomServicer, "SendOrder")

    def test_kiwoom_servicer_has_get_balance(self):
        from src.bridge.kiwoom_server import KiwoomServicer
        assert hasattr(KiwoomServicer, "GetBalance")

    def test_kiwoom_servicer_has_register_realtime(self):
        from src.bridge.kiwoom_server import KiwoomServicer
        assert hasattr(KiwoomServicer, "RegisterRealtime")


# ------------------------------------------------------------------ #
# KiwoomServicer stub 응답 확인
# ------------------------------------------------------------------ #

class TestKiwoomServicerStubResponses:
    @pytest.fixture
    def servicer(self):
        # kiwoom_pb2는 서버 모듈 내에서 직접 임포트됨 (32bit stub)
        # 서버 임포트 시 kiwoom_pb2/kiwoom_pb2_grpc를 src.bridge 경로에서 가져오지 않으므로
        # 모듈 수준 패치 필요
        with patch.dict("sys.modules", {
            "kiwoom_pb2": __import__("src.bridge.kiwoom_pb2", fromlist=["kiwoom_pb2"]),
            "kiwoom_pb2_grpc": __import__("src.bridge.kiwoom_pb2_grpc", fromlist=["kiwoom_pb2_grpc"]),
        }):
            from src.bridge.kiwoom_server import KiwoomServicer
            return KiwoomServicer()

    def test_init_connected_false(self, servicer):
        assert servicer._connected is False

    def test_init_ocx_none(self, servicer):
        assert servicer._ocx is None

    def test_login_sets_connected_true(self, servicer):
        from src.bridge import kiwoom_pb2
        req = kiwoom_pb2.LoginRequest(user_id="u", password="p")
        resp = servicer.Login(req, context=None)
        assert servicer._connected is True
        assert resp.success is True

    def test_get_stock_price_returns_correct_code(self, servicer):
        from src.bridge import kiwoom_pb2
        req = kiwoom_pb2.StockPriceRequest(code="005930")
        resp = servicer.GetStockPrice(req, context=None)
        assert resp.code == "005930"

    def test_send_order_returns_success(self, servicer):
        from src.bridge import kiwoom_pb2
        req = kiwoom_pb2.OrderRequest(
            account="ACC", code="005930", order_type="BUY", quantity=10, price=70000
        )
        resp = servicer.SendOrder(req, context=None)
        assert resp.success is True

    def test_get_balance_returns_zero_deposit(self, servicer):
        from src.bridge import kiwoom_pb2
        req = kiwoom_pb2.BalanceRequest(account="ACC")
        resp = servicer.GetBalance(req, context=None)
        assert resp.deposit == 0

    def test_register_realtime_returns_success(self, servicer):
        from src.bridge import kiwoom_pb2
        req = kiwoom_pb2.RealtimeRequest(codes=["005930"], fid_list=["10"])
        resp = servicer.RegisterRealtime(req, context=None)
        assert resp.success is True


# ------------------------------------------------------------------ #
# serve() 함수 - gRPC 서버 생성 확인
# ------------------------------------------------------------------ #

class TestServeFunction:
    def test_serve_returns_server_object(self):
        with patch.dict("sys.modules", {
            "kiwoom_pb2": __import__("src.bridge.kiwoom_pb2", fromlist=["kiwoom_pb2"]),
            "kiwoom_pb2_grpc": __import__("src.bridge.kiwoom_pb2_grpc", fromlist=["kiwoom_pb2_grpc"]),
        }):
            with patch("src.bridge.kiwoom_server.grpc.server") as mock_grpc_server:
                mock_server = MagicMock()
                mock_grpc_server.return_value = mock_server

                from importlib import import_module, reload
                import src.bridge.kiwoom_server as ks_mod
                reload(ks_mod)

                srv = ks_mod.serve("localhost", 50051)
                mock_server.start.assert_called_once()
                assert srv is mock_server
