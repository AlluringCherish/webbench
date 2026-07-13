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
# 20260713_204917_005444/main_20260713_204917_005444.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the BookstoreOnline requirements and produce a detailed design_spec.md covering pages, routes, elements, data files, and navigation.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md tracing all user-visible pages, elements with IDs, navigation, and data requirements; \"\n        \"WebArchitect reads requirements_analysis.md and user input to produce design_spec.md covering Flask routes, page titles, element IDs, data file usage, \"\n        \"and navigation paths.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in detailed web application requirements extraction.\n\nYour goal is to analyze user task descriptions and create a comprehensive requirements_analysis.md file that precisely captures all user-visible pages, element IDs, page titles, navigation buttons, and data requirements.\n\nTask Details:\n- Read the full user_task_description input artifact\n- Extract every requested page with exact page titles\n- Extract all exact element IDs on each page\n- Identify all navigation buttons and their target pages\n- Document all user actions that affect navigation or data flow\n- Capture data storage requirements including referenced local text files and their usage\n\nRequirements Analysis:\n1. **Pages and Page Titles**:\n   - Enumerate all nine pages with their exact titles\n2. **Element IDs**:\n   - List all element IDs on each page exactly as specified\n   - Include dynamic element IDs with patterns (e.g., view-book-button-{book_id})\n3. **Navigation Mapping**:\n   - Identify buttons and navigation relationships between pages\n4. **Data Artifacts**:\n   - List all data files and their formats referenced by the user task\n   \nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save requirements_analysis.md\n- Ensure no omissions of pages, IDs, or navigation buttons\n- Use exact strings and casing from user task description\n- Output only requirements_analysis.md in expected format\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and specifications.\n\nYour goal is to transform the detailed requirements_analysis.md and user task description into a precise design_spec.md that defines all Flask routes, HTTP methods, page titles, exact element IDs, navigation flows, and data storage contracts for local text files.\n\nTask Details:\n- Read both user_task_description and requirements_analysis.md thoroughly\n- Define Flask routes with route paths, HTTP methods (GET/POST), function names consistent and clear\n- Specify exact page titles for all pages\n- Enumerate all element IDs exactly as analyzed, including dynamic ID patterns\n- Specify navigation flows mapping buttons to route functions\n- Document data storage files usage, formats, fields, and access within the app\n\nDesign Specification Requirements:\n1. **Routes**:\n   - Define route for each page with URL pattern and HTTP method(s)\n   - Use clear function names matching page purposes (lowercase with underscores)\n   - Detail context variables passed to templates for each route\n\n2. **Page Titles and Elements**:\n   - List exact page titles as per requirements\n   - Include all element IDs precisely, with dynamic element ID patterns specified\n\n3. **Navigation Mapping**:\n   - Map all navigation buttons to Flask route functions using url_for format\n   - Include both static and dynamic button mappings\n\n4. **Data Storage Contracts**:\n   - Specify data files in data/ directory with exact filename and pipe-delimited format\n   - Enumerate fields in each data file and their order\n   - Describe file purpose and usage in the app\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_spec.md\n- Maintain exact naming, spelling, and casing from inputs and requirements_analysis.md\n- Ensure coverage of ALL pages, routes, elements, navigation, and data files\n- Provide actionable specifications enabling Backend and Frontend implementation without ambiguity\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md captures all pages, exact requested element IDs, page titles, navigation buttons, and data storage details before architecture.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"WebArchitect\",\n            \"reviewer_agent\": \"ImplementationEngineer\",\n            \"review_criteria\": (\n                \"Verify design_spec.md fully covers all Flask routes, page titles, element IDs, data files, and navigation flows required to implement the app.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the BookstoreOnline Flask application as app_draft.py and templates_draft/*.html according to design_spec.md, supporting local text file data management and all specified pages with navigation.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineer writes app_draft.py and templates_draft/*.html implementing all Flask routes, page titles, element IDs, navigation, and reading/writing required local text files. \"\n        \"IntegrationEngineer then converts the drafts into final app.py and templates/*.html ready for deployment.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineer\",\n            \"prompt\": \"\"\"You are a Full-Stack Developer specializing in Python Flask web applications.\n\nYour goal is to develop a complete draft implementation of the BookstoreOnline application including all frontend and backend components. The deliverables are app_draft.py and all HTML templates in templates_draft/ directory.\n\nTask Details:\n- Read user_task_description and design_spec.md for reference\n- Implement app_draft.py with all Flask routes, backend logic, and data file management as specified\n- Implement all HTML templates under templates_draft/ with exact element IDs and page titles\n- Focus on reading/writing local text files as defined, matching data schemas exactly\n- Do NOT produce final production code; draft implementation only\n\nImplementation Guidelines:\n1. **Flask Application Development**\n   - Implement all routes as described in design_spec.md including Dashboard, Catalog, Book Details, Cart, Checkout, Order History, Reviews, Write Review, Bestsellers\n   - Use exact route names, function names, and HTTP methods specified\n   - Manage data using local text files (e.g., books.txt, cart.txt, orders.txt) with exact parsing and writing logic per schema\n   - Implement backend logic for adding/removing items from cart, placing orders, writing reviews\n   - Ensure navigation between pages is implemented via buttons and links reflecting design_spec.md navigation flows\n\n2. **Template Implementation**\n   - Create template files in templates_draft/ with filenames matching design_spec.md\n   - Use exact element IDs as specified including dynamic IDs with correct Jinja2 syntax (e.g., view-book-button-{{ book.book_id }})\n   - Ensure page titles match exactly in <title> and <h1> tags\n   - Implement loops and conditionals for lists of items (books, orders, reviews) per specification\n   - Include forms and buttons for interactions like updating quantities, submitting reviews as described\n\n3. **Data Handling**\n   - Read and write data files with pipe-delimited fields exactly in the order given by user_task_description\n   - Handle file read/write errors gracefully\n   - Maintain data integrity and consistency across all pages that interact with data\n\n4. **Project Constraints**\n   - Do not implement authentication or features beyond scope\n   - Focus on correctness, completeness, and accuracy of element IDs, routes, data flow, and navigation\n   - All implementation must be draft quality for integration engineer to refine\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and templates_draft/*.html files\n- Strictly follow data schema and element ID naming conventions from user_task_description and design_spec.md\n- Ensure all pages and functionalities specified are covered in the draft implementation\n- Do NOT finalize code; produce draft versions ready for integration\n- Do NOT embed code snippets in messages except for guidance; always write output files\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web applications and template integration.\n\nYour goal is to transform draft implementations into final production-ready code by verifying and refining app_draft.py and templates_draft/*.html into app.py and templates/*.html.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html\n- Convert app_draft.py into a production-ready app.py with verified routes, data handling, and navigation\n- Refine templates_draft/*.html into templates/*.html ensuring exact element IDs, page titles, and navigation flows\n- Verify data file integration matches schemas and functionality is consistent with design_spec.md\n- Ensure the final code is deployable and aligns perfectly with all project specifications\n\nIntegration and Verification Guidelines:\n1. **Code Review and Refinement**\n   - Review app_draft.py for completeness and correctness in route implementations and backend logic\n   - Fix inconsistencies, correct route definitions, and improve data file management where needed\n   - Ensure all user interactions and page navigations are correctly wired and tested\n\n2. **Template Verification**\n   - Check all templates for exact presence of element IDs and page titles as per design_spec.md\n   - Convert dynamic IDs and Jinja2 expressions correctly for production\n   - Clean any draft artifacts or development placeholders from templates\n\n3. **Data Management**\n   - Verify read/write operations on local text files use exact schemas and maintain data integrity\n   - Ensure no data loss or format issues in final code\n\n4. **Final Packaging**\n   - Save final backend as app.py\n   - Save all final templates in templates/ directory\n   - Maintain clear separation from draft files\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to write final app.py and templates/*.html\n- Strictly adhere to naming conventions and data schema order from user_task_description and design_spec.md\n- Deliver polished, production-ready code ready for deployment\n- Do not add new features beyond the provided specification\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"ImplementationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Check app_draft.py and templates_draft/*.html against design_spec.md for completeness, correctness, and exact compliance before integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"IntegrationEngineer\",\n            \"reviewer_agent\": \"VerificationEngineer\",\n            \"review_criteria\": (\n                \"Ensure final app.py and templates/*.html strictly follow design_spec.md with accurate routes, page titles, element IDs, navigation, and local text file data management.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and test the final app.py and templates/*.html for syntax, runtime, and UI element correctness, producing a validation_report.md and applying necessary fixes to finalize the application.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"VerificationEngineer validates app.py and templates/*.html including syntax, execution, UI element presence, correct navigation, and data file management, producing validation_report.md; \"\n        \"BugFixEngineer applies reported fixes to produce the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"VerificationEngineer\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python web application verification.\n\nYour goal is to validate and test the final backend and frontend components to ensure correctness in syntax, runtime behavior, UI elements, navigation, and data interactions, producing a comprehensive validation_report.md.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate all Python code files for syntax and runtime errors\n- Verify presence and correctness of all UI element IDs on templates against design_spec.md\n- Test navigation flows between pages using route and template mappings from design_spec.md\n- Check that local text file data loading and saving in app.py conform to design_spec.md data schemas\n- Output a detailed validation_report.md enumerating any errors, warnings, and suggestions for fixes\n\nValidation Procedures:\n1. Syntax and Runtime Checks:\n   - Use validate_python_file tool on app.py\n   - Execute critical backend routes to confirm runtime without errors using execute_python_code\n\n2. UI Element Verification:\n   - Parse templates/*.html to confirm existence of all required element IDs per design_spec.md\n   - Check dynamic element ID patterns using sample data where applicable\n\n3. Navigation Testing:\n   - Confirm all navigation buttons and links route correctly to their target pages as specified in design_spec.md\n\n4. Data File Access:\n   - Verify app.py accesses and parses all required data files with correct field order and formats per design_spec.md\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools for code checks\n- MUST produce clear, actionable validation_report.md covering syntax, runtime, UI, navigation, and data file issues\n- Report must include severity levels and recommended fixes\n- Do NOT modify any source files in this step\n- Save the report with write_text_file tool\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"BugFixEngineer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in bug fixing and code refinement for Python web applications.\n\nYour goal is to address all issues documented in validation_report.md by modifying the backend and frontend code to produce final, corrected app.py and templates/*.html files.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, and validation_report.md from CONTEXT\n- Analyze the validation_report.md for clear, actionable issues and recommended fixes\n- Apply necessary code and template corrections to fix:\n  - Syntax and runtime errors in app.py\n  - Missing or incorrect UI element IDs in templates\n  - Navigation and routing inconsistencies\n  - Data file parsing and I/O errors\n- Ensure all fixes conform strictly to design_spec.md specifications and user requirements\n\nBug Fixing Guidelines:\n1. Code Corrections:\n   - Fix Python syntax and runtime errors as per validation report\n   - Maintain existing functionality and coding standards\n\n2. UI Template Updates:\n   - Add or correct element IDs to match design_spec.md exactly\n   - Fix navigation link routes and button actions accordingly\n\n3. Data Handling:\n   - Ensure all data file access matches field order and format specified\n   - Avoid introducing new features or deviations from original design\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save final app.py and templates/*.html files\n- All corrections must fully resolve validation issues without regressions\n- Maintain consistency with user_task_description and design_spec.md\n- Provide clean, well-structured updated files ready for deployment\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"VerificationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"VerificationEngineer\",\n            \"reviewer_agent\": \"BugFixEngineer\",\n            \"review_criteria\": (\n                \"Check that validation_report.md contains clear, actionable, and design-aligned issues and recommendations.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"BugFixEngineer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Confirm that the final updated app.py and templates/*.html fully address validation issues and conform to original requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'BookstoreOnline' Web Application

