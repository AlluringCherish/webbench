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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create detailed design specification document with Flask routes, HTML templates, and data schemas for 'EventPlanning' app\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces a design_spec.md detailing Flask route endpoints, HTML template structures with element IDs, \"\n        \"and data schema definitions for all files described in the requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce a comprehensive design specification document (design_spec.md) that enables independent backend and frontend development for the 'EventPlanning' app.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce design_spec.md covering three main parts: Flask routes, HTML templates, and data file schemas\n- Ensure all Flask routes correspond to pages and functionalities described\n- Include all specified element IDs per page in the HTML templates section\n- Define data schemas for all data files exactly as per requirements with field order and example data\n- Do NOT assume undocumented features or add extra pages/functions\n\n**Section 1: Flask Routes Specification**\n\nDefine a complete table covering:\n- Route Path: URLs for each page and actions (e.g., /dashboard, /events, /book_ticket)\n- Function Names: Flask handler function names (use clear, lower_snake_case)\n- HTTP Methods: GET for page rendering, POST for form submissions where applicable\n- Template Files: Corresponding HTML template file names\n- Context Variables: Variables passed to templates with types and structures explained\n\nRequirements:\n- Root '/' must redirect to dashboard page\n- Include routes for all 8 pages plus necessary actions (e.g., ticket booking, participant add)\n- Detail context variables for each template precisely (including lists and dicts)\n- Use consistent naming conventions for functions and variables\n\n**Section 2: HTML Template Specifications**\n\nFor each page, specify:\n- Template file path (e.g., templates/dashboard.html)\n- Page title for <title> and <h1> tags matching provided page titles exactly\n- Complete list of required element IDs with tag types and short descriptions\n- Context variables available on page with their structure (dict fields, list contents)\n- Navigation buttons and their target routes (using Flask url_for function calls)\n- Dynamic element IDs with patterns (e.g., view-event-button-{event_id}) and how to render in Jinja2 syntax\n\nRequirements:\n- All element IDs from page specifications must be included exactly and case-sensitively\n- Context variable names and structures must be consistent with Section 1\n- Navigation must correspond to defined routes\n- Include instructions for handling dynamic IDs with template loops or conditionals\n\n**Section 3: Data File Schemas**\n\nFor each data file:\n- Specify file path under data/ directory\n- Exact pipe-delimited field order matching requirements\n- Brief description of data stored in file\n- Include 2-3 realistic example data rows as given\n- Emphasize no headers in files, parsing should start at first line\n- Note field data types implicitly from content (e.g., int, str, float)\n\nRequirements:\n- Schemas must be precise and complete for reliable backend data loading\n- No deviation from specified schema or field order allowed\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developers can implement all Flask routes and data loading solely based on Section 1 and Section 3\n- Frontend developers can build all templates with exact element IDs and interactions from Section 2\n- No assumptions allowed beyond the documented specifications\n- Use the write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md for backend accuracy: all Flask routes appropriately named with correct HTTP methods, \"\n                \"data schema definitions complete and matching requirements, and correct route-to-function mappings.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md for frontend completeness: all HTML templates with exact element IDs per page specifications, \"\n                \"correct context variable usage, and navigation button mappings.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement Flask backend and HTML frontend in parallel according to the design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using design_spec.md backend specifications including routes and data schemas. \"\n        \"FrontendDeveloper implements HTML templates/*.html using design_spec.md frontend specifications including all element IDs.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application according to the backend specifications provided for event planning systems.\n\nTask Details:\n- Read design_spec.md backend sections detailing all Flask routes and data file schemas from CONTEXT\n- Implement app.py with all specified routes, data loading, and business logic exactly as per design_doc\n- Use the exact route paths, function names, HTTP methods, and context variables defined\n- Load data files with pipe-delimited format from data/ directory following the schemas exactly\n- Do NOT read or modify frontend templates or frontend-only specifications\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   # Initialize Flask app with necessary imports\n   '''\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   '''\n\n2. **Root and Navigation Routes**:\n   - Implement the root '/' route to redirect to dashboard page using: redirect(url_for('dashboard'))\n   - Implement all routes specified for Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venues, Event Schedules, Bookings Summary\n\n3. **Data Handling**:\n   - Load data from the following files: events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, schedules.txt\n   - Parse each line splitting on '|', matching the exact field order given in design_spec.md\n   - Map data to dictionaries or lists with clear keys matching field names\n   - Handle file IO errors gracefully without crashing\n\n4. **Route Logic**:\n   - Use request.args or request.form to capture query parameters or form data for filtering, searching, and booking\n   - Pass context variables to templates exactly as specified in design_spec.md with correct variable names and types\n   - Implement booking logic updating ticket availability and booking storage if specified\n\n5. **Best Practices**:\n   - Use url_for for internal links and redirects\n   - Ensure functions match naming conventions and case sensitivity\n   - Add main guard: if __name__ == '__main__': app.run(debug=True, port=5000)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the complete app.py file\n- Strictly follow design_spec.md backend sections; no assumptions beyond given information\n- Function names, route URLs, and variable names must match design_spec.md exactly\n- Data file parsing must strictly follow specified field order and delimiter\n- Do NOT implement or modify any frontend templates within this task\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement complete HTML templates for the EventPlanning application as specified in the frontend design documentation.\n\nTask Details:\n- Read design_spec.md frontend sections describing all required HTML templates, element IDs, and context variables\n- Create all specified templates under templates/ directory following exact filenames and template structures\n- Include all required element IDs exactly as specified, respecting casing and format\n- Use Jinja2 syntax for dynamic content rendering, looping over lists and rendering variables as directed\n- Do NOT read or modify backend code or backend specifications\n\nImplementation Requirements:\n1. **Template Structure**:\n   # Each HTML file must start with standard HTML5 skeleton\n   '''\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ page_title }}</title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1>{{ page_title }}</h1>\n           <!-- Content goes here -->\n       </div>\n   </body>\n   </html>\n   '''\n\n2. **Element IDs and Dynamic Content**:\n   - Include all element IDs as specified: static and dynamic IDs (e.g., id=\"view-event-button-{{ event.event_id }}\")\n   - Use correct Jinja2 control structures for loops: {% for event in events %} ... {% endfor %}\n   - Access variables using dot notation matching design_spec.md context variables (e.g., {{ event.event_name }})\n\n3. **Forms and Buttons**:\n   - Implement forms for booking tickets or filtering searches with method=\"POST\" or \"GET\" as specified\n   - Use action URLs using url_for() with correct function names per design_spec.md\n\n4. **Navigation and Links**:\n   - Implement navigation buttons and links using url_for() to ensure routing consistency\n   - Use exact function names for url_for calls matching backend specifications\n\n5. **File Management**:\n   - Each template saved as individual file under templates/ directory (e.g., templates/dashboard.html)\n   - Follow naming conventions strictly; do NOT create extra templates beyond those specified\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save each HTML template file\n- All element IDs must be exactly as specified (case-sensitive)\n- All context variable names and usage must match design_spec.md exactly\n- Navigation links and form actions must use url_for with accurate function names\n- Do NOT implement any backend logic or data handling in these templates\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Review app.py for completeness of all routes, correctness of data handling per design_spec.md, and adherence to specifications. \"\n                \"Verify dashboard root route redirects properly.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all HTML templates implement design_spec.md element IDs, context variable structures, and navigation consistency.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce a comprehensive design specification document (design_spec.md) that enables independent backend and frontend development for the 'EventPlanning' app.

