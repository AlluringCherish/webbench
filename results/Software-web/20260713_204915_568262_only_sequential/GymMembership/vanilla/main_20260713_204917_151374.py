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
# 20260713_204917_151374/main_20260713_204917_151374.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the GymMembership requirements and produce a detailed design_spec.md outlining pages, elements, navigation, and data formats.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md detailing all pages, elements, and data storage; \"\n        \"then WebArchitect reads requirements_analysis.md and produces design_spec.md defining Flask routes, templates, page IDs, \"\n        \"navigation flows, data file use, and context variable contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in comprehensive web application requirements gathering.\n\nYour goal is to produce a thorough requirements_analysis.md document enumerating all pages, UI elements with their IDs, navigation flows, and local data file specifications based on user-provided task descriptions.\n\nTask Details:\n- Read user_task_description to identify all pages and their intended functions\n- Extract all UI elements with exact IDs per page\n- Detail navigation buttons and their target pages\n- Specify data storage files with exact fields and formats as provided\n- Generate requirements_analysis.md including above details for architect use\n\nRequirements Documentation:\n1. **Page and Element Enumeration**\n   - List each page by name and exact title\n   - For each page, detail all UI elements with their element IDs and types\n2. **Navigation Mapping**\n   - Specify all navigation buttons/links with source and destination pages\n3. **Data Storage Specification**\n   - Detail each data file: filename, field names and order, data format (pipe-delimited)\n   - Include sample data as examples\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save requirements_analysis.md\n- Preserve exact element IDs and data field orders from user requirements\n- Ensure clarity and completeness for WebArchitect's usage\n- No assumptions beyond given user_task_description\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design specifications.\n\nYour goal is to create a detailed design_spec.md document for the GymMembership Flask app, transforming requirements_analysis.md into comprehensive route-to-template mappings, page element IDs, navigation flows, data file formats, and context variable contracts suitable for independent backend and frontend development.\n\nTask Details:\n- Read requirements_analysis.md thoroughly and user_task_description for complete context\n- Produce design_spec.md including:\n  - Flask routes table mapping URLs to templates and handler function names\n  - Exact element IDs per page as defined in requirements_analysis.md\n  - Navigation mappings with button IDs directing to Flask routes\n  - Data file usage details: reading and writing methods, exact field order\n  - Context variable structures passed from routes to templates\n\nDesign Specification Structure:\n1. **Flask Routes**\n   - Define all routes starting with root '/' redirecting to Dashboard\n   - Include function names, HTTP methods, template files, and context variables with types\n2. **HTML Templates**\n   - Specify each template file under templates/, page titles, and all required element IDs with types\n   - Map navigation buttons to route functions with url_for calls\n3. **Data File Schemas**\n   - Specify data files under data/, pipe-delimited fields with exact orders and example data\n   - Clarify data loading and saving format expected in backend\n\nConsistency and Conventions:\n- Function names in snake_case matching page purposes\n- Context variable names consistent between routes and templates\n- Navigation flows must use exact button IDs and route names from specifications\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- Preserve all element IDs and data field orders exactly as in requirements_analysis.md\n- Ensure routes, templates, and data schemas enable independent backend/frontend implementations\n- Include sufficient detail to avoid ambiguities\n- Root route '/' must redirect to 'dashboard' route\n- Do NOT add features or pages not specified in requirements_analysis.md or user_task_description\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": \"Verify that requirements_analysis.md captures every page, element ID, navigation button, and data file structure exactly as requested without omissions.\",\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the GymMembership Flask application as app_draft.py and templates_draft/*.html consistent with design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes app_draft.py and all templates_draft/*.html following design_spec.md, implementing exact routes,\"\n        \"page titles, element IDs, local text-file data access, and navigation flows; IntegrationEngineer then refines these into final app.py and \"\n        \"templates/*.html, removing draft artifacts and ensuring readiness for validation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web application draft implementations.\n\nYour goal is to write the Flask application draft (app_draft.py) and all related HTML templates in the templates_draft/ directory, strictly following design_spec.md.\n\nTask Details:\n- Read design_spec.md and user_task_description from CONTEXT\n- Implement all Flask routes as specified in design_spec.md with exact function names\n- Use local plaintext data files (data/*.txt) as specified for data loading and saving\n- Implement HTML templates with all specified element IDs and page titles exactly\n- Ensure the root route '/' redirects or serves the Dashboard page as specified\n- Output app_draft.py and templates_draft/*.html files reflecting draft status but with full functionality\n\nImplementation Guidelines:\n1. Flask App Draft:\n   - Set up Flask app with required routes, handlers, and data file accesses\n   - Follow design_spec.md for precise route paths, HTTP methods, and context variables\n   - Use Python standard file I/O for reading/writing pipe-delimited text files\n   - Implement form handling for POST routes\n   - Maintain dashboard as root route\n\n2. HTML Templates Draft:\n   - Create full-featured HTML templates in templates_draft/ directory\n   - Use exact element IDs and page titles from design_spec.md\n   - Use Jinja2 templating syntax for context variables and loops\n   - Implement navigation buttons linking to Flask routes exactly\n   - Include draft indicators in filenames or comments to distinguish draft status\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_draft.py and all templates in templates_draft/\n- Must not add or omit routes or elements beyond design_spec.md specifications\n- Ensure data file reading/parsing matches design_spec.md field order exactly\n- Root route '/' must serve or redirect to Dashboard\n- Templates must include all specified element IDs exactly as per design_spec.md\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in finalizing Flask web applications.\n\nYour goal is to convert the draft Flask app (app_draft.py) and draft templates (templates_draft/*.html) into finalized, polished versions (app.py, templates/*.html) fully compliant with design_spec.md.\n\nTask Details:\n- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description from CONTEXT\n- Remove draft-specific artifacts, comments, or placeholders from code and templates\n- Refine and polish app.py and templates to match exact UI element IDs, route implementations, and page titles\n- Ensure data file access and parsing strictly follow design_spec.md schemas and formats\n- Enforce root Dashboard page as root route '/' with correct navigation\n- Produce clean, production-ready code and templates suitable for validation and deployment\n\nRefinement Guidelines:\n1. Flask App Finalization:\n   - Clean up draft artifacts and comments\n   - Verify all routes exist and use exact function names as per design_spec.md\n   - Confirm data file reading/writing matches specified field orders\n   - Optimize code readability and maintain functionality\n\n2. HTML Templates Finalization:\n   - Remove draft indicators, placeholders, and comments\n   - Verify all element IDs exist exactly as specified\n   - Confirm page titles and navigation links match design_spec.md exactly\n   - Ensure Jinja2 templating conforms to Flask usage standards\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save finalized app.py and templates/*.html\n- Ensure full compliance with design_spec.md UI element IDs, route names, and page titles\n- Maintain root route '/' as Dashboard page with correct navigation\n- Do not add functionality beyond design_spec.md requirements\n- Output must be clean and ready for validation testing\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": \"Check accuracy of app_draft.py and templates_draft/*.html against design_spec.md for route correctness, element IDs, data file handling, and navigation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and fix the final Flask application producing a fully runnable app.py and templates/*.html that meet all requirements.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator validates the final app.py and templates/*.html for runtime errors, route availability, data file accesses, and UI element presence, \"\n        \"then SequentialFixer applies corrections based on validation_report.md ensuring full functionality and compliance.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in validating Flask web applications.\n\nYour goal is to ensure the final Flask app.py and templates/*.html are fully functional, error-free, and meet all specified user requirements.\n\nTask Details:\n- Read design_spec.md, app.py, templates/*.html, and user_task_description from context\n- Produce a comprehensive validation_report.md detailing syntax/runtime errors, route existence, and UI element presence\n- Focus on runtime correctness of Flask app, availability of all required routes, and required UI elements on all pages\n\nValidation Objectives:\n1. **Syntax and Runtime Validation**:\n   - Use validate_python_file and execute_python_code tools to check app.py syntax and runtime\n   - Report detailed errors with file lines and messages\n\n2. **Route Verification**:\n   - Confirm all Flask routes from design_spec.md exist in app.py\n   - Test routes respond with status code 200 or appropriate redirects\n   - Verify root (/) route redirects to dashboard page\n\n3. **Template Content Verification**:\n   - Parse templates/*.html to ensure all requested HTML pages exist\n   - Verify all required element IDs are present on their corresponding pages\n   - Check that navigation elements and buttons match the specifications\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for all code checks\n- Use write_text_file tool to save detailed validation_report.md\n- Clearly state all detected issues and improvement suggestions\n- Validation report MUST enable SequentialFixer to accurately locate and fix problems\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask applications and frontend HTML templating.\n\nYour goal is to analyze validation_report.md and produce corrected app.py and templates/*.html that fully comply with GymMembership requirements and fix all identified issues.\n\nTask Details:\n- Read validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description from context\n- Implement fixes to app.py to resolve all runtime, routing, and data file access issues\n- Update templates/*.html to add missing UI elements, fix incorrect IDs, and correct navigation flows\n- Ensure the final outputs are fully functional and consistent with all design specifications and user requirements\n\nFix Implementation Guidelines:\n1. **Code Corrections**:\n   - Use write_text_file tool to save revised app.py\n   - Focus on fixing syntax, runtime errors, and missing or incorrect routes\n   - Verify data file accesses follow design_spec.md schema exactly\n\n2. **Template Updates**:\n   - Use write_text_file tool to save corrected templates/*.html files individually\n   - Include all required element IDs and correct page titles\n   - Match navigation and dynamic element naming as per design_spec.md\n\n3. **Consistency and Completeness**:\n   - Maintain naming consistency with design_spec.md and user requirements\n   - Ensure root route redirects to dashboard page\n   - Do not add functionality beyond original specifications\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively for output files\n- Preserve exact naming, ID conventions, and file structures per original design_spec.md\n- Deliver fully runnable Flask app with complete UI as per requirements\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": \"Ensure validation_report.md identifies all runtime, routing, and UI element inconsistencies for repair.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": \"Confirm that fixed app.py and templates/*.html fully implement the original user requirements and design specifications.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'GymMembership' Web Application

