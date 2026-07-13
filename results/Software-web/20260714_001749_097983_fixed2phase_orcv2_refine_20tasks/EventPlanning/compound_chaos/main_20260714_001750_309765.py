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
# 20260714_001750_309765/main_20260714_001750_309765.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the complete adaptive web design specification for the EventPlanning application including all 8 pages, exact element IDs, navigation flow, and local data file structures; deliver design_spec.md and gated design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator creates or revises design_spec.md based on user_task_description and previous design_feedback.md. \"\n        \"DesignCritic reviews design_spec.md ensuring completeness of pages, element IDs, data storage format, and navigation; \"\n        \"writes design_feedback.md starting with [APPROVED] or NEED_MODIFY. \"\n        \"At most two refinement iterations.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in adaptive web application design using Python.\n\nYour goal is to write or comprehensively revise the full adaptive web design specification for the EventPlanning application, including page layout, exact element IDs, navigation flow between the eight pages, and detailed local data file structures.\n\nTask Details:\n- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT\n- On initial iteration, create complete design_spec.md covering all 8 pages with required elements and data formats\n- When feedback begins with NEED_MODIFY, apply each correction fully and overwrite design_spec.md\n- When feedback begins with [APPROVED], preserve the design_spec.md as is\n\n**Section 1: Page Layout and Element IDs**\n- Specify the exact layout, container divs, buttons, inputs, tables, dropdowns, and other elements with precise IDs per page\n- Include all eight pages: Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, and Bookings Summary\n- Each page should include the page title, overview, and detailed elements with types and IDs\n\n**Section 2: Navigation Flow**\n- Define navigation paths and button/link interaction mapping between pages\n- Ensure users can intuitively move through browsing events, booking tickets, viewing venues, and managing participants\n- Start the website from the Dashboard page\n\n**Section 3: Local Data File Structures**\n- Specify the exact text file names and their data formats, including field names and delimiters\n- Include example data for each file reflecting the user_task_description\n- Must cover events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, and schedules.txt\n\nCRITICAL REQUIREMENTS:\n- Run at most two Generator/Critic iterations, stopping immediately upon approval\n- Apply every supported NEED_MODIFY item fully, do not add new requirements beyond the user task\n- Use write_text_file tool to save the complete design_spec.md without extra formatting or status markers\n- Output filename must be design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in comprehensive web application design specifications with Python and text file data management.\n\nYour goal is to perform a detailed review of design_spec.md ensuring that all 8 pages are fully covered with required element IDs, that inter-page navigation is logical, local text file data storage formats accurately match the user requirements, and the overall design meets the user task. Provide gated feedback with exact prefixes [APPROVED] or NEED_MODIFY.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Verify presence and correctness of each page’s layout, element types, and exact IDs\n- Check the navigation flow covers all required pages with consistent and logical transitions\n- Validate that local data files are specified exactly with correct formats, field orders, delimiters, and example data\n- Write design_feedback.md beginning with [APPROVED] if all requirements are met or NEED_MODIFY followed by precise corrections for any omissions or errors\n\nReview Requirements:\n1. Confirm all eight pages (Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, Bookings Summary) exist with complete element sets and correct IDs.\n2. Validate navigation paths are clearly specified and enable full user flows described in the user task.\n3. Validate data storage specifications match user task requirements including filenames, exact field delimiters, and example data correctness.\n4. Ensure no requirements outside the scope of the user task are introduced.\n5. The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY with no preceding whitespace or characters.\n\nCRITICAL REQUIREMENTS:\n- At most two iterative reviews allowed, stop immediately on [APPROVED]\n- Use write_text_file tool to output complete design_feedback.md\n- Do not add extraneous content or formatting before the feedback marker\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Conduct a comprehensive check for completeness, correctness of element IDs, page titles, local data formats compliance, and logical navigation flow.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the complete adaptive implementation of the EventPlanning Python web app with all required pages, exact element IDs, local text file data handling, and produce app.py with templates/*.html files along with gated code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator writes or revises the full backend and frontend implementation producing app.py and HTML templates for all pages, implementing navigation and local text file data management based on design_spec.md and previous code_feedback.md. \"\n        \"CodeCritic reviews the app.py and templates for correctness of element IDs, page functionality, data file access, and adherence to design_spec.md producing code_feedback.md starting with [APPROVED] or NEED_MODIFY. \"\n        \"At most two refinement iterations.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Web Developer specializing in comprehensive Flask-based web application implementations.\n\nYour goal is to implement or thoroughly revise the complete Python web application backend and frontend. Deliverables include a fully functional app.py and corresponding templates/*.html files that realize the full design_spec.md requirements with exact page elements and IDs, implement navigation between pages starting from the Dashboard, and handle all local text file data operations.\n\nTask Details:\n- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT.\n- On first iteration, produce complete app.py and all HTML templates implementing all pages and exact element IDs.\n- On NEED_MODIFY feedback, incorporate all suggested corrections by full rewrite maintaining consistency.\n- Output updated app.py and templates/*.html files.\n\n**Section 1: Backend Implementation**\n- Implement Flask routes to serve all specified pages with exact URL paths and render templates with required context variables.\n- Implement file read/write logic for all local text data files (events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, schedules.txt) as per design_spec.md format.\n- Implement any filtering, searching, and data processing logic described by design_spec.md.\n- Ensure navigation is consistent, starting from Dashboard page as the home route.\n\n**Section 2: Frontend HTML Templates**\n- Create HTML templates for all pages with exact element IDs specified in design_spec.md.\n- Define elements using appropriate HTML tags (div, button, table, input, dropdown, etc.) exactly as described.\n- Include navigation controls linking to other pages.\n- Ensure templates provide placeholders for dynamic content from backend rendering.\n\n**Section 3: Consistency and Error Handling**\n- Maintain consistent naming across routes, template files, and element IDs.\n- Implement basic error handling for file I/O and user inputs.\n- Follow Python best practices and clean code structure.\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to output app.py and all templates/*.html files.\n- Implement all pages listed in design_spec.md with exact element IDs.\n- Implement local text file format handling exactly as specified.\n- On NEED_MODIFY feedback, fully rewrite output artifacts applying all corrections.\n- Run at most two iterations; stop immediately on [APPROVED] feedback.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web application and frontend template review.\n\nYour goal is to perform a detailed review of app.py and HTML templates ensuring correctness of element IDs, route implementations starting with Dashboard as home, local text file operations, and full functional alignment with design_spec.md. Provide clear gated feedback in code_feedback.md starting with [APPROVED] or NEED_MODIFY for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT.\n- Verify all pages exist and include exact element IDs as specified.\n- Check all Flask routes correspond to pages and navigation is properly implemented starting at Dashboard.\n- Confirm all local text files are accessed correctly with matching field formats per design_spec.md.\n- Review dynamic content handling and search/filter features accuracy.\n- Provide precise corrections if requirements are missing, incorrect, or inconsistent.\n\nReview Checklist:\n1. All eight pages implemented with exact element IDs documented.\n2. Navigation links are correct and start from Dashboard route '/‘ or equivalent.\n3. All data file read/write operations match specified formats and paths.\n4. Dynamic content rendering matches design_spec.md descriptions.\n5. No extraneous functionality beyond design_spec.md.\n6. Correct naming consistency across app.py and templates.\n\nCRITICAL REQUIREMENTS:\n- The very first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.\n- Provide complete, gated feedback or full approval; do not add requirements.\n- Use write_text_file tool to save the entire feedback artifact.\n- Run at most two review iterations; stop on first [APPROVED].\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Ensure all pages are implemented with exact element IDs, correct navigation routes, local text data storage conformity, and that the app runs without error.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in adaptive web application design using Python.

