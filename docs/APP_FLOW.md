App Flow — Navigation & User Journey Map
1. Product Navigation Philosophy
The application should feel:
fast
minimal
distraction-free
workflow-focused
This is NOT a dashboard-heavy SaaS.
The user should:
paste JD
paste resume
generate outputs
download PDF
apply for jobs
Everything should happen in a single streamlined workflow.

2. Application Structure
Application Type
Single-page workflow application with lightweight navigation.

Navigation Style
Primary Navigation
Top navigation bar only.
No:
sidebar
nested menus
complex dashboard

Recommended Navigation Items
[Logo]

Resume Builder
Cover Letter
Cold Email
ATS Score
Optional:
Reset Session

3. Entry Point
Landing Route
/

First Screen User Sees
Homepage / Resume Workflow Page
This page contains:
app title
tagline
job description textarea
resume textarea
action buttons
This is the main operational page.
No onboarding screens.
No login screens.

4. Screens / Pages
Screen 1 — Homepage / Main Workspace
Route
/

Purpose
Primary workspace where users:
paste job description
paste resume
generate outputs

Components
Header
Contains:
app logo/name
tagline

Job Description Section
Components:
large textarea
character counter
“Analyze JD” button

Resume Section
Components:
resume textarea
word count
“Generate Resume” button

Output Actions
Buttons:
Generate ATS Resume
Generate Cover Letter
Generate Cold Email
Generate ATS Score

Download Section
Buttons:
Download PDF
Copy Resume
Copy Cover Letter
Copy Cold Email

Screen 2 — Generated Resume Preview
Route
/resume-preview

Purpose
Displays:
ATS-optimized resume
final HTML rendering
PDF preview

Layout
Left Side
Generated content.
Right Side
Actions:
download PDF
regenerate
edit text manually

Screen 3 — Cover Letter Output
Route
/cover-letter

Purpose
Displays generated cover letter.

Features
editable textarea
copy button
regenerate button

Screen 4 — Cold Email Output
Route
/cold-email

Purpose
Displays generated cold email.

Features
editable text
copy button
regenerate button

Screen 5 — ATS Analysis Page
Route
/ats-analysis

Purpose
Shows:
ATS score
matched keywords
missing keywords
optimization suggestions

Example
ATS Score: 84/100

Matched Skills:
✔ FastAPI
✔ PostgreSQL
✔ Docker

Missing Keywords:
✘ AWS Lambda
✘ CI/CD

5. Navigation Structure
Primary Navigation Flow
Homepage
  ↓
Generate Resume
  ↓
Resume Preview
  ↓
Generate Cover Letter / Email
  ↓
Download PDF

Navigation Behavior
Back Navigation
Users should always be able to:
return to homepage
edit JD/resume
regenerate outputs

State Persistence
During session only:
preserve text inputs
preserve generated outputs
Use:
localStorage
No database needed.

6. Key User Journeys
Journey 1 — Resume Generation (Primary Flow)
Step 1
User lands on homepage.

Step 2
User pastes:
job description
existing resume

Step 3
Clicks:
Generate ATS Resume

Step 4
Frontend sends request to FastAPI backend.

Step 5
Backend:
analyzes JD
extracts keywords
calls OpenAI
generates optimized content

Step 6
Backend injects content into fixed HTML template.

Step 7
Frontend displays:
resume preview
ATS score

Step 8
User downloads PDF.

Journey 2 — Cover Letter Generation
Step 1
User already generated resume.

Step 2
Clicks:
Generate Cover Letter

Step 3
Backend generates cover letter using:
optimized resume
JD

Step 4
User reviews/edit/copies cover letter.

Journey 3 — Cold Email Generation
Step 1
User clicks:
Generate Cold Email

Step 2
Backend generates concise recruiter/founder email.

Step 3
User:
copies email
pastes into Gmail/LinkedIn

7. Loading States
Resume Generation Loading
While generating:
Generating ATS Resume...
Analyzing keywords...
Optimizing bullet points...
Building PDF...
Use:
skeleton loaders
progress indicators

Cover Letter Loading
Generating cover letter...

Cold Email Loading
Generating cold email...

Important UX Rule
Buttons should:
disable during generation
prevent duplicate requests

8. Empty States
Empty Job Description
If JD textarea empty:
Please paste a job description first.

Empty Resume
If resume textarea empty:
Please paste your resume text first.

No Generated Resume
If user opens preview without generation:
No resume generated yet.

9. Error States
AI API Failure
Message:
Something went wrong while generating content.
Please try again.

PDF Generation Failure
Message:
Unable to generate PDF right now.

Rate Limit Error
Message:
Too many requests. Please wait a moment and try again.

Timeout Error
Message:
Generation is taking longer than expected.

Invalid Resume Length
Message:
Resume content is too short.

Invalid JD Length
Message:
Job description appears incomplete.

10. Modal / Drawer / Overlay Interactions
Regenerate Confirmation Modal
When clicking:
Regenerate Resume
Show modal:
This will replace the current generated resume.
Continue?
Buttons:
Cancel
Continue

PDF Download Success Toast
Resume PDF downloaded successfully.

Copy Success Toast
Copied to clipboard.

ATS Tips Drawer (Optional)
Right-side drawer:
missing keywords
optimization tips
suggestions

11. Redirect Logic
Generate Resume
Action
Click:
Generate ATS Resume
Redirect
/resume-preview

Generate Cover Letter
Redirect
/cover-letter

Generate Cold Email
Redirect
/cold-email

Generate ATS Score
Redirect
/ats-analysis

Invalid Navigation Redirect
If user directly opens:
/resume-preview
without generation:
 redirect back to:
/

12. Session Handling
V1 Session Strategy
Use:
localStorage
Store:
JD text
resume text
generated outputs

Session Expiry
Session clears:
on refresh reset
manual reset
browser storage clear

13. Mobile Responsiveness
Mobile Support
App should support:
laptops
tablets
mobile devices

Mobile Layout
On mobile:
stack sections vertically
full-width textareas
sticky action buttons

14. UX Design Principles
The app should feel:
productivity-focused
instant
lightweight
minimal friction
Avoid:
unnecessary animations
complex onboarding
dashboard clutter
excessive steps

15. Recommended MVP UI Flow
Paste Job Description
       ↓
Paste Resume
       ↓
Generate ATS Resume
       ↓
View ATS Score
       ↓
Generate Cover Letter
       ↓
Generate Cold Email
       ↓
Download PDF
This should ideally happen in:
under 5 minutes

