# Professor Agent — Agentic AI System  
**FastAPI Backend · Async Agent Workflows · React Frontend**

Professor Agent is a production-style **agentic AI system** that runs **asynchronous, multi-step workflows** for academic and research tasks.  
It combines a **FastAPI backend** with a **React (Vite) frontend**, and includes a **literature metadata retrieval service** powered by OpenAlex, Crossref, and arXiv.

The project is designed for **coursework, hackathons, and research demos**, while intentionally following **real-world backend and system architecture patterns**.

---

## What This Project Does

Professor Agent can:

- Run long-running **agent workflows asynchronously**
- Track **job progress step-by-step** (lesson plan, grants, collaborators, literature, proposal)
- Retrieve **real scholarly metadata** programmatically
- Expose a clean **REST API** with automatic Swagger documentation
- Surface workflow status and results through a **React dashboard**

---

## High-Level Architecture

The system is split into two clear layers:

### Backend (FastAPI)
- Manages agent workflows and background execution
- Exposes REST endpoints
- Orchestrates retrieval pipelines and job state

### Frontend (React + Vite)
- Submits agent jobs
- Polls job status
- Displays intermediate and final results

The backend follows a **layered architecture**:

- **api** → HTTP endpoints (public interface)  
- **services** → business logic & agent workflows  
- **models** → Pydantic schemas  
- **infra** → infrastructure (job store, background execution)  
- **core** → configuration, logging, CORS  

This separation keeps the system **maintainable, testable, and easy to extend** (e.g., replacing in-memory jobs with Redis).

---

## Repository Structure

```text
.
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI entry point
│       ├── api/
│       │   ├── router.py
│       │   └── endpoints/
│       │       ├── agentic_async.py
│       │       ├── literature.py
│       │       └── retrieval.py
│       ├── core/
│       │   ├── config.py
│       │   ├── cors.py
│       │   └── logging.py
│       ├── infra/
│       │   └── job_store.py
│       ├── models/
│       │   ├── agentic.py
│       │   └── literature.py
│       ├── pipelines/
│       │   ├── build_corpus.py
│       │   ├── ingest.py
│       │   ├── preprocess.py
│       │   └── run_pipeline.py
│       └── services/
│           ├── agentic_service.py
│           ├── literature_service.py
│           ├── literature_sources.py
│           └── retrieval_service.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api/
│       │   └── agentApi.js
│       ├── components/
│       │   ├── ContextResults.jsx
│       │   ├── JobForm.jsx
│       │   ├── JobStatus.jsx
│       │   └── StepList.jsx
│       ├── hooks/
│       │   └── useAgentJob.js
│       ├── pages/
│       │   └── AgentDashboard.jsx
│       └── styles/
│           └── main.css
│
├── scripts/
│   └── clean_hackathon_data.py
│
├── data/                    # local only (not committed)
├── .env                     # local only (not committed)
├── .gitignore
├── requirements.txt
└── README.md

4. Data

The data/ directory is intentionally excluded from version control because it may contain sensitive or proprietary datasets.

Expected local layout (example):
data/
├── faculty_profiles_raw/
├── faculty_profiles_clean/
├── grants_raw/
└── grants_clean/

For local development, place raw and cleaned datasets under data/.
See data/README.md for additional guidance.
Synthetic or sample data may be used if the original datasets are unavailable.

5. Requirements

Python 3.10+ (recommended: 3.11)

Internet connection (for literature APIs)

Windows / macOS / Linux

6. Dependencies
fastapi>=0.110
uvicorn[standard]>=0.24
pydantic>=2.6
python-dotenv>=1.0
requests>=2.31

7. Setup Instructions
7.1 Create and Activate Virtual Environment

Windows (PowerShell):

cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1

macOS / Linux:

cd backend
python3 -m venv .venv
source .venv/bin/activate

7.2 Install Dependencies
pip install -r requirements.txt

7.3 Create Environment Variables

This application uses environment variables for configuration.
Note: Literature APIs do not require API keys.

8. Running the Application
From the backend/ directory:
uvicorn app.main:app --reload

9. Testing in the Browser
Health Check
http://127.0.0.1:8000/health

Expected:
{ "status": "ok" }

Ping
http://127.0.0.1:8000/api/ping

Expected:
{ "message": "pong" }

Swagger API Docs
http://127.0.0.1:8000/docs

10. Key API Endpoints
10.1 Start Agent Workflow (Async)

POST /api/agentic_workflow_async

Example request body:

{
  "goal": "Hospital readmission prediction using ML",
  "project_idea": "Predict 30-day readmission using structured EHR data",
  "profile_text": "MS Data Analytics student focusing on ML systems"
}

10.2 Poll Job Status
GET /api/agentic_workflow_status/{job_id}

10.3 Literature Review
GET /api/literature_review?query=your+topic

11. Notes on Design Choices

Jobs run using background threads (simple and effective for demos)

Job state is stored in memory (easy to replace with Redis/DB later)

External APIs are accessed via requests

Pydantic enforces strict request/response schemas

12. Common Issues

Import Errors
Ensure filenames match imports exactly (e.g. agentic_async.py).

.env Not Loading

.env is in backend/

python-dotenv is installed

Environment variables are passed correctly in Docker (if containerized)

13. License

Educational / academic use.

