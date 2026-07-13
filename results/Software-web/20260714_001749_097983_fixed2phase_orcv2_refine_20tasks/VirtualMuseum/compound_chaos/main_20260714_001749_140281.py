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
# 20260714_001749_140281/main_20260714_001749_140281.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the complete design specification and UI contract for the VirtualMuseum Python web application including all pages, element IDs, navigation flows, and data storage, producing design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator produces design_spec.md detailing all required pages (Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides), UI elements with IDs, navigation button mappings, and data file formats; \"\n        \"DesignCritic reviews design_spec.md for completeness, clarity, and consistency writing design_feedback.md starting with [APPROVED] or NEED_MODIFY for revision; \"\n        \"This refinement loop runs at most two iterations.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to author and refine a comprehensive design specification document for the VirtualMuseum web application, including page layouts, exact UI element IDs, navigation schemes, and local data file formats, iterating at most twice based on critic feedback.\n\nTask Details:\n- Read the user_task_description from CONTEXT to understand all functional requirements.\n- Read existing design_spec.md and design_feedback.md artifacts for incremental refinement.\n- Output a complete design_spec.md detailing all seven required pages, UI element IDs, navigation button mappings, and file format data structures.\n- On iteration two, apply all NEED_MODIFY feedback by rewriting the entire design_spec.md. On approval, preserve current design_spec.md.\n\n**Section 1: Page Layouts and Element IDs**\n- Specify each page (Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides).\n- Include all UI elements with their exact type and unique element IDs as provided.\n- Provide container element IDs and detailed description of key UI components.\n\n**Section 2: Navigation Mapping**\n- Define navigation button IDs on each page and their destination pages.\n- Ensure navigation paths start from Dashboard as the main hub.\n- Maintain consistency of button IDs and their target pages per User Task description.\n\n**Section 3: Data Storage Formats**\n- Specify all data files within the 'data' directory with exact filenames.\n- Define file formats (pipe-separated) and full schemas for each data type (users, galleries, exhibitions, artifacts, audioguides, tickets, events, event registrations, collection logs).\n- Provide example records as specified without inventing data fields.\n\nCRITICAL SUCCESS CRITERIA:\n- Follow the Refinement Loop with at most two iterations, rewriting design_spec.md completely on NEED_MODIFY feedback.\n- Ensure clarity, completeness, and strict adherence to user_task_description.\n- Use write_text_file tool to save the design_spec.md file.\n- Output exactly as design_spec.md.\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"},\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}],\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Software Design Reviewer specializing in Python web application design specification validation.\n\nYour goal is to review the design_spec.md document for completeness, clarity, alignment with the VirtualMuseum requirements, and consistency; produce gated feedback in design_feedback.md starting with [APPROVED] or NEED_MODIFY to guide refinement, running at most two iterations.\n\nTask Details:\n- Read user_task_description and the current design_spec.md from CONTEXT.\n- Verify all seven required pages and their UI element IDs are specified completely.\n- Verify navigation button mappings accurately connect the pages as described.\n- Check data file formats, table schemas, pipe-delimited fields, and example records strictly follow the requirements.\n- Identify missing, inconsistent, or unclear elements and provide detailed NEED_MODIFY feedback.\n- Write [APPROVED] if the specification fully meets the requirements with no missing or inconsistent information.\n\nReview Requirements:\n1. Confirm page container IDs and all element IDs match those declared in the user task.\n2. Validate navigation button IDs and their correct target page mappings.\n3. Confirm all data files with exact names, their pipe-separated field schemas, and example content are fully documented.\n4. Ensure consistency and no undocumented features beyond user requirements.\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY followed immediately by clear corrections.\n- Use write_text_file tool to save design_feedback.md.\n- Stop after at most two review iterations or immediately upon approval.\n- Provide feedback only within the defined context and scope.\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_feedback.md\"}],\n        },\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Check for completeness of all pages, element IDs, navigation accuracy, adherence to data format specifications, and clarity of design_spec.md; ensure no requirements are omitted or inconsistent.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}],\n        }\n    ],\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Develop and refine the full backend and frontend implementation of VirtualMuseum Python web app including app.py and templates/*.html from design_spec.md and address code_feedback.md to final approved quality\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator writes or revises app.py and templates/*.html implementing all specified pages, elements, navigation, data loading/saving from local text files in 'data' directory as defined in design_spec.md; \"\n        \"CodeCritic reviews code bundle for functional completeness, conformance to design_spec.md, syntax, runtime validation, and UI correctness producing code_feedback.md starting with [APPROVED] or NEED_MODIFY; \"\n        \"The refinement loop runs at most two iterations.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Full Stack Developer specializing in Python web applications with expertise in integrating backend logic and frontend UI using local text files for data persistence.\n\nYour goal is to implement or revise the complete app.py backend and HTML templates under templates/*.html for the VirtualMuseum platform, ensuring compliance with design_spec.md and addressing all feedback in code_feedback.md within at most two iterations.\n\nTask Details:\n- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration, implement complete app.py and HTML templates covering all specified pages, UI elements with exact IDs, navigation, and local text file data handling under 'data' directory\n- On feedback starting with NEED_MODIFY, apply all corrections fully and overwrite both app.py and templates/*.html\n- On feedback starting with [APPROVED], preserve the approved implementation without changes\n\n**Implementation Requirements: Backend**\n- Implement Python backend in app.py managing all routes, data loading/saving from local text files as specified in design_spec.md\n- Provide complete data persistence using local text files with pipe-delimited formats in the 'data' directory\n- Include all business logic for exhibitions, artifacts, audio guides, tickets, events, and registrations\n- Ensure route handlers match design_spec.md page names and support the required UI interactions\n\n**Implementation Requirements: Frontend**\n- Develop HTML templates for all seven pages named and structured as per design_spec.md requirements under templates/*.html\n- Use exact element IDs for all UI components listed (e.g., dashboard-page, exhibition-summary, artifact-catalog-button, etc.)\n- Implement navigation buttons and filters exactly as specified\n- Embed dynamic content bindings consistent with backend context variables\n\n**Quality and Testing**\n- Use validate_python_file tool to check syntax and runtime for app.py after generation\n- Use write_text_file tool to save app.py and all templates/*.html after edits\n- Focus on correctness of all UI elements, exact navigation paths, proper data file reads/writes, and adherence to all design contracts\n\nCRITICAL SUCCESS CRITERIA:\n- Produce complete, consistent app.py and templates/*.html implementing all design features\n- Apply all NEED_MODIFY feedback fully within at most two iterations\n- Use write_text_file tool to save all output files\n- Use validate_python_file tool to validate app.py correctness before saving\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specialized in Python web applications and frontend UI review, focusing on verifying backend logic, data handling, UI correctness, and code validity.\n\nYour goal is to review app.py and templates/*.html for correctness, complete adherence to design_spec.md, correct local text file data operations, and successful syntax and runtime validation; then produce code_feedback.md starting with [APPROVED] or NEED_MODIFY within at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify all required pages, UI elements, and navigation exactly match design_spec.md\n- Check all element IDs exist and are correctly implemented in frontend templates\n- Confirm backend routes and logic implement all features specified including data persistence with pipe-delimited local text files in 'data' directory\n- Validate app.py syntax and runtime using validate_python_file tool\n- Write code_feedback.md starting exactly with [APPROVED] if all criteria met or NEED_MODIFY followed by detailed correction instructions\n- Stop refinement loop upon first [APPROVED] feedback or after two iterations\n\nReview Requirements:\n1. Confirm all seven pages exist with all specified UI elements and IDs as per design_spec.md\n2. Verify navigation buttons correctly link pages as stated\n3. Verify backend reads/writes all local text data files correctly with the defined formats and fields\n4. Validate app.py syntax and runtime pass with no errors\n5. Check UI correctness and backend logic completeness\n\nCRITICAL REQUIREMENTS:\n- code_feedback.md MUST start with exactly [APPROVED] or NEED_MODIFY on byte 1\n- Use write_text_file tool to save full feedback text\n- Provide clear, actionable corrections on NEED_MODIFY\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Verify code conformance to design_spec.md, correctness of data file interactions, completeness of all pages and UI elements with specified IDs, and successful syntax/runtime validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to author and refine a comprehensive design specification document for the VirtualMuseum web application, including page layouts, exact UI element IDs, navigation schemes, and local data file formats, iterating at most twice based on critic feedback.

