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
# 20260714_001750_056410/main_20260714_001750_056410.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create detailed backend and frontend design specifications for the OnlineLibrary app and merge them into a unified design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDesignArchitect and FrontendDesignArchitect independently create backend and frontend design documents respectively; DesignMerger reconciles both into a consistent design_spec.md.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python backend systems and local text-file data management.\n\nYour goal is to design the backend architecture specification for a Python-based OnlineLibrary web app enabling user management, book catalog, borrowings, reservations, reviews, fines, and associated business logic.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create backend_design.md\n- Specify detailed backend routes, data models, file schemas, and Python logic to fulfill the app features\n- Focus on users, books, borrowings, reservations, reviews, fines, and all required functionalities\n- Do not read or rely on frontend_design.md\n\n**Section 1: Backend Routes and Business Logic**\n- List each Flask route path, HTTP method, function name, and related backend logic summary\n- Describe parameters, return data, and error handling\n- Specify session and user authentication management\n\n**Section 2: Data Models and File Schemas**\n- Define all local text file data schemas with precise field order and delimiter '|'\n- Include files: users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt\n- For each file, detail field names, types, constraints, and sample data rows\n- Include relationships between data entities and status handling\n\n**Section 3: Backend Functional Requirements**\n- Detail key operations: search, borrow, return, review management, reservations, fine calculations\n- Define due date computation and status transitions (e.g., Active, Returned, Overdue)\n- Outline backend validations and business rules\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can implement app.py backend from backend_design.md alone\n- All backend requirements come exclusively from user_task_description\n- Use write_text_file tool to output backend_design.md\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a UI/UX Architect specializing in HTML template design and interactive web UI components.\n\nYour goal is to design frontend specifications for the OnlineLibrary web app, detailing templates, element IDs, navigation, and interactive UI elements for the defined pages.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create frontend_design.md\n- Specify 10 HTML template designs corresponding to app pages, including page titles\n- Define all element IDs, their types, purposes, and layout role per page\n- Map navigation flows, user interactions on buttons, form fields, and dynamic UI components\n- Do not read or rely on backend_design.md\n\n**Section 1: HTML Template Specifications**\n- For each page (Dashboard, Catalog, Details, Borrow Confirmation, My Borrowings, Reservations, Reviews, Write Review, Profile, Payment Confirmation):\n  - Specify template filename and page title\n  - List each element ID, element type (e.g., div, button, input), and descriptive role\n- Specify dynamic elements such as lists, tables, search inputs, buttons with variable IDs\n\n**Section 2: Navigation and Interactivity**\n- Define navigation paths among pages and buttons triggering navigation\n- Describe UI behaviors such as filtering, search input handling, form submission buttons\n- Note user feedback elements placement (e.g., messages, confirmations)\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement HTML templates from frontend_design.md\n- Specifications derive strictly from user_task_description\n- Use write_text_file tool to output frontend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in integrating backend and frontend design documents for Python web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into one unified and internally consistent design_spec.md that meets the OnlineLibrary user requirements without added or removed features.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Validate completeness and mutual consistency across backend and frontend designs\n- Reconcile naming conventions for routes, elements, and context variables\n- Merge backend routes, data schema, business logic, and frontend template, navigation, and UI component specifications\n- Address any discrepancies in functionality or data representations\n\n**Section 1: Backend Design Integration**\n- Consolidate all backend routes, data file schemas with examples, and business rules\n- Ensure file names, fields, and data formats match frontend data usage where relevant\n\n**Section 2: Frontend Design Integration**\n- Consolidate all HTML templates, element IDs, interactive elements, and navigation flows\n- Align UI behaviors with backend route functions and data models\n\n**Section 3: Consistency and Completeness Checks**\n- Perform adaptive consistency checks on keys, IDs, and route names across both designs\n- Ensure no element or feature in the backend or frontend design is missing or inconsistent\n- Confirm full coverage of all user requirements\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper and FrontendDeveloper can rely on design_spec.md alone for implementation\n- No requirements are added, trimmed, or altered beyond user_task_description\n- Use write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness and conforming to user task.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design completeness including page elements and navigation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend and frontend from design_spec.md in parallel and merge into complete application files app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDeveloper and FrontendDeveloper independently implement backend Flask app and frontend HTML templates using design_spec.md; IntegrationMerger reconciles and integrates their outputs into final app.py and templates/*.html.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask web applications.\n\nYour goal is to implement the complete Flask backend app.py managing data with local text files in the 'data' directory, fully based on the backend sections of design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Implement all Flask routes, data file handling, and business logic as specified\n- Create app.py independently without reading frontend templates\n- Use data file formats and paths exactly as declared in design_spec.md\n\n**Section 1: Backend Implementation Requirements**\n- Implement all routes with specified HTTP methods, function names, and logic\n- Handle local text files for users, books, borrowings, reservations, reviews, and fines with pipe-delimited parsing\n- Implement borrowing, returning, review submission, reservation handling, and payment logic following design_spec.md details\n- Implement all required calculations, date handling, and data consistency within app.py\n\n**Section 2: Data File Handling**\n- Read and write from text files in 'data' directory exactly as specified\n- Use pipe '|' delimiter for all files\n- Maintain data integrity and consistent status updates for borrowings, reservations, fines, and reviews\n\n**Section 3: Output**\n- Produce a standalone app.py implementing the entire backend\n- Follow Flask app conventions suitable for integration with provided frontend templates\n\nCRITICAL SUCCESS CRITERIA:\n- Must use write_text_file tool to output app.py\n- app.py must fully implement backend routes and logic described in design_spec.md\n- Must not read or rely on sibling outputs but use design_spec.md only\n- Output exactly app.py with no extra files\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask applications.\n\nYour goal is to implement all 10 frontend HTML templates with correct element IDs, buttons, navigation, and UI components according to the frontend sections of design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Independently implement templates/*.html for all specified pages listed in design_spec.md\n- Follow exact element IDs, page titles, context variables, and navigation button behaviors\n- Ensure templates correspond precisely to design_spec.md frontend specifications\n\n**Section 1: HTML Template Requirements**\n- Create templates for Dashboard, Book Catalog, Book Details, Borrow Confirmation, My Borrowings, My Reservations, My Reviews, Write Review, User Profile, and Payment Confirmation pages\n- Include required elements with IDs, input fields, buttons, tables, and navigation links as described\n- Use Jinja2 syntax for dynamic data placeholders matching backend context variables\n\n**Section 2: Navigation and UI Components**\n- Implement navigation buttons triggering correct page transitions\n- Implement proper form layouts and input field attributes\n- Ensure UI design supports user actions like searching, filtering, borrowing, reviewing, and profile editing\n\n**Section 3: Output**\n- Produce HTML template files named exactly as templates/*.html\n- Templates must support seamless integration with backend app.py\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output templates/*.html files\n- Templates must reflect frontend interface as per design_spec.md\n- Work independently without reading sibling outputs\n- Output only the declared set of HTML template files\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging backend Flask applications with frontend HTML/Jinja2 templates.\n\nYour goal is to reconcile and integrate the backend app.py and frontend templates/*.html ensuring full consistency with design_spec.md, producing finalized and fully consistent app.py and templates/*.html files.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Compare backend and frontend implementations against design_spec.md requirements\n- Resolve discrepancies in route names, context variable names, template usage, and navigation links\n- Ensure that backend outputs match template inputs for fluid user experience\n\n**Section 1: Consistency Checks**\n- Verify route and function names in app.py match template form actions and links\n- Confirm context variable keys and data structures are compatible\n- Check navigation buttons in templates correspond to backend routes and redirect logic\n\n**Section 2: Integration and Correction**\n- Adjust app.py or templates/*.html artifacts as needed for interface alignment without adding new requirements\n- Ensure no breaking mismatches remain between backend and frontend\n- Retain original artifact completeness and correctness after merge\n\n**Section 3: Output**\n- Produce final app.py and templates/*.html reflecting consistent and integrated application\n- Output artifacts must be deployable and comply with original design_spec.md\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output cleaned and reconciled app.py and templates/*.html\n- Do not invent new features or remove declared functionality\n- Focus on integration and consistency only, no partial implementations\n- Output exactly one app.py and the full templates/*.html set\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend implementation correctness and compliance with design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check frontend templates correctness and compliance with design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'OnlineLibrary' Web Application

