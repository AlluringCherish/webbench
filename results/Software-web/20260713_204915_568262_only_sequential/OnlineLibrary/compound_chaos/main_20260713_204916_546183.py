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
# 20260713_204916_546183/main_20260713_204916_546183.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the OnlineLibrary requirements and produce a complete design_spec.md specifying all page designs, navigation routes, page titles, element IDs, data files format, and user interactions.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst reads the user task description and writes requirements_analysis.md outlining all requested pages, elements, \"\n        \"navigation, data formats, and user flows; only after its completion, \"\n        \"WebArchitect reads requirements_analysis.md and writes design_spec.md with detailed Flask route mappings, exact element IDs, \"\n        \"template and data file structures, and interaction contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in software requirements documentation and analysis for web applications.\n\nYour goal is to analyze the overall user task description and produce requirements_analysis.md detailing all page-level requirements to enable clear architectural design.\n\nTask Details:\n- Read user_task_description thoroughly for OnlineLibrary requirements\n- Identify and document all page titles, user-visible element IDs, and navigation buttons\n- Describe user interactions and functional flows between pages\n- Include descriptions of all data storage files and their formats as specified\n- Produce a comprehensive requirements analysis document covering all visible and functional aspects\n\nDocumentation Requirements:\n1. **Page Descriptions**:\n   - For each page, specify title, key element IDs with types, and purpose\n   - List all buttons and their navigation targets with button IDs\n\n2. **Navigation Flow**:\n   - Map navigation buttons to their target pages explicitly\n   - Include dynamic IDs patterns (e.g., view-book-button-{book_id}) and their semantics\n\n3. **Data Storage Formats**:\n   - Include all data files described in the user task with exact file names and field layouts\n   - Summarize example data formats for reference\n\n4. **User Flows**:\n   - Describe typical user scenarios (borrowing, reserving, reviewing)\n   - Indicate page transitions and actions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output requirements_analysis.md\n- Cover ALL pages exactly as per user description\n- Include all element IDs and their types precisely\n- Explicitly specify dynamic ID patterns\n- Document data files clearly with fields and examples\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in designing Flask web application architectures and technical specifications.\n\nYour goal is to convert a detailed requirements analysis document into a complete design_spec.md that specifies the Flask app structure, routes, template mappings, element IDs, data file schemas, and user interaction contracts.\n\nTask Details:\n- Read requirements_analysis.md fully and accurately\n- Map all user-facing pages to Flask routes (e.g., /dashboard, /catalog, /book/<id>)\n- Specify route methods (GET/POST) and template filenames for each route\n- Provide exact lists of element IDs per template with their types and purposes\n- Define data files parsing specifications: file paths, pipe-delimited fields, field ordering, and example data\n- Detail user interaction flows and post actions (e.g., borrow confirmation, review submission)\n- Ensure the root '/' route redirects to the dashboard page as the start point\n- Include any technical constraints or important notes on implementation\n\nSpecification Requirements:\n1. **Flask Routes Specification**:\n   - Table of routes: path, function name, HTTP methods, template file\n   - Context variables passed to templates, including types and structures\n\n2. **Template Element IDs**:\n   - Per template list of static and dynamic element IDs\n   - Patterns for dynamic IDs with variables (e.g., review-button-{review_id})\n\n3. **Data File Schemas**:\n   - For each data file, specify path and exact pipe-delimited fields order\n   - Provide example rows illustrating realistic data\n\n4. **User Actions and Flows**:\n   - Describe forms, buttons, and expected POST actions\n   - Confirm navigation consistency and correctness\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- Ensure all route functions have clear, consistent names\n- Maintain exact field and element ID naming as per requirements_analysis.md\n- Root route '/' MUST redirect to dashboard route\n- Support complete backend and frontend implementation based on this design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md fully covers all user-visible pages, with explicit element IDs, page titles, navigation buttons, \"\n                \"data storage formats, and functional descriptions before architecture begins.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the OnlineLibrary web application with a runnable Flask app.py and all required templates/*.html following design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer first writes app_draft.py and templates_draft/*.html implementing all requested pages with specified elements, navigation, \"\n        \"data file access as per design_spec.md; after completion, IntegrationEngineer refines and integrates drafts into final app.py and templates/*.html, \"\n        \"ensuring all route handlers, templates, and local file handling work flawlessly.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer experienced in Flask web application development.\n\nYour goal is to write the initial draft implementation of the OnlineLibrary web application, including app_draft.py and all HTML templates in templates_draft/ directory.\n\nTask Details:\n- Read design_spec.md for complete specifications on routes, page elements with exact IDs, navigation patterns, and data file reading/writing in data/ directory\n- Create app_draft.py implementing all Flask route handlers with render_template usage as per specification\n- Develop all templates_draft/*.html files matching specified page designs, element IDs, and navigation paths\n- Implement data file access strictly using data/*.txt files with pipe-delimited formats as per design_spec.md\n- Focus on correctness of routes, data loading, and template rendering, ensuring all pages and navigation flows are included\n\nImplementation Requirements:\n1. **Draft Backend (app_draft.py)**:\n   - Use Flask framework and implement all routes mentioned in design_spec.md\n   - For each route, return render_template() with appropriate template from templates_draft/\n   - Read and write data files in data/ directory following exact field orders and formats\n   - Include necessary imports and Flask app configuration (e.g., secret key)\n\n2. **Draft Frontend (templates_draft/)**:\n   - Create separate HTML template files for each page specified\n   - Use exact element IDs and structures as specified in design_spec.md\n   - Implement navigation buttons and links consistent with route names in app_draft.py\n   - Use Jinja2 syntax for dynamic content rendering and loops\n\n3. **Data File Handling**:\n   - Read data files in data/ directory using pipe delimiter ('|')\n   - Parse fields exactly as specified; handle empty or missing fields gracefully\n   - Do not hardcode data; read from files dynamically\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- Ensure all routes start from dashboard page as root\n- Element IDs must match design_spec.md exactly (case-sensitive)\n- Data read/write must comply strictly with data file formats defined\n- Do not add features or routes beyond those specified in design_spec.md and design_spec.md\n- Provide complete implementations, not partial snippets, using write_text_file for files\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer skilled in Flask web application refinement and integration.\n\nYour goal is to refine and integrate drafts produced by DraftEngineer into a final, runnable OnlineLibrary Flask app.py and finalized HTML templates in templates/ directory.\n\nTask Details:\n- Read design_spec.md and the drafts: app_draft.py and templates_draft/*.html\n- Remove any draft folder dependencies, ensuring app.py and templates/*.html are properly organized\n- Close design gaps to achieve complete compliance with design_spec.md requirements\n- Verify all routes start from the dashboard page and that navigation flows correctly through all pages\n- Ensure data file reading and writing use only data/*.txt files with exact formats and field orders\n- Confirm all element IDs from design_spec.md are present and correct in final templates\n- Guarantee final app.py and templates/*.html are fully functional and ready for deployment\n\nRefinement Requirements:\n1. **Code & Template Integration**:\n   - Merge draft code into clean, final app.py with proper route handlers and minimal redundancy\n   - Update template paths to templates/*.html and eliminate references to templates_draft/\n   - Refactor code for maintainability without altering specified functionality\n\n2. **Completeness Check**:\n   - Ensure every page and feature specified in design_spec.md is implemented and reachable\n   - Confirm all dynamic data bindings use correct Jinja2 syntax and variable names\n   - Validate that all navigation buttons link to correct Flask routes\n\n3. **Data Handling Verification**:\n   - Verify that all data file operations follow the pipe-delimited formats and field orders\n   - Fix any discrepancies in data file reading/writing logic from drafts\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and templates/*.html\n- Final artifacts must have no draft folder references or imports\n- Strictly follow design_spec.md instructions for all routes, data flows, and UI elements\n- Focus on integration quality, correctness, and completeness over adding new features\n- Do not provide implementation snippets in chat only; always save full files via write_text_file\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": \"Check app_draft.py and templates_draft/*.html against design_spec.md to ensure all routes, pages, element IDs, and local file handling conform before final integration.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the final OnlineLibrary app.py and templates/*.html for syntax, runtime, and functional correctness, producing a validation_report.md and corrected final app.py and templates.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator validates app.py and templates/*.html for syntax and runtime errors and tests all routes/functions as per design_spec.md, writing validation_report.md; \"\n        \"SequentialFixer then fixes all identified issues and produces the final corrected app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web applications.\n\nYour goal is to validate the final app.py and templates/*.html files to ensure syntax correctness, runtime stability, and functional compliance with design specifications.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Produce a detailed validation_report.md documenting syntax, runtime, and functional test results\n- Focus validation on route accessibility, template rendering, context variable correctness, and navigation flow as specified\n\nValidation Procedures:\n1. Syntax and Runtime Validation:\n   - Use validate_python_file tool on app.py for syntax and runtime errors\n   - Check template files for common HTML/Jinja2 errors by rendering or parsing\n\n2. Functional Testing:\n   - Execute app.py in a test environment using execute_python_code\n   - Programmatically access each Flask route defined in design_spec.md\n   - Verify HTTP response status codes, presence of key HTML elements by ID, and correct context data display\n\n3. Documentation:\n   - Write a clear validation_report.md including:\n     - Summary of syntax and runtime validations\n     - List of functional test cases with pass/fail status\n     - Detailed descriptions of any issues or discrepancies\n     - Suggestions for fixes or improvements\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools for testing\n- Write detailed validation_report.md using write_text_file tool\n- Report must cover ALL routes and templates as per design_spec.md\n- Maintain professional, clear, and actionable language in report\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in software refinement and bug fixing for Python Flask web applications.\n\nYour goal is to apply corrections to app.py and templates/*.html based on validation_report.md to produce a final, fully functional, and compliant system.\n\nTask Details:\n- Read validation_report.md, app.py, and templates/*.html from CONTEXT\n- Produce corrected app.py and templates/*.html files that address all reported issues\n- Ensure full conformity with design_spec.md requirements and validation feedback\n\nFixing Guidelines:\n1. Analyze validation_report.md for syntax, runtime, and functional defects\n2. Edit app.py to fix syntax errors, runtime failures, and incorrect implementations\n3. Modify templates/*.html to fix missing elements, incorrect IDs, improper context variable usage, and navigation errors\n4. Maintain coding best practices and consistency with design_spec.md\n5. Prepare final versions ready for deployment and further review\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output corrected app.py and templates/*.html files\n- Ensure all fixes directly address validation_report.md items\n- Retain full feature and route coverage as specified\n- Do NOT introduce unrelated changes\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": \"Ensure validation_report.md is complete, precise, and includes actionable items covering syntax, runtime, and functional tests per design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": \"Verify the final app.py and templates/*.html fully address and resolve validation_report.md issues and retain full requirement coverage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in software requirements documentation and analysis for web applications.

