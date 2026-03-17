from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
import os
import logging

from ccpa_guardian.main import CCPAGuardian
from ccpa_guardian.config import STATIC_DIR, HOST, PORT

logger = logging.getLogger("CCPA-API")

# Global instance
guardian = CCPAGuardian()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 CCPA Guardian: Initializing AI Brain and Legal Index...")
    guardian.startup()
    logger.info("✅ System Ready!")
    yield

app = FastAPI(title="CCPA Guardian API", lifespan=lifespan)

# Mount frontend
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def read_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to CCPA Guardian. Frontend not found at /static/index.html"}

class AnalyzeRequest(BaseModel):
    prompt: str

class AnalyzeResponse(BaseModel):
    harmful: bool
    articles: List[str]
    reasoning: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_practice(request: AnalyzeRequest):
    try:
        result = guardian.run_query(request.prompt)
        return AnalyzeResponse(
            harmful=result['harmful'],
            articles=result['articles'],
            reasoning=result['reasoning']
        )
    except Exception as e:
        logger.error(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def run_api():
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)

if __name__ == "__main__":
    run_api()
