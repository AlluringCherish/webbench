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
# 20260714_001749_789281/main_20260714_001749_789281.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the MovieTicketing web app design contract with page structure, element IDs, navigation, and data management; deliver design_spec.md and design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator creates or revises design_spec.md based on user_task_description and previous design_feedback.md; DesignCritic reviews and writes design_feedback.md indicating approval or needed modifications.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Python web application design specifications.\n\nYour goal is to design and iteratively refine a complete MovieTicketing web application design contract for at most two iterations, including page structures, UI element IDs, navigation flows, and data storage formats.\n\nTask Details:\n- Read the user_task_description from CONTEXT for full project requirements\n- Read current design_spec.md and design_feedback.md when present\n- On the first iteration, produce a comprehensive design_spec.md detailing all pages, UI element IDs, navigation, and exact data file formats\n- When design_feedback.md begins with NEED_MODIFY, apply all correction feedback and rewrite the complete design_spec.md artifact\n- Stop immediately on [APPROVED] feedback without further changes\n\n**Section 1: Page and UI Element Specification**\n- Define all eight specified pages with exact page titles and container element IDs\n- Specify all UI elements with their exact IDs, types, and purposes as per user requirements\n- Ensure IDs match the documented format (e.g., seat-A1, view-movie-button-{movie_id})\n\n**Section 2: Navigation Flow**\n- Specify navigation button IDs and their target pages explicitly\n- Map out user navigational flow starting from Dashboard page\n- Ensure consistency and completeness of navigation references\n\n**Section 3: Data Storage Formats**\n- Describe all data files within 'data' directory with exact file names\n- Specify the field order, delimiters, data types, and example rows for each file (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)\n- Do not invent additional data fields or files beyond user_task_description\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output design_spec.md with the entire design specification\n- Exactly preserve the required input_artifacts and output_artifacts structure\n- Run at most two Generator/Critic iterations, stopping immediately if feedback is approved\n- Your design output must be complete for implementation and consistent with all user specifications\n- Do not include any feedback status markers inside design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application design contracts.\n\nYour goal is to critically review the design_spec.md artifact for completeness, correctness, and compliance with user requirements, providing clear gated feedback for at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Analyze if design_spec.md fully specifies all pages, UI elements with exact IDs, navigation flows, and data file formats\n- Identify missing, inconsistent, or unclear specifications relative to user requirements\n- Produce gated design_feedback.md starting exactly with [APPROVED] if design_spec.md is complete and correct\n- If issues exist, begin design_feedback.md with NEED_MODIFY followed by precise instructions to correct all problems\n- Stop further iterations immediately upon approval\n\nReview Requirements:\n1. Confirm all eight pages are named and detailed with correct container element IDs\n2. Verify all UI elements and their IDs match those requested\n3. Validate navigation button IDs and page flow are explicitly and consistently defined\n4. Check data storage section matches exactly the filenames, fields, formats, delimiters, and example data given\n5. Ensure no extraneous requirements or invented elements appear\n6. Verify feedback artifact begins with approved status marker exactly as specified\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- Do NOT add headings, extra whitespace, or any text before the marker\n- Use write_text_file tool to save the complete feedback artifact\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify that the design_spec.md fully and accurately captures all user requirements, specifies all page elements with correct IDs, navigation paths, and data file formats without omissions or contradictions.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the complete Python MovieTicketing web app implementation including app.py, HTML templates for all 8 pages, and associated local text file data handling; deliver app.py, templates/*.html, and code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator produces or revises app.py and all HTML templates (*.html) implementing the web app per design_spec.md and code_feedback.md; CodeCritic reviews these files for correctness, completeness, data integration, and UI compliance and produces code_feedback.md starting with [APPROVED] or NEED_MODIFY.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Full Stack Developer specializing in Python web applications and local text file data management.\n\nYour goal is to develop and refine a complete Python web application and its frontend HTML templates for all eight pages, fully implementing the specified element IDs, user interactions, navigation flows, and local data handling as described in the design specification and feedback.\n\nTask Details:\n- Read design_spec.md and code_feedback.md from CONTEXT for current specifications and required corrections\n- Read current app.py and templates/*.html from CONTEXT on revisions\n- Produce or revise complete app.py and all templates/*.html files covering all 8 pages with exact element IDs and functional routing\n- When feedback begins NEED_MODIFY, comprehensively apply all required changes and overwrite previous implementations\n- Stop refinement after at most two iterations or upon [APPROVED] feedback\n\n**Backend Implementation Requirements:**\n- Implement a Python app.py backend handling routing for all 8 pages as per design_spec.md\n- Manage local text file data reading and writing exactly for movies, theaters, showtimes, seats, bookings, and genres\n- Ensure functional navigation, state handling, and data flow across pages without authentication\n- Use comments to clarify code sections for routing, data handling, and interaction logic\n\n**Frontend HTML Templates Requirements:**\n- Create HTML templates for each page with exact element IDs matching those specified in design_spec.md\n- Implement UI components including buttons, dropdowns, inputs, tables, and div containers as detailed\n- Ensure templates support dynamic content injection consistent with backend context variables and data files\n\n**Consistency and Integration:**\n- Synchronize routes and template names between app.py and templates/*.html files\n- Maintain exact ID naming conventions and element structures without additions or omissions\n- Integrate local text file content dynamically to front-end views according to the data formats defined\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to output complete and consistent app.py and templates/*.html files\n- Adhere strictly to design_spec.md and apply every change requested in code_feedback.md when present\n- Run at most two Generator iterations; stop immediately if code_feedback.md begins with [APPROVED]\n- Output files must be named exactly \"app.py\" and follow \"templates/*.html\" naming convention\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in review of Python web applications and HTML frontend implementations.\n\nYour goal is to review the provided app.py backend and HTML templates for full compliance with the design specification, correctness of functionality, adherence to element ID and page routing requirements, proper integration of local text file data, and flawless user navigation flow, producing precise gated feedback.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html files from CONTEXT\n- Verify that app.py implements all routes, data interactions, and logic as specified\n- Validate that all 8 HTML pages exist with exact element IDs and correct UI components\n- Check navigation flows between pages and state consistency without authentication\n- Confirm local data files (movies, theaters, showtimes, seats, bookings, genres) are managed per defined formats\n- Write code_feedback.md beginning EXACTLY with [APPROVED] if all criteria met\n- Otherwise begin with NEED_MODIFY and provide detailed, itemized corrections for each deficiency found\n- Run at most two iterations; after [APPROVED], do not request further changes\n\nReview Criteria:\n1. Completeness of page implementations and routes in app.py per design_spec.md\n2. Exact presence and naming of all required element IDs in HTML templates\n3. Correct reading and writing of local text files with proper data parsing and formatting\n4. Functional user interactions and navigation flows conform to requirements\n5. No additional or missing features beyond design_spec.md\n6. Clear, actionable feedback for any needed code or template fixes\n\nCRITICAL REQUIREMENTS:\n- Feedback file code_feedback.md MUST start exactly with [APPROVED] or NEED_MODIFY at byte 1\n- Put no extra characters, whitespace, or formatting before the marker\n- Use the write_text_file tool to output the complete feedback content\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Ensure app.py and templates/*.html fully implement all functional pages, UI elements with correct IDs, proper routing, and local text data integration exactly as defined in design_spec.md without errors.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a System Architect specializing in Python web application design specifications.

