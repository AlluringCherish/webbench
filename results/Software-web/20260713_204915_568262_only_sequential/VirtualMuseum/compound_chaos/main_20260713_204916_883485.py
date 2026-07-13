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
# 20260713_204916_883485/main_20260713_204916_883485.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the VirtualMuseum requirements and produce a detailed design_spec.md specifying pages, routes, and data structures\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first produces requirements_analysis.md capturing user needs and data specifications; \"\n        \"then SystemArchitect consumes it and writes design_spec.md covering Flask routes, page titles, element IDs, data file structures, \"\n        \"and navigation flows.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in capturing detailed software requirements from user task descriptions for web applications.\n\nYour goal is to extract all user requirements for the VirtualMuseum web application into a comprehensive requirements_analysis.md document.\n\nTask Details:\n- Read the full user_task_description artifact\n- Extract all page designs, including page titles, container IDs, UI elements, buttons, tables, and navigation flows\n- Extract detailed data storage specifications including each data file and its exact fields with formats and examples\n- Create a single requirements_analysis.md document containing full capture of all above information for SystemArchitect consumption\n\nInstructions:\n1. Organize extracted content clearly, grouping by pages and data files\n2. Include exact element IDs and their types (div, button, input, table, dropdown, etc.)\n3. Include navigation button IDs and their target pages\n4. Describe the data files with filename, field order, delimiter, and provide sample data rows\n5. Avoid adding assumptions or interpretations beyond the provided user_task_description\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to save requirements_analysis.md\n- Preserve exact element IDs, file names, and field orders from user_task_description\n- Output a markdown format file with clear, structured sections\n- Ensure completeness so SystemArchitect can design without needing further clarifications\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in designing Flask web application specifications including routing, UI layout, navigation, and data schemas.\n\nYour goal is to create a comprehensive design_spec.md defining the entire Flask app architecture for VirtualMuseum, enabling developers to implement backend and frontend independently.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md for full context\n- Define all Flask endpoints with URL paths, function names (lowercase with underscores), HTTP methods, templates rendered, and context variables passed\n- Define all HTML template pages with exact page titles and a complete list of element IDs (divs, buttons, inputs, tables, dropdowns, etc.)\n- Specify navigation flows starting from the Dashboard page and all button actions linking pages via url_for functions\n- Specify all local data files in data/ directory with exact file names, pipe-delimited fields in precise order, field names, and example data rows reflecting user data storage section\n\nImplementation Instructions:\n1. Flask Routes Specification:\n   - Use clear function names reflecting page purpose\n   - Include '/' root route redirecting to dashboard page\n   - Map buttons and dynamic actions (e.g., view-exhibition-button-{exhibition_id}) to appropriate routes with parameter names\n\n2. HTML Templates Specification:\n   - Specify template filenames (e.g., dashboard.html, artifact_catalog.html)\n   - List all element IDs exactly as provided, including dynamic ID patterns with template variables\n   - Include page titles for <title> and <h1> tags\n\n3. Data File Specifications:\n   - For each data file: path, delimiter ('|'), field order with descriptive names, example data rows\n   - Ensure all fields from user specification appear exactly in order\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md supports independent backend/frontend implementation without missing details\n- All element IDs and navigation mappings exactly match those declared in requirements_analysis.md and user task\n- Function names are consistent and use snake_case\n- Data file schemas are complete and precise matching user examples\n- Use write_text_file tool to save design_spec.md exactly as specified\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md fully and accurately captures all page specifications, UI element IDs, navigation, and data file details.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement a Flask-based VirtualMuseum web application with all specified pages, navigation, and data file integration as app_draft.py and templates drafts\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"Developer writes app_draft.py implementing all Flask routes and logic based on design_spec.md; TemplateDesigner creates draft HTML templates under templates_draft/ directory with exact element IDs, titles, buttons, and navigation; only after both complete, IntegrationEngineer combines drafts into final app.py and template files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Developer\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with expertise in backend logic and data integration.\n\nYour goal is to implement all backend routes and logic for the VirtualMuseum based on design specifications, enabling features for exhibitions, artifacts, audio guides, tickets, virtual events, and collections with data stored locally.\n\nTask Details:\n- Read design_spec.md and user_task_description from CONTEXT\n- Produce a complete Flask backend script app_draft.py\n- Implement all Flask routes starting from Dashboard page with proper navigation\n- Read/write data files under 'data' directory using specified pipe-delimited schemas\n- DO NOT implement frontend templates in this step\n\nImplementation Requirements:\n1. **Flask Application Setup:**\n   - Initialize Flask app with proper configuration\n   - Setup root '/' route redirecting to dashboard page\n2. **Routes and Logic:**\n   - Implement all routes defined in design_spec.md for exhibitions, artifacts, audio guides, tickets, events, collections\n   - Each route must render proper templates (placeholders if necessary) and pass correct context variables\n   - Handle GET and POST requests as applicable (e.g., ticket purchasing, event registration)\n3. **Data File Integration:**\n   - Parse and write data files under 'data' directory\n   - Follow exact field order and pipe-delimited format specified in design_spec.md and user_task_description\n   - Implement robust file I/O with error handling\n4. **Code Quality:**\n   - Use modular functions where possible\n   - Comment code concisely using single-quote docstrings or inline hash comments\n   - Adhere strictly to design_spec.md for field names, variable names, and route function names\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save your output as app_draft.py\n- Follow design_spec.md exactly without assumptions\n- Ensure all route functions match design_spec.md and user_task_description\n- Focus on backend logic only; do not create or embed HTML here\n- Provide fully working Flask route structure starting from dashboard\n\nOutput: app_draft.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"TemplateDesigner\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask web applications.\n\nYour goal is to create draft HTML templates under templates_draft/ directory that replicate the full UI page structures for VirtualMuseum, including exact element IDs, buttons, and page titles as per design specifications.\n\nTask Details:\n- Read design_spec.md and user_task_description from CONTEXT\n- Implement all HTML templates required to build all specified pages\n- Use exact element IDs and page titles as defined in design_spec.md\n- Include buttons and navigation elements with correct IDs and hrefs (placeholders if needed)\n- Save all templates inside templates_draft/ directory\n- Do NOT implement backend logic or routes\n\nImplementation Requirements:\n1. **Template Structure:**\n   - Use standard HTML5 with Jinja2 templating where needed\n   - Include matching <title> and <h1> tags per page titles in design_spec.md\n   - Replicate all container divs, tables, inputs, dropdowns, and buttons with exact IDs\n2. **Dynamic Elements:**\n   - For repeating elements with dynamic IDs (e.g., view-exhibition-button-{exhibition_id}), use Jinja2 loops and templates\n   - ID format example: id=\"view-exhibition-button-{{ exhibition.exhibition_id }}\"\n3. **Navigation:**\n   - Include navigation buttons as per design_spec.md with correct target pages (use url_for placeholders)\n4. **Code Quality:**\n   - Use single-quote docstrings or hash comments for any inline comments\n   - Follow best practices for indented readable HTML/Jinja2 code\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save templates in templates_draft/*.html\n- All element IDs and page titles must exactly match design_spec.md\n- Do NOT include backend logic or Python code here\n- Templates must be drafts ready for integration and backend linking\n- Ensure all pages listed in user_task_description are covered\n\nOutput: templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in integrating backend Flask applications with frontend templates.\n\nYour goal is to integrate app draft code and template drafts into final working deliverables app.py and templates/*.html with strict adherence to design specifications for VirtualMuseum.\n\nTask Details:\n- Read app_draft.py, templates_draft/*.html, design_spec.md, and user_task_description from CONTEXT\n- Combine backend Flask routes and frontend templates into final app.py and templates/*.html\n- Ensure all render_template calls in app.py point to templates/ directory\n- Resolve any inconsistencies between backend and template drafts, enforcing exact element IDs, page titles, button IDs, and navigation\n- Validate that integration matches all requirements in design_spec.md\n\nIntegration Requirements:\n1. **Backend and Frontend Integration:**\n   - Modify app_draft.py code as needed to use final templates paths and names\n   - Ensure all Flask routes properly render final templates/*.html with correct context variables\n2. **Template Finalization:**\n   - Move templates from templates_draft/ to templates/\n   - Verify all element IDs and UI elements exactly match design_spec.md\n   - Fix any mismatches in buttons or navigation elements\n3. **Quality Assurance:**\n   - Confirm all pages start at Dashboard route\n   - Ensure no dangling routes or broken references remain\n   - Maintain single-quote docstring or hash comment style in all code and templates\n4. **Output Packaging:**\n   - Save completed app.py and templates/*.html files ready for deployment\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html\n- Enforce exact matching of all element IDs and page titles from design_spec.md\n- All render_template calls must reference templates/*.html, not templates_draft/\n- Provide a complete, consistent, and deployable Flask web app structure\n- Do NOT leave integration gaps or placeholder references to drafts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"Developer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"TemplateDesigner\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Developer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Verify app_draft.py correctness against design_spec.md before integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"TemplateDesigner\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Check templates_draft/*.html for exact UI element IDs, titles, navigation buttons, and consistent styling as per design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the final app.py and templates/*.html for Flask runtime correctness and full compliance with design_spec.md, and produce the final corrected application\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator tests app.py and templates/*.html for syntax, runtime behavior, Flask test client routing, and UI compliance writing validation_report.md; \"\n        \"FinalFixer corrects issues from validation_report.md and rewrites app.py and templates/*.html accordingly.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer with expertise in Python Flask applications and frontend HTML testing.\n\nYour goal is to validate the runtime correctness and UI compliance of the final Flask backend app.py and templates/*.html.\n\nTask Details:\n- Read app.py and all templates/*.html files thoroughly for syntax and runtime issues\n- Use design_spec.md to verify full compliance with Flask routes, page titles, and UI element IDs\n- Produce a comprehensive validation_report.md documenting all findings and issues\n- Use user_task_description for contextual understanding to ensure requirements coverage\n\n**Validation Steps:**\n\n1. **Syntax and Runtime Validation:**\n   - Run syntax and runtime checks on app.py using validate_python_file tool\n   - Ensure no exceptions or errors on startup\n\n2. **Flask Routing Behavior:**\n   - Use Flask test client in execution environment to test all routes starting from the dashboard '/'\n   - Verify each route returns expected page, status code 200, and redirects as specified\n   - Ensure navigation buttons lead to correct routes\n\n3. **Frontend UI Validation:**\n   - Parse templates/*.html for exact page titles matching design_spec.md page titles\n   - Verify presence of all required element IDs exactly as specified per page\n   - Check dynamic element ID patterns for repeated or parameterized elements\n   - Validate navigation button IDs link properly using url_for function names consistent with routes\n\n4. **Reporting:**\n   - Document issues by severity (Critical, Major, Minor)\n   - List missing routes, mismatched titles, missing/misnamed UI elements, navigation errors\n   - Provide line or section references where possible\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for checks\n- Use write_text_file to produce validation_report.md\n- Report must clearly differentiate backend and frontend issues\n- Validate strictly against design_spec.md, using user_task_description as supplemental context\n- Output only the validation_report.md file as final output of this phase\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FinalFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specialized in Python Flask web applications and frontend HTML templating.\n\nYour goal is to apply all corrections and fixes from validation_report.md to produce a final, fully compliant app.py and set of templates/*.html files.\n\nTask Details:\n- Read validation_report.md carefully to understand all identified issues\n- Use original app.py and templates/*.html as base for corrections\n- Use design_spec.md and user_task_description as source of truth for specifications\n- Correct syntax, runtime, routing, page titles, element IDs, and navigation issues as specified\n- Produce corrected app.py and templates/*.html files conforming fully to design_spec.md\n\n**Fixing Instructions:**\n\n1. **Backend Corrections:**\n   - Fix any syntax or runtime errors in app.py\n   - Adjust Flask routes to match design_spec.md exactly\n   - Ensure route handlers pass correct context variables with correct names and types\n   - Fix redirects, HTTP methods, and form handling inconsistencies\n\n2. **Frontend Corrections:**\n   - Edit templates/*.html to fix page titles to exactly match design_spec.md\n   - Add missing or rename incorrect element IDs\n   - Correct navigation button hrefs and dynamic element IDs\n   - Validate Jinja2 syntax and context variable usage for correctness\n\n3. **Final Validation:**\n   - Ensure all fixes fully resolve issues listed in validation_report.md\n   - Maintain code quality and clarity while fixing\n   - Do not add features or modifications beyond the scope of reported issues\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output corrected app.py and templates/*.html\n- Outputs must fully conform to design_spec.md and user_task_description\n- Deliver only updated app.py and templates/*.html files as final outputs of this phase\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"FinalFixer\",\n            \"review_criteria\": (\n                \"Ensure validation_report.md covers all runtime, syntax and UI compliance issues.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FinalFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify final app.py and templates/*.html fully implement all requirements and resolve validation report issues.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Business Analyst specializing in capturing detailed software requirements from user task descriptions for web applications.

