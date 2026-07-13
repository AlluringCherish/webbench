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
# 20260714_001749_566950/main_20260714_001749_566950.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend design specifications for the FoodDelivery web application and merge them into one consistent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect specifies Flask routes, data schema, and local text file data management; \"\n        \"FrontendDesignArchitect specifies HTML templates, element IDs, context variables, and navigation. \"\n        \"DesignMerger reconciles backend_design.md and frontend_design.md into a single design_spec.md delivering a consistent design aligned to the user task.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask backend development and local text file data management.\n\nYour goal is to design the Flask backend routes, define API endpoints, data handling logic, and data models for a Python-based web application using local text files.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently produce backend_design.md describing backend architecture\n- Specify Flask route URLs, HTTP methods, and relevant API endpoints\n- Define data models clearly tied to local text files with schema, formats, and example rows\n- Exclude frontend or template design details and do not read frontend_design.md\n\n**Section 1: Flask Routes and APIs**\n- List each route path and HTTP method handled by Flask\n- Include route purposes (e.g., Dashboard, Browse Restaurants, Cart management)\n- Specify expected input parameters, request methods, and response formats\n- Detail route interactions for adding/removing items, placing orders, and retrieving data\n\n**Section 2: Data Models and Local Text File Schemas**\n- Detail local data files (e.g., restaurants.txt, menus.txt) with exact field names, delimiters, types, and example entries\n- Define relationships between data files (e.g., menus linked to restaurants by restaurant_id)\n- Explain data handling logic to read, write, and update these files within Flask routes\n\n**Section 3: Backend Data Validation and Business Logic**\n- Specify constraints such as file-based data consistency, minimum orders, and availability flags\n- Outline how order status and delivery tracking will be managed in backend\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save output as backend_design.md\n- Produce a standalone and complete backend design artifact based solely on user_task_description\n- Format backend_design.md clearly with sections for routes, data models, and data handling logic\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a UX/UI Designer specializing in HTML and Jinja2 template architecture for web applications.\n\nYour goal is to design the frontend HTML templates, page structures, element IDs, context variables, and navigation flow for a Python web application.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create frontend_design.md documenting frontend interface design\n- Specify each HTML template with exact page titles and container IDs\n- List all UI elements with their element IDs, types (div, button, input, etc.), and purpose\n- Define context variables passed to templates and their expected data types/structures\n- Map all navigation links and button actions to the appropriate pages/routes\n- Exclude backend route or data model details and do not read backend_design.md\n\n**Section 1: HTML Template Specifications**\n- List templates corresponding to each page (Dashboard, Restaurants Listing, Cart, Checkout, etc.)\n- Provide page titles and main container element IDs for each template\n- Specify required UI controls and their IDs for user interactions (search, filter, add to cart)\n\n**Section 2: Context Variables and Data Binding**\n- Define each context variable name, type, and structure feeding dynamic page content\n- Include sample data examples for list variables (e.g., featured restaurants, cart items)\n- Describe how data should populate template elements and controls\n\n**Section 3: Navigation and User Flow**\n- Specify button and link element IDs used for navigation\n- Map navigation actions clearly to expected routes or pages\n- Include details for back-navigation and filtering controls\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save output as frontend_design.md\n- Create a self-contained frontend design spec solely based on user_task_description\n- Format frontend_design.md clearly with templates, element IDs, context variables, and navigation map\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Systems Integrator specializing in merging backend and frontend design specifications into a coherent web application contract.\n\nYour goal is to integrate backend_design.md and frontend_design.md into one consistent design_spec.md that aligns precisely with the FoodDelivery user task requirements.\n\nTask Details:\n- Read backend_design.md, frontend_design.md, and user_task_description from CONTEXT\n- Combine backend routes, data models and frontend templates, element IDs, context variables, and navigation into unified specification\n- Resolve inconsistencies between backend routes and frontend navigation (matching route names, parameters)\n- Ensure data model fields are consistently referenced in frontend context variables and backend data handling\n- Preserve all required detail from both designs without inventing new requirements or removing existing ones\n\n**Section 1: Integrated Flask Routes and APIs**\n- Consolidate all backend routes with their methods, purposes, and expected inputs\n- Confirm these routes support all frontend navigation and data needs\n\n**Section 2: Unified Data Model and Local Text Files Schema**\n- Merge data schemas from backend_design.md into a canonical form\n- Ensure alignment with frontend context variables and UI elements\n\n**Section 3: Combined Frontend Template and Navigation Specifications**\n- Include all HTML templates with their titles, container element IDs, and critical UI components\n- Present agreed context variables and their formats used to populate templates\n- Map navigation flows explicitly to backend routes\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save output as design_spec.md\n- Produce a final comprehensive specification usable by backend and frontend developers\n- Include all sections with no contradictions or missing elements\n- Do not add or omit requirements beyond input artifacts\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend design completeness, consistency with user requirements, and accuracy of route and data model definitions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design alignment with user requirements, correct element IDs, page navigation, and template structure.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend and frontend artifacts in parallel from design_spec.md and merge them to produce final app.py and templates with verified interface consistency\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py based on the design_spec.md backend contract; \"\n        \"FrontendDeveloper implements all HTML templates with exact element IDs and navigation from design_spec.md frontend contract; \"\n        \"IntegrationMerger reconciles app.py and templates/*.html with design_spec.md, ensuring full interface consistency and correctness.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Python backend developer specializing in Flask web applications with local text file data management.\n\nYour goal is to implement the complete Flask backend application that supports all routes, business logic, and data operations specified in the design_spec.md artifact.\n\nTask Details:\n- Read design_spec.md from CONTEXT to extract backend route specifications, data schemas, and required logic\n- Independently implement app.py including route handlers, data file I/O, and business rules from design_spec.md backend contract\n- Create the backend Flask application using local text files for data persistence matching the specified formats and examples\n- Write a complete, runnable app.py with all backend endpoints aligned with the design_spec.md inputs\n\n**Implementation Requirements:**\n- Implement Flask routes with correct HTTP methods, endpoints, and route functions as per design_spec.md\n- Perform all file reading/writing on local text files under 'data' directory, strictly using defined text schemas\n- Include all functionality to support browsing, ordering, cart management, checkout, tracking, and reviews\n- Use appropriate Flask app structure, imports, and route decorators; ensure modular and readable code\n\n**Data Handling Specifications:**\n- Parse and write files like restaurants.txt, menus.txt, cart.txt, orders.txt, order_items.txt, deliveries.txt, and reviews.txt using the exact delimiter and field orders\n- Implement business logic such as search, filter, order creation, delivery tracking, and review handling using these data files\n\nCRITICAL SUCCESS CRITERIA:\n- The backend app.py must fully implement the backend contract in design_spec.md without omissions or extraneous features\n- Use write_text_file tool exclusively to output app.py\n- Do not read or depend on frontend templates or sibling agent outputs\n- Write only the declared output artifact: app.py\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a frontend developer skilled in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement all user interface HTML templates with precise element IDs, navigation, and visual components as defined in the design_spec.md artifact.\n\nTask Details:\n- Read design_spec.md from CONTEXT to identify all required HTML templates, element IDs, page titles, and navigation flows\n- Independently implement the full set of templates/*.html files with exact structure and IDs specified in design_spec.md frontend contract\n- Templates must support functionality across all nine FoodDelivery pages including dashboard, restaurant listing, menus, item details, cart, checkout, orders, tracking, and reviews\n\n**Template Implementation Requirements:**\n- Create each HTML file named and structured as per design_spec.md specifications with all defined divs, buttons, inputs, dropdowns, and tables\n- Assign element IDs precisely as listed; ensure correct placement, nesting, and type for each element\n- Implement navigation elements such as buttons and links to match specified flows and functions\n- Use Jinja2 syntax where dynamic content and loops are described in design_spec.md\n- Ensure the UI is consistent, usable, and handles all frontend requirements without backend logic\n\nCRITICAL SUCCESS CRITERIA:\n- Frontend templates must exactly match element IDs, page structure, and navigation states stated in design_spec.md\n- Use write_text_file tool exclusively to output all templates under templates/*.html\n- Do not read or depend on backend code or sibling agent outputs\n- Write only the declared output artifact: templates/*.html\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a software integration specialist focused on merging Flask backend and frontend template implementations for consistent web applications.\n\nYour goal is to reconcile and merge the implementations of app.py and templates/*.html with the design_spec.md contract, ensuring full interface consistency, correctness, and compliance without adding new features.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify that all Flask routes and data handling in app.py match design_spec.md backend specifications\n- Verify that all HTML templates, element IDs, and navigation in templates/*.html match design_spec.md frontend specifications\n- Identify and correct any interface mismatches between backend routes and frontend links, form actions, and template context variables\n- Produce a consistent, corrected, and cleaned app.py and templates/*.html artifact set aligned fully with design_spec.md\n\n**Verification & Correction Guidelines:**\n- Check every route in app.py against design_spec.md for existence, HTTP method, and expected behavior\n- Confirm each template element ID, structure, and navigation target matches design_spec.md definitions\n- Ensure no missing or extraneous endpoints, templates, or navigation elements\n- Fix interface inconsistencies such as mismatched route URLs, missing handlers, or template IDs without backend support\n- Maintain original feature scope; do not invent additional features or requirements\n\nCRITICAL SUCCESS CRITERIA:\n- Final app.py and templates/*.html fully conform to design_spec.md contract and are mutually consistent\n- Use write_text_file tool exclusively to output the corrected app.py and templates/*.html\n- Ensure no added features or modifications outside reconciliation scope\n- Write only the declared output artifacts: app.py, templates/*.html\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check that app.py fully implements the backend routes, data handling, and logic per design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify that all frontend templates meet the design_spec.md element ID, navigation flow, and UI specifications.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a Software Architect specializing in Flask backend development and local text file data management.

