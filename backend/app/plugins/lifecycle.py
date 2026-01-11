from typing import Protocol


class PluginLifecycle(Protocol):
    async def on_load(self) -> None:
        ...

    async def on_unload(self) -> None:
        ...
