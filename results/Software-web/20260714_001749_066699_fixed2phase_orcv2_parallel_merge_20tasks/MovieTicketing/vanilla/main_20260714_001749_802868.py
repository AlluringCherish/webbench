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
# 20260714_001749_802868/main_20260714_001749_802868.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications and merge them into a consistent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDesignArchitect defines Flask routes, data schemas and business logic contracts; FrontendDesignArchitect specifies HTML templates, element IDs, context variables and navigation details independently; DesignMerger consolidates both designs into design_spec.md ensuring consistency and compliance with user requirements.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Software System Architect specializing in Flask backend development and file-based data management using Python.\n\nYour goal is to define the backend design to fully support the 'MovieTicketing' web application functionalities by specifying Flask routes, data file schemas, and backend operations based strictly on the user task description.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently produce backend_design.md describing all necessary Flask routes and data schemas\n- Define precise route paths, HTTP methods, and route functions to handle movie browsing, showtimes, seat selection, booking, and theater information\n- Specify exact data file formats and field details to allow interaction with the local text data files\n- Do not read or incorporate frontend_design.md or sibling outputs\n\n**Section 1: Flask Routes and Backend Operations**\n- List each route path, HTTP method, and its functionality\n- For each route, specify required input parameters and returned data or rendered template context variables\n- Describe interactions with data files: reads, writes, and updates with exact file names and field mappings\n\n**Section 2: Data File Formats and Business Logic Contracts**\n- Document each text data file schema as pipe-separated fields with field names and data types\n- Provide field order, example rows, and constraints to ensure consistency\n- Define backend logic rules such as seat availability checks and booking creation flow\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDesignArchitect must produce a blueprint sufficient for implementation of a Flask app managing local text data per user requirements\n- Use write_text_file tool exclusively to output backend_design.md\n- Do not read sibling artifacts or add requirements beyond user_task_description\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Frontend System Architect specializing in HTML template design and user interface specification for Flask-based web applications.\n\nYour goal is to create complete frontend HTML template specifications with element IDs, context variables, and navigation flows, supporting the 'MovieTicketing' application features according to the user task description.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently develop frontend_design.md describing all HTML templates, page titles, element IDs, and navigation mappings\n- Specify templates for all eight pages including Dashboard, Movie Catalog, Movie Details, Showtime Selection, Seat Selection, Booking Confirmation, Booking History, and Theater Information\n- Detail element IDs as specified in the user task, define all context variables passed to templates, and outline navigation and button actions\n- Do not read or assume backend_design.md or sibling outputs\n\n**Section 1: HTML Template Specifications**\n- For each page, specify template filename and exact page title\n- List all significant element IDs with their element types and descriptive roles\n- Define all context variables passed into templates including their names, types, and expected values\n- Map buttons and links to navigation flows (routes or dynamic actions)\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDesignArchitect must produce a template design enabling accurate UI implementation aligning with user_task_description\n- Use write_text_file tool exclusively to output frontend_design.md\n- Do not add requirements or read sibling artifacts\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect with expertise in consolidating backend and frontend designs into a consistent web application design specification.\n\nYour goal is to merge backend_design.md and frontend_design.md into a single coherent design_spec.md that aligns precisely with the user task description and complies with both backend and frontend constraints.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Analyze and reconcile backend routes, data schemas, and frontend templates, element IDs, and navigation flows\n- Resolve any discrepancies between element naming, route paths, context variable definitions, and navigation links\n- Ensure the final design_spec.md is consistent, complete, and does not introduce new requirements beyond user_task_description and provided designs\n\n**Section 1: Consolidated Backend and Frontend Specification**\n- Present combined Flask route definitions with linked frontend template filenames\n- Ensure context variables are aligned between backend routes and frontend templates\n- Unify element IDs and navigation flows ensuring they correctly correspond to backend operations\n\n**Section 2: Data Schema and Page Design Consistency**\n- Validate that data file schemas support all frontend-displayed data and backend operations\n- Confirm all pages and UI elements specified in frontend_design.md are supported by backend routes and data files\n- Provide notes on any design consistency adjustments made\n\nCRITICAL SUCCESS CRITERIA:\n- DesignMerger must produce a final design_spec.md enabling seamless implementation by backend and frontend developers\n- Use write_text_file tool exclusively to output design_spec.md\n- Verify completeness, correctness, and consistency without adding features beyond input artifacts\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness, correctness, and compliance with requirements; ensure no conflicts with frontend design.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design completeness, correctness, element IDs, and navigation flows; ensure no conflicts with backend design.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend and frontend code independently from design_spec.md and merge them into complete functional app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDeveloper implements Flask app.py features according to backend design; FrontendDeveloper implements templates/*.html per frontend design; IntegrationMerger merges and reconciles both implementations for functional correctness and interface consistency.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask web applications.\n\nYour goal is to implement a complete Flask backend according to the adaptive backend design in design_spec.md, including all routes, business logic, and data management using local text files.\n\nTask Details:\n- Read design_spec.md from CONTEXT focusing on backend routes, data schema, and logic\n- Create app.py implementing independent backend functionality without dependency on frontend outputs\n- Output app.py implementing all specified Flask routes, file reads/writes, and logic for the MovieTicketing application\n\n**Implementation Requirements: Routes and Business Logic**\n- Implement HTTP routes as specified, including URL paths, methods, and expected behaviors\n- Perform all local text file data reads and writes as per data schema (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)\n- Maintain data integrity and handle all business logic such as seat selection, booking processing, and data filtering\n\n**Data File Handling**\n- Use the specified pipe-delimited formats for all data files\n- Implement robust parsing and writing functions compliant with the specified data schema\n- Ensure consistency with design_spec.md’s data schema descriptions\n\n**File and Project Structure**\n- Place app.py at project root\n- Do not include any frontend code here; focus strictly on backend implementation\n\nCRITICAL SUCCESS CRITERIA:\n- Fully functional Flask backend covering all backend_design.md routes and logic\n- Correct input/output data handling with local text files\n- Use write_text_file tool to save app.py\n- Use validate_python_file tool to check syntax and runtime of app.py\n- Write only the declared app.py output artifact\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML with Jinja2 templating for Flask web applications.\n\nYour goal is to implement the full set of HTML templates according to the frontend design section in design_spec.md, respecting all specified element IDs, layout, and dynamic data placeholders.\n\nTask Details:\n- Read design_spec.md from CONTEXT focusing on frontend template specifications, element IDs, context variables, and navigation\n- Create all necessary templates/*.html implementing the exact layout, element IDs, and placeholders\n- Implement templates independent of backend source code; do not read any sibling outputs\n\n**Template Structure and Content**\n- Implement templates for all pages described including Dashboard, Movie Catalog, Movie Details, Showtime Selection, Seat Selection, Booking Confirmation, Booking History, and Theater Information\n- Ensure element IDs exactly match those specified for each page\n- Use Jinja2 syntax for dynamic data placeholders as defined in design_spec.md\n- Implement navigation elements as per design_spec.md\n\n**File and Project Structure**\n- Place all template files in templates/ directory\n- Follow naming conventions provided in design_spec.md or inferred from page titles\n\nCRITICAL SUCCESS CRITERIA:\n- Templates are complete, correctly structured, and matching element IDs and placeholders\n- No dependencies on backend implementation details beyond design_spec.md\n- Use write_text_file tool to save templates/*.html outputs\n- Write only the declared templates/*.html output artifacts\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web applications combining backend and frontend implementations.\n\nYour goal is to merge and reconcile independently developed app.py backend and templates/*.html frontend according to design_spec.md, resolving interface inconsistencies and producing a cohesive, fully functional final application.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Identify mismatches in route URLs, template rendering calls, context variable names, and element IDs\n- Reconcile app.py and templates/*.html for consistency without adding new features\n- Correct interface and integration issues such as variable mismatches, missing routes, or template file names\n- Validate app.py syntax and runtime correctness after merging fixes\n\n**Consistency and Integration Requirements**\n- Ensure all routes in app.py correspond to templates provided and vice versa\n- Verify dynamic data placeholders in templates align with app.py context data\n- Confirm navigation elements in templates link to existing backend routes\n- Fix issues strictly within scope: interface consistency and integration correctness\n\n**Output and Validation**\n- Output merged and corrected app.py and templates/*.html\n- Validate app.py using validate_python_file tool to ensure functionality\n- Maintain original project structure and naming conventions\n\nCRITICAL SUCCESS CRITERIA:\n- Fully integrated, consistent backend and frontend codebase conforming to design_spec.md\n- No functionality added beyond original designs\n- Use write_text_file to output final app.py and templates/*.html\n- Use validate_python_file tool to check final app.py syntax and runtime\n- Write only the declared output artifacts app.py and templates/*.html\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend implementation against design_spec.md, verify routes, logic, and text file data handling correctness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check frontend templates against design_spec.md, verifying element IDs, dynamic data placeholders, layout, and navigation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'MovieTicketing' Web Application

