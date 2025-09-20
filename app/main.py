# Bootstraps the FastAPI app, creates tables on startup, mounts routers, and adds a health check.

from fastapi import FastAPI
from app.db.session import Base, engine
from app.db.models import FAQ
from app.routers import kb, ask

# Create all tables if they don't exist (lightweight for MVP)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI KB (Postgres)")

# Simple health endpoint for quick checks / readiness probes
@app.get("/health")
def health():
    return {"status": "ok"}

# Mount the routers (URL prefixes live in each router)
app.include_router(kb.router)
app.include_router(ask.router)
