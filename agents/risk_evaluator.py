from typing import Dict, Any
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class RiskEvaluatorAgent(BaseAgent):
    """
    Interprets risk_score into a simple narrative category for your dashboard.
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="RiskEvaluator",
            role="risk_evaluator",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def evaluate(self, scores: Dict[str, float]) -> Dict[str, Any]:
        risk = scores.get("risk_score", 0)

        if risk <= 30:
            level = "low"
        elif risk <= 60:
            level = "medium"
        else:
            level = "high"

        result = {"risk_score": risk, "risk_level": level}
        self.emit_decision(
            message=f"Risk evaluated as {level.upper()} (score={risk:.1f}).",
            payload=result,
        )
        return result