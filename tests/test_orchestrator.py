"""TradingOrchestrator 테스트"""

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass


@dataclass
class FakeStockPrice:
    code: str = "005930"
    current_price: int = 70000
    open_price: int = 69000
    high_price: int = 71000
    low_price: int = 68500
    volume: int = 50000


@dataclass
class FakeOrderResult:
    success: bool = True
    order_no: str = "12345"
    message: str = "OK"


@dataclass
class FakeHoldingItem:
    code: str = "005930"
    name: str = "삼성전자"
    quantity: int = 100
    avg_price: int = 65000
    current_price: int = 70000
    eval_amount: int = 7_000_000


@dataclass
class FakeBalance:
    deposit: int = 10_000_000
    holdings: list = None
    total_eval_amount: int = 10_000_000

    def __post_init__(self):
        if self.holdings is None:
            self.holdings = []


def make_mock_container():
    """모든 서비스가 Mock인 ServiceContainer 대역."""
    container = MagicMock()

    # bridge
    container.bridge.is_connected = True
    container.bridge.get_stock_price.return_value = FakeStockPrice()
    container.bridge.send_order.return_value = FakeOrderResult()
    container.bridge.get_balance.return_value = FakeBalance()

    # strategy_engine - ensemble_evaluate -> 매수 시그널
    container.strategy_engine.ensemble_evaluate.return_value = {
        "signal": "매수",
        "confidence": 0.7,
        "agreement": 0.8,
        "details": [{"strategy": "momentum", "signal": "매수", "confidence": 0.7}],
    }

    # risk_manager
    container.risk_manager.validate_order.return_value = (True, "")
    container.risk_manager.calculate_position_size.return_value = 700_000

    # trade_logger
    container.trade_logger.log_trade.return_value = 1

    return container


class TestOrchestratorLifecycle:
    """오케스트레이터 생명주기 테스트."""

    def test_initial_state_stopped(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        assert orch.is_running is False

    def test_start_changes_state(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        signals = []
        orch.status_changed.connect(signals.append)

        orch.start()
        assert orch.is_running is True
        assert "running" in signals

        orch.stop()

    def test_stop_changes_state(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        orch.start()

        signals = []
        orch.status_changed.connect(signals.append)

        orch.stop()
        assert orch.is_running is False
        assert "stopped" in signals

    def test_double_start_ignored(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        orch.start()
        orch.start()  # 두 번째 호출은 무시
        assert orch.is_running is True
        orch.stop()

    def test_emergency_stop(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        orch = TradingOrchestrator(container)
        orch.start()

        signals = []
        orch.status_changed.connect(signals.append)

        orch.emergency_stop()
        assert orch.is_running is False
        assert "emergency_stopped" in signals
        container.risk_manager.kill_switch_on.assert_called_once()


class TestOrchestratorConfig:
    """오케스트레이터 설정 테스트."""

    def test_set_watched_stocks(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        orch.set_watched_stocks(["005930", "000660"])
        assert orch._watched_stocks == ["005930", "000660"]

    def test_set_account(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        orch.set_account("1234567890")
        assert orch._account == "1234567890"

    def test_set_tick_interval_minimum(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        orch = TradingOrchestrator(make_mock_container())
        orch.set_tick_interval(500)
        assert orch._tick_interval == 1000  # 최소 1초


class TestOrchestratorPipeline:
    """매매 파이프라인 테스트."""

    def test_tick_skips_when_not_running(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        orch = TradingOrchestrator(container)
        orch.set_watched_stocks(["005930"])

        orch._tick()
        container.bridge.get_stock_price.assert_not_called()

    def test_tick_skips_when_bridge_disconnected(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        container.bridge.is_connected = False
        orch = TradingOrchestrator(container)
        orch._running = True
        orch.set_watched_stocks(["005930"])

        orch._tick()
        container.bridge.get_stock_price.assert_not_called()

    def test_process_stock_buy_signal(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        orch = TradingOrchestrator(container)
        orch.set_account("ACC001")

        signal_results = []
        order_results = []
        orch.signal_generated.connect(signal_results.append)
        orch.order_executed.connect(order_results.append)

        orch._process_stock("005930")

        # 시그널 생성 확인
        assert len(signal_results) == 1
        assert signal_results[0]["signal"] == "매수"

        # 주문 실행 확인
        assert len(order_results) == 1
        assert order_results[0]["action"] == "매수"
        assert order_results[0]["success"] is True

        # trade_logger 호출 확인
        container.trade_logger.log_trade.assert_called_once()

    def test_process_stock_hold_signal_no_order(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        container.strategy_engine.ensemble_evaluate.return_value = {
            "signal": "관망",
            "confidence": 0.3,
            "agreement": 0.5,
            "details": [],
        }
        orch = TradingOrchestrator(container)

        order_results = []
        orch.order_executed.connect(order_results.append)

        orch._process_stock("005930")

        # 관망이면 주문 실행 안 함
        assert len(order_results) == 0
        container.bridge.send_order.assert_not_called()

    def test_process_stock_risk_rejection(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        container.risk_manager.validate_order.return_value = (False, "킬 스위치 발동 중")
        orch = TradingOrchestrator(container)
        orch.set_account("ACC001")

        order_results = []
        orch.order_executed.connect(order_results.append)

        orch._process_stock("005930")

        # 리스크 거부 시 주문 실행 안 함
        assert len(order_results) == 0
        container.bridge.send_order.assert_not_called()

    def test_process_stock_sell_signal(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        container.strategy_engine.ensemble_evaluate.return_value = {
            "signal": "매도",
            "confidence": 0.6,
            "agreement": 0.7,
            "details": [],
        }
        # 매도 시 보유 종목이 있어야 매도 진행
        container.bridge.get_balance.return_value = FakeBalance(
            holdings=[FakeHoldingItem(code="005930", quantity=100)]
        )
        orch = TradingOrchestrator(container)
        orch.set_account("ACC001")

        order_results = []
        orch.order_executed.connect(order_results.append)

        orch._process_stock("005930")

        assert len(order_results) == 1
        assert order_results[0]["action"] == "매도"
        assert order_results[0]["quantity"] == 100
        # 매도 시 포지션 사이징 미호출
        container.risk_manager.calculate_position_size.assert_not_called()

    def test_process_stock_order_failure_no_log(self, qapp):
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        container.bridge.send_order.return_value = FakeOrderResult(
            success=False, order_no="", message="주문 실패"
        )
        orch = TradingOrchestrator(container)
        orch.set_account("ACC001")

        orch._process_stock("005930")

        # 주문 실패 시 trade_logger 호출 안 함
        container.trade_logger.log_trade.assert_not_called()

    def test_full_tick_cycle(self, qapp):
        """start -> tick -> stop 전체 사이클 테스트."""
        from src.engine.orchestrator import TradingOrchestrator

        container = make_mock_container()
        orch = TradingOrchestrator(container)
        orch.set_watched_stocks(["005930", "000660"])
        orch.set_account("ACC001")

        orch._running = True
        orch._tick()

        # QThread 워커 완료 대기
        if hasattr(orch, "_worker") and orch._worker is not None:
            orch._worker.wait()

        # 2종목 각각 시세 조회
        assert container.bridge.get_stock_price.call_count == 2
