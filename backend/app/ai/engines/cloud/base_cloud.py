"""
DEPRECATED.
This module is not used.
Kept for historical reference only.
"""

import time
from typing import Dict, Any
from app.ai.engines.base import BaseAIEngine


class BaseCloudEngine(BaseAIEngine):
    """
    Base class for all cloud-based AI engines.
    """

    def __init__(self, engine_id: str):
        super().__init__(engine_id=engine_id)
        self._requests = 0
        self._total_latency = 0.0

    def _record(self, latency: float):
        self._requests += 1
        self._total_latency += latency

    def metrics(self) -> Dict[str, Any]:
        avg_latency = (
            self._total_latency / self._requests if self._requests else 0.0
        )
        return {
            "requests": self._requests,
            "avg_latency": avg_latency,
            "healthy": self.healthy,
        }
