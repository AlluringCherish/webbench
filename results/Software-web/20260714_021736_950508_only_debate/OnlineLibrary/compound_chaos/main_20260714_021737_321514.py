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
# 20260714_021737_321514/main_20260714_021737_321514.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Debate the adaptive Web design contract for the OnlineLibrary app for exactly two total rounds and produce a unified design_spec.md document.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = \"DesignDebaterA and DesignDebaterB independently draft design artifacts for the OnlineLibrary app in round 1, revise from each other's drafts in round 2, then DesignJudge adjudicates and synthesizes the final design_spec.md incorporating the user requirements and exact page routes, elements, and file data formats.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignDebaterA\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create and improve a detailed design_debate_a.md for the OnlineLibrary application through exactly two total debate rounds.\n\nTask Details:\n- Read user_task_description each round focusing on the 'OnlineLibrary' web app requirements\n- In round 1, independently write a complete design_debate_a.md covering Flask routes, HTTP methods, templates, page navigation flows, element IDs, and local text file data handling\n- In round 2, read previous design_debate_a.md and peer design_debate_b.md; update your design_debate_a.md incorporating valid peer improvements only\n- Overwrite the entire design_debate_a.md artifact every round\n\n**Section 1: Flask Routes Specification**\n- Precisely specify all route paths, HTTP methods, corresponding template files, and required context variables for each of the ten pages declared by the user\n- Ensure routes preserve all user-declared page names and enable the Dashboard as the default entry '/'\n- Specify navigation targets and transitions exactly as per user page design\n- Maintain correct mapping of page element IDs and dynamic IDs for repeated elements (e.g., buttons with {book_id})\n\n**Section 2: HTML Template and Page Elements**\n- Document template file names and page titles exactly as stated by the user\n- List all UI element IDs and their types per page, preserving dynamic IDs formatting\n- Specify interactions like buttons and forms with exact field names and methods when relevant\n\n**Section 3: Data Persistence and Local Text Files**\n- Specify data files used per functionality, respecting the exact file names and formats given\n- Map how Flask routes access and update the local text files in the 'data' directory\n- Include data format schemas and delimiters as per specification with no deviations\n\nCRITICAL SUCCESS CRITERIA:\n- Implement two total debate rounds: independent round 1 and one peer-informed round 2\n- Produce a comprehensive, implementation-ready design_debate_a.md each round\n- Keep all user-declared routes, methods, element IDs, navigation flows, and local text data schemas exact\n- Use write_text_file tool to output design_debate_a.md\n\nOutput: design_debate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignDebaterB\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create and improve a comprehensive design_debate_b.md for the OnlineLibrary application through exactly two total debate rounds.\n\nTask Details:\n- Read user_task_description each round with attention to adaptive Flask route contracts and page element IDs\n- In round 1, independently write a complete design_debate_b.md that defines exact Flask route contracts, page context variables, local text file data integration, and dynamic element ID usage\n- In round 2, revise design_debate_b.md based on review of own and peer designs (design_debate_a.md) keeping conformance to user requirements and the adaptive web contract\n- Overwrite the entire design_debate_b.md artifact every round\n\n**Section 1: Flask Route Contracts**\n- Specify all user-declared routes with HTTP methods, templates, expected context variables, and form definitions\n- Preserve the exact page routes, including dynamic parameters such as {book_id}, {borrow_id}, etc.\n- Ensure default route '/' renders or redirects to Dashboard page\n\n**Section 2: Context Variables and Page Navigation**\n- Define all context variables passed to templates, including dynamic data from local files\n- List client-side element IDs, including dynamically generated IDs, exactly as declared\n- Specify navigation flows between pages using button or link element IDs\n\n**Section 3: Local Text Data Integration**\n- Describe reading and writing of local text files with the exact filenames and schema\n- Ensure correct data mapping between route handlers and local file persistence\n- Maintain use of 'data' directory and '|' delimiter text formats without alteration\n\nCRITICAL SUCCESS CRITERIA:\n- Perform exactly two total rounds: initial independent and one peer-informed revision\n- Provide complete design_debate_b.md in each round, strictly following the adaptive web design contract\n- Use write_text_file tool for saving design_debate_b.md\n\nOutput: design_debate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignJudge\",\n            \"prompt\": \"\"\"You are a Senior System Architect adjudicating two competing Flask web application designs for the OnlineLibrary app.\n\nYour goal is to write a single authoritative design_spec.md document merging the final artifacts from both debaters after exactly two debate rounds, respecting the user requirements strictly.\n\nTask Details:\n- Read user_task_description, final design_debate_a.md, and design_debate_b.md \n- Compare all Flask routes, templates, page element IDs, context variables, navigation flows, and local text file interactions\n- Resolve conflicts or differences strictly based on the user requirements document, preserving declared routes, HTTP methods, element IDs including dynamic ones, and data formats\n- Write a full and internally consistent canonical design_spec.md that supports implementation without omitted routes or overlooked data handling\n\n**Section 1: Flask Routes and Methods**\n- Enumerate all user-declared page routes, HTTP methods, and associated templates\n- Prescribe exact function names, URL parameters, and expected context variables\n- Ensure '/' serves or redirects to the Dashboard page precisely\n\n**Section 2: HTML Template Specifications and Elements**\n- Specify all page template files, titles, and element IDs with exact naming (including dynamic )\n- Detail navigation flows between pages with exact button IDs for links or actions\n\n**Section 3: Local Text Data Files and Formats**\n- Describe the local text files used (filenames, directories, delimiter '|', field schemas)\n- Confirm how the web app reads from and writes to these files per user functionality\n- Maintain the data directory organization without adding files or altering schema\n\nCRITICAL SUCCESS CRITERIA:\n- Final design_spec.md must be complete, internally consistent, and fulfill the user's original detailed requirements\n- Preserve every declared page, route, element ID, HTTP method, field name, navigation path, and file format\n- Use write_text_file tool to save design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignDebaterA\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Verify design_debate_a.md exists, is non-empty, coherent, follows requirements format, contains Flask route specs for all user-declared pages including element IDs and data persistence.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignDebaterB\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Check design_debate_b.md exists, is relevant, readable, specifies adaptive web contract conformance including exact routes, forms, and page element IDs.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignJudge\",\n            \"reviewer_agent\": \"DesignDebaterA\",\n            \"review_criteria\": \"Confirm design_spec.md exists, is non-empty, correct, complete with the final canonical web design definition meeting user requirements as specified.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Debate full Python Flask implementation of OnlineLibrary with all defined routes, templates, local text data management, and UI elements for exactly two total rounds and produce final app.py and templates/*.html artifacts.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = \"ImplementationDebaterA and ImplementationDebaterB independently develop candidate app.py and templates sets from design_spec.md in round 1, each revises their versions with peer insights in round 2, then ImplementationJudge combines and adjudicates the final complete app.py and HTML templates without adding features.\",\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDebaterA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specialized in full-stack web application implementation focusing on backend logic, frontend templates, and local text file data handling.\n\nYour goal is to create and revise a complete Flask app.py and a full set of HTML templates implementing all specified routes, UI elements, page titles, precise HTML element IDs (including dynamic IDs), navigation flows, and local text file data management as defined for the OnlineLibrary application.\n\nTask Details:\n- Read design_spec.md fully each round for precise route, template, and data requirements\n- Produce or update app_debate_a.py and templates_debate_a/*.html implementing all defined pages and behaviors\n- Preserve all exact user-declared route paths, HTTP methods, template file names, context variables, HTML element IDs (static and dynamic), form actions/methods, and navigation targets\n- In round 2, use app_debate_b.py and templates_debate_b/*.html peer artifacts to improve and correct your implementation\n- Use local text files as specified for data loading and persistence under ‘data’ directory using pipe delimiter\n\n**Section 1: Flask Application Implementation Requirements**\n- Implement all Flask routes matching the declared URLs in design_spec.md, including the root route `/` rendering or redirecting to Dashboard page\n- Ensure GET and POST methods as specified, preserving exact form field names and submission behaviors\n- Handle data read/write exclusively via local text files as per given formats, parsing pipe-delimited records accurately\n- Incorporate borrowing logic, reservation management, reviews, payments, and user profile edits respecting data integrity and specified UI flows\n\n**Section 2: HTML Template Implementation Guidelines**\n- Implement all templates with file names and folder structure reflecting templates_debate_a/*.html\n- Ensure page titles and precise HTML element IDs exactly match the specification including dynamic IDs like `view-book-button-{book_id}`\n- Maintain consistent navigation buttons with exact target routes and element IDs\n- Preserve form element names, methods, and actions as declared, supporting all user inputs for searches, reviews, profile updates, borrow confirmations, and payments\n\n**Section 3: Revision and Consistency Rules**\n- In round 2, analyze provided peer app_debate_b.py and templates_debate_b/*.html to identify discrepancies or missed requirements\n- Correct your own candidate app_debate_a.py and templates_debate_a/*.html accordingly without adding unrequested features\n- Ensure consistent data usage, route implementations, and UI element presence between your artifacts and peer artifacts\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool for saving the complete app_debate_a.py and every template file in templates_debate_a/\n- Strictly adhere to all user-specified route paths, HTTP methods, template names, context variables, HTML element IDs (including dynamic), form field names, and local text file data formats\n- Implement exact navigation flows, including `/` rendering or redirecting to Dashboard page\n- Produce output files only: app_debate_a.py and templates_debate_a/*.html, no additional outputs or refinement markers\n\nOutput: app_debate_a.py and templates_debate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDebaterB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in implementing comprehensive web applications with full backend and frontend integration, optimized for local text file data persistence.\n\nYour goal is to develop and revise an independent Flask app_debate_b.py along with a complete set of templates_debate_b/*.html implementing all Functionalities, routes, and UI interfaces for OnlineLibrary as specified.\n\nTask Details:\n- Fully absorb design_spec.md input to understand all required routes, context variables, element IDs, and data handling\n- Independently build or update app_debate_b.py and templates_debate_b/*.html incorporating all pages, UI components, and local file data management\n- Maintain exact matching of user-declared route paths, HTTP methods, HTML element IDs (including dynamic IDs), form field names, navigation targets, and data file operations\n- In round 2, consult app_debate_a.py and templates_debate_a/*.html for peer input to enhance completeness and correctness\n- Employ pipe-delimited local text files as the sole data source/sink within the ‘data’ directory, applying correct parsing and writing\n\n**Section 1: Flask Backend Implementation**\n- Realize all Flask routes per specification, providing exact GET/POST method behaviors, including root `/` that must load or redirect to Dashboard\n- Implement borrow, return, reservation, review, profile, and payment endpoints accurately reading/writing the designated text files\n- Ensure code clarity and maintain consistent variable naming aligned with design_spec.md\n\n**Section 2: HTML Frontend Template Implementation**\n- Deliver all templates according to the declared filenames under templates_debate_b/\n- All elements must have the precise HTML IDs specified; for dynamic IDs such as `return-book-button-{borrow_id}`, generate as required\n- Include all navigation and buttons as specified with their exact IDs and targets\n- Preserve form characteristics including method, action, field names for all input controls\n\n**Section 3: Peer Review Integration**\n- For the revision round, analyze the peer app_debate_a.py and templates_debate_a/*.html to identify deficiencies or missing elements\n- Improve your candidate outputs accordingly without introducing non-specified features\n- Maintain strict compliance with user declarations across all artifacts and rounds\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app_debate_b.py and templates_debate_b/*.html files\n- Do not deviate from explicit user requirements including routes, element IDs, and data formats\n- Root route `/` must render or redirect to Dashboard page precisely as specified\n- Only produce declared output files; avoid extraneous commentary or refinement markers\n\nOutput: app_debate_b.py and templates_debate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationJudge\",\n            \"prompt\": \"\"\"You are a Senior Python Flask Developer and Integrator responsible for adjudicating two competing implementations into a final canonical online library web application.\n\nYour goal is to synthesize, reconcile, and write a comprehensive, fully functional app.py and complete set of templates/*.html consistent strictly with design_spec.md, app_debate_a.py, app_debate_b.py, and their respective template sets, without adding additional features.\n\nTask Details:\n- Read design_spec.md for authoritative requirements and context including all routes, templates, UI elements, and local text file data formats\n- Consume final round outputs: app_debate_a.py and templates_debate_a/*.html plus app_debate_b.py and templates_debate_b/*.html\n- Compare and merge Flask routes, application logic, and template HTML elements ensuring correctness and completeness\n- Resolve any conflicting implementations in favor of user declared specifications with no enhancements\n- Produce one canonical app.py implementing all required features with exact route paths, HTTP methods, data handling, and navigation flows\n- Produce canonical templates/*.html files with precise element IDs, dynamic IDs, page titles, and form structures matching spec\n\n**Section 1: Integration and Consistency Verification**\n- Validate all routes, methods, and navigation flows present in both candidates and conforming to design_spec.md\n- Ensure all local data file operations align to declared file formats and file paths under 'data' directory\n- Confirm every UI element ID and dynamic ID matches the authoritative page design, preserving user expectations\n\n**Section 2: Canonical Artifact Generation**\n- Deliver a single app.py and a set of templates/*.html files representing the authoritative implementation\n- Ensure root path `/` renders or redirects to the Dashboard page exactly\n- Use write_text_file tool to save all outputs cleanly without auxiliary commentary or extra files\n\nCRITICAL SUCCESS CRITERIA:\n- Final artifacts fully implement all pages, routes, UI elements, and data handling per user specification and design_spec.md\n- No new features or requirements are introduced beyond user directives\n- All file names, IDs, methods, and navigation targets are exactly as specified\n- Outputs are ready for functional deployment as a Flask application\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDebaterA\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve candidate app_debate_a.py and templates_debate_a/*.html presence, readability, adherence to design_spec.md, and absence of catastrophic errors; no full completion required.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDebaterB\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve candidate app_debate_b.py and templates_debate_b/*.html presence, accuracy, conformity to design_spec.md, and no catastrophic mistakes; no full completion required.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationJudge\",\n            \"reviewer_agent\": \"ImplementationDebaterA\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html exist, are readable, fully implement design_spec.md with no feature additions, and are broadly usable as a Flask application.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignDebaterA": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and improve a detailed design_debate_a.md for the OnlineLibrary application through exactly two total debate rounds.

