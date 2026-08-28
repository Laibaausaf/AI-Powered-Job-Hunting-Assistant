"""
Module D - Job Search Management Dashboard. All writes persist in SQLite,
so status survives refresh/re-login (the acceptance bar in the spec) simply
because it's a real database, not client-side state.
"""
import datetime as dt
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

VALID_STATUSES = ["Saved", "Applied", "Interviewing", "Offer", "Rejected", "Closed"]


@router.post("/applications", response_model=schemas.ApplicationOut)
def add_or_update_application(
    payload: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Save/view a job onto the dashboard (e.g. clicked from search results)."""
    job = db.query(models.Job).filter(models.Job.id == payload.job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")

    app_row = db.query(models.Application).filter(
        models.Application.user_id == current_user.id,
        models.Application.job_id == payload.job_id,
    ).first()

    if not app_row:
        app_row = models.Application(
            user_id=current_user.id, job_id=payload.job_id, status=payload.status,
            status_history=[{"status": payload.status, "changed_at": dt.datetime.utcnow().isoformat()}],
        )
        db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return app_row


@router.get("/applications", response_model=List[schemas.ApplicationOut])
def list_applications(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    q = db.query(models.Application).filter(models.Application.user_id == current_user.id)
    if status:
        q = q.filter(models.Application.status == status)
    return q.order_by(models.Application.updated_at.desc()).all()


@router.get("/applications/upcoming", response_model=List[schemas.ApplicationOut])
def upcoming_followups(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Follow-up dates and deadlines, soonest first."""
    return (
        db.query(models.Application)
        .filter(
            models.Application.user_id == current_user.id,
            models.Application.follow_up_date.isnot(None),
        )
        .order_by(models.Application.follow_up_date.asc())
        .all()
    )


@router.patch("/applications/{application_id}", response_model=schemas.ApplicationOut)
def update_status(
    application_id: int,
    payload: schemas.ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    app_row = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == current_user.id,
    ).first()
    if not app_row:
        raise HTTPException(404, "Application not found")
    if payload.status not in VALID_STATUSES:
        raise HTTPException(400, f"status must be one of {VALID_STATUSES}")

    app_row.status = payload.status
    if payload.follow_up_date is not None:
        app_row.follow_up_date = payload.follow_up_date

    history = app_row.status_history or []
    history.append({"status": payload.status, "changed_at": dt.datetime.utcnow().isoformat()})
    app_row.status_history = history

    db.commit()
    db.refresh(app_row)
    return app_row


@router.get("/summary")
def status_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Counts per status - powers the funnel/bar chart in the spec."""
    rows = db.query(models.Application).filter(models.Application.user_id == current_user.id).all()
    counts = {s: 0 for s in VALID_STATUSES}
    for r in rows:
        counts[r.status] = counts.get(r.status, 0) + 1
    return counts