Your goal is to write or comprehensively revise the full adaptive web design specification for the EventPlanning application, including page layout, exact element IDs, navigation flow between the eight pages, and detailed local data file structures.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- On initial iteration, create complete design_spec.md covering all 8 pages with required elements and data formats
- When feedback begins with NEED_MODIFY, apply each correction fully and overwrite design_spec.md
- When feedback begins with [APPROVED], preserve the design_spec.md as is

**Section 1: Page Layout and Element IDs**
- Specify the exact layout, container divs, buttons, inputs, tables, dropdowns, and other elements with precise IDs per page
- Include all eight pages: Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, and Bookings Summary
- Each page should include the page title, overview, and detailed elements with types and IDs

**Section 2: Navigation Flow**
- Define navigation paths and button/link interaction mapping between pages
- Ensure users can intuitively move through browsing events, booking tickets, viewing venues, and managing participants
- Start the website from the Dashboard page

**Section 3: Local Data File Structures**
- Specify the exact text file names and their data formats, including field names and delimiters
- Include example data for each file reflecting the user_task_description
- Must cover events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, and schedules.txt

CRITICAL REQUIREMENTS:
- Run at most two Generator/Critic iterations, stopping immediately upon approval
- Apply every supported NEED_MODIFY item fully, do not add new requirements beyond the user task
- Use write_text_file tool to save the complete design_spec.md without extra formatting or status markers
- Output filename must be design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in comprehensive web application design specifications with Python and text file data management.

