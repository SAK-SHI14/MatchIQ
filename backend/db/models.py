import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Float, DateTime, JSON, Text, ForeignKey, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    required_skills: Mapped[List[str]] = mapped_column(JSON)
    embedding: Mapped[Optional[List[float]]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    candidates: Mapped[List["Candidate"]] = relationship(back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_descriptions.id"))
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    parsed_text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Optional[List[float]]] = mapped_column(JSON)
    match_score: Mapped[float] = mapped_column(Float, default=0.0)
    skill_gaps: Mapped[Optional[dict]] = mapped_column(JSON) # {missing: [..], importance: {..}}
    interview_questions: Mapped[Optional[List[str]]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    job: Mapped["JobDescription"] = relationship(back_populates="candidates")
