from typing import Set, Dict


class PermissionSet:
    def __init__(self, permissions: Set[str]):
        self.permissions = permissions

    def allows(self, permission: str) -> bool:
        return permission in self.permissions


class PermissionManager:
    """
    Central permission authority.
    """

    def __init__(self):
        self._roles: Dict[str, PermissionSet] = {}

    def register_role(self, role: str, permissions: Set[str]) -> None:
        self._roles[role] = PermissionSet(permissions)

    def check(self, role: str, permission: str) -> bool:
        if role not in self._roles:
            return False
        return self._roles[role].allows(permission)


# Global singleton
PERMISSIONS = PermissionManager()
