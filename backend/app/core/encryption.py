from cryptography.fernet import Fernet
from typing import Optional
import base64
import os


class EncryptionManager:
    """
    Central encryption utility for memory and secrets.

    Design rules:
    - Reads ENCRYPTION_KEY from the *process environment*
    - Fails fast with a clear error if missing
    - Compatible with Fernet keys or raw secrets
    """

    def __init__(self, key: Optional[str] = None):
        # Allow explicit override, otherwise read from environment
        key = key or os.getenv("ENCRYPTION_KEY")

        if not key:
            raise RuntimeError(
                "ENCRYPTION_KEY not set in environment. "
                "Ensure .env is loaded before starting the app."
            )

        self._fernet = Fernet(self._normalize_key(key))

    def _normalize_key(self, key: str) -> bytes:
        """
        Normalize a user-provided key into a valid Fernet key.

        - Accepts full Fernet keys (44 chars, base64)
        - Accepts arbitrary secrets and derives a Fernet-compatible key
        """
        raw = key.encode()

        # Already a valid Fernet key
        if len(raw) == 44:
            return raw

        # Derive a Fernet-compatible key from arbitrary secret
        return base64.urlsafe_b64encode(raw.ljust(32, b"0"))

    def encrypt(self, data: str) -> str:
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token.encode()).decode()
