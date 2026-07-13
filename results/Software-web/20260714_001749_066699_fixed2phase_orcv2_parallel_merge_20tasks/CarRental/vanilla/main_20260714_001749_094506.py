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
# 20260714_001749_094506/main_20260714_001749_094506.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend designs covering Flask routes, data schemas, and all 9 CarRental pages with exact element IDs and local text file data format; produce a consistent merged design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDesignArchitect specifies Flask backend routes, data management, and business logic in backend_design.md; FrontendDesignArchitect specifies HTML templates, element IDs, layout, and navigation in frontend_design.md; DesignMerger consolidates these two documents into a unified design_spec.md meeting all user requirements.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend development and local file data management using Python.\n\nYour goal is to create a complete Flask backend design supporting all required CarRental pages, including routes, business logic, and data schemas stored in local text files.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand all required pages, backend functionalities, and data formats\n- Independently create backend_design.md describing Flask routes, data read/write logic, and data schemas for local text files\n- Do not read or rely on any frontend design files; focus solely on backend components\n\n**Section 1: Flask Routes and Business Logic Design**\n- Define a Flask route for each of the 9 pages including URL paths, HTTP methods, and expected request parameters\n- Specify search, booking, reservation management, insurance handling, and special request workflows in route handlers\n- Include logic for reading and writing data in the specified text-file formats under the 'data' directory\n\n**Section 2: Data File Schemas and Formats**\n- Specify schemas for each local text file (vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, reservations.txt)\n- Detail field names, data types, delimiters, and example data rows strictly as provided in user requirements\n- Ensure naming consistency with route handlers and data access logic\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can implement Flask app.py routes and data handling directly from backend_design.md\n- All routes and data schemas fully cover user task requirements and comply with data format constraints\n- Use write_text_file tool to produce backend_design.md exactly as a text file\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and Jinja2 template design for Flask web applications.\n\nYour goal is to create detailed frontend design for the CarRental web application, specifying HTML templates with exact element IDs, layouts, UI components, and navigation structures for all 9 pages.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand all page titles, elements with exact IDs, and UI/UX requirements\n- Independently create frontend_design.md detailing templates for all pages, element IDs, navigation flows, and data placeholders for dynamic content\n- Do not read or rely on any backend design files; focus solely on frontend components\n\n**Section 1: HTML Template Specifications**\n- For each of the 9 pages, specify the template filename and page title\n- List all required element IDs with element types and their purpose or content described precisely as in the user task\n- Specify buttons, dropdowns, inputs, and other UI components including dynamic elements with unique IDs using clear naming conventions (e.g., view-details-button-{vehicle_id})\n\n**Section 2: Navigation and Interaction Design**\n- Map navigation flows between pages triggered by buttons and links, specifying associated element IDs\n- Include placeholders for dynamic data rendered from backend context variables\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement templates/*.html with correct structure and element IDs from frontend_design.md\n- The design covers all pages and UI components described in the user task completely and accurately\n- Use write_text_file tool to produce frontend_design.md exactly as a text file\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in consolidating backend and frontend design specifications into a coherent Flask web app contract.\n\nYour goal is to merge backend_design.md and frontend_design.md into a consistent design_spec.md document that satisfies all user requirements without adding new features.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Cross-check route definitions, data schemas, and element IDs for consistency and naming conformity\n- Produce design_spec.md combining backend Flask routes, data file schemas, and frontend HTML template specs in a unified format\n- Resolve naming mismatches between backend context variables and frontend element IDs to ensure alignment\n\n**Section 1: Backend Routes and Data Schemas**\n- Preserve all routes, HTTP methods, route parameters, and business logic from backend_design.md\n- Retain all local text file data schemas exactly as designed, ensuring no conflicts with frontend needs\n\n**Section 2: Frontend Templates and Navigation**\n- Preserve all template pages, element IDs, UI components, and navigation mapping from frontend_design.md\n- Align frontend context variables and naming conventions with backend routes for seamless integration\n\n**Section 3: Consistency and Completeness Checks**\n- Ensure every page route has an associated HTML template with matching names and identifiers\n- Verify data file formats support all required backend operations and frontend data placeholders\n- Confirm no feature is added beyond what user_task_description mandates\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper obtains complete API contract and data schema in design_spec.md\n- FrontendDeveloper obtains complete UI contract consistent with backend in design_spec.md\n- Use write_text_file tool exclusively to output finalized design_spec.md text file\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Validate completeness and correctness of backend routes and data schema design per user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Validate frontend element IDs, page structure, and compliance with all UI requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend app.py and frontend templates for all 9 pages based on design_spec.md and merge them into a working CarRental application with matching interfaces and pages\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDeveloper implements app.py following backend design rules; FrontendDeveloper creates templates/*.html for all pages per frontend design; IntegrationMerger integrates both producing final app.py and templates/*.html ensuring interface consistency.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with Python and local text file data management.\n\nYour goal is to implement a complete Flask backend application (app.py) for the CarRental system based on the provided design_spec.md, handling vehicle management, bookings, reservations, insurance, and special requests via local text files.\n\nTask Details:\n- Read design_spec.md from CONTEXT for backend route and business logic specifications.\n- Independently create app.py implementing all Flask routes, data operations, and business logic.\n- Do not access or depend on frontend templates/*.html files.\n\n**Section 1: Flask Route Implementation**\n- Implement all Flask routes as specified in design_spec.md including HTTP methods, URLs, and expected responses.\n- Ensure route handlers load, parse, and update local text files in the 'data' directory following defined schemas.\n- Implement logic for vehicle search, bookings, reservation management, insurance selection, rental history, special requests, and location listings.\n- Follow error handling and validation rules as implied by design.\n\n**Section 2: Data Handling with Local Text Files**\n- Use file I/O to read and update the vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, and reservations.txt files respecting their exact data formats.\n- Implement parsing logic for pipe-delimited data fields and maintain data integrity.\n- Handle all business logic computations such as price calculation, status updates, and availability checks within backend.\n\n**Section 3: Application Structure and Configuration**\n- Use Flask app structure, blueprints if applicable, and configuration consistent with a production-ready app.py.\n- Implement templates rendering calls but do not supply template files.\n- Include necessary imports, app initialization, and route registration.\n\nCRITICAL SUCCESS CRITERIA:\n- Flask backend app.py must fully implement all routes and logic declared in design_spec.md.\n- Must use write_text_file tool to output final app.py file with correct syntax and completeness.\n- Must not read or incorporate frontend template files.\n- Output only the declared artifact app.py with no refinement feedback.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask web applications.\n\nYour goal is to implement complete HTML templates (*.html) for the CarRental web app with exact element IDs, structure, and UI as specified in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT for frontend template structures, element IDs, pages, and UI details.\n- Independently create templates/*.html files for all 9 CarRental pages with exact page titles, container IDs, buttons, forms, and other UI elements.\n- Do not read or depend on backend app.py code or route implementations.\n\n**Section 1: HTML Template Implementation**\n- Create one .html file per page with precise element IDs as specified in design_spec.md.\n- Ensure all buttons, dropdowns, inputs, tables, and div containers match declared IDs and types.\n- Implement UI layout including headers, footers, navigation links, and forms as per page descriptions without adding features.\n\n**Section 2: Jinja2 Context Variables and Template Logic**\n- Include placeholder blocks for Jinja2 variables referenced by backend app.py routes to display data dynamically.\n- Maintain consistent naming conventions and context variable usage as declared in design_spec.md.\n- Do not introduce new UI elements beyond those declared.\n\n**Section 3: File Structure and Formatting**\n- Organize templates in templates/ directory with meaningful filenames.\n- Ensure valid HTML5 with embedded Jinja2 templating syntax where relevant.\n- Avoid inline scripts or styles unless specified.\n\nCRITICAL SUCCESS CRITERIA:\n- Templates must exactly match design_spec.md element IDs and layout requirements.\n- Must use write_text_file tool to save all templates/*.html files.\n- Must not read or rely on backend implementation files.\n- Output only the declared artifact templates/*.html without refinement feedback.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integrator specializing in combining Flask backend and frontend template implementations for web applications.\n\nYour goal is to merge the independently created app.py and templates/*.html files into a consistent, deployable CarRental application, ensuring interface alignment and matching elements without adding new features.\n\nTask Details:\n- Read design_spec.md, backend app.py, and frontend templates/*.html files from CONTEXT.\n- Compare app.py routes, context variables, and template filenames with templates/*.html element IDs and page structures.\n- Resolve any inconsistencies in route URLs, template names, and element IDs ensuring full alignment with design_spec.md.\n- Produce final app.py and templates/*.html files with unified interfaces conforming to the input specifications.\n\n**Section 1: Interface Consistency Verification**\n- Check that every Flask route in app.py corresponds to an existing template file and page element IDs.\n- Ensure all element IDs used in templates/*.html are referenced appropriately in app.py rendering calls.\n- Verify naming conventions for variables, buttons, and page containers are consistent across backend and frontend.\n\n**Section 2: Merged Artifact Creation**\n- Edit or adjust app.py and templates/*.html only to fix inconsistencies found without adding or removing functionality.\n- Preserve all declared functionality and UI elements from input artifacts.\n- Produce correctly formatted, runnable app.py and valid HTML template files ready for deployment.\n\n**Section 3: Final Output Requirements**\n- Output final consolidated app.py and templates/*.html as canonical deliverables.\n- Do not add any new features or design elements beyond input artifacts.\n\nCRITICAL SUCCESS CRITERIA:\n- Final app.py and templates/*.html must implement consistent routes, rendering calls, and element IDs from design_spec.md.\n- Use write_text_file tool to save final app.py and all template files.\n- Focus exclusively on interface alignment and artifact synthesis.\n- Output only the declared artifacts app.py and templates/*.html without any refinement markers.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify app.py implementation correctly follows design_spec.md, including routes and data handling.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}, {\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify templates/*.html match design_spec.md element IDs and page layouts exactly.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}, {\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend development and local file data management using Python.

