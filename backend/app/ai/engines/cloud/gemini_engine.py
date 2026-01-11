from typing import Dict, Any
import time

from app.ai.engines.base import BaseAIEngine
from app.core.config import Config


# --- SAFE IMPORT (legacy + future compatible) -------------------------------

try:
    import google.generativeai as genai  # legacy SDK (deprecated but still works)
except ImportError:
    try:
        from google import genai  # new SDK
    except ImportError:
        genai = None


class GeminiEngine(BaseAIEngine):
    def __init__(self):
        super().__init__(engine_id="gemini")

        if genai is None:
            raise RuntimeError(
                "Gemini SDK not installed. Install google-generativeai or google-genai."
            )

        api_key = Config.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        # Legacy SDK configuration
        if hasattr(genai, "configure"):
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                Config.get("GEMINI_MODEL", "gemini-1.5-flash")
            )
        else:
            # Placeholder for new SDK path (future-proof)
            self.client = genai.Client(api_key=api_key)
            self.model = self.client.models.get(
                Config.get("GEMINI_MODEL", "gemini-1.5-flash")
            )

        self._requests = 0
        self._latency = 0.0

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        start = time.perf_counter()

        try:
            payload = f"{context}\n\n{prompt}"

            # Legacy async API
            if hasattr(self.model, "generate_content_async"):
                response = await self.model.generate_content_async(payload)
                text = response.text
            else:
                # New SDK (sync for now, wrapped safely)
                response = self.model.generate_content(payload)
                text = response.text

            self.healthy = True
            return text

        except Exception:
            self.healthy = False
            raise

        finally:
            self._requests += 1
            self._latency += time.perf_counter() - start

    async def health_check(self) -> bool:
        return bool(Config.get("GEMINI_API_KEY")) and genai is not None

    def metrics(self) -> Dict[str, Any]:
        avg = self._latency / self._requests if self._requests else 0.0
        return {
            "engine": "gemini",
            "requests": self._requests,
            "avg_latency": avg,
            "healthy": self.healthy,
        }
