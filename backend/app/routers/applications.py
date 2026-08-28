"""
Module B - Application Assistance, and the write side of Module D's
tracking (an Application row is created here when a user tailors/applies,
then Module D's dashboard router reads/updates its status).
"""
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth
from app.services import matching, llm_service

router = APIRouter(prefix="/applications", tags=["applications"])


def _resolve_job_description(payload: schemas.TailorRequest, db: Session):
    """Job can come from our seeded DB (job_id) or be pasted text - either
    is acceptable per Module B's spec."""
    if payload.job_id:
        job = db.query(models.Job).filter(models.Job.id == payload.job_id).first()
        if not job:
            raise HTTPException(404, "Job not found")
        return job.title, job.company, job.description, (job.skills or [])
    if payload.job_description:
        return "this role", "the company", payload.job_description, []
    raise HTTPException(400, "Provide either job_id or job_description")


@router.post("/tailor", response_model=schemas.TailorResponse)
def tailor_application(
    payload: schemas.TailorRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    resume_text = payload.resume_text or current_user.resume_text
    if not resume_text:
        raise HTTPException(400, "No resume on file. Upload one via POST /profile/resume, or pass resume_text.")

    title, company, description, job_skills = _resolve_job_description(payload, db)

    # If job came from free-pasted text (no pre-tagged skills), extract some
    # from a general vocabulary built from resume + seeded jobs so gaps are meaningful.
    if not job_skills:
        known_skills = set(current_user.skills or [])
        for (js,) in db.query(models.Job.skills).all():
            if js:
                known_skills.update(js)
        job_skills = matching.extract_skills_from_text(description, sorted(known_skills))

    resume_skills = current_user.skills or matching.extract_skills_from_text(resume_text, job_skills)
    score, matched, missing = matching.compute_match(resume_skills, job_skills)

    ai_output = llm_service.generate_bullets_and_letter(
        resume_text=resume_text,
        job_description=description,
        matched_skills=matched,
        missing_skills=missing,
        job_title=title,
        company=company,
    )

    # If this ties to a job in our DB, upsert a tracked Application row
    # (Saved status) so it shows up on the Module D dashboard automatically.
    if payload.job_id:
        existing = db.query(models.Application).filter(
            models.Application.user_id == current_user.id,
            models.Application.job_id == payload.job_id,
        ).first()
        if not existing:
            existing = models.Application(
                user_id=current_user.id, job_id=payload.job_id, status="Saved",
                status_history=[{"status": "Saved", "changed_at": dt.datetime.utcnow().isoformat()}],
            )
            db.add(existing)
        existing.cover_letter = ai_output["cover_letter"]
        existing.match_score = score
        existing.skill_gaps = missing
        db.commit()

    return schemas.TailorResponse(
        skill_gaps=missing,
        resume_bullet_suggestions=ai_output["resume_bullet_suggestions"],
        cover_letter=ai_output["cover_letter"],
        match_score=score,
    )
