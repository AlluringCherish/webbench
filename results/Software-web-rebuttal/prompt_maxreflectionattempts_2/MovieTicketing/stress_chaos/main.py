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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complete design specification for MovieTicketing app covering Flask routes, HTML templates, and data schemas enabling parallel implementation\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect creates design_spec.md detailing Flask routes with function names, context variables, HTTP methods; HTML template element IDs and structure; \"\n        \"data schema formats for all data files necessary for independent backend/fronted development.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create a comprehensive design specification document that enables Backend and Frontend developers to work independently and in parallel on the MovieTicketing application.\n\nTask Details:\n- Read the entire user_task_description from CONTEXT\n- Produce design_spec.md containing three distinct sections optimized for parallel development:\n  1) Flask routes with function names, HTTP methods, and complete context variables\n  2) HTML template specifications with all element IDs, page titles, and navigation details\n  3) Data file schemas with exact field order and pipe-delimited format for all data files\n- Do NOT assume or include implementation details beyond specifications or actual code beyond what is required for clear specs\n\n**Section 1: Flask Routes Specification**\n\nSpecify a complete route list with:\n- Route path (e.g., /dashboard, /movies/<int:movie_id>)\n- Function name (use clear, consistent lowercase with underscores)\n- HTTP method (GET, POST)\n- Template file rendered\n- All context variables passed to template with explicit types (str, int, float, list, dict)\n- For any list of dict, provide field structures precisely\n\nEnsure:\n- Root route '/' redirects to dashboard page\n- Include all pages specified in the user requirements with correct route patterns, including dynamic routes\n\n**Section 2: HTML Template Specifications**\n\nFor each page template:\n- Provide exact filename (e.g., templates/dashboard.html)\n- Specify page title for <title> and <h1>\n- List all required element IDs with element types and usage descriptions\n- Detail dynamic elements with patterns for IDs (e.g., view-movie-button-{movie_id})\n- Specify navigation mapping for buttons/links to Flask routes using url_for() naming conventions matching Section 1 function names\n\n**Section 3: Data File Schemas**\n\nFor each data file in the data directory:\n- Specify filename and relative path (data/{filename}.txt)\n- Define exact field order separated by pipes (|)\n- Provide brief description of content\n- Include 2-3 realistic example rows from user requirements\n\nRequirements:\n- Field order MUST be exact for backend parsing\n- Use pipe '|' delimiter exclusively\n- No header lines in the data files\n\nCRITICAL SUCCESS CRITERIA:\n- The design specification must allow backend and frontend teams to implement their components fully independently without communication\n- All route names, function names, context variables, and template element IDs must be consistent and match exactly between sections\n- The specification supports exact reproduction of all user task requirements\n- Use write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Review design_spec.md Section 1 and 3 for backend completeness: \"\n                \"All specified Flask routes correspond to user requirements, including function names, context variable correctness, HTTP methods, \"\n                \"and data schemas are correctly formatted with exact field order.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Review design_spec.md Section 2 for frontend completeness: \"\n                \"All HTML templates specified with exact element IDs, page layout requirements, and navigation details matching the user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend independently in parallel using design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with all Flask routes and data access based on design_spec.md Sections 1 and 3. \"\n        \"FrontendDeveloper implements all HTML templates (*.html) based on design_spec.md Section 2.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application that fulfills all specified routes with correct HTTP methods, properly loads and saves data files as defined in data schemas, and ensures the root route redirects to the dashboard page.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) from CONTEXT only\n- Implement all Flask routes with exact function names, HTTP methods, template rendering, and context variables\n- Load and save data using the exact schemas and formats defined in Section 3\n- Do NOT read or implement anything from frontend template specifications (Section 2)\n- Do NOT assume any authentication requirement or add features beyond specifications\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   - Initialize the Flask app with a secret key\n   - Include standard imports: flask, render_template, redirect, url_for, request\n\n2. **Root Route**:\n   - Implement '/' route that performs redirect to the dashboard page route\n\n3. **Data File Handling**:\n   - Load all data files from data/*.txt with pipe-delimited parsing\n   - Parse files without header lines, matching exact field orders specified in Section 3\n   - Implement robust error handling for file I/O\n   - Save updates back to the appropriate files when necessary, maintaining schema and format\n\n4. **Route Implementations**:\n   - Include all routes specified in Section 1 with their HTTP methods\n   - For each route, render the specified template and pass all context variables exactly as defined\n   - Handle POST form submissions as specified\n   - Implement data filtering, searching, and mutation functionalities per route specification\n\n5. **Best Practices**:\n   - Use url_for for all redirects and links within the backend\n   - Organize code for clarity and modularity\n   - Add main guard: if __name__ == '__main__': app.run()\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the final app.py\n- Follow naming and typing conventions exactly as specified in design_spec.md Sections 1 and 3\n- Do NOT include frontend template implementation or references to Section 2 contents\n- Ensure root route redirects to dashboard as specified\n- Do NOT provide code snippets only via chat—always save the output file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask-based web applications.\n\nYour goal is to implement all HTML templates (*.html) with complete page structures, element IDs, and navigation controls, strictly following the specifications in design_spec.md Section 2.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) from CONTEXT only\n- Implement all HTML templates with exact element IDs, page titles, and context variables\n- Use Jinja2 syntax for dynamic content and loops\n- Implement all navigation controls using correct url_for functions as specified\n- Do NOT read or implement backend logic, data schemas, or routes (Sections 1 and 3)\n- Do NOT assume authentication or add features outside spec\n\nImplementation Requirements:\n1. **Template Structure**:\n   - Include <!DOCTYPE html>, <html>, <head> with exact <title>, and <body> with content divs\n   - Use exact element IDs for all divs, buttons, inputs, tables, etc.\n   - For dynamic IDs (e.g., view-movie-button-{movie_id}), use Jinja2 syntax: id=\"view-movie-button-{{ movie.movie_id }}\"\n\n2. **Context Variables**:\n   - Access context variables exactly as specified\n   - Use loops and conditionals where required\n\n3. **Navigation and Links**:\n   - Implement all navigation controls with url_for referencing function names from Section 1\n   - For dynamic parameters, use correct Jinja2 syntax: url_for('function_name', id=item.id)\n\n4. **Forms and Buttons**:\n   - Use appropriate form methods and action URLs as specified\n   - Include all specified input fields and submission buttons with proper IDs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files under templates/ directory\n- All element IDs and page titles must match design_spec.md Section 2 exactly (case-sensitive)\n- Navigation url_for function names and parameters must be exact matches\n- Do NOT add any extra pages or elements not specified\n- Do NOT provide code snippets only via chat—always save the actual template files\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all specified Flask routes correctly, uses correct HTTP methods, context variables, and \"\n                \"data loading/saving follows data schemas defined in design_spec.md Sections 1 and 3. Confirm root route redirects to dashboard.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify templates/*.html implement all page elements with exact IDs, correct navigation using url_for, and page titles exactly match design_spec.md Section 2.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create a comprehensive design specification document that enables Backend and Frontend developers to work independently and in parallel on the MovieTicketing application.

