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
# 20260714_001749_998926/main_20260714_001749_998926.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the comprehensive design specification for the 'OnlineLibrary' Python web application and produce design_spec.md and gated design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator creates or revises design_spec.md based on user_task_description and prior design_feedback.md; DesignCritic reviews the design_spec.md, producing design_feedback.md with approval or modification requests. The loop runs for at most two iterations, stopping early if DesignCritic's feedback begins with [APPROVED].\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to produce a detailed, adaptive design specification document that describes all web pages, element IDs, data formats, and local storage structure for the 'OnlineLibrary' Python web application. This document will be iteratively refined at most twice based on critic feedback.\n\nTask Details:\n- Read user_task_description from CONTEXT to fully understand application requirements\n- Read current design_spec.md and design_feedback.md from CONTEXT for revision guidance\n- On initial iteration, produce a complete design_spec.md covering all 10 pages, page elements with IDs, and data file schemas\n- On NEED_MODIFY feedback, apply requested changes fully and rewrite the entire design_spec.md\n- On [APPROVED], finalize design_spec.md without adding new requirements\n\n**Section 1: Web Pages and Elements**\n- Specify each page’s title, a brief overview, and a list of all UI elements with exact IDs and types\n- Ensure all 10 pages described in user_task_description are included with their specified elements and navigation\n\n**Section 2: Data Storage Design**\n- Describe local text file formats, field orders, delimiters (pipe '|'), and example data rows for users, books, borrowings, reservations, reviews, and fines\n- Include file organization under ‘data’ directory\n\n**Section 3: Navigation and Inter-page Relationships**\n- Define navigation paths and button actions linking pages as per user flow starting from Dashboard\n\nCRITICAL SUCCESS CRITERIA:\n- Strictly follow user_task_description without inventing new pages or elements\n- Complete detail for all required pages and data files in design_spec.md\n- Implement refinements fully on NEED_MODIFY feedback, run at most two iterations\n- Output file must be design_spec.md\n- Use write_text_file tool to save output\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application design specifications.\n\nYour goal is to thoroughly review the design_spec.md document to ensure it aligns precisely with the user_task_description, has consistent page elements and IDs, correct data storage schemas, and overall usability. Provide gated feedback within two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT for comprehensive verification\n- Confirm presence and accuracy of all 10 web pages and their specified UI elements\n- Verify all data files formats, field delimiters, field names, orders, and examples conform to user requirements\n- Check navigation flows for logical completeness and consistency\n- Provide [APPROVED] if all criteria met or NEED_MODIFY followed by explicit actionable corrections\n- Limit feedback to design_spec.md content only without adding unrelated requirements\n\nReview Criteria:\n1. Completeness of page titles, overview, element IDs, and element types as described in user_task_description\n2. Consistency of element IDs across pages and navigation correctness\n3. Accuracy and clarity of data file schemas and examples, with pipe-delimited format\n4. Adherence to local text file storage under 'data' directory as required\n5. No additional unrequested features or content\n\nCRITICAL REQUIREMENTS:\n- Feedback in design_feedback.md must begin exactly with either [APPROVED] or NEED_MODIFY\n- No additional prefixes or formatting outside the feedback marker\n- Use write_text_file tool to write the full feedback document\n- Stop iteration immediately upon [APPROVED]\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify completeness of page definitions, element IDs, data formats, and adherence to all user requirements without adding new features.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Produce and iteratively refine the complete Python Flask application including app.py and all HTML templates with exact element IDs, local text file data integration, and verification via gated code_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator develops or revises app.py and templates/*.html based on design_spec.md and previous code_feedback.md; CodeCritic reviews the codebase for correctness, style, functional completeness, and compliance with design_spec.md, producing code_feedback.md beginning with [APPROVED] or NEED_MODIFY. The process runs for up to two iterations or until approval.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building complete backend applications and corresponding HTML frontend templates.\n\nYour goal is to implement or fully revise the Python Flask backend (app.py) and all HTML templates (templates/*.html) for a comprehensive web application, iteratively refining from critic feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, previous app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On the first iteration, create complete app.py and templates/*.html covering all 10 specified pages, navigation, exact element IDs, and local text file data management\n- If feedback begins NEED_MODIFY, apply all supported corrections and rewrite the complete backend and templates\n- If feedback begins [APPROVED], preserve the approved code artifacts\n\n**Section 1: Backend Implementation**\n- Implement Flask routes corresponding to all app pages with route names, URL paths, and HTTP methods as inferred from design_spec.md\n- Implement data loading, manipulation, and saving using local text files in the prescribed data directory and formats\n- Manage user sessions for username or login state as needed to personalize pages and track interactions\n- Implement business logic for searching, borrowing, returning, reserving books, review writing, profile management, fines payment, and navigation\n\n**Section 2: Frontend Templates**\n- Create or revise HTML templates with exact specified page titles and element IDs according to design_spec.md\n- Include all page-specific elements (buttons, inputs, divs, tables) with their roles and IDs precisely as required\n- Ensure navigation buttons link correctly between pages\n- Design consistent layout and integration with Flask backend context variables for dynamic content rendering\n\n**Section 3: Code Quality and Integration**\n- Follow Python and Flask best practices for readability, maintainability, and error handling\n- Integrate all features and pages into a coherent single Flask app with blueprints if necessary\n- Ensure file paths and data parsing strictly follow the indicated formats and delimiters\n- Prepare app.py and templates/*.html artifacts ready for validation\n\nCRITICAL SUCCESS CRITERIA:\n- Run at most two Generator/Critic iterations\n- Apply every supported NEED_MODIFY feedback item fully by rewriting complete artifacts\n- Preserve exact element IDs, page titles, and navigation details as specified\n- Use write_text_file tool to output app.py and templates/*.html files\n- Output artifacts: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in reviewing Python Flask backend code and HTML frontend templates for correctness, compliance, and quality.\n\nYour goal is to review app.py and all templates/*.html against design_spec.md and provide gated approval or modification feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify Python Flask backend for syntax, runtime correctness, and business logic adherence to design_spec.md features and specifications\n- Verify exact presence and correctness of all required element IDs, page titles, buttons, inputs, and divisions in HTML templates\n- Confirm proper implementation of local text file reading/writing with correct formats and data flow\n- Generate code_feedback.md starting exactly with [APPROVED] if fully compliant, else start with NEED_MODIFY followed by concrete required corrections\n\nReview Requirements:\n1. Validate that each Flask route corresponds to a required page with proper URL, method, and logic\n2. Confirm all specified element IDs exist on the appropriate templates as per design_spec.md\n3. Validate navigation buttons and links between pages functionally match specifications\n4. Verify local text file data handling is complete, consistent, and error-free\n5. Check code style, error handling, and Python best practices adherence as feasible\n6. Do not add requirements beyond design_spec.md nor omit any required functionality\n\nCRITICAL REQUIREMENTS:\n- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- Do not add any prefix or whitespace before the status marker\n- Use write_text_file tool to save the full feedback\n- Provide a detailed list of deficiencies if NEED_MODIFY is used\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"code_feedback.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Ensure all pages, elements, data storage, and functionality strictly comply with design_spec.md and coding best practices without omissions or unauthorized extensions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to produce a detailed, adaptive design specification document that describes all web pages, element IDs, data formats, and local storage structure for the 'OnlineLibrary' Python web application. This document will be iteratively refined at most twice based on critic feedback.

