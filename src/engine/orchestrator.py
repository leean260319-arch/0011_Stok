"""자동매매 오케스트레이터 - 실시간 시세 -> 분석 -> 전략 -> 리스크 -> 주문 파이프라인"""

# v1.0 - 2026-03-17: 신규 작성
# v1.1 - 2026-03-17: C1 시그널 키 통일, H4 QThread 기반 워커로 변경

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QThread

from src.utils.logger import get_logger

logger = get_logger("engine.orchestrator")


class _TickWorker(QThread):
    """백그라운드에서 매매 파이프라인을 실행하는 워커."""

    tick_done = pyqtSignal()

    def __init__(self, orchestrator):
        super().__init__()
        self._orch = orchestrator

    def run(self):
        for stock_code in self._orch._watched_stocks:
            if not self._orch._running:
                break
            self._orch._process_stock(stock_code)
        self.tick_done.emit()


class TradingOrchestrator(QObject):
    """자동매매 파이프라인을 관리한다.

    Signals:
        signal_generated: 시그널 생성 시 (dict)
        order_executed: 주문 실행 시 (dict)
        status_changed: 상태 변경 시 (str)
        dashboard_updated: 대시보드 갱신 데이터 (dict)
    """

    signal_generated = pyqtSignal(dict)
    order_executed = pyqtSignal(dict)
    status_changed = pyqtSignal(str)
    dashboard_updated = pyqtSignal(dict)
    screening_completed = pyqtSignal(list)  # list[ScreenerResult]
    portfolio_updated = pyqtSignal(dict)  # 포트폴리오 갱신 데이터

    def __init__(self, container):
        """
        Args:
            container: ServiceContainer 인스턴스
        """
        super().__init__()
        self._container = container
        self._running = False
        self._watched_stocks = []
        self._account = ""

        # 주기적 실행 타이머 (기본 5초)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._tick_interval = 5000

    @property
    def is_running(self) -> bool:
        return self._running

    def set_watched_stocks(self, stock_codes: list[str]):
        """감시 종목 설정."""
        self._watched_stocks = list(stock_codes)
        logger.info("감시 종목 설정: %d종목", len(stock_codes))

    def set_account(self, account: str):
        """매매 계좌번호 설정."""
        self._account = account

    def set_tick_interval(self, ms: int):
        """틱 주기 설정 (밀리초)."""
        self._tick_interval = max(1000, ms)
        if self._running:
            self._timer.setInterval(self._tick_interval)

    def start(self):
        """자동매매 시작. 감시 종목이 비어있으면 AI 자동 선정."""
        if self._running:
            return
        self._running = True

        # 감시 종목이 없으면 AI 스크리닝 실행
        if not self._watched_stocks:
            self._auto_select_stocks()

        self._timer.start(self._tick_interval)
        self.status_changed.emit("running")
        logger.info("자동매매 시작: %d종목 감시", len(self._watched_stocks))

    def _auto_select_stocks(self):
        """AI 스크리너로 종목 자동 선정."""
        screener = self._container.stock_screener
        if screener is None:
            logger.warning("StockScreener 미초기화, 종목 자동선정 불가")
            return

        results = screener.screen_quick(market="ALL", max_picks=5)
        if results:
            self._watched_stocks = [r.code for r in results]
            self.screening_completed.emit(results)
            logger.info(
                "AI 종목 자동선정: %s",
                [(r.code, r.name, f"{r.total_score:.3f}") for r in results],
            )

    def stop(self):
        """자동매매 중지."""
        self._running = False
        self._timer.stop()
        self.status_changed.emit("stopped")
        logger.info("자동매매 중지")

    def emergency_stop(self):
        """긴급 정지 (킬 스위치) - 매매 중지 + RiskManager 킬 스위치 발동."""
        self.stop()
        risk_manager = self._container.risk_manager
        if risk_manager:
            risk_manager.kill_switch_on()
        self.status_changed.emit("emergency_stopped")
        logger.warning("긴급 정지 발동")

    def _tick(self):
        """주기적 실행: 각 감시 종목에 대해 백그라운드 워커로 파이프라인 실행."""
        if not self._running:
            return

        # MarketDataProvider 또는 bridge 중 하나만 있으면 실행 가능
        bridge = self._container.bridge
        market_data = self._container.market_data_provider
        if market_data is None and (bridge is None or not bridge.is_connected):
            return

        if hasattr(self, "_worker") and self._worker.isRunning():
            return  # 이전 tick이 아직 실행 중이면 건너뜀

        self._worker = _TickWorker(self)
        self._worker.tick_done.connect(self._worker.deleteLater)
        self._worker.start()

    def _process_stock(self, stock_code: str):
        """단일 종목에 대한 매매 파이프라인 실행.

        1. 시세 조회 (MarketDataProvider 우선, bridge fallback)
        2. OHLCV 데이터로 기술지표 계산
        3. 전략 앙상블 평가
        4. 리스크 검증
        5. 주문 실행
        6. 매매 기록
        """
        import pandas as pd
        from src.engine.chart_analyzer import ChartAnalyzer
        from src.engine.signal_generator import SignalGenerator

        bridge = self._container.bridge
        market_data_provider = self._container.market_data_provider
        strategy_engine = self._container.strategy_engine
        risk_manager = self._container.risk_manager
        trade_logger = self._container.trade_logger

        # 1. 시세 조회: MarketDataProvider 우선, bridge fallback
        if market_data_provider:
            snapshot = market_data_provider.get_current_price(stock_code)
            market_data = {
                "stock_code": stock_code,
                "close": snapshot.current_price,
                "open": snapshot.open_price,
                "high": snapshot.high_price,
                "low": snapshot.low_price,
                "volume": snapshot.volume,
            }
        elif bridge and bridge.is_connected:
            stock_price = bridge.get_stock_price(stock_code)
            market_data = {
                "stock_code": stock_code,
                "close": stock_price.current_price,
                "open": stock_price.open_price,
                "high": stock_price.high_price,
                "low": stock_price.low_price,
                "volume": stock_price.volume,
            }
        else:
            return

        if market_data["close"] == 0:
            logger.debug("시세 없음: %s", stock_code)
            return

        # 2. OHLCV 히스토리: MarketDataProvider 우선
        history_df = None
        if market_data_provider:
            history_df = market_data_provider.get_ohlcv_history(stock_code, days=120)
        elif bridge and hasattr(bridge, "get_price_history"):
            history = bridge.get_price_history(stock_code)
            if history is not None and len(history) >= 20:
                history_df = pd.DataFrame(history)

        if history_df is not None and len(history_df) >= 20:
            analyzer = ChartAnalyzer(history_df)

            # RSI
            rsi_series = analyzer.calc_rsi()
            rsi_clean = rsi_series.dropna()
            if len(rsi_clean) > 0:
                market_data["rsi"] = float(rsi_clean.iloc[-1])

            # MACD 크로스
            macd_df = analyzer.calc_macd()
            macd_col = [c for c in macd_df.columns if c.startswith("MACD_") and "h" not in c.lower() and "s" not in c.lower()]
            signal_col = [c for c in macd_df.columns if "MACDs_" in c]
            if macd_col and signal_col:
                valid = macd_df[[macd_col[0], signal_col[0]]].dropna()
                if len(valid) >= 2:
                    prev_m = float(valid.iloc[-2][macd_col[0]])
                    prev_s = float(valid.iloc[-2][signal_col[0]])
                    curr_m = float(valid.iloc[-1][macd_col[0]])
                    curr_s = float(valid.iloc[-1][signal_col[0]])
                    if prev_m < prev_s and curr_m >= curr_s:
                        market_data["macd_cross"] = "golden"
                    elif prev_m > prev_s and curr_m <= curr_s:
                        market_data["macd_cross"] = "dead"

            # 볼린저밴드
            bb_df = analyzer.calc_bollinger()
            lower_col = [c for c in bb_df.columns if "BBL_" in c]
            upper_col = [c for c in bb_df.columns if "BBU_" in c]
            if lower_col and upper_col:
                valid_bb = bb_df[[lower_col[0], upper_col[0]]].dropna()
                if len(valid_bb) > 0:
                    market_data["bb_lower"] = float(valid_bb.iloc[-1][lower_col[0]])
                    market_data["bb_upper"] = float(valid_bb.iloc[-1][upper_col[0]])

            # SignalGenerator 시그널
            sg = SignalGenerator(analyzer)
            signal_result = sg.generate_signal()
            market_data["signal_score"] = signal_result.get("score", 0)
            market_data["signal_reasons"] = signal_result.get("reasons", [])

        # 3. 전략 앙상블 평가 (기술지표가 주입된 market_data 사용)
        ensemble = strategy_engine.ensemble_evaluate(market_data)
        signal = ensemble.get("signal", "관망")
        confidence = ensemble.get("confidence", 0)

        signal_data = {
            "stock_code": stock_code,
            "signal": signal,
            "confidence": confidence,
            "details": ensemble,
        }
        self.signal_generated.emit(dict(signal_data))

        if signal == "관망":
            return

        # 3. 리스크 검증
        order = {
            "symbol": stock_code,
            "price": market_data["close"],
            "quantity": 1,
        }

        # bridge 연결 여부 확인 (주문 실행용)
        has_bridge = bridge and bridge.is_connected

        # 매도 수량: 보유 수량 전량
        if signal == "매도":
            if not has_bridge:
                logger.info("시뮬레이션 매도 시그널: %s (bridge 미연결)", stock_code)
                return
            balance = bridge.get_balance(self._account)
            held_qty = 0
            for h in getattr(balance, "holdings", []):
                if getattr(h, "code", "") == stock_code:
                    held_qty = getattr(h, "quantity", 0)
                    break
            order["quantity"] = held_qty
            if order["quantity"] <= 0:
                return

        # 매수 수량: 실제 승률 기반 Kelly (bridge 있을 때만 실제 잔고 사용)
        if signal == "매수":
            stats = trade_logger.get_trade_stats() if trade_logger else {}
            win_rate = stats.get("win_rate", 0.5)
            avg_win = stats.get("avg_win", 0.03)
            avg_loss = stats.get("avg_loss", 0.02)

            if has_bridge:
                balance = bridge.get_balance(self._account)
                account_balance = balance.deposit
            else:
                # bridge 없으면 시뮬레이션 잔고 사용
                account_balance = 10_000_000  # 기본 1000만원

            position_amount = risk_manager.calculate_position_size(
                account_balance=account_balance,
                win_rate=win_rate,
                avg_win=avg_win,
                avg_loss=avg_loss,
                signal_confidence=confidence,
            )
            order["quantity"] = max(1, int(position_amount / market_data["close"]))

        is_valid, reason = risk_manager.validate_order(order)
        if not is_valid:
            logger.info("주문 거부: %s - %s", stock_code, reason)
            return

        # 포트폴리오/계좌 검증 (bridge 연결 시)
        if has_bridge:
            balance = bridge.get_balance(self._account)
            portfolio = {
                "total_value": getattr(balance, "total_value", 0) or getattr(balance, "deposit", 0),
                "positions": {
                    getattr(h, "code", ""): {"value": getattr(h, "quantity", 0) * getattr(h, "current_price", 0)}
                    for h in getattr(balance, "holdings", [])
                },
            }
            is_valid, reason = risk_manager.validate_portfolio(order, portfolio)
            if not is_valid:
                logger.info("포트폴리오 검증 거부: %s - %s", stock_code, reason)
                return

            account_info = {
                "total_equity": getattr(balance, "total_value", 0) or getattr(balance, "deposit", 0),
                "available_cash": getattr(balance, "deposit", 0),
                "daily_pnl_pct": 0.0,
                "weekly_pnl_pct": 0.0,
                "monthly_pnl_pct": 0.0,
            }
            is_valid, reason = risk_manager.validate_account(order, account_info)
            if not is_valid:
                logger.info("계좌 검증 거부: %s - %s", stock_code, reason)
                return

        # 4. 주문 실행 (bridge 연결 시 실제 주문, 아니면 가상 포트폴리오)
        order_type = "buy" if signal == "매수" else "sell"
        virtual_portfolio = self._container.virtual_portfolio

        if has_bridge:
            order_result = bridge.send_order(
                account=self._account,
                code=stock_code,
                order_type=order_type,
                quantity=order["quantity"],
                price=order["price"],
            )
            order_success = order_result.success
            order_message = order_result.message
        elif virtual_portfolio:
            # 가상 포트폴리오로 시뮬레이션 매매
            stock_name = ""
            mdp = self._container.market_data_provider
            if mdp:
                snap = mdp.get_current_price(stock_code)
                stock_name = snap.name
            if signal == "매수":
                order_success = virtual_portfolio.buy(
                    stock_code, stock_name, order["price"], order["quantity"])
            else:
                order_success = virtual_portfolio.sell(
                    stock_code, order["price"], order["quantity"])
            order_message = "가상매매 완료" if order_success else "가상매매 실패"
        else:
            order_success = True
            order_message = "시뮬레이션 로그"

        self.order_executed.emit({
            "stock_code": stock_code,
            "action": signal,
            "quantity": order["quantity"],
            "price": order["price"],
            "success": order_success,
            "message": order_message,
        })

        # 5. 매매 기록
        if trade_logger and order_success:
            from datetime import datetime
            from src.engine.trade_logger import TradeRecord

            record = TradeRecord(
                timestamp=datetime.now().isoformat(),
                stock_code=stock_code,
                stock_name="",
                direction=order_type,
                price=order["price"],
                quantity=order["quantity"],
                signal_score=confidence,
                signal_detail=str(ensemble.get("details", [])),
                strategy_name="ensemble",
                confidence=confidence,
                reason=str(ensemble.get("details", [])),
            )
            trade_logger.log_trade(record)

        logger.info(
            "주문 %s: %s %s %d주 @ %d",
            "실행" if has_bridge else "시뮬레이션",
            stock_code, signal, order["quantity"], order["price"],
        )

        # 6. 가상 포트폴리오 현재가 갱신 + 시그널 발행
        if virtual_portfolio:
            mdp = self._container.market_data_provider
            if mdp:
                virtual_portfolio.update_prices(mdp)
            self.portfolio_updated.emit(virtual_portfolio.get_portfolio_summary())

        # 7. 대시보드 갱신 시그널 발행
        dashboard_data = {
            "account": {},
            "auto_trade": {
                "is_running": self._running,
                "strategy_name": "ensemble",
                "filled_count": len(virtual_portfolio.get_trade_history()) if virtual_portfolio else 0,
            },
            "last_signal": signal_data,
        }
        if virtual_portfolio:
            summary = virtual_portfolio.get_portfolio_summary()
            dashboard_data["account"] = {
                "total_balance": summary["total_eval"],
                "available_cash": summary["cash"],
                "profit_rate": summary["total_profit_rate"],
            }
        self.dashboard_updated.emit(dashboard_data)