Your goal is to analyze the overall user task description and produce requirements_analysis.md detailing all page-level requirements to enable clear architectural design.

Task Details:
- Read user_task_description thoroughly for OnlineLibrary requirements
- Identify and document all page titles, user-visible element IDs, and navigation buttons
- Describe user interactions and functional flows between pages
- Include descriptions of all data storage files and their formats as specified
- Produce a comprehensive requirements analysis document covering all visible and functional aspects

Documentation Requirements:
1. **Page Descriptions**:
   - For each page, specify title, key element IDs with types, and purpose
   - List all buttons and their navigation targets with button IDs

2. **Navigation Flow**:
   - Map navigation buttons to their target pages explicitly
   - Include dynamic IDs patterns (e.g., view-book-button-{book_id}) and their semantics

3. **Data Storage Formats**:
   - Include all data files described in the user task with exact file names and field layouts
   - Summarize example data formats for reference

4. **User Flows**:
   - Describe typical user scenarios (borrowing, reserving, reviewing)
   - Indicate page transitions and actions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md
- Cover ALL pages exactly as per user description
- Include all element IDs and their types precisely
- Explicitly specify dynamic ID patterns
- Document data files clearly with fields and examples

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in designing Flask web application architectures and technical specifications.

Your goal is to convert a detailed requirements analysis document into a complete design_spec.md that specifies the Flask app structure, routes, template mappings, element IDs, data file schemas, and user interaction contracts.

