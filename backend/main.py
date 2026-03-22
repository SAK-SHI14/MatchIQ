"""
SmartHire AI - FastAPI Application Entry Point.
Runs ML inference in-process (no Celery needed for local dev).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.db.database import engine, Base
from backend.routes import upload, match, gaps, interview, jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Creates all DB tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅  SmartHire AI ready. DB tables created.")
    yield


app = FastAPI(
    title="SmartHire AI API",
    description="Resume × Job Intelligence System — BERT matching, skill gap analysis, RAG interview questions.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route groups
app.include_router(jobs.router)
app.include_router(upload.router)
app.include_router(match.router)
app.include_router(gaps.router)
app.include_router(interview.router)


@app.get("/", tags=["Health"])
async def health_check():
    """Basic liveness probe."""
    return {
        "status": "healthy",
        "app": "SmartHire AI",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
