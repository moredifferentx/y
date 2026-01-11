import time
from typing import Dict, Any
import openai

from app.ai.engines.base import BaseAIEngine
from app.core.config import Config


class OpenAIEngine(BaseAIEngine):
    def __init__(self):
        super().__init__(engine_id="openai")
        openai.api_key = Config.get("OPENAI_API_KEY")
        self.model = Config.get("OPENAI_MODEL", "gpt-4o-mini")
        self._requests = 0
        self._latency = 0.0

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        start = time.perf_counter()
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": str(context)},
                    {"role": "user", "content": prompt},
                ],
            )
            self.healthy = True
            return response.choices[0].message.content
        except Exception:
            self.healthy = False
            raise
        finally:
            self._requests += 1
            self._latency += time.perf_counter() - start

    async def health_check(self) -> bool:
        return bool(Config.get("OPENAI_API_KEY"))

    def metrics(self) -> Dict[str, Any]:
        avg = self._latency / self._requests if self._requests else 0.0
        return {
            "engine": "openai",
            "requests": self._requests,
            "avg_latency": avg,
            "healthy": self.healthy,
        }
