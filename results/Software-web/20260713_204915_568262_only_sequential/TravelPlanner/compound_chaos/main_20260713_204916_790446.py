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
# 20260713_204916_790446/main_20260713_204916_790446.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the TravelPlanner requirements and produce a complete design_spec.md detailing all pages, elements, interactions, and data storage specifications.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst writes requirements_analysis.md from user task description; \"\n        \"then WebArchitect reads requirements_analysis.md and writes design_spec.md covering Flask routes, page titles, element IDs, \"\n        \"navigation methods, data contracts for local text files, and interactions.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in software requirement extraction for web applications.\n\nYour goal is to extract and document all user-visible pages, UI elements, navigation flows, and data storage specifications precisely as described, enabling downstream design.\n\nTask Details:\n- Read user_task_description thoroughly\n- Extract every page with exact page titles as given\n- Extract all UI element IDs precisely, including dynamic IDs with patterns\n- Capture all navigation buttons and their target pages/actions\n- Document data storage format and example data file specifications exactly as specified\n- Do NOT add authentication or any hidden features beyond the user task\n\nOutput Artifact:\n- Write requirements_analysis.md with detailed pages, elements, navigation flows, and data file descriptions\n\nRequirements:\n- Maintain exact naming and IDs as specified\n- Cover all 10 pages with their detailed elements\n- Include data format lines and realistic example data\n- Produce a clear, structured, human-readable markdown report\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as requirements_analysis.md\n- Do NOT add or omit any user-visible page or element\n- Preserve all exact field orders and file names for data files\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in full-stack web application design for Python Flask frameworks.\n\nYour goal is to create a detailed design_spec.md translating requirements analysis into Flask route specifications, page templates with exact element IDs, navigation mappings, and data storage contracts for local text files.\n\nTask Details:\n- Read requirements_analysis.md and user_task_description carefully\n- Specify Flask routes and HTTP methods for all pages with clear function names\n- Define page titles and exact element IDs for each HTML template\n- Specify template filenames matching page purposes\n- Map navigation buttons to Flask route functions using url_for syntax\n- Detail data file contracts for each local data file in data/*.txt including field orders and formats\n- Include interactions like button functions and page linking\n\nOutput Artifact:\n- Write comprehensive design_spec.md outlining backend routes, frontend elements, navigation, and data specs clearly for implementation\n\nRequirements:\n- Keep all element IDs exact as analyzed with no changes\n- Use standard Flask conventions for route and function naming\n- Maintain explicit data file field order and pipe-delimited format\n- Clarify which templates correspond to which routes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_spec.md\n- Design must enable independent backend and frontend development based on this specification\n- Follow exact data file naming and format as specified\n- All page titles and element IDs must match input exactly\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": \"Ensure requirements_analysis.md covers every user-visible page, exact element IDs, navigation buttons, and data file format as specified.\",\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"WebArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": \"Verify design_spec.md is coherent, complete, and ready for implementation including precise Flask routing and data file usage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the TravelPlanner Flask web application consisting of app_draft.py and templates_draft/*.html from design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper writes app_draft.py using design_spec.md with routes, local file data handling, and button navigation; \"\n        \"FrontendDeveloper writes all templates_draft/*.html files implementing page layout, element IDs, forms, and buttons.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to develop a functional Flask backend implementation that matches design specifications.\n\nTask Details:\n- Read design_spec.md and user_task_description for project context\n- Implement app_draft.py with all Flask routes as specified\n- Use local text files for data storage, reading, and writing exactly as described\n- Implement routing logic and button-triggered navigation per specification\n- Output is app_draft.py fully implementing backend logic and routing\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Routing and Methods**:\n   - Implement ALL routes with correct HTTP methods (GET/POST) from design_spec.md\n   - Routes must render templates or redirect as defined\n   - Pass correct context variables to templates\n\n3. **Data Handling**:\n   - Read and write data to local text files in 'data/' folder\n   - Parse and serialize pipe-delimited data files exactly as specified\n   - Reflect changes in files when relevant (e.g., adding trips, bookings)\n\n4. **Button-triggered Navigation**:\n   - Implement backend handling for button actions navigating between pages\n   - Use url_for and redirect as appropriate\n\n5. **Error Handling**:\n   - Gracefully handle file access errors and invalid inputs\n   - Provide default empty lists or values when data missing\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as app_draft.py\n- Strictly follow design_spec.md for routes, data structure, and navigation\n- Do NOT include frontend code or templates here\n- Do NOT assume data formats beyond those described\n- Ensure function names, route paths, and context variables match specification exactly\n\nOutput: app_draft.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to create complete HTML template files implementing all pages with specified element IDs and UI structure.\n\nTask Details:\n- Read design_spec.md and user_task_description to understand page layouts and UI requirements\n- Implement ALL templates_draft/*.html files with all container divs, buttons, inputs, dropdowns, and other UI elements\n- Use the exact element IDs as specified, including dynamic ID patterns\n- Implement forms and buttons consistent with backend routing for user interactions\n- Output final set of HTML files as templates_draft/*.html\n\nImplementation Requirements:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\" />\n       <title>Page Title</title>\n   </head>\n   <body>\n       <div id=\"container-id\">\n           <!-- Implement specified elements -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs**:\n   - Include all specified IDs exactly as provided (case-sensitive)\n   - For dynamic IDs like view-destination-button-{dest_id}, use Jinja2 syntax:\n     id=\"view-destination-button-{{ dest_id }}\"\n\n3. **Forms and Buttons**:\n   - Forms must send data via POST where applicable\n   - Button IDs must match specification\n   - Navigation buttons link using url_for functions consistent with backend routes\n\n4. **Page Titles and Headers**:\n   - Use exact page titles as specified in design_spec.md in both <title> and <h1>\n\n5. **Data Binding**:\n   - Use Jinja2 variables passed from backend for dynamic data display\n   - Iterate lists and conditionally display content as needed\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save each HTML template in templates_draft/\n- Element IDs and page titles must match design_spec.md exactly\n- Templates must be ready to integrate with Flask backend without modification\n- Do NOT include backend code or data file handling here\n\nOutput: templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": \"Ensure app_draft.py routes correctly map to templates with proper reading/writing of local text data files.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"Tester\",\n            \"review_criteria\": \"Validate templates_draft/*.html files contain all specified page elements, IDs, and navigation buttons consistent with backend routes.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and finalize app.py and templates/*.html to ensure a fully functional TravelPlanner application meeting all specifications.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"Tester validates app_draft.py and templates_draft/*.html and produces validation_report.md; \"\n        \"FinalIntegrator implements fixes from the report producing the final app.py and templates/*.html files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in web application validation with expertise in Python Flask backend and HTML frontend.\n\nYour goal is to perform comprehensive syntax, runtime, and functional validation of the draft backend and frontend artifacts to produce a detailed validation report with actionable findings.\n\nTask Details:\n- Read app_draft.py and all files in templates_draft/*.html along with design_spec.md and user_task_description\n- Validate complete implementation correctness against specifications including routes, navigation, data file interactions, and presence of all UI elements with correct IDs\n- Produce a validation_report.md that documents all syntax/runtime errors, missing or incorrect elements, navigation mismatches, and data handling issues with clear, actionable instructions\n- Focus exclusively on the provided draft code and specification without suggesting new features\n\nValidation Requirements:\n1. **Python Backend Validation**:\n   - Use validate_python_file tool to check syntax and runtime errors on app_draft.py\n   - Execute critical paths where possible to verify dynamic functionality\n   - Confirm all Flask routes match design_spec.md routes exactly, including HTTP methods and context variables\n   - Verify data file reading conforms to specified field orders and handles errors gracefully\n\n2. **Frontend Templates Validation**:\n   - Check all required HTML elements with exact IDs exist in templates_draft/*.html\n   - Confirm page titles and headings match design_spec.md precisely\n   - Ensure navigation mappings (url_for calls) are correctly implemented\n   - Validate dynamic IDs follow templating conventions matching patterns from design_spec.md\n\n3. **Integration Checks**:\n   - Confirm data flows between backend and frontend via context variables are consistent\n   - Identify any mismatch between backend data provision and frontend data usage\n   - Verify forms and buttons use correct methods and actions as per specification\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools to perform thorough backend validation\n- Use write_text_file tool to write validation_report.md with clear sections for syntax errors, runtime errors, UI issues, navigation inconsistencies, and data handling problems\n- Output validation_report.md exactly as specified\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FinalIntegrator\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in backend and frontend integration for Flask web applications.\n\nYour goal is to implement all fixes and improvements identified in validation_report.md to produce final, fully conformant app.py and HTML templates that meet all specification requirements and pass all validation criteria.\n\nTask Details:\n- Read validation_report.md, app_draft.py, and all templates_draft/*.html along with design_spec.md and user_task_description\n- Apply all fixes described in validation_report.md related to syntax, runtime, routing, navigation, UI elements, and data file handling\n- Output final app.py and templates/*.html ensuring full compliance with design_spec.md functionality and UI element specifications\n- Focus strictly on fixing issues detailed in validation_report.md without adding unrequested features or modifications\n\nImplementation Guidelines:\n1. **Backend Fixes**:\n   - Correct all syntax and runtime errors in app_draft.py per report\n   - Adjust Flask routes, data loading, and context variables as required for conformity\n   - Ensure root route and all page routes operate as specified\n\n2. **Frontend Fixes**:\n   - Fix or add missing UI elements with exact IDs per design_spec.md\n   - Correct page titles and headings to match specification\n   - Fix navigation links/buttons using url_for with accurate route names and parameters\n   - Ensure dynamic IDs in templates follow proper Jinja2 syntax and match specification patterns\n\n3. **Testing and Verification**:\n   - Validate fixes do not introduce new errors\n   - Confirm consistency between backend context data and frontend usage\n   - Prepare final deliverables with all fixes incorporated\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and all templates/*.html files\n- All fixes must strictly address issues from validation_report.md\n- Resulting files must fully conform to design_spec.md and user_task_description\n- Deliverables must be ready for final deployment and testing\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"Tester\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"FinalIntegrator\",\n            \"review_criteria\": \"Verify that validation_report.md covers all needed fixes and that all issues are actionable and traceable to design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FinalIntegrator\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html fully implement design_spec.md and pass all key functional and UI requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'TravelPlanner' Web Application

