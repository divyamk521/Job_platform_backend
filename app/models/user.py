from sqlalchemy import Column, Integer, String, DateTime, Enum,Boolean
from sqlalchemy.sql import func
from app.models.base import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    recruiter = "recruiter"
    job_seeker = "job_seeker"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())