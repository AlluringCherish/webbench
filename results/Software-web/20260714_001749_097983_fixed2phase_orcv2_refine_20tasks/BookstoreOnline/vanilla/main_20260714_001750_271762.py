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
# 20260714_001750_271762/main_20260714_001750_271762.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the adaptive Web design contract for the 'BookstoreOnline' app, producing design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator writes design_spec.md describing all nine pages, data storage format, and element IDs; \"\n        \"DesignCritic reviews design_spec.md for completeness, correctness, and feasibility, producing design_feedback.md. \"\n        \"Two iterations maximum, stopping on [APPROVED].\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Web Application Designer specializing in Python-based web applications with local text file data management.\n\nYour goal is to generate or revise a complete and detailed design specification document ('design_spec.md') for the 'BookstoreOnline' application, reflecting the user task requirements and incorporating feedback from the design critic. The document must comprehensively describe all nine pages with their element IDs and layouts, plus the local text data storage format.\n\nTask Details:\n- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT\n- On initial iteration, produce full design_spec.md covering pages, page elements, and data formats\n- On subsequent iteration triggered by NEED_MODIFY feedback, apply all corrections and overwrite design_spec.md\n- On [APPROVED] feedback, preserve the final approved design\n\n**Section 1: Page Layouts and Elements**\n- Specify all nine pages by page title and overview\n- Include all UI elements with exact IDs, types, and contextual descriptions\n- Maintain consistency with user task description requirements\n\n**Section 2: Data Storage Specification**\n- Detail each local data text file schema with filename, format, fields, and example data\n- Ensure alignment with page functionalities and data usage in UI\n\n**Section 3: Consistency and Completeness**\n- The design_spec.md must fully represent all user requirements\n- Do not omit required pages or their specified elements\n- Do not add elements or pages not in user requirements\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save the complete design_spec.md\n- The document must be human-readable Markdown\n- Run at most two iterations, stopping immediately on [APPROVED] feedback\n- Apply every NEED_MODIFY comment thoroughly without adding new requirements\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ],\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer with expertise in Python web application design and local file data management.\n\nYour goal is to review the provided 'design_spec.md' for the 'BookstoreOnline' application to ensure it fully complies with the user task description and is complete, internally consistent, and feasible. Produce gated feedback in 'design_feedback.md' that explicitly starts with [APPROVED] or NEED_MODIFY, guiding a maximum of two refinement iterations.\n\nTask Details:\n- Read user_task_description and current design_spec.md from CONTEXT\n- Verify coverage of all nine pages with correct page titles, overviews, and element IDs\n- Validate data storage specifications aligning with UI functionalities\n- Check for consistency and absence of extra or omitted requirements\n- Write [APPROVED] if the design_spec.md is complete and correct\n- If corrections are needed, begin feedback with NEED_MODIFY followed by specific targeted corrections\n\nReview Requirements:\n1. Confirm all pages specified exactly as per user requirements\n2. All UI elements and their IDs match the user task list for each page\n3. Data file schemas cover the seven specified text files with accurate fields and example data\n4. Feasibility checks ensuring the design can be implemented as described\n5. No additions beyond stated user requirements or contradictions\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY\n- No extra leading characters or whitespace before the feedback marker\n- Use write_text_file tool to save complete design_feedback.md\n- At most two review iterations are permitted; stop immediately if approved\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ],\n        },\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Check design_spec.md for coverage of all user requirements, accurate page and element specifications, and consistency with local text data storage format.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ],\n        }\n    ],\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine complete backend and frontend implementation producing app.py and templates/*.html, gated by code_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator writes or revises app.py and all templates/*.html using design_spec.md and code_feedback.md as inputs; \"\n        \"CodeCritic reviews the code bundle for correctness, functional completeness, exact element IDs, and compliance, producing code_feedback.md. \"\n        \"Two iterations maximum, stopping on [APPROVED].\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Full-Stack Python Developer expert in backend and frontend web application implementation.\n\nYour goal is to generate or revise the complete backend (app.py) and frontend templates (templates/*.html) implementing all pages and local text file data management according to design_spec.md. Revise based on code_feedback.md for at most two iterations.\n\nTask Details:\n- Read design_spec.md describing page routes, element IDs, and data specifications from CONTEXT\n- On iteration one, create full app.py and all required templates/*.html\n- When code_feedback.md begins with NEED_MODIFY, apply all corrections fully and overwrite app.py and templates/*.html\n- When code_feedback.md begins with [APPROVED], finalize and preserve the output artifacts\n\n**Section 1: Backend Implementation**\n- Implement app.py with Flask routes matching all pages described in design_spec.md\n- Implement data access and manipulation using local text files as per data format specs\n- Manage shopping cart, orders, reviews, and bestsellers data according to requirements\n- Use only standard Python libraries and specified local text file formats\n- Ensure endpoints produce data in correct context for rendering templates\n\n**Section 2: Frontend Templates**\n- Create templates/*.html files corresponding to each described page\n- Include exact HTML element IDs as specified (e.g., dashboard-page, featured-books, etc.)\n- Implement all buttons, inputs, dropdowns, tables, and UI elements for user interactions\n- Use Jinja2 templating syntax consistent with Flask backend context variables\n- Ensure all interactive elements have correct IDs and names for user flows\n\n**Section 3: Data Storage and Access**\n- Follow exact data format and file naming conventions specified in the requirements\n- Load and update data files atomically to prevent data corruption\n- Reflect stock availability and prices correctly throughout UI and backend logic\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to output app.py and all templates/*.html files separately\n- Maintain exact element IDs and data file schema consistency from design_spec.md\n- Implement all features including browsing, cart management, checkout, reviews, and order history\n- Run at most two Generator/Critic iterations, stopping immediately if code_feedback.md starts with [APPROVED]\n- Do not add new pages or features beyond those described\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n            ],\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in web application backend and frontend code reviews.\n\nYour goal is to review app.py and templates/*.html for correctness, functional completeness, accurate element IDs, and compliance with design_spec.md, providing gated feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify backend routes, data file integrations, and logic completeness\n- Verify frontend templates contain all specified pages with exact element IDs and UI elements\n- Confirm all user flows and interactive elements function as designed\n- Write code_feedback.md starting with [APPROVED] if complete and correct, or NEED_MODIFY followed by detailed corrections\n\nReview Criteria:\n1. All routes and pages conform to design_spec.md specification exactly\n2. Local text file data formats and handling match the requirements document\n3. Element IDs in HTML templates are all present and correct as specified\n4. User interaction flows (cart, checkout, reviews, orders) are fully implemented\n5. No missing or extraneous features beyond user_task specification\n\nCRITICAL REQUIREMENTS:\n- code_feedback.md MUST begin with exactly [APPROVED] or NEED_MODIFY at byte 1\n- Provide actionable, detailed correction instructions when NEED_MODIFY\n- Use the write_text_file tool to output the complete code_feedback.md file\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"},\n            ],\n        },\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Check implementation correctness, completeness against design_spec.md, and adherence to element ID conventions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n            ],\n        }\n    ],\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Web Application Designer specializing in Python-based web applications with local text file data management.