Your goal is to design the Flask backend routes, define API endpoints, data handling logic, and data models for a Python-based web application using local text files.

Task Details:
- Read user_task_description from CONTEXT
- Independently produce backend_design.md describing backend architecture
- Specify Flask route URLs, HTTP methods, and relevant API endpoints
- Define data models clearly tied to local text files with schema, formats, and example rows
- Exclude frontend or template design details and do not read frontend_design.md

**Section 1: Flask Routes and APIs**
- List each route path and HTTP method handled by Flask
- Include route purposes (e.g., Dashboard, Browse Restaurants, Cart management)
- Specify expected input parameters, request methods, and response formats
- Detail route interactions for adding/removing items, placing orders, and retrieving data

**Section 2: Data Models and Local Text File Schemas**
- Detail local data files (e.g., restaurants.txt, menus.txt) with exact field names, delimiters, types, and example entries
- Define relationships between data files (e.g., menus linked to restaurants by restaurant_id)
- Explain data handling logic to read, write, and update these files within Flask routes

**Section 3: Backend Data Validation and Business Logic**
- Specify constraints such as file-based data consistency, minimum orders, and availability flags
- Outline how order status and delivery tracking will be managed in backend

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save output as backend_design.md
- Produce a standalone and complete backend design artifact based solely on user_task_description
- Format backend_design.md clearly with sections for routes, data models, and data handling logic

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a UX/UI Designer specializing in HTML and Jinja2 template architecture for web applications.

