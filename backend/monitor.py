"""System monitoring: uptime, logs, health checks, restart control."""
import os
import sys
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger(__name__)

# Setup file logging
LOG_DIR = os.environ.get("LOG_DIR", "/workspaces/y/logs")
os.makedirs(LOG_DIR, exist_ok=True)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "bot.log"))
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)


class HealthMonitor:
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.restart_count = 0
        self.last_error = None
        self.logs: List[Dict] = []

    def get_uptime(self) -> Dict:
        """Get uptime info."""
        delta = datetime.utcnow() - self.start_time
        return {
            "uptime_seconds": int(delta.total_seconds()),
            "uptime_human": str(delta),
            "start_time": self.start_time.isoformat(),
            "restart_count": self.restart_count,
        }

    def add_log(self, level: str, message: str):
        """Add log entry."""
        self.logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
        })
        # Keep last 1000 logs in memory
        if len(self.logs) > 1000:
            self.logs.pop(0)

    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent logs."""
        return self.logs[-limit:]

    def health_check(self) -> Dict:
        """Full health check."""
        return {
            **self.get_uptime(),
            "status": "healthy",
            "last_error": self.last_error,
            "log_count": len(self.logs),
        }

    async def restart_bot(self):
        """Attempt graceful restart."""
        self.restart_count += 1
        self.add_log("WARNING", "Bot restart initiated")
        logger.warning("Restarting bot...")
        # In production, use a process manager (systemd, supervisor, etc.)
        await asyncio.sleep(1)
        os.execl(sys.executable, sys.executable, *sys.argv)


monitor = HealthMonitor()
