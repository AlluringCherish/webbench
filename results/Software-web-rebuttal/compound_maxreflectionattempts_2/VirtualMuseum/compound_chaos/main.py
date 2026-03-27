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
    "phase1": "def architecture_design_phase(\n    goal: str = \"Develop a comprehensive design specification covering Flask routes, HTML templates, and data schemas for the VirtualMuseum application\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces a detailed design_spec.md divided into 3 sections: \"\n        \"1) Flask routes with function names, context variables, and HTTP methods; \"\n        \"2) HTML templates with exact element IDs and navigation mappings; \"\n        \"3) Data schemas for all required text files using pipe-delimited format with field definitions. \"\n        \"This design_spec.md enables independent parallel development in subsequent phases.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in web application architecture for Flask projects.\n\nYour goal is to create a detailed and complete design specification document that divides the entire system architecture into three independent parts that enable parallel backend and frontend development and accurate data management.\n\nTask Details:\n- Read user_task_description from CONTEXT thoroughly\n- Create design_spec.md containing three main sections:\n  1. Flask routes with function names, HTTP methods, template rendering, and context variables\n  2. HTML templates specification with exact element IDs, page titles, and navigation button mappings using url_for\n  3. Data file schemas for all required data text files with pipe-delimited exact field orders and example data\n- Do NOT include any implementation code or frontend/backend combined detail beyond these three sections\n\n**Section 1: Flask Routes Specification**\n\n- Provide a complete list of all Flask routes with details:\n  - Route Path (e.g., /dashboard, /exhibitions, /exhibition/<int:id>)\n  - Function Name in snake_case\n  - HTTP Method (GET, POST, as applicable)\n  - Template filename for rendering (e.g., dashboard.html)\n  - Context variables passed to the template with exact names and types (str, int, list, dict, etc.)\n- Ensure root route ('/') redirects to dashboard\n- Specify routes for all pages and actions including filters, navigation, and form submissions\n\n**Section 2: HTML Templates Specification**\n\n- For each template:\n  - Specify exact filename in templates/ directory (e.g., dashboard.html)\n  - Provide exact page title for <title> and main <h1>\n  - List ALL required element IDs exactly as described in user requirements including buttons, tables, inputs, and dynamic IDs (with patterns)\n  - Map each navigation button ID to Flask route function via url_for() calls, including dynamic buttons\n  - Define context variables available in template rendering, with data types and usage notes\n- Use dynamic element ID patterns clearly with Jinja2 variable syntax as needed (e.g., id=\"view-exhibition-button-{{ exhibition.exhibition_id }}\")\n\n**Section 3: Data File Schemas**\n\n- For each data text file:\n  - Provide exact filename in data/ directory (e.g., data/exhibitions.txt)\n  - Define pipe-delimited field order with exact field names as column headers for clarity (though no header line in actual files)\n  - Describe content/purpose of the file\n  - Provide 2-3 realistic example rows of data\n- Ensure inclusion of all files referenced in system:\n  users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt\n\nCRITICAL SUCCESS CRITERIA:\n- The specification must enable Backend Developer to implement full Flask app.py with all routes, data load/parsing based solely on Sections 1 & 3\n- The specification must enable Frontend Developer to implement all templates exactly based solely on Section 2\n- All element IDs, page titles, and context variable names must match precisely between sections\n- Use write_text_file tool to output design_spec.md\n- Do NOT include implementation code or frontend/backend logic beyond specification\n- Do NOT assume any missing information beyond user_task_description\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md for backend relevance: completeness of Flask routes, including function names, HTTP methods, and data handling schemas for each required endpoint. \"\n                \"Check that all data schemas reflect the full set of fields for data files in pipe-delimited format with exact field orders.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md for frontend relevance: completeness of HTML templates specification including all element IDs, page titles, navigation button mappings using url_for, and context variables needed for rendering.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend Flask application and frontend HTML templates in parallel based on the finalized design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper independently implements app.py based on relevant sections of design_spec.md including all Flask route handlers, data loading and saving logic, and business logic. \"\n        \"FrontendDeveloper independently implements all HTML templates with correct element IDs, context variable usage, and button navigation as specified.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete backend Flask application based on the finalized design specifications.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) only from CONTEXT\n- Implement all Flask routes with correct HTTP methods, function names, and route paths as specified\n- Load, save, and manipulate data from data/*.txt files following exact schemas given in Section 3\n- Adhere strictly to context variable names and data format (pipe-delimited, no headers)\n- Do NOT read or consider Section 2 (Frontend) or any template files\n- Do NOT add features not specified in design_spec.md\n\nImplementation Requirements:\n1. **Flask Application Setup:**\n   ```python\n   from flask import Flask, render_template, request, redirect, url_for\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root Route:**\n   - Implement '/' route that redirects to dashboard page using `redirect(url_for('dashboard'))`\n\n3. **Data Handling:**\n   - Read/write data from files in 'data/' directory as specified\n   - Use pipe-delimited parsing: `line.strip().split('|')`\n   - Follow exact field order and data types as in Section 3 data schemas\n   - Handle file not found or IO exceptions gracefully\n   - No header lines included in data files\n\n4. **Route Implementations:**\n   - Implement every Flask route specified in Section 1 with exact function names\n   - Use render_template with template names matching routes\n   - Pass context variables exactly as specified (names, types, and structures)\n   - Implement POST handlers according to specification, processing form data\n\n5. **Best Practices:**\n   - Use `if __name__ == \"__main__\": app.run(port=5000, debug=True)`\n   - Use url_for for all internal redirects and links\n   - Validate inputs and handle error cases sensibly without crashing\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app.py\n- Function and route names must exactly match design_spec.md Section 1\n- Data files must be parsed and saved exactly according to Section 3 schema (pipe-delimited, no header)\n- Do NOT read or modify frontend templates or Section 2 content\n- Do NOT add undocumented features or routes\n- Ensure root route '/' redirects correctly to dashboard\n- No inline code snippets in chat; all output must be saved via write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to develop all HTML templates for the application based on the provided design specifications.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) only from CONTEXT\n- Implement all required HTML templates with exact element IDs, page titles, and navigation button mappings\n- Use context variables as specified with correct Jinja2 syntax and variable names\n- Do NOT read or modify backend code or Section 1 and 3 content\n- Do NOT add templates not specified in design_spec.md or add extra UI features\n\nImplementation Requirements:\n1. **Template Structure:**\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>Exact Page Title</title>\n   </head>\n   <body>\n       <div id=\"container-id\">\n           <h1>Exact Page Title</h1>\n           <!-- Content and controls as specified -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **File Naming and Location:**\n   - Save all template files in the 'templates/' directory\n   - Follow exact filenames provided in Section 2 (e.g. templates/dashboard.html)\n\n3. **Element IDs:**\n   - Implement ALL required element IDs with exact casing and spelling\n   - For dynamic IDs (e.g., view-exhibition-button-{exhibition_id}) use Jinja2 syntax, e.g. id=\"view-exhibition-button-{{ exhibition.exhibition_id }}\"\n\n4. **Context Variables:**\n   - Use context variables exactly as described, respecting types and structures\n   - Loop over lists and access dict fields properly with Jinja2 syntax\n\n5. **Navigation Buttons:**\n   - Implement buttons and links that navigate using url_for calls exactly matching function names in the design spec\n   - Use static links and dynamic links with parameters as specified\n\n6. **Forms:**\n   - Implement forms with correct method (POST/GET) and action using url_for\n   - Input elements must have matching name attributes and IDs for correct backend integration\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all HTML template files\n- Element IDs, page titles, and navigation button url_for calls must match design_spec.md Section 2 exactly\n- Do NOT modify or read backend code or data schemas\n- Do NOT add extra UI elements or templates beyond spec\n- Do NOT provide code snippets solely in chat; all output must be saved via write_text_file\n- Each template must be saved as a separate file (e.g., templates/dashboard.html, templates/exhibitions.html, etc.)\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Check app.py correctness: implementation of all Flask routes and HTTP methods, correctness of data file handling matching data schemas, adherence to route names and context variables, \"\n                \"and correct root route redirecting to dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Check templates/*.html completeness and accuracy: presence of all required element IDs, correct rendering of context variables, accurate implementation of navigation button url_for calls, \"\n                \"and conformity to specified page titles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in web application architecture for Flask projects.

