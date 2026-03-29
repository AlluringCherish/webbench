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
    "phase1": "def architecture_design_phase(\n    goal: str = \"Create detailed design specification covering Flask routes, HTML templates, and data schemas for BookstoreOnline\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect drafts design_spec.md with sections: \"\n        \"1) Flask routes with function names, context variables, HTTP methods; \"\n        \"2) HTML templates with element IDs, context variables, navigation; \"\n        \"3) Data schemas with exact field order, pipe-delimited format, for use in backend.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create a detailed design specification document that enables independent Backend and Frontend developers to implement the BookstoreOnline application fully.\n\nTask Details:\n- Read user_task_description from CONTEXT in full\n- Produce design_spec.md covering all Flask routes, frontend HTML templates, and backend data schemas\n- Include all pages and features described in the user task\n- Do NOT assume or add features beyond the user task\n- Preserve exact data formats and field orders as specified\n\n**Section 1: Flask Routes Specification**\n\n- Define all routes needed for each page (Dashboard, Catalog, Book Details, Cart, Checkout, Order History, Reviews, Write Review, Bestsellers)\n- Specify for each route:\n  - Route path (e.g., /dashboard, /catalog, /book/<int:book_id>)\n  - Function name (lowercase with underscores)\n  - HTTP method(s) (GET or POST)\n  - Template file rendered\n  - Context variables with precise names and data types (list, dict, str, int, float)\n- Describe how form submissions (e.g., adding to cart, placing order, submitting review) are handled\n- Root route '/' must redirect to the dashboard page\n\n**Section 2: HTML Templates Specification**\n\n- For each page template, specify:\n  - File path in templates/ (e.g., templates/dashboard.html)\n  - Exact page title for <title> tag and main <h1> heading\n  - ALL element IDs required with element type and purpose\n    - Static element IDs like dashboard-page, view-cart-button, proceed-checkout-button\n    - Dynamic element IDs with patterns like view-book-button-{book_id}, update-quantity-{item_id}\n  - Context variables available and their structures\n  - Navigation mappings using url_for() for buttons and links\n- Follow exact naming and casing conventions as in user requirements\n- Include form structure details for POST routes (e.g., checkout and review submission forms)\n\n**Section 3: Data Schemas Specification**\n\n- For each data file in the data directory (books.txt, categories.txt, cart.txt, orders.txt, order_items.txt, reviews.txt, bestsellers.txt):\n  - Specify file path and format (pipe-delimited '|')\n  - List precise field order and field names\n  - Provide a brief description of what the file stores\n  - Include 2-3 realistic example rows matching the user task examples\n- Ensure field orders and names perfectly align with backend parsing needs\n- No headers in data files; parsing starts from first line\n\nCRITICAL SUCCESS CRITERIA:\n- Specification enables Backend and Frontend developers to implement independently without ambiguity\n- All element IDs, routes, and data schemas match user task exactly\n- No features beyond user task added or assumed\n- Use write_text_file tool to output design_spec.md\n- Output file: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md Sections 1 and 3 for backend completeness: all Flask routes with correct names, HTTP methods, context variables; \"\n                \"data schemas match required fields, correct order and format for all data files.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md Section 2 for frontend completeness: template files with all element IDs, context variables align with specs, \"\n                \"navigation uses correct url_for calls and matches page structure.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_development_phase(\n    goal: str = \"Implement backend and frontend components in parallel according to design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using design_spec.md sections 1 and 3: Flask routes, data loading/saving with correct schemas. \"\n        \"FrontendDeveloper implements templates/*.html using design_spec.md section 2: all pages with specified element IDs and navigation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend covering all application routes and data handling as specified in the design documents.\n\nTask Details:\n- Read design_spec.md Section 1 (Flask Routes) and Section 3 (Data Schemas) only\n- Implement app.py with all backend routes from Section 1\n- Load, save, and manipulate data files per the schemas defined in Section 3 using correct field order\n- Do not read or rely on frontend specifications in Section 2\n- Avoid assumptions beyond the design specification\n\nImplementation Guidelines:\n1. **Flask Setup**:\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n2. **Root and Routes**:\n   - Implement root route '/' that redirects to the dashboard page\n   - Implement each route from Section 1 with exact function names, HTTP methods, and templates\n   - Use render_template with context variables exactly as specified\n3. **Data Handling**:\n   - Parse data files from data/*.txt using pipe-delimited format with exact field order from Section 3\n   - Handle reading and writing errors gracefully\n   - Use dictionaries or appropriate data structures matching the schemas\n4. **Forms and Requests**:\n   - For POST routes, handle form data via request.form\n   - Validate input data as necessary per design spec constraints\n5. **Best Practices**:\n   - Include `if __name__ == '__main__':` block to run app on default port with debug enabled\n   - Use url_for for route redirects and URL generation\n   - Ensure robust error handling and data integrity\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to write the entire app.py file\n- Do not implement features outside of Section 1 and Section 3 specifications\n- Maintain exact naming conventions for functions, variables, and templates\n- Follow data schema strictly for all file operations\n- Do not provide code snippets in chat responses alone; write all code to file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement complete and fully functional HTML templates based on the design specification's frontend requirements.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) only\n- Implement all HTML templates (*.html) covering every page and UI element specified\n- Include all element IDs, page titles, and navigation links exactly as specified\n- Do not read or depend on backend code or Sections 1 and 3\n- Do not assume or add features beyond the design spec\n\nImplementation Instructions:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>Page Title from Section 2</title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1>Page Title from Section 2</h1>\n           <!-- Page Content Here -->\n       </div>\n   </body>\n   </html>\n   ```\n2. **File Naming and Location**:\n   - Save templates in a directory named 'templates'\n   - Use exact file names as specified (e.g., dashboard.html, catalog.html)\n3. **Element IDs**:\n   - Include all static and dynamic element IDs exactly as specified, paying attention to case sensitivity\n   - Use Jinja2 syntax for dynamic IDs, e.g., id=\"view-book-button-{{ book.book_id }}\"\n4. **Context Variables**:\n   - Use context variables exactly as named and typed in Section 2\n   - Support loops, conditionals, and data display using Jinja2 constructs\n5. **Navigation and Links**:\n   - Implement all navigation using url_for with exact function names\n   - Static buttons and links as well as dynamic links must be implemented per specification\n6. **Forms and User Interaction**:\n   - Implement forms for POST requests with proper method and action attributes\n   - Include all required input fields and buttons with specified IDs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all .html templates\n- Do not add pages, elements, or features not specified in Section 2\n- Element IDs and page titles must match exactly including case and formatting\n- Do not provide partial code snippets in chat; output must be saved files\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py implements all Flask routes accurately as per Section 1 of design_spec.md, \"\n                \"data handling matches schemas in Section 3, and root route redirects to dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify templates/*.html contain all specified element IDs, context variables, and navigation links as per Section 2 of design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def integration_testing_phase(\n    goal: str = \"Conduct integration testing of backend and frontend components to ensure feature correctness and data consistency\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"IntegrationTester executes integrated app.py and templates to verify all user functionalities: browsing, cart management, checkout, reviews, and order history. \"\n        \"Tester writes feedback on issues or approval. Developer revises implementation based on feedback until approved.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"IntegrationTester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in end-to-end integration testing of web applications using Python and HTML templates.\n\nYour goal is to comprehensively test the integrated BookstoreOnline application’s backend (app.py) and frontend (templates) to ensure all user features work correctly and data is consistent.\n\nTask Details:\n- Read app.py and all HTML templates from CONTEXT\n- Test all user workflows including browsing books, managing cart, checkout process, writing reviews, and viewing order history\n- Identify and document functional bugs, UI inconsistencies, and data integrity issues\n- Produce detailed test_feedback.txt including clear issue descriptions or approval status with the marker \"[APPROVED]\" when no issues remain\n- Do NOT modify any code or templates\n\nTesting Requirements:\n1. **Functional Testing**:\n   - Verify navigation between pages (Dashboard, Catalog, Book Details, Cart, Checkout, Orders, Reviews, Write Review, Bestsellers)\n   - Confirm correct data display using data files schema\n   - Test interaction elements such as buttons, inputs, filters, and dynamic lists\n   - Validate cart quantity updates, item removals, and checkout flow correctness\n   - Confirm review submission and display consistency\n   - Verify order history and filtering by status\n\n2. **UI Consistency**:\n   - Check presence of all required element IDs exactly as specified\n   - Ensure layout stability when data changes\n   - Validate dynamic element IDs are correctly rendered with variables\n\n3. **Data Integrity**:\n   - Cross-check displayed data matches backend data structures\n   - Confirm all price calculations and totals are accurate\n   - Validate reading and writing flows for orders and reviews\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to run functional tests on app.py where applicable\n- Use write_text_file tool to save detailed test_feedback.txt\n- Feedback file must contain \"[APPROVED]\" to signal no detected issues\n- Provide clear issue descriptions with reproduction steps if any problem arises\n- Do NOT perform fixes or code changes in this step\n\nOutput: test_feedback.txt\"\"\",\n            \"tools\": [\"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationFixer\",\n            \"prompt\": \"\"\"You are a Full-Stack Developer specializing in Python Flask applications with HTML frontend integration.\n\nYour goal is to iteratively fix bugs and inconsistencies in backend (app.py) and frontend (templates) to achieve full integration approval from the IntegrationTester.\n\nTask Details:\n- Read test_feedback.txt to understand tester-reported issues\n- Read current app.py and all HTML templates from CONTEXT\n- Modify and fix backend and/or frontend artifacts to resolve all reported problems\n- Preserve application architecture and data format consistency\n- Output updated app.py and templates/*.html reflecting fixes\n- Do NOT introduce new features beyond addressing listed issues\n- Be prepared for multiple iterations until IntegrationTester marks \"[APPROVED]\"\n\nImplementation Guidelines:\n1. **Analyze Feedback**:\n   - Identify all functional, UI, and data issues reported\n   - Prioritize fixes based on severity and user impact\n\n2. **Fix Backend**:\n   - Correct route handlers, data loading, and business logic as needed\n   - Ensure data reads/writes align exactly with specified formats\n\n3. **Fix Frontend**:\n   - Adjust templates for missing or incorrect element IDs\n   - Fix dynamic ID rendering and data presentation inconsistencies\n   - Verify all navigation elements work as expected\n\n4. **Testing and Validation**:\n   - Manually re-check critical fixes after each iteration (no testing tool runs here)\n   - Prepare for next round of integration testing\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save revised app.py and templates\n- Closely follow tester feedback to fully resolve all issues\n- Do NOT alter files unrelated to reported issues\n- Maintain coding best practices and consistent style\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\", \"source\": \"IntegrationTester\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"IntegrationTester\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Assess test_feedback.txt to ensure all major issues found during integration testing are clearly documented and explained.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"IntegrationFixer\",\n            \"reviewer_agent\": \"IntegrationTester\",\n            \"review_criteria\": (\n                \"Verify that IntegrationFixer addresses all test_feedback.txt issues effectively in next implementation iteration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"test_feedback.txt\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create a detailed design specification document that enables independent Backend and Frontend developers to implement the BookstoreOnline application fully.