## 1. Objective
Develop a comprehensive web application named 'BookstoreOnline' using Python, with data managed through local text files. The application enables users to browse books, add items to cart, checkout, write reviews, and track order history. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'BookstoreOnline' application is Python.

## 3. Page Design

The 'BookstoreOnline' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Bookstore Dashboard
- **Overview**: The main hub displaying featured books, bestsellers, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-books** - Type: Div - Display of featured book recommendations.
  - **ID: browse-catalog-button** - Type: Button - Button to navigate to book catalog page.
  - **ID: view-cart-button** - Type: Button - Button to navigate to shopping cart page.
  - **ID: bestsellers-button** - Type: Button - Button to navigate to bestsellers page.

### 2. Book Catalog Page
- **Page Title**: Book Catalog
- **Overview**: A page displaying all available books with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search books by title, author, or ISBN.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Fiction, Non-Fiction, Science, History, etc.).
  - **ID: books-grid** - Type: Div - Grid displaying book cards with cover, title, author, and price.
  - **ID: view-book-button-{book_id}** - Type: Button - Button to view book details (each book card has this).

### 3. Book Details Page
- **Page Title**: Book Details
- **Overview**: A page displaying detailed information about a specific book.
- **Elements**:
  - **ID: book-details-page** - Type: Div - Container for the book details page.
  - **ID: book-title** - Type: H1 - Display book title.
  - **ID: book-author** - Type: Div - Display book author.
  - **ID: book-price** - Type: Div - Display book price.
  - **ID: add-to-cart-button** - Type: Button - Button to add book to shopping cart.
  - **ID: book-reviews** - Type: Div - Section displaying customer reviews.

