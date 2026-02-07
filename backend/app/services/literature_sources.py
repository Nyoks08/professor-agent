from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
import time
import json
import re

import requests
from requests import Response
import xml.etree.ElementTree as ET


# -----------------------------
# Unified schema for your agent
# -----------------------------
@dataclass
class Paper:
    source: str                 # "openalex" | "crossref" | "arxiv"
    title: str
    authors: List[str]
    year: Optional[int]
    venue: Optional[str]        # journal / conference / repository
    abstract: Optional[str]
    url: Optional[str]          # landing page
    doi: Optional[str] = None


def _clean_text(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def _http_get(url: str, params: Dict[str, Any] | None = None, timeout: int = 25) -> Response:
    headers = {
        "User-Agent": "ProfessorAgent/0.1 (mailto:you@example.com)"
    }
    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r


# -----------------------------
# OpenAlex
# -----------------------------
def search_openalex(query: str, max_results: int = 10, timeout: int = 25) -> List[Paper]:
    """
    OpenAlex works endpoint: https://api.openalex.org/works?search=...
    Tip: include a real email in User-Agent if you deploy this.
    """
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per-page": max(1, min(max_results, 25)),
    }
    data = _http_get(url, params=params, timeout=timeout).json()
    results = data.get("results", []) or []

    papers: List[Paper] = []
    for w in results:
        title = _clean_text(w.get("title")) or "Untitled"
        year = w.get("publication_year")
        # Authors
        authors = []
        for a in (w.get("authorships") or []):
            name = a.get("author", {}).get("display_name")
            if name:
                authors.append(name)
        # Abstract (OpenAlex may return an inverted index)
        abstract = None
        inv = w.get("abstract_inverted_index")
        if isinstance(inv, dict):
            # rebuild inverted index to text (simple)
            tokens: Dict[int, str] = {}
            for token, positions in inv.items():
                for p in positions:
                    tokens[p] = token
            abstract = " ".join(tokens[i] for i in sorted(tokens)) if tokens else None

        venue = None
        primary = w.get("primary_location") or {}
        venue = _clean_text((primary.get("source") or {}).get("display_name"))

        doi = w.get("doi")
        url_out = w.get("id")  # OpenAlex URL to work
        papers.append(Paper(
            source="openalex",
            title=title,
            authors=authors,
            year=year if isinstance(year, int) else None,
            venue=venue,
            abstract=_clean_text(abstract),
            url=url_out,
            doi=_clean_text(doi),
        ))
    return papers


# -----------------------------
# Crossref
# -----------------------------
def search_crossref(query: str, max_results: int = 10, timeout: int = 25) -> List[Paper]:
    """
    Crossref works endpoint: https://api.crossref.org/works?query=...
    """
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": max(1, min(max_results, 25)),
        "mailto": "you@example.com",  # recommended by Crossref
    }
    data = _http_get(url, params=params, timeout=timeout).json()
    items = (data.get("message") or {}).get("items", []) or []

    papers: List[Paper] = []
    for it in items:
        title = _clean_text((it.get("title") or ["Untitled"])[0]) or "Untitled"

        # Authors
        authors = []
        for a in (it.get("author") or []):
            given = a.get("given") or ""
            family = a.get("family") or ""
            name = _clean_text(f"{given} {family}".strip())
            if name:
                authors.append(name)

        # Year
        year = None
        issued = (it.get("issued") or {}).get("date-parts")
        if isinstance(issued, list) and issued and isinstance(issued[0], list) and issued[0]:
            y = issued[0][0]
            year = y if isinstance(y, int) else None

        venue = _clean_text(it.get("container-title")[0]) if it.get("container-title") else None
        doi = _clean_text(it.get("DOI"))
        url_out = _clean_text(it.get("URL"))

        # Crossref usually doesn't include abstracts for many records
        abstract = _clean_text(it.get("abstract"))
        # abstract may be JATS / HTML-ish
        if abstract:
            abstract = re.sub(r"<[^>]+>", " ", abstract)
            abstract = _clean_text(abstract)

        papers.append(Paper(
            source="crossref",
            title=title,
            authors=authors,
            year=year,
            venue=venue,
            abstract=abstract,
            url=url_out,
            doi=doi,
        ))
    return papers


# -----------------------------
# arXiv
# -----------------------------
def search_arxiv(query: str, max_results: int = 10, timeout: int = 25) -> List[Paper]:
    """
    arXiv Atom API: http://export.arxiv.org/api/query?search_query=all:...
    Returns Atom XML; we parse it into Paper objects.
    """
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max(1, min(max_results, 25)),
    }
    xml_text = _http_get(url, params=params, timeout=timeout).text
    root = ET.fromstring(xml_text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    papers: List[Paper] = []
    for e in entries:
        title = _clean_text(e.findtext("atom:title", default="", namespaces=ns)) or "Untitled"
        abstract = _clean_text(e.findtext("atom:summary", default="", namespaces=ns))
        url_out = _clean_text(e.findtext("atom:id", default="", namespaces=ns))
        authors = [_clean_text(a.findtext("atom:name", default="", namespaces=ns)) or ""
                   for a in e.findall("atom:author", ns)]
        authors = [a for a in authors if a]

        # arXiv doesn't have venue like journals; treat as arXiv
        venue = "arXiv"
        year = None
        published = e.findtext("atom:published", default="", namespaces=ns)
        if published and len(published) >= 4 and published[:4].isdigit():
            year = int(published[:4])

        papers.append(Paper(
            source="arxiv",
            title=title,
            authors=authors,
            year=year,
            venue=venue,
            abstract=abstract,
            url=url_out,
            doi=None,
        ))
    return papers


# -----------------------------
# Multi-source search + fallback
# -----------------------------
def search_literature(
    query: str,
    max_results_per_source: int = 8,
    timeout: int = 25,
) -> List[Paper]:
    """
    Try OpenAlex first, then Crossref, then arXiv.
    Deduplicate by DOI if present, else by normalized title.
    """
    all_papers: List[Paper] = []

    try:
        all_papers.extend(search_openalex(query, max_results=max_results_per_source, timeout=timeout))
    except Exception:
        pass

    try:
        all_papers.extend(search_crossref(query, max_results=max_results_per_source, timeout=timeout))
    except Exception:
        pass

    try:
        all_papers.extend(search_arxiv(query, max_results=max_results_per_source, timeout=timeout))
    except Exception:
        pass

    # Deduplicate
    seen = set()
    deduped: List[Paper] = []
    for p in all_papers:
        key = p.doi.lower().strip() if p.doi else re.sub(r"\W+", "", p.title.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(p)

    return deduped


# -----------------------------
# Utility: JSON serialization
# -----------------------------
def papers_to_json(papers: List[Paper]) -> str:
    return json.dumps([asdict(p) for p in papers], indent=2)
