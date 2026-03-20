"""키움 API 고수준 래퍼
버전: 1.0.0
설명: KiwoomWrapper - bridge를 주입받아 사용하는 고수준 인터페이스
     APIThrottler - 초당 5회, 시간당 1000회 제한
     register_realtime, auto_reconnect, send_order, on_chejan, get_balance
"""
from __future__ import annotations

import asyncio
import collections
import functools
import threading
import time
from typing import Any, Callable, Deque, Dict, List, Optional

from src.bridge.kiwoom_bridge import Balance, KiwoomBridge, OrderResult, StockPrice
from src.utils.constants import API_RATE_PER_HOUR, API_RATE_PER_SEC
from src.utils.logger import get_logger

logger = get_logger("bridge.wrapper")

# 호가 단위 테이블 (가격 -> 호가 단위)
_TICK_SIZE_TABLE = [
    (2_000, 1),
    (5_000, 5),
    (20_000, 10),
    (50_000, 50),
    (200_000, 100),
    (500_000, 500),
    (float("inf"), 1000),
]


def get_tick_size(price: int) -> int:
    """가격에 따른 호가 단위 반환"""
    for limit, tick in _TICK_SIZE_TABLE:
        if price < limit:
            return tick
    return 1000


def validate_price(price: int) -> bool:
    """호가 단위 검증"""
    if price <= 0:
        return True  # 시장가
    tick = get_tick_size(price)
    return price % tick == 0


