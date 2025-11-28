from sqlalchemy.orm import Session
from db.engine import init_engine
from db.session import create_session
from db.models import Blueprint

from scheduler import context
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory

from agents.opportunity_classifier import OpportunityClassifierAgent
from agents.roi_ranker import ROIRankerAgent
from agents.strategy_builder import StrategyBuilderAgent
import random


SAMPLE_OPPORTUNITIES = [
    "Get paid to label AI datasets",
    "Earn by classifying short audio clips",
    "Automated affiliate income with AI tools",
    "Moderate AI-generated images",
    "Get paid to help train LLMs",
]


def alpha_scan_job():
    """
    Every scan produces ONE new blueprint from random sample.
    Later replaced with real scrapers / APIs.
    """

    # Build local session
    engine = init_engine()
    session: Session = create_session(engine)

    try:
        event_bus: EventBus = context.event_bus
        if event_bus is None:
            # No bus registered, nothing to do.
            return

        title = random.choice(SAMPLE_OPPORTUNITIES)

        # Agents
        classifier = OpportunityClassifierAgent(session, event_bus)
        ranker = ROIRankerAgent(session, event_bus)
        strategist = StrategyBuilderAgent(session, event_bus)

        scores = classifier.classify(title, source="alpha_scan")
        ranked = ranker.rank([scores])
        strategy = strategist.build_strategy(title, scores, source="alpha_scan")

        bp = Blueprint(
            title=title,
            source="alpha_scan",
            origin_url="N/A",
            roi_score=scores["roi_score"],
            automation_score=scores["automation_score"],
            risk_score=scores["risk_score"],
            strategy=strategy,
            status="new",
        )
        session.add(bp)
        session.commit()

        event_bus.publish(
            event_type=EventType.BLUEPRINT_DISCOVERED,
            category=EventCategory.BLUEPRINT,
            message=f"Alpha Scan discovered blueprint: {title}",
            blueprint_id=bp.id,
            payload=strategy,
        )
    finally:
        session.close()