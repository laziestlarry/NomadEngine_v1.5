from pydantic import BaseModel
from typing import Optional, Any, Dict


class StatusResponse(BaseModel):
    engine: str
    status: str
    message: str
    events_last_id: int


class TaskCreateResponse(BaseModel):
    status: str
    task_id: int
    message: str


class WorkerStatus(BaseModel):
    id: int
    name: str
    kind: str
    last_seen_at: Optional[str]
    active: bool