## 1. Objective
Develop a comprehensive web application named 'GymMembership' using Python, with data managed through local text files. The application enables users to browse membership plans, view class schedules, explore trainer profiles, book personal training sessions, and track workout records. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'GymMembership' application is Python.

## 3. Page Design

The 'GymMembership' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Gym Membership Dashboard
- **Overview**: The main hub displaying member highlights, featured classes, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: member-welcome** - Type: Div - Welcome section with member status information.
  - **ID: browse-membership-button** - Type: Button - Button to navigate to membership plans page.
  - **ID: view-schedule-button** - Type: Button - Button to navigate to class schedule page.
  - **ID: book-trainer-button** - Type: Button - Button to navigate to personal training booking page.

### 2. Membership Plans Page
- **Page Title**: Membership Plans
- **Overview**: A page displaying all available membership plans with details and pricing.
- **Elements**:
  - **ID: membership-page** - Type: Div - Container for the membership plans page.
  - **ID: plan-filter** - Type: Dropdown - Dropdown to filter by membership type (Basic, Premium, Elite).
  - **ID: plans-grid** - Type: Div - Grid displaying membership plan cards with name, price, and features.
  - **ID: view-details-button-{plan_id}** - Type: Button - Button to view plan details (each plan card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Plan Details Page
- **Page Title**: Plan Details
- **Overview**: A page displaying comprehensive information about a specific membership plan.
- **Elements**:
  - **ID: plan-details-page** - Type: Div - Container for the plan details page.
  - **ID: plan-title** - Type: H1 - Display plan name.
  - **ID: plan-price** - Type: Div - Display plan price and billing cycle.
  - **ID: plan-features** - Type: Div - Display all features included in the plan.
  - **ID: enroll-plan-button** - Type: Button - Button to enroll in the plan.
  - **ID: plan-reviews** - Type: Div - Section displaying member reviews of the plan.

### 4. Class Schedule Page
- **Page Title**: Class Schedule
- **Overview**: A page displaying fitness classes with time, duration, trainer, and capacity information.
- **Elements**:
  - **ID: schedule-page** - Type: Div - Container for the schedule page.
  - **ID: schedule-search** - Type: Input - Field to search classes by name or trainer.
  - **ID: schedule-filter** - Type: Dropdown - Dropdown to filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.).
  - **ID: classes-grid** - Type: Div - Grid displaying class cards with schedule and instructor.
  - **ID: enroll-class-button-{class_id}** - Type: Button - Button to enroll in class (each class card has this).

