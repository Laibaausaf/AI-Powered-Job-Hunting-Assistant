# API Reference

Base URL:

http://localhost:8000

Swagger:

http://localhost:8000/docs

---

## Authentication

POST /auth/register

POST /auth/login

GET /auth/me

---

## Jobs

GET /jobs/search

GET /jobs/{job_id}

Query parameters:

- query
- location
- remote_only
- role_level
- salary_min
- posted_after_days
- limit

---

## Profile

POST /profile/resume

GET /profile/autofill

Supported resume formats:

- PDF
- DOCX
- TXT

---

## Application Assistance

POST /applications/tailor

Supports:

- job_id
- pasted job description
- resume
- skill-gap calculation
- tailored resume bullets
- cover letter

---

## Interview

POST /interview/generate

POST /interview/answer

GET /interview/session/{session_id}

---

## Dashboard

POST /dashboard/applications

GET /dashboard/applications

GET /dashboard/applications/upcoming

PATCH /dashboard/applications/{application_id}

GET /dashboard/summary

---

## Analytics

GET /analytics

Optional query:

role_for_benchmark

---

## Authentication

Protected endpoints require:

Authorization: Bearer <JWT>

Use the Swagger "Authorize" button.

---

## Important

The exact request and response schemas are defined in:

backend/app/schemas.py

If this document and the implementation disagree, inspect the actual backend implementation and update this document rather than inventing a new API.