## 1. Objective
Develop a comprehensive web application named 'OnlineLibrary' using Python, with data managed through local text files. The application enables users to search and browse books, borrow and return books, write reviews, manage reservations, and track their borrowing history. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'OnlineLibrary' application is Python.

## 3. Page Design

The 'OnlineLibrary' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Library Dashboard
- **Overview**: The main hub displaying featured books and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying username.
  - **ID: browse-books-button** - Type: Button - Button to navigate to book catalog page.
  - **ID: my-borrows-button** - Type: Button - Button to navigate to my borrowings page.

### 2. Book Catalog Page
- **Page Title**: Book Catalog
- **Overview**: A page displaying all available books with filtering and search options.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the book catalog page.
  - **ID: search-input** - Type: Input - Field to search books by title or author.
  - **ID: book-grid** - Type: Div - Grid displaying book cards with cover, title, author, and status.
  - **ID: view-book-button-{book_id}** - Type: Button - Button to navigate to book details page (each book card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Book Details Page
- **Page Title**: Book Details
- **Overview**: A page displaying detailed information about a specific book.
- **Elements**:
  - **ID: book-details-page** - Type: Div - Container for the book details page.
  - **ID: book-title** - Type: H1 - Display book title.
  - **ID: book-author** - Type: Div - Display book author.
  - **ID: book-status** - Type: Div - Display availability status (Available, Borrowed, Reserved).
  - **ID: borrow-button** - Type: Button - Button to borrow the book.
  - **ID: reviews-section** - Type: Div - Section displaying user reviews.
  - **ID: write-review-button** - Type: Button - Button to write a review.
  - **ID: back-to-catalog** - Type: Button - Button to navigate back to catalog.

### 4. Borrow Confirmation Page
- **Page Title**: Borrow Confirmation
- **Overview**: A page to confirm book borrowing details.
- **Elements**:
  - **ID: borrow-page** - Type: Div - Container for the borrow confirmation page.
  - **ID: borrow-book-info** - Type: Div - Display information about the book being borrowed.
  - **ID: due-date-display** - Type: Div - Display the due date for return (14 days from borrow).
  - **ID: confirm-borrow-button** - Type: Button - Button to confirm borrowing.
  - **ID: cancel-borrow-button** - Type: Button - Button to cancel and go back.

### 5. My Borrowings Page
- **Page Title**: My Borrowings
- **Overview**: A page displaying all books currently borrowed by the user.
- **Elements**:
  - **ID: my-borrows-page** - Type: Div - Container for the my borrowings page.
  - **ID: filter-status** - Type: Dropdown - Dropdown to filter by status (All, Active, Returned, Overdue).
  - **ID: borrows-table** - Type: Table - Table displaying borrowed books with title, borrow date, due date, status.
  - **ID: return-book-button-{borrow_id}** - Type: Button - Button to return book (each active borrow has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. My Reservations Page
- **Page Title**: My Reservations
- **Overview**: A page displaying all book reservations made by the user.
- **Elements**:
  - **ID: reservations-page** - Type: Div - Container for the reservations page.
  - **ID: reservations-table** - Type: Table - Table displaying reserved books with title, reservation date, status.
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each row has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Overview**: A page displaying all reviews written by the user.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of reviews with book title, rating, review text.
  - **ID: edit-review-button-{review_id}** - Type: Button - Button to edit review (each review has this).
  - **ID: delete-review-button-{review_id}** - Type: Button - Button to delete review (each review has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write Review
- **Overview**: A page for users to write or edit a review for a book.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: book-info-display** - Type: Div - Display information about the book being reviewed.
  - **ID: rating-input** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.
  - **ID: back-to-book** - Type: Button - Button to navigate back to book details.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: borrow-history** - Type: Div - Display list of all previously borrowed books.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Payment Confirmation Page
- **Page Title**: Payment Confirmation
- **Overview**: A page to confirm payment of overdue fines.
- **Elements**:
  - **ID: payment-page** - Type: Div - Container for the payment confirmation page.
  - **ID: fine-amount-display** - Type: Div - Display the fine amount to be paid.
  - **ID: confirm-payment-button** - Type: Button - Button to confirm payment.
  - **ID: back-to-profile** - Type: Button - Button to navigate back to profile.

## 4. Data Storage

The 'OnlineLibrary' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|address
  ```
- **Example Data**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. Books Data
- **File Name**: `books.txt`
- **Data Format**:
  ```
  book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
  ```
- **Example Data**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```

### 3. Borrowings Data
- **File Name**: `borrowings.txt`
- **Data Format**:
  ```
  borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
  ```
- **Example Data**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|username|book_id|reservation_date|status
  ```
- **Example Data**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|username|book_id|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. Fines Data
- **File Name**: `fines.txt`
- **Data Format**:
  ```
  fine_id|username|borrow_id|amount|status|date_issued
  ```
- **Example Data**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
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
            """You are a Software Architect specializing in Python backend systems and local text-file data management.

Your goal is to design the backend architecture specification for a Python-based OnlineLibrary web app enabling user management, book catalog, borrowings, reservations, reviews, fines, and associated business logic.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md
- Specify detailed backend routes, data models, file schemas, and Python logic to fulfill the app features
- Focus on users, books, borrowings, reservations, reviews, fines, and all required functionalities
- Do not read or rely on frontend_design.md

**Section 1: Backend Routes and Business Logic**
- List each Flask route path, HTTP method, function name, and related backend logic summary
- Describe parameters, return data, and error handling
- Specify session and user authentication management

**Section 2: Data Models and File Schemas**
- Define all local text file data schemas with precise field order and delimiter '|'
- Include files: users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt
- For each file, detail field names, types, constraints, and sample data rows
- Include relationships between data entities and status handling

**Section 3: Backend Functional Requirements**
- Detail key operations: search, borrow, return, review management, reservations, fine calculations
- Define due date computation and status transitions (e.g., Active, Returned, Overdue)
- Outline backend validations and business rules

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement app.py backend from backend_design.md alone
- All backend requirements come exclusively from user_task_description
- Use write_text_file tool to output backend_design.md

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a UI/UX Architect specializing in HTML template design and interactive web UI components.

Your goal is to design frontend specifications for the OnlineLibrary web app, detailing templates, element IDs, navigation, and interactive UI elements for the defined pages.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md
- Specify 10 HTML template designs corresponding to app pages, including page titles
- Define all element IDs, their types, purposes, and layout role per page
- Map navigation flows, user interactions on buttons, form fields, and dynamic UI components
- Do not read or rely on backend_design.md

**Section 1: HTML Template Specifications**
- For each page (Dashboard, Catalog, Details, Borrow Confirmation, My Borrowings, Reservations, Reviews, Write Review, Profile, Payment Confirmation):
  - Specify template filename and page title
  - List each element ID, element type (e.g., div, button, input), and descriptive role
- Specify dynamic elements such as lists, tables, search inputs, buttons with variable IDs

**Section 2: Navigation and Interactivity**
- Define navigation paths among pages and buttons triggering navigation
- Describe UI behaviors such as filtering, search input handling, form submission buttons
- Note user feedback elements placement (e.g., messages, confirmations)

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement HTML templates from frontend_design.md
- Specifications derive strictly from user_task_description
- Use write_text_file tool to output frontend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in integrating backend and frontend design documents for Python web applications.

Your goal is to merge backend_design.md and frontend_design.md into one unified and internally consistent design_spec.md that meets the OnlineLibrary user requirements without added or removed features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Validate completeness and mutual consistency across backend and frontend designs
- Reconcile naming conventions for routes, elements, and context variables
- Merge backend routes, data schema, business logic, and frontend template, navigation, and UI component specifications
- Address any discrepancies in functionality or data representations

**Section 1: Backend Design Integration**
- Consolidate all backend routes, data file schemas with examples, and business rules
- Ensure file names, fields, and data formats match frontend data usage where relevant

**Section 2: Frontend Design Integration**
- Consolidate all HTML templates, element IDs, interactive elements, and navigation flows
- Align UI behaviors with backend route functions and data models

**Section 3: Consistency and Completeness Checks**
- Perform adaptive consistency checks on keys, IDs, and route names across both designs
- Ensure no element or feature in the backend or frontend design is missing or inconsistent
- Confirm full coverage of all user requirements

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper and FrontendDeveloper can rely on design_spec.md alone for implementation
- No requirements are added, trimmed, or altered beyond user_task_description
- Use write_text_file tool to output design_spec.md

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

Your goal is to implement the complete Flask backend app.py managing data with local text files in the 'data' directory, fully based on the backend sections of design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT
- Implement all Flask routes, data file handling, and business logic as specified
- Create app.py independently without reading frontend templates
- Use data file formats and paths exactly as declared in design_spec.md

**Section 1: Backend Implementation Requirements**
- Implement all routes with specified HTTP methods, function names, and logic
- Handle local text files for users, books, borrowings, reservations, reviews, and fines with pipe-delimited parsing
- Implement borrowing, returning, review submission, reservation handling, and payment logic following design_spec.md details
- Implement all required calculations, date handling, and data consistency within app.py

**Section 2: Data File Handling**
- Read and write from text files in 'data' directory exactly as specified
- Use pipe '|' delimiter for all files
- Maintain data integrity and consistent status updates for borrowings, reservations, fines, and reviews

**Section 3: Output**
- Produce a standalone app.py implementing the entire backend
- Follow Flask app conventions suitable for integration with provided frontend templates

CRITICAL SUCCESS CRITERIA:
- Must use write_text_file tool to output app.py
- app.py must fully implement backend routes and logic described in design_spec.md
- Must not read or rely on sibling outputs but use design_spec.md only
- Output exactly app.py with no extra files

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templates for Flask applications.

Your goal is to implement all 10 frontend HTML templates with correct element IDs, buttons, navigation, and UI components according to the frontend sections of design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT
- Independently implement templates/*.html for all specified pages listed in design_spec.md
- Follow exact element IDs, page titles, context variables, and navigation button behaviors
- Ensure templates correspond precisely to design_spec.md frontend specifications

**Section 1: HTML Template Requirements**
- Create templates for Dashboard, Book Catalog, Book Details, Borrow Confirmation, My Borrowings, My Reservations, My Reviews, Write Review, User Profile, and Payment Confirmation pages
- Include required elements with IDs, input fields, buttons, tables, and navigation links as described
- Use Jinja2 syntax for dynamic data placeholders matching backend context variables

**Section 2: Navigation and UI Components**
- Implement navigation buttons triggering correct page transitions
- Implement proper form layouts and input field attributes
- Ensure UI design supports user actions like searching, filtering, borrowing, reviewing, and profile editing

**Section 3: Output**
- Produce HTML template files named exactly as templates/*.html
- Templates must support seamless integration with backend app.py

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output templates/*.html files
- Templates must reflect frontend interface as per design_spec.md
- Work independently without reading sibling outputs
- Output only the declared set of HTML template files

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging backend Flask applications with frontend HTML/Jinja2 templates.

Your goal is to reconcile and integrate the backend app.py and frontend templates/*.html ensuring full consistency with design_spec.md, producing finalized and fully consistent app.py and templates/*.html files.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Compare backend and frontend implementations against design_spec.md requirements
- Resolve discrepancies in route names, context variable names, template usage, and navigation links
- Ensure that backend outputs match template inputs for fluid user experience

**Section 1: Consistency Checks**
- Verify route and function names in app.py match template form actions and links
- Confirm context variable keys and data structures are compatible
- Check navigation buttons in templates correspond to backend routes and redirect logic

**Section 2: Integration and Correction**
- Adjust app.py or templates/*.html artifacts as needed for interface alignment without adding new requirements
- Ensure no breaking mismatches remain between backend and frontend
- Retain original artifact completeness and correctness after merge

**Section 3: Output**
- Produce final app.py and templates/*.html reflecting consistent and integrated application
- Output artifacts must be deployable and comply with original design_spec.md

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output cleaned and reconciled app.py and templates/*.html
- Do not invent new features or remove declared functionality
- Focus on integration and consistency only, no partial implementations
- Output exactly one app.py and the full templates/*.html set

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
        ("DesignMerger", """Verify backend design completeness and conforming to user task.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design completeness including page elements and navigation.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend implementation correctness and compliance with design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Check frontend templates correctness and compliance with design_spec.md.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
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
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )
    DesignMerger = build_resilient_agent(
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

    # Parallel execution of backend and frontend design creation
    await asyncio.gather(
        execute(BackendDesignArchitect, "Read user_task_description and create detailed backend_design.md with backend routes, data models, and business logic."),
        execute(FrontendDesignArchitect, "Read user_task_description and create detailed frontend_design.md with HTML template specifications, element IDs, navigation, and UI interactions.")
    )

    # Read backend_design.md and frontend_design.md for merging
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

    # Merge backend and frontend designs into unified design_spec.md
    await execute(
        DesignMerger,
        f"Read user_task_description, backend_design.md, and frontend_design.md and merge into coherent design_spec.md.\n\n"
        f"=== Backend Design ===\n{backend_design}\n\n"
        f"=== Frontend Design ===\n{frontend_design}"
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
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement complete backend app.py from design_spec.md backend sections. "
            "Use exact data file formats and routes as specified. Output app.py."
        ),
        execute(
            FrontendDeveloper,
            "Implement all 10 frontend HTML templates using design_spec.md frontend sections. "
            "Include correct IDs, navigation, Jinja2 syntax as specified. Output templates/*.html."
        )
    )

    # Read outputs for integration merge
    backend_code = ""
    frontend_templates_content = ""
    try:
        backend_code = open("app.py").read()
    except Exception:
        pass
    for filepath in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates_content += f"\n=== {filepath} ===\n" + open(filepath).read()
        except Exception:
            pass

    # Run IntegrationMerger to reconcile and finalize outputs
    await execute(
        IntegrationMerger,
        f"Read design_spec.md, backend app.py and frontend templates/*.html.\n\n"
        f"=== app.py ===\n{backend_code}\n\n"
        f"=== templates/*.html ===\n{frontend_templates_content}"
        "\n\nReconcile all differences ensuring consistency in route names, variable names, template usage, "
        "and navigation buttons. Output final consistent app.py and templates/*.html."
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
