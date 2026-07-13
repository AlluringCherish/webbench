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
# 20260714_001750_246627/main_20260714_001750_246627.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications for TravelPlanner and merge them into a coherent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect and FrontendDesignArchitect independently produce backend_design.md and frontend_design.md based on the user task. \"\n        \"DesignMerger consumes both specifications along with the original user task and produces the merged design_spec.md ensuring internal consistency.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Python Flask backend development and local text file data schema design.\n\nYour goal is to create a comprehensive backend design specification for the TravelPlanner application, suitable for independent implementation.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Independently produce backend_design.md\n- Specify all Python Flask routes with methods, endpoints, and template names\n- Define all local text file data schemas for all entities described in user_task_description, including field names, types, delimiters, and example rows\n- Do not reference or read frontend_design.md; work without sibling output artifacts\n\n**Section 1: Flask Backend Routes Specification**\n- List each route path and HTTP method mapped to a Flask function name\n- Specify the template filename each route renders and associated context variables\n- Include any redirect behavior and form submission handlers described in user requirements\n\n**Section 2: Local Text File Data Schemas**\n- For each text data file described (destinations.txt, itineraries.txt, hotels.txt, flights.txt, packages.txt, trips.txt, bookings.txt):\n  - Specify exact filename and relative path (data/)\n  - Define pipe-delimited field names, order, and expected data types\n  - Provide at least one fully formatted example row matching the schema\n- Ensure schemas align with backend routes’ data usage and user requirements\n\nCRITICAL SUCCESS CRITERIA:\n- Resulting backend_design.md enables creation of app.py implementing all stated routes and file-based data models\n- Output uses only user_task_description and does not assume or incorporate frontend design details\n- MUST use write_text_file tool to output backend_design.md\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and UI design for web applications with focus on element IDs and navigation flows.\n\nYour goal is to create a detailed frontend design specification defining the HTML templates and UI layout for the TravelPlanner application.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Independently produce frontend_design.md specifying all required templates and page elements\n- Define all HTML page templates with exact page titles, container divs, input fields, buttons, tables, dropdowns, and any dynamic elements\n- Specify element IDs for every interactive UI component described in the requirements\n- Document navigation flows including button/link actions and page-to-page transitions mapping to route paths\n- Do not access or rely on backend_design.md; work independently of sibling outputs\n\n**Section 1: HTML Template Specifications**\n- For each page listed (Dashboard, Destinations, Destination Details, Itinerary Planning, Accommodations, Transportation, Travel Packages, Trip Management, Booking Confirmation, Travel Recommendations):\n  - Specify template filename (e.g., dashboard.html)\n  - Set exact page title\n  - List all element IDs with their HTML tag and functional description according to user requirements\n\n**Section 2: UI Navigation and Interaction**\n- Map each button or clickable element ID to its navigation target or triggered action\n- Include usage of dropdowns and input fields with their expected roles in filtering or data entry\n\nCRITICAL SUCCESS CRITERIA:\n- frontend_design.md fully enables implementation of templates/*.html with described layout and IDs\n- All elements and navigation flows derive solely from user_task_description\n- MUST use write_text_file tool to output frontend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in merging complementary backend and frontend design specifications for Flask web applications.\n\nYour goal is to produce a coherent, internally consistent design_spec.md artifact by merging backend_design.md and frontend_design.md for the TravelPlanner application.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Reconcile backend routes, local text file schema, and frontend template element IDs and navigation flows\n- Merge specifications into a single design_spec.md preserving original requirements without introducing new features\n- Align backend context variables with frontend UI element IDs for consistency\n- Verify no conflicting route, template, or element definitions; resolve discrepancies adaptively maintaining user requirements\n\n**Section 1: Merged Backend Specification**\n- Present unified routes list with methods, paths, templates, and context variables consistent with frontend usage\n- Include comprehensive local text file schemas with field details and examples from backend_design.md\n\n**Section 2: Merged Frontend Specification**\n- Present all templates with page titles, element IDs, and UI layout details from frontend_design.md\n- Show navigation flow linkage consistent with backend routes\n\n**Section 3: Consistency and Completeness Verification**\n- Confirm backend data models and frontend UI elements fully address all user functionalities\n- Highlight any necessary harmonization actions performed\n- Ensure output artifact enables downstream implementation without ambiguity\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md integrates backend and frontend designs maintaining full user requirement coverage\n- Output must be produced only by DesignMerger using write_text_file tool\n- Do not add new requirements or features beyond those in input artifacts\n- Write exactly design_spec.md only, no additional outputs or refinement markings\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness and adherence to user requirements for TravelPlanner backend architecture.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design completeness and adherence to user requirements for TravelPlanner UI and element IDs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend Flask app.py and frontend HTML templates in parallel based on design_spec.md and merge them into final runnable files\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements the app.py Flask backend based on design_spec.md; FrontendDeveloper implements templates/*.html based on design_spec.md. \"\n        \"IntegrationMerger reconciles both implementations into final app.py and templates/*.html ensuring interface consistency.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask web applications.\n\nYour goal is to implement the backend Flask application as app.py based on the design specification without dependencies on frontend implementation.\n\nTask Details:\n- Read design_spec.md from CONTEXT independently\n- Implement app.py reflecting all backend routes, data loading from local text files, and business logic\n- Use provided design specifications for routes, data schemas, and backend process flows\n- Output a runnable Flask backend app.py, matching declared interfaces\n\n**Section 1: Flask Backend Implementation Requirements**\n- Implement all Flask routes with correct paths, HTTP methods, and template rendering calls\n- Load and parse data files as specified (e.g., destinations.txt, itineraries.txt, flights.txt, etc.)\n- Implement backend logic to support user actions like browsing, searching, booking, and managing trips\n- Follow naming and structural conventions defined in design_spec.md for route handlers and data functions\n\n**Section 2: Data Handling and File I/O**\n- Read and write local data files in the data directory with exact formats specified\n- Implement parsing logic for pipe-separated values with correct field interpretations\n- Include example data handling matching the given data format examples in design_spec.md\n\n**Section 3: Application Setup and Execution**\n- Use Flask best practices for app creation, route definition, and error handling\n- Include clear code comments using single-quote docstrings and comments\n- Ensure the file is self-contained and runnable as the backend server\n\nCRITICAL SUCCESS CRITERIA:\n- Must use write_text_file tool to save app.py\n- Only produce app.py as output artifact\n- Implement all backend requirements exclusively from design_spec.md without referencing frontend artifacts\n- The implementation must be ready for deployment and integration with frontend templates\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement all required HTML templates independently based on the design specification without dependencies on backend code.\n\nTask Details:\n- Read design_spec.md from CONTEXT independently\n- Create all HTML templates in templates/*.html as specified\n- Implement exact UI structure, element IDs, context variables, and navigation behaviors as documented\n- Output a complete set of HTML templates consistent with design_spec.md\n\n**Section 1: Template Structure and Formatting**\n- Define each page template matching declared page titles and element IDs\n- Use Jinja2 templating syntax for dynamic content placeholders and control structures\n- Ensure navigation links and buttons match the route names prescribed by the backend design\n\n**Section 2: UI Elements and Accessibility**\n- Implement elements with exact IDs and types as specified (div, input, button, dropdown, table, etc.)\n- Layout pages clearly and structurally per specification, with correct context-variable usage\n- Include comments using single-quote docstrings or hash comments for clarity\n\n**Section 3: Template File Output and Naming**\n- Save each template in the templates directory with the correct filename pattern (*.html)\n- Templates must be ready to render with the backend Flask app without modification\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save each template file within templates/*.html\n- Output only the templates/*.html artifact\n- Implement entirely from design_spec.md independent of backend implementation\n- Ensure template structure is compliant with the given UI element details and navigation requirements\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in reconciling backend and frontend implementations of Flask web applications.\n\nYour goal is to merge and reconcile backend app.py and frontend templates/*.html to produce final consistent deployable artifacts.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify interface consistency between backend routes and frontend templates\n- Resolve mismatches in route names, context variables, and data handling\n- Produce final deployable app.py and templates/*.html that are fully consistent and runnable\n\n**Section 1: Interface Consistency Checks**\n- Match all Flask route handlers with corresponding template render calls\n- Check all context variables expected by templates are provided by backend\n- Validate route paths, HTTP methods, and template filenames are consistent across artifacts\n\n**Section 2: Code and Template Adaptation**\n- Modify backend or frontend artifacts only to fix interface mismatches without adding features\n- Maintain original design_spec.md requirements strictly without addition or omission\n- Preserve coding style and formatting conventions established in both implementations\n\n**Section 3: Final Artifact Preparation**\n- Save reconciled app.py and all templates/*.html ensuring runnable integration\n- Include comments documenting any adjustments made for interface alignment\n- Confirm final files are deployable with no unresolved references or errors\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to produce final app.py and templates/*.html\n- Output the declared backend and frontend file artifacts only\n- Ensure perfect interface conformance with design_spec.md requirements\n- Final artifacts must be ready for deployment and testing without modification\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Review backend code app.py for conformance with design_spec.md and correct any interface mismatches.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Review frontend templates/*.html for conformance with design_spec.md and correct any interface mismatches.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Python Flask backend development and local text file data schema design.

