from typing import Dict, Any, Optional
from .engine_registry import ENGINE_REGISTRY
from app.core.event_bus import EVENT_BUS
from app.core.state_manager import STATE
from app.monitoring import log

await log(f"Active AI engine set to: {engine_id}")
log(f"Engine fallback triggered: {failed_engine} → {fallback_engine}")
log(f"AI generation error in engine {engine_id}: {str(e)}")



class EngineRouter:
    """
    Routes generation requests to the active AI engine.
    """

    def __init__(self):
        self._active_engine_id: Optional[str] = None
        self._fallback_engine_id: Optional[str] = None

    async def set_active(self, engine_id: str) -> None:
        self._active_engine_id = engine_id
        await EVENT_BUS.emit("engine.switched", engine_id=engine_id)

    async def set_fallback(self, engine_id: str) -> None:
        self._fallback_engine_id = engine_id

    async def generate(
        self,
        prompt: str,
        context: Dict[str, Any],
    ) -> str:
        engine = await ENGINE_REGISTRY.get(self._active_engine_id)
        if not engine:
            raise RuntimeError("No active AI engine set")

        try:
            if not await engine.health_check():
                raise RuntimeError("Primary engine unhealthy")

            return await engine.generate(prompt, context)

        except Exception:
            if not self._fallback_engine_id:
                raise

            fallback = await ENGINE_REGISTRY.get(self._fallback_engine_id)
            if not fallback:
                raise

            await STATE.set("ai", "last_fallback", self._fallback_engine_id)
            return await fallback.generate(prompt, context)


# Global singleton
ENGINE_ROUTER = EngineRouter()
