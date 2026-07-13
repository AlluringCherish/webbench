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
# 20260714_001750_232629/main_20260714_001750_232629.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create and refine the detailed design specification for the TravelPlanner web application, producing 'design_spec.md' and gated 'design_feedback.md'.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator drafts and revises the comprehensive design_spec.md including all pages, UI element IDs, data storage format, and user navigation flows. \"\n        \"DesignCritic reviews design_spec.md for completeness, consistency, and adherence to requirements, producing design_feedback.md starting with [APPROVED] or NEED_MODIFY.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to develop and iteratively refine the complete design specification for the TravelPlanner web application, producing a full design_spec.md document.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand overall requirements\n- On first iteration, create comprehensive design_spec.md covering all pages, UI element IDs, local data storage formats, and navigation flows\n- On feedback starting with NEED_MODIFY, apply all provided changes fully and overwrite design_spec.md\n- When feedback starts with [APPROVED], preserve the approved design specification and stop iteration\n- Read current design_spec.md and design_feedback.md from CONTEXT for iterative refinement\n- Output the complete design_spec.md after each iteration using write_text_file\n\n**Section 1: Page Specifications**\n- Define each of the ten pages with title, overview, and container element IDs\n- Specify all essential UI elements with exact IDs and types as per user requirements\n- Include navigation flow and button linkage descriptions between pages\n\n**Section 2: Data Storage Formats**\n- Specify exact text file names and locations under a data directory\n- For each data file, define format schema including field names, delimiters, and example rows\n- Include all data described in user requirements: destinations, itineraries, hotels, flights, packages, trips, bookings\n\n**Section 3: Consistency and Completeness**\n- Ensure all UI elements and data fields exactly match requirements document\n- Maintain uniform ID and naming conventions across page and data specs\n- Avoid adding requirements not stated by user_task_description\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save the full design_spec.md file each iteration\n- Limit to at most two iterations and cease on receiving [APPROVED] feedback\n- Provide complete, clear, and consistent design specification for backend and frontend implementation\n- Do not include feedback status marker inside design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application design specifications for TravelPlanner.\n\nYour goal is to evaluate the submitted design_spec.md for completeness, correctness, and adherence to the user requirements, providing gated feedback labeled [APPROVED] or NEED_MODIFY.\n\nTask Details:\n- Read user_task_description and the design_spec.md from CONTEXT\n- Review that all ten pages are fully specified with correct titles, container IDs, and UI element IDs/types matching user requirements\n- Verify that all required data files are specified with correct formats, field orders, delimiter, and representative examples\n- Confirm that navigation flow and page linkage details are clearly described\n- Check naming consistency of IDs, fields and data files\n- Provide feedback beginning exactly with [APPROVED] when design_spec.md meets all criteria\n- Provide feedback beginning exactly with NEED_MODIFY followed by detailed correction points if gaps or inconsistencies exist\n- Write complete feedback using write_text_file\n\nReview Requirements:\n1. Completeness of each page’s specification with all listed UI elements and IDs\n2. Accuracy and completeness of each data file format and example content\n3. Consistency of naming conventions and adherence to user specifications\n4. No introduction of new features or departures from the user requirements document\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md must be exactly [APPROVED] or NEED_MODIFY\n- No preceding whitespace, headings, or extraneous characters before marker\n- Use write_text_file tool to save the complete feedback\n- Limit to at most two review iterations and stop immediately upon [APPROVED]\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify completeness of page designs, all element IDs, data formats, and ensure no missing features per user requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Iteratively develop and refine the TravelPlanner Python Flask web application including app.py and templates/*.html, producing code feedback for gating.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator writes and revises the Flask app.py and HTML templates based on design_spec.md and code_feedback.md. \"\n        \"CodeCritic reviews the implementation for functional correctness, alignment with design, route conformance, element IDs, and performance, producing code_feedback.md starting with [APPROVED] or NEED_MODIFY.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in full-stack web application development with local file data management.\n\nYour goal is to implement and iteratively refine the complete TravelPlanner Flask application, including app.py and HTML templates, guided by the design specification and critic feedback.\n\nTask Details:\n- Read design_spec.md and previous app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration, create complete app.py and all templates/*.html according to design_spec.md\n- On subsequent iterations where code_feedback.md begins with NEED_MODIFY, apply every suggested modification and rewrite the full app.py and templates/*.html\n- When code_feedback.md begins with [APPROVED], preserve the approved implementation unchanged\n\n**Section 1: Flask Application Implementation**\n- Implement all routes corresponding to pages specified in design_spec.md with correct route paths and HTTP methods\n- Implement handlers that read and write data using local text files as described in design_spec.md\n- Ensure all element IDs in templates correspond exactly to specification for front-end integration\n- Provide navigation links enabling user flow starting at the Dashboard page\n\n**Section 2: HTML Templates Implementation**\n- Create templates for all pages described in design_spec.md with fully specified page structure and elements\n- Include all specified element IDs for buttons, inputs, div containers, tables, etc.\n- Templates must be valid HTML with Flask Jinja2 syntax as needed for dynamic content insertion\n\n**Section 3: Integration and Data Handling**\n- Manage data inputs and outputs to/from local text files exactly as per design_spec.md field definitions and formats\n- Implement data conversions and date handling as required for itinerary and bookings\n- Maintain consistency between route logic and template data context\n\nCRITICAL REQUIREMENTS:\n- Run at most two iterations of generation and review\n- Always write complete and updated app.py and templates/*.html files on modification requests\n- Use the write_text_file tool to output updated app.py and template files\n- Focus implementation strictly on specified input/output artifacts from design_spec.md and feedback files\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer and Code Reviewer specialized in Python Flask applications with local text file data storage.\n\nYour goal is to review the implementation of app.py and templates/*.html against design_spec.md and provide gated feedback to ensure functional correctness and specification compliance.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate app.py syntax and runtime correctness using validate_python_file tool\n- Check routes implemented match design_spec.md with correct URLs and HTTP methods\n- Verify presence and correctness of all specified element IDs in HTML templates\n- Confirm compliance with all design_spec.md requirements for data handling, page flow, and UI elements\n- Produce code_feedback.md beginning with exactly [APPROVED] if implementation is complete and correct, otherwise NEED_MODIFY followed by detailed correction instructions\n\nReview Criteria:\n1. All required pages and routes are implemented and accessible starting from the Dashboard\n2. All specified element IDs appear exactly and functionally in templates\n3. Data input/output follows the specified local text file formats and field structures\n4. app.py has no syntax or runtime errors as validated by the tool\n5. Adherence to design_spec.md with no missing features or deviations\n\nCRITICAL REQUIREMENTS:\n- Feedback must start with the exact prefixes [APPROVED] or NEED_MODIFY in code_feedback.md\n- Use write_text_file to write the feedback file atomically\n- Use validate_python_file tool to verify app.py correctness\n- Run at most two critique iterations and stop upon receiving [APPROVED]\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Ensure all required pages, routes, element IDs, local text file data handling, and design conformance are correctly implemented and error-free.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to develop and iteratively refine the complete design specification for the TravelPlanner web application, producing a full design_spec.md document.

