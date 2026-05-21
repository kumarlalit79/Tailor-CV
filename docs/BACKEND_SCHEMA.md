Backend Schema — Data Model & Backend Architecture
1. Backend Philosophy
The backend should remain:
Simple + Stateless + Fast
This project does NOT need:
complex databases
authentication systems
user management
session management
role-based access
microservices
queues
event buses
for V1.
The goal is:
Generate resume → return result → download PDF
That’s it.

2. Database Architecture
V1 Database Decision
No Database Required
This is the correct architecture for MVP.

Why No Database?
Because the app:
has no signup/login
stores no users
stores no resume history
stores no analytics
stores no subscriptions
stores no saved documents
All operations are:
request → process → return response

Current Data Flow
Frontend
  ↓
FastAPI Backend
  ↓
OpenAI API
  ↓
Generate Output
  ↓
Return JSON/PDF
No persistence layer needed.

3. Backend Data Models (Pydantic Schemas)
Even without a database, we STILL need:
request schemas
response schemas
validation models
using:
Pydantic

Resume Generation Request Schema
class ResumeRequest(BaseModel):
   job_description: str
   resume_text: str

Resume Generation Response Schema
class ResumeResponse(BaseModel):
   optimized_resume: str
   ats_score: int
   matched_keywords: list[str]
   missing_keywords: list[str]
   pdf_url: str | None

Cover Letter Request Schema
class CoverLetterRequest(BaseModel):
   optimized_resume: str
   job_description: str

Cover Letter Response Schema
class CoverLetterResponse(BaseModel):
   cover_letter: str

Cold Email Request Schema
class ColdEmailRequest(BaseModel):
   optimized_resume: str
   job_description: str

Cold Email Response Schema
class ColdEmailResponse(BaseModel):
   cold_email: str

ATS Score Response Schema
class ATSResponse(BaseModel):
   ats_score: int
   matched_keywords: list[str]
   missing_keywords: list[str]
   suggestions: list[str]

4. Authentication Architecture
Authentication Requirement
No Authentication in V1
No:
signup
login
OAuth
JWT
sessions
cookies

Reason
Authentication adds:
complexity
backend state
database dependency
session handling
edge cases
without improving MVP value.

User Access Model
Access Type
Public Access
Anyone can:
paste JD
paste resume
generate outputs
download PDF

Permissions Model
Not required.
No:
admin
user
guest
RBAC

5. Sensitive Data Handling
Even without auth, the app still processes:
resumes
emails
phone numbers
personal information
So backend should follow minimal security practices.

Sensitive Fields
Potential sensitive content:
email address
phone number
LinkedIn URL
GitHub URL
work history

Storage Policy
Important Rule
DO NOT store resumes permanently.
Process in-memory only.

Temporary File Policy
Generated PDFs may be:
temporarily stored
auto-deleted later

Example Strategy
generated/
  └── temp/
Delete files:
after 30 minutes
or:
after download

Logging Restrictions
DO NOT log:
full resume content
API payloads
personal information
Allowed:
request duration
success/failure
error types

6. File / Media Storage Structure
File Uploads
V1 Decision
No file uploads.
Only:
paste text input

Generated PDF Storage
Temporary structure:
backend/
│
├── generated/
│   ├── resumes/
│   └── temp/

File Naming Convention
{user_name}_{company_name}_resume.pdf
Example:
Lalit_Kumar_Google_Resume.pdf

7. Webhooks / Event Triggers
V1 Decision
No webhooks required.

Reason
The app:
has no external integrations
has no async workflows
has no payment system
has no notifications

Future Webhook Possibilities
Possible future integrations:
payment success
email delivery
resume analytics
job tracking
Not needed now.

8. API Architecture
Base URL
/api/v1

API Design Principles
APIs should be:
RESTful
stateless
JSON-first
predictable
lightweight

9. API Endpoint List
Health Check
GET /health
Purpose:
deployment monitoring
uptime checks

Analyze Job Description
POST /analyze-jd
Input:
{
 "job_description": "..."
}
Output:
{
 "role": "Backend Engineer",
 "skills": [],
 "keywords": []
}

Generate ATS Resume
POST /generate-resume
Input:
{
 "job_description": "...",
 "resume_text": "..."
}
Output:
{
 "optimized_resume": "...",
 "ats_score": 87,
 "matched_keywords": [],
 "missing_keywords": []
}

Generate Cover Letter
POST /generate-cover-letter

Generate Cold Email
POST /generate-cold-email

Generate ATS Score
POST /generate-ats-score

Download Resume PDF
GET /download-resume/{file_id}

10. Backend Service Architecture
Recommended Service Structure
services/
│
├── openai_service.py
├── resume_service.py
├── ats_service.py
├── pdf_service.py
└── jd_analysis_service.py

Service Responsibilities
openai_service.py
Handles:
OpenAI API calls
prompt execution
response parsing

resume_service.py
Handles:
resume optimization
template injection
formatting logic

ats_service.py
Handles:
keyword matching
ATS score calculation
suggestions

pdf_service.py
Handles:
HTML rendering
PDF generation
file cleanup

jd_analysis_service.py
Handles:
keyword extraction
role detection
tech stack detection

11. HTML Template Architecture
Important Rule
Resume template MUST remain:
hardcoded HTML + CSS
AI must NEVER:
generate layout
generate CSS
generate HTML structure

Template Structure
templates/
  └── resume_template.html

CSS Structure
static/
  └── resume.css

Rendering Flow
AI Content
   ↓
Pydantic Validation
   ↓
Inject Into HTML Template
   ↓
Generate PDF

12. Resume Rendering Constraints (Critical)
These settings are mandatory.

Resume Font Settings
Font Family: Times New Roman

Name Style
18px
Bold
Uppercase
Centered

Role Line
14px
Normal
Centered

Contact Line
10px
Normal
Centered

Section Headings
12px
Bold
Uppercase

Body Content
11px–12px
Normal
Compact spacing

Page Margins
Top: 0.1in
Bottom: 0in
Left: 0.3in
Right: 0.3in

Resume Constraints
Must:
remain single-page
remain ATS-friendly
avoid overflow

Forbidden Elements
DO NOT USE:
icons
tables
images
multi-columns
progress bars
graphics
em dash

13. Environment Variables
Backend .env
OPENAI_API_KEY=

OPENAI_MODEL=gpt-4o-mini

PDF_OUTPUT_DIR=

FRONTEND_URL=

ENVIRONMENT=development

14. Future Scalability (Not Needed Now)
Possible future additions:
PostgreSQL
Redis
Celery
authentication
resume history
analytics
rate limiting
But for V1:
keep backend extremely simple

