from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.jobs import JobCreate
from app.models.interest import Interest
from sqlalchemy import func
from app.utils.logger import logger
from sqlalchemy import or_



def create_job(db: Session, job_data: JobCreate, recruiter_id: int):
    job = Job(
        title=job_data.title,
        description=job_data.description,
        google_form_link=job_data.google_form_link,
        recruiter_id=recruiter_id
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    logger.info(f"Recruiter {recruiter_id} created job {job.id}")
    return job

def get_jobs(
    db: Session,
    page: int = 1,
    limit: int = 10,
    recruiter_id: int | None = None,
    location: str | None = None
):

    query = db.query(Job)

    # recruiter filter
    if recruiter_id:
        query = query.filter(Job.recruiter_id == recruiter_id)

    # location filter
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    # pagination
    jobs = query.offset((page - 1) * limit).limit(limit).all()

    return jobs

def get_jobs_by_recruiter(db: Session, recruiter_id: int):
    return db.query(Job).filter(Job.recruiter_id == recruiter_id).all()

def get_jobs_with_counts(db: Session):
    return (
        db.query(Job, func.count(Interest.id).label("applicants"))
        .outerjoin(Interest, Interest.job_id == Job.id)
        .group_by(Job.id)
        .all()
    )

def search_jobs(db: Session, query: str):

    jobs = db.query(Job).filter(
        or_(
            Job.title.ilike(f"%{query}%"),
            Job.description.ilike(f"%{query}%")
        )
    ).all()

    return jobs

def get_recruiter_jobs(db: Session, recruiter_id: int):
    return db.query(Job).filter(Job.recruiter_id == recruiter_id).all()

def recruiter_dashboard(db: Session, recruiter_id: int):

    total_jobs = db.query(Job).filter(Job.recruiter_id == recruiter_id).count()

    total_applications = (
        db.query(func.count(Interest.id))
        .join(Job, Job.id == Interest.job_id)
        .filter(Job.recruiter_id == recruiter_id)
        .scalar()
    )

    return {
        "total_jobs": total_jobs,
        "total_applications": total_applications
    }