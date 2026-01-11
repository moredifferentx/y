class Plugin:
    async def on_load(self):
        print("[ExamplePlugin] Loaded")

    async def on_unload(self):
        print("[ExamplePlugin] Unloaded")
