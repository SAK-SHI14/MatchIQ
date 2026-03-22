"""
Upload endpoints: POST /api/upload/resume and POST /api/upload/jd.
ML inference is run in-process (no Celery required for local development).
"""
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.db.models import Candidate, JobDescription
from backend.ml.parser import ResumeParser
from backend.ml.preprocessor import TextPreprocessor
from backend.ml.embedder import BERTEmbedder
from backend.ml.matcher import MatchEngine
from backend.ml.gap_analyzer import SkillGapAnalyzer
from backend.ml.interview_gen import InterviewGenerator

router = APIRouter(prefix="/api/upload", tags=["Upload"])

# Singleton ML objects (loaded once at import time)
parser = ResumeParser()
preprocessor = TextPreprocessor()
embedder = BERTEmbedder()
matcher = MatchEngine()
gap_analyzer = SkillGapAnalyzer()
interview_gen = InterviewGenerator()

REQUIRED_SKILLS = [
    "Python", "Pandas", "Scikit-learn", "SQL",
    "Machine Learning", "Data Visualization",
    "Communication", "Problem Solving", "NumPy",
]


async def _run_ml_pipeline(candidate: Candidate, job: JobDescription, db: AsyncSession):
    """
    Runs the full ML pipeline for a candidate and persists results.
    Runs in a thread pool so it doesn't block the event loop.
    """
    def _pipeline():
        # 1. Clean text
        clean_resume = preprocessor.clean_text(candidate.parsed_text)
        clean_jd = preprocessor.clean_text(job.text)

        # 2. Embed
        resume_emb = embedder.get_embedding(clean_resume)
        jd_emb = embedder.get_embedding(clean_jd)

        # 3. Match score
        score = matcher.calculate_match_score(resume_emb, jd_emb)

        # 4. Skill gap
        found = preprocessor.extract_skills(candidate.parsed_text, job.required_skills or REQUIRED_SKILLS)
        gaps = gap_analyzer.analyze(job.required_skills or REQUIRED_SKILLS, found)

        # 5. Interview questions
        try:
            questions = interview_gen.generate_questions(
                job.text, candidate.parsed_text, gaps["missing_skills"]
            )
        except Exception as e:
            print(f"Interview gen error (non-fatal): {e}")
            questions = [
                f"Explain your experience with {s}." for s in gaps["missing_skills"][:5]
            ]

        return resume_emb, score, gaps, questions

    loop = asyncio.get_event_loop()
    resume_emb, score, gaps, questions = await loop.run_in_executor(None, _pipeline)

    candidate.embedding = resume_emb
    candidate.match_score = score
    candidate.skill_gaps = gaps
    candidate.interview_questions = questions
    await db.commit()


@router.post("/resume")
async def upload_resume(
    job_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Accepts a PDF or DOCX resume, stores the parsed text, then
    runs the full ML pipeline (embed → match → gaps → interview Qs).
    """
    try:
        contents = await file.read()
        parsed_text = parser.parse(contents, file.filename)

        if not parsed_text:
            raise HTTPException(status_code=400, detail="Could not parse file — check format.")

        # Fetch job for embedding
        job = await db.get(JobDescription, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job ID not found.")

        # Derive a readable name from the filename
        stem = file.filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()

        candidate = Candidate(
            job_id=job_id,
            name=stem,
            email=f"{stem.lower().replace(' ', '.')}@example.com",
            parsed_text=parsed_text,
            match_score=0.0,
        )
        db.add(candidate)
        await db.commit()
        await db.refresh(candidate)

        # Fire ML pipeline (non-blocking via thread pool)
        asyncio.create_task(_run_ml_pipeline(candidate, job, db))

        return {
            "status": "success",
            "data": {
                "candidate_id": str(candidate.id),
                "name": candidate.name,
                "message": "Resume uploaded — AI analysis started.",
            },
            "model_used": "all-MiniLM-L6-v2",
            "confidence": 1.0,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jd")
async def upload_jd(
    title: str = Form(...),
    text: str = Form(...),
    skills: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Accepts a job description title, text and comma-separated required skills.
    """
    try:
        req_skills = [s.strip() for s in skills.split(",") if s.strip()]
        job = JobDescription(title=title, text=text, required_skills=req_skills)
        db.add(job)
        await db.commit()
        await db.refresh(job)

        return {
            "status": "success",
            "data": {"job_id": str(job.id), "title": job.title},
            "model_used": "Manual/NLP",
            "confidence": 1.0,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
