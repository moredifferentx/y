"""
Cloud AI Engines (Active)

Supported:
- OpenAI
- Google Gemini

All other cloud modules in this directory are deprecated.
"""

from app.monitoring import log

from .openai_engine import OpenAIEngine
from .gemini_engine import GeminiEngine


def register_cloud_engines():
    """
    Explicitly registers all cloud-based AI engines.
    This function is required by the engine bootstrap system.
    """

    log("[ai] Registering cloud engines...")

    # Importing is enough if engines self-register
    _ = OpenAIEngine
    log("[ai] OpenAI engine loaded")

    _ = GeminiEngine
    log("[ai] Gemini engine loaded")


__all__ = [
    "OpenAIEngine",
    "GeminiEngine",
    "register_cloud_engines",
]
