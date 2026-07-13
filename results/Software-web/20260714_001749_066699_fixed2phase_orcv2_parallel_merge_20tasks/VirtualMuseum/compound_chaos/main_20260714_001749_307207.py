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
# 20260714_001749_307207/main_20260714_001749_307207.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications for the VirtualMuseum app and merge them into a consistent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect designs Flask routes, data schemas, and local text file usage based on the user task description; \"\n        \"FrontendDesignArchitect designs the HTML templates with exact element IDs, navigation, and page structures based on the user task; \"\n        \"DesignMerger consolidates backend_design.md and frontend_design.md into one consistent design_spec.md without adding requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in backend Flask web application design and local text file data modeling.\n\nYour goal is to design the backend architecture for the VirtualMuseum application, specifying all Flask routes, associated data models based on local text files, and business logic contracts.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Independently create backend_design.md detailing routes, data file schemas, and expected request/response data\n- Output must include detailed route paths, HTTP methods, and exact data file usage schemas under 'data/' directory\n- Do not reference or read frontend_design.md or sibling outputs\n\n**Section 1: Flask Route Specification**\n- Enumerate all Flask routes supporting the user task functionality including Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, and Audio Guides\n- Specify HTTP methods (GET, POST as applicable), route URL patterns, parameter requirements, and intended template rendering or JSON responses\n- Define input and output data per route, emphasizing local text file interaction\n\n**Section 2: Local Text File Data Schemas**\n- Specify data schemas for each text file under 'data/' with exact filename, delimiter '|', field names, types, and description\n- Include example rows for each data file mirroring provided examples in user_task_description\n- Ensure all files listed (users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt) are fully covered and consistent\n- Define any backend logic related to data validation, filtering, and pagination relevant to the routes\n\n**Section 3: Business Logic and Data Contracts**\n- Define any backend behavior such as user authentication checks, filtering mechanisms, ticket purchasing process, event registration management, and artifact exhibition linkage\n- State the expected side effects on data files per user action\n\nCRITICAL SUCCESS CRITERIA:\n- Please use write_text_file tool to save all output to backend_design.md\n- Output must be clear, comprehensive, and directly implementable for backend development\n- Do not read or include frontend design details\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and Jinja2 template design for Flask web applications.\n\nYour goal is to design detailed frontend HTML template specifications for the VirtualMuseum application, including page layout, exact element IDs, navigation paths, and interactive UI components.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Independently create frontend_design.md specifying exact templates for all requested pages and UI elements\n- Specify page titles, container IDs, form elements, buttons, tables, dropdowns, and other interactive elements as described\n- Define navigation flow and corresponding button/link actions for all pages\n- Do not reference or read backend_design.md or sibling outputs\n\n**Section 1: Templates and Layout**\n- Specify one HTML template per page: Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides\n- For each template, list exact element IDs, element types, and a description of their purpose\n- Include page titles exactly as stated in user_task_description\n\n**Section 2: Navigation and Interaction**\n- Map all buttons and navigation elements to their target pages or behaviors\n- Specify interactive elements such as search inputs, filters, dropdowns, and play buttons with exact IDs and expected frontend handling\n- Define how dynamic content areas (tables, lists) are structured with context variables placeholders for backend rendering\n\n**Section 3: UI Component Details**\n- Provide details on tables (columns, headers), input fields (types and validation), and buttons (actions and dynamic IDs)\n- Ensure that element IDs and navigation actions align with user_task_description exactly\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save all output to frontend_design.md\n- Outputs must be precise to enable frontend developers to create templates/*.html files exactly as specified\n- Do not include backend data or route specifications\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in reconciliation and integration of backend and frontend design specifications for Flask web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into one comprehensive design_spec.md that is fully consistent with the user_task_description without adding requirements.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Analyze all backend routes, data schemas, and frontend template element specifications\n- Identify and resolve inconsistencies, naming mismatches, or conflicting navigation paths\n- Produce a complete and consistent design_spec.md document, organized in sections reflecting both backend architecture and frontend UI design\n\n**Section 1: Backend Design Summary**\n- Preserve all Flask routes, local text file schemas, and business logic from backend_design.md\n- Ensure data schemas and route parameters correspond exactly to frontend context variables and navigation needs\n\n**Section 2: Frontend Design Summary**\n- Preserve all template details, exact element IDs, page titles, UI components, and navigation from frontend_design.md\n- Adjust element IDs or navigation references only to achieve consistency with backend design if unavoidable\n\n**Section 3: Consistency Verification**\n- Explicitly state any reconciled naming conventions between backend route parameters and frontend element IDs\n- Confirm that all user task requirements are fully addressed with no omissions\n- Validate navigation flow completeness across all pages and buttons\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output design_spec.md\n- Output must enable downstream developers to implement both backend and frontend without ambiguity\n- Write only declared output artifact without refinement markers or additional files\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify completeness and correctness of backend design according to user task and integration consistency.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design aligns with user task, includes exact element IDs and navigation consistent with backend.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend Flask app.py and frontend HTML templates concurrently based on design_spec.md and integrate them into a final deployable application\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py according to backend specifications in design_spec.md; \"\n        \"FrontendDeveloper implements all HTML templates with exact IDs and navigation per frontend design_spec.md; \"\n        \"IntegrationMerger integrates and reconciles app.py and templates/*.html ensuring interface consistency and readiness for deployment.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications and local file-based data management.\n\nYour goal is to implement the complete Flask backend application app.py based on the backend specifications in design_spec.md, managing data through local text files.\n\nTask Details:\n- Read design_spec.md from CONTEXT as the single source of truth including all backend route specifications, data models, and logic contracts\n- Independently generate app.py implementing all routes, business logic, and local file I/O exactly as prescribed\n- Write app.py providing Flask routes, request handling, file-based data persistence, and navigation endpoints\n- Do not read or depend on any frontend implementation artifacts\n\n**Section 1: Flask Route Implementation**\n- Implement all Flask routes defined in design_spec.md with correct paths, HTTP methods, and handlers\n- Include request parsing, response generation, template rendering calls (template names per design_spec.md)\n- Manage session or user authentication if specified\n\n**Section 2: Data Storage and Access**\n- Implement reading and writing for all local text files in the 'data' directory using prescribed pipe-delimited schema\n- Ensure data-loading functions deliver correct data structures reflecting design_spec.md schemas\n- Implement data mutation (create, update, delete) routes with file write synchronization\n\n**Section 3: Business Logic and Navigation**\n- Implement all business rules such as filtering, searching, ticket purchasing logic, event registration, audio guide playback control per design_spec.md\n- Ensure navigation actions correspond to routes used in frontend templates\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output a fully functional app.py implementing all backend functionality described in design_spec.md\n- Do not read or write any other filenames than app.py\n- Backend app.py must be self-contained with all logic and data access implemented as specified in design_spec.md\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 template design for Flask applications.\n\nYour goal is to create all required HTML templates for the VirtualMuseum web application based on frontend specifications in design_spec.md, ensuring exact element IDs, layouts, and navigation as specified.\n\nTask Details:\n- Read design_spec.md from CONTEXT, extracting all HTML template requirements for the 7 pages\n- Independently produce all templates/*.html files with correct Jinja2 syntax, element IDs, and page structure as per design_spec.md\n- Do not read or depend on backend artifacts or sibling templates work\n\n**Section 1: Page and Element Specifications**\n- Implement each of the 7 pages: Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides\n- Use exact element IDs, element types, and structures defined in design_spec.md for each page container and UI element\n- Include page titles as specified, headers, tables with proper columns, buttons with correct IDs\n\n**Section 2: Navigation and Interaction Controls**\n- Implement navigation buttons and links with URLs or endpoint references matching backend routes per design_spec.md\n- Use Jinja2 placeholders and template inheritance as suitable but preserve all required element IDs\n\n**Section 3: Filtering and Input Elements**\n- Include all search fields, dropdowns, and input controls with the specified element IDs and types\n- Ensure buttons and controls reflect action semantics from design_spec.md\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output templates/*.html implementing all frontend UI templates as specified\n- Output must have no deviations in element IDs or page titles from design_spec.md\n- Templates must be complete and deployable with the backend app.py\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in deploying Flask web applications by merging backend and frontend components.\n\nYour goal is to integrate the independently developed app.py backend and templates/*.html frontend artifacts into a harmonized, deployable Flask application with interface consistency.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Perform adaptive reconciliation of backend routes, frontend templates, and interface elements to fix inconsistencies\n- Ensure all backend routes used in templates exist and all templates use element IDs and navigation exact per the merged design_spec.md\n- Update app.py and templates/*.html as needed without adding new features beyond design_spec.md\n\n**Section 1: Consistency and Interface Validation**\n- Verify app.py routes match endpoints referenced in templates/*.html\n- Confirm Jinja2 templates use only declared element IDs and navigation controls from design_spec.md\n- Detect and resolve any mismatches in route names, template filenames, or context variables\n\n**Section 2: Artifact Integration and Correction**\n- Correct any implementation errors in app.py or template files for interface compliance\n- Ensure that template rendering calls in app.py use correct template files with all required context\n- Validate that local text file I/O in app.py corresponds strictly to schemas in design_spec.md\n\n**Section 3: Final Production Output**\n- Produce final versions of app.py and templates/*.html ready for deployment as a cohesive unit\n- Ensure no refinement or debugging markers included; artifacts must be clean and conformant\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output final app.py and templates/*.html\n- Only write declared final artifact files, no extra files or refinement marks\n- Final artifacts must be consistent and fully aligned with design_spec.md requirements\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check that backend implementation conforms to the backend portions of design_spec.md and is consistent with frontend.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend templates conform exactly to design_spec.md including element IDs and navigation coherence with backend.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'VirtualMuseum' Web Application

