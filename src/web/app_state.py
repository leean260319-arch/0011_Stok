"""웹 대시보드 공유 상태 객체 - PyQt6 <-> FastAPI 브릿지
버전: v1.0
"""
import copy
import threading
from datetime import datetime


class AppState:
    """PyQt6 앱과 웹 대시보드가 공유하는 상태 객체 (싱글톤, thread-safe)."""

    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> "AppState":
        """싱글톤 인스턴스 반환."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """싱글톤 인스턴스 초기화 (테스트용)."""
        with cls._lock:
            cls._instance = None

    def __init__(self):
        self._lock_data = threading.Lock()
        # 계좌 정보
        self.account: dict = {
            "total_asset": 0,
            "deposit": 0,
            "total_profit": 0,
            "profit_rate": 0.0,
            "daily_realized": 0,
            "daily_unrealized": 0,
        }
        # 보유 종목 리스트
        self.positions: list[dict] = []
        # 자동매매 상태
        self.auto_trade: dict = {
            "is_running": False,
            "strategy_name": "",
            "filled_count": 0,
            "start_time": None,
        }
        # 킬 스위치 상태
        self.kill_switch_active: bool = False
        # AI 시그널
        self.ai_signal: dict = {
            "signal_type": "hold",
            "confidence": 0.0,
            "reasoning": "",
            "timestamp": None,
        }
        # 감성 분석
        self.sentiment: dict = {
            "score": 0.0,
            "label": "neutral",
            "news_count": 0,
        }
        # 시장 지수
        self.market_index: dict = {
            "kospi": {"price": 0, "change_rate": 0.0},
            "kosdaq": {"price": 0, "change_rate": 0.0},
        }
        # 매매 로그 (최근 100건)
        self.trade_logs: list[dict] = []
        # 알림 (최근 50건)
        self.alerts: list[dict] = []
        # 시스템 상태
        self.system: dict = {
            "api_connected": False,
            "market_status": "closed",
            "uptime": None,
            "last_update": None,
        }

    @staticmethod
    def get_market_status() -> str:
        """현재 시장 상태 반환 (KRX 평일 09:00~15:30)."""
        now = datetime.now()
        weekday = now.weekday()
        current_minutes = now.hour * 60 + now.minute
        if weekday >= 5:
            return "closed"
        if 9 * 60 <= current_minutes < 15 * 60 + 30:
            return "open"
        return "closed"

    def update_account(self, **kwargs) -> None:
        """계좌 정보 업데이트."""
        with self._lock_data:
            self.account.update(kwargs)
            self.account["last_update"] = datetime.now().isoformat()

    def update_positions(self, positions: list[dict]) -> None:
        """보유 종목 리스트 교체."""
        with self._lock_data:
            self.positions = positions

    def add_trade_log(self, log: dict) -> None:
        """매매 로그 추가 (최근 100건 유지)."""
        with self._lock_data:
            self.trade_logs.insert(0, {**log, "timestamp": datetime.now().isoformat()})
            self.trade_logs = self.trade_logs[:100]

    def add_alert(self, category: str, message: str) -> None:
        """알림 추가 (최근 50건 유지)."""
        with self._lock_data:
            self.alerts.insert(0, {
                "category": category,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "read": False,
            })
            self.alerts = self.alerts[:50]

    def set_kill_switch(self, active: bool) -> None:
        """킬 스위치 상태 설정."""
        with self._lock_data:
            self.kill_switch_active = active

    def start_auto_trade(self, strategy_name: str) -> None:
        """자동매매 시작 상태 설정."""
        with self._lock_data:
            self.auto_trade["is_running"] = True
            self.auto_trade["strategy_name"] = strategy_name
            self.auto_trade["start_time"] = datetime.now().isoformat()

    def get_auto_trade_strategy(self) -> str:
        """현재 자동매매 전략 이름을 반환한다."""
        with self._lock_data:
            return self.auto_trade["strategy_name"]

    def stop_auto_trade(self) -> None:
        """자동매매 중지 상태 설정."""
        with self._lock_data:
            self.auto_trade["is_running"] = False
            self.auto_trade["strategy_name"] = ""
            self.auto_trade["start_time"] = None

    def update_ai_signal(self, **kwargs) -> None:
        """AI 시그널 업데이트."""
        with self._lock_data:
            self.ai_signal.update(kwargs)

    def update_system(self, **kwargs) -> None:
        """시스템 상태 업데이트."""
        with self._lock_data:
            self.system.update(kwargs)

    def get_account(self) -> dict:
        """계좌 정보를 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.account)

    def get_positions(self) -> list:
        """보유 종목 목록을 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.positions)

    def get_trade_logs(self, limit: int = 20) -> list:
        """매매 로그를 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.trade_logs[:limit])

    def get_alerts(self) -> list:
        """알림 목록을 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.alerts)

    def get_ai_signal(self) -> dict:
        """AI 시그널을 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.ai_signal)

    def get_sentiment(self) -> dict:
        """감성분석 현황을 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.sentiment)

    def get_market_index(self) -> dict:
        """시장 지수를 thread-safe하게 반환한다."""
        with self._lock_data:
            return copy.deepcopy(self.market_index)

    def get_snapshot(self) -> dict:
        """전체 상태 스냅샷 반환 (WebSocket 브로드캐스트용)."""
        with self._lock_data:
            return {
                "account": copy.deepcopy(self.account),
                "positions": copy.deepcopy(self.positions),
                "auto_trade": copy.deepcopy(self.auto_trade),
                "kill_switch_active": self.kill_switch_active,
                "ai_signal": copy.deepcopy(self.ai_signal),
                "sentiment": copy.deepcopy(self.sentiment),
                "market_index": copy.deepcopy(self.market_index),
                "trade_logs": copy.deepcopy(self.trade_logs[:20]),
                "alerts": copy.deepcopy([a for a in self.alerts if not a["read"]][:10]),
                "system": {**copy.deepcopy(self.system), "market_status": self.get_market_status()},
            }