## 1. Objective
Develop a comprehensive web application named 'TravelPlanner' using Python, with data managed through local text files. The application enables users to browse destinations, plan itineraries, search accommodations, book flights, view travel packages, and manage trip details. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'TravelPlanner' application is Python.

## 3. Page Design

The 'TravelPlanner' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Travel Planner Dashboard
- **Overview**: The main hub displaying featured destinations, upcoming trips, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-destinations** - Type: Div - Display of featured travel destinations.
  - **ID: upcoming-trips** - Type: Div - Display of upcoming planned trips.
  - **ID: browse-destinations-button** - Type: Button - Button to navigate to destinations page.
  - **ID: plan-itinerary-button** - Type: Button - Button to navigate to itinerary planning page.

### 2. Destinations Page
- **Page Title**: Travel Destinations
- **Overview**: A page displaying all available travel destinations with search and filter capabilities.
- **Elements**:
  - **ID: destinations-page** - Type: Div - Container for the destinations page.
  - **ID: search-destination** - Type: Input - Field to search destinations by name or country.
  - **ID: region-filter** - Type: Dropdown - Dropdown to filter by region (Asia, Europe, Americas, Africa, Oceania).
  - **ID: destinations-grid** - Type: Div - Grid displaying destination cards with image, name, and country.
  - **ID: view-destination-button-{dest_id}** - Type: Button - Button to view destination details (each destination card has this).

