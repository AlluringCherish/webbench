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
# 20260714_001750_117717/main_20260714_001750_117717.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the adaptive Web design contract specifying all page layouts, element IDs, navigation flow and data file schema; deliver design_spec.md and design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator drafts design_spec.md from user_task_description and prior design_feedback.md; DesignCritic reviews and produces design_feedback.md with gating status.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in Python web application UI/UX and data storage design.\n\nYour goal is to create or revise a comprehensive design specification document covering all page layouts, element IDs, navigation flow, and data file schemas derived from user requirements and prior critic feedback for at most two iterations.\n\nTask Details:\n- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT\n- On first iteration, author complete design_spec.md covering page titles, element IDs, navigation, and data file formats\n- On feedback NEED_MODIFY, incorporate all corrections and rewrite the full design_spec.md\n- Preserve the approved design if feedback starts with [APPROVED]\n\n**Section 1: Page Layout and Element IDs**\n- Specify every page by its title and contain a clear list of element IDs with their HTML types and descriptions\n- Include all navigation buttons and their purposes exactly as described in user requirements\n- Maintain consistency of element IDs for navigation across pages (e.g., back-to-dashboard)\n\n**Section 2: Navigation Flow**\n- Define the navigation logic between pages via button IDs and target pages\n- Describe how users transition between pages according to the user task specification\n\n**Section 3: Data File Schema Specification**\n- Document all data files stored locally under 'data/' directory exactly as specified\n- For each file, specify filename, exact pipe-delimited field structure with field names and data type hints\n- Include examples as in user requirements; do not invent additional fields or files\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two cycles of Generator/Critic revisions\n- Integrate every supported NEED_MODIFY item fully without omitting details or adding new requirements\n- Use write_text_file tool to save design_spec.md\n- Do not write any feedback marker in design_spec.md\n- Focus exclusively on user requirements for page elements, navigation, and data schema\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application UI/UX and data storage contracts.\n\nYour goal is to review design_spec.md for completeness, accuracy, and alignment with the user_task_description; provide gated feedback in design_feedback.md to allow at most two refinement iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Assess the completeness and correctness of page titles, required element IDs, navigation flow, and data file schemas against user requirements\n- Validate data file schemas match the exact fields, formats, delimiters, and example rows described\n- Verify navigation IDs and flows are coherent and complete\n- Write feedback starting exactly with [APPROVED] if fully compliant\n- Otherwise write NEED_MODIFY followed by explicit, actionable corrections listing missing or inconsistent items\n\nReview Criteria:\n1. All nine pages must be specified with correct page titles and element IDs including described button IDs.\n2. Navigation buttons and their target pages must be fully and accurately described.\n3. Data files under 'data/' directory must be documented with exact field schemas, delimiters, and examples.\n4. No extra or omitted requirements beyond user task are permitted.\n5. Feedback must be clear and unambiguous to guide full correction.\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY without any prefix or heading\n- Use write_text_file tool to save complete feedback\n- Stop refinement immediately after approval or max two iterations reached\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify design_spec.md aligns precisely with all user-stated page structure, element ID requirements, navigation logic, and data file formats.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Develop and refine the full RestaurantReservation Python Flask web app implementation with all specified pages, element IDs, navigation, and data management per design_spec.md; deliver app.py, templates/*.html and gated code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or revises canonical app.py and templates/*.html from design_spec.md and code_feedback.md; CodeCritic assesses code correctness, page completeness, route correctness, element ID exactness, and data file access, producing code_feedback.md with approval status.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in full-stack web applications using local text file data management.\n\nYour goal is to implement or revise the complete RestaurantReservation Flask application, including app.py and all HTML templates, fully conforming to the design specification and incorporating critic feedback, within at most two iterations.\n\nTask Details:\n- Read design_spec.md and the latest code_feedback.md from CONTEXT to guide development and refinement.\n- Read current app.py and all templates/*.html as starting points.\n- Produce complete app.py and all templates/*.html reflecting all nine pages, exact element IDs, navigation routes, and local text file data usage.\n- On first iteration, produce full implementation; on NEED_MODIFY feedback, apply all corrections and overwrite prior artifacts.\n- Preserve specified naming, directory structure, and data file integration as per design_spec.md.\n\n**Section 1: Flask Application Structure**\n- Implement all specified routes corresponding to each page (Dashboard, Menu, Dish Details, Make Reservation, My Reservations, Waitlist, My Reviews, Write Review, User Profile).\n- Each route must render appropriate template with precise context variables.\n- Ensure navigation buttons trigger correct route redirects.\n- Use local text files in 'data' directory for all data operations (users.txt, menu.txt, reservations.txt, waitlist.txt, reviews.txt) with exact parsing format (pipe-delimited).\n\n**Section 2: HTML Template Requirements**\n- Develop one template per page in templates directory (*.html).\n- Include all specified page-level container divs with exact IDs.\n- Include all required interactive elements with exact IDs and types (buttons, inputs, dropdowns, tables, divs).\n- Templates must interact properly with Flask context variables and forms.\n\n**Section 3: Data Integration and Management**\n- Read and write data to text files maintaining specified formats.\n- Ensure data consistency and correct usage of file-based data in routes and templates.\n- Support data operations like browsing menu, submitting reservations and reviews, managing waitlist, and user profile updates.\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output app.py and all templates/*.html.\n- Run at most two iterations; apply all supported NEED_MODIFY corrections fully.\n- Output artifacts must exactly match names and folders: app.py, templates/*.html.\n- Do not add or omit pages, element IDs, or data files beyond design_spec.md.\n- Implement robust navigation and data handling as described.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application code and template verification.\n\nYour goal is to conduct a comprehensive review of app.py and all templates/*.html to verify full implementation compliance with the provided design_spec.md, and produce gated feedback within at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT.\n- Review presence and correctness of all nine specified pages and their route handlers.\n- Verify every specified element ID within HTML templates is present and matches design_spec.md exactly.\n- Validate button and form routes for correctness and navigation accuracy.\n- Confirm data file usage (read/write operations) matches specified local text file formats and locations.\n- Write code_feedback.md starting with exactly [APPROVED] if implementation meets all criteria or NEED_MODIFY followed by specific actionable corrections.\n\nReview Criteria:\n1. All nine pages implemented with full routes and templates.\n2. Exact element IDs for containers, buttons, inputs, dropdowns, tables, and divs per page.\n3. Navigation flows correctly across pages via buttons and links.\n4. Data file handling matches specification; no missing or extraneous data access.\n5. Code and templates follow Flask and HTML best practices.\n\nCRITICAL REQUIREMENTS:\n- code_feedback.md MUST begin exactly with [APPROVED] or NEED_MODIFY marker, no preceding text or whitespace.\n- Provide detailed modification instructions on NEED_MODIFY.\n- Use write_text_file tool to save code_feedback.md as the output.\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Ensure accuracy and completeness of app.py and templates/*.html against design_spec.md, including correctness of routes, element IDs, and data file handling.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Designer specializing in Python web application UI/UX and data storage design.

