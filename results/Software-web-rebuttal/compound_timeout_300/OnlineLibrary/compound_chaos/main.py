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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create a detailed design specification document for 'OnlineLibrary' covering Flask routes, HTML templates, and data schemas to enable separate backend and frontend development\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect will produce 'design_spec.md' encompassing three sections: \"\n        \"1) Flask routes with function names, context variables, and HTTP methods; \"\n        \"2) HTML templates with element IDs and navigation mappings; \"\n        \"3) Data schemas describing fields and formats for local text files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications with expertise in local text file data management.\n\nYour goal is to produce a comprehensive design specification document that enables Backend and Frontend developers to work independently and efficiently.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Create design_spec.md containing three thorough sections: Flask Routes, HTML Templates, and Data Schemas\n- Include details needed to implement backend routes, frontend element IDs, navigation, and local file data schemas\n- Do NOT assume or alter any user requirements; no implementation included here\n\n**Section 1: Flask Routes Specification (Backend Development)**\n\nFor each route, specify the following:\n- URL path (e.g., /dashboard, /book/<int:book_id>)\n- Function name (lowercase with underscores)\n- HTTP method (GET, POST)\n- Template file rendered (e.g., dashboard.html)\n- Context variables passed to template with exact names and types (str, int, list, dict, float, etc.)\n\nRequirements:\n- Root '/' route must redirect to the dashboard page\n- Include routes for all pages listed in the user requirements, covering user actions (borrow, return, review, reservation)\n- Context variables must clearly define data structures, especially lists of dicts\n- Borrow and return flows should include necessary form processing routes and confirmation displays\n\n**Section 2: HTML Template Specifications (Frontend Development)**\n\nFor each HTML template, specify:\n- Filename and path (templates/{template_name}.html)\n- Page title (content for both <title> and <h1> tags)\n- All required element IDs with exact matching case and type (div, button, input, textarea, dropdown, table, etc.)\n- Context variables accessible in the template with full structure details\n- Navigation mappings using Flask's url_for with exact function names and route parameters for dynamic links\n- Include dynamic element ID patterns derived from user requirements (e.g., return-book-button-{borrow_id} → id=\"return-book-button-{{ borrow.borrow_id }}\")\n\nRequirements:\n- Include all element IDs from the user requirements exactly as specified\n- Navigation function names and context variable names must match those defined in Section 1 exactly\n- Support forms for POST actions with appropriate method and action attributes\n\n**Section 3: Data File Schemas (Backend Development)**\n\nFor each data file in the 'data' directory, specify:\n- Filename and path (data/{filename}.txt)\n- Pipe-delimited field order and exact field names\n- Description of the data stored in the file\n- 2-3 example rows with realistic data matching field order\n- Highlight any special parsing notes or field types as needed\n\nData files to document include: users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt.\n\nRequirements:\n- Follow pipe '|' delimiter strictly; no header lines\n- Field order must be exact as backend will parse files without modifications\n- Example data must represent typical realistic records\n\nCRITICAL SUCCESS CRITERIA:\n- The specification fully supports complete backend implementation for Flask routes and data handling\n- The specification fully supports frontend HTML template creation with correct elements and navigation\n- Use write_text_file tool to output design_spec.md\n- Do NOT include any implementation code; focus on clear, unambiguous specification only\n- Element IDs, function names, context variables, and data fields must exactly match user requirements to avoid any ambiguity\n- Support easy independent parallel development of backend and frontend teams\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Review completeness and accuracy of backend-related sections: \"\n                \"Flask route definitions with correct function names, context variables, HTTP methods, \"\n                \"and data schema details for local file formats.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Ensure frontend-related sections are complete and precise: \"\n                \"all HTML element IDs, page titles, context variables, and navigation url_for mappings match requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend Flask app and frontend HTML templates in parallel, strictly following the design specification document\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper will implement 'app.py' covering Flask routes, data loading, and logic using design_spec.md sections 1 and 3. \"\n        \"FrontendDeveloper will implement templates/*.html files using design_spec.md section 2. \"\n        \"Both agents work independently to deliver their respective components.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application fulfilling all functional requirements for the 'OnlineLibrary' system as specified in design_spec.md sections 1 and 3.\n\nTask Details:\n- Read design_spec.md Section 1 (Flask Routes) and Section 3 (Data Schemas) ONLY from CONTEXT\n- Implement full app.py covering routes, business logic, and data handling as per specification\n- Load and parse all required data files from the data/ directory using exact pipe-delimited field orders\n- Provide full support for user management, book catalog browsing, borrowing, returning, reservations, reviews, fines, and profile management\n- DO NOT read or rely on frontend template files or Section 2 of design_spec.md\n- DO NOT assume or invent functionality beyond the specification\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   - Initialize Flask app with appropriate imports from flask (Flask, render_template, redirect, url_for, request, flash)\n   - Configure app secret key for session management\n\n2. **Route Implementation**:\n   - Implement ALL routes as specified in Section 1 with correct function names, HTTP methods, and template rendering\n   - The root route '/' MUST redirect to the dashboard page using redirect(url_for('dashboard'))\n   - Pass context variables to templates exactly as specified\n   - Handle form submissions, POST requests, and URL parameters as per spec\n\n3. **Data Management**:\n   - Read and write data files (users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt) using pipe-delimited parsing\n   - Implement data models as dictionaries or appropriate structures matching field names and order from Section 3\n   - Update files persistently on borrow, return, reservation cancelation, review editing, and other user actions\n   - Handle file I/O errors gracefully and maintain data integrity\n\n4. **Business Logic**:\n   - Enforce borrowing rules, due date calculations (e.g., 14 days from borrow date), status updates (Active, Returned, Overdue, Cancelled)\n   - Calculate fines and track payment status\n   - Support search and filtering features for books and borrowings\n   - Manage user session state as needed (e.g., current logged-in username)\n\n5. **Best Practices**:\n   - Use url_for() for all internal links and redirects\n   - Modularize code where possible for readability and maintainability\n   - Provide clear error handling and user feedback via flashing or status messages\n   - Follow Python coding standards and Flask conventions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app.py\n- Must exactly follow context variable names, route functions, HTTP methods as specified in design_spec.md Section 1\n- Data file parsing MUST strictly follow the field order and format in Section 3\n- Do NOT add or omit routes or functionalities not specified\n- Do NOT write code snippets only in messages; all code must be saved via write_text_file\n- Root route MUST redirect to dashboard page\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to develop complete, accurate frontend HTML templates for all pages of the 'OnlineLibrary' web app, strictly following design_spec.md section 2 specifications.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT\n- Implement all templates as specified, including dashboard, book catalog, details, borrow confirmations, user profile, reviews, reservations, payment pages, and others\n- Ensure every template uses exact element IDs, button IDs, and navigation mappings as detailed\n- Use Jinja2 template syntax for dynamic content, loops, and conditionals according to context variable descriptions\n- DO NOT read backend code or Section 1 and Section 3 of design_spec.md\n- DO NOT assume or create any features beyond the specification\n\nImplementation Requirements:\n1. **Template Structure and Naming**:\n   - Save template files under templates/ directory\n   - Use exact filenames specified (e.g., dashboard.html, catalog.html, book_details.html, etc.)\n\n2. **Element IDs**:\n   - Include ALL element IDs exactly as specified, with precise casing and patterns for dynamic elements (e.g., view-book-button-{{ book.book_id }})\n   - For dynamic IDs, use Jinja2 expressions in ID attributes correctly\n\n3. **Page Titles and Headings**:\n   - Match page titles exactly for `<title>` tags and main `<h1>` headings as specified\n\n4. **Jinja2 Syntax**:\n   - Use correct Jinja2 templating for context variables ({{ var }}), loops ({% for %}), and conditionals ({% if %})\n   - Render dynamic navigation links with url_for() using specified function names and parameters\n\n5. **Forms and Buttons**:\n   - Implement forms for POST actions with proper method=\"POST\" and action referencing url_for() of corresponding route\n   - Include buttons with specified IDs and text from the spec\n\n6. **Navigation**:\n   - Ensure all navigation buttons and links correspond exactly to Flask route functions as per design_spec.md Section 2 mappings\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all templates\n- ALL element IDs and button IDs MUST match exactly as specified (including dynamic patterns)\n- Page titles and headings MUST match design_spec.md exactly\n- Navigation url_for functions MUST be correct and consistent with backend routing\n- Do NOT add templates or elements not specified in design_spec.md Section 2\n- Do NOT send code only in chat messages; all templates must be saved via write_text_file\n- Each template file must be saved as a separate file (templates/dashboard.html, templates/catalog.html, etc.)\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify backend code correctness and alignment with design_spec.md for all Flask routes: \"\n                \"presence, HTTP methods, context variables, correct data parsing, status management, and root redirect to dashboard.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify frontend HTML templates accurately implement design_spec.md details: \"\n                \"all element IDs, button functions, navigation url_for calls, and page titles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def testing_and_quality_assurance_phase(\n    goal: str = \"Perform comprehensive testing and QA on the implemented backend and frontend, ensuring correct functionality, UI accuracy, and data integrity\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"Tester conducts functional, integration, and regression tests on the system by running app.py and interacting with templates. \"\n        \"Generates a detailed test report named 'test_report.md'.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in functional and integration testing of Flask web applications.\n\nYour goal is to verify the correctness, UI consistency, and data integrity of the entire OnlineLibrary system through comprehensive testing and prepare a detailed test report.\n\nTask Details:\n- Read app.py, templates/*.html, and design_spec.md from CONTEXT\n- Perform functional tests covering all user flows: book search, borrowing, returning, writing reviews, reservations, profile management, and payments\n- Check that UI elements exist and behave as per design specifications in design_spec.md, including element IDs and navigation\n- Verify data persistence and consistency across all data files in the data directory during simulated user interactions\n- Produce test_report.md documenting test cases, results, and issues found\n- Write status markers (\"[APPROVED]\" or \"NEED_MODIFY\") to test_feedback.txt based on overall test outcome\n\nTesting Procedures:\n1. **Functional Testing**:\n   - Execute app.py in test environment using execute_python_code tool\n   - Automate or manually simulate user interactions covering all pages and features, including edge cases\n   - Verify backend responses and correctness of data updates in borrowings.txt, reservations.txt, reviews.txt, fines.txt, and related files\n\n2. **UI Verification**:\n   - Inspect templates/*.html for presence of required element IDs and proper navigation links/buttons as outlined in design_spec.md\n   - Confirm that dynamic element IDs and Jinja2 syntax function correctly in simulated usage\n\n3. **Data Consistency and Persistence**:\n   - Check that actions correctly update data files with expected field format and values\n   - Confirm no data corruption or loss during operations\n\n4. **Reporting and Feedback**:\n   - Document all test cases, expected vs actual results, and issues in test_report.md clearly\n   - For any critical failure or unresolved issue, write \"NEED_MODIFY\" to test_feedback.txt; else write \"[APPROVED]\"\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to run app.py and validate runtime behavior\n- Use write_text_file tool to save test_report.md and test_feedback.txt\n- Do NOT modify source files or design_spec.md\n- Feedback file (test_feedback.txt) must contain EXACTLY one marker: \"[APPROVED]\" or \"NEED_MODIFY\"\n- Maintain complete traceability to design_spec.md specifications and input artifacts\n\nOutput: test_report.md, test_feedback.txt\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Assess test report for backend-related issues, including route failures, data handling errors, and logical flaws.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Assess test report for frontend issues, UI inconsistencies, incorrect element behavior, and navigation problems.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase4": "def refinement_loop_phase(\n    goal: str = \"Iteratively improve backend and frontend implementations based on test feedback until all tests pass to satisfaction\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DeveloperImprover revises 'app.py' and 'templates/*.html' based on detailed feedback in 'test_feedback.txt'. \"\n        \"QAReviewer evaluates revisions, writing approval status to 'test_feedback.txt'. Loop continues until '[APPROVED]' status is recorded.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DeveloperImprover\",\n            \"prompt\": \"\"\"You are a Full Stack Developer proficient in Python Flask backend development and HTML templating.\n\nYour goal is to iteratively improve and enhance the backend code (app.py) and frontend templates (templates/*.html) to fully meet all test requirements and user expectations, based on detailed feedback.\n\nTask Details:\n- Read input files app.py and templates/*.html from CONTEXT\n- Analyze test feedback in test_feedback.txt to identify required fixes and enhancements\n- Produce improved versions of app.py and templates/*.html addressing all issues\n- Do NOT introduce unrelated new features or break existing functionality\n\nImprovement Process:\n1. Carefully parse test_feedback.txt for detailed issues and suggestions\n2. Update app.py backend to fix bugs, improve logic, and enhance functionality per feedback\n3. Revise all relevant HTML template files to correct layout, element IDs, navigation, and dynamic content as specified\n4. Maintain existing code style and consistency; preserve data flow and variable names\n5. Validate changes locally to ensure all tests can pass after revisions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and all templates/*.html files\n- Do NOT ignore any feedback items; address all explicitly\n- Preserve input_artifacts data formats exactly\n- Do NOT add completely new modules or change project architecture\n- Output updated files only (app.py and templates/*.html)\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\", \"source\": \"QAReviewer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"QAReviewer\",\n            \"prompt\": \"\"\"You are a Software Quality Assurance Engineer specialized in web application testing and verification.\n\nYour goal is to review all modifications made by the DeveloperImprover to backend (app.py) and frontend (templates/*.html), verifying that all issues reported in the test report have been fully resolved, and determine readiness for deployment with explicit approval status.\n\nReview Process:\n- Read updated app.py and templates/*.html from CONTEXT\n- Review test_report.md thoroughly for all test cases, failure points, and criteria\n- Cross-check revisions against test_report.md expected results and prior feedback\n- Write a status marker to the test_feedback.txt file:\n  - Write '[APPROVED]' if ALL test criteria are met without outstanding issues\n  - Write 'NEED_MODIFY' if any problems remain requiring further fixes\n\nFeedback File Requirements:\n- test_feedback.txt must be human-readable with clear status marker at top\n- Provide concise notes summarizing approved criteria or reasons for modification requests\n- File is used as gating feedback for further DeveloperImprover iterations\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to write test_feedback.txt\n- Do NOT approve if any issues remain unresolved\n- Keep feedback professional and explicit to facilitate clear improvement actions\n\nOutput: test_feedback.txt\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"DeveloperImprover\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"DeveloperImprover\"},\n                {\"type\": \"text_file\", \"name\": \"test_report.md\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DeveloperImprover\",\n            \"reviewer_agent\": \"QAReviewer\",\n            \"review_criteria\": (\n                \"QAReviewer confirms DeveloperImprover has addressed issues per test report and feedback; validates readiness for deployment.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"test_report.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications with expertise in local text file data management.

