"""
Async Utilities (RESERVED)

Purpose:
- Shared async helpers used across the system
- Central place for:
  - background task scheduling
  - async retry helpers
  - cancellation-safe wrappers

Status:
- Reserved for future use
- Not currently imported
- SAFE to leave unused

Do NOT delete.
"""

import asyncio
from typing import Awaitable, Callable


async def run_background(coro: Awaitable) -> None:
    """
    Fire-and-forget async task.
    Used when task lifetime should not block caller.
    """
    asyncio.create_task(coro)


async def retry(
    fn: Callable,
    retries: int = 3,
    delay: float = 0.5,
):
    """
    Simple async retry helper.
    """
    for attempt in range(retries):
        try:
            return await fn()
        except Exception:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(delay)
