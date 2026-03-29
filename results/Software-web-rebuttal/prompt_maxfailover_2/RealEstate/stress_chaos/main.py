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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development for RealEstate app\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect writes design_spec.md with 3 sections: \"\n        \"Section 1 for Flask routes and HTTP methods, \"\n        \"Section 2 for HTML templates with element IDs and navigation, \"\n        \"Section 3 for data schemas for each data file in pipe-delimited format.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create a comprehensive design specification document that enables Backend and Frontend developers to work independently and efficiently on the RealEstate web application.\n\nTask Details:\n- Read the entire user_task_description from CONTEXT\n- Create design_spec.md with three comprehensive sections:\n  - Section 1: Flask routes and HTTP methods, with precise function names and context variables\n  - Section 2: HTML templates detailing exact element IDs, page titles, navigation mappings, and data context variables\n  - Section 3: Data file schemas for each data file, specifying exact pipe-delimited field order and example data\n- Preserve the integrity of all input artifacts (user_task_description) without adding unauthorized assumptions\n- Output must support parallel independent development for backend and frontend teams\n\nSection 1: Flask Routes Specification (Backend)\n- Specify all routes required for the 8 pages with paths, HTTP methods (GET/POST), function names (lowercase_with_underscores)\n- Include route parameters where applicable (e.g., property_id)\n- Define the HTML template rendered for each route\n- Enumerate all context variables passed to templates with types (str, int, float, list, dict)\n- Define expected form data for POST routes (e.g., inquiry submissions, adding/removing favorites)\n- Root route '/' must redirect to dashboard page\n\nSection 2: HTML Templates (Frontend)\n- List all required templates corresponding to each route\n- For each template specify:\n  - Page title (used in <title> and <h1>)\n  - All element IDs exactly as specified in the requirements, including static and dynamic IDs (with variable placeholders)\n  - Context variables accessible in template with descriptions and types\n  - Navigation mappings using Flask url_for() with function names consistent with Section 1\n  - Forms with input fields and submit buttons specifying IDs and action routes\n\nSection 3: Data File Schemas (Backend)\n- For each data file (properties.txt, locations.txt, inquiries.txt, favorites.txt, agents.txt):\n  - Define file path as data/{filename}\n  - Specify exact pipe-delimited field names in order\n  - Provide a brief description of the data stored\n  - Include 2-3 realistic example rows matching the user task data\n  - All parsing is pipe-delimited without header lines\n\nCRITICAL SUCCESS CRITERIA:\n- Backend development can implement complete Flask app.py with no cross-team dependencies except design_spec.md Sections 1 and 3\n- Frontend development can implement complete HTML templates with no knowledge of backend code, relying solely on Section 2\n- All element IDs and function names must match exactly across sections\n- No assumptions about additional routes, data, or features beyond user requirements\n- Use write_text_file tool to output design_spec.md\n- Do NOT include partial or incomplete specifications; ensure full coverage of UI pages, routes, data files, and navigation\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md for backend completeness: Section 1 contains all Flask routes with correct function names, context variables, HTTP methods; \"\n                \"Section 3 contains all data schemas mapping to files with exact field names, order, and pipe delimiter. \"\n                \"Verify root route redirects to dashboard and all backend routes needed are specified.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md for frontend completeness: Section 2 contains all HTML templates with exact element IDs, data context variables, and navigation mappings using Flask url_for. \"\n                \"Verify all page titles, buttons, inputs, and containers are specified and consistent with requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend in parallel based on the design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py including all Flask routes and data handling as specified by Section 1 and Section 3 of design_spec.md. \"\n        \"FrontendDeveloper implements all HTML templates with correct element IDs and navigation based on Section 2 of design_spec.md. \"\n        \"Both agents work independently, producing app.py and templates/*.html respectively.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend with all required routes, data loading, and business logic as specified in the design specification documents.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) exclusively from CONTEXT.\n- Implement app.py with all Flask routes and HTTP methods exactly as defined in Section 1.\n- Load and process data from the data/*.txt files according to schemas defined in Section 3.\n- Do NOT read or depend on Section 2 (Frontend templates) or any frontend source code.\n- Do NOT add functionality beyond what Section 1 and Section 3 specify.\n\nImplementation Requirements:\n\n1. **Flask App Initialization**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root and Routing**:\n   - Implement the root route '/' to redirect to the dashboard page using:\n     ```python\n     return redirect(url_for('dashboard'))\n     ```\n   - Implement all routes exactly as listed in Section 1, matching route paths, function names (snake_case), HTTP methods, templates to render, and passed context variables.\n\n3. **Data File Parsing**:\n   - Read from data text files (properties.txt, locations.txt, inquiries.txt, favorites.txt, agents.txt) with pipe-delimited fields.\n   - Parse each line with:\n     ```python\n     parts = line.strip().split('|')\n     ```\n   - Map fields strictly according to the order specified in Section 3 schemas.\n   - Handle file not found or I/O errors gracefully.\n   - No header lines; parse from the first line.\n\n4. **Form Handling and POST Requests**:\n   - For any POST routes (e.g., inquiry submission), handle form data securely using `request.form`.\n   - Validate input and update data files accordingly.\n\n5. **Business Logic**:\n   - Maintain status and integrity of inquiries, favorites, and property availability per specification.\n   - Ensure all backend logic aligns strictly with Section 1 and Section 3 rules.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the output as app.py.\n- All function names, route paths, HTTP methods, and context variable names/types must exactly match design_spec.md Section 1.\n- Data loading and saving must strictly adhere to schemas defined in Section 3.\n- Root route MUST redirect to dashboard.\n- Do NOT add any endpoints, features, or logic beyond specification.\n- Do NOT output code snippets only; always use write_text_file.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask applications.\n\nYour goal is to implement complete HTML templates implementing all user interface pages with correct element IDs, navigation, and front-end structure as per design specifications.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) exclusively from CONTEXT.\n- Implement all HTML templates (*.html) exactly as specified including page titles, element IDs, buttons, and navigation links.\n- Do NOT read nor rely on backend code, Section 1, or Section 3.\n- Do NOT add UI elements, pages, or navigation routes not specified in Section 2.\n\nImplementation Requirements:\n\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>Page Title as specified</title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1>Page Title as specified</h1>\n           <!-- page content here -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs and Naming**:\n   - Implement all specified element IDs with exact names and casing (e.g., dashboard-page, browse-properties-button).\n   - For dynamic IDs like view-property-button-{property_id}, use Jinja2 templating with {{ }} syntax:\n     ```html\n     id=\"view-property-button-{{ property.property_id }}\"\n     ```\n\n3. **Navigation Links**:\n   - Use Flask's `url_for()` for all navigation links and form actions as specified.\n   - For static navigation buttons, implement as:\n     ```html\n     <a href=\"{{ url_for('function_name') }}\">\n       <button id=\"element-id\">Button Text</button>\n     </a>\n     ```\n   - For dynamic navigation buttons (with IDs including variables), implement as:\n     ```html\n     <a href=\"{{ url_for('function_name', id=property.property_id) }}\">\n       <button id=\"view-property-button-{{ property.property_id }}\">View</button>\n     </a>\n     ```\n\n4. **Forms and Inputs**:\n   - Create forms with appropriate method=\"POST\" attributes if specified.\n   - Include all input fields and buttons with specified IDs.\n\n5. **Jinja2 Template Variables and Logic**:\n   - Use variables and structures as described in Section 2.\n   - Loops, conditionals, and variable usage must match context variables.\n   - No assumptions beyond the provided specification.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files in templates/ directory.\n- All element IDs, page titles, and navigation URLs must exactly match design_spec.md Section 2.\n- Do NOT add or remove templates beyond specification.\n- Do NOT provide partial code or samples only; always save complete files.\n- Ensure navigation links correspond exactly to backend route function names.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all Flask routes and HTTP methods exactly as specified in design_spec.md Section 1; \"\n                \"confirm data loading uses correct schemas from Section 3; \"\n                \"check root route redirects to dashboard and all backend logic aligns with spec.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all HTML templates contain the correct element IDs and navigation using url_for as specified in design_spec.md Section 2; \"\n                \"check page titles and buttons are accurately implemented.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create a comprehensive design specification document that enables Backend and Frontend developers to work independently and efficiently on the RealEstate web application.

