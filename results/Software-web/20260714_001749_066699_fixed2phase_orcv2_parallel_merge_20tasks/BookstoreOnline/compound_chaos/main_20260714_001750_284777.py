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
# 20260714_001750_284777/main_20260714_001750_284777.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications for 'BookstoreOnline' and merge them into one consistent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect designs the Flask routes and data schemas, including local text file formats and data handling requirements. \"\n        \"FrontendDesignArchitect designs the HTML templates, element IDs, navigation, and page structure as per the specifications. \"\n        \"DesignMerger consolidates backend_design.md and frontend_design.md ensuring consistency with the user task and outputs design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend development and data schema design for Python applications using local text file storage.\n\nYour goal is to produce the backend design specification covering all Flask routes, local text data file formats, and backend logic needed for the 'BookstoreOnline' user requirements.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create backend_design.md\n- Specify all Flask routes with methods, route paths, expected request parameters, and response templates\n- Specify all data schemas for local text files (books.txt, categories.txt, cart.txt, orders.txt, order_items.txt, reviews.txt, bestsellers.txt) including exact file names, delimiter '|', field order, data types, and example rows\n- Do not read or rely on frontend_design.md\n\n**Section 1: Flask Routes Specification**\n- Define route URL patterns, HTTP methods, function names, and associated template filenames\n- Detail context variables passed to templates, form data received, and actions performed (e.g., add to cart, checkout, submit review)\n- Include routes for all nine pages (Dashboard, Book Catalog, Book Details, Shopping Cart, Checkout, Order History, Reviews, Write Review, Bestsellers)\n- Include navigation routes between pages and button action handling\n\n**Section 2: Text File Data Schemas**\n- For each data file, describe file name, exact delimiter, column names with data types, and constraints\n- Provide sample data rows matching user examples for clarity\n- Include data manipulation considerations (e.g., updating stock, cart contents, order status)\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can implement the entire Flask backend using backend_design.md alone\n- Routes and data schemas strictly align with user_task_description and local text file storage approach\n- Must use write_text_file tool to output backend_design.md\n- Output only the declared artifact backend_design.md without refinement markers\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in HTML/Jinja2 template design and user interface structure for Python web applications.\n\nYour goal is to produce the frontend design specification covering all HTML templates, exact element IDs, page structure, and navigation flows to implement the 'BookstoreOnline' web UI.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create frontend_design.md\n- Specify all HTML templates for the nine pages detailed in user_task_description\n- Define exact element IDs, element types (div, button, table, input, dropdown, textarea, etc.), and page titles\n- Specify navigation flows between pages triggered by buttons and links\n- Include lists/grids/tables structure, context variables used in templates, and dynamic elements such as book lists, cart items, reviews, and bestsellers\n- Do not read or rely on backend_design.md\n\n**Section 1: HTML Template Specifications**\n- Specify each template file name and page title\n- List every element ID with its HTML tag type and description reflecting user_task_description\n- Define dynamic content placeholders (e.g., book cards, reviews list) and how data from context variables maps to layout\n- Map buttons and navigation controls to their target pages or actions\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement all templates from frontend_design.md alone\n- Element IDs, page titles, and navigation flow are fully consistent with user_task_description\n- Must use write_text_file tool to output frontend_design.md\n- Output only the declared artifact frontend_design.md without refinement markers\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in web application specification integration and consistency validation.\n\nYour goal is to merge backend_design.md and frontend_design.md into one cohesive design_spec.md that fully satisfies the 'BookstoreOnline' user requirements without contradictions or omissions.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Independently reconcile backend and frontend specifications ensuring alignment on routes, templates, element IDs, navigation, and data schemas\n- Validate completeness of all nine pages and their functionalities as specified by user_task_description\n- Produce a consolidated design_spec.md including backend Flask routes, data schemas, frontend templates, element IDs, and navigation maps\n\n**Section 1: Backend and Frontend Consistency Checks**\n- Cross-check route URLs with template file names and frontend navigation targets\n- Ensure element IDs referenced in backend context variables exist in frontend templates\n- Resolve any naming discrepancies in routing, context variable usage, or data files\n\n**Section 2: Comprehensive Design Specification**\n- Combine all backend and frontend details into one unified specification document\n- Organize sections clearly: Flask routes, local text file data schemas, HTML templates, element IDs, and navigation flows\n- Highlight how data flows between backend and frontend using local text files as persistent store\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper and FrontendDeveloper can implement their parts directly from design_spec.md\n- The consolidated artifact contains no conflicting specifications or missing requirements\n- Must use write_text_file tool to output design_spec.md\n- Output only the declared artifact design_spec.md without refinement markers\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure backend design completeness and alignment with user requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure frontend design completeness and alignment with user requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend and frontend artifacts from design_spec.md in parallel and integrate them into a consistent 'BookstoreOnline' application\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using backend specifications from design_spec.md including data management from local text files. \"\n        \"FrontendDeveloper implements all HTML templates (*.html) including all required pages and element IDs. \"\n        \"IntegrationMerger reconciles app.py and templates/*.html ensuring interface consistency and produces final deployable app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask applications with local text file data management.\n\nYour goal is to implement the complete Flask backend app.py based exclusively on backend specifications from design_spec.md, managing all data operations on local text files as declared.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Independently implement app.py with Flask routes and data file handling as specified\n- Produce app.py implementing all backend logic including CRUD, data parsing, and business rules per design_spec.md\n- Do not read or use any frontend templates or outputs\n\n**Implementation Requirements: Flask Backend**\n- Implement each route with correct URL, HTTP methods, and handlers as defined\n- Implement reading from and writing to designated text files (e.g., books.txt, cart.txt, orders.txt) per specified schema\n- Handle all user actions: browsing books, cart management, checkout, reviews, and order history without authentication\n- Use consistent variable and function names per design_spec.md conventions\n- Implement data parsing with correct field delimiters and types from text files\n- Return JSON or render templates endpoints as appropriate (render_template calls match frontend expectations)\n\n**Code Structure and Standards:**\n- Use single-quoted docstrings for any inline documentation or code comments\n- Follow Flask best practices for route definition, error handling, and modularity\n- Include writing to 'data' directory files with proper file locking or atomic writes if needed\n- No external databases or persistent storage outside specified text files permitted\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save app.py output\n- Implement only declared routes and data interactions as per design_spec.md\n- Generated app.py is complete, self-contained, and ready for integration with frontend templates\n- Do not use or produce any files beyond app.py\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask applications.\n\nYour goal is to fully implement all frontend HTML templates (*.html) for the 'BookstoreOnline' application, strictly following the structure, element IDs, and navigation requirements specified in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT\n- Independently create all templates/*.html reflecting the nine pages described\n- Include all specified page titles, container divs, buttons, inputs, tables, dropdowns, and navigation elements exactly as named\n- Implement Jinja2 templating syntax where dynamic data rendering is implied\n- Do not read, validate, or assume any backend implementations beyond design_spec.md\n\n**Template Implementation Guidelines:**\n- Preserve exact ID attributes for all elements like dashboard-page, featured-books, search-input, cart-items-table, etc.\n- Include navigation controls between pages as specified (e.g., buttons linking dashboard to catalog, back-to-dashboard buttons)\n- Structure tables for cart, orders, and reviews with appropriate columns and placeholders for dynamic content\n- Implement forms for order checkout and write review pages with correct input types and IDs\n- Follow HTML5 standards and keep templates modular and readable\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save template files in templates/*.html\n- Templates completely reflect design_spec.md page and element requirements without deviation\n- Do not use or write any files beyond the declared templates\n- Generated frontend is ready to integrate seamlessly with backend app.py\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Specialist skilled in merging Flask backend and Jinja2 frontend templates.\n\nYour goal is to review and merge the independently implemented app.py backend and templates/*.html frontend outputs to ensure full consistency, correctness, and readiness for production deployment of the 'BookstoreOnline' application.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate that app.py routes match template filenames, element IDs, and navigation flows in templates\n- Ensure data variable names passed from backend to frontend templates are consistent and correctly referenced\n- Detect and resolve interface discrepancies between backend endpoints and frontend template expectations\n- Produce final integrated and consistent app.py and templates/*.html artifacts ready for deployment\n\n**Integration and Consistency Checks:**\n- Verify all route URLs in app.py exist as links or forms in frontend templates\n- Check that all template variables rendered are set or passed correctly from app.py\n- Confirm all input elements, buttons, and forms in templates correspond to backend handlers managing data files\n- Harmonize any naming conflicts or missing elements found between backend and frontend\n- Ensure no additional features or requirements beyond design_spec.md are introduced\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output final app.py and templates/*.html\n- Output artifacts overwrite prior worker versions with fully reconciled content\n- Focus only on inputs from declared artifacts, no external assumptions\n- Provide integrated deliverables that enable seamless Flask app execution with complete UI\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Validate backend implementation against design_spec.md and integration interface.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Validate frontend HTML templates against design_spec.md and integration interface.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend development and data schema design for Python applications using local text file storage.

