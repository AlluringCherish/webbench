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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces design_spec.md detailing Flask routes mapping to 10 pages, \"\n        \"HTML templates with element IDs and context variables, and data schemas for local text files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create comprehensive design specifications that enable Backend and Frontend developers to work independently without mutual implementation dependencies.\n\nTask Details:\n- Read full user_task_description from CONTEXT\n- Produce design_spec.md covering:\n  - Complete Flask routes for all 10 pages with HTTP methods and context variables\n  - HTML template specifications including exact element IDs, page titles, and context variables\n  - Navigation mappings with url_for functions for all buttons and links\n  - Data schemas for all local text files used by the app with field order and examples\n- Do NOT assume knowledge beyond user_task_description and data formats\n- Output artifacts must precisely conform to specified format for downstream development\n\n**Section 1: Flask Routes Specification**\n\nProvide a detailed route table including:\n- Route endpoint (e.g., /dashboard, /destinations, /destinations/<int:dest_id>)\n- HTTP methods (GET, POST as applicable)\n- Function names (lowercase with underscores)\n- Template files to render\n- Context variables passed, with types and structures (e.g., list of dict with fields)\n- Navigation actions triggered by buttons/links (e.g., browse-destinations-button leads to /destinations)\n\n**Section 2: HTML Templates Specification**\n\nFor each HTML template, specify:\n- Exact filename (templates/{name}.html)\n- Page title (used in <title> and <h1>)\n- Full list of element IDs with their HTML types and functional descriptions\n- Context variables available with data types and sample structure\n- Navigation mappings for buttons and links using url_for(), matching Flask routes exactly\n- Dynamic element ID patterns with Jinja2 syntax (e.g., view-destination-button-{{ dest.dest_id }})\n\n**Section 3: Data File Schemas**\n\nFor each local text file used for data storage:\n- Path (data/{filename}.txt)\n- Exact pipe-delimited field names and order\n- Brief description of stored data\n- Example rows illustrating expected data\n- Clarify no header row exists in files\n\nCRITICAL SUCCESS CRITERIA:\n- Specification supports full independent backend and frontend development without further information\n- Route function names and template variable names are consistent throughout\n- All element IDs in page designs are accurately captured\n- Data schemas strictly follow user data format samples with exact field order\n- Use write_text_file tool to generate design_spec.md\n- Do NOT provide partial or ambiguous specifications\n- Do NOT include any implementation code snippets in this document\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Review design_spec.md to ensure complete and accurate specifications for Flask routes including endpoints, HTTP methods, \"\n                \"context variables for each route, and precise data schemas for handling local text files.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Review design_spec.md to verify all HTML templates have correct element IDs, \"\n                \"navigation mappings (url_for usage), page titles, and context variables detailed for frontend implementation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend app.py and frontend HTML templates in parallel based on design specifications\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py based on design_spec.md sections covering Flask routes and data handling. \"\n        \"FrontendDeveloper implements templates/*.html based on design_spec.md sections covering HTML with exact element IDs and navigation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application (app.py) based on provided design specifications.\n\nTask Details:\n- Read design_spec.md sections covering Flask routes and data schemas ONLY\n- Implement all specified Flask routes with correct HTTP methods and function names\n- Load and process data from local text files in 'data/' directory using exact field orders specified\n- Pass correct context variables to templates as specified\n- Do NOT read or implement any frontend template details\n- Do NOT modify design_spec.md or frontend artifacts\n\nImplementation Requirements:\n1. **Flask App Setup**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Routing**:\n   - Implement all routes defined in design_spec.md with exact function names\n   - Use correct HTTP methods (GET, POST) as specified\n   - The root route '/' must redirect to the dashboard page using:\n     ```python\n     return redirect(url_for('dashboard'))\n     ```\n\n3. **Data Handling**:\n   - Load data from 'data/*.txt' files with pipe-delimited format (|)\n   - Parse fields exactly in order specified in design_spec.md data schemas\n   - Use dictionary structures with exact field names as keys\n   - Handle file I/O errors gracefully and use empty lists if files are missing\n   - No header lines present; parse from first line\n\n4. **Context Variables**:\n   - Pass all context variables to templates exactly as specified in design_spec.md\n   - Ensure variable names and types match specification exactly\n\n5. **Best Practices**:\n   - Use url_for for all internal redirects and links\n   - Implement POST route handling for any forms as specified\n   - Add main Flask app run guard\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the complete 'app.py'\n- Follow design_spec.md exactly; do not add undocumented features\n- Function names, route paths, and context variables must match specification precisely\n- Do NOT attempt to implement frontend templates or UI\n- Do NOT provide code snippets as plain text; always write to file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement complete HTML templates based on provided design specifications.\n\nTask Details:\n- Read design_spec.md sections covering HTML templates with exact element IDs, structure, and navigation ONLY\n- Implement all specified HTML templates with correct filenames under 'templates/' directory\n- Use exact element IDs, page titles, and navigation mappings as specified\n- Use Jinja2 syntax for dynamic content, loops, and conditionals exactly as per specification\n- Do NOT read or implement any backend logic or data handling code\n- Do NOT modify design_spec.md or backend artifacts\n\nImplementation Requirements:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>Page Title from design_spec.md</title>\n   </head>\n   <body>\n       <div id=\"container-id\">\n           <h1>Page Title</h1>\n           <!-- Page content -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs**:\n   - Include ALL specified element IDs exactly as named (case-sensitive)\n   - For dynamic IDs (e.g., view-destination-button-{dest_id}), use Jinja2 syntax:\n     ```html\n     id=\"view-destination-button-{{ dest.dest_id }}\"\n     ```\n\n3. **Context Variables and Content**:\n   - Use context variables as provided in design_spec.md for rendering dynamic data\n   - Use loops and conditionals in Jinja2 as needed\n   - Do not assume additional variables beyond specification\n\n4. **Navigation**:\n   - Implement all navigation as url_for calls in hrefs or form actions\n   - Follow exact function names for Flask routes as specified\n\n5. **Forms**:\n   - Implement forms with method=\"POST\" and action using url_for if specified\n   - Include all required fields with exact element IDs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files under 'templates/' directory\n- All element IDs, page titles, and navigation links must match design_spec.md exactly\n- Do NOT add any templates or elements not specified in design_spec.md\n- Do NOT include backend logic or code in templates\n- Do NOT provide code snippets as plain text; always write to file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all specified Flask routes, uses correct HTTP methods, loads and processes data from local text files \"\n                \"with correct field orders, and ensures root route redirects to dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all templates/*.html implement design_spec.md exactly: presence of all specified element IDs, correct usage of context variables, \"\n                \"accurate navigation via url_for, and matching page titles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create comprehensive design specifications that enable Backend and Frontend developers to work independently without mutual implementation dependencies.

