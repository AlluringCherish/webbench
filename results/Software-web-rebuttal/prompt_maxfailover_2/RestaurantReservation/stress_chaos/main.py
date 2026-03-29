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
    "phase1": "def architecture_design_phase(\n    goal: str = \"Create a comprehensive design specification detailing Flask routes, HTML templates, and data schemas enabling parallel development of backend and frontend\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces a design_spec.md describing all Flask routes with function names, context variables, HTTP methods, \"\n        \"HTML templates with exact element IDs and navigation mappings, and data schemas with all local text file formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce a comprehensive design specification document that enables Backend and Frontend developers to work independently and in parallel, based on detailed architecture for the RestaurantReservation app.\n\nTask Details:\n- Read user_task_description from CONTEXT for requirements and data details\n- Create design_spec.md with three sections: Flask routes, HTML templates, and data file schemas\n- Include ALL necessary info for backend and frontend implementation based on provided user task\n- Do NOT assume missing information beyond given user task and data formats\n\n**Section 1: Flask Routes Specification (For Backend Developer)**\n\nDefine complete Flask route details with columns/entries for:\n- URL Path (e.g., /dashboard, /menu, /dish/<int:dish_id>)\n- Function Name (lowercase_with_underscores)\n- HTTP Methods (GET, POST as required)\n- Template File to render\n- Context Variables passed to templates with types (list, dict, str, int, float)\n- Request form fields expected (for POST routes)\n\nRequirements:\n- Root route '/' MUST redirect to dashboard page ('/dashboard')\n- Function names and routes must match the page designs exactly\n- Context variables must support all data views and page elements\n- Clearly specify dynamic route parameters and their types (e.g., dish_id: int)\n- Include POST routes for form submissions: reservations, reviews, profile updates, waitlist joins\n- Context variables for lists must specify item structures (e.g., menus: list of dict with fields dish_id, name, price, etc.)\n\n**Section 2: HTML Template Specifications (For Frontend Developer)**\n\nFor each required page template, specify:\n- Filename (templates/{template_name}.html)\n- Page Title (for <title> and main <h1>)\n- Complete list of element IDs with element types and brief description\n- Context variables available in template with their detailed structures\n- Navigation mappings for buttons/links with corresponding Flask routes (use url_for function names)\n- Include instructions for dynamic IDs (e.g., id=\"view-dish-button-{{ dish.dish_id }}\")\n\nRequirements:\n- All element IDs from user task MUST be present exactly as specified\n- Context variable names and structures must match Section 1 Flask route context variables\n- Navigation actions must align with routes in Section 1\n- Clearly specify form actions and input field names for POST submissions\n- Use Jinja2 syntax conventions for loops, conditionals, and variable output\n\n**Section 3: Data File Schemas (For Backend Developer)**\n\nFor each local data file, specify:\n- Path (data/{filename}.txt)\n- Pipe-delimited format with exact field order\n- Description of data stored\n- Field names with explicit meanings\n- 2-3 example rows demonstrating real values as given\n\nFiles to cover:\n- users.txt\n- menu.txt\n- reservations.txt\n- waitlist.txt\n- reviews.txt\n\nRequirements:\n- Field names and order must be precise for correct parsing\n- Example data must be realistic and consistent with user task\n- No header lines included in files\n\nCRITICAL SUCCESS CRITERIA:\n- Specification supports full backend and frontend implementation independently\n- No assumptions or missing elements beyond user task and data specs\n- Element IDs and template names exactly match user requirements\n- Context variables and routes fully cover all data interactions and pages\n- Use write_text_file tool to save design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md backend section for completeness of all Flask routes, expected request methods, \"\n                \"context variables, and accurate data schema details for all data files.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md frontend section for presence of all HTML templates with exact element IDs, structure, \"\n                \"and navigation workflow consistent with user task requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend Flask application and frontend HTML templates independently following design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements the app.py providing all route handlers and data processing based on design_spec.md backend section. \"\n        \"FrontendDeveloper implements all HTML templates and routing UI elements based on design_spec.md frontend section.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend providing all route handlers, data loading, and business logic based on the backend section of the design specification.\n\nTask Details:\n- Read design_spec.md backend section ONLY from CONTEXT\n- Implement complete app.py covering all Flask routes and handlers defined in the design spec\n- Load and parse data files from the data directory exactly as specified in the data schemas\n- Ensure business logic faithfully follows design specifications for reservations, reviews, waitlist, profiles, and menus\n- Do NOT read or depend on frontend template files or sections\n- Do NOT make assumptions beyond what is specified in design_spec.md backend section\n\nImplementation Requirements:\n1. **Flask App Initialization**:\n   # Initialize Flask app with necessary imports and secret key\n   '''\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   '''\n\n2. **Root and Navigation Routes**:\n   - Implement root route '/' to redirect to dashboard page using:\n     return redirect(url_for('dashboard'))\n   - Implement all routes with exact function names and HTTP methods per specification\n\n3. **Data File Handling**:\n   - Load all required data from data/*.txt files using pipe-delimited parsing:\n     parts = line.strip().split('|')\n   - Match exact field order as specified in design spec data schemas\n   - Handle file I/O gracefully, no headers in data files\n\n4. **Route and Business Logic**:\n   - Implement all backend routes with exact context variable names and types\n   - Implement form handling for POST requests using request.form\n   - Manage user sessions or identify users where needed according to spec\n   - Support all operations: menu browsing, reservations, reviews, waitlist, profile\n\n5. **Error Handling and Data Integrity**:\n   - Gracefully handle missing data or incorrect inputs\n   - Maintain data consistency aligned with design spec\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Follow design_spec.md backend section EXACTLY for routes, handlers, and data handling\n- Function names and data field names MUST match specification verbatim\n- Do NOT add or omit any routes beyond specification\n- Do NOT provide code only in chat; always save app.py via write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to create all HTML templates implementing frontend UI and navigation elements based on the frontend section of the design specification.\n\nTask Details:\n- Read design_spec.md frontend section ONLY from CONTEXT\n- Implement all HTML templates with correct element IDs, page titles, and navigation buttons as specified\n- Use Jinja2 templating syntax to loop over data and render context variables exactly as designed\n- Do NOT read or use backend source code or backend-only sections\n- Do NOT guess or assume beyond the frontend design specification\n\nImplementation Requirements:\n1. **Template Structure and Formatting**:\n   # All templates must be HTML5 valid with proper indentation\n   # Include <title> tag and <h1> tag matching page titles from spec\n   # Use Jinja2 control structures for looping and conditionals\n\n2. **Element IDs and Navigation**:\n   - Place ALL required element IDs exactly as specified (case-sensitive)\n   - Implement buttons and links using url_for() with exact function names\n   - For dynamic elements like view-dish-button-{dish_id}, use id=\"view-dish-button-{{ dish.dish_id }}\"\n\n3. **Forms and User Interaction**:\n   - Implement all forms correctly with method and action attributes\n   - Use proper input types and names matching backend expectations\n\n4. **File Organization**:\n   - Save templates into templates/ directory\n   - Each page corresponds to a single HTML file named after the route or page purpose\n   - Use write_text_file for saving files\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all HTML template files under templates/ directory\n- Do NOT add HTML files or contents not specified in frontend section\n- Element IDs and navigation routes MUST match design_spec.md frontend section exactly\n- Page titles in both <title> and <h1> tags MUST match specification\n- Do NOT provide code only in chat; always save files via write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all backend routes correctly, adheres to data schemas in design_spec.md, \"\n                \"and includes route logic for start page dashboard and correct request handling.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all templates/*.html files correctly implement page structures, element IDs, navigation buttons, \"\n                \"and context variable usage as per design_spec.md frontend section.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def integration_testing_phase(\n    goal: str = \"Perform comprehensive integration tests on the combined backend and frontend implementation to ensure functional correctness\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"Tester integrates the backend and frontend, executes test cases across all app features and pages, \"\n        \"then writes detailed feedback. Developer refines implementation iteratively until Tester approves functionality.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Developer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python web applications with integrated backend and frontend components.\n\nYour goal is to fix bugs and improve the Flask backend (app.py) and HTML templates (templates/*.html) based on detailed feedback from the Tester, iterating until the application is fully functional.\n\nTask Details:\n- Read app.py and templates/*.html from CONTEXT as the current implementation\n- Read feedback.txt from Tester to understand reported issues\n- Produce improved versions of app.py and templates/*.html that resolve all detected issues\n- Do NOT modify artifacts outside app.py and templates/*.html\n- Do NOT make assumptions; all changes must directly address feedback\n\nDevelopment Requirements:\n1. **Bug Fixing and Improvement**:\n   - Analyze feedback.txt thoroughly to identify issues and required changes\n   - Fix backend logic, route handlers, data loading, and template rendering as needed\n   - Update HTML templates to ensure UI elements, navigation, and dynamic content behave correctly\n\n2. **Testing Support**:\n   - Use execute_python_code tool to run tests or debug code snippets if needed\n   - Ensure no side effects break other parts of the app\n\n3. **Code and File Management**:\n   - Use write_text_file tool to save all updated source files\n   - Maintain existing file structure and naming conventions exactly\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and templates/*.html files\n- Use execute_python_code tool for local test executions and debugging\n- Only modify files specified in output artifacts\n- Address every issue in feedback.txt completely before producing final version\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in end-to-end functional testing of integrated Python web applications.\n\nYour goal is to conduct comprehensive integration testing of the combined backend and frontend of the RestaurantReservation web application, identify all issues, and provide detailed feedback until the application is fully functional.\n\nTask Details:\n- Read app.py and templates/*.html from CONTEXT as the current integrated implementation\n- Execute thorough testing across all nine application pages and features based on the user requirements\n- Test user flows including dashboard navigation, menu browsing, dish details, reservations, waitlist, reviews, profile management, and related UI elements\n- Document all detected bugs, functional issues, missing behaviors, and UI inconsistencies in feedback.txt\n- Write \"[APPROVED]\" in feedback.txt if all test cases pass without any issues; otherwise write \"NEED_MODIFY\" followed by detailed issue descriptions\n- Do not assume correctness: verify each input and output artifact functionally\n\nTesting Requirements:\n1. **Test Coverage**:\n   - Validate each page loads correctly with all required elements and IDs as specified\n   - Verify all navigation buttons perform exactly as expected\n   - Confirm backend and frontend integration works properly for data persistence, retrieval, and display\n   - Confirm forms handle input correctly and data files are consistent\n\n2. **Issue Reporting**:\n   - Structure feedback.txt with clear, actionable points\n   - Include references to specific artifacts or code locations where applicable\n\n3. **Iteration Control**:\n   - Feedback file status gate: write \"[APPROVED]\" only when all criteria are met to terminate refinement loop\n   - Otherwise, write \"NEED_MODIFY\" and list all issues to prompt fixes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save feedback.txt\n- Provide precise, comprehensive test results and recommendations\n- Follow feedback file status gating strictly for iterative development control\n\nOutput: feedback.txt\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Developer\",\n            \"reviewer_agent\": \"Tester\",\n            \"review_criteria\": (\n                \"Verify that Developer's bug fixes and improvements correctly resolve all issues from previous test cycles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Ensure that final tested implementation meets architecture design and covers all user requirements specified.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce a comprehensive design specification document that enables Backend and Frontend developers to work independently and in parallel, based on detailed architecture for the RestaurantReservation app.

