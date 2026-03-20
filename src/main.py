"""T013: 앱 진입점 - QApplication 초기화, 이벤트 루프, 시스템 트레이"""

# 버전 정보
# v1.0 - 2026-03-16: 신규 작성
# v1.1 - 2026-03-17: 배포 완전성 - 디렉토리 자동 생성, 첫 실행 감지, SetupWizard 연동
# v1.2 - 2026-03-17: ServiceContainer + TradingOrchestrator 통합, DB 초기화 연동

import os
import sys
import traceback

from PyQt6.QtWidgets import QApplication

from src.utils.constants import DB_DIR, LOG_DIR, DATA_DIR, DB_PATH, CONFIG_PATH
from src.utils.logger import setup_logging, get_logger

logger = get_logger("main")


def _setup_exception_handler():
    """전역 예외 핸들러 - 예기치 않은 에러 시 로그 기록 후 알림."""
    _logger = get_logger("main")

    def _excepthook(exc_type, exc_value, exc_tb):
        _logger.critical(
            "치명적 오류 발생: %s: %s\n%s",
            exc_type.__name__,
            exc_value,
            "".join(traceback.format_exception(exc_type, exc_value, exc_tb)),
        )

    sys.excepthook = _excepthook


def _ensure_directories() -> None:
    """필수 디렉토리가 없으면 생성한다."""
    for d in [DB_DIR, LOG_DIR, DATA_DIR]:
        os.makedirs(d, exist_ok=True)


def _is_first_run() -> bool:
    """최초 실행인지 확인한다. DB 파일이 없으면 최초 실행으로 판단한다."""
    return not os.path.exists(DB_PATH)


def create_app() -> QApplication:
    """QApplication 인스턴스를 반환한다. 이미 존재하면 기존 인스턴스를 반환한다."""
    existing = QApplication.instance()
    if existing is not None:
        return existing
    return QApplication(sys.argv)


