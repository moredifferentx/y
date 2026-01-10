import json
import asyncio
from typing import Dict

DEFAULT_PRESETS = {
    "friendly": {"tone": "friendly", "emoji_use": 0.6, "formality": 0.3},
    "logical": {"tone": "logical", "emoji_use": 0.1, "formality": 0.8},
}


class PersonalityManager:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.presets: Dict[str, dict] = dict(DEFAULT_PRESETS)
        self.server_overrides: Dict[str, dict] = {}
        self.moods: Dict[str, str] = {}

    async def list_presets(self):
        return list(self.presets.keys())

    async def get_preset(self, name: str):
        return self.presets.get(name)

    async def set_override(self, server_id: str, profile: dict):
        async with self.lock:
            self.server_overrides[server_id] = profile
            return True

    async def get_profile_for_server(self, server_id: str):
        return self.server_overrides.get(server_id, self.presets.get("friendly"))

    async def set_mood(self, server_id: str, mood: str):
        async with self.lock:
            self.moods[server_id] = mood

    async def get_mood(self, server_id: str):
        return self.moods.get(server_id, "neutral")


manager = PersonalityManager()
