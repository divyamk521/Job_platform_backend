from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from app.models.base import Base


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))
    job_seeker_id = Column(Integer, ForeignKey("users.id"))
    resume_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())