Task Details:
- Read user_task_description from CONTEXT for requirements and data details
- Create design_spec.md with three sections: Flask routes, HTML templates, and data file schemas
- Include ALL necessary info for backend and frontend implementation based on provided user task
- Do NOT assume missing information beyond given user task and data formats

**Section 1: Flask Routes Specification (For Backend Developer)**

Define complete Flask route details with columns/entries for:
- URL Path (e.g., /dashboard, /menu, /dish/<int:dish_id>)
- Function Name (lowercase_with_underscores)
- HTTP Methods (GET, POST as required)
- Template File to render
- Context Variables passed to templates with types (list, dict, str, int, float)
- Request form fields expected (for POST routes)

Requirements:
- Root route '/' MUST redirect to dashboard page ('/dashboard')
- Function names and routes must match the page designs exactly
- Context variables must support all data views and page elements
- Clearly specify dynamic route parameters and their types (e.g., dish_id: int)
- Include POST routes for form submissions: reservations, reviews, profile updates, waitlist joins
- Context variables for lists must specify item structures (e.g., menus: list of dict with fields dish_id, name, price, etc.)

**Section 2: HTML Template Specifications (For Frontend Developer)**

For each required page template, specify:
- Filename (templates/{template_name}.html)
- Page Title (for <title> and main <h1>)
- Complete list of element IDs with element types and brief description
- Context variables available in template with their detailed structures
- Navigation mappings for buttons/links with corresponding Flask routes (use url_for function names)
- Include instructions for dynamic IDs (e.g., id="view-dish-button-{{ dish.dish_id }}")