Your goal is to produce a comprehensive design specification document that enables Backend and Frontend developers to work independently and efficiently.

Task Details:
- Read user_task_description from CONTEXT
- Create design_spec.md containing three thorough sections: Flask Routes, HTML Templates, and Data Schemas
- Include details needed to implement backend routes, frontend element IDs, navigation, and local file data schemas
- Do NOT assume or alter any user requirements; no implementation included here

**Section 1: Flask Routes Specification (Backend Development)**

For each route, specify the following:
- URL path (e.g., /dashboard, /book/<int:book_id>)
- Function name (lowercase with underscores)
- HTTP method (GET, POST)
- Template file rendered (e.g., dashboard.html)
- Context variables passed to template with exact names and types (str, int, list, dict, float, etc.)

Requirements:
- Root '/' route must redirect to the dashboard page
- Include routes for all pages listed in the user requirements, covering user actions (borrow, return, review, reservation)
- Context variables must clearly define data structures, especially lists of dicts
- Borrow and return flows should include necessary form processing routes and confirmation displays

**Section 2: HTML Template Specifications (Frontend Development)**

For each HTML template, specify:
- Filename and path (templates/{template_name}.html)
- Page title (content for both <title> and <h1> tags)
- All required element IDs with exact matching case and type (div, button, input, textarea, dropdown, table, etc.)
- Context variables accessible in the template with full structure details
- Navigation mappings using Flask's url_for with exact function names and route parameters for dynamic links
- Include dynamic element ID patterns derived from user requirements (e.g., return-book-button-{borrow_id} → id="return-book-button-{{ borrow.borrow_id }}")

