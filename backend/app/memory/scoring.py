class ImportanceScorer:
    """
    Scores memory importance (0.0 – 1.0).
    """

    @staticmethod
    def score(
        emotional_intensity: float = 0.0,
        repetition: int = 1,
        explicit: bool = False,
    ) -> float:
        score = 0.1
        score += emotional_intensity * 0.5
        score += min(repetition * 0.1, 0.3)
        if explicit:
            score += 0.2
        return min(score, 1.0)
