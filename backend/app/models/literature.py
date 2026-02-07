from pydantic import BaseModel
from typing import List, Optional


class PaperOut(BaseModel):
    source: str
    title: str
    authors: List[str]
    year: Optional[int] = None
    venue: Optional[str] = None
    abstract: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None


class LiteratureResponse(BaseModel):
    query: str
    results: List[PaperOut]
    warning: Optional[str] = None  # e.g., "No results found" or "Some sources unavailable"
