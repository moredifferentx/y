import time
import httpx
from typing import Dict, Any, Optional

from app.core.config import Config
from ..base import BaseAIEngine
from .metrics import OllamaMetrics
from .health import OllamaHealth


class OllamaEngine(BaseAIEngine):
    """
    Ollama local LLM engine.

    - Connects via HTTP to a locally hosted Ollama server
    - Model and endpoint are configurable via .env
    - Supports ANY Ollama model name (llama3, llama3:8b, mistral, etc.)
    """

    def __init__(
        self,
        model: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        super().__init__(engine_id="ollama")

        # Load from environment with safe defaults
        self.model = model or Config.get("OLLAMA_MODEL", "llama3")
        self.endpoint = endpoint or Config.get(
            "OLLAMA_HOST", "http://localhost:11434"
        )

        self.metrics_collector = OllamaMetrics()
        self.health_checker = OllamaHealth(self.endpoint)

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        start = time.perf_counter()

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            try:
                response = await client.post(
                    f"{self.endpoint}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"Ollama request failed: {e}")

            data = response.json()

        duration = time.perf_counter() - start

        # Token estimate based on prompt length (simple + safe)
        self.metrics_collector.record(duration, len(prompt))

        return data.get("response", "").strip()

    async def health_check(self) -> bool:
        self.healthy = await self.health_checker.check()
        return self.healthy

    def metrics(self) -> Dict[str, Any]:
        snapshot = self.metrics_collector.snapshot()
        snapshot.update(
            {
                "model": self.model,
                "endpoint": self.endpoint,
            }
        )
        return snapshot
