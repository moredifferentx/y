from typing import Set


class PluginPermissions:
    def __init__(self, permissions: Set[str]):
        self.permissions = permissions

    def allows(self, permission: str) -> bool:
        return permission in self.permissions
