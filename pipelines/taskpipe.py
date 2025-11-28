from typing import List, Dict, Any
from sqlalchemy.orm import Session

from db.models import Task, Blueprint
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory
from agents.workflow_planner import WorkflowPlannerAgent
from agents.human_step_mapper import HumanStepMapperAgent
from agents.autofill_agent import AutofillAgent
from agents.optimization_agent import OptimizationAgent


class TaskPipe:
    """
    Takes a blueprint + strategy and produces concrete Task records in the DB.
    """

    def __init__(self, session: Session, event_bus: EventBus):
        self.session = session
        self.event_bus = event_bus

        self.workflow_planner = WorkflowPlannerAgent(session, event_bus)
        self.human_mapper = HumanStepMapperAgent(session, event_bus)
        self.autofill_agent = AutofillAgent(session, event_bus)
        self.optimizer = OptimizationAgent(session, event_bus)

    def create_tasks_for_blueprint(self, blueprint: Blueprint) -> List[Task]:
        strategy = blueprint.strategy or {}
        blueprint_id = blueprint.id

        # 1. Plan base tasks from strategy
        planned = self.workflow_planner.plan_tasks(blueprint_id, strategy)

        # 2. Mark human steps
        marked = self.human_mapper.mark_human_steps(planned)

        # 3. Generate autofill info
        enriched = self.autofill_agent.generate_for_tasks(blueprint.title, marked)

        # 4. Optimization pass (for future merging / tuning)
        optimized = self.optimizer.optimize(blueprint_id, enriched, strategy)

        # 5. Persist to DB as Task rows
        created_tasks: List[Task] = []

        for t in optimized:
            task = Task(
                blueprint_id=blueprint_id,
                name=t.get("name", "Unnamed task"),
                short_description=t.get("short_description", ""),
                category=t.get("category"),
                importance=t.get("importance", 50),
                priority=t.get("priority", 50),
                status="pending",
                payload={
                    "requires_human": t.get("requires_human", False),
                    "autofill": t.get("autofill"),
                },
            )
            self.session.add(task)
            self.session.flush()  # get id

            self.event_bus.publish(
                event_type=EventType.TASK_CREATED,
                category=EventCategory.TASK,
                message=f"Task #{task.id} created for blueprint #{blueprint_id}: {task.name}",
                task_id=task.id,
                blueprint_id=blueprint_id,
                payload={
                    "short_description": task.short_description,
                    "category": task.category,
                    "importance": task.importance,
                    "priority": task.priority,
                },
            )

            created_tasks.append(task)

        self.session.commit()

        # Mark blueprint as active if not already
        if blueprint.status in ("new", "approved"):
            blueprint.status = "active"
            self.session.add(blueprint)
            self.session.commit()

            self.event_bus.publish(
                event_type=EventType.BLUEPRINT_ACTIVATED,
                category=EventCategory.BLUEPRINT,
                message=f"Blueprint #{blueprint.id} activated with {len(created_tasks)} tasks.",
                blueprint_id=blueprint.id,
            )

        return created_tasks