Task Details:
- Read user_task_description from CONTEXT in full
- Produce design_spec.md covering all Flask routes, frontend HTML templates, and backend data schemas
- Include all pages and features described in the user task
- Do NOT assume or add features beyond the user task
- Preserve exact data formats and field orders as specified

**Section 1: Flask Routes Specification**

- Define all routes needed for each page (Dashboard, Catalog, Book Details, Cart, Checkout, Order History, Reviews, Write Review, Bestsellers)
- Specify for each route:
  - Route path (e.g., /dashboard, /catalog, /book/<int:book_id>)
  - Function name (lowercase with underscores)
  - HTTP method(s) (GET or POST)
  - Template file rendered
  - Context variables with precise names and data types (list, dict, str, int, float)
- Describe how form submissions (e.g., adding to cart, placing order, submitting review) are handled
- Root route '/' must redirect to the dashboard page

**Section 2: HTML Templates Specification**

- For each page template, specify:
  - File path in templates/ (e.g., templates/dashboard.html)
  - Exact page title for <title> tag and main <h1> heading
  - ALL element IDs required with element type and purpose
    - Static element IDs like dashboard-page, view-cart-button, proceed-checkout-button
    - Dynamic element IDs with patterns like view-book-button-{book_id}, update-quantity-{item_id}
  - Context variables available and their structures
  - Navigation mappings using url_for() for buttons and links
