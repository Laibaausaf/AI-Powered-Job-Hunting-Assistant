# AI CONTEXT — AI-Powered Job Hunting Assistant

## 1. PROJECT IDENTITY

Project Name:
AI-Powered Job Hunting Assistant

Repository:
AI-Powered-Job-Hunting-Assistant

Repository URL:
https://github.com/Laibaausaf/AI-Powered-Job-Hunting-Assistant

Project Type:
Hackathon MVP / Full-stack AI career platform

Team:
3 members

Current development focus:
Backend + Database + AI foundation

Frontend:
Not implemented yet. Frontend will be developed separately.

---

# 2. PRODUCT PURPOSE

The AI-Powered Job Hunting Assistant is designed as a centralized career-management platform.

The goal is not to provide isolated AI utilities.

The goal is to guide a job seeker through the complete job-search workflow:

Discover
→ Understand
→ Tailor
→ Prepare
→ Apply
→ Track
→ Analyze

The platform should feel like a personal recruitment/career manager.

---

# 3. IMPORTANT CURRENT REALITY

DO NOT ASSUME THE ORIGINAL PROJECT PLAN IS THE CURRENT IMPLEMENTATION.

The backend has already been implemented.

Before modifying anything:

1. Read this file.
2. Read PROJECT_STATUS.md.
3. Read backend/README.md.
4. Read the relevant file in docs/.
5. Inspect the existing source code.
6. Preserve existing working architecture unless there is a clear reason to change it.

Do not rebuild the backend from scratch.

Do not replace FastAPI with another framework.

Do not replace SQLite/SQLAlchemy unless explicitly requested.

Do not introduce another ORM.

Do not create duplicate services that already exist.

---

# 4. CURRENT TECHNOLOGY STACK

Backend:

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Pydantic Settings

Authentication:

- bcrypt password hashing
- JWT
- python-jose

AI:

- Anthropic Claude API
- anthropic Python SDK
- Configurable Claude model

Document processing:

- pypdf
- python-docx
- python-multipart

Environment management:

- python-dotenv
- pydantic-settings

Frontend:

Not implemented yet.

---

# 5. CURRENT BACKEND STRUCTURE

backend/

    app/

        routers/
            analytics.py
            applications.py
            auth.py
            dashboard.py
            interview.py
            jobs.py
            profile.py

        services/
            llm_service.py
            matching.py
            resume_parser.py

        __init__.py
        auth.py
        config.py
        database.py
        main.py
        models.py
        schemas.py
        seed_data.py

    .env.example
    .gitignore
    README.md
    requirements.txt

---

# 6. CURRENT DATABASE MODELS

The current database contains:

## User

Stores:

- id
- email
- hashed password
- full name
- cached resume text
- cached extracted skills
- created timestamp

## Job

Stores:

- id
- title
- company
- location
- remote status
- role level
- salary range
- description
- skills
- posted date
- source

## Application

Stores:

- id
- user
- job
- status
- follow-up date
- cover letter
- match score
- skill gaps
- status history
- timestamps

## InterviewSession

Stores:

- id
- user
- job
- generated questions
- creation timestamp

## InterviewAnswer

Stores:

- id
- interview session
- question index
- answer text
- AI feedback
- creation timestamp

---

# 7. JOB DATA

The current MVP uses a deterministic synthetic seed dataset.

The dataset contains 250 job postings.

Every seeded job has:

source = "seed"

The dataset includes roles such as:

- Frontend Developer
- Backend Developer
- Full Stack Developer
- Data Analyst
- Data Scientist
- Machine Learning Engineer
- DevOps Engineer
- Mobile Developer
- Product Manager
- UX Designer
- QA Engineer
- Cloud Engineer

The dataset contains local, international, hybrid, on-site and remote examples.

IMPORTANT:

The current system does NOT perform live LinkedIn scraping.

The live job API integration is currently a future/optional feature.

Do not claim that LinkedIn jobs are currently being fetched.

---

# 8. CURRENT BACKEND MODULES

## Authentication

Implemented:

POST /auth/register

POST /auth/login

GET /auth/me

---

## Job Search

Implemented:

GET /jobs/search

GET /jobs/{job_id}

Search supports:

- free-text query
- location
- remote-only
- role level
- minimum salary
- posting age
- result limit

---

## Resume Processing

Implemented:

POST /profile/resume

Supported files:

- PDF
- DOCX
- TXT

The parser extracts text and stores the resume text against the user.

Skills are extracted using the current deterministic vocabulary-based matching service.

---

## Job Matching

Implemented.

Match scoring is deterministic and explainable.

Current formula:

matched required skills / total required skills × 100

The matching service also handles common skill aliases.

The LLM is NOT responsible for the numerical score.

---

## Application Assistance

Implemented:

POST /applications/tailor

The service can:

- analyze resume against a job
- identify skill gaps
- generate tailored resume bullet suggestions
- generate a tailored cover letter
- calculate match score
- create/update a tracked application for database jobs