Your goal is to generate or revise a complete and detailed design specification document ('design_spec.md') for the 'BookstoreOnline' application, reflecting the user task requirements and incorporating feedback from the design critic. The document must comprehensively describe all nine pages with their element IDs and layouts, plus the local text data storage format.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- On initial iteration, produce full design_spec.md covering pages, page elements, and data formats
- On subsequent iteration triggered by NEED_MODIFY feedback, apply all corrections and overwrite design_spec.md
- On [APPROVED] feedback, preserve the final approved design

**Section 1: Page Layouts and Elements**
- Specify all nine pages by page title and overview
- Include all UI elements with exact IDs, types, and contextual descriptions
- Maintain consistency with user task description requirements

**Section 2: Data Storage Specification**
- Detail each local data text file schema with filename, format, fields, and example data
- Ensure alignment with page functionalities and data usage in UI

**Section 3: Consistency and Completeness**
- The design_spec.md must fully represent all user requirements
- Do not omit required pages or their specified elements
- Do not add elements or pages not in user requirements

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save the complete design_spec.md
- The document must be human-readable Markdown
- Run at most two iterations, stopping immediately on [APPROVED] feedback
- Apply every NEED_MODIFY comment thoroughly without adding new requirements

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer with expertise in Python web application design and local file data management.

Your goal is to review the provided 'design_spec.md' for the 'BookstoreOnline' application to ensure it fully complies with the user task description and is complete, internally consistent, and feasible. Produce gated feedback in 'design_feedback.md' that explicitly starts with [APPROVED] or NEED_MODIFY, guiding a maximum of two refinement iterations.

Task Details:
- Read user_task_description and current design_spec.md from CONTEXT
- Verify coverage of all nine pages with correct page titles, overviews, and element IDs
- Validate data storage specifications aligning with UI functionalities
- Check for consistency and absence of extra or omitted requirements
- Write [APPROVED] if the design_spec.md is complete and correct
- If corrections are needed, begin feedback with NEED_MODIFY followed by specific targeted corrections