Task Details:
- Read user_task_description each round focusing on the 'OnlineLibrary' web app requirements
- In round 1, independently write a complete design_debate_a.md covering Flask routes, HTTP methods, templates, page navigation flows, element IDs, and local text file data handling
- In round 2, read previous design_debate_a.md and peer design_debate_b.md; update your design_debate_a.md incorporating valid peer improvements only
- Overwrite the entire design_debate_a.md artifact every round

**Section 1: Flask Routes Specification**
- Precisely specify all route paths, HTTP methods, corresponding template files, and required context variables for each of the ten pages declared by the user
- Ensure routes preserve all user-declared page names and enable the Dashboard as the default entry '/'
- Specify navigation targets and transitions exactly as per user page design
- Maintain correct mapping of page element IDs and dynamic IDs for repeated elements (e.g., buttons with {book_id})

**Section 2: HTML Template and Page Elements**
- Document template file names and page titles exactly as stated by the user
- List all UI element IDs and their types per page, preserving dynamic IDs formatting
- Specify interactions like buttons and forms with exact field names and methods when relevant

**Section 3: Data Persistence and Local Text Files**
- Specify data files used per functionality, respecting the exact file names and formats given
- Map how Flask routes access and update the local text files in the 'data' directory
- Include data format schemas and delimiters as per specification with no deviations

