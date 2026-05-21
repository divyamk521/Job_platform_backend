from fastapi.security import OAuth2PasswordBearer


from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.token import TokenData
from app.models.user import User,UserRole




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#tells how clients obtain tokens and swagger authorize function
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()

    if user is None:
        raise credentials_exception

    return user

def get_current_admin(current_user = Depends(get_current_user)):

    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user

def get_current_recruiter(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.recruiter:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters allowed"
        )
    return current_user

def get_current_job_seeker(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.job_seeker:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only job seekers allowed"
        )
    return current_user

def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user