def main() -> None:
    """앱 진입점: 디렉토리 생성, DB 초기화, QApplication 생성, MainWindow 표시, 이벤트 루프 실행."""
    _setup_exception_handler()

    from src.app import MainWindow, SystemTray
    from src.config import ConfigManager
    from src.service_container import ServiceContainer
    from src.engine.orchestrator import TradingOrchestrator

    # 1. 필수 디렉토리 생성
    _ensure_directories()

    # 2. 로거 초기화
    setup_logging()

    # 3. 설정 파일 로드 (없으면 기본값 사용, 저장)
    config_mgr = ConfigManager()
    config = config_mgr.load(CONFIG_PATH)
    if not os.path.exists(CONFIG_PATH):
        config_mgr.save(CONFIG_PATH, config)

    first_run = _is_first_run()

    # 3.5 UI 스케일 적용 (QApplication 생성 전)
    ui_scale = config_mgr.get("ui.ui_scale", 100)
    if ui_scale != 100:
        os.environ["QT_SCALE_FACTOR"] = str(ui_scale / 100.0)

    # 4. QApplication 생성
    app = create_app()

    # 5. 최초 실행: SetupWizard 표시
    if first_run:
        from src.ui.setup_wizard import SetupWizard
        from src.security.credential_manager import CredentialManager
        from PyQt6.QtWidgets import QDialog, QVBoxLayout

        dlg = QDialog()
        dlg.setWindowTitle("StokAI 초기 설정")
        dlg.resize(500, 400)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(0, 0, 0, 0)
        wizard = SetupWizard()
        wizard.wizard_completed.connect(dlg.accept)
        layout.addWidget(wizard)
        dlg.exec()

        # 마법사 완료 후 데이터 저장
        if wizard.is_complete():
            cred_mgr = CredentialManager()

            # 0단계: 앱 비밀번호
            step0 = wizard.get_step_data(0)
            if step0.get("password"):
                cred_mgr.save("app_password", step0["password"])

            # 1단계: 계좌 정보 및 키움 API
            step1 = wizard.get_step_data(1)
            if step1.get("account_number"):
                config_mgr.set("kiwoom.account_number", step1["account_number"])
            if step1.get("account_password"):
                cred_mgr.save("account_password", step1["account_password"])
            if step1.get("api_key"):
                cred_mgr.save("kiwoom_api_key", step1["api_key"])

            # 2단계: AI API 키
            step2 = wizard.get_step_data(2)
            if step2.get("openai_api_key"):
                cred_mgr.save("openai_api_key", step2["openai_api_key"])
                config_mgr.set("ai.primary_api_key", step2["openai_api_key"])
            if step2.get("deepseek_api_key"):
                cred_mgr.save("deepseek_api_key", step2["deepseek_api_key"])
                config_mgr.set("ai.fallback_api_key", step2["deepseek_api_key"])

            # 3단계: 리스크 설정
            step3 = wizard.get_step_data(3)
            if step3.get("daily_loss_limit") is not None:
                config_mgr.set("risk.daily_loss_limit_pct", step3["daily_loss_limit"])
            if step3.get("max_position") is not None:
                config_mgr.set("risk.max_position_pct", step3["max_position"])
            if step3.get("stop_loss") is not None:
                config_mgr.set("risk.stop_loss_pct", step3["stop_loss"])
            if step3.get("take_profit") is not None:
                config_mgr.set("risk.take_profit_pct", step3["take_profit"])

            # 설정 파일 저장
            config_mgr.save(CONFIG_PATH, config_mgr.get_all())
            logger.info("SetupWizard 설정 저장 완료")

    # 6. ServiceContainer 전체 초기화
    container = ServiceContainer(config_mgr)
    container.init_all()

    # 7. TradingOrchestrator 생성
    orchestrator = TradingOrchestrator(container)

    # 7.5 AlertManager를 orchestrator 시그널에 연결
    alert_manager = container.alert_manager
    if alert_manager and orchestrator:
        orchestrator.order_executed.connect(alert_manager.on_trade_executed)
        orchestrator.status_changed.connect(
            lambda status: alert_manager.on_kill_switch()
            if status == "emergency_stopped" else None
        )

    # 7.6 NewsScheduler 시작
    news_scheduler = container.news_scheduler
    if news_scheduler:
        watched = config_mgr.get("watchlist", [])
        if watched:
            news_scheduler.set_stock_codes(watched)
        news_scheduler.start()

    # 8. MainWindow 표시 (container + orchestrator 주입)
    window = MainWindow(container=container, orchestrator=orchestrator)

    tray = SystemTray(parent=window)
    window.tray = tray
    tray.show()

    # 8.1 킬 스위치 -> orchestrator 긴급 정지 연결
    if orchestrator:
        window.right_panel.kill_switch.activated.connect(orchestrator.emergency_stop)
        orchestrator.screening_completed.connect(window._on_screening_completed)
        orchestrator.portfolio_updated.connect(window._on_portfolio_updated)

    # 8.2 AlertManager 알림 -> AlertView 표시
    if alert_manager:
        from datetime import datetime

        def _on_alert_added(alert_dict: dict):
            """AlertManager 알림을 AlertView 위젯에 추가한다."""
            window.alert_view.add_alert(
                category=alert_dict.get("category", "system"),
                message=f"{alert_dict.get('title', '')} - {alert_dict.get('message', '')}",
                timestamp=datetime.now(),
            )

        alert_manager.alert_added.connect(_on_alert_added)

    # 8.3 NewsScheduler 뉴스 -> NewsView 표시
    if news_scheduler:
        def _on_news_fetched(articles: list):
            """수집된 뉴스를 NewsView 위젯에 추가한다."""
            for art in articles:
                window.news_view.add_news(
                    title=art.get("title", ""),
                    source=art.get("source", ""),
                    sentiment=art.get("sentiment", "neutral"),
                    url=art.get("url", ""),
                )

        news_scheduler.news_fetched.connect(_on_news_fetched)

    # 8.4 웹 대시보드 AppState 연결 (orchestrator 시그널 -> AppState 업데이트)
    if orchestrator:
        from src.web.app_state import AppState

        app_state = AppState.get_instance()

        def _on_signal_for_appstate(data: dict):
            """AI 시그널을 AppState에 반영한다."""
            signal_map = {"매수": "buy", "매도": "sell", "관망": "hold"}
            app_state.update_ai_signal(
                signal_type=signal_map.get(data.get("signal", "관망"), "hold"),
                confidence=data.get("confidence", 0.0),
                reasoning=str(data.get("details", "")),
            )

        orchestrator.signal_generated.connect(_on_signal_for_appstate)

        def _on_order_for_appstate(data: dict):
            """주문 실행 결과를 AppState 매매 로그에 추가한다."""
            app_state.add_trade_log(data)

        orchestrator.order_executed.connect(_on_order_for_appstate)

        def _on_status_for_appstate(status: str):
            """자동매매 상태를 AppState에 반영한다."""
            if status == "running":
                app_state.start_auto_trade(strategy_name="ensemble")
            elif status in ("stopped", "emergency_stopped"):
                app_state.stop_auto_trade()
            if status == "emergency_stopped":
                app_state.set_kill_switch(True)

        orchestrator.status_changed.connect(_on_status_for_appstate)

    # 8.6 전략 목록 초기화 - strategy_engine에 등록된 전략 표시
    if container and container.strategy_engine:
        for strategy in container.strategy_engine.strategies:
            window.strategy_list.add_strategy(strategy.name, is_active=True)

    # 9. 웹 대시보드 서버 시작
    if config_mgr.get("web_dashboard.enabled", True):
        from src.web.server import WebDashboardServer
        from src.utils.constants import get_local_ip, get_public_ip

        web_port = config_mgr.get("web_dashboard.port", 8080)
        web_username = config_mgr.get("web_dashboard.username", "admin")
        web_password = config_mgr.get("web_dashboard.password", "")
        if not web_password:
            import secrets
            web_password = secrets.token_urlsafe(12)
            config_mgr.set("web_dashboard.password", web_password)
            config_mgr.save(CONFIG_PATH, config_mgr.get_all())
            logger.info("웹 대시보드 비밀번호 자동 생성됨")
        web_server = WebDashboardServer(
            host="0.0.0.0", port=web_port, username=web_username, password=web_password
        )
        web_server.start()
        window.web_server = web_server
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        display_ip = public_ip or local_ip
        window.set_web_url(f"http://{display_ip}:{web_port}")
        window.set_tray_web_url(f"http://{display_ip}:{web_port}")
        logger.info(f"웹 대시보드: http://{display_ip}:{web_port} (LAN: {local_ip})")

    # 10. 종료 시 서비스 shutdown
    app.aboutToQuit.connect(container.shutdown)

    window.show()

    logger.info("StokAI 시작")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
