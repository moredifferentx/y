from typing import Dict
from .engines.base import BaseAIEngine
import asyncio


class EngineRegistry:
    """
    Runtime AI engine registry.
    """

    def __init__(self):
        self._engines: Dict[str, BaseAIEngine] = {}
        self._lock = asyncio.Lock()

    async def register(self, engine: BaseAIEngine) -> None:
        async with self._lock:
            self._engines[engine.engine_id] = engine

    async def unregister(self, engine_id: str) -> None:
        async with self._lock:
            engine = self._engines.pop(engine_id, None)
            if engine:
                await engine.shutdown()

    async def get(self, engine_id: str) -> BaseAIEngine | None:
        async with self._lock:
            return self._engines.get(engine_id)

    async def list(self) -> Dict[str, BaseAIEngine]:
        async with self._lock:
            return dict(self._engines)


# Global singleton
ENGINE_REGISTRY = EngineRegistry()
