import time
from typing import Dict, Any
import google.generativeai as genai

from app.ai.engines.base import BaseAIEngine
from app.core.config import Config


class GeminiEngine(BaseAIEngine):
    def __init__(self):
        super().__init__(engine_id="gemini")
        genai.configure(api_key=Config.get("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(
            Config.get("GEMINI_MODEL", "gemini-1.5-flash")
        )
        self._requests = 0
        self._latency = 0.0

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        start = time.perf_counter()
        try:
            response = await self.model.generate_content_async(
                f"{context}\n\n{prompt}"
            )
            self.healthy = True
            return response.text
        except Exception:
            self.healthy = False
            raise
        finally:
            self._requests += 1
            self._latency += time.perf_counter() - start

    async def health_check(self) -> bool:
        return bool(Config.get("GEMINI_API_KEY"))

    def metrics(self) -> Dict[str, Any]:
        avg = self._latency / self._requests if self._requests else 0.0
        return {
            "engine": "gemini",
            "requests": self._requests,
            "avg_latency": avg,
            "healthy": self.healthy,
        }
