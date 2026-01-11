import time
import httpx
from typing import Dict, Any
from ..base import BaseAIEngine
from .metrics import OllamaMetrics
from .health import OllamaHealth


class OllamaEngine(BaseAIEngine):
    def __init__(self, model: str, endpoint: str = "http://localhost:11434"):
        super().__init__(engine_id="ollama")
        self.model = model
        self.endpoint = endpoint
        self.metrics_collector = OllamaMetrics()
        self.health_checker = OllamaHealth(endpoint)

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()

        duration = time.perf_counter() - start
        self.metrics_collector.record(duration, len(prompt))
        return data.get("response", "")

    async def health_check(self) -> bool:
        self.healthy = await self.health_checker.check()
        return self.healthy

    def metrics(self) -> Dict[str, Any]:
        return self.metrics_collector.snapshot()