Your goal is to perform a detailed review of design_spec.md ensuring that all 8 pages are fully covered with required element IDs, that inter-page navigation is logical, local text file data storage formats accurately match the user requirements, and the overall design meets the user task. Provide gated feedback with exact prefixes [APPROVED] or NEED_MODIFY.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify presence and correctness of each page’s layout, element types, and exact IDs
- Check the navigation flow covers all required pages with consistent and logical transitions
- Validate that local data files are specified exactly with correct formats, field orders, delimiters, and example data
- Write design_feedback.md beginning with [APPROVED] if all requirements are met or NEED_MODIFY followed by precise corrections for any omissions or errors

Review Requirements:
1. Confirm all eight pages (Dashboard, Events Listing, Event Details, Ticket Booking, Participants Management, Venue Information, Event Schedules, Bookings Summary) exist with complete element sets and correct IDs.
2. Validate navigation paths are clearly specified and enable full user flows described in the user task.
3. Validate data storage specifications match user task requirements including filenames, exact field delimiters, and example data correctness.
4. Ensure no requirements outside the scope of the user task are introduced.
5. The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY with no preceding whitespace or characters.

CRITICAL REQUIREMENTS:
- At most two iterative reviews allowed, stop immediately on [APPROVED]
- Use write_text_file tool to output complete design_feedback.md
- Do not add extraneous content or formatting before the feedback marker

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Web Developer specializing in comprehensive Flask-based web application implementations.

