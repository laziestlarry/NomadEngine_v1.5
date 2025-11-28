from fastapi import APIRouter

from db.engine import init_engine
from db.session import create_session
from events.event_store import EventStore

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
def system_health():
    """
    Lightweight liveness check.
    Returns 200 if API process is running and DB is reachable.
    """
    engine = init_engine()
    # simple connection test; will raise if DB is unavailable
    connection = engine.connect()
    connection.close()

    return {
        "engine": "Nomad v1.5",
        "status": "ok",
        "message": "Nomad Engine API + DB reachable",
    }


@router.get("/status")
def system_status():
    """
    Richer status endpoint you can use as your personal quick-check.
    """
    engine = init_engine()
    session = create_session(engine)

    store = EventStore(session)
    last_id = store.get_last_event_id()

    return {
        "engine": "Nomad v1.5",
        "status": "online",
        "message": "Nomad Engine Alive",
        "events_last_id": last_id,
    }


@router.get("/timeline")
def system_timeline(limit: int = 50):
    """
    Recent events timeline for quick introspection / debugging.
    """
    engine = init_engine()
    session = create_session(engine)
    store = EventStore(session)

    events = store.list_recent(limit=limit)
    return {"count": len(events), "events": events}