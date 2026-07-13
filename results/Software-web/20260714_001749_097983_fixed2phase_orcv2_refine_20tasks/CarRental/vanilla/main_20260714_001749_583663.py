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
# 20260714_001749_583663/main_20260714_001749_583663.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the design contract for the 'CarRental' Python Flask web application, producing 'design_spec.md' and gated 'design_feedback.md'.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\"DesignGenerator writes or revises 'design_spec.md' describing the architecture, page designs, element IDs, \"\n                                        \"data storage format, and user flows for the CarRental application based on 'user_task_description' and previous 'design_feedback.md'. \"\n                                        \"DesignCritic reviews 'design_spec.md' and writes 'design_feedback.md' beginning with [APPROVED] or NEED_MODIFY. \"\n                                        \"Loop runs for at most two iterations or until approval.\"),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python Flask web applications with expertise in UI/UX design and local text file data management.\n\nYour goal is to author and revise a thorough design specification document describing the architecture, page designs (including element IDs), navigation flows, and local data file schemas for the CarRental app, refining it from critic feedback within two iterations.\n\nTask Details:\n- Read 'user_task_description' from CONTEXT to understand user requirements.\n- Read previous 'design_spec.md' and 'design_feedback.md' if available to guide refinements.\n- Produce a comprehensive 'design_spec.md' covering all nine required pages, their element IDs, navigation flows starting from the Dashboard, and detailed data file format specifications.\n- Overwrite 'design_spec.md' fully when feedback begins with 'NEED_MODIFY'; preserve content when feedback begins with '[APPROVED]'.\n\n**Section 1: Page Designs and Element IDs**\n- Specify page titles, container div IDs, and unique element IDs for all UI components as per the user task.\n- Ensure all elements listed in the user specification are detailed, including dynamic IDs like 'view-details-button-{vehicle_id}'.\n\n**Section 2: Navigation and User Flows**\n- Define the navigation paths linking pages, starting from Dashboard as entry point.\n- Include button actions for page transitions consistent with user task.\n- No authentication flows; public access to all features.\n\n**Section 3: Data File Storage and Formats**\n- Specify exact data file names and detailed record field formats including field orders and separators.\n- Cover all data files specified: vehicles, customers, locations, rentals, insurance, reservations.\n- Provide example data rows consistent with user task.\n\nCRITICAL SUCCESS CRITERIA:\n- Execute at most two full Generator/Critic refinement iterations.\n- Implement all corrections indicated by NEED_MODIFY feedback fully and consistently.\n- Use only the 'write_text_file' tool to save 'design_spec.md'.\n- Do not add requirements beyond user_task_description.\n- Preserve explicit page design and data format details.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python Flask web applications and UI/UX compliance with textual data management.\n\nYour goal is to critically review 'design_spec.md' against the provided user task and ensure completeness, correctness, and conformance, producing gated, constructive feedback in 'design_feedback.md' within two iterations.\n\nTask Details:\n- Read 'user_task_description' and 'design_spec.md' from CONTEXT.\n- Evaluate that all specified pages, element IDs, navigation flows, and data file formats are covered as required.\n- Confirm no authentication is included and navigation starts from Dashboard as instructed.\n- Write feedback beginning exactly with '[APPROVED]' if complete and correct.\n- Write 'NEED_MODIFY' followed by concrete correction instructions if issues or omissions exist.\n\nReview Criteria:\n1. Each of the nine pages contains specified titles, container IDs, and all listed UI element IDs.\n2. Navigation structure matches user flow descriptions; Dashboard page is the start point.\n3. Data storage files and formats strictly adhere to the user-provided schemas and examples.\n4. No extraneous or missing features beyond user requests.\n5. Feedback is clear, precise, and action-guided for revision.\n\nCRITICAL REQUIREMENTS:\n- Start 'design_feedback.md' with exactly '[APPROVED]' or 'NEED_MODIFY' at byte 1.\n- Use only the 'write_text_file' tool to output feedback.\n- Do not add new requirements; only gate or propose corrections to existing content.\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": (\"Check that the design_spec.md covers all required pages with specified element IDs, data storage \"\n                                \"formats, no authentication, proper navigation flow starting from Dashboard, and consistency with user instructions.\"),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the complete Python Flask implementation with app.py and templates/*.html along with gated code_feedback.md for the CarRental web application.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\"AppGenerator writes or revises 'app.py' and all HTML template files 'templates/*.html' implementing the CarRental design_spec.md and handles all specified features and element IDs. \"\n                                        \"CodeCritic reviews output conformance to design_spec.md, checks functionality, data file integration, and writes 'code_feedback.md' starting with [APPROVED] or NEED_MODIFY. \"\n                                        \"Loop runs at most two iterations or until approval.\"),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in web applications using local text file data storage.\n\nYour goal is to implement and refine a complete Flask backend and frontend combining app.py and multiple HTML templates, according to design specifications and critic feedback.\n\nTask Details:\n- Read design_spec.md, existing app.py and templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration, create working app.py and all required HTML templates implementing all nine pages and specified element IDs\n- On receiving feedback starting with NEED_MODIFY, fully revise app.py and templates/*.html applying all corrections\n- Stop iteration at [APPROVED] feedback\n- Output complete app.py and all templates/*.html files\n\n**Implementation Requirements: Backend (app.py)**\n- Implement Flask routes and logic for all nine pages as per design_spec.md\n- Use local text files in 'data' directory for storing and accessing vehicles, customers, rentals, insurance, locations, and reservations\n- No user authentication; all features are publicly accessible starting at Dashboard page\n- Code should handle reading, writing, and updating data files reliably with proper parsing of pipe-delimited fields\n- Include navigation routes exactly matching design_spec.md page names and IDs\n\n**Implementation Requirements: Frontend (templates/*.html)**\n- Create one HTML template per page with correct filenames and structure\n- Ensure all specified element IDs appear exactly as defined for page containers, buttons, inputs, tables, and display sections\n- Implement consistent navigation and links from dashboard to all pages\n- Reflect dynamic content placeholders for vehicles, reservations, insurance plans, and rental history matching backend data\n\n**Development Workflow**\n- Use write_text_file tool to save each output file (app.py and all templates/*.html)\n- Maintain clean, readable Flask code with route decorators, view functions, template rendering, and data file helper functions\n- Apply all requested changes from code_feedback.md preserving the structure and naming conventions\n\nCRITICAL SUCCESS CRITERIA:\n- Complete implementation of all nine pages and their required element IDs\n- Local text files are read and updated correctly according to design_spec.md formats\n- Website launches starting at dashboard page without any authentication\n- Use write_text_file exclusively to export code and templates\n- On feedback NEED_MODIFY, fully overwrite previous artifacts with corrections\n- Stop after at most two iterations or on [APPROVED] feedback\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in code and web UI verification for Python Flask applications using local text file databases.\n\nYour goal is to critically evaluate app.py and HTML templates against design_spec.md and provide gated feedback at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Review completeness and correctness of implemented routes and pages as specified\n- Verify all required element IDs exist exactly as defined\n- Verify features functionally match specifications: navigation flows, data reading/writing, no authentication, and start at dashboard page\n- Validate proper access and update of local text files with correct formats\n- Provide feedback starting with [APPROVED] if requirements are met\n- Otherwise, start feedback with NEED_MODIFY followed by specific correction instructions\n- Stop review after [APPROVED] or maximum two iterations\n\nReview Criteria:\n1. Confirm all nine pages exist with all specified elements and IDs\n2. Confirm correct Flask route implementations supporting page navigation and user interactions\n3. Confirm local text data files are accessed and updated correctly matching design_spec.md format\n4. Confirm no use of authentication mechanisms and initial landing is dashboard page\n5. Confirm HTML templates follow design_spec.md element and ID requirements exactly\n6. Ensure feedback contains precise actionable modifications without adding new requirements\n\nCRITICAL REQUIREMENTS:\n- code_feedback.md must start exactly with [APPROVED] or NEED_MODIFY at byte-1\n- Use write_text_file tool to save complete feedback\n- Perform at most two review cycles, stopping on approval\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"code_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": (\"Verify that app.py and HTML templates completely implement all design_spec.md features, element IDs exactly as defined, \"\n                                \"local text data files are read and updated properly, the website starts at dashboard page, and no authentication is implemented.\"),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python Flask web applications with expertise in UI/UX design and local text file data management.