Task Details:
- Read requirements_analysis.md fully and accurately
- Map all user-facing pages to Flask routes (e.g., /dashboard, /catalog, /book/<id>)
- Specify route methods (GET/POST) and template filenames for each route
- Provide exact lists of element IDs per template with their types and purposes
- Define data files parsing specifications: file paths, pipe-delimited fields, field ordering, and example data
- Detail user interaction flows and post actions (e.g., borrow confirmation, review submission)
- Ensure the root '/' route redirects to the dashboard page as the start point
- Include any technical constraints or important notes on implementation

Specification Requirements:
1. **Flask Routes Specification**:
   - Table of routes: path, function name, HTTP methods, template file
   - Context variables passed to templates, including types and structures

2. **Template Element IDs**:
   - Per template list of static and dynamic element IDs
   - Patterns for dynamic IDs with variables (e.g., review-button-{review_id})

3. **Data File Schemas**:
   - For each data file, specify path and exact pipe-delimited fields order
   - Provide example rows illustrating realistic data

4. **User Actions and Flows**:
   - Describe forms, buttons, and expected POST actions
   - Confirm navigation consistency and correctness

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Ensure all route functions have clear, consistent names
- Maintain exact field and element ID naming as per requirements_analysis.md
- Root route '/' MUST redirect to dashboard route
- Support complete backend and frontend implementation based on this design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend and Frontend Developer experienced in Flask web application development.

