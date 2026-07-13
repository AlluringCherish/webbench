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
# 20260714_001750_193488/main_20260714_001750_193488.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the FoodDelivery web application design specification with detailed page layouts, element IDs, and data storage formats; deliver design_spec.md and gated design_feedback.md.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"DesignGenerator writes design_spec.md based on user_task_description and design_feedback.md; DesignCritic reviews design_spec.md and writes design_feedback.md starting with [APPROVED] or NEED_MODIFY.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python web application design specifications.\n\nYour goal is to create and iteratively revise a complete design specification for a FoodDelivery web application, focusing on page layouts, element IDs, navigation flow, and data storage formats.\n\nTask Details:\n- Read the full user_task_description from CONTEXT to capture all functional and data requirements.\n- Read the current design_spec.md and design_feedback.md artifacts from CONTEXT, if present.\n- On the first iteration, produce a full design_spec.md document covering all pages and data formats.\n- If design_feedback.md begins with NEED_MODIFY, incorporate all requested changes and overwrite design_spec.md.\n- Cease iterations after two or on receiving [APPROVED] feedback.\n\n**Section 1: Page Layouts and Element IDs**\n- Specify each page with its exact title and a container element ID.\n- Detail all UI elements per page with their element IDs, types, and brief purpose.\n- Maintain consistency of element ID naming and map navigation controls explicitly.\n\n**Section 2: Navigation Flow**\n- Define how users navigate between pages, referencing button IDs and expected actions.\n- Ensure the Dashboard page is the application’s start point.\n- Provide a clear mapping of page transitions via UI elements.\n\n**Section 3: Data Storage Formats**\n- List all local data files with exact file names.\n- Specify file data schemas by field names, separators, and data types.\n- Include example data rows consistent with the specification.\n\nCRITICAL SUCCESS CRITERIA:\n- Use the write_text_file tool to save design_spec.md.\n- Keep the design_spec.md artifact self-contained and authoritative for implementation.\n- Follow the Refinement Loop protocol with two iterations max.\n- Produce clear, unambiguous, and comprehensive specifications aligned with user_task_description.\n- Do not include status markers inside design_spec.md.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Python web application specifications.\n\nYour goal is to review the design_spec.md artifact for completeness, clarity, and alignment with the FoodDelivery user requirements and provide gated feedback for at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT.\n- Verify all specified pages contain page titles and required element IDs with types and purposes.\n- Confirm navigation flow matches the described UI controls and starts with the Dashboard page.\n- Validate all data storage files include filename, exact field schemas, separators, types, and example records.\n- Write feedback in design_feedback.md starting exactly with [APPROVED] if complete and consistent.\n- If incomplete, unclear, or missing details, begin feedback with NEED_MODIFY followed by concrete, itemized corrections.\n\nReview Criteria:\n1. Completeness of page layouts and all UI element IDs per provided user task.\n2. Clarity in navigation scheme and correctness of page transition mappings.\n3. Accuracy and consistency of all data storage file specifications with example data.\n4. No contradictions or ambiguities relative to user_task_description.\n5. No additional requirements beyond original user task.\n\nCRITICAL REQUIREMENTS:\n- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.\n- Do not add headings or whitespace before the status marker.\n- Use write_text_file tool to save the full review feedback.\n- Adhere strictly to the two-iteration refinement loop and stop upon approval.\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Verify design_spec.md fully addresses all features, page elements, element IDs, navigation scheme, and data storage requirements without missing or ambiguous details.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Refine the full Python implementation and verification of the FoodDelivery app including app.py, HTML templates and gated code_feedback.md for at most two iterations.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"AppGenerator develops and revises app.py and templates/*.html from design_spec.md and code_feedback.md; CodeCritic reviews the implementation for correctness, completeness, adherence to design, and produces code_feedback.md starting with [APPROVED] or NEED_MODIFY.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specialized in web applications using local text file data storage.\n\nYour goal is to implement and iteratively refine the full FoodDelivery application including app.py and all HTML templates for dashboard, restaurants listing, menus, cart, orders, delivery tracking, and reviews.\n\nTask Details:\n- Read design_spec.md describing detailed page designs and data file formats from CONTEXT.\n- Read existing app.py, templates/*.html, and prior code_feedback.md for iterative refinement.\n- On first iteration, create full app.py and templates/*.html implementing all specified pages and features.\n- On NEED_MODIFY feedback, apply all corrections and overwrite app.py and templates/*.html completely.\n- On [APPROVED] feedback, preserve approved implementation.\n\n**Implementation Requirements:**\n- Implement Flask routes and view functions for all 9 pages: Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, Reviews.\n- Use local text files in 'data' directory exactly as specified for Restaurants, Menus, Cart, Orders, Order Items, Deliveries, Reviews.\n- Preserve all element IDs exactly as per design_spec.md in templates for correct navigation and UI interaction.\n- Implement button actions, search/filter inputs, quantity updates, and page navigations as described.\n- Ensure no authentication; all pages are publicly accessible.\n\n**Data Persistence Requirements:**\n- Read and write data files with correct parsing and formatting preserving exact field orders and types.\n- Implement adding to cart, updating quantities, placing orders, tracking deliveries, and managing reviews with file modifications.\n- Ensure data consistency between files and UI.\n\n**Refinement Loop Instructions:**\n- Use write_text_file tool to write final app.py and all templates/*.html.\n- Run at most two iterations; stop immediately upon receiving [APPROVED] in code_feedback.md.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specialized in verifying Python Flask web applications with local file-based data management.\n\nYour goal is to review the FoodDelivery app.py and HTML templates for syntax correctness, runtime behavior, and conformance to design_spec.md, producing gated feedback in code_feedback.md.\n\nTask Details:\n- Read design_spec.md describing required pages, elements, IDs, navigation, and data formats.\n- Read the submitted app.py and all templates/*.html from CONTEXT.\n- Do not assume undocumented features beyond design_spec.md.\n- Validate that all specified element IDs exist exactly as documented.\n- Check Flask routes and handlers are complete, consistent, and correctly linked to templates.\n- Verify data file interactions correctly read and write expected fields and formats.\n- Verify no syntax or runtime errors in app.py.\n- On complete conformance, write feedback starting with [APPROVED].\n- On any issues or incomplete features, write feedback starting with NEED_MODIFY and detailed corrections.\n\nReview Checklist:\n1. Complete implementation of all 9 pages with correct routes and templates.\n2. Exact match of all element IDs in HTML templates.\n3. Correct implementation of user actions (search, filters, add to cart, checkout).\n4. Proper reading/writing of specified text data files per documented formats.\n5. Syntax and runtime validation of app.py (use testing or code inspection).\n6. Consistency and correctness of navigation flows and button actions.\n7. No additional features or undocumented deviations from design_spec.md.\n\nCRITICAL REQUIREMENTS:\n- Begin written feedback file code_feedback.md with exactly [APPROVED] or NEED_MODIFY at byte 1.\n- Use write_text_file tool to save the complete feedback for review.\n- Conduct at most two review iterations; approve immediately if no issues.\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Verify app.py and templates/*.html fully implement design_spec.md web pages and features with correct element IDs and data file interactions, free of syntax or runtime errors.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'FoodDelivery' Web Application