### 5. Trainer Profiles Page
- **Page Title**: Trainer Profiles
- **Overview**: A page displaying all available trainers with expertise, certifications, and specialties.
- **Elements**:
  - **ID: trainers-page** - Type: Div - Container for the trainers page.
  - **ID: trainer-search** - Type: Input - Field to search trainers by name or specialty.
  - **ID: specialty-filter** - Type: Dropdown - Dropdown to filter by specialty (Strength, Cardio, Flexibility, Weight Loss).
  - **ID: trainers-grid** - Type: Div - Grid displaying trainer cards with photo, name, and expertise.
  - **ID: view-trainer-button-{trainer_id}** - Type: Button - Button to view trainer profile (each trainer card has this).

### 6. Trainer Detail Page
- **Page Title**: Trainer Profile
- **Overview**: A page displaying detailed information about a specific trainer.
- **Elements**:
  - **ID: trainer-detail-page** - Type: Div - Container for the trainer detail page.
  - **ID: trainer-name** - Type: H1 - Display trainer name.
  - **ID: trainer-bio** - Type: Div - Display trainer biography and experience.
  - **ID: trainer-certifications** - Type: Div - Display trainer certifications.
  - **ID: book-session-button** - Type: Button - Button to book a session with this trainer.
  - **ID: trainer-reviews** - Type: Div - Section displaying reviews from clients.

