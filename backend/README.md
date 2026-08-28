# AI Job Hunting Assistant — Backend

FastAPI + SQLite backend covering Modules A–E of the HackHorizon problem statement.
AI features (tailoring, cover letters, interview questions/feedback) run on the
**Anthropic Claude API**. Job data is a **seed dataset** (250 synthetic postings,
clearly labeled `source="seed"`) per Section 9's note that live scraping may be
blocked during judging — see `app/seed_data.py` for where to plug in a real API later.

## 1. Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and paste your Anthropic API key (get one at https://console.anthropic.com/)
```

## 2. Seed the job database (run once)

```bash
python -m app.seed_data
```
This creates `jobhunt.db` with 250 seed jobs (Module A requires ≥200).

## 3. Run the server

```bash
uvicorn app.main:app --reload
```

- API base URL: http://localhost:8000
- Interactive docs (Swagger UI, great for your teammate + judges): http://localhost:8000/docs

## 4. Demo flow matching Section 5's use cases

1. `POST /auth/register` → `POST /auth/login` → copy the `access_token`, use it as a
   Bearer token on all further requests (click "Authorize" in `/docs`).
2. `POST /profile/resume` (multipart file upload, PDF/DOCX/TXT) → extracts and
   caches skills on your user.
3. `GET /jobs/search?query=remote junior data analyst SQL Python&remote_only=true`
   → ranked results with a match score once your resume is on file (UC-1).
4. `POST /applications/tailor` with a `job_id` → skill gaps, tailored bullets,
   cover letter, and it auto-creates a "Saved" dashboard row (UC-2).
5. `GET /profile/autofill` → demo auto-fill fields from your resume.
6. `POST /interview/generate` with a `job_id` → ≥8 questions across 3 categories;
   then `POST /interview/answer` for each one to get feedback (UC-3).
7. `GET /dashboard/applications`, `PATCH /dashboard/applications/{id}` to move
   status Saved → Applied → Interviewing → Offer/Rejected, `GET
   /dashboard/applications/upcoming` for follow-up deadlines (UC-4).
8. `GET /analytics?role_for_benchmark=Data Analyst` → response rate, avg
   time-to-response, status breakdown, salary benchmark (UC-5).

## 5. Project layout

```
app/
├── main.py            # FastAPI app + router registration
├── config.py          # env-based settings
├── database.py        # SQLite/SQLAlchemy session
├── models.py           # User, Job, Application, InterviewSession, InterviewAnswer
├── schemas.py           # Pydantic request/response contracts (frontend should build against these)
├── auth.py              # mock local auth (register/login/JWT)
├── seed_data.py          # generates the 250-job seed dataset
├── routers/               # one file per module (A–E) + auth + profile
└── services/
    ├── llm_service.py     # all Claude API calls
    ├── matching.py         # skill-overlap match score (deterministic, explainable)
    └── resume_parser.py     # PDF/DOCX/TXT text extraction
```

## 6. Notes for judging / README disclosures (Section 6.3)

- Job postings are **seed/sample data**, not live-scraped — disclosed via each
  job's `source` field and in this README.
- The Anthropic API key is read from `.env` (never hardcoded, never sent to the
  client) — see `.env.example`.
- Match scores are computed with a transparent skills-overlap formula
  (`app/services/matching.py`) rather than an opaque model call, so results are
  independently verifiable by a judge against the top-5 acceptance bar.
- Auth is intentionally minimal (bcrypt-hashed passwords + JWT) — sufficient to
  isolate per-user demo data, not intended as production security.

## 7. Still to build (your part / teammate's part)

- Frontend (React/Vue/etc.) consuming this API — see `app/schemas.py` for exact
  response shapes.
- Optional stretch goals (Section 8): live job API integration
  (`app/seed_data.py::ingest_from_api` is the stub), browser extension,
  voice-to-text for mock interviews, etc.