- Follow exact naming and casing conventions as in user requirements
- Include form structure details for POST routes (e.g., checkout and review submission forms)

**Section 3: Data Schemas Specification**

- For each data file in the data directory (books.txt, categories.txt, cart.txt, orders.txt, order_items.txt, reviews.txt, bestsellers.txt):
  - Specify file path and format (pipe-delimited '|')
  - List precise field order and field names
  - Provide a brief description of what the file stores
  - Include 2-3 realistic example rows matching the user task examples
- Ensure field orders and names perfectly align with backend parsing needs
- No headers in data files; parsing starts from first line

CRITICAL SUCCESS CRITERIA:
- Specification enables Backend and Frontend developers to implement independently without ambiguity
- All element IDs, routes, and data schemas match user task exactly
- No features beyond user task added or assumed
- Use write_text_file tool to output design_spec.md
- Output file: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend covering all application routes and data handling as specified in the design documents.

Task Details:
- Read design_spec.md Section 1 (Flask Routes) and Section 3 (Data Schemas) only
- Implement app.py with all backend routes from Section 1
- Load, save, and manipulate data files per the schemas defined in Section 3 using correct field order
- Do not read or rely on frontend specifications in Section 2
- Avoid assumptions beyond the design specification

Implementation Guidelines:
1. **Flask Setup**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```
2. **Root and Routes**:
   - Implement root route '/' that redirects to the dashboard page
   - Implement each route from Section 1 with exact function names, HTTP methods, and templates
   - Use render_template with context variables exactly as specified
3. **Data Handling**:
   - Parse data files from data/*.txt using pipe-delimited format with exact field order from Section 3
   - Handle reading and writing errors gracefully
   - Use dictionaries or appropriate data structures matching the schemas
4. **Forms and Requests**:
   - For POST routes, handle form data via request.form
   - Validate input data as necessary per design spec constraints
5. **Best Practices**:
   - Include `if __name__ == '__main__':` block to run app on default port with debug enabled
   - Use url_for for route redirects and URL generation
   - Ensure robust error handling and data integrity

CRITICAL REQUIREMENTS:
- Use write_text_file tool to write the entire app.py file
- Do not implement features outside of Section 1 and Section 3 specifications
- Maintain exact naming conventions for functions, variables, and templates
- Follow data schema strictly for all file operations
- Do not provide code snippets in chat responses alone; write all code to file

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

Your goal is to implement complete and fully functional HTML templates based on the design specification's frontend requirements.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) only
- Implement all HTML templates (*.html) covering every page and UI element specified
- Include all element IDs, page titles, and navigation links exactly as specified
- Do not read or depend on backend code or Sections 1 and 3
- Do not assume or add features beyond the design spec

Implementation Instructions:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Page Title from Section 2</title>
   </head>
   <body>
       <div id="main-container-id">
           <h1>Page Title from Section 2</h1>
           <!-- Page Content Here -->
       </div>
   </body>
   </html>
   ```
