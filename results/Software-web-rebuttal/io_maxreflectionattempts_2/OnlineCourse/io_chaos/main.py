import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
from chaos import ChaosController

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development for OnlineCourse app\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces design_spec.md including Flask routes with function names and context variables, \"\n        \"HTML templates with detailed element IDs, data schemas defining exact field orders and data formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create comprehensive design specifications that enable Backend and Frontend developers to work completely independently without knowing each other's implementation details.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand all pages, elements, and data schemas\n- Create design_spec.md with three main sections optimized for independent parallel development:\n  * Flask Routes (with function names, HTTP methods, and template context variables)\n  * HTML Templates (with detailed element IDs and navigation url_for mappings)\n  * Data Schemas (exact field order and pipe-delimited format for all data files)\n- Do NOT assume or include implementation details beyond specification requirements\n\n**Section 1: Flask Routes Specification (For Backend Developer)**\n\nProvide a complete table with columns:\n- Route Path: URL pattern for each app page and actions\n- Function Name: Flask function name with consistent lowercase_underscore format\n- HTTP Method: GET or POST where applicable\n- Template File: Name of HTML template to render\n- Context Variables: List all variables passed to template with exact names and types\n\nRequirements:\n- Include root route '/' that redirects to Dashboard page\n- Include dynamic routes with parameters as required (e.g., course_id, assignment_id)\n- Specify behavior and data for POST routes (form handling)\n- Include logic notes on enrollment, progress updates, assignment submissions, and certificate generation\n\n**Section 2: HTML Template Specifications (For Frontend Developer)**\n\nFor each template file:\n- Specify file path, e.g., templates/dashboard.html\n- Define page title for <title> and <h1> tags exactly as in user requirements\n- Include all required element IDs exactly as specified (case-sensitive)\n- For dynamic elements (e.g., view-course-button-{course_id}), specify ID pattern and Jinja2 syntax for iteration\n- Enumerate all context variables accessible in template with types and structure\n- Map navigation buttons/links to Flask routes using exact url_for function names with parameters where applicable\n- Indicate button states when applicable (e.g., enroll button disabled when already enrolled)\n\nRequirements:\n- ALL element IDs from user specs must be included exactly, including repeated elements with templates for dynamic IDs\n- Navigation mappings must correspond exactly to Flask function names in Section 1\n- Context variable names must be consistent with Section 1\n- Provide notes on form fields and POST submission targets where relevant\n\n**Section 3: Data File Schemas (For Backend Developer)**\n\nFor each data file (e.g., users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt):\n- Specify file path relative to 'data/' directory\n- Define exact pipe-delimited field order and field names\n- Describe the contents and purpose of each field clearly\n- Provide 2-3 realistic example lines matching the format\n- Ensure examples use realistic data consistent with user_task_description\n\nRequirements:\n- Use pipe-delimited format exclusively (|)\n- No header lines; parsing starts from line 1\n- Field order MUST be precise to ensure correct data parsing\n- Include notes on special constraints, e.g., date formats, status values\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developer can implement all app routes and logic using ONLY Section 1 + Section 3\n- Frontend developer can implement all HTML templates using ONLY Section 2 without backend code\n- No interdependencies requiring direct communication between backend and frontend teams\n- All element IDs, function names, and context variables are consistent and complete\n- Use write_text_file tool to output design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 1 (Flask routes) includes all specified routes with correct function names, HTTP methods, \"\n                \"and context variables; Section 3 (data schemas) has accurate field orders and data formats matching requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 2 (HTML templates) includes all element IDs exactly as specified, correct context variables, \"\n                \"and navigation with proper url_for mappings.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend components in parallel based on design specification for OnlineCourse app\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using design_spec.md Sections 1 and 3 focusing on routes, data handling and business logic. \"\n        \"FrontendDeveloper implements templates/*.html using design_spec.md Section 2 focusing on page structures, element IDs, and navigation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement the complete backend for the OnlineCourse web application, including all Flask routes, business logic, data file handling, and progress tracking based on the design specification.\n\nTask Details:\n- Read design_spec.md Section 1 (Flask Routes) and Section 3 (Data Schemas) only from CONTEXT\n- Implement app.py with all Flask routes defined, handling HTTP methods and business logic\n- Load and save data in 'data/' directory using pipe-delimited files as described in Section 3\n- Correctly calculate and update course progress and handle enrollment, assignment submissions, and certificate generation\n- Do NOT read Section 2 (Frontend Templates) or modify frontend code\n\nImplementation Guidelines:\n1. **Flask Application Setup**:\n   - Initialize Flask app with proper configuration\n   - Implement root route '/' to redirect to dashboard page using: return redirect(url_for('dashboard'))\n\n2. **Data Handling**:\n   - Use pipe-delimited (|) parsing for all data files in 'data/' folder\n   - Match field orders exactly as described in Section 3 for users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt\n   - Implement reading and writing functions for each data type with error handling\n   - Update enrollments.txt for progress changes and enrollment additions\n   - Update submissions.txt on assignment submissions\n   - Generate certificate entries in certificates.txt on course completion (100% progress)\n\n3. **Route Implementation**:\n   - Implement all routes with exact function names and HTTP methods from Section 1\n   - Implement business rules such as:\n     - Enrollment button disables/enables based on enrollment status\n     - Lesson completion updates progress sequentially\n     - Late submission tracking via submit_date\n     - Certificate generation triggers on completion\n\n4. **Best Practices**:\n   - Use Flask's url_for for redirects and links\n   - Handle all errors gracefully and validate inputs\n   - Add if __name__ == '__main__': block to run app with debug=True on port 5000\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save complete app.py\n- Function names, route paths, and context variables must match design_spec.md Section 1 exactly\n- Data file parsing and writing must strictly follow Section 3 schemas and orders\n- Do NOT implement any frontend code or template logic\n- Ensure business logic correctness for enrollment, progress tracking, and certificate issuance\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement all HTML templates (*.html) for the OnlineCourse application based on the design_spec.md Section 2, ensuring correct page layouts, element IDs, and navigation.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) only from CONTEXT\n- Implement all HTML templates with required structure, element IDs, and navigation\n- Use Jinja2 syntax for dynamic content, loops, and conditionals as specified\n- Do NOT read or modify backend logic or data handling code\n- Preserve all element IDs exactly as specified, including dynamic IDs like view-course-button-{course_id}\n\nImplementation Guidelines:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>Page Title from Section 2</title>\n   </head>\n   <body>\n       <div id=\"main-container\">\n           <h1>Page Title from Section 2</h1>\n           <!-- Page content here -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs**:\n   - Use exact element IDs as specified, including dash-case and dynamic patterns\n   - For repeated dynamic IDs, use Jinja2 syntax, e.g., id=\"view-course-button-{{ course.course_id }}\"\n\n3. **Navigation Links**:\n   - Use url_for with exact function names from Section 2 for all buttons and links\n   - For dynamic navigation, pass required parameters matching route definitions\n\n4. **Forms and Inputs**:\n   - Implement forms for assignment submissions and profile updates with proper method and action attributes\n   - Use required attributes and input types as specified\n\n5. **Conditionals and Loops**:\n   - Use Jinja2 conditionals to handle enrolled status, button disabling, and data presence\n   - Use for-loops to render course lists, assignments, certificates, and lessons\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files in templates/ directory\n- All element IDs must match design_spec.md Section 2 exactly, including case-sensitive and dynamic patterns\n- Page titles must match Section 2 exactly in both <title> and <h1>\n- Navigation must use exact url_for functions as specified\n- Do NOT implement backend logic or data file handling in templates\n- Do NOT provide partial code in chat; always save complete files\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Check app.py to confirm all Flask routes from design_spec.md Section 1 are implemented correctly, \"\n                \"data handling respects schemas from Section 3, root route redirects to dashboard, and progress calculation logic matches requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify templates/*.html implement all element IDs and layout from design_spec.md Section 2 exactly, \"\n                \"navigation uses correct url_for calls, and page titles are accurate.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
  - **ID: view-course-button-{course_id}** - Type: Button - View course details. (Repeated Element)
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
  - **ID: continue-learning-button-{course_id}** - Type: Button - Continue learning a course. (Repeated Element)
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
  - **ID: submit-assignment-button-{assignment_id}** - Type: Button - Submit a pending assignment. (Repeated Element)
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create comprehensive design specifications that enable Backend and Frontend developers to work completely independently without knowing each other's implementation details.

