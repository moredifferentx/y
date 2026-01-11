from app.core.encryption import EncryptionManager
from .stores.user import UserMemoryStore
from .stores.server import ServerMemoryStore
from .stores.emotional import EmotionalMemoryStore
from .stores.ephemeral import EphemeralMemoryStore
from .scoring import ImportanceScorer
from app.monitoring import log
log(f"Memory stored: user={user_id}, type={memory_type}")
log(f"Memory decayed: memory_id={id}")



class MemoryManager:
    """
    Unified memory control layer.
    """

    def __init__(self):
        self.encryptor = EncryptionManager()
        self.user = UserMemoryStore(self.encryptor)
        self.server = ServerMemoryStore(self.encryptor)
        self.emotional = EmotionalMemoryStore(self.encryptor)
        self.ephemeral = EphemeralMemoryStore()
        self.scorer = ImportanceScorer()

    async def initialize(self):
        await self.user.init()
        await self.server.init()
        await self.emotional.init()


# Global singleton
MEMORY = MemoryManager()
