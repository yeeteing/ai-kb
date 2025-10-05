# Bootstraps the FastAPI app, creates tables on startup, mounts routers, and adds a health check.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from db.session import ping

environment = os.environ.get('APP_ENV', 'development')

if environment == 'production':
    print("Running in production mode")
    from config_prod import *
else:
    print("Running in dev mode")
    from config_dev import *
    
app = FastAPI(title="AI KB (Postgres)")
  
# allow your frontend origin(s) while developing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000"],  # Flask dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Simple health endpoint for quick checks / readiness probes
@app.get("/health")
def health():
    return {"ok": True, "db": ping()}
