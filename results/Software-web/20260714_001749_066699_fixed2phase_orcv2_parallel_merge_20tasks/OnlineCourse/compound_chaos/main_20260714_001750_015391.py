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
from chaos import ChaosController
# 20260714_001750_015391/main_20260714_001750_015391.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend designs for the 'OnlineCourse' app and produce a merged design specification document.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect specifies Flask routes, data schema, and business logic from the user task description; \"\n        \"FrontendDesignArchitect specifies HTML templates, element IDs, UI structure, and navigation. \"\n        \"DesignMerger reconciles backend_design.md and frontend_design.md into a consistent design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend development and data schema design for Python web applications.\n\nYour goal is to design and specify the backend routes, data file schemas, enrollment and progress tracking logic, and API contracts necessary to implement the 'OnlineCourse' web application.\n\nTask Details:\n- Read user_task_description from CONTEXT for all backend requirements including pages, functionalities, and data storage\n- Produce backend_design.md independently describing all Flask routes, HTTP methods, expected inputs, outputs, and business logic\n- Define exact text file schemas (fields, delimiters, formats, examples) for users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, and certificates.txt\n- Specify logic for enrollment management, progress calculation, assignment submissions, and certificate generation\n- Do not access or rely on frontend_design.md outputs\n\n**Section 1: Flask Routes Specification**\n- List each Flask route with path, HTTP methods, expected request parameters, response format, and behavior\n- Include routes for all nine pages and their interactive features (e.g., enrollment, progress update, submissions)\n- Define redirects, login/session assumptions (if any), and error handling\n\n**Section 2: Data File Schemas**\n- Specify each data file path and exact pipe '|' delimited fields with data types and descriptions\n- Provide example data rows for each file matching the requirements document\n- Include enrollment progress tracking and status fields with format details\n\n**Section 3: Business Logic and API Contracts**\n- Describe enrollment logic: creation, initial progress zero, date recording\n- Detail progress update rules: lessons completion sequence, progress percentage calculation\n- Outline submission and grading data flow\n- Describe certificate generation criteria and data update procedures\n\nCRITICAL SUCCESS CRITERIA:\n- Output is complete and independently sufficient backend_design.md\n- All route and data schema elements strictly derived from user_task_description\n- Use write_text_file tool strictly to save backend_design.md\n- Do not read or assume frontend_design.md details\n- Output artifacts: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and frontend template design for Python web applications.\n\nYour goal is to design the complete frontend HTML templates, element IDs, UI layouts, and navigation flows for the nine pages of the 'OnlineCourse' web application according to the requirements.\n\nTask Details:\n- Read user_task_description from CONTEXT for complete frontend page designs, UI elements, and navigation details\n- Independently produce frontend_design.md describing the HTML template structure, element IDs, page titles, and navigation flow\n- Specify exact element IDs (including repeated elements with parameters) and types for all buttons, divs, inputs, and other controls per page requirements\n- Map navigation links and button actions to the corresponding pages and user flows\n- Exclude backend routing, data schema, and business logic details—focus solely on frontend templates\n- Do not access or rely on backend_design.md outputs\n\n**Section 1: HTML Template Structure**\n- For each of the nine pages, specify the template filename and page title exactly as given\n- List all element IDs with element type and purpose\n- Specify the layout hierarchy and any repeated elements using parameterized IDs (e.g., view-course-button-{course_id})\n\n**Section 2: Navigation and UI Behavior**\n- Define navigation buttons and their target pages\n- Describe UI state changes such as button enabling/disabling based on user status (enrolled/not enrolled)\n- Specify location of dynamic content placeholders or template variables for course info, assignments, progress, and certificates\n\nCRITICAL SUCCESS CRITERIA:\n- Output is a complete frontend_design.md describing all UI templates and navigation flows\n- All element IDs and pages strictly derived from user_task_description\n- Use write_text_file tool strictly to save frontend_design.md\n- Do not read or assume backend_design.md details\n- Output artifacts: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in synthesizing backend and frontend design specifications into coherent unified documentation for Flask web applications.\n\nYour goal is to combine backend_design.md and frontend_design.md with the user_task_description into one consistent design_spec.md that reconciles all routes, data schemas, UI templates, element IDs, and navigation flows without adding new requirements.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Validate completeness and consistency between backend routes and frontend templates for the nine pages\n- Ensure all route context variables and UI element IDs are aligned and naming consistent\n- Integrate backend data schemas with frontend UI data placeholders coherently\n- Preserve all backend and frontend sections and reconcile any conflicts or overlap strictly within original requirements\n\n**Section 1: Integrated Flask Routes and API Contracts**\n- Combine backend routes and endpoint specifications ensuring alignment with frontend navigation and UI actions\n- Document consistent input/output formats and parameters referenced in frontend templates\n\n**Section 2: Combined HTML Template Specifications**\n- Present all frontend templates with exact element IDs as per frontend_design.md\n- Ensure navigation flow matches backend routing and business logic\n- Clarify dynamic UI components tied to backend data schemas\n\n**Section 3: Data Schemas and Business Logic Summary**\n- Present unified data file schemas and examples from backend_design.md\n- Ensure descriptions match frontend data usage and UI display\n\nCRITICAL SUCCESS CRITERIA:\n- Output is a single design_spec.md artifact fully consistent with inputs\n- Backend and frontend designs are fully reconciled without information loss or conflict\n- Use write_text_file tool strictly to save design_spec.md\n- Output artifact: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend routes, data schemas, and logic completeness for 'OnlineCourse' against requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Validate frontend templates, element IDs, and navigation flow for accuracy and completeness.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend and frontend code artifacts from design_spec.md and integrate them into a consistent final web application.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py backend logic independently from design_spec.md; \"\n        \"FrontendDeveloper implements templates/*.html frontend UI independently using design_spec.md; \"\n        \"IntegrationMerger integrates and reconciles backend and frontend artifacts into final app.py and templates/*.html ensuring interface consistency.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with local text-file data handling.\n\nYour goal is to implement the complete Flask backend app.py based on design_spec.md independently of the frontend implementation.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Implement all Flask routes, business logic, data file handling, enrollment, progress tracking, certificate generation\n- Produce a fully functional app.py covering all declared routes and data operations, reflecting the user task requirements\n- Do not read or assume templates/*.html sibling outputs\n\n**Implementation Requirements:**\n- Implement Flask route handlers exactly as specified, with correct HTTP methods and route paths\n- Handle all file operations on data/*.txt files using the specified formats for users, courses, enrollments, assignments, submissions, certificates\n- Manage user enrollment creation with initial progress and dates, update progress on lesson completion, and generate certificates at 100% progress\n- Provide error handling for data consistency and access\n\n**Code Style and Integration:**\n- Use Python with Flask idioms and standard libraries only\n- Include comments using hash (#) style and use triple single-quotes (''') for any code documentation\n- Maintain clear separation of route logic, file I/O, and business rules in the code structure\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool exclusively to output app.py\n- Implementation strictly follows design_spec.md specifications and data formats from user task\n- Do not write any output other than app.py and do not use sibling outputs\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to implement all required HTML templates (*.html) independently, following the design_spec.md without dependence on backend code specifics.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Implement templates/*.html with full page structures, element IDs, buttons, inputs, tables, and navigation flows\n- Ensure each template corresponds to a page defined in design_spec.md, with correct page titles and required repeated element IDs as indicated\n- Do not read or assume app.py backend code sibling outputs\n\n**Implementation Requirements:**\n- Implement Jinja2-compatible HTML templates with consistent file naming and structure as per design_spec.md\n- Include all specified element IDs exactly, with appropriate element types (div, h1, button, input, textarea, table)\n- Ensure navigation buttons and links correspond to the declared routes and produce correct user navigation flow\n- Use semantic HTML and organize layout clearly for all nine pages described in user task documentation\n\n**Code Style and Integration:**\n- Use consistent indentation, escaping, and Jinja2 syntax as needed\n- Include brief comments via HTML or Jinja2 comments as appropriate for clarity\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool exclusively to output templates/*.html files\n- Implementation strictly follows design_spec.md frontend specifications and page details from user task\n- Do not write any output other than templates/*.html and do not use sibling outputs\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask backend and frontend template consolidation.\n\nYour goal is to merge and reconcile backend app.py and frontend templates/*.html artifacts into a consistent final deployment-ready web application.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Identify and resolve any interface mismatches between backend routes, expected templates, and frontend navigation elements\n- Ensure data flows, route handlers, and template element IDs align perfectly and navigation structures function coherently\n- Produce reconciled final app.py and templates/*.html outputs that satisfy user requirements and are mutually consistent\n\n**Integration Process:**\n- Compare route declarations and handlers in app.py with template files referencing those routes\n- Verify all buttons and navigation links in templates correspond to valid backend routes\n- Correct any naming or interface mismatches without adding new features or removing declared functionality\n- Ensure adherence to design_spec.md as the source of truth and no additional requirements are introduced\n\n**Validation and Consistency Checks:**\n- Validate that app.py runs without syntax errors and handles declared routes as expected\n- Validate templates render correctly with required element IDs and navigation paths\n- Preserve all user task and design_spec.md data format and UI element constraints\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool exclusively to output final app.py and templates/*.html\n- Final artifacts are fully consistent, deployable, and reflect user task specifications without deviation\n- Do not produce or modify any other artifacts beyond declared outputs\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend app.py for correct route implementations, data file management, and business logic conformity.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend templates/*.html adhere to design_spec.md including all element IDs and navigation correctness.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend development and data schema design for Python web applications.

