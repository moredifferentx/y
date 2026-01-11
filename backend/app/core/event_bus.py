import asyncio
from collections import defaultdict
from typing import Callable, Dict, List, Any, Coroutine


class EventBus:
    """
    Async internal event bus.
    Enables decoupled communication between subsystems.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[..., Coroutine[Any, Any, None]]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, event: str, handler: Callable[..., Coroutine[Any, Any, None]]) -> None:
        async with self._lock:
            self._subscribers[event].append(handler)

    async def emit(self, event: str, **payload: Any) -> None:
        async with self._lock:
            handlers = list(self._subscribers.get(event, []))

        for handler in handlers:
            asyncio.create_task(handler(**payload))


# Global singleton
EVENT_BUS = EventBus()
