"""Image generation module using local or cloud APIs."""
import os
import base64
import httpx
from typing import Optional


class ImageGenerator:
    def __init__(self):
        self.cloud_key = os.environ.get("OPENAI_API_KEY")
        self.local_enabled = os.environ.get("IMAGE_LOCAL_ENABLED", "false").lower() == "true"
        self.local_endpoint = os.environ.get("IMAGE_LOCAL_ENDPOINT", "http://localhost:5000")

    async def generate(self, prompt: str, style: str = "default", size: str = "512x512") -> Optional[str]:
        """Generate image, returns base64 encoded image or URL."""
        if self.local_enabled:
            try:
                return await self._generate_local(prompt, style)
            except Exception:
                pass  # fallback to cloud

        if self.cloud_key:
            try:
                return await self._generate_openai(prompt, size)
            except Exception:
                pass

        return None

    async def _generate_local(self, prompt: str, style: str) -> Optional[str]:
        """Use local model (e.g., Stable Diffusion via ollama or similar)."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {"prompt": prompt, "style": style}
            r = await client.post(f"{self.local_endpoint}/generate", json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("image_url") or data.get("image_base64")

    async def _generate_openai(self, prompt: str, size: str) -> Optional[str]:
        """Use OpenAI's DALL-E API."""
        headers = {"Authorization": f"Bearer {self.cloud_key}"}
        body = {"prompt": prompt, "n": 1, "size": size, "response_format": "b64_json"}
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post("https://api.openai.com/v1/images/generations", headers=headers, json=body)
            r.raise_for_status()
            data = r.json()
            if data.get("data") and len(data["data"]) > 0:
                return "data:image/png;base64," + data["data"][0].get("b64_json", "")
        return None


generator = ImageGenerator()
