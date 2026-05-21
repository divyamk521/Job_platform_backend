from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime
from app.models.user import UserRole





class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
        

    model_config = ConfigDict(use_enum_values=True)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserAdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True