Your goal is to create a comprehensive backend design specification for the TravelPlanner application, suitable for independent implementation.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently produce backend_design.md
- Specify all Python Flask routes with methods, endpoints, and template names
- Define all local text file data schemas for all entities described in user_task_description, including field names, types, delimiters, and example rows
- Do not reference or read frontend_design.md; work without sibling output artifacts

**Section 1: Flask Backend Routes Specification**
- List each route path and HTTP method mapped to a Flask function name
- Specify the template filename each route renders and associated context variables
- Include any redirect behavior and form submission handlers described in user requirements

**Section 2: Local Text File Data Schemas**
- For each text data file described (destinations.txt, itineraries.txt, hotels.txt, flights.txt, packages.txt, trips.txt, bookings.txt):
  - Specify exact filename and relative path (data/)
  - Define pipe-delimited field names, order, and expected data types
  - Provide at least one fully formatted example row matching the schema
- Ensure schemas align with backend routes’ data usage and user requirements

CRITICAL SUCCESS CRITERIA:
- Resulting backend_design.md enables creation of app.py implementing all stated routes and file-based data models
- Output uses only user_task_description and does not assume or incorporate frontend design details
- MUST use write_text_file tool to output backend_design.md

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML and UI design for web applications with focus on element IDs and navigation flows.

