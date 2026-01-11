"""
Language Utilities (RESERVED)

Purpose:
- Language detection
- Per-server language resolution
- Future internationalization (i18n)
- Custom language pack loading

Status:
- Reserved for future multilingual support
- Not currently wired
- Matches roadmap

Do NOT delete.
"""

from typing import Optional


def detect_language(text: str) -> Optional[str]:
    """
    Basic language detection stub.
    Returns ISO language code in future.
    """
    return None


def resolve_language(
    server_language: Optional[str],
    user_language: Optional[str],
) -> str:
    """
    Resolve final language preference.
    """
    return user_language or server_language or "en"
