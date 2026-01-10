"""Environment management: secure editing and auto-reload."""
import os
import asyncio
from typing import Dict
from dotenv import load_dotenv, dotenv_values

ENV_FILE = os.environ.get("ENV_FILE", "/workspaces/y/.env")


class EnvironmentManager:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.current_env: Dict[str, str] = {}
        self.load()

    def load(self):
        """Load environment from .env file."""
        if os.path.exists(ENV_FILE):
            self.current_env = dotenv_values(ENV_FILE)
        else:
            self.current_env = {}

    async def get_all(self) -> Dict:
        """Get all env vars (mask sensitive ones)."""
        async with self.lock:
            masked = {}
            sensitive_keys = {"API_KEY", "TOKEN", "SECRET", "PASSWORD"}
            for k, v in self.current_env.items():
                if any(s in k.upper() for s in sensitive_keys):
                    masked[k] = "***REDACTED***"
                else:
                    masked[k] = v
            return masked

    async def set_var(self, key: str, value: str, secure: bool = False) -> bool:
        """Set environment variable."""
        # Validation: prevent dangerous keys
        if key.startswith("_"):
            return False

        async with self.lock:
            self.current_env[key] = value
            os.environ[key] = value

            # Write to .env file
            try:
                lines = []
                if os.path.exists(ENV_FILE):
                    with open(ENV_FILE, "r") as f:
                        for line in f:
                            if not line.startswith(key + "="):
                                lines.append(line.rstrip())
                lines.append(f"{key}={value}")
                with open(ENV_FILE, "w") as f:
                    f.write("\n".join(lines) + "\n")
                return True
            except Exception:
                return False

    async def reload(self):
        """Reload from .env file."""
        async with self.lock:
            self.load()
            for k, v in self.current_env.items():
                os.environ[k] = v


manager = EnvironmentManager()