Review Requirements:
1. Confirm all pages specified exactly as per user requirements
2. All UI elements and their IDs match the user task list for each page
3. Data file schemas cover the seven specified text files with accurate fields and example data
4. Feasibility checks ensuring the design can be implemented as described
5. No additions beyond stated user requirements or contradictions

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- No extra leading characters or whitespace before the feedback marker
- Use write_text_file tool to save complete design_feedback.md
- At most two review iterations are permitted; stop immediately if approved

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Full-Stack Python Developer expert in backend and frontend web application implementation.

Your goal is to generate or revise the complete backend (app.py) and frontend templates (templates/*.html) implementing all pages and local text file data management according to design_spec.md. Revise based on code_feedback.md for at most two iterations.

Task Details:
- Read design_spec.md describing page routes, element IDs, and data specifications from CONTEXT
- On iteration one, create full app.py and all required templates/*.html
- When code_feedback.md begins with NEED_MODIFY, apply all corrections fully and overwrite app.py and templates/*.html
- When code_feedback.md begins with [APPROVED], finalize and preserve the output artifacts

**Section 1: Backend Implementation**
- Implement app.py with Flask routes matching all pages described in design_spec.md
- Implement data access and manipulation using local text files as per data format specs
- Manage shopping cart, orders, reviews, and bestsellers data according to requirements
- Use only standard Python libraries and specified local text file formats
- Ensure endpoints produce data in correct context for rendering templates

**Section 2: Frontend Templates**
- Create templates/*.html files corresponding to each described page
- Include exact HTML element IDs as specified (e.g., dashboard-page, featured-books, etc.)
- Implement all buttons, inputs, dropdowns, tables, and UI elements for user interactions
- Use Jinja2 templating syntax consistent with Flask backend context variables
- Ensure all interactive elements have correct IDs and names for user flows

**Section 3: Data Storage and Access**
- Follow exact data format and file naming conventions specified in the requirements
- Load and update data files atomically to prevent data corruption
- Reflect stock availability and prices correctly throughout UI and backend logic

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to output app.py and all templates/*.html files separately
- Maintain exact element IDs and data file schema consistency from design_spec.md
- Implement all features including browsing, cart management, checkout, reviews, and order history
- Run at most two Generator/Critic iterations, stopping immediately if code_feedback.md starts with [APPROVED]
- Do not add new pages or features beyond those described

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in web application backend and frontend code reviews.

Your goal is to review app.py and templates/*.html for correctness, functional completeness, accurate element IDs, and compliance with design_spec.md, providing gated feedback for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify backend routes, data file integrations, and logic completeness
- Verify frontend templates contain all specified pages with exact element IDs and UI elements
- Confirm all user flows and interactive elements function as designed
- Write code_feedback.md starting with [APPROVED] if complete and correct, or NEED_MODIFY followed by detailed corrections

Review Criteria:
1. All routes and pages conform to design_spec.md specification exactly
2. Local text file data formats and handling match the requirements document
3. Element IDs in HTML templates are all present and correct as specified
4. User interaction flows (cart, checkout, reviews, orders) are fully implemented
5. No missing or extraneous features beyond user_task specification

CRITICAL REQUIREMENTS:
- code_feedback.md MUST begin with exactly [APPROVED] or NEED_MODIFY at byte 1
- Provide actionable, detailed correction instructions when NEED_MODIFY
- Use the write_text_file tool to output the complete code_feedback.md file

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Check design_spec.md for coverage of all user requirements, accurate page and element specifications, and consistency with local text data storage format.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md""", [])
    ],

    'AppGenerator': [
        ("CodeCritic", """Check implementation correctness, completeness against design_spec.md, and adherence to element ID conventions.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py""", [])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    DesignCritic = build_resilient_agent(
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
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
            "Generate or revise the complete design_spec.md for 'BookstoreOnline' application.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md for completeness, correctness, and feasibility for 'BookstoreOnline'. "
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
import glob

async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
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

        await execute(
            AppGenerator,
            "Create or revise the complete backend (app.py) and frontend templates (templates/*.html) implementing all pages and local text file data management according to design_spec.md.\n\n"
            f"=== design_spec.md from CONTEXT ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
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
            "Review app.py and all templates/*.html for correctness, functional completeness, accurate element IDs, and compliance with design_spec.md.\n\n"
            f"=== design_spec.md from CONTEXT ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
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
