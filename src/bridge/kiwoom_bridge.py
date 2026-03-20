"""키움 gRPC 클라이언트 (64bit Python 환경)
버전: 1.0.0
설명: KiwoomBridge - gRPC 채널을 통해 32bit 서버와 통신
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import grpc

from src.bridge import kiwoom_pb2, kiwoom_pb2_grpc
from src.utils.logger import get_logger

logger = get_logger("bridge.client")


@dataclass
class StockPrice:
    code: str
    current_price: int
    open_price: int
    high_price: int
    low_price: int
    volume: int


@dataclass
class OrderResult:
    success: bool
    order_no: str
    message: str


@dataclass
class HoldingItem:
    code: str
    name: str
    quantity: int
    avg_price: int
    current_price: int
    eval_amount: int


@dataclass
class Balance:
    deposit: int
    holdings: List[HoldingItem] = field(default_factory=list)
    total_eval_amount: int = 0


class KiwoomBridge:
    """gRPC 클라이언트 - 키움 32bit 서버와 통신"""

    def __init__(self):
        self._channel: grpc.Channel | None = None
        self._stub: kiwoom_pb2_grpc.KiwoomServiceStub | None = None
        self._connected = False

    def connect(self, host: str = "localhost", port: int = 50051) -> None:
        """gRPC 채널 연결"""
        self._channel = grpc.insecure_channel(f"{host}:{port}")
        self._stub = kiwoom_pb2_grpc.KiwoomServiceStub(self._channel)
        self._connected = True
        logger.info("KiwoomBridge 연결: %s:%d", host, port)

    def disconnect(self) -> None:
        """gRPC 채널 종료"""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stub = None
        self._connected = False
        logger.info("KiwoomBridge 연결 종료")

    @property
    def is_connected(self) -> bool:
        return self._connected

    def login(self, user_id: str = "", password: str = "") -> bool:
        """로그인 요청"""
        response = self._stub.Login(
            kiwoom_pb2.LoginRequest(user_id=user_id, password=password)
        )
        logger.info("로그인 결과: %s", response.message)
        return response.success

    def get_stock_price(self, code: str) -> StockPrice:
        """종목 시세 조회"""
        response = self._stub.GetStockPrice(kiwoom_pb2.StockPriceRequest(code=code))
        return StockPrice(
            code=response.code,
            current_price=response.current_price,
            open_price=response.open_price,
            high_price=response.high_price,
            low_price=response.low_price,
            volume=response.volume,
        )

    def send_order(
        self,
        account: str,
        code: str,
        order_type: str,
        quantity: int,
        price: int,
    ) -> OrderResult:
        """주문 전송"""
        response = self._stub.SendOrder(
            kiwoom_pb2.OrderRequest(
                account=account,
                code=code,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )
        )
        return OrderResult(
            success=response.success,
            order_no=response.order_no,
            message=response.message,
        )

    def get_balance(self, account: str) -> Balance:
        """잔고 조회"""
        response = self._stub.GetBalance(kiwoom_pb2.BalanceRequest(account=account))
        holdings = [
            HoldingItem(
                code=h.code,
                name=h.name,
                quantity=h.quantity,
                avg_price=h.avg_price,
                current_price=h.current_price,
                eval_amount=h.eval_amount,
            )
            for h in response.holdings
        ]
        return Balance(
            deposit=response.deposit,
            holdings=holdings,
            total_eval_amount=response.total_eval_amount,
        )

    def get_account_list(self) -> list[str]:
        """계좌 목록을 조회한다.

        gRPC 서버에서 로그인 후 계좌 목록을 반환한다.
        서버 미구현 시 빈 리스트 반환.
        """
        if not self.is_connected:
            return []
        # gRPC 서버에 GetAccountList RPC가 구현되면 호출
        # 현재는 빈 리스트 반환 (서버 미구현 시)
        return []

    def get_price_history(self, stock_code: str, count: int = 60) -> list[dict]:
        """종목의 과거 OHLCV 데이터를 조회한다.

        Args:
            stock_code: 종목 코드
            count: 조회할 봉 수 (기본 60)

        Returns:
            OHLCV dict 리스트. gRPC 서버 미구현 시 빈 리스트 반환.
        """
        if not self.is_connected:
            return []
        # gRPC를 통해 과거 데이터 조회 (서버 구현 필요)
        # 현재는 빈 리스트 반환 (서버 미구현 시)
        return []

    def register_realtime(self, codes: List[str], fid_list: List[str]) -> bool:
        """실시간 시세 등록"""
        response = self._stub.RegisterRealtime(
            kiwoom_pb2.RealtimeRequest(codes=codes, fid_list=fid_list)
        )
        return response.success
