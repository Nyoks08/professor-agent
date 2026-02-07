from fastapi import APIRouter, Query
from typing import Optional

from app.services.retrieval_service import RetrievalService

router = APIRouter()

# simple in-memory singleton (fine for demos)
_retriever = RetrievalService()


@router.get("/retrieve")
def retrieve(
    query: str = Query(..., min_length=2),
    top_k: int = Query(5, ge=1, le=20),
    source_type: Optional[str] = Query(None, description="grant or faculty_profile"),
):
    results = _retriever.search(query=query, top_k=top_k, source_type=source_type)
    return {"query": query, "top_k": top_k, "source_type": source_type, "results": results}