# System Architecture

## 1. Overview

The AI-Powered Job Hunting Assistant is a web-based career management platform.

The platform connects job discovery, job matching, application assistance, interview preparation, application tracking, and analytics into one user journey.

The system follows a layered architecture:

Frontend
↓
Backend API
↓
Application Services
↓
Database / AI Services / Job Data

---

## 2. High-Level Architecture

```text
┌─────────────────────────────────────┐
│             FRONTEND                │
│         Next.js / React             │
│                                     │
│ Landing Page                        │
│ Job Search                          │
│ Job Details                         │
│ Application Assistant               │
│ Interview Preparation               │
│ Application Tracker                 │
│ Analytics                           │
│ Profile                             │
└─────────────────┬───────────────────┘
                  │
                  │ HTTP / REST API
                  ▼
┌─────────────────────────────────────┐
│             BACKEND                 │
│              FastAPI                │
│                                     │
│ API Routes                          │
│ Validation                          │
│ Business Logic                      │
│ Application Services                │
│ Authentication                      │
└───────────────┬─────────┬───────────┘
                │         │
                │         │
                ▼         ▼
        ┌────────────┐  ┌──────────────┐
        │ DATABASE   │  │ AI SERVICES  │
        │            │  │              │
        │ Users      │  │ Resume       │
        │ Jobs       │  │ Matching     │
        │ Applications│ │ Skill gaps   │
        │ Interviews │  │ Cover letters│
        │ Resumes    │  │ Interview AI │
        └────────────┘  └──────────────┘
                │
                ▼
        ┌────────────────┐
        │   JOB DATA     │
        │                │
        │ Seeded jobs     │
        │ External sources│
        └────────────────┘