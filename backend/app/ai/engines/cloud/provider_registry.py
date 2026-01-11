"""
DEPRECATED.
This module is not used.
Kept for historical reference only.
"""

from typing import Dict
from .schemas import ProviderSchema


class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, Dict] = {}

    def register(
        self,
        name: str,
        base_url: str,
        api_key: str,
        schema: ProviderSchema,
        headers: Dict[str, str],
    ):
        self._providers[name] = {
            "base_url": base_url,
            "api_key": api_key,
            "schema": schema,
            "headers": headers,
        }

    def get(self, name: str) -> Dict:
        return self._providers[name]

    def list(self):
        return list(self._providers.keys())


PROVIDERS = ProviderRegistry()
