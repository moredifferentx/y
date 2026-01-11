import aiosqlite
from typing import Any, Dict, Optional
from app.core.encryption import EncryptionManager
import json
import os


DB_PATH = os.getenv("MEMORY_DB_PATH", "data/memory.db")


class BaseMemoryStore:
    table_name: str = ""

    def __init__(self, encryptor: EncryptionManager):
        self.encryptor = encryptor

    async def _connect(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        return await aiosqlite.connect(DB_PATH)

    async def _serialize(self, data: Dict[str, Any]) -> str:
        return self.encryptor.encrypt(json.dumps(data))

    async def _deserialize(self, blob: str) -> Dict[str, Any]:
        return json.loads(self.encryptor.decrypt(blob))