Your goal is to create or revise a comprehensive design specification document covering all page layouts, element IDs, navigation flow, and data file schemas derived from user requirements and prior critic feedback for at most two iterations.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- On first iteration, author complete design_spec.md covering page titles, element IDs, navigation, and data file formats
- On feedback NEED_MODIFY, incorporate all corrections and rewrite the full design_spec.md
- Preserve the approved design if feedback starts with [APPROVED]

**Section 1: Page Layout and Element IDs**
- Specify every page by its title and contain a clear list of element IDs with their HTML types and descriptions
- Include all navigation buttons and their purposes exactly as described in user requirements
- Maintain consistency of element IDs for navigation across pages (e.g., back-to-dashboard)

**Section 2: Navigation Flow**
- Define the navigation logic between pages via button IDs and target pages
- Describe how users transition between pages according to the user task specification

**Section 3: Data File Schema Specification**
- Document all data files stored locally under 'data/' directory exactly as specified
- For each file, specify filename, exact pipe-delimited field structure with field names and data type hints
- Include examples as in user requirements; do not invent additional fields or files

CRITICAL SUCCESS CRITERIA:
- Run at most two cycles of Generator/Critic revisions
- Integrate every supported NEED_MODIFY item fully without omitting details or adding new requirements
- Use write_text_file tool to save design_spec.md
- Do not write any feedback marker in design_spec.md
- Focus exclusively on user requirements for page elements, navigation, and data schema

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application UI/UX and data storage contracts.

Your goal is to review design_spec.md for completeness, accuracy, and alignment with the user_task_description; provide gated feedback in design_feedback.md to allow at most two refinement iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Assess the completeness and correctness of page titles, required element IDs, navigation flow, and data file schemas against user requirements
- Validate data file schemas match the exact fields, formats, delimiters, and example rows described
- Verify navigation IDs and flows are coherent and complete
- Write feedback starting exactly with [APPROVED] if fully compliant
- Otherwise write NEED_MODIFY followed by explicit, actionable corrections listing missing or inconsistent items

