from fastapi import APIRouter
from sqlalchemy.orm import Session
import time
from fastapi.responses import StreamingResponse

from db.engine import init_engine
from db.session import create_session
from events.event_store import EventStore

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/recent")
def recent_events():
    session = create_session(init_engine())
    store = EventStore(session)
    return store.list_recent(100)


@router.get("/stream")
def stream_events():
    def event_generator():
        session = create_session(init_engine())
        store = EventStore(session)

        last_id = store.get_last_event_id()

        while True:
            new = store.get_events_since(last_id)
            for e in new:
                last_id = e["id"]
                yield f"data: {e}\n\n"
            time.sleep(0.8)

    return StreamingResponse(event_generator(), media_type="text/event-stream")