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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect creates design_spec.md with detailed specifications for Flask routes, HTML templates, \"\n        \"data schemas, and UI element mappings to enable parallel backend and frontend development.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create detailed design specifications enabling Backend and Frontend developers to work independently and in parallel, producing a complete 'GymMembership' web application.\n\nTask Details:\n- Read user_task_description from CONTEXT thoroughly to understand app requirements, page designs, and data formats.\n- Produce design_spec.md containing comprehensive Flask routes, data schemas exactly matching data files, and detailed HTML template specs with all element IDs.\n- Output must support independent backend (Flask routes and data schema) and frontend (HTML templates and navigation) development.\n- Do NOT add features beyond the given requirements or assume extra functionalities.\n\n**Section 1: Flask Routes Specification**\n\n- List all routes for the 9 pages plus any root or auxiliary routes.\n- For each route specify:\n  - Route path (e.g., '/', '/memberships', '/plan/<int:plan_id>')\n  - Function name in lowercase with underscores\n  - HTTP method(s) (GET for page view; POST where needed for form submissions like booking or logging workouts)\n  - Template file to render\n  - Context variables passed to templates with precise names and types (str, int, list, dict, etc.)\n- Root route ('/') MUST redirect to the Dashboard page.\n- Include details for dynamic routes with parameter names.\n\n**Section 2: HTML Template Specifications**\n\n- Define an HTML template for each page with exact filename (e.g., dashboard.html, memberships.html).\n- Specify page titles matching user requirements exactly.\n- List all required element IDs with their element types and brief descriptions.\n- Detail context variables available in each template with access patterns (e.g., looping over list of plans).\n- Specify navigation elements and buttons including their IDs and linked routes using Flask url_for() function names.\n- Handle dynamic elements with example Jinja2 syntax for IDs with parameters ({plan_id}, {trainer_id}, etc.).\n\n**Section 3: Data File Schemas**\n\n- Specify for each data file:\n  - File path (data/filename.txt)\n  - Exact pipe-delimited field order matching user documentation\n  - Clear field names and types\n  - Short description of the file content\n  - 2-3 example data rows illustrating realistic content\n- Emphasize exact field order critical for backend parsing.\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developers can implement app.py with complete Flask routes and data loading using Section 1 and Section 3 only.\n- Frontend developers can implement all HTML templates using Section 2 only.\n- Element IDs and context variable names are consistent and exact across all sections.\n- Root route is implemented as a redirect to dashboard.\n- Use write_text_file tool to output design_spec.md\n- Do NOT include backend code or frontend HTML snippets in the prompt response; only spec.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 1 contains all Flask route definitions with correct function names, HTTP methods, and expected context variables. \"\n                \"Verify data schemas match the data formats and field orders exactly as specified. \"\n                \"Ensure root route redirects to Dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 2 specifies all HTML templates with exact element IDs and context variable usage. \"\n                \"Ensure navigation button IDs and page titles match user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend in parallel based on design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using Flask routes and data schemas from design_spec.md Section 1 and data formats. \"\n        \"FrontendDeveloper implements all HTML templates with specified element IDs and navigation from design_spec.md Section 2.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement complete Flask backend based on design specifications.\n\nTask Details:\n- Read design_spec.md Section 1 (Flask Routes) and data schemas from data formats in CONTEXT\n- Implement complete app.py with ALL Flask routes, HTTP methods, and root redirect to dashboard\n- Load and save data from text files using exact field orders as per data formats\n- DO NOT read frontend templates or assume anything beyond specs\n\nImplementation Requirements:\n1. **Flask App Setup**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root Route**:\n   - Implement '/' route that redirects to dashboard page\n   - Use: return redirect(url_for('dashboard'))\n\n3. **Data Handling**:\n   - Load data from data/*.txt files using pipe-delimited format\n   - Parse lines as: parts = line.strip().split('|')\n   - Map parts to fields EXACTLY as specified in data formats\n   - Provide saving capabilities if applicable (e.g., logging workouts, bookings)\n   - Include error handling for file I/O\n\n4. **Route Implementations**:\n   - Implement ALL routes specified in design_spec.md Section 1 with correct HTTP methods\n   - Use render_template with exact template names\n   - Pass precise context variables and types as per specs\n   - Handle POST requests to accept form data from booking and logging pages\n\n5. **Best Practices**:\n   - Use url_for for route references and redirects\n   - Include if __name__ == '__main__': app.run(debug=True, port=5000)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Function names and route paths must match design_spec.md exactly\n- Data file parsing must follow data schemas field order exactly\n- Root route MUST redirect to dashboard\n- Do NOT add features beyond specs\n- Do NOT output code only within chat, save all code with write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask applications.\n\nYour goal is to implement complete HTML templates based on design specifications.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) ONLY\n- Implement ALL HTML templates with specified element IDs, page titles, and navigation buttons\n- DO NOT read backend code or data schemas\n- Follow design_spec.md exactly for structure and navigation\n\nImplementation Requirements:\n1. **HTML Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title><!-- Page title from spec --></title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1><!-- Page title --></h1>\n           <!-- Content with specified element IDs -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs**:\n   - Include ALL element IDs exactly as specified (case-sensitive)\n   - For dynamic IDs like view-details-button-{plan_id}, use Jinja2 syntax:\n     id=\"view-details-button-{{ plan.plan_id }}\"\n\n3. **Page Titles**:\n   - Must exactly match specification in both <title> and <h1>\n\n4. **Context Variables & Rendering**:\n   - Use context variables as specified\n   - Use Jinja2 syntax for loops and conditionals:\n     {% for item in items %} ... {% endfor %}\n     {% if condition %} ... {% endif %}\n\n5. **Navigation Buttons / Links**:\n   - Implement navigation buttons using url_for references exactly as per spec\n   - Static buttons:\n     ```html\n     <a href=\"{{ url_for('function_name') }}\">\n       <button id=\"element-id\">Text</button>\n     </a>\n     ```\n   - Dynamic buttons:\n     ```html\n     <a href=\"{{ url_for('function_name', id=item.id) }}\">\n       <button id=\"element-id-{{ item.id }}\">Text</button>\n     </a>\n     ```\n\n6. **Form Handling** (for POST routes):\n   ```html\n   <form method=\"POST\" action=\"{{ url_for('function_name') }}\">\n       <input type=\"text\" name=\"field_name\" id=\"field-id\" required>\n       <button type=\"submit\" id=\"submit-button-id\">Submit</button>\n   </form>\n   ```\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all templates (*.html)\n- All element IDs must be exact and case-sensitive\n- Page titles must exactly match specifications\n- Navigation function names and parameters must match design_spec.md\n- Do NOT add templates or elements beyond specification\n- Do NOT output partial code only; save templates via write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Check app.py matches design_spec.md: all Flask routes implemented with correct HTTP methods, \"\n                \"data files loaded and saved using exact field orders, root redirection implemented.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Review all templates for correct element IDs, accurate page titles, proper rendering of context variables, \"\n                \"and correct navigation button url_for links as per design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create detailed design specifications enabling Backend and Frontend developers to work independently and in parallel, producing a complete 'GymMembership' web application.

