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
# 20260713_204916_621901/main_20260713_204916_621901.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the RealEstate requirements and produce a complete design_spec.md detailing pages, routes, element IDs, and data contracts.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md detailing all pages, elements, and data storage formats; \"\n        \"WebArchitect then reads requirements_analysis.md and produces design_spec.md with Flask route definitions, page templates, \"\n        \"element IDs, and data file interface contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in detailed web application functional analysis and documentation.\n\nYour goal is to extract and document all functional requirements from user task descriptions into a comprehensive analysis document.\n\nTask Details:\n- Read the user_task_description artifact for the RealEstate web application\n- Produce requirements_analysis.md detailing all pages with exact element IDs and types\n- Document user interactions, navigation flows, and button/input actions\n- Specify data storage formats and file layouts exactly as given\n- Ensure coverage of every page, element, and data file specified\n\nDocumentation Requirements:\n1. Pages and Elements:\n   - List each page with its exact page title\n   - Enumerate all elements with exact IDs, types, and brief descriptions\n   - Capture dynamic IDs with naming patterns (e.g., view-property-button-{property_id})\n\n2. User Interaction Flows:\n   - Describe button functions and navigation targets\n   - Detail input field purposes and expected user input types\n\n3. Data Storage:\n   - Describe each data file in 'data/' folder with exact field names and order\n   - Include examples rows as provided\n   - Specify data file format (pipe-delimited)\n\n4. Format:\n   - Use Markdown format for clarity\n   - Use sections, tables, and bullet points for ease of reading\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to output requirements_analysis.md\n- Preserve all IDs and data format details exactly as per user task\n- Do not add or remove features; stay within user task scope\n- Document precisely as provided with no assumptions\n- Output a human-readable and well-organized markdown file\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and specification.\n\nYour goal is to convert detailed requirements analysis into a precise design specification document that defines Flask app routes, page templates, element IDs, user interactions, and data file contracts.\n\nTask Details:\n- Read requirements_analysis.md artifact produced by RequirementsAnalyst\n- Create design_spec.md containing complete Flask route definitions starting from the Dashboard page\n- For each page, specify page titles and all element IDs exactly\n- Include navigation routes triggered by buttons and links\n- Define data file reading and writing contracts matching data formats exactly\n- Specify data file paths, field order, delimiter, and example rows\n\nDesign Specification Requirements:\n1. Flask Routes:\n   - List route paths and associated Flask function names (snake_case)\n   - Specify HTTP methods (GET, POST) and expected templates rendered\n   - Define context variables passed to templates with types\n\n2. Page Templates:\n   - Specify exact template filenames corresponding to routes\n   - Include page titles and all element IDs per page\n   - Define user interaction elements and navigation flows\n\n3. Data Files:\n   - Provide data file paths (data/*.txt)\n   - Define pipe-delimited field orders matching requirements_analysis.md\n   - Include brief field descriptions and example data rows\n\n4. Format:\n   - Use markdown format with clear sections and tables\n   - Ensure completeness and clarity to support independent backend/frontend development\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- Adhere strictly to IDs, field orders, and routes from requirements_analysis.md and user task\n- The root route '/' must redirect to the Dashboard page route\n- Maintain consistent function naming and capitalization\n- Do not invent or omit any specifications beyond the given data\n- Output a human-readable, structured markdown file\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": \"Check that requirements_analysis.md thoroughly covers all pages, elements with precise IDs, user navigation flow, and data storage formats as per user task.\",\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the RealEstate Flask web application producing app_draft.py and templates_draft/*.html based on design_spec.md\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftDeveloper writes app_draft.py implementing all Flask routes, handlers, and logic, and templates_draft/*.html for every page \"\n        \"based on design_spec.md; IntegrationDeveloper then refines them into final app.py and templates/*.html with all navigation and data integration.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftDeveloper\",\n            \"prompt\": \"\"\"You are a Flask Web Application Developer specializing in building Python Flask apps with Jinja2 templating.\n\nYour goal is to write a complete draft Flask application (app_draft.py) and corresponding HTML template drafts (templates_draft/*.html) that implement all routes, pages, and functionality described in the design_spec.md.\n\nTask Details:\n- Read the full design_spec.md to understand all routes, page titles, element IDs, and required user interactions\n- Implement all Flask routes and handlers starting from the Dashboard page\n- Create templates_draft/*.html implementing exact element IDs and page titles on all pages\n- Implement form handling for user inputs and CRUD operations on local text file data as specified\n- Generate app_draft.py and all template draft files in templates_draft/\n\nImplementation Guidelines:\n1. Flask Application:\n   - Set up Flask app with routes matching all pages described in design_spec.md\n   - Use render_template to serve templates_draft/*.html\n   - Implement CRUD logic to read/update local data text files following the exact schemas\n   - Start root route at Dashboard page\n2. Template Drafts:\n   - Use Jinja2 syntax for dynamic content and looping over data lists\n   - Include all specified element IDs exactly as described\n   - Page titles must match design_spec.md exactly in <title> and <h1> tags\n3. Forms and Buttons:\n   - Implement form handlers using Flask request.form and appropriate methods (GET/POST)\n   - Use button click handling to navigate routes or submit forms\n4. Data Persistence:\n   - Handle local text files with exact parsing of pipe-delimited fields per design_spec.md\n   - Read and write data files atomically for data consistency\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save 'app_draft.py' and all 'templates_draft/*.html' files\n- Ensure all routes start from the Dashboard page exactly as specified\n- Maintain exact element IDs and page titles across templates\n- Implement full CRUD logic on local text files matching the provided data schemas\n- Provide a fully runnable draft Flask app with template drafts\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationDeveloper\",\n            \"prompt\": \"\"\"You are a Software Integrator specializing in Flask web applications and template integration.\n\nYour goal is to integrate the draft Flask app (app_draft.py) and draft templates (templates_draft/*.html) into a final polished Flask application (app.py) and final templates (templates/*.html), ensuring seamless navigation, exact element IDs, and proper data persistence.\n\nTask Details:\n- Read design_spec.md, the draft 'app_draft.py', and all 'templates_draft/*.html'\n- Refine and unify app.py with complete route handling starting from Dashboard page\n- Integrate templates into templates/*.html with consistent element IDs and exact page titles\n- Resolve cross-references between routes and templates to ensure full navigation and data integration\n- Ensure the app writes/reads all local text files correctly and persists all CRUD operations\n- Clean up draft code for robustness and maintainability\n\nIntegration Guidelines:\n1. Route Consistency:\n   - Confirm all routes originate or link to Dashboard page as entry point\n   - Ensure all route handlers align with templates and data operations\n2. Template Refinement:\n   - Confirm templates have exact element IDs and titles\n   - Fix any broken links or missing navigation buttons\n   - Ensure templates are organized in templates/ directory\n3. Data Management:\n   - Verify data files are correctly accessed and updated atomically\n   - Confirm consistency with design_spec.md data schemas\n4. Final Packaging:\n   - Provide a complete runnable app.py and all templates/*.html\n   - Ensure no draft artifacts remain (no templates_draft/ usage)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final 'app.py' and 'templates/*.html'\n- Maintain exact page titles and element IDs as specified\n- Ensure full data persistence with local text files per design spec\n- All pages must be reachable starting from Dashboard page\n- No usage of draft files or paths in final output\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftDeveloper\",\n            \"reviewer_agent\": \"IntegrationDeveloper\",\n            \"review_criteria\": \"Verify app_draft.py and templates_draft/*.html correctly implement all routes, page titles, element IDs, user interactions, and local text file data management as specified in design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate app.py and templates/*.html for full functionality and conformity, producing validation_report.md and final corrected app.py and templates\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"AppValidator runs syntax and runtime validation on app.py and templates/*.html and writes validation_report.md; \"\n        \"FinalFixer applies fixes and refinements to app.py and templates/*.html until all issues are resolved.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppValidator\",\n            \"prompt\": \"\"\"You are a Software Quality Engineer specializing in Python Flask web application validation.\n\nYour goal is to validate the entire RealEstate web application implementation to ensure full functionality and specification conformity.\n\nTask Details:\n- Read design_spec.md for complete specifications including all pages, routes, element IDs, and data schemas\n- Analyze app.py and all templates/*.html files for syntax correctness and runtime behavior\n- Verify all pages and routes are implemented exactly as specified\n- Check that element IDs appear exactly as required in templates\n- Confirm app.py correctly reads/writes all required local text data files according to schemas\n- Ensure the app launches correctly starting from the Dashboard page\n\nValidation Requirements:\n1. **Syntax and Runtime Validation:**\n   - Use validate_python_file tool to check syntax and runtime of app.py\n   - Execute critical route handlers to confirm runtime stability\n\n2. **Route and Page Coverage:**\n   - Verify all specified pages with correct routes exist\n   - Confirm HTTP methods are appropriate per specification\n   - Routes should return correct template files\n\n3. **Template Element IDs:**\n   - Examine templates/*.html for all required element IDs (static and dynamic)\n   - Ensure dynamic IDs use correct templating syntax matching design_spec.md patterns\n\n4. **Data File Operations:**\n   - Check proper file I/O for data files (properties.txt, inquiries.txt, favorites.txt, agents.txt, locations.txt)\n   - Validate correct parsing with exact field order and pipe-delimited format\n\n5. **Startup Behavior:**\n   - Ensure root route redirects or renders the Dashboard page correctly\n\nProduce a detailed validation_report.md enumerating:\n- Syntax or runtime errors found\n- Missing or incorrect routes or pages\n- Missing, misspelled, or incorrectly implemented element IDs\n- Data file parsing or writing issues\n- Any deviations from startup requirements\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file for syntax/runtime checks\n- MUST use execute_python_code for runtime verification where feasible\n- Use write_text_file tool to output complete validation_report.md\n- Output report must be clear for guiding correction in next phase\n- Focus strictly on files: app.py, templates/*.html, design_spec.md for validation context\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FinalFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in code refinement and bug fixes for Flask web applications.\n\nYour goal is to apply corrections and improvements to app.py and templates/*.html based on validation_report.md to ensure full specification compliance and flawless operation.\n\nTask Details:\n- Read validation_report.md carefully for all syntax, runtime, and specification issues identified\n- Review design_spec.md for original detailed design requirements as needed\n- Modify app.py to fix all reported errors and improve robustness in route handling and data file operations\n- Update templates/*.html to correct any missing or incorrect element IDs and ensure all pages comply with design_spec.md\n- Ensure the application starts correctly at the Dashboard page and all features work as intended\n\nImplementation Guidance:\n1. **Fix Syntax and Runtime Errors:**\n   - Correct all Python syntax errors reported\n   - Adjust code logic to resolve runtime issues or exceptions\n\n2. **Route and Page Corrections:**\n   - Add missing routes or update existing ones to match exact specifications\n   - Ensure route handlers use correct templates and context variables\n\n3. **Template Adjustments:**\n   - Add or rename element IDs to conform exactly to design_spec.md, including dynamic patterns\n   - Confirm templates render expected data and navigation elements properly\n\n4. **Data File I/O:**\n   - Fix any problems reading or writing local text files\n   - Ensure parsing matches field order and format exactly\n\n5. **Final Testing:**\n   - Verify app.py runs without syntax or runtime errors after fixes\n   - Validate all templates are consistent and complete\n\nCRITICAL REQUIREMENTS:\n- ALWAYS use write_text_file tool to save modified app.py and templates\n- Maintain strict adherence to original design_spec.md and validation_report.md\n- Do NOT introduce new features beyond fixes and improvements\n- Produce final corrected artifacts reflecting full validation compliance\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"AppValidator\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppValidator\",\n            \"reviewer_agent\": \"FinalFixer\",\n            \"review_criteria\": \"Ensure validation_report.md identifies all functional gaps, syntax and runtime errors, and verifies exact element IDs and data file operations.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FinalFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html fully resolve validation issues and remain consistent with original requirement coverage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'RealEstate' Web Application

