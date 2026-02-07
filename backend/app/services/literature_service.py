from typing import List, Optional
import logging

from fastapi import HTTPException
from app.models.literature import LiteratureResponse, PaperOut
from app.services.literature_sources import search_literature

logger = logging.getLogger(__name__)

def run_literature_search(query: str) -> LiteratureResponse:
    """
    Calls external literature sources (OpenAlex/Crossref/arXiv) and returns a Pydantic response.
    Includes simple error handling and empty-result handling.
    """
    try:
        papers = search_literature(query, max_results_per_source=5, timeout=25)
    except Exception as e:
        logger.exception("Literature search failed")
        # Clean API error for frontend
        raise HTTPException(status_code=502, detail="Literature sources unavailable right now. Try again later.")

    results: List[PaperOut] = [
        PaperOut(
            source=p.source,
            title=p.title,
            authors=p.authors,
            year=p.year,
            venue=p.venue,
            abstract=p.abstract,
            url=p.url,
            doi=getattr(p, "doi", None),
        )
        for p in papers
    ]

    warning: Optional[str] = None
    if not results:
        warning = "No results found for this query. Try a broader keyword."

    return LiteratureResponse(query=query, results=results, warning=warning)
