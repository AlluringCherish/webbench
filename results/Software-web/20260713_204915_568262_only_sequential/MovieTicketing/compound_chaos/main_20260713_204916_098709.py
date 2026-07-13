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
# 20260713_204916_098709/main_20260713_204916_098709.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze user requirements and produce a comprehensive design_spec.md detailing pages, routes, elements, and data files.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst produces requirements_analysis.md based on the user task description; \"\n        \"WebArchitect then reads requirements_analysis.md to generate design_spec.md specifying Flask routes, page titles, element IDs, \"\n        \"data storage formats, and flexible parsing contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in software requirements elicitation and documentation.\n\nYour goal is to analyze the user's task description to identify and trace all user-visible pages, UI elements, data entities, and storage requirements, and produce a detailed requirements analysis document.\n\nTask Details:\n- Read user_task_description artifact thoroughly to extract all pages, elements, and data specifications\n- Produce requirements_analysis.md with exact tracing of each page's purpose, elements with IDs and types, and data file formats\n- Ensure complete coverage of the eight specified web pages and six data files as described by the user\n- Include precise descriptions of UI elements and their functionalities\n\nDocumentation Requirements:\n1. Pages and UI Elements:\n   - List each page with its title and overview\n   - Enumerate all element IDs per page with type (Div, Button, Input, etc.) and role\n   - Include dynamic element ID patterns (e.g., view-movie-button-{movie_id})\n\n2. Data Entities and Storage:\n   - List each data file by filename with field names and order\n   - Provide examples illustrating data content format\n   - Note parsing constraints such as delimiter usage and no header lines\n\n3. Navigation and Functional Flow:\n   - Detail navigation flows between pages via buttons and links\n   - Specify filters and dropdown options where applicable\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output the requirements_analysis.md file\n- Preserve exact input artifact content structure and terminology\n- Provide clear, concise, and comprehensive tracing suitable for technical translation by WebArchitect\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and specification.\n\nYour goal is to convert the detailed requirements analysis into a comprehensive design specification document that defines all Flask routes, HTTP methods, page titles, element IDs, navigation flows, and data parsing contracts for text files.\n\nTask Details:\n- Read requirements_analysis.md and user_task_description artifacts\n- Produce design_spec.md that specifies:\n  - Flask routes with URL patterns, function names, HTTP methods (GET/POST)\n  - Page titles and exact page container element IDs\n  - All UI element IDs with types for each page, including dynamic formats\n  - Navigation mappings between pages via buttons and links using url_for functions\n  - Data file contracts specifying filenames, field order, delimiters, and example data\n- Ensure parsing contracts are detailed and reflect flexible but exact requirements from the data files\n- Define a complete contract for all six specified data files with field names and examples\n\nDesign Specification Requirements:\n1. Flask Routes Specification:\n   - List all routes by URL pattern and function name (snake_case)\n   - Specify method (GET or POST) per route\n   - Specify template file to render per route\n   - Include context variables and their types passed to templates\n\n2. Page and Element Specification:\n   - Exactly specify page container IDs and page titles\n   - List all element IDs per page with element types (Div, Button, Input, Dropdown, Table, etc.)\n   - Specify patterns for dynamic element IDs with placeholders\n\n3. Navigation Flow:\n   - Map all navigation buttons to corresponding routes via url_for\n   - Include static and dynamic navigations (with parameters)\n\n4. Data Parsing Contracts:\n   - For each data file, specify:\n     - Filename and path (data/)\n     - Exact field order using pipe '|' delimiter\n     - Data description\n     - 2-3 realistic example rows from user data\n   - Note absence of header lines and parsing approach\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- Follow user task definitions strictly without assumptions\n- Ensure consistency of element IDs between navigation and pages\n- Provide clear and unambiguous specifications for backend developers\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md contains complete and accurate tracing of all user-visible pages, elements, \"\n                \"and data storage requirements before architecture proceeds.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the MovieTicketing Flask web application with exact requested routes, templates, and data handling.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineer writes app_draft.py and all templates_draft/*.html from design_spec.md; \"\n        \"IntegrationEngineer then refines these drafts into final app.py and templates/*.html enforcing exact routes, element IDs, and data parsing.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineer\",\n            \"prompt\": \"\"\"You are a Flask web developer specializing in Python web applications.\n\nYour goal is to develop a draft Flask application and all required HTML templates implementing the specifications for a movie ticketing system.\n\nTask Details:\n- Read design_spec.md and user_task_description thoroughly\n- Produce a draft Flask app named app_draft.py including routes for all 8 pages\n- Create draft HTML templates under templates_draft/ with correct page titles and all specified element IDs\n- Implement navigation buttons as specified to enable page transitions starting from Dashboard\n- Parse local text-based data files as described, ensuring data fields and formats align with design spec and user task\n\nImplementation Requirements:\n1. **Flask App Structure**:\n   - Use Flask routing and view functions\n   - Define routes matching all 8 pages and their functionalities\n   - Ensure the '/' route redirects to Dashboard page route\n   - Use render_template() referencing templates in templates_draft/\n\n2. **Data Handling**:\n   - Load and parse text data files locally with exact field orders and pipe-delimited format\n   - Handle files: movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt\n   - Prepare data as dicts or lists for passing to templates\n\n3. **Templates Drafts**:\n   - Place template files in templates_draft/ directory\n   - Implement specified element IDs exactly as per user task page design\n   - Include page titles matching specified titles in <title> and <h1> tags\n   - Include navigation buttons with IDs to transition between pages\n   - Implement dynamic IDs using Jinja2 where applicable (e.g., view-movie-button-{movie_id})\n\n4. **Routing and Navigation**:\n   - Ensure all navigation buttons and links use url_for() pointing to correct Flask route functions\n   - Navigation must start from Dashboard page on app launch\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to output app_draft.py and all templates in templates_draft/\n- Maintain exact element ID naming and page titles as per user task\n- Follow data file formats exactly for loading and parsing\n- The draft app and templates must be functional but can allow placeholder content where required\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Python Flask integration specialist experienced in refining draft web applications.\n\nYour goal is to refine the draft Flask app and HTML templates into final production-ready code that strictly conforms to all route specifications, element IDs, and data parsing rules for the movie ticketing system.\n\nTask Details:\n- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description\n- Produce finalized app.py implementing all routes starting from Dashboard page with exact route behaviors\n- Refine templates/*.html from templates_draft/ enforcing exact element IDs and layout consistency\n- Ensure stable, robust parsing of all local text-based data files as specified (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)\n- Enforce all navigation buttons and links correspond to correct Flask routes\n\nRefinement Requirements:\n1. **Routing**:\n   - Confirm '/' route redirects accurately to Dashboard route\n   - Validate that all endpoints precisely match design_spec.md definitions\n   - Ensure HTTP methods and route parameters are correctly handled\n\n2. **Templates**:\n   - Adopt all element IDs exactly as specified without deviation\n   - Maintain accurate page titles in <title> and <h1>\n   - Fix any draft template inconsistencies in layout or element presence\n\n3. **Data Handling**:\n   - Confirm data files are parsed with correct delimiter and exact field orders\n   - Include error handling for file reading\n   - Data passed to templates must match design specification exactly\n\n4. **Final Integration**:\n   - Test navigation flows start from Dashboard with all buttons functional\n   - Ensure no placeholder content remains; all pages fully implement their data presentation\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to output final app.py and all templates in templates/\n- Strictly maintain all element IDs and route names as defined\n- Data parsing must be robust and conform exactly to file schemas\n- Final code and templates must be complete and production-ready\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Review app_draft.py and templates_draft/*.html to ensure full compliance with design_spec.md, including correct routes, \"\n                \"element IDs, and local file data handling.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the completed app.py and templates/*.html for correctness, completeness, and runnability.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator runs syntax and runtime validation on app.py and templates/*.html, producing validation_report.md; \"\n        \"SequentialFixer then applies fixes and writes final artifacts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application validation and verification.\n\nYour goal is to thoroughly validate the app.py and HTML templates, ensuring correctness in syntax, runtime stability, route handling, and compliance with the design specification. Deliver a detailed validation_report.md documenting all findings.\n\nTask Details:\n- Read design_spec.md, app.py, templates/*.html, and user_task_description from CONTEXT\n- Validate app.py for Python syntax and runtime errors using tools\n- Validate templates/*.html for correct structure, element IDs, and content matching design_spec.md\n- Verify all Flask routes exist and handle requests as specified in design_spec.md\n- Check stable interaction with data files (file paths, parsing, field orders)\n- Produce validation_report.md with all validation results and issues found\n\nValidation Requirements:\n1. **Syntax Validation**:\n   - Use validate_python_file tool on app.py\n   - Identify any syntax or runtime errors preventing app start\n\n2. **Runtime Testing**:\n   - Use execute_python_code tool to run app.py minimally to detect runtime exceptions on start\n\n3. **Design Compliance**:\n   - Confirm routes in app.py match design_spec.md Section 1 (function names, decorators)\n   - Confirm context variables passed to templates correspond exactly to design_spec.md\n   - Validate templates/*.html contain all required element IDs and match design_spec.md Section 2 content and structure\n   - Check page titles and navigation mappings are accurate\n\n4. **Data File Handling**:\n   - Check file paths and loading logic in app.py match design_spec.md Section 3\n   - Verify data parsing uses correct field order, no headers assumed unless specified\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for code verification\n- Use write_text_file tool to output validation_report.md documenting all findings with examples\n- Provide clear, actionable comments for any issues discovered\n- Focus strictly on inputs given; do not extend beyond specified artifacts\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in automated code correction and integration for Flask web applications.\n\nYour goal is to apply necessary corrections from the provided validation_report.md to finalize app.py and templates/*.html, ensuring the entire MovieTicketing application fully meets all user requirements and design specifications.\n\nTask Details:\n- Read validation_report.md, design_spec.md, app.py, templates/*.html, and user_task_description from CONTEXT\n- Identify all issues flagged in validation_report.md\n- Correct app.py syntax, runtime, route handling, and data file usage errors\n- Fix templates/*.html defects including missing element IDs, incorrect content, navigation, and title mismatches\n- Maintain full compliance with design_spec.md and user_task_description\n- Deliver corrected artifact files: app.py and templates/*.html\n\nCorrection Requirements:\n1. **Code Corrections**:\n   - Fix all syntax and runtime errors preventing proper app operation\n   - Ensure routes correspond exactly with design_spec.md Section 1 specifications\n   - Verify all context variables are consistent and complete\n\n2. **Template Corrections**:\n   - Add or fix missing element IDs and ensure exact naming\n   - Adjust page titles and navigation buttons as per design_spec.md Section 2\n   - Preserve Jinja2 templating where applicable and test for rendering readiness\n\n3. **Data Handling**:\n   - Confirm data file loads parse fields in exact order as design_spec.md Section 3\n   - Do not introduce new features beyond fixing reported issues\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save corrected app.py and templates/*.html\n- Fully resolve all issues reported in validation_report.md with traceability to requirements\n- Maintain original artifact file names and formats exactly\n- Focus exclusively on artifacts listed; do not generate unrelated files\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Ensure that validation_report.md accurately identifies syntax, runtime, and design compliance issues.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify that final app.py and templates/*.html fully resolve all issues from validation_report.md while maintaining full \"\n                \"traceability to user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Business Analyst specializing in software requirements elicitation and documentation.

