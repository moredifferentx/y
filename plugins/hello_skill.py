"""Example Discord AI plugin for custom skill injection."""
from backend.plugins import Plugin


class Plugin(Plugin):
    def __init__(self):
        super().__init__("hello_skill", "1.0")
        self.register_skill("greet", self.greet)
        self.register_skill("add_numbers", self.add_numbers)

    async def on_load(self):
        """Called when plugin loads."""
        print(f"Plugin {self.name} loaded!")

    async def on_unload(self):
        """Called when plugin unloads."""
        print(f"Plugin {self.name} unloaded!")

    async def greet(self, name: str = "Friend") -> str:
        """Greet a user."""
        return f"Hello {name}! This is from the hello_skill plugin."

    async def add_numbers(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