Your goal is to create a detailed and complete design specification document that divides the entire system architecture into three independent parts that enable parallel backend and frontend development and accurate data management.

Task Details:
- Read user_task_description from CONTEXT thoroughly
- Create design_spec.md containing three main sections:
  1. Flask routes with function names, HTTP methods, template rendering, and context variables
  2. HTML templates specification with exact element IDs, page titles, and navigation button mappings using url_for
  3. Data file schemas for all required data text files with pipe-delimited exact field orders and example data
- Do NOT include any implementation code or frontend/backend combined detail beyond these three sections

**Section 1: Flask Routes Specification**

- Provide a complete list of all Flask routes with details:
  - Route Path (e.g., /dashboard, /exhibitions, /exhibition/<int:id>)
  - Function Name in snake_case
  - HTTP Method (GET, POST, as applicable)
  - Template filename for rendering (e.g., dashboard.html)
  - Context variables passed to the template with exact names and types (str, int, list, dict, etc.)
- Ensure root route ('/') redirects to dashboard
- Specify routes for all pages and actions including filters, navigation, and form submissions

**Section 2: HTML Templates Specification**

- For each template:
  - Specify exact filename in templates/ directory (e.g., dashboard.html)
  - Provide exact page title for <title> and main <h1>
  - List ALL required element IDs exactly as described in user requirements including buttons, tables, inputs, and dynamic IDs (with patterns)
  - Map each navigation button ID to Flask route function via url_for() calls, including dynamic buttons
  - Define context variables available in template rendering, with data types and usage notes
