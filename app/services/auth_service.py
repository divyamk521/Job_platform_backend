from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password,create_access_token
from fastapi import HTTPException,Depends
from app.core.database import get_db


def create_user(db: Session, user_data: UserCreate):
    hashed = hash_password(user_data.password)

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed,
        role=user_data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}