Your goal is to produce the backend design specification covering all Flask routes, local text data file formats, and backend logic needed for the 'BookstoreOnline' user requirements.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md
- Specify all Flask routes with methods, route paths, expected request parameters, and response templates
- Specify all data schemas for local text files (books.txt, categories.txt, cart.txt, orders.txt, order_items.txt, reviews.txt, bestsellers.txt) including exact file names, delimiter '|', field order, data types, and example rows
- Do not read or rely on frontend_design.md

**Section 1: Flask Routes Specification**
- Define route URL patterns, HTTP methods, function names, and associated template filenames
- Detail context variables passed to templates, form data received, and actions performed (e.g., add to cart, checkout, submit review)
- Include routes for all nine pages (Dashboard, Book Catalog, Book Details, Shopping Cart, Checkout, Order History, Reviews, Write Review, Bestsellers)
- Include navigation routes between pages and button action handling

**Section 2: Text File Data Schemas**
- For each data file, describe file name, exact delimiter, column names with data types, and constraints
- Provide sample data rows matching user examples for clarity
- Include data manipulation considerations (e.g., updating stock, cart contents, order status)

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement the entire Flask backend using backend_design.md alone
- Routes and data schemas strictly align with user_task_description and local text file storage approach
- Must use write_text_file tool to output backend_design.md
- Output only the declared artifact backend_design.md without refinement markers

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in HTML/Jinja2 template design and user interface structure for Python web applications.

