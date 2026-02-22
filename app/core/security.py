from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashed password
def hash_password(password: str):
    if len(password.encode('utf-8')) > 72:
        # Option A: Truncate (common practice)
        password = password[:72] 
        # Option B: Raise an actual FastAPI HTTPException 400
    return pwd_context.hash(password)

#passowrd verification
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

#creating jwt access token for login endpoint
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt