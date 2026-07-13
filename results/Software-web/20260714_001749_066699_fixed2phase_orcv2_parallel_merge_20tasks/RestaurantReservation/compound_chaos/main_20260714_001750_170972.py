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
# 20260714_001750_170972/main_20260714_001750_170972.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create backend and frontend design specifications for the RestaurantReservation web application and merge them into a consistent design_spec.md document\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect designs Flask backend routes, data models, and file interactions based on the user task; \"\n        \"FrontendDesignArchitect designs HTML templates with exact element IDs and navigations; \"\n        \"DesignMerger reconciles backend and frontend designs into a unified design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend development with expertise in designing RESTful routes, data models, and file-based data interactions for Python web applications.\n\nYour goal is to create a comprehensive backend design specification for the RestaurantReservation app that includes all required Flask routes, data schemas, and exact text file data parsing/writing instructions.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Independently produce backend_design.md detailing Flask route definitions, data file schemas, and file interaction specifications\n- Focus on backend functionality only; do not read or assume frontend_design.md\n- Declare all data files and formats for data stored in the local 'data' directory\n\n**Section 1: Flask Route Specifications**\n- Specify each route's URL path, HTTP methods, and function name\n- Define the expected input parameters, payloads (query, form, JSON), and response types\n- Include navigation-related routes and their behaviors linked to pages described in user_task_description\n- State expected template filenames for each route if applicable, but exclude frontend layout details\n\n**Section 2: Data File Schemas and Handling**\n- Specify the exact schema for each text data file in 'data' directory: filename, delimiter, fields order, and field descriptions\n- Include examples of rows with realistic sample data following each schema\n- Detail read/write/update/delete operations per data file including locking or concurrency considerations if any\n- Ensure all data schemas and operations align strictly with user_task_description data formats and business rules\n\nCRITICAL SUCCESS CRITERIA:\n- Output backend_design.md using write_text_file tool\n- The artifact must enable backend developers to implement all required Flask routes and data handling independent of frontend_design.md\n- Adhere strictly to user_task_description data formats and required application features\n- Do not generate or assume any frontend UI elements or templates\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML and Jinja2 template design for Python web applications, focusing on detailed frontend page layouts, element IDs, navigation flows, and dynamic context variables.\n\nYour goal is to create a clear and exact frontend design specification for the RestaurantReservation app that includes all HTML templates, page-specific element IDs, buttons, and navigation flows described by the user task.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Independently produce frontend_design.md detailing all template file paths, page titles, element IDs with their types, and navigation/link flows between pages\n- Provide detailed context variable names and structures needed to render each template based on backend data\n- Focus on frontend presentation and navigation only; do not read or assume backend_design.md\n\n**Section 1: Template and Page Specifications**\n- List each HTML template file for the nine pages with precise filenames\n- Specify the exact page title strings\n- For each page, list all element IDs with their HTML tag/type and purpose as described\n- Include button IDs with exact action descriptions for page navigation or form submission\n\n**Section 2: Navigation and Context Variables**\n- Define the navigation matrix linking all pages via buttons/links by their element IDs\n- Specify context variables per template needed for dynamic page rendering as described (e.g., user info, menu items, reservations)\n- Ensure all elements and variables strictly adhere to the user_task_description; no external UI details are added\n\nCRITICAL SUCCESS CRITERIA:\n- Output frontend_design.md using write_text_file tool\n- The artifact must enable frontend developers to implement all HTML templates and navigation flows independent of backend_design.md\n- Specify only declared UI elements and navigation given in user_task_description\n- Use consistent naming of elements and context variables matching backend contracts is encouraged but not required here\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in integrating backend and frontend design specifications into a coherent, consistent design document for Flask-based Python web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into a unified design_spec.md for the RestaurantReservation app without introducing any new requirements. Ensure internal consistency and alignment with the user task.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Reconcile backend routes with frontend templates to ensure matching route-to-template mappings\n- Align navigation element IDs and button actions between backend route specifications and frontend page flow\n- Ensure data schemas referenced in backend_design.md match the context variables used in frontend_design.md\n- Produce design_spec.md that clearly separates backend routes, frontend templates, navigation flows, and data schemas\n\n**Section 1: Flask Backend and Data Schemas**\n- Include reconciled route listings with HTTP methods, URLs, and linked template filenames\n- Confirm all data file schemas and examples are consistent and referenced in frontend sections\n\n**Section 2: Frontend Templates and Navigation**\n- Present all frontend template specifications with page titles, element IDs, and navigation mappings\n- Validate that all navigation buttons correspond to backend routes and properly linked pages\n- Ensure context variables used in templates align with backend data schemas and route outputs\n\nCRITICAL SUCCESS CRITERIA:\n- Output design_spec.md using write_text_file tool\n- The merged design must enable seamless, error-free backend and frontend implementation\n- No additional features beyond input artifacts; the specification must reflect exactly the user task requirements\n- Resolve all discrepancies and produce one source of truth for developers\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness and alignment with user requirements\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design completeness and alignment with user requirements\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement the backend app.py and frontend templates for RestaurantReservation app based on design_spec.md and integrate them into final deployable artifacts\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with routes, data handling, business logic from design_spec.md independently; \"\n        \"FrontendDeveloper implements templates/*.html with all exact element IDs and navigation requirements independently; \"\n        \"IntegrationMerger reconciles backend and frontend for interface consistency and produces the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web application backend development with Python.\n\nYour goal is to implement the complete backend app.py for the RestaurantReservation application, including all routes, data handling using local text files, and business logic as specified in the design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT to understand all required routes, data schemas, and logic\n- Implement data storage and retrieval using local text files with exact formats\n- Output app.py implementing all backend functionality independently from frontend templates\n- Do not read or assume frontend templates implementations\n\n**Section 1: Flask Backend Implementation**\n- Implement Flask routes per design_spec.md with correct HTTP methods and route paths\n- Use input validation, error handling, and redirects as required\n- Manage data files exactly as specified (users.txt, menu.txt, reservations.txt, waitlist.txt, reviews.txt)\n- Use pipe ('|') delimiter and ensure consistent parsing and writing logic\n\n**Section 2: Data Handling and Business Logic**\n- Implement CRUD operations on local text files as required by reservations, reviews, waitlist, menus, and user profiles\n- Ensure concurrency-safe file read/write logic if applicable\n- Implement reservation booking, waitlist management, review submissions, and user profile updates as designed\n\n**Section 3: Implementation Requirements**\n- Use standard Flask app structure and idiomatic Python coding\n- Include relevant comments using single-quote docstrings in the source code as documentation only\n- Implement without incorporating any frontend code or templates\n\nCRITICAL SUCCESS CRITERIA:\n- The app.py fully implements backend logic from design_spec.md alone\n- Data file interactions strictly follow specified formats and paths\n- Use write_text_file tool to output app.py\n- Produce only app.py as output artifact; no other files or refinements\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 template design for Flask web applications.\n\nYour goal is to implement all HTML templates (*.html) for the RestaurantReservation application, including all specified element IDs, page titles, layout, and navigation defined in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT to understand all required templates, page structures, element IDs, and navigation flows\n- Implement complete and independent HTML/Jinja2 templates with the exact IDs and elements specified\n- Do not read or assume any backend implementation details beyond those in design_spec.md\n\n**Section 1: HTML Template Implementation**\n- Create templates for all website pages with exact element IDs as specified\n- Conform to naming, structure, and navigation flow requirements from design_spec.md\n- Use Jinja2 syntax for dynamic content and context variables as directed\n\n**Section 2: Layout and Navigation**\n- Implement navigation buttons and links with correct target routes and IDs\n- Ensure user experience matches the described page flows and button behaviors\n- Do not implement backend logic; focus on interface, IDs, and template correctness\n\n**Section 3: Implementation Requirements**\n- Follow standard Flask/Jinja2 project conventions for template file placement\n- Use single-quote docstrings or hash comments if including notes or comments in templates\n- Output a complete set of templates/*.html files ready for integration\n\nCRITICAL SUCCESS CRITERIA:\n- All templates include the exact element IDs and navigation defined only in design_spec.md\n- Use write_text_file tool to output templates/*.html files\n- Produce only templates/*.html as output artifacts\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in reconciling backend and frontend Flask web application components.\n\nYour goal is to merge and reconcile the implemented backend app.py and frontend templates/*.html for the RestaurantReservation application into final deployable artifacts, correcting only interface inconsistencies.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate consistency between backend routes and frontend navigation elements\n- Reconcile any mismatches in route names, context variable names, and template references\n- Correct interface inconsistencies while preserving worker implementations' original logic\n\n**Section 1: Backend-Frontend Interface Consistency**\n- Ensure that Flask route function names and paths match frontend navigation button targets\n- Align context variable names expected by templates with those provided by backend\n- Confirm data file usage is consistent across app.py and templates where relevant\n\n**Section 2: Artifact Integration and Refinement**\n- Merge adjustments without adding new functionality or requirements\n- Maintain clear separation of backend logic and frontend templates\n- Document reconciliation decisions using single-quote docstrings or hash comments if applicable\n\n**Section 3: Final Output Requirements**\n- Produce final app.py and templates/*.html files ready for deployment\n- Use write_text_file tool exclusively for saving final artifacts\n- Do not produce additional files or refinement markers beyond declared outputs\n\nCRITICAL SUCCESS CRITERIA:\n- Final artifacts are consistent, deployable, and strictly based on input worker outputs and design_spec.md\n- Interface inconsistencies corrected only as necessary for integration\n- Output only the final app.py and templates/*.html as declared\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend implementation matches design_spec.md and handles all specified data files and routes\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check frontend templates conform to design_spec.md element IDs and navigation requirements\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend development with expertise in designing RESTful routes, data models, and file-based data interactions for Python web applications.