Your goal is to design and specify the backend routes, data file schemas, enrollment and progress tracking logic, and API contracts necessary to implement the 'OnlineCourse' web application.

Task Details:
- Read user_task_description from CONTEXT for all backend requirements including pages, functionalities, and data storage
- Produce backend_design.md independently describing all Flask routes, HTTP methods, expected inputs, outputs, and business logic
- Define exact text file schemas (fields, delimiters, formats, examples) for users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, and certificates.txt
- Specify logic for enrollment management, progress calculation, assignment submissions, and certificate generation
- Do not access or rely on frontend_design.md outputs

**Section 1: Flask Routes Specification**
- List each Flask route with path, HTTP methods, expected request parameters, response format, and behavior
- Include routes for all nine pages and their interactive features (e.g., enrollment, progress update, submissions)
- Define redirects, login/session assumptions (if any), and error handling

**Section 2: Data File Schemas**
- Specify each data file path and exact pipe '|' delimited fields with data types and descriptions
- Provide example data rows for each file matching the requirements document
- Include enrollment progress tracking and status fields with format details

**Section 3: Business Logic and API Contracts**
- Describe enrollment logic: creation, initial progress zero, date recording
- Detail progress update rules: lessons completion sequence, progress percentage calculation
- Outline submission and grading data flow
- Describe certificate generation criteria and data update procedures