## 1. Objective
Develop a comprehensive web application named 'MovieTicketing' using Python, with data managed through local text files. The application enables users to browse movies, view showtimes, select seats, book tickets, view booking history, and manage theater information. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'MovieTicketing' application is Python.

## 3. Page Design

The 'MovieTicketing' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Movie Ticketing Dashboard
- **Overview**: The main hub displaying featured movies, upcoming releases, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-movies** - Type: Div - Display of featured movie recommendations.
  - **ID: browse-movies-button** - Type: Button - Button to navigate to movie catalog page.
  - **ID: view-bookings-button** - Type: Button - Button to navigate to booking history page.
  - **ID: showtimes-button** - Type: Button - Button to navigate to showtimes page.

### 2. Movie Catalog Page
- **Page Title**: Movie Catalog
- **Overview**: A page displaying all available movies with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search movies by title or genre.
  - **ID: genre-filter** - Type: Dropdown - Dropdown to filter by genre (Action, Comedy, Drama, Horror, etc.).
  - **ID: movies-grid** - Type: Div - Grid displaying movie cards with poster, title, rating, and duration.
  - **ID: view-movie-button-{movie_id}** - Type: Button - Button to view movie details (each movie card has this).

### 3. Movie Details Page
- **Page Title**: Movie Details
- **Overview**: A page displaying detailed information about a specific movie.
- **Elements**:
  - **ID: movie-details-page** - Type: Div - Container for the movie details page.
  - **ID: movie-title** - Type: H1 - Display movie title.
  - **ID: movie-director** - Type: Div - Display movie director.
  - **ID: movie-rating** - Type: Div - Display movie rating.
  - **ID: movie-description** - Type: Div - Display movie description.
  - **ID: select-showtime-button** - Type: Button - Button to proceed to showtime selection.

