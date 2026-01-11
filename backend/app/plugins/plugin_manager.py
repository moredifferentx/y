import importlib.util
import json
import pathlib
from typing import Dict

from app.plugins.registry import PLUGIN_REGISTRY
from app.plugins.permissions import PluginPermissions
from app.plugins.sandbox import sandbox_globals
from app.monitoring import log


PLUGIN_ROOT = pathlib.Path("plugins/python")


class PluginManager:
    def __init__(self):
        self._permissions: Dict[str, PluginPermissions] = {}

    async def load(self, name: str):
        path = PLUGIN_ROOT / name
        if not path.exists():
            raise RuntimeError(f"Plugin '{name}' not found")

        try:
            # ---- Load manifest & permissions ----
            manifest = json.loads((path / "manifest.json").read_text())
            permissions = json.loads((path / "permissions.json").read_text())

            self._permissions[name] = PluginPermissions(set(permissions))

            # ---- Load plugin module ----
            spec = importlib.util.spec_from_file_location(
                name,
                path / "plugin.py",
            )
            module = importlib.util.module_from_spec(spec)

            # Sandbox environment
            module.__dict__.update(sandbox_globals())

            spec.loader.exec_module(module)

            plugin_cls = getattr(module, "Plugin", None)
            if not plugin_cls:
                raise RuntimeError("Plugin must export class Plugin")

            instance = plugin_cls()

            # ---- Register plugin ----
            PLUGIN_REGISTRY.register(name, instance)

            if hasattr(instance, "on_load"):
                await instance.on_load()

            log(f"Plugin loaded: {name}")

        except Exception as e:
            log(f"Plugin load failed: {name} → {e}")
            raise

    async def unload(self, name: str):
        plugin = PLUGIN_REGISTRY.get(name)
        if not plugin:
            return

        try:
            if hasattr(plugin, "on_unload"):
                await plugin.on_unload()

            PLUGIN_REGISTRY.unregister(name)
            log(f"Plugin unloaded: {name}")

        except Exception as e:
            log(f"Plugin unload failed: {name} → {e}")
            raise

    def list(self):
        return list(PLUGIN_REGISTRY._plugins.keys())


# Global singleton
PLUGIN_MANAGER = PluginManager()
