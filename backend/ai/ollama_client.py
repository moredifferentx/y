import os
import httpx


class OllamaClient:
    def __init__(self, model: str = None):
        self.model = model or os.environ.get("OLLAMA_MODEL", "llama2")
        self.base = os.environ.get("OLLAMA_BASE", "http://localhost:11434")

    async def generate(self, prompt: str, metadata: dict) -> str:
        url = f"{self.base}/api/generate"
        payload = {"model": self.model, "prompt": prompt}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            # Ollama returns 'output' or 'choices' depending on versions; be forgiving
            if isinstance(data, dict):
                return data.get("output") or (data.get("choices") and data.get("choices")[0].get("content")) or ""
            return str(data)