Your goal is to create a comprehensive backend design specification for the RestaurantReservation app that includes all required Flask routes, data schemas, and exact text file data parsing/writing instructions.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently produce backend_design.md detailing Flask route definitions, data file schemas, and file interaction specifications
- Focus on backend functionality only; do not read or assume frontend_design.md
- Declare all data files and formats for data stored in the local 'data' directory

**Section 1: Flask Route Specifications**
- Specify each route's URL path, HTTP methods, and function name
- Define the expected input parameters, payloads (query, form, JSON), and response types
- Include navigation-related routes and their behaviors linked to pages described in user_task_description
- State expected template filenames for each route if applicable, but exclude frontend layout details

**Section 2: Data File Schemas and Handling**
- Specify the exact schema for each text data file in 'data' directory: filename, delimiter, fields order, and field descriptions
- Include examples of rows with realistic sample data following each schema
- Detail read/write/update/delete operations per data file including locking or concurrency considerations if any
- Ensure all data schemas and operations align strictly with user_task_description data formats and business rules

CRITICAL SUCCESS CRITERIA:
- Output backend_design.md using write_text_file tool
- The artifact must enable backend developers to implement all required Flask routes and data handling independent of frontend_design.md
- Adhere strictly to user_task_description data formats and required application features
- Do not generate or assume any frontend UI elements or templates

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML and Jinja2 template design for Python web applications, focusing on detailed frontend page layouts, element IDs, navigation flows, and dynamic context variables.

