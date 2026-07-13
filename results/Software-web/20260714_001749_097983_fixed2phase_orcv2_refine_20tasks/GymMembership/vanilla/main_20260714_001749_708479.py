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
# 20260714_001749_708479/main_20260714_001749_708479.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create a detailed design specification document for the GymMembership web application's UI, page structure, element IDs, navigation flow, and data handling, delivering 'design_spec.md' and gated 'design_feedback.md'.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\"DesignGenerator writes 'design_spec.md' describing the full UI design, page layout with exact element IDs, navigation logic, and data storage format based on the user task. \"\n                                      \"DesignCritic reviews 'design_spec.md' against the user task and writes 'design_feedback.md' starting with [APPROVED] or NEED_MODIFY. \"\n                                      \"The loop iterates at most twice until approval or stopping after two iterations.\"),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application UI and data design.\n\nYour goal is to produce or revise a complete design specification document for the GymMembership web application, detailing all pages, UI element IDs, navigation flow, and local text file data format, guided by user requirements and critic feedback.\n\nTask Details:\n- Read user_task_description, the latest design_spec.md, and design_feedback.md from CONTEXT\n- On the first iteration, create a full design_spec.md covering page titles, element IDs, navigation, and data storage format\n- Upon feedback beginning with NEED_MODIFY, apply all corrections and completely rewrite design_spec.md\n- Upon feedback beginning with [APPROVED], preserve and finalize design_spec.md\n\n**Section 1: Page and UI Element Design**\n- Describe each page with its title and overview\n- Specify all UI elements precisely with their element IDs and types\n- Detail the navigation structure including buttons or links and their target pages\n\n**Section 2: Local Data Storage Format**\n- Specify file names, data schema, and field separators for the local text files managing membership, classes, trainers, bookings, and workouts\n- Provide example data records matching the schema\n\n**Section 3: Data and Navigation Consistency**\n- Ensure element IDs match across pages and navigation buttons connect valid targets\n- Verify data storage format aligns with UI elements displaying or modifying the data\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two Generator/Critic iterations until [APPROVED] or two revisions\n- Fully cover all nine specified pages and their detailed elements with exact IDs\n- Fully specify navigation logic and data text file layouts as per user task\n- Use write_text_file tool to output design_spec.md\n- Do not include any feedback marker in design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application UI and local data design.\n\nYour goal is to review the design_spec.md against the user requirements for GymMembership, ensuring completeness, correctness, consistency, and adherence; provide gated feedback starting with exactly [APPROVED] or NEED_MODIFY for up to two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Check coverage and correctness of all nine specified pages, their element IDs, and navigation flows\n- Verify data storage format correctness and alignment with UI design\n- Confirm no contradictions, missing pages, or navigation dead ends exist\n- Write feedback indexed by starting with [APPROVED] when design_spec.md fully meets requirements, or NEED_MODIFY followed by concrete correction instructions otherwise\n\nReview Criteria:\n1. All pages are fully described with required element IDs and types\n2. Navigation elements and flows are clearly specified and consistent\n3. Data files and their formats match user examples and usage described in UI\n4. Design matches user task scope and avoids additions or omissions\n5. Feedback begins exactly with [APPROVED] or NEED_MODIFY without prefixes\n\nCRITICAL REQUIREMENTS:\n- Feedback files must start with exact marker byte-1 sequences [APPROVED] or NEED_MODIFY\n- Save complete feedback text with write_text_file tool\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Check that design_spec.md fully covers all required pages, element IDs, navigation flows, data storage formats, and no contradictions or missing details.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Develop and refine the complete GymMembership web application with app.py and templates/*.html implementing all pages, exact element IDs, local text file data handling, starting from dashboard, delivering app.py, templates/*.html, and code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\"AppGenerator writes or revises app.py and templates/*.html implementing the GymMembership application following design_spec.md and addressing code_feedback.md. \"\n                                      \"CodeCritic reviews the implementation for correctness, element ID accuracy, navigation, and data handling consistency; produces code_feedback.md starting with [APPROVED] or NEED_MODIFY. \"\n                                      \"Iterations run at most twice until approval or stopping after two iterations.\"),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Web Developer specializing in building Flask web applications with local text file data handling.\n\nYour goal is to implement or revise a complete GymMembership web application including app.py and templates/*.html, following design_spec.md and incorporating any code_feedback.md, for up to two refinement iterations.\n\nTask Details:\n- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT.\n- On first iteration, produce the full implementation of app.py and all template files.\n- On code_feedback.md starting with NEED_MODIFY, carefully revise and overwrite all outputs applying all feedback.\n- On code_feedback.md starting with [APPROVED], maintain the approved implementation.\n- Output fully implemented and consistent app.py and templates/*.html files.\n\n**Implementation Requirements:**\n- Implement all nine pages exactly as specified: Dashboard, Membership Plans, Plan Details, Class Schedule, Trainer Profiles, Trainer Detail, PT Booking, Workout Records, Log Workout.\n- Use exact element IDs for each page element as specified in design_spec.md.\n- Implement navigation between pages via the specified buttons and links.\n- Handle data persistence entirely via local text files in the 'data' directory: memberships.txt, classes.txt, trainers.txt, bookings.txt, workouts.txt.\n- Ensure file reading and writing conform to provided data file formats.\n- Do not implement user authentication; all features are directly accessible.\n- The application must start at the Dashboard page.\n\n**Templates Implementation Details:**\n- Each template file corresponds to one page and must contain all required elements with specified IDs.\n- Include buttons, dropdowns, tables, inputs with the correct types and IDs.\n- Follow naming consistent with app.py route handlers.\n\n**Code Quality:**\n- Use concise, clear Python and HTML syntax.\n- Include comments using single-quote docstrings or hash comments only.\n- Apply robust local file parsing and writing utilities.\n- Prepare the app.py and templates for immediate testing.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and all templates/*.html.\n- Run at most two iterations; stop immediately if code_feedback.md begins with [APPROVED].\n- Do not add features beyond those described in design_spec.md.\n- Preserve exact element IDs and page navigation flows.\n- Overwrite app.py and all templates completely on NEED_MODIFY feedback.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python web application code and HTML template verification.\n\nYour goal is to review app.py and templates/*.html implementing the GymMembership application for correctness, adherence to design specifications, finish conditions, and produce gated feedback code_feedback.md for up to two refinement iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and all templates/*.html from CONTEXT.\n- Confirm all required page elements for the nine pages exist with exact element IDs as specified.\n- Verify navigation buttons and links enable correct page transitions.\n- Validate local text file data handling in app.py matches required format and functionality.\n- Check that no authentication is implemented and starting page is Dashboard.\n- Write feedback starting exactly with [APPROVED] if all criteria pass.\n- Otherwise start with NEED_MODIFY followed by explicit, actionable corrections.\n- Focus on structural correctness, element IDs, navigation consistency, data file usage, and user task compliance.\n- Do not add new feature requests or extraneous comments.\n\nReview Checklist:\n1. Page completeness: all pages present with required elements and IDs.\n2. Navigation correctness between pages via specified buttons.\n3. Accurate reading and writing to local text files with correct fields and formats.\n4. Starting the app at the Dashboard page.\n5. No authentication implemented.\n6. Correct code structure, no syntax errors.\n7. Feedback must enable AppGenerator to revise fully within two iterations.\n\nCRITICAL REQUIREMENTS:\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.\n- No additional formatting or decoration before this marker.\n- Use write_text_file tool to save code_feedback.md.\n- Limit review scope strictly to user task requirements and design_spec.md compliance.\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Gate implementation accuracy for app.py and templates/*.html based on design_spec.md, focusing on element ID correctness, page navigation, data storage, and completeness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application UI and data design.

