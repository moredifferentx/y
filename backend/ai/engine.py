import asyncio
from .ollama_client import OllamaClient
from .cloud_client import OpenAIClient


class AIManager:
    def __init__(self):
        self.engines = {
            "ollama": OllamaClient(),
            "openai": OpenAIClient(),
        }
        self.current_name = "ollama"
        self.current = self.engines[self.current_name]
        self.lock = asyncio.Lock()

    async def switch_engine(self, name: str) -> bool:
        async with self.lock:
            if name not in self.engines:
                return False
            # create fresh instance to avoid shared state
            if name == "ollama":
                self.engines["ollama"] = OllamaClient()
            else:
                self.engines["openai"] = OpenAIClient()
            self.current_name = name
            self.current = self.engines[name]
            return True

    async def generate(self, prompt: str, metadata: dict | None = None) -> str:
        # Try current engine, fallback to cloud if it fails
        try:
            text = await self.current.generate(prompt, metadata or {})
            return text
        except Exception:
            # fallback path: if current isn't openai, try openai
            if self.current_name != "openai":
                try:
                    return await self.engines["openai"].generate(prompt, metadata or {})
                except Exception:
                    pass
            raise