### 4. Shopping Cart Page
- **Page Title**: Shopping Cart
- **Overview**: A page displaying items in the cart with quantity management and checkout option.
- **Elements**:
  - **ID: cart-page** - Type: Div - Container for the cart page.
  - **ID: cart-items-table** - Type: Table - Table displaying cart items with title, quantity, price, and subtotal.
  - **ID: update-quantity-{item_id}** - Type: Input (number) - Field to update item quantity (each cart item has this).
  - **ID: remove-item-button-{item_id}** - Type: Button - Button to remove item from cart (each cart item has this).
  - **ID: proceed-checkout-button** - Type: Button - Button to proceed to checkout.
  - **ID: total-amount** - Type: Div - Display total cart amount.

### 5. Checkout Page
- **Page Title**: Checkout
- **Overview**: A page for users to enter shipping information and complete purchase.
- **Elements**:
  - **ID: checkout-page** - Type: Div - Container for the checkout page.
  - **ID: customer-name** - Type: Input - Field to input customer name.
  - **ID: shipping-address** - Type: Textarea - Field to input shipping address.
  - **ID: payment-method** - Type: Dropdown - Dropdown to select payment method (Credit Card, PayPal, Bank Transfer).
  - **ID: place-order-button** - Type: Button - Button to confirm and place order.

