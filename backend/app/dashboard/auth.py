from fastapi import Depends, HTTPException, Header
from app.core.config import Config


async def require_admin(x_admin_token: str = Header(...)):
    expected = Config.get("DASHBOARD_ADMIN_TOKEN")
    if not expected or x_admin_token != expected:
        raise HTTPException(status_code=403, detail="Unauthorized")
