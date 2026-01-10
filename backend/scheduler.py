"""Event scheduler for automated behaviors."""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)


class ScheduledEvent:
    def __init__(self, event_id: str, trigger: str, action: Callable, interval_seconds: int = None):
        self.id = event_id
        self.trigger = trigger  # e.g., "time", "message_count", "server_active"
        self.action = action
        self.interval_seconds = interval_seconds or 3600
        self.next_run = datetime.utcnow()
        self.last_run = None
        self.enabled = True

    async def should_run(self) -> bool:
        """Check if event should run."""
        if not self.enabled:
            return False
        return datetime.utcnow() >= self.next_run

    async def run(self):
        """Execute the event action."""
        try:
            await self.action()
            self.last_run = datetime.utcnow()
            self.next_run = datetime.utcnow() + timedelta(seconds=self.interval_seconds)
            logger.info(f"Event {self.id} executed successfully")
        except Exception as e:
            logger.exception(f"Error executing event {self.id}: {e}")


class EventScheduler:
    def __init__(self):
        self.events: Dict[str, ScheduledEvent] = {}
        self.lock = asyncio.Lock()
        self.running = False

    async def register(self, event: ScheduledEvent):
        """Register a scheduled event."""
        async with self.lock:
            self.events[event.id] = event

    async def unregister(self, event_id: str):
        """Unregister a scheduled event."""
        async with self.lock:
            if event_id in self.events:
                del self.events[event_id]

    async def start(self):
        """Start the scheduler loop."""
        self.running = True
        while self.running:
            async with self.lock:
                for event in self.events.values():
                    if await event.should_run():
                        asyncio.create_task(event.run())
            await asyncio.sleep(5)  # check every 5 seconds

    async def stop(self):
        """Stop the scheduler."""
        self.running = False

    async def list_events(self) -> List[Dict]:
        """List all scheduled events."""
        async with self.lock:
            return [
                {
                    "id": e.id,
                    "trigger": e.trigger,
                    "interval": e.interval_seconds,
                    "enabled": e.enabled,
                    "next_run": e.next_run.isoformat(),
                }
                for e in self.events.values()
            ]


scheduler = EventScheduler()
