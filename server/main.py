# Bootstraps the FastAPI app, creates tables on startup, mounts routers, and adds a health check.

from fastapi import FastAPI
import os

environment = os.environ.get('APP_ENV', 'development')

if environment == 'production':
    print("Running in production mode")
    from config_prod import *
else:
    print("Running in dev mode")
    from config_dev import *
    
app = FastAPI(title="AI KB (Postgres)")

# Simple health endpoint for quick checks / readiness probes
@app.get("/health")
def health():
    return {"status": "ok"}