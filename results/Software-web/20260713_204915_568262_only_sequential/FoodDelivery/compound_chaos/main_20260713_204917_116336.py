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
# 20260713_204917_116336/main_20260713_204917_116336.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the FoodDelivery requirements and produce a detailed design_spec.md covering all pages, routes, elements, data files, and interactions.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md with detailed page routes, titles, element IDs, and core user flows; \"\n        \"only after that WebArchitect reads this and produces design_spec.md documenting Flask route methods, template names, data file usage, and UI contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in gathering and documenting detailed web application requirements.\n\nYour goal is to extract and trace every requested route, page title, exact element IDs, interaction flows, and data dependencies from the user requirements into a comprehensive requirements_analysis.md file.\n\nTask Details:\n- Examine user_task_description to identify ALL application pages, routes, page titles, and exact element IDs described\n- Document the interaction and navigation flows among pages\n- Trace all UI elements that are interactive (buttons, inputs, dropdowns) including dynamic IDs with patterns\n- Identify data files referenced and their usage contexts from the requirements\n- Produce requirements_analysis.md capturing this detailed inventory to enable architectural design\n\nRequirements Analysis Instructions:\n1. **Page Routes and Titles**:\n   - List all pages with their corresponding routes and exact page titles\n2. **UI Element IDs**:\n   - For each page, list all element IDs exactly as specified\n   - Include element type and role (e.g., Button, Input, Div)\n   - Highlight dynamic element IDs with placeholders, e.g. view-restaurant-button-{restaurant_id}\n3. **User Interaction Flows**:\n   - Describe typical navigation paths triggered by buttons\n   - Specify how pages relate (e.g., dashboard → restaurants page → menu page)\n4. **Data File References**:\n   - Identify which pages read/write each data file\n   - Briefly describe how data files are used in the UI context\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as requirements_analysis.md\n- Ensure complete and exact capture of all details from user_task_description\n- Use clear markdown formatting and structure for readability\n- Do not start architecture or design speculation; focus purely on requirement extraction\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in designing Flask web application architecture and UI contracts.\n\nYour goal is to transform requirements_analysis.md into a detailed design_spec.md that defines Flask routes, HTTP methods, template file names, page titles, element IDs, buttons, inputs, data file formats, navigation flows, and interaction contracts.\n\nTask Details:\n- Read requirements_analysis.md thoroughly to understand all page routes, element IDs, and navigation flows\n- Consult user_task_description as needed for confirmation of data file formats and examples\n- Produce design_spec.md specifying:\n  - Exact Flask route paths and HTTP methods for each page\n  - Template filenames under templates/ directory for corresponding pages\n  - All static and dynamic element IDs per page with descriptions\n  - List of all buttons, inputs with their names and expected behaviors\n  - Data file access contracts: filenames, field orders, and usage contexts for backend implementation\n  - Navigation flow mapping including route redirects and button actions\n\nDesign Specification Instructions:\n1. **Flask Routes and Methods**:\n   - Define route path (e.g., /dashboard), HTTP method (GET/POST), and function name for each page\n2. **Template Files**:\n   - Specify template file names (e.g., dashboard.html) corresponding to routes\n3. **UI Element Specifications**:\n   - Include all element IDs as listed, indicating type (Div, Button, Input) and dynamic placeholders\n4. **Data Files Usage**:\n   - Document the data files read/write operations with exact field formats from user_task_description\n5. **Navigation and Interaction**:\n   - Specify navigation triggered by buttons (e.g., browse-restaurants-button → /restaurants)\n   - Define expected form submissions or data updates for POST routes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_spec.md\n- Ensure all route function names are descriptive and consistent\n- Follow exact naming and formatting for files, routes, and variables per requirements_analysis.md\n- Do not include implementation code; provide design and specification only\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify that requirements_analysis.md precisely lists all page routes, titles, UI element IDs per page, \"\n                \"and captures all interactive UI elements and data file references to ensure clarity before architecture drafting.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement a complete Flask application with app.py and templates/*.html following design_spec.md, supporting all pages, UI elements, and local text file data access.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes app_draft.py and all templates_draft/*.html files from design_spec.md; only after both complete, \"\n        \"IntegrationEngineer produces final app.py and templates/*.html closing all gaps and enforcing web-compatible routes, element IDs, and data interactions.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to write a complete draft Flask application and draft HTML templates that implement all features, pages, and UI components as specified.\n\nTask Details:\n- Read design_spec.md and user_task_description fully\n- Create app_draft.py with all Flask routes covering every page and functionality\n- Implement data access from local text files exactly as specified\n- Draft templates_draft/*.html with all required element IDs and UI components from the design\n- Focus on completeness of draft implementation for review and integration\n\nImplementation Requirements:\n1. **Flask App Draft**:\n   - Define Flask routes for all specified pages with correct URL paths\n   - Use render_template to render drafts located in templates_draft/\n   - Access and parse all required local text files for data loading\n   - Handle data in appropriate structures matching design specs\n   - Use basic error handling for file I/O issues\n\n2. **Templates Draft**:\n   - Draft HTML templates for all pages with correct element IDs as required\n   - Use consistent Jinja2 syntax for context variables and loops\n   - Include UI elements fully representing user interactions (buttons, inputs, filters)\n\n3. **Draft Scope**:\n   - No final polishing, focus on correctness and coverage\n   - Use templates_draft/ folder for all HTML drafts\n   - Ensure all UI elements specified in user_task_description appear with correct IDs\n   - Output complete working draft code and templates\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and templates_draft/*.html\n- Ensure all Flask routes match design_spec.md specifications exactly\n- All UI element IDs must match user_task_description precisely\n- Data file reading must follow specified data formats and field order\n- Focus on draft completeness; no final cleanup required\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web application integration.\n\nYour goal is to integrate draft backend code and draft templates into a final runnable Flask app and polished templates fully aligned with specifications.\n\nTask Details:\n- Read app_draft.py, templates_draft/*.html, design_spec.md, and user_task_description\n- Refine and consolidate draft code into final app.py with robust route handling\n- Move and finalize templates into templates/ directory with exact element IDs\n- Ensure render_template calls reference correct final template paths\n- Implement robust data file handling exactly as specified for all files\n- Fix any inconsistencies, gaps, or errors found in draft artifacts\n\nIntegration Requirements:\n1. **Final Flask App**:\n   - Implement all routes with precise URL paths and function names per design_spec.md\n   - Use render_template for templates/*.html only (no drafts)\n   - Include error handling and input validation as appropriate\n   - Maintain readability and maintainability of code\n\n2. **Final Templates**:\n   - Use all element IDs exactly as specified\n   - Ensure templates provide complete, consistent UI across all pages\n   - Use final templates/ directory for all HTML files\n\n3. **Data Handling**:\n   - Parse local text files exactly with required field order and types\n   - Ensure data structures passed to templates conform to specifications\n   - Handle absent or malformed data gracefully\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html\n- Output must be runnable Flask application matching design_spec.md precisely\n- UI element IDs in templates must be exact matches to specifications\n- Data file access must follow exact format and field order\n- Address all review comments and gaps from DraftEngineer outputs\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Verify that app_draft.py and templates_draft/*.html fully implement design_spec.md routes and UI, \"\n                \"with correct Flask route decorators, template rendering, and local file data interactions before final integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate and test app.py with templates/*.html for Flask compliance, syntax, route coverage, element correctness, and produce the final corrected app.py and templates.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator performs comprehensive validation of app.py and templates/*.html generating validation_report.md; \"\n        \"SequentialFixer reads this report and applies corrections producing final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web applications and frontend template validation.\n\nYour goal is to comprehensively validate the Flask backend app.py and all frontend templates/*.html, ensuring compliance with Flask conventions, syntax correctness, route coverage, and correctness of HTML element IDs and data bindings; produce a detailed validation_report.md.\n\nTask Details:\n- Read app.py, templates/*.html, design_spec.md, and user_task_description artifacts from context\n- Validate Python syntax and runtime instantiation of Flask app in app.py\n- Verify all Flask routes defined in design_spec.md are accessible and return appropriate responses\n- Check all templates/*.html for presence and correctness of requested element IDs as specified in design_spec.md\n- Verify data bindings in templates correspond with context variables defined in backend routes\n- Generate a precise and reproducible validation_report.md detailing all findings, errors, omissions, and successes\n\nValidation Procedures:\n1. **Python Syntax and Runtime Checks**\n   - Use validate_python_file tool on app.py to confirm syntax and runtime compliance\n2. **Flask Route Coverage Testing**\n   - Programmatically access all routes defined in design_spec.md to confirm availability and correct HTTP methods\n3. **Template Element Verification**\n   - Parse each template file for presence of all element IDs specified for each page in design_spec.md\n   - Confirm elements have correct structure and expected data bindings (Jinja2 variables)\n4. **Report Compilation**\n   - Summarize all detected issues: syntax errors, missing routes, incorrect element IDs, mismatched data bindings\n   - Provide actionable feedback with exact file locations and line references where possible\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools for code validation and route testing\n- MUST use write_text_file tool to output comprehensive validation_report.md\n- Report must be clear, concise, and guide corrections effectively without ambiguity\n- Focus exclusively on input artifacts: app.py, templates/*.html, design_spec.md, user_task_description\n- No assumptions beyond provided artifacts or user task details\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application maintenance and frontend template correction.\n\nYour goal is to apply all actionable corrections described in validation_report.md to app.py and templates/*.html, producing final versions fully compliant with the user requirements and design specifications.\n\nTask Details:\n- Read validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description artifacts from context\n- Analyze the validation report carefully to identify all required fixes and improvements\n- Correct app.py code to resolve syntax errors, fix route issues, and ensure backend logic matches design_spec.md\n- Edit templates/*.html files to add missing element IDs, fix structure or data bindings, and align with design_spec.md\n- Produce final fully validated app.py and templates/*.html files ready for deployment\n\nCorrection Guidelines:\n1. **Backend Code Updates**\n   - Follow design_spec.md strictly to correct routes, context variables, and data handling as per report findings\n2. **Frontend Template Updates**\n   - Add or fix all required HTML element IDs exactly as specified\n   - Correct or add Jinja2 variable bindings for context data consistency\n3. **Verification and Format**\n   - Ensure fixed files maintain original formatting standards and run without syntax errors\n   - Do NOT introduce features or changes not described in validation_report.md or design_spec.md\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save corrected app.py and all templates/*.html files\n- Corrections must fully address validation_report.md findings to ensure compliance\n- Output files must match input file naming exactly\n- Maintain positive focus on compliance with requirements and design_spec.md\n- Do NOT include the validation report text or status markers in output files\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Ensure validation_report.md contains precise, reproducible findings covering Flask route coverage, template element ID correctness, \"\n                \"and runtime errors to guide correction effectively.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify the final app.py and templates/*.html fully realize the user requirements as documented in requirements_analysis.md and design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in gathering and documenting detailed web application requirements.

