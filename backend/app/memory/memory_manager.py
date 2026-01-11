from typing import Optional
from datetime import datetime

from app.core.encryption import EncryptionManager
from app.monitoring.logs import log

from .stores.user import UserMemoryStore
from .stores.server import ServerMemoryStore
from .stores.emotional import EmotionalMemoryStore
from .stores.ephemeral import EphemeralMemoryStore
from .scoring import ImportanceScorer


class MemoryManager:
    """
    Unified memory control layer.
    Handles encryption, scoring, storage, and decay.
    """

    def __init__(self):
        self.encryptor = EncryptionManager()
        self.scorer = ImportanceScorer()

        self.user = UserMemoryStore(self.encryptor)
        self.server = ServerMemoryStore(self.encryptor)
        self.emotional = EmotionalMemoryStore(self.encryptor)
        self.ephemeral = EphemeralMemoryStore()

    async def initialize(self):
        await self.user.init()
        await self.server.init()
        await self.emotional.init()
        await self.ephemeral.init()

        await log("Memory system initialized")

    # -----------------------------
    # WRITE METHODS
    # -----------------------------

    async def remember_user(
        self,
        user_id: str,
        content: str,
        importance: Optional[float] = None,
    ):
        score = importance or self.scorer.score(content)
        await self.user.add(user_id, content, score)

        await log(
            f"Memory stored: user={user_id}, type=user, importance={score}"
        )

    async def remember_server(
        self,
        server_id: str,
        content: str,
        importance: Optional[float] = None,
    ):
        score = importance or self.scorer.score(content)
        await self.server.add(server_id, content, score)

        await log(
            f"Memory stored: server={server_id}, type=server, importance={score}"
        )

    async def remember_emotion(
        self,
        user_id: str,
        emotion: str,
        intensity: float,
    ):
        await self.emotional.add(user_id, emotion, intensity)

        await log(
            f"Emotional memory stored: user={user_id}, emotion={emotion}, intensity={intensity}"
        )

    async def remember_ephemeral(
        self,
        scope: str,
        content: str,
        expires_at: datetime,
    ):
        await self.ephemeral.add(scope, content, expires_at)

        await log(
            f"Ephemeral memory stored: scope={scope}, expires_at={expires_at}"
        )

    # -----------------------------
    # READ METHODS
    # -----------------------------

    async def recall_user(self, user_id: str, limit: int = 10):
        return await self.user.get(user_id, limit)

    async def recall_server(self, server_id: str, limit: int = 10):
        return await self.server.get(server_id, limit)

    async def recall_emotions(self, user_id: str, limit: int = 10):
        return await self.emotional.get(user_id, limit)


# Global singleton (SAFE)
MEMORY = MemoryManager()