Your goal is to author and revise a thorough design specification document describing the architecture, page designs (including element IDs), navigation flows, and local data file schemas for the CarRental app, refining it from critic feedback within two iterations.

Task Details:
- Read 'user_task_description' from CONTEXT to understand user requirements.
- Read previous 'design_spec.md' and 'design_feedback.md' if available to guide refinements.
- Produce a comprehensive 'design_spec.md' covering all nine required pages, their element IDs, navigation flows starting from the Dashboard, and detailed data file format specifications.
- Overwrite 'design_spec.md' fully when feedback begins with 'NEED_MODIFY'; preserve content when feedback begins with '[APPROVED]'.

**Section 1: Page Designs and Element IDs**
- Specify page titles, container div IDs, and unique element IDs for all UI components as per the user task.
- Ensure all elements listed in the user specification are detailed, including dynamic IDs like 'view-details-button-{vehicle_id}'.

**Section 2: Navigation and User Flows**
- Define the navigation paths linking pages, starting from Dashboard as entry point.
- Include button actions for page transitions consistent with user task.
- No authentication flows; public access to all features.

**Section 3: Data File Storage and Formats**
- Specify exact data file names and detailed record field formats including field orders and separators.
- Cover all data files specified: vehicles, customers, locations, rentals, insurance, reservations.
- Provide example data rows consistent with user task.

