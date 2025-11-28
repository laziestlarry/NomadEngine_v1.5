from typing import Dict, Any
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class StrategyBuilderAgent(BaseAgent):
    """
    Builds a high-level strategy object from classification scores.
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="StrategyBuilder",
            role="strategy_builder",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def build_strategy(self, title: str, scores: Dict[str, float], source: str = "") -> Dict[str, Any]:
        roi = scores.get("roi_score", 0)
        auto = scores.get("automation_score", 0)
        risk = scores.get("risk_score", 0)

        if auto >= 70:
            execution_flow = ["NodeWorker", "APIConnector"]
        else:
            execution_flow = ["PythonWorker", "ManualStepPrep", "NodeWorker"]

        if roi >= 70 and risk <= 40:
            priority = 10
        elif roi >= 50:
            priority = 30
        else:
            priority = 60

        strategy = {
            "title": title,
            "source": source,
            "roi_score": roi,
            "automation_score": auto,
            "risk_score": risk,
            "execution_flow": execution_flow,
            "expected_roi_days": 3 if roi >= 70 else 7,
            "recommended_priority": priority,
        }

        self.emit_decision(
            message=f"Built strategy for '{title[:60]}...' → priority={priority}, flow={execution_flow}",
            payload=strategy,
        )

        return strategy