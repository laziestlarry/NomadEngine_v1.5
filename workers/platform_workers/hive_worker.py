from sqlalchemy.orm import Session

from db.models import Task
from events.event_bus import EventBus
from workers.platform_workers.generic_worker import GenericPlatformWorker


class HiveWorker(GenericPlatformWorker):
    """
    Stub for Hive Micro worker.
    """

    def __init__(self, event_bus: EventBus):
        super().__init__(platform_name="hive", event_bus=event_bus)

    def execute_task(self, session: Session, task: Task) -> bool:
        return super().execute_task(session, task)