## 1. Objective
Develop a comprehensive web application named 'FoodDelivery' using Python, with data managed through local text files. The application enables users to browse restaurants, view menus, place food orders, track deliveries, and write reviews. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'FoodDelivery' application is Python.

## 3. Page Design

The 'FoodDelivery' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Food Delivery Dashboard
- **Overview**: The main hub displaying featured restaurants, popular cuisines, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-restaurants** - Type: Div - Display of featured restaurant recommendations.
  - **ID: browse-restaurants-button** - Type: Button - Button to navigate to restaurant listing page.
  - **ID: view-cart-button** - Type: Button - Button to navigate to shopping cart page.
  - **ID: active-orders-button** - Type: Button - Button to navigate to active orders page.

### 2. Restaurant Listing Page
- **Page Title**: Browse Restaurants
- **Overview**: A page displaying all available restaurants with search and filter capabilities.
- **Elements**:
  - **ID: restaurants-page** - Type: Div - Container for the restaurants page.
  - **ID: search-input** - Type: Input - Field to search restaurants by name or cuisine type.
  - **ID: cuisine-filter** - Type: Dropdown - Dropdown to filter by cuisine (Chinese, Italian, Indian, American, etc.).
  - **ID: restaurants-grid** - Type: Div - Grid displaying restaurant cards with logo, name, rating, and delivery time.
  - **ID: view-restaurant-button-{restaurant_id}** - Type: Button - Button to view restaurant menu (each restaurant card has this).

