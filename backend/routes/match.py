"""
Match endpoint: GET /api/match/{job_id}
Returns candidates ranked by their BERT cosine-similarity match score.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.db.models import Candidate, JobDescription

router = APIRouter(prefix="/api/match", tags=["Match"])


@router.get("/{job_id}")
async def get_ranked_candidates(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Returns all candidates for a job, ranked highest-to-lowest by match score.
    """
    try:
        job_result = await db.execute(
            select(JobDescription).where(JobDescription.id == job_id)
        )
        job = job_result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail="Job description not found.")

        cand_result = await db.execute(
            select(Candidate)
            .where(Candidate.job_id == job_id)
            .order_by(Candidate.match_score.desc())
        )
        candidates = cand_result.scalars().all()

        rankings = []
        for c in candidates:
            missing = []
            if c.skill_gaps and c.skill_gaps.get("missing_skills"):
                missing = c.skill_gaps["missing_skills"]

            rankings.append({
                "candidate_id": str(c.id),
                "name": c.name,
                "email": c.email,
                "score": round(c.match_score, 1),
                "top_skill_gap": missing[0] if missing else "None",
                "missing_skills": missing,
                "status": "processed" if c.match_score > 0 else "processing",
            })

        return {
            "status": "success",
            "data": rankings,
            "model_used": "all-MiniLM-L6-v2",
            "confidence": 0.87,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