Task Details:
- Read user_task_description from CONTEXT to understand all pages, elements, and data schemas
- Create design_spec.md with three main sections optimized for independent parallel development:
  * Flask Routes (with function names, HTTP methods, and template context variables)
  * HTML Templates (with detailed element IDs and navigation url_for mappings)
  * Data Schemas (exact field order and pipe-delimited format for all data files)
- Do NOT assume or include implementation details beyond specification requirements

**Section 1: Flask Routes Specification (For Backend Developer)**

Provide a complete table with columns:
- Route Path: URL pattern for each app page and actions
- Function Name: Flask function name with consistent lowercase_underscore format
- HTTP Method: GET or POST where applicable
- Template File: Name of HTML template to render
- Context Variables: List all variables passed to template with exact names and types

Requirements:
- Include root route '/' that redirects to Dashboard page
- Include dynamic routes with parameters as required (e.g., course_id, assignment_id)
- Specify behavior and data for POST routes (form handling)
- Include logic notes on enrollment, progress updates, assignment submissions, and certificate generation

**Section 2: HTML Template Specifications (For Frontend Developer)**

For each template file:
- Specify file path, e.g., templates/dashboard.html
- Define page title for <title> and <h1> tags exactly as in user requirements
- Include all required element IDs exactly as specified (case-sensitive)
- For dynamic elements (e.g., view-course-button-{course_id}), specify ID pattern and Jinja2 syntax for iteration
- Enumerate all context variables accessible in template with types and structure
- Map navigation buttons/links to Flask routes using exact url_for function names with parameters where applicable
- Indicate button states when applicable (e.g., enroll button disabled when already enrolled)

