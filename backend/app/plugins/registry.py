from typing import Dict, Any


class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, Any] = {}
        self._states: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, plugin: Any):
        self._plugins[name] = plugin
        self._states[name] = {}

    def unregister(self, name: str):
        self._plugins.pop(name, None)
        self._states.pop(name, None)

    def get(self, name: str):
        return self._plugins.get(name)

    def state(self, name: str) -> Dict[str, Any]:
        return self._states.setdefault(name, {})
    

PLUGIN_REGISTRY = PluginRegistry()