Your goal is to extract all user requirements for the VirtualMuseum web application into a comprehensive requirements_analysis.md document.

Task Details:
- Read the full user_task_description artifact
- Extract all page designs, including page titles, container IDs, UI elements, buttons, tables, and navigation flows
- Extract detailed data storage specifications including each data file and its exact fields with formats and examples
- Create a single requirements_analysis.md document containing full capture of all above information for SystemArchitect consumption

Instructions:
1. Organize extracted content clearly, grouping by pages and data files
2. Include exact element IDs and their types (div, button, input, table, dropdown, etc.)
3. Include navigation button IDs and their target pages
4. Describe the data files with filename, field order, delimiter, and provide sample data rows
5. Avoid adding assumptions or interpretations beyond the provided user_task_description

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to save requirements_analysis.md
- Preserve exact element IDs, file names, and field orders from user_task_description
- Output a markdown format file with clear, structured sections
- Ensure completeness so SystemArchitect can design without needing further clarifications

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in designing Flask web application specifications including routing, UI layout, navigation, and data schemas.

Your goal is to create a comprehensive design_spec.md defining the entire Flask app architecture for VirtualMuseum, enabling developers to implement backend and frontend independently.

Task Details:
- Read user_task_description and requirements_analysis.md for full context
- Define all Flask endpoints with URL paths, function names (lowercase with underscores), HTTP methods, templates rendered, and context variables passed
- Define all HTML template pages with exact page titles and a complete list of element IDs (divs, buttons, inputs, tables, dropdowns, etc.)
- Specify navigation flows starting from the Dashboard page and all button actions linking pages via url_for functions
- Specify all local data files in data/ directory with exact file names, pipe-delimited fields in precise order, field names, and example data rows reflecting user data storage section

