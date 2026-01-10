import os
import httpx


class OpenAIClient:
    def __init__(self, model: str = None):
        self.model = model or os.environ.get("CLOUD_MODEL", "gpt-4o-mini")
        self.key = os.environ.get("OPENAI_API_KEY")
        self.base = "https://api.openai.com/v1/chat/completions"

    async def generate(self, prompt: str, metadata: dict) -> str:
        if not self.key:
            raise RuntimeError("OpenAI API key not configured")
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(self.base, headers=headers, json=body)
            r.raise_for_status()
            data = r.json()
            # Pull out text safely
            choices = data.get("choices")
            if choices and len(choices) > 0:
                return choices[0].get("message", {}).get("content", "")
            return data.get("error", {}).get("message", "")
