# ace/strategy.py
from typing import Dict, Any

from sqlalchemy.orm import Session

from ace.constitution import constitution
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory
from core.logger import logger

from agents.opportunity_classifier_agent import OpportunityClassifierAgent  # <-- adjust if needed


class AceStrategy:
    """
    Lightweight ACE-style layer:
    - wraps the OpportunityClassifierAgent
    - applies constitution checks
    - emits one clear decision event
    """

    def __init__(self, session: Session, event_bus: EventBus):
        self.session = session
        self.event_bus = event_bus
        self.classifier = OpportunityClassifierAgent(session, event_bus)

    def evaluate_opportunity(
        self,
        description: str,
        source: str = "manual",
        context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Returns a decision package, e.g.:

        {
          "scores": { ... },
          "allowed": True/False,
          "constitution_check": { ... },
          "source": "youtube",
          "description": "...",
        }
        """
        context = context or {}

        scores = self.classifier.classify(
            description,
            source=source,
            extra_context=context,
        )

        # Normalise/guard
        roi = float(scores.get("roi_score", 0.0))
        auto = float(scores.get("automation_score", 0.0))
        risk = float(scores.get("risk_score", 1.0))

        allowed, check = constitution.check_scores(
            {"roi_score": roi, "automation_score": auto, "risk_score": risk}
        )

        decision = {
            "description": description,
            "source": source,
            "scores": {
                "roi_score": roi,
                "automation_score": auto,
                "risk_score": risk,
            },
            "allowed": allowed,
            "constitution_check": check,
        }

        msg = (
            f"ACE decision for opportunity (source={source}): "
            f"roi={roi:.2f}, auto={auto:.2f}, risk={risk:.2f}, allowed={allowed}"
        )

        logger.info("[ACE] " + msg)

        self.event_bus.publish(
            event_type=EventType.AGENT_DECISION,
            category=EventCategory.AGENT,
            message=msg,
            payload=decision,
        )

        return decision
