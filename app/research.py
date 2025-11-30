from typing import Dict, Any, List, Optional

from .llm_client import call_llm_json
from .data_loader import (
    load_openalex_sample,
    load_nih_grants_sample,
    get_example_edx_courses,
)


def _format_papers_for_prompt(papers: List[Dict[str, Any]], max_items: int = 5) -> str:
    lines = []
    for p in papers[:max_items]:
        title = p.get("title", "Untitled")
        year = p.get("publication_year", "")
        authorships = p.get("authorships") or []
        first_author = ""
        if authorships:
            first_author = authorships[0].get("author", {}).get("display_name", "")
        parts = [f"• {title}"]
        if year:
            parts.append(f"({year})")
        if first_author:
            parts.append(f"— {first_author}")
        lines.append(" ".join(parts))
    return "\n".join(lines) if lines else "No related papers found in the sample."


def _format_grants_for_prompt(grants: List[Dict[str, Any]], max_items: int = 5) -> str:
    lines = []
    for g in grants[:max_items]:
        title = g.get("project_title", "Untitled grant")
        inst = g.get("institute", g.get("agency", "NIH"))
        mech = g.get("mechanism", "")
        year = g.get("fiscal_year", "")
        terms = ", ".join(g.get("project_terms", [])[:3])
        parts = [f"• {title}"]
        meta = []
        if inst:
            meta.append(inst)
        if mech:
            meta.append(mech)
        if year:
            meta.append(str(year))
        if meta:
            parts.append(f"({', '.join(meta)})")
        if terms:
            parts.append(f"— key terms: {terms}")
        lines.append(" ".join(parts))
    return "\n".join(lines) if lines else "No grants found in the sample."


def _format_courses_for_prompt(courses: List[Dict[str, Any]], max_items: int = 5) -> str:
    lines = []
    for c in courses[:max_items]:
        title = c.get("course_title") or c.get("title") or "Untitled course"
        subject = c.get("subject", "")
        level = c.get("level", "")
        parts = [f"• {title}"]
        meta = [x for x in [subject, level] if x]
        if meta:
            parts.append(f"({', '.join(meta)})")
        lines.append(" ".join(parts))
    return "\n".join(lines) if lines else "No online courses found in the sample."


def generate_research_helper(
    idea: str,
    discipline: Optional[str] = None,
    target_audience: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a structured research brief for a professor's idea.
    Uses OpenAlex papers, NIH grants, and optional EdX courses as context.
    """

    # ---- 1) Load datasets ----
    papers = load_openalex_sample()
    grants = load_nih_grants_sample()
    edx_courses = get_example_edx_courses(idea, n=5)

    papers_text = _format_papers_for_prompt(papers, max_items=5)
    grants_text = _format_grants_for_prompt(grants, max_items=5)
    courses_text = _format_courses_for_prompt(edx_courses, max_items=5)

    # ---- 2) System prompt ----
    system_prompt = (
        "You are an AI research assistant helping university professors shape research projects. "
        "Given an initial idea and some example papers, grants, and online courses, "
        "you propose refined research questions, methods, datasets, and possible funding directions. "
        "You must be realistic and grounded in the context provided. "
        "Do NOT fabricate citations; if unsure, keep suggestions high-level."
    )

    # ---- 3) User prompt with embedded context ----
    user_prompt = f"""
Professor's initial idea:
-------------------------
{idea}

Discipline (if provided): {discipline or "not specified"}
Target audience (if provided): {target_audience or "not specified"}

Sample research papers (from OpenAlex sample):
----------------------------------------------
{papers_text}

Sample NIH-style grants:
------------------------
{grants_text}

Sample online courses (from EdX dataset, if any):
-------------------------------------------------
{courses_text}

Task:
-----
Using the information above, produce a JSON object with the following structure:

{{
  "refined_research_question": "...",
  "background_summary": "...",
  "related_papers": [
    {{
      "title": "...",
      "year": 2020,
      "lead_author": "...",
      "why_relevant": "..."
    }}
  ],
  "potential_grants": [
    {{
      "agency": "NIH",
      "institute": "NIGMS",
      "mechanism": "R25",
      "project_title": "...",
      "fit_reason": "Why this project idea aligns with the grant."
    }}
  ],
  "suggested_methods": [
    "Method 1",
    "Method 2"
  ],
  "suggested_datasets_or_tools": [
    "Dataset or tool 1",
    "Dataset or tool 2"
  ],
  "ethical_or_practical_considerations": [
    "Risk / constraint 1",
    "Risk / constraint 2"
  ],
  "possible_course_integration": [
    "How this research could feed into a course or module."
  ]
}}

Important:
- Return ONLY valid JSON, no markdown and no commentary.
- Make the JSON parseable by json.loads in Python.
- If you don't have enough information for specific fields, keep them high-level rather than inventing details.
"""

    return call_llm_json(system_prompt, user_prompt)


# Optional alias in case main.py expects a different name
generate_research_brief = generate_research_helper

# Backwards compatibility wrapper for main.py
def generate_research_suggestions(
    idea: str,
    discipline: str = None,
    target_audience: str = None
):
    return generate_research_helper(
        idea=idea,
        discipline=discipline,
        target_audience=target_audience
    )