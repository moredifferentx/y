from typing import Dict, Any


DEFAULT_PERSONALITY = {
    "friendly": 0.7,
    "logical": 0.6,
    "chaotic": 0.2,
    "empathetic": 0.7,
    "formality": 0.4,
    "humor": 0.5,
}


class Personality:
    def __init__(self, traits: Dict[str, float] | None = None):
        self.traits = dict(DEFAULT_PERSONALITY)
        if traits:
            self.update(traits)

    def update(self, traits: Dict[str, float]) -> None:
        for k, v in traits.items():
            if 0.0 <= v <= 1.0:
                self.traits[k] = v

    def snapshot(self) -> Dict[str, float]:
        return dict(self.traits)

    def style_hint(self) -> str:
        """
        Compact style instruction injected into context.
        """
        return (
            f"Tone: {'formal' if self.traits['formality'] > 0.6 else 'casual'}, "
            f"Empathy: {self.traits['empathetic']}, "
            f"Humor: {self.traits['humor']}"
        )