Requirements:
- Include all element IDs from the user requirements exactly as specified
- Navigation function names and context variable names must match those defined in Section 1 exactly
- Support forms for POST actions with appropriate method and action attributes

**Section 3: Data File Schemas (Backend Development)**

For each data file in the 'data' directory, specify:
- Filename and path (data/{filename}.txt)
- Pipe-delimited field order and exact field names
- Description of the data stored in the file
- 2-3 example rows with realistic data matching field order
- Highlight any special parsing notes or field types as needed

Data files to document include: users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt.

Requirements:
- Follow pipe '|' delimiter strictly; no header lines
- Field order must be exact as backend will parse files without modifications
- Example data must represent typical realistic records

CRITICAL SUCCESS CRITERIA:
- The specification fully supports complete backend implementation for Flask routes and data handling
- The specification fully supports frontend HTML template creation with correct elements and navigation
- Use write_text_file tool to output design_spec.md
- Do NOT include any implementation code; focus on clear, unambiguous specification only
- Element IDs, function names, context variables, and data fields must exactly match user requirements to avoid any ambiguity
- Support easy independent parallel development of backend and frontend teams

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

Your goal is to implement a complete Flask backend application fulfilling all functional requirements for the 'OnlineLibrary' system as specified in design_spec.md sections 1 and 3.