Your goal is to implement or thoroughly revise the complete Python web application backend and frontend. Deliverables include a fully functional app.py and corresponding templates/*.html files that realize the full design_spec.md requirements with exact page elements and IDs, implement navigation between pages starting from the Dashboard, and handle all local text file data operations.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT.
- On first iteration, produce complete app.py and all HTML templates implementing all pages and exact element IDs.
- On NEED_MODIFY feedback, incorporate all suggested corrections by full rewrite maintaining consistency.
- Output updated app.py and templates/*.html files.

**Section 1: Backend Implementation**
- Implement Flask routes to serve all specified pages with exact URL paths and render templates with required context variables.
- Implement file read/write logic for all local text data files (events.txt, venues.txt, tickets.txt, bookings.txt, participants.txt, schedules.txt) as per design_spec.md format.
- Implement any filtering, searching, and data processing logic described by design_spec.md.
- Ensure navigation is consistent, starting from Dashboard page as the home route.

**Section 2: Frontend HTML Templates**
- Create HTML templates for all pages with exact element IDs specified in design_spec.md.
- Define elements using appropriate HTML tags (div, button, table, input, dropdown, etc.) exactly as described.
- Include navigation controls linking to other pages.
- Ensure templates provide placeholders for dynamic content from backend rendering.

**Section 3: Consistency and Error Handling**
- Maintain consistent naming across routes, template files, and element IDs.
- Implement basic error handling for file I/O and user inputs.
- Follow Python best practices and clean code structure.

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to output app.py and all templates/*.html files.
- Implement all pages listed in design_spec.md with exact element IDs.
- Implement local text file format handling exactly as specified.
- On NEED_MODIFY feedback, fully rewrite output artifacts applying all corrections.
- Run at most two iterations; stop immediately on [APPROVED] feedback.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web application and frontend template review.

Your goal is to perform a detailed review of app.py and HTML templates ensuring correctness of element IDs, route implementations starting with Dashboard as home, local text file operations, and full functional alignment with design_spec.md. Provide clear gated feedback in code_feedback.md starting with [APPROVED] or NEED_MODIFY for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Verify all pages exist and include exact element IDs as specified.
- Check all Flask routes correspond to pages and navigation is properly implemented starting at Dashboard.
- Confirm all local text files are accessed correctly with matching field formats per design_spec.md.
- Review dynamic content handling and search/filter features accuracy.
- Provide precise corrections if requirements are missing, incorrect, or inconsistent.

Review Checklist:
1. All eight pages implemented with exact element IDs documented.
2. Navigation links are correct and start from Dashboard route '/‘ or equivalent.
3. All data file read/write operations match specified formats and paths.
4. Dynamic content rendering matches design_spec.md descriptions.
5. No extraneous functionality beyond design_spec.md.
6. Correct naming consistency across app.py and templates.

CRITICAL REQUIREMENTS:
- The very first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.
- Provide complete, gated feedback or full approval; do not add requirements.
- Use write_text_file tool to save the entire feedback artifact.
- Run at most two review iterations; stop on first [APPROVED].

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
        ("DesignCritic", """Conduct a comprehensive check for completeness, correctness of element IDs, page titles, local data formats compliance, and logical navigation flow.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Ensure all pages are implemented with exact element IDs, correct navigation routes, local text data storage conformity, and that the app runs without error.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    DesignCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
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
            "Create or revise the complete adaptive web design specification for the EventPlanning application including all 8 pages, exact element IDs, navigation flow, and local data file structures.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the design_spec.md ensuring completeness of pages, element IDs, data storage format, and navigation.\n"
            "Write design_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
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
        timeout_threshold=350,
        failure_threshold=2,
        recovery_time=60
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_py_content = ""
        templates_content = ""
        code_feedback_content = ""

        # Read current app.py content
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                app_py_content = f.read()
        except FileNotFoundError:
            pass

        # Read all templates/*.html content combined
        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    templates_content += f"\n=== {template_path} ===\n" + f.read()
            except OSError:
                pass

        # On iteration > 0, read code_feedback.md content
        if iteration > 0:
            try:
                with open("code_feedback.md", "r", encoding="utf-8") as f:
                    code_feedback_content = f.read()
            except FileNotFoundError:
                code_feedback_content = ""

        # Prepare message for AppGenerator
        msg_for_generator = (
            "Create or revise the complete app.py and templates/*.html files for the EventPlanning Python web app.\n\n"
            f"=== design_spec.md from CONTEXT ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
            f"=== Current app.py ===\n{app_py_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{code_feedback_content}\n\n"
            "If feedback starts with NEED_MODIFY, incorporate all corrections by full rewrite.\n"
            "If first iteration, produce full implementation with exact element IDs, navigation, and file data handling."
        )

        # Execute AppGenerator
        await execute(AppGenerator, msg_for_generator)

        # Re-read outputs after Generator finishes
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                app_py_content = f.read()
        except FileNotFoundError:
            app_py_content = ""

        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    templates_content += f"\n=== {template_path} ===\n" + f.read()
            except OSError:
                pass

        # Prepare message for CodeCritic
        msg_for_critic = (
            "Review the latest app.py and templates for correctness of element IDs, page functionality, local text file operations, "
            "navigation starting from Dashboard, and full compliance with design_spec.md.\n\n"
            f"=== design_spec.md from CONTEXT ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
            f"=== Latest app.py ===\n{app_py_content}\n\n"
            f"=== Latest Templates ===\n{templates_content}"
        )

        # Execute CodeCritic
        await execute(CodeCritic, msg_for_critic)

        # Read latest code_feedback.md content
        try:
            with open("code_feedback.md", "r", encoding="utf-8") as f:
                code_feedback_content = f.read()
        except FileNotFoundError:
            code_feedback_content = ""

        # Stop if approved
        if code_feedback_content.startswith("[APPROVED]"):
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