CRITICAL SUCCESS CRITERIA:
- Output is complete and independently sufficient backend_design.md
- All route and data schema elements strictly derived from user_task_description
- Use write_text_file tool strictly to save backend_design.md
- Do not read or assume frontend_design.md details
- Output artifacts: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML and frontend template design for Python web applications.

Your goal is to design the complete frontend HTML templates, element IDs, UI layouts, and navigation flows for the nine pages of the 'OnlineCourse' web application according to the requirements.

Task Details:
- Read user_task_description from CONTEXT for complete frontend page designs, UI elements, and navigation details
- Independently produce frontend_design.md describing the HTML template structure, element IDs, page titles, and navigation flow
- Specify exact element IDs (including repeated elements with parameters) and types for all buttons, divs, inputs, and other controls per page requirements
- Map navigation links and button actions to the corresponding pages and user flows
- Exclude backend routing, data schema, and business logic details—focus solely on frontend templates
- Do not access or rely on backend_design.md outputs

**Section 1: HTML Template Structure**
- For each of the nine pages, specify the template filename and page title exactly as given
- List all element IDs with element type and purpose
- Specify the layout hierarchy and any repeated elements using parameterized IDs (e.g., view-course-button-{course_id})

**Section 2: Navigation and UI Behavior**
- Define navigation buttons and their target pages
- Describe UI state changes such as button enabling/disabling based on user status (enrolled/not enrolled)
- Specify location of dynamic content placeholders or template variables for course info, assignments, progress, and certificates

CRITICAL SUCCESS CRITERIA:
- Output is a complete frontend_design.md describing all UI templates and navigation flows
- All element IDs and pages strictly derived from user_task_description
- Use write_text_file tool strictly to save frontend_design.md
- Do not read or assume backend_design.md details
- Output artifacts: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in synthesizing backend and frontend design specifications into coherent unified documentation for Flask web applications.

Your goal is to combine backend_design.md and frontend_design.md with the user_task_description into one consistent design_spec.md that reconciles all routes, data schemas, UI templates, element IDs, and navigation flows without adding new requirements.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Validate completeness and consistency between backend routes and frontend templates for the nine pages
- Ensure all route context variables and UI element IDs are aligned and naming consistent
- Integrate backend data schemas with frontend UI data placeholders coherently
- Preserve all backend and frontend sections and reconcile any conflicts or overlap strictly within original requirements

**Section 1: Integrated Flask Routes and API Contracts**
- Combine backend routes and endpoint specifications ensuring alignment with frontend navigation and UI actions
- Document consistent input/output formats and parameters referenced in frontend templates

**Section 2: Combined HTML Template Specifications**
- Present all frontend templates with exact element IDs as per frontend_design.md
- Ensure navigation flow matches backend routing and business logic
- Clarify dynamic UI components tied to backend data schemas

