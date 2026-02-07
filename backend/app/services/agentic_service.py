import threading
import time
from typing import Callable, Dict

from app.models.agentic import AgenticStartRequest, AgenticStartResponse, AgenticStatusResponse
from app.infra.job_store import (
    create_job, get_job, update_job_status, update_step, set_artifact
)
from app.services.literature_service import run_literature_search
from app.services.retrieval_service import RetrievalService


# ---------------------------
# Retrieval singleton (loads corpus once)
# ---------------------------
_retriever = RetrievalService()


# ---------------------------
# Agent "actions" (steps)
# ---------------------------

def _action_context_retrieval(job_id: str, payload: dict) -> None:
    """
    Runs AFTER goal is parsed/available and BEFORE planning steps.
    Pulls relevant faculty + grants from artifacts/agent_corpus.jsonl.
    """
    update_step(job_id, "context_retrieval", "running", "Retrieving local context (faculty + grants)...")

    query = payload.get("goal") or payload.get("project_idea") or "research topic"

    faculty_hits = _retriever.search(query=query, top_k=5, source_type="faculty_profile")
    grant_hits = _retriever.search(query=query, top_k=5, source_type="grant")

    context = {
        "query": query,
        "top_k": 5,
        "results": {
            "faculty": faculty_hits,
            "grants": grant_hits,
        },
    }

    set_artifact(job_id, "context_retrieval", context)
    update_step(job_id, "context_retrieval", "done", f"Context retrieved (faculty={len(faculty_hits)}, grants={len(grant_hits)})")


def _action_lesson_plan(job_id: str, payload: dict) -> None:
    update_step(job_id, "lesson_plan", "running", "Drafting lesson plan...")
    time.sleep(0.7)  # placeholder (later replace with your ML/LLM logic)
    set_artifact(job_id, "lesson_plan", {"outline": ["Week 1...", "Week 2..."]})
    update_step(job_id, "lesson_plan", "done", "Lesson plan created")


def _action_slides(job_id: str, payload: dict) -> None:
    update_step(job_id, "slides", "running", "Preparing slide outline...")
    time.sleep(0.7)
    set_artifact(job_id, "slides", {"slides": ["Title", "Agenda", "Content..."]})
    update_step(job_id, "slides", "done", "Slides outline created")


def _action_grants(job_id: str, payload: dict) -> None:
    """
    Placeholder. Later you can use artifacts['context_retrieval'] to seed grant suggestions.
    """
    update_step(job_id, "grants", "running", "Searching grants...")
    time.sleep(0.7)
    set_artifact(job_id, "grants", {"top_grants": []})  # later: NIH/NSF/Grants.gov
    update_step(job_id, "grants", "done", "Grant search complete")


def _action_collaborators(job_id: str, payload: dict) -> None:
    """
    Placeholder. Later you can use artifacts['context_retrieval'] faculty hits to recommend collaborators.
    """
    update_step(job_id, "collaborators", "running", "Matching collaborators...")
    time.sleep(0.7)
    set_artifact(job_id, "collaborators", {"matches": []})  # later: profiles_cua.json
    update_step(job_id, "collaborators", "done", "Collaborators matched")


def _action_literature(job_id: str, payload: dict) -> None:
    update_step(job_id, "literature", "running", "Searching literature sources...")
    query = payload.get("goal") or payload.get("project_idea") or "research topic"
    lit = run_literature_search(query)
    set_artifact(job_id, "literature", lit.model_dump())
    update_step(job_id, "literature", "done", "Literature results collected")


def _action_proposal(job_id: str, payload: dict) -> None:
    update_step(job_id, "proposal", "running", "Drafting proposal outline...")
    time.sleep(0.7)
    set_artifact(job_id, "proposal", {"proposal_outline": ["Problem", "Methods", "Timeline"]})
    update_step(job_id, "proposal", "done", "Proposal outline drafted")


ACTIONS: Dict[str, Callable[[str, dict], None]] = {
    "context_retrieval": _action_context_retrieval,  # ✅ new step
    "lesson_plan": _action_lesson_plan,
    "slides": _action_slides,
    "grants": _action_grants,
    "collaborators": _action_collaborators,
    "literature": _action_literature,
    "proposal": _action_proposal,
}


# ---------------------------
# Worker that runs steps
# ---------------------------
def _run_job(job_id: str) -> None:
    job = get_job(job_id)
    if not job:
        return

    update_job_status(job_id, "running")

    payload = job.get("payload", {})

    try:
        for step in job["steps"]:
            name = step["name"]
            action = ACTIONS.get(name)
            if not action:
                update_step(job_id, name, "failed", "No action implemented")
                raise RuntimeError(f"No action implemented for step: {name}")

            action(job_id, payload)

        update_job_status(job_id, "done")

    except Exception as e:
        update_job_status(job_id, "failed", error=str(e))


# ---------------------------
# Public functions called by API
# ---------------------------

def start_agentic_job(payload: AgenticStartRequest) -> AgenticStartResponse:
    job_id = create_job(payload.model_dump())

    # Start worker in background (simple thread for now)
    t = threading.Thread(target=_run_job, args=(job_id,), daemon=True)
    t.start()

    job = get_job(job_id)
    return AgenticStartResponse(
        job_id=job_id,
        status=job["status"],
        steps=job["steps"],
        artifacts=job.get("artifacts", {}),
        error=job.get("error"),
    )


def get_agentic_job_status(job_id: str) -> AgenticStatusResponse:
    job = get_job(job_id)
    if not job:
        # You can convert to HTTPException in the endpoint layer later
        return AgenticStatusResponse(
            job_id=job_id,
            status="not_found",
            steps=[],
            artifacts={},
            error="Job not found",
        )

    return AgenticStatusResponse(
        job_id=job_id,
        status=job["status"],
        steps=job["steps"],
        artifacts=job.get("artifacts", {}),
        error=job.get("error"),
    )