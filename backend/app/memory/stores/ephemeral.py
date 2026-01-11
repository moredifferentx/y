from typing import Dict, Any
import time


class EphemeralMemoryStore:
    """
    In-memory short-term context (non-persistent).
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any):
        self._store[key] = {"value": value, "ts": time.time()}

    def get(self, key: str, default=None):
        return self._store.get(key, {}).get("value", default)

    def clear(self):
        self._store.clear()
