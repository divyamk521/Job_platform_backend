from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.jobs import JobCreate


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

    return job

def get_jobs(db: Session):
    return db.query(Job).order_by(Job.created_at.desc()).all()

def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def get_jobs_by_recruiter(db: Session, recruiter_id: int):
    return db.query(Job).filter(Job.recruiter_id == recruiter_id).all()