Your goal is to analyze the user's task description to identify and trace all user-visible pages, UI elements, data entities, and storage requirements, and produce a detailed requirements analysis document.

Task Details:
- Read user_task_description artifact thoroughly to extract all pages, elements, and data specifications
- Produce requirements_analysis.md with exact tracing of each page's purpose, elements with IDs and types, and data file formats
- Ensure complete coverage of the eight specified web pages and six data files as described by the user
- Include precise descriptions of UI elements and their functionalities

Documentation Requirements:
1. Pages and UI Elements:
   - List each page with its title and overview
   - Enumerate all element IDs per page with type (Div, Button, Input, etc.) and role
   - Include dynamic element ID patterns (e.g., view-movie-button-{movie_id})

2. Data Entities and Storage:
   - List each data file by filename with field names and order
   - Provide examples illustrating data content format
   - Note parsing constraints such as delimiter usage and no header lines

3. Navigation and Functional Flow:
   - Detail navigation flows between pages via buttons and links
   - Specify filters and dropdown options where applicable

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output the requirements_analysis.md file
- Preserve exact input artifact content structure and terminology
- Provide clear, concise, and comprehensive tracing suitable for technical translation by WebArchitect

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design and specification.

Your goal is to convert the detailed requirements analysis into a comprehensive design specification document that defines all Flask routes, HTTP methods, page titles, element IDs, navigation flows, and data parsing contracts for text files.

