import asyncio
import uvicorn
from fastapi import FastAPI

from app.discord import DiscordBot
from app.core.config import Config
from app.memory import MEMORY

from app.ai.engines.cloud import register_cloud_engines
from app.ai.engine_router import ENGINE_ROUTER
from app.ai.engines.ollama.engine import OllamaEngine
from app.ai.engine_registry import ENGINE_REGISTRY

from app.dashboard import dashboard_api, websocket_endpoint


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
    bot = DiscordBot()
    await bot.start(Config.get("DISCORD_BOT_TOKEN"))


# ==================================================
# MAIN BOOTSTRAP
# ==================================================

async def main():
    # ---- Load config & memory ----
    Config.load()
    await MEMORY.initialize()

    # ---- Register AI engines ----
    await ENGINE_REGISTRY.register(OllamaEngine())
    await register_cloud_engines()

    # ---- Default routing ----
    await ENGINE_ROUTER.set_active("ollama")
    await ENGINE_ROUTER.set_fallback("openai")

    # ---- Start Discord bot (non-blocking) ----
    asyncio.create_task(start_discord_bot())

    # ---- Start FastAPI (dashboard) ----
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=int(Config.get("DASHBOARD_PORT", 8000)),
        log_level="info",
        loop="asyncio",
    )
    server = uvicorn.Server(config)
    await server.serve()


# ==================================================
# ENTRYPOINT
# ==================================================

if __name__ == "__main__":
    asyncio.run(main())
