# Database Design

## AI-Powered Job Hunting Assistant

---

# 1. Purpose

The database stores the persistent information required by the current MVP of the AI-Powered Job Hunting Assistant.

The database allows the backend to remember information even after the application is restarted.

The current database supports:

- User accounts
- User profile information
- User resume text and skills
- Job postings
- Job search and matching
- Job applications
- Application statuses
- Match scores
- Skill gaps
- Interview practice sessions
- Interview questions
- Interview answers
- AI interview feedback
- Application analytics

The current implementation uses:

- **SQLite** as the database
- **SQLAlchemy** as the ORM

---

# 2. Current Database Technology

## Database

```text
SQLite

┌────────────────────┐
│        USER        │
├────────────────────┤
│ id                 │
│ email              │
│ hashed_password    │
│ full_name          │
│ resume_text        │
│ skills             │
│ created_at         │
└─────────┬──────────┘
          │
          │ 1
          │
          │
          ├───────────────────────┐
          │                       │
          │                       │
          │ *                     │ *
          ▼                       ▼
┌────────────────────┐   ┌──────────────────────┐
│    APPLICATION     │   │   INTERVIEW SESSION  │
├────────────────────┤   ├──────────────────────┤
│ id                 │   │ id                   │
│ user_id            │   │ user_id              │
│ job_id             │   │ job_id               │
│ status             │   │ questions            │
│ match_score        │   │ created_at           │
│ skill_gaps         │   └──────────┬───────────┘
│ cover_letter       │              │
│ follow_up_date     │              │ 1
│ status_history     │              │
│ created_at         │              │ *
│ updated_at         │              ▼
└─────────┬──────────┘      ┌──────────────────────┐
          │                 │   INTERVIEW ANSWER  │
          │ *               ├──────────────────────┤
          ▼                 │ id                   │
┌────────────────────┐      │ session_id           │
│        JOB         │      │ question_index       │
├────────────────────┤      │ answer               │
│ id                 │      │ feedback             │
│ title              │      │ created_at           │
│ company            │      └──────────────────────┘
│ location           │
│ remote             │
│ role_level         │
│ salary_min         │
│ salary_max         │
│ description        │
│ skills             │
│ posted_at          │
│ source             │
└────────────────────┘