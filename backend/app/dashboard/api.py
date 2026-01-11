from fastapi import APIRouter
from app.core.config import Config
from app.core.event_bus import EVENT_BUS

from app.ai.engine_registry import ENGINE_REGISTRY
from app.ai.engine_router import ENGINE_ROUTER
from app.ai.engines.cloud import register_cloud_engines

from app.plugins import PLUGIN_MANAGER
from app.cognition import Personality, MoodEngine
from app.monitoring import log

log(f"Cloud engine enabled: {engine}")
log(f"Cloud engine disabled: {engine}")
log("Cloud engines reloaded from .env")


# OPTIONAL: enable if you want admin auth enforced
# from app.dashboard.auth import require_admin

router = APIRouter()
# router = APIRouter(dependencies=[require_admin])  # ← enable later if needed


# ==================================================
# CLOUD AI (OPENAI / GEMINI) — EXISTING + EXTENDED
# ==================================================

@router.get("/cloud/status")
async def cloud_status():
    engines = await ENGINE_REGISTRY.list()
    return {
        "openai": "openai" in engines,
        "gemini": "gemini" in engines,
    }


@router.post("/cloud/toggle/{engine}")
async def toggle_cloud(engine: str, enabled: bool):
    if not enabled:
        await ENGINE_REGISTRY.unregister(engine)
        return {"status": "disabled", "engine": engine}

    # Reload env + re-register cloud engines
    Config.reload()
    await register_cloud_engines()

    return {"status": "enabled", "engine": engine}


@router.post("/cloud/reload")
async def reload_cloud_engines():
    Config.reload()
    await register_cloud_engines()
    return {"status": "reloaded"}


# ==================================================
# AI ENGINE ROUTING
# ==================================================

@router.get("/ai/engines")
async def list_ai_engines():
    engines = await ENGINE_REGISTRY.list()
    return list(engines.keys())


@router.post("/ai/engine/active")
async def set_active_engine(engine_id: str):
    await ENGINE_ROUTER.set_active(engine_id)
    return {"status": "ok", "active": engine_id}


# ==================================================
# PLUGINS
# ==================================================

@router.get("/plugins")
async def list_plugins():
    return PLUGIN_MANAGER.list()


@router.post("/plugins/load")
async def load_plugin(name: str):
    await PLUGIN_MANAGER.load(name)
    return {"status": "loaded", "plugin": name}


@router.post("/plugins/unload")
async def unload_plugin(name: str):
    await PLUGIN_MANAGER.unload(name)
    return {"status": "unloaded", "plugin": name}


# ==================================================
# COGNITION (PERSONALITY & MOOD)
# ==================================================

PERSONALITY = Personality()
MOOD = MoodEngine()


@router.get("/cognition")
async def get_cognition_state():
    return {
        "personality": PERSONALITY.snapshot(),
        "mood": MOOD.snapshot(),
    }


@router.post("/cognition/personality")
async def update_personality(traits: dict):
    PERSONALITY.update(traits)
    await EVENT_BUS.emit(
        "cognition.personality.updated",
        traits=traits,
    )
    return {"status": "updated", "traits": traits}


@router.post("/cognition/mood")
async def override_mood(mood: str):
    MOOD.set_override(mood)
    await EVENT_BUS.emit(
        "cognition.mood.updated",
        mood=mood,
    )
    return {"status": "updated", "mood": mood}

from app.monitoring import (
    get_hardware_stats,
    collect_engine_metrics,
    get_logs,
    health_check,
)

# ================= MONITORING =================

@router.get("/monitoring/hardware")
async def monitoring_hardware():
    return get_hardware_stats()

@router.get("/monitoring/metrics")
async def monitoring_metrics():
    return await collect_engine_metrics()

@router.get("/monitoring/health")
async def monitoring_health():
    return await health_check()

@router.get("/monitoring/logs")
async def monitoring_logs():
    return get_logs()
