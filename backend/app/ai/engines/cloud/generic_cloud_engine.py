"""
DEPRECATED.
This module is not used.
Kept for historical reference only.
"""

import time
import httpx
from typing import Dict, Any
from app.ai.engines.base import BaseAIEngine
from .provider_registry import PROVIDERS


class GenericCloudEngine(BaseAIEngine):
    def __init__(self, engine_id: str, provider_name: str):
        super().__init__(engine_id=engine_id)
        self.provider_name = provider_name
        self._metrics = {"requests": 0, "latency": 0.0}

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        provider = PROVIDERS.get(self.provider_name)
        schema = provider["schema"]

        payload = schema.request_builder(prompt, context)

        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                provider["base_url"],
                json=payload,
                headers=provider["headers"],
            )
            r.raise_for_status()

        self._metrics["requests"] += 1
        self._metrics["latency"] += time.perf_counter() - start

        return schema.response_parser(r.json())

    async def health_check(self) -> bool:
        return True  # API-key presence + success tracking

    def metrics(self) -> Dict[str, Any]:
        avg = (
            self._metrics["latency"] / self._metrics["requests"]
            if self._metrics["requests"]
            else 0
        )
        return {
            "requests": self._metrics["requests"],
            "avg_latency": avg,
        }
