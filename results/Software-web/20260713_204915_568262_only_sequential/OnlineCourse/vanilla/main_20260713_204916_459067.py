import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import essential_modules
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
# 20260713_204916_459067/main_20260713_204916_459067.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the 'OnlineCourse' web application requirements and produce a comprehensive design_spec.md detailing pages, routes, elements, navigation, and data storage.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md covering all pages, elements, functionality, and data file specs; \"\n        \"only after completion, WebArchitect reads requirements_analysis.md and produces design_spec.md detailing Flask app routes, \"\n        \"template structure, data storage contracts, and UI element IDs.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in software requirements documentation for web applications.\n\nYour goal is to extract detailed, precise, and structured requirements for each page, UI elements, navigation flows, and data file formats, producing a complete requirements_analysis.md.\n\nTask Details:\n- Read the full user_task_description input artifact from CONTEXT\n- Extract all page titles, exact element IDs, UI components descriptions, navigation button mappings\n- Specify all functionality requirements for interactive elements\n- Detail data file formats with field order, delimiters, and example rows\n- Create requirements_analysis.md covering all above aspects exhaustively\n\nRequirements Documentation Instructions:\n1. **Pages and Elements**:\n   - List each page by its name and page title\n   - Enumerate all UI elements with exact IDs, types, and roles\n   - Specify which elements are repeated with patterns (e.g., buttons with dynamic IDs)\n\n2. **Navigation Flow**:\n   - Map buttons and links to destination pages or routes explicitly\n   - Describe dynamic navigation elements using placeholders (e.g., {course_id})\n\n3. **Functional Behavior**:\n   - Document all provided interactivity and data update behaviors tied to UI\n   - Clarify data update rules such as enrollment creation, progress updates, submission recording, certificate issuance\n\n4. **Data Schemas**:\n   - Provide comprehensive file formats for all data text files\n   - Include field names, delimiters (pipe |), and realistic example entries\n   - Specify relationships between files where relevant\n\nCRITICAL SUCCESS CRITERIA:\n- The document enables any architect to design routes, templates, and data interface without missing details\n- All element IDs are precise and consistent\n- All functionality steps are fully represented in the requirements\n- Output saved exclusively using write_text_file tool as requirements_analysis.md\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application route and template design.\n\nYour goal is to convert the detailed requirements_analysis.md into a precise, complete design_spec.md that fully specifies Flask routes, HTTP methods, template file layouts, UI element IDs, page rendering contexts, and data storage contracts.\n\nTask Details:\n- Read requirements_analysis.md input artifact fully\n- Define all Flask routes with URL patterns, HTTP methods (GET/POST), and associated template files\n- Specify precise template filenames and folder structure\n- List ALL UI element IDs exactly as required for each page template\n- State page rendering contracts including context variable names and types (list, dict, str, int)\n- Fully detail data file schemas located in data/ directory with exact field order, pipe delimiters, and example data\n- Include navigation mappings linking buttons to Flask route endpoints including dynamic parameter usage\n\nDesign Specification Instructions:\n1. **Flask Routes**:\n   - Build a route table specifying route, function name, HTTP method, template filename, and template context variables\n   - Use function names matching page purposes, snake_case naming convention\n   - The root route '/' redirects to the dashboard page route\n\n2. **Templates and UI Elements**:\n   - Specify each template with exact filename under templates/ folder\n   - Include all required element IDs verbatim\n   - Define context variables passed to each template with structured types and sample structures where applicable\n\n3. **Data Storage Schemas**:\n   - For each data file in data/, specify filename, exact pipe-delimited field order, purpose, and 2-3 example rows\n   - Align data file schemas to requirements_analysis.md definitions exactly\n\nCRITICAL SUCCESS CRITERIA:\n- The design_spec.md enables implementers to develop backend and frontend without ambiguity\n- All routing, template, and data details must be precise and consistent\n- Use write_text_file tool explicitly to save design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Validate that requirements_analysis.md fully captures all user requirements including page titles, element IDs, navigation, \"\n                \"functionality details, and data file schemas before architecture creation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the 'OnlineCourse' web application as a Flask app.py and templates/*.html based on design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes app_draft.py and all templates_draft/*.html files using design_spec.md specifications; \"\n        \"upon completion, IntegrationEngineer converts drafts to final app.py and templates/*.html ensuring all routes, elements, \"\n        \"and data persistence with local text files per design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.\n\nYour goal is to create initial draft implementations of the Flask backend and all HTML templates for the OnlineCourse application.\n\nTask Details:\n- Read design_spec.md thoroughly for all backend route and logic specifications, as well as frontend page titles, element IDs, and UI structure\n- Implement all Flask routes and related logic supporting user authentication, course browsing, enrollment, assignment submission, progress tracking, certificate generation\n- Create draft templates_draft/*.html with exact page titles and element IDs matching design_spec.md\n- Focus only on drafting the core functionalities and UI layouts as per specs\n- Output app_draft.py and templates_draft/*.html with consistent naming and structure\n\nImplementation Guidelines:\n1. **Backend Draft (app_draft.py)**:\n   - Implement routes using Flask with names and HTTP methods specified in design_spec.md\n   - Implement data loading and saving using local text files as defined\n   - Support user session management if specified\n   - Include stubs or minimal implementations for complex features if needed, to be refined later\n\n2. **Frontend Draft (templates_draft/*.html)**:\n   - Use Jinja2 templating syntax consistent with Flask\n   - Implement pages with all mandatory element IDs exactly matching design_spec.md\n   - Include placeholders for dynamic content consistent with backend context variables\n   - Use correct page titles and semantic HTML structure\n\n3. **Consistency and Completeness**:\n   - Ensure element IDs, route names, and variable names are consistent between backend and frontend drafts\n   - Use draft-specific directories and filenames as stated (templates_draft/*.html, app_draft.py)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- All element IDs and page titles must match design_spec.md exactly\n- Flask route implementations must align with design_spec.md logical functionality\n- Draft incomplete features with clear placeholders for later refinement\n- Avoid final naming or file paths that should only appear in final integration\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web applications and template integration.\n\nYour goal is to produce the final integrated version of the OnlineCourse application backend and frontend by refining and combining drafts.\n\nTask Details:\n- Read design_spec.md, app_draft.py, and templates_draft/*.html to understand final requirements and draft implementations\n- Create final app.py implementing all specified routes, logic, and data persistence precisely as per design_spec.md\n- Convert templates_draft/*.html into final templates/*.html with correct paths and removing draft-specific references\n- Ensure the integration supports local text file storage and all user interactions, navigation flows, and UI elements function correctly\n- Address any inconsistencies and discrepancies found between drafts and design spec\n\nIntegration and Refinement Guidelines:\n1. **Backend Finalization**:\n   - Merge draft backend code into a clean, runnable app.py\n   - Implement or refine all route handlers for full functionality\n   - Ensure file I/O matches design_spec.md data formats exactly\n   - Remove draft placeholders and incomplete stubs\n\n2. **Frontend Finalization**:\n   - Rename all templates to templates/*.html without draft subfolder\n   - Verify and enforce that all element IDs and page titles precisely match design_spec.md\n   - Ensure proper Jinja2 syntax and complete UI features are present\n   - Remove any draft-specific code or comments\n\n3. **Testing and Validation**:\n   - Verify routing and navigation across all pages\n   - Validate data persistence with local text files\n   - Confirm all user actions (enrollment, submission, progress tracking, certificates) operate as intended\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html files\n- Final implemented code and templates must fully comply with design_spec.md\n- Remove all draft references from final files\n- Deliver stable, runnable Flask application with complete functionality\n- Preserve all element IDs and page titles exactly as specified\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Check that app_draft.py and templates_draft/*.html correctly implement all design_spec.md requested routes, templates, UI elements, \"\n                \"and data persistence before producing final app.py and templates/*.html.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and verify the final app.py and templates/*.html for syntax, runtime correctness, and requirement conformance.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator runs syntax and runtime validation on app.py, checks templates/*.html for all required elements and page titles, \"\n        \"and produces validation_report.md; after validation, SequentialFixer applies fixes and creates the final validated app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in web application validation with expertise in Python Flask apps.\n\nYour goal is to rigorously validate the final backend and frontend implementations to ensure syntax, runtime correctness, and full UI requirement compliance.\n\nTask Details:\n- Read design_spec.md for complete specification reference\n- Validate app.py for syntax errors and runtime correctness covering all Flask routes\n- Inspect templates/*.html for presence of all required element IDs, correct page titles, and adherence to UI structure\n- Conduct sample navigation tests and validate data persistence in expected files\n- Produce a detailed validation_report.md describing all discovered issues and their context\n\nValidation Procedures:\n1. **Backend Validation**\n   - Use validate_python_file tool to perform syntax and runtime checks on app.py\n   - Execute key Flask routes to test functionality and data flow\n   - Verify context variables passed to templates conform to design_spec.md\n\n2. **Frontend Validation**\n   - Parse all templates/*.html files to verify presence of required element IDs exactly as specified\n   - Check correct page titles in both <title> and <h1> tags\n   - Validate dynamic IDs and repeated elements follow specification patterns\n   - Confirm navigation buttons link correctly according to design_spec.md\n\n3. **Functional Testing**\n   - Perform sample interactions including enrollment, assignment submission, course progress update, and certificate generation\n   - Verify updates are reflected correctly in respective data files (e.g., enrollments.txt, submissions.txt, certificates.txt)\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools for backend validation\n- MUST use write_text_file tool to produce validation_report.md\n- Report must have clear descriptions of errors, warnings, and suggestions\n- Maintain strict adherence to design_spec.md for reference\n- Focus exclusively on provided input files, no assumptions outside specification\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Full Stack Developer specializing in iterative refinement and bug fixing for Flask web applications.\n\nYour goal is to address all issues recorded in validation_report.md, revising app.py and templates/*.html to meet full functional and UI requirements, ensuring the final application passes all validation criteria.\n\nTask Details:\n- Read validation_report.md for all identified issues and required corrections\n- Use design_spec.md as a reference to validate correctness of fixes\n- Modify app.py to correct any syntax, runtime, or functional defects identified\n- Update templates/*.html to fix missing element IDs, incorrect page titles, navigation, and UI components as per specifications\n- Ensure all corrections maintain overall application integrity and align with user requirements\n\nFixing Instructions:\n1. **Backend Corrections**\n   - Resolve all syntax and runtime errors from validation_report.md\n   - Adjust route implementations and data handling to comply with design_spec.md\n   - Maintain clean, well-commented, and readable code\n\n2. **Frontend Corrections**\n   - Add missing or incorrect element IDs exactly as specified\n   - Correct page titles in <title> and <h1> tags for each template\n   - Fix navigation links and button identifiers to match specification\n   - Confirm dynamic IDs and repeated elements match naming conventions and structure\n\n3. **Final Verification**\n   - After corrections, ensure consistency between backend and frontend components\n   - Prepare final versions ready for full validation cycles\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool for all output files\n- Final app.py and templates/*.html MUST fully conform to design_spec.md\n- All fixes MUST resolve issues from validation_report.md completely\n- Maintain positive, specification-driven improvements without introducing new features\n- Do NOT include any validation markers or comments in output files\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Verify validation_report.md accurately documents all issues with app.py and templates/*.html, and that fixes applied resolve them.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Confirm that the final app.py and templates/*.html fully implement all user requirements as captured in requirements_analysis.md \"\n                \"and design_spec.md with no regressions.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'OnlineCourse' Web Application

