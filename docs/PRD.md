PRD — AI Resume Tailor
App Name
TailorCV
Tagline
“Generate ATS-optimized resumes, cover letters, and cold emails in minutes.”

1. Problem Statement
Job seekers currently waste a huge amount of time manually tailoring resumes for every application.
Typical workflow today:
Copy job description from LinkedIn/Wellfound/Naukri
Open ChatGPT
Paste job description
Paste resume
Explain prompts again
Ask for ATS optimization
Ask for cover letter
Ask for cold email
Reformat everything manually
Export to PDF
This process is repetitive, slow, inconsistent, and frustrating.
Most existing resume builders also focus heavily on design instead of ATS optimization and practical job application workflows.

2. Target Audience
This product is built for:
software engineers
college students
freshers
backend/frontend/full-stack developers
professionals applying to multiple jobs daily
startup-focused job seekers
Especially users who:
apply to 10–50 jobs weekly
need tailored resumes quickly
want ATS-friendly resumes
send cold emails to founders/recruiters
are already using AI tools manually

3. Core Value Proposition
TailorCV automates the complete job application preparation workflow in one place.
Instead of manually using ChatGPT for every application, users can:
paste job description
paste existing resume
instantly generate:
ATS-friendly tailored resume
cover letter
cold email
ATS score
download polished single-page PDF resumes
Key differentiators:
single-page ATS-first resume generation
fixed professional template
optimized specifically for startup and tech hiring
extremely fast workflow
no unnecessary design complexity
no signup required
no manual formatting

4. Target User Persona
Persona 1 — Startup Job Hunter
A backend/full-stack developer applying to startups through LinkedIn, Wellfound, and cold outreach. They apply to many jobs daily and need customized resumes quickly without spending hours editing documents manually.
Persona 2 — College Student / Fresher
A student with limited experience who struggles to tailor resumes according to job descriptions and ATS keywords. They need a simple tool that helps improve resume quality and professionalism instantly.

5. Product Vision
The app should feel:
fast
minimal
practical
ATS-focused
productivity-driven
The goal is not to become a fancy design-based resume builder.
The goal is:
“Tailor and generate job-ready application material in under 5 minutes.”

6. Resume Design Requirements
The generated resume must always:
remain single-page
follow the same fixed structure
maintain ATS compatibility
avoid design-heavy layouts
use consistent typography and spacing

7. Resume Template Specifications
Typography
Name
Font: Times New Roman
Font Size: 18px
Font Weight: Bold
Role / Title
Font Size: 14px
Font Weight: Normal
Contact Line
Font Size: 10px
Font Weight: Normal
Section Headings
Examples:
Summary
Technical Skills
Work Experience
Projects
Education
Style:
Font Size: 12px
Font Weight: Bold
Uppercase
Body Text
Examples:
summary content
experience bullets
project details
Style:
Font Size: 11–12px
Font Weight: Normal

Page Layout
Margins
Top: 0.1
Bottom: 0
Left: 0.3
Right: 0.3
Format Rules
Single-page only
ATS-friendly formatting
Minimal spacing
No icons
No tables
No multi-column layouts
No graphics/images
No em dash usage anywhere

8. Core Features
Must Have Features (V1)
1. Job Description Input
User can paste a job description into a text area.

2. Resume Input
User can paste existing resume text into a text area.
No file upload in V1.

3. Job Description Analysis
System extracts:
role name
required skills
ATS keywords
technologies
responsibilities

4. ATS Resume Generation
AI generates a tailored resume based on:
user resume
job description
ATS keywords
Rules:
keep facts truthful
improve wording
optimize bullets
inject keywords naturally
maintain fixed template structure
keep resume single-page

5. ATS Score Generation
System generates:
ATS compatibility score
missing keyword suggestions
improvement feedback
Example:
ATS Score: 87/100

Missing Keywords:
- Docker
- CI/CD
- AWS Lambda

6. Cover Letter Generation
Generate professional cover letter based on:
tailored resume
job description
Rules:
concise
professional
no em dash

7. Cold Email Generation
Generate short cold outreach email:
100–150 words
founder/recruiter-friendly
concise
personalized
no em dash

8. PDF Download
User can download generated resume as PDF.
Naming format:
Lalit_Kumar_Google_Resume.pdf

9. Fixed Resume Template
All generated resumes must follow:
same HTML structure
same CSS
same spacing
same typography
AI only replaces content.

Nice to Have Features (V2/V3)
Resume History
Save previous generated resumes.

Multiple Templates
Allow users to switch templates.

DOCX Export
Export resume as DOCX.

Resume Keyword Highlighting
Highlight keywords added from JD.

Smart Suggestions
Suggest improvements before generation.

Resume Version Comparison
Compare old vs new resume.

AI Job Match Percentage
Show:
Job Match: 82%

Resume Analytics
Track:
keyword match
readability
ATS optimization

9. User Stories
Resume Generation
As a job seeker, I want to paste my resume and job description so that I can instantly generate a tailored ATS-friendly resume.

ATS Optimization
As a user, I want the system to optimize my resume keywords so that my resume performs better in ATS systems.

Cover Letter
As a user, I want to generate a professional cover letter automatically so that I do not need to write one manually for every application.

Cold Email
As a user, I want to generate concise cold emails so that I can quickly reach out to founders and recruiters.

PDF Download
As a user, I want to download my resume as PDF so that I can immediately apply for jobs.

Fixed Formatting
As a user, I want all resumes to maintain a professional single-page structure so that formatting remains consistent and ATS-friendly.

10. Out of Scope (V1)
The following will NOT be included in Version 1:
user authentication
signup/login
payment integration
database storage
resume upload parsing
LinkedIn scraping
job auto-fetching
AI interview preparation
multi-page resumes
drag-and-drop resume builder
collaborative editing
image-based resume designs
recruiter dashboards
analytics dashboard
public resume links

11. Technical Requirements
Backend
FastAPI
Pydantic
Jinja2 Templates

Frontend
HTML
CSS
JavaScript
Optional React later

PDF Generation
WeasyPrint
 or
wkhtmltopdf

AI Layer
OpenAI API
OpenRouter
Gemini API fallback

12. Functional Workflow
Step 1
User pastes job description.

Step 2
System analyzes job description.

Step 3
User pastes current resume.

Step 4
AI generates:
optimized resume content
ATS score
cover letter
cold email

Step 5
Backend injects generated content into fixed HTML template.

Step 6
HTML converts to PDF.

Step 7
User downloads final files.

13. Non-Functional Requirements
Performance
Resume generation under 60 seconds
Full workflow under 5 minutes

Reliability
Consistent formatting
Stable PDF generation

Simplicity
Minimal UI
No unnecessary steps

ATS Compatibility
Avoid tables/icons/graphics
Single-column layout
Semantic headings

14. Success Metrics
The product is considered successful if:
User Efficiency
Users can generate:
resume
cover letter
cold email
within 5 minutes.

Resume Quality
Generated resumes:
remain single-page
maintain formatting consistency
improve ATS keyword matching

User Satisfaction
Users feel the app:
saves time
reduces repetitive ChatGPT usage
simplifies job applications

Technical Success
PDF generation succeeds consistently
API response time remains acceptable
formatting remains stable across outputs

15. Future Vision
Potential future direction:
AI-powered job application assistant
auto-generated recruiter outreach
AI interview preparation
job match scoring
saved resume library
browser extension for LinkedIn/Wellfound
SaaS productization