Your goal is to extract and trace every requested route, page title, exact element IDs, interaction flows, and data dependencies from the user requirements into a comprehensive requirements_analysis.md file.

Task Details:
- Examine user_task_description to identify ALL application pages, routes, page titles, and exact element IDs described
- Document the interaction and navigation flows among pages
- Trace all UI elements that are interactive (buttons, inputs, dropdowns) including dynamic IDs with patterns
- Identify data files referenced and their usage contexts from the requirements
- Produce requirements_analysis.md capturing this detailed inventory to enable architectural design

Requirements Analysis Instructions:
1. **Page Routes and Titles**:
   - List all pages with their corresponding routes and exact page titles
2. **UI Element IDs**:
   - For each page, list all element IDs exactly as specified
   - Include element type and role (e.g., Button, Input, Div)
   - Highlight dynamic element IDs with placeholders, e.g. view-restaurant-button-{restaurant_id}
3. **User Interaction Flows**:
   - Describe typical navigation paths triggered by buttons
   - Specify how pages relate (e.g., dashboard → restaurants page → menu page)
4. **Data File References**:
   - Identify which pages read/write each data file
   - Briefly describe how data files are used in the UI context

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as requirements_analysis.md
- Ensure complete and exact capture of all details from user_task_description
- Use clear markdown formatting and structure for readability
- Do not start architecture or design speculation; focus purely on requirement extraction

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in designing Flask web application architecture and UI contracts.

