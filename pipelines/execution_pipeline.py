from typing import List
from sqlalchemy.orm import Session

from db.models import Task, Worker
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory


def select_pending_tasks(session: Session, limit: int = 20) -> List[Task]:
    """
    Fetch pending tasks ordered by priority & importance.
    """
    tasks = (
        session.query(Task)
        .filter(Task.status == "pending")
        .order_by(Task.priority.asc(), Task.importance.desc())
        .limit(limit)
        .all()
    )
    return tasks


def assign_tasks_to_worker(session: Session, event_bus: EventBus, worker: Worker, tasks: List[Task]) -> None:
    """
    Naive assignment: attach tasks to a given worker and mark as 'queued'.
    """
    for t in tasks:
        t.assigned_worker_id = worker.id
        t.status = "queued"
        session.add(t)

        event_bus.publish(
            event_type=EventType.TASK_ASSIGNED,
            category=EventCategory.TASK,
            message=f"Task #{t.id} assigned to worker #{worker.id} ({worker.name})",
            task_id=t.id,
            payload={
                "short_description": t.short_description,
                "category": t.category,
                "priority": t.priority,
                "importance": t.importance,
                "worker_name": worker.name,
            },
        )

    session.commit()


def mark_task_started(session: Session, event_bus: EventBus, task: Task) -> None:
    t = session.get(Task, task.id)
    if not t:
        return

    t.status = "running"
    session.add(t)
    session.commit()

    event_bus.publish(
        event_type=EventType.TASK_STARTED,
        category=EventCategory.TASK,
        message=f"Task #{t.id} started.",
        task_id=t.id,
        payload={
            "short_description": t.short_description,
            "category": t.category,
        },
    )


def mark_task_completed(session: Session, event_bus: EventBus, task: Task) -> None:
    t = session.get(Task, task.id)
    if not t:
        return

    t.status = "completed"
    session.add(t)
    session.commit()

    event_bus.publish(
        event_type=EventType.TASK_COMPLETED,
        category=EventCategory.TASK,
        message=f"Task #{t.id} completed.",
        task_id=t.id,
        payload={
            "short_description": t.short_description,
            "category": t.category,
        },
    )


def mark_task_failed(session: Session, event_bus: EventBus, task: Task, error_message: str) -> None:
    t = session.get(Task, task.id)
    if not t:
        return

    t.status = "failed"
    t.last_error_message = error_message
    session.add(t)
    session.commit()

    event_bus.publish(
        event_type=EventType.TASK_FAILED,
        category=EventCategory.TASK,
        message=f"Task #{t.id} failed: {error_message[:120]}",
        task_id=t.id,
        payload={
            "short_description": t.short_description,
            "category": t.category,
            "error": error_message,
        },
    )