Task Details:
- Read the entire user_task_description from CONTEXT
- Create design_spec.md with three comprehensive sections:
  - Section 1: Flask routes and HTTP methods, with precise function names and context variables
  - Section 2: HTML templates detailing exact element IDs, page titles, navigation mappings, and data context variables
  - Section 3: Data file schemas for each data file, specifying exact pipe-delimited field order and example data
- Preserve the integrity of all input artifacts (user_task_description) without adding unauthorized assumptions
- Output must support parallel independent development for backend and frontend teams

Section 1: Flask Routes Specification (Backend)
- Specify all routes required for the 8 pages with paths, HTTP methods (GET/POST), function names (lowercase_with_underscores)
- Include route parameters where applicable (e.g., property_id)
- Define the HTML template rendered for each route
- Enumerate all context variables passed to templates with types (str, int, float, list, dict)
- Define expected form data for POST routes (e.g., inquiry submissions, adding/removing favorites)
- Root route '/' must redirect to dashboard page

Section 2: HTML Templates (Frontend)
- List all required templates corresponding to each route
- For each template specify:
  - Page title (used in <title> and <h1>)
  - All element IDs exactly as specified in the requirements, including static and dynamic IDs (with variable placeholders)
  - Context variables accessible in template with descriptions and types
  - Navigation mappings using Flask url_for() with function names consistent with Section 1
  - Forms with input fields and submit buttons specifying IDs and action routes

