from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAIEngine(ABC):
    """
    Abstract base class for all AI engines.
    """

    def __init__(self, engine_id: str):
        self.engine_id = engine_id
        self.healthy: bool = True

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        context: Dict[str, Any],
    ) -> str:
        """
        Generate a response from the AI engine.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check whether the engine is healthy.
        """
        raise NotImplementedError

    @abstractmethod
    def metrics(self) -> Dict[str, Any]:
        """
        Return live performance metrics.
        """
        raise NotImplementedError

    async def shutdown(self) -> None:
        """
        Optional cleanup hook for hot-swap.
        """
        return
