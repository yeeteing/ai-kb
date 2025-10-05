# 🧠 AI-KB: Mini Reasoning Engine

Mini reasoning engine built with **FastAPI** + **PostgreSQL** that grounds LLM answers in organization-specific FAQs.  
Includes clean APIs (`/kb/faq`, `/ask`), Postgres full-text search, latency metrics, and optional **OpenAI** integration.

---

## 🚀 Features
- **Knowledge Base API** – Add FAQs per org (`POST /kb/faq`)  
- **Reasoning Engine** – Retrieve relevant FAQs with **Postgres full-text search**  
- **Ask Endpoint** – Ground LLM answers in context (`POST /ask`)  
- **Latency Metrics** – Response includes retrieval + LLM timing  
- **Extensible** – Works in demo mode (no API key) or with OpenAI  

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy  
- **Database:** PostgreSQL (full-text search via `tsvector`)  
- **LLM Integration:** OpenAI API (optional)  
- **Dev Tools:** Docker, pytest, uvicorn  

---

## 📦 Setup

### 1. Clone & install
```bash
git clone https://github.com/<your-username>/ai-kb.git
cd ai-kb
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run PostgreSQL (Docker)
```
docker run --name pg16 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=ai_kb -p 5432:5432 -d postgres:16
```

### 3. Configure environment

Create a .env file:
In your terminal, root of ai-kb project, run: `nano .env`
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_kb
LLM_PROVIDER=openai
# leave empty for demo mode
OPENAI_API_KEY=
TOP_K=4
SCORE_THRESHOLD=0.15
```

### 4. Run API
``` uvicorn app.main:app --reload ```

Docs available at 👉 `http://127.0.0.1:8000/docs`

## 🧪 Demo
Add FAQs
```
curl -X POST http://127.0.0.1:8000/kb/faq -H "Content-Type: application/json" \
  -d '{"org_id":"demo","question":"How do I reset my password?","answer":"Go to Settings → Security → Reset Password."}'
```
```
curl -X POST http://127.0.0.1:8000/kb/faq -H "Content-Type: application/json" \
  -d '{"org_id":"demo","question":"What is your refund policy?","answer":"Refunds within 30 days with proof of purchase."}'
```
Ask a question
```
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" \
  -d '{"org_id":"demo","question":"How do I reset my password?"}'
```

Sample response
```
{
  "answer": "(demo) Based on the context, here’s the best answer I can provide.",
  "context": [
    {
      "source": "faq",
      "question": "How do I reset my password?",
      "text": "Go to Settings → Security → Reset Password."
    }
  ],
  "latency_ms": {"retrieve": 2, "llm": 0, "total": 2}
}
```
![ai-kb](ai-kb-demo.gif)

## ✅ Health Check
curl http://127.0.0.1:8000/health
#### {"status":"ok"}

## 🧑‍💻 Development

Run tests:
```
pytest -q
```

## 📌 Roadmap

 Add latency histograms via Prometheus

 Swap FTS for pgvector embeddings or Elasticsearch BM25

 Add API key auth + rate limiting

 Optional web UI (React/Angular chat)

 ## Endpoints

- POST /kb/faq — add FAQs

- POST /ask — retrieve relevant FAQs (Postgres full-text search) + answer via LLM (or demo text)

- GET /health — health check

---

## 📝 TODO
See [TODO.md](TODO.md) for a simple checklist to get started locally and plan production setup.