## 1. Objective
Develop a comprehensive web application named 'VirtualMuseum' using Python, with data managed through local text files. The application enables museums to manage virtual exhibitions, curate artifact collections, provide audio guides, sell visitor tickets, and host virtual events. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'VirtualMuseum' application is Python.

## 3. Page Design

The 'VirtualMuseum' web application will consist of the following seven pages:

### 1. Dashboard Page
- **Page Title**: Museum Dashboard
- **Overview**: The main hub displaying overview of exhibitions, artifacts, and navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: exhibition-summary** - Type: Div - Summary showing total exhibitions, active exhibitions count.
  - **ID: artifact-catalog-button** - Type: Button - Button to navigate to artifact catalog page.
  - **ID: exhibitions-button** - Type: Button - Button to navigate to exhibitions page.
  - **ID: visitor-tickets-button** - Type: Button - Button to navigate to visitor tickets page.
  - **ID: virtual-events-button** - Type: Button - Button to navigate to virtual events page.
  - **ID: audio-guides-button** - Type: Button - Button to navigate to audio guides page.

### 2. Artifact Catalog Page
- **Page Title**: Artifact Catalog
- **Overview**: A page displaying all artifacts with search and filter capabilities.
- **Elements**:
  - **ID: artifact-catalog-page** - Type: Div - Container for the artifact catalog page.
  - **ID: artifact-table** - Type: Table - Table displaying artifacts with ID, name, period, origin, exhibition, and actions.
  - **ID: search-artifact** - Type: Input - Field to search artifacts by name or ID.
  - **ID: apply-artifact-filter** - Type: Button - Button to apply filters.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Exhibitions Page
