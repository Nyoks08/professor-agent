# 📘 Professor Agent — AI Research & Teaching Assistant  
**An Agentic AI system that helps university professors generate lesson plans, refine research ideas, and explore relevant papers, grants, and courses.**

This project integrates:

- **Teaching Assistant Mode** → Generates structured lesson plans using real US course data  
- **Research Assistant Mode** → Suggests refined research questions, related papers, NIH-style grants, and online courses  
- **Agentic Workflow** → Uses curated datasets and LLM reasoning to produce grounded output  
- **FastAPI Backend** + **OpenRouter LLM API**  

---

## 🚀 Features

### 🔵 **Teaching Assistant**
- Generates a full JSON lesson plan
- Uses US course catalog + EdX courses for grounding
- Supports few-shot examples

### 🟣 **Research Assistant**
- Refines professor research ideas  
- Provides related papers, grants, datasets, and methodology suggestions  

---

## 🗂️ Project Structure

```
professor-agent/
│
├─ app/
│  ├─ main.py                 
│  ├─ teaching.py             
│  ├─ research.py             
│  ├─ llm_client.py           
│  ├─ config.py               
│  ├─ data_loader.py          
│  └─ prepare_us_courses.py   
│
├─ data/
│  ├─ us_courses_raw.csv
│  ├─ us_courses_clean.csv
│  ├─ openalex_sample.json
│  ├─ nih_grants_sample.json
│  ├─ edx_courses.csv
│  └─ lesson_plan_samples.json
│
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## 📦 Installation

```bash
git clone https://github.com/Nyoks08/professor-agent.git
cd professor-agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
uvicorn app.main:app --reload
```

Visit:
http://127.0.0.1:8000/docs
