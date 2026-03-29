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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development for CarRental with page routes, templates, and data schemas\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect creates design_spec.md with 3 sections: Flask Routes for all pages, \"\n        \"HTML Templates defining element IDs and layout, and Data Schemas describing text file formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create comprehensive design specifications that enable Backend and Frontend developers to work completely independently without requiring knowledge of each other's code.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Create design_spec.md with three main sections covering complete Flask routes for all CarRental pages, HTML template layouts with element IDs, and data schemas defining all text file formats exactly\n- Ensure all data formats are pipe-delimited and field orders match user requirements\n- Do NOT assume any authentication or add features beyond specified requirements\n\n**Section 1: Flask Routes Specification (Backend)**\n\nProvide a detailed route table that includes:\n- Route Path: URL pattern (e.g., /dashboard, /vehicle/<int:vehicle_id>)\n- Function Name: Flask function names, lowercase with underscores\n- HTTP Method(s): GET or POST as applicable\n- Template File: Exact HTML template filename\n- Context Variables: All variables passed to template with precise type annotations (str, int, list, dict, etc.)\n\nRequirements:\n- Root route '/' MUST redirect to the dashboard page\n- All function names must be consistent and descriptive of page functionality\n- Context variables must exactly match fields in data schemas or form inputs\n- Include navigation endpoints aligning with page buttons and links\n\n**Section 2: HTML Template Specifications (Frontend)**\n\nFor each page template:\n- Specify filename under templates/ directory (e.g., templates/dashboard.html)\n- Provide exact Page Title (used in <title> and <h1>)\n- Enumerate all required element IDs with element types and purpose\n  - Include static and dynamic IDs, specifying dynamic patterns (e.g., view-details-button-{vehicle_id})\n- Define navigation mappings using Flask url_for function names matching Section 1 routes\n- Outline context variables accessible in template with expected structures and types\n\nRequirements:\n- Include all element IDs from user requirements to guarantee UI completeness\n- Use Jinja2 templating syntax for dynamic content and loops\n- Ensure consistency in naming conventions with Section 1 context variables\n- Do NOT introduce elements or navigation items not described in requirements\n\n**Section 3: Data File Schemas**\n\nFor each data file in data/ directory:\n- Specify filename and precise pipe-delimited format with exact field order\n- Define field names and expected data types (e.g., int, float, str, date)\n- Provide 2-3 example data lines demonstrating realistic content\n- Document what the file stores and its relation to the application domain\n\nFiles to cover:\n- vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, reservations.txt\n\nRequirements:\n- Strict pipe-delimited formatting with NO headers\n- Field order MUST be exactly as specified in user requirements\n- Examples should reflect typical values and formats shown\n\nCRITICAL SUCCESS CRITERIA:\n- The backend can be implemented with Section 1 and Section 3 ONLY, fully supporting all page functionalities and data interactions\n- The frontend can implement all HTML templates with Section 2 ONLY, ensuring correct UI elements, navigation, and dynamic content rendering\n- No cross-dependency between backend and frontend code implementations\n- All naming conventions, IDs, routing paths, and context variables must be consistent and error-free\n- Use write_text_file tool exclusively for saving design_spec.md\n- Do NOT add any authentication or features beyond those specified\n- Maintain clarity, completeness, and precision in all specifications\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md for backend completeness: \"\n                \"Verify Flask routes for all pages exist with correct function names, context variables, and HTTP methods, \"\n                \"Verify data schemas match required text file formats with exact field order and delimiter consistency.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md for frontend completeness: \"\n                \"Verify HTML templates define all pages with correct element IDs, navigation mappings using url_for, and required UI components.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend of CarRental web app in parallel based on architecture design_spec.md\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using design_spec.md's Flask routes and data schemas. \"\n        \"FrontendDeveloper implements all HTML templates using design_spec.md's frontend specifications. \"\n        \"Both work independently.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications for car rental systems.\n\nYour goal is to implement the complete Flask backend app.py based on design_spec.md specifying all Flask routes and data schemas.\n\nTask Details:\n- Read design_spec.md Sections describing Flask routes and data file schemas ONLY\n- Implement all routes exactly as specified with correct HTTP methods\n- Load and save data from/to data/*.txt files according to schemas\n- Do NOT read or implement any frontend templates or UI code\n- Do NOT assume details not provided in design_spec.md\n\nImplementation Requirements:\n1. **Flask Application Setup:**\n   ```python\n   from flask import Flask, render_template, request, redirect, url_for\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root and Navigation Routes:**\n   - Implement '/' route redirecting to dashboard page\n   - Implement routes to handle all pages as per design_spec.md with exact function names and URL routes\n   - Use render_template() with correct template file names from design_spec.md\n\n3. **Data Handling:**\n   - Read data from data files using pipe-delimited format as specified\n   - Parse each line with line.strip().split('|')\n   - Match field order and types exactly according to design_spec.md\n   - Write data back in same pipe-delimited format if needed\n   - Handle possible data read/write errors gracefully\n\n4. **Forms and POST Handling:**\n   - Implement route handlers for POST requests to handle booking, modifications, cancellations, and special requests\n   - Use request.form to process input fields\n   - Validate inputs according to specified fields; handle errors appropriately\n\n5. **Business Logic:**\n   - Enforce workflow rules such as navigation sequence (e.g., booking to insurance)\n   - Maintain consistent naming for context variables and functions as per design_spec.md\n   - Do NOT implement authentication or features not specified\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app.py\n- Strictly follow Flask route and data schema specifications from design_spec.md\n- Function and variable names MUST exactly match design_spec.md\n- Do NOT include any frontend template code or styling\n- Do NOT invent features or routes not described in design_spec.md\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications focused on car rental services.\n\nYour goal is to implement all HTML templates (*.html) for the CarRental web app strictly following the frontend specifications and element IDs described in design_spec.md.\n\nTask Details:\n- Read design_spec.md Sections describing HTML templates, element IDs, navigation, and page layout ONLY\n- Implement all HTML template files corresponding to each UI page specified\n- Include ALL required element IDs with exact naming and casing\n- Use Jinja2 templating syntax for dynamic data and loops\n- Implement navigation and links using url_for() functions with correct routing names\n- Do NOT read or implement any backend Python code or data handling logic\n- Do NOT add or modify element IDs beyond what is specified\n\nImplementation Requirements:\n1. **Template Structure:**\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ page_title }}</title>\n   </head>\n   <body>\n       <div id=\"main-container\">\n           <h1>{{ page_title }}</h1>\n           <!-- Page-specific content -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs and Layout:**\n   - Include all static and dynamic IDs exactly (e.g., view-details-button-{{ vehicle_id }})\n   - Use proper Jinja2 syntax for dynamic IDs and data rendering\n   - Preserve HTML semantics and accessibility best practices\n\n3. **Forms and Inputs:**\n   - Implement forms for booking, insurance selection, requests submission as specified\n   - Use method=\"POST\" for forms interacting with backend routes that handle POST\n\n4. **Navigation:**\n   - Map buttons and links using url_for() with route names exactly as specified\n   - Include navigation buttons to enable smooth page flow as designed\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save each template file individually inside templates/ folder\n- Ensure all element IDs conform exactly to design_spec.md (case-sensitive)\n- Page titles in <title> and <h1> must match design_spec.md exactly\n- Do NOT add features or pages not specified\n- Do NOT include any backend Python code in templates\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all Flask routes exactly as specified in design_spec.md with correct context variables, HTTP methods, \"\n                \"and data loading/saving functions conforming to defined data schemas.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all HTML templates match design_spec.md in element IDs, layout, and navigation routing using url_for functions, \"\n                \"ensuring full compliance with frontend design specifications.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
 }

