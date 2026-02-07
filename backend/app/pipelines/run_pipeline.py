from app.pipelines.ingest import ingest_raw
from app.pipelines.preprocess import preprocess
from app.pipelines.build_corpus import build_agent_corpus


def run():
    raw = ingest_raw()
    print(f"Loaded faculty_profiles: {len(raw['faculty_profiles'])}")
    print(f"Loaded grants: {len(raw['grants'])}")

    docs = preprocess(raw)
    print(f"Normalized docs total: {len(docs)}")

    out_path = build_agent_corpus(docs)
    print(f"✅ Pipeline complete: {out_path}")


if __name__ == "__main__":
    run()