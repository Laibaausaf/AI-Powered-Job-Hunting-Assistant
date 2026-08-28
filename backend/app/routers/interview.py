"""
Module C - Interview Preparation. Questions are generated fresh from the
job description each call (never hardcoded), satisfying the "questions must
change when the JD changes" acceptance bar. The mock-interview flow stores a
session + per-question answers/feedback so the frontend can step through it.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth
from app.services import llm_service

router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/generate", response_model=schemas.InterviewSessionOut)
def generate_questions(
    payload: schemas.InterviewGenRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if payload.job_id:
        job = db.query(models.Job).filter(models.Job.id == payload.job_id).first()
        if not job:
            raise HTTPException(404, "Job not found")
        description = job.description
    elif payload.job_description:
        description = payload.job_description
    else:
        raise HTTPException(400, "Provide either job_id or job_description")

    questions = llm_service.generate_interview_questions(description, payload.num_questions)

    session = models.InterviewSession(
        user_id=current_user.id, job_id=payload.job_id, questions=questions,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/answer", response_model=schemas.AnswerFeedback)
def submit_answer(
    payload: schemas.AnswerSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """One call per question in the mock-interview sequence (spec requires
    >=3 in a row). Frontend loops this across the session's questions."""
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == payload.session_id,
        models.InterviewSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Interview session not found")

    if payload.question_index >= len(session.questions):
        raise HTTPException(400, "question_index out of range for this session")

    q = session.questions[payload.question_index]
    feedback = llm_service.evaluate_answer(
        question=q["question"], answer_text=payload.answer_text,
        answer_outline=q.get("answer_outline", []),
    )

    answer_row = models.InterviewAnswer(
        session_id=session.id,
        question_index=payload.question_index,
        answer_text=payload.answer_text,
        feedback=feedback,
    )
    db.add(answer_row)
    db.commit()

    return schemas.AnswerFeedback(**feedback)


@router.get("/session/{session_id}", response_model=schemas.InterviewSessionOut)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == session_id,
        models.InterviewSession.user_id == current_user.id,
    ).first()
    if not session:
        raise HTTPException(404, "Interview session not found")
    return session
