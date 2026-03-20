"""가상 포트폴리오 - bridge 없이 시뮬레이션 매매 추적

버전: 1.0.0
작성일: 2026-03-18
설명: 자동매매 시뮬레이션 시 보유종목/잔고/수익률을 추적하는 가상 포트폴리오
"""

from dataclasses import dataclass, field
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger("engine.virtual_portfolio")


@dataclass
class Position:
    """보유 종목"""

    code: str
    name: str
    quantity: int
    avg_price: float
    current_price: float = 0.0
    bought_at: str = ""

    @property
    def eval_amount(self) -> float:
        return self.quantity * self.current_price

    @property
    def profit_loss(self) -> float:
        return (self.current_price - self.avg_price) * self.quantity

    @property
    def profit_rate(self) -> float:
        if self.avg_price == 0:
            return 0.0
        return (self.current_price - self.avg_price) / self.avg_price * 100


class VirtualPortfolio:
    """가상 포트폴리오 - 시뮬레이션 매매 추적.

    bridge(키움 API) 없이도 매수/매도를 추적하여
    보유종목, 잔고, 수익률을 관리한다.
    """

    def __init__(self, initial_cash: int = 10_000_000):
        self._initial_cash = initial_cash
        self._cash = initial_cash
        self._positions: dict[str, Position] = {}
        self._trade_history: list[dict] = []
        self._daily_values: list[dict] = []
        logger.info("VirtualPortfolio 초기화: 초기자금 %s원", f"{initial_cash:,}")

    @property
    def cash(self) -> int:
        return self._cash

    @property
    def positions(self) -> dict[str, Position]:
        return self._positions

    @property
    def total_eval(self) -> float:
        """총 평가금액 (현금 + 보유종목 평가)."""
        pos_value = sum(p.eval_amount for p in self._positions.values())
        return self._cash + pos_value

    @property
    def total_profit_rate(self) -> float:
        """총 수익률 (%)."""
        if self._initial_cash == 0:
            return 0.0
        return (self.total_eval - self._initial_cash) / self._initial_cash * 100

    def buy(self, code: str, name: str, price: int, quantity: int) -> bool:
        """매수 실행.

        Returns:
            True: 매수 성공, False: 잔고 부족
        """
        cost = price * quantity
        if cost > self._cash:
            logger.warning("매수 실패 (잔고 부족): %s %d주 @ %d (필요: %s, 잔고: %s)",
                         code, quantity, price, f"{cost:,}", f"{self._cash:,}")
            return False

        self._cash -= cost

        if code in self._positions:
            pos = self._positions[code]
            total_cost = pos.avg_price * pos.quantity + price * quantity
            pos.quantity += quantity
            pos.avg_price = total_cost / pos.quantity
        else:
            self._positions[code] = Position(
                code=code,
                name=name,
                quantity=quantity,
                avg_price=float(price),
                current_price=float(price),
                bought_at=datetime.now().isoformat(),
            )

        self._trade_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "매수",
            "code": code,
            "name": name,
            "price": price,
            "quantity": quantity,
            "amount": cost,
            "cash_after": self._cash,
        })

        logger.info("매수: %s(%s) %d주 @ %s원 (잔고: %s원)",
                    code, name, quantity, f"{price:,}", f"{self._cash:,}")
        return True

    def sell(self, code: str, price: int, quantity: int = 0) -> bool:
        """매도 실행. quantity=0이면 전량 매도.

        Returns:
            True: 매도 성공, False: 보유 없음
        """
        if code not in self._positions:
            logger.warning("매도 실패 (미보유): %s", code)
            return False

        pos = self._positions[code]
        sell_qty = quantity if quantity > 0 else pos.quantity
        sell_qty = min(sell_qty, pos.quantity)

        proceeds = price * sell_qty
        self._cash += proceeds

        profit = (price - pos.avg_price) * sell_qty
        profit_rate = (price - pos.avg_price) / pos.avg_price * 100 if pos.avg_price > 0 else 0

        self._trade_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "매도",
            "code": code,
            "name": pos.name,
            "price": price,
            "quantity": sell_qty,
            "amount": proceeds,
            "profit": profit,
            "profit_rate": profit_rate,
            "cash_after": self._cash,
        })

        pos.quantity -= sell_qty
        if pos.quantity <= 0:
            del self._positions[code]

        logger.info("매도: %s %d주 @ %s원 (손익: %s원, %.1f%%, 잔고: %s원)",
                    code, sell_qty, f"{price:,}", f"{profit:,.0f}",
                    profit_rate, f"{self._cash:,}")
        return True

    def update_prices(self, market_data_provider) -> None:
        """보유 종목의 현재가를 갱신한다."""
        for code, pos in self._positions.items():
            snapshot = market_data_provider.get_current_price(code)
            if snapshot.current_price > 0:
                pos.current_price = float(snapshot.current_price)
                if not pos.name and snapshot.name:
                    pos.name = snapshot.name

    def record_daily_value(self) -> None:
        """일별 평가금액을 기록한다 (수익률 차트용)."""
        self._daily_values.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_eval": self.total_eval,
            "cash": self._cash,
            "positions_value": sum(p.eval_amount for p in self._positions.values()),
            "profit_rate": self.total_profit_rate,
        })

    def get_portfolio_summary(self) -> dict:
        """포트폴리오 요약 반환 (UI 표시용)."""
        positions_list = []
        for pos in self._positions.values():
            positions_list.append({
                "code": pos.code,
                "name": pos.name,
                "quantity": pos.quantity,
                "avg_price": pos.avg_price,
                "current_price": pos.current_price,
                "eval_amount": pos.eval_amount,
                "profit_loss": pos.profit_loss,
                "profit_rate": pos.profit_rate,
            })

        return {
            "initial_cash": self._initial_cash,
            "cash": self._cash,
            "total_eval": self.total_eval,
            "total_profit_rate": self.total_profit_rate,
            "positions": positions_list,
            "trade_count": len(self._trade_history),
        }

    def get_trade_history(self) -> list[dict]:
        """매매 이력 반환."""
        return list(self._trade_history)

    def get_daily_values(self) -> list[dict]:
        """일별 평가금액 반환 (차트용)."""
        return list(self._daily_values)

    def get_allocation(self) -> list[dict]:
        """자산 배분 반환 (파이차트용)."""
        result = []
        total = self.total_eval
        if total <= 0:
            return result

        if self._cash > 0:
            result.append({
                "name": "현금",
                "value": self._cash,
                "ratio": self._cash / total * 100,
            })

        for pos in self._positions.values():
            if pos.eval_amount > 0:
                result.append({
                    "name": pos.name or pos.code,
                    "value": pos.eval_amount,
                    "ratio": pos.eval_amount / total * 100,
                })

        return result
