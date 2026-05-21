Job Recruitment Platform Backend

A scalable and production-ready backend system for a Job Recruitment Platform built using FastAPI, PostgreSQL, SQLAlchemy, Redis, Docker, and Alembic, implementing secure authentication, role-based access control, resume management, recruiter dashboards, and optimized job search APIs.

🚀 Features
JWT Authentication & Authorization
Role-Based Access Control (Admin / Recruiter / Job Seeker)
Job Posting & Management APIs
Job Search with Pagination & Filtering
Resume Upload & Download APIs
Recruiter Dashboard & Applicant Tracking
Admin Analytics Dashboard
API Rate Limiting using SlowAPI
Redis Caching for Optimized Search
Dockerized FastAPI + PostgreSQL Setup
Alembic Database Migrations
Modular Service-Layer Architecture
🛠 Tech Stack
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
Redis
DevOps & Tools
Docker
Docker Compose
Alembic
Uvicorn
Security
JWT Authentication
RBAC (Role-Based Access Control)
API Rate Limiting
📁 Project Structure
job_platform_backend/
│
├── app/
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   └── main.py
│
├── alembic/
├── uploads/
├── logs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
🔐 Authentication & Roles

The platform supports three user roles:

Role	Permissions
Admin	Manage users, analytics dashboard
Recruiter	Post jobs, view applicants
Job Seeker	Apply for jobs, upload resumes

Authentication is implemented using JWT Tokens.

📌 Core APIs
Authentication
POST /auth/register
POST /auth/login
GET  /auth/me
Jobs
POST /jobs
GET  /jobs
GET  /jobs/search
Applications
POST /applications/{job_id}
GET  /applications/job/{job_id}
Admin
GET /admin/dashboard
Recruiter
GET /recruiter/dashboard
GET /recruiter/jobs
⚡ Redis Caching

Integrated Redis caching for job search optimization to improve API response time and reduce repeated database queries.

Example:

GET /jobs/search?q=python
📄 Resume Management
Secure resume upload system
Resume retrieval APIs
File storage handling with unique filenames
Recruiter access to uploaded resumes
🐳 Docker Setup
Build & Run Containers
docker compose up --build
Stop Containers
docker compose down
🗄 Database Migrations
Create Migration
alembic revision --autogenerate -m "message"
Apply Migration
alembic upgrade head
🔒 Security Features
JWT Authentication
RBAC Authorization
API Rate Limiting
Secure File Upload Handling
Password Hashing
📈 Scalability Features
Service-layer architecture
Pagination & Filtering
Redis caching
Dockerized deployment
Modular code structure
▶️ Run Locally
Clone Repository
git clone <repository-url>
cd job_platform_backend
Create Virtual Environment
python -m venv env
Activate Environment
Windows
env\Scripts\activate
Linux/Mac
source env/bin/activate
Install Dependencies
pip install -r requirements.txt
Run Server
uvicorn app.main:app --reload
📚 API Documentation

Swagger UI:

http://127.0.0.1:8000/docs
🎯 Future Improvements
Background Tasks for Resume Processing
Email Notifications
AI-Based Resume Matching
Elasticsearch Integration
CI/CD Pipeline
Cloud Deployment (AWS/GCP)

👩‍💻 Author

Divya M K
Backend Developer | FastAPI | PostgreSQL | Docker | Python