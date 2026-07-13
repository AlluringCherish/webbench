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
# 20260713_204916_927944/main_20260713_204916_927944.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the CarRental web application requirements and produce a complete design_spec.md detailing all pages, elements, data files, and interactions.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first produces requirements_analysis.md capturing detailed user requirements; then WebArchitect reads it and writes design_spec.md \"\n        \"covering page structure, element IDs, navigation, data files, file formats, and programmatic constraints.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in web application requirements analysis.\n\nYour goal is to extract and document all user requirements to produce a detailed requirements_analysis.md file capturing complete features, page structures, UI elements, data storage formats, and navigation flows.\n\nTask Details:\n- Read the full user_task_description artifact from CONTEXT\n- Extract all pages with their titles, purposes, and UI elements including exact element IDs and types\n- Document the local data files including filenames, field orders, formats, and example data\n- Capture navigation flows between pages with button/link functionality\n\nRequirements Analysis:\n1. **Page Structures**\n   - List all pages with page titles and overviews\n   - Detail all UI elements per page with IDs, types, and roles\n\n2. **Data Storage**\n   - List all required data files under 'data/' directory\n   - Define file formats (pipe-delimited) and field orders precisely\n   - Capture example data entries for each file\n\n3. **Navigation and Interaction Flows**\n   - Identify interactive elements triggering page transitions\n   - Capture sequence and dependencies among pages\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output requirements_analysis.md\n- The analysis MUST be comprehensive, clear, and structured for use by downstream architectural design\n- Include verbatim element IDs and field names as provided in user requirements\n- Focus solely on requirements extraction without design or implementation speculation\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web application design and architecture.\n\nYour goal is to create a comprehensive design_spec.md that defines the complete Flask app structure for the CarRental project, enabling independent backend and frontend development.\n\nTask Details:\n- Read requirements_analysis.md from CONTEXT thoroughly\n- Define all 9 pages with exact element IDs, their purposes, and structure as Flask templates\n- Specify navigation flows between pages starting from the Dashboard page\n- Detail all local data files under 'data/' directory:\n  - Provide filenames, precise pipe-delimited field orders, field descriptions\n  - Include sample realistic data rows per file\n- Clarify programmatic constraints and integration points for backend/frontend teams\n\nDesign Specification Requirements:\n1. **Page Definitions**\n   - Include page names, titles, and container div IDs\n   - Detail all element IDs (buttons, inputs, dropdowns, tables) per page\n   - Map interactive elements to navigation endpoints\n\n2. **Data File Schemas**\n   - File path: data/{filename}.txt\n   - Exact field order using pipe-delimited format (|)\n   - Description and example data for each file\n\n3. **Navigation Mapping**\n   - Clearly document buttons/links initiating page transitions using Flask route references\n   - Ensure starting point is Dashboard page '/'\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_spec.md\n- The specification MUST be sufficiently detailed to enable independent parallel backend and frontend implementation\n- All element IDs, data field names, and navigation sources MUST match requirements_analysis.md exactly\n- Avoid including implementation code; focus on detailed design and specifications\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md correctly and comprehensively captures all pages, elements, data formats, and navigation before architecture design.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the CarRental Flask web application with app.py and complete templates/*.html per design_spec.md, managing data via local text files.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineer first writes app_draft.py and draft templates_draft/*.html from design_spec.md, then IntegrationEngineer integrates drafts into the final \"\n        \"app.py and templates/*.html ensuring Flask compatibility and all functional requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Implementation Engineer specializing in Flask web application development.\n\nYour goal is to create a full draft implementation of the Flask backend app and all frontend HTML templates to closely follow the design specification, enabling a complete functional prototype.\n\nTask Details:\n- Read design_spec.md fully to extract route specifications, UI element IDs, data storage formats, and page layouts\n- Produce app_draft.py implementing Flask routes, request handling, and business logic accordingly\n- Produce templates_draft/*.html for all 9 specified pages, ensuring all element IDs and UI components match design_spec.md exactly\n- Focus on integration readiness: code and templates must be coherent and aligned with design_spec.md input and output requirements\n\nBackend Draft Implementation:\n1. Setup Flask app structure in app_draft.py with all routes from design_spec.md\n2. Implement request handling for GET and POST as specified\n3. Load and save data with local text files under data/ directory using precise pipe-delimited formats\n4. Use exact function and route names to align with specification\n5. Decorate templates rendering with corresponding context variables as per specification\n\nFrontend Draft Implementation:\n1. Implement complete HTML templates for 9 pages under templates_draft/\n2. Include all element IDs exactly as specified: static and dynamic with correct Jinja2 templating for variable interpolation\n3. Incorporate UI components including buttons, tables, forms, and inputs as described\n4. Assure navigation and linking correctly correspond to Flask route functions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all template files under templates_draft/\n- All element IDs and route names must match design_spec.md exactly (case-sensitive)\n- Data file reading and writing in app_draft.py must respect exact file formats and field ordering\n- Maintain separation of backend and frontend responsibilities but ensure draft completeness\n- Do not finalize – this is a draft for integration later\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Senior Flask Integration Engineer specializing in combining backend and frontend drafts into production-ready Flask applications.\n\nYour goal is to integrate the draft backend (app_draft.py) and draft frontend templates (templates_draft/*.html) into a finalized Flask application (app.py with templates/*.html), ensuring full compliance with design specification and flawless functionality.\n\nTask Details:\n- Read design_spec.md comprehensively to verify all route, template, and data schema requirements\n- Use app_draft.py and templates_draft/*.html as source drafts for integration and refinement\n- Produce final app.py that runs the Flask server starting at Dashboard page, with correct routing and business logic per specification\n- Produce final templates/*.html with complete, correct HTML, UI elements, and Jinja2 syntax precisely as required\n- Verify backend reads and writes local data files in data/ directory with exact pipe-delimited formats and field order from design_spec.md\n\nIntegration Requirements:\n1. Review and refine route handlers ensuring proper Flask idioms for redirects, rendering, and form processing\n2. Confirm all route function names, HTTP methods, and URL paths correspond exactly to design_spec.md\n3. Align template files with final directory and filename conventions under templates/\n4. Ensure dynamic element IDs use Jinja2 expression syntax correctly, matching specification\n5. Optimize file I/O with proper error handling for all local data text files\n6. Remove any draft-only code or placeholders, replacing with production-quality implementations\n7. Confirm the root route redirects to Dashboard page exactly as required\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and all templates under templates/\n- All routes, template filenames, and element IDs must exactly match design_spec.md specification\n- Data load/save code must strictly follow data file formats in data/ folder\n- Final app.py must be executable as a standalone Flask app without reliance on drafts\n- No draft artifact references must remain in final deliverables\n- Ensure seamless navigation and UI integrity as per specification\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"ImplementationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Check app_draft.py and templates_draft/*.html to ensure full coverage of design_spec.md including precise element IDs, routing, and local data file handling before final integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and refine the final CarRental Flask app.py and templates/*.html to ensure correctness, complete functionality, and adherence to design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"QualityAssurer validates app.py and templates/*.html against design_spec.md producing validation_report.md; then SequentialFixer applies corrections producing the final validated application.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"QualityAssurer\",\n            \"prompt\": \"\"\"You are a Software Quality Assurance Engineer specializing in Python Flask applications and frontend HTML validation.\n\nYour goal is to validate the final CarRental Flask backend and frontend templates for correctness, functionality completeness, and adherence to design specifications.\n\nTask Details:\n- Read design_spec.md to understand all page, route, data schema, and template specifications\n- Validate app.py for syntax correctness, runtime errors, and complete route coverage\n- Validate all templates/*.html files for presence of correct element IDs, page titles, and data bindings\n- Confirm handling of all pages, routes, and correct reading/writing of local text files as per design_spec.md\n- Produce validation_report.md detailing all issues found and verification results\n\nValidation Requirements:\n1. **Backend Validation**:\n   - Use validate_python_file tool on app.py for syntax and runtime checks\n   - Verify all Flask routes defined in design_spec.md are implemented\n   - Verify data reading/parsing from local data/*.txt files matches schema and usage correctly\n   - Test basic runtime behavior of app.py using execute_python_code within constraints\n\n2. **Frontend Validation**:\n   - Check all required HTML element IDs and page titles exist exactly as specified in design_spec.md\n   - Verify dynamic elements correctly use Jinja2 templating for variables and loops\n   - Confirm navigation elements and buttons functionally correspond to routes\n\n3. **Coverage Verification**:\n   - Ensure each page defined in design_spec.md is implemented and accessible\n   - Confirm form inputs, buttons, and interactive components handle data correctly\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file tool for Python file validation\n- MUST use execute_python_code tool for runtime testing\n- Write detailed validation_report.md with findings, issues, and recommendations using write_text_file\n- Do not modify any files; only assess and report\n- Focus solely on artifacts: app.py, templates/*.html, design_spec.md\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application maintenance and frontend templating.\n\nYour goal is to apply corrections from validation_report.md to finalize app.py and templates/*.html ensuring full compliance with design_spec.md and all validation criteria.\n\nTask Details:\n- Read validation_report.md to identify all required fixes and issues\n- Use design_spec.md as authoritative reference for required functionality and specifications\n- Apply necessary code fixes to app.py to correct syntax, runtime, and route handling issues\n- Update templates/*.html files to correct element IDs, page titles, data bindings, and navigation as specified\n- Ensure no regressions or loss of functionality occur in the final deliverables\n\nImplementation Requirements:\n1. **Backend Corrections**:\n   - Modify code preserving original design and data schemas\n   - Fix all reported errors and omissions from validation_report.md\n\n2. **Frontend Corrections**:\n   - Correct all specified element ID and page title mismatches\n   - Fix Jinja2 syntax for dynamic content and navigation as needed\n   - Ensure accessible and consistent UI elements per design_spec.md\n\n3. **Final Validation**:\n   - Confirm corrections align with design_spec.md requirements\n   - Maintain clean, readable, and consistent code style\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html files\n- Strictly follow specifications in design_spec.md and corrections in validation_report.md\n- Deliver final validated source code and templates ready for deployment\n- Do not introduce features beyond original scope\n- Preserve data schema and file naming conventions\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"QualityAssurer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"QualityAssurer\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Confirm validation_report.md accurately identifies all issues and that corrections for final app.py and templates/*.html address these while retaining full feature coverage.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify that final app.py and templates/*.html fully implement all requirements from validation_report.md and ultimately the original user task.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Business Analyst specializing in web application requirements analysis.

