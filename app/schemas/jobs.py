from pydantic import BaseModel
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str
    google_form_link: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: str | None
    google_form_link: str | None
    recruiter_id: int
    created_at: datetime

    class Config:
        from_attributes = True