Your goal is to create a detailed frontend design specification defining the HTML templates and UI layout for the TravelPlanner application.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently produce frontend_design.md specifying all required templates and page elements
- Define all HTML page templates with exact page titles, container divs, input fields, buttons, tables, dropdowns, and any dynamic elements
- Specify element IDs for every interactive UI component described in the requirements
- Document navigation flows including button/link actions and page-to-page transitions mapping to route paths
- Do not access or rely on backend_design.md; work independently of sibling outputs

**Section 1: HTML Template Specifications**
- For each page listed (Dashboard, Destinations, Destination Details, Itinerary Planning, Accommodations, Transportation, Travel Packages, Trip Management, Booking Confirmation, Travel Recommendations):
  - Specify template filename (e.g., dashboard.html)
  - Set exact page title
  - List all element IDs with their HTML tag and functional description according to user requirements

**Section 2: UI Navigation and Interaction**
- Map each button or clickable element ID to its navigation target or triggered action
- Include usage of dropdowns and input fields with their expected roles in filtering or data entry

CRITICAL SUCCESS CRITERIA:
- frontend_design.md fully enables implementation of templates/*.html with described layout and IDs
- All elements and navigation flows derive solely from user_task_description
- MUST use write_text_file tool to output frontend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in merging complementary backend and frontend design specifications for Flask web applications.

Your goal is to produce a coherent, internally consistent design_spec.md artifact by merging backend_design.md and frontend_design.md for the TravelPlanner application.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Reconcile backend routes, local text file schema, and frontend template element IDs and navigation flows
- Merge specifications into a single design_spec.md preserving original requirements without introducing new features
- Align backend context variables with frontend UI element IDs for consistency
- Verify no conflicting route, template, or element definitions; resolve discrepancies adaptively maintaining user requirements

**Section 1: Merged Backend Specification**
- Present unified routes list with methods, paths, templates, and context variables consistent with frontend usage
- Include comprehensive local text file schemas with field details and examples from backend_design.md

**Section 2: Merged Frontend Specification**
- Present all templates with page titles, element IDs, and UI layout details from frontend_design.md
- Show navigation flow linkage consistent with backend routes

**Section 3: Consistency and Completeness Verification**
- Confirm backend data models and frontend UI elements fully address all user functionalities
- Highlight any necessary harmonization actions performed
- Ensure output artifact enables downstream implementation without ambiguity

CRITICAL SUCCESS CRITERIA:
- design_spec.md integrates backend and frontend designs maintaining full user requirement coverage
- Output must be produced only by DesignMerger using write_text_file tool
- Do not add new requirements or features beyond those in input artifacts
- Write exactly design_spec.md only, no additional outputs or refinement markings

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Python Flask web applications.

Your goal is to implement the backend Flask application as app.py based on the design specification without dependencies on frontend implementation.

Task Details:
- Read design_spec.md from CONTEXT independently
- Implement app.py reflecting all backend routes, data loading from local text files, and business logic
- Use provided design specifications for routes, data schemas, and backend process flows
- Output a runnable Flask backend app.py, matching declared interfaces

**Section 1: Flask Backend Implementation Requirements**
- Implement all Flask routes with correct paths, HTTP methods, and template rendering calls
- Load and parse data files as specified (e.g., destinations.txt, itineraries.txt, flights.txt, etc.)
- Implement backend logic to support user actions like browsing, searching, booking, and managing trips
- Follow naming and structural conventions defined in design_spec.md for route handlers and data functions

**Section 2: Data Handling and File I/O**
- Read and write local data files in the data directory with exact formats specified
- Implement parsing logic for pipe-separated values with correct field interpretations
- Include example data handling matching the given data format examples in design_spec.md

**Section 3: Application Setup and Execution**
- Use Flask best practices for app creation, route definition, and error handling
- Include clear code comments using single-quote docstrings and comments
- Ensure the file is self-contained and runnable as the backend server

CRITICAL SUCCESS CRITERIA:
- Must use write_text_file tool to save app.py
- Only produce app.py as output artifact
- Implement all backend requirements exclusively from design_spec.md without referencing frontend artifacts
- The implementation must be ready for deployment and integration with frontend templates

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement all required HTML templates independently based on the design specification without dependencies on backend code.

Task Details:
- Read design_spec.md from CONTEXT independently
- Create all HTML templates in templates/*.html as specified
- Implement exact UI structure, element IDs, context variables, and navigation behaviors as documented
- Output a complete set of HTML templates consistent with design_spec.md

**Section 1: Template Structure and Formatting**
- Define each page template matching declared page titles and element IDs
- Use Jinja2 templating syntax for dynamic content placeholders and control structures
- Ensure navigation links and buttons match the route names prescribed by the backend design

**Section 2: UI Elements and Accessibility**
- Implement elements with exact IDs and types as specified (div, input, button, dropdown, table, etc.)
- Layout pages clearly and structurally per specification, with correct context-variable usage
- Include comments using single-quote docstrings or hash comments for clarity

**Section 3: Template File Output and Naming**
- Save each template in the templates directory with the correct filename pattern (*.html)
- Templates must be ready to render with the backend Flask app without modification

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save each template file within templates/*.html
- Output only the templates/*.html artifact
- Implement entirely from design_spec.md independent of backend implementation
- Ensure template structure is compliant with the given UI element details and navigation requirements

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in reconciling backend and frontend implementations of Flask web applications.

Your goal is to merge and reconcile backend app.py and frontend templates/*.html to produce final consistent deployable artifacts.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify interface consistency between backend routes and frontend templates
- Resolve mismatches in route names, context variables, and data handling
- Produce final deployable app.py and templates/*.html that are fully consistent and runnable

**Section 1: Interface Consistency Checks**
- Match all Flask route handlers with corresponding template render calls
- Check all context variables expected by templates are provided by backend
- Validate route paths, HTTP methods, and template filenames are consistent across artifacts

**Section 2: Code and Template Adaptation**
- Modify backend or frontend artifacts only to fix interface mismatches without adding features
- Maintain original design_spec.md requirements strictly without addition or omission
- Preserve coding style and formatting conventions established in both implementations

**Section 3: Final Artifact Preparation**
- Save reconciled app.py and all templates/*.html ensuring runnable integration
- Include comments documenting any adjustments made for interface alignment
- Confirm final files are deployable with no unresolved references or errors

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to produce final app.py and templates/*.html
- Output the declared backend and frontend file artifacts only
- Ensure perfect interface conformance with design_spec.md requirements
- Final artifacts must be ready for deployment and testing without modification

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
        ("DesignMerger", """Verify backend design completeness and adherence to user requirements for TravelPlanner backend architecture.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design completeness and adherence to user requirements for TravelPlanner UI and element IDs.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Review backend code app.py for conformance with design_spec.md and correct any interface mismatches.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Review frontend templates/*.html for conformance with design_spec.md and correct any interface mismatches.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        max_retries=3,
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
        max_retries=3,
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
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel generation of backend_design.md and frontend_design.md
    await asyncio.gather(
        execute(BackendDesignArchitect, "Analyze user_task_description and create backend_design.md with Flask routes and local text file schemas."),
        execute(FrontendDesignArchitect, "Analyze user_task_description and create frontend_design.md with detailed HTML templates, element IDs, and navigation flows.")
    )

    backend_design = ""
    frontend_design = ""
    try:
        backend_design = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md with user_task_description.\n\n"
        f"=== Backend Design ===\n{backend_design}\n\n"
        f"=== Frontend Design ===\n{frontend_design}"
    )
# Phase1_End
# Phase2_Start
import glob
import asyncio

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
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

    # Parallel implementation by BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper, "Implement backend Flask app.py based on design_spec.md provided by DesignMerger."),
        execute(FrontendDeveloper, "Implement frontend templates/*.html based on design_spec.md provided by DesignMerger.")
    )

    # Read the outputs of BackendDeveloper and FrontendDeveloper
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass

    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # IntegrationMerger merges and reconciles backend and frontend implementations
    await execute(
        IntegrationMerger,
        "Merge and reconcile backend app.py and frontend templates/*.html for final consistent deployable artifacts.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
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