Implementation Instructions:
1. Flask Routes Specification:
   - Use clear function names reflecting page purpose
   - Include '/' root route redirecting to dashboard page
   - Map buttons and dynamic actions (e.g., view-exhibition-button-{exhibition_id}) to appropriate routes with parameter names

2. HTML Templates Specification:
   - Specify template filenames (e.g., dashboard.html, artifact_catalog.html)
   - List all element IDs exactly as provided, including dynamic ID patterns with template variables
   - Include page titles for <title> and <h1> tags

3. Data File Specifications:
   - For each data file: path, delimiter ('|'), field order with descriptive names, example data rows
   - Ensure all fields from user specification appear exactly in order

CRITICAL SUCCESS CRITERIA:
- design_spec.md supports independent backend/frontend implementation without missing details
- All element IDs and navigation mappings exactly match those declared in requirements_analysis.md and user task
- Function names are consistent and use snake_case
- Data file schemas are complete and precise matching user examples
- Use write_text_file tool to save design_spec.md exactly as specified

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "Developer": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with expertise in backend logic and data integration.

Your goal is to implement all backend routes and logic for the VirtualMuseum based on design specifications, enabling features for exhibitions, artifacts, audio guides, tickets, virtual events, and collections with data stored locally.

Task Details:
- Read design_spec.md and user_task_description from CONTEXT
- Produce a complete Flask backend script app_draft.py
- Implement all Flask routes starting from Dashboard page with proper navigation
- Read/write data files under 'data' directory using specified pipe-delimited schemas
- DO NOT implement frontend templates in this step