### 7. PT Booking Page
- **Page Title**: Book Personal Training
- **Overview**: A page for users to schedule personal training sessions with trainers.
- **Elements**:
  - **ID: booking-page** - Type: Div - Container for the booking page.
  - **ID: select-trainer** - Type: Dropdown - Dropdown to select trainer.
  - **ID: session-date** - Type: Input (date) - Field to select session date.
  - **ID: session-time** - Type: Dropdown - Dropdown to select session time slot.
  - **ID: session-duration** - Type: Dropdown - Dropdown to select session duration (30, 60, 90 minutes).
  - **ID: confirm-booking-button** - Type: Button - Button to confirm booking.

### 8. Workout Records Page
- **Page Title**: My Workout Records
- **Overview**: A page displaying user's personal workout history and progress tracking.
- **Elements**:
  - **ID: workouts-page** - Type: Div - Container for the workouts page.
  - **ID: workouts-table** - Type: Table - Table displaying workout history with date, type, duration, and calories burned.
  - **ID: filter-by-type** - Type: Dropdown - Dropdown to filter workouts by type (Class, PT Session, Personal).
  - **ID: log-workout-button** - Type: Button - Button to log a new workout.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Log Workout Page
- **Page Title**: Log Workout
- **Overview**: A page for users to record their workout sessions and progress.
- **Elements**:
  - **ID: log-workout-page** - Type: Div - Container for the log workout page.
  - **ID: workout-type** - Type: Dropdown - Dropdown to select workout type (Cardio, Strength, Flexibility, Sports).
  - **ID: workout-duration** - Type: Input (number) - Field to input workout duration in minutes.
  - **ID: calories-burned** - Type: Input (number) - Field to input estimated calories burned.
  - **ID: workout-notes** - Type: Textarea - Field to add notes about the workout.
  - **ID: submit-workout-button** - Type: Button - Button to submit workout record.

