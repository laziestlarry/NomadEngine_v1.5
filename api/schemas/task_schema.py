from pydantic import BaseModel
from typing import Optional, Dict, Any

class TaskOut(BaseModel):
    id: int
    name: str
    short_description: Optional[str]
    category: Optional[str]
    status: str
    priority: int
    importance: int
    payload: Optional[Dict[str, Any]]