Task Details:
- Read requirements_analysis.md and user_task_description artifacts
- Produce design_spec.md that specifies:
  - Flask routes with URL patterns, function names, HTTP methods (GET/POST)
  - Page titles and exact page container element IDs
  - All UI element IDs with types for each page, including dynamic formats
  - Navigation mappings between pages via buttons and links using url_for functions
  - Data file contracts specifying filenames, field order, delimiters, and example data
- Ensure parsing contracts are detailed and reflect flexible but exact requirements from the data files
- Define a complete contract for all six specified data files with field names and examples

Design Specification Requirements:
1. Flask Routes Specification:
   - List all routes by URL pattern and function name (snake_case)
   - Specify method (GET or POST) per route
   - Specify template file to render per route
   - Include context variables and their types passed to templates

2. Page and Element Specification:
   - Exactly specify page container IDs and page titles
   - List all element IDs per page with element types (Div, Button, Input, Dropdown, Table, etc.)
   - Specify patterns for dynamic element IDs with placeholders

3. Navigation Flow:
   - Map all navigation buttons to corresponding routes via url_for
   - Include static and dynamic navigations (with parameters)

4. Data Parsing Contracts:
   - For each data file, specify:
     - Filename and path (data/)
     - Exact field order using pipe '|' delimiter
     - Data description
     - 2-3 realistic example rows from user data
   - Note absence of header lines and parsing approach

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Follow user task definitions strictly without assumptions
- Ensure consistency of element IDs between navigation and pages
- Provide clear and unambiguous specifications for backend developers

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineer": {
        "prompt": (
            """You are a Flask web developer specializing in Python web applications.

Your goal is to develop a draft Flask application and all required HTML templates implementing the specifications for a movie ticketing system.

Task Details:
- Read design_spec.md and user_task_description thoroughly
- Produce a draft Flask app named app_draft.py including routes for all 8 pages
- Create draft HTML templates under templates_draft/ with correct page titles and all specified element IDs
- Implement navigation buttons as specified to enable page transitions starting from Dashboard
- Parse local text-based data files as described, ensuring data fields and formats align with design spec and user task

Implementation Requirements:
1. **Flask App Structure**:
   - Use Flask routing and view functions
   - Define routes matching all 8 pages and their functionalities
   - Ensure the '/' route redirects to Dashboard page route
   - Use render_template() referencing templates in templates_draft/

2. **Data Handling**:
   - Load and parse text data files locally with exact field orders and pipe-delimited format
   - Handle files: movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt
   - Prepare data as dicts or lists for passing to templates

3. **Templates Drafts**:
   - Place template files in templates_draft/ directory
   - Implement specified element IDs exactly as per user task page design
   - Include page titles matching specified titles in <title> and <h1> tags
   - Include navigation buttons with IDs to transition between pages
   - Implement dynamic IDs using Jinja2 where applicable (e.g., view-movie-button-{movie_id})

4. **Routing and Navigation**:
   - Ensure all navigation buttons and links use url_for() pointing to correct Flask route functions
   - Navigation must start from Dashboard page on app launch

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to output app_draft.py and all templates in templates_draft/
- Maintain exact element ID naming and page titles as per user task
- Follow data file formats exactly for loading and parsing
- The draft app and templates must be functional but can allow placeholder content where required

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Python Flask integration specialist experienced in refining draft web applications.

Your goal is to refine the draft Flask app and HTML templates into final production-ready code that strictly conforms to all route specifications, element IDs, and data parsing rules for the movie ticketing system.

Task Details:
- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description
- Produce finalized app.py implementing all routes starting from Dashboard page with exact route behaviors
- Refine templates/*.html from templates_draft/ enforcing exact element IDs and layout consistency
- Ensure stable, robust parsing of all local text-based data files as specified (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)
- Enforce all navigation buttons and links correspond to correct Flask routes

Refinement Requirements:
1. **Routing**:
   - Confirm '/' route redirects accurately to Dashboard route
   - Validate that all endpoints precisely match design_spec.md definitions
   - Ensure HTTP methods and route parameters are correctly handled

2. **Templates**:
   - Adopt all element IDs exactly as specified without deviation
   - Maintain accurate page titles in <title> and <h1>
   - Fix any draft template inconsistencies in layout or element presence

3. **Data Handling**:
   - Confirm data files are parsed with correct delimiter and exact field orders
   - Include error handling for file reading
   - Data passed to templates must match design specification exactly

4. **Final Integration**:
   - Test navigation flows start from Dashboard with all buttons functional
   - Ensure no placeholder content remains; all pages fully implement their data presentation

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to output final app.py and all templates in templates/
- Strictly maintain all element IDs and route names as defined
- Data parsing must be robust and conform exactly to file schemas
- Final code and templates must be complete and production-ready

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'ImplementationEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application validation and verification.

Your goal is to thoroughly validate the app.py and HTML templates, ensuring correctness in syntax, runtime stability, route handling, and compliance with the design specification. Deliver a detailed validation_report.md documenting all findings.

Task Details:
- Read design_spec.md, app.py, templates/*.html, and user_task_description from CONTEXT
- Validate app.py for Python syntax and runtime errors using tools
- Validate templates/*.html for correct structure, element IDs, and content matching design_spec.md
- Verify all Flask routes exist and handle requests as specified in design_spec.md
- Check stable interaction with data files (file paths, parsing, field orders)
- Produce validation_report.md with all validation results and issues found

Validation Requirements:
1. **Syntax Validation**:
   - Use validate_python_file tool on app.py
   - Identify any syntax or runtime errors preventing app start

2. **Runtime Testing**:
   - Use execute_python_code tool to run app.py minimally to detect runtime exceptions on start

3. **Design Compliance**:
   - Confirm routes in app.py match design_spec.md Section 1 (function names, decorators)
   - Confirm context variables passed to templates correspond exactly to design_spec.md
   - Validate templates/*.html contain all required element IDs and match design_spec.md Section 2 content and structure
   - Check page titles and navigation mappings are accurate

4. **Data File Handling**:
   - Check file paths and loading logic in app.py match design_spec.md Section 3
   - Verify data parsing uses correct field order, no headers assumed unless specified

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for code verification
- Use write_text_file tool to output validation_report.md documenting all findings with examples
- Provide clear, actionable comments for any issues discovered
- Focus strictly on inputs given; do not extend beyond specified artifacts

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Engineer specializing in automated code correction and integration for Flask web applications.

Your goal is to apply necessary corrections from the provided validation_report.md to finalize app.py and templates/*.html, ensuring the entire MovieTicketing application fully meets all user requirements and design specifications.

Task Details:
- Read validation_report.md, design_spec.md, app.py, templates/*.html, and user_task_description from CONTEXT
- Identify all issues flagged in validation_report.md
- Correct app.py syntax, runtime, route handling, and data file usage errors
- Fix templates/*.html defects including missing element IDs, incorrect content, navigation, and title mismatches
- Maintain full compliance with design_spec.md and user_task_description
- Deliver corrected artifact files: app.py and templates/*.html

Correction Requirements:
1. **Code Corrections**:
   - Fix all syntax and runtime errors preventing proper app operation
   - Ensure routes correspond exactly with design_spec.md Section 1 specifications
   - Verify all context variables are consistent and complete

2. **Template Corrections**:
   - Add or fix missing element IDs and ensure exact naming
   - Adjust page titles and navigation buttons as per design_spec.md Section 2
   - Preserve Jinja2 templating where applicable and test for rendering readiness

3. **Data Handling**:
   - Confirm data file loads parse fields in exact order as design_spec.md Section 3
   - Do not introduce new features beyond fixing reported issues

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html
- Fully resolve all issues reported in validation_report.md with traceability to requirements
- Maintain original artifact file names and formats exactly
- Focus exclusively on artifacts listed; do not generate unrelated files

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md contains complete and accurate tracing of all user-visible pages, elements, "
                "and data storage requirements before architecture proceeds.""", [{'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'ImplementationEngineer': [
        ("IntegrationEngineer", """Review app_draft.py and templates_draft/*.html to ensure full compliance with design_spec.md, including correct routes, "
                "element IDs, and local file data handling.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Ensure that validation_report.md accurately identifies syntax, runtime, and design compliance issues.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify that final app.py and templates/*.html fully resolve all issues from validation_report.md while maintaining full "
                "traceability to user requirements.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    # Build agents
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=260,
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
        max_retries=3,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md covering all pages, UI elements, data files, navigation flows")

    # Read requirements_analysis.md content to inject for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except Exception:
        pass

    await execute(WebArchitect,
                  f"Based on requirements_analysis.md and user_task_description, produce design_spec.md specifying Flask routes, pages, element IDs, navigation, and data file contracts.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Create agents
    ImplementationEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
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
        failure_threshold=2,
        recovery_time=50
    )

    # Execute ImplementationEngineer first
    await execute(ImplementationEngineer,
                  "Develop draft Flask app named app_draft.py with all 8 routes, "
                  "and create draft HTML templates under templates_draft/ with exact page titles and element IDs. "
                  "Include navigation buttons for page transitions starting from Dashboard. "
                  "Parse local text-based data files with exact formats.")

    # Read draft app and draft templates for injection
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # Note: For templates_draft/*.html, since this is a wildcard, just read as empty or not read here explicitly.
        # Agents should read these internally, but requirement states to inject content for subsequent calls when refinement loop or debate patterns,
        # Here, we won't read all templates files individually, just pass message referencing them
        templates_draft_content = ""  
    except:
        pass

    # Execute IntegrationEngineer with injected draft app and templates content
    await execute(IntegrationEngineer,
                  "Refine draft app_draft.py and templates_draft/*.html into final app.py and templates/*.html "
                  "enforcing exact routes, element IDs, and data parsing from design_spec.md. "
                  "Start routing from Dashboard page with exact route behaviors. "
                  "Ensure robust file parsing and accurate navigation buttons. "                   
                  f"=== app_draft.py ===\n{app_draft_content}\n"
                  f"=== templates_draft/*.html ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    WebValidator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=50
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
        recovery_time=50
    )

    # Execute WebValidator first for full validation and produce validation_report.md
    await execute(WebValidator, 
                  "Validate app.py using validate_python_file and execute_python_code tools. "
                  "Validate templates/*.html for structure, element IDs, and design_spec.md compliance. "
                  "Check Flask routes, context variables, and data file handling against design_spec.md sections. "
                  "Produce detailed validation_report.md with all findings and actionable comments.")

    # Read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    # SequentialFixer applies fixes based on validation_report.md
    await execute(SequentialFixer,
                  f"Fix all issues identified in validation_report.md to finalize app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md and user requirements. "
                  f"Maintain artifact file names and formats.\n\n=== Validation Report ===\n{validation_report_content}")
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