### 3. Destination Details Page
- **Page Title**: Destination Details
- **Overview**: A page displaying detailed information about a specific destination.
- **Elements**:
  - **ID: destination-details-page** - Type: Div - Container for the destination details page.
  - **ID: destination-name** - Type: H1 - Display destination name.
  - **ID: destination-country** - Type: Div - Display destination country.
  - **ID: destination-description** - Type: Div - Display detailed description of the destination.
  - **ID: add-to-trip-button** - Type: Button - Button to add destination to trip.
  - **ID: destination-attractions** - Type: Div - Section displaying main attractions and activities.

### 4. Itinerary Planning Page
- **Page Title**: Plan Your Itinerary
- **Overview**: A page for users to create and manage travel itineraries with activities and schedules.
- **Elements**:
  - **ID: itinerary-page** - Type: Div - Container for the itinerary page.
  - **ID: itinerary-name-input** - Type: Input - Field to enter itinerary name.
  - **ID: start-date-input** - Type: Input (date) - Field to select trip start date.
  - **ID: end-date-input** - Type: Input (date) - Field to select trip end date.
  - **ID: add-activity-button** - Type: Button - Button to add activity to itinerary.
  - **ID: itinerary-list** - Type: Div - Display list of created itineraries with edit/delete options.

### 5. Accommodations Page
- **Page Title**: Search Accommodations
- **Overview**: A page for searching and browsing hotel options with filters and pricing.
- **Elements**:
  - **ID: accommodations-page** - Type: Div - Container for the accommodations page.
  - **ID: destination-input** - Type: Input - Field to enter destination city for hotels.
  - **ID: check-in-date** - Type: Input (date) - Field to select check-in date.
  - **ID: check-out-date** - Type: Input (date) - Field to select check-out date.
  - **ID: price-filter** - Type: Dropdown - Dropdown to filter hotels by price range (Budget, Mid-range, Luxury).
  - **ID: hotels-list** - Type: Div - List of available hotels with name, rating, price, and amenities.

