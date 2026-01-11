from typing import Dict, Any, Optional

from .engine_registry import ENGINE_REGISTRY
from app.core.event_bus import EVENT_BUS
from app.core.state_manager import STATE
from app.monitoring.logs import log


class EngineRouter:
    """
    Routes generation requests to the active AI engine
    with health checks and fallback support.
    """

    def __init__(self):
        self._active_engine_id: Optional[str] = None
        self._fallback_engine_id: Optional[str] = None

    async def set_active(self, engine_id: str) -> None:
        """
        Set the active AI engine.
        Must exist at startup.
        """
        engines = await ENGINE_REGISTRY.list()
        if engine_id not in engines:
            raise ValueError(f"Engine '{engine_id}' is not registered")

        self._active_engine_id = engine_id

        await log(f"Active AI engine set to: {engine_id}")
        await EVENT_BUS.emit("engine.switched", engine_id=engine_id)

    async def set_fallback(self, engine_id: str) -> None:
        """
        Set the fallback AI engine.
        Validation is deferred until fallback is actually used.
        """
        self._fallback_engine_id = engine_id

        engines = await ENGINE_REGISTRY.list()
        if engine_id not in engines:
            await log(
                f"Warning: fallback engine '{engine_id}' "
                f"is not registered yet (will validate on use)"
            )
        else:
            await log(f"Fallback AI engine set to: {engine_id}")

    async def generate(
        self,
        prompt: str,
        context: Dict[str, Any],
    ) -> str:
        """
        Generate a response using the active engine,
        falling back if needed.
        """
        if not self._active_engine_id:
            raise RuntimeError("No active AI engine set")

        engine = await ENGINE_REGISTRY.get(self._active_engine_id)
        if not engine:
            raise RuntimeError(
                f"Active AI engine '{self._active_engine_id}' not found"
            )

        try:
            if not await engine.health_check():
                raise RuntimeError("Primary engine unhealthy")

            return await engine.generate(prompt, context)

        except Exception as e:
            await log(
                f"AI generation error in engine "
                f"{self._active_engine_id}: {str(e)}"
            )

            if not self._fallback_engine_id:
                raise

            fallback = await ENGINE_REGISTRY.get(self._fallback_engine_id)
            if not fallback:
                raise RuntimeError(
                    f"Fallback engine '{self._fallback_engine_id}' not registered"
                )

            await log(
                f"Engine fallback triggered: "
                f"{self._active_engine_id} → {self._fallback_engine_id}"
            )

            await STATE.set(
                "ai",
                "last_fallback",
                self._fallback_engine_id,
            )

            return await fallback.generate(prompt, context)


# Global singleton
ENGINE_ROUTER = EngineRouter()
