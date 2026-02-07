import os
from pydantic import BaseModel


class Settings(BaseModel):
    # Environment
    ENV: str = os.getenv("ENV", "dev")

    # LLM configuration (we’ll use later)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3")

    # Timeouts
    REQUEST_TIMEOUT_SECS: int = int(os.getenv("REQUEST_TIMEOUT_SECS", "30"))

    # Debug / behavior flags
    DEBUG: bool = ENV == "dev"


# Singleton settings object
settings = Settings()
