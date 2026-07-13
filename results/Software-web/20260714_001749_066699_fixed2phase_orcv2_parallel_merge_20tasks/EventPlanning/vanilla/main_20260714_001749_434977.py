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
# 20260714_001749_434977/main_20260714_001749_434977.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Define backend route/data schemas and frontend templates with exact element IDs for EventPlanning app, merging into a unified design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect specifies Flask app routes, data schema, and local text files for event planning features; \"\n        \"FrontendDesignArchitect specifies the HTML templates, including exact element IDs and navigation flow; \"\n        \"DesignMerger consolidates backend_design.md and frontend_design.md into a coherent design_spec.md ensuring no omissions or conflicts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend design and local file data schema specification.\n\nYour goal is to define the backend Flask routes, data models, and local text file handling schemas for the EventPlanning web application, strictly based on user requirements and provided data formats.\n\nTask Details:\n- Read user_task_description from CONTEXT fully for feature requirements and data format details.\n- Independently produce backend_design.md describing all Flask routes and detailed data file schemas.\n- Do not reference frontend_design.md or sibling outputs.\n\n**Section 1: Flask Routes Specification**\n- Define all necessary Flask route URLs, HTTP methods (GET, POST), and route functions matching user features.\n- Specify context variables passed to templates per route, including names and types.\n- Indicate file operations with local data files located in the 'data' directory for events, venues, tickets, bookings, participants, and schedules.\n- Must include routes for Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, and Bookings Summary.\n\n**Section 2: Data File Schemas**\n- Provide explicit schema definitions for each data file (events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, schedules.txt).\n- Each schema must include field names, data delimiters, format, expected data types, and example rows as given.\n- Detail file reading and writing format, including field order and data constraints.\n- Do not invent new files or fields beyond user specifications.\n\nCRITICAL SUCCESS CRITERIA:\n- The backend_design.md enables BackendDevelopers to implement the Flask app backend with correct routes and file-based data handling.\n- Use write_text_file tool to save backend_design.md.\n- Write only backend_design.md and no other outputs.\n- Adhere strictly to user_task_description for all content.\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in frontend HTML and template design with a focus on element identification and navigation.\n\nYour goal is to define all frontend HTML templates covering the eight pages of the EventPlanning app with full element IDs and a consistent navigation flow, based on user requirements.\n\nTask Details:\n- Read user_task_description from CONTEXT in full for page structure, element IDs, and navigation requirements.\n- Independently produce frontend_design.md describing all required templates, element IDs, and navigation mapping.\n- Do not read backend_design.md or sibling outputs.\n\n**Section 1: HTML Template Specifications**\n- Specify each HTML template file name corresponding to the eight pages.\n- List all mandatory elements with exact IDs and element types (div, button, table, input, dropdown, etc.).\n- Define textual page titles exactly as per user task.\n- Detail navigation flow between pages triggered by buttons/links, including their IDs and destination pages.\n- Include dynamic elements like event or venue buttons with placeholder IDs reflecting identifiers (e.g., view-event-button-{event_id}).\n\n**Section 2: Navigation and Interaction**\n- Map buttons and interactive elements to their intended actions/navigations.\n- Specify form controls and inputs with types and accepted values (dropdowns with options, input types, etc.).\n- Provide any required page container div IDs for layout grouping.\n\nCRITICAL SUCCESS CRITERIA:\n- frontend_design.md allows FrontendDevelopers to implement templates/*.html with exact element IDs and navigation flows.\n- Use write_text_file tool to save frontend_design.md.\n- Write only frontend_design.md with no extra files or markers.\n- Follow user_task_description details exactly.\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in merging complementary backend and frontend design specifications for Flask web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into a comprehensive and consistent design_spec.md for the EventPlanning application, ensuring no requirements are omitted or conflicted.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT in full.\n- Verify completeness and consistency between backend routes, data schemas, and frontend templates with element IDs and navigation.\n- Synthesize a single design_spec.md that integrates backend route specifications, data file schemas, and frontend template element definitions.\n- Resolve any conflicts by aligning context variable naming, element ID usage, and navigation references exactly as per the user task.\n- Do not add new features or requirements beyond input artifacts.\n\n**Section 1: Flask Backend Design**\n- Consolidate route URLs, methods, and data file handling from backend_design.md.\n- Confirm all routes correspond with frontend navigation.\n\n**Section 2: Frontend Template Design**\n- Consolidate templates, page titles, element IDs, and navigation from frontend_design.md.\n- Link buttons and interactive elements to corresponding backend routes.\n\n**Section 3: Data File Schema Alignment**\n- Validate that backend data schemas support frontend data display requirements.\n- Include example data snippets from both specifications.\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md contains a fully reconciled, conflict-free backend and frontend design.\n- Use write_text_file tool to save design_spec.md.\n- Write only design_spec.md; avoid adding explanations or comments.\n- Ensure the artifact fully covers all user requirements.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend route and data schema completeness and accuracy against the user task.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend template coverage, element ID accuracy, and navigation compliance with requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend Flask app.py and frontend HTML templates for EventPlanning from design_spec.md and integrate them into final deliverables\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py based on backend specifications in design_spec.md; \"\n        \"FrontendDeveloper implements HTML templates for all pages according to design_spec.md; \"\n        \"IntegrationMerger combines app.py and templates/*.html ensuring interface consistency and correctness.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications using Python.\n\nYour goal is to implement a complete backend Flask app.py based on the provided design specifications for an event planning system, managing data stored in local text files.\n\nTask Details:\n- Read design_spec.md from CONTEXT for all backend route, data schema, and logic specifications.\n- Independently create app.py implementing routes, handlers, and data access for events, tickets, bookings, participants, venues, and schedules.\n- Output a full app.py capable of fulfilling user task functionality described by design_spec.md without reliance on frontend code.\n\n**Backend Implementation Requirements**\n- Implement Flask routes matching design_spec.md route paths exactly.\n- Use local text file data storage as specified; manage reading and writing files safely.\n- Support all functionality including event listing, detailed views, ticket booking, participant management, venue info, scheduling, and booking summaries.\n- Include route handlers, request parsing, response rendering calls (to templates), and data updates where applicable.\n- Follow data file formats and field delimiters as per specifications in design_spec.md.\n- Ensure error handling and valid HTTP responses for typical client interactions.\n\n**Code Formatting and Structure**\n- Use single-quotes docstrings only for any code comments or examples.\n- Organize code logically by feature or route group.\n- No partial implementations; deliver a ready-to-run Flask backend.\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save app.py.\n- Output exactly one artifact: app.py.\n- Do not read or assume any frontend template files.\n- Backend must be self-contained, complete per design_spec.md.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask applications.\n\nYour goal is to implement all frontend HTML templates for the EventPlanning application’s eight pages according to design_spec.md, ensuring correct layout, element IDs, and page navigation.\n\nTask Details:\n- Read design_spec.md from CONTEXT for page structures, element IDs, template names, and navigation details.\n- Independently create the complete set of HTML templates (*.html) for:\n  Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, Bookings Summary.\n- Match all element IDs and page titles exactly as specified.\n- Use Jinja2 template syntax for dynamic content areas as inferred from context variables in design_spec.md.\n- Do not depend on backend code or other agents’ outputs.\n\n**Frontend Template Requirements**\n- Provide one .html file per page with correct filename conventions indicated in design_spec.md.\n- Include navigation elements linking pages using route names from design_spec.md.\n- Ensure all interactive elements (buttons, inputs, dropdowns) have correct IDs.\n- Use semantic HTML5 elements where appropriate and maintain clean, readable formatting.\n- Include placeholder/template expressions for dynamic data from backend context variables.\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool for all template files to templates/*.html.\n- Output exactly the declared templates with no additions or omissions.\n- Templates must be stand-alone, not mixing backend logic.\n- Follow design_spec.md strictly regarding IDs and page content structure.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Specialist skilled in combining Flask backend and frontend templates into a coherent web application deliverable.\n\nYour goal is to integrate the independently developed app.py backend and frontend HTML templates into final working deliverables, ensuring full adherence to design_spec.md for route consistency, data flow, element ID usage, and page navigation.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT.\n- Reconcile backend routes with frontend navigation and template file usage.\n- Validate matching of route names, context variable references, and element IDs between backend and frontend.\n- Correct inconsistencies or missing links by adapting app.py or templates while maintaining original developer input.\n- Produce final integrated app.py and templates/*.html that fully implement all specified features and UI.\n\n**Integration and Consistency Requirements**\n- Check that all Flask routes used in app.py correspond to templates delivered.\n- Verify template element IDs match design_spec.md and backend context variable usage.\n- Confirm navigation buttons and links function correctly referencing valid routes.\n- Ensure data context passed from backend aligns with frontend rendering requirements.\n- No addition of new features beyond design_spec.md.\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output both finalized app.py and templates/*.html.\n- Output exactly the declared artifacts containing the merged and harmonized code.\n- Maintain all functionality and UI elements as specified.\n- Final deliverables ready for deployment or testing.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Ensure backend implementation correctly follows design_spec.md routes and data access specifications.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Ensure frontend templates match design_spec.md in element IDs, layout, and navigation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend design and local file data schema specification.