CRITICAL SUCCESS CRITERIA:
- Implement two total debate rounds: independent round 1 and one peer-informed round 2
- Produce a comprehensive, implementation-ready design_debate_a.md each round
- Keep all user-declared routes, methods, element IDs, navigation flows, and local text data schemas exact
- Use write_text_file tool to output design_debate_a.md

Output: design_debate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_a.md'}],

    },

    "DesignDebaterB": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and improve a comprehensive design_debate_b.md for the OnlineLibrary application through exactly two total debate rounds.

Task Details:
- Read user_task_description each round with attention to adaptive Flask route contracts and page element IDs
- In round 1, independently write a complete design_debate_b.md that defines exact Flask route contracts, page context variables, local text file data integration, and dynamic element ID usage
- In round 2, revise design_debate_b.md based on review of own and peer designs (design_debate_a.md) keeping conformance to user requirements and the adaptive web contract
- Overwrite the entire design_debate_b.md artifact every round

**Section 1: Flask Route Contracts**
- Specify all user-declared routes with HTTP methods, templates, expected context variables, and form definitions
- Preserve the exact page routes, including dynamic parameters such as {book_id}, {borrow_id}, etc.
- Ensure default route '/' renders or redirects to Dashboard page

**Section 2: Context Variables and Page Navigation**
- Define all context variables passed to templates, including dynamic data from local files
- List client-side element IDs, including dynamically generated IDs, exactly as declared
- Specify navigation flows between pages using button or link element IDs