---

## Resume Autofill

Implemented:

GET /profile/autofill

Claude extracts:

- name
- email
- experience summary
- skills

The user's stored email is used as the email fallback.

---

## Interview Preparation

Implemented:

POST /interview/generate

POST /interview/answer

GET /interview/session/{session_id}

The system generates job-specific interview questions.

Categories currently include:

- behavioral
- technical
- culture_fit

Answer feedback currently includes:

- clarity
- structure
- relevance
- written feedback

---

## Application Tracking

Implemented:

POST /dashboard/applications

GET /dashboard/applications

GET /dashboard/applications/upcoming

PATCH /dashboard/applications/{application_id}

GET /dashboard/summary

Supported statuses:

- Saved
- Applied
- Interviewing
- Offer
- Rejected
- Closed

Status changes are persisted in SQLite.

---

## Analytics

Implemented:

GET /analytics

Current analytics include:

- total applications
- response rate
- average time to response
- status breakdown
- optional salary benchmark

Analytics are calculated from stored application records.

---

# 9. AI SERVICE

All Claude API communication is centralized in:

backend/app/services/llm_service.py

Current AI functions:

1. Generate tailored resume bullet suggestions
2. Generate cover letters
3. Extract autofill/profile information
4. Generate interview questions
5. Evaluate interview answers

The frontend must never directly access the Anthropic API.

The backend is responsible for AI calls.

---

# 10. AI VS DETERMINISTIC LOGIC

Use AI for:

- language understanding
- resume interpretation
- generation
- interview question generation
- interview feedback
- cover letters
- contextual suggestions

Use normal Python/backend logic for:

- database operations
- filtering
- sorting
- pagination
- authentication
- authorization
- status changes
- date calculations
- analytics
- match-score mathematics
- validation

Do not replace deterministic logic with an LLM unnecessarily.

---

# 11. CURRENT AI MODEL CONFIGURATION

Environment variable:

CLAUDE_MODEL

Current default:

claude-3-5-haiku-20241022

The model is loaded from `.env` through `app/config.py`.

---

# 12. ENVIRONMENT VARIABLES

Required:

ANTHROPIC_API_KEY

Optional/configurable:

CLAUDE_MODEL

JWT_SECRET

JWT_ALGORITHM

JWT_EXPIRE_MINUTES

DATABASE_URL

The real `.env` file must NEVER be committed.

Use `.env.example` as the public template.

---

# 13. LOCAL BACKEND STARTUP

From the repository root:

cd backend

Create environment:

python -m venv .venv

Windows PowerShell:

.venv\Scripts\Activate.ps1

Windows Git Bash:

source .venv/Scripts/activate

Install dependencies:

pip install -r requirements.txt

Create:

backend/.env

using:

backend/.env.example

Fill in the Anthropic API key.

Seed the database:

python -m app.seed_data

Start server:

uvicorn app.main:app --reload

Backend:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Health:

http://localhost:8000/health

---

# 14. FRONTEND INTEGRATION

The frontend must communicate with FastAPI.

The frontend must NOT:

- access SQLite directly
- access SQLAlchemy directly
- contain Anthropic API keys
- implement duplicate backend business logic

Frontend integration should follow:

Frontend
→ FastAPI
→ Services
→ Database / Claude

---

# 15. CURRENT PROJECT STATUS

Implemented:

- Repository foundation
- Backend structure
- FastAPI application
- SQLite database
- SQLAlchemy models
- Authentication
- JWT
- Password hashing
- Seed dataset
- Job search
- Job filtering
- Job ranking
- Deterministic match scoring
- Resume parsing
- Claude AI service
- Application tailoring
- Cover letter generation
- Resume bullet suggestions
- Autofill
- Interview generation
- Interview feedback
- Application tracking
- Follow-up tracking
- Analytics

Not implemented:

- Frontend
- Live LinkedIn integration
- Live Indeed integration
- Live Rozee integration
- Browser extension
- Production deployment
- Production-grade authentication
- Full automated test suite
- Final UI/UX

---

# 16. DEVELOPMENT RULE FOR AI ASSISTANTS

Before changing code:

1. Read AI_CONTEXT.md.
2. Read PROJECT_STATUS.md.
3. Read relevant docs.
4. Inspect existing code.
5. Identify the smallest required change.
6. Explain which files will change.
7. Implement.
8. Test.
9. Update documentation if behavior changed.

Never blindly regenerate the backend.

Never overwrite existing functionality without checking it first.

Never expose secrets.

Never commit `.env`.

Never assume planned functionality is already implemented.

---

# 17. CURRENT DEVELOPMENT PRIORITY

Current priority:

1. Verify backend locally
2. Fix backend issues discovered during testing
3. Verify every API endpoint
4. Verify AI calls
5. Verify database persistence
6. Integrate frontend
7. Build final user experience
8. Perform end-to-end testing
9. Polish demo
10. Deploy