Your goal is to create a clear and exact frontend design specification for the RestaurantReservation app that includes all HTML templates, page-specific element IDs, buttons, and navigation flows described by the user task.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently produce frontend_design.md detailing all template file paths, page titles, element IDs with their types, and navigation/link flows between pages
- Provide detailed context variable names and structures needed to render each template based on backend data
- Focus on frontend presentation and navigation only; do not read or assume backend_design.md

**Section 1: Template and Page Specifications**
- List each HTML template file for the nine pages with precise filenames
- Specify the exact page title strings
- For each page, list all element IDs with their HTML tag/type and purpose as described
- Include button IDs with exact action descriptions for page navigation or form submission

**Section 2: Navigation and Context Variables**
- Define the navigation matrix linking all pages via buttons/links by their element IDs
- Specify context variables per template needed for dynamic page rendering as described (e.g., user info, menu items, reservations)
- Ensure all elements and variables strictly adhere to the user_task_description; no external UI details are added

CRITICAL SUCCESS CRITERIA:
- Output frontend_design.md using write_text_file tool
- The artifact must enable frontend developers to implement all HTML templates and navigation flows independent of backend_design.md
- Specify only declared UI elements and navigation given in user_task_description
- Use consistent naming of elements and context variables matching backend contracts is encouraged but not required here

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in integrating backend and frontend design specifications into a coherent, consistent design document for Flask-based Python web applications.

