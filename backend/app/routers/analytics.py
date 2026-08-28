"""
Module E - Insights & Analytics. Every metric is recomputed on each request
directly from the applications table, so it always reflects the latest
tracked data (the acceptance bar requires recompute-on-change, and querying
live rather than caching gets that for free).
"""
import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("", response_model=schemas.AnalyticsOut)
def get_analytics(
    role_for_benchmark: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    apps = db.query(models.Application).filter(models.Application.user_id == current_user.id).all()

    total = len(apps)
    applied_or_further = [a for a in apps if a.status in ("Applied", "Interviewing", "Offer", "Rejected")]
    responded = [a for a in apps if a.status in ("Interviewing", "Offer", "Rejected")]

    response_rate = round(100 * len(responded) / len(applied_or_further), 1) if applied_or_further else 0.0

    # avg time-to-response: time between "Applied" and the next status change, from status_history
    response_times = []
    for a in apps:
        history = a.status_history or []
        applied_at = next((h["changed_at"] for h in history if h["status"] == "Applied"), None)
        next_after_applied = None
        if applied_at:
            found_applied = False
            for h in history:
                if found_applied and h["status"] != "Applied":
                    next_after_applied = h["changed_at"]
                    break
                if h["status"] == "Applied":
                    found_applied = True
            if next_after_applied:
                d1 = dt.datetime.fromisoformat(applied_at)
                d2 = dt.datetime.fromisoformat(next_after_applied)
                response_times.append((d2 - d1).total_seconds() / 86400)

    avg_response_days = round(sum(response_times) / len(response_times), 1) if response_times else None

    status_breakdown = {}
    for a in apps:
        status_breakdown[a.status] = status_breakdown.get(a.status, 0) + 1

    salary_benchmark = None
    if role_for_benchmark:
        jobs = db.query(models.Job).filter(models.Job.title.ilike(f"%{role_for_benchmark}%")).all()
        if jobs:
            mins = [j.salary_min for j in jobs if j.salary_min]
            maxs = [j.salary_max for j in jobs if j.salary_max]
            salary_benchmark = {
                "role": role_for_benchmark,
                "sample_size": len(jobs),
                "avg_min": round(sum(mins) / len(mins)) if mins else None,
                "avg_max": round(sum(maxs) / len(maxs)) if maxs else None,
                "source": "seed dataset (sample/mock data, not live market data)",
            }

    return schemas.AnalyticsOut(
        total_applications=total,
        response_rate_pct=response_rate,
        avg_time_to_response_days=avg_response_days,
        status_breakdown=status_breakdown,
        salary_benchmark=salary_benchmark,
    )
