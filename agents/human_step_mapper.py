from typing import List, Dict, Any
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class HumanStepMapperAgent(BaseAgent):
    """
    Detects which tasks likely require human intervention (e.g., click-throughs, KYC).
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="HumanStepMapper",
            role="human_step_mapper",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def mark_human_steps(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for t in tasks:
            cat = t.get("category", "")
            requires_human = cat in ["human_prep", "kyc", "compliance"]
            t["requires_human"] = requires_human

        self.emit_decision(
            message=f"Marked human-required steps in {len(tasks)} tasks.",
            payload={"tasks": tasks},
        )

        return tasks