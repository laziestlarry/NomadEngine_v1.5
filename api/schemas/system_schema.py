from pydantic import BaseModel

class SystemStatus(BaseModel):
    engine: str
    status: str
    message: str
    events_last_id: int