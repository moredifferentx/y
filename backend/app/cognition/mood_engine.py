import time
from typing import Dict


MOODS = ("happy", "neutral", "sad", "angry", "playful", "focused")


class MoodEngine:
    def __init__(self):
        self.current = "neutral"
        self.intensity = 0.5
        self.last_update = time.time()
        self.override: str | None = None

    def set_override(self, mood: str):
        if mood in MOODS:
            self.override = mood
            self.current = mood

    def clear_override(self):
        self.override = None

    def update_from_emotion(self, emotion: str, intensity: float):
        if self.override:
            return

        mapping = {
            "joy": "happy",
            "anger": "angry",
            "sadness": "sad",
            "play": "playful",
            "focus": "focused",
        }
        self.current = mapping.get(emotion, "neutral")
        self.intensity = max(0.1, min(intensity, 1.0))
        self.last_update = time.time()

    def snapshot(self) -> Dict[str, float | str]:
        return {
            "mood": self.current,
            "intensity": self.intensity,
        }
