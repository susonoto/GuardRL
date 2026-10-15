from typing import Literal, Optional
from pydantic import BaseModel, Field, IPvAnyAddress

class LogEvent(BaseModel):
    timestamp: str
    src_ip: IPvAnyAddress
    username: Optional[str] = None
    event_type: str = "unknown"
    status_code: Optional[int] = None
    path: str = "/"
    user_agent: str = "unknown"
    bytes_sent: int = Field(default=0, ge=0)

class Decision(BaseModel):
    employee_id: str = Field(min_length=2, max_length=128)
    decision: Literal["approve", "reject"]
    reason: str = Field(min_length=3, max_length=1000)
    ticket_id: Optional[str] = None