Requirements:
- All element IDs from user task MUST be present exactly as specified
- Context variable names and structures must match Section 1 Flask route context variables
- Navigation actions must align with routes in Section 1
- Clearly specify form actions and input field names for POST submissions
- Use Jinja2 syntax conventions for loops, conditionals, and variable output

**Section 3: Data File Schemas (For Backend Developer)**

For each local data file, specify:
- Path (data/{filename}.txt)
- Pipe-delimited format with exact field order
- Description of data stored
- Field names with explicit meanings
- 2-3 example rows demonstrating real values as given

Files to cover:
- users.txt
- menu.txt
- reservations.txt
- waitlist.txt
- reviews.txt

Requirements:
- Field names and order must be precise for correct parsing
- Example data must be realistic and consistent with user task
- No header lines included in files

CRITICAL SUCCESS CRITERIA:
- Specification supports full backend and frontend implementation independently
- No assumptions or missing elements beyond user task and data specs
- Element IDs and template names exactly match user requirements
- Context variables and routes fully cover all data interactions and pages
- Use write_text_file tool to save design_spec.md

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

Your goal is to implement a complete Flask backend providing all route handlers, data loading, and business logic based on the backend section of the design specification.

Task Details:
- Read design_spec.md backend section ONLY from CONTEXT
- Implement complete app.py covering all Flask routes and handlers defined in the design spec
- Load and parse data files from the data directory exactly as specified in the data schemas
- Ensure business logic faithfully follows design specifications for reservations, reviews, waitlist, profiles, and menus
- Do NOT read or depend on frontend template files or sections
- Do NOT make assumptions beyond what is specified in design_spec.md backend section

