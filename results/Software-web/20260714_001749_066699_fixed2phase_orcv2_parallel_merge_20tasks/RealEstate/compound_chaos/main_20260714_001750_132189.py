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
# 20260714_001750_132189/main_20260714_001750_132189.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Define backend data structures and API endpoints, frontend HTML templates and UI element IDs for all 8 pages, and merge into a comprehensive design specification document 'design_spec.md'.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect designs Python backend data reading/writing logic and Flask routes based on data files and user features; \"\n        \"FrontendDesignArchitect designs the HTML template structure, element IDs, navigation, and visual layout for all 8 pages; \"\n        \"DesignMerger merges backend_design.md and frontend_design.md with user task constraints into a consistent design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Backend System Architect specializing in Python Flask web application backend development.\n\nYour goal is to specify the backend design including Flask routes, data loading and saving logic, and data schema handling for all functionalities described in the user requirements. Deliver a comprehensive backend_design.md defining how to implement the backend server.\n\nTask Details:\n- Read user_task_description from CONTEXT fully\n- Independently create backend_design.md\n- Define Flask routes mapping URL paths to backend functions\n- Specify data reading/writing logic using local text files in 'data' directory\n- Define detailed schema and format for each data file (properties, inquiries, favorites, agents, locations)\n- Cover all user stories related to property browsing, searching, inquiries, favorites, and agent/location data\n- Do not read or rely on frontend_design.md\n\n**Section 1: Flask Routes Design**\n- List all Flask routes with HTTP methods and route parameters\n- Specify route purpose and request/response behavior including JSON or template render\n- Map routes to user features (Dashboard landing, search filters, detail view, inquiries, favorites, agent directory, locations)\n\n**Section 2: Data File Schema and Access**\n- For each local data file, specify:\n  - Filename and file path\n  - Pipe-delimited column list with field types and descriptions\n  - Example rows consistent with user data format\n- Define backend logic for reading and writing these files safely and efficiently\n- Handle filtering, sorting, and searches in backend logic for relevant routes\n\n**Section 3: Integration and API Design**\n- Define any API endpoints for AJAX or form submissions (inquiry submission, favorites add/remove)\n- Specify expected input parameters and output formats\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can fully implement the Flask app based solely on backend_design.md\n- Data access and route specifications directly address user requirements for all 8 pages\n- Write output using the write_text_file tool to backend_design.md\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Frontend System Architect specializing in HTML5 and Jinja2 template design for Flask web applications.\n\nYour goal is to specify the frontend design including precise HTML templates, element IDs, page structure, navigation flow, and UI element details for all 8 pages. Deliver a frontend_design.md covering all UI components required by the user requirements.\n\nTask Details:\n- Read user_task_description from CONTEXT fully\n- Independently create frontend_design.md\n- Specify template filenames and expected page titles\n- For each page, provide:\n  - Structure and hierarchy of main containers and sections\n  - Exact element IDs with element types and their purpose\n  - Button and input element IDs with description of their behavior and connections\n- Map navigation elements and buttons to page transitions\n- Include notes on layout considerations and UI component grouping\n- Do not read or rely on backend_design.md\n\n**Section 1: Template and Page Structure**\n- List all HTML templates for 8 pages with file paths\n- Specify page titles and main container IDs\n\n**Section 2: UI Element and ID Specifications**\n- Enumerate all critical element IDs on each page with their HTML type\n- Specify dynamic or repeated elements with pattern IDs (e.g., view-property-button-{property_id})\n\n**Section 3: Navigation and User Interactions**\n- Define button IDs and their navigation targets or JS event triggers\n- Describe form elements and submission triggers including inquiry forms\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement templates/*.html solely from frontend_design.md\n- All pages and elements reflect user instructions exactly\n- Write output using the write_text_file tool to frontend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in integration of backend and frontend design specifications for Flask web applications.\n\nYour goal is to integrate backend_design.md and frontend_design.md into a single coherent design_spec.md. Ensure full functional coverage, artifact consistency, and no added requirements beyond user_task_description.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Reconcile backend routes, data access, and API with frontend templates, element IDs, and navigation\n- Resolve any naming conflicts and ensure data passed by routes matches frontend variable usage\n- Ensure all user features from user_task_description appear in design_spec.md with backend and frontend coordinated\n- Produce a comprehensive design_spec.md that developers use as a single source of truth\n\n**Section 1: Backend Routes and Data Schema Integration**\n- Summarize backend routes and ensure alignment with frontend needs\n- Confirm data files schemas are consistent with frontend data consumption\n\n**Section 2: Frontend Template and Navigation Integration**\n- Summarize template structure and element IDs aligned to backend routes\n- Validate navigation flows and UI interaction triggers are coherent with backend API\n\n**Section 3: Cross-Artifact Consistency Checks**\n- Check route parameter names match element ID bindings and API inputs\n- Confirm no missing pages, elements, or backend handlers\n- Ensure no new requirements added beyond user task\n\nCRITICAL SUCCESS CRITERIA:\n- Generated design_spec.md supports pure implementation by both backend and frontend developers\n- All artifacts merged without conflicts and full coverage assured\n- Use write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify that backend_design.md comprehensively specifies all Flask routes, data access, and processing according to requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify that frontend_design.md covers all 8 pages with correct element IDs and navigation per user requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement the Python Flask backend and all HTML frontend templates per design_spec.md, then verify consistency and integration correctness in final app.py and templates/*.html.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper builds app.py implementing all Flask routes, data file access, and logic per design_spec.md; \"\n        \"FrontendDeveloper implements HTML templates with specified IDs and navigation per design_spec.md; \"\n        \"IntegrationMerger integrates and verifies backend and frontend implementations, resolves interface inconsistencies, and produces final deliverables app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask web applications with local text file data management.\n\nYour goal is to implement the complete Flask backend app.py based on the comprehensive design_spec.md, supporting all required routes, business logic, and data file interactions.\n\nTask Details:\n- Read design_spec.md from CONTEXT covering all route specifications, data file schemas, and business logic details.\n- Implement app.py independently without reading frontend templates or other sibling outputs.\n- Output a full Flask application backend including route handlers, file I/O for data files, form processing, and logic per design_spec.md.\n\n**Implementation Requirements:**\n- Support all Flask routes as defined, including parameter handling and HTTP methods.\n- Implement local text file access and parsing according to design_spec.md data schemas.\n- Include error handling for file operations and invalid user inputs.\n- Implement business logic for property browsing, searching, inquiries, favorites management, and agent data.\n- Follow coding best practices with modular functions and clear code structure.\n\n**Output Specifications:**\n- Produce a syntactically correct and runnable app.py.\n- Use the write_text_file tool to save app.py exactly as specified.\n\nCRITICAL SUCCESS CRITERIA:\n- app.py fully implements all features and routes described in design_spec.md.\n- No reading of sibling-output frontend templates or additional refinement markers.\n- Use only the declared output artifact app.py.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask web applications.\n\nYour goal is to implement all required HTML templates with accurate element IDs, UI components, and navigation flows as per the detailed design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT describing all page templates, element IDs, and UI component requirements.\n- Independently implement templates/*.html without reading or depending on backend code or sibling outputs.\n- Output complete and consistent HTML templates supporting all pages, elements, and navigation specified.\n\n**Implementation Requirements:**\n- Create template files for all pages with exact IDs as specified.\n- Use Jinja2 syntax for dynamic content placeholders matching backend context variables.\n- Implement buttons, dropdowns, input fields, tables, and navigation links as required.\n- Ensure accessibility and semantic HTML structure.\n\n**Output Specifications:**\n- Produce valid, well-formatted HTML templates compatible with Flask render_template usage.\n- Use the write_text_file tool to save each template file under templates/ with appropriate names.\n\nCRITICAL SUCCESS CRITERIA:\n- Templates/*.html conform exactly to design_spec.md requirements including IDs, elements, and navigation.\n- No assumptions from sibling backend code beyond design_spec.md.\n- Only produce declared output artifact templates/*.html.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Specialist focusing on Flask backend and frontend UI integration.\n\nYour goal is to integrate the independently developed backend app.py and frontend templates/*.html, verify consistency, resolve interface mismatches, and produce final coherent deliverables.\n\nTask Details:\n- Read design_spec.md, backend app.py, and frontend templates/*.html from CONTEXT.\n- Verify that all Flask routes in app.py match frontend template pages and navigation flows.\n- Ensure backend context variables are correctly referenced in templates and element IDs are consistent.\n- Resolve discrepancies in routing, template naming, and data passing without adding new features or requirements.\n- Output finalized app.py and templates/*.html with full integration correctness.\n\n**Integration Verification:**\n- Confirm route-to-template bindings, URL parameters, and HTTP methods are consistent.\n- Validate that Jinja2 context variables in templates correspond to app.py data provisioning.\n- Check element IDs match design_spec.md and are consistent between backend logic and frontend markup.\n- Ensure all navigation buttons and links correctly connect expected pages and actions.\n\n**Output Specifications:**\n- Produce final app.py and templates/*.html fully consistent and production ready.\n- Use write_text_file to save both app.py and all templates in templates/ directory.\n\nCRITICAL SUCCESS CRITERIA:\n- Final artifacts reflect full alignment of backend and frontend per design_spec.md.\n- No additional features beyond inputs; no refinement markers or sibling artifact reads except allowed inputs.\n- Must only write declared output artifacts app.py and templates/*.html.\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend app.py implementation matches design_spec.md routes, data logic, and structure.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check frontend templates/*.html fully conform to design_spec.md required IDs, markup, and navigation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a Backend System Architect specializing in Python Flask web application backend development.