Your goal is to produce or revise a complete design specification document for the GymMembership web application, detailing all pages, UI element IDs, navigation flow, and local text file data format, guided by user requirements and critic feedback.

Task Details:
- Read user_task_description, the latest design_spec.md, and design_feedback.md from CONTEXT
- On the first iteration, create a full design_spec.md covering page titles, element IDs, navigation, and data storage format
- Upon feedback beginning with NEED_MODIFY, apply all corrections and completely rewrite design_spec.md
- Upon feedback beginning with [APPROVED], preserve and finalize design_spec.md

**Section 1: Page and UI Element Design**
- Describe each page with its title and overview
- Specify all UI elements precisely with their element IDs and types
- Detail the navigation structure including buttons or links and their target pages

**Section 2: Local Data Storage Format**
- Specify file names, data schema, and field separators for the local text files managing membership, classes, trainers, bookings, and workouts
- Provide example data records matching the schema

**Section 3: Data and Navigation Consistency**
- Ensure element IDs match across pages and navigation buttons connect valid targets
- Verify data storage format aligns with UI elements displaying or modifying the data

CRITICAL SUCCESS CRITERIA:
- Run at most two Generator/Critic iterations until [APPROVED] or two revisions
- Fully cover all nine specified pages and their detailed elements with exact IDs
- Fully specify navigation logic and data text file layouts as per user task
- Use write_text_file tool to output design_spec.md
- Do not include any feedback marker in design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application UI and local data design.

