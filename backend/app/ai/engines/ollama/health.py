import httpx


class OllamaHealth:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    async def check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.endpoint}/api/tags")
                return r.status_code == 200
        except Exception:
            return False
