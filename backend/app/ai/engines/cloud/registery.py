from app.monitoring import log

def register_cloud_engines():
    """
    Registers all cloud-based AI engines.
    This function is intentionally side-effect driven.
    """

    log("[ai] Registering cloud engines...")

    try:
        from .gemini_engine import GeminiEngine
        log("[ai] Gemini engine loaded")
    except Exception as e:
        log(f"[ai] Failed to load Gemini engine: {e}")