Your goal is to merge backend_design.md and frontend_design.md into a unified design_spec.md for the RestaurantReservation app without introducing any new requirements. Ensure internal consistency and alignment with the user task.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Reconcile backend routes with frontend templates to ensure matching route-to-template mappings
- Align navigation element IDs and button actions between backend route specifications and frontend page flow
- Ensure data schemas referenced in backend_design.md match the context variables used in frontend_design.md
- Produce design_spec.md that clearly separates backend routes, frontend templates, navigation flows, and data schemas

**Section 1: Flask Backend and Data Schemas**
- Include reconciled route listings with HTTP methods, URLs, and linked template filenames
- Confirm all data file schemas and examples are consistent and referenced in frontend sections

**Section 2: Frontend Templates and Navigation**
- Present all frontend template specifications with page titles, element IDs, and navigation mappings
- Validate that all navigation buttons correspond to backend routes and properly linked pages
- Ensure context variables used in templates align with backend data schemas and route outputs

CRITICAL SUCCESS CRITERIA:
- Output design_spec.md using write_text_file tool
- The merged design must enable seamless, error-free backend and frontend implementation
- No additional features beyond input artifacts; the specification must reflect exactly the user task requirements
- Resolve all discrepancies and produce one source of truth for developers

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web application backend development with Python.

Your goal is to implement the complete backend app.py for the RestaurantReservation application, including all routes, data handling using local text files, and business logic as specified in the design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT to understand all required routes, data schemas, and logic
- Implement data storage and retrieval using local text files with exact formats
- Output app.py implementing all backend functionality independently from frontend templates
- Do not read or assume frontend templates implementations

**Section 1: Flask Backend Implementation**
- Implement Flask routes per design_spec.md with correct HTTP methods and route paths
- Use input validation, error handling, and redirects as required
- Manage data files exactly as specified (users.txt, menu.txt, reservations.txt, waitlist.txt, reviews.txt)
- Use pipe ('|') delimiter and ensure consistent parsing and writing logic

**Section 2: Data Handling and Business Logic**
- Implement CRUD operations on local text files as required by reservations, reviews, waitlist, menus, and user profiles
- Ensure concurrency-safe file read/write logic if applicable
- Implement reservation booking, waitlist management, review submissions, and user profile updates as designed

**Section 3: Implementation Requirements**
- Use standard Flask app structure and idiomatic Python coding
- Include relevant comments using single-quote docstrings in the source code as documentation only
- Implement without incorporating any frontend code or templates

CRITICAL SUCCESS CRITERIA:
- The app.py fully implements backend logic from design_spec.md alone
- Data file interactions strictly follow specified formats and paths
- Use write_text_file tool to output app.py
- Produce only app.py as output artifact; no other files or refinements

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 template design for Flask web applications.

Your goal is to implement all HTML templates (*.html) for the RestaurantReservation application, including all specified element IDs, page titles, layout, and navigation defined in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT to understand all required templates, page structures, element IDs, and navigation flows
- Implement complete and independent HTML/Jinja2 templates with the exact IDs and elements specified
- Do not read or assume any backend implementation details beyond those in design_spec.md

