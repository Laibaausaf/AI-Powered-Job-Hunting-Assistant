# AI Career Manager — Shared AI Context

## 1. Project Identity

Project Name:
AI-Powered Job Hunting Assistant

Repository:
AI-Powered-Job-Hunting-Assistant

This is a collaborative AI-powered job hunting platform being developed by a team of three.

The project is an MVP for a hackathon.

---

## 2. Core Purpose

The platform acts as an intelligent career assistant for job seekers.

The user should be able to move through the complete job-search journey from one platform:

Discover Jobs
→ Understand Job Fit
→ Improve Resume
→ Prepare Application
→ Prepare for Interview
→ Track Applications
→ Understand Job Search Progress

The product should feel like a helpful recruitment/career manager rather than a collection of disconnected AI tools.

---

## 3. MVP Modules

The MVP consists of five major modules:

1. Job Search & Recommendations
2. Application Assistance
3. Interview Preparation
4. Application Management
5. Insights & Analytics

---

## 4. Development Priority

The project is being developed in this order:

1. Backend foundation
2. Database
3. Job data
4. Job search and filtering
5. AI job matching
6. Resume analysis
7. Application assistance
8. Interview preparation
9. Application tracking
10. Analytics
11. Frontend integration
12. Testing
13. Final UI polish
14. Deployment

Frontend development will be handled separately by Team Member 3.

---

## 5. Team Responsibilities

### Team Member 1 — Backend + Database + Integration

Responsibilities:

- FastAPI backend
- Database design
- Database implementation
- Job data management
- Job search
- Job filtering
- Job ranking
- Application management
- Analytics calculations
- API design
- Backend/frontend integration
- Overall technical coordination

### Team Member 2 — AI / ML

Responsibilities:

- Resume processing
- Resume analysis
- Job matching
- Match score generation
- Skill-gap analysis
- Resume improvement suggestions
- Cover-letter generation
- Interview question generation
- Mock interview feedback
- AI service integration

### Team Member 3 — Frontend

Responsibilities:

- Next.js / React frontend
- UI/UX
- Landing page
- Navigation
- Job search interface
- Job cards
- Job details
- Resume/application interface
- Interview interface
- Application dashboard
- Analytics dashboard
- Profile interface
- Frontend API integration

---

## 6. Important Architecture Principle

The backend is the central application layer.

Frontend communicates with the backend through APIs.

AI functionality is accessed through backend services.

The frontend must never contain private API keys.

The database must not be directly accessed by the frontend.

The AI service must not directly control database state without going through defined backend logic.

---

## 7. AI Responsibility vs Normal Application Logic

Use AI for tasks that require language understanding or generation.

AI responsibilities include:

- Understanding resumes
- Understanding job descriptions
- Semantic job matching
- Explaining job match
- Identifying skill gaps
- Resume suggestions
- Cover-letter generation
- Interview question generation
- Interview answer evaluation

Use normal backend logic for deterministic operations.

Normal application logic includes:

- Database CRUD
- Filtering
- Sorting
- Pagination
- Application status changes
- Date calculations
- Follow-up dates
- Analytics calculations
- Validation
- Authentication
- Authorization

Do not use an LLM for simple deterministic calculations.

---

## 8. Job Data

The MVP must contain at least 200 job postings.

Every job should follow one standardized internal structure regardless of its source.

The system should be able to represent jobs from multiple job platforms.

Potential sources may include:

- LinkedIn
- Indeed
- Rozee
- Other legitimate job sources or APIs

Live scraping is not a required dependency for the MVP.

A seeded dataset may be used for demonstration.

Job source information must be stored with each job.

---

## 9. Job Matching

The system should produce a personalized match score from 0 to 100.

The match should consider relevant information such as:

- Skills
- Experience
- Education
- Job requirements
- User profile

The result should include an understandable explanation.

The explanation should help the user understand:

- Why the job matches
- What they already have
- What they are missing
- What they could improve

---

## 10. Application Assistance

The application module should support:

- Resume input
- Job description input
- Skill-gap analysis
- Resume improvement suggestions
- Tailored cover-letter generation
- Editable generated content

