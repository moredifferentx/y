"""
Hot Reload Utilities (RESERVED)

Purpose:
- Central hooks for runtime reload without restart
- Intended targets:
  - .env reload
  - AI engine re-registration
  - plugin reload coordination
  - config refresh signals

Status:
- Reserved for future use
- No active imports yet
- Architecture placeholder ONLY

Do NOT delete.
"""

from typing import Callable, List


_reload_hooks: List[Callable] = []


def register_reload_hook(fn: Callable):
    """
    Register a function to be called on hot reload.
    """
    _reload_hooks.append(fn)


async def trigger_reload():
    """
    Trigger all registered reload hooks.
    """
    for fn in _reload_hooks:
        result = fn()
        if hasattr(result, "__await__"):
            await result
