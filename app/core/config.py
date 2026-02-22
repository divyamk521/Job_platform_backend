from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database
    database_name: str
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str

    # auth
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # optional swagger auth
    swagger_username: str
    swagger_password: str

    class Config:
        env_file = ".env"


settings = Settings()


# API metadata (nice touch for docs)
title = "Job Platform API"
description = """
Backend for Job Application Platform

Roles:
- Recruiter
- Job Seeker

Features:
- Job posting
- Interest tracking
- Google form integration
- Image upload
"""