from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.utils.dependencies import get_current_admin
from fastapi import Query
from app.schemas.user import UserAdminResponse
from sqlalchemy import func
from app.models.user import UserRole
from app.utils.dependencies import get_current_admin
from app.services.admin_services import admin_analytics

router = APIRouter(prefix="/admin", tags=["Admin"])





@router.get("/analytics")
def analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    return admin_analytics(db)

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_deleted = True

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}

@router.patch("/users/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()

    return {"message": "User blocked"}

@router.patch("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()

    return {"message": "User unblocked"}

@router.get("/users/count")
def user_count(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):

    total = db.query(func.count(User.id)).filter(
        User.created_at >= start_date,
        User.created_at <= end_date
    ).scalar()

    recruiter_count = db.query(func.count(User.id)).filter(
        User.created_at >= start_date,
        User.created_at <= end_date,
        User.role == UserRole.recruiter
    ).scalar()

    job_seeker_count = db.query(func.count(User.id)).filter(
        User.created_at >= start_date,
        User.created_at <= end_date,
        User.role == UserRole.job_seeker
    ).scalar()

    return {
        "total_users": total,
        "recruiters": recruiter_count,
        "job_seekers": job_seeker_count
    }

@router.get("/users", response_model=list[UserAdminResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    users = (
        db.query(User)
        .filter(User.is_deleted == False)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return users