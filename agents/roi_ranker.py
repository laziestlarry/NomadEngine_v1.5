from typing import List, Dict, Any
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class ROIRankerAgent(BaseAgent):
    """
    Ranks opportunities or blueprints by "score":
    score = roi * 0.7 + automation * 0.3 - risk * 0.2
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="ROIRanker",
            role="roi_ranker",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def rank(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ranked = []

        for item in items:
            roi = float(item.get("roi_score", 0))
            auto = float(item.get("automation_score", 0))
            risk = float(item.get("risk_score", 0))

            score = roi * 0.7 + auto * 0.3 - risk * 0.2
            item_with_score = dict(item)
            item_with_score["combined_score"] = score
            ranked.append(item_with_score)

        ranked.sort(key=lambda x: x["combined_score"], reverse=True)

        if ranked:
            top = ranked[0]
            self.emit_decision(
                message=f"Top-ranked item: ROI={top.get('roi_score', 0):.1f}, AUTO={top.get('automation_score', 0):.1f}, RISK={top.get('risk_score', 0):.1f}, SCORE={top['combined_score']:.1f}",
                payload={"top_item": top},
            )

        return ranked