## 1. Objective
Develop a comprehensive web application named 'OnlineCourse' using Python, with data managed through local text files. The application enables users to browse and enroll in courses, submit assignments, track progress, and receive certificates. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'OnlineCourse' application is Python.

## 3. Page Design

The 'OnlineCourse' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Learning Dashboard
- **Overview**: Main hub displaying enrolled courses and progress.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying user's name.
  - **ID: enrolled-courses** - Type: Div - Display of currently enrolled courses.
  - **ID: browse-courses-button** - Type: Button - Navigate to course catalog.
  - **ID: my-courses-button** - Type: Button - Navigate to my courses page.

### 2. Course Catalog Page
- **Page Title**: Available Courses
- **Overview**: Browse all available courses.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search courses.
  - **ID: course-grid** - Type: Div - Grid display of course cards.
  - **ID: view-course-button-{course_id}** - Type: Button - View course details. (반복 요소)
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

### 3. Course Details Page
- **Page Title**: Course Details
- **Overview**: Detailed information about a course including syllabus and enrollment option.
- **Elements**:
  - **ID: course-details-page** - Type: Div - Container for the course details page.
  - **ID: course-title** - Type: H1 - Display of course title.
  - **ID: course-description** - Type: Div - Full description of course content.
  - **ID: enroll-button** - Type: Button - Button to enroll in the course.
  - **ID: back-to-catalog** - Type: Button - Button to navigate back to course catalog.
