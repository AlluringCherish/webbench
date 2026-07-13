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
# 20260713_204916_660124/main_20260713_204916_660124.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the RestaurantReservation requirements and produce design_spec.md detailing Flask routes, page structure, element IDs, and data management using local text files.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md capturing all page elements, navigation, and user stories; \"\n        \"then WebArchitect reads requirements_analysis.md and produces design_spec.md covering Flask app routing, template filenames and locations, \"\n        \"exact page titles, element IDs, form inputs, data file access, and user flow ensuring dashboard as the root page.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst with expertise in web application UI/UX and data workflow analysis.\n\nYour goal is to extract and document detailed requirements for all user-visible pages, including UI elements, user actions, data interactions, and navigation flows, producing a structured requirements_analysis.md file.\n\nTask Details:\n- Analyze user_task_description for all pages and elements, including page titles, element IDs, and user actions\n- Document user workflows, navigation paths, and interactions in requirements_analysis.md\n- Capture data file schemas, including exact field names and formats\n- Include comprehensive descriptions and examples for clarity and exhaustiveness\n\nInstructions:\n1. Identify and list all pages with their page titles and container IDs\n2. Enumerate all UI elements per page with exact element IDs, types, and descriptions\n3. Describe user actions such as button clicks, form submissions, and dynamic interactions\n4. Detail navigation flows linking buttons to target pages or actions\n5. Describe and list data files used by the app with formats and examples\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output requirements_analysis.md\n- Follow markdown formatting for clarity and structure\n- Preserve exact element ID names and data schema field orders\n- Ensure completeness to enable downstream architecture design without omissions\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and architecture.\n\nYour goal is to design a detailed Flask web app architecture document (design_spec.md) based on requirements_analysis.md that facilitates independent backend and frontend development.\n\nTask Details:\n- Read requirements_analysis.md thoroughly and consult user_task_description as needed\n- Define all Flask routes mapping URLs to functions and templates, ensuring root route '/' leads to Dashboard\n- Specify template filenames and locations under templates/ directory for all pages\n- Document exact page titles and container element IDs for each page template\n- Detail all interactive elements: buttons (with target routes), form inputs (with names, types), and expected form actions\n- Specify data file accesses including exact file names in data/ directory, with pipe-delimited field schemas\n- Capture user navigation flows and interactions clearly to support frontend and backend implementation\n\nArchitecture Specifications:\n1. **Flask Routes:**\n   - Route path (e.g., /dashboard, /menu, /dish/<int:dish_id>)\n   - Function name (lowercase with underscores)\n   - HTTP method (GET or POST)\n   - Template filename (templates/{template_name}.html)\n   - Context variables passed to template\n\n2. **Templates:**\n   - File path in templates/\n   - Page title in <title> and <h1>\n   - Main container element ID\n   - All button and input element IDs with descriptions\n\n3. **Forms:**\n   - Input fields with names and types\n   - Submit buttons with action routes\n\n4. **Data Files:**\n   - Filename in data/\n   - Pipe-delimited field order and meaning\n   - Usage context per route or feature\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- Ensure consistency and exact matching of all element IDs, filenames, route names, and data schemas\n- Root route '/' must redirect or render Dashboard page\n- Provide complete architecture spanning backend routing and frontend structure\n- Design must allow independent backend and frontend development without ambiguity\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md fully captures every user-visible page, exact element IDs, data file formats, navigation paths, \"\n                \"and user functionality needed before architecture design.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the RestaurantReservation Flask application including app.py and templates/*.html files according to design_spec.md and requirements.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes initial app_draft.py and all templates_draft/*.html with correct routing, page content, element IDs, forms, and data \"\n        \"handling per design_spec.md. IntegrationEngineer then finalizes app.py and templates/*.html for deployment by replacing draft paths and closing gaps.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.\n\nYour goal is to develop an initial draft of the complete Flask backend (app_draft.py) with all routes starting from '/' as Dashboard, and draft all corresponding HTML templates under templates_draft/*.html with full page content, element IDs, and form handling as per specifications.\n\nTask Details:\n- Read design_spec.md and user_task_description comprehensively\n- Input artifacts: design_spec.md, user_task_description\n- Output artifacts: app_draft.py implementing all Flask routes and logic; templates_draft/*.html with all required pages and element IDs\n- Focus on correct routing, page titles, element IDs, and reading/writing pipe-delimited data files exactly as specified\n\nImplementation Requirements:\n1. **Flask Backend (app_draft.py)**\n   - Implement all routes listed, starting with '/' route rendering Dashboard page\n   - Use Flask render_template() referencing templates in templates_draft/\n   - Read and write data from/to data/*.txt files using pipe-delimited parsing matching exact field order\n   - Handle GET and POST methods for forms (reservation, reviews, profile update)\n   - Implement data management for users, menu, reservations, waitlist, reviews as per data formats\n   - Use clear function names consistent with page purposes\n   - Provide route handlers for all specified pages without omissions\n\n2. **Frontend Templates (templates_draft/*.html)**\n   - Create Jinja2 HTML templates for each specified page inside templates_draft/\n   - Include all specified element IDs exactly as required\n   - Include page titles matching design_spec.md / user_task_description exactly (e.g., 'Restaurant Dashboard')\n   - Implement navigation elements linking using url_for() with correct endpoint names\n   - Implement forms with correct input element IDs, names, and methods matching backend route handlers\n   - Use proper Jinja2 looping and conditionals for dynamic content rendering (e.g., menu items, reservations list)\n   - For dynamic element IDs (e.g., view-dish-button-{dish_id}), use Jinja2 syntax: id=\"view-dish-button-{{ dish.dish_id }}\"\n\n3. **Data Handling**\n   - Use file paths exactly as 'data/filename.txt' for all data files\n   - Parse and output pipe-delimited records without header lines\n   - Handle any missing or empty data gracefully in templates and routes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- Template files must be saved individually inside templates_draft/ directory\n- All element IDs and page titles must strictly match specifications without deviation\n- Data file handling must adhere exactly to field orders and formats described\n- Implement only what is specified in design_spec.md and user_task_description (no extra features)\n- Ensure '/' route renders Dashboard page properly\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web application deployment preparation.\n\nYour goal is to refine initial draft implementations by converting app_draft.py and templates_draft/*.html into final app.py and templates/*.html files, ensuring all routes, template references, and data file paths conform perfectly to production standards.\n\nTask Details:\n- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description\n- Input artifacts: design_spec.md, app_draft.py, templates_draft/*.html, user_task_description\n- Output artifacts: finalized app.py, templates/*.html for deployment\n- Focus on removing draft paths, correcting template folder references, and enforcing '/' route as Dashboard\n- Ensure all data file paths exactly match 'data/*.txt' with no deviations\n- Confirm all page titles and element IDs match specifications perfectly\n- Close gaps or inconsistencies found in draft implementation without adding new features\n\nRefinement Requirements:\n1. **Backend Refinement (app.py)**\n   - Replace all 'templates_draft/' references with 'templates/'\n   - Verify '/' route serves dashboard page\n   - Validate all routes and functions correspond exactly to design_spec.md\n   - Confirm data file path usage is consistent and correct\n   - Eliminate any draft-specific paths, variables, or temporary code\n\n2. **Frontend Templates (templates/*.html)**\n   - Rename and move all draft HTML templates to templates/ directory\n   - Ensure element IDs and page titles strictly follow design_spec.md and user_task_description\n   - Verify all navigation endpoints using url_for() correspond to final route names\n   - Clean any draft placeholders or annotations present in draft templates\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html files\n- All filenames and paths must be exact with no residual draft references\n- Do not add or remove pages or functionality beyond specifications\n- Ensure final codebase is ready for deployment with consistent naming and routing\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Ensure app_draft.py and templates_draft/*.html implement all routes, elements, and data management from design_spec.md with accurate page titles and element IDs.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the final app.py and templates/*.html for correctness, compliance with requirements, and seamless functionality.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator performs syntax and runtime checks on app.py, ensures templates/*.html render correctly, tests route accessibility, and verifies UI elements, IDs, \"\n        \"startup behavior, and data handling per design_spec.md. SequentialFixer applies corrections from validation_report.md and produces the final corrected application files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web application validation.\n\nYour goal is to thoroughly validate backend and frontend code to ensure compliance with specifications and flawless runtime behavior.\n\nTask Details:\n- Read input files app.py and all templates/*.html from IntegrationEngineer\n- Refer to design_spec.md for expected routes, UI element IDs, and data handling rules\n- Read user_task_description for overall project context and requirements\n- Produce validation_report.md detailing all issues, defects, and actionable improvement suggestions\n\nValidation Focus:\n1. **Python Code Validation**\n   - Perform syntax and runtime checks on app.py using validate_python_file tool\n   - Confirm Flask app startup without errors\n   - Verify all Flask routes are implemented per design_spec.md\n   - Test route accessibility and expected HTTP methods\n\n2. **Template Rendering Validation**\n   - Render each template and verify presence of all specified element IDs exactly\n   - Confirm dynamic ID patterns and static IDs are correct\n   - Check Jinja2 template syntax and variable usage compliance\n\n3. **Data Handling Verification**\n   - Verify data read/write operations for all local text files match design_spec.md schemas\n   - Confirm correct parsing, field order, and data loading logic\n   - Check handling of file I/O errors and empty data cases\n\n4. **Functional Behavior Testing**\n   - Validate UI navigations and button actions route to correct pages\n   - Confirm startup page is Dashboard\n   - Check form handling behavior for POST routes\n   - Validate waitlist and reservations management according to requirements\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for all code checks\n- Summarize all findings clearly in validation_report.md with recommendations\n- Provide precise, actionable feedback without code fixes\n- Use write_text_file tool to save validation_report.md\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python Flask web application bug fixing and refinement.\n\nYour goal is to implement all corrections from validation reports to deliver a fully functional and requirements-compliant final application.\n\nTask Details:\n- Read validation_report.md summarizing detected issues and recommendations\n- Read current versions of app.py and all templates/*.html from IntegrationEngineer\n- Refer to design_spec.md and user_task_description for correct behavior and requirement confirmation\n- Apply fixes and improvements in app.py and templates to resolve all functional, UI, and data handling defects\n- Ensure stable route handling, accurate data processing, and exact UI element ID compliance\n- Maintain all original functionality and structure outside of necessary fixes\n\nFix Implementation Requirements:\n1. **Bug Fixes**\n   - Correct Python syntax and runtime errors in app.py\n   - Fix route and HTTP method inconsistencies\n   - Repair data parsing and file I/O handling problems\n\n2. **UI and Template Corrections**\n   - Add or correct missing or incorrect element IDs in all templates\n   - Fix Jinja2 syntax errors and data binding issues\n   - Ensure navigation buttons route correctly\n\n3. **Quality Assurance**\n   - Confirm application starts at Dashboard page\n   - Verify all specified workflows and features operate as intended\n   - Maintain consistent naming and formatting standards\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save corrected app.py and templates/*.html\n- Apply all fixes as specified without introducing new features\n- Maintain clean, readable, and well-organized code\n- Submit only the corrected final files as output\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": \"Ensure validation_report.md clearly identifies all functional, UI, and data handling defects with actionable recommendations.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify the final app.py and templates/*.html fully resolve all issues reported in validation_report.md and strictly match design_spec.md and requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'RestaurantReservation' Web Application

