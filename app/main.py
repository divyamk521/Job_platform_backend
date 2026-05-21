from fastapi import FastAPI
from app.core.database import engine
from app.models.base import Base
from app.models import User, Job
from app.routes import recruiter
from app.routes import applications
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.routes import  auth,jobs,interests,admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

app = FastAPI()

app.mount("/resumes", StaticFiles(directory="uploads/resumes"), name="resumes")

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)




@app.get("/")
def health():
    return {"status": "running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(root.router)
# # app.include_router(docs.router)
app.include_router(recruiter.router)
app.include_router(admin.router)
app.include_router(interests.router)
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)