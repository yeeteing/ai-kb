# Defines our single table for the MVP: FAQs.
# Each FAQ belongs to an org (multi-tenant-friendly), and has question/answer text.

from sqlalchemy import Column, Integer, Text, String
from app.db.session import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)     # PK
    org_id = Column(String(64), index=True, nullable=False) # which org this FAQ belongs to
    question = Column(Text, nullable=False)                 # FAQ question
    answer = Column(Text, nullable=False)                   # FAQ answer

