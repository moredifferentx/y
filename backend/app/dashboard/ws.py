from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio

from app.core.event_bus import EVENT_BUS
from app.ai.engine_router import ENGINE_ROUTER
from app.ai.engine_registry import ENGINE_REGISTRY
from app.plugins import PLUGIN_MANAGER
from app.cognition import Personality, MoodEngine
from app.monitoring import (
    get_hardware_stats,
    collect_engine_metrics,
    get_logs,
    log,
)

# ==================================================
# STATE
# ==================================================

connections: List[WebSocket] = []

PERSONALITY = Personality()
MOOD = MoodEngine()


# ==================================================
# BROADCAST UTIL
# ==================================================

async def broadcast(payload: dict):
    dead = []
    for ws in connections:
        try:
            await ws.send_json(payload)
        except Exception:
            dead.append(ws)

    for ws in dead:
        if ws in connections:
            connections.remove(ws)


# ==================================================
# EVENT LISTENERS
# ==================================================

async def engine_switch_listener(engine_id: str):
    await broadcast({
        "type": "engine.switch",
        "engine": engine_id,
    })


async def personality_listener(traits: dict):
    await broadcast({
        "type": "personality.update",
        "traits": traits,
    })


async def mood_listener(mood: str):
    await broadcast({
        "type": "mood.update",
        "mood": mood,
    })


async def plugin_loaded_listener(plugin: str):
    await broadcast({
        "type": "plugin.loaded",
        "plugin": plugin,
    })


async def plugin_unloaded_listener(plugin: str):
    await broadcast({
        "type": "plugin.unloaded",
        "plugin": plugin,
    })


# ==================================================
# ✅ SAFE STARTUP HOOK (FIX)
# ==================================================

async def start_dashboard_ws():
    """
    Must be called during FastAPI startup.
    Registers EventBus listeners safely.
    """
    await EVENT_BUS.subscribe("engine.switched", engine_switch_listener)
    await EVENT_BUS.subscribe("cognition.personality.updated", personality_listener)
    await EVENT_BUS.subscribe("cognition.mood.updated", mood_listener)
    await EVENT_BUS.subscribe("plugin.loaded", plugin_loaded_listener)
    await EVENT_BUS.subscribe("plugin.unloaded", plugin_unloaded_listener)

    log("Dashboard WebSocket event listeners registered")


# ==================================================
# WEBSOCKET ENDPOINT
# ==================================================

async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    log("Dashboard WebSocket connected")

    engines = await ENGINE_REGISTRY.list()

    await ws.send_json({
        "type": "init",
        "state": {
            "active_engine": ENGINE_ROUTER._active_engine_id,
            "engines": list(engines.keys()),
            "cloud": {
                "openai": "openai" in engines,
                "gemini": "gemini" in engines,
            },
            "plugins": PLUGIN_MANAGER.list(),
            "personality": PERSONALITY.snapshot(),
            "mood": MOOD.snapshot(),
            "hardware": get_hardware_stats(),
            "metrics": await collect_engine_metrics(),
            "logs": get_logs(),
        },
    })

    try:
        while True:
            await asyncio.sleep(2)
            await ws.send_json({
                "type": "monitoring.update",
                "hardware": get_hardware_stats(),
                "metrics": await collect_engine_metrics(),
                "logs": get_logs(),
            })
    except WebSocketDisconnect:
        if ws in connections:
            connections.remove(ws)
        log("Dashboard WebSocket disconnected")
