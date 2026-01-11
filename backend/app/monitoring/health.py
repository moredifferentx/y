from app.ai.engine_registry import ENGINE_REGISTRY

async def health_check():
    engines = await ENGINE_REGISTRY.list()
    status = {}
    for name, engine in engines.items():
        try:
            status[name] = await engine.health_check()
        except Exception:
            status[name] = False
    return {"status": "ok", "engines": status}