- **Functionality**:
  - Enroll button creates entry in enrollments.txt with 0% initial progress
  - If already enrolled, button shows "Already Enrolled" and is disabled
  - Enrollment date is recorded as current date

### 4. My Courses Page
- **Page Title**: My Courses
- **Overview**: Display enrolled courses and progress.
- **Elements**:
  - **ID: my-courses-page** - Type: Div - Container for the my courses page.
  - **ID: courses-list** - Type: Div - List of enrolled courses with progress.
  - **ID: continue-learning-button-{course_id}** - Type: Button - Continue learning a course. (반복 요소)
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

### 5. Course Learning Page
- **Page Title**: Course Learning
- **Overview**: View course content and lessons with progress tracking.
- **Elements**:
  - **ID: learning-page** - Type: Div - Container for the course learning page.
  - **ID: lessons-list** - Type: Div - List of all lessons in the course.
  - **ID: lesson-content** - Type: Div - Display of current lesson materials.
  - **ID: mark-complete-button** - Type: Button - Button to mark current lesson as completed.
  - **ID: back-to-my-courses** - Type: Button - Button to navigate back to enrolled courses.
- **Functionality**:
  - Progress is calculated as (completed lessons / total lessons) × 100
  - Marking lesson complete updates enrollments.txt progress field
  - Course completion (100% progress) automatically generates certificate
  - Lessons must be completed in sequence

