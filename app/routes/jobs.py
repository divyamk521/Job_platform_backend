from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.jobs import JobCreate, JobResponse
from app.services.job_service import create_job,get_jobs
from app.utils.dependencies import get_current_recruiter,get_current_user
from app.services.job_service import get_jobs_by_recruiter


router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobResponse)
def create_job_route(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_recruiter)
):
    return create_job(db, job, current_user.id)

@router.get("/", response_model=list[JobResponse])
def list_jobs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # both roles allowed
):
    return get_jobs(db)

from fastapi import HTTPException, status
from app.services.job_service import get_job


@router.get("/{job_id}", response_model=JobResponse)
def job_detail(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    job = get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return job

@router.get("/recruiter/{recruiter_id}", response_model=list[JobResponse])
def jobs_by_recruiter(
    recruiter_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_jobs_by_recruiter(db, recruiter_id)