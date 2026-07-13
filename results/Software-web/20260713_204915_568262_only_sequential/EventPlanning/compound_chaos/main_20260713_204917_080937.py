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
# 20260713_204917_080937/main_20260713_204917_080937.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the user's EventPlanning web app requirements and produce a detailed design_spec.md covering all pages, navigation flow, and data representation.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first produces requirements_analysis.md with detailed page breakdown and data format mapping; \"\n        \"then WebArchitect reads requirements_analysis.md and user task to produce design_spec.md specifying Flask routes, templates, page structure, element IDs, \"\n        \"data files access, navigation actions, and initial format contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in web application requirements gathering and UI specifications.\n\nYour goal is to analyze the user task description and produce a comprehensive requirements_analysis.md capturing all UI pages, element IDs, data storage formats, and user workflows with detailed clarity.\n\nTask Details:\n- Read user_task_description thoroughly to understand application scope\n- Extract each page's name, page title, main elements with IDs and types\n- Detail navigation buttons and their targets clearly\n- Document all data file names, field orders, formats, and example data\n- Capture user workflows implied by navigation and actions\n\nRequirements Analysis Composition:\n1. **Page Specifications:** List all pages with UI elements and exact IDs/types\n2. **Navigation Flows:** Describe button/link navigation between pages\n3. **Data Formats:** Specify each data file's field order, format, and description\n4. **User Actions:** Outline main user actions and expected outcomes (e.g., ticket booking)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as requirements_analysis.md\n- Maintain exact element ID names and case sensitivity\n- Thoroughness and completeness are essential for next phase clarity\n- Focus only on analysis and documentation; no design or implementation yet\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design specifications.\n\nYour goal is to convert detailed requirements analysis into a precise design_spec.md that defines Flask routes, HTTP methods, template filenames, page titles, UI element IDs, navigation targets, and backend data file handling logic.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md carefully for complete context\n- Define exact Flask route names and HTTP methods per page and user actions\n- Specify template file names matching pages and roles\n- Document all element IDs and their page placements\n- Map navigation buttons to route functions explicitly\n- Outline initial backend data reading plans from local files per data schemas\n\nDesign Specification Sections:\n1. **Flask Routes:** Route path, function names (lowercase underscore), HTTP methods, templates, context variables\n2. **HTML Templates:** Template filenames, page titles, element IDs, navigation actions\n3. **Data Files:** Files accessed, format details, fields order, example data references\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_spec.md\n- Ensure consistency of naming conventions across routes, templates, and navigation\n- All element IDs must match exactly from analysis phase\n- Focus on accuracy to enable seamless parallel backend/frontend development\n- Do not provide code implementations, only detailed specifications\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md accurately and comprehensively covers all user-visible pages, UI element IDs, navigation links, \"\n                \"and exact data file schema details before design_spec.md creation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the EventPlanning Flask web app with a runnable app.py and all required templates/*.html files, fully respecting the design_spec.md and user requirements.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationAgent first creates app_draft.py and templates_draft/*.html based on design_spec.md; after drafting, IntegrationAgent refines and integrates drafts \"\n        \"into final app.py and templates/*.html ready for execution, enforcing exact routes, element IDs, data file interactions, and navigation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationAgent\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web application development with expertise in local text file data handling.\n\nYour goal is to create a complete draft of the Flask backend app_draft.py and all frontend templates_draft/*.html files that implement the web app structure, routes, HTTP methods, rendering via render_template, specified element IDs, and backend data handling strictly according to design_spec.md and user requirements.\n\nTask Details:\n- Read user_task_description and design_spec.md thoroughly\n- Create app_draft.py with all required Flask routes, methods, and data reading/writing logic for local text files as specified\n- Implement all HTML draft templates in templates_draft/ using exact element IDs, page titles, and navigation details from design_spec.md\n- Focus on draft completeness and functionality; placeholders are allowed but the structure must be full\n- Include all specified pages: dashboard, events listing, event details, ticket booking, participants management, venue info, schedules, bookings summary\n\nImplementation Guidelines:\n1. Flask Application:\n   - Configure Flask instance with SECRET_KEY set to 'dev-secret-key'\n   - Implement route for '/' redirecting to dashboard page\n   - For each page route, use render_template with correct template filename inside templates_draft/\n   - Use request.form for POST data handling when booking tickets or adding participants\n   - Parse and manipulate data files in the data/ directory using pipe '|' delimited splitting matching field order and names\n   - Implement error handling for file operations gracefully\n\n2. Templates:\n   - Save all templates as templates_draft/{page}.html with exact element IDs as specified\n   - Use Jinja2 syntax for dynamic IDs, loops, and conditionals consistent with data passed from backend\n   - Match page titles exactly as specified in user_task_description\n   - Map navigation buttons to appropriate routes using url_for as per design_spec.md details\n\n3. Backend-Frontend Interface:\n   - Pass context variables matching design_spec.md expectations for each template rendering\n   - Maintain naming consistency for variables across backend and templates\n   - Ensure all specified UI elements (buttons, inputs, tables, dropdowns) are present with correct IDs\n\n4. Code Quality:\n   - Organize code cleanly with comments describing each route and major functionality\n   - Provide stubbed or example implementations where necessary but ensure app_draft.py runs without errors\n   - Use write_text_file tool to save app_draft.py and each template file in templates_draft/\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save all output files\n- Preserve exact element IDs and file paths as given, using templates_draft/ directory\n- Follow data file schemas and field orders exactly for reading and writing\n- Do NOT finalize or integrate code; this is a draft stage for integration later\n- Output: app_draft.py and templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationAgent\",\n            \"prompt\": \"\"\"You are a Senior Flask Developer specializing in integrating and finalizing Flask applications with frontend templates and ensuring full compliance with specifications.\n\nYour goal is to integrate the draft backend app_draft.py and draft templates templates_draft/*.html into a final runnable Flask application app.py and finalized templates/*.html files. You must remove draft placeholders, fix broken links and references, and ensure precise implementation of all routes, element IDs, and proper data handling from local text files as specified.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_draft.py, and all templates_draft/*.html files\n- Integrate and refactor code to produce a clean, consistent, and complete final app.py\n- Clean up templates by removing draft markers and fixing all dynamic elements\n- Save all finalized templates in templates/ directory with exact file names\n- Validate that all routes exist and map to correct template renders with proper context variables\n- Ensure element IDs, navigation, and data interaction strictly match user requirements and design_spec.md\n\nIntegration Requirements:\n1. Backend Integration:\n   - Consolidate all route handlers from app_draft.py into app.py\n   - Remove drafts, commented-out code, and incomplete placeholders\n   - Verify all data loading/writing matches data schema and parsing instructions\n   - Implement robust error handling and input validation where applicable\n   - Ensure root route '/' redirects to dashboard\n\n2. Templates Finalization:\n   - Transfer and finalize all templates removing draft annotations\n   - Verify all element IDs are present and unique per page as specified\n   - Correct all hyperlinks and form actions to use proper url_for calls\n   - Ensure consistency in Jinja2 variable usage and loops matching backend data\n\n3. Testing and Validation:\n   - Perform a functional check that app.py runs without errors\n   - Verify navigation flows correctly between all pages\n   - Confirm data from local text files loads and displays properly on templates\n   - Validate all UI elements are present and functional per specification\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app.py and all templates/*.html\n- Preserve exact element IDs, filenames, and data interaction as specified\n- Final code must be fully runnable without draft placeholders or missing functionality\n- Maintain naming and routing conventions per design_spec.md and user_task_description\n- Output: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"ImplementationAgent\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"ImplementationAgent\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationAgent\",\n            \"reviewer_agent\": \"IntegrationAgent\",\n            \"review_criteria\": (\n                \"Ensure app_draft.py and templates_draft/*.html conform fully to design_spec.md and contain all required pages and UI elements \"\n                \"before integration into final app.py and templates.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the final app.py and templates/*.html for syntax, runtime execution, and adherence to the design_spec.md; produce validation_report.md and corrected final files.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ValidatorAgent first runs static and dynamic validation checks on app.py and templates/*.html and writes validation_report.md; \"\n        \"FixerAgent applies corrections based on report to finalize the app.py and templates.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidatorAgent\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specialized in Python Flask web applications and frontend HTML templating.\n\nYour goal is to validate the syntax, runtime behavior, and correctness of the backend app.py and frontend templates/*.html files to ensure full compliance with the design_spec.md specifications.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html from CONTEXT\n- Produce validation_report.md outlining all errors, missing routes, incorrect element IDs, broken navigation, and data handling issues\n- Focus on verifying exact route availability, template rendering correctness, presence of all required element IDs, functional navigation buttons, and proper local data file access\n\nValidation Steps:\n1. **Backend Syntax and Runtime Validation**\n   - Use validate_python_file tool on app.py for syntax and runtime checks\n   - Execute key routes to verify they return correct HTTP status codes and render templates without error\n2. **Route and Function Validation**\n   - Ensure all routes specified in design_spec.md exist in app.py with correct function names and HTTP methods\n3. **Template Integrity Checks**\n   - Parse templates/*.html to confirm existence of all requested element IDs from design_spec.md page designs\n   - Verify navigation buttons include correct url_for mappings matching backend routes\n4. **Data File Access Verification**\n   - Confirm app.py reads all required data files with the exact field order as per design_spec.md schemas\n5. **Error and Issue Reporting**\n   - Document all discrepancies, syntax/runtime errors, missing elements, navigation failures, data misalignments\n   - Format validation_report.md with clear sections and actionable items\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools for all code validations\n- MUST write validation_report.md using write_text_file tool\n- MUST identify all missing or incorrect routes, template issues, navigation link problems, and data file handling defects\n- Use positive, actionable language in the report\n- Focus exclusively on files and specifications listed in input artifacts\n- Do NOT provide fixes or corrections in this phase, only detailed validation findings\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationAgent\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationAgent\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FixerAgent\",\n            \"prompt\": \"\"\"You are a Software Developer specialized in Python Flask backend and HTML templating for web applications.\n\nYour goal is to apply necessary corrections to app.py and templates/*.html based on validation_report.md to achieve full compliance with design_spec.md and pass all validation checks.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, and validation_report.md from CONTEXT\n- Apply all fixes required to resolve discrepancies, syntax/runtime errors, missing elements, navigation errors, and data handling defects reported\n- Output corrected app.py and templates/*.html reflecting all necessary improvements\n\nCorrection Requirements:\n1. **Backend Corrections**\n   - Fix syntax and runtime errors detected by validator\n   - Ensure all routes and function definitions comply exactly with design_spec.md\n   - Correct data file reading routines to match field order and access patterns\n2. **Template Fixes**\n   - Add or correct missing element IDs and ensure exact naming from design_spec.md\n   - Repair navigation controls to use correct url_for targets matching backend routes\n   - Ensure template rendering is seamless without errors\n3. **Verification**\n   - Double-check all changes against the validation_report.md instructions\n   - Produce final artifacts ready for successful validation with no outstanding issues\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save corrected app.py and all templates/*.html files\n- MUST ensure final artifacts fully address all reported issues comprehensively\n- MUST maintain feature completeness as per user requirements and design_spec.md\n- Do NOT introduce new features or unrelated changes beyond fixes indicated\n- Submit only corrected files named exactly as input artifacts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationAgent\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationAgent\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"ValidatorAgent\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidatorAgent\",\n            \"reviewer_agent\": \"FixerAgent\",\n            \"review_criteria\": (\n                \"Verify validation_report.md thoroughly identifies all missing or incorrect route handlers, elements, navigation, and data handling \"\n                \"issues before fixes are applied.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FixerAgent\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Confirm that final app.py and templates/*.html fully address the validation report and retain full feature coverage of user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'EventPlanning' Web Application

