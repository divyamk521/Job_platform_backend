import os
import shutil
import uuid
from sqlalchemy.orm import Session
from app.models.application import Application

# project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "resumes")


def apply_to_job(db: Session, job_id: int, user_id: int, file):

    # ensure directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{user_id}_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    print("Saving resume to:", file_path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    application = Application(
        job_id=job_id,
        user_id=user_id,
        resume_path=f"/resumes/{filename}"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application