## 4. Data Storage

The 'GymMembership' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Memberships Data
- **File Name**: `memberships.txt`
- **Data Format**:
  ```
  membership_id|plan_name|price|billing_cycle|features|max_classes
  ```
- **Example Data**:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Name**: `classes.txt`
- **Data Format**:
  ```
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
  ```
- **Example Data**:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Name**: `trainers.txt`
- **Data Format**:
  ```
  trainer_id|name|specialty|certifications|experience_years|bio
  ```
- **Example Data**:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
  ```
- **Example Data**:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Name**: `workouts.txt`
- **Data Format**:
  ```
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
  ```
- **Example Data**:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
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
            """You are a Requirements Analyst specializing in comprehensive web application requirements gathering.

Your goal is to produce a thorough requirements_analysis.md document enumerating all pages, UI elements with their IDs, navigation flows, and local data file specifications based on user-provided task descriptions.

Task Details:
- Read user_task_description to identify all pages and their intended functions
- Extract all UI elements with exact IDs per page
- Detail navigation buttons and their target pages
- Specify data storage files with exact fields and formats as provided
- Generate requirements_analysis.md including above details for architect use

Requirements Documentation:
1. **Page and Element Enumeration**
   - List each page by name and exact title
   - For each page, detail all UI elements with their element IDs and types
2. **Navigation Mapping**
   - Specify all navigation buttons/links with source and destination pages
3. **Data Storage Specification**
   - Detail each data file: filename, field names and order, data format (pipe-delimited)
   - Include sample data as examples

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save requirements_analysis.md
- Preserve exact element IDs and data field orders from user requirements
- Ensure clarity and completeness for WebArchitect's usage
- No assumptions beyond given user_task_description

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design specifications.

Your goal is to create a detailed design_spec.md document for the GymMembership Flask app, transforming requirements_analysis.md into comprehensive route-to-template mappings, page element IDs, navigation flows, data file formats, and context variable contracts suitable for independent backend and frontend development.

Task Details:
- Read requirements_analysis.md thoroughly and user_task_description for complete context
- Produce design_spec.md including:
  - Flask routes table mapping URLs to templates and handler function names
  - Exact element IDs per page as defined in requirements_analysis.md
  - Navigation mappings with button IDs directing to Flask routes
  - Data file usage details: reading and writing methods, exact field order
  - Context variable structures passed from routes to templates

Design Specification Structure:
1. **Flask Routes**
   - Define all routes starting with root '/' redirecting to Dashboard
   - Include function names, HTTP methods, template files, and context variables with types
2. **HTML Templates**
   - Specify each template file under templates/, page titles, and all required element IDs with types
   - Map navigation buttons to route functions with url_for calls
3. **Data File Schemas**
   - Specify data files under data/, pipe-delimited fields with exact orders and example data
   - Clarify data loading and saving format expected in backend

Consistency and Conventions:
- Function names in snake_case matching page purposes
- Context variable names consistent between routes and templates
- Navigation flows must use exact button IDs and route names from specifications

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Preserve all element IDs and data field orders exactly as in requirements_analysis.md
- Ensure routes, templates, and data schemas enable independent backend/frontend implementations
- Include sufficient detail to avoid ambiguities
- Root route '/' must redirect to 'dashboard' route
- Do NOT add features or pages not specified in requirements_analysis.md or user_task_description

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web application draft implementations.

Your goal is to write the Flask application draft (app_draft.py) and all related HTML templates in the templates_draft/ directory, strictly following design_spec.md.

Task Details:
- Read design_spec.md and user_task_description from CONTEXT
- Implement all Flask routes as specified in design_spec.md with exact function names
- Use local plaintext data files (data/*.txt) as specified for data loading and saving
- Implement HTML templates with all specified element IDs and page titles exactly
- Ensure the root route '/' redirects or serves the Dashboard page as specified
- Output app_draft.py and templates_draft/*.html files reflecting draft status but with full functionality

Implementation Guidelines:
1. Flask App Draft:
   - Set up Flask app with required routes, handlers, and data file accesses
   - Follow design_spec.md for precise route paths, HTTP methods, and context variables
   - Use Python standard file I/O for reading/writing pipe-delimited text files
   - Implement form handling for POST routes
   - Maintain dashboard as root route

2. HTML Templates Draft:
   - Create full-featured HTML templates in templates_draft/ directory
   - Use exact element IDs and page titles from design_spec.md
   - Use Jinja2 templating syntax for context variables and loops
   - Implement navigation buttons linking to Flask routes exactly
   - Include draft indicators in filenames or comments to distinguish draft status

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_draft.py and all templates in templates_draft/
- Must not add or omit routes or elements beyond design_spec.md specifications
- Ensure data file reading/parsing matches design_spec.md field order exactly
- Root route '/' must serve or redirect to Dashboard
- Templates must include all specified element IDs exactly as per design_spec.md

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in finalizing Flask web applications.

Your goal is to convert the draft Flask app (app_draft.py) and draft templates (templates_draft/*.html) into finalized, polished versions (app.py, templates/*.html) fully compliant with design_spec.md.

Task Details:
- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description from CONTEXT
- Remove draft-specific artifacts, comments, or placeholders from code and templates
- Refine and polish app.py and templates to match exact UI element IDs, route implementations, and page titles
- Ensure data file access and parsing strictly follow design_spec.md schemas and formats
- Enforce root Dashboard page as root route '/' with correct navigation
- Produce clean, production-ready code and templates suitable for validation and deployment

Refinement Guidelines:
1. Flask App Finalization:
   - Clean up draft artifacts and comments
   - Verify all routes exist and use exact function names as per design_spec.md
   - Confirm data file reading/writing matches specified field orders
   - Optimize code readability and maintain functionality

2. HTML Templates Finalization:
   - Remove draft indicators, placeholders, and comments
   - Verify all element IDs exist exactly as specified
   - Confirm page titles and navigation links match design_spec.md exactly
   - Ensure Jinja2 templating conforms to Flask usage standards

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save finalized app.py and templates/*.html
- Ensure full compliance with design_spec.md UI element IDs, route names, and page titles
- Maintain root route '/' as Dashboard page with correct navigation
- Do not add functionality beyond design_spec.md requirements
- Output must be clean and ready for validation testing

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in validating Flask web applications.

Your goal is to ensure the final Flask app.py and templates/*.html are fully functional, error-free, and meet all specified user requirements.

Task Details:
- Read design_spec.md, app.py, templates/*.html, and user_task_description from context
- Produce a comprehensive validation_report.md detailing syntax/runtime errors, route existence, and UI element presence
- Focus on runtime correctness of Flask app, availability of all required routes, and required UI elements on all pages

Validation Objectives:
1. **Syntax and Runtime Validation**:
   - Use validate_python_file and execute_python_code tools to check app.py syntax and runtime
   - Report detailed errors with file lines and messages

2. **Route Verification**:
   - Confirm all Flask routes from design_spec.md exist in app.py
   - Test routes respond with status code 200 or appropriate redirects
   - Verify root (/) route redirects to dashboard page

3. **Template Content Verification**:
   - Parse templates/*.html to ensure all requested HTML pages exist
   - Verify all required element IDs are present on their corresponding pages
   - Check that navigation elements and buttons match the specifications

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for all code checks
- Use write_text_file tool to save detailed validation_report.md
- Clearly state all detected issues and improvement suggestions
- Validation report MUST enable SequentialFixer to accurately locate and fix problems

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Backend Developer specializing in Flask applications and frontend HTML templating.

Your goal is to analyze validation_report.md and produce corrected app.py and templates/*.html that fully comply with GymMembership requirements and fix all identified issues.

Task Details:
- Read validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description from context
- Implement fixes to app.py to resolve all runtime, routing, and data file access issues
- Update templates/*.html to add missing UI elements, fix incorrect IDs, and correct navigation flows
- Ensure the final outputs are fully functional and consistent with all design specifications and user requirements

Fix Implementation Guidelines:
1. **Code Corrections**:
   - Use write_text_file tool to save revised app.py
   - Focus on fixing syntax, runtime errors, and missing or incorrect routes
   - Verify data file accesses follow design_spec.md schema exactly

2. **Template Updates**:
   - Use write_text_file tool to save corrected templates/*.html files individually
   - Include all required element IDs and correct page titles
   - Match navigation and dynamic element naming as per design_spec.md

3. **Consistency and Completeness**:
   - Maintain naming consistency with design_spec.md and user requirements
   - Ensure root route redirects to dashboard page
   - Do not add functionality beyond original specifications

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively for output files
- Preserve exact naming, ID conventions, and file structures per original design_spec.md
- Deliver fully runnable Flask app with complete UI as per requirements

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify that requirements_analysis.md captures every page, element ID, navigation button, and data file structure exactly as requested without omissions.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Check accuracy of app_draft.py and templates_draft/*.html against design_spec.md for route correctness, element IDs, data file handling, and navigation.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Ensure validation_report.md identifies all runtime, routing, and UI element inconsistencies for repair.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Confirm that fixed app.py and templates/*.html fully implement the original user requirements and design specifications.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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

    # Sequential Flow
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md detailing GymMembership pages, UI elements with exact IDs, navigation flows, and data file specifications.")

    # Read requirements_analysis.md content for WebArchitect input
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Using requirements_analysis.md content and user_task_description, produce design_spec.md with Flask routes, templates, element IDs, navigation mappings, data file formats, and context variable contracts.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
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
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential execution: DraftEngineer then IntegrationEngineer

    # DraftEngineer creates app_draft.py and templates_draft/*.html based on design_spec.md
    await execute(DraftEngineer,
                  "Implement app_draft.py and all templates in templates_draft/ strictly following design_spec.md. "
                  "Include exact routes, element IDs, page titles, and local data file handling. "
                  "Ensure root route '/' redirects or serves Dashboard page.")

    # Read outputs for IntegrationEngineer injection
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # Note: For multiple draft templates, read all and concatenate with separators
    import glob
    try:
        template_files = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for filepath in template_files:
            with open(filepath, "r") as f:
                templates_draft_content += f"=== {filepath} ===\n{f.read()}\n\n"
    except:
        pass

    # IntegrationEngineer refines draft into final app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Refine and polish app_draft.py and templates_draft/*.html into final app.py and templates/*.html fully compliant with design_spec.md. "
                  f"Remove draft artifacts and placeholders. Maintain exact route names and UI elements.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"{templates_draft_content}")
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
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )

    # Sequential execution
    # Step 1: WebValidator validates code and templates producing validation_report.md
    await execute(WebValidator,
                  "Validate app.py using validate_python_file and execute_python_code tools for syntax and runtime errors. "
                  "Verify all Flask routes from design_spec.md exist and respond correctly, including root route redirect. "
                  "Parse all templates/*.html to check presence of all required element IDs, page titles and navigation elements. "
                  "Write detailed validation_report.md describing all found issues and suggestions.")

    # Step 2: SequentialFixer fixes all issues from validation_report.md, updating app.py and templates/*.html
    # Read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    await execute(SequentialFixer,
                  f"Analyze validation_report.md and fix all reported issues in app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md and user requirements, including routing, UI elements, and data file access.\n\n"
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
