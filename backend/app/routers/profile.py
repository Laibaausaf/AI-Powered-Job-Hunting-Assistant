from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, auth
from app.services import resume_parser, matching, llm_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Parse an uploaded resume (PDF/DOCX/TXT), cache its text + extracted
    skills on the user record. Every other module reads from here instead of
    re-parsing, so the resume only needs to be uploaded once per session."""
    text = await resume_parser.extract_text(file)

    known_skills = set()
    for (job_skills,) in db.query(models.Job.skills).all():
        if job_skills:
            known_skills.update(job_skills)

    skills = matching.extract_skills_from_text(text, sorted(known_skills))

    current_user.resume_text = text
    current_user.skills = skills
    db.commit()

    return {"resume_length_chars": len(text), "extracted_skills": skills}


@router.get("/autofill")
def get_autofill_fields(
    current_user: models.User = Depends(auth.get_current_user),
):
    """Module B: auto-populate a demo application form from the parsed resume."""
    from fastapi import HTTPException
    if not current_user.resume_text:
        raise HTTPException(400, "Upload a resume first via POST /profile/resume")

    fields = llm_service.extract_autofill_fields(current_user.resume_text)
    fields.setdefault("email", current_user.email)
    return fields
