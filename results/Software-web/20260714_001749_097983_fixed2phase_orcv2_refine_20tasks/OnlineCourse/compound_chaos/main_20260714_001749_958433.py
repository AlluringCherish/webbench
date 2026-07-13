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
# 20260714_001749_958433/main_20260714_001749_958433.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the comprehensive design specification for the 'OnlineCourse' Python web application capturing all pages, UI element IDs, data formats, and user workflows into design_spec.md with gated feedback in design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator writes design_spec.md from user_task_description and design_feedback.md; DesignCritic reviews design_spec.md producing design_feedback.md; iteration runs up to two times or stops on [APPROVED].\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to produce a detailed and complete design specification document capturing UI pages, element IDs, data storage schemas, and user workflows for the 'OnlineCourse' Python web application, refining it through critic feedback for up to two iterations.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Read prior versions of design_spec.md and design_feedback.md when available to determine if REWRITE is needed\n- On first iteration, create a thorough design_spec.md describing all required pages, UI element IDs, data formats, and functional workflows\n- On feedback that begins with NEED_MODIFY, apply every correction fully and overwrite design_spec.md\n- On feedback starting with [APPROVED], preserve the approved design\n\n**Section 1: UI Pages and Element IDs**\n- Document all 9 application pages with page titles, purpose, and all specified element IDs including repeated elements (e.g. buttons with dynamic IDs)\n- Include navigation flows among pages as described\n- Ensure element types and IDs match user requirements exactly\n\n**Section 2: Data Storage Formats**\n- Specify text file names and exact data field formats per user specification\n- Include data field orders, separators, and example rows as structured text\n- Confirm data file uses consistent delimiter and encodings\n\n**Section 3: Functional Workflows**\n- Detail user interactions such as enrollment, assignment submission, progress tracking, and certificate issuance\n- Specify logic for button states, progress calculations, sequential lesson completion, and automatic certificate generation\n- Reflect all user objectives and requirements fully\n\nCRITICAL SUCCESS CRITERIA:\n- Produce fully comprehensive design_spec.md aligned with user_task_description\n- Rewrite entire artifact on NEED_MODIFY feedback, using all supported corrections\n- Use write_text_file tool to output design_spec.md\n- Run at most two Generator/Critic iterations, stopping immediately on approved status\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application design specifications.\n\nYour goal is to review the design_spec.md document for completeness, correctness of page layouts, accuracy of UI element IDs, consistency of data formats, and full adherence to the user's functional objectives; provide gated feedback marking completion as [APPROVED] or identify issues as NEED_MODIFY for up to two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Check coverage of all nine required pages with correct titles and exact UI element IDs including repeated dynamic elements\n- Verify data storage schemas match the specified local text file formats, field delimiters, and example data\n- Confirm functional workflows reflect all required user interactions from enrollment through certificate generation\n- Write feedback in design_feedback.md starting with exactly [APPROVED] if all criteria met\n- Otherwise, write NEED_MODIFY followed by specific, actionable corrections without adding new requirements beyond user_task_description\n\nReview Criteria:\n1. Completeness of page designs and UI element ID accuracy\n2. Accuracy and consistency of data file names, field formats, and example entries\n3. Fidelity of workflows including button states, progress calculations, and message displays\n4. Alignment with stated user objectives and no missing requirements\n5. No introduction of unstated functions or data structures\n\nCRITICAL REQUIREMENTS:\n- Begin design_feedback.md with byte-1 marker exactly '[APPROVED]' or 'NEED_MODIFY'\n- No additional prefixes, whitespace, or headings before marker\n- Use write_text_file tool to save full feedback document\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Ensure the design covers all required pages and UI elements with correct IDs, accurately describes local text data storage formats, and aligns fully with user functional objectives.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine complete Python Flask web application source code (app.py and templates/*.html) implementing the 'OnlineCourse' system to specification with gated feedback in code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or fully revises app.py and all templates/*.html implementing design_spec.md and code_feedback.md feedback; CodeCritic reviews code correctness, UI element IDs, data file handling, and application functionality, producing code_feedback.md; iteration runs up to two times or stops on [APPROVED].\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in web application backend and frontend template development.\n\nYour goal is to develop or fully revise the complete Flask app.py backend and corresponding HTML templates implementing all pages, UI elements with exact IDs, local text file data management, and workflow logic according to design_spec.md and any code_feedback.md for up to two refinement iterations.\n\nTask Details:\n- Read design_spec.md to understand full application structure, pages, elements, and data file formats\n- Read existing app.py, templates/*.html, and code_feedback.md for requested changes\n- On first iteration, create fully functional app.py and templates implementing all specified pages and features\n- On feedback starting with NEED_MODIFY, apply all corrections fully and overwrite app.py and templates\n- Preserve approval if code_feedback.md begins with [APPROVED]\n- Focus on Python backend logic for data files and Flask routes, plus exact HTML templates with specified element IDs\n\n**Section 1: Backend Implementation**\n- Implement all Flask routes and view functions for 9 pages with routing and navigation\n- Manage local text files (users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt) for CRUD operations\n- Implement business logic for enrollment, progress tracking, assignment submissions, and certificate generation\n- Enforce sequential lesson completion and progress updates in enrollments.txt\n- Include proper date handling for enrollment and submissions\n\n**Section 2: Frontend Templates**\n- Create HTML templates for each page with all specified element IDs exactly as declared\n- Use Flask templating for dynamic content (user info, course lists, assignments, progress, certificates)\n- Include buttons and controls with IDs for navigation and actions\n- Ensure consistent navigation links between pages as per design\n\n**Section 3: Refinement and File Output**\n- Use write_text_file tool to output complete app.py and templates/*.html files\n- Submit fully integrated code reflecting corrections or new implementation each iteration\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two full Generator/Critic iterations or stop immediately on approval\n- Apply every NEED_MODIFY item fully and correctly on rewrite iterations\n- Maintain exact UI element IDs and data file formats from design_spec.md\n- Use write_text_file tool to save output files app.py and templates/*.html\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask applications and HTML frontend verification.\n\nYour goal is to review app.py and HTML templates for syntax correctness, full functional completeness, strict adherence to UI element ID specifications, correct local text file handling, and workflow consistency; provide gated feedback for up to two iterations beginning each code_feedback.md with [APPROVED] or NEED_MODIFY.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate Python syntax and runtime correctness using validate_python_file\n- Verify all 9 pages' UI elements have exact IDs as specified\n- Confirm Flask routes and backend logic fully implement design requirements\n- Check proper reading, writing, and updating of local text data files (users, courses, enrollments, assignments, submissions, certificates)\n- Verify workflow logic like enrollment handling, progress calculation, assignment submission, and certificate issuance\n- Write code_feedback.md starting exactly with [APPROVED] if all criteria met or NEED_MODIFY and specific corrections otherwise\n\nReview Checklist:\n1. Syntax and runtime errors absent in app.py\n2. All UI element IDs present and correctly named in templates\n3. Complete route coverage for all pages with correct navigation links\n4. Accurate data file interaction matching design specification format and business logic\n5. Correct handling of user interaction flows, statuses, and updates in data files\n6. Clear, actionable feedback with specific fix instructions if needed\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file tool for syntax/runtime validation\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- Use write_text_file tool to save full feedback text\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Validate code correctness, full implementation of design_spec.md functional requirements, exact UI element IDs usage, and local text file data integration.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to produce a detailed and complete design specification document capturing UI pages, element IDs, data storage schemas, and user workflows for the 'OnlineCourse' Python web application, refining it through critic feedback for up to two iterations.