**Section 1: HTML Template Implementation**
- Create templates for all website pages with exact element IDs as specified
- Conform to naming, structure, and navigation flow requirements from design_spec.md
- Use Jinja2 syntax for dynamic content and context variables as directed

**Section 2: Layout and Navigation**
- Implement navigation buttons and links with correct target routes and IDs
- Ensure user experience matches the described page flows and button behaviors
- Do not implement backend logic; focus on interface, IDs, and template correctness

**Section 3: Implementation Requirements**
- Follow standard Flask/Jinja2 project conventions for template file placement
- Use single-quote docstrings or hash comments if including notes or comments in templates
- Output a complete set of templates/*.html files ready for integration

CRITICAL SUCCESS CRITERIA:
- All templates include the exact element IDs and navigation defined only in design_spec.md
- Use write_text_file tool to output templates/*.html files
- Produce only templates/*.html as output artifacts

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in reconciling backend and frontend Flask web application components.

Your goal is to merge and reconcile the implemented backend app.py and frontend templates/*.html for the RestaurantReservation application into final deployable artifacts, correcting only interface inconsistencies.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate consistency between backend routes and frontend navigation elements
- Reconcile any mismatches in route names, context variable names, and template references
- Correct interface inconsistencies while preserving worker implementations' original logic

**Section 1: Backend-Frontend Interface Consistency**
- Ensure that Flask route function names and paths match frontend navigation button targets
- Align context variable names expected by templates with those provided by backend
- Confirm data file usage is consistent across app.py and templates where relevant

**Section 2: Artifact Integration and Refinement**
- Merge adjustments without adding new functionality or requirements
- Maintain clear separation of backend logic and frontend templates
- Document reconciliation decisions using single-quote docstrings or hash comments if applicable

**Section 3: Final Output Requirements**
- Produce final app.py and templates/*.html files ready for deployment
- Use write_text_file tool exclusively for saving final artifacts
- Do not produce additional files or refinement markers beyond declared outputs

CRITICAL SUCCESS CRITERIA:
- Final artifacts are consistent, deployable, and strictly based on input worker outputs and design_spec.md
- Interface inconsistencies corrected only as necessary for integration
- Output only the final app.py and templates/*.html as declared

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
        ("DesignMerger", """Verify backend design completeness and alignment with user requirements""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design completeness and alignment with user requirements""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend implementation matches design_spec.md and handles all specified data files and routes""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Check frontend templates conform to design_spec.md element IDs and navigation requirements""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        failure_threshold=2,
        recovery_time=60
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
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
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

    # Parallel execution of Backend and Frontend Design Architects
    await asyncio.gather(
        execute(BackendDesignArchitect, "Create backend_design.md specifying Flask routes, data schemas, and data file handling."),
        execute(FrontendDesignArchitect, "Create frontend_design.md specifying HTML templates, element IDs, and navigation flows.")
    )

    # Read backend_design.md and frontend_design.md for merging
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

    # Merge designs into unified design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into design_spec.md ensuring consistency and alignment.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

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
        recovery_time=60
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
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete backend app.py based on design_spec.md design. Output app.py."),
        execute(FrontendDeveloper,
                "Implement all templates/*.html based on design_spec.md with exact element IDs and navigation. Output templates/*.html.")
    )

    # Read backend and frontend outputs for merger
    backend_code = ""
    try:
        backend_code = open("app.py").read()
    except FileNotFoundError:
        pass

    frontend_templates_content = ""
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Execute IntegrationMerger to reconcile and produce final app.py and templates/*.html
    await execute(
        IntegrationMerger,
        "Merge and reconcile backend app.py and frontend templates/*.html for RestaurantReservation app.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== Backend app.py ===\n{backend_code}\n\n"
        f"=== Frontend Templates ===\n{frontend_templates_content}"
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