Your goal is to define the backend Flask routes, data models, and local text file handling schemas for the EventPlanning web application, strictly based on user requirements and provided data formats.

Task Details:
- Read user_task_description from CONTEXT fully for feature requirements and data format details.
- Independently produce backend_design.md describing all Flask routes and detailed data file schemas.
- Do not reference frontend_design.md or sibling outputs.

**Section 1: Flask Routes Specification**
- Define all necessary Flask route URLs, HTTP methods (GET, POST), and route functions matching user features.
- Specify context variables passed to templates per route, including names and types.
- Indicate file operations with local data files located in the 'data' directory for events, venues, tickets, bookings, participants, and schedules.
- Must include routes for Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, and Bookings Summary.

**Section 2: Data File Schemas**
- Provide explicit schema definitions for each data file (events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, schedules.txt).
- Each schema must include field names, data delimiters, format, expected data types, and example rows as given.
- Detail file reading and writing format, including field order and data constraints.
- Do not invent new files or fields beyond user specifications.

CRITICAL SUCCESS CRITERIA:
- The backend_design.md enables BackendDevelopers to implement the Flask app backend with correct routes and file-based data handling.
- Use write_text_file tool to save backend_design.md.
- Write only backend_design.md and no other outputs.
- Adhere strictly to user_task_description for all content.

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in frontend HTML and template design with a focus on element identification and navigation.

