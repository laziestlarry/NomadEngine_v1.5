from typing import Dict, Any, Optional
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory
from core.logger import logger


class NodeBridge:
    """
    Placeholder for a bridge to a Node.js worker.
    In v1.5, this is just a stub; later upgrades will connect it to a real Node process
    via HTTP / WebSocket / message queue.
    """

    def __init__(self, base_url: str, event_bus: EventBus):
        self.base_url = base_url
        self.event_bus = event_bus

    def send_task(self, task_payload: Dict[str, Any]) -> None:
        """
        Stub: log the intention to send to Node.
        """
        logger.info(f"[NodeBridge] Would send task to Node worker: {task_payload}")
        self.event_bus.publish(
            event_type=EventType.WORKER_HEARTBEAT,
            category=EventCategory.WORKER,
            message="NodeBridge stub invoked.",
            payload={"target_url": self.base_url},
        )

    def check_status(self) -> Optional[Dict[str, Any]]:
        """
        Stub method. Later, query Node worker health/status.
        """
        return {"status": "unknown (stub)", "url": self.base_url}