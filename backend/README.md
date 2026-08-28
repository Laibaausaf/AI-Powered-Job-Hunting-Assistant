# AI Job Hunting Assistant — Backend

This directory contains the implemented FastAPI backend of the
AI-Powered Job Hunting Assistant.

## Current Status

The backend MVP is implemented.

It currently provides:

- Authentication
- JWT authorization
- SQLite database
- SQLAlchemy models
- 250 synthetic seed jobs
- Job search
- Job filtering
- Deterministic job matching
- Resume parsing
- Claude AI integration
- Resume tailoring
- Cover-letter generation
- Interview preparation
- Mock interview feedback
- Application tracking
- Follow-up tracking
- Analytics

The frontend is being developed separately.

## Important Limitation

The current job dataset is synthetic seed data.

The system does NOT currently fetch live LinkedIn, Indeed, or Rozee jobs.

Live job API integration is a future feature.

For complete setup instructions, read:

docs/SETUP.md