### 6. Order History Page
- **Page Title**: Order History
- **Overview**: A page displaying all previous orders with tracking information.
- **Elements**:
  - **ID: orders-page** - Type: Div - Container for the orders page.
  - **ID: orders-table** - Type: Table - Table displaying orders with order ID, date, total amount, and status.
  - **ID: view-order-button-{order_id}** - Type: Button - Button to view order details (each order has this).
  - **ID: order-status-filter** - Type: Dropdown - Dropdown to filter by status (All, Pending, Shipped, Delivered).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Reviews Page
- **Page Title**: Customer Reviews
- **Overview**: A page displaying all customer reviews and allowing users to write new reviews.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of all reviews with book title, rating, and review text.
  - **ID: write-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: filter-by-rating** - Type: Dropdown - Dropdown to filter reviews by rating (All, 5 stars, 4 stars, etc.).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write a Review
- **Overview**: A page for users to write reviews for purchased books.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: select-book** - Type: Dropdown - Dropdown to select book to review.
  - **ID: rating-select** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.

### 9. Bestsellers Page
- **Page Title**: Bestsellers
- **Overview**: A page displaying top-selling books ranked by sales.
- **Elements**:
  - **ID: bestsellers-page** - Type: Div - Container for the bestsellers page.
  - **ID: bestsellers-list** - Type: Div - Ranked list of bestselling books with rank, title, author, and sales count.
  - **ID: time-period-filter** - Type: Dropdown - Dropdown to filter by time period (This Week, This Month, All Time).
  - **ID: view-book-button-{book_id}** - Type: Button - Button to view book details (each bestseller has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'BookstoreOnline' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Books Data
- **File Name**: `books.txt`
- **Data Format**:
  ```
  book_id|title|author|isbn|category|price|stock|description
  ```
- **Example Data**:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File Name**: `cart.txt`
- **Data Format**:
  ```
  cart_id|book_id|quantity|added_date
  ```
- **Example Data**:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File Name**: `orders.txt`
- **Data Format**:
  ```
  order_id|customer_name|order_date|total_amount|status|shipping_address
  ```
- **Example Data**:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File Name**: `order_items.txt`
- **Data Format**:
  ```
  order_item_id|order_id|book_id|quantity|price
  ```
- **Example Data**:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|book_id|customer_name|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File Name**: `bestsellers.txt`
- **Data Format**:
  ```
  book_id|sales_count|period
  ```
- **Example Data**:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in detailed web application requirements extraction.

Your goal is to analyze user task descriptions and create a comprehensive requirements_analysis.md file that precisely captures all user-visible pages, element IDs, page titles, navigation buttons, and data requirements.

Task Details:
- Read the full user_task_description input artifact
- Extract every requested page with exact page titles
- Extract all exact element IDs on each page
- Identify all navigation buttons and their target pages
- Document all user actions that affect navigation or data flow
- Capture data storage requirements including referenced local text files and their usage

Requirements Analysis:
1. **Pages and Page Titles**:
   - Enumerate all nine pages with their exact titles
2. **Element IDs**:
   - List all element IDs on each page exactly as specified
   - Include dynamic element IDs with patterns (e.g., view-book-button-{book_id})
3. **Navigation Mapping**:
   - Identify buttons and navigation relationships between pages
4. **Data Artifacts**:
   - List all data files and their formats referenced by the user task
   
CRITICAL REQUIREMENTS:
- Use write_text_file tool to save requirements_analysis.md
- Ensure no omissions of pages, IDs, or navigation buttons
- Use exact strings and casing from user task description
- Output only requirements_analysis.md in expected format

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design and specifications.

Your goal is to transform the detailed requirements_analysis.md and user task description into a precise design_spec.md that defines all Flask routes, HTTP methods, page titles, exact element IDs, navigation flows, and data storage contracts for local text files.

Task Details:
- Read both user_task_description and requirements_analysis.md thoroughly
- Define Flask routes with route paths, HTTP methods (GET/POST), function names consistent and clear
- Specify exact page titles for all pages
- Enumerate all element IDs exactly as analyzed, including dynamic ID patterns
- Specify navigation flows mapping buttons to route functions
- Document data storage files usage, formats, fields, and access within the app

Design Specification Requirements:
1. **Routes**:
   - Define route for each page with URL pattern and HTTP method(s)
   - Use clear function names matching page purposes (lowercase with underscores)
   - Detail context variables passed to templates for each route

2. **Page Titles and Elements**:
   - List exact page titles as per requirements
   - Include all element IDs precisely, with dynamic element ID patterns specified

3. **Navigation Mapping**:
   - Map all navigation buttons to Flask route functions using url_for format
   - Include both static and dynamic button mappings

4. **Data Storage Contracts**:
   - Specify data files in data/ directory with exact filename and pipe-delimited format
   - Enumerate fields in each data file and their order
   - Describe file purpose and usage in the app

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_spec.md
- Maintain exact naming, spelling, and casing from inputs and requirements_analysis.md
- Ensure coverage of ALL pages, routes, elements, navigation, and data files
- Provide actionable specifications enabling Backend and Frontend implementation without ambiguity

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineer": {
        "prompt": (
            """You are a Full-Stack Developer specializing in Python Flask web applications.

Your goal is to develop a complete draft implementation of the BookstoreOnline application including all frontend and backend components. The deliverables are app_draft.py and all HTML templates in templates_draft/ directory.

Task Details:
- Read user_task_description and design_spec.md for reference
- Implement app_draft.py with all Flask routes, backend logic, and data file management as specified
- Implement all HTML templates under templates_draft/ with exact element IDs and page titles
- Focus on reading/writing local text files as defined, matching data schemas exactly
- Do NOT produce final production code; draft implementation only

Implementation Guidelines:
1. **Flask Application Development**
   - Implement all routes as described in design_spec.md including Dashboard, Catalog, Book Details, Cart, Checkout, Order History, Reviews, Write Review, Bestsellers
   - Use exact route names, function names, and HTTP methods specified
   - Manage data using local text files (e.g., books.txt, cart.txt, orders.txt) with exact parsing and writing logic per schema
   - Implement backend logic for adding/removing items from cart, placing orders, writing reviews
   - Ensure navigation between pages is implemented via buttons and links reflecting design_spec.md navigation flows

2. **Template Implementation**
   - Create template files in templates_draft/ with filenames matching design_spec.md
   - Use exact element IDs as specified including dynamic IDs with correct Jinja2 syntax (e.g., view-book-button-{{ book.book_id }})
   - Ensure page titles match exactly in <title> and <h1> tags
   - Implement loops and conditionals for lists of items (books, orders, reviews) per specification
   - Include forms and buttons for interactions like updating quantities, submitting reviews as described

3. **Data Handling**
   - Read and write data files with pipe-delimited fields exactly in the order given by user_task_description
   - Handle file read/write errors gracefully
   - Maintain data integrity and consistency across all pages that interact with data

4. **Project Constraints**
   - Do not implement authentication or features beyond scope
   - Focus on correctness, completeness, and accuracy of element IDs, routes, data flow, and navigation
   - All implementation must be draft quality for integration engineer to refine

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and templates_draft/*.html files
- Strictly follow data schema and element ID naming conventions from user_task_description and design_spec.md
- Ensure all pages and functionalities specified are covered in the draft implementation
- Do NOT finalize code; produce draft versions ready for integration
- Do NOT embed code snippets in messages except for guidance; always write output files

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web applications and template integration.

Your goal is to transform draft implementations into final production-ready code by verifying and refining app_draft.py and templates_draft/*.html into app.py and templates/*.html.

Task Details:
- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html
- Convert app_draft.py into a production-ready app.py with verified routes, data handling, and navigation
- Refine templates_draft/*.html into templates/*.html ensuring exact element IDs, page titles, and navigation flows
- Verify data file integration matches schemas and functionality is consistent with design_spec.md
- Ensure the final code is deployable and aligns perfectly with all project specifications

Integration and Verification Guidelines:
1. **Code Review and Refinement**
   - Review app_draft.py for completeness and correctness in route implementations and backend logic
   - Fix inconsistencies, correct route definitions, and improve data file management where needed
   - Ensure all user interactions and page navigations are correctly wired and tested

2. **Template Verification**
   - Check all templates for exact presence of element IDs and page titles as per design_spec.md
   - Convert dynamic IDs and Jinja2 expressions correctly for production
   - Clean any draft artifacts or development placeholders from templates

3. **Data Management**
   - Verify read/write operations on local text files use exact schemas and maintain data integrity
   - Ensure no data loss or format issues in final code

4. **Final Packaging**
   - Save final backend as app.py
   - Save all final templates in templates/ directory
   - Maintain clear separation from draft files

CRITICAL REQUIREMENTS:
- Use write_text_file tool to write final app.py and templates/*.html
- Strictly adhere to naming conventions and data schema order from user_task_description and design_spec.md
- Deliver polished, production-ready code ready for deployment
- Do not add new features beyond the provided specification

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'ImplementationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "VerificationEngineer": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python web application verification.

Your goal is to validate and test the final backend and frontend components to ensure correctness in syntax, runtime behavior, UI elements, navigation, and data interactions, producing a comprehensive validation_report.md.

Task Details:
- Read user_task_description, design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate all Python code files for syntax and runtime errors
- Verify presence and correctness of all UI element IDs on templates against design_spec.md
- Test navigation flows between pages using route and template mappings from design_spec.md
- Check that local text file data loading and saving in app.py conform to design_spec.md data schemas
- Output a detailed validation_report.md enumerating any errors, warnings, and suggestions for fixes

Validation Procedures:
1. Syntax and Runtime Checks:
   - Use validate_python_file tool on app.py
   - Execute critical backend routes to confirm runtime without errors using execute_python_code

2. UI Element Verification:
   - Parse templates/*.html to confirm existence of all required element IDs per design_spec.md
   - Check dynamic element ID patterns using sample data where applicable

3. Navigation Testing:
   - Confirm all navigation buttons and links route correctly to their target pages as specified in design_spec.md

4. Data File Access:
   - Verify app.py accesses and parses all required data files with correct field order and formats per design_spec.md

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for code checks
- MUST produce clear, actionable validation_report.md covering syntax, runtime, UI, navigation, and data file issues
- Report must include severity levels and recommended fixes
- Do NOT modify any source files in this step
- Save the report with write_text_file tool

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "BugFixEngineer": {
        "prompt": (
            """You are a Software Developer specializing in bug fixing and code refinement for Python web applications.

Your goal is to address all issues documented in validation_report.md by modifying the backend and frontend code to produce final, corrected app.py and templates/*.html files.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, and validation_report.md from CONTEXT
- Analyze the validation_report.md for clear, actionable issues and recommended fixes
- Apply necessary code and template corrections to fix:
  - Syntax and runtime errors in app.py
  - Missing or incorrect UI element IDs in templates
  - Navigation and routing inconsistencies
  - Data file parsing and I/O errors
- Ensure all fixes conform strictly to design_spec.md specifications and user requirements

Bug Fixing Guidelines:
1. Code Corrections:
   - Fix Python syntax and runtime errors as per validation report
   - Maintain existing functionality and coding standards

2. UI Template Updates:
   - Add or correct element IDs to match design_spec.md exactly
   - Fix navigation link routes and button actions accordingly

3. Data Handling:
   - Ensure all data file access matches field order and format specified
   - Avoid introducing new features or deviations from original design

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save final app.py and templates/*.html files
- All corrections must fully resolve validation issues without regressions
- Maintain consistency with user_task_description and design_spec.md
- Provide clean, well-structured updated files ready for deployment

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'VerificationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md captures all pages, exact requested element IDs, page titles, navigation buttons, and data storage details before architecture.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'WebArchitect': [
        ("ImplementationEngineer", """Verify design_spec.md fully covers all Flask routes, page titles, element IDs, data files, and navigation flows required to implement the app.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineer': [
        ("IntegrationEngineer", """Check app_draft.py and templates_draft/*.html against design_spec.md for completeness, correctness, and exact compliance before integration.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'IntegrationEngineer': [
        ("VerificationEngineer", """Ensure final app.py and templates/*.html strictly follow design_spec.md with accurate routes, page titles, element IDs, navigation, and local text file data management.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'VerificationEngineer': [
        ("BugFixEngineer", """Check that validation_report.md contains clear, actionable, and design-aligned issues and recommendations.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'BugFixEngineer': [
        ("RequirementsAnalyst", """Confirm that the final updated app.py and templates/*.html fully address validation issues and conform to original requirements.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Create agents
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
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution
    # Step 1: RequirementsAnalyst creates requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce comprehensive requirements_analysis.md capturing all pages, exact element IDs, page titles, navigation buttons, and data requirements.")

    # Step 2: WebArchitect creates design_spec.md based on user input and requirements_analysis.md
    req_analysis_content = ""
    try:
        req_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    user_task_desc = ""
    entries = CONTEXT.get("user_task_description", [])
    if entries:
        user_task_desc = entries[-1]["content"]

    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md. Produce design_spec.md with complete Flask routes (paths, HTTP methods, function names), page titles, exact element IDs (including dynamic patterns), navigation mappings (buttons→route functions), and data storage contracts (data files with filenames, pipe-delimited formats, fields, and usage). Ensure no ambiguity and full coverage.\n\n"
                  f"=== User Task Description ===\n{user_task_desc}\n\n"
                  f"=== Requirements Analysis ===\n{req_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Declare agents
    ImplementationEngineer = build_resilient_agent(
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )

    # Sequential execution: First ImplementationEngineer, then IntegrationEngineer
    # Execute ImplementationEngineer to produce app_draft.py and templates_draft/*.html
    await execute(ImplementationEngineer,
                  "Develop full draft implementation with app_draft.py and templates_draft/*.html "
                  "including all Flask routes, local text file data management, pages, navigation, and element IDs "
                  "per design_spec.md and user_task_description.")

    # Read draft files for integration
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # For templates_draft/*.html, assume reading all template files content
    # Since file names are unknown, read all matching pattern files in directory would be necessary in real environment
    # Here we read as empty string placeholder as per instructions
    try:
        import glob
        template_files = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for tf in template_files:
            try:
                templates_draft_content += f"\n=== {tf} ===\n" + open(tf).read() + "\n"
            except:
                continue
    except:
        templates_draft_content = ""

    # Execute IntegrationEngineer to convert drafts into final production code app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Refine and verify draft code into final production-ready app.py and templates/*.html. "
                  f"Use user_task_description, design_spec.md, app_draft.py, and all draft templates.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n"
                  f"=== templates_draft/*.html ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    VerificationEngineer = build_resilient_agent(
        agent_name="VerificationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    BugFixEngineer = build_resilient_agent(
        agent_name="BugFixEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential Flow Execution
    # 1. VerificationEngineer runs validation and produces validation_report.md
    await execute(
        VerificationEngineer,
        "Validate syntax and runtime of app.py using validate_python_file and execute_python_code. "
        "Verify all UI element IDs and navigation in templates/*.html against design_spec.md. "
        "Check data file access and parsing in app.py as per design_spec.md. "
        "Output a comprehensive validation_report.md with errors, warnings, and fix suggestions."
    )

    # 2. BugFixEngineer applies fixes based on validation_report.md and outputs corrected files
    # Reading validation_report.md content to inject for bug fixing
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    # Reading current artifacts for bug fixing injection
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except Exception:
        pass
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    # For templates/*.html, read as a single string; if multiple files, concatenate with separators for clarity
    try:
        import glob
        templates_files = glob.glob("templates/*.html")
        templates_contents_list = []
        for tf in templates_files:
            try:
                tf_content = open(tf).read()
                templates_contents_list.append(f"=== {tf} ===\n{tf_content}\n")
            except Exception:
                continue
        templates_content = "\n".join(templates_contents_list)
    except Exception:
        templates_content = ""

    await execute(
        BugFixEngineer,
        f"Analyze validation_report.md and fix all issues in app.py and templates/*.html accordingly. "
        f"Preserve design_spec.md requirements. Output final app.py and templates/*.html files.\n\n"
        f"=== validation_report.md ===\n{validation_report_content}\n\n"
        f"=== design_spec.md ===\n{design_spec_content}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
    )
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
