from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.jobs import JobCreate, JobResponse
from app.utils.dependencies import get_current_recruiter, get_current_user

from app.services.job_service import (
    create_job,
    get_jobs,
    get_jobs_by_recruiter,
    get_jobs_with_counts,
    search_jobs
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# -------------------------
# Create Job
# -------------------------
@router.post("/", response_model=JobResponse)
def create_job_route(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):
    return create_job(db, job, current_user.id)


# -------------------------
# List Jobs (Pagination + Filters)
# -------------------------
@router.get("/", response_model=list[JobResponse])
def fetch_jobs(
    page: int = 1,
    limit: int = 10,
    recruiter_id: int | None = None,
    location: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_jobs(
        db,
        page=page,
        limit=limit,
        recruiter_id=recruiter_id,
        location=location
    )


# -------------------------
# Search Jobs
# -------------------------
@router.get("/search", response_model=list[JobResponse])
def search_jobs_endpoint(
    q: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return search_jobs(db, q)


# -------------------------
# Jobs By Recruiter
# -------------------------
@router.get("/recruiter/{recruiter_id}", response_model=list[JobResponse])
def jobs_by_recruiter(
    recruiter_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_jobs_by_recruiter(db, recruiter_id)


# -------------------------
# Recruiter Dashboard
# -------------------------
@router.get("/with-counts")
def jobs_with_counts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):

    data = get_jobs_with_counts(db)

    result = []

    for job, count in data:
        result.append({
            "job_id": job.id,
            "title": job.title,
            "applicants": count
        })

    return result