Your goal is to produce the frontend design specification covering all HTML templates, exact element IDs, page structure, and navigation flows to implement the 'BookstoreOnline' web UI.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md
- Specify all HTML templates for the nine pages detailed in user_task_description
- Define exact element IDs, element types (div, button, table, input, dropdown, textarea, etc.), and page titles
- Specify navigation flows between pages triggered by buttons and links
- Include lists/grids/tables structure, context variables used in templates, and dynamic elements such as book lists, cart items, reviews, and bestsellers
- Do not read or rely on backend_design.md

**Section 1: HTML Template Specifications**
- Specify each template file name and page title
- List every element ID with its HTML tag type and description reflecting user_task_description
- Define dynamic content placeholders (e.g., book cards, reviews list) and how data from context variables maps to layout
- Map buttons and navigation controls to their target pages or actions

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement all templates from frontend_design.md alone
- Element IDs, page titles, and navigation flow are fully consistent with user_task_description
- Must use write_text_file tool to output frontend_design.md
- Output only the declared artifact frontend_design.md without refinement markers

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in web application specification integration and consistency validation.

Your goal is to merge backend_design.md and frontend_design.md into one cohesive design_spec.md that fully satisfies the 'BookstoreOnline' user requirements without contradictions or omissions.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Independently reconcile backend and frontend specifications ensuring alignment on routes, templates, element IDs, navigation, and data schemas
- Validate completeness of all nine pages and their functionalities as specified by user_task_description
- Produce a consolidated design_spec.md including backend Flask routes, data schemas, frontend templates, element IDs, and navigation maps

**Section 1: Backend and Frontend Consistency Checks**
- Cross-check route URLs with template file names and frontend navigation targets
- Ensure element IDs referenced in backend context variables exist in frontend templates
- Resolve any naming discrepancies in routing, context variable usage, or data files

**Section 2: Comprehensive Design Specification**
- Combine all backend and frontend details into one unified specification document
- Organize sections clearly: Flask routes, local text file data schemas, HTML templates, element IDs, and navigation flows
- Highlight how data flows between backend and frontend using local text files as persistent store

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper and FrontendDeveloper can implement their parts directly from design_spec.md
- The consolidated artifact contains no conflicting specifications or missing requirements
- Must use write_text_file tool to output design_spec.md
- Output only the declared artifact design_spec.md without refinement markers

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Python Flask applications with local text file data management.

Your goal is to implement the complete Flask backend app.py based exclusively on backend specifications from design_spec.md, managing all data operations on local text files as declared.

Task Details:
- Read design_spec.md from CONTEXT
- Independently implement app.py with Flask routes and data file handling as specified
- Produce app.py implementing all backend logic including CRUD, data parsing, and business rules per design_spec.md
- Do not read or use any frontend templates or outputs

**Implementation Requirements: Flask Backend**
- Implement each route with correct URL, HTTP methods, and handlers as defined
- Implement reading from and writing to designated text files (e.g., books.txt, cart.txt, orders.txt) per specified schema
- Handle all user actions: browsing books, cart management, checkout, reviews, and order history without authentication
- Use consistent variable and function names per design_spec.md conventions
- Implement data parsing with correct field delimiters and types from text files
- Return JSON or render templates endpoints as appropriate (render_template calls match frontend expectations)

