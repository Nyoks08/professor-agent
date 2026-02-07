from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


BASE = Path(__file__).resolve().parents[1]  # backend/data
GRANTS_RAW = BASE / "grants_raw" / "grants.json"
FACULTY_RAW = BASE / "faculty_profiles_raw" / "faculty_profiles.json"

GRANTS_OUT = BASE / "grants_clean" / "grants_clean.json"
FACULTY_OUT = BASE / "faculty_profiles_clean" / "faculty_profiles_clean.json"


def _clean_text(x: Any) -> Optional[str]:
    if x is None:
        return None
    s = str(x)
    s = re.sub(r"\s+", " ", s).strip()
    return s if s else None


def _listify(x: Any) -> List[str]:
    """Turn string/list/None into a clean list[str]."""
    if x is None:
        return []
    if isinstance(x, list):
        items = x
    else:
        # split common separators
        items = re.split(r"[;,/|]", str(x))
    out = []
    for item in items:
        t = _clean_text(item)
        if t:
            out.append(t)
    # de-dup preserve order
    seen = set()
    dedup = []
    for t in out:
        k = t.lower()
        if k in seen:
            continue
        seen.add(k)
        dedup.append(t)
    return dedup


def _extract_first(d: Dict[str, Any], keys: List[str]) -> Any:
    """Try multiple possible keys because source JSON may vary."""
    for k in keys:
        if k in d and d[k] not in (None, "", [], {}):
            return d[k]
    return None


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------
# Grants cleaning
# ---------------------------
def clean_grants(raw: Any) -> List[Dict[str, Any]]:
    # raw can be list or dict wrapper
    records = raw.get("grants") if isinstance(raw, dict) and "grants" in raw else raw
    if not isinstance(records, list):
        raise ValueError("Grants JSON must be a list (or dict with key 'grants').")

    cleaned: List[Dict[str, Any]] = []

    for g in records:
        if not isinstance(g, dict):
            continue

        # common field guesses (adjust later once we see your real keys)
        grant_id = _extract_first(g, ["id", "ID", "opportunity_number", "Opportunity Number", "OpportunityID"])
        title = _extract_first(g, ["title", "Title", "opportunity_title", "Opportunity Title", "OpportunityName"])
        agency = _extract_first(g, ["agency", "Agency", "sponsor", "Sponsor", "Organization", "Funding Agency"])
        url = _extract_first(g, ["url", "URL", "link", "Link", "Opportunity URL"])
        deadline = _extract_first(g, ["deadline", "Deadline", "close_date", "Close Date", "Due Date"])
        desc = _extract_first(g, ["description", "Description", "synopsis", "Synopsis", "Abstract"])

        # handle nested synopsis objects (common in grants APIs)
        if isinstance(desc, dict):
            desc = _extract_first(desc, ["description", "Description", "text", "Text", "details", "Details"])

        keywords = _extract_first(g, ["keywords", "Keywords", "topics", "Topics", "Research Areas"])
        eligibility = _extract_first(g, ["eligibility", "Eligibility", "eligible_applicants", "Eligible Applicants"])

        cleaned.append({
            "id": _clean_text(grant_id) or f"grant_{uuid.uuid4().hex[:10]}",
            "title": _clean_text(title) or "Untitled grant",
            "agency": _clean_text(agency),
            "description": _clean_text(desc),
            "deadline": _clean_text(deadline),   # keep as string for now; we can normalize dates after we inspect format
            "url": _clean_text(url),
            "keywords": _listify(keywords),
            "eligibility": _listify(eligibility),
            "source": "professor_folder",
        })

    return cleaned


# ---------------------------
# Faculty cleaning
# ---------------------------
def clean_faculty(raw: Any) -> List[Dict[str, Any]]:
    records = raw.get("faculty") if isinstance(raw, dict) and "faculty" in raw else raw
    if not isinstance(records, list):
        raise ValueError("Faculty JSON must be a list (or dict with key 'faculty').")

    cleaned: List[Dict[str, Any]] = []

    for f in records:
        if not isinstance(f, dict):
            continue

        name = _extract_first(f, ["name", "Name", "full_name", "Full Name"])
        dept = _extract_first(f, ["department", "Department", "dept", "Dept", "school", "School"])
        email = _extract_first(f, ["email", "Email", "contact_email", "Contact Email"])
        bio = _extract_first(f, ["bio", "Bio", "summary", "Summary", "about", "About"])
        interests = _extract_first(f, ["interests", "Interests", "research_interests", "Research Interests", "keywords", "Keywords"])

        cleaned.append({
            "id": _clean_text(_extract_first(f, ["id", "ID"])) or f"faculty_{uuid.uuid4().hex[:10]}",
            "name": _clean_text(name) or "Unknown",
            "department": _clean_text(dept),
            "interests": _listify(interests),
            "bio": _clean_text(bio),
            "email": _clean_text(email),
        })

    return cleaned


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def main() -> None:
    grants_raw = load_json(GRANTS_RAW)
    faculty_raw = load_json(FACULTY_RAW)

    grants_clean = clean_grants(grants_raw)
    faculty_clean = clean_faculty(faculty_raw)

    write_json(GRANTS_OUT, grants_clean)
    write_json(FACULTY_OUT, faculty_clean)

    print(f"✅ Wrote {len(grants_clean)} cleaned grants → {GRANTS_OUT}")
    print(f"✅ Wrote {len(faculty_clean)} cleaned faculty → {FACULTY_OUT}")


if __name__ == "__main__":
    main()