## 1. Objective
Develop a comprehensive web application named 'EventPlanning' using Python, with data managed through local text files. The application enables users to browse events, book tickets, view venue information, manage participants, and explore event schedules. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'EventPlanning' application is Python.

## 3. Page Design

The 'EventPlanning' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Event Planning Dashboard
- **Overview**: The main hub displaying upcoming events, featured venues, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-events** - Type: Div - Display of featured event recommendations.
  - **ID: browse-events-button** - Type: Button - Button to navigate to events listing page.
  - **ID: view-tickets-button** - Type: Button - Button to navigate to tickets page.
  - **ID: venues-button** - Type: Button - Button to navigate to venues page.

### 2. Events Listing Page
- **Page Title**: Events Catalog
- **Overview**: A page displaying all available events with search and filter capabilities.
- **Elements**:
  - **ID: events-page** - Type: Div - Container for the events listing page.
  - **ID: event-search-input** - Type: Input - Field to search events by name, location, or date.
  - **ID: event-category-filter** - Type: Dropdown - Dropdown to filter by category (Conference, Concert, Sports, Workshop, Social).
  - **ID: events-grid** - Type: Div - Grid displaying event cards with image, title, date, and location.
  - **ID: view-event-button-{event_id}** - Type: Button - Button to view event details (each event card has this).