Implementation Requirements:
1. **Flask App Initialization**:
   # Initialize Flask app with necessary imports and secret key
   '''
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   '''

2. **Root and Navigation Routes**:
   - Implement root route '/' to redirect to dashboard page using:
     return redirect(url_for('dashboard'))
   - Implement all routes with exact function names and HTTP methods per specification

3. **Data File Handling**:
   - Load all required data from data/*.txt files using pipe-delimited parsing:
     parts = line.strip().split('|')
   - Match exact field order as specified in design spec data schemas
   - Handle file I/O gracefully, no headers in data files

4. **Route and Business Logic**:
   - Implement all backend routes with exact context variable names and types
   - Implement form handling for POST requests using request.form
   - Manage user sessions or identify users where needed according to spec
   - Support all operations: menu browsing, reservations, reviews, waitlist, profile

5. **Error Handling and Data Integrity**:
   - Gracefully handle missing data or incorrect inputs
   - Maintain data consistency aligned with design spec

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Follow design_spec.md backend section EXACTLY for routes, handlers, and data handling
- Function names and data field names MUST match specification verbatim
- Do NOT add or omit any routes beyond specification
- Do NOT provide code only in chat; always save app.py via write_text_file

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

Your goal is to create all HTML templates implementing frontend UI and navigation elements based on the frontend section of the design specification.

Task Details:
- Read design_spec.md frontend section ONLY from CONTEXT
- Implement all HTML templates with correct element IDs, page titles, and navigation buttons as specified
- Use Jinja2 templating syntax to loop over data and render context variables exactly as designed
- Do NOT read or use backend source code or backend-only sections
- Do NOT guess or assume beyond the frontend design specification

Implementation Requirements:
1. **Template Structure and Formatting**:
   # All templates must be HTML5 valid with proper indentation
   # Include <title> tag and <h1> tag matching page titles from spec
   # Use Jinja2 control structures for looping and conditionals

2. **Element IDs and Navigation**:
   - Place ALL required element IDs exactly as specified (case-sensitive)
   - Implement buttons and links using url_for() with exact function names
   - For dynamic elements like view-dish-button-{dish_id}, use id="view-dish-button-{{ dish.dish_id }}"

3. **Forms and User Interaction**:
   - Implement all forms correctly with method and action attributes
   - Use proper input types and names matching backend expectations

4. **File Organization**:
   - Save templates into templates/ directory
   - Each page corresponds to a single HTML file named after the route or page purpose
   - Use write_text_file for saving files

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all HTML template files under templates/ directory
- Do NOT add HTML files or contents not specified in frontend section
- Element IDs and navigation routes MUST match design_spec.md frontend section exactly
- Page titles in both <title> and <h1> tags MUST match specification
- Do NOT provide code only in chat; always save files via write_text_file

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Developer": {
        "prompt": (
            """You are a Software Developer specializing in Python web applications with integrated backend and frontend components.

Your goal is to fix bugs and improve the Flask backend (app.py) and HTML templates (templates/*.html) based on detailed feedback from the Tester, iterating until the application is fully functional.

Task Details:
- Read app.py and templates/*.html from CONTEXT as the current implementation
- Read feedback.txt from Tester to understand reported issues
- Produce improved versions of app.py and templates/*.html that resolve all detected issues
- Do NOT modify artifacts outside app.py and templates/*.html
- Do NOT make assumptions; all changes must directly address feedback

Development Requirements:
1. **Bug Fixing and Improvement**:
   - Analyze feedback.txt thoroughly to identify issues and required changes
   - Fix backend logic, route handlers, data loading, and template rendering as needed
   - Update HTML templates to ensure UI elements, navigation, and dynamic content behave correctly

2. **Testing Support**:
   - Use execute_python_code tool to run tests or debug code snippets if needed
   - Ensure no side effects break other parts of the app

3. **Code and File Management**:
   - Use write_text_file tool to save all updated source files
   - Maintain existing file structure and naming conventions exactly

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and templates/*.html files
- Use execute_python_code tool for local test executions and debugging
- Only modify files specified in output artifacts
- Address every issue in feedback.txt completely before producing final version

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'feedback.txt', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in end-to-end functional testing of integrated Python web applications.

Your goal is to conduct comprehensive integration testing of the combined backend and frontend of the RestaurantReservation web application, identify all issues, and provide detailed feedback until the application is fully functional.

Task Details:
- Read app.py and templates/*.html from CONTEXT as the current integrated implementation
- Execute thorough testing across all nine application pages and features based on the user requirements
- Test user flows including dashboard navigation, menu browsing, dish details, reservations, waitlist, reviews, profile management, and related UI elements
- Document all detected bugs, functional issues, missing behaviors, and UI inconsistencies in feedback.txt
- Write "[APPROVED]" in feedback.txt if all test cases pass without any issues; otherwise write "NEED_MODIFY" followed by detailed issue descriptions
- Do not assume correctness: verify each input and output artifact functionally

Testing Requirements:
1. **Test Coverage**:
   - Validate each page loads correctly with all required elements and IDs as specified
   - Verify all navigation buttons perform exactly as expected
   - Confirm backend and frontend integration works properly for data persistence, retrieval, and display
   - Confirm forms handle input correctly and data files are consistent

2. **Issue Reporting**:
   - Structure feedback.txt with clear, actionable points
   - Include references to specific artifacts or code locations where applicable

3. **Iteration Control**:
   - Feedback file status gate: write "[APPROVED]" only when all criteria are met to terminate refinement loop
   - Otherwise, write "NEED_MODIFY" and list all issues to prompt fixes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save feedback.txt
- Provide precise, comprehensive test results and recommendations
- Follow feedback file status gating strictly for iterative development control

Output: feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'feedback.txt'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Check design_spec.md backend section for completeness of all Flask routes, expected request methods, "
                "context variables, and accurate data schema details for all data files.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md frontend section for presence of all HTML templates with exact element IDs, structure, "
                "and navigation workflow consistent with user task requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all backend routes correctly, adheres to data schemas in design_spec.md, "
                "and includes route logic for start page dashboard and correct request handling.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all templates/*.html files correctly implement page structures, element IDs, navigation buttons, "
                "and context variable usage as per design_spec.md frontend section.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Developer': [
        ("Tester", """Verify that Developer's bug fixes and improvements correctly resolve all issues from previous test cycles.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'feedback.txt'}])
    ],

    'Tester': [
        ("SystemArchitect", """Ensure that final tested implementation meets architecture design and covers all user requirements specified.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'feedback.txt'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
async def architecture_design_phase():
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
    await execute(SystemArchitect, "Produce comprehensive design_spec.md covering Flask routes, HTML templates, and data schemas based on user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create agents
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
        recovery_time=30
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement complete app.py backend as specified in design_spec.md backend section"),
        execute(FrontendDeveloper, "Implement all HTML templates as specified in design_spec.md frontend section")
    )
# Phase2_End

# Phase3_Start

async def integration_testing_phase():
    # Create agents
    Developer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Developer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 3
    for iteration in range(MAX_LOOPS):
        if iteration == 0:
            # Initial Developer run with no feedback
            await execute(Developer, "Fix bugs and improve app.py and templates/*.html according to Tester feedback.txt")
        else:
            # Read feedback.txt and provide to Developer, terminate if approved
            try:
                with open("feedback.txt", "r") as f:
                    feedback_content = f.read()
            except FileNotFoundError:
                break
            if "[APPROVED]" in feedback_content:
                break
            await execute(Developer, f"Fix all issues reported in the following feedback:\n{feedback_content}")

        # Tester runs integration tests and writes feedback.txt
        await execute(Tester, "Perform comprehensive integration tests on app.py and templates/*.html and write feedback.txt")

        # Check for approval to break loop
        try:
            with open("feedback.txt", "r") as f:
                feedback_content = f.read()
            if "[APPROVED]" in feedback_content:
                break
        except FileNotFoundError:
            pass
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
        architecture_design_phase()
    ]
    step2 = [
        parallel_implementation_phase()
    ]
    step3 = [
        integration_testing_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

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