Your goal is to extract and document all user requirements to produce a detailed requirements_analysis.md file capturing complete features, page structures, UI elements, data storage formats, and navigation flows.

Task Details:
- Read the full user_task_description artifact from CONTEXT
- Extract all pages with their titles, purposes, and UI elements including exact element IDs and types
- Document the local data files including filenames, field orders, formats, and example data
- Capture navigation flows between pages with button/link functionality

Requirements Analysis:
1. **Page Structures**
   - List all pages with page titles and overviews
   - Detail all UI elements per page with IDs, types, and roles

2. **Data Storage**
   - List all required data files under 'data/' directory
   - Define file formats (pipe-delimited) and field orders precisely
   - Capture example data entries for each file

3. **Navigation and Interaction Flows**
   - Identify interactive elements triggering page transitions
   - Capture sequence and dependencies among pages

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md
- The analysis MUST be comprehensive, clear, and structured for use by downstream architectural design
- Include verbatim element IDs and field names as provided in user requirements
- Focus solely on requirements extraction without design or implementation speculation

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Software Architect specializing in Flask web application design and architecture.

Your goal is to create a comprehensive design_spec.md that defines the complete Flask app structure for the CarRental project, enabling independent backend and frontend development.

Task Details:
- Read requirements_analysis.md from CONTEXT thoroughly
- Define all 9 pages with exact element IDs, their purposes, and structure as Flask templates
- Specify navigation flows between pages starting from the Dashboard page
- Detail all local data files under 'data/' directory:
  - Provide filenames, precise pipe-delimited field orders, field descriptions
  - Include sample realistic data rows per file
