"""웹 대시보드 서버 - FastAPI + uvicorn 백그라운드 스레드
버전: v1.0
"""
import asyncio
import json
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

from src.web.app_state import AppState
from src.web.auth import WebAuth
from src.web.ws_manager import WebSocketManager
from src.web.api_routes import router as api_router, set_deps, ApiDeps

# 패키지 디렉토리 기준 경로
_WEB_DIR = Path(__file__).parent
_TEMPLATE_DIR = _WEB_DIR / "templates"
_STATIC_DIR = _WEB_DIR / "static"


async def _broadcast_loop(ws_manager: WebSocketManager, app_state: AppState, auth: "WebAuth") -> None:
    """1초마다 AppState 스냅샷을 WebSocket으로 브로드캐스트."""
    cleanup_counter = 0
    while True:
        await asyncio.sleep(1)
        if ws_manager.connection_count > 0:
            snapshot = app_state.get_snapshot()
            await ws_manager.broadcast({"type": "state_update", "data": snapshot})
        cleanup_counter += 1
        if cleanup_counter >= 600:  # 10분마다
            auth.cleanup_expired_sessions()
            cleanup_counter = 0


class WebDashboardServer:
    """웹 대시보드 서버 - PyQt6 앱과 동일 프로세스에서 백그라운드 실행."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8080, username: str = "", password: str = ""):
        self.host = host
        self.port = port
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._server: uvicorn.Server | None = None

        # 공유 객체
        self.state = AppState.get_instance()
        self.auth = WebAuth()
        self.ws_manager = WebSocketManager()

        if username and password:
            self.auth.set_credentials(username, password)
        elif password:
            self.auth.set_password(password)

        self._app = self._create_app()

    def _create_app(self) -> FastAPI:
        """FastAPI 앱 생성 및 설정."""
        ws_mgr = self.ws_manager
        st = self.state
        auth = self.auth

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            task = asyncio.create_task(_broadcast_loop(ws_mgr, st, auth))
            yield
            task.cancel()

        app = FastAPI(title="StokAI Web Dashboard", version="1.0.0", lifespan=lifespan)

        # 의존성 주입
        deps = ApiDeps(auth=self.auth, state=self.state, ws_manager=self.ws_manager)
        set_deps(deps)

        # REST API 라우터
        app.include_router(api_router)

        # 정적 파일
        if _STATIC_DIR.exists():
            app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

        # 템플릿
        templates = Jinja2Templates(directory=str(_TEMPLATE_DIR))

        # --- HTML 페이지 ---

        @app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            """메인 페이지 - 로그인 여부에 따라 분기."""
            return templates.TemplateResponse("login.html", {"request": request})

        @app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard(request: Request, token: str = Query("")):
            """대시보드 페이지 - 인증 필요."""
            if not token or not self.auth.validate_session(token):
                return RedirectResponse(url="/", status_code=302)
            return templates.TemplateResponse("dashboard.html", {"request": request})

        # --- WebSocket ---

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket, token: str = Query("")):
            """WebSocket 연결 - 인증 토큰 검증 후 실시간 데이터 수신."""
            if not self.auth.validate_session(token):
                await websocket.close(code=4001, reason="인증 실패")
                return
            await self.ws_manager.connect(websocket)
            try:
                while True:
                    raw = await websocket.receive_text()
                    if not self.auth.validate_session(token):
                        await websocket.close(code=4001, reason="세션 만료")
                        break
                    data = json.loads(raw)
                    await self._handle_ws_command(data)
            except WebSocketDisconnect:
                self.ws_manager.disconnect(websocket)

        return app

    async def _handle_ws_command(self, data: dict) -> None:
        """WebSocket 클라이언트에서 수신한 명령 처리."""
        command = data.get("command", "")
        _VALID_COMMANDS = {"kill_switch_on", "kill_switch_off", "autotrade_start", "autotrade_stop"}
        if command not in _VALID_COMMANDS:
            return
        strategy = data.get("strategy_name", "default")
        if strategy and len(strategy) > 100:
            return
        if command == "kill_switch_on":
            self.state.set_kill_switch(True)
            self.state.add_alert("kill_switch", "킬 스위치 발동 (WebSocket)")
        elif command == "kill_switch_off":
            self.state.set_kill_switch(False)
            self.state.add_alert("kill_switch", "킬 스위치 해제 (WebSocket)")
        elif command == "autotrade_start":
            self.state.start_auto_trade(strategy)
            self.state.add_alert("autotrade", f"자동매매 시작: {strategy} (WebSocket)")
        elif command == "autotrade_stop":
            self.state.stop_auto_trade()
            self.state.add_alert("autotrade", "자동매매 중지 (WebSocket)")

    def start(self) -> None:
        """백그라운드 스레드로 서버 시작."""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        """uvicorn 서버 실행 (별도 이벤트 루프)."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        config = uvicorn.Config(
            self._app,
            host=self.host,
            port=self.port,
            log_level="warning",
        )
        self._server = uvicorn.Server(config)
        self._loop.run_until_complete(self._server.serve())

    def stop(self) -> None:
        """서버 중지."""
        if self._server:
            self._server.should_exit = True

    @property
    def app(self) -> FastAPI:
        """FastAPI 앱 인스턴스 (테스트용)."""
        return self._app

    @property
    def url(self) -> str:
        """서버 URL."""
        return f"http://{self.host}:{self.port}"