Requirements:
- ALL element IDs from user specs must be included exactly, including repeated elements with templates for dynamic IDs
- Navigation mappings must correspond exactly to Flask function names in Section 1
- Context variable names must be consistent with Section 1
- Provide notes on form fields and POST submission targets where relevant

**Section 3: Data File Schemas (For Backend Developer)**

For each data file (e.g., users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt):
- Specify file path relative to 'data/' directory
- Define exact pipe-delimited field order and field names
- Describe the contents and purpose of each field clearly
- Provide 2-3 realistic example lines matching the format
- Ensure examples use realistic data consistent with user_task_description

Requirements:
- Use pipe-delimited format exclusively (|)
- No header lines; parsing starts from line 1
- Field order MUST be precise to ensure correct data parsing
- Include notes on special constraints, e.g., date formats, status values

CRITICAL SUCCESS CRITERIA:
- Backend developer can implement all app routes and logic using ONLY Section 1 + Section 3
- Frontend developer can implement all HTML templates using ONLY Section 2 without backend code
- No interdependencies requiring direct communication between backend and frontend teams
- All element IDs, function names, and context variables are consistent and complete
- Use write_text_file tool to output design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement the complete backend for the OnlineCourse web application, including all Flask routes, business logic, data file handling, and progress tracking based on the design specification.

Task Details:
- Read design_spec.md Section 1 (Flask Routes) and Section 3 (Data Schemas) only from CONTEXT
- Implement app.py with all Flask routes defined, handling HTTP methods and business logic
- Load and save data in 'data/' directory using pipe-delimited files as described in Section 3
- Correctly calculate and update course progress and handle enrollment, assignment submissions, and certificate generation
- Do NOT read Section 2 (Frontend Templates) or modify frontend code

Implementation Guidelines:
1. **Flask Application Setup**:
   - Initialize Flask app with proper configuration
   - Implement root route '/' to redirect to dashboard page using: return redirect(url_for('dashboard'))

2. **Data Handling**:
   - Use pipe-delimited (|) parsing for all data files in 'data/' folder
   - Match field orders exactly as described in Section 3 for users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt
   - Implement reading and writing functions for each data type with error handling
   - Update enrollments.txt for progress changes and enrollment additions
   - Update submissions.txt on assignment submissions
   - Generate certificate entries in certificates.txt on course completion (100% progress)

3. **Route Implementation**:
   - Implement all routes with exact function names and HTTP methods from Section 1
   - Implement business rules such as:
     - Enrollment button disables/enables based on enrollment status
     - Lesson completion updates progress sequentially
     - Late submission tracking via submit_date
     - Certificate generation triggers on completion