### 3. Restaurant Menu Page
- **Page Title**: Restaurant Menu
- **Overview**: A page displaying detailed menu items for a specific restaurant with descriptions and prices.
- **Elements**:
  - **ID: menu-page** - Type: Div - Container for the menu page.
  - **ID: restaurant-name** - Type: H1 - Display restaurant name.
  - **ID: restaurant-info** - Type: Div - Display restaurant info (address, phone, rating).
  - **ID: menu-items-grid** - Type: Div - Grid displaying menu items with photos, names, descriptions, and prices.
  - **ID: add-to-cart-button-{item_id}** - Type: Button - Button to add menu item to cart (each item has this).
  - **ID: view-item-details-{item_id}** - Type: Button - Button to view item details (each menu item has this).

### 4. Item Details Page
- **Page Title**: Item Details
- **Overview**: A page displaying detailed information about a specific menu item including ingredients and nutritional info.
- **Elements**:
  - **ID: item-details-page** - Type: Div - Container for the item details page.
  - **ID: item-name** - Type: H1 - Display item name.
  - **ID: item-description** - Type: Div - Display item description and ingredients.
  - **ID: item-price** - Type: Div - Display item price.
  - **ID: quantity-input** - Type: Input (number) - Field to select quantity before adding to cart.
  - **ID: add-to-cart-button** - Type: Button - Button to add item with selected quantity to cart.

### 5. Shopping Cart Page
- **Page Title**: Shopping Cart
- **Overview**: A page displaying items in the cart with quantity management and checkout option.
- **Elements**:
  - **ID: cart-page** - Type: Div - Container for the cart page.
  - **ID: cart-items-table** - Type: Table - Table displaying cart items with name, quantity, price, and subtotal.
  - **ID: update-quantity-{item_id}** - Type: Input (number) - Field to update item quantity (each cart item has this).
  - **ID: remove-item-button-{item_id}** - Type: Button - Button to remove item from cart (each cart item has this).
  - **ID: proceed-checkout-button** - Type: Button - Button to proceed to checkout.
  - **ID: total-amount** - Type: Div - Display total cart amount.

### 6. Checkout Page
- **Page Title**: Checkout
- **Overview**: A page for users to enter delivery information and complete order placement.
- **Elements**:
  - **ID: checkout-page** - Type: Div - Container for the checkout page.
  - **ID: customer-name** - Type: Input - Field to input customer name.
  - **ID: delivery-address** - Type: Textarea - Field to input delivery address.
  - **ID: phone-number** - Type: Input - Field to input phone number.
  - **ID: payment-method** - Type: Dropdown - Dropdown to select payment method (Credit Card, Cash, PayPal).
  - **ID: place-order-button** - Type: Button - Button to confirm and place order.

### 7. Active Orders Page
- **Page Title**: Active Orders
- **Overview**: A page displaying current orders being prepared or delivered with tracking information.
- **Elements**:
  - **ID: active-orders-page** - Type: Div - Container for the active orders page.
  - **ID: orders-list** - Type: Div - List displaying active orders with order ID, restaurant, status, and ETA.
  - **ID: track-order-button-{order_id}** - Type: Button - Button to view detailed tracking (each order has this).
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Preparing, On the Way, Delivered).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Order Tracking Page
- **Page Title**: Track Order
- **Overview**: A page displaying detailed order tracking information with delivery person details and real-time status updates.
- **Elements**:
  - **ID: tracking-page** - Type: Div - Container for the tracking page.
  - **ID: order-details** - Type: Div - Display complete order details and timeline.
  - **ID: delivery-driver-info** - Type: Div - Display delivery driver name, phone, and vehicle info.
  - **ID: estimated-time** - Type: Div - Display estimated delivery time.
  - **ID: order-items-list** - Type: Div - List of items in the order.
  - **ID: back-to-orders** - Type: Button - Button to navigate back to active orders.

