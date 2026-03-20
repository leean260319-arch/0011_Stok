"""이벤트 큐 모듈
버전: 1.0.0
설명: asyncio.Queue 기반 이벤트 큐 - 시세→전략 엔진/UI 분배
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List


@dataclass
class Event:
    """이벤트 기본 클래스"""

    event_type: str
    data: Any = None
    source: str = ""


class EventQueue:
    """asyncio.Queue 기반 이벤트 큐 - put/get/subscribe/dispatch"""

    def __init__(self, maxsize: int = 0):
        self._queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=maxsize)
        self._subscribers: Dict[str, List[Callable[[Event], Any]]] = {}

    # ------------------------------------------------------------------ #
    # 기본 큐 인터페이스
    # ------------------------------------------------------------------ #

    async def put(self, event: Event) -> None:
        """이벤트 큐에 삽입"""
        await self._queue.put(event)

    async def get(self) -> Event:
        """이벤트 큐에서 꺼내기 (대기)"""
        return await self._queue.get()

    def task_done(self) -> None:
        """큐 작업 완료 알림"""
        self._queue.task_done()

    def qsize(self) -> int:
        """현재 큐 크기"""
        return self._queue.qsize()

    def empty(self) -> bool:
        """큐가 비어있는지 확인"""
        return self._queue.empty()

    # ------------------------------------------------------------------ #
    # Pub/Sub 인터페이스
    # ------------------------------------------------------------------ #

    def subscribe(self, event_type: str, callback: Callable[[Event], Any]) -> None:
        """특정 이벤트 타입에 콜백 등록"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Event], Any]) -> None:
        """콜백 등록 해제"""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                cb for cb in self._subscribers[event_type] if cb is not callback
            ]

    async def dispatch(self, event: Event) -> None:
        """이벤트를 큐에 넣고 구독자에게 즉시 전달"""
        await self._queue.put(event)
        await self._notify(event)

    async def _notify(self, event: Event) -> None:
        """등록된 콜백 호출 (async/sync 모두 지원)"""
        callbacks = self._subscribers.get(event.event_type, [])
        wildcard = self._subscribers.get("*", [])
        for cb in callbacks + wildcard:
            result = cb(event)
            if asyncio.iscoroutine(result):
                await result

    async def process_forever(self) -> None:
        """큐에서 이벤트를 꺼내 구독자에게 계속 전달 (루프)"""
        while True:
            event = await self._queue.get()
            await self._notify(event)
            self._queue.task_done()