Task Details:
- Read the entire user_task_description from CONTEXT
- Produce design_spec.md containing three distinct sections optimized for parallel development:
  1) Flask routes with function names, HTTP methods, and complete context variables
  2) HTML template specifications with all element IDs, page titles, and navigation details
  3) Data file schemas with exact field order and pipe-delimited format for all data files
- Do NOT assume or include implementation details beyond specifications or actual code beyond what is required for clear specs

**Section 1: Flask Routes Specification**

Specify a complete route list with:
- Route path (e.g., /dashboard, /movies/<int:movie_id>)
- Function name (use clear, consistent lowercase with underscores)
- HTTP method (GET, POST)
- Template file rendered
- All context variables passed to template with explicit types (str, int, float, list, dict)
- For any list of dict, provide field structures precisely

Ensure:
- Root route '/' redirects to dashboard page
- Include all pages specified in the user requirements with correct route patterns, including dynamic routes

**Section 2: HTML Template Specifications**

For each page template:
- Provide exact filename (e.g., templates/dashboard.html)
- Specify page title for <title> and <h1>
- List all required element IDs with element types and usage descriptions
- Detail dynamic elements with patterns for IDs (e.g., view-movie-button-{movie_id})
- Specify navigation mapping for buttons/links to Flask routes using url_for() naming conventions matching Section 1 function names

**Section 3: Data File Schemas**

For each data file in the data directory:
- Specify filename and relative path (data/{filename}.txt)
- Define exact field order separated by pipes (|)
- Provide brief description of content
- Include 2-3 realistic example rows from user requirements

Requirements:
- Field order MUST be exact for backend parsing
- Use pipe '|' delimiter exclusively
- No header lines in the data files