Your goal is to write the initial draft implementation of the OnlineLibrary web application, including app_draft.py and all HTML templates in templates_draft/ directory.

Task Details:
- Read design_spec.md for complete specifications on routes, page elements with exact IDs, navigation patterns, and data file reading/writing in data/ directory
- Create app_draft.py implementing all Flask route handlers with render_template usage as per specification
- Develop all templates_draft/*.html files matching specified page designs, element IDs, and navigation paths
- Implement data file access strictly using data/*.txt files with pipe-delimited formats as per design_spec.md
- Focus on correctness of routes, data loading, and template rendering, ensuring all pages and navigation flows are included

Implementation Requirements:
1. **Draft Backend (app_draft.py)**:
   - Use Flask framework and implement all routes mentioned in design_spec.md
   - For each route, return render_template() with appropriate template from templates_draft/
   - Read and write data files in data/ directory following exact field orders and formats
   - Include necessary imports and Flask app configuration (e.g., secret key)

2. **Draft Frontend (templates_draft/)**:
   - Create separate HTML template files for each page specified
   - Use exact element IDs and structures as specified in design_spec.md
   - Implement navigation buttons and links consistent with route names in app_draft.py
   - Use Jinja2 syntax for dynamic content rendering and loops

3. **Data File Handling**:
   - Read data files in data/ directory using pipe delimiter ('|')
   - Parse fields exactly as specified; handle empty or missing fields gracefully
   - Do not hardcode data; read from files dynamically

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Ensure all routes start from dashboard page as root
- Element IDs must match design_spec.md exactly (case-sensitive)
- Data read/write must comply strictly with data file formats defined
- Do not add features or routes beyond those specified in design_spec.md and design_spec.md
- Provide complete implementations, not partial snippets, using write_text_file for files

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer skilled in Flask web application refinement and integration.

Your goal is to refine and integrate drafts produced by DraftEngineer into a final, runnable OnlineLibrary Flask app.py and finalized HTML templates in templates/ directory.

Task Details:
- Read design_spec.md and the drafts: app_draft.py and templates_draft/*.html
- Remove any draft folder dependencies, ensuring app.py and templates/*.html are properly organized
- Close design gaps to achieve complete compliance with design_spec.md requirements
- Verify all routes start from the dashboard page and that navigation flows correctly through all pages
- Ensure data file reading and writing use only data/*.txt files with exact formats and field orders
- Confirm all element IDs from design_spec.md are present and correct in final templates
- Guarantee final app.py and templates/*.html are fully functional and ready for deployment

Refinement Requirements:
1. **Code & Template Integration**:
   - Merge draft code into clean, final app.py with proper route handlers and minimal redundancy
   - Update template paths to templates/*.html and eliminate references to templates_draft/
   - Refactor code for maintainability without altering specified functionality

2. **Completeness Check**:
   - Ensure every page and feature specified in design_spec.md is implemented and reachable
   - Confirm all dynamic data bindings use correct Jinja2 syntax and variable names
   - Validate that all navigation buttons link to correct Flask routes

3. **Data Handling Verification**:
   - Verify that all data file operations follow the pipe-delimited formats and field orders
   - Fix any discrepancies in data file reading/writing logic from drafts

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and templates/*.html
- Final artifacts must have no draft folder references or imports
- Strictly follow design_spec.md instructions for all routes, data flows, and UI elements
- Focus on integration quality, correctness, and completeness over adding new features
- Do not provide implementation snippets in chat only; always save full files via write_text_file

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web applications.

Your goal is to validate the final app.py and templates/*.html files to ensure syntax correctness, runtime stability, and functional compliance with design specifications.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Produce a detailed validation_report.md documenting syntax, runtime, and functional test results
- Focus validation on route accessibility, template rendering, context variable correctness, and navigation flow as specified

Validation Procedures:
1. Syntax and Runtime Validation:
   - Use validate_python_file tool on app.py for syntax and runtime errors
   - Check template files for common HTML/Jinja2 errors by rendering or parsing

2. Functional Testing:
   - Execute app.py in a test environment using execute_python_code
   - Programmatically access each Flask route defined in design_spec.md
   - Verify HTTP response status codes, presence of key HTML elements by ID, and correct context data display

3. Documentation:
   - Write a clear validation_report.md including:
     - Summary of syntax and runtime validations
     - List of functional test cases with pass/fail status
     - Detailed descriptions of any issues or discrepancies
     - Suggestions for fixes or improvements

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for testing
- Write detailed validation_report.md using write_text_file tool
- Report must cover ALL routes and templates as per design_spec.md
- Maintain professional, clear, and actionable language in report

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Engineer specializing in software refinement and bug fixing for Python Flask web applications.

Your goal is to apply corrections to app.py and templates/*.html based on validation_report.md to produce a final, fully functional, and compliant system.

Task Details:
- Read validation_report.md, app.py, and templates/*.html from CONTEXT
- Produce corrected app.py and templates/*.html files that address all reported issues
- Ensure full conformity with design_spec.md requirements and validation feedback

Fixing Guidelines:
1. Analyze validation_report.md for syntax, runtime, and functional defects
2. Edit app.py to fix syntax errors, runtime failures, and incorrect implementations
3. Modify templates/*.html to fix missing elements, incorrect IDs, improper context variable usage, and navigation errors
4. Maintain coding best practices and consistency with design_spec.md
5. Prepare final versions ready for deployment and further review

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output corrected app.py and templates/*.html files
- Ensure all fixes directly address validation_report.md items
- Retain full feature and route coverage as specified
- Do NOT introduce unrelated changes

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md fully covers all user-visible pages, with explicit element IDs, page titles, navigation buttons, "
                "data storage formats, and functional descriptions before architecture begins.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Check app_draft.py and templates_draft/*.html against design_spec.md to ensure all routes, pages, element IDs, and local file handling conform before final integration.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Ensure validation_report.md is complete, precise, and includes actionable items covering syntax, runtime, and functional tests per design_spec.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify the final app.py and templates/*.html fully address and resolve validation_report.md issues and retain full requirement coverage.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    # Create agents
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=220,
        failure_threshold=1,
        recovery_time=30
    )
    WebArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution flow
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst, "Analyze user task description and produce comprehensive requirements_analysis.md covering all pages, element IDs, navigation buttons, user flows, and data storage formats.")

    # Read requirements_analysis.md file content for WebArchitect
    requirements_analysis = ""
    try:
        requirements_analysis = open("requirements_analysis.md").read()
    except:
        pass

    # Step 2: WebArchitect produces design_spec.md based on requirements_analysis.md
    await execute(WebArchitect, f"Based on requirements_analysis.md content below, create design_spec.md specifying Flask routes, templates, element IDs, data file schemas, and user interactions.\n\n=== requirements_analysis.md ===\n{requirements_analysis}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # DraftEngineer executes first to produce drafts (app_draft.py and templates_draft/*.html)
    await execute(DraftEngineer,
                  "Read design_spec.md and implement app_draft.py and all templates_draft/*.html for OnlineLibrary Flask app. "
                  "Include all routes, data loading from data/*.txt, element IDs exactly as specified.")

    # Read drafts for IntegrationEngineer
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except Exception:
        pass
    try:
        import glob
        import os
        drafts = glob.glob("templates_draft/*.html")
        templates_files_content = []
        for file_path in drafts:
            try:
                content = open(file_path).read()
                templates_files_content.append(f"=== {os.path.basename(file_path)} ===\n{content}\n")
            except Exception:
                continue
        templates_draft_content = "\n".join(templates_files_content)
    except Exception:
        pass

    # IntegrationEngineer refines drafts into final app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Read design_spec.md for final specifications.\n"
                  f"Integrate drafts from DraftEngineer into final app.py and templates/*.html.\n"
                  f"Remove all draft folder dependencies.\n"
                  f"Ensure routes start with dashboard page and all element IDs, navigation, and data file access conform to design_spec.md.\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n"
                  f"=== templates_draft ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    # Create agents
    WebValidator = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file contents for injection
    design_spec_md = ""
    app_py = ""
    templates_html = ""
    try:
        design_spec_md = open("design_spec.md").read()
    except:
        pass
    try:
        app_py = open("app.py").read()
    except:
        pass
    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_content_list = []
        for tf in template_files:
            try:
                content = open(tf).read()
                templates_content_list.append(f"=== {tf} ===\n{content}")
            except:
                pass
        templates_html = "\n\n".join(templates_content_list)
    except:
        templates_html = ""

    # Execute WebValidator
    await execute(WebValidator,
                  f"Read design_spec.md, app.py, templates/*.html for syntax, runtime, and functional validation. "
                  f"Use validate_python_file on app.py. "
                  f"Use execute_python_code for testing routes per design_spec.md. "
                  f"Check templates for HTML/Jinja2 errors. "
                  f"Write detailed validation_report.md summarizing all findings.\n\n"
                  f"=== design_spec.md ===\n{design_spec_md}\n\n=== app.py ===\n{app_py}\n\n=== templates/*.html ===\n{templates_html}")

    # Read validation_report.md content for SequentialFixer injection
    validation_report_md = ""
    try:
        validation_report_md = open("validation_report.md").read()
    except:
        pass

    # Execute SequentialFixer to fix all reported issues
    await execute(SequentialFixer,
                  f"Read validation_report.md, app.py, templates/*.html from CONTEXT. "
                  f"Fix all syntax, runtime and functional issues per report, fully conforming to design_spec.md. "
                  f"Output corrected app.py and templates/*.html files.\n\n"
                  f"=== validation_report.md ===\n{validation_report_md}\n\n"
                  f"=== app.py ===\n{app_py}\n\n=== templates/*.html ===\n{templates_html}")
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
