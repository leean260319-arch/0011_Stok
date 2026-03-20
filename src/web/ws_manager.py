"""WebSocket 연결 관리자 - 연결 관리 및 브로드캐스트
버전: v1.0
"""
import json

from fastapi import WebSocket


class WebSocketManager:
    """WebSocket 연결 관리 및 브로드캐스트."""

    def __init__(self):
        self._connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """WebSocket 연결 수락 및 등록."""
        await websocket.accept()
        self._connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """WebSocket 연결 해제."""
        if websocket in self._connections:
            self._connections.remove(websocket)

    async def broadcast(self, data: dict) -> None:
        """모든 연결된 클라이언트에 데이터 전송."""
        dead: list[WebSocket] = []
        message = json.dumps(data, ensure_ascii=False, default=str)
        for ws in self._connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections.remove(ws)

    @property
    def connection_count(self) -> int:
        """현재 연결된 클라이언트 수."""
        return len(self._connections)
