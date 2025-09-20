# Provides a function to search FAQs for a given org and query.
# Uses Postgres Full-Text Search (FTS) with to_tsvector/plainto_tsquery and ts_rank scoring.

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.config import settings

def search_faqs(db: Session, org_id: str, query: str, k: int | None = None):
    k = k or settings.TOP_K

    # SQL text query because FTS functions are easiest to express directly in SQL.
    # - to_tsvector builds a searchable document from question+answer
    # - plainto_tsquery turns the user query into a search vector
    # - ts_rank produces a relevance score we can sort by
    sql = text("""
      SELECT id, question, answer,
             ts_rank(to_tsvector('english', question || ' ' || answer),
                     plainto_tsquery(:q)) AS score
      FROM faqs
      WHERE org_id = :org
        AND to_tsvector('english', question || ' ' || answer) @@ plainto_tsquery(:q)
      ORDER BY score DESC
      LIMIT :k
    """)

    rows = db.execute(sql, {"q": query, "org": org_id, "k": k}).mappings().all()

    # Normalize the results into a simple list of dicts
    return [{
        "source": "faq",
        "question": r["question"],
        "text": r["answer"],
        "score": float(r["score"] or 0.0)
    } for r in rows]