### 6. Transportation Page
- **Page Title**: Book Flights
- **Overview**: A page for searching and booking flights with departure and arrival options.
- **Elements**:
  - **ID: transportation-page** - Type: Div - Container for the transportation page.
  - **ID: departure-city** - Type: Input - Field to enter departure city.
  - **ID: arrival-city** - Type: Input - Field to enter arrival city.
  - **ID: departure-date** - Type: Input (date) - Field to select departure date.
  - **ID: flight-class-filter** - Type: Dropdown - Dropdown to filter by flight class (Economy, Business, First Class).
  - **ID: available-flights** - Type: Div - List of available flights with airlines, times, and prices.

### 7. Travel Packages Page
- **Page Title**: Travel Packages
- **Overview**: A page displaying pre-designed travel packages with complete trip information.
- **Elements**:
  - **ID: packages-page** - Type: Div - Container for the packages page.
  - **ID: packages-grid** - Type: Div - Grid displaying travel package cards with destination, duration, and price.
  - **ID: duration-filter** - Type: Dropdown - Dropdown to filter packages by duration (3-5 days, 7-10 days, 14+ days).
  - **ID: view-package-details-button-{pkg_id}** - Type: Button - Button to view package details (each package has this).
  - **ID: book-package-button-{pkg_id}** - Type: Button - Button to book selected package (each package has this).

### 8. Trip Management Page
- **Page Title**: My Trips
- **Overview**: A page displaying all created trips with options to view, edit, or delete them.
- **Elements**:
  - **ID: trips-page** - Type: Div - Container for the trips page.
  - **ID: trips-table** - Type: Table - Table displaying all trips with destination, dates, and status.
  - **ID: view-trip-details-button-{trip_id}** - Type: Button - Button to view trip details (each trip has this).
  - **ID: edit-trip-button-{trip_id}** - Type: Button - Button to edit trip (each trip has this).
  - **ID: delete-trip-button-{trip_id}** - Type: Button - Button to delete trip (each trip has this).

### 9. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Overview**: A page displaying booking confirmation details with reservation information.
- **Elements**:
  - **ID: confirmation-page** - Type: Div - Container for the confirmation page.
  - **ID: confirmation-number** - Type: Div - Display confirmation/booking number.
  - **ID: booking-details** - Type: Div - Display detailed booking information (dates, amounts, locations).
  - **ID: download-itinerary-button** - Type: Button - Button to download trip itinerary as PDF.
  - **ID: share-trip-button** - Type: Button - Button to share trip details.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Travel Recommendations Page
- **Page Title**: Travel Recommendations
- **Overview**: A page displaying personalized travel recommendations and trending destinations.
- **Elements**:
  - **ID: recommendations-page** - Type: Div - Container for the recommendations page.
  - **ID: trending-destinations** - Type: Div - Display trending destinations ranked by popularity.
  - **ID: recommendation-season-filter** - Type: Dropdown - Dropdown to filter by travel season (Spring, Summer, Fall, Winter).
  - **ID: budget-filter** - Type: Dropdown - Dropdown to filter by budget range (Low, Medium, High).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'TravelPlanner' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Destinations Data
