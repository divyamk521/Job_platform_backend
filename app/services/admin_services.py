from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User, UserRole
from app.models.job import Job
from app.models.interest import Interest


def admin_analytics(db: Session):

    total_users = db.query(User).count()

    total_recruiters = (
        db.query(User)
        .filter(User.role == UserRole.recruiter)
        .count()
    )

    total_job_seekers = (
        db.query(User)
        .filter(User.role == UserRole.job_seeker)
        .count()
    )

    total_jobs = db.query(Job).count()

    total_applications = db.query(Interest).count()

    return {
        "total_users": total_users,
        "total_recruiters": total_recruiters,
        "total_job_seekers": total_job_seekers,
        "total_jobs": total_jobs,
        "total_applications": total_applications
    }