Your goal is to specify the backend design including Flask routes, data loading and saving logic, and data schema handling for all functionalities described in the user requirements. Deliver a comprehensive backend_design.md defining how to implement the backend server.

Task Details:
- Read user_task_description from CONTEXT fully
- Independently create backend_design.md
- Define Flask routes mapping URL paths to backend functions
- Specify data reading/writing logic using local text files in 'data' directory
- Define detailed schema and format for each data file (properties, inquiries, favorites, agents, locations)
- Cover all user stories related to property browsing, searching, inquiries, favorites, and agent/location data
- Do not read or rely on frontend_design.md

**Section 1: Flask Routes Design**
- List all Flask routes with HTTP methods and route parameters
- Specify route purpose and request/response behavior including JSON or template render
- Map routes to user features (Dashboard landing, search filters, detail view, inquiries, favorites, agent directory, locations)

**Section 2: Data File Schema and Access**
- For each local data file, specify:
  - Filename and file path
  - Pipe-delimited column list with field types and descriptions
  - Example rows consistent with user data format
- Define backend logic for reading and writing these files safely and efficiently
- Handle filtering, sorting, and searches in backend logic for relevant routes

**Section 3: Integration and API Design**
- Define any API endpoints for AJAX or form submissions (inquiry submission, favorites add/remove)
- Specify expected input parameters and output formats

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can fully implement the Flask app based solely on backend_design.md
- Data access and route specifications directly address user requirements for all 8 pages
- Write output using the write_text_file tool to backend_design.md

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a Frontend System Architect specializing in HTML5 and Jinja2 template design for Flask web applications.

