from pydantic import BaseModel
from datetime import datetime


class InterestResponse(BaseModel):
    id: int
    job_id: int
    job_seeker_id: int
    created_at: datetime

    class Config:
        from_attributes = True