Your goal is to design the frontend HTML templates, page structures, element IDs, context variables, and navigation flow for a Python web application.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md documenting frontend interface design
- Specify each HTML template with exact page titles and container IDs
- List all UI elements with their element IDs, types (div, button, input, etc.), and purpose
- Define context variables passed to templates and their expected data types/structures
- Map all navigation links and button actions to the appropriate pages/routes
- Exclude backend route or data model details and do not read backend_design.md

**Section 1: HTML Template Specifications**
- List templates corresponding to each page (Dashboard, Restaurants Listing, Cart, Checkout, etc.)
- Provide page titles and main container element IDs for each template
- Specify required UI controls and their IDs for user interactions (search, filter, add to cart)

**Section 2: Context Variables and Data Binding**
- Define each context variable name, type, and structure feeding dynamic page content
- Include sample data examples for list variables (e.g., featured restaurants, cart items)
- Describe how data should populate template elements and controls

**Section 3: Navigation and User Flow**
- Specify button and link element IDs used for navigation
- Map navigation actions clearly to expected routes or pages
- Include details for back-navigation and filtering controls

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save output as frontend_design.md
- Create a self-contained frontend design spec solely based on user_task_description
- Format frontend_design.md clearly with templates, element IDs, context variables, and navigation map

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Systems Integrator specializing in merging backend and frontend design specifications into a coherent web application contract.

