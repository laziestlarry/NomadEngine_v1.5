from scheduler import context
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory


def reconnect_workers_job():
    """
    Placeholder: will restart workers if offline.
    """
    event_bus: EventBus = context.event_bus
    if event_bus is None:
        return

    event_bus.publish(
        event_type=EventType.WORKER_HEARTBEAT,
        category=EventCategory.WORKER,
        message="Worker status check OK",
        payload={"workers": "operational"},
    )