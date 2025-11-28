from sqlalchemy.orm import Session
from db.engine import init_engine
from db.session import create_session
from db.models import IncomeRecord

from scheduler import context
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory

import random


def income_scan_job():
    """
    Simulates an income detection event.
    Later replaced with Toloka/Hive/Remotasks API queries.
    """

    engine = init_engine()
    session: Session = create_session(engine)

    try:
        event_bus: EventBus = context.event_bus
        if event_bus is None:
            return

        amount = round(random.uniform(0.25, 2.5), 2)
        rec = IncomeRecord(
            platform="simulated",
            amount=amount,
            currency="USD",
        )
        session.add(rec)
        session.commit()

        event_bus.publish(
            event_type=EventType.INCOME_DETECTED,
            category=EventCategory.INCOME,
            message=f"Income detected: ${amount}",
            payload={"amount": amount},
        )
    finally:
        session.close()