Generated content should be presented as suggestions.

The user remains in control and should be able to edit generated content.

---

## 11. Interview Preparation

The interview module should support:

- Job-specific interview questions
- Technical questions
- Behavioral questions
- General questions
- Mock interview
- Answer evaluation
- Actionable feedback

The system should not simply generate random questions.

Questions should be connected to the selected job and its requirements.

---

## 12. Application Management

Users should be able to save and track jobs.

Supported application statuses:

- Saved
- Applied
- Interviewing
- Offer
- Rejected
- Closed

Application state must persist in the database.

The system should support follow-up dates.

---

## 13. Analytics

Analytics should be calculated from persistent application data.

Potential metrics include:

- Applications submitted
- Interviews received
- Offers received
- Response rate
- Average match score
- Applications by status

Analytics should not be fake hardcoded numbers when real tracked data exists.

---

## 14. Data Integrity Rules

Do not create duplicate database records unnecessarily.

Do not overwrite user information without confirmation.

Validate user input before storing it.

Validate AI-generated structured output before saving it.

Database relationships must remain consistent.

Deleting one record must not unintentionally destroy unrelated records.

---

## 15. Human-Friendly Product Rules

The product should feel helpful and understandable.

Avoid unnecessary technical terminology in the user interface.

AI-generated recommendations should explain the reason behind them.

Users should be able to edit AI-generated content.

Errors should be understandable to normal users.

Never expose raw stack traces or internal errors to users.

Empty states should provide helpful next actions.

Loading states should be clear.

The platform should guide users instead of making them figure out what to do next.

---

## 16. Development Rules

Before modifying the project:

1. Read this file.
2. Read PROJECT_STATUS.md.
3. Read relevant documentation inside docs/.
4. Inspect existing code.
5. Understand existing APIs before changing them.
6. Do not unnecessarily restructure the project.
7. Do not introduce a new framework without team agreement.
8. Do not overwrite another teammate's work.
9. Keep changes focused on the assigned feature.
10. Test changes before considering them complete.

---

## 17. Git Rules

Do not develop directly on main.

Create a feature branch.

Example:

feature/job-search-api

feature/resume-analysis

feature/interview-ai

feature/application-dashboard

Commit focused changes.

Create a Pull Request before merging into main.

After another feature is merged:

git checkout main

git pull origin main

Then update the working branch if necessary.

---

## 18. Environment Variables

Never hardcode API keys.

Never commit the real .env file.

Use .env.example to document required environment variables.

Private credentials must remain local or in the approved deployment environment.

---

## 19. Coding Philosophy

Prefer:

- Simple solutions
- Clear names
- Small functions
- Reusable services
- Explicit validation
- Understandable code
- Minimal dependencies

Avoid unnecessary:

- Abstraction
- Complex design patterns
- Duplicate code
- Frameworks
- Microservices
- Over-engineering

This is an MVP.

Reliability and clarity are more important than complexity.

---

## 20. Current Project State

Phase:

Project Foundation

Current status:

- Repository created
- Team collaborators added
- Basic project folders created
- Shared AI context being created

Core application functionality has not been implemented yet.

---

## 21. Important Rule for AI Coding Assistants

Before writing or modifying code:

FIRST:
Understand the existing project.

SECOND:
Read the relevant documentation.

THIRD:
Explain briefly what files will be changed and why.

FOURTH:
Make the smallest necessary change.

FIFTH:
Test the change.

SIXTH:
Report what was changed.

Do not assume that a missing feature means the entire architecture should be redesigned.

Do not delete working code just to replace it with a preferred implementation.

The existing project is the source of truth.

---

## 22. MVP Philosophy

The objective is not to build every possible career feature.

The objective is to demonstrate a reliable end-to-end career assistant.

A user should be able to:

Find a job
→ See why it matches
→ Identify missing skills
→ Improve their application
→ Generate a tailored cover letter
→ Prepare for an interview
→ Track the application
→ See progress through analytics

Every major feature should contribute to this journey.