Task Details:
- Read the user_task_description from CONTEXT to understand all functional requirements.
- Read existing design_spec.md and design_feedback.md artifacts for incremental refinement.
- Output a complete design_spec.md detailing all seven required pages, UI element IDs, navigation button mappings, and file format data structures.
- On iteration two, apply all NEED_MODIFY feedback by rewriting the entire design_spec.md. On approval, preserve current design_spec.md.

**Section 1: Page Layouts and Element IDs**
- Specify each page (Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides).
- Include all UI elements with their exact type and unique element IDs as provided.
- Provide container element IDs and detailed description of key UI components.

**Section 2: Navigation Mapping**
- Define navigation button IDs on each page and their destination pages.
- Ensure navigation paths start from Dashboard as the main hub.
- Maintain consistency of button IDs and their target pages per User Task description.

**Section 3: Data Storage Formats**
- Specify all data files within the 'data' directory with exact filenames.
- Define file formats (pipe-separated) and full schemas for each data type (users, galleries, exhibitions, artifacts, audioguides, tickets, events, event registrations, collection logs).
- Provide example records as specified without inventing data fields.

CRITICAL SUCCESS CRITERIA:
- Follow the Refinement Loop with at most two iterations, rewriting design_spec.md completely on NEED_MODIFY feedback.
- Ensure clarity, completeness, and strict adherence to user_task_description.
- Use write_text_file tool to save the design_spec.md file.
- Output exactly as design_spec.md."""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Software Design Reviewer specializing in Python web application design specification validation.

Your goal is to review the design_spec.md document for completeness, clarity, alignment with the VirtualMuseum requirements, and consistency; produce gated feedback in design_feedback.md starting with [APPROVED] or NEED_MODIFY to guide refinement, running at most two iterations.

Task Details:
- Read user_task_description and the current design_spec.md from CONTEXT.
- Verify all seven required pages and their UI element IDs are specified completely.
- Verify navigation button mappings accurately connect the pages as described.
- Check data file formats, table schemas, pipe-delimited fields, and example records strictly follow the requirements.
- Identify missing, inconsistent, or unclear elements and provide detailed NEED_MODIFY feedback.
- Write [APPROVED] if the specification fully meets the requirements with no missing or inconsistent information.

Review Requirements:
1. Confirm page container IDs and all element IDs match those declared in the user task.
2. Validate navigation button IDs and their correct target page mappings.
3. Confirm all data files with exact names, their pipe-separated field schemas, and example content are fully documented.
4. Ensure consistency and no undocumented features beyond user requirements.

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY followed immediately by clear corrections.
- Use write_text_file tool to save design_feedback.md.
- Stop after at most two review iterations or immediately upon approval.
- Provide feedback only within the defined context and scope.

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Full Stack Developer specializing in Python web applications with expertise in integrating backend logic and frontend UI using local text files for data persistence.

Your goal is to implement or revise the complete app.py backend and HTML templates under templates/*.html for the VirtualMuseum platform, ensuring compliance with design_spec.md and addressing all feedback in code_feedback.md within at most two iterations.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, implement complete app.py and HTML templates covering all specified pages, UI elements with exact IDs, navigation, and local text file data handling under 'data' directory
- On feedback starting with NEED_MODIFY, apply all corrections fully and overwrite both app.py and templates/*.html
- On feedback starting with [APPROVED], preserve the approved implementation without changes

**Implementation Requirements: Backend**
- Implement Python backend in app.py managing all routes, data loading/saving from local text files as specified in design_spec.md
- Provide complete data persistence using local text files with pipe-delimited formats in the 'data' directory
- Include all business logic for exhibitions, artifacts, audio guides, tickets, events, and registrations
- Ensure route handlers match design_spec.md page names and support the required UI interactions

**Implementation Requirements: Frontend**
- Develop HTML templates for all seven pages named and structured as per design_spec.md requirements under templates/*.html
- Use exact element IDs for all UI components listed (e.g., dashboard-page, exhibition-summary, artifact-catalog-button, etc.)
- Implement navigation buttons and filters exactly as specified
- Embed dynamic content bindings consistent with backend context variables

**Quality and Testing**
- Use validate_python_file tool to check syntax and runtime for app.py after generation
- Use write_text_file tool to save app.py and all templates/*.html after edits
- Focus on correctness of all UI elements, exact navigation paths, proper data file reads/writes, and adherence to all design contracts

CRITICAL SUCCESS CRITERIA:
- Produce complete, consistent app.py and templates/*.html implementing all design features
- Apply all NEED_MODIFY feedback fully within at most two iterations
- Use write_text_file tool to save all output files
- Use validate_python_file tool to validate app.py correctness before saving

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specialized in Python web applications and frontend UI review, focusing on verifying backend logic, data handling, UI correctness, and code validity.

Your goal is to review app.py and templates/*.html for correctness, complete adherence to design_spec.md, correct local text file data operations, and successful syntax and runtime validation; then produce code_feedback.md starting with [APPROVED] or NEED_MODIFY within at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify all required pages, UI elements, and navigation exactly match design_spec.md
- Check all element IDs exist and are correctly implemented in frontend templates
- Confirm backend routes and logic implement all features specified including data persistence with pipe-delimited local text files in 'data' directory
- Validate app.py syntax and runtime using validate_python_file tool
- Write code_feedback.md starting exactly with [APPROVED] if all criteria met or NEED_MODIFY followed by detailed correction instructions
- Stop refinement loop upon first [APPROVED] feedback or after two iterations

Review Requirements:
1. Confirm all seven pages exist with all specified UI elements and IDs as per design_spec.md
2. Verify navigation buttons correctly link pages as stated
3. Verify backend reads/writes all local text data files correctly with the defined formats and fields
4. Validate app.py syntax and runtime pass with no errors
5. Check UI correctness and backend logic completeness

CRITICAL REQUIREMENTS:
- code_feedback.md MUST start with exactly [APPROVED] or NEED_MODIFY on byte 1
- Use write_text_file tool to save full feedback text
- Provide clear, actionable corrections on NEED_MODIFY

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Check for completeness of all pages, element IDs, navigation accuracy, adherence to data format specifications, and clarity of design_spec.md; ensure no requirements are omitted or inconsistent.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md""", [])
    ],

    'AppGenerator': [
        ("CodeCritic", """Verify code conformance to design_spec.md, correctness of data file interactions, completeness of all pages and UI elements with specified IDs, and successful syntax/runtime validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        current_spec = ""
        feedback_content = ""
        try:
            current_spec = open("design_spec.md").read()
        except FileNotFoundError:
            pass
        if iteration > 0:
            try:
                feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            DesignGenerator,
            "Author or revise the full design_spec.md for the VirtualMuseum web application including all pages, UI element IDs, navigation, and data file specs.\n\n"
            f"=== Current design_spec.md ===\n{current_spec}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_spec = open("design_spec.md").read()
        except FileNotFoundError:
            current_spec = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md fully against the user requirements for VirtualMuseum including pages, elements, navigation, and data formats.\n"
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY with detailed feedback.\n\n"
            f"=== Latest design_spec.md ===\n{current_spec}"
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    AppGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        design_spec_content = ""
        app_content = ""
        templates_content = ""
        feedback_content = ""

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

        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html.\n\n"
            f"=== design_spec.md ===\n{design_spec_content}\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current templates ===\n{templates_content}\n\n"
            f"=== Current code_feedback.md ===\n{feedback_content}"
        )

        # Reload latest after AppGenerator run
        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            app_content = ""

        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except Exception:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates for correctness and adherence to design_spec.md.\n"
            "Run validate_python_file on app.py before writing feedback.\n"
            "Write code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== design_spec.md ===\n{design_spec_content}\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest templates ===\n{templates_content}"
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