### 4. Showtime Selection Page
- **Page Title**: Select Showtime
- **Overview**: A page displaying available showtimes for the selected movie in different theaters.
- **Elements**:
  - **ID: showtime-page** - Type: Div - Container for the showtime page.
  - **ID: showtimes-list** - Type: Div - List of available showtimes with date, time, theater, and price.
  - **ID: theater-filter** - Type: Dropdown - Dropdown to filter showtimes by theater.
  - **ID: date-filter** - Type: Input - Field to filter showtimes by date.
  - **ID: select-showtime-button-{showtime_id}** - Type: Button - Button to select a specific showtime.

### 5. Seat Selection Page
- **Page Title**: Select Seats
- **Overview**: A page for users to select seats from an interactive seat map.
- **Elements**:
  - **ID: seat-selection-page** - Type: Div - Container for the seat selection page.
  - **ID: seat-map** - Type: Div - Interactive seat map showing available and booked seats.
  - **ID: selected-seats-display** - Type: Div - Display of currently selected seats.
  - **ID: seat-{row}{col}** - Type: Button - Individual seat button (e.g., seat-A1, seat-B3).
  - **ID: proceed-booking-button** - Type: Button - Button to proceed to booking confirmation.

### 6. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Overview**: A page for users to review booking details and complete the purchase.
- **Elements**:
  - **ID: confirmation-page** - Type: Div - Container for the confirmation page.
  - **ID: booking-summary** - Type: Div - Summary of booking details (movie, showtime, seats, total).
  - **ID: customer-name** - Type: Input - Field to input customer name.
  - **ID: customer-email** - Type: Input - Field to input customer email.
  - **ID: confirm-booking-button** - Type: Button - Button to confirm and complete booking.