Task Details:
- Read full user_task_description from CONTEXT
- Produce design_spec.md covering:
  - Complete Flask routes for all 10 pages with HTTP methods and context variables
  - HTML template specifications including exact element IDs, page titles, and context variables
  - Navigation mappings with url_for functions for all buttons and links
  - Data schemas for all local text files used by the app with field order and examples
- Do NOT assume knowledge beyond user_task_description and data formats
- Output artifacts must precisely conform to specified format for downstream development

**Section 1: Flask Routes Specification**

Provide a detailed route table including:
- Route endpoint (e.g., /dashboard, /destinations, /destinations/<int:dest_id>)
- HTTP methods (GET, POST as applicable)
- Function names (lowercase with underscores)
- Template files to render
- Context variables passed, with types and structures (e.g., list of dict with fields)
- Navigation actions triggered by buttons/links (e.g., browse-destinations-button leads to /destinations)

**Section 2: HTML Templates Specification**

For each HTML template, specify:
- Exact filename (templates/{name}.html)
- Page title (used in <title> and <h1>)
- Full list of element IDs with their HTML types and functional descriptions
- Context variables available with data types and sample structure
- Navigation mappings for buttons and links using url_for(), matching Flask routes exactly
- Dynamic element ID patterns with Jinja2 syntax (e.g., view-destination-button-{{ dest.dest_id }})

**Section 3: Data File Schemas**

For each local text file used for data storage:
- Path (data/{filename}.txt)
- Exact pipe-delimited field names and order
- Brief description of stored data
- Example rows illustrating expected data
- Clarify no header row exists in files

CRITICAL SUCCESS CRITERIA:
- Specification supports full independent backend and frontend development without further information
- Route function names and template variable names are consistent throughout
- All element IDs in page designs are accurately captured
- Data schemas strictly follow user data format samples with exact field order
- Use write_text_file tool to generate design_spec.md
- Do NOT provide partial or ambiguous specifications
- Do NOT include any implementation code snippets in this document

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

