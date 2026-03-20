"""REST API 엔드포인트 - 웹 대시보드용
버전: v1.0
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from src.web.app_state import AppState
from src.web.auth import WebAuth
from src.web.ws_manager import WebSocketManager


# ---------------------------------------------------------------------------
# 요청/응답 모델
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    """로그인 요청."""
    username: str = ""
    password: str


class LoginResponse(BaseModel):
    """로그인 응답."""
    token: str


class AutoTradeStartRequest(BaseModel):
    """자동매매 시작 요청."""
    strategy_name: str


class MessageResponse(BaseModel):
    """일반 메시지 응답."""
    message: str


# ---------------------------------------------------------------------------
# 의존성 주입을 위한 컨테이너
# ---------------------------------------------------------------------------

class ApiDeps:
    """API 라우터가 사용하는 공유 객체 컨테이너."""

    def __init__(self, auth: WebAuth, state: AppState, ws_manager: WebSocketManager):
        self.auth = auth
        self.state = state
        self.ws_manager = ws_manager


_deps: ApiDeps | None = None


def set_deps(deps: ApiDeps) -> None:
    """의존성 주입 설정."""
    global _deps
    _deps = deps


def get_deps() -> ApiDeps:
    """현재 의존성 반환."""
    return _deps


# ---------------------------------------------------------------------------
# 인증 의존성
# ---------------------------------------------------------------------------

def require_auth(request: Request) -> str:
    """Authorization 헤더에서 Bearer 토큰을 추출하고 검증."""
    deps = get_deps()
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다")
    token = auth_header[7:]
    if not deps.auth.validate_session(token):
        raise HTTPException(status_code=401, detail="유효하지 않은 세션입니다")
    return token


# ---------------------------------------------------------------------------
# 라우터
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/api")


# --- 로그인/로그아웃 (인증 불필요) ---

@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    """아이디/비밀번호 검증 후 세션 토큰 발급."""
    deps = get_deps()
    if deps.auth.is_locked():
        remaining = deps.auth.remaining_lock_seconds()
        raise HTTPException(
            status_code=423,
            detail=f"로그인이 잠겼습니다. {remaining}초 후 재시도하세요.",
        )
    if deps.auth.get_username():
        # 아이디+비밀번호 모드
        if not deps.auth.verify(body.username, body.password):
            remaining_attempts = deps.auth.remaining_attempts()
            if deps.auth.is_locked():
                raise HTTPException(
                    status_code=423,
                    detail=f"로그인이 잠겼습니다. {deps.auth.remaining_lock_seconds()}초 후 재시도하세요.",
                )
            raise HTTPException(
                status_code=401,
                detail="아이디 또는 비밀번호가 일치하지 않습니다",
            )
    else:
        # 하위 호환: 비밀번호만 모드
        if not deps.auth.verify_password(body.password):
            raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다")
    token = deps.auth.create_session()
    return LoginResponse(token=token)


@router.post("/logout", response_model=MessageResponse)
def logout(token: str = Depends(require_auth)):
    """세션 종료."""
    deps = get_deps()
    deps.auth.revoke_session(token)
    return MessageResponse(message="로그아웃 완료")


# --- 조회 API (인증 필요) ---

@router.get("/status")
def get_status(_: str = Depends(require_auth)):
    """전체 상태 스냅샷."""
    deps = get_deps()
    return deps.state.get_snapshot()


@router.get("/account")
def get_account(_: str = Depends(require_auth)):
    """계좌 정보."""
    deps = get_deps()
    return deps.state.get_account()


@router.get("/positions")
def get_positions(_: str = Depends(require_auth)):
    """보유 종목 목록."""
    deps = get_deps()
    return deps.state.get_positions()


@router.get("/trade-logs")
def get_trade_logs(limit: int = 20, _: str = Depends(require_auth)):
    """매매 로그."""
    deps = get_deps()
    limit = max(1, min(limit, 100))
    return deps.state.get_trade_logs(limit)


@router.get("/alerts")
def get_alerts(_: str = Depends(require_auth)):
    """알림 목록."""
    deps = get_deps()
    return deps.state.get_alerts()


@router.get("/ai-signal")
def get_ai_signal(_: str = Depends(require_auth)):
    """현재 AI 시그널."""
    deps = get_deps()
    return deps.state.get_ai_signal()


@router.get("/sentiment")
def get_sentiment(_: str = Depends(require_auth)):
    """감성 분석 현황."""
    deps = get_deps()
    return deps.state.get_sentiment()


@router.get("/market")
def get_market(_: str = Depends(require_auth)):
    """시장 지수."""
    deps = get_deps()
    return deps.state.get_market_index()


# --- 제어 API (인증 필요) ---

@router.post("/autotrade/start", response_model=MessageResponse)
async def autotrade_start(body: AutoTradeStartRequest, _: str = Depends(require_auth)):
    """자동매매 시작."""
    deps = get_deps()
    deps.state.start_auto_trade(body.strategy_name)
    deps.state.add_alert("autotrade", f"자동매매 시작: {body.strategy_name}")
    snapshot = deps.state.get_snapshot()
    await deps.ws_manager.broadcast({"type": "state_update", "data": snapshot})
    return MessageResponse(message=f"자동매매 시작: {body.strategy_name}")


@router.post("/autotrade/stop", response_model=MessageResponse)
async def autotrade_stop(_: str = Depends(require_auth)):
    """자동매매 중지."""
    deps = get_deps()
    strategy = deps.state.get_auto_trade_strategy()
    deps.state.stop_auto_trade()
    deps.state.add_alert("autotrade", "자동매매 중지")
    snapshot = deps.state.get_snapshot()
    await deps.ws_manager.broadcast({"type": "state_update", "data": snapshot})
    return MessageResponse(message=f"자동매매 중지 (전략: {strategy})")


@router.post("/kill-switch/on", response_model=MessageResponse)
async def kill_switch_on(_: str = Depends(require_auth)):
    """킬 스위치 발동."""
    deps = get_deps()
    deps.state.set_kill_switch(True)
    deps.state.add_alert("kill_switch", "킬 스위치 발동")
    snapshot = deps.state.get_snapshot()
    await deps.ws_manager.broadcast({"type": "state_update", "data": snapshot})
    return MessageResponse(message="킬 스위치 발동")


@router.post("/kill-switch/off", response_model=MessageResponse)
async def kill_switch_off(_: str = Depends(require_auth)):
    """킬 스위치 해제."""
    deps = get_deps()
    deps.state.set_kill_switch(False)
    deps.state.add_alert("kill_switch", "킬 스위치 해제")
    snapshot = deps.state.get_snapshot()
    await deps.ws_manager.broadcast({"type": "state_update", "data": snapshot})
    return MessageResponse(message="킬 스위치 해제")
