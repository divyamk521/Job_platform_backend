from sqlalchemy.orm import Session
from app.models.interest import Interest
from app.models.job import Job
from app.models.user import User
from fastapi import HTTPException, status
from app.utils.logger import logger



def apply_job(db: Session, job_id: int, user_id: int):

    existing = (
        db.query(Interest)
        .filter(
            Interest.job_id == job_id,
            Interest.job_seeker_id == user_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already applied"
        )

    interest = Interest(
        job_id=job_id,
        job_seeker_id=user_id
    )

    db.add(interest)
    db.commit()
    db.refresh(interest)

    job = db.query(Job).filter(Job.id == job_id).first()
    logger.info(f"User {user_id} successfully applied to job {job_id}")

    return interest, job.google_form_link

def get_applicants_for_recruiter(db: Session, recruiter_id: int):
    return (
        db.query(Interest, User, Job)
        .join(Job, Job.id == Interest.job_id)
        .join(User, User.id == Interest.job_seeker_id)
        .filter(Job.recruiter_id == recruiter_id)
        .all()
    )

def get_applicants_for_job(db: Session, job_id: int):
    return (
        db.query(User)
        .join(Interest, Interest.job_seeker_id == User.id)
        .filter(Interest.job_id == job_id)
        .all()
    )