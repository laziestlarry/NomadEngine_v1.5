from db.engine import init_engine
from db.session import create_session

from scheduler import context
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory


def health_check_job():
    """
    Basic heartbeat: confirms scheduler is alive.
    """

    # If needed later, can inspect DB state. For now, no DB queries.
    event_bus: EventBus = context.event_bus
    if event_bus is None:
        return

    event_bus.publish(
        event_type=EventType.HEALTH_RECOVERY,
        category=EventCategory.HEALTH,
        message="Scheduler heartbeat OK",
        payload={"status": "alive"},
    )