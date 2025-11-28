import datetime as dt
from typing import Optional, Dict, Any


class EventCategory:
    SYSTEM = "system"
    TASK = "task"
    BLUEPRINT = "blueprint"
    WORKER = "worker"
    SCHEDULER = "scheduler"
    INCOME = "income"
    AGENT = "agent"
    HEALTH = "health"


class EventType:
    # System lifecycle
    SYSTEM_START = "system_start"
    SYSTEM_READY = "system_ready"
    SYSTEM_ERROR = "system_error"

    # Tasks
    TASK_CREATED = "task_created"
    TASK_ASSIGNED = "task_assigned"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"

    # Blueprints
    BLUEPRINT_DISCOVERED = "blueprint_discovered"
    BLUEPRINT_APPROVED = "blueprint_approved"
    BLUEPRINT_REJECTED = "blueprint_rejected"
    BLUEPRINT_ACTIVATED = "blueprint_activated"

    # Workers
    WORKER_ONLINE = "worker_online"
    WORKER_OFFLINE = "worker_offline"
    WORKER_HEARTBEAT = "worker_heartbeat"

    # Scheduler
    SCHEDULER_JOB_RUN = "scheduler_job_run"
    SCHEDULER_JOB_ERROR = "scheduler_job_error"

    # Income / money
    INCOME_DETECTED = "income_detected"
    INCOME_PAYOUT_CONFIRMED = "income_payout_confirmed"

    # Agents / AI brains
    AGENT_DECISION = "agent_decision"
    AGENT_ERROR = "agent_error"

    # Health checks
    HEALTH_WARNING = "health_warning"
    HEALTH_RECOVERY = "health_recovery"


def make_event(
    event_type: str,
    category: str,
    message: str = "",
    payload: Optional[Dict[str, Any]] = None,
    task_id: Optional[int] = None,
    blueprint_id: Optional[int] = None,
    worker_id: Optional[int] = None,
    agent_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Helper to create a consistent event dict that both EventBus and EventStore can handle.
    """
    return {
        "id": None,  # EventBus will assign an in-memory ID
        "type": event_type,
        "category": category,
        "message": message,
        "payload": payload or {},
        "task_id": task_id,
        "blueprint_id": blueprint_id,
        "worker_id": worker_id,
        "agent_id": agent_id,
        "created_at": dt.datetime.utcnow().isoformat(),
    }