Your goal is to review the design_spec.md against the user requirements for GymMembership, ensuring completeness, correctness, consistency, and adherence; provide gated feedback starting with exactly [APPROVED] or NEED_MODIFY for up to two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Check coverage and correctness of all nine specified pages, their element IDs, and navigation flows
- Verify data storage format correctness and alignment with UI design
- Confirm no contradictions, missing pages, or navigation dead ends exist
- Write feedback indexed by starting with [APPROVED] when design_spec.md fully meets requirements, or NEED_MODIFY followed by concrete correction instructions otherwise

Review Criteria:
1. All pages are fully described with required element IDs and types
2. Navigation elements and flows are clearly specified and consistent
3. Data files and their formats match user examples and usage described in UI
4. Design matches user task scope and avoids additions or omissions
5. Feedback begins exactly with [APPROVED] or NEED_MODIFY without prefixes

CRITICAL REQUIREMENTS:
- Feedback files must start with exact marker byte-1 sequences [APPROVED] or NEED_MODIFY
- Save complete feedback text with write_text_file tool

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Web Developer specializing in building Flask web applications with local text file data handling.

Your goal is to implement or revise a complete GymMembership web application including app.py and templates/*.html, following design_spec.md and incorporating any code_feedback.md, for up to two refinement iterations.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT.
- On first iteration, produce the full implementation of app.py and all template files.
- On code_feedback.md starting with NEED_MODIFY, carefully revise and overwrite all outputs applying all feedback.
- On code_feedback.md starting with [APPROVED], maintain the approved implementation.
- Output fully implemented and consistent app.py and templates/*.html files.

**Implementation Requirements:**
- Implement all nine pages exactly as specified: Dashboard, Membership Plans, Plan Details, Class Schedule, Trainer Profiles, Trainer Detail, PT Booking, Workout Records, Log Workout.
- Use exact element IDs for each page element as specified in design_spec.md.
- Implement navigation between pages via the specified buttons and links.
- Handle data persistence entirely via local text files in the 'data' directory: memberships.txt, classes.txt, trainers.txt, bookings.txt, workouts.txt.
- Ensure file reading and writing conform to provided data file formats.
- Do not implement user authentication; all features are directly accessible.
- The application must start at the Dashboard page.

**Templates Implementation Details:**
- Each template file corresponds to one page and must contain all required elements with specified IDs.
- Include buttons, dropdowns, tables, inputs with the correct types and IDs.
- Follow naming consistent with app.py route handlers.

**Code Quality:**
- Use concise, clear Python and HTML syntax.
- Include comments using single-quote docstrings or hash comments only.
- Apply robust local file parsing and writing utilities.
- Prepare the app.py and templates for immediate testing.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all templates/*.html.
- Run at most two iterations; stop immediately if code_feedback.md begins with [APPROVED].
- Do not add features beyond those described in design_spec.md.
- Preserve exact element IDs and page navigation flows.
- Overwrite app.py and all templates completely on NEED_MODIFY feedback.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python web application code and HTML template verification.

Your goal is to review app.py and templates/*.html implementing the GymMembership application for correctness, adherence to design specifications, finish conditions, and produce gated feedback code_feedback.md for up to two refinement iterations.

Task Details:
- Read design_spec.md, app.py, and all templates/*.html from CONTEXT.
- Confirm all required page elements for the nine pages exist with exact element IDs as specified.
- Verify navigation buttons and links enable correct page transitions.
- Validate local text file data handling in app.py matches required format and functionality.
- Check that no authentication is implemented and starting page is Dashboard.
- Write feedback starting exactly with [APPROVED] if all criteria pass.
- Otherwise start with NEED_MODIFY followed by explicit, actionable corrections.
- Focus on structural correctness, element IDs, navigation consistency, data file usage, and user task compliance.
- Do not add new feature requests or extraneous comments.

Review Checklist:
1. Page completeness: all pages present with required elements and IDs.
2. Navigation correctness between pages via specified buttons.
3. Accurate reading and writing to local text files with correct fields and formats.
4. Starting the app at the Dashboard page.
5. No authentication implemented.
6. Correct code structure, no syntax errors.
7. Feedback must enable AppGenerator to revise fully within two iterations.

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.
- No additional formatting or decoration before this marker.
- Use write_text_file tool to save code_feedback.md.
- Limit review scope strictly to user task requirements and design_spec.md compliance.

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Check that design_spec.md fully covers all required pages, element IDs, navigation flows, data storage formats, and no contradictions or missing details.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Gate implementation accuracy for app.py and templates/*.html based on design_spec.md, focusing on element ID correctness, page navigation, data storage, and completeness.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
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
            "Create or revise a complete design_spec.md for the GymMembership web app UI, page structure with exact element IDs, navigation flow, and data storage format.\n"
            f"User task description:\n{CONTEXT.get('user_task_description', '')}\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md for completeness, correctness, and consistency with user task for GymMembership UI design.\n"
            f"User task description:\n{CONTEXT.get('user_task_description', '')}\n\n"
            f"=== Latest design_spec.md ===\n{current_design}\n\n"
            "Write design_feedback.md starting exactly with [APPROVED] if fully correct or NEED_MODIFY with concrete corrections."
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=30
    )
    CodeCritic = build_resilient_agent(
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_code = ""
        templates_code = ""
        feedback_content = ""
        try:
            app_code = open("app.py").read()
        except FileNotFoundError:
            pass
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_code += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Implement or revise full app.py and all templates/*.html for the GymMembership web app.\n\n"
            f"=== design_spec.md ===\n{CONTENTS.get('design_spec.md','')}\n\n"
            f"=== Current app.py ===\n{app_code}\n\n"
            f"=== Current Templates ===\n{templates_code}\n\n"
            f"=== CodeCritic Feedback ===\n{feedback_content}"
        )

        try:
            app_code = open("app.py").read()
        except FileNotFoundError:
            app_code = ""
        templates_code = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_code += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates for correctness of GymMembership application implementation, element IDs, navigation, data handling, and adherence to design_spec.md.\n\n"
            f"=== design_spec.md ===\n{CONTENTS.get('design_spec.md','')}\n\n"
            f"=== Latest app.py ===\n{app_code}\n\n"
            f"=== Latest Templates ===\n{templates_code}"
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
