"""Multi-language support system."""
import json
import os
from typing import Dict

SUPPORTED_LANGUAGES = {
    "en": {
        "name": "English",
        "hello": "Hello!",
        "goodbye": "Goodbye!",
        "thanks": "Thanks!",
        "error": "Oops, something went wrong.",
    },
    "es": {
        "name": "Spanish",
        "hello": "¡Hola!",
        "goodbye": "¡Adiós!",
        "thanks": "¡Gracias!",
        "error": "Oops, algo salió mal.",
    },
    "fr": {
        "name": "French",
        "hello": "Bonjour!",
        "goodbye": "Au revoir!",
        "thanks": "Merci!",
        "error": "Oups, quelque chose n'a pas fonctionné.",
    },
    "de": {
        "name": "German",
        "hello": "Hallo!",
        "goodbye": "Auf Wiedersehen!",
        "thanks": "Danke!",
        "error": "Hoppla, etwas ist schiefgelaufen.",
    },
    "ja": {
        "name": "Japanese",
        "hello": "こんにちは!",
        "goodbye": "さようなら!",
        "thanks": "ありがとう!",
        "error": "申し訳ありませんが、エラーが発生しました。",
    },
}


class LanguageManager:
    def __init__(self):
        self.strings: Dict[str, Dict[str, str]] = dict(SUPPORTED_LANGUAGES)
        self.server_languages: Dict[str, str] = {}
        self.user_languages: Dict[str, str] = {}
        self.auto_detect = True
        self._load_custom()

    def _load_custom(self):
        """Load custom language files from languages/ directory."""
        lang_dir = os.environ.get("LANGUAGE_DIR", "/workspaces/y/languages")
        if os.path.exists(lang_dir):
            for f in os.listdir(lang_dir):
                if f.endswith(".json"):
                    code = f.replace(".json", "")
                    try:
                        with open(os.path.join(lang_dir, f)) as fp:
                            self.strings[code] = json.load(fp)
                    except Exception:
                        pass

    def set_server_language(self, server_id: str, lang_code: str):
        """Set language for entire server."""
        if lang_code in self.strings:
            self.server_languages[server_id] = lang_code
            return True
        return False

    def set_user_language(self, user_id: str, lang_code: str):
        """Set language for specific user."""
        if lang_code in self.strings:
            self.user_languages[user_id] = lang_code
            return True
        return False

    def get_string(self, key: str, user_id: str = None, server_id: str = None, lang_code: str = None) -> str:
        """Get translated string."""
        # Priority: explicit lang_code > user language > server language > default (en)
        if not lang_code:
            if user_id and user_id in self.user_languages:
                lang_code = self.user_languages[user_id]
            elif server_id and server_id in self.server_languages:
                lang_code = self.server_languages[server_id]
            else:
                lang_code = "en"

        if lang_code not in self.strings:
            lang_code = "en"

        return self.strings[lang_code].get(key, self.strings["en"].get(key, key))

    def list_languages(self):
        """List all available languages."""
        return {code: data.get("name", code) for code, data in self.strings.items()}


manager = LanguageManager()
