"""
DEPRECATED.
This module is not used.
Kept for historical reference only.
"""

import time
from typing import Dict, Any
import anthropic
from app.core.config import Config
from .base_cloud import BaseCloudEngine


class AnthropicEngine(BaseCloudEngine):
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        super().__init__(engine_id="anthropic")
        self.client = anthropic.AsyncAnthropic(
            api_key=Config.get("ANTHROPIC_API_KEY")
        )
        self.model = model

    async def generate(self, prompt: str, context: Dict[str, Any]) -> str:
        start = time.perf_counter()

        try:
            msg = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system=str(context),
            )
            self.healthy = True
            return msg.content[0].text

        except Exception:
            self.healthy = False
            raise

        finally:
            self._record(time.perf_counter() - start)

    async def health_check(self) -> bool:
        return bool(Config.get("ANTHROPIC_API_KEY"))