- Clarify programmatic constraints and integration points for backend/frontend teams

Design Specification Requirements:
1. **Page Definitions**
   - Include page names, titles, and container div IDs
   - Detail all element IDs (buttons, inputs, dropdowns, tables) per page
   - Map interactive elements to navigation endpoints

2. **Data File Schemas**
   - File path: data/{filename}.txt
   - Exact field order using pipe-delimited format (|)
   - Description and example data for each file

3. **Navigation Mapping**
   - Clearly document buttons/links initiating page transitions using Flask route references
   - Ensure starting point is Dashboard page '/'

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_spec.md
- The specification MUST be sufficiently detailed to enable independent parallel backend and frontend implementation
- All element IDs, data field names, and navigation sources MUST match requirements_analysis.md exactly
- Avoid including implementation code; focus on detailed design and specifications

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineer": {
        "prompt": (
            """You are a Backend and Frontend Implementation Engineer specializing in Flask web application development.

Your goal is to create a full draft implementation of the Flask backend app and all frontend HTML templates to closely follow the design specification, enabling a complete functional prototype.

Task Details:
- Read design_spec.md fully to extract route specifications, UI element IDs, data storage formats, and page layouts
- Produce app_draft.py implementing Flask routes, request handling, and business logic accordingly
- Produce templates_draft/*.html for all 9 specified pages, ensuring all element IDs and UI components match design_spec.md exactly
- Focus on integration readiness: code and templates must be coherent and aligned with design_spec.md input and output requirements

Backend Draft Implementation:
1. Setup Flask app structure in app_draft.py with all routes from design_spec.md
2. Implement request handling for GET and POST as specified
3. Load and save data with local text files under data/ directory using precise pipe-delimited formats
4. Use exact function and route names to align with specification
5. Decorate templates rendering with corresponding context variables as per specification

Frontend Draft Implementation:
1. Implement complete HTML templates for 9 pages under templates_draft/
2. Include all element IDs exactly as specified: static and dynamic with correct Jinja2 templating for variable interpolation
3. Incorporate UI components including buttons, tables, forms, and inputs as described
4. Assure navigation and linking correctly correspond to Flask route functions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all template files under templates_draft/
- All element IDs and route names must match design_spec.md exactly (case-sensitive)
- Data file reading and writing in app_draft.py must respect exact file formats and field ordering
- Maintain separation of backend and frontend responsibilities but ensure draft completeness
- Do not finalize – this is a draft for integration later

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Senior Flask Integration Engineer specializing in combining backend and frontend drafts into production-ready Flask applications.

Your goal is to integrate the draft backend (app_draft.py) and draft frontend templates (templates_draft/*.html) into a finalized Flask application (app.py with templates/*.html), ensuring full compliance with design specification and flawless functionality.

Task Details:
- Read design_spec.md comprehensively to verify all route, template, and data schema requirements
- Use app_draft.py and templates_draft/*.html as source drafts for integration and refinement
- Produce final app.py that runs the Flask server starting at Dashboard page, with correct routing and business logic per specification
- Produce final templates/*.html with complete, correct HTML, UI elements, and Jinja2 syntax precisely as required
- Verify backend reads and writes local data files in data/ directory with exact pipe-delimited formats and field order from design_spec.md

Integration Requirements:
1. Review and refine route handlers ensuring proper Flask idioms for redirects, rendering, and form processing
2. Confirm all route function names, HTTP methods, and URL paths correspond exactly to design_spec.md
3. Align template files with final directory and filename conventions under templates/
4. Ensure dynamic element IDs use Jinja2 expression syntax correctly, matching specification
5. Optimize file I/O with proper error handling for all local data text files
6. Remove any draft-only code or placeholders, replacing with production-quality implementations
7. Confirm the root route redirects to Dashboard page exactly as required

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and all templates under templates/
- All routes, template filenames, and element IDs must exactly match design_spec.md specification
- Data load/save code must strictly follow data file formats in data/ folder
- Final app.py must be executable as a standalone Flask app without reliance on drafts
- No draft artifact references must remain in final deliverables
- Ensure seamless navigation and UI integrity as per specification

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'ImplementationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "QualityAssurer": {
        "prompt": (
            """You are a Software Quality Assurance Engineer specializing in Python Flask applications and frontend HTML validation.

Your goal is to validate the final CarRental Flask backend and frontend templates for correctness, functionality completeness, and adherence to design specifications.

Task Details:
- Read design_spec.md to understand all page, route, data schema, and template specifications
- Validate app.py for syntax correctness, runtime errors, and complete route coverage
- Validate all templates/*.html files for presence of correct element IDs, page titles, and data bindings
- Confirm handling of all pages, routes, and correct reading/writing of local text files as per design_spec.md
- Produce validation_report.md detailing all issues found and verification results

Validation Requirements:
1. **Backend Validation**:
   - Use validate_python_file tool on app.py for syntax and runtime checks
   - Verify all Flask routes defined in design_spec.md are implemented
   - Verify data reading/parsing from local data/*.txt files matches schema and usage correctly
   - Test basic runtime behavior of app.py using execute_python_code within constraints

2. **Frontend Validation**:
   - Check all required HTML element IDs and page titles exist exactly as specified in design_spec.md
   - Verify dynamic elements correctly use Jinja2 templating for variables and loops
   - Confirm navigation elements and buttons functionally correspond to routes

3. **Coverage Verification**:
   - Ensure each page defined in design_spec.md is implemented and accessible
   - Confirm form inputs, buttons, and interactive components handle data correctly

CRITICAL REQUIREMENTS:
- MUST use validate_python_file tool for Python file validation
- MUST use execute_python_code tool for runtime testing
- Write detailed validation_report.md with findings, issues, and recommendations using write_text_file
- Do not modify any files; only assess and report
- Focus solely on artifacts: app.py, templates/*.html, design_spec.md

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application maintenance and frontend templating.

Your goal is to apply corrections from validation_report.md to finalize app.py and templates/*.html ensuring full compliance with design_spec.md and all validation criteria.

Task Details:
- Read validation_report.md to identify all required fixes and issues
- Use design_spec.md as authoritative reference for required functionality and specifications
- Apply necessary code fixes to app.py to correct syntax, runtime, and route handling issues
- Update templates/*.html files to correct element IDs, page titles, data bindings, and navigation as specified
- Ensure no regressions or loss of functionality occur in the final deliverables

Implementation Requirements:
1. **Backend Corrections**:
   - Modify code preserving original design and data schemas
   - Fix all reported errors and omissions from validation_report.md

2. **Frontend Corrections**:
   - Correct all specified element ID and page title mismatches
   - Fix Jinja2 syntax for dynamic content and navigation as needed
   - Ensure accessible and consistent UI elements per design_spec.md

3. **Final Validation**:
   - Confirm corrections align with design_spec.md requirements
   - Maintain clean, readable, and consistent code style

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Strictly follow specifications in design_spec.md and corrections in validation_report.md
- Deliver final validated source code and templates ready for deployment
- Do not introduce features beyond original scope
- Preserve data schema and file naming conventions

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'QualityAssurer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md correctly and comprehensively captures all pages, elements, data formats, and navigation before architecture design.""", [{'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'ImplementationEngineer': [
        ("IntegrationEngineer", """Check app_draft.py and templates_draft/*.html to ensure full coverage of design_spec.md including precise element IDs, routing, and local data file handling before final integration.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'QualityAssurer': [
        ("SequentialFixer", """Confirm validation_report.md accurately identifies all issues and that corrections for final app.py and templates/*.html address these while retaining full feature coverage.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify that final app.py and templates/*.html fully implement all requirements from validation_report.md and ultimately the original user task.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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

    # Sequential Flow
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Extract and document all user requirements from user_task_description. Save detailed requirements_analysis.md.")
    # Read requirements_analysis.md content for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Step 2: WebArchitect reads requirements_analysis.md and produces design_spec.md
    await execute(WebArchitect,
                  f"Read the following requirements_analysis.md content carefully and produce design_spec.md with detailed page definitions, element IDs, navigation mappings, data file schemas, and programmatic constraints.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    ImplementationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationEngineer",
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
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Execute ImplementationEngineer to create app_draft.py and templates_draft/*.html from design_spec.md
    await execute(ImplementationEngineer,
                  "Create app_draft.py implementing Flask backend routes and request handling per design_spec.md. "
                  "Also create complete templates_draft/*.html for all 9 pages with exact element IDs and UI components. "
                  "Save outputs to app_draft.py and templates_draft/*.html.")

    # Read draft files to inject content for IntegrationEngineer
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        import os
        templates_draft_files = [f for f in os.listdir("templates_draft") if f.endswith(".html")]
        templates_draft_content = ""
        for fname in templates_draft_files:
            try:
                templates_draft_content += f"=== {fname} ===\n" + open(f"templates_draft/{fname}").read() + "\n\n"
            except:
                pass
    except:
        pass

    # Execute IntegrationEngineer to produce final app.py and templates/*.html from drafts and design_spec.md
    await execute(IntegrationEngineer,
                  f"Use app_draft.py and templates_draft/*.html below along with full design_spec.md to produce finalized app.py "
                  f"and templates/*.html with exact routing, functional requirements, and data file handling.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"=== templates_draft ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Declare agents
    QualityAssurer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="QualityAssurer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=45
    )
    SequentialFixer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Read input artifacts content for QualityAssurer
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except Exception:
        pass
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    # Note: For templates/*.html, aggregate contents of all template files into a single string
    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_agg = []
        for tf in template_files:
            try:
                content = open(tf).read()
                templates_agg.append(f"=== {tf} ===\n{content}\n")
            except Exception:
                continue
        templates_content = "\n".join(templates_agg)
    except Exception:
        templates_content = ""

    # Execute QualityAssurer with core instructions
    await execute(QualityAssurer,
                  "Validate CarRental Flask backend app.py and frontend templates/*.html against design_spec.md. "
                  "Use validate_python_file tool on app.py for syntax/runtime checking and execute_python_code tool for runtime tests. "
                  "Check all Flask routes, element IDs, page titles, data bindings, navigation correctness, and coverage. "
                  "Write detailed validation_report.md describing all issues and verification results. "
                  "Input contents:\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n"
                  f"=== app.py ===\n{app_py_content}\n"
                  f"=== templates/*.html ===\n{templates_content}")

    # After QualityAssurer completes, SequentialFixer runs to fix issues
    # Read validation_report.md content for SequentialFixer injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(SequentialFixer,
                  "Apply all necessary fixes to finalize app.py and templates/*.html ensuring compliance with design_spec.md and all validation criteria. "
                  "Read validation_report.md below and design_spec.md, app.py, templates/*.html to identify and address all reported issues. "
                  "Output final corrected app.py and templates/*.html files.\n"
                  f"=== validation_report.md ===\n{validation_report_content}\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n"
                  f"=== app.py ===\n{app_py_content}\n"
                  f"=== templates/*.html ===\n{templates_content}")
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