Section 3: Data File Schemas (Backend)
- For each data file (properties.txt, locations.txt, inquiries.txt, favorites.txt, agents.txt):
  - Define file path as data/{filename}
  - Specify exact pipe-delimited field names in order
  - Provide a brief description of the data stored
  - Include 2-3 realistic example rows matching the user task data
  - All parsing is pipe-delimited without header lines

CRITICAL SUCCESS CRITERIA:
- Backend development can implement complete Flask app.py with no cross-team dependencies except design_spec.md Sections 1 and 3
- Frontend development can implement complete HTML templates with no knowledge of backend code, relying solely on Section 2
- All element IDs and function names must match exactly across sections
- No assumptions about additional routes, data, or features beyond user requirements
- Use write_text_file tool to output design_spec.md
- Do NOT include partial or incomplete specifications; ensure full coverage of UI pages, routes, data files, and navigation

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

Your goal is to implement a complete Flask backend with all required routes, data loading, and business logic as specified in the design specification documents.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) exclusively from CONTEXT.
- Implement app.py with all Flask routes and HTTP methods exactly as defined in Section 1.
- Load and process data from the data/*.txt files according to schemas defined in Section 3.
- Do NOT read or depend on Section 2 (Frontend templates) or any frontend source code.
- Do NOT add functionality beyond what Section 1 and Section 3 specify.

Implementation Requirements:

1. **Flask App Initialization**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root and Routing**:
   - Implement the root route '/' to redirect to the dashboard page using:
     ```python
     return redirect(url_for('dashboard'))
     ```
   - Implement all routes exactly as listed in Section 1, matching route paths, function names (snake_case), HTTP methods, templates to render, and passed context variables.

3. **Data File Parsing**:
   - Read from data text files (properties.txt, locations.txt, inquiries.txt, favorites.txt, agents.txt) with pipe-delimited fields.
   - Parse each line with:
     ```python
     parts = line.strip().split('|')
     ```
   - Map fields strictly according to the order specified in Section 3 schemas.
   - Handle file not found or I/O errors gracefully.
   - No header lines; parse from the first line.

4. **Form Handling and POST Requests**:
   - For any POST routes (e.g., inquiry submission), handle form data securely using `request.form`.
   - Validate input and update data files accordingly.

5. **Business Logic**:
   - Maintain status and integrity of inquiries, favorites, and property availability per specification.
   - Ensure all backend logic aligns strictly with Section 1 and Section 3 rules.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the output as app.py.
- All function names, route paths, HTTP methods, and context variable names/types must exactly match design_spec.md Section 1.
- Data loading and saving must strictly adhere to schemas defined in Section 3.
- Root route MUST redirect to dashboard.
- Do NOT add any endpoints, features, or logic beyond specification.
- Do NOT output code snippets only; always use write_text_file.

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask applications.

Your goal is to implement complete HTML templates implementing all user interface pages with correct element IDs, navigation, and front-end structure as per design specifications.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) exclusively from CONTEXT.
- Implement all HTML templates (*.html) exactly as specified including page titles, element IDs, buttons, and navigation links.
- Do NOT read nor rely on backend code, Section 1, or Section 3.
- Do NOT add UI elements, pages, or navigation routes not specified in Section 2.

Implementation Requirements:

1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Page Title as specified</title>
   </head>
   <body>
       <div id="main-container-id">
           <h1>Page Title as specified</h1>
           <!-- page content here -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs and Naming**:
   - Implement all specified element IDs with exact names and casing (e.g., dashboard-page, browse-properties-button).
   - For dynamic IDs like view-property-button-{property_id}, use Jinja2 templating with {{ }} syntax:
     ```html
     id="view-property-button-{{ property.property_id }}"
     ```

3. **Navigation Links**:
   - Use Flask's `url_for()` for all navigation links and form actions as specified.
   - For static navigation buttons, implement as:
     ```html
     <a href="{{ url_for('function_name') }}">
       <button id="element-id">Button Text</button>
     </a>
     ```
   - For dynamic navigation buttons (with IDs including variables), implement as:
     ```html
     <a href="{{ url_for('function_name', id=property.property_id) }}">
       <button id="view-property-button-{{ property.property_id }}">View</button>
     </a>
     ```

4. **Forms and Inputs**:
   - Create forms with appropriate method="POST" attributes if specified.
   - Include all input fields and buttons with specified IDs.

5. **Jinja2 Template Variables and Logic**:
   - Use variables and structures as described in Section 2.
   - Loops, conditionals, and variable usage must match context variables.
   - No assumptions beyond the provided specification.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files in templates/ directory.
- All element IDs, page titles, and navigation URLs must exactly match design_spec.md Section 2.
- Do NOT add or remove templates beyond specification.
- Do NOT provide partial code or samples only; always save complete files.
- Ensure navigation links correspond exactly to backend route function names.

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
        ("BackendDeveloper", """Check design_spec.md for backend completeness: Section 1 contains all Flask routes with correct function names, context variables, HTTP methods; "
                "Section 3 contains all data schemas mapping to files with exact field names, order, and pipe delimiter. "
                "Verify root route redirects to dashboard and all backend routes needed are specified.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md for frontend completeness: Section 2 contains all HTML templates with exact element IDs, data context variables, and navigation mappings using Flask url_for. "
                "Verify all page titles, buttons, inputs, and containers are specified and consistent with requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all Flask routes and HTTP methods exactly as specified in design_spec.md Section 1; "
                "confirm data loading uses correct schemas from Section 3; "
                "check root route redirects to dashboard and all backend logic aligns with spec.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all HTML templates contain the correct element IDs and navigation using url_for as specified in design_spec.md Section 2; "
                "check page titles and buttons are accurately implemented.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Chaos Controller Setup ====================
chaos_controller = ChaosController(
    agent_chaos_enabled=False,
    stress_chaos_enabled=True,
    io_chaos_enabled=False,
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Start chaos experiment with 20% probability
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=0.2
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "stress_chaos",
    "probability": 0.2,
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

print(f"Chaos scenario 'stress_chaos' activated with 20% probability")
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
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect agent with task to create design_spec.md
    await execute(
        SystemArchitect,
        "Create comprehensive design_spec.md covering Flask routes, HTML templates with exact element IDs and navigation, and data file schemas as specified."
    )
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
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py including all Flask routes and data handling per design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all HTML templates with correct element IDs, navigation, and page structure per design_spec.md Section 2")
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
