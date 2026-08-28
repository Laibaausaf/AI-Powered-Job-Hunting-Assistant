"""
Entry point. Run with: uvicorn app.main:app --reload
Interactive API docs (great for your teammate + judges) at /docs once running.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, jobs, profile, applications, interview, dashboard, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Job Hunting Assistant API",
    description="Backend for HackHorizon Problem Statement 1",
    version="0.1.0",
)

# Allow the React/Vue frontend (running on a different port) to call this API.
# Tighten allow_origins to your deployed frontend URL before submission.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(profile.router)
app.include_router(applications.router)
app.include_router(interview.router)
app.include_router(dashboard.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "AI Job Hunting Assistant API. See /docs for endpoints."}


@app.get("/health")
def health():
    return {"status": "healthy"}