Your goal is to define all frontend HTML templates covering the eight pages of the EventPlanning app with full element IDs and a consistent navigation flow, based on user requirements.

Task Details:
- Read user_task_description from CONTEXT in full for page structure, element IDs, and navigation requirements.
- Independently produce frontend_design.md describing all required templates, element IDs, and navigation mapping.
- Do not read backend_design.md or sibling outputs.

**Section 1: HTML Template Specifications**
- Specify each HTML template file name corresponding to the eight pages.
- List all mandatory elements with exact IDs and element types (div, button, table, input, dropdown, etc.).
- Define textual page titles exactly as per user task.
- Detail navigation flow between pages triggered by buttons/links, including their IDs and destination pages.
- Include dynamic elements like event or venue buttons with placeholder IDs reflecting identifiers (e.g., view-event-button-{event_id}).

**Section 2: Navigation and Interaction**
- Map buttons and interactive elements to their intended actions/navigations.
- Specify form controls and inputs with types and accepted values (dropdowns with options, input types, etc.).
- Provide any required page container div IDs for layout grouping.

CRITICAL SUCCESS CRITERIA:
- frontend_design.md allows FrontendDevelopers to implement templates/*.html with exact element IDs and navigation flows.
- Use write_text_file tool to save frontend_design.md.
- Write only frontend_design.md with no extra files or markers.
- Follow user_task_description details exactly.

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in merging complementary backend and frontend design specifications for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into a comprehensive and consistent design_spec.md for the EventPlanning application, ensuring no requirements are omitted or conflicted.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT in full.
- Verify completeness and consistency between backend routes, data schemas, and frontend templates with element IDs and navigation.
- Synthesize a single design_spec.md that integrates backend route specifications, data file schemas, and frontend template element definitions.
- Resolve any conflicts by aligning context variable naming, element ID usage, and navigation references exactly as per the user task.
- Do not add new features or requirements beyond input artifacts.

**Section 1: Flask Backend Design**
- Consolidate route URLs, methods, and data file handling from backend_design.md.
- Confirm all routes correspond with frontend navigation.

**Section 2: Frontend Template Design**
- Consolidate templates, page titles, element IDs, and navigation from frontend_design.md.
- Link buttons and interactive elements to corresponding backend routes.

**Section 3: Data File Schema Alignment**
- Validate that backend data schemas support frontend data display requirements.
- Include example data snippets from both specifications.

CRITICAL SUCCESS CRITERIA:
- design_spec.md contains a fully reconciled, conflict-free backend and frontend design.
- Use write_text_file tool to save design_spec.md.
- Write only design_spec.md; avoid adding explanations or comments.
- Ensure the artifact fully covers all user requirements.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications using Python.

Your goal is to implement a complete backend Flask app.py based on the provided design specifications for an event planning system, managing data stored in local text files.

Task Details:
- Read design_spec.md from CONTEXT for all backend route, data schema, and logic specifications.
- Independently create app.py implementing routes, handlers, and data access for events, tickets, bookings, participants, venues, and schedules.
- Output a full app.py capable of fulfilling user task functionality described by design_spec.md without reliance on frontend code.

**Backend Implementation Requirements**
- Implement Flask routes matching design_spec.md route paths exactly.
- Use local text file data storage as specified; manage reading and writing files safely.
- Support all functionality including event listing, detailed views, ticket booking, participant management, venue info, scheduling, and booking summaries.
- Include route handlers, request parsing, response rendering calls (to templates), and data updates where applicable.
- Follow data file formats and field delimiters as per specifications in design_spec.md.
- Ensure error handling and valid HTTP responses for typical client interactions.

**Code Formatting and Structure**
- Use single-quotes docstrings only for any code comments or examples.
- Organize code logically by feature or route group.
- No partial implementations; deliver a ready-to-run Flask backend.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save app.py.
- Output exactly one artifact: app.py.
- Do not read or assume any frontend template files.
- Backend must be self-contained, complete per design_spec.md.

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask applications.

Your goal is to implement all frontend HTML templates for the EventPlanning application’s eight pages according to design_spec.md, ensuring correct layout, element IDs, and page navigation.

Task Details:
- Read design_spec.md from CONTEXT for page structures, element IDs, template names, and navigation details.
- Independently create the complete set of HTML templates (*.html) for:
  Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, Bookings Summary.
- Match all element IDs and page titles exactly as specified.
- Use Jinja2 template syntax for dynamic content areas as inferred from context variables in design_spec.md.
- Do not depend on backend code or other agents’ outputs.

**Frontend Template Requirements**
- Provide one .html file per page with correct filename conventions indicated in design_spec.md.
- Include navigation elements linking pages using route names from design_spec.md.
- Ensure all interactive elements (buttons, inputs, dropdowns) have correct IDs.
- Use semantic HTML5 elements where appropriate and maintain clean, readable formatting.
- Include placeholder/template expressions for dynamic data from backend context variables.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool for all template files to templates/*.html.
- Output exactly the declared templates with no additions or omissions.
- Templates must be stand-alone, not mixing backend logic.
- Follow design_spec.md strictly regarding IDs and page content structure.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Specialist skilled in combining Flask backend and frontend templates into a coherent web application deliverable.

Your goal is to integrate the independently developed app.py backend and frontend HTML templates into final working deliverables, ensuring full adherence to design_spec.md for route consistency, data flow, element ID usage, and page navigation.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Reconcile backend routes with frontend navigation and template file usage.
- Validate matching of route names, context variable references, and element IDs between backend and frontend.
- Correct inconsistencies or missing links by adapting app.py or templates while maintaining original developer input.
- Produce final integrated app.py and templates/*.html that fully implement all specified features and UI.

**Integration and Consistency Requirements**
- Check that all Flask routes used in app.py correspond to templates delivered.
- Verify template element IDs match design_spec.md and backend context variable usage.
- Confirm navigation buttons and links function correctly referencing valid routes.
- Ensure data context passed from backend aligns with frontend rendering requirements.
- No addition of new features beyond design_spec.md.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output both finalized app.py and templates/*.html.
- Output exactly the declared artifacts containing the merged and harmonized code.
- Maintain all functionality and UI elements as specified.
- Final deliverables ready for deployment or testing.

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
        ("DesignMerger", """Verify backend route and data schema completeness and accuracy against the user task.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend template coverage, element ID accuracy, and navigation compliance with requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Ensure backend implementation correctly follows design_spec.md routes and data access specifications.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Ensure frontend templates match design_spec.md in element IDs, layout, and navigation.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    DesignMerger = build_resilient_agent(
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Define Flask routes, data file schemas, and local file handling for EventPlanning app. Save output to backend_design.md."),
        execute(FrontendDesignArchitect, "Specify all HTML templates with exact element IDs, page titles, and navigation flow for EventPlanning app. Save output to frontend_design.md.")
    )

    # Read backend and frontend design outputs
    backend_design_content, frontend_design_content = "", ""
    try:
        backend_design_content = open("backend_design.md").read()
    except Exception:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except Exception:
        pass

    # Merge backend and frontend designs into unified design_spec.md
    await execute(
        DesignMerger,
        "Merge backend_design.md and frontend_design.md into a comprehensive, consistent design_spec.md for EventPlanning app.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
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

    # Parallel: BackendDeveloper and FrontendDeveloper generate app.py and templates/*.html respectively
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete Flask backend app.py based on design_spec.md backend specifications for EventPlanning, handling all routes, data schemas, and functionality."),
        execute(FrontendDeveloper,
                "Implement all EventPlanning frontend HTML templates (*.html) based on design_spec.md, ensuring correct element IDs, page titles, and navigation using Jinja2 syntax.")
    )

    # Upon both completion, read outputs for integration
    design_spec_content = ""
    app_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except FileNotFoundError:
        pass
    try:
        app_content = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # IntegrationMerger merges and harmonizes app.py and templates using design_spec.md
    await execute(IntegrationMerger,
                  f"Integrate and harmonize backend app.py and frontend templates/*.html.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_content}\n\n"
                  f"=== Templates *.html ===\n{templates_content}")
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
