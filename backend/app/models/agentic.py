from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class StepStatus(BaseModel):
    name: str
    status: str
    message: Optional[str] = None

class AgenticStartRequest(BaseModel):
    goal: str
    profile_text: Optional[str] = None
    project_idea: Optional[str] = None

class AgenticStartResponse(BaseModel):
    job_id: str
    status: str
    steps: List[StepStatus]
    artifacts: Dict[str, Any] = {}
    error: Optional[str] = None

class AgenticStatusResponse(AgenticStartResponse):
    pass