Task Details:
- Read user_task_description from CONTEXT to fully understand application requirements
- Read current design_spec.md and design_feedback.md from CONTEXT for revision guidance
- On initial iteration, produce a complete design_spec.md covering all 10 pages, page elements with IDs, and data file schemas
- On NEED_MODIFY feedback, apply requested changes fully and rewrite the entire design_spec.md
- On [APPROVED], finalize design_spec.md without adding new requirements

**Section 1: Web Pages and Elements**
- Specify each page’s title, a brief overview, and a list of all UI elements with exact IDs and types
- Ensure all 10 pages described in user_task_description are included with their specified elements and navigation

**Section 2: Data Storage Design**
- Describe local text file formats, field orders, delimiters (pipe '|'), and example data rows for users, books, borrowings, reservations, reviews, and fines
- Include file organization under ‘data’ directory

**Section 3: Navigation and Inter-page Relationships**
- Define navigation paths and button actions linking pages as per user flow starting from Dashboard

CRITICAL SUCCESS CRITERIA:
- Strictly follow user_task_description without inventing new pages or elements
- Complete detail for all required pages and data files in design_spec.md
- Implement refinements fully on NEED_MODIFY feedback, run at most two iterations
- Output file must be design_spec.md
- Use write_text_file tool to save output

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application design specifications.

Your goal is to thoroughly review the design_spec.md document to ensure it aligns precisely with the user_task_description, has consistent page elements and IDs, correct data storage schemas, and overall usability. Provide gated feedback within two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT for comprehensive verification
- Confirm presence and accuracy of all 10 web pages and their specified UI elements
- Verify all data files formats, field delimiters, field names, orders, and examples conform to user requirements
- Check navigation flows for logical completeness and consistency
- Provide [APPROVED] if all criteria met or NEED_MODIFY followed by explicit actionable corrections
- Limit feedback to design_spec.md content only without adding unrelated requirements