### 6. My Assignments Page
- **Page Title**: My Assignments
- **Overview**: View and submit assignments.
- **Elements**:
  - **ID: assignments-page** - Type: Div - Container for assignments page.
  - **ID: assignments-table** - Type: Table - Table displaying all assignments.
  - **ID: submit-assignment-button-{assignment_id}** - Type: Button - Submit a pending assignment. (반복 요소)
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

### 7. Submit Assignment Page
- **Page Title**: Submit Assignment
- **Overview**: Submit assignment work with text responses.
- **Elements**:
  - **ID: submit-page** - Type: Div - Container for the assignment submission page.
  - **ID: assignment-info** - Type: Div - Display of assignment title and description.
  - **ID: submission-text** - Type: Textarea - Field to input text response.
  - **ID: submit-button** - Type: Button - Button to submit the assignment.
  - **ID: back-to-assignments** - Type: Button - Button to navigate back to assignments list.
- **Functionality**:
  - Submission creates entry in submissions.txt with status "Submitted"
  - Submit date is recorded for late submission tracking
  - Confirmation message displays after successful submission

### 8. Certificates Page
- **Page Title**: My Certificates
- **Overview**: View earned course completion certificates.
- **Elements**:
  - **ID: certificates-page** - Type: Div - Container for the certificates page.
  - **ID: certificates-grid** - Type: Div - Grid display of certificate cards.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.
