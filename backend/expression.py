"""Expression system: typing styles, reactions, emojis based on mood and context."""
import asyncio
import random
from typing import Dict, List

MOOD_EMOJIS = {
    "happy": ["😊", "🎉", "😄", "✨", "🌟"],
    "neutral": ["😐", "👍", "📝", "🤔"],
    "sad": ["😢", "💔", "😔", "😞"],
    "angry": ["😠", "🔥", "💢", "😤"],
    "playful": ["😄", "🎮", "😆", "🤪", "😜"],
    "focused": ["🎯", "💪", "⚡", "🧠"],
}

MOOD_STYLES = {
    "happy": {"typing_speed": 0.015, "emoji_freq": 0.6, "caps": 0.2, "exclamation": 0.5},
    "neutral": {"typing_speed": 0.02, "emoji_freq": 0.2, "caps": 0.05, "exclamation": 0.1},
    "sad": {"typing_speed": 0.025, "emoji_freq": 0.1, "caps": 0.0, "exclamation": 0.0},
    "angry": {"typing_speed": 0.01, "emoji_freq": 0.4, "caps": 0.4, "exclamation": 0.7},
    "playful": {"typing_speed": 0.012, "emoji_freq": 0.7, "caps": 0.3, "exclamation": 0.6},
    "focused": {"typing_speed": 0.022, "emoji_freq": 0.1, "caps": 0.1, "exclamation": 0.2},
}


class ExpressionEngine:
    def __init__(self):
        self.reaction_cache: Dict[str, List[str]] = {}

    def get_emojis_for_mood(self, mood: str) -> List[str]:
        """Get emoji list for a specific mood."""
        return MOOD_EMOJIS.get(mood, MOOD_EMOJIS["neutral"])

    def get_typing_delay(self, mood: str, text_length: int) -> float:
        """Calculate typing delay based on mood and text length."""
        style = MOOD_STYLES.get(mood, MOOD_STYLES["neutral"])
        base_delay = style["typing_speed"]
        return max(0.5, min(5.0, text_length * base_delay))

    def apply_mood_expression(self, text: str, mood: str) -> str:
        """Apply mood-based expression to text (caps, exclamations, etc)."""
        style = MOOD_STYLES.get(mood, MOOD_STYLES["neutral"])

        # Random capitalization
        if random.random() < style["caps"]:
            text = text.upper()

        # Add exclamation marks
        if random.random() < style["exclamation"]:
            text = text.rstrip(".!?") + "!" * random.randint(1, 3)

        # Add emoji
        if random.random() < style["emoji_freq"]:
            emojis = self.get_emojis_for_mood(mood)
            text += " " + random.choice(emojis)

        return text

    def get_reaction_emojis(self, mood: str, context: str = "") -> List[str]:
        """Get reaction emojis based on mood and context."""
        base_emojis = self.get_emojis_for_mood(mood)
        # Add context-aware emojis
        if "thanks" in context.lower() or "thank" in context.lower():
            base_emojis = ["🙏", "👍", "💯"] + base_emojis
        if "sad" in context.lower() or "sorry" in context.lower():
            base_emojis = ["💔", "😔", "🤝"] + base_emojis
        if "love" in context.lower() or "like" in context.lower():
            base_emojis = ["❤️", "😍", "💕"] + base_emojis
        return base_emojis[:5]  # limit to 5


engine = ExpressionEngine()
