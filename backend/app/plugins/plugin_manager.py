import importlib.util
import json
import pathlib
from typing import Dict

from app.plugins.registry import PLUGIN_REGISTRY
from app.plugins.permissions import PluginPermissions
from app.plugins.sandbox import sandbox_globals
from app.monitoring import log

log(f"Plugin loaded: {name}")
log(f"Plugin unloaded: {name}")
log(f"Plugin load failed: {name} → {str(e)}")



PLUGIN_ROOT = pathlib.Path("plugins/python")


class PluginManager:
    def __init__(self):
        self._permissions: Dict[str, PluginPermissions] = {}

    async def load(self, name: str):
        path = PLUGIN_ROOT / name
        if not path.exists():
            raise RuntimeError(f"Plugin '{name}' not found")

        # Load manifest
        manifest = json.loads((path / "manifest.json").read_text())
        permissions = json.loads((path / "permissions.json").read_text())

        self._permissions[name] = PluginPermissions(set(permissions))

        # Load plugin code
        spec = importlib.util.spec_from_file_location(
            name,
            path / "plugin.py",
        )
        module = importlib.util.module_from_spec(spec)

        # Sandbox
        module.__dict__.update(sandbox_globals())

        spec.loader.exec_module(module)

        plugin = getattr(module, "Plugin", None)
        if not plugin:
            raise RuntimeError("Plugin must export class Plugin")

        instance = plugin()

        PLUGIN_REGISTRY.register(name, instance)

        if hasattr(instance, "on_load"):
            await instance.on_load()

    async def unload(self, name: str):
        plugin = PLUGIN_REGISTRY.get(name)
        if not plugin:
            return

        if hasattr(plugin, "on_unload"):
            await plugin.on_unload()

        PLUGIN_REGISTRY.unregister(name)

    def list(self):
        return list(PLUGIN_REGISTRY._plugins.keys())


# Global singleton
PLUGIN_MANAGER = PluginManager()