### 3. Event Details Page
- **Page Title**: Event Details
- **Overview**: A page displaying detailed information about a specific event.
- **Elements**:
  - **ID: event-details-page** - Type: Div - Container for the event details page.
  - **ID: event-title** - Type: H1 - Display event title.
  - **ID: event-date** - Type: Div - Display event date and time.
  - **ID: event-location** - Type: Div - Display event location.
  - **ID: event-description** - Type: Div - Display detailed event description.
  - **ID: book-ticket-button** - Type: Button - Button to book ticket for this event.

### 4. Ticket Booking Page
- **Page Title**: Book Your Tickets
- **Overview**: A page for users to select and book tickets for events.
- **Elements**:
  - **ID: ticket-booking-page** - Type: Div - Container for the ticket booking page.
  - **ID: select-event-dropdown** - Type: Dropdown - Dropdown to select event to book tickets.
  - **ID: ticket-quantity-input** - Type: Input (number) - Field to enter number of tickets.
  - **ID: ticket-type-select** - Type: Dropdown - Dropdown to select ticket type (General, VIP, Early Bird).
  - **ID: book-now-button** - Type: Button - Button to proceed with ticket booking.
  - **ID: booking-confirmation** - Type: Div - Display booking confirmation details.

### 5. Participants Management Page
- **Page Title**: Participants Management
- **Overview**: A page for managing event participants and attendee lists.
- **Elements**:
  - **ID: participants-page** - Type: Div - Container for the participants management page.
  - **ID: participants-table** - Type: Table - Table displaying participants with name, email, event, and status.
  - **ID: add-participant-button** - Type: Button - Button to add new participant.
  - **ID: search-participant-input** - Type: Input - Field to search participants by name or email.
  - **ID: participant-status-filter** - Type: Dropdown - Dropdown to filter by status (Registered, Confirmed, Attended).