## 1. Objective
Develop a comprehensive web application named 'RealEstate' using Python, with data managed through local text files. The application enables users to browse property listings, search by location and price, view property details, submit inquiries, and manage favorite properties. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'RealEstate' application is Python.

## 3. Page Design

The 'RealEstate' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Real Estate Dashboard
- **Overview**: The main hub displaying featured properties, recent listings, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-properties** - Type: Div - Display of featured property recommendations.
  - **ID: browse-properties-button** - Type: Button - Button to navigate to property search page.
  - **ID: my-inquiries-button** - Type: Button - Button to navigate to inquiries page.
  - **ID: my-favorites-button** - Type: Button - Button to navigate to favorites page.

### 2. Property Search Page
- **Page Title**: Property Search
- **Overview**: A page displaying all available properties with advanced search and filter capabilities.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-input** - Type: Input - Field to search properties by location/city.
  - **ID: price-range-min** - Type: Input (number) - Field to set minimum price filter.
  - **ID: price-range-max** - Type: Input (number) - Field to set maximum price filter.
  - **ID: property-type-filter** - Type: Dropdown - Dropdown to filter by property type (House, Apartment, Condo, Land).
  - **ID: properties-grid** - Type: Div - Grid displaying property cards with image, location, price, and beds/baths.
  - **ID: view-property-button-{property_id}** - Type: Button - Button to view property details (each property card has this).

