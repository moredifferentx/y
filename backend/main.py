import asyncio
import uvicorn
from fastapi import FastAPI

from app.discord import DiscordBot
from app.core.config import Config
from app.memory import MEMORY  # imported but NOT re-initialized

from app.ai.engines.cloud import register_cloud_engines
from app.ai.engine_router import ENGINE_ROUTER
from app.ai.engines.ollama.engine import OllamaEngine
from app.ai.engine_registry import ENGINE_REGISTRY

from app.dashboard import dashboard_api, websocket_endpoint
from app.dashboard.ws import start_dashboard_ws
from app.monitoring import log


# ==================================================
# FASTAPI APP (DASHBOARD BACKEND)
# ==================================================

app = FastAPI(title="Discord AI Dashboard")

app.include_router(dashboard_api, prefix="/api/dashboard")
app.add_api_websocket_route("/ws/dashboard", websocket_endpoint)


# ==================================================
# DISCORD BOT TASK
# ==================================================

async def start_discord_bot():
    try:
        bot = DiscordBot()
        await bot.start(Config.get("DISCORD_TOKEN"))
    except Exception as e:
        log(f"[discord] Bot crashed: {e}")


# ==================================================
# FASTAPI STARTUP (FINAL FIX)
# ==================================================

@app.on_event("startup")
async def on_startup():
    # ---- Load config ----
    Config.load()

    # ❌ DO NOT call MEMORY.initialize() here
    # It is already initialized elsewhere (aiosqlite cannot be started twice)

    # ---- Register AI engines ----
    await ENGINE_REGISTRY.register(OllamaEngine())

    try:
        register_cloud_engines()  # sync
    except Exception as e:
        log(f"[ai] Cloud engine registration failed: {e}")

    # ---- Default routing ----
    await ENGINE_ROUTER.set_active("ollama")
    await ENGINE_ROUTER.set_fallback("openai")

    # ---- Start dashboard WS listeners ----
    await start_dashboard_ws()

    # ---- Start Discord bot (non-blocking) ----
    asyncio.create_task(start_discord_bot())

    log("Application startup complete")


# ==================================================
# ENTRYPOINT (CORRECT)
# ==================================================

if __name__ == "__main__":
    Config.load()

    uvicorn.run(
        app,  # ✅ pass app object
        host="0.0.0.0",
        port=int(Config.get("DASHBOARD_PORT", 8000)),
        log_level="info",
    )