- **Functionality**:
  - Certificates are automatically generated when course progress reaches 100%
  - Certificate entry is added to certificates.txt with current date
  - Only completed courses appear in the grid

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: View and edit profile.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for profile page.
  - **ID: profile-email** - Type: Input - Email input field.
  - **ID: profile-fullname** - Type: Input - Full name input field.
  - **ID: update-profile-button** - Type: Button - Save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

## 4. Data Storage

The 'OnlineCourse' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**: `username|email|fullname`
- **Example Data**:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### 2. Courses Data
- **File Name**: `courses.txt`
- **Data Format**: `course_id|title|description|category|level|duration|status`
- **Example Data**:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### 3. Enrollments Data
- **File Name**: `enrollments.txt`
- **Data Format**: `enrollment_id|username|course_id|enrollment_date|progress|status`
- **Example Data**:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### 4. Assignments Data
- **File Name**: `assignments.txt`
- **Data Format**: `assignment_id|course_id|title|description|due_date|max_points`
- **Example Data**:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### 5. Submissions Data
- **File Name**: `submissions.txt`
- **Data Format**: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- **Example Data**:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### 6. Certificates Data
- **File Name**: `certificates.txt`
- **Data Format**: `certificate_id|username|course_id|issue_date`
- **Example Data**:
  ```
  1|jane|1|2024-11-22
  ```
