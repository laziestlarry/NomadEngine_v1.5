from core.settings import settings
from db.engine import init_engine
from db.session import create_session
from db.models import Base
from scheduler.scheduler_engine import start_scheduler_engine
from events.event_bus import EventBus
from events.event_store import EventStore
from events.event_definitions import EventType, EventCategory
from core.logger import logger


def bootstrap_system():
    print("[BOOTSTRAP] Starting Nomad v1.5...")

    engine = init_engine(settings.DB_PATH)
    Base.metadata.create_all(engine)

    session = create_session(engine)

    # Initialize event systems
    event_bus = EventBus()
    event_store = EventStore(session)
    event_store.attach_to_bus(event_bus)

    logger.info("[BOOTSTRAP] DB initialized.")
    logger.info("[BOOTSTRAP] Event systems ready.")

    # Announce that system is starting
    event_bus.publish(
        event_type=EventType.SYSTEM_START,
        category=EventCategory.SYSTEM,
        message="Nomad v1.5 bootstrap starting.",
    )

    # Start scheduler, pass bus + session so jobs can emit events
    start_scheduler_engine(event_bus)

    event_bus.publish(
        event_type=EventType.SYSTEM_READY,
        category=EventCategory.SYSTEM,
        message="Nomad v1.5 is online and ready.",
    )

    logger.info("[BOOTSTRAP] Scheduler online.")
    print("=== NOMAD v1.5 SYSTEM ONLINE ===")