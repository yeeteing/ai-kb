# The "reasoning engine" endpoint:
# 1) retrieve relevant FAQs via Postgres FTS
# 2) filter out low-scoring hits
# 3) send the good hits' text to the LLM (or demo mode)
# 4) return the answer + the supporting context + latency breakdown

from time import perf_counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas import AskIn, AskOut
from app.services.retriever import search_faqs
from app.services.llm import answer_with_llm
from app.config import settings

router = APIRouter(tags=["ask"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ask", response_model=AskOut)
async def ask(payload: AskIn, db: Session = Depends(get_db)):
    # Measure retrieval latency
    t0 = perf_counter()
    hits = search_faqs(db, payload.org_id, payload.question, k=settings.TOP_K)
    t1 = perf_counter()

    # Keep only hits above the relevance threshold
    good = [h for h in hits if h["score"] >= settings.SCORE_THRESHOLD]

    # If nothing is relevant, explicitly say "I don't know" (safer than guessing)
    if not good:
        dur = round((t1 - t0) * 1000)
        return {"answer": "I don't know.", "context": [], "latency_ms": {"retrieve": dur, "llm": 0, "total": dur}}

    # Build context for the LLM from the answers of the best hits
    ctx = [h["text"] for h in good]

    # Measure LLM latency
    t2 = perf_counter()
    ans = await answer_with_llm(ctx, payload.question)
    t3 = perf_counter()

    # Return the final structured response
    return {
        "answer": ans,
        "context": [{"source": h["source"], "question": h["question"], "text": h["text"]} for h in good],
        "latency_ms": {
            "retrieve": round((t1 - t0) * 1000),
            "llm": round((t3 - t2) * 1000),
            "total": round((t3 - t0) * 1000)
        }
    }
