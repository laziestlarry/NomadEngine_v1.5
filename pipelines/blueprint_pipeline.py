from typing import List
from sqlalchemy.orm import Session

from db.models import Blueprint
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory
from pipelines.taskpipe import TaskPipe


def process_new_blueprints(session: Session, event_bus: EventBus) -> int:
    """
    Finds blueprints with status 'new' or 'approved' and generates tasks for them.
    Returns the number of blueprints processed.
    """
    to_process: List[Blueprint] = (
        session.query(Blueprint)
        .filter(Blueprint.status.in_(["new", "approved"]))
        .order_by(Blueprint.id.asc())
        .limit(10)
        .all()
    )

    if not to_process:
        return 0

    tp = TaskPipe(session, event_bus)

    count = 0
    for bp in to_process:
        tp.create_tasks_for_blueprint(bp)
        count += 1

    event_bus.publish(
        event_type=EventType.AGENT_DECISION,
        category=EventCategory.AGENT,
        message=f"Blueprint pipeline processed {count} blueprints into tasks.",
        payload={"blueprints_processed": count},
    )

    return count