Your goal is to create a complete Flask backend design supporting all required CarRental pages, including routes, business logic, and data schemas stored in local text files.

Task Details:
- Read user_task_description from CONTEXT to understand all required pages, backend functionalities, and data formats
- Independently create backend_design.md describing Flask routes, data read/write logic, and data schemas for local text files
- Do not read or rely on any frontend design files; focus solely on backend components

**Section 1: Flask Routes and Business Logic Design**
- Define a Flask route for each of the 9 pages including URL paths, HTTP methods, and expected request parameters
- Specify search, booking, reservation management, insurance handling, and special request workflows in route handlers
- Include logic for reading and writing data in the specified text-file formats under the 'data' directory

**Section 2: Data File Schemas and Formats**
- Specify schemas for each local text file (vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, reservations.txt)
- Detail field names, data types, delimiters, and example data rows strictly as provided in user requirements
- Ensure naming consistency with route handlers and data access logic

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement Flask app.py routes and data handling directly from backend_design.md
- All routes and data schemas fully cover user task requirements and comply with data format constraints
- Use write_text_file tool to produce backend_design.md exactly as a text file

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

Your goal is to create detailed frontend design for the CarRental web application, specifying HTML templates with exact element IDs, layouts, UI components, and navigation structures for all 9 pages.

