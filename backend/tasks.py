import os
from celery import Celery
from backend.ml.parser import ResumeParser
from backend.ml.preprocessor import TextPreprocessor
from backend.ml.embedder import BERTEmbedder
from backend.ml.matcher import MatchEngine
from backend.ml.gap_analyzer import SkillGapAnalyzer
from backend.ml.interview_gen import InterviewGenerator
from backend.db.database import AsyncSessionLocal
from backend.db.models import Candidate, JobDescription
import uuid
import asyncio

# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery("smarthire_tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Initialize ML models
parser = ResumeParser()
preprocessor = TextPreprocessor()
embedder = BERTEmbedder()
matcher = MatchEngine()
gap_analyzer = SkillGapAnalyzer()
interview_gen = InterviewGenerator()

@celery_app.task(name="process_resume_task")
def process_resume_task(candidate_id: str, job_id: str):
    """
    Async task to process a newly uploaded resume: parse, embed, match, and analyze.
    """
    try:
        return asyncio.run(async_process_resume(candidate_id, job_id))
    except Exception as e:
        print(f"Error in Celery task: {e}")
        return {"status": "error", "message": str(e)}

async def async_process_resume(candidate_id: str, job_id: str):
    """
    The actual async implementation for resume processing.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch Candidate and JD
        candidate = await db.get(Candidate, uuid.UUID(candidate_id))
        job = await db.get(JobDescription, uuid.UUID(job_id))
        
        if not candidate or not job:
            return {"status": "error", "message": "ID not found"}

        # 2. Text Normalization
        cleaned_resume = preprocessor.clean_text(candidate.parsed_text)
        cleaned_jd = preprocessor.clean_text(job.text)
        
        # 3. Generate Embeddings
        resume_emb = embedder.get_embedding(cleaned_resume)
        jd_emb = embedder.get_embedding(cleaned_jd)
        
        # 4. Calculate Match Score
        score = matcher.calculate_match_score(resume_emb, jd_emb)
        
        # 5. Extract Skills and Analyze Gaps
        found_skills = preprocessor.extract_skills(candidate.parsed_text, job.required_skills)
        gaps = gap_analyzer.analyze(job.required_skills, found_skills)
        
        # 6. Generate Interview Questions
        questions = interview_gen.generate_questions(job.text, candidate.parsed_text, gaps['missing_skills'])
        
        # 7. Update Database
        candidate.embedding = resume_emb
        candidate.match_score = score
        candidate.skill_gaps = gaps
        candidate.interview_questions = questions
        
        await db.commit()
        
        return {
            "status": "success",
            "candidate_id": candidate_id,
            "match_score": score,
            "skills_found": found_skills,
            "model_used": "all-MiniLM-L6-v2",
            "confidence": round(score/100, 2)
        }
