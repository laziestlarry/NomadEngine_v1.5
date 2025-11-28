from sqlalchemy.orm import Session

from db.models import Task
from events.event_bus import EventBus
from workers.platform_workers.generic_worker import GenericPlatformWorker


class TolokaWorker(GenericPlatformWorker):
    """
    Stub for Toloka-specific worker.
    In future, this will integrate Toloka API calls:
    - create pools
    - upload tasks (HITs)
    - fetch results
    """

    def __init__(self, event_bus: EventBus):
        super().__init__(platform_name="toloka", event_bus=event_bus)

    def execute_task(self, session: Session, task: Task) -> bool:
        # For now, just call parent stub
        return super().execute_task(session, task)