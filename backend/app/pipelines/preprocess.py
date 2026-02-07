from __future__ import annotations

from typing import Any


def _as_list(x: Any) -> list:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def normalize_faculty(record: dict) -> dict:
    """
    Map your faculty JSON into the canonical schema.
    NOTE: If your keys differ, tell me one sample record and I’ll adjust this mapping.
    """
    name = record.get("name") or record.get("full_name") or record.get("faculty_name")
    bio = record.get("bio") or record.get("biography") or record.get("summary") or ""

    interests = record.get("research_interests") or record.get("interests") or record.get("keywords") or []

    return {
        "doc_id": record.get("id") or record.get("faculty_id") or name,
        "source_type": "faculty_profile",
        "title": name or "Unknown Faculty",
        "summary": bio,
        "people": [name] if name else [],
        "org": record.get("institution") or record.get("department") or "",
        "year": None,
        "keywords": _as_list(interests),
        "raw": record,
    }


def normalize_grant(record: dict) -> dict:
    """
    Map your grant JSON into the canonical schema.
    """
    title = record.get("title") or record.get("grant_title") or "Untitled Grant"
    abstract = record.get("abstract") or record.get("summary") or ""

    investigators = (
        record.get("investigators")
        or record.get("pi")
        or record.get("principal_investigator")
        or record.get("authors")
        or []
    )

    return {
        "doc_id": record.get("award_id") or record.get("id") or record.get("grant_id") or title,
        "source_type": "grant",
        "title": title,
        "summary": abstract,
        "people": _as_list(investigators),
        "org": record.get("institution") or record.get("funder") or "",
        "year": record.get("year") or record.get("award_year"),
        "keywords": _as_list(record.get("keywords") or record.get("topics") or []),
        "raw": record,
    }


def preprocess(raw: dict[str, list[dict]]) -> list[dict]:
    docs: list[dict] = []

    for r in raw.get("faculty_profiles", []):
        docs.append(normalize_faculty(r))

    for r in raw.get("grants", []):
        docs.append(normalize_grant(r))

    return docs