### 3. Property Details Page
- **Page Title**: Property Details
- **Overview**: A page displaying detailed information about a specific property.
- **Elements**:
  - **ID: property-details-page** - Type: Div - Container for the property details page.
  - **ID: property-address** - Type: H1 - Display property address.
  - **ID: property-price** - Type: Div - Display property price.
  - **ID: property-description** - Type: Div - Display property description.
  - **ID: property-features** - Type: Div - Display property features (beds, baths, square footage).
  - **ID: add-to-favorites-button** - Type: Button - Button to add property to favorites.
  - **ID: submit-inquiry-button** - Type: Button - Button to submit inquiry for property.

### 4. Property Inquiry Page
- **Page Title**: Submit Property Inquiry
- **Overview**: A page for users to submit inquiries for properties they are interested in.
- **Elements**:
  - **ID: inquiry-page** - Type: Div - Container for the inquiry page.
  - **ID: select-property** - Type: Dropdown - Dropdown to select property for inquiry.
  - **ID: inquiry-name** - Type: Input - Field to input customer name.
  - **ID: inquiry-email** - Type: Input (email) - Field to input customer email.
  - **ID: inquiry-phone** - Type: Input (tel) - Field to input customer phone.
  - **ID: inquiry-message** - Type: Textarea - Field to write inquiry message.
  - **ID: submit-inquiry-button** - Type: Button - Button to submit inquiry.

