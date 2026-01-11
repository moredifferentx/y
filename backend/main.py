# ==================================================
# ENV MUST LOAD FIRST (CRITICAL)
# ==================================================
from dotenv import load_dotenv
load_dotenv()

# ==================================================
# STANDARD LIBS
# ==================================================
import os
import asyncio
import uvicorn
from fastapi import FastAPI

# ==================================================
# APP IMPORTS (SAFE AFTER load_dotenv)
# ==================================================
from app.discord import DiscordBot
from app.core.config import Config
from app.memory import MEMORY  # imported but NOT re-initialized

from app.ai.engines.cloud import register_cloud_engines
from app.ai.engine_router import ENGINE_ROUTER
from app.ai.engines.ollama.engine import OllamaEngine
from app.ai.engine_registry import ENGINE_REGISTRY

from app.dashboard import dashboard_api, websocket_endpoint
from app.dashboard.ws import start_dashboard_ws

# NOTE: do NOT use async log() for critical startup paths


# ==================================================
# FASTAPI APP (DASHBOARD BACKEND)
# ==================================================
app = FastAPI(title="Discord AI Dashboard")

app.include_router(dashboard_api, prefix="/api/dashboard")
app.add_api_websocket_route("/ws/dashboard", websocket_endpoint)


# ==================================================
# DISCORD BOT TASK (LOUD + SAFE)
# ==================================================
async def start_discord_bot():
    print("[discord] Initializing Discord bot...")

    try:
        bot = DiscordBot()

        print("[discord] Bot instance created")
        print("[discord] Token present:", bool(bot.token))

        await bot.start(bot.token)

    except Exception as e:
        # NEVER swallow this again
        print("[discord][FATAL] Bot failed to start:")
        print(repr(e))


# ==================================================
# FASTAPI STARTUP
# ==================================================
@app.on_event("startup")
async def on_startup():
    print("[startup] Loading configuration")
    Config.load()

    # ---- MEMORY already initialized at import time ----

    print("[startup] Registering AI engines")
    await ENGINE_REGISTRY.register(OllamaEngine())

    try:
        register_cloud_engines()
    except Exception as e:
        print("[ai][warn] Cloud engine registration failed:", e)

    print("[startup] Setting AI routing")
    await ENGINE_ROUTER.set_active("ollama")
    await ENGINE_ROUTER.set_fallback("openai")

    print("[startup] Starting dashboard websocket")
    asyncio.create_task(start_dashboard_ws())

    print("[startup] Starting Discord bot task")
    asyncio.create_task(start_discord_bot())

    print("[startup] Application startup complete")


# ==================================================
# ENTRYPOINT
# ==================================================
if __name__ == "__main__":
    print("[entrypoint] Booting backend")

    Config.load()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(Config.get("DASHBOARD_PORT", 8000)),
        log_level="info",
    )
