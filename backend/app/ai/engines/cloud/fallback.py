from app.ai.engine_registry import ENGINE_REGISTRY
from app.ai.engine_router import ENGINE_ROUTER


async def configure_fallback(primary: str, fallback: str):
    """
    Configure primary + fallback engines safely.
    """
    primary_engine = await ENGINE_REGISTRY.get(primary)
    fallback_engine = await ENGINE_REGISTRY.get(fallback)

    if not primary_engine or not fallback_engine:
        raise RuntimeError("Invalid engine configuration")

    await ENGINE_ROUTER.set_active(primary)
    await ENGINE_ROUTER.set_fallback(fallback)