class APIThrottler:
    """초당 5회, 시간당 1000회 API 호출 제한기"""

    def __init__(
        self,
        rate_per_sec: int = API_RATE_PER_SEC,
        rate_per_hour: int = API_RATE_PER_HOUR,
    ):
        self._rate_per_sec = rate_per_sec
        self._rate_per_hour = rate_per_hour
        self._lock = threading.Lock()
        self._sec_calls: Deque[float] = collections.deque()
        self._hour_calls: Deque[float] = collections.deque()

    def _clean_old(self, now: float) -> None:
        """오래된 타임스탬프 제거"""
        while self._sec_calls and now - self._sec_calls[0] >= 1.0:
            self._sec_calls.popleft()
        while self._hour_calls and now - self._hour_calls[0] >= 3600.0:
            self._hour_calls.popleft()

    def acquire(self) -> None:
        """호출 전 제한 확인 및 대기"""
        with self._lock:
            while True:
                now = time.monotonic()
                self._clean_old(now)

                if len(self._hour_calls) >= self._rate_per_hour:
                    wait = 3600.0 - (now - self._hour_calls[0]) + 0.001
                    time.sleep(wait)
                    continue

                if len(self._sec_calls) >= self._rate_per_sec:
                    wait = 1.0 - (now - self._sec_calls[0]) + 0.001
                    time.sleep(wait)
                    continue

                ts = time.monotonic()
                self._sec_calls.append(ts)
                self._hour_calls.append(ts)
                break

    def throttle(self, func: Callable) -> Callable:
        """스로틀링 데코레이터"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.acquire()
            return func(*args, **kwargs)

        return wrapper


class KiwoomWrapper:
    """키움 API 고수준 래퍼"""

    MAX_RECONNECT = 3

    def __init__(self, bridge: KiwoomBridge):
        self._bridge = bridge
        self._throttler = APIThrottler()
        self._realtime_codes: List[str] = []
        self._positions: Dict[str, Dict[str, Any]] = {}
        self._reconnect_count = 0
        self._reconnecting = False

    # ------------------------------------------------------------------ #
    # 로그인 / 연결
    # ------------------------------------------------------------------ #

    def login(self, user_id: str = "", password: str = "") -> bool:
        """로그인"""
        result = self._bridge.login(user_id, password)
        if result:
            self._reconnect_count = 0
        return result

    # ------------------------------------------------------------------ #
    # 시세 조회
    # ------------------------------------------------------------------ #

    def get_stock_price(self, code: str) -> StockPrice:
        """종목 시세 조회 (스로틀링 적용)"""
        self._throttler.acquire()
        return self._bridge.get_stock_price(code)

    # ------------------------------------------------------------------ #
    # 실시간 시세
    # ------------------------------------------------------------------ #

    def register_realtime(self, codes: List[str], fid_list: Optional[List[str]] = None) -> bool:
        """실시간 시세 등록"""
        if fid_list is None:
            fid_list = ["10", "11", "12", "13", "15"]  # 현재가, 시가, 고가, 저가, 거래량
        success = self._bridge.register_realtime(codes, fid_list)
        if success:
            for code in codes:
                if code not in self._realtime_codes:
                    self._realtime_codes.append(code)
            logger.info("실시간 등록: %s", codes)
        return success

    # ------------------------------------------------------------------ #
    # 주문
    # ------------------------------------------------------------------ #

    def send_order(
        self,
        account: str,
        code: str,
        order_type: str,
        quantity: int,
        price: int = 0,
    ) -> OrderResult:
        """주문 실행 (호가 단위 검증 포함)"""
        if price > 0 and not validate_price(price):
            tick = get_tick_size(price)
            raise ValueError(
                f"호가 단위 오류: price={price}, 호가단위={tick}"
            )
        if quantity <= 0:
            raise ValueError(f"수량 오류: quantity={quantity}")
        if order_type not in ("BUY", "SELL", "BUY_MARKET", "SELL_MARKET"):
            raise ValueError(f"주문 유형 오류: order_type={order_type}")

        self._throttler.acquire()
        result = self._bridge.send_order(account, code, order_type, quantity, price)
        logger.info(
            "주문 전송: account=%s code=%s type=%s qty=%d price=%d -> %s",
            account, code, order_type, quantity, price, result.order_no,
        )
        return result

    # ------------------------------------------------------------------ #
    # 체결 처리
    # ------------------------------------------------------------------ #

    def on_chejan(self, code: str, quantity: int, price: int, side: str) -> None:
        """체결/잔고 이벤트 수신 - 포지션 자동 업데이트"""
        if code not in self._positions:
            self._positions[code] = {"quantity": 0, "avg_price": 0}

        pos = self._positions[code]
        if side == "BUY":
            total_cost = pos["avg_price"] * pos["quantity"] + price * quantity
            pos["quantity"] += quantity
            if pos["quantity"] > 0:
                pos["avg_price"] = total_cost // pos["quantity"]
        elif side == "SELL":
            pos["quantity"] = max(0, pos["quantity"] - quantity)
            if pos["quantity"] == 0:
                pos["avg_price"] = 0

        logger.info(
            "체결 업데이트: code=%s side=%s qty=%d price=%d -> position=%s",
            code, side, quantity, price, pos,
        )

    def get_position(self, code: str) -> Dict[str, Any]:
        """포지션 조회"""
        return self._positions.get(code, {"quantity": 0, "avg_price": 0})

    # ------------------------------------------------------------------ #
    # 잔고 조회
    # ------------------------------------------------------------------ #

    def get_balance(self, account: str) -> Balance:
        """잔고 조회 (스로틀링 적용)"""
        self._throttler.acquire()
        return self._bridge.get_balance(account)

    # ------------------------------------------------------------------ #
    # 자동 재연결
    # ------------------------------------------------------------------ #

    def auto_reconnect(
        self,
        host: str = "localhost",
        port: int = 50051,
        user_id: str = "",
        password: str = "",
    ) -> bool:
        """연결 끊김 감지 후 최대 3회 재시도"""
        if self._reconnecting:
            return False
        self._reconnecting = True
        self._reconnect_count = 0
        success = False

        while self._reconnect_count < self.MAX_RECONNECT:
            self._reconnect_count += 1
            logger.info(
                "재연결 시도 %d/%d", self._reconnect_count, self.MAX_RECONNECT
            )
            self._bridge.connect(host, port)
            if self._bridge.is_connected:
                result = self._bridge.login(user_id, password)
                if result:
                    # 실시간 재등록
                    if self._realtime_codes:
                        self.register_realtime(self._realtime_codes)
                    success = True
                    break

        self._reconnecting = False
        if not success:
            logger.warning("재연결 실패: 최대 시도 횟수 초과")
        return success
