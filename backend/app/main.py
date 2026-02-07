from fastapi import FastAPI
from dotenv import load_dotenv

from app.core.cors import setup_cors
from app.core.logging import setup_logging
from app.api.router import api_router

def create_app() -> FastAPI:
    # Load env vars from backend/.env
    load_dotenv()

    setup_logging()

    app = FastAPI(title="Agentic AI (Professor Agent)", version="0.1.0")

    setup_cors(app)

    # Mount all API routes under /api
    app.include_router(api_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()