### 9. Reviews Page
- **Page Title**: Order Reviews
- **Overview**: A page displaying all customer reviews for restaurants and allowing users to write new reviews.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of all reviews with restaurant name, rating, and review text.
  - **ID: write-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: filter-by-rating** - Type: Dropdown - Dropdown to filter reviews by rating (All, 5 stars, 4 stars, etc.).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'FoodDelivery' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Restaurants Data
- **File Name**: `restaurants.txt`
- **Data Format**:
  ```
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
  ```
- **Example Data**:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. Menus Data
- **File Name**: `menus.txt`
- **Data Format**:
  ```
  item_id|restaurant_id|item_name|category|description|price|availability
  ```
- **Example Data**:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. Cart Data
- **File Name**: `cart.txt`
- **Data Format**:
  ```
  cart_id|item_id|restaurant_id|quantity|added_date
  ```
- **Example Data**:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. Orders Data
- **File Name**: `orders.txt`
- **Data Format**:
  ```
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
  ```
- **Example Data**:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. Order Items Data
- **File Name**: `order_items.txt`
- **Data Format**:
  ```
  order_item_id|order_id|item_id|quantity|price
  ```
- **Example Data**:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. Deliveries Data
- **File Name**: `deliveries.txt`
- **Data Format**:
  ```
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
  ```