Your goal is to implement a complete Flask backend application (app.py) based on provided design specifications.

Task Details:
- Read design_spec.md sections covering Flask routes and data schemas ONLY
- Implement all specified Flask routes with correct HTTP methods and function names
- Load and process data from local text files in 'data/' directory using exact field orders specified
- Pass correct context variables to templates as specified
- Do NOT read or implement any frontend template details
- Do NOT modify design_spec.md or frontend artifacts

Implementation Requirements:
1. **Flask App Setup**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Routing**:
   - Implement all routes defined in design_spec.md with exact function names
   - Use correct HTTP methods (GET, POST) as specified
   - The root route '/' must redirect to the dashboard page using:
     ```python
     return redirect(url_for('dashboard'))
     ```

3. **Data Handling**:
   - Load data from 'data/*.txt' files with pipe-delimited format (|)
   - Parse fields exactly in order specified in design_spec.md data schemas
   - Use dictionary structures with exact field names as keys
   - Handle file I/O errors gracefully and use empty lists if files are missing
   - No header lines present; parse from first line

4. **Context Variables**:
   - Pass all context variables to templates exactly as specified in design_spec.md
   - Ensure variable names and types match specification exactly

5. **Best Practices**:
   - Use url_for for all internal redirects and links
   - Implement POST route handling for any forms as specified
   - Add main Flask app run guard

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the complete 'app.py'
- Follow design_spec.md exactly; do not add undocumented features
- Function names, route paths, and context variables must match specification precisely
- Do NOT attempt to implement frontend templates or UI
- Do NOT provide code snippets as plain text; always write to file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement complete HTML templates based on provided design specifications.

Task Details:
- Read design_spec.md sections covering HTML templates with exact element IDs, structure, and navigation ONLY
- Implement all specified HTML templates with correct filenames under 'templates/' directory
- Use exact element IDs, page titles, and navigation mappings as specified
- Use Jinja2 syntax for dynamic content, loops, and conditionals exactly as per specification
- Do NOT read or implement any backend logic or data handling code
- Do NOT modify design_spec.md or backend artifacts

Implementation Requirements:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Page Title from design_spec.md</title>
   </head>
   <body>
       <div id="container-id">
           <h1>Page Title</h1>
           <!-- Page content -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs**:
   - Include ALL specified element IDs exactly as named (case-sensitive)
   - For dynamic IDs (e.g., view-destination-button-{dest_id}), use Jinja2 syntax:
     ```html
     id="view-destination-button-{{ dest.dest_id }}"
     ```

3. **Context Variables and Content**:
   - Use context variables as provided in design_spec.md for rendering dynamic data
   - Use loops and conditionals in Jinja2 as needed
   - Do not assume additional variables beyond specification

4. **Navigation**:
   - Implement all navigation as url_for calls in hrefs or form actions
   - Follow exact function names for Flask routes as specified

5. **Forms**:
   - Implement forms with method="POST" and action using url_for if specified
   - Include all required fields with exact element IDs

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files under 'templates/' directory
- All element IDs, page titles, and navigation links must match design_spec.md exactly
- Do NOT add any templates or elements not specified in design_spec.md
- Do NOT include backend logic or code in templates
- Do NOT provide code snippets as plain text; always write to file

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
        ("BackendDeveloper", """Review design_spec.md to ensure complete and accurate specifications for Flask routes including endpoints, HTTP methods, "
                "context variables for each route, and precise data schemas for handling local text files.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Review design_spec.md to verify all HTML templates have correct element IDs, "
                "navigation mappings (url_for usage), page titles, and context variables detailed for frontend implementation.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all specified Flask routes, uses correct HTTP methods, loads and processes data from local text files "
                "with correct field orders, and ensures root route redirects to dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}]),
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all templates/*.html implement design_spec.md exactly: presence of all specified element IDs, correct usage of context variables, "
                "accurate navigation via url_for, and matching page titles.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}]),
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
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create design_spec.md with complete Flask routes, HTML template specs, and data file schemas based on user_task_description")
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
        execute(BackendDeveloper, "Implement backend app.py based on design_spec.md sections covering Flask routes and data handling"),
        execute(FrontendDeveloper, "Implement frontend templates/*.html based on design_spec.md sections covering HTML with exact element IDs and navigation")
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