**Section 3: Data Schemas and Business Logic Summary**
- Present unified data file schemas and examples from backend_design.md
- Ensure descriptions match frontend data usage and UI display

CRITICAL SUCCESS CRITERIA:
- Output is a single design_spec.md artifact fully consistent with inputs
- Backend and frontend designs are fully reconciled without information loss or conflict
- Use write_text_file tool strictly to save design_spec.md
- Output artifact: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with local text-file data handling.

Your goal is to implement the complete Flask backend app.py based on design_spec.md independently of the frontend implementation.

Task Details:
- Read design_spec.md from CONTEXT
- Implement all Flask routes, business logic, data file handling, enrollment, progress tracking, certificate generation
- Produce a fully functional app.py covering all declared routes and data operations, reflecting the user task requirements
- Do not read or assume templates/*.html sibling outputs

**Implementation Requirements:**
- Implement Flask route handlers exactly as specified, with correct HTTP methods and route paths
- Handle all file operations on data/*.txt files using the specified formats for users, courses, enrollments, assignments, submissions, certificates
- Manage user enrollment creation with initial progress and dates, update progress on lesson completion, and generate certificates at 100% progress
- Provide error handling for data consistency and access

**Code Style and Integration:**
- Use Python with Flask idioms and standard libraries only
- Include comments using hash (#) style and use triple single-quotes (''') for any code documentation
- Maintain clear separation of route logic, file I/O, and business rules in the code structure

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output app.py
- Implementation strictly follows design_spec.md specifications and data formats from user task
- Do not write any output other than app.py and do not use sibling outputs

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement all required HTML templates (*.html) independently, following the design_spec.md without dependence on backend code specifics.

Task Details:
- Read design_spec.md from CONTEXT
- Implement templates/*.html with full page structures, element IDs, buttons, inputs, tables, and navigation flows
- Ensure each template corresponds to a page defined in design_spec.md, with correct page titles and required repeated element IDs as indicated
- Do not read or assume app.py backend code sibling outputs

**Implementation Requirements:**
- Implement Jinja2-compatible HTML templates with consistent file naming and structure as per design_spec.md
- Include all specified element IDs exactly, with appropriate element types (div, h1, button, input, textarea, table)
- Ensure navigation buttons and links correspond to the declared routes and produce correct user navigation flow
- Use semantic HTML and organize layout clearly for all nine pages described in user task documentation

**Code Style and Integration:**
- Use consistent indentation, escaping, and Jinja2 syntax as needed
- Include brief comments via HTML or Jinja2 comments as appropriate for clarity

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output templates/*.html files
- Implementation strictly follows design_spec.md frontend specifications and page details from user task
- Do not write any output other than templates/*.html and do not use sibling outputs

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask backend and frontend template consolidation.

Your goal is to merge and reconcile backend app.py and frontend templates/*.html artifacts into a consistent final deployment-ready web application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Identify and resolve any interface mismatches between backend routes, expected templates, and frontend navigation elements
- Ensure data flows, route handlers, and template element IDs align perfectly and navigation structures function coherently
- Produce reconciled final app.py and templates/*.html outputs that satisfy user requirements and are mutually consistent

**Integration Process:**
- Compare route declarations and handlers in app.py with template files referencing those routes
- Verify all buttons and navigation links in templates correspond to valid backend routes
- Correct any naming or interface mismatches without adding new features or removing declared functionality
- Ensure adherence to design_spec.md as the source of truth and no additional requirements are introduced

**Validation and Consistency Checks:**
- Validate that app.py runs without syntax errors and handles declared routes as expected
- Validate templates render correctly with required element IDs and navigation paths
- Preserve all user task and design_spec.md data format and UI element constraints

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output final app.py and templates/*.html
- Final artifacts are fully consistent, deployable, and reflect user task specifications without deviation
- Do not produce or modify any other artifacts beyond declared outputs

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'BackendDesignArchitect': [
        ("DesignMerger", """Verify backend routes, data schemas, and logic completeness for 'OnlineCourse' against requirements.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Validate frontend templates, element IDs, and navigation flow for accuracy and completeness.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend app.py for correct route implementations, data file management, and business logic conformity.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend templates/*.html adhere to design_spec.md including all element IDs and navigation correctness.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}





# ==================== Chaos Controller Setup ====================
import random
import os
from chaos.injectors import ChaosMode

COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "stress_method": random.choice(['WORD_SHUFFLE', 'WORD_DELETION', 'WORD_REPLACEMENT']),
    "io_method": random.choice(['WORD_SHUFFLE', 'WORD_DELETION', 'WORD_REPLACEMENT']),
    "stress_probability": 0.2,
    "io_probability": 0.2
}
if os.environ.get("CHAOS_AGENT_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["agent_intensity"] = float(os.environ["CHAOS_AGENT_PROBABILITY_OVERRIDE"])
if os.environ.get("CHAOS_STRESS_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["stress_probability"] = float(os.environ["CHAOS_STRESS_PROBABILITY_OVERRIDE"])
if os.environ.get("CHAOS_IO_PROBABILITY_OVERRIDE"):
    COMPOUND_CONFIG["io_probability"] = float(os.environ["CHAOS_IO_PROBABILITY_OVERRIDE"])

MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_target_agent_names = [
    name.strip()
    for name in os.environ.get("CHAOS_TARGET_AGENT_NAMES", "").split(",")
    if name.strip()
] or list(AGENT_PROFILES.keys())

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["stress_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=chaos_target_agent_names
)

# V2 probabilities: agent chaos uses random 0.2-0.6; stress/io use 0.2.
# V1 methods: one word-based Stress mode and one word-based IO mode per task.
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

all_agents = list(AGENT_PROFILES.keys())
chaos_controller.set_targets_by_probability(
    "stress",
    running_agents=all_agents,
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["stress_probability"]
)
chaos_controller.set_targets_by_probability(
    "io",
    running_agents=all_agents,
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["io_probability"]
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "probability": COMPOUND_CONFIG["agent_intensity"],
    "target_agent_names": chaos_target_agent_names,
    "probabilities": {
        "agent_chaos": COMPOUND_CONFIG["agent_intensity"],
        "stress_chaos": COMPOUND_CONFIG["stress_probability"],
        "io_chaos": COMPOUND_CONFIG["io_probability"]
    },
    "compound_config": COMPOUND_CONFIG,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
    },
    "logical_targets": {
        "agent_chaos_targets": chaos_controller.agent_chaos_logical_targets,
        "stress_chaos_targets": chaos_controller.stress_chaos_logical_targets,
        "io_chaos_targets": chaos_controller.io_chaos_logical_targets
    },
    "targets": {
        "agent_chaos_targets": chaos_controller.agent_chaos_targets,
        "stress_chaos_targets": chaos_controller.stress_chaos_targets,
        "io_chaos_targets": chaos_controller.io_chaos_targets
    },
    "registered_files": dict(chaos_controller.agent_file_registry)
}

with open("chaos_config.json", "w") as f:
    json.dump(chaos_config_data, f, indent=2)

print("[*] Chaos scenario 'compound_chaos' activated with compound probabilities")
print(f"[*] Compound config: {COMPOUND_CONFIG}")
print(f"[*] Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Run BackendDesignArchitect and FrontendDesignArchitect in parallel
    await asyncio.gather(
        execute(BackendDesignArchitect, "Read user_task_description and produce complete backend_design.md with routes, data schemas, and business logic."),
        execute(FrontendDesignArchitect, "Read user_task_description and produce complete frontend_design.md with HTML templates, element IDs, and navigation flows.")
    )

    # Read outputs for DesignMerger
    backend_design_content, frontend_design_content = "", ""
    try:
        backend_design_content = open("backend_design.md").read()
    except Exception:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except Exception:
        pass

    # Execute DesignMerger to combine backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md with user_task_description into one consistent design_spec.md.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete app.py backend using design_spec.md. Follow all route handlers, data file management, business logic, progress tracking, and certificate generation."),
        execute(FrontendDeveloper,
                "Implement all required HTML templates (*.html) with full page structure, element IDs, buttons, forms, navigation, and layout according to design_spec.md.")
    )

    # After backend and frontend implementations, read their output artifacts for integration
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except FileNotFoundError:
        pass
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Execute IntegrationMerger to merge and reconcile backend and frontend into final consistent artifacts
    await execute(
        IntegrationMerger,
        f"Read design_spec.md, current app.py and templates/*.html outputs.\n"
        "Identify and resolve interface mismatches between backend routes and frontend templates (element IDs, navigation links).\n"
        "Ensure app.py and templates/*.html are fully consistent and deployable.\n\n"
        f"=== design_spec.md ===\n{design_spec_content}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates content ===\n{templates_content}"
    )
# Phase2_End
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
        implementation_and_verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)

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

    # Print chaos engineering report
    print("\n" + "="*80)
    print("Chaos Engineering Report")
    print("="*80)
    chaos_controller.print_report(context=CONTEXT)


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