### 7. Booking History Page
- **Page Title**: Booking History
- **Overview**: A page displaying all previous bookings with ticket information.
- **Elements**:
  - **ID: bookings-page** - Type: Div - Container for the bookings page.
  - **ID: bookings-table** - Type: Table - Table displaying bookings with booking ID, movie, date, seats, and status.
  - **ID: view-booking-button-{booking_id}** - Type: Button - Button to view booking details (each booking has this).
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Confirmed, Cancelled, Completed).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Theater Information Page
- **Page Title**: Theater Information
- **Overview**: A page displaying information about theaters and their facilities.
- **Elements**:
  - **ID: theater-page** - Type: Div - Container for the theater page.
  - **ID: theaters-list** - Type: Div - List of all theaters with location, screens, and facilities.
  - **ID: theater-location-filter** - Type: Dropdown - Dropdown to filter theaters by location.
  - **ID: facilities-display** - Type: Div - Display of theater facilities and amenities.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'MovieTicketing' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Movies Data
- **File Name**: `movies.txt`
- **Data Format**:
  ```
  movie_id|title|director|genre|rating|duration|description|release_date
  ```
- **Example Data**:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### 2. Theaters Data
- **File Name**: `theaters.txt`
- **Data Format**:
  ```
  theater_id|theater_name|location|city|screens|facilities
  ```
- **Example Data**:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### 3. Showtimes Data
- **File Name**: `showtimes.txt`
- **Data Format**:
  ```
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
  ```
- **Example Data**:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### 4. Seats Data
- **File Name**: `seats.txt`
- **Data Format**:
  ```
  seat_id|theater_id|screen_id|row|column|seat_type|status
  ```
