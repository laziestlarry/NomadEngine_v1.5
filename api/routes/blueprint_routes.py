from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.engine import init_engine
from db.session import create_session
from db.models import Blueprint
from pipelines.blueprint_pipeline import process_new_blueprints

router = APIRouter(prefix="/blueprints", tags=["blueprints"])


@router.get("/list")
def list_blueprints():
    session = create_session(init_engine())
    rows = session.query(Blueprint).order_by(Blueprint.id.asc()).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "source": b.source,
            "status": b.status,
            "strategy": b.strategy,
        }
        for b in rows
    ]


@router.post("/process")
def process_blueprints():
    session = create_session(init_engine())
    count = process_new_blueprints(session, None)  # event_bus injected in jobs
    return {"processed": count}