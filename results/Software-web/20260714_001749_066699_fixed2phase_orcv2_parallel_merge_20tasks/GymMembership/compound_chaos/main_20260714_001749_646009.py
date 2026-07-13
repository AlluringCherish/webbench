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
# 20260714_001749_646009/main_20260714_001749_646009.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend Flask design specifications and merge them into a unified design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect and FrontendDesignArchitect independently write their respective design sections based on the user task description; \"\n        \"DesignMerger consumes both design documents and user task to produce a consolidated design_spec.md with consistent backend and frontend contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend development and text-file data integration for web applications.\n\nYour goal is to design the complete Flask backend routes, data access logic, and interaction with local text files to support all GymMembership features and pages independently of the frontend design.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand all required pages and features\n- Create backend_design.md independently specifying all Flask routes, request handling logic, and data schemas\n- Specify exactly how local text files in the 'data' directory are read and written, including format and parsing rules\n- Do not read or assume frontend_design.md content\n\n**Section 1: Flask Routes Specification**\n- Define each route URL and HTTP methods\n- Specify route functions' behaviors and their connected templates\n- Declare the context variables passed to templates with names, types, and structures\n- Include all endpoints required by user features: dashboard, membership plans, plan details, class schedules, trainers, trainer detail, booking, workouts, and logging\n\n**Section 2: Data Storage and File Formats**\n- Specify file paths, text file formats (delimiter, fields), and schemas per the user task\n- Provide example lines for each data file to illustrate parsing expectations\n- Define reading and updating logic for bookings and workouts in text files\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can implement app.py solely from backend_design.md\n- Backend routes and data access cover full user feature set\n- Use write_text_file tool to output backend_design.md only\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML template design and frontend navigation for Flask web applications.\n\nYour goal is to design the full set of HTML templates, element IDs, navigation flows, and interactive UI elements required for all GymMembership pages independently of the backend design.\n\nTask Details:\n- Read user_task_description from CONTEXT to identify all pages, element IDs, and navigation paths\n- Create frontend_design.md independently specifying templates, page titles, required HTML elements with exact IDs and types\n- Describe necessary context variables expected from backend for dynamic content rendering\n- Define user interaction elements such as buttons, dropdowns, inputs, and their expected behavior and navigation\n- Do not read or assume backend_design.md content\n\n**Section 1: Template Structure and Elements**\n- Specify template file paths with page names and titles\n- List all page containers, buttons, inputs, dropdowns, tables, and other UI elements by ID and type\n- Define page navigation flows via buttons and links matching user task pages\n\n**Section 2: Context Variables Specification**\n- For each template, list variables and data structures required for dynamic rendering\n- Ensure variables correspond to user task features such as memberships, classes, trainers, bookings, and workouts\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement all templates (*.html) solely from frontend_design.md\n- All pages and interactive elements match user task page design and required element IDs\n- Use write_text_file tool to output frontend_design.md only\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in backend-frontend design integration for Flask web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md along with user_task_description into a single internally consistent design_spec.md that ensures full coverage and coherence of routes, templates, element IDs, context variables, data schemas, and navigation for the GymMembership application.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Analyze and reconcile routes, template references, context variables, data schemas, and page navigation flows for consistency\n- Resolve naming conflicts and unify design contracts without adding new features beyond the user description\n- Compose design_spec.md with structured sections addressing backend routes, data file schemas, frontend templates, and navigation\n\n**Section 1: Backend Routes and Data Access**\n- Consolidate route definitions, methods, and data access logic from backend_design.md\n- Ensure context variables match those expected by frontend_design.md templates\n\n**Section 2: Frontend Templates and UI Elements**\n- Consolidate templates, pages, element IDs, and UI controls from frontend_design.md\n- Ensure navigation elements align with backend routes\n\n**Section 3: Data File Format and Access**\n- Include canonical definitions of local text file schemas and their usage consistent with both designs\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper and FrontendDeveloper can implement from design_spec.md alone\n- All designs are consistent, complete, and reflect user_task_description fully\n- Use write_text_file tool to output design_spec.md only\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Merge backend design ensuring all backend endpoints and data access conform to user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Merge frontend design ensuring all pages, element IDs, and navigation match backend contracts and user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend Flask app and frontend templates from design_spec.md and merge into final app.py and HTML templates\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper and FrontendDeveloper independently implement the backend app.py and frontend HTML templates respectively using design_spec.md; \"\n        \"IntegrationMerger combines both implementations correcting interface inconsistencies and produces the canonical app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with local text file data management.\n\nYour goal is to implement the complete Flask backend for the GymMembership web application based on design_spec.md, including routes, business logic, and data handling.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Independently create app.py implementing all specified routes and logic\n- Manage all data access and updates via local text files as defined in design_spec.md\n- Do not read or assume frontend template implementation details or outputs\n\n**Implementation Requirements:**\n- Implement Flask routes matching design_spec.md specifications exactly\n- Implement reading and writing logic for memberships.txt, classes.txt, trainers.txt, bookings.txt, workouts.txt per design_spec.md schema\n- Implement business logic for browsing plans, viewing schedules, booking sessions, and recording workouts as described\n- Use clear function and variable names that align with design_spec.md context and route names\n- Handle input validation and error handling per web app best practices\n\n**File Output:**\n- Provide a single app.py Flask application source file\n- Use only local text file data storage under 'data/' directory consistent with design_spec.md data formats\n\nCRITICAL SUCCESS CRITERIA:\n- app.py fully implements backend routes and logic per design_spec.md\n- All declared input artifacts and output artifacts are respected without external assumptions\n- Use write_text_file tool exclusively to write app.py output\n- Do not include any frontend HTML or template code in this artifact\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask web applications.\n\nYour goal is to implement all HTML templates (*.html) for the GymMembership frontend based on the design_spec.md, including all pages, UI elements, and navigation.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Independently create HTML template files implementing all specified pages with required element IDs, buttons, navigation flows, and layout\n- Do not read or assume backend application code or outputs\n\n**Implementation Requirements:**\n- Implement templates for all nine pages as specified: Dashboard, Membership Plans, Plan Details, Class Schedule, Trainer Profiles, Trainer Detail, PT Booking, Workout Records, Log Workout\n- Use the specified element IDs exactly for all containers, inputs, buttons, tables, and dropdowns\n- Implement navigation buttons linking pages per design_spec.md requirements\n- Use Jinja2 templating syntax for dynamic content placeholders and control flow as implied by design_spec.md\n- Ensure frontend-only code; no backend logic or route implementations included\n\n**File Output:**\n- Provide HTML template files located in templates/ directory, with filename patterns matching each page\n- Use clean, readable HTML5 with embedded Jinja2 as appropriate\n\nCRITICAL SUCCESS CRITERIA:\n- templates/*.html accurately reflects all design_spec.md page layouts and element IDs\n- Adhere strictly to naming conventions and element IDs in design_spec.md\n- Use write_text_file tool exclusively for saving HTML templates\n- Output all required template files; no backend Python code included\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in harmonizing Flask backend and frontend template implementations.\n\nYour goal is to combine and reconcile the independently implemented app.py backend and templates/*.html frontend artifacts with design_spec.md to produce a consistent, final working GymMembership application.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify that backend routes and frontend templates align on route names, context variables, and element IDs\n- Resolve inconsistencies in route names, template names, navigation links, and variable references between backend and frontend\n- Merge app.py and templates/*.html into final canonical files without adding new requirements\n\n**Integration Requirements:**\n- Ensure all Flask routes in app.py correspond to frontend templates\n- Adjust template references and route URLs to maintain consistency per design_spec.md\n- Verify context data sent by backend matches placeholders in templates\n- Validate no missing elements or broken navigation links across the combined implementation\n- Preserve original function and file structures, applying only necessary harmonizing corrections\n\nCRITICAL SUCCESS CRITERIA:\n- Final app.py and templates/*.html are fully consistent, integratable, and implement the GymMembership system per design_spec.md\n- All naming and linkage issues resolved with no added functionalities\n- Exclusively use write_text_file tool for outputting final files\n- Output only app.py and templates/*.html as declared; no intermediate or refinement markers\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify backend app.py conforms to design_spec.md routes, data access, and logic correctness.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend templates/*.html conform to design_spec.md element IDs, navigation, and layout.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend development and text-file data integration for web applications.