**Section 3: Local Text Data Integration**
- Describe reading and writing of local text files with the exact filenames and schema
- Ensure correct data mapping between route handlers and local file persistence
- Maintain use of 'data' directory and '|' delimiter text formats without alteration

CRITICAL SUCCESS CRITERIA:
- Perform exactly two total rounds: initial independent and one peer-informed revision
- Provide complete design_debate_b.md in each round, strictly following the adaptive web design contract
- Use write_text_file tool for saving design_debate_b.md

Output: design_debate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_b.md'}],

    },

    "DesignJudge": {
        "prompt": (
            """You are a Senior System Architect adjudicating two competing Flask web application designs for the OnlineLibrary app.

Your goal is to write a single authoritative design_spec.md document merging the final artifacts from both debaters after exactly two debate rounds, respecting the user requirements strictly.

Task Details:
- Read user_task_description, final design_debate_a.md, and design_debate_b.md 
- Compare all Flask routes, templates, page element IDs, context variables, navigation flows, and local text file interactions
- Resolve conflicts or differences strictly based on the user requirements document, preserving declared routes, HTTP methods, element IDs including dynamic ones, and data formats
- Write a full and internally consistent canonical design_spec.md that supports implementation without omitted routes or overlooked data handling

**Section 1: Flask Routes and Methods**
- Enumerate all user-declared page routes, HTTP methods, and associated templates
- Prescribe exact function names, URL parameters, and expected context variables
- Ensure '/' serves or redirects to the Dashboard page precisely

**Section 2: HTML Template Specifications and Elements**
- Specify all page template files, titles, and element IDs with exact naming (including dynamic )
- Detail navigation flows between pages with exact button IDs for links or actions

**Section 3: Local Text Data Files and Formats**
- Describe the local text files used (filenames, directories, delimiter '|', field schemas)
- Confirm how the web app reads from and writes to these files per user functionality
- Maintain the data directory organization without adding files or altering schema

CRITICAL SUCCESS CRITERIA:
- Final design_spec.md must be complete, internally consistent, and fulfill the user's original detailed requirements
- Preserve every declared page, route, element ID, HTTP method, field name, navigation path, and file format
- Use write_text_file tool to save design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDebaterA": {
        "prompt": (
            """You are a Python Flask Developer specialized in full-stack web application implementation focusing on backend logic, frontend templates, and local text file data handling.

Your goal is to create and revise a complete Flask app.py and a full set of HTML templates implementing all specified routes, UI elements, page titles, precise HTML element IDs (including dynamic IDs), navigation flows, and local text file data management as defined for the OnlineLibrary application.

Task Details:
- Read design_spec.md fully each round for precise route, template, and data requirements
- Produce or update app_debate_a.py and templates_debate_a/*.html implementing all defined pages and behaviors
- Preserve all exact user-declared route paths, HTTP methods, template file names, context variables, HTML element IDs (static and dynamic), form actions/methods, and navigation targets
- In round 2, use app_debate_b.py and templates_debate_b/*.html peer artifacts to improve and correct your implementation
- Use local text files as specified for data loading and persistence under ‘data’ directory using pipe delimiter

**Section 1: Flask Application Implementation Requirements**
- Implement all Flask routes matching the declared URLs in design_spec.md, including the root route `/` rendering or redirecting to Dashboard page
- Ensure GET and POST methods as specified, preserving exact form field names and submission behaviors
- Handle data read/write exclusively via local text files as per given formats, parsing pipe-delimited records accurately
- Incorporate borrowing logic, reservation management, reviews, payments, and user profile edits respecting data integrity and specified UI flows

**Section 2: HTML Template Implementation Guidelines**
- Implement all templates with file names and folder structure reflecting templates_debate_a/*.html
- Ensure page titles and precise HTML element IDs exactly match the specification including dynamic IDs like `view-book-button-{book_id}`
- Maintain consistent navigation buttons with exact target routes and element IDs
- Preserve form element names, methods, and actions as declared, supporting all user inputs for searches, reviews, profile updates, borrow confirmations, and payments

**Section 3: Revision and Consistency Rules**
- In round 2, analyze provided peer app_debate_b.py and templates_debate_b/*.html to identify discrepancies or missed requirements
- Correct your own candidate app_debate_a.py and templates_debate_a/*.html accordingly without adding unrequested features
- Ensure consistent data usage, route implementations, and UI element presence between your artifacts and peer artifacts

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool for saving the complete app_debate_a.py and every template file in templates_debate_a/
- Strictly adhere to all user-specified route paths, HTTP methods, template names, context variables, HTML element IDs (including dynamic), form field names, and local text file data formats
- Implement exact navigation flows, including `/` rendering or redirecting to Dashboard page
- Produce output files only: app_debate_a.py and templates_debate_a/*.html, no additional outputs or refinement markers

Output: app_debate_a.py and templates_debate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}],

    },

    "ImplementationDebaterB": {
        "prompt": (
            """You are a Python Flask Developer specializing in implementing comprehensive web applications with full backend and frontend integration, optimized for local text file data persistence.

Your goal is to develop and revise an independent Flask app_debate_b.py along with a complete set of templates_debate_b/*.html implementing all Functionalities, routes, and UI interfaces for OnlineLibrary as specified.

Task Details:
- Fully absorb design_spec.md input to understand all required routes, context variables, element IDs, and data handling
- Independently build or update app_debate_b.py and templates_debate_b/*.html incorporating all pages, UI components, and local file data management
- Maintain exact matching of user-declared route paths, HTTP methods, HTML element IDs (including dynamic IDs), form field names, navigation targets, and data file operations
- In round 2, consult app_debate_a.py and templates_debate_a/*.html for peer input to enhance completeness and correctness
- Employ pipe-delimited local text files as the sole data source/sink within the ‘data’ directory, applying correct parsing and writing

**Section 1: Flask Backend Implementation**
- Realize all Flask routes per specification, providing exact GET/POST method behaviors, including root `/` that must load or redirect to Dashboard
- Implement borrow, return, reservation, review, profile, and payment endpoints accurately reading/writing the designated text files
- Ensure code clarity and maintain consistent variable naming aligned with design_spec.md

**Section 2: HTML Frontend Template Implementation**
- Deliver all templates according to the declared filenames under templates_debate_b/
- All elements must have the precise HTML IDs specified; for dynamic IDs such as `return-book-button-{borrow_id}`, generate as required
- Include all navigation and buttons as specified with their exact IDs and targets
- Preserve form characteristics including method, action, field names for all input controls

**Section 3: Peer Review Integration**
- For the revision round, analyze the peer app_debate_a.py and templates_debate_a/*.html to identify deficiencies or missing elements
- Improve your candidate outputs accordingly without introducing non-specified features
- Maintain strict compliance with user declarations across all artifacts and rounds

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app_debate_b.py and templates_debate_b/*.html files
- Do not deviate from explicit user requirements including routes, element IDs, and data formats
- Root route `/` must render or redirect to Dashboard page precisely as specified
- Only produce declared output files; avoid extraneous commentary or refinement markers

Output: app_debate_b.py and templates_debate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}],

    },

    "ImplementationJudge": {
        "prompt": (
            """You are a Senior Python Flask Developer and Integrator responsible for adjudicating two competing implementations into a final canonical online library web application.

Your goal is to synthesize, reconcile, and write a comprehensive, fully functional app.py and complete set of templates/*.html consistent strictly with design_spec.md, app_debate_a.py, app_debate_b.py, and their respective template sets, without adding additional features.

Task Details:
- Read design_spec.md for authoritative requirements and context including all routes, templates, UI elements, and local text file data formats
- Consume final round outputs: app_debate_a.py and templates_debate_a/*.html plus app_debate_b.py and templates_debate_b/*.html
- Compare and merge Flask routes, application logic, and template HTML elements ensuring correctness and completeness
- Resolve any conflicting implementations in favor of user declared specifications with no enhancements
- Produce one canonical app.py implementing all required features with exact route paths, HTTP methods, data handling, and navigation flows
- Produce canonical templates/*.html files with precise element IDs, dynamic IDs, page titles, and form structures matching spec

**Section 1: Integration and Consistency Verification**
- Validate all routes, methods, and navigation flows present in both candidates and conforming to design_spec.md
- Ensure all local data file operations align to declared file formats and file paths under 'data' directory
- Confirm every UI element ID and dynamic ID matches the authoritative page design, preserving user expectations

**Section 2: Canonical Artifact Generation**
- Deliver a single app.py and a set of templates/*.html files representing the authoritative implementation
- Ensure root path `/` renders or redirects to the Dashboard page exactly
- Use write_text_file tool to save all outputs cleanly without auxiliary commentary or extra files

CRITICAL SUCCESS CRITERIA:
- Final artifacts fully implement all pages, routes, UI elements, and data handling per user specification and design_spec.md
- No new features or requirements are introduced beyond user directives
- All file names, IDs, methods, and navigation targets are exactly as specified
- Outputs are ready for functional deployment as a Flask application

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignDebaterA': [
        ("DesignJudge", """Verify design_debate_a.md exists, is non-empty, coherent, follows requirements format, contains Flask route specs for all user-declared pages including element IDs and data persistence.""", [{'type': 'text_file', 'name': 'design_debate_a.md'}])
    ],

    'DesignDebaterB': [
        ("DesignJudge", """Check design_debate_b.md exists, is relevant, readable, specifies adaptive web contract conformance including exact routes, forms, and page element IDs.""", [{'type': 'text_file', 'name': 'design_debate_b.md'}])
    ],

    'DesignJudge': [
        ("DesignDebaterA", """Confirm design_spec.md exists, is non-empty, correct, complete with the final canonical web design definition meeting user requirements as specified.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDebaterA': [
        ("ImplementationJudge", """Approve candidate app_debate_a.py and templates_debate_a/*.html presence, readability, adherence to design_spec.md, and absence of catastrophic errors; no full completion required.""", [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}])
    ],

    'ImplementationDebaterB': [
        ("ImplementationJudge", """Approve candidate app_debate_b.py and templates_debate_b/*.html presence, accuracy, conformity to design_spec.md, and no catastrophic mistakes; no full completion required.""", [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}])
    ],

    'ImplementationJudge': [
        ("ImplementationDebaterA", """Confirm final app.py and templates/*.html exist, are readable, fully implement design_spec.md with no feature additions, and are broadly usable as a Flask application.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=30
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        design_a_text = ""
        design_b_text = ""
        if round_num > 1:
            try:
                design_a_text = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a_text = ""
            try:
                design_b_text = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b_text = ""
        if round_num == 1:
            msg_a = "(No peer draft yet - this is the initial round)"
            msg_b = "(No peer draft yet - this is the initial round)"
        else:
            msg_a = f"Peer DesignDebaterB draft:\n{design_b_text}"
            msg_b = f"Peer DesignDebaterA draft:\n{design_a_text}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After two rounds, DesignJudge adjudicates and synthesizes the final canonical design_spec.md
    try:
        design_a_text = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        design_a_text = ""
    try:
        design_b_text = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        design_b_text = ""

    await execute(
        DesignJudge,
        "Adjudicate and merge the final design drafts from DesignDebaterA and DesignDebaterB into a single cohesive design_spec.md.\n\n"
        "=== DesignDebateA ===\n" + design_a_text + "\n\n=== DesignDebateB ===\n" + design_b_text
    )
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    ImplementationDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial drafts, 2=peer-informed revisions)
    for round_num in range(1, 3):
        peer_a_app = peer_a_templates = peer_b_app = peer_b_templates = ""

        if round_num > 1:
            try:
                peer_b_app = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                peer_b_app = ""
            peer_b_templates = ""
            for tpl_path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    peer_b_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

            try:
                peer_a_app = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                peer_a_app = ""
            peer_a_templates = ""
            for tpl_path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    peer_a_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

        if round_num == 1:
            msg_a = "Round 1 of 2: independently create full app_debate_a.py and templates_debate_a/*.html from design_spec.md."
            msg_b = "Round 1 of 2: independently create full app_debate_b.py and templates_debate_b/*.html from design_spec.md."
        else:
            msg_a = (
                "Round 2 of 2: revise app_debate_a.py and templates_debate_a/*.html using peer artifacts below.\n\n"
                "=== Peer app_debate_b.py ===\n" + peer_b_app + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + peer_b_templates
            )
            msg_b = (
                "Round 2 of 2: revise app_debate_b.py and templates_debate_b/*.html using peer artifacts below.\n\n"
                "=== Peer app_debate_a.py ===\n" + peer_a_app + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + peer_a_templates
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # After 2 rounds, read both final candidates fully
    try:
        final_a_app = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        final_a_app = ""
    final_a_templates = ""
    for tpl_path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            final_a_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    try:
        final_b_app = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        final_b_app = ""
    final_b_templates = ""
    for tpl_path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            final_b_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    # ImplementationJudge compares and adjudicates final app and templates
    await execute(
        ImplementationJudge,
        "Adjudicate the two final round-2 candidates and write final canonical app.py and templates/*.html.\n\n"
        "=== Candidate A app_debate_a.py ===\n" + final_a_app + "\n\n"
        "=== Candidate A templates_debate_a/*.html ===\n" + final_a_templates + "\n\n"
        "=== Candidate B app_debate_b.py ===\n" + final_b_app + "\n\n"
        "=== Candidate B templates_debate_b/*.html ===\n" + final_b_templates
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
