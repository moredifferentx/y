import os
import threading
from dotenv import load_dotenv
from typing import Any, Dict


class Config:
    """
    Centralized configuration manager.
    Supports safe runtime reload without restarts.
    """

    _lock = threading.RLock()
    _cache: Dict[str, Any] = {}
    _loaded: bool = False

    @classmethod
    def load(cls, force: bool = False) -> None:
        with cls._lock:
            if cls._loaded and not force:
                return

            load_dotenv(override=True)
            cls._cache = dict(os.environ)
            cls._loaded = True

    @classmethod
    def reload(cls) -> None:
        cls.load(force=True)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        if not cls._loaded:
            cls.load()
        return cls._cache.get(key, default)

    @classmethod
    def all(cls) -> Dict[str, Any]:
        if not cls._loaded:
            cls.load()
        return dict(cls._cache)