Your goal is to design the complete Flask backend routes, data access logic, and interaction with local text files to support all GymMembership features and pages independently of the frontend design.

Task Details:
- Read user_task_description from CONTEXT to understand all required pages and features
- Create backend_design.md independently specifying all Flask routes, request handling logic, and data schemas
- Specify exactly how local text files in the 'data' directory are read and written, including format and parsing rules
- Do not read or assume frontend_design.md content

**Section 1: Flask Routes Specification**
- Define each route URL and HTTP methods
- Specify route functions' behaviors and their connected templates
- Declare the context variables passed to templates with names, types, and structures
- Include all endpoints required by user features: dashboard, membership plans, plan details, class schedules, trainers, trainer detail, booking, workouts, and logging

**Section 2: Data Storage and File Formats**
- Specify file paths, text file formats (delimiter, fields), and schemas per the user task
- Provide example lines for each data file to illustrate parsing expectations
- Define reading and updating logic for bookings and workouts in text files

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement app.py solely from backend_design.md
- Backend routes and data access cover full user feature set
- Use write_text_file tool to output backend_design.md only

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML template design and frontend navigation for Flask web applications.

Your goal is to design the full set of HTML templates, element IDs, navigation flows, and interactive UI elements required for all GymMembership pages independently of the backend design.

