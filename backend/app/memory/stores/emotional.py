from .base import BaseMemoryStore
from typing import Dict, Any
import time


class EmotionalMemoryStore(BaseMemoryStore):
    table_name = "emotional_memory"

    async def init(self):
        async with await self._connect() as db:
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    emotion TEXT,
                    intensity REAL,
                    created_at REAL
                )
            """)
            await db.commit()

    async def add(self, user_id: str, emotion: str, intensity: float):
        payload = {"emotion": emotion, "intensity": intensity}
        async with await self._connect() as db:
            await db.execute(
                f"INSERT INTO {self.table_name} VALUES (NULL, ?, ?, ?, ?)",
                (user_id, emotion, intensity, time.time()),
            )
            await db.commit()
