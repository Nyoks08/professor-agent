from __future__ import annotations

from pathlib import Path
import json


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


REPO_ROOT = _repo_root()
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

CORPUS_PATH = ARTIFACTS_DIR / "agent_corpus.jsonl"


def build_agent_corpus(docs: list[dict]) -> Path:
    """
    Builds a JSONL corpus the agent can retrieve from.
    Each line: {"text": "...", "metadata": {...}}
    """
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        for d in docs:
            keywords = d.get("keywords") or []
            people = d.get("people") or []

            text = (
                f"Title: {d.get('title','')}\n"
                f"Type: {d.get('source_type','')}\n"
                f"Summary: {d.get('summary','')}\n"
                f"People: {', '.join([str(p) for p in people if p])}\n"
                f"Organization: {d.get('org','')}\n"
                f"Year: {d.get('year','')}\n"
                f"Keywords: {', '.join([str(k) for k in keywords if k])}\n"
            ).strip()

            row = {
                "text": text,
                "metadata": {
                    "doc_id": d.get("doc_id"),
                    "source_type": d.get("source_type"),
                },
            }

            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return CORPUS_PATH