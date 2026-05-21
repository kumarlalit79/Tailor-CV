TRD — Technical Requirements Document
1. Project Overview
Project Name
TailorCV
Project Type
AI-powered ATS Resume Tailoring Platform
Objective
Build a lightweight web application that allows users to:
paste job descriptions
paste existing resume text
generate ATS-optimized resumes
generate cover letters
generate cold emails
download resume as PDF
The application should prioritize:
speed
simplicity
ATS compatibility
fixed professional formatting
minimal user friction

2. System Architecture
Architecture Style
Monolithic backend-first architecture.
Reason:
simpler deployment
easier debugging
faster development
ideal for MVP

3. Frontend Technology Stack
Framework
Next.js
Use:
Next.js App Router
TypeScript

Why Next.js
Chosen because:
clean routing
easy deployment on Vercel
server-side rendering support
modern frontend architecture
scalable for future SaaS conversion

Frontend Responsibilities
Frontend will handle:
UI rendering
form submission
loading states
displaying generated outputs
PDF download triggering
Frontend should NOT:
contain AI logic
process resume generation
store sensitive keys

Frontend Styling
Recommended:
Tailwind CSS
Reason:
fast UI development
clean responsive design
minimal CSS maintenance

UI Philosophy
UI should be:
clean
minimal
productivity-focused
not design-heavy
Avoid:
animations overload
dashboard complexity
unnecessary components

4. Backend Technology Stack
Framework
FastAPI

Language
Python 3.12+

Why FastAPI
Chosen because:
extremely fast API development
async support
OpenAPI documentation
AI ecosystem compatibility
clean architecture support
ideal for AI workflow APIs

Backend Responsibilities
Backend handles:
prompt orchestration
OpenAI communication
ATS scoring
HTML generation
PDF generation
business logic
validation
template rendering

5. Database Requirements
Database Needed?
V1 Decision:
NO DATABASE REQUIRED.
This is the correct decision for MVP.

Why No Database
Because V1:
has no signup/login
stores no user history
stores no resumes
has no analytics
has no payments
Everything can remain stateless.

Future Database (Optional)
If added later:
PostgreSQL
Recommended provider:
Supabase
 or
Neon

When Database Will Be Needed
Only if adding:
authentication
resume history
saved resumes
user accounts
subscriptions
analytics

6. Authentication
Authentication Requirement
No authentication in V1.

Reason
Reducing complexity:
faster development
simpler UX
easier deployment
better MVP execution

Future Authentication Options
Possible future integrations:
Clerk
Auth.js
Supabase Auth
Not needed now.

7. Hosting & Deployment
Frontend Hosting
Platform
Vercel

Why Vercel
seamless Next.js deployment
easy CI/CD
free hobby tier
fast global CDN
easy environment variable management

Backend Hosting
Recommended Options
Option 1 — Render
Render
Best for:
FastAPI beginners
easy deployment
simple configuration

Option 2 — Railway
Railway
Very beginner-friendly.

Option 3 — VPS (Later)
Use:
Docker
Nginx
Ubuntu server
Only after scaling.

Important Deployment Note
DO NOT host FastAPI backend on Vercel initially.
Reason:
serverless timeout issues
AI generation latency
PDF generation instability
Use:
Vercel → frontend
Render/Railway → backend
This is the proper architecture.

8. Third-Party APIs & Services
AI Provider
Primary Provider
OpenAI

Recommended Models
Preferred
GPT-4.1 Mini
GPT-4o Mini
Reason:
fast
affordable
good formatting consistency

Backup Provider
OpenRouter
Useful for:
free models
testing
fallback support

PDF Generation
Recommended Library
WeasyPrint

Alternative
wkhtmltopdf

Why HTML-to-PDF
Because:
resume design remains controlled
formatting consistency improves
ATS compatibility remains stable

9. Resume Generation Architecture
Important Technical Principle
AI MUST NOT generate:
HTML
CSS
layout structure
AI ONLY generates:
content
keywords
optimized bullet points
summaries
cover letters
emails

Resume Rendering Flow
Resume Text + Job Description
          ↓
     OpenAI Processing
          ↓