Task Details:
- Read user_task_description from CONTEXT to understand overall requirements
- On first iteration, create comprehensive design_spec.md covering all pages, UI element IDs, local data storage formats, and navigation flows
- On feedback starting with NEED_MODIFY, apply all provided changes fully and overwrite design_spec.md
- When feedback starts with [APPROVED], preserve the approved design specification and stop iteration
- Read current design_spec.md and design_feedback.md from CONTEXT for iterative refinement
- Output the complete design_spec.md after each iteration using write_text_file

**Section 1: Page Specifications**
- Define each of the ten pages with title, overview, and container element IDs
- Specify all essential UI elements with exact IDs and types as per user requirements
- Include navigation flow and button linkage descriptions between pages

**Section 2: Data Storage Formats**
- Specify exact text file names and locations under a data directory
- For each data file, define format schema including field names, delimiters, and example rows
- Include all data described in user requirements: destinations, itineraries, hotels, flights, packages, trips, bookings

**Section 3: Consistency and Completeness**
- Ensure all UI elements and data fields exactly match requirements document
- Maintain uniform ID and naming conventions across page and data specs
- Avoid adding requirements not stated by user_task_description

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save the full design_spec.md file each iteration
- Limit to at most two iterations and cease on receiving [APPROVED] feedback
- Provide complete, clear, and consistent design specification for backend and frontend implementation
- Do not include feedback status marker inside design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application design specifications for TravelPlanner.

Your goal is to evaluate the submitted design_spec.md for completeness, correctness, and adherence to the user requirements, providing gated feedback labeled [APPROVED] or NEED_MODIFY.

Task Details:
- Read user_task_description and the design_spec.md from CONTEXT
- Review that all ten pages are fully specified with correct titles, container IDs, and UI element IDs/types matching user requirements
- Verify that all required data files are specified with correct formats, field orders, delimiter, and representative examples
- Confirm that navigation flow and page linkage details are clearly described
- Check naming consistency of IDs, fields and data files
- Provide feedback beginning exactly with [APPROVED] when design_spec.md meets all criteria
- Provide feedback beginning exactly with NEED_MODIFY followed by detailed correction points if gaps or inconsistencies exist
- Write complete feedback using write_text_file

