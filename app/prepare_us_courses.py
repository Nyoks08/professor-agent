import sys
from pathlib import Path

import pandas as pd


def prepare_us_courses():
    """
    Read raw US courses file, clean it, and save a compact version
    for use in the Professor Agent backend.
    """
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"

    raw_path = data_dir / "us_courses_raw.csv"
    clean_path = data_dir / "us_courses_clean.csv"

    if not raw_path.exists():
        print(f"[ERROR] Raw file not found: {raw_path}")
        print("Make sure you placed the raw CSV as 'data/us_courses_raw.csv'")
        sys.exit(1)

    print(f"[INFO] Loading raw courses from: {raw_path}")
    df = pd.read_csv(raw_path)

    # Keep only useful columns if they exist
    expected_cols = ["university", "campus", "term", "department", "course", "section"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        print(f"[WARNING] These expected columns are missing in raw file: {missing}")
        print("[INFO] Available columns are:", list(df.columns))
        # Keep only intersection
        keep_cols = [c for c in expected_cols if c in df.columns]
    else:
        keep_cols = expected_cols

    df = df[keep_cols]

    # Drop rows without department or course
    for col in ["department", "course"]:
        if col in df.columns:
            df = df.dropna(subset=[col])

    # Clean strings
    for col in ["university", "campus", "term", "department", "course", "section"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Create course_title = "DEPT COURSE"
    if "department" in df.columns and "course" in df.columns:
        df["course_title"] = df["department"] + " " + df["course"].astype(str)
    else:
        df["course_title"] = ""

    # Optional: nicer label including university if present
    if "university" in df.columns:
        df["course_label"] = df["university"] + " — " + df["course_title"]
    else:
        df["course_label"] = df["course_title"]

    # Deduplicate by university + term + course_title
    dedup_cols = [c for c in ["university", "term", "course_title"] if c in df.columns]
    if dedup_cols:
        df_unique = df[dedup_cols + ["course_label"]].drop_duplicates()
    else:
        df_unique = df.drop_duplicates()

    print(f"[INFO] Saving cleaned courses to: {clean_path}")
    df_unique.to_csv(clean_path, index=False)
    print(f"[INFO] Done. Cleaned rows: {len(df_unique)}")


if __name__ == "__main__":
    prepare_us_courses()