Task Details:
- Read user_task_description from CONTEXT
- Read prior versions of design_spec.md and design_feedback.md when available to determine if REWRITE is needed
- On first iteration, create a thorough design_spec.md describing all required pages, UI element IDs, data formats, and functional workflows
- On feedback that begins with NEED_MODIFY, apply every correction fully and overwrite design_spec.md
- On feedback starting with [APPROVED], preserve the approved design

**Section 1: UI Pages and Element IDs**
- Document all 9 application pages with page titles, purpose, and all specified element IDs including repeated elements (e.g. buttons with dynamic IDs)
- Include navigation flows among pages as described
- Ensure element types and IDs match user requirements exactly

**Section 2: Data Storage Formats**
- Specify text file names and exact data field formats per user specification
- Include data field orders, separators, and example rows as structured text
- Confirm data file uses consistent delimiter and encodings

**Section 3: Functional Workflows**
- Detail user interactions such as enrollment, assignment submission, progress tracking, and certificate issuance
- Specify logic for button states, progress calculations, sequential lesson completion, and automatic certificate generation
- Reflect all user objectives and requirements fully

CRITICAL SUCCESS CRITERIA:
- Produce fully comprehensive design_spec.md aligned with user_task_description
- Rewrite entire artifact on NEED_MODIFY feedback, using all supported corrections
- Use write_text_file tool to output design_spec.md
- Run at most two Generator/Critic iterations, stopping immediately on approved status

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application design specifications.

Your goal is to review the design_spec.md document for completeness, correctness of page layouts, accuracy of UI element IDs, consistency of data formats, and full adherence to the user's functional objectives; provide gated feedback marking completion as [APPROVED] or identify issues as NEED_MODIFY for up to two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Check coverage of all nine required pages with correct titles and exact UI element IDs including repeated dynamic elements
- Verify data storage schemas match the specified local text file formats, field delimiters, and example data
- Confirm functional workflows reflect all required user interactions from enrollment through certificate generation
- Write feedback in design_feedback.md starting with exactly [APPROVED] if all criteria met
- Otherwise, write NEED_MODIFY followed by specific, actionable corrections without adding new requirements beyond user_task_description

