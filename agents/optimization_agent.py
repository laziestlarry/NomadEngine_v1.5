from typing import Dict, Any, List
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class OptimizationAgent(BaseAgent):
    """
    Suggests optimizations: combining tasks, reducing manual steps, etc.
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="OptimizationAgent",
            role="optimizer",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def optimize(self, blueprint_id: int, tasks: List[Dict[str, Any]], strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Simple heuristic: if there are multiple 'human_prep' tasks, combine them
        human_tasks = [t for t in tasks if t.get("category") == "human_prep"]
        if len(human_tasks) > 1:
            self.emit_decision(
                message=f"Found {len(human_tasks)} human_prep tasks, suggest combining into fewer steps.",
                payload={"blueprint_id": blueprint_id},
                blueprint_id=blueprint_id,
            )

        # For now, return tasks unchanged; later we can merge them.
        return tasks