Task Details:
- Read design_spec.md Section 1 (Flask Routes) and Section 3 (Data Schemas) ONLY from CONTEXT
- Implement full app.py covering routes, business logic, and data handling as per specification
- Load and parse all required data files from the data/ directory using exact pipe-delimited field orders
- Provide full support for user management, book catalog browsing, borrowing, returning, reservations, reviews, fines, and profile management
- DO NOT read or rely on frontend template files or Section 2 of design_spec.md
- DO NOT assume or invent functionality beyond the specification

Implementation Requirements:
1. **Flask Application Setup**:
   - Initialize Flask app with appropriate imports from flask (Flask, render_template, redirect, url_for, request, flash)
   - Configure app secret key for session management

2. **Route Implementation**:
   - Implement ALL routes as specified in Section 1 with correct function names, HTTP methods, and template rendering
   - The root route '/' MUST redirect to the dashboard page using redirect(url_for('dashboard'))
   - Pass context variables to templates exactly as specified
   - Handle form submissions, POST requests, and URL parameters as per spec

3. **Data Management**:
   - Read and write data files (users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt) using pipe-delimited parsing
   - Implement data models as dictionaries or appropriate structures matching field names and order from Section 3
   - Update files persistently on borrow, return, reservation cancelation, review editing, and other user actions
   - Handle file I/O errors gracefully and maintain data integrity