CRITICAL SUCCESS CRITERIA:
- Execute at most two full Generator/Critic refinement iterations.
- Implement all corrections indicated by NEED_MODIFY feedback fully and consistently.
- Use only the 'write_text_file' tool to save 'design_spec.md'.
- Do not add requirements beyond user_task_description.
- Preserve explicit page design and data format details.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python Flask web applications and UI/UX compliance with textual data management.

Your goal is to critically review 'design_spec.md' against the provided user task and ensure completeness, correctness, and conformance, producing gated, constructive feedback in 'design_feedback.md' within two iterations.

Task Details:
- Read 'user_task_description' and 'design_spec.md' from CONTEXT.
- Evaluate that all specified pages, element IDs, navigation flows, and data file formats are covered as required.
- Confirm no authentication is included and navigation starts from Dashboard as instructed.
- Write feedback beginning exactly with '[APPROVED]' if complete and correct.
- Write 'NEED_MODIFY' followed by concrete correction instructions if issues or omissions exist.

Review Criteria:
1. Each of the nine pages contains specified titles, container IDs, and all listed UI element IDs.
2. Navigation structure matches user flow descriptions; Dashboard page is the start point.
3. Data storage files and formats strictly adhere to the user-provided schemas and examples.
4. No extraneous or missing features beyond user requests.
5. Feedback is clear, precise, and action-guided for revision.

CRITICAL REQUIREMENTS:
- Start 'design_feedback.md' with exactly '[APPROVED]' or 'NEED_MODIFY' at byte 1.
- Use only the 'write_text_file' tool to output feedback.
- Do not add new requirements; only gate or propose corrections to existing content.

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in web applications using local text file data storage.

Your goal is to implement and refine a complete Flask backend and frontend combining app.py and multiple HTML templates, according to design specifications and critic feedback.