2. **File Naming and Location**:
   - Save templates in a directory named 'templates'
   - Use exact file names as specified (e.g., dashboard.html, catalog.html)
3. **Element IDs**:
   - Include all static and dynamic element IDs exactly as specified, paying attention to case sensitivity
   - Use Jinja2 syntax for dynamic IDs, e.g., id="view-book-button-{{ book.book_id }}"
4. **Context Variables**:
   - Use context variables exactly as named and typed in Section 2
   - Support loops, conditionals, and data display using Jinja2 constructs
5. **Navigation and Links**:
   - Implement all navigation using url_for with exact function names
   - Static buttons and links as well as dynamic links must be implemented per specification
6. **Forms and User Interaction**:
   - Implement forms for POST requests with proper method and action attributes
   - Include all required input fields and buttons with specified IDs

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all .html templates
- Do not add pages, elements, or features not specified in Section 2
- Element IDs and page titles must match exactly including case and formatting
- Do not provide partial code snippets in chat; output must be saved files

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "IntegrationTester": {
        "prompt": (
            """You are a Software Test Engineer specializing in end-to-end integration testing of web applications using Python and HTML templates.

Your goal is to comprehensively test the integrated BookstoreOnline application’s backend (app.py) and frontend (templates) to ensure all user features work correctly and data is consistent.

Task Details:
- Read app.py and all HTML templates from CONTEXT
- Test all user workflows including browsing books, managing cart, checkout process, writing reviews, and viewing order history
- Identify and document functional bugs, UI inconsistencies, and data integrity issues
- Produce detailed test_feedback.txt including clear issue descriptions or approval status with the marker "[APPROVED]" when no issues remain
- Do NOT modify any code or templates

Testing Requirements:
1. **Functional Testing**:
   - Verify navigation between pages (Dashboard, Catalog, Book Details, Cart, Checkout, Orders, Reviews, Write Review, Bestsellers)
   - Confirm correct data display using data files schema
   - Test interaction elements such as buttons, inputs, filters, and dynamic lists
   - Validate cart quantity updates, item removals, and checkout flow correctness
   - Confirm review submission and display consistency
   - Verify order history and filtering by status

2. **UI Consistency**:
   - Check presence of all required element IDs exactly as specified
   - Ensure layout stability when data changes
   - Validate dynamic element IDs are correctly rendered with variables

3. **Data Integrity**:
   - Cross-check displayed data matches backend data structures
   - Confirm all price calculations and totals are accurate
   - Validate reading and writing flows for orders and reviews

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to run functional tests on app.py where applicable
- Use write_text_file tool to save detailed test_feedback.txt
- Feedback file must contain "[APPROVED]" to signal no detected issues
- Provide clear issue descriptions with reproduction steps if any problem arises
- Do NOT perform fixes or code changes in this step

Output: test_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'test_feedback.txt'}],
    },

    "IntegrationFixer": {
        "prompt": (
            """You are a Full-Stack Developer specializing in Python Flask applications with HTML frontend integration.

Your goal is to iteratively fix bugs and inconsistencies in backend (app.py) and frontend (templates) to achieve full integration approval from the IntegrationTester.

Task Details:
- Read test_feedback.txt to understand tester-reported issues
- Read current app.py and all HTML templates from CONTEXT
- Modify and fix backend and/or frontend artifacts to resolve all reported problems
- Preserve application architecture and data format consistency
- Output updated app.py and templates/*.html reflecting fixes
- Do NOT introduce new features beyond addressing listed issues
- Be prepared for multiple iterations until IntegrationTester marks "[APPROVED]"

Implementation Guidelines:
1. **Analyze Feedback**:
   - Identify all functional, UI, and data issues reported
   - Prioritize fixes based on severity and user impact

2. **Fix Backend**:
   - Correct route handlers, data loading, and business logic as needed
   - Ensure data reads/writes align exactly with specified formats

3. **Fix Frontend**:
   - Adjust templates for missing or incorrect element IDs
   - Fix dynamic ID rendering and data presentation inconsistencies
   - Verify all navigation elements work as expected

4. **Testing and Validation**:
   - Manually re-check critical fixes after each iteration (no testing tool runs here)
   - Prepare for next round of integration testing

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save revised app.py and templates
- Closely follow tester feedback to fully resolve all issues
- Do NOT alter files unrelated to reported issues
- Maintain coding best practices and consistent style

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'test_feedback.txt', 'source': 'IntegrationTester'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Check design_spec.md Sections 1 and 3 for backend completeness: all Flask routes with correct names, HTTP methods, context variables; "
                "data schemas match required fields, correct order and format for all data files.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md Section 2 for frontend completeness: template files with all element IDs, context variables align with specs, "
                "navigation uses correct url_for calls and matches page structure.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py implements all Flask routes accurately as per Section 1 of design_spec.md, "
                "data handling matches schemas in Section 3, and root route redirects to dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify templates/*.html contain all specified element IDs, context variables, and navigation links as per Section 2 of design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'IntegrationTester': [
        ("SystemArchitect", """Assess test_feedback.txt to ensure all major issues found during integration testing are clearly documented and explained.""", [{'type': 'text_file', 'name': 'test_feedback.txt'}])
    ],

    'IntegrationFixer': [
        ("IntegrationTester", """Verify that IntegrationFixer addresses all test_feedback.txt issues effectively in next implementation iteration.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'test_feedback.txt'}])
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
    await execute(SystemArchitect, "Create detailed design_spec.md covering Flask routes, HTML templates, and data schemas for BookstoreOnline as specified in user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_development_phase():
    # Create agents
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=180,
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
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py based on design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all HTML templates based on design_spec.md Section 2")
    )
# Phase2_End

# Phase3_Start

async def integration_testing_phase():
    # Create IntegrationTester agent
    IntegrationTester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationTester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )
    # Create IntegrationFixer agent
    IntegrationFixer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 3
    for iteration in range(MAX_LOOPS):
        if iteration == 0:
            # First run: run IntegrationTester only
            await execute(IntegrationTester, "Perform comprehensive integration testing on app.py and templates and write test_feedback.txt")
        else:
            # Subsequent runs: IntegrationFixer fixes reported issues, then IntegrationTester tests again
            try:
                with open("test_feedback.txt", "r") as f:
                    feedback = f.read()
            except FileNotFoundError:
                break

            if "[APPROVED]" in feedback:
                break

            await execute(IntegrationFixer, f"Fix all issues reported in test_feedback.txt:\n{feedback}")
            await execute(IntegrationTester, "Perform comprehensive integration testing on updated app.py and templates and write test_feedback.txt")

        # After each iteration check approval
        try:
            with open("test_feedback.txt", "r") as f:
                feedback = f.read()
            if "[APPROVED]" in feedback:
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
        parallel_development_phase()
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
