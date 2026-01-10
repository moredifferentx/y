"""Relationship and trust scoring system."""
import asyncio
from datetime import datetime, timedelta
from typing import Dict

class RelationshipScore:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.trust = 50.0  # 0-100
        self.affinity = 50.0  # 0-100
        self.interaction_count = 0
        self.last_interaction = datetime.utcnow()
        self.friend_bias = False
        self.enemy_bias = False

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "trust": self.trust,
            "affinity": self.affinity,
            "interaction_count": self.interaction_count,
            "friend_bias": self.friend_bias,
            "enemy_bias": self.enemy_bias,
        }


class RelationshipManager:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.scores: Dict[str, RelationshipScore] = {}

    async def get_score(self, user_id: str) -> RelationshipScore:
        async with self.lock:
            if user_id not in self.scores:
                self.scores[user_id] = RelationshipScore(user_id)
            return self.scores[user_id]

    async def update_interaction(self, user_id: str, sentiment: float = 0.0, is_positive: bool = True):
        """Update after interaction. Sentiment: -1 to 1. Affects trust/affinity."""
        score = await self.get_score(user_id)
        async with self.lock:
            score.interaction_count += 1
            score.last_interaction = datetime.utcnow()

            # Update trust/affinity based on sentiment
            if is_positive:
                score.trust = min(100.0, score.trust + sentiment * 5)
                score.affinity = min(100.0, score.affinity + sentiment * 3)
            else:
                score.trust = max(0.0, score.trust - abs(sentiment) * 5)
                score.affinity = max(0.0, score.affinity - abs(sentiment) * 3)

            # Auto-set biases at thresholds
            if score.trust > 80 and score.affinity > 75:
                score.friend_bias = True
                score.enemy_bias = False
            elif score.trust < 30 and score.affinity < 25:
                score.enemy_bias = True
                score.friend_bias = False
            else:
                score.friend_bias = False
                score.enemy_bias = False

    async def decay_relationships(self):
        """Decay relationships over time (daily background task)."""
        async with self.lock:
            now = datetime.utcnow()
            for score in self.scores.values():
                days_since = (now - score.last_interaction).days
                if days_since > 0:
                    decay = min(days_since * 2, 10)  # max 10 points per day
                    score.affinity = max(0.0, score.affinity - decay)

    async def export(self):
        """Export all relationship data."""
        return {uid: s.to_dict() for uid, s in self.scores.items()}


manager = RelationshipManager()