Review Criteria:
1. Completeness of page designs and UI element ID accuracy
2. Accuracy and consistency of data file names, field formats, and example entries
3. Fidelity of workflows including button states, progress calculations, and message displays
4. Alignment with stated user objectives and no missing requirements
5. No introduction of unstated functions or data structures

CRITICAL REQUIREMENTS:
- Begin design_feedback.md with byte-1 marker exactly '[APPROVED]' or 'NEED_MODIFY'
- No additional prefixes, whitespace, or headings before marker
- Use write_text_file tool to save full feedback document

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in web application backend and frontend template development.

Your goal is to develop or fully revise the complete Flask app.py backend and corresponding HTML templates implementing all pages, UI elements with exact IDs, local text file data management, and workflow logic according to design_spec.md and any code_feedback.md for up to two refinement iterations.

Task Details:
- Read design_spec.md to understand full application structure, pages, elements, and data file formats
- Read existing app.py, templates/*.html, and code_feedback.md for requested changes
- On first iteration, create fully functional app.py and templates implementing all specified pages and features
- On feedback starting with NEED_MODIFY, apply all corrections fully and overwrite app.py and templates
- Preserve approval if code_feedback.md begins with [APPROVED]
- Focus on Python backend logic for data files and Flask routes, plus exact HTML templates with specified element IDs

**Section 1: Backend Implementation**
- Implement all Flask routes and view functions for 9 pages with routing and navigation
- Manage local text files (users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt) for CRUD operations
- Implement business logic for enrollment, progress tracking, assignment submissions, and certificate generation
- Enforce sequential lesson completion and progress updates in enrollments.txt
- Include proper date handling for enrollment and submissions

**Section 2: Frontend Templates**
- Create HTML templates for each page with all specified element IDs exactly as declared
- Use Flask templating for dynamic content (user info, course lists, assignments, progress, certificates)
- Include buttons and controls with IDs for navigation and actions
- Ensure consistent navigation links between pages as per design

**Section 3: Refinement and File Output**
- Use write_text_file tool to output complete app.py and templates/*.html files
- Submit fully integrated code reflecting corrections or new implementation each iteration

CRITICAL SUCCESS CRITERIA:
- Run at most two full Generator/Critic iterations or stop immediately on approval
- Apply every NEED_MODIFY item fully and correctly on rewrite iterations
- Maintain exact UI element IDs and data file formats from design_spec.md
- Use write_text_file tool to save output files app.py and templates/*.html

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask applications and HTML frontend verification.

Your goal is to review app.py and HTML templates for syntax correctness, full functional completeness, strict adherence to UI element ID specifications, correct local text file handling, and workflow consistency; provide gated feedback for up to two iterations beginning each code_feedback.md with [APPROVED] or NEED_MODIFY.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate Python syntax and runtime correctness using validate_python_file
- Verify all 9 pages' UI elements have exact IDs as specified
- Confirm Flask routes and backend logic fully implement design requirements
- Check proper reading, writing, and updating of local text data files (users, courses, enrollments, assignments, submissions, certificates)
- Verify workflow logic like enrollment handling, progress calculation, assignment submission, and certificate issuance
- Write code_feedback.md starting exactly with [APPROVED] if all criteria met or NEED_MODIFY and specific corrections otherwise

Review Checklist:
1. Syntax and runtime errors absent in app.py
2. All UI element IDs present and correctly named in templates
3. Complete route coverage for all pages with correct navigation links
4. Accurate data file interaction matching design specification format and business logic
5. Correct handling of user interaction flows, statuses, and updates in data files
6. Clear, actionable feedback with specific fix instructions if needed

CRITICAL REQUIREMENTS:
- Use validate_python_file tool for syntax/runtime validation
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Use write_text_file tool to save full feedback text

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Ensure the design covers all required pages and UI elements with correct IDs, accurately describes local text data storage formats, and aligns fully with user functional objectives.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Validate code correctness, full implementation of design_spec.md functional requirements, exact UI element IDs usage, and local text file data integration.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        current_design = ""
        feedback_content = ""
        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            pass
        if iteration > 0:
            try:
                feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            DesignGenerator,
            "Produce or refine design_spec.md for the 'OnlineCourse' Python web application.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review design_spec.md for completeness, UI element ID accuracy, data format consistency, and workflow fidelity per user_task_description.\nWrite design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== Latest design_spec.md ===\n{current_design}"
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""
        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    AppGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=500,
        failure_threshold=2,
        recovery_time=60
    )
    CodeCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_content = ""
        templates_content = ""
        feedback_content = ""

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            pass

        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html.\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{feedback_content}"
        )

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            app_content = ""

        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates against design_spec.md. "
            "Write code_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest Templates ===\n{templates_content}"
        )

        try:
            feedback_content = open("code_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
            break
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
