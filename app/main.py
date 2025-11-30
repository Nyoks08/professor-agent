from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import get_settings
from .teaching import generate_lesson_plan
from .research import generate_research_suggestions

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend for Professor Agent – Teaching & Research Assistant",
)

# Allow frontend (Streamlit/React) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LessonRequest(BaseModel):
    course_title: str
    level: str
    duration_minutes: int
    topic: str


class ResearchRequest(BaseModel):
    idea: str


@app.get("/")
def root():
    return {"message": "Professor Agent backend running", "version": settings.app_version}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate_lesson")
def lesson_endpoint(req: LessonRequest):
    result = generate_lesson_plan(
        course_title=req.course_title,
        level=req.level,
        duration=req.duration_minutes,
        topic=req.topic,
    )
    return {"request": req, "result": result}


@app.post("/research_helper")
def research_endpoint(req: ResearchRequest):
    result = generate_research_suggestions(idea=req.idea)
    return {"request": req, "result": result}