CRITICAL SUCCESS CRITERIA:
- The design specification must allow backend and frontend teams to implement their components fully independently without communication
- All route names, function names, context variables, and template element IDs must be consistent and match exactly between sections
- The specification supports exact reproduction of all user task requirements
- Use write_text_file tool to output design_spec.md

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

Your goal is to implement a complete Flask backend application that fulfills all specified routes with correct HTTP methods, properly loads and saves data files as defined in data schemas, and ensures the root route redirects to the dashboard page.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) from CONTEXT only
- Implement all Flask routes with exact function names, HTTP methods, template rendering, and context variables
- Load and save data using the exact schemas and formats defined in Section 3
- Do NOT read or implement anything from frontend template specifications (Section 2)
- Do NOT assume any authentication requirement or add features beyond specifications

Implementation Requirements:
1. **Flask Application Setup**:
   - Initialize the Flask app with a secret key
   - Include standard imports: flask, render_template, redirect, url_for, request

2. **Root Route**:
   - Implement '/' route that performs redirect to the dashboard page route

3. **Data File Handling**:
   - Load all data files from data/*.txt with pipe-delimited parsing
   - Parse files without header lines, matching exact field orders specified in Section 3
   - Implement robust error handling for file I/O
   - Save updates back to the appropriate files when necessary, maintaining schema and format

4. **Route Implementations**:
   - Include all routes specified in Section 1 with their HTTP methods
   - For each route, render the specified template and pass all context variables exactly as defined
   - Handle POST form submissions as specified
   - Implement data filtering, searching, and mutation functionalities per route specification

5. **Best Practices**:
   - Use url_for for all redirects and links within the backend
   - Organize code for clarity and modularity
   - Add main guard: if __name__ == '__main__': app.run()

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the final app.py
- Follow naming and typing conventions exactly as specified in design_spec.md Sections 1 and 3
- Do NOT include frontend template implementation or references to Section 2 contents
- Ensure root route redirects to dashboard as specified
- Do NOT provide code snippets only via chat—always save the output file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask-based web applications.

Your goal is to implement all HTML templates (*.html) with complete page structures, element IDs, and navigation controls, strictly following the specifications in design_spec.md Section 2.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) from CONTEXT only
- Implement all HTML templates with exact element IDs, page titles, and context variables
- Use Jinja2 syntax for dynamic content and loops
- Implement all navigation controls using correct url_for functions as specified
- Do NOT read or implement backend logic, data schemas, or routes (Sections 1 and 3)
- Do NOT assume authentication or add features outside spec

Implementation Requirements:
1. **Template Structure**:
   - Include <!DOCTYPE html>, <html>, <head> with exact <title>, and <body> with content divs
   - Use exact element IDs for all divs, buttons, inputs, tables, etc.
   - For dynamic IDs (e.g., view-movie-button-{movie_id}), use Jinja2 syntax: id="view-movie-button-{{ movie.movie_id }}"

2. **Context Variables**:
   - Access context variables exactly as specified
   - Use loops and conditionals where required

3. **Navigation and Links**:
   - Implement all navigation controls with url_for referencing function names from Section 1
   - For dynamic parameters, use correct Jinja2 syntax: url_for('function_name', id=item.id)

4. **Forms and Buttons**:
   - Use appropriate form methods and action URLs as specified
   - Include all specified input fields and submission buttons with proper IDs

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files under templates/ directory
- All element IDs and page titles must match design_spec.md Section 2 exactly (case-sensitive)
- Navigation url_for function names and parameters must be exact matches
- Do NOT add any extra pages or elements not specified
- Do NOT provide code snippets only via chat—always save the actual template files

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
        ("BackendDeveloper", """Review design_spec.md Section 1 and 3 for backend completeness: "
                "All specified Flask routes correspond to user requirements, including function names, context variable correctness, HTTP methods, "
                "and data schemas are correctly formatted with exact field order.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Review design_spec.md Section 2 for frontend completeness: "
                "All HTML templates specified with exact element IDs, page layout requirements, and navigation details matching the user requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all specified Flask routes correctly, uses correct HTTP methods, context variables, and "
                "data loading/saving follows data schemas defined in design_spec.md Sections 1 and 3. Confirm root route redirects to dashboard.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify templates/*.html implement all page elements with exact IDs, correct navigation using url_for, and page titles exactly match design_spec.md Section 2.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],


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
    await execute(SystemArchitect, "Create design_spec.md with comprehensive Flask routes, HTML templates, and data schemas for MovieTicketing app enabling parallel backend/frontend development")
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
        recovery_time=30
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py backend using design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all HTML templates using design_spec.md Section 2")
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
