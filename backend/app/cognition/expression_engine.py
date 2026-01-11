import asyncio
import random
from typing import List


class ExpressionEngine:
    def __init__(self):
        pass

    async def typing_delay(self, base: float = 0.4):
        await asyncio.sleep(base + random.uniform(0.1, 0.6))

    def split_message(self, text: str, max_len: int = 1800) -> List[str]:
        if len(text) <= max_len:
            return [text]

        chunks = []
        while text:
            chunks.append(text[:max_len])
            text = text[max_len:]
        return chunks

    def emoji_for_mood(self, mood: str) -> str:
        return {
            "happy": "😊",
            "sad": "😔",
            "angry": "😠",
            "playful": "😄",
            "focused": "🧠",
            "neutral": "",
        }.get(mood, "")
