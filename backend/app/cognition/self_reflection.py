from typing import Dict, Any
from app.memory import MEMORY


class SelfReflection:
    """
    Post-response reflection & memory consolidation.
    """

    async def reflect(
        self,
        user_id: str,
        content: str,
        emotion_scores: Dict[str, float],
    ):
        dominant = max(emotion_scores, key=emotion_scores.get, default=None)
        intensity = emotion_scores.get(dominant, 0.0) if dominant else 0.0

        if dominant and intensity > 0.4:
            await MEMORY.emotional.add(
                user_id=user_id,
                emotion=dominant,
                intensity=intensity,
            )
