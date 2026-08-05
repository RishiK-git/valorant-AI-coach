import uuid
from typing import Any

from api.models import JobStatus


class Job:
    def __init__(self):
        self.id: str = str(uuid.uuid4())
        self.status: JobStatus = JobStatus.pending
        self.result: Any = None
        self.error: str | None = None


# In-memory store: job_id -> Job
_jobs: dict[str, Job] = {}


def create_job() -> Job:
    """Create a new pending job and register it in the store."""
    job = Job()
    _jobs[job.id] = job
    return job


def get_job(job_id: str) -> Job | None:
    """Retrieve a job by ID. Returns None if not found."""
    return _jobs.get(job_id)
