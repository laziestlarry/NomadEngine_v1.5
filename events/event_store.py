from typing import Dict, Any, List
from sqlalchemy.orm import Session

from db.models import EventLog
from core.logger import logger


class EventStore:
    """
    Persistent event logger.

    - Listens to EventBus events
    - Writes them to the events table
    - Can query recent events from DB (for history beyond RAM buffer)
    """

    def __init__(self, session: Session):
        self.session = session

    def handle_event(self, event: Dict[str, Any]) -> None:
        """
        Convert an in-memory event dict into a DB record.
        """
        try:
            record = EventLog(
                type=event.get("type"),
                category=event.get("category"),
                task_id=event.get("task_id"),
                blueprint_id=event.get("blueprint_id"),
                worker_id=event.get("worker_id"),
                agent_id=event.get("agent_id"),
                payload=event.get("payload"),
            )
            self.session.add(record)
            self.session.commit()
        except Exception as e:
            logger.error(f"[EventStore] Failed to store event: {e}")
            self.session.rollback()

    def attach_to_bus(self, bus) -> None:
        """
        Subscribe to EventBus so every published event is automatically stored.
        """

        def _callback(event: Dict[str, Any]):
            self.handle_event(event)

        bus.subscribe(_callback)
        logger.info("[EventStore] Attached to EventBus.")

    # ---------- NEW HELPERS FOR API LAYER ----------

    def get_last_event_id(self) -> int:
        """
        Return last event id, or 0 if none.
        """
        last = (
            self.session.query(EventLog.id)
            .order_by(EventLog.id.desc())
            .first()
        )
        if not last:
            return 0
        return int(last[0])

    def list_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Return recent events as dicts for API.
        """
        rows = (
            self.session.query(EventLog)
            .order_by(EventLog.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": e.id,
                "type": e.type,
                "category": e.category,
                "task_id": e.task_id,
                "blueprint_id": e.blueprint_id,
                "worker_id": e.worker_id,
                "agent_id": e.agent_id,
                "payload": e.payload,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in rows
        ]

    def get_events_since(self, last_id: int, limit: int = 200) -> List[Dict[str, Any]]:
        """
        Return events with id > last_id.
        """
        rows = (
            self.session.query(EventLog)
            .filter(EventLog.id > last_id)
            .order_by(EventLog.id.asc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": e.id,
                "type": e.type,
                "category": e.category,
                "task_id": e.task_id,
                "blueprint_id": e.blueprint_id,
                "worker_id": e.worker_id,
                "agent_id": e.agent_id,
                "payload": e.payload,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in rows
        ]

    def get_recent_from_db(self, limit: int = 100) -> List[EventLog]:
        """
        (Legacy helper) Retrieve recent raw EventLog rows.
        """
        return (
            self.session.query(EventLog)
            .order_by(EventLog.id.desc())
            .limit(limit)
            .all()
        )