from typing import Dict, Any, List
from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent


class WorkflowPlannerAgent(BaseAgent):
    """
    Plans a concrete workflow (task list) from a blueprint strategy.
    """

    def __init__(self, session: Session, event_bus, config=None):
        super().__init__(
            name="WorkflowPlanner",
            role="workflow_planner",
            session=session,
            event_bus=event_bus,
            config=config or {},
        )

    def plan_tasks(self, blueprint_id: int, strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        flow = strategy.get("execution_flow", [])
        tasks: List[Dict[str, Any]] = []

        # Very simple initial mapping:
        for step in flow:
            if step == "NodeWorker":
                tasks.append({
                    "name": "Execute platform automation",
                    "short_description": "Run income platform API / browser automation.",
                    "category": "platform_exec",
                    "importance": 80,
                    "priority": strategy.get("recommended_priority", 50),
                })
            elif step == "APIConnector":
                tasks.append({
                    "name": "Configure API connectors",
                    "short_description": "Set up necessary API keys and endpoints for this stream.",
                    "category": "setup",
                    "importance": 70,
                    "priority": strategy.get("recommended_priority", 50) + 5,
                })
            elif step == "ManualStepPrep":
                tasks.append({
                    "name": "Prepare manual steps",
                    "short_description": "Generate pre-filled forms / answers for required human clicks.",
                    "category": "human_prep",
                    "importance": 60,
                    "priority": strategy.get("recommended_priority", 50) + 10,
                })
            elif step == "PythonWorker":
                tasks.append({
                    "name": "Run Python-side logic",
                    "short_description": "Execute Python scripts for data preparation / checks.",
                    "category": "compute",
                    "importance": 65,
                    "priority": strategy.get("recommended_priority", 50),
                })

        self.emit_decision(
            message=f"Planned {len(tasks)} tasks for blueprint #{blueprint_id}.",
            payload={"blueprint_id": blueprint_id, "tasks": tasks},
            blueprint_id=blueprint_id,
        )

        return tasks