Implementation Requirements:
1. **Flask Application Setup:**
   - Initialize Flask app with proper configuration
   - Setup root '/' route redirecting to dashboard page
2. **Routes and Logic:**
   - Implement all routes defined in design_spec.md for exhibitions, artifacts, audio guides, tickets, events, collections
   - Each route must render proper templates (placeholders if necessary) and pass correct context variables
   - Handle GET and POST requests as applicable (e.g., ticket purchasing, event registration)
3. **Data File Integration:**
   - Parse and write data files under 'data' directory
   - Follow exact field order and pipe-delimited format specified in design_spec.md and user_task_description
   - Implement robust file I/O with error handling
4. **Code Quality:**
   - Use modular functions where possible
   - Comment code concisely using single-quote docstrings or inline hash comments
   - Adhere strictly to design_spec.md for field names, variable names, and route function names

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save your output as app_draft.py
- Follow design_spec.md exactly without assumptions
- Ensure all route functions match design_spec.md and user_task_description
- Focus on backend logic only; do not create or embed HTML here
- Provide fully working Flask route structure starting from dashboard

Output: app_draft.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}],

    },

    "TemplateDesigner": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask web applications.

Your goal is to create draft HTML templates under templates_draft/ directory that replicate the full UI page structures for VirtualMuseum, including exact element IDs, buttons, and page titles as per design specifications.

