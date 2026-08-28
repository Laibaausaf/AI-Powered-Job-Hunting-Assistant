# System Architecture

## AI-Powered Job Hunting Assistant

This document describes the architecture that is currently implemented in the project.

The project is being developed as a full-stack AI-powered career platform.

The current implementation focuses on the backend, database, and AI services.

The frontend will be developed separately and will communicate with the backend through REST APIs.

---

# 1. High-Level Architecture

The platform follows a layered architecture:

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │   FRONTEND    │
              │   Web Client  │
              └───────┬───────┘
                      │
                 HTTP / REST
                      │
                      ▼
              ┌───────────────┐
              │    FASTAPI    │
              │   main.py     │
              └───────┬───────┘
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
        ┌───────────┐    ┌────────────┐
        │  Routers  │    │    Auth    │
        │           │    │ JWT/Bcrypt │
        └─────┬─────┘    └────────────┘
              │
              ▼
        ┌──────────────┐
        │   Services   │
        ├──────────────┤
        │ Matching     │
        │ Resume       │
        │ LLM / Claude │
        └──────┬───────┘
               │
        ┌──────┴─────────┐
        │                │
        ▼                ▼
  ┌─────────────┐  ┌─────────────┐
  │ SQLAlchemy  │  │ Claude API  │
  │ ORM         │  │ Anthropic   │
  └──────┬──────┘  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │   SQLite    │
  │  Database   │
  └─────────────┘