- **Page Title**: Exhibitions
- **Overview**: A page displaying all exhibitions with details and status.
- **Elements**:
  - **ID: exhibitions-page** - Type: Div - Container for the exhibitions page.
  - **ID: exhibition-list** - Type: Table - Table displaying all exhibitions with title, type, dates, gallery, and status.
  - **ID: filter-exhibition-type** - Type: Dropdown - Dropdown to filter by exhibition type (Permanent, Temporary, Virtual).
  - **ID: apply-exhibition-filter** - Type: Button - Button to apply exhibition filter.
  - **ID: view-exhibition-button-{exhibition_id}** - Type: Button - Button to view exhibition details (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Exhibition Details Page
- **Page Title**: Exhibition Details
- **Overview**: A detailed view of a specific exhibition with its artifacts.
- **Elements**:
  - **ID: exhibition-details-page** - Type: Div - Container for the exhibition details page.
  - **ID: exhibition-title** - Type: H1 - Title of the exhibition.
  - **ID: exhibition-description** - Type: Div - Description of the exhibition.
  - **ID: exhibition-dates** - Type: Div - Start and end dates of the exhibition.
  - **ID: exhibition-artifacts** - Type: Table - Table displaying artifacts in this exhibition.
  - **ID: back-to-exhibitions** - Type: Button - Button to navigate back to exhibitions list.

### 5. Visitor Tickets Page
- **Page Title**: Visitor Tickets
- **Overview**: A page for visitors to purchase tickets and view ticket sales.
- **Elements**:
  - **ID: visitor-tickets-page** - Type: Div - Container for the visitor tickets page.
  - **ID: ticket-type** - Type: Dropdown - Dropdown to select ticket type (Standard, Student, Senior, Family, VIP).
  - **ID: number-of-tickets** - Type: Input (number) - Field to input number of tickets.
  - **ID: purchase-ticket-button** - Type: Button - Button to purchase tickets.
  - **ID: my-tickets-table** - Type: Table - Table displaying user's purchased tickets.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Virtual Events Page
- **Page Title**: Virtual Events
- **Overview**: A page to view and manage virtual museum events like webinars and artist talks.
- **Elements**:
  - **ID: virtual-events-page** - Type: Div - Container for the virtual events page.
  - **ID: event-list** - Type: Table - Table displaying all events with title, date, time, type, and registration status.
  - **ID: register-event-button-{event_id}** - Type: Button - Button to register for an event (each row has this button).
  - **ID: cancel-registration-button-{registration_id}** - Type: Button - Button to cancel registration (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Audio Guides Page
- **Page Title**: Audio Guides
- **Overview**: A page to browse and access audio guides for exhibits.
- **Elements**:
  - **ID: audio-guides-page** - Type: Div - Container for the audio guides page.
  - **ID: audio-guide-list** - Type: Table - Table displaying all audio guides with exhibit number, title, language, and duration.
  - **ID: filter-language** - Type: Dropdown - Dropdown to filter by language (English, Spanish, French).
  - **ID: apply-language-filter** - Type: Button - Button to apply language filter.
  - **ID: play-guide-button-{guide_id}** - Type: Button - Button to play audio guide (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'VirtualMuseum' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Authentication Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username
  ```
- **Example Data**:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. Gallery Data
- **File Name**: `galleries.txt`
- **Data Format**:
  ```
  gallery_id|gallery_name|floor|capacity|theme|status
  ```
- **Example Data**:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. Exhibition Data
- **File Name**: `exhibitions.txt`
- **Data Format**:
  ```
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
  ```
- **Example Data**:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. Artifact Data
- **File Name**: `artifacts.txt`
- **Data Format**:
  ```
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
  ```
- **Example Data**:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. Audio Guide Data
- **File Name**: `audioguides.txt`
- **Data Format**:
  ```
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
  ```
- **Example Data**:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. Ticket Data
- **File Name**: `tickets.txt`
- **Data Format**:
  ```
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
  ```
- **Example Data**:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. Virtual Event Data
- **File Name**: `events.txt`
- **Data Format**:
  ```
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
  ```
- **Example Data**:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. Event Registration Data
- **File Name**: `event_registrations.txt`
- **Data Format**:
  ```
  registration_id|event_id|username|registration_date
  ```
- **Example Data**:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. Collection Log Data
- **File Name**: `collection_logs.txt`
- **Data Format**:
  ```
  log_id|artifact_id|activity_type|date|notes|condition|curator
  ```
- **Example Data**:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
  ```

All files will be saved in the `data` directory to ensure organization and easy access. The format uses a pipe (`|`) delimiter for better readability and parsing. Different types of data will be isolated to ensure efficient data management and retrieval.
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
            """You are a System Architect specializing in backend Flask web application design and local text file data modeling.

Your goal is to design the backend architecture for the VirtualMuseum application, specifying all Flask routes, associated data models based on local text files, and business logic contracts.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently create backend_design.md detailing routes, data file schemas, and expected request/response data
- Output must include detailed route paths, HTTP methods, and exact data file usage schemas under 'data/' directory
- Do not reference or read frontend_design.md or sibling outputs

**Section 1: Flask Route Specification**
- Enumerate all Flask routes supporting the user task functionality including Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, and Audio Guides
- Specify HTTP methods (GET, POST as applicable), route URL patterns, parameter requirements, and intended template rendering or JSON responses
- Define input and output data per route, emphasizing local text file interaction

**Section 2: Local Text File Data Schemas**
- Specify data schemas for each text file under 'data/' with exact filename, delimiter '|', field names, types, and description
- Include example rows for each data file mirroring provided examples in user_task_description
- Ensure all files listed (users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt) are fully covered and consistent
- Define any backend logic related to data validation, filtering, and pagination relevant to the routes

**Section 3: Business Logic and Data Contracts**
- Define any backend behavior such as user authentication checks, filtering mechanisms, ticket purchasing process, event registration management, and artifact exhibition linkage
- State the expected side effects on data files per user action

CRITICAL SUCCESS CRITERIA:
- Please use write_text_file tool to save all output to backend_design.md
- Output must be clear, comprehensive, and directly implementable for backend development
- Do not read or include frontend design details

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML and Jinja2 template design for Flask web applications.

Your goal is to design detailed frontend HTML template specifications for the VirtualMuseum application, including page layout, exact element IDs, navigation paths, and interactive UI components.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently create frontend_design.md specifying exact templates for all requested pages and UI elements
- Specify page titles, container IDs, form elements, buttons, tables, dropdowns, and other interactive elements as described
- Define navigation flow and corresponding button/link actions for all pages
- Do not reference or read backend_design.md or sibling outputs

**Section 1: Templates and Layout**
- Specify one HTML template per page: Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides
- For each template, list exact element IDs, element types, and a description of their purpose
- Include page titles exactly as stated in user_task_description

**Section 2: Navigation and Interaction**
- Map all buttons and navigation elements to their target pages or behaviors
- Specify interactive elements such as search inputs, filters, dropdowns, and play buttons with exact IDs and expected frontend handling
- Define how dynamic content areas (tables, lists) are structured with context variables placeholders for backend rendering

**Section 3: UI Component Details**
- Provide details on tables (columns, headers), input fields (types and validation), and buttons (actions and dynamic IDs)
- Ensure that element IDs and navigation actions align with user_task_description exactly

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save all output to frontend_design.md
- Outputs must be precise to enable frontend developers to create templates/*.html files exactly as specified
- Do not include backend data or route specifications

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in reconciliation and integration of backend and frontend design specifications for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into one comprehensive design_spec.md that is fully consistent with the user_task_description without adding requirements.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Analyze all backend routes, data schemas, and frontend template element specifications
- Identify and resolve inconsistencies, naming mismatches, or conflicting navigation paths
- Produce a complete and consistent design_spec.md document, organized in sections reflecting both backend architecture and frontend UI design

**Section 1: Backend Design Summary**
- Preserve all Flask routes, local text file schemas, and business logic from backend_design.md
- Ensure data schemas and route parameters correspond exactly to frontend context variables and navigation needs

**Section 2: Frontend Design Summary**
- Preserve all template details, exact element IDs, page titles, UI components, and navigation from frontend_design.md
- Adjust element IDs or navigation references only to achieve consistency with backend design if unavoidable

**Section 3: Consistency Verification**
- Explicitly state any reconciled naming conventions between backend route parameters and frontend element IDs
- Confirm that all user task requirements are fully addressed with no omissions
- Validate navigation flow completeness across all pages and buttons

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output design_spec.md
- Output must enable downstream developers to implement both backend and frontend without ambiguity
- Write only declared output artifact without refinement markers or additional files

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications and local file-based data management.

Your goal is to implement the complete Flask backend application app.py based on the backend specifications in design_spec.md, managing data through local text files.

Task Details:
- Read design_spec.md from CONTEXT as the single source of truth including all backend route specifications, data models, and logic contracts
- Independently generate app.py implementing all routes, business logic, and local file I/O exactly as prescribed
- Write app.py providing Flask routes, request handling, file-based data persistence, and navigation endpoints
- Do not read or depend on any frontend implementation artifacts

**Section 1: Flask Route Implementation**
- Implement all Flask routes defined in design_spec.md with correct paths, HTTP methods, and handlers
- Include request parsing, response generation, template rendering calls (template names per design_spec.md)
- Manage session or user authentication if specified

**Section 2: Data Storage and Access**
- Implement reading and writing for all local text files in the 'data' directory using prescribed pipe-delimited schema
- Ensure data-loading functions deliver correct data structures reflecting design_spec.md schemas
- Implement data mutation (create, update, delete) routes with file write synchronization

**Section 3: Business Logic and Navigation**
- Implement all business rules such as filtering, searching, ticket purchasing logic, event registration, audio guide playback control per design_spec.md
- Ensure navigation actions correspond to routes used in frontend templates

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output a fully functional app.py implementing all backend functionality described in design_spec.md
- Do not read or write any other filenames than app.py
- Backend app.py must be self-contained with all logic and data access implemented as specified in design_spec.md

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 template design for Flask applications.

Your goal is to create all required HTML templates for the VirtualMuseum web application based on frontend specifications in design_spec.md, ensuring exact element IDs, layouts, and navigation as specified.

Task Details:
- Read design_spec.md from CONTEXT, extracting all HTML template requirements for the 7 pages
- Independently produce all templates/*.html files with correct Jinja2 syntax, element IDs, and page structure as per design_spec.md
- Do not read or depend on backend artifacts or sibling templates work

**Section 1: Page and Element Specifications**
- Implement each of the 7 pages: Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides
- Use exact element IDs, element types, and structures defined in design_spec.md for each page container and UI element
- Include page titles as specified, headers, tables with proper columns, buttons with correct IDs

**Section 2: Navigation and Interaction Controls**
- Implement navigation buttons and links with URLs or endpoint references matching backend routes per design_spec.md
- Use Jinja2 placeholders and template inheritance as suitable but preserve all required element IDs

**Section 3: Filtering and Input Elements**
- Include all search fields, dropdowns, and input controls with the specified element IDs and types
- Ensure buttons and controls reflect action semantics from design_spec.md

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output templates/*.html implementing all frontend UI templates as specified
- Output must have no deviations in element IDs or page titles from design_spec.md
- Templates must be complete and deployable with the backend app.py

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in deploying Flask web applications by merging backend and frontend components.

Your goal is to integrate the independently developed app.py backend and templates/*.html frontend artifacts into a harmonized, deployable Flask application with interface consistency.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Perform adaptive reconciliation of backend routes, frontend templates, and interface elements to fix inconsistencies
- Ensure all backend routes used in templates exist and all templates use element IDs and navigation exact per the merged design_spec.md
- Update app.py and templates/*.html as needed without adding new features beyond design_spec.md

**Section 1: Consistency and Interface Validation**
- Verify app.py routes match endpoints referenced in templates/*.html
- Confirm Jinja2 templates use only declared element IDs and navigation controls from design_spec.md
- Detect and resolve any mismatches in route names, template filenames, or context variables

**Section 2: Artifact Integration and Correction**
- Correct any implementation errors in app.py or template files for interface compliance
- Ensure that template rendering calls in app.py use correct template files with all required context
- Validate that local text file I/O in app.py corresponds strictly to schemas in design_spec.md

**Section 3: Final Production Output**
- Produce final versions of app.py and templates/*.html ready for deployment as a cohesive unit
- Ensure no refinement or debugging markers included; artifacts must be clean and conformant

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output final app.py and templates/*.html
- Only write declared final artifact files, no extra files or refinement marks
- Final artifacts must be consistent and fully aligned with design_spec.md requirements

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
        ("DesignMerger", """Verify completeness and correctness of backend design according to user task and integration consistency.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design aligns with user task, includes exact element IDs and navigation consistent with backend.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check that backend implementation conforms to the backend portions of design_spec.md and is consistent with frontend.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend templates conform exactly to design_spec.md including element IDs and navigation coherence with backend.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    FrontendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(BackendDesignArchitect,
                "Read user_task_description. Independently create backend_design.md specifying Flask routes, data schemas, "
                "local text file usage and business logic for VirtualMuseum backend."),
        execute(FrontendDesignArchitect,
                "Read user_task_description. Independently create frontend_design.md specifying detailed HTML template specifications, "
                "exact element IDs, navigation, and UI components for VirtualMuseum frontend.")
    )

    # Read backend_design.md and frontend_design.md for merger
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

    # Merge backend and frontend design specs into design_spec.md
    await execute(DesignMerger,
                  f"User task description:\n{CONTEXT.get('user_task_description', '')}\n\n"
                  f"=== Backend Design ===\n{backend_design_content}\n\n"
                  f"=== Frontend Design ===\n{frontend_design_content}")
# Phase1_End
# Phase2_Start
import glob
import asyncio

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
        recovery_time=60
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
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete app.py backend Flask application based on design_spec.md backend specifications, including routes, request handling, file-based data persistence, and business logic."),
        execute(FrontendDeveloper,
                "Implement all 7 HTML templates in templates/*.html with exact element IDs, Jinja2 syntax, page structure, and navigation as per design_spec.md frontend specifications.")
    )

    # Read outputs for IntegrationMerger
    backend_code = ""
    frontend_templates = ""
    try:
        backend_code = open("app.py").read()
    except Exception:
        pass
    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path).read()
        except Exception:
            pass

    # IntegrationMerger merges and reconciles backend and frontend artifacts
    await execute(
        IntegrationMerger,
        f"Integrate and reconcile app.py backend and templates/*.html frontend artifacts ensuring full interface consistency and readiness for deployment.\n\n"
        f"=== design_spec.md ===\n{CONTEXT['design_spec.md']}\n\n"
        f"=== app.py ===\n{backend_code}\n\n"
        f"=== Templates ===\n{frontend_templates}"
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
