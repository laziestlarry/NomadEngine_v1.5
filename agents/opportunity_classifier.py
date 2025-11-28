from typing import Dict, Any
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class OpportunityClassifierAgent(BaseAgent):
    """
    Classifies an opportunity into:
    - roi_score (0–100)
    - automation_score (0–100)
    - risk_score (0–100)
    Using simple heuristics now, later upgradable to LLM.
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="OpportunityClassifier",
            role="classifier",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def classify(self, title: str, source: str = "", metadata: Dict[str, Any] = None) -> Dict[str, float]:
        text = (title or "").lower()
        metadata = metadata or {}

        roi = 50.0
        automation = 50.0
        risk = 50.0

        # Heuristics (simple for now)
        if "ai" in text or "automation" in text or "bot" in text:
            automation += 25

        if "get paid" in text or "earn" in text or "income" in text:
            roi += 15

        if "no experience" in text or "beginner" in text:
            roi += 5

        if "survey" in text or "captcha" in text or "manual typing" in text:
            roi -= 15
            automation -= 10

        if "crypto" in text or "forex" in text or "binary options" in text:
            risk += 20
            roi -= 10

        # clamp 0–100
        roi = max(0, min(100, roi))
        automation = max(0, min(100, automation))
        risk = max(0, min(100, risk))

        result = {
            "roi_score": roi,
            "automation_score": automation,
            "risk_score": risk,
            "source": source,
        }

        self.emit_decision(
            message=f"Classified opportunity '{title[:60]}...' → ROI={roi:.1f}, AUTO={automation:.1f}, RISK={risk:.1f}",
            payload=result,
        )

        return result