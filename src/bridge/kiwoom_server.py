"""키움 gRPC 서버 (32bit Python 환경에서 실행)
버전: 1.0.0
설명: KOAPY 기반 gRPC 서버 - 키움 OCX 래핑 인터페이스
      실제 OCX 호출 부분은 placeholder (32bit Windows 전용)
"""
from concurrent import futures

import grpc

from src.bridge import kiwoom_pb2
from src.bridge import kiwoom_pb2_grpc
from src.utils.logger import get_logger

logger = get_logger("bridge.server")

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 50051


class KiwoomServicer(kiwoom_pb2_grpc.KiwoomServiceServicer):
    """키움 OCX를 래핑하는 gRPC 서비스 구현체 (32bit 전용)"""

    def __init__(self):
        self._connected = False
        self._ocx = None  # 실제 환경: win32com.client.Dispatch("KHOPENAPI.KHOpenAPICtrl.1")
        logger.info("KiwoomServicer 초기화")

    def Login(self, request, context):
        # [placeholder] 실제: self._ocx.CommConnect()
        logger.info("Login 요청: user_id=%s", request.user_id)
        self._connected = True
        return kiwoom_pb2.LoginResponse(success=True, message="로그인 성공 (stub)")

    def GetStockPrice(self, request, context):
        # [placeholder] 실제: self._ocx.GetCommData(...)
        logger.info("GetStockPrice 요청: code=%s", request.code)
        return kiwoom_pb2.StockPriceResponse(
            code=request.code,
            current_price=0,
            open_price=0,
            high_price=0,
            low_price=0,
            volume=0,
        )

    def SendOrder(self, request, context):
        # [placeholder] 실제: self._ocx.SendOrder(...)
        logger.info(
            "SendOrder 요청: account=%s code=%s type=%s qty=%d price=%d",
            request.account,
            request.code,
            request.order_type,
            request.quantity,
            request.price,
        )
        return kiwoom_pb2.OrderResponse(success=True, order_no="", message="주문 접수 (stub)")

    def GetBalance(self, request, context):
        # [placeholder] 실제: self._ocx.GetLoginInfo("ACCNO")
        logger.info("GetBalance 요청: account=%s", request.account)
        return kiwoom_pb2.BalanceResponse(deposit=0, holdings=[], total_eval_amount=0)

    def RegisterRealtime(self, request, context):
        # [placeholder] 실제: self._ocx.SetRealReg(...)
        logger.info("RegisterRealtime 요청: codes=%s", list(request.codes))
        return kiwoom_pb2.RealtimeResponse(success=True, message="실시간 등록 (stub)")


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> grpc.Server:
    """gRPC 서버 시작 및 반환"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kiwoom_pb2_grpc.add_KiwoomServiceServicer_to_server(KiwoomServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info("KiwoomServer 시작: %s:%d", host, port)
    return server


if __name__ == "__main__":
    srv = serve()
    srv.wait_for_termination()
