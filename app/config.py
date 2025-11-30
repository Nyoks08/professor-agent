import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

# Load .env file
load_dotenv()

@dataclass
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    llm_model: str = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-32B-Instruct")

    app_name: str = "Professor Agent Backend"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    print("DEBUG: Loaded API KEY =", s.openai_api_key)  # TEMPORARY debug print
    return s