Task Details:
- Read user_task_description from CONTEXT thoroughly to understand app requirements, page designs, and data formats.
- Produce design_spec.md containing comprehensive Flask routes, data schemas exactly matching data files, and detailed HTML template specs with all element IDs.
- Output must support independent backend (Flask routes and data schema) and frontend (HTML templates and navigation) development.
- Do NOT add features beyond the given requirements or assume extra functionalities.

**Section 1: Flask Routes Specification**

- List all routes for the 9 pages plus any root or auxiliary routes.
- For each route specify:
  - Route path (e.g., '/', '/memberships', '/plan/<int:plan_id>')
  - Function name in lowercase with underscores
  - HTTP method(s) (GET for page view; POST where needed for form submissions like booking or logging workouts)
  - Template file to render
  - Context variables passed to templates with precise names and types (str, int, list, dict, etc.)
- Root route ('/') MUST redirect to the Dashboard page.
- Include details for dynamic routes with parameter names.

**Section 2: HTML Template Specifications**

- Define an HTML template for each page with exact filename (e.g., dashboard.html, memberships.html).
- Specify page titles matching user requirements exactly.
- List all required element IDs with their element types and brief descriptions.
- Detail context variables available in each template with access patterns (e.g., looping over list of plans).
- Specify navigation elements and buttons including their IDs and linked routes using Flask url_for() function names.
- Handle dynamic elements with example Jinja2 syntax for IDs with parameters ({plan_id}, {trainer_id}, etc.).

**Section 3: Data File Schemas**

- Specify for each data file:
  - File path (data/filename.txt)
  - Exact pipe-delimited field order matching user documentation
  - Clear field names and types
  - Short description of the file content
  - 2-3 example data rows illustrating realistic content
- Emphasize exact field order critical for backend parsing.

CRITICAL SUCCESS CRITERIA:
- Backend developers can implement app.py with complete Flask routes and data loading using Section 1 and Section 3 only.
- Frontend developers can implement all HTML templates using Section 2 only.
- Element IDs and context variable names are consistent and exact across all sections.
- Root route is implemented as a redirect to dashboard.
- Use write_text_file tool to output design_spec.md
- Do NOT include backend code or frontend HTML snippets in the prompt response; only spec.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement complete Flask backend based on design specifications.

Task Details:
- Read design_spec.md Section 1 (Flask Routes) and data schemas from data formats in CONTEXT
- Implement complete app.py with ALL Flask routes, HTTP methods, and root redirect to dashboard
- Load and save data from text files using exact field orders as per data formats
- DO NOT read frontend templates or assume anything beyond specs

Implementation Requirements:
1. **Flask App Setup**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root Route**:
   - Implement '/' route that redirects to dashboard page
   - Use: return redirect(url_for('dashboard'))

