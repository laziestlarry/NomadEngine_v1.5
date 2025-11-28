from typing import Dict, Any
from sqlalchemy.orm import Session

from db.models import Task
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory


class GenericPlatformWorker:
    """
    Base class for specific platform workers (Toloka, Hive, Remotasks).
    """

    def __init__(self, platform_name: str, event_bus: EventBus):
        self.platform_name = platform_name
        self.event_bus = event_bus

    def execute_task(self, session: Session, task: Task) -> bool:
        """
        Execute a single task. Stub in v1.5.
        """
        self.event_bus.publish(
            event_type=EventType.TASK_COMPLETED,
            category=EventCategory.TASK,
            message=f"[{self.platform_name}] Stub executed task #{task.id}",
            task_id=task.id,
            payload={"platform": self.platform_name},
        )
        return True