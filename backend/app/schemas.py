"""
Pydantic models = the contract between backend and frontend. Your teammate
should build the frontend forms/tables directly against these shapes.
"""
import datetime as dt
from typing import Optional, List

from pydantic import BaseModel, EmailStr


# ---------- Auth ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]

    class Config:
        from_attributes = True


# ---------- Module A: Jobs ----------
class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    remote: str
    role_level: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: str
    skills: Optional[List[str]]
    posted_date: dt.datetime
    source: str

    class Config:
        from_attributes = True


class JobSearchResult(BaseModel):
    job: JobOut
    match_score: Optional[float] = None       # 0-100, only present if resume on file
    match_explanation: Optional[str] = None


class JobSearchFilters(BaseModel):
    query: str
    location: Optional[str] = None
    remote_only: Optional[bool] = None
    role_level: Optional[str] = None
    salary_min: Optional[int] = None
    posted_after_days: Optional[int] = None   # e.g. 30 = "posted this month"
    limit: int = 20


# ---------- Module B: Application assistance ----------
class TailorRequest(BaseModel):
    job_id: Optional[int] = None          # if job is from our DB
    job_description: Optional[str] = None  # or pasted text, if not in DB
    resume_text: Optional[str] = None      # optional override of stored resume


class TailorResponse(BaseModel):
    skill_gaps: List[str]
    resume_bullet_suggestions: List[str]
    cover_letter: str
    match_score: float


class AutoFillOut(BaseModel):
    name: Optional[str]
    email: Optional[str]
    experience_summary: Optional[str]
    skills: List[str]


# ---------- Module C: Interview prep ----------
class InterviewGenRequest(BaseModel):
    job_id: Optional[int] = None
    job_description: Optional[str] = None
    num_questions: int = 8


class InterviewQuestion(BaseModel):
    category: str   # behavioral | technical | culture_fit
    question: str
    answer_outline: List[str]


class InterviewSessionOut(BaseModel):
    id: int
    questions: List[InterviewQuestion]

    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    session_id: int
    question_index: int
    answer_text: str


class AnswerFeedback(BaseModel):
    clarity: int        # 1-5
    structure: int       # 1-5
    relevance: int        # 1-5
    notes: str


# ---------- Module D: Dashboard ----------
class ApplicationCreate(BaseModel):
    job_id: int
    status: str = "Saved"


class ApplicationStatusUpdate(BaseModel):
    status: str
    follow_up_date: Optional[dt.datetime] = None


class ApplicationOut(BaseModel):
    id: int
    job: JobOut
    status: str
    follow_up_date: Optional[dt.datetime]
    match_score: Optional[float]
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True


# ---------- Module E: Analytics ----------
class AnalyticsOut(BaseModel):
    total_applications: int
    response_rate_pct: float
    avg_time_to_response_days: Optional[float]
    status_breakdown: dict
    salary_benchmark: Optional[dict] = None
