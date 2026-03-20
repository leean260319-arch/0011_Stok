"""리스크 관리자 - 4단계 검증 + 킬 스위치

버전: 1.0.0
작성일: 2026-03-17
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# 한국 주식 호가 단위 테이블
# ---------------------------------------------------------------------------
TICK_SIZE_TABLE = [
    (2_000, 1),
    (5_000, 5),
    (20_000, 10),
    (50_000, 50),
    (200_000, 100),
    (500_000, 500),
    (float("inf"), 1_000),
]


def get_tick_size(price: float) -> int:
    """가격대별 호가 단위 반환"""
    for threshold, tick in TICK_SIZE_TABLE:
        if price < threshold:
            return tick
    return 1_000


class RiskManager:
    """4단계 리스크 검증 + 킬 스위치"""

    # 기본 설정
    MAX_ORDER_AMOUNT = 500_000_000  # 최대 주문 금액 5억
    CONCENTRATION_LIMIT = 0.30  # 종목 집중도 30%
    SECTOR_LIMIT = 0.50  # 섹터 편중 50%
    DAILY_LOSS_LIMIT = 3.0  # 일일 손실 한도 %
    WEEKLY_LOSS_LIMIT = 5.0  # 주간 손실 한도 %
    MONTHLY_LOSS_LIMIT = 10.0  # 월간 손실 한도 %
    MIN_CASH_RATIO = 0.20  # 최소 예수금 비율 20%
    MDD_KILL_THRESHOLD = 15.0  # MDD 킬 스위치 임계값 %
    CLOSE_BUFFER_MINUTES = 10  # 장 마감 전 차단 시간 (분)

    def __init__(self):
        self._killed = False

    # ------------------------------------------------------------------
    # 킬 스위치
    # ------------------------------------------------------------------

    def kill_switch_on(self) -> None:
        """킬 스위치 발동 - 모든 주문 차단"""
        self._killed = True

    def kill_switch_off(self) -> None:
        """킬 스위치 해제 (수동만 허용)"""
        self._killed = False

    def is_killed(self) -> bool:
        """킬 스위치 상태 확인"""
        return self._killed

    # ------------------------------------------------------------------
    # T055: 리스크 1단계 - 주문 검증
    # ------------------------------------------------------------------

    def validate_order(self, order: dict) -> tuple[bool, str]:
        """주문 기본 검증: 금액, 수량, 가격, 호가 단위

        Args:
            order: {"symbol": str, "price": float, "quantity": int}

        Returns:
            (통과 여부, 사유 메시지)
        """
        if self._killed:
            return False, "킬 스위치 발동 중 - 모든 주문 차단"

        price = order.get("price", 0)
        quantity = order.get("quantity", 0)

        if price <= 0:
            return False, "주문 가격이 0 이하입니다"

        if quantity <= 0:
            return False, "주문 수량이 0 이하입니다"

        order_amount = price * quantity
        if order_amount > self.MAX_ORDER_AMOUNT:
            return False, f"최대 주문 금액 초과: {order_amount:,.0f} > {self.MAX_ORDER_AMOUNT:,.0f}"

        # 호가 단위 검증
        tick_size = get_tick_size(price)
        if price % tick_size != 0:
            return False, f"호가 단위 불일치: {price} (호가 단위: {tick_size})"

        return True, ""

    # ------------------------------------------------------------------
    # T056: 리스크 2단계 - 포트폴리오 검증
    # ------------------------------------------------------------------

    def validate_portfolio(self, order: dict, portfolio: dict) -> tuple[bool, str]:
        """포트폴리오 검증: 종목 집중도 30%, 섹터 편중 50%

        Args:
            order: {"symbol": str, "price": float, "quantity": int}
            portfolio: {"total_value": float, "positions": dict, "sectors": dict}

        Returns:
            (통과 여부, 사유 메시지)
        """
        if self._killed:
            return False, "킬 스위치 발동 중 - 모든 주문 차단"

        total_value = portfolio.get("total_value", 0)
        if total_value <= 0:
            return False, "포트폴리오 총 가치가 0 이하입니다"

        price = order.get("price", 0)
        quantity = order.get("quantity", 0)
        order_amount = price * quantity
        symbol = order.get("symbol", "")

        # 종목 집중도 검증
        positions = portfolio.get("positions", {})
        existing_value = positions.get(symbol, {}).get("value", 0)
        new_concentration = (existing_value + order_amount) / total_value
        if new_concentration > self.CONCENTRATION_LIMIT:
            return False, (
                f"종목 집중도 초과: {symbol} "
                f"{new_concentration:.1%} > {self.CONCENTRATION_LIMIT:.0%}"
            )

        # 섹터 편중 검증
        order_sector = portfolio.get("order_sector", "")
        if order_sector:
            sectors = portfolio.get("sectors", {})
            current_sector_ratio = sectors.get(order_sector, 0)
            added_ratio = order_amount / total_value
            new_sector_ratio = current_sector_ratio + added_ratio
            if new_sector_ratio > self.SECTOR_LIMIT:
                return False, (
                    f"섹터 편중 초과: {order_sector} "
                    f"{new_sector_ratio:.1%} > {self.SECTOR_LIMIT:.0%}"
                )

        return True, ""

    # ------------------------------------------------------------------
    # T057: 리스크 3단계 - 계좌 검증
    # ------------------------------------------------------------------

    def validate_account(self, order: dict, account: dict) -> tuple[bool, str]:
        """계좌 검증: 일일/주간/월간 손실 한도, 최소 예수금

        Args:
            order: {"symbol": str, "price": float, "quantity": int}
            account: {"total_equity": float, "available_cash": float,
                      "daily_pnl_pct": float, "weekly_pnl_pct": float,
                      "monthly_pnl_pct": float}

        Returns:
            (통과 여부, 사유 메시지)
        """
        if self._killed:
            return False, "킬 스위치 발동 중 - 모든 주문 차단"

        daily = account.get("daily_pnl_pct", 0)
        weekly = account.get("weekly_pnl_pct", 0)
        monthly = account.get("monthly_pnl_pct", 0)

        if daily < -self.DAILY_LOSS_LIMIT:
            return False, f"일일 손실 한도 초과: {daily:.1f}% (한도: -{self.DAILY_LOSS_LIMIT}%)"

        if weekly < -self.WEEKLY_LOSS_LIMIT:
            return False, f"주간 손실 한도 초과: {weekly:.1f}% (한도: -{self.WEEKLY_LOSS_LIMIT}%)"

        if monthly < -self.MONTHLY_LOSS_LIMIT:
            return False, f"월간 손실 한도 초과: {monthly:.1f}% (한도: -{self.MONTHLY_LOSS_LIMIT}%)"

        total_equity = account.get("total_equity", 0)
        available_cash = account.get("available_cash", 0)
        if total_equity > 0:
            cash_ratio = available_cash / total_equity
            if cash_ratio < self.MIN_CASH_RATIO:
                return False, (
                    f"최소 예수금 비율 미달: {cash_ratio:.1%} < {self.MIN_CASH_RATIO:.0%}"
                )

        return True, ""

    # ------------------------------------------------------------------
    # T058: 리스크 4단계 - 시스템 안전장치
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # P2-02: Kelly Criterion 포지션 사이징
    # ------------------------------------------------------------------

    def calculate_position_size(
        self,
        account_balance: float,
        win_rate: float,
        avg_win: float,
        avg_loss: float,
        signal_confidence: float = 1.0,
        max_position_pct: float = 0.3,
    ) -> float:
        """Kelly Criterion 기반 포지션 사이징 (Half-Kelly).

        Args:
            account_balance: 계좌 잔고
            win_rate: 승률 (0.0~1.0)
            avg_win: 평균 수익률 (양수)
            avg_loss: 평균 손실률 (양수)
            signal_confidence: 시그널 신뢰도 (0.0~1.0)
            max_position_pct: 최대 포지션 비율

        Returns:
            투입 금액
        """
        if avg_loss <= 0 or win_rate <= 0 or win_rate >= 1.0:
            return account_balance * 0.05  # 최소 5%

        # Kelly 공식: f* = (b*p - q) / b
        b = avg_win / avg_loss  # 손익비
        p = win_rate
        q = 1.0 - p
        kelly = (b * p - q) / b

        # Half-Kelly (보수적)
        half_kelly = kelly * 0.5

        # 시그널 신뢰도 반영
        adjusted = half_kelly * signal_confidence

        # 범위 제한: 5% ~ max_position_pct
        fraction = max(0.05, min(adjusted, max_position_pct))

        return round(account_balance * fraction, 0)

    # ------------------------------------------------------------------
    # P2-03: ATR 기반 동적 손절
    # ------------------------------------------------------------------

    def calculate_dynamic_stop_loss(
        self,
        entry_price: float,
        atr: float,
        multiplier: float = 2.5,
        direction: str = "long",
    ) -> float:
        """ATR 기반 동적 손절가 계산.

        Args:
            entry_price: 진입 가격
            atr: ATR 값
            multiplier: ATR 배수 (기본 2.5)
            direction: "long" 또는 "short"

        Returns:
            손절가
        """
        if atr <= 0:
            # ATR 없으면 고정 2% 손절
            if direction == "long":
                return round(entry_price * 0.98, 0)
            return round(entry_price * 1.02, 0)

        offset = atr * multiplier
        if direction == "long":
            return round(entry_price - offset, 0)
        return round(entry_price + offset, 0)

    def calculate_trailing_stop(
        self,
        highest_price: float,
        atr: float,
        multiplier: float = 2.0,
    ) -> float:
        """ATR 기반 트레일링 스탑 계산.

        Args:
            highest_price: 진입 후 최고가
            atr: ATR 값
            multiplier: ATR 배수 (기본 2.0)

        Returns:
            트레일링 스탑 가격
        """
        if atr <= 0:
            return round(highest_price * 0.98, 0)  # 기본 2%
        return round(highest_price - atr * multiplier, 0)

    def system_safeguard(self, market_info: dict) -> tuple[bool, str]:
        """시스템 안전장치: MDD 킬 스위치, API 연결, 장 마감 전 차단

        Args:
            market_info: {"mdd_pct": float, "api_connected": bool,
                          "market_open": bool, "minutes_to_close": int}

        Returns:
            (통과 여부, 사유 메시지)
        """
        mdd = market_info.get("mdd_pct", 0)
        api_connected = market_info.get("api_connected", True)
        market_open = market_info.get("market_open", True)
        minutes_to_close = market_info.get("minutes_to_close", 60)

        # MDD 킬 스위치
        if mdd > self.MDD_KILL_THRESHOLD:
            self.kill_switch_on()
            return False, f"MDD {mdd:.1f}% 초과 - 킬 스위치 자동 발동 (임계값: {self.MDD_KILL_THRESHOLD}%)"

        # API 연결 확인
        if not api_connected:
            return False, "API 연결 끊김 - 주문 차단"

        # 장 마감 확인
        if not market_open:
            return False, "장 마감 상태 - 주문 차단"

        # 장 마감 전 차단
        if minutes_to_close < self.CLOSE_BUFFER_MINUTES:
            return False, f"장 마감 {minutes_to_close}분 전 - 주문 차단 (버퍼: {self.CLOSE_BUFFER_MINUTES}분)"

        return True, ""