user_task = """
# Requirements Document for 'CarRental' Web Application

## 1. Objective
Develop a comprehensive web application named 'CarRental' using Python, with data managed through local text files. The application enables users to search vehicles, book rentals, manage reservations, view rental history, and select insurance options. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'CarRental' application is Python.

## 3. Page Design

The 'CarRental' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Car Rental Dashboard
- **Overview**: The main hub displaying featured vehicles, current promotions, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-vehicles** - Type: Div - Display of featured vehicle recommendations.
  - **ID: search-vehicles-button** - Type: Button - Button to navigate to vehicle search page.
  - **ID: my-reservations-button** - Type: Button - Button to navigate to reservations page.
  - **ID: promotions-section** - Type: Div - Display of current promotions and offers.

### 2. Vehicle Search Page
- **Page Title**: Search Vehicles
- **Overview**: A page displaying all available vehicles with search and filter capabilities.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-filter** - Type: Dropdown - Dropdown to filter by pickup location.
  - **ID: vehicle-type-filter** - Type: Dropdown - Dropdown to filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - **ID: date-range-input** - Type: Input - Field to select rental date range.
  - **ID: vehicles-grid** - Type: Div - Grid displaying vehicle cards with image, model, price per day.
  - **ID: view-details-button-{vehicle_id}** - Type: Button - Button to view vehicle details (each vehicle card has this).

### 3. Vehicle Details Page
- **Page Title**: Vehicle Details
- **Overview**: A page displaying detailed information about a specific vehicle.
- **Elements**:
  - **ID: vehicle-details-page** - Type: Div - Container for the vehicle details page.
  - **ID: vehicle-name** - Type: H1 - Display vehicle name and model.
  - **ID: vehicle-specs** - Type: Div - Display vehicle specifications (engine, seats, transmission).
  - **ID: daily-rate** - Type: Div - Display daily rental rate.
  - **ID: book-now-button** - Type: Button - Button to book this vehicle.
  - **ID: vehicle-reviews** - Type: Div - Section displaying customer reviews.

### 4. Booking Page
- **Page Title**: Book Your Rental
- **Overview**: A page for users to complete rental booking with dates and location selection.
- **Elements**:
  - **ID: booking-page** - Type: Div - Container for the booking page.
  - **ID: pickup-location** - Type: Dropdown - Dropdown to select pickup location.
  - **ID: dropoff-location** - Type: Dropdown - Dropdown to select dropoff location.
  - **ID: pickup-date** - Type: Input - Field to select pickup date.
  - **ID: dropoff-date** - Type: Input - Field to select dropoff date.
  - **ID: calculate-price-button** - Type: Button - Button to calculate total rental price.
  - **ID: total-price** - Type: Div - Display calculated total price.
  - **ID: proceed-to-insurance-button** - Type: Button - Button to proceed to insurance options.

### 5. Insurance Options Page
- **Page Title**: Select Insurance Coverage
- **Overview**: A page for users to select insurance coverage for their rental.
- **Elements**:
  - **ID: insurance-page** - Type: Div - Container for the insurance page.
  - **ID: insurance-options** - Type: Div - Display of available insurance plans.
  - **ID: select-insurance-{insurance_id}** - Type: Radio - Radio button to select insurance plan (each plan has this).
  - **ID: insurance-description** - Type: Div - Display description of selected insurance plan.
  - **ID: insurance-price** - Type: Div - Display insurance price.
  - **ID: confirm-booking-button** - Type: Button - Button to confirm booking with insurance selection.

### 6. Rental History Page
- **Page Title**: Rental History
- **Overview**: A page displaying all previous rentals with details and status information.
- **Elements**:
  - **ID: history-page** - Type: Div - Container for the rental history page.
  - **ID: rentals-table** - Type: Table - Table displaying rentals with ID, vehicle, dates, location, and status.
  - **ID: view-rental-details-{rental_id}** - Type: Button - Button to view rental details (each rental has this).
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Active, Completed, Cancelled).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Reservation Management Page
- **Page Title**: My Reservations
- **Overview**: A page displaying current and upcoming reservations with management options.
- **Elements**:
  - **ID: reservations-page** - Type: Div - Container for the reservations page.
  - **ID: reservations-list** - Type: Div - List of all reservations with vehicle, dates, and status.
  - **ID: modify-reservation-button-{reservation_id}** - Type: Button - Button to modify reservation (each reservation has this).
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each reservation has this).
  - **ID: sort-by-date-button** - Type: Button - Button to sort reservations by date.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Special Requests Page
- **Page Title**: Special Requests
- **Overview**: A page for users to add special requests to their rental booking.
- **Elements**:
  - **ID: requests-page** - Type: Div - Container for the special requests page.
  - **ID: select-reservation** - Type: Dropdown - Dropdown to select reservation to add requests to.
  - **ID: driver-assistance-checkbox** - Type: Checkbox - Checkbox for driver assistance request.
  - **ID: gps-option-checkbox** - Type: Checkbox - Checkbox for GPS option.
  - **ID: child-seat-quantity** - Type: Input - Field to specify number of child seats needed.
  - **ID: special-notes** - Type: Textarea - Field to enter special notes and requests.
  - **ID: submit-requests-button** - Type: Button - Button to submit special requests.

### 9. Locations Page
- **Page Title**: Pickup and Dropoff Locations
- **Overview**: A page displaying all available rental pickup and dropoff locations with details.
- **Elements**:
  - **ID: locations-page** - Type: Div - Container for the locations page.
  - **ID: locations-list** - Type: Div - List of all rental locations with address and hours.
  - **ID: location-detail-button-{location_id}** - Type: Button - Button to view location details (each location has this).
  - **ID: hours-filter** - Type: Dropdown - Dropdown to filter by operating hours (24/7, Business Hours, Weekend).
  - **ID: search-location-input** - Type: Input - Field to search locations by city or name.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'CarRental' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Vehicles Data
- **File Name**: `vehicles.txt`
- **Data Format**:
  ```
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
  ```
- **Example Data**:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. Customers Data
- **File Name**: `customers.txt`
- **Data Format**:
  ```
  customer_id|name|email|phone|driver_license|license_expiry
  ```
- **Example Data**:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|city|address|phone|hours|available_vehicles
  ```
- **Example Data**:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. Rentals Data
- **File Name**: `rentals.txt`
- **Data Format**:
  ```
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
  ```
- **Example Data**:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. Insurance Data
- **File Name**: `insurance.txt`
- **Data Format**:
  ```
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
  ```
- **Example Data**:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
  ```
- **Example Data**:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
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

Your goal is to create comprehensive design specifications that enable Backend and Frontend developers to work completely independently without requiring knowledge of each other's code.

Task Details:
- Read user_task_description from CONTEXT
- Create design_spec.md with three main sections covering complete Flask routes for all CarRental pages, HTML template layouts with element IDs, and data schemas defining all text file formats exactly
- Ensure all data formats are pipe-delimited and field orders match user requirements
- Do NOT assume any authentication or add features beyond specified requirements

**Section 1: Flask Routes Specification (Backend)**

Provide a detailed route table that includes:
- Route Path: URL pattern (e.g., /dashboard, /vehicle/<int:vehicle_id>)
- Function Name: Flask function names, lowercase with underscores
- HTTP Method(s): GET or POST as applicable
- Template File: Exact HTML template filename
- Context Variables: All variables passed to template with precise type annotations (str, int, list, dict, etc.)

Requirements:
- Root route '/' MUST redirect to the dashboard page
- All function names must be consistent and descriptive of page functionality
- Context variables must exactly match fields in data schemas or form inputs
- Include navigation endpoints aligning with page buttons and links

**Section 2: HTML Template Specifications (Frontend)**

For each page template:
- Specify filename under templates/ directory (e.g., templates/dashboard.html)
- Provide exact Page Title (used in <title> and <h1>)
- Enumerate all required element IDs with element types and purpose
  - Include static and dynamic IDs, specifying dynamic patterns (e.g., view-details-button-{vehicle_id})
- Define navigation mappings using Flask url_for function names matching Section 1 routes
- Outline context variables accessible in template with expected structures and types

Requirements:
- Include all element IDs from user requirements to guarantee UI completeness
- Use Jinja2 templating syntax for dynamic content and loops
- Ensure consistency in naming conventions with Section 1 context variables
- Do NOT introduce elements or navigation items not described in requirements

**Section 3: Data File Schemas**

For each data file in data/ directory:
- Specify filename and precise pipe-delimited format with exact field order
- Define field names and expected data types (e.g., int, float, str, date)
- Provide 2-3 example data lines demonstrating realistic content
- Document what the file stores and its relation to the application domain

Files to cover:
- vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, reservations.txt

Requirements:
- Strict pipe-delimited formatting with NO headers
- Field order MUST be exactly as specified in user requirements
- Examples should reflect typical values and formats shown

CRITICAL SUCCESS CRITERIA:
- The backend can be implemented with Section 1 and Section 3 ONLY, fully supporting all page functionalities and data interactions
- The frontend can implement all HTML templates with Section 2 ONLY, ensuring correct UI elements, navigation, and dynamic content rendering
- No cross-dependency between backend and frontend code implementations
- All naming conventions, IDs, routing paths, and context variables must be consistent and error-free
- Use write_text_file tool exclusively for saving design_spec.md
- Do NOT add any authentication or features beyond those specified
- Maintain clarity, completeness, and precision in all specifications

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications for car rental systems.

Your goal is to implement the complete Flask backend app.py based on design_spec.md specifying all Flask routes and data schemas.

Task Details:
- Read design_spec.md Sections describing Flask routes and data file schemas ONLY
- Implement all routes exactly as specified with correct HTTP methods
- Load and save data from/to data/*.txt files according to schemas
- Do NOT read or implement any frontend templates or UI code
- Do NOT assume details not provided in design_spec.md

Implementation Requirements:
1. **Flask Application Setup:**
   ```python
   from flask import Flask, render_template, request, redirect, url_for
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root and Navigation Routes:**
   - Implement '/' route redirecting to dashboard page
   - Implement routes to handle all pages as per design_spec.md with exact function names and URL routes
   - Use render_template() with correct template file names from design_spec.md

3. **Data Handling:**
   - Read data from data files using pipe-delimited format as specified
   - Parse each line with line.strip().split('|')
   - Match field order and types exactly according to design_spec.md
   - Write data back in same pipe-delimited format if needed
   - Handle possible data read/write errors gracefully

4. **Forms and POST Handling:**
   - Implement route handlers for POST requests to handle booking, modifications, cancellations, and special requests
   - Use request.form to process input fields
   - Validate inputs according to specified fields; handle errors appropriately

5. **Business Logic:**
   - Enforce workflow rules such as navigation sequence (e.g., booking to insurance)
   - Maintain consistent naming for context variables and functions as per design_spec.md
   - Do NOT implement authentication or features not specified

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app.py
- Strictly follow Flask route and data schema specifications from design_spec.md
- Function and variable names MUST exactly match design_spec.md
- Do NOT include any frontend template code or styling
- Do NOT invent features or routes not described in design_spec.md

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications focused on car rental services.

Your goal is to implement all HTML templates (*.html) for the CarRental web app strictly following the frontend specifications and element IDs described in design_spec.md.

Task Details:
- Read design_spec.md Sections describing HTML templates, element IDs, navigation, and page layout ONLY
- Implement all HTML template files corresponding to each UI page specified
- Include ALL required element IDs with exact naming and casing
- Use Jinja2 templating syntax for dynamic data and loops
- Implement navigation and links using url_for() functions with correct routing names
- Do NOT read or implement any backend Python code or data handling logic
- Do NOT add or modify element IDs beyond what is specified

Implementation Requirements:
1. **Template Structure:**
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ page_title }}</title>
   </head>
   <body>
       <div id="main-container">
           <h1>{{ page_title }}</h1>
           <!-- Page-specific content -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs and Layout:**
   - Include all static and dynamic IDs exactly (e.g., view-details-button-{{ vehicle_id }})
   - Use proper Jinja2 syntax for dynamic IDs and data rendering
   - Preserve HTML semantics and accessibility best practices

3. **Forms and Inputs:**
   - Implement forms for booking, insurance selection, requests submission as specified
   - Use method="POST" for forms interacting with backend routes that handle POST

4. **Navigation:**
   - Map buttons and links using url_for() with route names exactly as specified
   - Include navigation buttons to enable smooth page flow as designed

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save each template file individually inside templates/ folder
- Ensure all element IDs conform exactly to design_spec.md (case-sensitive)
- Page titles in <title> and <h1> must match design_spec.md exactly
- Do NOT add features or pages not specified
- Do NOT include any backend Python code in templates

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
        ("BackendDeveloper", """Check design_spec.md for backend completeness: "
                "Verify Flask routes for all pages exist with correct function names, context variables, and HTTP methods, "
                "Verify data schemas match required text file formats with exact field order and delimiter consistency.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md for frontend completeness: "
                "Verify HTML templates define all pages with correct element IDs, navigation mappings using url_for, and required UI components.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all Flask routes exactly as specified in design_spec.md with correct context variables, HTTP methods, "
                "and data loading/saving functions conforming to defined data schemas.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all HTML templates match design_spec.md in element IDs, layout, and navigation routing using url_for functions, "
                "ensuring full compliance with frontend design specifications.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],


}




# ==================== Chaos Controller Setup ====================
chaos_controller = ChaosController(
    agent_chaos_enabled=False,
    stress_chaos_enabled=False,
    io_chaos_enabled=True,
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

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create comprehensive design_spec.md with Flask routes, HTML template specs, and data schemas for CarRental as per user_task_description")
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
        timeout_threshold=200,
        failure_threshold=1,
        recovery_time=30
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
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement backend app.py based on design_spec.md"),
        execute(FrontendDeveloper, "Implement all HTML templates in templates/ based on design_spec.md")
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