Task Details:
- Read design_spec.md and user_task_description from CONTEXT
- Implement all HTML templates required to build all specified pages
- Use exact element IDs and page titles as defined in design_spec.md
- Include buttons and navigation elements with correct IDs and hrefs (placeholders if needed)
- Save all templates inside templates_draft/ directory
- Do NOT implement backend logic or routes

Implementation Requirements:
1. **Template Structure:**
   - Use standard HTML5 with Jinja2 templating where needed
   - Include matching <title> and <h1> tags per page titles in design_spec.md
   - Replicate all container divs, tables, inputs, dropdowns, and buttons with exact IDs
2. **Dynamic Elements:**
   - For repeating elements with dynamic IDs (e.g., view-exhibition-button-{exhibition_id}), use Jinja2 loops and templates
   - ID format example: id="view-exhibition-button-{{ exhibition.exhibition_id }}"
3. **Navigation:**
   - Include navigation buttons as per design_spec.md with correct target pages (use url_for placeholders)
4. **Code Quality:**
   - Use single-quote docstrings or hash comments for any inline comments
   - Follow best practices for indented readable HTML/Jinja2 code

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save templates in templates_draft/*.html
- All element IDs and page titles must exactly match design_spec.md
- Do NOT include backend logic or Python code here
- Templates must be drafts ready for integration and backend linking
- Ensure all pages listed in user_task_description are covered

Output: templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in integrating backend Flask applications with frontend templates.

Your goal is to integrate app draft code and template drafts into final working deliverables app.py and templates/*.html with strict adherence to design specifications for VirtualMuseum.

Task Details:
- Read app_draft.py, templates_draft/*.html, design_spec.md, and user_task_description from CONTEXT
- Combine backend Flask routes and frontend templates into final app.py and templates/*.html
- Ensure all render_template calls in app.py point to templates/ directory
- Resolve any inconsistencies between backend and template drafts, enforcing exact element IDs, page titles, button IDs, and navigation
- Validate that integration matches all requirements in design_spec.md

Integration Requirements:
1. **Backend and Frontend Integration:**
   - Modify app_draft.py code as needed to use final templates paths and names
   - Ensure all Flask routes properly render final templates/*.html with correct context variables
2. **Template Finalization:**
   - Move templates from templates_draft/ to templates/
   - Verify all element IDs and UI elements exactly match design_spec.md
   - Fix any mismatches in buttons or navigation elements
3. **Quality Assurance:**
   - Confirm all pages start at Dashboard route
   - Ensure no dangling routes or broken references remain
   - Maintain single-quote docstring or hash comment style in all code and templates
4. **Output Packaging:**
   - Save completed app.py and templates/*.html files ready for deployment

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html
- Enforce exact matching of all element IDs and page titles from design_spec.md
- All render_template calls must reference templates/*.html, not templates_draft/
- Provide a complete, consistent, and deployable Flask web app structure
- Do NOT leave integration gaps or placeholder references to drafts

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app_draft.py', 'source': 'Developer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'TemplateDesigner'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer with expertise in Python Flask applications and frontend HTML testing.

Your goal is to validate the runtime correctness and UI compliance of the final Flask backend app.py and templates/*.html.

Task Details:
- Read app.py and all templates/*.html files thoroughly for syntax and runtime issues
- Use design_spec.md to verify full compliance with Flask routes, page titles, and UI element IDs
- Produce a comprehensive validation_report.md documenting all findings and issues
- Use user_task_description for contextual understanding to ensure requirements coverage

**Validation Steps:**

1. **Syntax and Runtime Validation:**
   - Run syntax and runtime checks on app.py using validate_python_file tool
   - Ensure no exceptions or errors on startup

2. **Flask Routing Behavior:**
   - Use Flask test client in execution environment to test all routes starting from the dashboard '/'
   - Verify each route returns expected page, status code 200, and redirects as specified
   - Ensure navigation buttons lead to correct routes

3. **Frontend UI Validation:**
   - Parse templates/*.html for exact page titles matching design_spec.md page titles
   - Verify presence of all required element IDs exactly as specified per page
   - Check dynamic element ID patterns for repeated or parameterized elements
   - Validate navigation button IDs link properly using url_for function names consistent with routes

4. **Reporting:**
   - Document issues by severity (Critical, Major, Minor)
   - List missing routes, mismatched titles, missing/misnamed UI elements, navigation errors
   - Provide line or section references where possible

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for checks
- Use write_text_file to produce validation_report.md
- Report must clearly differentiate backend and frontend issues
- Validate strictly against design_spec.md, using user_task_description as supplemental context
- Output only the validation_report.md file as final output of this phase

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "FinalFixer": {
        "prompt": (
            """You are a Software Developer specialized in Python Flask web applications and frontend HTML templating.

Your goal is to apply all corrections and fixes from validation_report.md to produce a final, fully compliant app.py and set of templates/*.html files.

Task Details:
- Read validation_report.md carefully to understand all identified issues
- Use original app.py and templates/*.html as base for corrections
- Use design_spec.md and user_task_description as source of truth for specifications
- Correct syntax, runtime, routing, page titles, element IDs, and navigation issues as specified
- Produce corrected app.py and templates/*.html files conforming fully to design_spec.md

**Fixing Instructions:**

1. **Backend Corrections:**
   - Fix any syntax or runtime errors in app.py
   - Adjust Flask routes to match design_spec.md exactly
   - Ensure route handlers pass correct context variables with correct names and types
   - Fix redirects, HTTP methods, and form handling inconsistencies

2. **Frontend Corrections:**
   - Edit templates/*.html to fix page titles to exactly match design_spec.md
   - Add missing or rename incorrect element IDs
   - Correct navigation button hrefs and dynamic element IDs
   - Validate Jinja2 syntax and context variable usage for correctness

3. **Final Validation:**
   - Ensure all fixes fully resolve issues listed in validation_report.md
   - Maintain code quality and clarity while fixing
   - Do not add features or modifications beyond the scope of reported issues

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output corrected app.py and templates/*.html
- Outputs must fully conform to design_spec.md and user_task_description
- Deliver only updated app.py and templates/*.html files as final outputs of this phase

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("SystemArchitect", """Verify requirements_analysis.md fully and accurately captures all page specifications, UI element IDs, navigation, and data file details.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'Developer': [
        ("IntegrationEngineer", """Verify app_draft.py correctness against design_spec.md before integration.""", [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'TemplateDesigner': [
        ("IntegrationEngineer", """Check templates_draft/*.html for exact UI element IDs, titles, navigation buttons, and consistent styling as per design_spec.md.""", [{'type': 'text_file', 'name': 'templates_draft/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'WebValidator': [
        ("FinalFixer", """Ensure validation_report.md covers all runtime, syntax and UI compliance issues.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FinalFixer': [
        ("RequirementsAnalyst", """Verify final app.py and templates/*.html fully implement all requirements and resolve validation report issues.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=200,
        failure_threshold=1,
        recovery_time=30
    )
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=240,
        failure_threshold=1,
        recovery_time=30
    )

    # Sequential flow execution
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and create requirements_analysis.md containing all page designs, element IDs, navigation flows, and data file specifications.")

    # Read requirements_analysis.md content for SystemArchitect input
    requirements_analysis_md = ""
    try:
        requirements_analysis_md = open("requirements_analysis.md").read()
    except:
        pass

    await execute(SystemArchitect,
                  f"Using user_task_description and the following requirements_analysis.md content, create design_spec.md specifying Flask routes with function names, HTTP methods, templates, context variables; HTML templates with exact page titles and element IDs; navigation flows; and data file schemas.\n\n=== requirements_analysis.md ===\n{requirements_analysis_md}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    Developer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Developer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    TemplateDesigner = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="TemplateDesigner",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential Flow execution:
    # 1. Developer implements backend app_draft.py
    await execute(Developer, "Implement all backend Flask routes and logic for VirtualMuseum in app_draft.py based on design_spec.md and user_task_description. Focus on backend logic only, no templates.")
    
    # 2. TemplateDesigner creates draft HTML templates in templates_draft/
    await execute(TemplateDesigner, "Create draft HTML templates for VirtualMuseum in templates_draft/ directory with exact element IDs, page titles, buttons, and navigation based on design_spec.md and user_task_description. No backend logic.")
    
    # 3. IntegrationEngineer integrates app_draft.py and templates_draft/*.html into final app.py and templates/*.html fully consistent with design_spec.md and user_task_description
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # Since templates_draft/*.html is multiple files, read all files matching pattern 'templates_draft/*.html'
    import glob
    import os

    templates_draft_all_content = {}
    for filepath in glob.glob("templates_draft/*.html"):
        try:
            with open(filepath, "r") as f:
                templates_draft_all_content[os.path.basename(filepath)] = f.read()
        except:
            templates_draft_all_content[os.path.basename(filepath)] = ""

    # Compose message for IntegrationEngineer including app_draft.py and all templates draft content
    templates_draft_combined = "\n\n".join([f"=== {filename} ===\n{content}" for filename, content in templates_draft_all_content.items()])

    msg_integration = (
        "Integrate backend app_draft.py and HTML templates drafts into final app.py and templates/*.html ensuring exact element IDs, page titles, buttons, navigation, and matching design_spec.md.\n\n"
        "=== app_draft.py ===\n" + app_draft_content + "\n\n"
        + templates_draft_combined
    )
    await execute(IntegrationEngineer, msg_integration)
# Phase2_End

# Phase3_Start

async def verification_phase():
    WebValidator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    FinalFixer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FinalFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file artifacts for injection
    app_py_content, templates_content, design_spec_content, user_task_desc = "", "", "", ""
    try:
        app_py_content = open("app.py").read()
    except:
        pass
    try:
        # Concatenate all templates/*.html files content for injection
        import glob
        templates_files = glob.glob("templates/*.html")
        templates_content = ""
        for tf in templates_files:
            try:
                content = open(tf).read()
                templates_content += f"=== {tf} ===\n{content}\n\n"
            except:
                continue
    except:
        pass
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    try:
        user_task_desc = CONTEXT.get("user_task_description", [])
        user_task_desc = user_task_desc[-1]["content"] if user_task_desc else ""
    except:
        pass

    # Step 1: WebValidator validates runtime correctness and UI compliance
    msg_validator = (
        "Validate app.py and templates/*.html for syntax, runtime correctness, Flask routing behavior, and "
        "UI compliance strictly against design_spec.md and user_task_description. Output a comprehensive "
        "validation_report.md detailing all backend and frontend issues found."
        f"\n\n=== app.py ===\n{app_py_content}\n"
        f"=== templates/*.html ===\n{templates_content}"
        f"=== design_spec.md ===\n{design_spec_content}\n"
        f"=== user_task_description ===\n{user_task_desc}"
    )
    await execute(WebValidator, msg_validator)

    # Step 2: FinalFixer reads validation_report.md and original sources, applies fixes accordingly
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    msg_finalfixer = (
        "Read validation_report.md below and apply all corrections to produce a fully compliant, corrected app.py "
        "and templates/*.html files according to design_spec.md and user_task_description. Do not add any "
        "features beyond the reported issues.\n\n"
        "=== validation_report.md ===\n"
        f"{validation_report_content}\n\n"
        "=== original app.py ===\n"
        f"{app_py_content}\n\n"
        "=== original templates/*.html ===\n"
        f"{templates_content}\n\n"
        "=== design_spec.md ===\n"
        f"{design_spec_content}\n\n"
        "=== user_task_description ===\n"
        f"{user_task_desc}"
    )
    await execute(FinalFixer, msg_finalfixer)
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