Structured JSON Output
          ↓
Inject Into HTML Template
          ↓
    HTML Resume
          ↓
     PDF Export

10. ATS Scoring System
V1 ATS Scoring Logic
Simple scoring based on:
keyword matching
required skill overlap
missing technologies
role relevance

Suggested Formula
ATS Score =
Keyword Match %
+ Skills Match %
+ Role Alignment %

Important Constraint
DO NOT attempt enterprise-grade ATS analysis initially.
Keep it lightweight and explainable.

11. API Design
Base URL
/api/v1

Endpoints
Analyze Job Description
POST /analyze-jd

Generate Resume
POST /generate-resume

Generate Cover Letter
POST /generate-cover-letter

Generate Cold Email
POST /generate-cold-email

Generate ATS Score
POST /generate-ats-score

Download PDF
GET /download-resume

12. Recommended Folder Structure
Frontend Structure (Next.js)
frontend/
│
├── app/
│   ├── page.tsx
│   ├── resume/
│   ├── cover-letter/
│   └── api/
│
├── components/
│   ├── forms/
│   ├── ui/
│   ├── loaders/
│   └── outputs/
│
├── services/
│   └── api.ts
│
├── types/
│
├── utils/
│
├── styles/
│
└── public/

Backend Structure (FastAPI)
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── resume.py
│   │   ├── ats.py
│   │   └── cover_letter.py
│   │
│   ├── services/
│   │   ├── openai_service.py
│   │   ├── ats_service.py
│   │   ├── pdf_service.py
│   │   └── resume_service.py
│   │
│   ├── templates/
│   │   └── resume_template.html
│   │
│   ├── static/
│   │   └── styles.css
│   │
│   ├── prompts/
│   │   ├── resume_prompt.txt
│   │   ├── cover_letter_prompt.txt
│   │   └── cold_email_prompt.txt
│   │
│   ├── schemas/
│   │
│   ├── utils/
│   │
│   └── config/
│
├── generated/
│
├── requirements.txt
│
└── .env

13. Naming Conventions
Backend
Files
Use:
snake_case.py
Example:
resume_service.py

Classes
Use:
PascalCase
Example:
class ResumeGenerator:

Functions
Use:
snake_case
Example:
generate_resume()

Frontend
Components
Use:
PascalCase.tsx
Example:
ResumeForm.tsx

Utility Functions
Use:
camelCase
Example:
generatePdf()

14. Environment Variables
Frontend (.env.local)
NEXT_PUBLIC_API_URL=

Backend (.env)
OPENAI_API_KEY=

OPENAI_MODEL=gpt-4o-mini

FRONTEND_URL=

PDF_OUTPUT_DIR=

ENVIRONMENT=development

15. Technical Constraints
Constraint 1 — Single Page Resume
All generated resumes MUST:
fit on one page
preserve spacing consistency
avoid overflow

Constraint 2 — No Em Dash Usage
System must avoid em dash:
—
in:
resumes
cover letters
cold emails

Constraint 3 — ATS Compatibility
Avoid:
icons
tables
graphics
multiple columns
images

Constraint 4 — Fixed Template
Resume layout must remain fixed.
AI modifies only:
content
wording
keywords

Constraint 5 — Response Time
Target:
resume generation < 60 seconds
complete workflow < 5 minutes

Constraint 6 — Stateless Backend
V1 backend should remain stateless.
No:
user sessions
stored resumes
background queues

16. Security Considerations
API Key Security
OpenAI keys MUST:
remain backend-only
never exposed to frontend

Input Validation
Validate:
resume length
JD length
malicious HTML/script input

Rate Limiting (Optional)
Future enhancement:
IP-based throttling

17. Scalability Considerations
Future scalability options:
Redis caching
Celery background jobs
PostgreSQL
Dockerization
Kubernetes
queue-based PDF generation
Not needed for MVP.

18. Recommended MVP Development Order
Phase 1
FastAPI setup
OpenAI integration
basic resume generation

Phase 2
HTML template injection
PDF generation

Phase 3
ATS scoring

Phase 4
cover letter generation
cold email generation

Phase 5
deploy frontend + backend

