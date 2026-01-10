"""Plugin system for custom skills and extensions."""
import os
import sys
import asyncio
import logging
import importlib.util
from typing import Dict, Callable, List

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
        self.skills: Dict[str, Callable] = {}
        self.enabled = True

    async def on_load(self):
        """Called when plugin is loaded."""
        pass

    async def on_unload(self):
        """Called when plugin is unloaded."""
        pass

    def register_skill(self, name: str, func: Callable):
        """Register a skill function."""
        self.skills[name] = func

    async def execute_skill(self, skill_name: str, *args, **kwargs):
        """Execute a skill."""
        if skill_name not in self.skills:
            raise ValueError(f"Skill {skill_name} not found")
        return await self.skills[skill_name](*args, **kwargs)


class PluginManager:
    def __init__(self, plugin_dir: str = None):
        self.plugin_dir = plugin_dir or os.environ.get("PLUGIN_DIR", "/workspaces/y/plugins")
        self.plugins: Dict[str, Plugin] = {}
        self.lock = asyncio.Lock()
        os.makedirs(self.plugin_dir, exist_ok=True)

    async def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin from file."""
        try:
            plugin_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")
            if not os.path.exists(plugin_path):
                logger.error(f"Plugin file not found: {plugin_path}")
                return False

            # Import plugin module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)

            # Get plugin class
            if not hasattr(module, "Plugin"):
                logger.error(f"Plugin {plugin_name} does not define Plugin class")
                return False

            plugin = module.Plugin()
            await plugin.on_load()

            async with self.lock:
                self.plugins[plugin_name] = plugin
                logger.info(f"Plugin {plugin_name} loaded successfully")
            return True
        except Exception as e:
            logger.exception(f"Error loading plugin {plugin_name}: {e}")
            return False

    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        async with self.lock:
            if plugin_name not in self.plugins:
                return False
            plugin = self.plugins[plugin_name]
            await plugin.on_unload()
            del self.plugins[plugin_name]
            return True

    async def list_plugins(self) -> List[Dict]:
        """List all loaded plugins and their skills."""
        async with self.lock:
            return [
                {
                    "name": p.name,
                    "version": p.version,
                    "enabled": p.enabled,
                    "skills": list(p.skills.keys()),
                }
                for p in self.plugins.values()
            ]

    async def execute_skill(self, plugin_name: str, skill_name: str, *args, **kwargs):
        """Execute a skill from a plugin."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} not loaded")
        plugin = self.plugins[plugin_name]
        return await plugin.execute_skill(skill_name, *args, **kwargs)

    async def load_all(self):
        """Auto-load all plugins from plugin directory."""
        if not os.path.exists(self.plugin_dir):
            return

        for f in os.listdir(self.plugin_dir):
            if f.endswith(".py") and not f.startswith("_"):
                plugin_name = f[:-3]
                await self.load_plugin(plugin_name)


manager = PluginManager()
