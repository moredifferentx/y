import time


class MemoryDecay:
    """
    Importance decay over time.
    """

    @staticmethod
    def apply(importance: float, created_at: float, half_life: float = 86400) -> float:
        age = time.time() - created_at
        decay_factor = 0.5 ** (age / half_life)
        return importance * decay_factor
