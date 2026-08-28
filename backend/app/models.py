"""
Database tables backing all 5 modules.

- User            -> mock auth (6.1)
- Job              -> Module A seed/search data
- Application      -> Module D dashboard row (one per job a user has
                      viewed/saved/applied to), also feeds Module E analytics
- InterviewSession -> Module C mock-interview flow
- InterviewAnswer  -> one row per answered question in a session
"""
import datetime as dt

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    resume_text = Column(Text, nullable=True)   # last parsed resume, cached
    skills = Column(JSON, nullable=True)         # extracted skill list, cached
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    applications = relationship("Application", back_populates="user")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    remote = Column(String, default="no")        # "yes" / "no" / "hybrid"
    role_level = Column(String, default="mid")    # intern/entry/mid/senior
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    skills = Column(JSON, nullable=True)          # list[str] parsed from description
    posted_date = Column(DateTime, default=dt.datetime.utcnow)
    source = Column(String, default="seed")       # "seed" or API name, per 6.3 disclosure


class Application(Base):
    """One row per job a user is tracking (Module D)."""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    status = Column(String, default="Saved")  # Saved/Applied/Interviewing/Offer/Rejected
    follow_up_date = Column(DateTime, nullable=True)

    cover_letter = Column(Text, nullable=True)
    match_score = Column(Float, nullable=True)
    skill_gaps = Column(JSON, nullable=True)

    status_history = Column(JSON, default=list)  # [{status, changed_at}] for response-time metrics
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    user = relationship("User", back_populates="applications")
    job = relationship("Job")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    questions = Column(JSON, nullable=False)   # list of {category, question, answer_outline}
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    answers = relationship("InterviewAnswer", back_populates="session")


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_index = Column(Integer, nullable=False)
    answer_text = Column(Text, nullable=False)
    feedback = Column(JSON, nullable=True)  # {clarity, structure, relevance, notes}
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    session = relationship("InterviewSession", back_populates="answers")
