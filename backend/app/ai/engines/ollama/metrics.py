import time
from typing import Dict


class OllamaMetrics:
    def __init__(self):
        self.requests = 0
        self.total_latency = 0.0
        self.last_request_ts = None

    def record(self, latency: float, tokens: int):
        self.requests += 1
        self.total_latency += latency
        self.last_request_ts = time.time()

    def snapshot(self) -> Dict[str, float]:
        avg_latency = (
            self.total_latency / self.requests if self.requests else 0.0
        )
        return {
            "requests": self.requests,
            "avg_latency": avg_latency,
            "last_request_ts": self.last_request_ts,
        }