- Use dynamic element ID patterns clearly with Jinja2 variable syntax as needed (e.g., id="view-exhibition-button-{{ exhibition.exhibition_id }}")

**Section 3: Data File Schemas**

- For each data text file:
  - Provide exact filename in data/ directory (e.g., data/exhibitions.txt)
  - Define pipe-delimited field order with exact field names as column headers for clarity (though no header line in actual files)
  - Describe content/purpose of the file
  - Provide 2-3 realistic example rows of data
- Ensure inclusion of all files referenced in system:
  users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt

CRITICAL SUCCESS CRITERIA:
- The specification must enable Backend Developer to implement full Flask app.py with all routes, data load/parsing based solely on Sections 1 & 3
- The specification must enable Frontend Developer to implement all templates exactly based solely on Section 2
- All element IDs, page titles, and context variable names must match precisely between sections
- Use write_text_file tool to output design_spec.md
- Do NOT include implementation code or frontend/backend logic beyond specification
- Do NOT assume any missing information beyond user_task_description

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

Your goal is to implement a complete backend Flask application based on the finalized design specifications.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) only from CONTEXT
- Implement all Flask routes with correct HTTP methods, function names, and route paths as specified
- Load, save, and manipulate data from data/*.txt files following exact schemas given in Section 3
- Adhere strictly to context variable names and data format (pipe-delimited, no headers)
- Do NOT read or consider Section 2 (Frontend) or any template files
- Do NOT add features not specified in design_spec.md

Implementation Requirements:
1. **Flask Application Setup:**
   ```python
   from flask import Flask, render_template, request, redirect, url_for
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root Route:**
   - Implement '/' route that redirects to dashboard page using `redirect(url_for('dashboard'))`

3. **Data Handling:**
   - Read/write data from files in 'data/' directory as specified
   - Use pipe-delimited parsing: `line.strip().split('|')`
   - Follow exact field order and data types as in Section 3 data schemas
   - Handle file not found or IO exceptions gracefully
   - No header lines included in data files

4. **Route Implementations:**
   - Implement every Flask route specified in Section 1 with exact function names
   - Use render_template with template names matching routes
   - Pass context variables exactly as specified (names, types, and structures)
   - Implement POST handlers according to specification, processing form data

5. **Best Practices:**
   - Use `if __name__ == "__main__": app.run(port=5000, debug=True)`
   - Use url_for for all internal redirects and links
   - Validate inputs and handle error cases sensibly without crashing

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app.py
- Function and route names must exactly match design_spec.md Section 1
- Data files must be parsed and saved exactly according to Section 3 schema (pipe-delimited, no header)
- Do NOT read or modify frontend templates or Section 2 content
- Do NOT add undocumented features or routes
- Ensure root route '/' redirects correctly to dashboard
- No inline code snippets in chat; all output must be saved via write_text_file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to develop all HTML templates for the application based on the provided design specifications.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) only from CONTEXT
- Implement all required HTML templates with exact element IDs, page titles, and navigation button mappings
- Use context variables as specified with correct Jinja2 syntax and variable names
- Do NOT read or modify backend code or Section 1 and 3 content
- Do NOT add templates not specified in design_spec.md or add extra UI features

Implementation Requirements:
1. **Template Structure:**
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Exact Page Title</title>
   </head>
   <body>
       <div id="container-id">
           <h1>Exact Page Title</h1>
           <!-- Content and controls as specified -->
       </div>
   </body>
   </html>
   ```

2. **File Naming and Location:**
   - Save all template files in the 'templates/' directory
   - Follow exact filenames provided in Section 2 (e.g. templates/dashboard.html)

3. **Element IDs:**
   - Implement ALL required element IDs with exact casing and spelling
   - For dynamic IDs (e.g., view-exhibition-button-{exhibition_id}) use Jinja2 syntax, e.g. id="view-exhibition-button-{{ exhibition.exhibition_id }}"

4. **Context Variables:**
   - Use context variables exactly as described, respecting types and structures
   - Loop over lists and access dict fields properly with Jinja2 syntax

5. **Navigation Buttons:**
   - Implement buttons and links that navigate using url_for calls exactly matching function names in the design spec
   - Use static links and dynamic links with parameters as specified

6. **Forms:**
   - Implement forms with correct method (POST/GET) and action using url_for
   - Input elements must have matching name attributes and IDs for correct backend integration

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all HTML template files
- Element IDs, page titles, and navigation button url_for calls must match design_spec.md Section 2 exactly
- Do NOT modify or read backend code or data schemas
- Do NOT add extra UI elements or templates beyond spec
- Do NOT provide code snippets solely in chat; all output must be saved via write_text_file
- Each template must be saved as a separate file (e.g., templates/dashboard.html, templates/exhibitions.html, etc.)

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
        ("BackendDeveloper", """Verify design_spec.md for backend relevance: completeness of Flask routes, including function names, HTTP methods, and data handling schemas for each required endpoint. "
                "Check that all data schemas reflect the full set of fields for data files in pipe-delimited format with exact field orders.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify design_spec.md for frontend relevance: completeness of HTML templates specification including all element IDs, page titles, navigation button mappings using url_for, and context variables needed for rendering.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Check app.py correctness: implementation of all Flask routes and HTTP methods, correctness of data file handling matching data schemas, adherence to route names and context variables, "
                "and correct root route redirecting to dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Check templates/*.html completeness and accuracy: presence of all required element IDs, correct rendering of context variables, accurate implementation of navigation button url_for calls, "
                "and conformity to specified page titles.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
async def architecture_design_phase():
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
    await execute(SystemArchitect, "Create design_spec.md with detailed Flask routes, HTML templates, and data schemas for VirtualMuseum per user_task_description")
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
        max_retries=2,
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
        max_retries=2,
        timeout_threshold=140,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement backend Flask app (app.py) from design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all HTML templates from design_spec.md Section 2 with exact element IDs and navigation")
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
        architecture_design_phase()
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
