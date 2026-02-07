from fastapi import APIRouter, HTTPException
from app.models.agentic import AgenticStartRequest, AgenticStartResponse, AgenticStatusResponse
from app.services.agentic_service import start_agentic_job, get_agentic_job_status

router = APIRouter()

@router.post("/agentic_workflow_async", response_model=AgenticStartResponse)
def agentic_workflow_async(payload: AgenticStartRequest):
    return start_agentic_job(payload)

@router.get("/agentic_workflow_status/{job_id}", response_model=AgenticStatusResponse)
def agentic_workflow_status(job_id: str):
    job = get_agentic_job_status(job_id)
    if job.status == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    return job
