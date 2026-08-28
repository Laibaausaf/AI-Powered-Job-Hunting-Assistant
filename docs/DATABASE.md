# Database Design

## 1. Purpose

The database stores persistent information required by the AI-Powered Job Hunting Assistant.

The database should support:

- User profiles
- Resumes
- Job postings
- Saved jobs
- Applications
- Interviews
- Mock interview sessions
- Follow-up dates
- Application analytics

The database should store important user actions so information remains available after the application is restarted.

---

# 2. Main Entities

The initial database will contain these core entities:

1. User
2. Profile
3. Resume
4. Job
5. Saved Job
6. Application
7. Interview
8. Interview Session

---

# 3. Entity Relationship Overview

```text
USER
 │
 ├────────────── PROFILE
 │
 ├────────────── RESUME
 │
 ├────────────── SAVED JOB
 │                    │
 │                    ▼
 │                   JOB
 │                    │
 │                    ▼
 └────────────── APPLICATION
                       │
                       ▼
                   INTERVIEW
                       │
                       ▼
                INTERVIEW SESSION