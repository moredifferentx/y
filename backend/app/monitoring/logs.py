from collections import deque
from typing import List
import asyncio

_LOGS = deque(maxlen=500)


async def log(msg: str) -> None:
    """
    Async-safe logger.
    """
    _LOGS.append(msg)


def log_sync(msg: str) -> None:
    """
    Sync-safe logger.
    Can be called from non-async contexts.
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(log(msg))
    except RuntimeError:
        # No running loop (startup / import time)
        _LOGS.append(msg)


def get_logs() -> List[str]:
    return list(_LOGS)