### 6. Venue Information Page
- **Page Title**: Venues
- **Overview**: A page displaying available venues for events with detailed information.
- **Elements**:
  - **ID: venues-page** - Type: Div - Container for the venues page.
  - **ID: venues-grid** - Type: Div - Grid displaying venue cards with name, capacity, and amenities.
  - **ID: venue-search-input** - Type: Input - Field to search venues by name or location.
  - **ID: venue-capacity-filter** - Type: Dropdown - Dropdown to filter by capacity (Small, Medium, Large).
  - **ID: view-venue-details-{venue_id}** - Type: Button - Button to view venue details (each venue card has this).

### 7. Event Schedules Page
- **Page Title**: Event Schedules
- **Overview**: A page displaying event schedules, timelines, and agenda information.
- **Elements**:
  - **ID: schedules-page** - Type: Div - Container for the schedules page.
  - **ID: schedules-timeline** - Type: Div - Timeline view of upcoming events and sessions.
  - **ID: schedule-filter-date** - Type: Input (date) - Field to filter schedules by date.
  - **ID: schedule-filter-event** - Type: Dropdown - Dropdown to filter by event.
  - **ID: export-schedule-button** - Type: Button - Button to export schedule data.

### 8. Bookings Summary Page
- **Page Title**: My Bookings
- **Overview**: A page displaying all user bookings with ticket information and booking status.
- **Elements**:
  - **ID: bookings-page** - Type: Div - Container for the bookings page.
  - **ID: bookings-table** - Type: Table - Table displaying bookings with event, date, ticket count, and status.
  - **ID: booking-search-input** - Type: Input - Field to search bookings by event name or booking ID.
  - **ID: cancel-booking-button-{booking_id}** - Type: Button - Button to cancel booking (each booking has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'EventPlanning' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Events Data
- **File Name**: `events.txt`
- **Data Format**:
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- **Example Data**:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- **File Name**: `venues.txt`
- **Data Format**:
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- **Example Data**:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- **File Name**: `tickets.txt`
- **Data Format**:
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- **Example Data**:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- **File Name**: `participants.txt`
- **Data Format**:
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- **File Name**: `schedules.txt`
- **Data Format**:
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- **Example Data**:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
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
            """You are a Business Analyst specializing in web application requirements gathering and UI specifications.

Your goal is to analyze the user task description and produce a comprehensive requirements_analysis.md capturing all UI pages, element IDs, data storage formats, and user workflows with detailed clarity.

Task Details:
- Read user_task_description thoroughly to understand application scope
- Extract each page's name, page title, main elements with IDs and types
- Detail navigation buttons and their targets clearly
- Document all data file names, field orders, formats, and example data
- Capture user workflows implied by navigation and actions

Requirements Analysis Composition:
1. **Page Specifications:** List all pages with UI elements and exact IDs/types
2. **Navigation Flows:** Describe button/link navigation between pages
3. **Data Formats:** Specify each data file's field order, format, and description
4. **User Actions:** Outline main user actions and expected outcomes (e.g., ticket booking)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as requirements_analysis.md
- Maintain exact element ID names and case sensitivity
- Thoroughness and completeness are essential for next phase clarity
- Focus only on analysis and documentation; no design or implementation yet

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

Your goal is to convert detailed requirements analysis into a precise design_spec.md that defines Flask routes, HTTP methods, template filenames, page titles, UI element IDs, navigation targets, and backend data file handling logic.

Task Details:
- Read user_task_description and requirements_analysis.md carefully for complete context
- Define exact Flask route names and HTTP methods per page and user actions
- Specify template file names matching pages and roles
- Document all element IDs and their page placements
- Map navigation buttons to route functions explicitly
- Outline initial backend data reading plans from local files per data schemas

Design Specification Sections:
1. **Flask Routes:** Route path, function names (lowercase underscore), HTTP methods, templates, context variables
2. **HTML Templates:** Template filenames, page titles, element IDs, navigation actions
3. **Data Files:** Files accessed, format details, fields order, example data references

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Ensure consistency of naming conventions across routes, templates, and navigation
- All element IDs must match exactly from analysis phase
- Focus on accuracy to enable seamless parallel backend/frontend development
- Do not provide code implementations, only detailed specifications

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationAgent": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web application development with expertise in local text file data handling.

Your goal is to create a complete draft of the Flask backend app_draft.py and all frontend templates_draft/*.html files that implement the web app structure, routes, HTTP methods, rendering via render_template, specified element IDs, and backend data handling strictly according to design_spec.md and user requirements.

Task Details:
- Read user_task_description and design_spec.md thoroughly
- Create app_draft.py with all required Flask routes, methods, and data reading/writing logic for local text files as specified
- Implement all HTML draft templates in templates_draft/ using exact element IDs, page titles, and navigation details from design_spec.md
- Focus on draft completeness and functionality; placeholders are allowed but the structure must be full
- Include all specified pages: dashboard, events listing, event details, ticket booking, participants management, venue info, schedules, bookings summary

Implementation Guidelines:
1. Flask Application:
   - Configure Flask instance with SECRET_KEY set to 'dev-secret-key'
   - Implement route for '/' redirecting to dashboard page
   - For each page route, use render_template with correct template filename inside templates_draft/
   - Use request.form for POST data handling when booking tickets or adding participants
   - Parse and manipulate data files in the data/ directory using pipe '|' delimited splitting matching field order and names
   - Implement error handling for file operations gracefully

2. Templates:
   - Save all templates as templates_draft/{page}.html with exact element IDs as specified
   - Use Jinja2 syntax for dynamic IDs, loops, and conditionals consistent with data passed from backend
   - Match page titles exactly as specified in user_task_description
   - Map navigation buttons to appropriate routes using url_for as per design_spec.md details

3. Backend-Frontend Interface:
   - Pass context variables matching design_spec.md expectations for each template rendering
   - Maintain naming consistency for variables across backend and templates
   - Ensure all specified UI elements (buttons, inputs, tables, dropdowns) are present with correct IDs

4. Code Quality:
   - Organize code cleanly with comments describing each route and major functionality
   - Provide stubbed or example implementations where necessary but ensure app_draft.py runs without errors
   - Use write_text_file tool to save app_draft.py and each template file in templates_draft/

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save all output files
- Preserve exact element IDs and file paths as given, using templates_draft/ directory
- Follow data file schemas and field orders exactly for reading and writing
- Do NOT finalize or integrate code; this is a draft stage for integration later
- Output: app_draft.py and templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationAgent": {
        "prompt": (
            """You are a Senior Flask Developer specializing in integrating and finalizing Flask applications with frontend templates and ensuring full compliance with specifications.

Your goal is to integrate the draft backend app_draft.py and draft templates templates_draft/*.html into a final runnable Flask application app.py and finalized templates/*.html files. You must remove draft placeholders, fix broken links and references, and ensure precise implementation of all routes, element IDs, and proper data handling from local text files as specified.

Task Details:
- Read user_task_description, design_spec.md, app_draft.py, and all templates_draft/*.html files
- Integrate and refactor code to produce a clean, consistent, and complete final app.py
- Clean up templates by removing draft markers and fixing all dynamic elements
- Save all finalized templates in templates/ directory with exact file names
- Validate that all routes exist and map to correct template renders with proper context variables
- Ensure element IDs, navigation, and data interaction strictly match user requirements and design_spec.md

Integration Requirements:
1. Backend Integration:
   - Consolidate all route handlers from app_draft.py into app.py
   - Remove drafts, commented-out code, and incomplete placeholders
   - Verify all data loading/writing matches data schema and parsing instructions
   - Implement robust error handling and input validation where applicable
   - Ensure root route '/' redirects to dashboard

2. Templates Finalization:
   - Transfer and finalize all templates removing draft annotations
   - Verify all element IDs are present and unique per page as specified
   - Correct all hyperlinks and form actions to use proper url_for calls
   - Ensure consistency in Jinja2 variable usage and loops matching backend data

3. Testing and Validation:
   - Perform a functional check that app.py runs without errors
   - Verify navigation flows correctly between all pages
   - Confirm data from local text files loads and displays properly on templates
   - Validate all UI elements are present and functional per specification

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app.py and all templates/*.html
- Preserve exact element IDs, filenames, and data interaction as specified
- Final code must be fully runnable without draft placeholders or missing functionality
- Maintain naming and routing conventions per design_spec.md and user_task_description
- Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'ImplementationAgent'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'ImplementationAgent'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidatorAgent": {
        "prompt": (
            """You are a Software Test Engineer specialized in Python Flask web applications and frontend HTML templating.

Your goal is to validate the syntax, runtime behavior, and correctness of the backend app.py and frontend templates/*.html files to ensure full compliance with the design_spec.md specifications.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html from CONTEXT
- Produce validation_report.md outlining all errors, missing routes, incorrect element IDs, broken navigation, and data handling issues
- Focus on verifying exact route availability, template rendering correctness, presence of all required element IDs, functional navigation buttons, and proper local data file access

Validation Steps:
1. **Backend Syntax and Runtime Validation**
   - Use validate_python_file tool on app.py for syntax and runtime checks
   - Execute key routes to verify they return correct HTTP status codes and render templates without error
2. **Route and Function Validation**
   - Ensure all routes specified in design_spec.md exist in app.py with correct function names and HTTP methods
3. **Template Integrity Checks**
   - Parse templates/*.html to confirm existence of all requested element IDs from design_spec.md page designs
   - Verify navigation buttons include correct url_for mappings matching backend routes
4. **Data File Access Verification**
   - Confirm app.py reads all required data files with the exact field order as per design_spec.md schemas
5. **Error and Issue Reporting**
   - Document all discrepancies, syntax/runtime errors, missing elements, navigation failures, data misalignments
   - Format validation_report.md with clear sections and actionable items

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for all code validations
- MUST write validation_report.md using write_text_file tool
- MUST identify all missing or incorrect routes, template issues, navigation link problems, and data file handling defects
- Use positive, actionable language in the report
- Focus exclusively on files and specifications listed in input artifacts
- Do NOT provide fixes or corrections in this phase, only detailed validation findings

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationAgent'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationAgent'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "FixerAgent": {
        "prompt": (
            """You are a Software Developer specialized in Python Flask backend and HTML templating for web applications.

Your goal is to apply necessary corrections to app.py and templates/*.html based on validation_report.md to achieve full compliance with design_spec.md and pass all validation checks.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, and validation_report.md from CONTEXT
- Apply all fixes required to resolve discrepancies, syntax/runtime errors, missing elements, navigation errors, and data handling defects reported
- Output corrected app.py and templates/*.html reflecting all necessary improvements

Correction Requirements:
1. **Backend Corrections**
   - Fix syntax and runtime errors detected by validator
   - Ensure all routes and function definitions comply exactly with design_spec.md
   - Correct data file reading routines to match field order and access patterns
2. **Template Fixes**
   - Add or correct missing element IDs and ensure exact naming from design_spec.md
   - Repair navigation controls to use correct url_for targets matching backend routes
   - Ensure template rendering is seamless without errors
3. **Verification**
   - Double-check all changes against the validation_report.md instructions
   - Produce final artifacts ready for successful validation with no outstanding issues

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save corrected app.py and all templates/*.html files
- MUST ensure final artifacts fully address all reported issues comprehensively
- MUST maintain feature completeness as per user requirements and design_spec.md
- Do NOT introduce new features or unrelated changes beyond fixes indicated
- Submit only corrected files named exactly as input artifacts

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationAgent'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationAgent'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'ValidatorAgent'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md accurately and comprehensively covers all user-visible pages, UI element IDs, navigation links, "
                "and exact data file schema details before design_spec.md creation.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'ImplementationAgent': [
        ("IntegrationAgent", """Ensure app_draft.py and templates_draft/*.html conform fully to design_spec.md and contain all required pages and UI elements "
                "before integration into final app.py and templates.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'ValidatorAgent': [
        ("FixerAgent", """Verify validation_report.md thoroughly identifies all missing or incorrect route handlers, elements, navigation, and data handling "
                "issues before fixes are applied.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'FixerAgent': [
        ("RequirementsAnalyst", """Confirm that final app.py and templates/*.html fully address the validation report and retain full feature coverage of user requirements.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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

    # Sequential Flow:
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md with complete page specs, navigation flows, data formats, user actions.")

    # Read requirements_analysis.md content
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Step 2: WebArchitect produces design_spec.md based on user_task_description and requirements_analysis.md
    await execute(WebArchitect,
                  f"Using user_task_description and the following requirements_analysis.md content, create detailed design_spec.md defining Flask routes, templates, page structure, element IDs, backend data files, and navigation actions.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Declare agents
    ImplementationAgent = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationAgent = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution
    # Step 1: ImplementationAgent creates app_draft.py and templates_draft/*.html drafts
    await execute(
        ImplementationAgent,
        "Create complete draft of app_draft.py with all Flask routes, data handling, and templates_draft/*.html with exact element IDs, page titles, and navigation, based on design_spec.md and user requirements."
    )

    # Step 2: Read draft files for IntegrationAgent
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # As templates_draft/*.html means multiple files, we read all and concatenate with separators for context
        import glob
        files = glob.glob("templates_draft/*.html")
        contents = []
        for f in files:
            try:
                content = open(f).read()
                contents.append(f"=== {f} ===\n{content}\n")
            except:
                contents.append(f"=== {f} ===\n\n")
        templates_draft_content = "\n".join(contents)
    except:
        pass

    # Step 3: IntegrationAgent integrates drafts into final app.py and templates/*.html
    await execute(
        IntegrationAgent,
        f"Integrate and finalize app.py and templates/*.html based on design_spec.md, user requirements, app_draft.py, and templates_draft/*.html drafts. Produce clean, runnable final application with full compliance.\n\n=== app_draft.py ===\n{app_draft_content}\n=== Templates Draft ===\n{templates_draft_content}"
    )
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Declare agents
    ValidatorAgent = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ValidatorAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )
    FixerAgent = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FixerAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file artifacts for injection
    user_task_description = ""
    design_spec = ""
    app_py = ""
    templates_content = ""

    try:
        user_entries = CONTEXT.get("user_task_description", [])
        user_task_description = user_entries[-1]["content"] if user_entries else ""
    except:
        pass

    try:
        design_entries = CONTEXT.get("design_spec.md", [])
        design_spec = design_entries[-1]["content"] if design_entries else ""
    except:
        pass

    try:
        app_py = open("app.py").read()
    except:
        app_py = ""

    import glob
    import os

    templates_files_content = ""
    try:
        templates_files = [f for f in glob.glob("templates/*.html") if os.path.isfile(f)]
        for tf in templates_files:
            try:
                content = open(tf).read()
                templates_files_content += f"=== {tf} ===\n{content}\n\n"
            except:
                pass
    except:
        templates_files_content = ""

    # Execute ValidatorAgent
    await execute(ValidatorAgent,
                  f"Validate backend and frontend files for compliance:\n"
                  f"user_task_description:\n{user_task_description}\n\n"
                  f"design_spec.md:\n{design_spec}\n\n"
                  f"app.py content:\n{app_py}\n\n"
                  f"templates content:\n{templates_files_content}\n\n"
                  "Run validate_python_file on app.py, check runtime routes, verify route existence, element IDs in templates, navigation correctness, data file access,"
                  " and produce detailed validation_report.md with all errors and actionable feedback. Use validate_python_file and execute_python_code tools. "
                  "Do NOT fix issues here.")
    
    # Read validation_report.md for FixerAgent injection
    validation_report = ""
    try:
        validation_report = open("validation_report.md").read()
    except:
        validation_report = ""

    # Execute FixerAgent to fix issues reported
    await execute(FixerAgent,
                  f"Apply all fixes to app.py and templates/*.html based on the validation report below:\n\n"
                  f"user_task_description:\n{user_task_description}\n\n"
                  f"design_spec.md:\n{design_spec}\n\n"
                  f"Current app.py content:\n{app_py}\n\n"
                  f"Current templates:\n{templates_files_content}\n\n"
                  f"Validation Report:\n{validation_report}\n\n"
                  "Fix all syntax/runtime errors, missing routes, element IDs, navigation issues, and data handling defects."
                  " Output corrected app.py and all templates/*.html as final artifacts.")
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