Review Criteria:
1. All nine pages must be specified with correct page titles and element IDs including described button IDs.
2. Navigation buttons and their target pages must be fully and accurately described.
3. Data files under 'data/' directory must be documented with exact field schemas, delimiters, and examples.
4. No extra or omitted requirements beyond user task are permitted.
5. Feedback must be clear and unambiguous to guide full correction.

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY without any prefix or heading
- Use write_text_file tool to save complete feedback
- Stop refinement immediately after approval or max two iterations reached

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in full-stack web applications using local text file data management.

Your goal is to implement or revise the complete RestaurantReservation Flask application, including app.py and all HTML templates, fully conforming to the design specification and incorporating critic feedback, within at most two iterations.

Task Details:
- Read design_spec.md and the latest code_feedback.md from CONTEXT to guide development and refinement.
- Read current app.py and all templates/*.html as starting points.
- Produce complete app.py and all templates/*.html reflecting all nine pages, exact element IDs, navigation routes, and local text file data usage.
- On first iteration, produce full implementation; on NEED_MODIFY feedback, apply all corrections and overwrite prior artifacts.
- Preserve specified naming, directory structure, and data file integration as per design_spec.md.

**Section 1: Flask Application Structure**
- Implement all specified routes corresponding to each page (Dashboard, Menu, Dish Details, Make Reservation, My Reservations, Waitlist, My Reviews, Write Review, User Profile).
- Each route must render appropriate template with precise context variables.
- Ensure navigation buttons trigger correct route redirects.
- Use local text files in 'data' directory for all data operations (users.txt, menu.txt, reservations.txt, waitlist.txt, reviews.txt) with exact parsing format (pipe-delimited).

**Section 2: HTML Template Requirements**
- Develop one template per page in templates directory (*.html).
- Include all specified page-level container divs with exact IDs.
- Include all required interactive elements with exact IDs and types (buttons, inputs, dropdowns, tables, divs).
- Templates must interact properly with Flask context variables and forms.

**Section 3: Data Integration and Management**
- Read and write data to text files maintaining specified formats.
- Ensure data consistency and correct usage of file-based data in routes and templates.
- Support data operations like browsing menu, submitting reservations and reviews, managing waitlist, and user profile updates.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output app.py and all templates/*.html.
- Run at most two iterations; apply all supported NEED_MODIFY corrections fully.
- Output artifacts must exactly match names and folders: app.py, templates/*.html.
- Do not add or omit pages, element IDs, or data files beyond design_spec.md.
- Implement robust navigation and data handling as described.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application code and template verification.

Your goal is to conduct a comprehensive review of app.py and all templates/*.html to verify full implementation compliance with the provided design_spec.md, and produce gated feedback within at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Review presence and correctness of all nine specified pages and their route handlers.
- Verify every specified element ID within HTML templates is present and matches design_spec.md exactly.
- Validate button and form routes for correctness and navigation accuracy.
- Confirm data file usage (read/write operations) matches specified local text file formats and locations.
- Write code_feedback.md starting with exactly [APPROVED] if implementation meets all criteria or NEED_MODIFY followed by specific actionable corrections.

Review Criteria:
1. All nine pages implemented with full routes and templates.
2. Exact element IDs for containers, buttons, inputs, dropdowns, tables, and divs per page.
3. Navigation flows correctly across pages via buttons and links.
4. Data file handling matches specification; no missing or extraneous data access.
5. Code and templates follow Flask and HTML best practices.

CRITICAL REQUIREMENTS:
- code_feedback.md MUST begin exactly with [APPROVED] or NEED_MODIFY marker, no preceding text or whitespace.
- Provide detailed modification instructions on NEED_MODIFY.
- Use write_text_file tool to save code_feedback.md as the output.

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
        ("DesignCritic", """Verify design_spec.md aligns precisely with all user-stated page structure, element ID requirements, navigation logic, and data file formats.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Ensure accuracy and completeness of app.py and templates/*.html against design_spec.md, including correctness of routes, element IDs, and data file handling.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
            "Create or revise the complete design_spec.md covering page layouts, element IDs, navigation flow, and data file schema.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md thoroughly against user_task_description.\n"
            "Write design_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY with detailed corrections.\n\n"
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
import asyncio
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

        # Run AppGenerator to create or revise the full app.py and all templates/*.html
        await execute(
            AppGenerator,
            "Create or revise complete app.py and all templates/*.html reflecting all nine pages, "
            "exact element IDs, navigation routes, and local text file data usage.\n\n"
            f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
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

        # Run CodeCritic to review the latest implementation and write gated feedback
        await execute(
            CodeCritic,
            "Review the latest app.py and all templates/*.html against design_spec.md for full correctness: "
            "route handlers, exact element IDs, navigation, and data file usage.\n\n"
            f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
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
