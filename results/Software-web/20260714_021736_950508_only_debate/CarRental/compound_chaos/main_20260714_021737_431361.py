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
# 20260714_021737_431361/main_20260714_021737_431361.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Debate adaptive Web design contract for CarRental app with specified pages, elements, routes, and local text file data format; produce design_spec.md\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = \"DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md in round 1; revise including peer outputs in round 2; DesignJudge adjudicates and merges final design_spec.md.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignDebaterA\",\n            \"prompt\": \"\"\"You are a Software System Architect specializing in Python Flask web application design specifications.\n\nYour goal is to create a comprehensive and complete Flask adaptive web design specification for the CarRental app through exactly two total debate rounds.\n\nTask Details:\n- Read user_task_description on every round to understand user requirements\n- In round 1, independently write the complete design_debate_a.md including Flask routes, HTML pages, element IDs, and local text file data formats\n- In round 2, revise design_debate_a.md based on your original draft and DesignDebaterB's design_debate_b.md, respecting user requirements and authoritative adaptive Web contract rules\n- Produce a full design specification covering all 9 pages with exact element IDs, routes, HTTP methods, templates, local text files, and required data schemas\n- Overwrite design_debate_a.md on every round with your complete design\n\n**Section 1: Web Routes and Navigation**\n- Define Flask routes including path and HTTP methods, ensuring `/` renders Dashboard page as mandatory entry\n- Match navigation targets and form actions exactly as per adaptive Web contract\n- Include context variables passed to templates with exact names and data types\n\n**Section 2: HTML Page and Element Specifications**\n- Specify page templates for each of the 9 pages with precise page titles and container element IDs\n- Include all listed page elements with exact IDs for controls, displays, buttons, forms, and dynamic elements such as button IDs with parameters\n- Preserve element types such as div, button, input, dropdown, table, radio, checkbox, textarea exactly\n\n**Section 3: Local Text Data File Format and Schema**\n- Specify data storage files with exact file names under `data/` folder (e.g., `vehicles.txt`)\n- Enumerate field order, field separator '|', field names, types, and example data rows unaltered\n- Include all 6 data files: vehicles, customers, locations, rentals, insurance, reservations\n\n**Section 4: Consistency Requirements**\n- Ensure all routes, methods, templates, and element IDs align with page specifications and local data usage\n- Preserve the adaptive Web contract rule: `/` entry point must render or redirect to Dashboard page\n- Maintain correct naming conventions for dynamic element IDs such as `view-details-button-{vehicle_id}`\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file to save design_debate_a.md\n- Produce complete, implementation-ready specification covering UI, routing, and data schema\n- Follow exactly two total debate rounds protocol: independent round 1, peer-informed round 2\n- Focus exclusively on declared input and output artifacts; do not add refinement feedback markings\n\nOutput: design_debate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignDebaterB\",\n            \"prompt\": \"\"\"You are a Software System Architect specializing in Python Flask web application design specifications.\n\nYour goal is to produce a full and compliant Flask adaptive web design specification for the CarRental app across two total debate rounds.\n\nTask Details:\n- Read user_task_description on each debate round to understand scope and requirements\n- In independent round 1, create a self-contained and complete design_debate_b.md with all required pages, elements, routes, templates, and data file schema\n- In round 2, revise design_debate_b.md by carefully integrating insights from DesignDebaterA's design_debate_a.md without adding outside requirements\n- Deliver an adaptive Web contract compliant specification that preserves precise element IDs, HTTP methods, route paths, and local text data formats\n- Overwrite design_debate_b.md completely on every round\n\n**Section 1: Flask Routing and Template Context**\n- Clearly define routes for all 9 pages with HTTP GET/POST methods exactly as per adaptive Web standard\n- Ensure `/` renders or redirects to Dashboard page as default entry point with no authentication\n- Provide template names and context variable dictionaries fully aligned with page design specs\n\n**Section 2: HTML Template and Dynamic Element IDs**\n- Document exact page titles, container div IDs, and form element IDs for controls including dynamically named IDs with parameters\n- Include controls like buttons, dropdowns, inputs, radios, tables, checkboxes, and textareas with exact ID and type matches\n\n**Section 3: Data File Specifications**\n- Fully specify each local text file as per user data format: name, field schema/order, field separator '|', example data rows verbatim\n- Cover all data files: vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, and reservations.txt\n\n**Section 4: Cross-Artifact Consistency**\n- Confirm all specifications respect the authoritative adaptive Web contract regarding route access, POST behaviors, persisted state, and navigation\n- Maintain exact naming conventions especially for dynamic element ID suffixed with database keys\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save design_debate_b.md\n- Deliver a complete, standalone adaptive Web compliant design spec without extraneous commentary\n- Follow exact 2-rounds debate pattern: initial draft and peer-informed revision\n- Only produce declared outputs; avoid any feedback or refinement commentary\n\nOutput: design_debate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignJudge\",\n            \"prompt\": \"\"\"You are a Senior Software System Architect tasked with adjudicating two Python Flask web app design specifications for CarRental.\n\nYour goal is to synthesize a final canonical design_spec.md after round 2 debate, fully compliant with the adaptive Web design contract and user requirements.\n\nTask Details:\n- Carefully read user_task_description, final design_debate_a.md, and design_debate_b.md\n- Compare both final design drafts requirement by requirement, focusing on exact Flask routes, HTML element IDs, templates, and data file schemas\n- Resolve any conflicts using authoritative adaptive Web contract rules and user requirements\n- Produce one comprehensive canonical design_spec.md that covers:\n  - The 9 pages with all specified element IDs and page titles\n  - Flask routing details including methods, paths, actions, and context variables\n  - Local text file data formats exactly as declared with field separator '|', field orders, and examples\n\n**Section 1: Web Application Route and Navigation Specification**\n- Confirm `/` route serves Dashboard or redirects thereto without authentication\n- Include all routes to pages with HTTP methods and template names\n- Ensure navigation buttons and form methods/actions align strictly with route specs\n\n**Section 2: HTML Templates and UI Element IDs**\n- Verify all 9 pages' container div IDs and constituent element IDs match user spec\n- Include dynamic IDs for buttons/forms that incorporate IDs (e.g., `view-details-button-{vehicle_id}`)\n- Maintain exact control types as per user page design\n\n**Section 3: Local Text File Schemas**\n- Finalize data file schema for all 6 text files per user format, including example data rows verbatim\n- Verify field separator is '|' and field orders/types are consistent\n\n**Section 4: Compliance and Consistency**\n- Ensure all routing, templates, element IDs, and file formats comply with adaptive Web contract and user requirements\n- Confirm no extra tasks or unsupported additions are introduced\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save design_spec.md\n- Deliver a clean, authoritative design specification fully ready for implementation\n- Approve inputs from debaters when readable, relevant, and consistent with contract, without requiring completeness\n- Do not require minor polish or reject for omissions if broadly usable\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignDebaterA\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Approve when design_debate_a.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignDebaterB\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Approve when design_debate_b.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignJudge\",\n            \"reviewer_agent\": \"DesignDebaterA\",\n            \"review_criteria\": \"Approve when design_spec.md exists, is non-empty, readable, broadly usable, and aligns with user requirements; allow minor omissions or polish issues.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Debate full implementation of CarRental Flask app with templates for all pages, strict local text file data handling per design_spec.md; produce app.py and templates/*.html\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = \"ImplementationDebaterA and ImplementationDebaterB independently create complete app.py and templates candidates in round 1; revise from peer candidates in round 2; ImplementationJudge integrates and finalizes canonical app.py and templates/*.html.\",\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDebaterA\",\n            \"prompt\": \"\"\"You are a Flask Backend Developer skilled in building Python web applications with Jinja2 templating and file-based data management.\n\nYour goal is to implement the complete CarRental Flask application and its Jinja2 templates for all nine pages, strictly following design_spec.md. Deliver fully functional app_debate_a.py and corresponding templates_debate_a/*.html files.\n\nTask Details:\n- Read design_spec.md entirely for all route, page, and data specifications\n- Read previous app_debate_a.py and templates_debate_a/*.html in all rounds\n- Read peer candidate app_debate_b.py and templates_debate_b/*.html in round 2\n- Write complete app_debate_a.py and templates_debate_a/*.html each round\n\n**Section 1: Flask Application Implementation**\n- Implement all Flask routes exactly as declared: paths, HTTP methods, template rendering\n- Ensure the root route '/' renders or redirects to the Dashboard page per Web contract\n- Implement all page handlers matching the route, element IDs, and forms specified\n- Use local text files in 'data' directory for data persistence, consistent with design_spec.md formats\n- Implement file reading/writing with proper locking or safe concurrent patterns\n\n**Section 2: Jinja2 Template Implementation**\n- Create templates for all 9 pages with exact filenames per debate artifacts\n- Preserve all element IDs, including dynamic IDs like view-details-button-{vehicle_id}\n- Implement forms with exact field names, methods, and actions as specified\n- Implement navigation elements as per design_spec.md, ensuring functional buttons and links\n\n**Section 3: Data Persistence and Local Text File Handling**\n- Read/write data from/to correct local text files under 'data' directory\n- Maintain exact data field order and format as specified by design_spec.md\n- Handle all CRUD operations as required by page functionality via flat file access\n- Preserve data integrity, avoid data corruption or loss on concurrent access\n\nCRITICAL SUCCESS CRITERIA:\n- MUST implement all 9 pages with exact routes, methods, element IDs, and form specs\n- MUST implement local text file backend strictly per design_spec.md data formats\n- MUST expose root route '/' as entry point rendering or redirecting to Dashboard page\n- MUST execute exactly two debate rounds: independent round 1 and peer-informed round 2\n- MUST use write_text_file tool to save app_debate_a.py and templates_debate_a/*.html\n- Output only app_debate_a.py and templates_debate_a/*.html; no refinement markers or ZIP files\n\nOutput: app_debate_a.py, templates_debate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDebaterB\",\n            \"prompt\": \"\"\"You are a Flask Backend Developer skilled in building Python web applications with Jinja2 templating and file-based data management.\n\nYour goal is to implement the complete CarRental Flask application and its Jinja2 templates for all nine pages, strictly following design_spec.md. Deliver fully functional app_debate_b.py and corresponding templates_debate_b/*.html files.\n\nTask Details:\n- Read design_spec.md entirely for all route, page, and data specifications\n- Read previous app_debate_b.py and templates_debate_b/*.html in all rounds\n- Read peer candidate app_debate_a.py and templates_debate_a/*.html in round 2\n- Write complete app_debate_b.py and templates_debate_b/*.html each round\n\n**Section 1: Flask Application Implementation**\n- Implement all Flask routes exactly as declared: paths, HTTP methods, template rendering\n- Ensure the root route '/' renders or redirects to the Dashboard page per Web contract\n- Implement all page handlers matching the route, element IDs, and forms specified\n- Use local text files in 'data' directory for data persistence, consistent with design_spec.md formats\n- Implement file reading/writing with proper locking or safe concurrent patterns\n\n**Section 2: Jinja2 Template Implementation**\n- Create templates for all 9 pages with exact filenames per debate artifacts\n- Preserve all element IDs, including dynamic IDs like view-details-button-{vehicle_id}\n- Implement forms with exact field names, methods, and actions as specified\n- Implement navigation elements as per design_spec.md, ensuring functional buttons and links\n\n**Section 3: Data Persistence and Local Text File Handling**\n- Read/write data from/to correct local text files under 'data' directory\n- Maintain exact data field order and format as specified by design_spec.md\n- Handle all CRUD operations as required by page functionality via flat file access\n- Preserve data integrity, avoid data corruption or loss on concurrent access\n\nCRITICAL SUCCESS CRITERIA:\n- MUST implement all 9 pages with exact routes, methods, element IDs, and form specs\n- MUST implement local text file backend strictly per design_spec.md data formats\n- MUST expose root route '/' as entry point rendering or redirecting to Dashboard page\n- MUST execute exactly two debate rounds: independent round 1 and peer-informed round 2\n- MUST use write_text_file tool to save app_debate_b.py and templates_debate_b/*.html\n- Output only app_debate_b.py and templates_debate_b/*.html; no refinement markers or ZIP files\n\nOutput: app_debate_b.py, templates_debate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationJudge\",\n            \"prompt\": \"\"\"You are a Senior Flask Backend Developer and Web Application Integrator specializing in Flask apps with local text file data backends and Jinja2 templates.\n\nYour goal is to evaluate both ImplementationDebaterA and ImplementationDebaterB final candidates and integrate them into a single canonical app.py and templates/*.html set conforming fully to design_spec.md and the adaptive Web contract.\n\nTask Details:\n- Read design_spec.md, app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, and templates_debate_b/*.html\n- Compare both implementations for adherence to all routes including root '/', HTTP methods, form actions, and element IDs matching design_spec.md\n- Verify local text file handling matches all specified data filenames, formats, and correct field ordering\n- Identify missing elements, incomplete or inconsistent data handling, and route discrepancies\n- Select best implementations or combine strengths without adding new requirements\n\n**Evaluation Criteria:**\n- Completeness of all 9 pages implementation with required features and navigation\n- Correctness of Flask routing and HTTP method usage\n- Exact preservation of all element IDs, including dynamic ones\n- Adherence to local text file data formats and operations specified in design_spec.md\n- Preservation of adaptive Web contract entry point '/' properly rendering or redirecting Dashboard\n- Clean, maintainable, and consistent code and template structure\n\nCRITICAL SUCCESS CRITERIA:\n- MUST approve when canonical app.py and templates/*.html are non-empty, follow design_spec.md fully, and preserve adaptive Web contract\n- MUST NOT add new requirements, only integrate and repair defects based on inputs\n- MUST produce final artifacts with write_text_file tool without ZIP archives or refinements\n- MUST adhere strictly to endpoint contract: '/' present as main entry point rendering or redirecting to correct page\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDebaterA\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve when app_debate_a.py and templates_debate_a/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDebaterB\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve when app_debate_b.py and templates_debate_b/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationJudge\",\n            \"reviewer_agent\": \"ImplementationDebaterA\",\n            \"review_criteria\": \"Approve when canonical app.py and templates/*.html exist, are non-empty, readable, broadly usable, and preserve adaptive Web contract; minor omissions allowed.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignDebaterA": {
        "prompt": (
            """You are a Software System Architect specializing in Python Flask web application design specifications.

Your goal is to create a comprehensive and complete Flask adaptive web design specification for the CarRental app through exactly two total debate rounds.

Task Details:
- Read user_task_description on every round to understand user requirements
- In round 1, independently write the complete design_debate_a.md including Flask routes, HTML pages, element IDs, and local text file data formats
- In round 2, revise design_debate_a.md based on your original draft and DesignDebaterB's design_debate_b.md, respecting user requirements and authoritative adaptive Web contract rules
- Produce a full design specification covering all 9 pages with exact element IDs, routes, HTTP methods, templates, local text files, and required data schemas
- Overwrite design_debate_a.md on every round with your complete design

**Section 1: Web Routes and Navigation**
- Define Flask routes including path and HTTP methods, ensuring `/` renders Dashboard page as mandatory entry
- Match navigation targets and form actions exactly as per adaptive Web contract
- Include context variables passed to templates with exact names and data types

**Section 2: HTML Page and Element Specifications**
- Specify page templates for each of the 9 pages with precise page titles and container element IDs
- Include all listed page elements with exact IDs for controls, displays, buttons, forms, and dynamic elements such as button IDs with parameters
- Preserve element types such as div, button, input, dropdown, table, radio, checkbox, textarea exactly

**Section 3: Local Text Data File Format and Schema**
- Specify data storage files with exact file names under `data/` folder (e.g., `vehicles.txt`)
- Enumerate field order, field separator '|', field names, types, and example data rows unaltered
- Include all 6 data files: vehicles, customers, locations, rentals, insurance, reservations

**Section 4: Consistency Requirements**
- Ensure all routes, methods, templates, and element IDs align with page specifications and local data usage
- Preserve the adaptive Web contract rule: `/` entry point must render or redirect to Dashboard page
- Maintain correct naming conventions for dynamic element IDs such as `view-details-button-{vehicle_id}`

CRITICAL SUCCESS CRITERIA:
- Use write_text_file to save design_debate_a.md
- Produce complete, implementation-ready specification covering UI, routing, and data schema
- Follow exactly two total debate rounds protocol: independent round 1, peer-informed round 2
- Focus exclusively on declared input and output artifacts; do not add refinement feedback markings

Output: design_debate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_a.md'}],

    },

    "DesignDebaterB": {
        "prompt": (
            """You are a Software System Architect specializing in Python Flask web application design specifications.

Your goal is to produce a full and compliant Flask adaptive web design specification for the CarRental app across two total debate rounds.

Task Details:
- Read user_task_description on each debate round to understand scope and requirements
- In independent round 1, create a self-contained and complete design_debate_b.md with all required pages, elements, routes, templates, and data file schema
- In round 2, revise design_debate_b.md by carefully integrating insights from DesignDebaterA's design_debate_a.md without adding outside requirements
- Deliver an adaptive Web contract compliant specification that preserves precise element IDs, HTTP methods, route paths, and local text data formats
- Overwrite design_debate_b.md completely on every round

**Section 1: Flask Routing and Template Context**
- Clearly define routes for all 9 pages with HTTP GET/POST methods exactly as per adaptive Web standard
- Ensure `/` renders or redirects to Dashboard page as default entry point with no authentication
- Provide template names and context variable dictionaries fully aligned with page design specs

**Section 2: HTML Template and Dynamic Element IDs**
- Document exact page titles, container div IDs, and form element IDs for controls including dynamically named IDs with parameters
- Include controls like buttons, dropdowns, inputs, radios, tables, checkboxes, and textareas with exact ID and type matches

**Section 3: Data File Specifications**
- Fully specify each local text file as per user data format: name, field schema/order, field separator '|', example data rows verbatim
- Cover all data files: vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, and reservations.txt

**Section 4: Cross-Artifact Consistency**
- Confirm all specifications respect the authoritative adaptive Web contract regarding route access, POST behaviors, persisted state, and navigation
- Maintain exact naming conventions especially for dynamic element ID suffixed with database keys

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save design_debate_b.md
- Deliver a complete, standalone adaptive Web compliant design spec without extraneous commentary
- Follow exact 2-rounds debate pattern: initial draft and peer-informed revision
- Only produce declared outputs; avoid any feedback or refinement commentary

Output: design_debate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_b.md'}],

    },

    "DesignJudge": {
        "prompt": (
            """You are a Senior Software System Architect tasked with adjudicating two Python Flask web app design specifications for CarRental.

Your goal is to synthesize a final canonical design_spec.md after round 2 debate, fully compliant with the adaptive Web design contract and user requirements.

Task Details:
- Carefully read user_task_description, final design_debate_a.md, and design_debate_b.md
- Compare both final design drafts requirement by requirement, focusing on exact Flask routes, HTML element IDs, templates, and data file schemas
- Resolve any conflicts using authoritative adaptive Web contract rules and user requirements
- Produce one comprehensive canonical design_spec.md that covers:
  - The 9 pages with all specified element IDs and page titles
  - Flask routing details including methods, paths, actions, and context variables
  - Local text file data formats exactly as declared with field separator '|', field orders, and examples

**Section 1: Web Application Route and Navigation Specification**
- Confirm `/` route serves Dashboard or redirects thereto without authentication
- Include all routes to pages with HTTP methods and template names
- Ensure navigation buttons and form methods/actions align strictly with route specs

**Section 2: HTML Templates and UI Element IDs**
- Verify all 9 pages' container div IDs and constituent element IDs match user spec
- Include dynamic IDs for buttons/forms that incorporate IDs (e.g., `view-details-button-{vehicle_id}`)
- Maintain exact control types as per user page design

**Section 3: Local Text File Schemas**
- Finalize data file schema for all 6 text files per user format, including example data rows verbatim
- Verify field separator is '|' and field orders/types are consistent

**Section 4: Compliance and Consistency**
- Ensure all routing, templates, element IDs, and file formats comply with adaptive Web contract and user requirements
- Confirm no extra tasks or unsupported additions are introduced

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save design_spec.md
- Deliver a clean, authoritative design specification fully ready for implementation
- Approve inputs from debaters when readable, relevant, and consistent with contract, without requiring completeness
- Do not require minor polish or reject for omissions if broadly usable

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDebaterA": {
        "prompt": (
            """You are a Flask Backend Developer skilled in building Python web applications with Jinja2 templating and file-based data management.

Your goal is to implement the complete CarRental Flask application and its Jinja2 templates for all nine pages, strictly following design_spec.md. Deliver fully functional app_debate_a.py and corresponding templates_debate_a/*.html files.

Task Details:
- Read design_spec.md entirely for all route, page, and data specifications
- Read previous app_debate_a.py and templates_debate_a/*.html in all rounds
- Read peer candidate app_debate_b.py and templates_debate_b/*.html in round 2
- Write complete app_debate_a.py and templates_debate_a/*.html each round

**Section 1: Flask Application Implementation**
- Implement all Flask routes exactly as declared: paths, HTTP methods, template rendering
- Ensure the root route '/' renders or redirects to the Dashboard page per Web contract
- Implement all page handlers matching the route, element IDs, and forms specified
- Use local text files in 'data' directory for data persistence, consistent with design_spec.md formats
- Implement file reading/writing with proper locking or safe concurrent patterns

**Section 2: Jinja2 Template Implementation**
- Create templates for all 9 pages with exact filenames per debate artifacts
- Preserve all element IDs, including dynamic IDs like view-details-button-{vehicle_id}
- Implement forms with exact field names, methods, and actions as specified
- Implement navigation elements as per design_spec.md, ensuring functional buttons and links

**Section 3: Data Persistence and Local Text File Handling**
- Read/write data from/to correct local text files under 'data' directory
- Maintain exact data field order and format as specified by design_spec.md
- Handle all CRUD operations as required by page functionality via flat file access
- Preserve data integrity, avoid data corruption or loss on concurrent access

CRITICAL SUCCESS CRITERIA:
- MUST implement all 9 pages with exact routes, methods, element IDs, and form specs
- MUST implement local text file backend strictly per design_spec.md data formats
- MUST expose root route '/' as entry point rendering or redirecting to Dashboard page
- MUST execute exactly two debate rounds: independent round 1 and peer-informed round 2
- MUST use write_text_file tool to save app_debate_a.py and templates_debate_a/*.html
- Output only app_debate_a.py and templates_debate_a/*.html; no refinement markers or ZIP files

Output: app_debate_a.py, templates_debate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}],

    },

    "ImplementationDebaterB": {
        "prompt": (
            """You are a Flask Backend Developer skilled in building Python web applications with Jinja2 templating and file-based data management.

Your goal is to implement the complete CarRental Flask application and its Jinja2 templates for all nine pages, strictly following design_spec.md. Deliver fully functional app_debate_b.py and corresponding templates_debate_b/*.html files.

Task Details:
- Read design_spec.md entirely for all route, page, and data specifications
- Read previous app_debate_b.py and templates_debate_b/*.html in all rounds
- Read peer candidate app_debate_a.py and templates_debate_a/*.html in round 2
- Write complete app_debate_b.py and templates_debate_b/*.html each round

**Section 1: Flask Application Implementation**
- Implement all Flask routes exactly as declared: paths, HTTP methods, template rendering
- Ensure the root route '/' renders or redirects to the Dashboard page per Web contract
- Implement all page handlers matching the route, element IDs, and forms specified
- Use local text files in 'data' directory for data persistence, consistent with design_spec.md formats
- Implement file reading/writing with proper locking or safe concurrent patterns

**Section 2: Jinja2 Template Implementation**
- Create templates for all 9 pages with exact filenames per debate artifacts
- Preserve all element IDs, including dynamic IDs like view-details-button-{vehicle_id}
- Implement forms with exact field names, methods, and actions as specified
- Implement navigation elements as per design_spec.md, ensuring functional buttons and links

**Section 3: Data Persistence and Local Text File Handling**
- Read/write data from/to correct local text files under 'data' directory
- Maintain exact data field order and format as specified by design_spec.md
- Handle all CRUD operations as required by page functionality via flat file access
- Preserve data integrity, avoid data corruption or loss on concurrent access

CRITICAL SUCCESS CRITERIA:
- MUST implement all 9 pages with exact routes, methods, element IDs, and form specs
- MUST implement local text file backend strictly per design_spec.md data formats
- MUST expose root route '/' as entry point rendering or redirecting to Dashboard page
- MUST execute exactly two debate rounds: independent round 1 and peer-informed round 2
- MUST use write_text_file tool to save app_debate_b.py and templates_debate_b/*.html
- Output only app_debate_b.py and templates_debate_b/*.html; no refinement markers or ZIP files

Output: app_debate_b.py, templates_debate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}],

    },

    "ImplementationJudge": {
        "prompt": (
            """You are a Senior Flask Backend Developer and Web Application Integrator specializing in Flask apps with local text file data backends and Jinja2 templates.

Your goal is to evaluate both ImplementationDebaterA and ImplementationDebaterB final candidates and integrate them into a single canonical app.py and templates/*.html set conforming fully to design_spec.md and the adaptive Web contract.

Task Details:
- Read design_spec.md, app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, and templates_debate_b/*.html
- Compare both implementations for adherence to all routes including root '/', HTTP methods, form actions, and element IDs matching design_spec.md
- Verify local text file handling matches all specified data filenames, formats, and correct field ordering
- Identify missing elements, incomplete or inconsistent data handling, and route discrepancies
- Select best implementations or combine strengths without adding new requirements

**Evaluation Criteria:**
- Completeness of all 9 pages implementation with required features and navigation
- Correctness of Flask routing and HTTP method usage
- Exact preservation of all element IDs, including dynamic ones
- Adherence to local text file data formats and operations specified in design_spec.md
- Preservation of adaptive Web contract entry point '/' properly rendering or redirecting Dashboard
- Clean, maintainable, and consistent code and template structure

CRITICAL SUCCESS CRITERIA:
- MUST approve when canonical app.py and templates/*.html are non-empty, follow design_spec.md fully, and preserve adaptive Web contract
- MUST NOT add new requirements, only integrate and repair defects based on inputs
- MUST produce final artifacts with write_text_file tool without ZIP archives or refinements
- MUST adhere strictly to endpoint contract: '/' present as main entry point rendering or redirecting to correct page

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignDebaterA': [
        ("DesignJudge", """Approve when design_debate_a.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.""", [{'type': 'text_file', 'name': 'design_debate_a.md'}])
    ],

    'DesignDebaterB': [
        ("DesignJudge", """Approve when design_debate_b.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.""", [{'type': 'text_file', 'name': 'design_debate_b.md'}])
    ],

    'DesignJudge': [
        ("DesignDebaterA", """Approve when design_spec.md exists, is non-empty, readable, broadly usable, and aligns with user requirements; allow minor omissions or polish issues.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDebaterA': [
        ("ImplementationJudge", """Approve when app_debate_a.py and templates_debate_a/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.""", [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}])
    ],

    'ImplementationDebaterB': [
        ("ImplementationJudge", """Approve when app_debate_b.py and templates_debate_b/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.""", [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}])
    ],

    'ImplementationJudge': [
        ("ImplementationDebaterA", """Approve when canonical app.py and templates/*.html exist, are non-empty, readable, broadly usable, and preserve adaptive Web contract; minor omissions allowed.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=360,
        failure_threshold=1,
        recovery_time=30
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        design_a = ""
        design_b = ""
        if round_num > 1:
            try:
                design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a = ""
            try:
                design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b = ""

        if round_num == 1:
            msg_a = "(No peer design yet; this is the initial independent draft round)"
            msg_b = "(No peer design yet; this is the initial independent draft round)"
        else:
            msg_a = f"Peer DesignDebaterB draft:\n{design_b}"
            msg_b = f"Peer DesignDebaterA draft:\n{design_a}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After rounds complete: Judge adjudicates final canonical design_spec.md
    try:
        final_design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_a = ""
    try:
        final_design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_b = ""

    await execute(
        DesignJudge,
        "Adjudicate final design drafts from DesignDebaterA and DesignDebaterB, synthesize authoritative design_spec.md fully compliant with adaptive Web contract and user requirements.\n\n"
        "=== DesignDebaterA's final draft ===\n" + final_design_a + "\n\n"
        "=== DesignDebaterB's final draft ===\n" + final_design_b
    )
# Phase1_End

# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    ImplementationDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        app_a_text = ""
        app_b_text = ""
        templates_a_text = ""
        templates_b_text = ""

        if round_num > 1:
            # Read previous own candidate app and templates
            try:
                app_a_text = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                app_a_text = ""
            try:
                app_b_text = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                app_b_text = ""
            for path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    templates_a_text += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
                except OSError:
                    pass
            for path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    templates_b_text += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
                except OSError:
                    pass

        if round_num == 1:
            msg_a = "Round 1 of 2: Independently create the complete app_debate_a.py and templates_debate_a/*.html based on design_spec.md."
            msg_b = "Round 1 of 2: Independently create the complete app_debate_b.py and templates_debate_b/*.html based on design_spec.md."
        else:
            msg_a = (
                "Round 2 of 2: Revise app_debate_a.py and templates_debate_a/*.html using the peer candidate below.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b_text + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + templates_b_text
            )
            msg_b = (
                "Round 2 of 2: Revise app_debate_b.py and templates_debate_b/*.html using the peer candidate below.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a_text + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + templates_a_text
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # Final: ImplementationJudge integrates and finalizes canonical app.py and templates/*.html
    app_a_text = ""
    app_b_text = ""
    templates_a_text = ""
    templates_b_text = ""
    try:
        app_a_text = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        app_a_text = ""
    try:
        app_b_text = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        app_b_text = ""
    for path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a_text += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
        except OSError:
            pass
    for path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b_text += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
        except OSError:
            pass

    await execute(
        ImplementationJudge,
        "Evaluate and integrate the two implementation candidates into canonical app.py and templates/*.html.\n\n"
        "=== app_debate_a.py ===\n" + app_a_text + "\n\n"
        "=== templates_debate_a/*.html ===\n" + templates_a_text + "\n\n"
        "=== app_debate_b.py ===\n" + app_b_text + "\n\n"
        "=== templates_debate_b/*.html ===\n" + templates_b_text,
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