3. **Data Handling**:
   - Load data from data/*.txt files using pipe-delimited format
   - Parse lines as: parts = line.strip().split('|')
   - Map parts to fields EXACTLY as specified in data formats
   - Provide saving capabilities if applicable (e.g., logging workouts, bookings)
   - Include error handling for file I/O

4. **Route Implementations**:
   - Implement ALL routes specified in design_spec.md Section 1 with correct HTTP methods
   - Use render_template with exact template names
   - Pass precise context variables and types as per specs
   - Handle POST requests to accept form data from booking and logging pages

5. **Best Practices**:
   - Use url_for for route references and redirects
   - Include if __name__ == '__main__': app.run(debug=True, port=5000)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Function names and route paths must match design_spec.md exactly
- Data file parsing must follow data schemas field order exactly
- Root route MUST redirect to dashboard
- Do NOT add features beyond specs
- Do NOT output code only within chat, save all code with write_text_file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask applications.

Your goal is to implement complete HTML templates based on design specifications.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) ONLY
- Implement ALL HTML templates with specified element IDs, page titles, and navigation buttons
- DO NOT read backend code or data schemas
- Follow design_spec.md exactly for structure and navigation

Implementation Requirements:
1. **HTML Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title><!-- Page title from spec --></title>
   </head>
   <body>
       <div id="main-container-id">
           <h1><!-- Page title --></h1>
           <!-- Content with specified element IDs -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs**:
   - Include ALL element IDs exactly as specified (case-sensitive)
   - For dynamic IDs like view-details-button-{plan_id}, use Jinja2 syntax:
     id="view-details-button-{{ plan.plan_id }}"

3. **Page Titles**:
   - Must exactly match specification in both <title> and <h1>

4. **Context Variables & Rendering**:
   - Use context variables as specified
   - Use Jinja2 syntax for loops and conditionals:
     {% for item in items %} ... {% endfor %}
     {% if condition %} ... {% endif %}

5. **Navigation Buttons / Links**:
   - Implement navigation buttons using url_for references exactly as per spec
   - Static buttons:
     ```html
     <a href="{{ url_for('function_name') }}">
       <button id="element-id">Text</button>
     </a>
     ```
   - Dynamic buttons:
     ```html
     <a href="{{ url_for('function_name', id=item.id) }}">
       <button id="element-id-{{ item.id }}">Text</button>
     </a>
     ```

6. **Form Handling** (for POST routes):
   ```html
   <form method="POST" action="{{ url_for('function_name') }}">
       <input type="text" name="field_name" id="field-id" required>
       <button type="submit" id="submit-button-id">Submit</button>
   </form>
   ```

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all templates (*.html)
- All element IDs must be exact and case-sensitive
- Page titles must exactly match specifications
- Navigation function names and parameters must match design_spec.md
- Do NOT add templates or elements beyond specification
- Do NOT output partial code only; save templates via write_text_file

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
        ("BackendDeveloper", """Verify design_spec.md Section 1 contains all Flask route definitions with correct function names, HTTP methods, and expected context variables. "
                "Verify data schemas match the data formats and field orders exactly as specified. "
                "Ensure root route redirects to Dashboard page.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify design_spec.md Section 2 specifies all HTML templates with exact element IDs and context variable usage. "
                "Ensure navigation button IDs and page titles match user requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Check app.py matches design_spec.md: all Flask routes implemented with correct HTTP methods, "
                "data files loaded and saved using exact field orders, root redirection implemented.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Review all templates for correct element IDs, accurate page titles, proper rendering of context variables, "
                "and correct navigation button url_for links as per design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Compound Chaos Controller Setup ====================
import random
from chaos.injectors import ChaosMode

# Compound Chaos: Per-task sampling
COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "prompt_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "io_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "prompt_probability": 0.2,
    "io_probability": 0.2
}

# ChaosMode mapping
MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["prompt_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Agent chaos is sampled with intensity
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

# Prompt/IO separately sampled at 0.2 probability (reset)
all_agents = list(AGENT_PROFILES.keys())
chaos_controller.stress_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["prompt_probability"]]
chaos_controller.io_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["io_probability"]]

# Guarantee at least 1
if not chaos_controller.stress_chaos_targets:
    chaos_controller.stress_chaos_targets = [random.choice(all_agents)]
if not chaos_controller.io_chaos_targets:
    chaos_controller.io_chaos_targets = [random.choice(all_agents)]

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "compound_config": COMPOUND_CONFIG,
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

print(f"Compound Chaos activated: Agent={COMPOUND_CONFIG['agent_intensity']}, Prompt={COMPOUND_CONFIG['prompt_method']}, IO={COMPOUND_CONFIG['io_method']}")
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
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create comprehensive design_spec.md with detailed Flask routes, HTML templates, and data schemas based on user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    # Create FrontendDeveloper agent
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement complete Flask backend app.py based on design_spec.md Section 1"),
        execute(FrontendDeveloper, "Implement all HTML templates with specified element IDs and navigation based on design_spec.md Section 2")
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
