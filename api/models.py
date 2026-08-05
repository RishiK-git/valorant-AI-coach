from enum import Enum
from typing import Any

from pydantic import BaseModel


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class SubmitResponse(BaseModel):
    job_id: str


class StatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Any = None
    error: str | None = None
