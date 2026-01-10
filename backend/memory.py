import json
import asyncio
from datetime import datetime, timedelta
from .models import Memory
from .db import AsyncSessionLocal
from sqlalchemy import select, delete


class MemoryStore:
    def __init__(self):
        self.lock = asyncio.Lock()

    async def add(self, owner: str, key: str, value: str, importance: float = 1.0):
        async with self.lock:
            async with AsyncSessionLocal() as session:
                m = Memory(owner=owner, key=key, value=value, importance=importance)
                session.add(m)
                await session.commit()
                await session.refresh(m)
                return m

    async def list_for_owner(self, owner: str):
        async with AsyncSessionLocal() as session:
            q = await session.execute(select(Memory).where(Memory.owner == owner).order_by(Memory.created_at.desc()))
            return q.scalars().all()

    async def delete(self, mem_id: int):
        async with AsyncSessionLocal() as session:
            await session.execute(delete(Memory).where(Memory.id == mem_id))
            await session.commit()

    async def decay(self, days: int = 30):
        # Reduce importance for old memories
        cutoff = datetime.utcnow() - timedelta(days=days)
        async with AsyncSessionLocal() as session:
            q = await session.execute(select(Memory).where(Memory.created_at < cutoff))
            for m in q.scalars().all():
                m.importance = max(0.0, m.importance * 0.9)
                session.add(m)
            await session.commit()

    async def export_owner(self, owner: str):
        rows = await self.list_for_owner(owner)
        return json.dumps([{"id": r.id, "key": r.key, "value": r.value, "importance": r.importance, "created_at": r.created_at.isoformat()} for r in rows])

    async def import_owner(self, owner: str, data: str):
        arr = json.loads(data)
        async with AsyncSessionLocal() as session:
            for item in arr:
                m = Memory(owner=owner, key=item.get("key"), value=item.get("value"), importance=item.get("importance", 1.0))
                session.add(m)
            await session.commit()


store = MemoryStore()
