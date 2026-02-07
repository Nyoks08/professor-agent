from fastapi import APIRouter, Query
from app.models.literature import LiteratureResponse
from app.services.literature_service import run_literature_search

router = APIRouter()

@router.get("/literature_review", response_model=LiteratureResponse)
def literature_review(query: str = Query(..., min_length=3, description="Topic or research question")):
    return run_literature_search(query)
