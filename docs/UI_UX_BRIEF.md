UI/UX Design Brief — Visual & Interaction Design Guide
1. Design Philosophy
Overall Aesthetic Direction
The application should follow a:
Minimal + Professional + Productivity-focused
design language.
The product should feel:
fast
clean
ATS-focused
engineering-oriented
utility-first
This is NOT:
a Dribbble-style creative portfolio app
a flashy SaaS dashboard
a colorful resume designer
The UI should communicate:
“Generate professional job application material quickly.”

2. Visual Style Direction
Primary Style
Design Keywords
minimal
modern
lightweight
structured
corporate
distraction-free

Visual Tone
The interface should feel similar to:
developer tools
productivity apps
AI workflow apps
document editors

Important UX Principle
The resume itself is the hero.
The app UI should not overpower the generated resume.

3. Color Palette
Primary Color
#111827
Dark charcoal/navy.
Used for:
buttons
headings
primary actions

Secondary Color
#374151
Used for:
borders
secondary text
inactive states

Accent Color
#2563EB
Blue accent.
Used for:
links
CTA buttons
active states
highlights

Background Color
#F9FAFB
Light gray background.

Card / Surface Color
#FFFFFF
White surfaces/cards.

Success Color
#16A34A
Used for:
ATS score success
copied state
success messages

Warning Color
#D97706
Used for:
missing keywords
warnings

Error Color
#DC2626
Used for:
failures
API errors
validation states

Text Colors
Primary Text
#111827
Secondary Text
#6B7280

4. Typography
Application UI Typography
Recommended Font
Use:
 Inter Font
Reason:
modern
highly readable
clean developer-tool feel

Heading Sizes
H1
36px
font-weight: 700

H2
28px
font-weight: 600

H3
22px
font-weight: 600

Body Text
15px–16px
font-weight: 400

Resume Typography (VERY IMPORTANT)
YES — your resume settings MUST absolutely be included.
And these settings belong inside:
Resume Rendering Specifications
inside:
TRD
Design System
Resume Template Engine documentation
These are NOT just “design preferences”.
These are:
Hard rendering constraints
for the PDF engine.

Resume Template Specifications (Finalized)
Resume Font
Font Family: Times New Roman

Name
Font Size: 18px
Font Weight: Bold
Text Transform: Uppercase
Alignment: Center

Role / Position Line
Font Size: 14px
Font Weight: Normal
Alignment: Center

Contact Line
Font Size: 10px
Font Weight: Normal
Alignment: Center

Section Headings
Examples:
SUMMARY
TECHNICAL SKILLS
WORK EXPERIENCE
PROJECTS
EDUCATION
Style:
Font Size: 12px
Font Weight: Bold
Text Transform: Uppercase
Border Bottom: Thin Gray Line
Margin Top: Tight

Resume Body Text
Examples:
summary content
bullet points
descriptions
Style:
Font Size: 11px–12px
Font Weight: Normal
Line Height: Compact

Resume Bullet Style
Use:
• standard bullet points
Avoid:
icons
fancy bullets
emojis

Resume Layout Constraints
Margins
Top: 0.1in
Bottom: 0in
Left: 0.3in
Right: 0.3in

Resume Width Rules
The system MUST:
dynamically shrink spacing
prevent overflow
preserve single-page layout

Resume Hard Constraints
Must Always:
remain single-page
remain ATS-friendly
preserve fixed structure
avoid visual design changes

Forbidden Resume Elements
DO NOT USE:
tables
multi-columns
icons
profile pictures
charts
progress bars
colored backgrounds
em dash
decorative elements

5. Component Style
Corners
Use:
Rounded corners (10px–14px)
NOT:
sharp enterprise corners

Buttons
Style:
soft rounded
medium height
bold text
clean shadows

Cards
Style:
Subtle shadow
Thin border
White background
Avoid:
glassmorphism
neumorphism
excessive blur

Inputs / Textareas
Style:
large textareas
comfortable spacing
subtle border
focus glow

Modals
Use:
centered modal
dark overlay
minimal actions

6. Light Mode / Dark Mode
V1 Recommendation
Light Mode ONLY
Reason:
resume readability
PDF consistency
faster implementation
cleaner professional look

Future Enhancement
Dark mode can be added later.
But:
Resume preview should always remain white.

7. Inspiration References
Product Inspiration
The app UI should feel inspired by:
Notion
Linear
Vercel
ChatGPT

Resume Design Inspiration
The generated resume should feel:
traditional
ATS-first
recruiter-friendly
information-dense
compact
Similar to:
high-performing startup engineering resumes

8. Key UI Patterns
Primary Layout Pattern
Use:
Two-section vertical workflow

Workflow Sections
Section 1
Inputs:
JD textarea
resume textarea

Section 2
Outputs:
ATS score
generated resume
cover letter
cold email

Cards
Use cards for:
ATS analysis
generated outputs
keyword suggestions

Modals
Use for:
regenerate confirmation
reset confirmation

Toast Notifications
Use for:
copy success
download success
generation completion

Avoid
DO NOT use:
sidebars
complex tables
analytics dashboards
nested menus

9. Mobile Responsiveness Requirements
Mobile Support
App MUST work properly on:
desktop
tablet
mobile

Mobile Layout Behavior
On smaller screens:
stack vertically
full-width textareas
sticky bottom action buttons

Textareas
Must remain:
easy to scroll
readable
touch-friendly

Resume Preview on Mobile
Use:
zoom support
horizontal scroll if needed

10. Accessibility Considerations
Contrast
All text must meet:
WCAG AA contrast standards

Font Sizes
Avoid:
less than 14px in app UI
Resume PDF exception allowed.

Keyboard Navigation
Support:
tab navigation
enter submission
textarea accessibility

Focus States
Inputs/buttons must have:
visible focus outlines
accessible hover states

Loading Accessibility
Loading indicators should include:
Generating resume...
instead of spinner-only UI.

11. Resume Rendering Engine Rules
Important Architecture Rule
The resume template MUST be:
hardcoded HTML + CSS
AI must NEVER:
generate CSS
generate layout
generate structure
AI only generates:
content
keywords
optimized wording

Rendering Flow
AI JSON Output
       ↓
Inject into HTML Template
       ↓
Render Fixed Resume
       ↓
Generate PDF

12. Final UX Goal
The user experience should feel like:
Paste → Generate → Download → Apply
with:
minimal friction
minimal clicks
professional output
fast workflow
within:
under 5 minutes

