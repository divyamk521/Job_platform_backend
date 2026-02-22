
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.interest_service import apply_job
from app.utils.dependencies import get_current_job_seeker
from app.utils.dependencies import get_current_recruiter
from app.services.interest_service import get_applicants_for_recruiter

router = APIRouter(prefix="/interests", tags=["Interests"])

@router.post("/{job_id}")
def apply(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_job_seeker)
):
    interest, form_link = apply_job(db, job_id, current_user.id)

    return {
        "message": "Application recorded",
        "google_form_link": form_link
    }

@router.get("/recruiter")
def recruiter_applicants(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):
    data = get_applicants_for_recruiter(db, current_user.id)

    result = []

    for interest, user, job in data:
        result.append({
            "job_id": job.id,
            "job_title": job.title,
            "applicant_id": user.id,
            "applicant_email": user.email,
            "applied_at": interest.created_at
        })

    return result