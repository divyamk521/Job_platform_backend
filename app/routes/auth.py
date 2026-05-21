from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.services.auth_service import create_user, login_user
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])

limiter = Limiter(key_func=get_remote_address)


# ------------------------
# Register
# ------------------------
@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


# ------------------------
# Login (Rate Limited)
# ------------------------
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data.username, form_data.password)


# ------------------------
# Current user
# ------------------------
@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user