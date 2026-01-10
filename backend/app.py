import os
import asyncio
import logging
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.ai.engine import AIManager
from backend.db import init_db
from backend.bot.discord_bot import start_discord_bot
from backend.memory import store as memory_store
from backend.personality import manager as personality_manager
from backend.expression import engine as expression_engine
from backend.relationships import manager as relationship_manager
from backend.image_gen import generator as image_generator
from backend.languages import manager as language_manager
from backend.conversation import scorer as conversation_scorer
from backend.scheduler import scheduler
from backend.monitor import monitor
from backend.env_manager import manager as env_manager
from backend.plugins import manager as plugin_manager
import psutil

logger = logging.getLogger(__name__)

app = FastAPI(title="Discord AI Bot", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_manager = AIManager()

# Serve static files (frontend)
FRONTEND_DIR = os.environ.get("FRONTEND_DIR", "/workspaces/y/frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    await init_db()
    await plugin_manager.load_all()
    asyncio.create_task(scheduler.start())
    logger.info("Startup complete")


@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0"}


# ===== AI ENGINE ENDPOINTS =====
@app.get("/status")
async def status():
    return {
        "engine": ai_manager.current_name,
        "engines": list(ai_manager.engines.keys()),
    }


@app.post("/switch_engine/{name}")
async def switch_engine(name: str):
    ok = await ai_manager.switch_engine(name)
    return {"ok": ok, "engine": ai_manager.current_name}


@app.post("/generate")
async def generate(prompt: dict):
    text = await ai_manager.generate(prompt.get("text", ""), metadata=prompt.get("meta"))
    monitor.add_log("INFO", f"Generated text for prompt")
    return {"text": text}


# ===== MEMORY ENDPOINTS =====
@app.post("/memory")
async def add_memory(item: dict):
    owner = item.get("owner")
    key = item.get("key")
    value = item.get("value")
    importance = float(item.get("importance", 1.0))
    if not owner or not key:
        raise HTTPException(status_code=400, detail="owner and key required")
    m = await memory_store.add(owner, key, value, importance)
    monitor.add_log("INFO", f"Memory added: {owner}/{key}")
    return {"ok": True, "id": m.id}


@app.get("/memory/{owner}")
async def list_memory(owner: str):
    rows = await memory_store.list_for_owner(owner)
    return [
        {
            "id": r.id,
            "key": r.key,
            "value": r.value,
            "importance": r.importance,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]


@app.delete("/memory/{mem_id}")
async def delete_memory(mem_id: int):
    await memory_store.delete(mem_id)
    monitor.add_log("INFO", f"Memory deleted: {mem_id}")
    return {"ok": True}


@app.post("/memory/{owner}/export")
async def export_memory(owner: str):
    data = await memory_store.export_owner(owner)
    return {"ok": True, "data": data}


@app.post("/memory/{owner}/import")
async def import_memory(owner: str, payload: dict):
    data = payload.get("data")
    if not data:
        raise HTTPException(status_code=400, detail="data required")
    await memory_store.import_owner(owner, data)
    monitor.add_log("INFO", f"Memory imported for: {owner}")
    return {"ok": True}


@app.post("/memory/decay")
async def decay_memory(payload: dict):
    days = payload.get("days", 30)
    await memory_store.decay(days=days)
    monitor.add_log("INFO", f"Memory decay run for {days} days")
    return {"ok": True}


# ===== PERSONALITY & MOOD ENDPOINTS =====
@app.get("/personality/presets")
async def list_presets():
    return {"presets": await personality_manager.list_presets()}


@app.post("/personality/override/{server_id}")
async def set_override(server_id: str, payload: dict):
    await personality_manager.set_override(server_id, payload)
    monitor.add_log("INFO", f"Personality override set for: {server_id}")
    return {"ok": True}


@app.get("/personality/{server_id}")
async def get_profile(server_id: str):
    profile = await personality_manager.get_profile_for_server(server_id)
    mood = await personality_manager.get_mood(server_id)
    return {"profile": profile, "mood": mood}


@app.post("/personality/{server_id}/mood")
async def set_mood(server_id: str, payload: dict):
    mood = payload.get("mood")
    if not mood:
        raise HTTPException(status_code=400, detail="mood required")
    await personality_manager.set_mood(server_id, mood)
    monitor.add_log("INFO", f"Mood set to {mood} for: {server_id}")
    return {"ok": True}


# ===== EXPRESSION ENDPOINTS =====
@app.get("/expression/emojis/{mood}")
async def get_emojis(mood: str):
    emojis = expression_engine.get_emojis_for_mood(mood)
    return {"mood": mood, "emojis": emojis}


@app.post("/expression/apply_mood")
async def apply_mood_expr(payload: dict):
    text = payload.get("text", "")
    mood = payload.get("mood", "neutral")
    result = expression_engine.apply_mood_expression(text, mood)
    return {"original": text, "transformed": result}


# ===== RELATIONSHIP ENDPOINTS =====
@app.get("/relationship/{user_id}")
async def get_relationship(user_id: str):
    score = await relationship_manager.get_score(user_id)
    return score.to_dict()


@app.post("/relationship/{user_id}/update")
async def update_relationship(user_id: str, payload: dict):
    sentiment = float(payload.get("sentiment", 0.0))
    is_positive = payload.get("is_positive", True)
    await relationship_manager.update_interaction(user_id, sentiment, is_positive)
    score = await relationship_manager.get_score(user_id)
    return score.to_dict()


@app.get("/relationships/export")
async def export_relationships():
    data = await relationship_manager.export()
    return {"ok": True, "data": data}


# ===== IMAGE GENERATION ENDPOINTS =====
@app.post("/image/generate")
async def generate_image(payload: dict):
    prompt = payload.get("prompt", "")
    style = payload.get("style", "default")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt required")
    image_url = await image_generator.generate(prompt, style)
    monitor.add_log("INFO", f"Image generated for prompt")
    return {"ok": bool(image_url), "image_url": image_url}


# ===== LANGUAGE ENDPOINTS =====
@app.get("/languages")
async def list_languages():
    return language_manager.list_languages()


@app.post("/language/server/{server_id}")
async def set_server_language(server_id: str, payload: dict):
    lang = payload.get("language")
    if not lang:
        raise HTTPException(status_code=400, detail="language required")
    ok = language_manager.set_server_language(server_id, lang)
    if not ok:
        raise HTTPException(status_code=400, detail="Unknown language")
    monitor.add_log("INFO", f"Server language set to {lang} for: {server_id}")
    return {"ok": True}


@app.post("/language/user/{user_id}")
async def set_user_language(user_id: str, payload: dict):
    lang = payload.get("language")
    if not lang:
        raise HTTPException(status_code=400, detail="language required")
    ok = language_manager.set_user_language(user_id, lang)
    if not ok:
        raise HTTPException(status_code=400, detail="Unknown language")
    return {"ok": True}


# ===== CONVERSATION SCORING ENDPOINTS =====
@app.post("/conversation/{conv_id}/add")
async def add_conv_message(conv_id: str, payload: dict):
    if conv_id not in conversation_scorer.conversations:
        await conversation_scorer.create_conversation(conv_id)
    conv = conversation_scorer.conversations[conv_id]
    role = payload.get("role", "user")
    content = payload.get("content", "")
    sentiment = float(payload.get("sentiment", 0.0))
    conv.add_message(role, content, sentiment)
    return {"ok": True}


@app.get("/conversation/{conv_id}/score")
async def get_conv_score(conv_id: str):
    return await conversation_scorer.score_conversation(conv_id)


# ===== MONITORING ENDPOINTS =====
@app.get("/health")
async def health_check():
    return monitor.health_check()


@app.get("/uptime")
async def uptime():
    return monitor.get_uptime()


@app.get("/logs")
async def get_logs(limit: int = 100):
    return {"logs": monitor.get_logs(limit)}


@app.post("/restart")
async def restart():
    monitor.add_log("WARNING", "Restart requested")
    asyncio.create_task(monitor.restart_bot())
    return {"ok": True, "restarting": True}


@app.get("/metrics")
async def metrics():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return {
        "engine": ai_manager.current_name,
        "cpu_percent": cpu,
        "memory_percent": mem,
        "disk_percent": disk,
        "uptime_seconds": int((monitor.get_uptime()["uptime_seconds"])),
    }


# ===== ENVIRONMENT ENDPOINTS =====
@app.get("/env")
async def get_env():
    return await env_manager.get_all()


@app.post("/env/{key}")
async def set_env(key: str, payload: dict):
    value = payload.get("value")
    if not value:
        raise HTTPException(status_code=400, detail="value required")
    ok = await env_manager.set_var(key, value)
    monitor.add_log("INFO", f"Env var set: {key}")
    return {"ok": ok}


@app.post("/env/reload")
async def reload_env():
    await env_manager.reload()
    monitor.add_log("INFO", "Environment reloaded")
    return {"ok": True}


# ===== SCHEDULER ENDPOINTS =====
@app.get("/scheduler/events")
async def list_events():
    return await scheduler.list_events()


# ===== PLUGIN ENDPOINTS =====
@app.get("/plugins")
async def list_plugins():
    return await plugin_manager.list_plugins()


@app.post("/plugin/load/{plugin_name}")
async def load_plugin(plugin_name: str):
    ok = await plugin_manager.load_plugin(plugin_name)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to load plugin")
    monitor.add_log("INFO", f"Plugin loaded: {plugin_name}")
    return {"ok": True}


@app.post("/plugin/unload/{plugin_name}")
async def unload_plugin(plugin_name: str):
    ok = await plugin_manager.unload_plugin(plugin_name)
    if not ok:
        raise HTTPException(status_code=400, detail="Plugin not found")
    monitor.add_log("INFO", f"Plugin unloaded: {plugin_name}")
    return {"ok": True}


@app.post("/plugin/{plugin_name}/skill/{skill_name}")
async def execute_skill(plugin_name: str, skill_name: str, payload: dict = None):
    try:
        result = await plugin_manager.execute_skill(plugin_name, skill_name, **(payload or {}))
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== WEBSOCKET =====
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            action = data.get("action")
            if action == "status":
                await ws.send_json({"engine": ai_manager.current_name})
            elif action == "switch":
                name = data.get("name")
                ok = await ai_manager.switch_engine(name)
                await ws.send_json({"switched": ok, "engine": ai_manager.current_name})
            elif action == "metrics":
                cpu = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory().percent
                await ws.send_json({"cpu_percent": cpu, "memory_percent": mem})
    except Exception as e:
        logger.exception(f"WebSocket error: {e}")
        await ws.close()


def start_services():
    loop = asyncio.get_event_loop()
    loop.create_task(start_discord_bot(ai_manager))


if __name__ == "__main__":
    import uvicorn

    start_services()
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        log_level="info",
    )
