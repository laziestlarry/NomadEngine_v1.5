from dataclasses import dataclass
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory
from core.logger import logger


@dataclass
class BaseAgent:
    name: str
    role: str
    session: Session
    event_bus: EventBus
    config: Optional[Dict[str, Any]] = None

    def emit_decision(self, message: str, payload: Optional[Dict[str, Any]] = None, blueprint_id=None, task_id=None):
        """
        Helper: log a decision event, both in logs and in EventBus.
        """
        logger.info(f"[Agent:{self.name}] {message}")
        self.event_bus.publish(
            event_type=EventType.AGENT_DECISION,
            category=EventCategory.AGENT,
            message=message,
            payload=payload or {},
            blueprint_id=blueprint_id,
            task_id=task_id,
        )