Your goal is to specify the frontend design including precise HTML templates, element IDs, page structure, navigation flow, and UI element details for all 8 pages. Deliver a frontend_design.md covering all UI components required by the user requirements.

Task Details:
- Read user_task_description from CONTEXT fully
- Independently create frontend_design.md
- Specify template filenames and expected page titles
- For each page, provide:
  - Structure and hierarchy of main containers and sections
  - Exact element IDs with element types and their purpose
  - Button and input element IDs with description of their behavior and connections
- Map navigation elements and buttons to page transitions
- Include notes on layout considerations and UI component grouping
- Do not read or rely on backend_design.md

**Section 1: Template and Page Structure**
- List all HTML templates for 8 pages with file paths
- Specify page titles and main container IDs

**Section 2: UI Element and ID Specifications**
- Enumerate all critical element IDs on each page with their HTML type
- Specify dynamic or repeated elements with pattern IDs (e.g., view-property-button-{property_id})

**Section 3: Navigation and User Interactions**
- Define button IDs and their navigation targets or JS event triggers
- Describe form elements and submission triggers including inquiry forms

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement templates/*.html solely from frontend_design.md
- All pages and elements reflect user instructions exactly
- Write output using the write_text_file tool to frontend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in integration of backend and frontend design specifications for Flask web applications.

Your goal is to integrate backend_design.md and frontend_design.md into a single coherent design_spec.md. Ensure full functional coverage, artifact consistency, and no added requirements beyond user_task_description.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Reconcile backend routes, data access, and API with frontend templates, element IDs, and navigation
- Resolve any naming conflicts and ensure data passed by routes matches frontend variable usage
- Ensure all user features from user_task_description appear in design_spec.md with backend and frontend coordinated
- Produce a comprehensive design_spec.md that developers use as a single source of truth

**Section 1: Backend Routes and Data Schema Integration**
- Summarize backend routes and ensure alignment with frontend needs
- Confirm data files schemas are consistent with frontend data consumption

**Section 2: Frontend Template and Navigation Integration**
- Summarize template structure and element IDs aligned to backend routes
- Validate navigation flows and UI interaction triggers are coherent with backend API

**Section 3: Cross-Artifact Consistency Checks**
- Check route parameter names match element ID bindings and API inputs
- Confirm no missing pages, elements, or backend handlers
- Ensure no new requirements added beyond user task

CRITICAL SUCCESS CRITERIA:
- Generated design_spec.md supports pure implementation by both backend and frontend developers
- All artifacts merged without conflicts and full coverage assured
- Use write_text_file tool to output design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Python Flask web applications with local text file data management.

Your goal is to implement the complete Flask backend app.py based on the comprehensive design_spec.md, supporting all required routes, business logic, and data file interactions.

Task Details:
- Read design_spec.md from CONTEXT covering all route specifications, data file schemas, and business logic details.
- Implement app.py independently without reading frontend templates or other sibling outputs.
- Output a full Flask application backend including route handlers, file I/O for data files, form processing, and logic per design_spec.md.

**Implementation Requirements:**
- Support all Flask routes as defined, including parameter handling and HTTP methods.
- Implement local text file access and parsing according to design_spec.md data schemas.
- Include error handling for file operations and invalid user inputs.
- Implement business logic for property browsing, searching, inquiries, favorites management, and agent data.
- Follow coding best practices with modular functions and clear code structure.

**Output Specifications:**
- Produce a syntactically correct and runnable app.py.
- Use the write_text_file tool to save app.py exactly as specified.

CRITICAL SUCCESS CRITERIA:
- app.py fully implements all features and routes described in design_spec.md.
- No reading of sibling-output frontend templates or additional refinement markers.
- Use only the declared output artifact app.py.

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask web applications.

Your goal is to implement all required HTML templates with accurate element IDs, UI components, and navigation flows as per the detailed design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT describing all page templates, element IDs, and UI component requirements.
- Independently implement templates/*.html without reading or depending on backend code or sibling outputs.
- Output complete and consistent HTML templates supporting all pages, elements, and navigation specified.

**Implementation Requirements:**
- Create template files for all pages with exact IDs as specified.
- Use Jinja2 syntax for dynamic content placeholders matching backend context variables.
- Implement buttons, dropdowns, input fields, tables, and navigation links as required.
- Ensure accessibility and semantic HTML structure.

**Output Specifications:**
- Produce valid, well-formatted HTML templates compatible with Flask render_template usage.
- Use the write_text_file tool to save each template file under templates/ with appropriate names.

CRITICAL SUCCESS CRITERIA:
- Templates/*.html conform exactly to design_spec.md requirements including IDs, elements, and navigation.
- No assumptions from sibling backend code beyond design_spec.md.
- Only produce declared output artifact templates/*.html.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Specialist focusing on Flask backend and frontend UI integration.

Your goal is to integrate the independently developed backend app.py and frontend templates/*.html, verify consistency, resolve interface mismatches, and produce final coherent deliverables.

Task Details:
- Read design_spec.md, backend app.py, and frontend templates/*.html from CONTEXT.
- Verify that all Flask routes in app.py match frontend template pages and navigation flows.
- Ensure backend context variables are correctly referenced in templates and element IDs are consistent.
- Resolve discrepancies in routing, template naming, and data passing without adding new features or requirements.
- Output finalized app.py and templates/*.html with full integration correctness.

**Integration Verification:**
- Confirm route-to-template bindings, URL parameters, and HTTP methods are consistent.
- Validate that Jinja2 context variables in templates correspond to app.py data provisioning.
- Check element IDs match design_spec.md and are consistent between backend logic and frontend markup.
- Ensure all navigation buttons and links correctly connect expected pages and actions.

**Output Specifications:**
- Produce final app.py and templates/*.html fully consistent and production ready.
- Use write_text_file to save both app.py and all templates in templates/ directory.

CRITICAL SUCCESS CRITERIA:
- Final artifacts reflect full alignment of backend and frontend per design_spec.md.
- No additional features beyond inputs; no refinement markers or sibling artifact reads except allowed inputs.
- Must only write declared output artifacts app.py and templates/*.html.

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'BackendDesignArchitect': [
        ("DesignMerger", """Verify that backend_design.md comprehensively specifies all Flask routes, data access, and processing according to requirements.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify that frontend_design.md covers all 8 pages with correct element IDs and navigation per user requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend app.py implementation matches design_spec.md routes, data logic, and structure.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Check frontend templates/*.html fully conform to design_spec.md required IDs, markup, and navigation.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
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

    # Parallel execution of backend and frontend design architecture
    await asyncio.gather(
        execute(BackendDesignArchitect, "Independently create backend_design.md specifying Flask routes, data schemas, and backend logic based on user_task_description."),
        execute(FrontendDesignArchitect, "Independently create frontend_design.md specifying all 8 HTML templates, element IDs, navigation, and UI components based on user_task_description.")
    )

    # Read the outputs from backend and frontend design architects for merger
    backend_design, frontend_design = "", ""
    try:
        backend_design = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend design into a unified design_spec.md
    await execute(DesignMerger,
                  f"User task description:\n{CONTEXT.get('user_task_description', '')}\n\n"
                  f"=== Backend Design Specification ===\n{backend_design}\n\n"
                  f"=== Frontend Design Specification ===\n{frontend_design}")
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import asyncio

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
        timeout_threshold=500,
        failure_threshold=2,
        recovery_time=60
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement full Flask backend app.py per design_spec.md including all routes, file I/O, and business logic."
        ),
        execute(
            FrontendDeveloper,
            "Implement all HTML templates under templates/ with exact IDs, Jinja2 syntax, and navigation per design_spec.md."
        )
    )

    # Read outputs after backend and frontend completion
    app_py_content = ""
    templates_content = ""
    import glob

    try:
        with open("app.py", "r", encoding="utf-8") as f:
            app_py_content = f.read()
    except Exception:
        pass

    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            with open(tpl_path, "r", encoding="utf-8") as f:
                templates_content += f"\n=== {tpl_path} ===\n" + f.read()
        except Exception:
            pass

    # Execute IntegrationMerger to finalize integrated app.py and templates/*.html
    await execute(
        IntegrationMerger,
        f"Integrate and verify backend and frontend implementations.\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}\n\n"
        f"Confirm full consistency between routes and templates, context variables, element IDs, navigation, and produce final app.py and templates/*.html."
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
