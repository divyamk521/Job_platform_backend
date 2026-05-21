from pydantic import BaseModel
from datetime import datetime


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    resume_path: str
    created_at: datetime

    class Config:
        from_attributes = True