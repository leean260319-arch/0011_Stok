"""WebSocketManager 테스트
버전: v1.0
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.web.ws_manager import WebSocketManager


@pytest.fixture
def manager() -> WebSocketManager:
    return WebSocketManager()


def make_mock_ws():
    """mock WebSocket 객체 생성."""
    ws = AsyncMock()
    ws.accept = AsyncMock()
    ws.send_text = AsyncMock()
    return ws


# ---------------------------------------------------------------------------
# connect / disconnect / connection_count
# ---------------------------------------------------------------------------

class TestConnection:
    @pytest.mark.asyncio
    async def test_connect(self, manager):
        ws = make_mock_ws()
        await manager.connect(ws)
        assert manager.connection_count == 1
        ws.accept.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_disconnect(self, manager):
        ws = make_mock_ws()
        await manager.connect(ws)
        manager.disconnect(ws)
        assert manager.connection_count == 0

    @pytest.mark.asyncio
    async def test_disconnect_nonexistent(self, manager):
        ws = make_mock_ws()
        # 에러 없이 무시
        manager.disconnect(ws)
        assert manager.connection_count == 0

    @pytest.mark.asyncio
    async def test_multiple_connections(self, manager):
        ws1 = make_mock_ws()
        ws2 = make_mock_ws()
        await manager.connect(ws1)
        await manager.connect(ws2)
        assert manager.connection_count == 2


# ---------------------------------------------------------------------------
# broadcast
# ---------------------------------------------------------------------------

class TestBroadcast:
    @pytest.mark.asyncio
    async def test_broadcast_to_all(self, manager):
        ws1 = make_mock_ws()
        ws2 = make_mock_ws()
        await manager.connect(ws1)
        await manager.connect(ws2)

        data = {"type": "test", "value": 42}
        await manager.broadcast(data)

        expected = json.dumps(data, ensure_ascii=False, default=str)
        ws1.send_text.assert_awaited_once_with(expected)
        ws2.send_text.assert_awaited_once_with(expected)

    @pytest.mark.asyncio
    async def test_broadcast_removes_dead_connections(self, manager):
        ws_alive = make_mock_ws()
        ws_dead = make_mock_ws()
        ws_dead.send_text.side_effect = Exception("connection closed")

        await manager.connect(ws_alive)
        await manager.connect(ws_dead)
        assert manager.connection_count == 2

        await manager.broadcast({"msg": "hello"})

        # 죽은 연결 제거됨
        assert manager.connection_count == 1

    @pytest.mark.asyncio
    async def test_broadcast_empty_connections(self, manager):
        # 연결 없어도 에러 없음
        await manager.broadcast({"msg": "nobody"})
        assert manager.connection_count == 0

    @pytest.mark.asyncio
    async def test_broadcast_korean_text(self, manager):
        ws = make_mock_ws()
        await manager.connect(ws)
        data = {"message": "한글 테스트"}
        await manager.broadcast(data)
        sent = ws.send_text.call_args[0][0]
        assert "한글 테스트" in sent