**Code Structure and Standards:**
- Use single-quoted docstrings for any inline documentation or code comments
- Follow Flask best practices for route definition, error handling, and modularity
- Include writing to 'data' directory files with proper file locking or atomic writes if needed
- No external databases or persistent storage outside specified text files permitted

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save app.py output
- Implement only declared routes and data interactions as per design_spec.md
- Generated app.py is complete, self-contained, and ready for integration with frontend templates
- Do not use or produce any files beyond app.py

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask applications.

Your goal is to fully implement all frontend HTML templates (*.html) for the 'BookstoreOnline' application, strictly following the structure, element IDs, and navigation requirements specified in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT
- Independently create all templates/*.html reflecting the nine pages described
- Include all specified page titles, container divs, buttons, inputs, tables, dropdowns, and navigation elements exactly as named
- Implement Jinja2 templating syntax where dynamic data rendering is implied
- Do not read, validate, or assume any backend implementations beyond design_spec.md

**Template Implementation Guidelines:**
- Preserve exact ID attributes for all elements like dashboard-page, featured-books, search-input, cart-items-table, etc.
- Include navigation controls between pages as specified (e.g., buttons linking dashboard to catalog, back-to-dashboard buttons)
- Structure tables for cart, orders, and reviews with appropriate columns and placeholders for dynamic content
- Implement forms for order checkout and write review pages with correct input types and IDs
- Follow HTML5 standards and keep templates modular and readable

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save template files in templates/*.html
- Templates completely reflect design_spec.md page and element requirements without deviation
- Do not use or write any files beyond the declared templates
- Generated frontend is ready to integrate seamlessly with backend app.py

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Specialist skilled in merging Flask backend and Jinja2 frontend templates.

Your goal is to review and merge the independently implemented app.py backend and templates/*.html frontend outputs to ensure full consistency, correctness, and readiness for production deployment of the 'BookstoreOnline' application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate that app.py routes match template filenames, element IDs, and navigation flows in templates
- Ensure data variable names passed from backend to frontend templates are consistent and correctly referenced
- Detect and resolve interface discrepancies between backend endpoints and frontend template expectations
- Produce final integrated and consistent app.py and templates/*.html artifacts ready for deployment

**Integration and Consistency Checks:**
- Verify all route URLs in app.py exist as links or forms in frontend templates
- Check that all template variables rendered are set or passed correctly from app.py
- Confirm all input elements, buttons, and forms in templates correspond to backend handlers managing data files
- Harmonize any naming conflicts or missing elements found between backend and frontend
- Ensure no additional features or requirements beyond design_spec.md are introduced

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output final app.py and templates/*.html
- Output artifacts overwrite prior worker versions with fully reconciled content
- Focus only on inputs from declared artifacts, no external assumptions
- Provide integrated deliverables that enable seamless Flask app execution with complete UI

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
        ("DesignMerger", """Ensure backend design completeness and alignment with user requirements.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Ensure frontend design completeness and alignment with user requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Validate backend implementation against design_spec.md and integration interface.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Validate frontend HTML templates against design_spec.md and integration interface.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(BackendDesignArchitect, "Independently create backend_design.md with all Flask routes, data schemas, and backend logic according to user_task_description."),
        execute(FrontendDesignArchitect, "Independently create frontend_design.md with all HTML templates, element IDs, page structure, and navigation flows according to user_task_description.")
    )

    # Read outputs for merger
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

    # Merge backend and frontend specifications into design_spec.md
    await execute(DesignMerger,
                  f"=== Backend Design ===\n{backend_design_content}\n\n=== Frontend Design ===\n{frontend_design_content}\n\n"
                  "Merge these into one consistent design_spec.md that fully satisfies the user_task_description.")
# Phase1_End

# Phase2_Start

async def implementation_and_verification_phase():
    import asyncio
    import glob

    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
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
        timeout_threshold=450,
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
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=45
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete app.py backend based on design_spec.md, managing all data files and logic without frontend dependencies."),
        execute(FrontendDeveloper,
                "Implement all frontend templates/*.html based on design_spec.md with exact element IDs, navigation, and Jinja2 templating.")
    )

    # Read artifacts for IntegrationMerger
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except FileNotFoundError:
        pass
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Execute IntegrationMerger to produce final integrated app.py and templates/*.html
    await execute(
        IntegrationMerger,
        f"Review and merge backend and frontend implementations ensuring full consistency and correctness.\n\n"
        f"=== design_spec.md ===\n{design_spec_content}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== Templates ===\n{templates_content}"
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
