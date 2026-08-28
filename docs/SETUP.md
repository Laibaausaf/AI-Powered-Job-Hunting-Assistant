# Backend Local Setup Guide

## 1. Requirements

Install the following before starting:

### Python

Recommended:

Python 3.11 or Python 3.12

Verify:

python --version

---

### Git

Verify:

git --version

---

### VS Code

Recommended editor:

Visual Studio Code

Recommended extensions:

- Python
- Pylance
- GitLens (optional)
- REST Client (optional)

---

# 2. Clone the Repository

Open terminal:

git clone https://github.com/Laibaausaf/AI-Powered-Job-Hunting-Assistant.git

Enter project:

cd AI-Powered-Job-Hunting-Assistant

---

# 3. Enter Backend

cd backend

---

# 4. Create Python Virtual Environment

Windows:

python -m venv .venv

This creates an isolated Python environment for the backend.

---

# 5. Activate Environment

## Windows PowerShell

.venv\Scripts\Activate.ps1

If PowerShell blocks the activation script, do not modify system settings blindly.

You can use Git Bash instead.

---

## Windows Git Bash

source .venv/Scripts/activate

After activation the terminal should show:

(.venv)

---

# 6. Install Dependencies

Run:

pip install -r requirements.txt

The requirements include:

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Pydantic Settings
- python-jose
- passlib/bcrypt
- python-multipart
- Anthropic SDK
- pypdf
- python-docx
- python-dotenv

---

# 7. Configure Environment

Inside:

backend/

copy:

.env.example

to:

.env

The final structure should be:

backend/
├── .env
├── .env.example
├── app/
└── requirements.txt

---

# 8. Environment Variables

The `.env` file requires:

ANTHROPIC_API_KEY=

CLAUDE_MODEL=claude-3-5-haiku-20241022

JWT_SECRET=

JWT_ALGORITHM=HS256

JWT_EXPIRE_MINUTES=1440

DATABASE_URL=sqlite:///./jobhunt.db

---

# 9. API Key Security

Never commit `.env`.

Never put the real Anthropic key inside:

.env.example

Never paste API keys into Python source files.

Never send API keys to the frontend.

If a key is accidentally committed, revoke it immediately.

---

# 10. Database Initialization

The backend automatically creates the database tables when the FastAPI application starts.

However, the job dataset must be seeded separately.

---

# 11. Seed Job Data

From:

backend/

run:

python -m app.seed_data

Expected result:

Seeded 250 jobs.

If the database already contains at least 200 jobs, the seed script will skip creating another dataset.

---

# 12. Start Backend

Run:

uvicorn app.main:app --reload

Expected server:

http://127.0.0.1:8000

or:

http://localhost:8000

---

# 13. Verify Backend

Open:

http://localhost:8000/

Expected:

{
  "status": "ok",
  "message": "AI Job Hunting Assistant API. See /docs for endpoints."
}

---

# 14. Health Check

Open:

http://localhost:8000/health

Expected:

{
  "status": "healthy"
}

---

# 15. Swagger UI

Open:

http://localhost:8000/docs

Swagger provides an interactive interface for testing the backend endpoints.

---

# 16. First Test Flow

Recommended order:

1. Register user
2. Login
3. Copy JWT access token
4. Click Authorize
5. Enter Bearer token
6. Upload resume
7. Search jobs
8. Open job
9. Tailor application
10. Generate interview
11. Submit interview answer
12. Create/update application
13. Check dashboard
14. Check analytics

---

# 17. Important Backend Rule

Do not modify the frontend to compensate for a backend API without checking the API contract first.

Read:

docs/API.md

before integrating.

---

# 18. Common Problems

## ModuleNotFoundError

Make sure:

- backend directory is current directory
- virtual environment is activated
- dependencies are installed

Run:

pip install -r requirements.txt

---

## Anthropic API Error

Check:

backend/.env

and verify:

ANTHROPIC_API_KEY=your_valid_key

Do not place the key in `.env.example`.

---

## Job Search Returns Nothing

Run:

python -m app.seed_data

Then verify that job records exist.

---

## Port Already In Use

Use:

uvicorn app.main:app --reload --port 8001

Then open:

http://localhost:8001/docs

---

# 19. Backend Entry Point

Main application:

backend/app/main.py

Run:

uvicorn app.main:app --reload

---

# 20. Configuration Source

Configuration is centralized in:

backend/app/config.py

It loads variables from:

backend/.env

using Pydantic Settings.

Do not read environment variables directly throughout the application.

---

# 21. Current Backend Limitation

The current job dataset is synthetic.

Live LinkedIn/Indeed/Rozee ingestion is not currently configured.

Do not expect live job listings when running the current MVP.

---

# 22. Development Rule

Before making changes:

1. Pull latest main.
2. Read AI_CONTEXT.md.
3. Read PROJECT_STATUS.md.
4. Read relevant documentation.
5. Inspect existing code.
6. Create a feature branch.
7. Make focused changes.
8. Test.
9. Commit.
10. Push.
11. Open a Pull Request.