4. **Best Practices**:
   - Use Flask's url_for for redirects and links
   - Handle all errors gracefully and validate inputs
   - Add if __name__ == '__main__': block to run app with debug=True on port 5000

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save complete app.py
- Function names, route paths, and context variables must match design_spec.md Section 1 exactly
- Data file parsing and writing must strictly follow Section 3 schemas and orders
- Do NOT implement any frontend code or template logic
- Ensure business logic correctness for enrollment, progress tracking, and certificate issuance

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement all HTML templates (*.html) for the OnlineCourse application based on the design_spec.md Section 2, ensuring correct page layouts, element IDs, and navigation.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) only from CONTEXT
- Implement all HTML templates with required structure, element IDs, and navigation
- Use Jinja2 syntax for dynamic content, loops, and conditionals as specified
- Do NOT read or modify backend logic or data handling code
- Preserve all element IDs exactly as specified, including dynamic IDs like view-course-button-{course_id}

Implementation Guidelines:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Page Title from Section 2</title>
   </head>
   <body>
       <div id="main-container">
           <h1>Page Title from Section 2</h1>
           <!-- Page content here -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs**:
   - Use exact element IDs as specified, including dash-case and dynamic patterns
   - For repeated dynamic IDs, use Jinja2 syntax, e.g., id="view-course-button-{{ course.course_id }}"

3. **Navigation Links**:
   - Use url_for with exact function names from Section 2 for all buttons and links
   - For dynamic navigation, pass required parameters matching route definitions

4. **Forms and Inputs**:
   - Implement forms for assignment submissions and profile updates with proper method and action attributes
   - Use required attributes and input types as specified

5. **Conditionals and Loops**:
   - Use Jinja2 conditionals to handle enrolled status, button disabling, and data presence
   - Use for-loops to render course lists, assignments, certificates, and lessons

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files in templates/ directory
- All element IDs must match design_spec.md Section 2 exactly, including case-sensitive and dynamic patterns
- Page titles must match Section 2 exactly in both <title> and <h1>
- Navigation must use exact url_for functions as specified
- Do NOT implement backend logic or data file handling in templates
- Do NOT provide partial code in chat; always save complete files

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    }
}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Verify design_spec.md Section 1 (Flask routes) includes all specified routes with correct function names, HTTP methods, "
                "and context variables; Section 3 (data schemas) has accurate field orders and data formats matching requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify design_spec.md Section 2 (HTML templates) includes all element IDs exactly as specified, correct context variables, "
                "and navigation with proper url_for mappings.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("RequirementsAnalyst", """RequirementsAnalyst validates system_architect_final_review.txt to confirm system quality and agrees all requirements are fulfilled.""", [{'type': 'text_file', 'name': 'system_architect_final_review.txt'}, {'type': 'user', 'name': 'user_task_description'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Check app.py to confirm all Flask routes from design_spec.md Section 1 are implemented correctly, "
                "data handling respects schemas from Section 3, root route redirects to dashboard, and progress calculation logic matches requirements.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}]),
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify templates/*.html implement all element IDs and layout from design_spec.md Section 2 exactly, "
                "navigation uses correct url_for calls, and page titles are accurate.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}]),
    ],

    'RequirementsAnalyst': [
        ("SystemArchitect", """SystemArchitect checks requirements_analyst_review.txt for completeness and cross-validates with final implementation "
                "ensuring all user requirements are met and system is coherent.""", [{'type': 'text_file', 'name': 'requirements_analyst_review.txt'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Chaos Controller Setup ====================
chaos_controller = ChaosController(
    agent_chaos_enabled=False,
    stress_chaos_enabled=False,
    io_chaos_enabled=True,
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Start chaos experiment with 20% probability
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=0.2
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "stress_chaos",
    "probability": 0.2,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
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

print(f"Chaos scenario 'stress_chaos' activated with 20% probability")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create design_spec.md with Flask routes, HTML templates with detailed element IDs, and data schemas as per user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Declare BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )
    # Declare FrontendDeveloper agent
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=30
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py backend routes and business logic using design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement templates/*.html frontend templates using design_spec.md Section 2 with exact element IDs and navigation")
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
        parallel_implementation_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    
    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)

    # Save metrics to JSON
    task_metrics = aggregate_task_metrics(CONTEXT)
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
        print(f"\n  Received signal {signum}, saving metrics before exit...")
        try:
            task_metrics = aggregate_task_metrics(CONTEXT)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")

    # Write header
    log_file.write("=== Execution Log ===\n")
    log_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("\n=== OUTPUT ===\n")
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

        # Write summary
        log_file.write(f"\n\n=== Summary ===\n")
        log_file.write(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.close()
