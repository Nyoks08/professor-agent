from typing import Dict, Any
from .llm_client import call_llm_json
from .data_loader import get_example_courses


def generate_lesson_plan(
    course_title: str,
    level: str,
    duration: int,
    topic: str,
) -> Dict[str, Any]:
    """
    Generate a structured lesson plan using the LLM.
    Enriches the prompt with example courses from the US courses dataset.
    """

    # ---- 1) Get example similar courses from the cleaned dataset ----
    similar_courses = get_example_courses(topic, n=5)

    if similar_courses:
        similar_courses_text_lines = []
        for c in similar_courses:
            label = c.get("course_label") or c.get("course_title") or "Unnamed course"
            uni = c.get("university", "")
            term = c.get("term", "")
            pieces = [label]
            if uni:
                pieces.append(f"({uni})")
            if term:
                pieces.append(f"[{term}]")
            line = " ".join(pieces)
            similar_courses_text_lines.append(f"- {line}")

        similar_courses_text = "\n".join(similar_courses_text_lines)
    else:
        similar_courses_text = "No matching courses found in the sample dataset."

    # ---- 2) System prompt: high-level behavior of the assistant ----
    system_prompt = (
        "You are a helpful teaching assistant for university professors. "
        "You design concise, practical lesson plans with clear learning objectives, "
        "a time-structured outline, suggested slide titles, and in-class activities. "
        "Use the example course list to stay realistic about course level, topic, "
        "and terminology, but do not mention the raw dataset in your output."
    )

    # ---- 3) User prompt: includes user input + dataset context ----
    user_prompt = f"""
Professor input
---------------
Course title: {course_title}
Level: {level}
Duration (minutes): {duration}
Lesson topic: {topic}

Example courses from a US course dataset that may be related:
{similar_courses_text}

Task
----
Using the context above, generate a lesson plan in the following JSON structure:

{{
  "course_title": "...",
  "level": "...",
  "duration_minutes": 0,
  "topic": "...",
  "learning_objectives": [
    "Objective 1",
    "Objective 2"
  ],
  "outline": [
    {{
      "time_block": "0-15 min",
      "title": "Introduction",
      "description": "..."
    }},
    {{
      "time_block": "15-35 min",
      "title": "Core Concept 1",
      "description": "..."
    }}
  ],
  "slide_ideas": [
    "Slide 1: ...",
    "Slide 2: ..."
  ],
  "activities": [
    {{
      "name": "Think-pair-share",
      "description": "Students discuss ...",
      "duration_minutes": 10
    }}
  ],
  "suggested_datasets_or_examples": [
    "Example: ...",
    "Dataset: ..."
  ]
}}

Important:
- Return ONLY JSON, no markdown, no commentary.
- Make sure the JSON is syntactically valid and parseable by json.loads in Python.
"""

    # ---- 4) Call the LLM and parse JSON ----
    result = call_llm_json(system_prompt, user_prompt)
    return result
