from cryptography.fernet import Fernet
from typing import Optional
import base64
import os


class EncryptionManager:
    """
    Central encryption utility for memory and secrets.
    """

    def __init__(self, key: Optional[str] = None):
        if key is None:
            key = os.environ.get("ENCRYPTION_KEY")

        if not key:
            raise RuntimeError("ENCRYPTION_KEY not set")

        self._fernet = Fernet(self._normalize_key(key))

    def _normalize_key(self, key: str) -> bytes:
        raw = key.encode()
        if len(raw) == 44:
            return raw
        return base64.urlsafe_b64encode(raw.ljust(32, b"0"))

    def encrypt(self, data: str) -> str:
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token.encode()).decode()