### 5. My Inquiries Page
- **Page Title**: My Inquiries
- **Overview**: A page displaying all submitted inquiries and their status.
- **Elements**:
  - **ID: inquiries-page** - Type: Div - Container for the inquiries page.
  - **ID: inquiries-table** - Type: Table - Table displaying inquiries with property, date, status, and contact info.
  - **ID: inquiry-status-filter** - Type: Dropdown - Dropdown to filter by status (All, Pending, Contacted, Resolved).
  - **ID: delete-inquiry-button-{inquiry_id}** - Type: Button - Button to delete inquiry (each inquiry has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. My Favorites Page
- **Page Title**: My Favorite Properties
- **Overview**: A page displaying all properties added to favorites.
- **Elements**:
  - **ID: favorites-page** - Type: Div - Container for the favorites page.
  - **ID: favorites-list** - Type: Div - List of all favorite properties with address, price, and action buttons.
  - **ID: remove-from-favorites-button-{property_id}** - Type: Button - Button to remove property from favorites (each property has this).
  - **ID: view-property-button-{property_id}** - Type: Button - Button to view property details (each property has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Agent Directory Page
- **Page Title**: Real Estate Agents
- **Overview**: A page displaying all real estate agents and their contact information.
- **Elements**:
  - **ID: agents-page** - Type: Div - Container for the agents page.
  - **ID: agents-list** - Type: Div - List of all agents with photo, name, specialization, and contact info.
  - **ID: agent-search** - Type: Input - Field to search agents by name.
  - **ID: contact-agent-button-{agent_id}** - Type: Button - Button to contact agent (each agent has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Locations Page
- **Page Title**: Featured Locations
- **Overview**: A page displaying popular locations with property count and details.
- **Elements**:
  - **ID: locations-page** - Type: Div - Container for the locations page.
  - **ID: locations-list** - Type: Div - List of all locations with name, property count, and average price.
  - **ID: view-location-button-{location_id}** - Type: Button - Button to view properties in location (each location has this).
  - **ID: location-sort** - Type: Dropdown - Dropdown to sort locations (By Name, By Properties Count, By Average Price).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'RealEstate' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Properties Data
- **File Name**: `properties.txt`
- **Data Format**:
  ```
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
  ```
- **Example Data**:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|location_name|region|average_price|property_count|description
  ```
- **Example Data**:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. Property Inquiries Data
- **File Name**: `inquiries.txt`
- **Data Format**:
  ```
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
  ```
- **Example Data**:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. Favorite Properties Data
- **File Name**: `favorites.txt`
- **Data Format**:
  ```
  favorite_id|property_id|added_date
  ```
- **Example Data**:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. Real Estate Agents Data
- **File Name**: `agents.txt`
- **Data Format**:
  ```
  agent_id|agent_name|specialization|email|phone|properties_sold
  ```
- **Example Data**:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
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
            """You are a Requirements Analyst specializing in detailed web application functional analysis and documentation.

Your goal is to extract and document all functional requirements from user task descriptions into a comprehensive analysis document.

Task Details:
- Read the user_task_description artifact for the RealEstate web application
- Produce requirements_analysis.md detailing all pages with exact element IDs and types
- Document user interactions, navigation flows, and button/input actions
- Specify data storage formats and file layouts exactly as given
- Ensure coverage of every page, element, and data file specified

Documentation Requirements:
1. Pages and Elements:
   - List each page with its exact page title
   - Enumerate all elements with exact IDs, types, and brief descriptions
   - Capture dynamic IDs with naming patterns (e.g., view-property-button-{property_id})

2. User Interaction Flows:
   - Describe button functions and navigation targets
   - Detail input field purposes and expected user input types

3. Data Storage:
   - Describe each data file in 'data/' folder with exact field names and order
   - Include examples rows as provided
   - Specify data file format (pipe-delimited)

4. Format:
   - Use Markdown format for clarity
   - Use sections, tables, and bullet points for ease of reading

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to output requirements_analysis.md
- Preserve all IDs and data format details exactly as per user task
- Do not add or remove features; stay within user task scope
- Document precisely as provided with no assumptions
- Output a human-readable and well-organized markdown file

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design and specification.

Your goal is to convert detailed requirements analysis into a precise design specification document that defines Flask app routes, page templates, element IDs, user interactions, and data file contracts.

Task Details:
- Read requirements_analysis.md artifact produced by RequirementsAnalyst
- Create design_spec.md containing complete Flask route definitions starting from the Dashboard page
- For each page, specify page titles and all element IDs exactly
- Include navigation routes triggered by buttons and links
- Define data file reading and writing contracts matching data formats exactly
- Specify data file paths, field order, delimiter, and example rows

Design Specification Requirements:
1. Flask Routes:
   - List route paths and associated Flask function names (snake_case)
   - Specify HTTP methods (GET, POST) and expected templates rendered
   - Define context variables passed to templates with types

2. Page Templates:
   - Specify exact template filenames corresponding to routes
   - Include page titles and all element IDs per page
   - Define user interaction elements and navigation flows

3. Data Files:
   - Provide data file paths (data/*.txt)
   - Define pipe-delimited field orders matching requirements_analysis.md
   - Include brief field descriptions and example data rows

4. Format:
   - Use markdown format with clear sections and tables
   - Ensure completeness and clarity to support independent backend/frontend development

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Adhere strictly to IDs, field orders, and routes from requirements_analysis.md and user task
- The root route '/' must redirect to the Dashboard page route
- Maintain consistent function naming and capitalization
- Do not invent or omit any specifications beyond the given data
- Output a human-readable, structured markdown file

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftDeveloper": {
        "prompt": (
            """You are a Flask Web Application Developer specializing in building Python Flask apps with Jinja2 templating.

Your goal is to write a complete draft Flask application (app_draft.py) and corresponding HTML template drafts (templates_draft/*.html) that implement all routes, pages, and functionality described in the design_spec.md.

Task Details:
- Read the full design_spec.md to understand all routes, page titles, element IDs, and required user interactions
- Implement all Flask routes and handlers starting from the Dashboard page
- Create templates_draft/*.html implementing exact element IDs and page titles on all pages
- Implement form handling for user inputs and CRUD operations on local text file data as specified
- Generate app_draft.py and all template draft files in templates_draft/

Implementation Guidelines:
1. Flask Application:
   - Set up Flask app with routes matching all pages described in design_spec.md
   - Use render_template to serve templates_draft/*.html
   - Implement CRUD logic to read/update local data text files following the exact schemas
   - Start root route at Dashboard page
2. Template Drafts:
   - Use Jinja2 syntax for dynamic content and looping over data lists
   - Include all specified element IDs exactly as described
   - Page titles must match design_spec.md exactly in <title> and <h1> tags
3. Forms and Buttons:
   - Implement form handlers using Flask request.form and appropriate methods (GET/POST)
   - Use button click handling to navigate routes or submit forms
4. Data Persistence:
   - Handle local text files with exact parsing of pipe-delimited fields per design_spec.md
   - Read and write data files atomically for data consistency

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save 'app_draft.py' and all 'templates_draft/*.html' files
- Ensure all routes start from the Dashboard page exactly as specified
- Maintain exact element IDs and page titles across templates
- Implement full CRUD logic on local text files matching the provided data schemas
- Provide a fully runnable draft Flask app with template drafts

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationDeveloper": {
        "prompt": (
            """You are a Software Integrator specializing in Flask web applications and template integration.

Your goal is to integrate the draft Flask app (app_draft.py) and draft templates (templates_draft/*.html) into a final polished Flask application (app.py) and final templates (templates/*.html), ensuring seamless navigation, exact element IDs, and proper data persistence.

Task Details:
- Read design_spec.md, the draft 'app_draft.py', and all 'templates_draft/*.html'
- Refine and unify app.py with complete route handling starting from Dashboard page
- Integrate templates into templates/*.html with consistent element IDs and exact page titles
- Resolve cross-references between routes and templates to ensure full navigation and data integration
- Ensure the app writes/reads all local text files correctly and persists all CRUD operations
- Clean up draft code for robustness and maintainability

Integration Guidelines:
1. Route Consistency:
   - Confirm all routes originate or link to Dashboard page as entry point
   - Ensure all route handlers align with templates and data operations
2. Template Refinement:
   - Confirm templates have exact element IDs and titles
   - Fix any broken links or missing navigation buttons
   - Ensure templates are organized in templates/ directory
3. Data Management:
   - Verify data files are correctly accessed and updated atomically
   - Confirm consistency with design_spec.md data schemas
4. Final Packaging:
   - Provide a complete runnable app.py and all templates/*.html
   - Ensure no draft artifacts remain (no templates_draft/ usage)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final 'app.py' and 'templates/*.html'
- Maintain exact page titles and element IDs as specified
- Ensure full data persistence with local text files per design spec
- All pages must be reachable starting from Dashboard page
- No usage of draft files or paths in final output

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftDeveloper'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "AppValidator": {
        "prompt": (
            """You are a Software Quality Engineer specializing in Python Flask web application validation.

Your goal is to validate the entire RealEstate web application implementation to ensure full functionality and specification conformity.

Task Details:
- Read design_spec.md for complete specifications including all pages, routes, element IDs, and data schemas
- Analyze app.py and all templates/*.html files for syntax correctness and runtime behavior
- Verify all pages and routes are implemented exactly as specified
- Check that element IDs appear exactly as required in templates
- Confirm app.py correctly reads/writes all required local text data files according to schemas
- Ensure the app launches correctly starting from the Dashboard page

Validation Requirements:
1. **Syntax and Runtime Validation:**
   - Use validate_python_file tool to check syntax and runtime of app.py
   - Execute critical route handlers to confirm runtime stability

2. **Route and Page Coverage:**
   - Verify all specified pages with correct routes exist
   - Confirm HTTP methods are appropriate per specification
   - Routes should return correct template files

3. **Template Element IDs:**
   - Examine templates/*.html for all required element IDs (static and dynamic)
   - Ensure dynamic IDs use correct templating syntax matching design_spec.md patterns

4. **Data File Operations:**
   - Check proper file I/O for data files (properties.txt, inquiries.txt, favorites.txt, agents.txt, locations.txt)
   - Validate correct parsing with exact field order and pipe-delimited format

5. **Startup Behavior:**
   - Ensure root route redirects or renders the Dashboard page correctly

Produce a detailed validation_report.md enumerating:
- Syntax or runtime errors found
- Missing or incorrect routes or pages
- Missing, misspelled, or incorrectly implemented element IDs
- Data file parsing or writing issues
- Any deviations from startup requirements

CRITICAL REQUIREMENTS:
- MUST use validate_python_file for syntax/runtime checks
- MUST use execute_python_code for runtime verification where feasible
- Use write_text_file tool to output complete validation_report.md
- Output report must be clear for guiding correction in next phase
- Focus strictly on files: app.py, templates/*.html, design_spec.md for validation context

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "FinalFixer": {
        "prompt": (
            """You are a Software Developer specializing in code refinement and bug fixes for Flask web applications.

Your goal is to apply corrections and improvements to app.py and templates/*.html based on validation_report.md to ensure full specification compliance and flawless operation.

Task Details:
- Read validation_report.md carefully for all syntax, runtime, and specification issues identified
- Review design_spec.md for original detailed design requirements as needed
- Modify app.py to fix all reported errors and improve robustness in route handling and data file operations
- Update templates/*.html to correct any missing or incorrect element IDs and ensure all pages comply with design_spec.md
- Ensure the application starts correctly at the Dashboard page and all features work as intended

Implementation Guidance:
1. **Fix Syntax and Runtime Errors:**
   - Correct all Python syntax errors reported
   - Adjust code logic to resolve runtime issues or exceptions

2. **Route and Page Corrections:**
   - Add missing routes or update existing ones to match exact specifications
   - Ensure route handlers use correct templates and context variables

3. **Template Adjustments:**
   - Add or rename element IDs to conform exactly to design_spec.md, including dynamic patterns
   - Confirm templates render expected data and navigation elements properly

4. **Data File I/O:**
   - Fix any problems reading or writing local text files
   - Ensure parsing matches field order and format exactly

5. **Final Testing:**
   - Verify app.py runs without syntax or runtime errors after fixes
   - Validate all templates are consistent and complete

CRITICAL REQUIREMENTS:
- ALWAYS use write_text_file tool to save modified app.py and templates
- Maintain strict adherence to original design_spec.md and validation_report.md
- Do NOT introduce new features beyond fixes and improvements
- Produce final corrected artifacts reflecting full validation compliance

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'AppValidator'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Check that requirements_analysis.md thoroughly covers all pages, elements with precise IDs, user navigation flow, and data storage formats as per user task.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftDeveloper': [
        ("IntegrationDeveloper", """Verify app_draft.py and templates_draft/*.html correctly implement all routes, page titles, element IDs, user interactions, and local text file data management as specified in design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'AppValidator': [
        ("FinalFixer", """Ensure validation_report.md identifies all functional gaps, syntax and runtime errors, and verifies exact element IDs and data file operations.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FinalFixer': [
        ("RequirementsAnalyst", """Confirm final app.py and templates/*.html fully resolve validation issues and remain consistent with original requirement coverage.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    # Create agents
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

    # Sequential execution per Sequential Flow
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md detailing all pages, elements, user interactions, navigation flows, and data storage formats exactly as specified.")

    # Step 2: WebArchitect reads requirements_analysis.md and produces design_spec.md
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        requirements_analysis_content = ""
    await execute(WebArchitect,
                  f"Read requirements_analysis.md content and produce design_spec.md with complete Flask routes, page templates, element IDs, navigation routes, and data file contracts matching requirements_analysis.md perfectly.\n\n"
                  f"=== requirements_analysis.md ===\n"
                  f"{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Create agents
    DraftDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DraftDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential Flow: DraftDeveloper first, then IntegrationDeveloper

    # Read draft files content for integration step
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # For templates_draft/*.html, read content of all files and join for injection
        import glob
        all_templates_draft = ""
        for template_file in glob.glob("templates_draft/*.html"):
            try:
                content = open(template_file).read()
                all_templates_draft += f"\n=== {template_file} ===\n{content}\n"
            except:
                continue
        templates_draft_content = all_templates_draft
    except:
        pass

    await execute(DraftDeveloper,
                  "Implement complete app_draft.py with all Flask routes, handlers, and logic based on design_spec.md. "
                  "Implement all templates_draft/*.html with exact element IDs and page titles. "
                  "Use local text files for data persistence and CRUD operations.")

    await execute(IntegrationDeveloper,
                  f"Refine and unify draft app and templates into final app.py and templates/*.html. "
                  f"Ensure full route consistency starting from Dashboard page, "
                  f"exact element IDs, page titles, and robust data persistence. "
                  f"Remove all draft artifacts and produce runnable final app.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"=== Templates Draft ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Create agents
    AppValidator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="AppValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
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

    # Read file artifacts needed for injection
    design_spec_content, app_py_content, templates_content = "", "", ""
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    try:
        app_py_content = open("app.py").read()
    except:
        pass
    # For templates/*.html, we concatenate all template files' content
    import glob
    import os
    templates_files = glob.glob("templates/*.html")
    templates_content_parts = []
    for tpl_file in templates_files:
        try:
            content = open(tpl_file).read()
            templates_content_parts.append(f"=== {os.path.basename(tpl_file)} ===\n{content}")
        except:
            pass
    templates_content = "\n\n".join(templates_content_parts)

    # Execute AppValidator
    await execute(AppValidator,
                  f"Validate app.py and templates/*.html for syntax, runtime, routes, element IDs, data file operations, and startup behavior. "
                  f"Reference design_spec.md for full specifications.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}\n\n"
                  "Output detailed validation_report.md with all findings.")

    # Read validation_report.md to inject into FinalFixer
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    # Execute FinalFixer, injecting the validation report and source files
    await execute(FinalFixer,
                  f"Fix all issues found in validation_report.md and refine app.py and templates/*.html to fully comply with design_spec.md.\n\n"
                  f"=== validation_report.md ===\n{validation_report_content}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}\n\n"
                  "Output final corrected app.py and templates/*.html.")
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