4. **Business Logic**:
   - Enforce borrowing rules, due date calculations (e.g., 14 days from borrow date), status updates (Active, Returned, Overdue, Cancelled)
   - Calculate fines and track payment status
   - Support search and filtering features for books and borrowings
   - Manage user session state as needed (e.g., current logged-in username)

5. **Best Practices**:
   - Use url_for() for all internal links and redirects
   - Modularize code where possible for readability and maintainability
   - Provide clear error handling and user feedback via flashing or status messages
   - Follow Python coding standards and Flask conventions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app.py
- Must exactly follow context variable names, route functions, HTTP methods as specified in design_spec.md Section 1
- Data file parsing MUST strictly follow the field order and format in Section 3
- Do NOT add or omit routes or functionalities not specified
- Do NOT write code snippets only in messages; all code must be saved via write_text_file
- Root route MUST redirect to dashboard page

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

Your goal is to develop complete, accurate frontend HTML templates for all pages of the 'OnlineLibrary' web app, strictly following design_spec.md section 2 specifications.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT
- Implement all templates as specified, including dashboard, book catalog, details, borrow confirmations, user profile, reviews, reservations, payment pages, and others
- Ensure every template uses exact element IDs, button IDs, and navigation mappings as detailed
- Use Jinja2 template syntax for dynamic content, loops, and conditionals according to context variable descriptions
- DO NOT read backend code or Section 1 and Section 3 of design_spec.md
- DO NOT assume or create any features beyond the specification

