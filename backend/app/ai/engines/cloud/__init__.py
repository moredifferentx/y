"""
Cloud AI Engines (Active)

Supported:
- OpenAI
- Google Gemini

All other cloud modules in this directory are deprecated.
"""

from app.monitoring.logs import log_sync

from .openai_engine import OpenAIEngine
from .gemini_engine import GeminiEngine


def register_cloud_engines():
    """
    Explicitly registers all cloud-based AI engines.
    This function is required by the engine bootstrap system.
    """

    log_sync("[ai] Registering cloud engines...")

    # Importing is enough if engines self-register
    _ = OpenAIEngine
    log_sync("[ai] OpenAI engine loaded")

    _ = GeminiEngine
    log_sync("[ai] Gemini engine loaded")


__all__ = [
    "OpenAIEngine",
    "GeminiEngine",
    "register_cloud_engines",
]
