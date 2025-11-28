from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.engine import init_engine
from db.session import create_session
from db.models import Task
from pipelines.execution_pipeline import select_pending_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/pending")
def list_pending_tasks():
    session = create_session(init_engine())
    tasks = select_pending_tasks(session, limit=50)

    return [
        {
            "id": t.id,
            "name": t.name,
            "short_description": t.short_description,
            "category": t.category,
            "status": t.status,
            "priority": t.priority,
            "importance": t.importance,
        }
        for t in tasks
    ]


@router.post("/add")
def add_task(payload: dict):
    session = create_session(init_engine())
    task = Task(
        name=payload.get("name", "Unnamed"),
        short_description=payload.get("short_description", ""),
        status="pending",
        payload=payload.get("payload", {}),
    )
    session.add(task)
    session.commit()

    return {"status": "ok", "task_id": task.id}