Your goal is to integrate backend_design.md and frontend_design.md into one consistent design_spec.md that aligns precisely with the FoodDelivery user task requirements.

Task Details:
- Read backend_design.md, frontend_design.md, and user_task_description from CONTEXT
- Combine backend routes, data models and frontend templates, element IDs, context variables, and navigation into unified specification
- Resolve inconsistencies between backend routes and frontend navigation (matching route names, parameters)
- Ensure data model fields are consistently referenced in frontend context variables and backend data handling
- Preserve all required detail from both designs without inventing new requirements or removing existing ones

**Section 1: Integrated Flask Routes and APIs**
- Consolidate all backend routes with their methods, purposes, and expected inputs
- Confirm these routes support all frontend navigation and data needs

**Section 2: Unified Data Model and Local Text Files Schema**
- Merge data schemas from backend_design.md into a canonical form
- Ensure alignment with frontend context variables and UI elements

**Section 3: Combined Frontend Template and Navigation Specifications**
- Include all HTML templates with their titles, container element IDs, and critical UI components
- Present agreed context variables and their formats used to populate templates
- Map navigation flows explicitly to backend routes

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save output as design_spec.md
- Produce a final comprehensive specification usable by backend and frontend developers
- Include all sections with no contradictions or missing elements
- Do not add or omit requirements beyond input artifacts

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Python backend developer specializing in Flask web applications with local text file data management.

Your goal is to implement the complete Flask backend application that supports all routes, business logic, and data operations specified in the design_spec.md artifact.

Task Details:
- Read design_spec.md from CONTEXT to extract backend route specifications, data schemas, and required logic
- Independently implement app.py including route handlers, data file I/O, and business rules from design_spec.md backend contract
- Create the backend Flask application using local text files for data persistence matching the specified formats and examples
- Write a complete, runnable app.py with all backend endpoints aligned with the design_spec.md inputs

**Implementation Requirements:**
- Implement Flask routes with correct HTTP methods, endpoints, and route functions as per design_spec.md
- Perform all file reading/writing on local text files under 'data' directory, strictly using defined text schemas
- Include all functionality to support browsing, ordering, cart management, checkout, tracking, and reviews
- Use appropriate Flask app structure, imports, and route decorators; ensure modular and readable code

**Data Handling Specifications:**
- Parse and write files like restaurants.txt, menus.txt, cart.txt, orders.txt, order_items.txt, deliveries.txt, and reviews.txt using the exact delimiter and field orders
- Implement business logic such as search, filter, order creation, delivery tracking, and review handling using these data files

CRITICAL SUCCESS CRITERIA:
- The backend app.py must fully implement the backend contract in design_spec.md without omissions or extraneous features
- Use write_text_file tool exclusively to output app.py
- Do not read or depend on frontend templates or sibling agent outputs
- Write only the declared output artifact: app.py

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a frontend developer skilled in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement all user interface HTML templates with precise element IDs, navigation, and visual components as defined in the design_spec.md artifact.