Task Details:
- Read user_task_description from CONTEXT to identify all pages, element IDs, and navigation paths
- Create frontend_design.md independently specifying templates, page titles, required HTML elements with exact IDs and types
- Describe necessary context variables expected from backend for dynamic content rendering
- Define user interaction elements such as buttons, dropdowns, inputs, and their expected behavior and navigation
- Do not read or assume backend_design.md content

**Section 1: Template Structure and Elements**
- Specify template file paths with page names and titles
- List all page containers, buttons, inputs, dropdowns, tables, and other UI elements by ID and type
- Define page navigation flows via buttons and links matching user task pages

**Section 2: Context Variables Specification**
- For each template, list variables and data structures required for dynamic rendering
- Ensure variables correspond to user task features such as memberships, classes, trainers, bookings, and workouts

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement all templates (*.html) solely from frontend_design.md
- All pages and interactive elements match user task page design and required element IDs
- Use write_text_file tool to output frontend_design.md only

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in backend-frontend design integration for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md along with user_task_description into a single internally consistent design_spec.md that ensures full coverage and coherence of routes, templates, element IDs, context variables, data schemas, and navigation for the GymMembership application.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Analyze and reconcile routes, template references, context variables, data schemas, and page navigation flows for consistency
- Resolve naming conflicts and unify design contracts without adding new features beyond the user description
- Compose design_spec.md with structured sections addressing backend routes, data file schemas, frontend templates, and navigation

**Section 1: Backend Routes and Data Access**
- Consolidate route definitions, methods, and data access logic from backend_design.md
- Ensure context variables match those expected by frontend_design.md templates

**Section 2: Frontend Templates and UI Elements**
- Consolidate templates, pages, element IDs, and UI controls from frontend_design.md
- Ensure navigation elements align with backend routes

**Section 3: Data File Format and Access**
- Include canonical definitions of local text file schemas and their usage consistent with both designs

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper and FrontendDeveloper can implement from design_spec.md alone
- All designs are consistent, complete, and reflect user_task_description fully
- Use write_text_file tool to output design_spec.md only

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with local text file data management.

Your goal is to implement the complete Flask backend for the GymMembership web application based on design_spec.md, including routes, business logic, and data handling.

Task Details:
- Read design_spec.md from CONTEXT
- Independently create app.py implementing all specified routes and logic
- Manage all data access and updates via local text files as defined in design_spec.md
- Do not read or assume frontend template implementation details or outputs

**Implementation Requirements:**
- Implement Flask routes matching design_spec.md specifications exactly
- Implement reading and writing logic for memberships.txt, classes.txt, trainers.txt, bookings.txt, workouts.txt per design_spec.md schema
- Implement business logic for browsing plans, viewing schedules, booking sessions, and recording workouts as described
- Use clear function and variable names that align with design_spec.md context and route names
- Handle input validation and error handling per web app best practices

**File Output:**
- Provide a single app.py Flask application source file
- Use only local text file data storage under 'data/' directory consistent with design_spec.md data formats

