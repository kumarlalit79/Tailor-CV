Implementation Plan — Step-by-Step Build Sequence
Project Goal
Build an AI-powered ATS Resume Tailoring application using:
Next.js frontend
FastAPI backend
OpenAI API
fixed HTML resume template
PDF export
The final MVP should allow users to:
paste job description
paste resume
generate ATS-friendly resume
generate ATS score
generate cover letter
generate cold email
download PDF
without signup/login.

Development Philosophy
The implementation should prioritize:
fast MVP delivery
stable architecture
production-style folder structure
clean codebase
simplicity over overengineering

Phase 1 — Project Setup & Foundation
Goal
Set up:
repositories
folder structures
frontend/backend communication
environment variables
local development workflow
This phase creates the foundation for the entire app.

Tasks
Frontend Setup
Initialize:
npx create-next-app@latest
Configuration:
TypeScript
App Router
Tailwind CSS
ESLint

Backend Setup
Create FastAPI backend:
python -m venv venv
Install:
FastAPI
uvicorn
pydantic
jinja2
openai
weasyprint
python-dotenv

Create Folder Structures
Frontend:
frontend/
Backend:
backend/

Configure Environment Variables
Frontend:
NEXT_PUBLIC_API_URL=
Backend:
OPENAI_API_KEY=
OPENAI_MODEL=
FRONTEND_URL=
PDF_OUTPUT_DIR=

Setup Git Repository
Initialize:
git init
Create:
.gitignore
README.md

Setup CORS
Allow frontend to connect with FastAPI backend.

Create Health Check Endpoint
GET /health

Done Criteria
Phase 1 is complete when:
frontend runs locally
backend runs locally
frontend successfully calls backend
environment variables work
folder structure finalized
Git repository initialized

Phase 2 — Resume Template Engine
Goal
Build the fixed ATS resume rendering system.
This is the MOST IMPORTANT phase.
The AI should only inject content into a predefined resume template.

Tasks
Create Resume HTML Template
File:
resume_template.html
Implement:
fixed structure
Times New Roman typography
ATS-friendly layout

Create Resume CSS
File:
resume.css
Include:
exact font sizes
spacing
margins
line heights

Implement Hard Constraints
Resume MUST:
remain single-page
avoid overflow
avoid tables/icons/images
use compact spacing

Apply Resume Specifications
Required Styling
Name
18px bold
Role
14px normal
Contact Line
10px normal
Section Headings
12px bold uppercase
Body Content
11–12px normal

Configure Page Margins
Top: 0.1in
Bottom: 0in
Left: 0.3in
Right: 0.3in

Build Template Injection Logic
Use:
Jinja2 templates
Flow:
JSON → HTML Template → Rendered Resume

Create Sample Static Resume
Use fake data to verify:
alignment
spacing
page fit

Done Criteria
Phase 2 is complete when:
static resume renders correctly
PDF export works
resume remains single-page
formatting matches your Google Docs resume
no overflow occurs
ATS-safe formatting verified

Phase 3 — AI Integration Layer
Goal
Integrate OpenAI API and implement resume generation logic.

Tasks
Create OpenAI Service
File:
openai_service.py
Handles:
API calls
prompt execution
response parsing

Add Resume Prompt Logic
Use your custom prompt files:
resume_prompt.txt
cover_letter_prompt.txt
cold_email_prompt.txt

Implement Resume Generation Endpoint
POST /generate-resume

Parse AI Output
Convert AI response into:
{
 "summary": "",
 "skills": [],
 "experience": [],
 "projects": []
}

Inject AI Output Into Template
Flow:
Resume + JD
   ↓
OpenAI
   ↓
Structured JSON
   ↓
Inject Into HTML

Optimize Prompt Size
Reduce:
unnecessary JD text
repeated instructions
Improve:
speed
token usage

Done Criteria
Phase 3 is complete when:
AI generates resume successfully
response time stays reasonable
generated resume fits template
AI output is stable
keywords inject properly
no formatting breaks occur

Phase 4 — Core Features Development
Goal
Build all primary product features.

Tasks
Build JD Analysis Endpoint
POST /analyze-jd
Extract:
role
skills
keywords

Build ATS Score Engine
POST /generate-ats-score
Logic:
keyword matching
missing skills
role alignment

Build Cover Letter Generator
POST /generate-cover-letter

Build Cold Email Generator
POST /generate-cold-email
Rules:
100–150 words
concise
no em dash

Build PDF Download Endpoint
GET /download-resume

Implement Temporary PDF Storage
Auto-delete generated PDFs after timeout.

Add Copy-to-Clipboard Functionality
Frontend:
resume
cover letter
cold email

Done Criteria
Phase 4 is complete when:
all generators work
ATS score displays correctly
PDF downloads correctly
cover letters generate correctly
cold emails generate correctly
outputs are copyable

Phase 5 — UI Polish & Responsive Design
Goal
Make the app visually polished and mobile responsive.

Tasks
Build Main Layout
Sections:
JD input
resume input
generated outputs

Implement Loading States
Examples:
Generating ATS Resume...
Generating Cover Letter...
Analyzing Keywords...

Add Toast Notifications
Examples:
Copied successfully
PDF downloaded

Add Error States
Examples:
API failure
timeout
empty fields

Mobile Responsiveness
Support:
mobile
tablet
desktop

Improve Resume Preview UI
Add:
preview container
PDF-like styling

Apply Final Color Palette
Use:
minimal white UI
dark text
blue accents

Done Criteria
Phase 5 is complete when:
UI feels polished
mobile layout works
loading states exist
error handling visible
resume preview looks professional

Phase 6 — Testing, Validation & Edge Cases
Goal
Ensure reliability and stability.

Tasks
Test Long Job Descriptions
Ensure:
no crashes
acceptable speed

Test Long Resumes
Ensure:
single-page enforcement
spacing adjustments

Test Invalid Inputs
Examples:
empty JD
empty resume
malformed content

Test PDF Generation
Verify:
spacing
font rendering
margin consistency

Test AI Failure Cases
Examples:
rate limits
timeout
malformed AI responses

Validate ATS Compatibility
Ensure:
no tables
no images
semantic headings
readable PDF text

Cross Browser Testing
Test:
Chrome
Edge
Firefox

Done Criteria
Phase 6 is complete when:
edge cases handled
no major crashes
PDF rendering stable
ATS-safe formatting verified
frontend validation works

Phase 7 — Deployment & Production Configuration
Goal
Deploy frontend and backend publicly.

Tasks
Deploy Frontend
Use:
 Vercel

Deploy Backend
Use:
 Render
 or
 Railway

Configure Production Environment Variables
Frontend:
NEXT_PUBLIC_API_URL=
Backend:
OPENAI_API_KEY=

Configure CORS for Production
Allow deployed frontend domain.

Add HTTPS
Ensure:
secure API requests
protected API keys

Optimize API Performance
Reduce:
prompt size
unnecessary AI calls

Final Production Testing
Verify:
PDF generation
mobile responsiveness
API stability
download flow

Done Criteria
Phase 7 is complete when:
app publicly accessible
frontend/backend communicate successfully
production environment stable
PDFs download correctly
OpenAI integration works in production

Final MVP Completion Checklist
The MVP is complete when users can:
✅ Paste job description
 ✅ Paste resume text
 ✅ Generate ATS-friendly resume
 ✅ Generate ATS score
 ✅ Generate cover letter
 ✅ Generate cold email
 ✅ Download single-page PDF
 ✅ Use app without signup/login
 ✅ Complete workflow in under 5 minutes

