import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.db.models import Candidate

router = APIRouter(prefix="/api/gaps", tags=["Gaps"])

@router.get("/{candidate_id}")
async def get_skill_gaps(candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Returns skill gap analysis for a specific candidate.
    """
    try:
        # Fetch candidate
        result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
        candidate = result.scalar_one_or_none()
        
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found.")

        if not candidate.skill_gaps:
            return {
                "status": "processing",
                "message": "Skill gap analysis is in progress.",
                "data": None,
                "model_used": "RandomForest-GapAnalyzer",
                "confidence": 0.0
            }

        return {
            "status": "success",
            "data": candidate.skill_gaps,
            "model_used": "RandomForest-GapAnalyzer",
            "confidence": 0.92
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
