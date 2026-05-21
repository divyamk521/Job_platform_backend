from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.dependencies import get_current_user
from app.schemas.application import ApplicationResponse
from app.services.application_service import apply_to_job

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/{job_id}", response_model=ApplicationResponse)
def apply_job(
    job_id: int,
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return apply_to_job(db, job_id, current_user.id, resume)