Review Requirements:
1. Completeness of each page’s specification with all listed UI elements and IDs
2. Accuracy and completeness of each data file format and example content
3. Consistency of naming conventions and adherence to user specifications
4. No introduction of new features or departures from the user requirements document

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md must be exactly [APPROVED] or NEED_MODIFY
- No preceding whitespace, headings, or extraneous characters before marker
- Use write_text_file tool to save the complete feedback
- Limit to at most two review iterations and stop immediately upon [APPROVED]

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in full-stack web application development with local file data management.

Your goal is to implement and iteratively refine the complete TravelPlanner Flask application, including app.py and HTML templates, guided by the design specification and critic feedback.

Task Details:
- Read design_spec.md and previous app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, create complete app.py and all templates/*.html according to design_spec.md
- On subsequent iterations where code_feedback.md begins with NEED_MODIFY, apply every suggested modification and rewrite the full app.py and templates/*.html
- When code_feedback.md begins with [APPROVED], preserve the approved implementation unchanged

**Section 1: Flask Application Implementation**
- Implement all routes corresponding to pages specified in design_spec.md with correct route paths and HTTP methods
- Implement handlers that read and write data using local text files as described in design_spec.md
- Ensure all element IDs in templates correspond exactly to specification for front-end integration
- Provide navigation links enabling user flow starting at the Dashboard page

**Section 2: HTML Templates Implementation**
- Create templates for all pages described in design_spec.md with fully specified page structure and elements
- Include all specified element IDs for buttons, inputs, div containers, tables, etc.
- Templates must be valid HTML with Flask Jinja2 syntax as needed for dynamic content insertion

**Section 3: Integration and Data Handling**
- Manage data inputs and outputs to/from local text files exactly as per design_spec.md field definitions and formats
- Implement data conversions and date handling as required for itinerary and bookings
- Maintain consistency between route logic and template data context

CRITICAL REQUIREMENTS:
- Run at most two iterations of generation and review
- Always write complete and updated app.py and templates/*.html files on modification requests
- Use the write_text_file tool to output updated app.py and template files
- Focus implementation strictly on specified input/output artifacts from design_spec.md and feedback files

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer and Code Reviewer specialized in Python Flask applications with local text file data storage.

Your goal is to review the implementation of app.py and templates/*.html against design_spec.md and provide gated feedback to ensure functional correctness and specification compliance.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate app.py syntax and runtime correctness using validate_python_file tool
- Check routes implemented match design_spec.md with correct URLs and HTTP methods
- Verify presence and correctness of all specified element IDs in HTML templates
- Confirm compliance with all design_spec.md requirements for data handling, page flow, and UI elements
- Produce code_feedback.md beginning with exactly [APPROVED] if implementation is complete and correct, otherwise NEED_MODIFY followed by detailed correction instructions

Review Criteria:
1. All required pages and routes are implemented and accessible starting from the Dashboard
2. All specified element IDs appear exactly and functionally in templates
3. Data input/output follows the specified local text file formats and field structures
4. app.py has no syntax or runtime errors as validated by the tool
5. Adherence to design_spec.md with no missing features or deviations

CRITICAL REQUIREMENTS:
- Feedback must start with the exact prefixes [APPROVED] or NEED_MODIFY in code_feedback.md
- Use write_text_file to write the feedback file atomically
- Use validate_python_file tool to verify app.py correctness
- Run at most two critique iterations and stop upon receiving [APPROVED]

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Verify completeness of page designs, all element IDs, data formats, and ensure no missing features per user requirements.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Ensure all required pages, routes, element IDs, local text file data handling, and design conformance are correctly implemented and error-free.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignGenerator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
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

        await execute(
            DesignGenerator,
            "Develop or revise the complete design_spec.md for TravelPlanner web application.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md against user_task_description. "
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
        chaos_controller=chaos_controller,
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=30
    )
    CodeCritic = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
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
            "Create or revise the complete app.py and templates/*.html according to design_spec.md and code_feedback.md.\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{feedback_content}"
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
            "Review the latest app.py and templates/*.html against design_spec.md.\n"
            "Validate syntax and runtime correctness using validate_python_file tool.\n"
            "Check routes, element IDs, data handling, page flow, and UI elements.\n"
            "Produce code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY with detailed instructions.\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest Templates ===\n{templates_content}"
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