Your goal is to transform requirements_analysis.md into a detailed design_spec.md that defines Flask routes, HTTP methods, template file names, page titles, element IDs, buttons, inputs, data file formats, navigation flows, and interaction contracts.

Task Details:
- Read requirements_analysis.md thoroughly to understand all page routes, element IDs, and navigation flows
- Consult user_task_description as needed for confirmation of data file formats and examples
- Produce design_spec.md specifying:
  - Exact Flask route paths and HTTP methods for each page
  - Template filenames under templates/ directory for corresponding pages
  - All static and dynamic element IDs per page with descriptions
  - List of all buttons, inputs with their names and expected behaviors
  - Data file access contracts: filenames, field orders, and usage contexts for backend implementation
  - Navigation flow mapping including route redirects and button actions

Design Specification Instructions:
1. **Flask Routes and Methods**:
   - Define route path (e.g., /dashboard), HTTP method (GET/POST), and function name for each page
2. **Template Files**:
   - Specify template file names (e.g., dashboard.html) corresponding to routes
3. **UI Element Specifications**:
   - Include all element IDs as listed, indicating type (Div, Button, Input) and dynamic placeholders
4. **Data Files Usage**:
   - Document the data files read/write operations with exact field formats from user_task_description
5. **Navigation and Interaction**:
   - Specify navigation triggered by buttons (e.g., browse-restaurants-button → /restaurants)
   - Define expected form submissions or data updates for POST routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_spec.md
