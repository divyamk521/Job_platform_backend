from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.dependencies import get_current_recruiter
from app.services.job_service import get_recruiter_jobs
from app.schemas.jobs import JobResponse
from app.services.interest_service import get_applicants_for_job
from app.schemas.user import UserResponse
from app.services.job_service import recruiter_dashboard


router = APIRouter(prefix="/recruiter", tags=["Recruiter"])


@router.get("/jobs", response_model=list[JobResponse])
def recruiter_jobs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):
    return get_recruiter_jobs(db, current_user.id)

@router.get("/dashboard")
def recruiter_dashboard_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):
    return recruiter_dashboard(db, current_user.id)

@router.get("/jobs/{job_id}/applicants", response_model=list[UserResponse])
def job_applicants(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):
    return get_applicants_for_job(db, job_id)