Implementation Requirements:
1. **Template Structure and Naming**:
   - Save template files under templates/ directory
   - Use exact filenames specified (e.g., dashboard.html, catalog.html, book_details.html, etc.)

2. **Element IDs**:
   - Include ALL element IDs exactly as specified, with precise casing and patterns for dynamic elements (e.g., view-book-button-{{ book.book_id }})
   - For dynamic IDs, use Jinja2 expressions in ID attributes correctly

3. **Page Titles and Headings**:
   - Match page titles exactly for `<title>` tags and main `<h1>` headings as specified

4. **Jinja2 Syntax**:
   - Use correct Jinja2 templating for context variables ({{ var }}), loops ({% for %}), and conditionals ({% if %})
   - Render dynamic navigation links with url_for() using specified function names and parameters

5. **Forms and Buttons**:
   - Implement forms for POST actions with proper method="POST" and action referencing url_for() of corresponding route
   - Include buttons with specified IDs and text from the spec

6. **Navigation**:
   - Ensure all navigation buttons and links correspond exactly to Flask route functions as per design_spec.md Section 2 mappings

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all templates
- ALL element IDs and button IDs MUST match exactly as specified (including dynamic patterns)
- Page titles and headings MUST match design_spec.md exactly
- Navigation url_for functions MUST be correct and consistent with backend routing
- Do NOT add templates or elements not specified in design_spec.md Section 2
- Do NOT send code only in chat messages; all templates must be saved via write_text_file
- Each template file must be saved as a separate file (templates/dashboard.html, templates/catalog.html, etc.)

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in functional and integration testing of Flask web applications.

Your goal is to verify the correctness, UI consistency, and data integrity of the entire OnlineLibrary system through comprehensive testing and prepare a detailed test report.

