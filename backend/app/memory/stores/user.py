from .base import BaseMemoryStore
from typing import Dict, Any, List
import time


class UserMemoryStore(BaseMemoryStore):
    table_name = "user_memory"

    async def init(self):
        async with await self._connect() as db:
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    data TEXT,
                    importance REAL,
                    created_at REAL
                )
            """)
            await db.commit()

    async def add(self, user_id: str, data: Dict[str, Any], importance: float):
        async with await self._connect() as db:
            await db.execute(
                f"INSERT INTO {self.table_name} VALUES (NULL, ?, ?, ?, ?)",
                (
                    user_id,
                    await self._serialize(data),
                    importance,
                    time.time(),
                ),
            )
            await db.commit()

    async def fetch(self, user_id: str) -> List[Dict[str, Any]]:
        async with await self._connect() as db:
            cursor = await db.execute(
                f"SELECT data FROM {self.table_name} WHERE user_id = ?",
                (user_id,),
            )
            rows = await cursor.fetchall()
            return [await self._deserialize(r[0]) for r in rows]