Review Criteria:
1. Completeness of page titles, overview, element IDs, and element types as described in user_task_description
2. Consistency of element IDs across pages and navigation correctness
3. Accuracy and clarity of data file schemas and examples, with pipe-delimited format
4. Adherence to local text file storage under 'data' directory as required
5. No additional unrequested features or content

CRITICAL REQUIREMENTS:
- Feedback in design_feedback.md must begin exactly with either [APPROVED] or NEED_MODIFY
- No additional prefixes or formatting outside the feedback marker
- Use write_text_file tool to write the full feedback document
- Stop iteration immediately upon [APPROVED]

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in building complete backend applications and corresponding HTML frontend templates.

Your goal is to implement or fully revise the Python Flask backend (app.py) and all HTML templates (templates/*.html) for a comprehensive web application, iteratively refining from critic feedback for at most two iterations.

Task Details:
- Read design_spec.md, previous app.py, templates/*.html, and code_feedback.md from CONTEXT
- On the first iteration, create complete app.py and templates/*.html covering all 10 specified pages, navigation, exact element IDs, and local text file data management
- If feedback begins NEED_MODIFY, apply all supported corrections and rewrite the complete backend and templates
- If feedback begins [APPROVED], preserve the approved code artifacts

**Section 1: Backend Implementation**
- Implement Flask routes corresponding to all app pages with route names, URL paths, and HTTP methods as inferred from design_spec.md
- Implement data loading, manipulation, and saving using local text files in the prescribed data directory and formats
- Manage user sessions for username or login state as needed to personalize pages and track interactions
- Implement business logic for searching, borrowing, returning, reserving books, review writing, profile management, fines payment, and navigation

**Section 2: Frontend Templates**
- Create or revise HTML templates with exact specified page titles and element IDs according to design_spec.md
- Include all page-specific elements (buttons, inputs, divs, tables) with their roles and IDs precisely as required
- Ensure navigation buttons link correctly between pages
- Design consistent layout and integration with Flask backend context variables for dynamic content rendering

**Section 3: Code Quality and Integration**
- Follow Python and Flask best practices for readability, maintainability, and error handling
- Integrate all features and pages into a coherent single Flask app with blueprints if necessary
- Ensure file paths and data parsing strictly follow the indicated formats and delimiters
- Prepare app.py and templates/*.html artifacts ready for validation

CRITICAL SUCCESS CRITERIA:
- Run at most two Generator/Critic iterations
- Apply every supported NEED_MODIFY feedback item fully by rewriting complete artifacts
- Preserve exact element IDs, page titles, and navigation details as specified
- Use write_text_file tool to output app.py and templates/*.html files
- Output artifacts: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in reviewing Python Flask backend code and HTML frontend templates for correctness, compliance, and quality.

Your goal is to review app.py and all templates/*.html against design_spec.md and provide gated approval or modification feedback for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify Python Flask backend for syntax, runtime correctness, and business logic adherence to design_spec.md features and specifications
- Verify exact presence and correctness of all required element IDs, page titles, buttons, inputs, and divisions in HTML templates
- Confirm proper implementation of local text file reading/writing with correct formats and data flow
- Generate code_feedback.md starting exactly with [APPROVED] if fully compliant, else start with NEED_MODIFY followed by concrete required corrections

Review Requirements:
1. Validate that each Flask route corresponds to a required page with proper URL, method, and logic
2. Confirm all specified element IDs exist on the appropriate templates as per design_spec.md
3. Validate navigation buttons and links between pages functionally match specifications
4. Verify local text file data handling is complete, consistent, and error-free
5. Check code style, error handling, and Python best practices adherence as feasible
6. Do not add requirements beyond design_spec.md nor omit any required functionality

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Do not add any prefix or whitespace before the status marker
- Use write_text_file tool to save the full feedback
- Provide a detailed list of deficiencies if NEED_MODIFY is used

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
        ("DesignCritic", """Verify completeness of page definitions, element IDs, data formats, and adherence to all user requirements without adding new features.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Ensure all pages, elements, data storage, and functionality strictly comply with design_spec.md and coding best practices without omissions or unauthorized extensions.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
            "Create or revise the complete design_spec.md based on user_task_description and prior feedback.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== Current design_feedback.md ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md for compliance with user_task_description.\n"
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
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

async def implementation_and_verification_phase():
    import glob

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
        design_spec_content = ""
        app_content = ""
        templates_content = ""
        feedback_content = ""

        try:
            design_spec_content = open("design_spec.md").read()
        except FileNotFoundError:
            pass

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
            "Create or revise the complete app.py and templates/*.html.\n\n"
            f"=== design_spec.md ===\n{design_spec_content}\n\n"
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
            "Review the latest app.py and templates against design_spec.md. "
            "Write code_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== design_spec.md ===\n{design_spec_content}\n\n"
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
