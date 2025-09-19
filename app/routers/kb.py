# Exposes endpoints to add FAQs.
# Uses a short-lived DB session per request via Depends(get_db).

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import FAQ
from app.schemas import FAQIn

router = APIRouter(prefix="/kb", tags=["kb"])

def get_db():
    # Yield a session, and ensure it's closed after the request finishes
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/faq")
def add_faq(item: FAQIn, db: Session = Depends(get_db)):
    # Create and persist a new FAQ row
    faq = FAQ(org_id=item.org_id, question=item.question, answer=item.answer)
    db.add(faq)
    db.commit()
    db.refresh(faq)  # populate auto fields like id
    return {"id": faq.id}