CRITICAL SUCCESS CRITERIA:
- app.py fully implements backend routes and logic per design_spec.md
- All declared input artifacts and output artifacts are respected without external assumptions
- Use write_text_file tool exclusively to write app.py output
- Do not include any frontend HTML or template code in this artifact

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask web applications.

Your goal is to implement all HTML templates (*.html) for the GymMembership frontend based on the design_spec.md, including all pages, UI elements, and navigation.

Task Details:
- Read design_spec.md from CONTEXT
- Independently create HTML template files implementing all specified pages with required element IDs, buttons, navigation flows, and layout
- Do not read or assume backend application code or outputs

**Implementation Requirements:**
- Implement templates for all nine pages as specified: Dashboard, Membership Plans, Plan Details, Class Schedule, Trainer Profiles, Trainer Detail, PT Booking, Workout Records, Log Workout
- Use the specified element IDs exactly for all containers, inputs, buttons, tables, and dropdowns
- Implement navigation buttons linking pages per design_spec.md requirements
- Use Jinja2 templating syntax for dynamic content placeholders and control flow as implied by design_spec.md
- Ensure frontend-only code; no backend logic or route implementations included

**File Output:**
- Provide HTML template files located in templates/ directory, with filename patterns matching each page
- Use clean, readable HTML5 with embedded Jinja2 as appropriate

CRITICAL SUCCESS CRITERIA:
- templates/*.html accurately reflects all design_spec.md page layouts and element IDs
- Adhere strictly to naming conventions and element IDs in design_spec.md
- Use write_text_file tool exclusively for saving HTML templates
- Output all required template files; no backend Python code included

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in harmonizing Flask backend and frontend template implementations.

Your goal is to combine and reconcile the independently implemented app.py backend and templates/*.html frontend artifacts with design_spec.md to produce a consistent, final working GymMembership application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify that backend routes and frontend templates align on route names, context variables, and element IDs
- Resolve inconsistencies in route names, template names, navigation links, and variable references between backend and frontend
- Merge app.py and templates/*.html into final canonical files without adding new requirements

**Integration Requirements:**
- Ensure all Flask routes in app.py correspond to frontend templates
- Adjust template references and route URLs to maintain consistency per design_spec.md
- Verify context data sent by backend matches placeholders in templates
- Validate no missing elements or broken navigation links across the combined implementation
- Preserve original function and file structures, applying only necessary harmonizing corrections

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html are fully consistent, integratable, and implement the GymMembership system per design_spec.md
- All naming and linkage issues resolved with no added functionalities
- Exclusively use write_text_file tool for outputting final files
- Output only app.py and templates/*.html as declared; no intermediate or refinement markers

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'BackendDesignArchitect': [
        ("DesignMerger", """Merge backend design ensuring all backend endpoints and data access conform to user requirements.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Merge frontend design ensuring all pages, element IDs, and navigation match backend contracts and user requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify backend app.py conforms to design_spec.md routes, data access, and logic correctness.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend templates/*.html conform to design_spec.md element IDs, navigation, and layout.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Create backend_design.md specifying all backend Flask routes, data schemas, and file access logic fully independently."),
        execute(FrontendDesignArchitect, "Create frontend_design.md specifying all HTML templates, element IDs, navigation flows, and UI elements fully independently.")
    )

    # Read backend_design.md and frontend_design.md outputs
    backend_design_content = ""
    frontend_design_content = ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge designs into unified design_spec.md
    await execute(
        DesignMerger,
        "Merge backend_design.md and frontend_design.md with user_task_description into a consistent design_spec.md with coherent routes, templates, context variables, data schemas, and navigation.\n\n"
        f"=== backend_design.md ===\n{backend_design_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_design_content}"
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement complete Flask backend app.py for GymMembership using design_spec.md, "
            "handling all routes, data files, and business logic exactly as specified."
        ),
        execute(
            FrontendDeveloper,
            "Implement all HTML templates (*.html) for GymMembership frontend with specified element IDs, "
            "navigation, and layouts per design_spec.md."
        )
    )

    # Read outputs for IntegrationMerger
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except Exception:
            pass

    # IntegrationMerger harmonizes backend and frontend
    await execute(
        IntegrationMerger,
        f"Combine and reconcile GymMembership backend app.py and frontend templates for consistency.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
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
