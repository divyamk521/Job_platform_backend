from fastapi import FastAPI
from app.core.database import engine
from app.models.base import Base
from app.models import User, Job

from app.routes import  auth,jobs,interests

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def health():
    return {"status": "running"}


# app.include_router(root.router)
# # app.include_router(docs.router)
# app.include_router(post.router)
app.include_router(interests.router)
app.include_router(auth.router)
app.include_router(jobs.router)