Task Details:
- Read user_task_description from CONTEXT
- Produce design_spec.md covering three main parts: Flask routes, HTML templates, and data file schemas
- Ensure all Flask routes correspond to pages and functionalities described
- Include all specified element IDs per page in the HTML templates section
- Define data schemas for all data files exactly as per requirements with field order and example data
- Do NOT assume undocumented features or add extra pages/functions

**Section 1: Flask Routes Specification**

Define a complete table covering:
- Route Path: URLs for each page and actions (e.g., /dashboard, /events, /book_ticket)
- Function Names: Flask handler function names (use clear, lower_snake_case)
- HTTP Methods: GET for page rendering, POST for form submissions where applicable
- Template Files: Corresponding HTML template file names
- Context Variables: Variables passed to templates with types and structures explained

Requirements:
- Root '/' must redirect to dashboard page
- Include routes for all 8 pages plus necessary actions (e.g., ticket booking, participant add)
- Detail context variables for each template precisely (including lists and dicts)
- Use consistent naming conventions for functions and variables

**Section 2: HTML Template Specifications**

For each page, specify:
- Template file path (e.g., templates/dashboard.html)
- Page title for <title> and <h1> tags matching provided page titles exactly
- Complete list of required element IDs with tag types and short descriptions
- Context variables available on page with their structure (dict fields, list contents)
- Navigation buttons and their target routes (using Flask url_for function calls)
- Dynamic element IDs with patterns (e.g., view-event-button-{event_id}) and how to render in Jinja2 syntax

Requirements:
- All element IDs from page specifications must be included exactly and case-sensitively
- Context variable names and structures must be consistent with Section 1
- Navigation must correspond to defined routes
- Include instructions for handling dynamic IDs with template loops or conditionals

**Section 3: Data File Schemas**

For each data file:
- Specify file path under data/ directory
- Exact pipe-delimited field order matching requirements
- Brief description of data stored in file
- Include 2-3 realistic example data rows as given
- Emphasize no headers in files, parsing should start at first line
- Note field data types implicitly from content (e.g., int, str, float)

Requirements:
- Schemas must be precise and complete for reliable backend data loading
- No deviation from specified schema or field order allowed

