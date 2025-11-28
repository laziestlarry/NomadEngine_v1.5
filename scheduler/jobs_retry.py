from sqlalchemy.orm import Session
from db.engine import init_engine
from db.session import create_session
from db.models import Task

from scheduler import context
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory


def retry_failed_tasks_job():
    engine = init_engine()
    session: Session = create_session(engine)

    try:
        event_bus: EventBus = context.event_bus
        if event_bus is None:
            return

        failed = (
            session.query(Task)
            .filter(Task.status == "failed")
            .limit(10)
            .all()
        )

        for t in failed:
            t.status = "pending"
            session.add(t)

            event_bus.publish(
                event_type=EventType.TASK_CREATED,
                category=EventCategory.TASK,
                message=f"Retrying failed task #{t.id}",
                task_id=t.id,
            )

        session.commit()
    finally:
        session.close()