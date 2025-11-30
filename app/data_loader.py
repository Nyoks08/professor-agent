import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


# ---------- Courses (Teaching Mode) ----------

def load_us_courses_clean() -> pd.DataFrame:
    """
    Load the cleaned US courses file created by prepare_us_courses.py.
    """
    path = DATA_DIR / "us_courses_clean.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Clean courses file not found at {path}. "
            f"Run 'python -m app.prepare_us_courses' first."
        )
    return pd.read_csv(path)


def get_example_courses(keyword: str, n: int = 5) -> List[Dict[str, Any]]:
    """
    Return up to n courses whose course_title contains the keyword.
    Used to enrich lesson-plan prompts with realistic course context.
    """
    df = load_us_courses_clean()
    if "course_title" not in df.columns:
        return []

    mask = df["course_title"].str.contains(keyword, case=False, na=False)
    subset = df[mask].head(n)

    cols = [c for c in ["university", "term", "course_title", "course_label"] if c in subset.columns]
    return subset[cols].to_dict(orient="records")


def load_edx_courses() -> Optional[pd.DataFrame]:
    """
    Load EdX course metadata if the file exists.
    This is optional enrichment for teaching / research prompts.
    """
    path = DATA_DIR / "edx_courses.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def get_example_edx_courses(keyword: str, n: int = 5) -> List[Dict[str, Any]]:
    df = load_edx_courses()
    if df is None:
        return []

    # try common text columns; adjust if your file uses different names
    text_cols = [c for c in ["course_title", "title", "short_description"] if c in df.columns]
    if not text_cols:
        return []

    mask = False
    for col in text_cols:
        mask = mask | df[col].astype(str).str.contains(keyword, case=False, na=False)

    subset = df[mask].head(n)
    cols = [c for c in ["course_title", "title", "subject", "level"] if c in subset.columns]
    if not cols:
        cols = subset.columns.tolist()

    return subset[cols].to_dict(orient="records")


def load_lesson_plan_samples() -> List[Dict[str, Any]]:
    """
    Load few-shot lesson plan examples (if you created lesson_plan_samples.json).
    """
    path = DATA_DIR / "lesson_plan_samples.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- OpenAlex Sample (Research Mode) ----------

def load_openalex_sample(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Load the cleaned OpenAlex sample JSON (a list of works).
    Default: data/openalex_sample.json
    """
    p = path or (DATA_DIR / "openalex_sample.json")
    if not p.exists():
        raise FileNotFoundError(f"OpenAlex sample file not found at {p}")

    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- NIH Grants Sample (Research Mode) ----------

def load_nih_grants_sample(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Load the NIH grants sample JSON (a list of grants).
    Default: data/nih_grants_sample.json
    """
    p = path or (DATA_DIR / "nih_grants_sample.json")
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)
