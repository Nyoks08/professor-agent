import threading
import uuid
from typing import Dict, Any, Optional

JOBS: Dict[str, Dict[str, Any]] = {}
LOCK = threading.Lock()

# Put context retrieval early (Option 2: after goal is available, before planning)
DEFAULT_STEPS = [
    {"name": "context_retrieval", "status": "queued", "message": None},

    {"name": "lesson_plan", "status": "queued", "message": None},
    {"name": "slides", "status": "queued", "message": None},
    {"name": "grants", "status": "queued", "message": None},
    {"name": "collaborators", "status": "queued", "message": None},
    {"name": "literature", "status": "queued", "message": None},
    {"name": "proposal", "status": "queued", "message": None},
]

def create_job(payload: Optional[dict] = None) -> str:
    job_id = str(uuid.uuid4())
    with LOCK:
        JOBS[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "payload": payload or {},
            "steps": [dict(s) for s in DEFAULT_STEPS],
            "artifacts": {},
            "error": None,
        }
    return job_id

def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    with LOCK:
        job = JOBS.get(job_id)
        return dict(job) if job else None

def update_job_status(job_id: str, status: str, error: Optional[str] = None) -> None:
    with LOCK:
        if job_id in JOBS:
            JOBS[job_id]["status"] = status
            JOBS[job_id]["error"] = error

def update_step(job_id: str, step_name: str, status: str, message: Optional[str] = None) -> None:
    with LOCK:
        job = JOBS.get(job_id)
        if not job:
            return
        for s in job["steps"]:
            if s["name"] == step_name:
                s["status"] = status
                s["message"] = message
                return

def set_artifact(job_id: str, key: str, value: Any) -> None:
    with LOCK:
        job = JOBS.get(job_id)
        if not job:
            return
        job["artifacts"][key] = value