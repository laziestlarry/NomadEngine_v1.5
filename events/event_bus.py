from typing import Callable, List, Dict, Any, Optional
import threading

from events.event_definitions import make_event, EventCategory


class EventBus:
    """
    Lightweight in-memory event bus.

    - Keeps a rolling buffer of events (default 1000)
    - Notifies subscribers when a new event is published
    - Designed to be combined with EventStore for persistence
    """

    def __init__(self, buffer_size: int = 1000):
        self._events: List[Dict[str, Any]] = []
        self._subscribers: List[Callable[[Dict[str, Any]], None]] = []
        self._buffer_size = buffer_size
        self._lock = threading.Lock()
        self._next_id = 1

    def subscribe(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a callback that will be called with the event dict every time an event is published.
        """
        with self._lock:
            self._subscribers.append(callback)

    def publish(
        self,
        event_type: str,
        category: str = EventCategory.SYSTEM,
        message: str = "",
        payload: Optional[Dict[str, Any]] = None,
        task_id: Optional[int] = None,
        blueprint_id: Optional[int] = None,
        worker_id: Optional[int] = None,
        agent_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create an event, store it in memory, and notify subscribers.
        """
        with self._lock:
            event = make_event(
                event_type=event_type,
                category=category,
                message=message,
                payload=payload,
                task_id=task_id,
                blueprint_id=blueprint_id,
                worker_id=worker_id,
                agent_id=agent_id,
            )
            event["id"] = self._next_id
            self._next_id += 1

            self._events.append(event)
            if len(self._events) > self._buffer_size:
                # keep rolling buffer
                self._events = self._events[-self._buffer_size :]

            # notify subscribers
            for cb in self._subscribers:
                try:
                    cb(event)
                except Exception:
                    # We never want one bad subscriber to break the bus
                    pass

            return event

    def get_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Return the last N events (for APIs, dashboards, etc).
        """
        with self._lock:
            return list(self._events[-limit:])

    def get_events_since(self, last_id: int) -> List[Dict[str, Any]]:
        """
        Return all events with id > last_id.
        """
        with self._lock:
            return [e for e in self._events if e["id"] > last_id]