## 1. Objective
Develop a comprehensive web application named 'RestaurantReservation' using Python, with data managed through local text files. The application enables users to browse restaurant menus, make table reservations, write reviews, check waitlist status, and manage their dining history. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'RestaurantReservation' application is Python.

## 3. Page Design

The 'RestaurantReservation' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Restaurant Dashboard
- **Overview**: The main hub displaying featured dishes, upcoming reservations, and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying username.
  - **ID: make-reservation-button** - Type: Button - Button to navigate to reservation page.
  - **ID: view-menu-button** - Type: Button - Button to navigate to menu page.
  - **ID: back-to-dashboard** - Type: Button - Button to refresh dashboard.
  - **ID: my-reservations-button** - Type: Button - Button to navigate to my reservations page.
  - **ID: my-reviews-button** - Type: Button - Button to navigate to my reviews page.
  - **ID: waitlist-button** - Type: Button - Button to navigate to waitlist page.
  - **ID: profile-button** - Type: Button - Button to navigate to user profile page.

### 2. Menu Page
- **Page Title**: Restaurant Menu
- **Overview**: A page displaying the restaurant menu with categories and filtering.
- **Elements**:
  - **ID: menu-page** - Type: Div - Container for the menu page.
  - **ID: menu-grid** - Type: Div - Grid displaying dish cards with image, name, price, description.
  - **ID: view-dish-button-{dish_id}** - Type: Button - Button to view dish details (each card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Dish Details Page
- **Page Title**: Dish Details
- **Overview**: A page displaying detailed information about a specific dish.
- **Elements**:
  - **ID: dish-details-page** - Type: Div - Container for the dish details page.
  - **ID: dish-name** - Type: H1 - Display dish name.
  - **ID: dish-price** - Type: Div - Display dish price.
  - **ID: back-to-menu** - Type: Button - Button to navigate back to menu.

### 4. Make Reservation Page
- **Page Title**: Make Reservation
- **Overview**: A page for users to make a table reservation.
- **Elements**:
  - **ID: reservation-page** - Type: Div - Container for the reservation page.
  - **ID: guest-name** - Type: Input - Field to input guest name.
  - **ID: party-size** - Type: Dropdown - Dropdown to select party size (1-10).
  - **ID: reservation-date** - Type: Input (date) - Field to select reservation date.
  - **ID: submit-reservation-button** - Type: Button - Button to submit reservation.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. My Reservations Page
- **Page Title**: My Reservations
- **Overview**: A page displaying all reservations made by the user.
- **Elements**:
  - **ID: my-reservations-page** - Type: Div - Container for the my reservations page.
  - **ID: reservations-table** - Type: Table - Table displaying reservations with date, time, party size, status.
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each upcoming reservation has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Waitlist Page
- **Page Title**: Waitlist
- **Overview**: A page for users to join the waitlist and check their position.
- **Elements**:
  - **ID: waitlist-page** - Type: Div - Container for the waitlist page.
  - **ID: waitlist-party-size** - Type: Dropdown - Dropdown to select party size.
  - **ID: join-waitlist-button** - Type: Button - Button to join waitlist.
  - **ID: user-position** - Type: Div - Display user's current position in waitlist.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Overview**: A page displaying all reviews written by the user.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of reviews with dish name, rating, review text.
  - **ID: write-new-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write Review
- **Overview**: A page for users to write a review for a dish.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: select-dish** - Type: Dropdown - Dropdown to select dish to review.
  - **ID: rating-input** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.
  - **ID: back-to-reviews** - Type: Button - Button to navigate back to my reviews.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'RestaurantReservation' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|full_name
  ```
- **Example Data**:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. Menu Items Data
- **File Name**: `menu.txt`
- **Data Format**:
  ```
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
  ```
- **Example Data**:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
  ```
- **Example Data**:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. Waitlist Data
- **File Name**: `waitlist.txt`
- **Data Format**:
  ```
  waitlist_id|username|party_size|join_time|status
  ```
- **Example Data**:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|username|dish_id|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

All files will be saved in the `data` directory to ensure organization and easy access. The format uses a pipe (`|`) delimiter for better readability and parsing.
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
            """You are a Requirements Analyst with expertise in web application UI/UX and data workflow analysis.

Your goal is to extract and document detailed requirements for all user-visible pages, including UI elements, user actions, data interactions, and navigation flows, producing a structured requirements_analysis.md file.

Task Details:
- Analyze user_task_description for all pages and elements, including page titles, element IDs, and user actions
- Document user workflows, navigation paths, and interactions in requirements_analysis.md
- Capture data file schemas, including exact field names and formats
- Include comprehensive descriptions and examples for clarity and exhaustiveness

Instructions:
1. Identify and list all pages with their page titles and container IDs
2. Enumerate all UI elements per page with exact element IDs, types, and descriptions
3. Describe user actions such as button clicks, form submissions, and dynamic interactions
4. Detail navigation flows linking buttons to target pages or actions
5. Describe and list data files used by the app with formats and examples

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md
- Follow markdown formatting for clarity and structure
- Preserve exact element ID names and data schema field orders
- Ensure completeness to enable downstream architecture design without omissions

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design and architecture.

Your goal is to design a detailed Flask web app architecture document (design_spec.md) based on requirements_analysis.md that facilitates independent backend and frontend development.

Task Details:
- Read requirements_analysis.md thoroughly and consult user_task_description as needed
- Define all Flask routes mapping URLs to functions and templates, ensuring root route '/' leads to Dashboard
- Specify template filenames and locations under templates/ directory for all pages
- Document exact page titles and container element IDs for each page template
- Detail all interactive elements: buttons (with target routes), form inputs (with names, types), and expected form actions
- Specify data file accesses including exact file names in data/ directory, with pipe-delimited field schemas
- Capture user navigation flows and interactions clearly to support frontend and backend implementation

Architecture Specifications:
1. **Flask Routes:**
   - Route path (e.g., /dashboard, /menu, /dish/<int:dish_id>)
   - Function name (lowercase with underscores)
   - HTTP method (GET or POST)
   - Template filename (templates/{template_name}.html)
   - Context variables passed to template

2. **Templates:**
   - File path in templates/
   - Page title in <title> and <h1>
   - Main container element ID
   - All button and input element IDs with descriptions

3. **Forms:**
   - Input fields with names and types
   - Submit buttons with action routes

4. **Data Files:**
   - Filename in data/
   - Pipe-delimited field order and meaning
   - Usage context per route or feature

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Ensure consistency and exact matching of all element IDs, filenames, route names, and data schemas
- Root route '/' must redirect or render Dashboard page
- Provide complete architecture spanning backend routing and frontend structure
- Design must allow independent backend and frontend development without ambiguity

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.

Your goal is to develop an initial draft of the complete Flask backend (app_draft.py) with all routes starting from '/' as Dashboard, and draft all corresponding HTML templates under templates_draft/*.html with full page content, element IDs, and form handling as per specifications.

Task Details:
- Read design_spec.md and user_task_description comprehensively
- Input artifacts: design_spec.md, user_task_description
- Output artifacts: app_draft.py implementing all Flask routes and logic; templates_draft/*.html with all required pages and element IDs
- Focus on correct routing, page titles, element IDs, and reading/writing pipe-delimited data files exactly as specified

Implementation Requirements:
1. **Flask Backend (app_draft.py)**
   - Implement all routes listed, starting with '/' route rendering Dashboard page
   - Use Flask render_template() referencing templates in templates_draft/
   - Read and write data from/to data/*.txt files using pipe-delimited parsing matching exact field order
   - Handle GET and POST methods for forms (reservation, reviews, profile update)
   - Implement data management for users, menu, reservations, waitlist, reviews as per data formats
   - Use clear function names consistent with page purposes
   - Provide route handlers for all specified pages without omissions

2. **Frontend Templates (templates_draft/*.html)**
   - Create Jinja2 HTML templates for each specified page inside templates_draft/
   - Include all specified element IDs exactly as required
   - Include page titles matching design_spec.md / user_task_description exactly (e.g., 'Restaurant Dashboard')
   - Implement navigation elements linking using url_for() with correct endpoint names
   - Implement forms with correct input element IDs, names, and methods matching backend route handlers
   - Use proper Jinja2 looping and conditionals for dynamic content rendering (e.g., menu items, reservations list)
   - For dynamic element IDs (e.g., view-dish-button-{dish_id}), use Jinja2 syntax: id="view-dish-button-{{ dish.dish_id }}"

3. **Data Handling**
   - Use file paths exactly as 'data/filename.txt' for all data files
   - Parse and output pipe-delimited records without header lines
   - Handle any missing or empty data gracefully in templates and routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Template files must be saved individually inside templates_draft/ directory
- All element IDs and page titles must strictly match specifications without deviation
- Data file handling must adhere exactly to field orders and formats described
- Implement only what is specified in design_spec.md and user_task_description (no extra features)
- Ensure '/' route renders Dashboard page properly

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web application deployment preparation.

Your goal is to refine initial draft implementations by converting app_draft.py and templates_draft/*.html into final app.py and templates/*.html files, ensuring all routes, template references, and data file paths conform perfectly to production standards.

Task Details:
- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description
- Input artifacts: design_spec.md, app_draft.py, templates_draft/*.html, user_task_description
- Output artifacts: finalized app.py, templates/*.html for deployment
- Focus on removing draft paths, correcting template folder references, and enforcing '/' route as Dashboard
- Ensure all data file paths exactly match 'data/*.txt' with no deviations
- Confirm all page titles and element IDs match specifications perfectly
- Close gaps or inconsistencies found in draft implementation without adding new features

Refinement Requirements:
1. **Backend Refinement (app.py)**
   - Replace all 'templates_draft/' references with 'templates/'
   - Verify '/' route serves dashboard page
   - Validate all routes and functions correspond exactly to design_spec.md
   - Confirm data file path usage is consistent and correct
   - Eliminate any draft-specific paths, variables, or temporary code

2. **Frontend Templates (templates/*.html)**
   - Rename and move all draft HTML templates to templates/ directory
   - Ensure element IDs and page titles strictly follow design_spec.md and user_task_description
   - Verify all navigation endpoints using url_for() correspond to final route names
   - Clean any draft placeholders or annotations present in draft templates

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- All filenames and paths must be exact with no residual draft references
- Do not add or remove pages or functionality beyond specifications
- Ensure final codebase is ready for deployment with consistent naming and routing

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web application validation.

Your goal is to thoroughly validate backend and frontend code to ensure compliance with specifications and flawless runtime behavior.

Task Details:
- Read input files app.py and all templates/*.html from IntegrationEngineer
- Refer to design_spec.md for expected routes, UI element IDs, and data handling rules
- Read user_task_description for overall project context and requirements
- Produce validation_report.md detailing all issues, defects, and actionable improvement suggestions

Validation Focus:
1. **Python Code Validation**
   - Perform syntax and runtime checks on app.py using validate_python_file tool
   - Confirm Flask app startup without errors
   - Verify all Flask routes are implemented per design_spec.md
   - Test route accessibility and expected HTTP methods

2. **Template Rendering Validation**
   - Render each template and verify presence of all specified element IDs exactly
   - Confirm dynamic ID patterns and static IDs are correct
   - Check Jinja2 template syntax and variable usage compliance

3. **Data Handling Verification**
   - Verify data read/write operations for all local text files match design_spec.md schemas
   - Confirm correct parsing, field order, and data loading logic
   - Check handling of file I/O errors and empty data cases

4. **Functional Behavior Testing**
   - Validate UI navigations and button actions route to correct pages
   - Confirm startup page is Dashboard
   - Check form handling behavior for POST routes
   - Validate waitlist and reservations management according to requirements

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for all code checks
- Summarize all findings clearly in validation_report.md with recommendations
- Provide precise, actionable feedback without code fixes
- Use write_text_file tool to save validation_report.md

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in Python Flask web application bug fixing and refinement.

Your goal is to implement all corrections from validation reports to deliver a fully functional and requirements-compliant final application.

Task Details:
- Read validation_report.md summarizing detected issues and recommendations
- Read current versions of app.py and all templates/*.html from IntegrationEngineer
- Refer to design_spec.md and user_task_description for correct behavior and requirement confirmation
- Apply fixes and improvements in app.py and templates to resolve all functional, UI, and data handling defects
- Ensure stable route handling, accurate data processing, and exact UI element ID compliance
- Maintain all original functionality and structure outside of necessary fixes

Fix Implementation Requirements:
1. **Bug Fixes**
   - Correct Python syntax and runtime errors in app.py
   - Fix route and HTTP method inconsistencies
   - Repair data parsing and file I/O handling problems

2. **UI and Template Corrections**
   - Add or correct missing or incorrect element IDs in all templates
   - Fix Jinja2 syntax errors and data binding issues
   - Ensure navigation buttons route correctly

3. **Quality Assurance**
   - Confirm application starts at Dashboard page
   - Verify all specified workflows and features operate as intended
   - Maintain consistent naming and formatting standards

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html
- Apply all fixes as specified without introducing new features
- Maintain clean, readable, and well-organized code
- Submit only the corrected final files as output

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md fully captures every user-visible page, exact element IDs, data file formats, navigation paths, "
                "and user functionality needed before architecture design.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Ensure app_draft.py and templates_draft/*.html implement all routes, elements, and data management from design_spec.md with accurate page titles and element IDs.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Ensure validation_report.md clearly identifies all functional, UI, and data handling defects with actionable recommendations.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("WebArchitect", """Verify the final app.py and templates/*.html fully resolve all issues reported in validation_report.md and strictly match design_spec.md and requirements.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Create RequirementsAnalyst agent
    RequirementsAnalyst = build_resilient_agent(
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
    # Create WebArchitect agent
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute RequirementsAnalyst first
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description. Extract all user-visible pages, element IDs, user actions, navigation flows, and data file schemas. Write detailed requirements_analysis.md in markdown.")

    # Read requirements_analysis.md content for WebArchitect
    req_analysis_content = ""
    try:
        req_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Execute WebArchitect after RequirementsAnalyst
    await execute(WebArchitect,
                  f"Read the following requirements_analysis.md content and user_task_description.\n"
                  f"=== requirements_analysis.md ===\n"
                  f"{req_analysis_content}\n"
                  f"Analyze and produce design_spec.md covering Flask routes, template files, page titles, element IDs, forms, data files, and user navigation. Ensure root '/' leads to dashboard.")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
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
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: DraftEngineer first, then IntegrationEngineer
    await execute(DraftEngineer,
                  "Develop initial app_draft.py with all Flask routes starting at '/', implementing data handling and forms according to design_spec.md and user requirements. "
                  "Also draft all templates_draft/*.html with correct element IDs, navigation, and page content per specs.")

    # Read draft outputs for integration
    app_draft_code, templates_draft_files = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    # read all templates_draft/*.html files content concatenated (if needed)
    # but since templates_draft/*.html are multiple files, we do not read content here; inject message refers to them collectively

    await execute(IntegrationEngineer,
                  "Refine app_draft.py and templates_draft/*.html by replacing draft paths with production paths, correct template references, verify '/' route as Dashboard, "
                  "and ensure all filenames, element IDs, and page titles strictly match design_spec.md and user requirements. Output final app.py and templates/*.html files.")
# Phase2_End

# Phase3_Start

async def verification_phase():
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file artifacts for injection
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    from glob import glob
    templates_files = glob("templates/*.html")
    aggregated_templates = []
    for tpl_file in templates_files:
        try:
            content = open(tpl_file).read()
            aggregated_templates.append(f"=== {tpl_file} ===\n{content}")
        except Exception:
            pass
    templates_content = "\n\n".join(aggregated_templates)

    # Execute WebValidator sequentially then SequentialFixer
    await execute(WebValidator,
                  f"Validate app.py, templates/*.html, and project correctness. "
                  f"Use validate_python_file and execute_python_code tools. "
                  f"Follow design_spec.md and user_task_description. "
                  f"Output detailed validation_report.md with issues and improvement suggestions.\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n=== templates ===\n{templates_content}")

    # After validation, read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(SequentialFixer,
                  f"Apply fixes from validation_report.md to app.py and templates/*.html. "
                  f"Ensure final app.py and templates fully comply with design_spec.md and user_task_description. "
                  f"Do not introduce new features, only corrections. Produce final corrected files.\n\n"
                  f"=== validation_report.md ===\n{validation_report_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n=== templates ===\n{templates_content}")
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