"""

CONTEXT = {
    "_metrics": {},  # Metrics tracking for all agents
    "user_task_description": [{
        "timestamp": time.time(),
        "agent_name": "user",
        "content": user_task
    }]
}

AGENT_PROFILES = {
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in software requirements documentation for web applications.

Your goal is to extract detailed, precise, and structured requirements for each page, UI elements, navigation flows, and data file formats, producing a complete requirements_analysis.md.

Task Details:
- Read the full user_task_description input artifact from CONTEXT
- Extract all page titles, exact element IDs, UI components descriptions, navigation button mappings
- Specify all functionality requirements for interactive elements
- Detail data file formats with field order, delimiters, and example rows
- Create requirements_analysis.md covering all above aspects exhaustively

Requirements Documentation Instructions:
1. **Pages and Elements**:
   - List each page by its name and page title
   - Enumerate all UI elements with exact IDs, types, and roles
   - Specify which elements are repeated with patterns (e.g., buttons with dynamic IDs)

2. **Navigation Flow**:
   - Map buttons and links to destination pages or routes explicitly
   - Describe dynamic navigation elements using placeholders (e.g., {course_id})

3. **Functional Behavior**:
   - Document all provided interactivity and data update behaviors tied to UI
   - Clarify data update rules such as enrollment creation, progress updates, submission recording, certificate issuance

4. **Data Schemas**:
   - Provide comprehensive file formats for all data text files
   - Include field names, delimiters (pipe |), and realistic example entries
   - Specify relationships between files where relevant

CRITICAL SUCCESS CRITERIA:
- The document enables any architect to design routes, templates, and data interface without missing details
- All element IDs are precise and consistent
- All functionality steps are fully represented in the requirements
- Output saved exclusively using write_text_file tool as requirements_analysis.md

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application route and template design.

Your goal is to convert the detailed requirements_analysis.md into a precise, complete design_spec.md that fully specifies Flask routes, HTTP methods, template file layouts, UI element IDs, page rendering contexts, and data storage contracts.

Task Details:
- Read requirements_analysis.md input artifact fully
- Define all Flask routes with URL patterns, HTTP methods (GET/POST), and associated template files
- Specify precise template filenames and folder structure
- List ALL UI element IDs exactly as required for each page template
- State page rendering contracts including context variable names and types (list, dict, str, int)
- Fully detail data file schemas located in data/ directory with exact field order, pipe delimiters, and example data
- Include navigation mappings linking buttons to Flask route endpoints including dynamic parameter usage

Design Specification Instructions:
1. **Flask Routes**:
   - Build a route table specifying route, function name, HTTP method, template filename, and template context variables
   - Use function names matching page purposes, snake_case naming convention
   - The root route '/' redirects to the dashboard page route

2. **Templates and UI Elements**:
   - Specify each template with exact filename under templates/ folder
   - Include all required element IDs verbatim
   - Define context variables passed to each template with structured types and sample structures where applicable

3. **Data Storage Schemas**:
   - For each data file in data/, specify filename, exact pipe-delimited field order, purpose, and 2-3 example rows
   - Align data file schemas to requirements_analysis.md definitions exactly

CRITICAL SUCCESS CRITERIA:
- The design_spec.md enables implementers to develop backend and frontend without ambiguity
- All routing, template, and data details must be precise and consistent
- Use write_text_file tool explicitly to save design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.

Your goal is to create initial draft implementations of the Flask backend and all HTML templates for the OnlineCourse application.

Task Details:
- Read design_spec.md thoroughly for all backend route and logic specifications, as well as frontend page titles, element IDs, and UI structure
- Implement all Flask routes and related logic supporting user authentication, course browsing, enrollment, assignment submission, progress tracking, certificate generation
- Create draft templates_draft/*.html with exact page titles and element IDs matching design_spec.md
- Focus only on drafting the core functionalities and UI layouts as per specs
- Output app_draft.py and templates_draft/*.html with consistent naming and structure

Implementation Guidelines:
1. **Backend Draft (app_draft.py)**:
   - Implement routes using Flask with names and HTTP methods specified in design_spec.md
   - Implement data loading and saving using local text files as defined
   - Support user session management if specified
   - Include stubs or minimal implementations for complex features if needed, to be refined later

2. **Frontend Draft (templates_draft/*.html)**:
   - Use Jinja2 templating syntax consistent with Flask
   - Implement pages with all mandatory element IDs exactly matching design_spec.md
   - Include placeholders for dynamic content consistent with backend context variables
   - Use correct page titles and semantic HTML structure

3. **Consistency and Completeness**:
   - Ensure element IDs, route names, and variable names are consistent between backend and frontend drafts
   - Use draft-specific directories and filenames as stated (templates_draft/*.html, app_draft.py)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- All element IDs and page titles must match design_spec.md exactly
- Flask route implementations must align with design_spec.md logical functionality
- Draft incomplete features with clear placeholders for later refinement
- Avoid final naming or file paths that should only appear in final integration

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web applications and template integration.

Your goal is to produce the final integrated version of the OnlineCourse application backend and frontend by refining and combining drafts.

Task Details:
- Read design_spec.md, app_draft.py, and templates_draft/*.html to understand final requirements and draft implementations
- Create final app.py implementing all specified routes, logic, and data persistence precisely as per design_spec.md
- Convert templates_draft/*.html into final templates/*.html with correct paths and removing draft-specific references
- Ensure the integration supports local text file storage and all user interactions, navigation flows, and UI elements function correctly
- Address any inconsistencies and discrepancies found between drafts and design spec

Integration and Refinement Guidelines:
1. **Backend Finalization**:
   - Merge draft backend code into a clean, runnable app.py
   - Implement or refine all route handlers for full functionality
   - Ensure file I/O matches design_spec.md data formats exactly
   - Remove draft placeholders and incomplete stubs

2. **Frontend Finalization**:
   - Rename all templates to templates/*.html without draft subfolder
   - Verify and enforce that all element IDs and page titles precisely match design_spec.md
   - Ensure proper Jinja2 syntax and complete UI features are present
   - Remove any draft-specific code or comments

3. **Testing and Validation**:
   - Verify routing and navigation across all pages
   - Validate data persistence with local text files
   - Confirm all user actions (enrollment, submission, progress tracking, certificates) operate as intended

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Final implemented code and templates must fully comply with design_spec.md
- Remove all draft references from final files
- Deliver stable, runnable Flask application with complete functionality
- Preserve all element IDs and page titles exactly as specified

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in web application validation with expertise in Python Flask apps.

Your goal is to rigorously validate the final backend and frontend implementations to ensure syntax, runtime correctness, and full UI requirement compliance.

Task Details:
- Read design_spec.md for complete specification reference
- Validate app.py for syntax errors and runtime correctness covering all Flask routes
- Inspect templates/*.html for presence of all required element IDs, correct page titles, and adherence to UI structure
- Conduct sample navigation tests and validate data persistence in expected files
- Produce a detailed validation_report.md describing all discovered issues and their context

Validation Procedures:
1. **Backend Validation**
   - Use validate_python_file tool to perform syntax and runtime checks on app.py
   - Execute key Flask routes to test functionality and data flow
   - Verify context variables passed to templates conform to design_spec.md

2. **Frontend Validation**
   - Parse all templates/*.html files to verify presence of required element IDs exactly as specified
   - Check correct page titles in both <title> and <h1> tags
   - Validate dynamic IDs and repeated elements follow specification patterns
   - Confirm navigation buttons link correctly according to design_spec.md

3. **Functional Testing**
   - Perform sample interactions including enrollment, assignment submission, course progress update, and certificate generation
   - Verify updates are reflected correctly in respective data files (e.g., enrollments.txt, submissions.txt, certificates.txt)

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for backend validation
- MUST use write_text_file tool to produce validation_report.md
- Report must have clear descriptions of errors, warnings, and suggestions
- Maintain strict adherence to design_spec.md for reference
- Focus exclusively on provided input files, no assumptions outside specification

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Full Stack Developer specializing in iterative refinement and bug fixing for Flask web applications.

Your goal is to address all issues recorded in validation_report.md, revising app.py and templates/*.html to meet full functional and UI requirements, ensuring the final application passes all validation criteria.

Task Details:
- Read validation_report.md for all identified issues and required corrections
- Use design_spec.md as a reference to validate correctness of fixes
- Modify app.py to correct any syntax, runtime, or functional defects identified
- Update templates/*.html to fix missing element IDs, incorrect page titles, navigation, and UI components as per specifications
- Ensure all corrections maintain overall application integrity and align with user requirements

Fixing Instructions:
1. **Backend Corrections**
   - Resolve all syntax and runtime errors from validation_report.md
   - Adjust route implementations and data handling to comply with design_spec.md
   - Maintain clean, well-commented, and readable code

2. **Frontend Corrections**
   - Add missing or incorrect element IDs exactly as specified
   - Correct page titles in <title> and <h1> tags for each template
   - Fix navigation links and button identifiers to match specification
   - Confirm dynamic IDs and repeated elements match naming conventions and structure

3. **Final Verification**
   - After corrections, ensure consistency between backend and frontend components
   - Prepare final versions ready for full validation cycles

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool for all output files
- Final app.py and templates/*.html MUST fully conform to design_spec.md
- All fixes MUST resolve issues from validation_report.md completely
- Maintain positive, specification-driven improvements without introducing new features
- Do NOT include any validation markers or comments in output files

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Validate that requirements_analysis.md fully captures all user requirements including page titles, element IDs, navigation, "
                "functionality details, and data file schemas before architecture creation.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Check that app_draft.py and templates_draft/*.html correctly implement all design_spec.md requested routes, templates, UI elements, "
                "and data persistence before producing final app.py and templates/*.html.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Verify validation_report.md accurately documents all issues with app.py and templates/*.html, and that fixes applied resolve them.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Confirm that the final app.py and templates/*.html fully implement all user requirements as captured in requirements_analysis.md "
                "and design_spec.md with no regressions.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Create agents
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution flow
    # Step 1: RequirementsAnalyst analyzes user_task_description and creates requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze the full user_task_description and produce detailed requirements_analysis.md including pages, UI elements with exact IDs, navigation flows, functionality behaviors, and data schemas.")

    # Step 2: WebArchitect reads requirements_analysis.md and creates design_spec.md specifying Flask routes, templates, UI elements, navigation and data contracts
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read requirements_analysis.md content below and produce design_spec.md specifying precise Flask routes, HTTP methods, template file structure, UI element IDs, context variables, navigation mappings, and data storage schemas.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Create agents
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Sequential execution
    await execute(DraftEngineer, "Read design_spec.md and create initial draft implementations: app_draft.py and templates_draft/*.html with core backend routes, logic, and frontend UI layouts matching all element IDs and page titles exactly. Save drafts with placeholders for incomplete features.")
    
    # Read drafts for integration
    app_draft_code, templates_draft_content = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    try:
        # Assuming multiple draft templates - reading all files content concatenated for context injection
        import glob
        content_list = []
        for filename in glob.glob("templates_draft/*.html"):
            with open(filename, 'r') as f:
                content_list.append(f.read())
        templates_draft_content = "\n\n".join(content_list)
    except:
        pass

    # Inject drafts content for integration
    await execute(IntegrationEngineer,
                  f"Using design_spec.md, app_draft.py, and templates_draft/*.html drafts, create final app.py and templates/*.html with complete route implementations, full functionality, and removal of draft placeholders and paths. Ensure all element IDs and page titles match design_spec.md precisely."
                  f"\n\n=== app_draft.py ===\n{app_draft_code}\n\n=== templates_draft/*.html ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential Flow Execution: Validate then fix
    await execute(WebValidator,
                  "Validate app.py using validate_python_file and execute_python_code tools, inspect templates/*.html for required elements, page titles and UI structure, "
                  "perform functional tests including enrollment, assignment submission, course progress update, certificate generation, "
                  "and produce detailed validation_report.md with all findings and suggestions.")

    # Read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(SequentialFixer,
                  f"Read validation_report.md for issues to fix. Update app.py and all templates/*.html to correct all reported errors, "
                  f"ensure full compliance with design_spec.md, maintain application integrity, and prepare final validated files.\n\n"
                  f"=== Validation Report ===\n{validation_report_content}")
# Phase3_End

# Orchestrate_Start

async def orchestrate():
    """Execute the complete multi-agent workflow in steps."""
    import time
    import json
    from pathlib import Path
    from essential_modules import aggregate_task_metrics
    orchestrate_start_time = time.time()

    step1 = [
        design_specification_phase()
    ]
    step2 = [
        implementation_phase()
    ]
    step3 = [
        verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    cc = None
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)
        cc = chaos_controller

    # Save metrics to JSON (with resilience_metrics if chaos enabled)
    task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
    metrics_path = Path("metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(task_metrics, f, indent=2)
    print(f" Metrics saved to: {{metrics_path.resolve()}}")
# Orchestrate_End

if __name__ == "__main__":
    import sys
    import signal
    from datetime import datetime
    from pathlib import Path
    import json

    # Signal handler for graceful shutdown on timeout
    def save_metrics_on_signal(signum, frame):
        print(f"\n  Received signal {signum}, saving metrics and reports before exit...")

        # Save chaos reports if chaos_controller exists (chaos scenarios only)
        try:
            if 'chaos_controller' in globals():
                print("Generating chaos report on timeout...")
                chaos_controller.print_report(context=CONTEXT, save_to_file=True)
                print("Chaos reports saved successfully")
        except Exception as e:
            print(f"  Error saving chaos report: {e}")
            import traceback
            traceback.print_exc()

        # Save metrics (independent of chaos report success/failure)
        try:
            # Pass chaos_controller if available for resilience_metrics
            cc = chaos_controller if 'chaos_controller' in globals() else None
            task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
            import traceback
            traceback.print_exc()

        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")
    log_file.flush()

    # Create a Tee class to write to both stdout and file
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()

    # Redirect stdout and stderr to both console and log file
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = Tee(original_stdout, log_file)
    sys.stderr = Tee(original_stderr, log_file)

    try:
        # Run orchestration
        asyncio.run(orchestrate())
    finally:
        # Restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        log_file.close()
