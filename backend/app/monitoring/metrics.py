from app.ai.engine_registry import ENGINE_REGISTRY

async def collect_engine_metrics():
    engines = await ENGINE_REGISTRY.list()
    data = {}
    for name, engine in engines.items():
        try:
            data[name] = engine.metrics()
        except Exception as e:
            data[name] = {"error": str(e)}
    return data