CRITICAL SUCCESS CRITERIA:
- Backend developers can implement all Flask routes and data loading solely based on Section 1 and Section 3
- Frontend developers can build all templates with exact element IDs and interactions from Section 2
- No assumptions allowed beyond the documented specifications
- Use the write_text_file tool to output design_spec.md

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

Your goal is to implement a complete Flask backend application according to the backend specifications provided for event planning systems.

Task Details:
- Read design_spec.md backend sections detailing all Flask routes and data file schemas from CONTEXT
- Implement app.py with all specified routes, data loading, and business logic exactly as per design_doc
- Use the exact route paths, function names, HTTP methods, and context variables defined
- Load data files with pipe-delimited format from data/ directory following the schemas exactly
- Do NOT read or modify frontend templates or frontend-only specifications

Implementation Requirements:
1. **Flask Application Setup**:
   # Initialize Flask app with necessary imports
   '''
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   '''

2. **Root and Navigation Routes**:
   - Implement the root '/' route to redirect to dashboard page using: redirect(url_for('dashboard'))
   - Implement all routes specified for Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venues, Event Schedules, Bookings Summary

3. **Data Handling**:
   - Load data from the following files: events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, schedules.txt
   - Parse each line splitting on '|', matching the exact field order given in design_spec.md
   - Map data to dictionaries or lists with clear keys matching field names
   - Handle file IO errors gracefully without crashing

4. **Route Logic**:
   - Use request.args or request.form to capture query parameters or form data for filtering, searching, and booking
   - Pass context variables to templates exactly as specified in design_spec.md with correct variable names and types
   - Implement booking logic updating ticket availability and booking storage if specified

5. **Best Practices**:
   - Use url_for for internal links and redirects
   - Ensure functions match naming conventions and case sensitivity
   - Add main guard: if __name__ == '__main__': app.run(debug=True, port=5000)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the complete app.py file
- Strictly follow design_spec.md backend sections; no assumptions beyond given information
- Function names, route URLs, and variable names must match design_spec.md exactly
- Data file parsing must strictly follow specified field order and delimiter
- Do NOT implement or modify any frontend templates within this task

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

Your goal is to implement complete HTML templates for the EventPlanning application as specified in the frontend design documentation.

Task Details:
- Read design_spec.md frontend sections describing all required HTML templates, element IDs, and context variables
- Create all specified templates under templates/ directory following exact filenames and template structures
- Include all required element IDs exactly as specified, respecting casing and format
- Use Jinja2 syntax for dynamic content rendering, looping over lists and rendering variables as directed
- Do NOT read or modify backend code or backend specifications

Implementation Requirements:
1. **Template Structure**:
   # Each HTML file must start with standard HTML5 skeleton
   '''
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ page_title }}</title>
   </head>
   <body>
       <div id="main-container-id">
           <h1>{{ page_title }}</h1>
           <!-- Content goes here -->
       </div>
   </body>
   </html>
   '''

2. **Element IDs and Dynamic Content**:
   - Include all element IDs as specified: static and dynamic IDs (e.g., id="view-event-button-{{ event.event_id }}")
   - Use correct Jinja2 control structures for loops: {% for event in events %} ... {% endfor %}
   - Access variables using dot notation matching design_spec.md context variables (e.g., {{ event.event_name }})

3. **Forms and Buttons**:
   - Implement forms for booking tickets or filtering searches with method="POST" or "GET" as specified
   - Use action URLs using url_for() with correct function names per design_spec.md

4. **Navigation and Links**:
   - Implement navigation buttons and links using url_for() to ensure routing consistency
   - Use exact function names for url_for calls matching backend specifications

5. **File Management**:
   - Each template saved as individual file under templates/ directory (e.g., templates/dashboard.html)
   - Follow naming conventions strictly; do NOT create extra templates beyond those specified

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save each HTML template file
- All element IDs must be exactly as specified (case-sensitive)
- All context variable names and usage must match design_spec.md exactly
- Navigation links and form actions must use url_for with accurate function names
- Do NOT implement any backend logic or data handling in these templates

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
        ("BackendDeveloper", """Verify design_spec.md for backend accuracy: all Flask routes appropriately named with correct HTTP methods, "
                "data schema definitions complete and matching requirements, and correct route-to-function mappings.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md for frontend completeness: all HTML templates with exact element IDs per page specifications, "
                "correct context variable usage, and navigation button mappings.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Review app.py for completeness of all routes, correctness of data handling per design_spec.md, and adherence to specifications. "
                "Verify dashboard root route redirects properly.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all HTML templates implement design_spec.md element IDs, context variable structures, and navigation consistency.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
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
    await execute(SystemArchitect, "Produce design_spec.md detailing Flask routes, HTML templates, and data schemas for 'EventPlanning' app based on user_task_description from CONTEXT")
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

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py backend according to design_spec.md"),
        execute(FrontendDeveloper, "Implement all HTML templates in templates/ directory according to design_spec.md")
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