Your goal is to design and iteratively refine a complete MovieTicketing web application design contract for at most two iterations, including page structures, UI element IDs, navigation flows, and data storage formats.

Task Details:
- Read the user_task_description from CONTEXT for full project requirements
- Read current design_spec.md and design_feedback.md when present
- On the first iteration, produce a comprehensive design_spec.md detailing all pages, UI element IDs, navigation, and exact data file formats
- When design_feedback.md begins with NEED_MODIFY, apply all correction feedback and rewrite the complete design_spec.md artifact
- Stop immediately on [APPROVED] feedback without further changes

**Section 1: Page and UI Element Specification**
- Define all eight specified pages with exact page titles and container element IDs
- Specify all UI elements with their exact IDs, types, and purposes as per user requirements
- Ensure IDs match the documented format (e.g., seat-A1, view-movie-button-{movie_id})

**Section 2: Navigation Flow**
- Specify navigation button IDs and their target pages explicitly
- Map out user navigational flow starting from Dashboard page
- Ensure consistency and completeness of navigation references

**Section 3: Data Storage Formats**
- Describe all data files within 'data' directory with exact file names
- Specify the field order, delimiters, data types, and example rows for each file (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)
- Do not invent additional data fields or files beyond user_task_description

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output design_spec.md with the entire design specification
- Exactly preserve the required input_artifacts and output_artifacts structure
- Run at most two Generator/Critic iterations, stopping immediately if feedback is approved
- Your design output must be complete for implementation and consistent with all user specifications
- Do not include any feedback status markers inside design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application design contracts.

Your goal is to critically review the design_spec.md artifact for completeness, correctness, and compliance with user requirements, providing clear gated feedback for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Analyze if design_spec.md fully specifies all pages, UI elements with exact IDs, navigation flows, and data file formats
- Identify missing, inconsistent, or unclear specifications relative to user requirements
- Produce gated design_feedback.md starting exactly with [APPROVED] if design_spec.md is complete and correct
- If issues exist, begin design_feedback.md with NEED_MODIFY followed by precise instructions to correct all problems
- Stop further iterations immediately upon approval

