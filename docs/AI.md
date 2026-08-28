# AI System Design

## 1. Purpose

The AI layer provides intelligent career assistance where normal application logic is not sufficient.

The AI layer should support:

- Resume understanding
- Job matching
- Skill-gap analysis
- Resume improvement
- Cover-letter generation
- Interview question generation
- Mock interview feedback

---

# 2. AI Architecture

The AI must be accessed through backend services.

```text
Frontend
    ↓
Backend API
    ↓
AI Service
    ↓
LLM Provider