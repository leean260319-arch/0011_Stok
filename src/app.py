"""T012/T016: 메인 윈도우 프레임 및 시스템 트레이 아이콘"""

# 버전 정보
# v1.0 - 2026-03-16: 신규 작성
# v1.1 - 2026-03-17: 뷰 통합 (QStackedWidget, LeftPanel, RightPanel, 설정 다이얼로그, dark_theme)
# v1.2 - 2026-03-17: 폰트 크기/UI 스케일 조절 기능 추가 (DisplaySettingsView, 줌 단축키)
# v1.3 - 2026-03-17: ServiceContainer + TradingOrchestrator 주입, 자동매매 토글 연동
# v1.4 - 2026-03-17: 모의/실전 투자 모드 인디케이터 (상태바 뱃지, 윈도우 타이틀, 트레이 툴팁)

from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QSplitter,
    QStackedWidget,
    QApplication,
    QSystemTrayIcon,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction

from src.ui.panels.left_panel import LeftPanel
from src.ui.panels.right_panel import RightPanel
from src.ui.dashboard import DashboardView
from src.ui.chart_view import ChartView
from src.ui.news_view import NewsView
from src.ui.trade_view import StrategyList, TradeLog
from src.ui.portfolio_view import PortfolioView
from src.ui.watchlist_view import WatchlistView
from src.ui.backtest_view import BacktestView
from src.ui.alert_view import AlertView
from src.ui.settings_view import SettingsView
from src.ui.ai_settings_view import AISettingsView
from src.ui.trade_settings_view import TradeSettingsView
from src.ui.web_settings_view import WebSettingsView
from src.ui.display_settings_view import DisplaySettingsView
from src.ui.themes.dark_theme import load_dark_theme
from src.utils.constants import APP_NAME, Colors
from src.utils.logger import get_logger

logger = get_logger("app")

# 하위 호환용 (기존 코드에서 DARK_THEME_QSS를 참조하는 경우)
DARK_THEME_QSS = load_dark_theme()

# 뷰 키 -> 인덱스 매핑용
_VIEW_KEYS = [
    "dashboard",
    "chart",
    "news",
    "trade",
    "portfolio",
    "watchlist",
    "backtest",
    "alert",
]


