import asyncio
from typing import Any, Dict
from collections import defaultdict


class StateManager:
    """
    Central async-safe state isolation manager.
    Prevents cross-contamination between engines, plugins, servers.
    """

    def __init__(self):
        self._lock = asyncio.Lock()
        self._state: Dict[str, Dict[str, Any]] = defaultdict(dict)

    async def get(self, namespace: str, key: str, default: Any = None) -> Any:
        async with self._lock:
            return self._state[namespace].get(key, default)

    async def set(self, namespace: str, key: str, value: Any) -> None:
        async with self._lock:
            self._state[namespace][key] = value

    async def delete(self, namespace: str, key: str) -> None:
        async with self._lock:
            self._state[namespace].pop(key, None)

    async def clear_namespace(self, namespace: str) -> None:
        async with self._lock:
            self._state.pop(namespace, None)

    async def snapshot(self, namespace: str) -> Dict[str, Any]:
        async with self._lock:
            return dict(self._state.get(namespace, {}))


# Global singleton (intentional)
STATE = StateManager()
