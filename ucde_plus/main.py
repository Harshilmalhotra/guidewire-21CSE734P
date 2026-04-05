from fastapi import FastAPI
from api.routes import router as fnol_router

app = FastAPI(title="UCDE++", description="Unified Claims Decision Engine", version="1.0.0")

app.include_router(fnol_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "UCDE++ Phase 1 Base System is running"}
