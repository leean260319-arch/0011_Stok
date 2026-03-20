"""EventQueue 테스트 - put/get/subscribe/dispatch/process_forever"""
import asyncio
from unittest.mock import MagicMock, AsyncMock

import pytest

from src.engine.event_queue import Event, EventQueue


# ------------------------------------------------------------------ #
# 픽스처
# ------------------------------------------------------------------ #

@pytest.fixture
def queue():
    return EventQueue()


@pytest.fixture
def event():
    return Event(event_type="PRICE", data={"code": "005930", "price": 70000}, source="test")


# ------------------------------------------------------------------ #
# Event 데이터클래스
# ------------------------------------------------------------------ #

class TestEventDataclass:
    def test_event_fields(self):
        e = Event(event_type="TICK", data=42, source="src")
        assert e.event_type == "TICK"
        assert e.data == 42
        assert e.source == "src"

    def test_event_default_data_none(self):
        e = Event(event_type="ORDER")
        assert e.data is None
        assert e.source == ""


# ------------------------------------------------------------------ #
# put / get / qsize / empty
# ------------------------------------------------------------------ #

class TestEventQueueBasic:
    @pytest.mark.asyncio
    async def test_put_increases_qsize(self, queue, event):
        assert queue.empty() is True
        await queue.put(event)
        assert queue.qsize() == 1

    @pytest.mark.asyncio
    async def test_get_returns_same_event(self, queue, event):
        await queue.put(event)
        result = await queue.get()
        assert result is event

    @pytest.mark.asyncio
    async def test_fifo_order(self, queue):
        e1 = Event("A")
        e2 = Event("B")
        e3 = Event("C")
        await queue.put(e1)
        await queue.put(e2)
        await queue.put(e3)
        assert (await queue.get()) is e1
        assert (await queue.get()) is e2
        assert (await queue.get()) is e3

    @pytest.mark.asyncio
    async def test_empty_returns_true_initially(self, queue):
        assert queue.empty() is True

    @pytest.mark.asyncio
    async def test_empty_returns_false_after_put(self, queue, event):
        await queue.put(event)
        assert queue.empty() is False

    @pytest.mark.asyncio
    async def test_task_done_does_not_raise(self, queue, event):
        await queue.put(event)
        await queue.get()
        queue.task_done()  # should not raise

    @pytest.mark.asyncio
    async def test_maxsize_blocks_when_full(self):
        q = EventQueue(maxsize=1)
        await q.put(Event("FIRST"))
        # 두 번째 put은 get 없이는 블록됨 - put_nowait으로 QueueFull 확인
        with pytest.raises(asyncio.QueueFull):
            q._queue.put_nowait(Event("SECOND"))


# ------------------------------------------------------------------ #
# subscribe / unsubscribe
# ------------------------------------------------------------------ #

class TestEventQueueSubscribe:
    def test_subscribe_registers_callback(self, queue):
        cb = MagicMock()
        queue.subscribe("PRICE", cb)
        assert cb in queue._subscribers["PRICE"]

    def test_subscribe_multiple_callbacks_same_type(self, queue):
        cb1 = MagicMock()
        cb2 = MagicMock()
        queue.subscribe("PRICE", cb1)
        queue.subscribe("PRICE", cb2)
        assert len(queue._subscribers["PRICE"]) == 2

    def test_unsubscribe_removes_callback(self, queue):
        cb = MagicMock()
        queue.subscribe("PRICE", cb)
        queue.unsubscribe("PRICE", cb)
        assert cb not in queue._subscribers.get("PRICE", [])

    def test_unsubscribe_nonexistent_type_is_safe(self, queue):
        cb = MagicMock()
        queue.unsubscribe("NONEXISTENT", cb)  # should not raise

    def test_unsubscribe_only_removes_target_callback(self, queue):
        cb1 = MagicMock()
        cb2 = MagicMock()
        queue.subscribe("PRICE", cb1)
        queue.subscribe("PRICE", cb2)
        queue.unsubscribe("PRICE", cb1)
        assert cb1 not in queue._subscribers["PRICE"]
        assert cb2 in queue._subscribers["PRICE"]


# ------------------------------------------------------------------ #
# dispatch / _notify
# ------------------------------------------------------------------ #

class TestEventQueueDispatch:
    @pytest.mark.asyncio
    async def test_dispatch_puts_event_in_queue(self, queue, event):
        await queue.dispatch(event)
        assert queue.qsize() == 1

    @pytest.mark.asyncio
    async def test_dispatch_calls_sync_subscriber(self, queue, event):
        cb = MagicMock()
        queue.subscribe("PRICE", cb)
        await queue.dispatch(event)
        cb.assert_called_once_with(event)

    @pytest.mark.asyncio
    async def test_dispatch_calls_async_subscriber(self, queue, event):
        cb = AsyncMock()
        queue.subscribe("PRICE", cb)
        await queue.dispatch(event)
        cb.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_dispatch_does_not_call_other_type_subscriber(self, queue):
        cb = MagicMock()
        queue.subscribe("ORDER", cb)
        event = Event("PRICE")
        await queue.dispatch(event)
        cb.assert_not_called()

    @pytest.mark.asyncio
    async def test_dispatch_calls_wildcard_subscriber(self, queue):
        cb = MagicMock()
        queue.subscribe("*", cb)
        e1 = Event("PRICE")
        e2 = Event("ORDER")
        await queue.dispatch(e1)
        await queue.dispatch(e2)
        assert cb.call_count == 2

    @pytest.mark.asyncio
    async def test_dispatch_calls_both_specific_and_wildcard(self, queue):
        specific_cb = MagicMock()
        wildcard_cb = MagicMock()
        queue.subscribe("PRICE", specific_cb)
        queue.subscribe("*", wildcard_cb)
        event = Event("PRICE")
        await queue.dispatch(event)
        specific_cb.assert_called_once_with(event)
        wildcard_cb.assert_called_once_with(event)


# ------------------------------------------------------------------ #
# process_forever
# ------------------------------------------------------------------ #

class TestEventQueueProcessForever:
    @pytest.mark.asyncio
    async def test_process_forever_dispatches_to_subscribers(self, queue):
        received = []

        def cb(e):
            received.append(e)

        queue.subscribe("PRICE", cb)
        e1 = Event("PRICE", data=1)
        e2 = Event("PRICE", data=2)
        await queue.put(e1)
        await queue.put(e2)

        async def run():
            await asyncio.wait_for(queue.process_forever(), timeout=0.1)

        with pytest.raises(asyncio.TimeoutError):
            await run()

        assert len(received) == 2
        assert received[0] is e1
        assert received[1] is e2