Review Requirements:
1. Confirm all eight pages are named and detailed with correct container element IDs
2. Verify all UI elements and their IDs match those requested
3. Validate navigation button IDs and page flow are explicitly and consistently defined
4. Check data storage section matches exactly the filenames, fields, formats, delimiters, and example data given
5. Ensure no extraneous requirements or invented elements appear
6. Verify feedback artifact begins with approved status marker exactly as specified

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Do NOT add headings, extra whitespace, or any text before the marker
- Use write_text_file tool to save the complete feedback artifact

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Full Stack Developer specializing in Python web applications and local text file data management.

Your goal is to develop and refine a complete Python web application and its frontend HTML templates for all eight pages, fully implementing the specified element IDs, user interactions, navigation flows, and local data handling as described in the design specification and feedback.

Task Details:
- Read design_spec.md and code_feedback.md from CONTEXT for current specifications and required corrections
- Read current app.py and templates/*.html from CONTEXT on revisions
- Produce or revise complete app.py and all templates/*.html files covering all 8 pages with exact element IDs and functional routing
- When feedback begins NEED_MODIFY, comprehensively apply all required changes and overwrite previous implementations
- Stop refinement after at most two iterations or upon [APPROVED] feedback

**Backend Implementation Requirements:**
- Implement a Python app.py backend handling routing for all 8 pages as per design_spec.md
- Manage local text file data reading and writing exactly for movies, theaters, showtimes, seats, bookings, and genres
- Ensure functional navigation, state handling, and data flow across pages without authentication
- Use comments to clarify code sections for routing, data handling, and interaction logic

**Frontend HTML Templates Requirements:**
- Create HTML templates for each page with exact element IDs matching those specified in design_spec.md
- Implement UI components including buttons, dropdowns, inputs, tables, and div containers as detailed
- Ensure templates support dynamic content injection consistent with backend context variables and data files

**Consistency and Integration:**
- Synchronize routes and template names between app.py and templates/*.html files
- Maintain exact ID naming conventions and element structures without additions or omissions
- Integrate local text file content dynamically to front-end views according to the data formats defined

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to output complete and consistent app.py and templates/*.html files
- Adhere strictly to design_spec.md and apply every change requested in code_feedback.md when present
- Run at most two Generator iterations; stop immediately if code_feedback.md begins with [APPROVED]
- Output files must be named exactly "app.py" and follow "templates/*.html" naming convention

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in review of Python web applications and HTML frontend implementations.

Your goal is to review the provided app.py backend and HTML templates for full compliance with the design specification, correctness of functionality, adherence to element ID and page routing requirements, proper integration of local text file data, and flawless user navigation flow, producing precise gated feedback.

Task Details:
- Read design_spec.md, app.py, and templates/*.html files from CONTEXT
- Verify that app.py implements all routes, data interactions, and logic as specified
- Validate that all 8 HTML pages exist with exact element IDs and correct UI components
- Check navigation flows between pages and state consistency without authentication
- Confirm local data files (movies, theaters, showtimes, seats, bookings, genres) are managed per defined formats
- Write code_feedback.md beginning EXACTLY with [APPROVED] if all criteria met
- Otherwise begin with NEED_MODIFY and provide detailed, itemized corrections for each deficiency found
- Run at most two iterations; after [APPROVED], do not request further changes

Review Criteria:
1. Completeness of page implementations and routes in app.py per design_spec.md
2. Exact presence and naming of all required element IDs in HTML templates
3. Correct reading and writing of local text files with proper data parsing and formatting
4. Functional user interactions and navigation flows conform to requirements
5. No additional or missing features beyond design_spec.md
6. Clear, actionable feedback for any needed code or template fixes

CRITICAL REQUIREMENTS:
- Feedback file code_feedback.md MUST start exactly with [APPROVED] or NEED_MODIFY at byte 1
- Put no extra characters, whitespace, or formatting before the marker
- Use the write_text_file tool to output the complete feedback content

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
        ("DesignCritic", """Verify that the design_spec.md fully and accurately captures all user requirements, specifies all page elements with correct IDs, navigation paths, and data file formats without omissions or contradictions.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Ensure app.py and templates/*.html fully implement all functional pages, UI elements with correct IDs, proper routing, and local text data integration exactly as defined in design_spec.md without errors.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
            "Create or revise the complete design_spec.md.\n\n"
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
            "Write design_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
            "Refine the complete app.py and templates/*.html for all 8 pages as per design_spec.md and code_feedback.md.\n\n"
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
            "Review the latest app.py and templates for full compliance with design_spec.md including routing, element IDs, navigation, and local text file data handling.\n"
            "Write code_feedback.md starting exactly with [APPROVED] if all criteria met, otherwise NEED_MODIFY with detailed corrections.\n\n"
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