- **File Name**: `destinations.txt`
- **Data Format**:
  ```
  dest_id|name|country|region|description|attractions|climate
  ```
- **Example Data**:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. Itineraries Data
- **File Name**: `itineraries.txt`
- **Data Format**:
  ```
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
  ```
- **Example Data**:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. Hotels Data
- **File Name**: `hotels.txt`
- **Data Format**:
  ```
  hotel_id|name|city|rating|price_per_night|amenities|category
  ```
- **Example Data**:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. Flights Data
- **File Name**: `flights.txt`
- **Data Format**:
  ```
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
  ```
- **Example Data**:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. Travel Packages Data
- **File Name**: `packages.txt`
- **Data Format**:
  ```
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
  ```
- **Example Data**:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. Trips Data
- **File Name**: `trips.txt`
- **Data Format**:
  ```
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
  ```
- **Example Data**:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
  ```
- **Example Data**:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
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
            """You are a Requirements Analyst specializing in software requirement extraction for web applications.

Your goal is to extract and document all user-visible pages, UI elements, navigation flows, and data storage specifications precisely as described, enabling downstream design.

Task Details:
- Read user_task_description thoroughly
- Extract every page with exact page titles as given
- Extract all UI element IDs precisely, including dynamic IDs with patterns
- Capture all navigation buttons and their target pages/actions
- Document data storage format and example data file specifications exactly as specified
- Do NOT add authentication or any hidden features beyond the user task

Output Artifact:
- Write requirements_analysis.md with detailed pages, elements, navigation flows, and data file descriptions

Requirements:
- Maintain exact naming and IDs as specified
- Cover all 10 pages with their detailed elements
- Include data format lines and realistic example data
- Produce a clear, structured, human-readable markdown report

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as requirements_analysis.md
- Do NOT add or omit any user-visible page or element
- Preserve all exact field orders and file names for data files

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in full-stack web application design for Python Flask frameworks.

Your goal is to create a detailed design_spec.md translating requirements analysis into Flask route specifications, page templates with exact element IDs, navigation mappings, and data storage contracts for local text files.

Task Details:
- Read requirements_analysis.md and user_task_description carefully
- Specify Flask routes and HTTP methods for all pages with clear function names
- Define page titles and exact element IDs for each HTML template
- Specify template filenames matching page purposes
- Map navigation buttons to Flask route functions using url_for syntax
- Detail data file contracts for each local data file in data/*.txt including field orders and formats
- Include interactions like button functions and page linking

Output Artifact:
- Write comprehensive design_spec.md outlining backend routes, frontend elements, navigation, and data specs clearly for implementation

Requirements:
- Keep all element IDs exact as analyzed with no changes
- Use standard Flask conventions for route and function naming
- Maintain explicit data file field order and pipe-delimited format
- Clarify which templates correspond to which routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Design must enable independent backend and frontend development based on this specification
- Follow exact data file naming and format as specified
- All page titles and element IDs must match input exactly

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to develop a functional Flask backend implementation that matches design specifications.

Task Details:
- Read design_spec.md and user_task_description for project context
- Implement app_draft.py with all Flask routes as specified
- Use local text files for data storage, reading, and writing exactly as described
- Implement routing logic and button-triggered navigation per specification
- Output is app_draft.py fully implementing backend logic and routing

Implementation Requirements:
1. **Flask Application Setup**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Routing and Methods**:
   - Implement ALL routes with correct HTTP methods (GET/POST) from design_spec.md
   - Routes must render templates or redirect as defined
   - Pass correct context variables to templates

3. **Data Handling**:
   - Read and write data to local text files in 'data/' folder
   - Parse and serialize pipe-delimited data files exactly as specified
   - Reflect changes in files when relevant (e.g., adding trips, bookings)

4. **Button-triggered Navigation**:
   - Implement backend handling for button actions navigating between pages
   - Use url_for and redirect as appropriate

5. **Error Handling**:
   - Gracefully handle file access errors and invalid inputs
   - Provide default empty lists or values when data missing

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as app_draft.py
- Strictly follow design_spec.md for routes, data structure, and navigation
- Do NOT include frontend code or templates here
- Do NOT assume data formats beyond those described
- Ensure function names, route paths, and context variables match specification exactly

Output: app_draft.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to create complete HTML template files implementing all pages with specified element IDs and UI structure.

Task Details:
- Read design_spec.md and user_task_description to understand page layouts and UI requirements
- Implement ALL templates_draft/*.html files with all container divs, buttons, inputs, dropdowns, and other UI elements
- Use the exact element IDs as specified, including dynamic ID patterns
- Implement forms and buttons consistent with backend routing for user interactions
- Output final set of HTML files as templates_draft/*.html

Implementation Requirements:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8" />
       <title>Page Title</title>
   </head>
   <body>
       <div id="container-id">
           <!-- Implement specified elements -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs**:
   - Include all specified IDs exactly as provided (case-sensitive)
   - For dynamic IDs like view-destination-button-{dest_id}, use Jinja2 syntax:
     id="view-destination-button-{{ dest_id }}"

3. **Forms and Buttons**:
   - Forms must send data via POST where applicable
   - Button IDs must match specification
   - Navigation buttons link using url_for functions consistent with backend routes

4. **Page Titles and Headers**:
   - Use exact page titles as specified in design_spec.md in both <title> and <h1>

5. **Data Binding**:
   - Use Jinja2 variables passed from backend for dynamic data display
   - Iterate lists and conditionally display content as needed

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save each HTML template in templates_draft/
- Element IDs and page titles must match design_spec.md exactly
- Templates must be ready to integrate with Flask backend without modification
- Do NOT include backend code or data file handling here

Output: templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in web application validation with expertise in Python Flask backend and HTML frontend.

Your goal is to perform comprehensive syntax, runtime, and functional validation of the draft backend and frontend artifacts to produce a detailed validation report with actionable findings.

Task Details:
- Read app_draft.py and all files in templates_draft/*.html along with design_spec.md and user_task_description
- Validate complete implementation correctness against specifications including routes, navigation, data file interactions, and presence of all UI elements with correct IDs
- Produce a validation_report.md that documents all syntax/runtime errors, missing or incorrect elements, navigation mismatches, and data handling issues with clear, actionable instructions
- Focus exclusively on the provided draft code and specification without suggesting new features

Validation Requirements:
1. **Python Backend Validation**:
   - Use validate_python_file tool to check syntax and runtime errors on app_draft.py
   - Execute critical paths where possible to verify dynamic functionality
   - Confirm all Flask routes match design_spec.md routes exactly, including HTTP methods and context variables
   - Verify data file reading conforms to specified field orders and handles errors gracefully

2. **Frontend Templates Validation**:
   - Check all required HTML elements with exact IDs exist in templates_draft/*.html
   - Confirm page titles and headings match design_spec.md precisely
   - Ensure navigation mappings (url_for calls) are correctly implemented
   - Validate dynamic IDs follow templating conventions matching patterns from design_spec.md

3. **Integration Checks**:
   - Confirm data flows between backend and frontend via context variables are consistent
   - Identify any mismatch between backend data provision and frontend data usage
   - Verify forms and buttons use correct methods and actions as per specification

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools to perform thorough backend validation
- Use write_text_file tool to write validation_report.md with clear sections for syntax errors, runtime errors, UI issues, navigation inconsistencies, and data handling problems
- Output validation_report.md exactly as specified

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app_draft.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "FinalIntegrator": {
        "prompt": (
            """You are a Software Engineer specializing in backend and frontend integration for Flask web applications.

Your goal is to implement all fixes and improvements identified in validation_report.md to produce final, fully conformant app.py and HTML templates that meet all specification requirements and pass all validation criteria.

Task Details:
- Read validation_report.md, app_draft.py, and all templates_draft/*.html along with design_spec.md and user_task_description
- Apply all fixes described in validation_report.md related to syntax, runtime, routing, navigation, UI elements, and data file handling
- Output final app.py and templates/*.html ensuring full compliance with design_spec.md functionality and UI element specifications
- Focus strictly on fixing issues detailed in validation_report.md without adding unrequested features or modifications

Implementation Guidelines:
1. **Backend Fixes**:
   - Correct all syntax and runtime errors in app_draft.py per report
   - Adjust Flask routes, data loading, and context variables as required for conformity
   - Ensure root route and all page routes operate as specified

2. **Frontend Fixes**:
   - Fix or add missing UI elements with exact IDs per design_spec.md
   - Correct page titles and headings to match specification
   - Fix navigation links/buttons using url_for with accurate route names and parameters
   - Ensure dynamic IDs in templates follow proper Jinja2 syntax and match specification patterns

3. **Testing and Verification**:
   - Validate fixes do not introduce new errors
   - Confirm consistency between backend context data and frontend usage
   - Prepare final deliverables with all fixes incorporated

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and all templates/*.html files
- All fixes must strictly address issues from validation_report.md
- Resulting files must fully conform to design_spec.md and user_task_description
- Deliverables must be ready for final deployment and testing

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'Tester'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Ensure requirements_analysis.md covers every user-visible page, exact element IDs, navigation buttons, and data file format as specified.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'WebArchitect': [
        ("BackendDeveloper", """Verify design_spec.md is coherent, complete, and ready for implementation including precise Flask routing and data file usage.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("FrontendDeveloper", """Ensure app_draft.py routes correctly map to templates with proper reading/writing of local text data files.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}])
    ],

    'FrontendDeveloper': [
        ("Tester", """Validate templates_draft/*.html files contain all specified page elements, IDs, and navigation buttons consistent with backend routes.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'Tester': [
        ("FinalIntegrator", """Verify that validation_report.md covers all needed fixes and that all issues are actionable and traceable to design_spec.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'FinalIntegrator': [
        ("RequirementsAnalyst", """Confirm final app.py and templates/*.html fully implement design_spec.md and pass all key functional and UI requirements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'validation_report.md'}])
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
    # Declare agents
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
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution flow:
    # 1. RequirementsAnalyst produces requirements_analysis.md from user_task_description
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce detailed requirements_analysis.md covering all pages, UI elements, navigation flows, and data specifications")

    # 2. WebArchitect reads requirements_analysis.md and user_task_description, then produces design_spec.md
    # Read requirements_analysis.md content to inject
    req_analysis_content = ""
    try:
        with open("requirements_analysis.md", "r") as f:
            req_analysis_content = f.read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read the following requirements_analysis.md content and user_task_description. "
                  f"Produce a comprehensive design_spec.md detailing Flask routes, templates, element IDs, navigation mappings, and data file contracts.\n\n"
                  f"=== requirements_analysis.md ===\n{req_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    await execute(BackendDeveloper,
                  "Implement app_draft.py with all Flask routes, local file data handling, routing, "
                  "button-triggered navigation based on design_spec.md and user_task_description.")

    await execute(FrontendDeveloper,
                  "Implement all HTML templates in templates_draft/ with exact element IDs, page titles, forms, "
                  "buttons, and navigation consistent with backend routes from design_spec.md and user_task_description.")
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Create agents
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FinalIntegrator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FinalIntegrator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=420,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential execution for verification phase
    await execute(Tester,
                  "Validate app_draft.py and templates_draft/*.html using validate_python_file and execute_python_code tools. "
                  "Check conformity to design_spec.md and user_task_description including backend routes, data handling, and UI elements. "
                  "Produce detailed validation_report.md with syntax/runtime errors, UI issues, navigation mismatches, and data handling problems.")

    # Read validation report content for FinalIntegrator
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    # FinalIntegrator applies fixes based on validation report
    app_draft_content, templates_draft_content, design_spec_content, user_task_desc = "", "", "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # Read all templates_draft/*.html files content as one string injection (concatenated)
    import glob
    import os
    templates_draft_files = glob.glob("templates_draft/*.html")
    templates_draft_content = ""
    for filepath in templates_draft_files:
        try:
            templates_draft_content += f"=== {os.path.basename(filepath)} ===\n"
            templates_draft_content += open(filepath).read() + "\n"
        except:
            continue
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    entries = CONTEXT.get("user_task_description", [])
    user_task_desc = entries[-1]["content"] if entries else ""

    await execute(FinalIntegrator,
                  f"Apply all fixes from the following validation_report.md to produce final app.py and templates/*.html. "
                  f"Fixes must address syntax, runtime, routing, navigation, UI elements, and data handling. Do not add unrequested features.\n\n"
                  f"=== Validation Report ===\n{validation_report_content}\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"=== Templates Draft ===\n{templates_draft_content}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== user_task_description ===\n{user_task_desc}")
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
