from typing import Dict, Any


class ContextManager:
    """
    Normalizes context before sending to engines.
    """

    @staticmethod
    def build(
        memory: Dict[str, Any],
        personality: Dict[str, Any],
        mood: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "memory": memory,
            "personality": personality,
            "mood": mood,
        }