Task Details:
- Read design_spec.md from CONTEXT to identify all required HTML templates, element IDs, page titles, and navigation flows
- Independently implement the full set of templates/*.html files with exact structure and IDs specified in design_spec.md frontend contract
- Templates must support functionality across all nine FoodDelivery pages including dashboard, restaurant listing, menus, item details, cart, checkout, orders, tracking, and reviews

**Template Implementation Requirements:**
- Create each HTML file named and structured as per design_spec.md specifications with all defined divs, buttons, inputs, dropdowns, and tables
- Assign element IDs precisely as listed; ensure correct placement, nesting, and type for each element
- Implement navigation elements such as buttons and links to match specified flows and functions
- Use Jinja2 syntax where dynamic content and loops are described in design_spec.md
- Ensure the UI is consistent, usable, and handles all frontend requirements without backend logic

CRITICAL SUCCESS CRITERIA:
- Frontend templates must exactly match element IDs, page structure, and navigation states stated in design_spec.md
- Use write_text_file tool exclusively to output all templates under templates/*.html
- Do not read or depend on backend code or sibling agent outputs
- Write only the declared output artifact: templates/*.html

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a software integration specialist focused on merging Flask backend and frontend template implementations for consistent web applications.

Your goal is to reconcile and merge the implementations of app.py and templates/*.html with the design_spec.md contract, ensuring full interface consistency, correctness, and compliance without adding new features.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify that all Flask routes and data handling in app.py match design_spec.md backend specifications
- Verify that all HTML templates, element IDs, and navigation in templates/*.html match design_spec.md frontend specifications
- Identify and correct any interface mismatches between backend routes and frontend links, form actions, and template context variables
- Produce a consistent, corrected, and cleaned app.py and templates/*.html artifact set aligned fully with design_spec.md

**Verification & Correction Guidelines:**
- Check every route in app.py against design_spec.md for existence, HTTP method, and expected behavior
- Confirm each template element ID, structure, and navigation target matches design_spec.md definitions
- Ensure no missing or extraneous endpoints, templates, or navigation elements
- Fix interface inconsistencies such as mismatched route URLs, missing handlers, or template IDs without backend support
- Maintain original feature scope; do not invent additional features or requirements

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html fully conform to design_spec.md contract and are mutually consistent
- Use write_text_file tool exclusively to output the corrected app.py and templates/*.html
- Ensure no added features or modifications outside reconciliation scope
- Write only the declared output artifacts: app.py, templates/*.html

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
        ("DesignMerger", """Verify backend design completeness, consistency with user requirements, and accuracy of route and data model definitions.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design alignment with user requirements, correct element IDs, page navigation, and template structure.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check that app.py fully implements the backend routes, data handling, and logic per design_spec.md.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify that all frontend templates meet the design_spec.md element ID, navigation flow, and UI specifications.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Design backend architecture and save backend_design.md based on user_task_description."),
        execute(FrontendDesignArchitect, "Design frontend templates and save frontend_design.md based on user_task_description.")
    )

    # Read backend_design.md and frontend_design.md for merger
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

    # Execute DesignMerger to consolidate backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"=== Backend Design ===\n{backend_design_content}\n\n=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
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
        timeout_threshold=350,
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement app.py based on design_spec.md backend contract. Ensure all routes, data schemas, and business logic are supported. Use local text files for data persistence."),
        execute(FrontendDeveloper,
                "Implement all HTML templates (*.html) based on design_spec.md frontend contract with exact element IDs, page structure, and navigation flows across all FoodDelivery pages.")
    )

    # Read backend and frontend outputs for merger
    app_py_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass

    templates_content = ""
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Execute IntegrationMerger to verify and reconcile app.py and templates with design_spec.md
    await execute(IntegrationMerger,
                  f"Verify and reconcile the backend app.py and frontend templates/*.html with design_spec.md.\n\n"
                  f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== Templates ===\n{templates_content}")
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
