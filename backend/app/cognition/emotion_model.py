from typing import Dict


class EmotionModel:
    """
    Simple deterministic emotion inference.
    Replaceable later with ML if desired.
    """

    KEYWORDS = {
        "joy": ["love", "great", "awesome", "thanks"],
        "anger": ["hate", "stupid", "angry", "annoying"],
        "sadness": ["sad", "depressed", "tired"],
        "play": ["lol", "haha", "funny"],
        "focus": ["explain", "details", "serious"],
    }

    def infer(self, text: str) -> Dict[str, float]:
        text = text.lower()
        scores = {k: 0.0 for k in self.KEYWORDS}

        for emotion, words in self.KEYWORDS.items():
            for w in words:
                if w in text:
                    scores[emotion] += 0.25

        return scores
