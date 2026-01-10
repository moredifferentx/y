"""Conversation scoring and self-reflection system."""
import asyncio
from typing import Dict, List
from datetime import datetime


class ConversationAnalysis:
    def __init__(self, conversation_id: str):
        self.id = conversation_id
        self.messages: List[Dict] = []
        self.created_at = datetime.utcnow()
        self.quality_score = 0.0
        self.sentiment_avg = 0.0
        self.engagement_score = 0.0
        self.reflection_notes = ""

    def add_message(self, role: str, content: str, sentiment: float = 0.0):
        """Add message to conversation."""
        self.messages.append({"role": role, "content": content, "sentiment": sentiment})

    def calculate_quality(self) -> float:
        """Calculate conversation quality (0-100)."""
        if not self.messages:
            return 0.0

        # Factor 1: Length diversity (avoid too short or too long)
        avg_len = sum(len(m["content"]) for m in self.messages) / len(self.messages)
        length_score = min(100, (avg_len / 200) * 100) if avg_len > 0 else 0

        # Factor 2: Sentiment consistency (positive is better)
        sentiments = [m.get("sentiment", 0) for m in self.messages]
        sentiment_avg = sum(sentiments) / len(sentiments) if sentiments else 0
        sentiment_score = ((sentiment_avg + 1) / 2) * 100  # convert -1..1 to 0..100

        # Factor 3: Engagement (number of exchanges)
        exchange_score = min(100, (len(self.messages) / 10) * 100)

        # Weighted average
        self.quality_score = (length_score * 0.3 + sentiment_score * 0.4 + exchange_score * 0.3)
        self.engagement_score = exchange_score
        self.sentiment_avg = sentiment_avg
        return self.quality_score

    def generate_reflection(self) -> str:
        """Generate self-reflection about the conversation."""
        quality = self.calculate_quality()
        notes = []

        if quality > 80:
            notes.append("Great conversation! Maintained good engagement.")
        elif quality > 60:
            notes.append("Good conversation overall.")
        else:
            notes.append("Could improve engagement in future interactions.")

        if self.sentiment_avg > 0.5:
            notes.append("User seemed happy and satisfied.")
        elif self.sentiment_avg < -0.5:
            notes.append("User seemed frustrated or unhappy. Could have been better.")

        if len(self.messages) < 3:
            notes.append("Short conversation.")
        else:
            notes.append(f"Good back-and-forth with {len(self.messages)} messages.")

        self.reflection_notes = " ".join(notes)
        return self.reflection_notes


class ConversationScorer:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.conversations: Dict[str, ConversationAnalysis] = {}

    async def create_conversation(self, conversation_id: str) -> ConversationAnalysis:
        """Create new conversation for scoring."""
        async with self.lock:
            conv = ConversationAnalysis(conversation_id)
            self.conversations[conversation_id] = conv
            return conv

    async def score_conversation(self, conversation_id: str) -> Dict:
        """Get detailed score of a conversation."""
        if conversation_id not in self.conversations:
            return {"error": "Conversation not found"}

        conv = self.conversations[conversation_id]
        conv.calculate_quality()
        conv.generate_reflection()

        return {
            "id": conversation_id,
            "quality_score": conv.quality_score,
            "sentiment_avg": conv.sentiment_avg,
            "engagement_score": conv.engagement_score,
            "reflection": conv.reflection_notes,
            "message_count": len(conv.messages),
        }

    async def cleanup_old(self, days: int = 30):
        """Remove old conversations."""
        from datetime import timedelta

        cutoff = datetime.utcnow() - timedelta(days=days)
        async with self.lock:
            to_remove = [
                cid for cid, conv in self.conversations.items() if conv.created_at < cutoff
            ]
            for cid in to_remove:
                del self.conversations[cid]


scorer = ConversationScorer()