Task Details:
- Read app.py, templates/*.html, and design_spec.md from CONTEXT
- Perform functional tests covering all user flows: book search, borrowing, returning, writing reviews, reservations, profile management, and payments
- Check that UI elements exist and behave as per design specifications in design_spec.md, including element IDs and navigation
- Verify data persistence and consistency across all data files in the data directory during simulated user interactions
- Produce test_report.md documenting test cases, results, and issues found
- Write status markers ("[APPROVED]" or "NEED_MODIFY") to test_feedback.txt based on overall test outcome

Testing Procedures:
1. **Functional Testing**:
   - Execute app.py in test environment using execute_python_code tool
   - Automate or manually simulate user interactions covering all pages and features, including edge cases
   - Verify backend responses and correctness of data updates in borrowings.txt, reservations.txt, reviews.txt, fines.txt, and related files

2. **UI Verification**:
   - Inspect templates/*.html for presence of required element IDs and proper navigation links/buttons as outlined in design_spec.md
   - Confirm that dynamic element IDs and Jinja2 syntax function correctly in simulated usage

3. **Data Consistency and Persistence**:
   - Check that actions correctly update data files with expected field format and values
   - Confirm no data corruption or loss during operations

4. **Reporting and Feedback**:
   - Document all test cases, expected vs actual results, and issues in test_report.md clearly
   - For any critical failure or unresolved issue, write "NEED_MODIFY" to test_feedback.txt; else write "[APPROVED]"

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to run app.py and validate runtime behavior
- Use write_text_file tool to save test_report.md and test_feedback.txt
- Do NOT modify source files or design_spec.md
- Feedback file (test_feedback.txt) must contain EXACTLY one marker: "[APPROVED]" or "NEED_MODIFY"
- Maintain complete traceability to design_spec.md specifications and input artifacts

Output: test_report.md, test_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'test_report.md'}, {'type': 'text_file', 'name': 'test_feedback.txt'}],
    },

    "DeveloperImprover": {
        "prompt": (
            """You are a Full Stack Developer proficient in Python Flask backend development and HTML templating.

Your goal is to iteratively improve and enhance the backend code (app.py) and frontend templates (templates/*.html) to fully meet all test requirements and user expectations, based on detailed feedback.

Task Details:
- Read input files app.py and templates/*.html from CONTEXT
- Analyze test feedback in test_feedback.txt to identify required fixes and enhancements
- Produce improved versions of app.py and templates/*.html addressing all issues
- Do NOT introduce unrelated new features or break existing functionality

Improvement Process:
1. Carefully parse test_feedback.txt for detailed issues and suggestions
2. Update app.py backend to fix bugs, improve logic, and enhance functionality per feedback
3. Revise all relevant HTML template files to correct layout, element IDs, navigation, and dynamic content as specified
4. Maintain existing code style and consistency; preserve data flow and variable names
5. Validate changes locally to ensure all tests can pass after revisions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all templates/*.html files
- Do NOT ignore any feedback items; address all explicitly
- Preserve input_artifacts data formats exactly
- Do NOT add completely new modules or change project architecture
- Output updated files only (app.py and templates/*.html)

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'test_feedback.txt', 'source': 'QAReviewer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "QAReviewer": {
        "prompt": (
            """You are a Software Quality Assurance Engineer specialized in web application testing and verification.

Your goal is to review all modifications made by the DeveloperImprover to backend (app.py) and frontend (templates/*.html), verifying that all issues reported in the test report have been fully resolved, and determine readiness for deployment with explicit approval status.

Review Process:
- Read updated app.py and templates/*.html from CONTEXT
- Review test_report.md thoroughly for all test cases, failure points, and criteria
- Cross-check revisions against test_report.md expected results and prior feedback
- Write a status marker to the test_feedback.txt file:
  - Write '[APPROVED]' if ALL test criteria are met without outstanding issues
  - Write 'NEED_MODIFY' if any problems remain requiring further fixes

Feedback File Requirements:
- test_feedback.txt must be human-readable with clear status marker at top
- Provide concise notes summarizing approved criteria or reasons for modification requests
- File is used as gating feedback for further DeveloperImprover iterations

CRITICAL REQUIREMENTS:
- Use write_text_file tool to write test_feedback.txt
- Do NOT approve if any issues remain unresolved
- Keep feedback professional and explicit to facilitate clear improvement actions

Output: test_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'DeveloperImprover'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'DeveloperImprover'}, {'type': 'text_file', 'name': 'test_report.md', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'test_feedback.txt'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Review completeness and accuracy of backend-related sections: "
                "Flask route definitions with correct function names, context variables, HTTP methods, "
                "and data schema details for local file formats.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Ensure frontend-related sections are complete and precise: "
                "all HTML element IDs, page titles, context variables, and navigation url_for mappings match requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify backend code correctness and alignment with design_spec.md for all Flask routes: "
                "presence, HTTP methods, context variables, correct data parsing, status management, and root redirect to dashboard.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify frontend HTML templates accurately implement design_spec.md details: "
                "all element IDs, button functions, navigation url_for calls, and page titles.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Tester': [
        ("BackendDeveloper", """Assess test report for backend-related issues, including route failures, data handling errors, and logical flaws.""", [{'type': 'text_file', 'name': 'test_report.md'}, {'type': 'text_file', 'name': 'app.py'}]),
        ("FrontendDeveloper", """Assess test report for frontend issues, UI inconsistencies, incorrect element behavior, and navigation problems.""", [{'type': 'text_file', 'name': 'test_report.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'DeveloperImprover': [
        ("QAReviewer", """QAReviewer confirms DeveloperImprover has addressed issues per test report and feedback; validates readiness for deployment.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'test_report.md'}])
    ]

}




# ==================== Compound Chaos Controller Setup ====================
import random
from chaos.injectors import ChaosMode

# Compound Chaos: Per-task sampling
COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "prompt_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "io_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "prompt_probability": 0.2,
    "io_probability": 0.2
}

# ChaosMode mapping
MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["prompt_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Agent chaos is sampled with intensity
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

# Prompt/IO separately sampled at 0.2 probability (reset)
all_agents = list(AGENT_PROFILES.keys())
chaos_controller.stress_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["prompt_probability"]]
chaos_controller.io_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["io_probability"]]

# Guarantee at least 1
if not chaos_controller.stress_chaos_targets:
    chaos_controller.stress_chaos_targets = [random.choice(all_agents)]
if not chaos_controller.io_chaos_targets:
    chaos_controller.io_chaos_targets = [random.choice(all_agents)]

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "compound_config": COMPOUND_CONFIG,
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

print(f"Compound Chaos activated: Agent={COMPOUND_CONFIG['agent_intensity']}, Prompt={COMPOUND_CONFIG['prompt_method']}, IO={COMPOUND_CONFIG['io_method']}")
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Create detailed design_spec.md defining Flask routes, HTML templates, and data schemas based on user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Declare agents
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py using design_spec.md Sections 1 and 3 for backend"),
        execute(FrontendDeveloper, "Implement all frontend templates using design_spec.md Section 2")
    )
# Phase2_End

# Phase3_Start

async def testing_and_quality_assurance_phase():
    # Create Tester agent
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute Tester: perform comprehensive testing and generate test_report.md and test_feedback.txt
    await execute(
        Tester,
        "Perform comprehensive functional, integration, regression tests on app.py and templates, verify UI and data integrity, write test_report.md and test_feedback.txt"
    )
# Phase3_End

# Phase4_Start

async def refinement_loop_phase():
    # Create DeveloperImprover agent
    DeveloperImprover = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DeveloperImprover",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    # Create QAReviewer agent
    QAReviewer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="QAReviewer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 5
    for iteration in range(MAX_LOOPS):
        # DeveloperImprover revises app.py and templates based on feedback
        if iteration == 0:
            await execute(
                DeveloperImprover,
                "Improve app.py and templates/*.html according to detailed issues in test_feedback.txt"
            )
        else:
            # Read feedback content if available and include in message
            try:
                with open("test_feedback.txt", "r") as f:
                    feedback_content = f.read()
                await execute(
                    DeveloperImprover,
                    f"Refine app.py and templates/*.html to fix all issues reported in the following feedback:\n{feedback_content}"
                )
            except FileNotFoundError:
                # If feedback file missing, proceed without feedback message
                await execute(
                    DeveloperImprover,
                    "Improve app.py and templates/*.html based on latest available feedback."
                )

        # QAReviewer reviews revisions and writes approval status to test_feedback.txt
        await execute(
            QAReviewer,
            "Review updated app.py and templates/*.html against test_report.md and prior feedback; write approval status to test_feedback.txt"
        )

        # Check for approval status in test_feedback.txt
        try:
            with open("test_feedback.txt", "r") as f:
                status_content = f.read()
            if "[APPROVED]" in status_content:
                break
        except FileNotFoundError:
            # If file not found, continue loop to try again
            pass
# Phase4_End

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
    step3 = [
        testing_and_quality_assurance_phase()
    ]
    step4 = [
        refinement_loop_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)
    await asyncio.gather(*step4)

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