- **Example Data**:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|restaurant_id|customer_name|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
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
            """You are a Software Architect specializing in Python web application design specifications.

Your goal is to create and iteratively revise a complete design specification for a FoodDelivery web application, focusing on page layouts, element IDs, navigation flow, and data storage formats.

Task Details:
- Read the full user_task_description from CONTEXT to capture all functional and data requirements.
- Read the current design_spec.md and design_feedback.md artifacts from CONTEXT, if present.
- On the first iteration, produce a full design_spec.md document covering all pages and data formats.
- If design_feedback.md begins with NEED_MODIFY, incorporate all requested changes and overwrite design_spec.md.
- Cease iterations after two or on receiving [APPROVED] feedback.

**Section 1: Page Layouts and Element IDs**
- Specify each page with its exact title and a container element ID.
- Detail all UI elements per page with their element IDs, types, and brief purpose.
- Maintain consistency of element ID naming and map navigation controls explicitly.

**Section 2: Navigation Flow**
- Define how users navigate between pages, referencing button IDs and expected actions.
- Ensure the Dashboard page is the application’s start point.
- Provide a clear mapping of page transitions via UI elements.

**Section 3: Data Storage Formats**
- List all local data files with exact file names.
- Specify file data schemas by field names, separators, and data types.
- Include example data rows consistent with the specification.

CRITICAL SUCCESS CRITERIA:
- Use the write_text_file tool to save design_spec.md.
- Keep the design_spec.md artifact self-contained and authoritative for implementation.
- Follow the Refinement Loop protocol with two iterations max.
- Produce clear, unambiguous, and comprehensive specifications aligned with user_task_description.
- Do not include status markers inside design_spec.md.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Python web application specifications.

Your goal is to review the design_spec.md artifact for completeness, clarity, and alignment with the FoodDelivery user requirements and provide gated feedback for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT.
- Verify all specified pages contain page titles and required element IDs with types and purposes.
- Confirm navigation flow matches the described UI controls and starts with the Dashboard page.
- Validate all data storage files include filename, exact field schemas, separators, types, and example records.
- Write feedback in design_feedback.md starting exactly with [APPROVED] if complete and consistent.
- If incomplete, unclear, or missing details, begin feedback with NEED_MODIFY followed by concrete, itemized corrections.

Review Criteria:
1. Completeness of page layouts and all UI element IDs per provided user task.
2. Clarity in navigation scheme and correctness of page transition mappings.
3. Accuracy and consistency of all data storage file specifications with example data.
4. No contradictions or ambiguities relative to user_task_description.
5. No additional requirements beyond original user task.

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.
- Do not add headings or whitespace before the status marker.
- Use write_text_file tool to save the full review feedback.
- Adhere strictly to the two-iteration refinement loop and stop upon approval.

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specialized in web applications using local text file data storage.

Your goal is to implement and iteratively refine the full FoodDelivery application including app.py and all HTML templates for dashboard, restaurants listing, menus, cart, orders, delivery tracking, and reviews.

Task Details:
- Read design_spec.md describing detailed page designs and data file formats from CONTEXT.
- Read existing app.py, templates/*.html, and prior code_feedback.md for iterative refinement.
- On first iteration, create full app.py and templates/*.html implementing all specified pages and features.
- On NEED_MODIFY feedback, apply all corrections and overwrite app.py and templates/*.html completely.
- On [APPROVED] feedback, preserve approved implementation.

**Implementation Requirements:**
- Implement Flask routes and view functions for all 9 pages: Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, Reviews.
- Use local text files in 'data' directory exactly as specified for Restaurants, Menus, Cart, Orders, Order Items, Deliveries, Reviews.
- Preserve all element IDs exactly as per design_spec.md in templates for correct navigation and UI interaction.
- Implement button actions, search/filter inputs, quantity updates, and page navigations as described.
- Ensure no authentication; all pages are publicly accessible.

**Data Persistence Requirements:**
- Read and write data files with correct parsing and formatting preserving exact field orders and types.
- Implement adding to cart, updating quantities, placing orders, tracking deliveries, and managing reviews with file modifications.
- Ensure data consistency between files and UI.

**Refinement Loop Instructions:**
- Use write_text_file tool to write final app.py and all templates/*.html.
- Run at most two iterations; stop immediately upon receiving [APPROVED] in code_feedback.md.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specialized in verifying Python Flask web applications with local file-based data management.

Your goal is to review the FoodDelivery app.py and HTML templates for syntax correctness, runtime behavior, and conformance to design_spec.md, producing gated feedback in code_feedback.md.

Task Details:
- Read design_spec.md describing required pages, elements, IDs, navigation, and data formats.
- Read the submitted app.py and all templates/*.html from CONTEXT.
- Do not assume undocumented features beyond design_spec.md.
- Validate that all specified element IDs exist exactly as documented.
- Check Flask routes and handlers are complete, consistent, and correctly linked to templates.
- Verify data file interactions correctly read and write expected fields and formats.
- Verify no syntax or runtime errors in app.py.
- On complete conformance, write feedback starting with [APPROVED].
- On any issues or incomplete features, write feedback starting with NEED_MODIFY and detailed corrections.

Review Checklist:
1. Complete implementation of all 9 pages with correct routes and templates.
2. Exact match of all element IDs in HTML templates.
3. Correct implementation of user actions (search, filters, add to cart, checkout).
4. Proper reading/writing of specified text data files per documented formats.
5. Syntax and runtime validation of app.py (use testing or code inspection).
6. Consistency and correctness of navigation flows and button actions.
7. No additional features or undocumented deviations from design_spec.md.

CRITICAL REQUIREMENTS:
- Begin written feedback file code_feedback.md with exactly [APPROVED] or NEED_MODIFY at byte 1.
- Use write_text_file tool to save the complete feedback for review.
- Conduct at most two review iterations; approve immediately if no issues.

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
        ("DesignCritic", """Verify design_spec.md fully addresses all features, page elements, element IDs, navigation scheme, and data storage requirements without missing or ambiguous details.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Verify app.py and templates/*.html fully implement design_spec.md web pages and features with correct element IDs and data file interactions, free of syntax or runtime errors.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
            "Create and iteratively revise a complete design_spec.md for the FoodDelivery web application.\n\n"
            "User requirements:\n"
            f"{CONTEXT.get('user_task_description', '')}\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== design_feedback.md ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review design_spec.md for completeness, clarity, and alignment with user requirements.\n"
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"User requirements:\n{CONTEXT.get('user_task_description', '')}\n\n"
            f"=== design_spec.md ===\n{current_design}"
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

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html for the FoodDelivery app.\n\n"
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
            "Review the latest app.py and templates against design_spec.md for the FoodDelivery application.\n"
            "Produce code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
