"""
Jobs listing endpoint: GET /api/jobs
Returns all job descriptions so the frontend can auto-select the first one.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.db.models import JobDescription

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("/")
async def list_jobs(db: AsyncSession = Depends(get_db)):
    """Returns all available job descriptions."""
    try:
        result = await db.execute(select(JobDescription).order_by(JobDescription.created_at.desc()))
        jobs = result.scalars().all()
        return {
            "status": "success",
            "data": [
                {"job_id": str(j.id), "title": j.title, "required_skills": j.required_skills}
                for j in jobs
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