- **Example Data**:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### 5. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
  ```
- **Example Data**:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### 6. Genres Data
- **File Name**: `genres.txt`
- **Data Format**:
  ```
  genre_id|genre_name|description
  ```
- **Example Data**:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
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
            """You are a Software System Architect specializing in Flask backend development and file-based data management using Python.

Your goal is to define the backend design to fully support the 'MovieTicketing' web application functionalities by specifying Flask routes, data file schemas, and backend operations based strictly on the user task description.

Task Details:
- Read user_task_description from CONTEXT
- Independently produce backend_design.md describing all necessary Flask routes and data schemas
- Define precise route paths, HTTP methods, and route functions to handle movie browsing, showtimes, seat selection, booking, and theater information
- Specify exact data file formats and field details to allow interaction with the local text data files
- Do not read or incorporate frontend_design.md or sibling outputs

**Section 1: Flask Routes and Backend Operations**
- List each route path, HTTP method, and its functionality
- For each route, specify required input parameters and returned data or rendered template context variables
- Describe interactions with data files: reads, writes, and updates with exact file names and field mappings

**Section 2: Data File Formats and Business Logic Contracts**
- Document each text data file schema as pipe-separated fields with field names and data types
- Provide field order, example rows, and constraints to ensure consistency
- Define backend logic rules such as seat availability checks and booking creation flow

CRITICAL SUCCESS CRITERIA:
- BackendDesignArchitect must produce a blueprint sufficient for implementation of a Flask app managing local text data per user requirements
- Use write_text_file tool exclusively to output backend_design.md
- Do not read sibling artifacts or add requirements beyond user_task_description

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a Frontend System Architect specializing in HTML template design and user interface specification for Flask-based web applications.

Your goal is to create complete frontend HTML template specifications with element IDs, context variables, and navigation flows, supporting the 'MovieTicketing' application features according to the user task description.

Task Details:
- Read user_task_description from CONTEXT
- Independently develop frontend_design.md describing all HTML templates, page titles, element IDs, and navigation mappings
- Specify templates for all eight pages including Dashboard, Movie Catalog, Movie Details, Showtime Selection, Seat Selection, Booking Confirmation, Booking History, and Theater Information
- Detail element IDs as specified in the user task, define all context variables passed to templates, and outline navigation and button actions
- Do not read or assume backend_design.md or sibling outputs

**Section 1: HTML Template Specifications**
- For each page, specify template filename and exact page title
- List all significant element IDs with their element types and descriptive roles
- Define all context variables passed into templates including their names, types, and expected values
- Map buttons and links to navigation flows (routes or dynamic actions)

CRITICAL SUCCESS CRITERIA:
- FrontendDesignArchitect must produce a template design enabling accurate UI implementation aligning with user_task_description
- Use write_text_file tool exclusively to output frontend_design.md
- Do not add requirements or read sibling artifacts

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect with expertise in consolidating backend and frontend designs into a consistent web application design specification.

Your goal is to merge backend_design.md and frontend_design.md into a single coherent design_spec.md that aligns precisely with the user task description and complies with both backend and frontend constraints.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Analyze and reconcile backend routes, data schemas, and frontend templates, element IDs, and navigation flows
- Resolve any discrepancies between element naming, route paths, context variable definitions, and navigation links
- Ensure the final design_spec.md is consistent, complete, and does not introduce new requirements beyond user_task_description and provided designs

**Section 1: Consolidated Backend and Frontend Specification**
- Present combined Flask route definitions with linked frontend template filenames
- Ensure context variables are aligned between backend routes and frontend templates
- Unify element IDs and navigation flows ensuring they correctly correspond to backend operations

**Section 2: Data Schema and Page Design Consistency**
- Validate that data file schemas support all frontend-displayed data and backend operations
- Confirm all pages and UI elements specified in frontend_design.md are supported by backend routes and data files
- Provide notes on any design consistency adjustments made

CRITICAL SUCCESS CRITERIA:
- DesignMerger must produce a final design_spec.md enabling seamless implementation by backend and frontend developers
- Use write_text_file tool exclusively to output design_spec.md
- Verify completeness, correctness, and consistency without adding features beyond input artifacts

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

Your goal is to implement a complete Flask backend according to the adaptive backend design in design_spec.md, including all routes, business logic, and data management using local text files.

Task Details:
- Read design_spec.md from CONTEXT focusing on backend routes, data schema, and logic
- Create app.py implementing independent backend functionality without dependency on frontend outputs
- Output app.py implementing all specified Flask routes, file reads/writes, and logic for the MovieTicketing application

**Implementation Requirements: Routes and Business Logic**
- Implement HTTP routes as specified, including URL paths, methods, and expected behaviors
- Perform all local text file data reads and writes as per data schema (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)
- Maintain data integrity and handle all business logic such as seat selection, booking processing, and data filtering

**Data File Handling**
- Use the specified pipe-delimited formats for all data files
- Implement robust parsing and writing functions compliant with the specified data schema
- Ensure consistency with design_spec.md’s data schema descriptions

**File and Project Structure**
- Place app.py at project root
- Do not include any frontend code here; focus strictly on backend implementation

CRITICAL SUCCESS CRITERIA:
- Fully functional Flask backend covering all backend_design.md routes and logic
- Correct input/output data handling with local text files
- Use write_text_file tool to save app.py
- Use validate_python_file tool to check syntax and runtime of app.py
- Write only the declared app.py output artifact

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML with Jinja2 templating for Flask web applications.

Your goal is to implement the full set of HTML templates according to the frontend design section in design_spec.md, respecting all specified element IDs, layout, and dynamic data placeholders.

Task Details:
- Read design_spec.md from CONTEXT focusing on frontend template specifications, element IDs, context variables, and navigation
- Create all necessary templates/*.html implementing the exact layout, element IDs, and placeholders
- Implement templates independent of backend source code; do not read any sibling outputs

**Template Structure and Content**
- Implement templates for all pages described including Dashboard, Movie Catalog, Movie Details, Showtime Selection, Seat Selection, Booking Confirmation, Booking History, and Theater Information
- Ensure element IDs exactly match those specified for each page
- Use Jinja2 syntax for dynamic data placeholders as defined in design_spec.md
- Implement navigation elements as per design_spec.md

**File and Project Structure**
- Place all template files in templates/ directory
- Follow naming conventions provided in design_spec.md or inferred from page titles

CRITICAL SUCCESS CRITERIA:
- Templates are complete, correctly structured, and matching element IDs and placeholders
- No dependencies on backend implementation details beyond design_spec.md
- Use write_text_file tool to save templates/*.html outputs
- Write only the declared templates/*.html output artifacts

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web applications combining backend and frontend implementations.

Your goal is to merge and reconcile independently developed app.py backend and templates/*.html frontend according to design_spec.md, resolving interface inconsistencies and producing a cohesive, fully functional final application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Identify mismatches in route URLs, template rendering calls, context variable names, and element IDs
- Reconcile app.py and templates/*.html for consistency without adding new features
- Correct interface and integration issues such as variable mismatches, missing routes, or template file names
- Validate app.py syntax and runtime correctness after merging fixes

**Consistency and Integration Requirements**
- Ensure all routes in app.py correspond to templates provided and vice versa
- Verify dynamic data placeholders in templates align with app.py context data
- Confirm navigation elements in templates link to existing backend routes
- Fix issues strictly within scope: interface consistency and integration correctness

**Output and Validation**
- Output merged and corrected app.py and templates/*.html
- Validate app.py using validate_python_file tool to ensure functionality
- Maintain original project structure and naming conventions

CRITICAL SUCCESS CRITERIA:
- Fully integrated, consistent backend and frontend codebase conforming to design_spec.md
- No functionality added beyond original designs
- Use write_text_file to output final app.py and templates/*.html
- Use validate_python_file tool to check final app.py syntax and runtime
- Write only the declared output artifacts app.py and templates/*.html

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'BackendDesignArchitect': [
        ("DesignMerger", """Verify backend design completeness, correctness, and compliance with requirements; ensure no conflicts with frontend design.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design completeness, correctness, element IDs, and navigation flows; ensure no conflicts with backend design.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend implementation against design_spec.md, verify routes, logic, and text file data handling correctness.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Check frontend templates against design_spec.md, verifying element IDs, dynamic data placeholders, layout, and navigation.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    DesignMerger = build_resilient_agent(
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(BackendDesignArchitect,
                "Create backend_design.md specifying all Flask routes, data schemas, and backend operations based solely on user_task_description."),
        execute(FrontendDesignArchitect,
                "Create frontend_design.md specifying all HTML templates, element IDs, context variables, and navigation flows based solely on user_task_description.")
    )

    # Read outputs from both architects
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

    # Merge backend and frontend designs into a consistent design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md ensuring design_spec.md is consistent, complete, and aligned with user_task_description.\n\n"
        f"=== backend_design.md ===\n{backend_design_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
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
        recovery_time=45
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=50
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement complete Flask backend in app.py based on design_spec.md backend routes, data schemas, and business logic."
        ),
        execute(
            FrontendDeveloper,
            "Implement full HTML templates in templates/*.html based on design_spec.md frontend layout, element IDs, context variables, and navigation."
        )
    )

    # After both backend and frontend complete, read latest app.py and templates/*.html for merger
    app_code = ""
    templates_content = ""
    try:
        app_code = open("app.py").read()
    except Exception:
        pass
    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {tpl_path} ===\n" + open(tpl_path).read()
        except Exception:
            pass

    # Execute IntegrationMerger to merge and reconcile backend and frontend artifacts
    await execute(
        IntegrationMerger,
        "Merge and reconcile app.py and templates/*.html for interface consistency and functional correctness according to design_spec.md.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== app.py ===\n{app_code}\n\n"
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