Task Details:
- Read design_spec.md, existing app.py and templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, create working app.py and all required HTML templates implementing all nine pages and specified element IDs
- On receiving feedback starting with NEED_MODIFY, fully revise app.py and templates/*.html applying all corrections
- Stop iteration at [APPROVED] feedback
- Output complete app.py and all templates/*.html files

**Implementation Requirements: Backend (app.py)**
- Implement Flask routes and logic for all nine pages as per design_spec.md
- Use local text files in 'data' directory for storing and accessing vehicles, customers, rentals, insurance, locations, and reservations
- No user authentication; all features are publicly accessible starting at Dashboard page
- Code should handle reading, writing, and updating data files reliably with proper parsing of pipe-delimited fields
- Include navigation routes exactly matching design_spec.md page names and IDs

**Implementation Requirements: Frontend (templates/*.html)**
- Create one HTML template per page with correct filenames and structure
- Ensure all specified element IDs appear exactly as defined for page containers, buttons, inputs, tables, and display sections
- Implement consistent navigation and links from dashboard to all pages
- Reflect dynamic content placeholders for vehicles, reservations, insurance plans, and rental history matching backend data

**Development Workflow**
- Use write_text_file tool to save each output file (app.py and all templates/*.html)
- Maintain clean, readable Flask code with route decorators, view functions, template rendering, and data file helper functions
- Apply all requested changes from code_feedback.md preserving the structure and naming conventions

CRITICAL SUCCESS CRITERIA:
- Complete implementation of all nine pages and their required element IDs
- Local text files are read and updated correctly according to design_spec.md formats
- Website launches starting at dashboard page without any authentication
- Use write_text_file exclusively to export code and templates
- On feedback NEED_MODIFY, fully overwrite previous artifacts with corrections
- Stop after at most two iterations or on [APPROVED] feedback

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in code and web UI verification for Python Flask applications using local text file databases.

Your goal is to critically evaluate app.py and HTML templates against design_spec.md and provide gated feedback at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Review completeness and correctness of implemented routes and pages as specified
- Verify all required element IDs exist exactly as defined
- Verify features functionally match specifications: navigation flows, data reading/writing, no authentication, and start at dashboard page
- Validate proper access and update of local text files with correct formats
- Provide feedback starting with [APPROVED] if requirements are met
- Otherwise, start feedback with NEED_MODIFY followed by specific correction instructions
- Stop review after [APPROVED] or maximum two iterations

Review Criteria:
1. Confirm all nine pages exist with all specified elements and IDs
2. Confirm correct Flask route implementations supporting page navigation and user interactions
3. Confirm local text data files are accessed and updated correctly matching design_spec.md format
4. Confirm no use of authentication mechanisms and initial landing is dashboard page
5. Confirm HTML templates follow design_spec.md element and ID requirements exactly
6. Ensure feedback contains precise actionable modifications without adding new requirements

CRITICAL REQUIREMENTS:
- code_feedback.md must start exactly with [APPROVED] or NEED_MODIFY at byte-1
- Use write_text_file tool to save complete feedback
- Perform at most two review cycles, stopping on approval

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Check that the design_spec.md covers all required pages with specified element IDs, data storage "
                                "formats, no authentication, proper navigation flow starting from Dashboard, and consistency with user instructions.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Verify that app.py and HTML templates completely implement all design_spec.md features, element IDs exactly as defined, "
                                "local text data files are read and updated properly, the website starts at dashboard page, and no authentication is implemented.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )
    DesignCritic = build_resilient_agent(
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        current_design = ""
        feedback_content = ""
        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            pass
        if iteration > 0:
            try:
                feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                pass

        # Compose prompt message for DesignGenerator
        if iteration == 0:
            msg = (
                "Create a comprehensive and complete design_spec.md describing the CarRental application architecture, "
                "page designs including element IDs, navigation flows starting from the Dashboard page, and data storage formats. "
                "Use user_task_description from CONTEXT. This is the initial iteration."
            )
        else:
            if feedback_content.startswith("NEED_MODIFY"):
                msg = (
                    "Revise the entire design_spec.md fully based on the following previous design and critic feedback.\n\n"
                    f"=== Previous design_spec.md ===\n{current_design}\n\n"
                    f"=== DesignCritic Feedback ===\n{feedback_content}"
                )
            elif feedback_content.startswith("[APPROVED]"):
                # If approved, no need to change design; preserve content
                msg = (
                    "The design_spec.md was approved with no changes needed. Preserve its content fully."
                )
            else:
                # Unknown or missing feedback, treat as need to revise
                msg = (
                    "Revise design_spec.md based on previous design and any feedback available.\n\n"
                    f"=== Previous design_spec.md ===\n{current_design}\n\n"
                    f"=== DesignCritic Feedback ===\n{feedback_content}"
                )

        await execute(DesignGenerator, msg)

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Critically review the latest design_spec.md for completeness, correctness, and conformance with user_task_description. "
            "Write design_feedback.md starting exactly with [APPROVED] if no issues, or NEED_MODIFY followed by detailed corrections otherwise.\n\n"
            f"=== Latest design_spec.md ===\n{current_design}"
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )
    CodeCritic = build_resilient_agent(
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_content = ""
        templates_content = ""
        feedback_content = ""

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            pass

        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html implementing all nine CarRental pages with required element IDs.\n\n"
            "Design specification and current code are provided.\n"
            "Apply any corrections from the following feedback:\n"
            f"{feedback_content}\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current templates/*.html ===\n{templates_content}"
        )

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            app_content = ""

        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates/*.html against design_spec.md for completeness, correctness, and exact element IDs.\n"
            "Confirm all features function as specified, data files are updated properly, and the site starts at the dashboard page without authentication.\n"
            "Provide feedback beginning exactly with [APPROVED] if all requirements are met, else NEED_MODIFY with detailed corrections.\n\n"
            f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest templates/*.html ===\n{templates_content}"
        )

        try:
            feedback_content = open("code_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
            break
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