class SettingsDialog(QDialog):
    """설정 다이얼로그 - 계정/AI/매매 설정을 탭으로 묶는다."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("설정")
        self.resize(600, 500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()

        self.settings_view = SettingsView()
        self.tab_widget.addTab(self.settings_view, "계정 설정")

        self.ai_settings_view = AISettingsView()
        self.tab_widget.addTab(self.ai_settings_view, "AI 설정")

        self.trade_settings_view = TradeSettingsView()
        self.tab_widget.addTab(self.trade_settings_view, "매매 설정")

        self.web_settings_view = WebSettingsView()
        self.tab_widget.addTab(self.web_settings_view, "웹 대시보드")

        self.display_settings_view = DisplaySettingsView()
        self.tab_widget.addTab(self.display_settings_view, "화면 설정")

        layout.addWidget(self.tab_widget)


class MainWindow(QMainWindow):
    """메인 윈도우 - 3-Panel QSplitter 레이아웃, 메뉴바, 상태바."""

    def __init__(self, parent=None, container=None, orchestrator=None) -> None:
        super().__init__(parent)
        self._container = container
        self._orchestrator = orchestrator
        self._left_panel_width = 250
        self._current_font_size = 12
        self._right_panel_width = 300
        self._is_live_mode = False
        self._setup_views()
        self._setup_ui()
        self._setup_menubar()
        self._setup_statusbar()
        self._apply_theme()
        self._connect_orchestrator_signals()
        self._update_mode_indicator()
        logger.info("MainWindow 초기화 완료")

    # ------------------------------------------------------------------
    # Orchestrator 시그널 연결
    # ------------------------------------------------------------------

    def _connect_orchestrator_signals(self) -> None:
        """Orchestrator 시그널을 UI 슬롯에 연결한다."""
        if self._orchestrator:
            self._orchestrator.signal_generated.connect(self._on_signal_generated)
            self._orchestrator.order_executed.connect(self._on_order_executed)
            self._orchestrator.status_changed.connect(self._on_status_changed)
            self._orchestrator.dashboard_updated.connect(self._on_dashboard_updated)
        # 백테스트 실행 버튼 연결
        self.backtest_view.run_clicked.connect(self._on_backtest_run)

        # 자동매매 제어 연결
        self.right_panel.autotrade_requested.connect(self._on_autotrade_requested)
        self.right_panel.stocks_changed.connect(self._on_stocks_changed)

    def _on_signal_generated(self, data: dict):
        """시그널 생성 시 AI 시그널 카드 및 AI 상태 인디케이터 갱신."""
        signal = data.get("signal", "관망")
        confidence = data.get("confidence", 0.0)
        details = data.get("details", {})
        reasoning = str(details.get("details", "")) if isinstance(details, dict) else str(details)

        # 시그널 타입을 영문 키로 변환
        signal_map = {"매수": "buy", "매도": "sell", "관망": "hold"}
        signal_type = signal_map.get(signal, "hold")

        self.right_panel.ai_signal_card.set_signal(signal_type, confidence, reasoning)
        self.right_panel.ai_status.set_status("complete")

        logger.info(
            "시그널: %s %s (신뢰도: %.2f)",
            data.get("stock_code"), signal, confidence,
        )

    def _on_order_executed(self, data: dict):
        """주문 실행 시 거래 로그 위젯에 행 추가."""
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.trade_log.add_log(
            timestamp=timestamp,
            event_type=data.get("action", ""),
            stock=data.get("stock_code", ""),
            price=data.get("price", 0),
            quantity=data.get("quantity", 0),
        )

        logger.info(
            "주문 실행: %s %s %d주 @ %d",
            data.get("stock_code"), data.get("action"),
            data.get("quantity", 0), data.get("price", 0),
        )

    def _on_status_changed(self, status: str):
        """자동매매 상태 변경 시 상태바 및 AI 상태 인디케이터 갱신."""
        status_text_map = {
            "running": "연결: 자동매매 실행 중",
            "stopped": "연결: 대기중",
            "emergency_stopped": "연결: 긴급 정지",
        }
        self._status_connection.setText(status_text_map.get(status, f"연결: {status}"))

        ai_status_map = {
            "running": "processing",
            "stopped": "idle",
            "emergency_stopped": "error",
        }
        self.right_panel.ai_status.set_status(ai_status_map.get(status, "idle"))

        logger.info("자동매매 상태: %s", status)

    def _on_dashboard_updated(self, data: dict):
        """대시보드 갱신 데이터로 각 위젯을 업데이트한다."""
        account = data.get("account", {})
        if account:
            self.dashboard_view._account_summary.set_data(
                total_asset=account.get("total_asset", 0),
                profit_rate=account.get("profit_rate", 0.0),
                deposit=account.get("deposit", 0),
            )
            self.dashboard_view._daily_pnl.set_data(
                realized=account.get("daily_realized", 0),
                unrealized=account.get("daily_unrealized", 0),
                rate=account.get("profit_rate", 0.0),
            )

        auto_trade = data.get("auto_trade", {})
        if auto_trade:
            self.dashboard_view._auto_trade_status.set_status(
                strategy_name=auto_trade.get("strategy_name", "-"),
                filled_count=auto_trade.get("filled_count", 0),
                is_running=auto_trade.get("is_running", False),
            )

    def _on_autotrade_requested(self, start: bool):
        """자동매매 시작/중지 요청 처리."""
        if not self._orchestrator:
            return
        if start:
            # 종목 설정 (비어있으면 AI 자동 선정)
            text = self.right_panel.stock_input.text().strip()
            codes = [c.strip() for c in text.split(",") if c.strip()]
            if codes:
                self._orchestrator.set_watched_stocks(codes)
            # else: orchestrator.start()에서 AI 자동 선정

            # 계좌 설정 (keyring에서 로드)
            from src.security.credential_manager import CredentialManager
            cm = CredentialManager()
            account = cm.get("account_number") or ""
            self._orchestrator.set_account(account)
            self._orchestrator.start()

            # 종목이 비었고 AI 선정 결과가 있으면 UI에 반영
            if not codes and self._orchestrator._watched_stocks:
                selected = ", ".join(self._orchestrator._watched_stocks)
                self.right_panel.stock_input.setText(selected)
        else:
            self._orchestrator.stop()

    def _on_portfolio_updated(self, summary: dict):
        """가상 포트폴리오 갱신 시 UI 반영."""
        # 테이블 초기화 후 재작성
        self.portfolio_view._table.setRowCount(0)
        for pos in summary.get("positions", []):
            self.portfolio_view.add_stock(
                name=pos.get("name", pos.get("code", "")),
                qty=pos.get("quantity", 0),
                avg_price=int(pos.get("avg_price", 0)),
                current_price=int(pos.get("current_price", 0)),
            )

        # 비중 파이차트 갱신
        vp = self._container.virtual_portfolio if self._container else None
        if vp:
            allocation = vp.get_allocation()
            self.portfolio_view._allocation_chart.set_data(allocation)

    def _on_screening_completed(self, results):
        """AI 종목 스크리닝 완료 시 UI 반영."""
        if not results:
            return
        # 종목 입력란에 선정된 종목 코드 표시
        codes = [r.code for r in results]
        self.right_panel.stock_input.setText(", ".join(codes))
        # AI 시그널 카드에 최상위 종목 표시
        top = results[0]
        self.right_panel.ai_signal_card.update_signal({
            "stock_code": top.code,
            "signal": top.signal,
            "confidence": abs(top.total_score),
            "details": {"reasons": top.reasons[:3], "name": top.name},
        })
        logger.info("AI 스크리닝 결과 UI 반영: %d종목", len(results))

    def _on_stocks_changed(self, codes: list):
        """감시 종목 변경."""
        if self._orchestrator:
            self._orchestrator.set_watched_stocks(codes)

    def _on_backtest_run(self):
        """백테스트 실행 버튼 클릭 처리."""
        logger.info("백테스트 실행 요청")

    # ------------------------------------------------------------------
    # 뷰 생성
    # ------------------------------------------------------------------

    def _setup_views(self) -> None:
        """center panel에 표시할 뷰 위젯들을 생성한다."""
        self.dashboard_view = DashboardView()
        self.chart_view = ChartView()
        self.news_view = NewsView()

        # 자동매매 뷰: 전략 목록 + 거래 로그 조합
        self.trade_view = QWidget()
        trade_layout = QVBoxLayout(self.trade_view)
        trade_layout.setContentsMargins(0, 0, 0, 0)
        self.strategy_list = StrategyList()
        self.trade_log = TradeLog()
        trade_layout.addWidget(self.strategy_list)
        trade_layout.addWidget(self.trade_log)

        self.portfolio_view = PortfolioView()
        self.watchlist_view = WatchlistView()
        self.backtest_view = BacktestView()
        self.alert_view = AlertView()

    # ------------------------------------------------------------------
    # UI 설정
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        """3-Panel QSplitter 레이아웃을 설정한다."""
        self.setWindowTitle(f"{APP_NAME} - AI 주식 자동매매")
        self.resize(1280, 800)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # 왼쪽 패널: 네비게이션
        self.left_panel = LeftPanel()
        self.left_panel.setObjectName("left_panel")
        self.left_panel.setMinimumWidth(0)
        self.left_panel.nav_clicked.connect(self._on_nav_clicked)

        # 중앙 패널: QStackedWidget
        self.center_panel = QWidget()
        self.center_panel.setObjectName("center_panel")
        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self.view_stack = QStackedWidget()
        self.view_stack.addWidget(self.dashboard_view)   # 0: dashboard
        self.view_stack.addWidget(self.chart_view)        # 1: chart
        self.view_stack.addWidget(self.news_view)         # 2: news
        self.view_stack.addWidget(self.trade_view)        # 3: trade
        self.view_stack.addWidget(self.portfolio_view)    # 4: portfolio
        self.view_stack.addWidget(self.watchlist_view)    # 5: watchlist
        self.view_stack.addWidget(self.backtest_view)     # 6: backtest
        self.view_stack.addWidget(self.alert_view)        # 7: alert
        center_layout.addWidget(self.view_stack)

        # 오른쪽 패널: 킬스위치, AI 시그널
        self.right_panel = RightPanel()
        self.right_panel.setObjectName("right_panel")
        self.right_panel.setMinimumWidth(0)

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.center_panel)
        self.splitter.addWidget(self.right_panel)

        self.splitter.setSizes(
            [self._left_panel_width, 730, self._right_panel_width]
        )

        layout.addWidget(self.splitter)

    def _on_nav_clicked(self, key: str) -> None:
        """네비게이션 클릭 시 center panel 뷰를 전환한다."""
        if key in _VIEW_KEYS:
            idx = _VIEW_KEYS.index(key)
            self.view_stack.setCurrentIndex(idx)

    def switch_view(self, key: str) -> None:
        """프로그래밍 방식으로 뷰를 전환한다."""
        self._on_nav_clicked(key)
        self.left_panel.select(key)

    def _setup_menubar(self) -> None:
        """메뉴바: 파일/보기/도구/도움말 메뉴를 생성한다."""
        mb = self.menuBar()

        file_menu = mb.addMenu("파일(&F)")
        file_menu.addAction("종료(&Q)").triggered.connect(QApplication.quit)

        view_menu = mb.addMenu("보기(&V)")
        act_left = QAction("왼쪽 패널 토글", self)
        act_left.triggered.connect(self.toggle_left_panel)
        view_menu.addAction(act_left)

        act_right = QAction("오른쪽 패널 토글", self)
        act_right.triggered.connect(self.toggle_right_panel)
        view_menu.addAction(act_right)

        view_menu.addSeparator()

        act_zoom_in = QAction("글꼴 확대", self)
        act_zoom_in.setShortcut("Ctrl+=")
        act_zoom_in.triggered.connect(self._zoom_in)
        view_menu.addAction(act_zoom_in)

        act_zoom_out = QAction("글꼴 축소", self)
        act_zoom_out.setShortcut("Ctrl+-")
        act_zoom_out.triggered.connect(self._zoom_out)
        view_menu.addAction(act_zoom_out)

        act_zoom_reset = QAction("글꼴 기본 크기", self)
        act_zoom_reset.setShortcut("Ctrl+0")
        act_zoom_reset.triggered.connect(self._zoom_reset)
        view_menu.addAction(act_zoom_reset)

        tools_menu = mb.addMenu("도구(&T)")
        act_settings = QAction("설정", self)
        act_settings.triggered.connect(self._open_settings)
        tools_menu.addAction(act_settings)

        help_menu = mb.addMenu("도움말(&H)")
        act_about = QAction("정보", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)

    def _show_about(self) -> None:
        """정보 다이얼로그를 표시한다."""
        from PyQt6.QtWidgets import QMessageBox
        from src.utils.constants import APP_VERSION
        QMessageBox.about(
            self, f"{APP_NAME} 정보",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "AI 기반 주식 자동매매 시스템\n"
            "PyQt6 + gRPC + OpenAI"
        )

    def _open_settings(self) -> None:
        """설정 다이얼로그를 연다."""
        logger.info("설정 다이얼로그 열기 시작")
        dialog = SettingsDialog(self)
        logger.info("설정 다이얼로그 생성 완료")
        current_size = getattr(self, "_current_font_size", 12)
        dialog.display_settings_view.set_font_size(current_size)
        dialog.display_settings_view.settings_changed.connect(
            lambda: self._on_display_settings_changed(dialog.display_settings_view)
        )
        # 현재 모드 상태를 다이얼로그에 동기화 후 시그널 연결
        dialog.settings_view.mode_toggle.blockSignals(True)
        dialog.settings_view.mode_toggle.set_checked(self._is_live_mode)
        if self._is_live_mode:
            dialog.settings_view._mode_label.setText("실전투자")
        dialog.settings_view.mode_toggle.blockSignals(False)
        # mode_changed: 비밀번호 검증 통과 후에만 발생하는 시그널
        dialog.settings_view.mode_changed.connect(
            lambda checked: self.set_trading_mode(checked)
        )
        # 저장된 자격증명 로드
        dialog.settings_view.load_credentials()

        # 서비스 연결
        if self._container:
            if self._container.bridge:
                dialog.settings_view.set_bridge(self._container.bridge)
            if self._container.config:
                dialog.ai_settings_view.set_config(self._container.config)
                dialog.trade_settings_view.set_config(self._container.config)
                dialog.web_settings_view.set_config(self._container.config)
            if self._container.risk_manager:
                dialog.trade_settings_view.set_risk_manager(self._container.risk_manager)

        # 연결 테스트 성공 시 상태바 "연결: 연결됨" 갱신
        def _on_connection_status(message: str, step: int) -> None:
            if step == 6:
                self._status_connection.setText("연결: 연결됨")

        dialog.settings_view.connection_status_changed.connect(_on_connection_status)

        dialog.exec()
        logger.info("설정 다이얼로그 닫힘")

    def _on_display_settings_changed(self, display_view) -> None:
        """화면 설정이 변경되었을 때 즉시 적용한다."""
        font_size = display_view.get_font_size()
        ui_scale = display_view.get_ui_scale()
        self._current_font_size = font_size
        self._apply_font_size(font_size)
        # UI 스케일은 앱 재시작 필요
        if ui_scale != 100:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self, "UI 스케일",
                f"UI 스케일 {ui_scale}%는 프로그램 재시작 후 적용됩니다."
            )
        logger.info(f"화면 설정 변경: font={font_size}px, scale={ui_scale}%")

    def _setup_statusbar(self) -> None:
        """상태바: 모드뱃지, 연결상태, AI 분석 진행률, 시장 상태, 시간을 표시한다."""
        sb = self.statusBar()

        # 모드 인디케이터 뱃지
        self._mode_badge = QLabel("모의투자")
        self._mode_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._mode_badge.setFixedWidth(80)
        sb.addWidget(self._mode_badge)
        sb.addWidget(QLabel("|"))

        self._status_connection = QLabel("연결: 대기중")
        self._status_ai = QLabel("AI: 준비")
        self._status_market = QLabel("시장: 폐장")
        self._status_web = QLabel("")
        self._status_time = QLabel("")

        sb.addWidget(self._status_connection)
        sb.addWidget(QLabel("|"))
        sb.addWidget(self._status_ai)
        sb.addWidget(QLabel("|"))
        sb.addWidget(self._status_market)
        sb.addWidget(QLabel("|"))
        sb.addWidget(self._status_web)
        sb.addPermanentWidget(self._status_time)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_time)
        self._timer.start(1000)
        self._update_time()

    def _update_time(self) -> None:
        """상태바 시간 + 시장 상태를 갱신한다."""
        from datetime import datetime
        now = datetime.now()
        self._status_time.setText(now.strftime("%Y-%m-%d %H:%M:%S"))

        # 시장 상태 갱신 (KRX: 평일 09:00~15:30)
        weekday = now.weekday()  # 0=월 ~ 6=일
        current_minutes = now.hour * 60 + now.minute
        market_open = 9 * 60       # 09:00
        market_close = 15 * 60 + 30  # 15:30

        if weekday >= 5:
            self._status_market.setText("시장: 휴장 (주말)")
            self._status_market.setStyleSheet("color: #888888;")
        elif market_open <= current_minutes < market_close:
            remaining = market_close - current_minutes
            h, m = divmod(remaining, 60)
            self._status_market.setText(f"시장: 개장 (마감 {h}시간 {m}분 전)")
            self._status_market.setStyleSheet("color: #00E676;")
        elif current_minutes < market_open:
            remaining = market_open - current_minutes
            h, m = divmod(remaining, 60)
            self._status_market.setText(f"시장: 장전 (개장 {h}시간 {m}분 전)")
            self._status_market.setStyleSheet("color: #FFA726;")
        else:
            self._status_market.setText("시장: 폐장")
            self._status_market.setStyleSheet("color: #888888;")

    def set_trading_mode(self, is_live: bool) -> None:
        """투자 모드를 변경하고 UI에 반영한다."""
        self._is_live_mode = is_live
        self._update_mode_indicator()
        if hasattr(self, "tray") and self.tray is not None:
            self.tray.update_trading_mode(is_live)

    def _update_mode_indicator(self) -> None:
        """모드 뱃지, 윈도우 타이틀을 현재 모드에 맞게 갱신한다."""
        if self._is_live_mode:
            self._mode_badge.setText("실전투자")
            self._mode_badge.setStyleSheet(
                "background-color: #F04451; color: #FFFFFF; "
                "font-weight: bold; border-radius: 4px; padding: 2px 6px;"
            )
            self.setWindowTitle(f"[실전] {APP_NAME} - AI 주식 자동매매")
        else:
            self._mode_badge.setText("모의투자")
            self._mode_badge.setStyleSheet(
                "background-color: #326AFF; color: #FFFFFF; "
                "font-weight: bold; border-radius: 4px; padding: 2px 6px;"
            )
            self.setWindowTitle(f"[모의] {APP_NAME} - AI 주식 자동매매")

    def set_web_url(self, url: str) -> None:
        """상태바에 웹 대시보드 URL을 표시한다."""
        self._status_web.setText(f"Web: {url}")

    def _apply_theme(self, font_size: int = 12) -> None:
        """다크 테마 QSS를 적용한다."""
        self.setStyleSheet(load_dark_theme(font_size))

    # ------------------------------------------------------------------
    # 패널 토글
    # ------------------------------------------------------------------

    def toggle_left_panel(self) -> None:
        """왼쪽 패널 접기/펼치기."""
        sizes = self.splitter.sizes()
        if sizes[0] > 0:
            self._left_panel_width = sizes[0]
            self.splitter.setSizes([0, sizes[1] + sizes[0], sizes[2]])
        else:
            restore = self._left_panel_width or 250
            total = sizes[1]
            self.splitter.setSizes([restore, total - restore, sizes[2]])

    def toggle_right_panel(self) -> None:
        """오른쪽 패널 접기/펼치기."""
        sizes = self.splitter.sizes()
        if sizes[2] > 0:
            self._right_panel_width = sizes[2]
            self.splitter.setSizes([sizes[0], sizes[1] + sizes[2], 0])
        else:
            restore = self._right_panel_width or 300
            total = sizes[1]
            self.splitter.setSizes([sizes[0], total - restore, restore])

    # ------------------------------------------------------------------
    # 폰트 크기 조절
    # ------------------------------------------------------------------

    def _zoom_in(self) -> None:
        """폰트 크기를 1px 증가한다."""
        self._current_font_size = getattr(self, "_current_font_size", 12)
        if self._current_font_size < 24:
            self._current_font_size += 1
            self._apply_font_size(self._current_font_size)

    def _zoom_out(self) -> None:
        """폰트 크기를 1px 감소한다."""
        self._current_font_size = getattr(self, "_current_font_size", 12)
        if self._current_font_size > 8:
            self._current_font_size -= 1
            self._apply_font_size(self._current_font_size)

    def _zoom_reset(self) -> None:
        """폰트 크기를 기본값(12px)으로 복원한다."""
        self._current_font_size = 12
        self._apply_font_size(12)

    def _apply_font_size(self, size: int) -> None:
        """폰트 크기를 변경하고 테마를 재적용한다."""
        from PyQt6.QtGui import QFont
        font = QFont("Malgun Gothic", size)
        QApplication.instance().setFont(font)
        self._apply_theme(size)
        self.statusBar().showMessage(f"글꼴 크기: {size}px", 2000)

    # ------------------------------------------------------------------
    # 창 이벤트
    # ------------------------------------------------------------------

    def changeEvent(self, event) -> None:
        """최소화 시 트레이로 이동."""
        from PyQt6.QtCore import QEvent
        if event.type() == QEvent.Type.WindowStateChange:
            if self.isMinimized() and hasattr(self, "tray") and self.tray is not None:
                self.hide()
        super().changeEvent(event)

    def closeEvent(self, event) -> None:
        """X 버튼 클릭 시 트레이로 최소화. 트레이가 없으면 종료."""
        if hasattr(self, "tray") and self.tray is not None and self.tray.isVisible():
            event.ignore()
            self.hide()
            self.tray.show_notification("StokAI", "시스템 트레이에서 실행 중입니다.")
        else:
            self._confirm_quit(event)

    def _confirm_quit(self, event=None) -> None:
        """종료 전 자동매매 상태를 확인하고 확인 대화상자를 표시한다."""
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("StokAI 종료")
        msg.setText("프로그램을 종료하시겠습니까?")
        msg.setInformativeText("자동매매가 실행 중이면 모든 매매가 중단됩니다.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            if hasattr(self, "web_server"):
                self.web_server.stop()
            if hasattr(self, "_timer"):
                self._timer.stop()
            if hasattr(self, "tray") and self.tray is not None:
                if hasattr(self.tray, "_tooltip_timer"):
                    self.tray._tooltip_timer.stop()
            QApplication.quit()
        elif event is not None:
            event.ignore()

    def set_tray_web_url(self, url: str) -> None:
        """트레이 아이콘에 웹 대시보드 URL을 전달한다."""
        if hasattr(self, "tray") and self.tray is not None:
            self.tray.update_web_url(url)


class SystemTray(QSystemTrayIcon):
    """시스템 트레이 아이콘 - 백그라운드 실행, 상태 모니터링, 빠른 제어."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._main_window = parent
        self._autotrade_running = False
        self._kill_switch_active = False
        self._is_live_mode = False
        self._setup_icon()
        self._setup_menu()
        self.activated.connect(self._on_activated)
        # 툴팁 업데이트 타이머 (10초 주기)
        self._tooltip_timer = QTimer(self)
        self._tooltip_timer.timeout.connect(self._update_tooltip)
        self._tooltip_timer.start(10000)
        self._update_tooltip()

    def _setup_icon(self) -> None:
        """트레이 아이콘을 설정한다."""
        import os
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "stokai.ico")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            icon = QIcon.fromTheme("application-x-executable")
            if icon.isNull():
                icon = QApplication.style().standardIcon(
                    QApplication.style().StandardPixmap.SP_ComputerIcon
                )
        self.setIcon(icon)
        self.setToolTip(APP_NAME)

    def _setup_menu(self) -> None:
        """우클릭 컨텍스트 메뉴를 설정한다."""
        menu = QMenu()

        # -- 상태 표시 (비활성, 정보용) --
        self._act_status = QAction("StokAI - 실행 중", menu)
        self._act_status.setEnabled(False)
        menu.addAction(self._act_status)

        self._act_pnl = QAction("손익: --", menu)
        self._act_pnl.setEnabled(False)
        menu.addAction(self._act_pnl)

        menu.addSeparator()

        # -- 창 제어 --
        self._act_show = QAction("창 열기", menu)
        self._act_show.triggered.connect(self._show_window)
        menu.addAction(self._act_show)

        menu.addSeparator()

        # -- 자동매매 제어 --
        self._act_autotrade = QAction("자동매매: 정지", menu)
        self._act_autotrade.triggered.connect(self._toggle_autotrade)
        menu.addAction(self._act_autotrade)

        self._act_kill = QAction("킬 스위치 발동", menu)
        self._act_kill.triggered.connect(self._toggle_kill_switch)
        menu.addAction(self._act_kill)

        menu.addSeparator()

        # -- 웹 대시보드 --
        self._act_web = QAction("웹 대시보드 열기", menu)
        self._act_web.triggered.connect(self._open_web_dashboard)
        menu.addAction(self._act_web)

        menu.addSeparator()

        # -- 설정 / 종료 --
        act_settings = QAction("설정", menu)
        act_settings.triggered.connect(self._open_settings)
        menu.addAction(act_settings)

        act_quit = QAction("프로그램 종료", menu)
        act_quit.triggered.connect(self._quit_app)
        menu.addAction(act_quit)

        self.setContextMenu(menu)

    # -- 상태 업데이트 --

    def _update_tooltip(self) -> None:
        """트레이 아이콘 툴팁을 현재 상태로 갱신한다."""
        lines = [APP_NAME]
        mode_text = "실전투자" if self._is_live_mode else "모의투자"
        lines.append(f"모드: {mode_text}")
        if self._main_window and hasattr(self._main_window, "_status_connection"):
            lines.append(self._main_window._status_connection.text())
        if self._main_window and hasattr(self._main_window, "_status_market"):
            lines.append(self._main_window._status_market.text())
        self.setToolTip("\n".join(lines))

    def update_trading_mode(self, is_live: bool) -> None:
        """투자 모드 변경을 트레이에 반영한다."""
        self._is_live_mode = is_live
        self._update_tooltip()

    def update_autotrade_status(self, running: bool, strategy: str = "") -> None:
        """자동매매 상태를 트레이 메뉴에 반영한다."""
        self._autotrade_running = running
        if running:
            self._act_autotrade.setText(f"자동매매 중지 ({strategy})")
            self._act_status.setText("StokAI - 자동매매 실행 중")
        else:
            self._act_autotrade.setText("자동매매: 정지")
            self._act_status.setText("StokAI - 대기 중")

    def update_kill_switch_status(self, active: bool) -> None:
        """킬 스위치 상태를 트레이 메뉴에 반영한다."""
        self._kill_switch_active = active
        if active:
            self._act_kill.setText("킬 스위치 해제")
        else:
            self._act_kill.setText("킬 스위치 발동")

    def update_pnl(self, pnl_text: str) -> None:
        """손익 정보를 트레이 메뉴에 반영한다."""
        self._act_pnl.setText(f"손익: {pnl_text}")

    def update_web_url(self, url: str) -> None:
        """웹 대시보드 URL을 저장한다."""
        self._web_url = url
        self._act_web.setText(f"웹 대시보드: {url}")

    # -- 알림 --

    def show_notification(self, title: str, message: str, icon_type=None) -> None:
        """시스템 트레이 팝업 알림을 표시한다."""
        if icon_type is None:
            icon_type = QSystemTrayIcon.MessageIcon.Information
        if self.supportsMessages():
            self.showMessage(title, message, icon_type, 3000)

    def notify_trade(self, stock_name: str, action: str, price: int, qty: int) -> None:
        """매매 체결 알림."""
        self.show_notification(
            f"매매 체결: {action}",
            f"{stock_name} {qty}주 @ {price:,}원"
        )

    def notify_kill_switch(self, active: bool) -> None:
        """킬 스위치 상태 변경 알림."""
        if active:
            self.show_notification(
                "킬 스위치 발동",
                "모든 자동매매가 즉시 중단되었습니다.",
                QSystemTrayIcon.MessageIcon.Warning
            )
        else:
            self.show_notification("킬 스위치 해제", "자동매매를 재개할 수 있습니다.")

    def notify_error(self, message: str) -> None:
        """오류 알림."""
        self.show_notification(
            "오류 발생", message,
            QSystemTrayIcon.MessageIcon.Critical
        )

    # -- 액션 핸들러 --

    def _show_window(self) -> None:
        """메인 윈도우를 표시한다."""
        if self._main_window is None:
            return
        self._main_window.show()
        self._main_window.showNormal()
        self._main_window.raise_()
        self._main_window.activateWindow()

    def _toggle_autotrade(self) -> None:
        """자동매매 시작/중지를 토글한다."""
        if self._main_window is None:
            return
        orchestrator = getattr(self._main_window, "_orchestrator", None)
        if orchestrator is not None:
            if orchestrator.is_running:
                orchestrator.stop()
                self._autotrade_running = False
                self.update_autotrade_status(False)
                self.show_notification("자동매매 중지", "자동매매가 중지되었습니다.")
            else:
                orchestrator.start()
                self._autotrade_running = True
                self.update_autotrade_status(True)
                self.show_notification("자동매매 시작", "자동매매가 시작되었습니다.")
        else:
            if not self._autotrade_running:
                self.show_notification("자동매매", "자동매매를 시작하려면 메인 창에서 전략을 선택하세요.")
                self._show_window()
            else:
                self._autotrade_running = False
                self.update_autotrade_status(False)
                self.show_notification("자동매매 중지", "자동매매가 중지되었습니다.")

    def _toggle_kill_switch(self) -> None:
        """킬 스위치를 토글한다."""
        if self._main_window is None:
            return
        self._kill_switch_active = not self._kill_switch_active
        orchestrator = getattr(self._main_window, "_orchestrator", None)
        if orchestrator is not None and self._kill_switch_active:
            orchestrator.emergency_stop()
            self._autotrade_running = False
            self.update_autotrade_status(False)
        self.update_kill_switch_status(self._kill_switch_active)
        self.notify_kill_switch(self._kill_switch_active)

    def _open_web_dashboard(self) -> None:
        """웹 대시보드를 기본 브라우저에서 연다."""
        import webbrowser
        url = getattr(self, "_web_url", "")
        if url:
            webbrowser.open(url)
        else:
            self.show_notification("웹 대시보드", "웹 대시보드가 비활성화 상태입니다.")

    def _open_settings(self) -> None:
        """설정 다이얼로그를 연다."""
        if self._main_window is not None:
            self._show_window()
            self._main_window._open_settings()

    def _quit_app(self) -> None:
        """종료 확인 후 앱을 종료한다."""
        if self._main_window is not None:
            self._main_window._confirm_quit()
        else:
            QApplication.quit()

    def _on_activated(self, reason) -> None:
        """트레이 아이콘 더블클릭 시 메인 윈도우 복원."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_window()