Task Details:
- Read user_task_description from CONTEXT to understand all page titles, elements with exact IDs, and UI/UX requirements
- Independently create frontend_design.md detailing templates for all pages, element IDs, navigation flows, and data placeholders for dynamic content
- Do not read or rely on any backend design files; focus solely on frontend components

**Section 1: HTML Template Specifications**
- For each of the 9 pages, specify the template filename and page title
- List all required element IDs with element types and their purpose or content described precisely as in the user task
- Specify buttons, dropdowns, inputs, and other UI components including dynamic elements with unique IDs using clear naming conventions (e.g., view-details-button-{vehicle_id})

**Section 2: Navigation and Interaction Design**
- Map navigation flows between pages triggered by buttons and links, specifying associated element IDs
- Include placeholders for dynamic data rendered from backend context variables

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement templates/*.html with correct structure and element IDs from frontend_design.md
- The design covers all pages and UI components described in the user task completely and accurately
- Use write_text_file tool to produce frontend_design.md exactly as a text file

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in consolidating backend and frontend design specifications into a coherent Flask web app contract.

Your goal is to merge backend_design.md and frontend_design.md into a consistent design_spec.md document that satisfies all user requirements without adding new features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Cross-check route definitions, data schemas, and element IDs for consistency and naming conformity
- Produce design_spec.md combining backend Flask routes, data file schemas, and frontend HTML template specs in a unified format
- Resolve naming mismatches between backend context variables and frontend element IDs to ensure alignment

**Section 1: Backend Routes and Data Schemas**
- Preserve all routes, HTTP methods, route parameters, and business logic from backend_design.md
- Retain all local text file data schemas exactly as designed, ensuring no conflicts with frontend needs

**Section 2: Frontend Templates and Navigation**
- Preserve all template pages, element IDs, UI components, and navigation mapping from frontend_design.md
- Align frontend context variables and naming conventions with backend routes for seamless integration

**Section 3: Consistency and Completeness Checks**
- Ensure every page route has an associated HTML template with matching names and identifiers
- Verify data file formats support all required backend operations and frontend data placeholders
- Confirm no feature is added beyond what user_task_description mandates

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper obtains complete API contract and data schema in design_spec.md
- FrontendDeveloper obtains complete UI contract consistent with backend in design_spec.md
- Use write_text_file tool exclusively to output finalized design_spec.md text file

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with Python and local text file data management.

Your goal is to implement a complete Flask backend application (app.py) for the CarRental system based on the provided design_spec.md, handling vehicle management, bookings, reservations, insurance, and special requests via local text files.

Task Details:
- Read design_spec.md from CONTEXT for backend route and business logic specifications.
- Independently create app.py implementing all Flask routes, data operations, and business logic.
- Do not access or depend on frontend templates/*.html files.

**Section 1: Flask Route Implementation**
- Implement all Flask routes as specified in design_spec.md including HTTP methods, URLs, and expected responses.
- Ensure route handlers load, parse, and update local text files in the 'data' directory following defined schemas.
- Implement logic for vehicle search, bookings, reservation management, insurance selection, rental history, special requests, and location listings.
- Follow error handling and validation rules as implied by design.

**Section 2: Data Handling with Local Text Files**
- Use file I/O to read and update the vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, and reservations.txt files respecting their exact data formats.
- Implement parsing logic for pipe-delimited data fields and maintain data integrity.
- Handle all business logic computations such as price calculation, status updates, and availability checks within backend.

**Section 3: Application Structure and Configuration**
- Use Flask app structure, blueprints if applicable, and configuration consistent with a production-ready app.py.
- Implement templates rendering calls but do not supply template files.
- Include necessary imports, app initialization, and route registration.

CRITICAL SUCCESS CRITERIA:
- Flask backend app.py must fully implement all routes and logic declared in design_spec.md.
- Must use write_text_file tool to output final app.py file with correct syntax and completeness.
- Must not read or incorporate frontend template files.
- Output only the declared artifact app.py with no refinement feedback.

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

Your goal is to implement complete HTML templates (*.html) for the CarRental web app with exact element IDs, structure, and UI as specified in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT for frontend template structures, element IDs, pages, and UI details.
- Independently create templates/*.html files for all 9 CarRental pages with exact page titles, container IDs, buttons, forms, and other UI elements.
- Do not read or depend on backend app.py code or route implementations.

**Section 1: HTML Template Implementation**
- Create one .html file per page with precise element IDs as specified in design_spec.md.
- Ensure all buttons, dropdowns, inputs, tables, and div containers match declared IDs and types.
- Implement UI layout including headers, footers, navigation links, and forms as per page descriptions without adding features.

**Section 2: Jinja2 Context Variables and Template Logic**
- Include placeholder blocks for Jinja2 variables referenced by backend app.py routes to display data dynamically.
- Maintain consistent naming conventions and context variable usage as declared in design_spec.md.
- Do not introduce new UI elements beyond those declared.

**Section 3: File Structure and Formatting**
- Organize templates in templates/ directory with meaningful filenames.
- Ensure valid HTML5 with embedded Jinja2 templating syntax where relevant.
- Avoid inline scripts or styles unless specified.

CRITICAL SUCCESS CRITERIA:
- Templates must exactly match design_spec.md element IDs and layout requirements.
- Must use write_text_file tool to save all templates/*.html files.
- Must not read or rely on backend implementation files.
- Output only the declared artifact templates/*.html without refinement feedback.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integrator specializing in combining Flask backend and frontend template implementations for web applications.

Your goal is to merge the independently created app.py and templates/*.html files into a consistent, deployable CarRental application, ensuring interface alignment and matching elements without adding new features.

Task Details:
- Read design_spec.md, backend app.py, and frontend templates/*.html files from CONTEXT.
- Compare app.py routes, context variables, and template filenames with templates/*.html element IDs and page structures.
- Resolve any inconsistencies in route URLs, template names, and element IDs ensuring full alignment with design_spec.md.
- Produce final app.py and templates/*.html files with unified interfaces conforming to the input specifications.

**Section 1: Interface Consistency Verification**
- Check that every Flask route in app.py corresponds to an existing template file and page element IDs.
- Ensure all element IDs used in templates/*.html are referenced appropriately in app.py rendering calls.
- Verify naming conventions for variables, buttons, and page containers are consistent across backend and frontend.

**Section 2: Merged Artifact Creation**
- Edit or adjust app.py and templates/*.html only to fix inconsistencies found without adding or removing functionality.
- Preserve all declared functionality and UI elements from input artifacts.
- Produce correctly formatted, runnable app.py and valid HTML template files ready for deployment.

**Section 3: Final Output Requirements**
- Output final consolidated app.py and templates/*.html as canonical deliverables.
- Do not add any new features or design elements beyond input artifacts.

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html must implement consistent routes, rendering calls, and element IDs from design_spec.md.
- Use write_text_file tool to save final app.py and all template files.
- Focus exclusively on interface alignment and artifact synthesis.
- Output only the declared artifacts app.py and templates/*.html without any refinement markers.

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
        ("DesignMerger", """Validate completeness and correctness of backend routes and data schema design per user requirements.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Validate frontend element IDs, page structure, and compliance with all UI requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify app.py implementation correctly follows design_spec.md, including routes and data handling.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify templates/*.html match design_spec.md element IDs and page layouts exactly.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
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
        execute(BackendDesignArchitect, "Create backend_design.md with Flask routes, business logic, and data schemas for CarRental app based on user_task_description."),
        execute(FrontendDesignArchitect, "Create frontend_design.md with HTML templates, exact element IDs, layouts, navigation flows for CarRental app based on user_task_description.")
    )

    # Read backend_design.md and frontend_design.md outputs
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

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        "Merge backend_design.md and frontend_design.md into design_spec.md ensuring consistency, alignment of context variables and element IDs, and no new features added.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel backend and frontend implementation
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete Flask backend app.py for CarRental system based on design_spec.md; handle all routes, data files, and business logic; do not read templates."),
        execute(FrontendDeveloper,
                "Implement complete templates/*.html files (9 pages) for CarRental system based on design_spec.md; exact element IDs, UI, and Jinja2 context variables; do not read app.py.")
    )

    # Read outputs from backend and frontend developers
    backend_app_py = ""
    frontend_templates_content = ""
    try:
        backend_app_py = open("app.py").read()
    except Exception:
        pass

    import glob
    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates_content += f"\n=== {tpl_path} ===\n" + open(tpl_path).read()
        except Exception:
            pass

    # Merge backend and frontend to unify interfaces
    await execute(
        IntegrationMerger,
        f"Merge backend and frontend CarRental app implementations ensuring consistent routes, template names, and element IDs as per design_spec.md.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== Backend app.py ===\n{backend_app_py}\n\n"
        f"=== Frontend templates ===\n{frontend_templates_content}"
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
