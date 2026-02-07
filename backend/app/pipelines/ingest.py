from __future__ import annotations

from pathlib import Path
import json
from typing import Any


def _repo_root() -> Path:
    # pipelines -> app -> backend -> repo root
    return Path(__file__).resolve().parents[3]


REPO_ROOT = _repo_root()
DATA_DIR = REPO_ROOT / "data"


def _load_json_file(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_folder(folder: Path) -> list[dict]:
    """
    Loads JSON records from a folder.

    Supports:
    - many .json files (each file is a dict record)
    - single .json file containing a list[dict]
    """
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    files = sorted(folder.glob("*.json"))
    if not files:
        return []

    records: list[dict] = []

    for fp in files:
        data = _load_json_file(fp)

        if isinstance(data, list):
            # one file contains multiple records
            records.extend([x for x in data if isinstance(x, dict)])
        elif isinstance(data, dict):
            # one file per record
            records.append(data)
        else:
            # ignore unexpected shapes
            continue

    return records


def ingest_raw() -> dict[str, list[dict]]:
    """
    Reads raw JSON data from:
      data/faculty_profiles_raw/
      data/grants_raw/
    """
    return {
        "faculty_profiles": load_json_folder(DATA_DIR / "faculty_profiles_raw"),
        "grants": load_json_folder(DATA_DIR / "grants_raw"),
    }