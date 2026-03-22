import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.db.models import Candidate

router = APIRouter(prefix="/api/interview", tags=["Interview"])

@router.get("/{candidate_id}")
async def get_interview_questions(candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Returns AI-generated interview questions for a candidate.
    """
    try:
        result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
        candidate = result.scalar_one_or_none()
        
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found.")

        if not candidate.interview_questions:
            return {
                "status": "processing",
                "message": "Questions are being generated...",
                "data": [],
                "model_used": "HF-flan-t5/Claude",
                "confidence": 0.0
            }

        return {
            "status": "success",
            "data": candidate.interview_questions,
            "model_used": "HF-flan-t5/Claude",
            "confidence": 0.89
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
