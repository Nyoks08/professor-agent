from pathlib import Path
import json
import re
from typing import List, Optional


def _repo_root() -> Path:
    # services -> app -> backend -> repo root
    return Path(__file__).resolve().parents[3]


REPO_ROOT = _repo_root()
CORPUS_PATH = REPO_ROOT / "artifacts" / "agent_corpus.jsonl"


_word_re = re.compile(r"[A-Za-z0-9_]+")


def _tokens(text: str) -> set[str]:
    return set(t.lower() for t in _word_re.findall(text))


class RetrievalService:
    def __init__(self):
        self.docs = self._load_corpus()

    def _load_corpus(self) -> List[dict]:
        if not CORPUS_PATH.exists():
            raise FileNotFoundError(f"Corpus not found: {CORPUS_PATH}")

        docs = []
        with open(CORPUS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    docs.append(json.loads(line))
        return docs

    def search(
        self,
        query: str,
        top_k: int = 5,
        source_type: Optional[str] = None,
    ) -> List[dict]:
        q = _tokens(query)
        scored = []

        for d in self.docs:
            if source_type and d.get("metadata", {}).get("source_type") != source_type:
                continue

            text = d.get("text", "")
            t = _tokens(text)
            score = len(q & t)  # overlap count

            if score > 0:
                snippet = text[:300].replace("\n", " ")
                scored.append((score, {
                    "score": score,
                    "snippet": snippet,
                    "metadata": d.get("metadata", {}),
                }))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]