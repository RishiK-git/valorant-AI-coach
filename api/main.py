import asyncio
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException, UploadFile

from api.jobs import Job, create_job, get_job
from api.models import JobStatus, StatusResponse, SubmitResponse
from coach_video import coach_video

app = FastAPI(title="Valorant AI Coach")

ACCEPTED_EXTENSIONS = {
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".flv", ".wmv", ".m4v", ".ts", ".mts",
}

INTERVAL_SEC = 2.0
MAX_FRAMES = 20

_executor = ThreadPoolExecutor()


def _run_analysis(job: Job, video_path: str) -> None:
    """
    Blocking analysis task — runs in a thread pool.
    Updates the job in-place on completion or failure.
    """
    try:
        job.status = JobStatus.running
        job.result = coach_video(video_path, interval_sec=INTERVAL_SEC, max_frames=MAX_FRAMES)
        job.status = JobStatus.completed
    except Exception as exc:
        job.status = JobStatus.failed
        job.error = str(exc)
    finally:
        os.unlink(video_path)


@app.post("/analyze", response_model=SubmitResponse, status_code=202)
async def analyze(file: UploadFile):
    """
    Accept a video upload, enqueue analysis, and return a job ID.
    Poll GET /status/{job_id} for results.
    """
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in ACCEPTED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Accepted: {sorted(ACCEPTED_EXTENSIONS)}",
        )

    # Write upload to a temp file that persists until analysis finishes
    suffix = ext
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    job = create_job()
    loop = asyncio.get_event_loop()
    loop.run_in_executor(_executor, _run_analysis, job, tmp_path)

    return SubmitResponse(job_id=job.id)


@app.get("/status/{job_id}", response_model=StatusResponse)
async def status(job_id: str):
    """Return the current status and result (if completed) for a job."""
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return StatusResponse(
        job_id=job.id,
        status=job.status,
        result=job.result,
        error=job.error,
    )
