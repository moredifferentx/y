import httpx
from app.core.config import Config


class OllamaHealth:
    """
    Health checker for Ollama local LLM.

    - Verifies Ollama server is reachable
    - Optionally verifies configured model exists
    """

    def __init__(self, endpoint: str | None = None):
        self.endpoint = endpoint or Config.get(
            "OLLAMA_HOST", "http://localhost:11434"
        )
        self.model = Config.get("OLLAMA_MODEL")

    async def check(self) -> bool:
        """
        Returns True if:
        - Ollama server is reachable
        - AND (if OLLAMA_MODEL is set) model exists
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.endpoint}/api/tags")
                r.raise_for_status()

                # If no model specified, server health is enough
                if not self.model:
                    return True

                data = r.json()
                models = [m["name"] for m in data.get("models", [])]

                return self.model in models

        except Exception:
            return False