- Ensure all route function names are descriptive and consistent
- Follow exact naming and formatting for files, routes, and variables per requirements_analysis.md
- Do not include implementation code; provide design and specification only

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to write a complete draft Flask application and draft HTML templates that implement all features, pages, and UI components as specified.

Task Details:
- Read design_spec.md and user_task_description fully
- Create app_draft.py with all Flask routes covering every page and functionality
- Implement data access from local text files exactly as specified
- Draft templates_draft/*.html with all required element IDs and UI components from the design
- Focus on completeness of draft implementation for review and integration

Implementation Requirements:
1. **Flask App Draft**:
   - Define Flask routes for all specified pages with correct URL paths
   - Use render_template to render drafts located in templates_draft/
   - Access and parse all required local text files for data loading
   - Handle data in appropriate structures matching design specs
   - Use basic error handling for file I/O issues

2. **Templates Draft**:
   - Draft HTML templates for all pages with correct element IDs as required
   - Use consistent Jinja2 syntax for context variables and loops
   - Include UI elements fully representing user interactions (buttons, inputs, filters)

3. **Draft Scope**:
   - No final polishing, focus on correctness and coverage
   - Use templates_draft/ folder for all HTML drafts
   - Ensure all UI elements specified in user_task_description appear with correct IDs
   - Output complete working draft code and templates

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and templates_draft/*.html
- Ensure all Flask routes match design_spec.md specifications exactly
- All UI element IDs must match user_task_description precisely
- Data file reading must follow specified data formats and field order
- Focus on draft completeness; no final cleanup required

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web application integration.

Your goal is to integrate draft backend code and draft templates into a final runnable Flask app and polished templates fully aligned with specifications.

Task Details:
- Read app_draft.py, templates_draft/*.html, design_spec.md, and user_task_description
- Refine and consolidate draft code into final app.py with robust route handling
- Move and finalize templates into templates/ directory with exact element IDs
- Ensure render_template calls reference correct final template paths
- Implement robust data file handling exactly as specified for all files
- Fix any inconsistencies, gaps, or errors found in draft artifacts

Integration Requirements:
1. **Final Flask App**:
   - Implement all routes with precise URL paths and function names per design_spec.md
   - Use render_template for templates/*.html only (no drafts)
   - Include error handling and input validation as appropriate
   - Maintain readability and maintainability of code

2. **Final Templates**:
   - Use all element IDs exactly as specified
   - Ensure templates provide complete, consistent UI across all pages
   - Use final templates/ directory for all HTML files

3. **Data Handling**:
   - Parse local text files exactly with required field order and types
   - Ensure data structures passed to templates conform to specifications
   - Handle absent or malformed data gracefully

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html
- Output must be runnable Flask application matching design_spec.md precisely
- UI element IDs in templates must be exact matches to specifications
- Data file access must follow exact format and field order
- Address all review comments and gaps from DraftEngineer outputs

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web applications and frontend template validation.

Your goal is to comprehensively validate the Flask backend app.py and all frontend templates/*.html, ensuring compliance with Flask conventions, syntax correctness, route coverage, and correctness of HTML element IDs and data bindings; produce a detailed validation_report.md.

Task Details:
- Read app.py, templates/*.html, design_spec.md, and user_task_description artifacts from context
- Validate Python syntax and runtime instantiation of Flask app in app.py
- Verify all Flask routes defined in design_spec.md are accessible and return appropriate responses
- Check all templates/*.html for presence and correctness of requested element IDs as specified in design_spec.md
- Verify data bindings in templates correspond with context variables defined in backend routes
- Generate a precise and reproducible validation_report.md detailing all findings, errors, omissions, and successes

Validation Procedures:
1. **Python Syntax and Runtime Checks**
   - Use validate_python_file tool on app.py to confirm syntax and runtime compliance
2. **Flask Route Coverage Testing**
   - Programmatically access all routes defined in design_spec.md to confirm availability and correct HTTP methods
3. **Template Element Verification**
   - Parse each template file for presence of all element IDs specified for each page in design_spec.md
   - Confirm elements have correct structure and expected data bindings (Jinja2 variables)
4. **Report Compilation**
   - Summarize all detected issues: syntax errors, missing routes, incorrect element IDs, mismatched data bindings
   - Provide actionable feedback with exact file locations and line references where possible

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for code validation and route testing
- MUST use write_text_file tool to output comprehensive validation_report.md
- Report must be clear, concise, and guide corrections effectively without ambiguity
- Focus exclusively on input artifacts: app.py, templates/*.html, design_spec.md, user_task_description
- No assumptions beyond provided artifacts or user task details

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application maintenance and frontend template correction.

Your goal is to apply all actionable corrections described in validation_report.md to app.py and templates/*.html, producing final versions fully compliant with the user requirements and design specifications.

Task Details:
- Read validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description artifacts from context
- Analyze the validation report carefully to identify all required fixes and improvements
- Correct app.py code to resolve syntax errors, fix route issues, and ensure backend logic matches design_spec.md
- Edit templates/*.html files to add missing element IDs, fix structure or data bindings, and align with design_spec.md
- Produce final fully validated app.py and templates/*.html files ready for deployment

Correction Guidelines:
1. **Backend Code Updates**
   - Follow design_spec.md strictly to correct routes, context variables, and data handling as per report findings
2. **Frontend Template Updates**
   - Add or fix all required HTML element IDs exactly as specified
   - Correct or add Jinja2 variable bindings for context data consistency
3. **Verification and Format**
   - Ensure fixed files maintain original formatting standards and run without syntax errors
   - Do NOT introduce features or changes not described in validation_report.md or design_spec.md

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save corrected app.py and all templates/*.html files
- Corrections must fully address validation_report.md findings to ensure compliance
- Output files must match input file naming exactly
- Maintain positive focus on compliance with requirements and design_spec.md
- Do NOT include the validation report text or status markers in output files

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify that requirements_analysis.md precisely lists all page routes, titles, UI element IDs per page, "
                "and captures all interactive UI elements and data file references to ensure clarity before architecture drafting.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Verify that app_draft.py and templates_draft/*.html fully implement design_spec.md routes and UI, "
                "with correct Flask route decorators, template rendering, and local file data interactions before final integration.""", [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Ensure validation_report.md contains precise, reproducible findings covering Flask route coverage, template element ID correctness, "
                "and runtime errors to guide correction effectively.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify the final app.py and templates/*.html fully realize the user requirements as documented in requirements_analysis.md and design_spec.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution according to Sequential Flow pattern
    await execute(RequirementsAnalyst,
                  "Extract all pages, routes, page titles, element IDs, interaction flows, and data file references "
                  "from user_task_description. Save detailed requirements_analysis.md.")
    # Read requirements_analysis.md content to inject in next agent
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except Exception:
        requirements_analysis_content = ""

    # Pass requirements_analysis.md and user_task_description to WebArchitect
    user_task_description = ""
    entries = CONTEXT.get("user_task_description", [])
    if entries:
        user_task_description = entries[-1]["content"]

    await execute(WebArchitect,
                  f"Read requirements_analysis.md and user_task_description.\n"
                  f"Produce detailed design_spec.md defining Flask routes, HTTP methods, templates, element IDs, buttons, inputs, "
                  f"data file formats, and navigation flows.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}\n\n"
                  f"=== user_task_description ===\n{user_task_description}")
# Phase1_End

# Phase2_Start

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
        recovery_time=45
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
        recovery_time=45
    )

    # Sequential execution
    # Step 1: DraftEngineer writes app_draft.py and templates_draft/*.html
    await execute(DraftEngineer,
                  "Read design_spec.md and user_task_description. "
                  "Write a complete draft Flask app (app_draft.py) covering all pages and UI elements, "
                  "reading local text files as specified. "
                  "Create draft HTML templates in templates_draft/ with all required element IDs and UI components.")
    
    # Read drafts for injection
    app_draft_code, templates_draft = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    try:
        # Since templates_draft/*.html can be multiple files, read all files in templates_draft/ folder content if available
        import glob
        paths = glob.glob("templates_draft/*.html")
        contents = []
        for p in paths:
            try:
                contents.append(f"=== {p} ===\n" + open(p).read())
            except:
                pass
        templates_draft = "\n\n".join(contents)
    except:
        pass

    # Step 2: IntegrationEngineer creates final app.py and templates/*.html using drafts
    await execute(IntegrationEngineer,
                  f"Refine and integrate drafts into final app.py and templates/*.html. "
                  f"Use app_draft.py and all templates_draft/*.html content below, along with design_spec.md and user_task_description. "
                  f"Fix all gaps, enforce correct routes, element IDs, data handling, and final polish.\n\n"
                  f"=== app_draft.py ===\n{app_draft_code}\n\n"
                  f"=== templates_draft ===\n{templates_draft}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    WebValidator = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
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
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential Flow: WebValidator then SequentialFixer
    await execute(
        WebValidator,
        (
            "Comprehensively validate app.py and templates/*.html for Flask syntax, runtime, route coverage, "
            "template element IDs and data bindings using design_spec.md and user_task_description. "
            "Generate detailed validation_report.md."
        )
    )

    # Read validation_report.md to pass content for context if needed (optional here, just execute directly)
    report_content = ""
    try:
        report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(
        SequentialFixer,
        (
            "Apply all corrections described in validation_report.md to app.py and templates/*.html "
            "to produce final compliant files fully meeting design_spec.md and user requirements. "
            "Use the following validation report for detailed fixes:\n"
            f"=== validation_report.md ===\n{report_content}"
        )
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
