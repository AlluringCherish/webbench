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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create detailed design specification document enabling independent backend and frontend development, including Flask routes, HTML templates, and data schemas\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect drafts design_spec.md covering three sections: \"\n        \"1) Flask routes with function names, context variables, and HTTP methods; \"\n        \"2) HTML templates specifying exact element IDs and layouts for all pages; \"\n        \"3) Data schemas outlining field names and formats for all text data files.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce a comprehensive design specification document enabling Backend and Frontend developers to work independently with clear deliverables.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce design_spec.md with three detailed sections:\n  1) Flask routes table (function names, HTTP methods, context variables)\n  2) HTML template specifications (exact element IDs, page layouts, navigation mappings)\n  3) Data schemas for all text data files (field names, order, format, examples)\n- Do NOT include implementation code or frontend/backend code\n- Do NOT assume any details beyond user_task_description\n\n**Section 1: Flask Routes Specification**\n\nCreate a table listing all routes with columns:\n- Route Path (e.g., /dashboard, /restaurants, /menu/<int:restaurant_id>)\n- Function Name (snake_case)\n- HTTP Method (GET or POST)\n- Template file (e.g., dashboard.html)\n- Context Variables passed to template with exact names and types\n- For dynamic routes, indicate parameter names and types\n\nRequirements:\n- Include root route '/' redirecting to dashboard\n- Provide context variables needed for rendering each page exactly\n- Use consistent function naming aligned with page purposes\n- Specify HTTP method(s) for each route clearly\n\n**Section 2: HTML Template Specifications**\n\nFor each template, specify:\n- File path (templates/{filename}.html)\n- Page Title for <title> and <h1>\n- All required element IDs with exact casing and element type (div, button, input, etc.)\n- Layout overview (brief description)\n- Navigation mappings: button/link element IDs linked to Flask route functions using url_for()\n- Dynamic element ID patterns (e.g., add-to-cart-button-{item_id}) described with Jinja2 usage\n\nRequirements:\n- All element IDs from page design MUST be included exactly\n- Navigation IDs must correspond to routes in Section 1\n- Template names and page titles must match user_task_description\n\n**Section 3: Data Schemas**\n\nSpecify data files in data/ directory with:\n- File name\n- Field order separated by pipe (|), with exact field names\n- Description of each file's purpose\n- 2-3 example data rows (from user_task_description)\n- Data types for fields (int, float, string, date)\n\nRequirements:\n- Use pipe-delimited format consistently\n- Field order must match exactly backend parsing requirements\n- Example data must be realistic and reflect user data\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developer can implement all routes and data loading only from Sections 1 and 3\n- Frontend developer can build templates from Section 2 without backend references\n- Context variable names are consistent between Sections 1 and 2\n- Element IDs and navigation mappings fully match user task specifications\n- Data schemas support all data files required in user task description\n\nUse write_text_file tool to save design_spec.md as output.\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md Section 1 for completeness and correctness of all Flask routes, \"\n                \"including function names, HTTP methods, and context variable details; and Section 3 for accurate data schemas \"\n                \"with correct field order and data types matching user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Check design_spec.md Section 2 for complete and precise HTML template specifications: \"\n                \"all element IDs, page layouts, and navigation mappings must be clearly defined and match user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend (app.py) and frontend (templates/*.html) independently based on the design specification\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py using Section 1 and Section 3 of design_spec.md, \"\n        \"handling Flask routing, data loading, and business logic. \"\n        \"FrontendDeveloper implements HTML templates (*.html) using Section 2 of design_spec.md focusing on UI and element IDs. \"\n        \"Both agents work concurrently without dependencies.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application (app.py) based solely on design specifications.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) from CONTEXT only\n- Implement all Flask routes and their handlers as specified, including the root route redirect\n- Load and handle data files located in data/ using the exact field orders defined in Section 3\n- DO NOT read or assume anything from Section 2 (frontend design) or any template source\n- DO NOT introduce functionality beyond the specification\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   # Import necessary modules and initialize Flask app\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root Route**:\n   - Implement '/' route to redirect to Dashboard page using url_for\n   - Example:\n   ```python\n   @app.route('/')\n   def root():\n       return redirect(url_for('dashboard'))\n   ```\n\n3. **Data Loading**:\n   - Load data from text files in data/ directory using pipe-delimited parsing\n   - Use exact field names and order from Section 3\n   - Example parsing line:\n   ```python\n   parts = line.strip().split('|')\n   record = {\n       'field1': parts[0],\n       'field2': parts[1],\n       # ...\n   }\n   ```\n   - Handle file I/O errors gracefully\n   - No header lines in data files\n\n4. **Route Implementation**:\n   - Implement ALL routes from Section 1 with exact function names and context variables\n   - Use render_template() with template file names from Section 1\n   - For POST routes, handle form data with request.form appropriately\n   - Validate input data and handle edge cases\n\n5. **Best Practices**:\n   - Include `if __name__ == '__main__': app.run(debug=True, port=5000)`\n   - Use url_for() for URL generation everywhere\n   - Return appropriate HTTP status codes where needed\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Strictly follow Section 1 route names, HTTP methods, and context variables\n- Follow field order and formats from Section 3 exactly for all data files\n- Do NOT read or use frontend information from Section 2\n- Do NOT add features not specified in Sections 1 and 3\n- Do NOT send code snippets via chat only; always write to app.py via write_text_file\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to implement complete frontend HTML templates (*.html) based on detailed design specifications.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) from CONTEXT only\n- Implement all HTML templates for the FoodDelivery app with exact page layouts, element IDs, and navigation flow\n- Do NOT read or assume anything from Section 1 or 3 (Backend or Data Schemas)\n- Do NOT read or modify any backend code (app.py)\n- Follow design_spec.md exactly without assumptions or omissions\n\nImplementation Requirements:\n1. **Template Structure**:\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ page_title }}</title>\n   </head>\n   <body>\n       <div id=\"main-container\">\n           <!-- Content as per design_spec.md Section 2 -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **File Naming and Location**:\n   - Save all templates in the templates/ directory\n   - Use filenames as specified (e.g., dashboard.html, restaurants.html)\n   - One file per page specification\n\n3. **Element IDs and UI Elements**:\n   - Include ALL element IDs EXACTLY as specified (case-sensitive)\n   - For dynamic elements (e.g., buttons with IDs including item IDs), use Jinja2 syntax\n     - Example: id=\"view-restaurant-button-{{ restaurant.restaurant_id }}\"\n\n4. **Page Titles**:\n   - Match page titles exactly as specified in Section 2, in both <title> and top-level <h1> tags\n\n5. **Context Variables and Jinja2 Syntax**:\n   - Use context variables as described in specifications\n   - Loop over lists: `{% for item in items %}...{% endfor %}`\n   - Conditional rendering for optional sections with `{% if condition %}...{% endif %}`\n\n6. **Navigation and URLs**:\n   - Implement navigation using Flask's url_for() syntax within templates\n   - For static links:\n     ```html\n     <a href=\"{{ url_for('function_name') }}\">\n         <button id=\"element-id\">Button Text</button>\n     </a>\n     ```\n   - For dynamic links:\n     ```html\n     <a href=\"{{ url_for('function_name', id=item.id) }}\">\n         <button id=\"element-id-{{ item.id }}\">Button Text</button>\n     </a>\n     ```\n\n7. **Forms**:\n   - For pages with POST forms, implement proper form tags and inputs\n   - Use CSRF tokens if specified (else omit)\n   - Use method=\"POST\" and action=\"{{ url_for('function_name') }}\"\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files in templates/\n- All element IDs must be present and exactly match specification (case-sensitive)\n- Page titles must match exactly both in <title> and <h1>\n- Navigation links must use correct url_for() function names\n- Do NOT add or remove pages or elements beyond specification\n- Do NOT provide code snippets only; always output full files via write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify backend (app.py) correctly implements all Flask routes and data schemas \"\n                \"from design_spec.md Sections 1 and 3, including root route redirect, proper context variables, \"\n                \"and data file handling.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify frontend HTML templates exactly match design_spec.md Section 2 specifications: \"\n                \"all element IDs, navigation, and page titles present and accurate.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def integration_and_testing_phase(\n    goal: str = \"Integrate backend and frontend components, perform functional testing, and ensure correct operation of FoodDelivery web app\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"IntegrationTester deploys combined app.py and templates, executes test cases, and writes detailed feedback. \"\n        \"DeveloperRefiner revises implementation iteratively based on feedback until all tests pass and functionality is verified.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"IntegrationTester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer with expertise in full-stack web application integration and functional testing.\n\nYour goal is to perform thorough integration testing of the combined backend and frontend of the FoodDelivery web app, verifying all user features and writing detailed feedback indicating approval or modification needs.\n\nTask Details:\n- Read app.py backend code and all HTML templates from templates/*.html\n- Refer to user_task_description for expected functionalities and UI elements\n- Test all main user workflows: browsing restaurants, viewing menus, ordering, cart management, checkout, order tracking, and reviews\n- Output integration_feedback.txt with comprehensive evaluation and status markers ([APPROVED] or NEED_MODIFY)\n\n**Testing Scope**\n\n- Verify presence and correct operation of UI elements with specified IDs\n- Ensure correct data flows between backend and frontend for all pages and user actions\n- Validate form inputs, button functions, page navigations, and data persistence\n- Check handling of edge cases and error conditions for user actions\n\n**Integration Testing Procedure**\n\n1. **Setup and Launch**\n   - Deploy app.py and templates together in test environment\n   - Run backend server and load frontend pages\n\n2. **Functional Test Cases**\n   - Dashboard: verify featured restaurants, navigation buttons function as expected\n   - Restaurant Listing: search, filter, view restaurant menu workflows\n   - Menu and Item Details: correct item info display and add-to-cart functionality\n   - Shopping Cart: quantity updates, removal, total amount calculation, proceed to checkout\n   - Checkout: input validation, placing order, order confirmation\n   - Active Orders & Tracking: status filters, tracking details display\n   - Reviews: display reviews, filter by rating, navigation to write review\n\n3. **Feedback Writing**\n   - For each feature/page, write concise evaluation with any errors or issues found\n   - Conclude overall status: write \"[APPROVED]\" if all tests pass completely, otherwise \"NEED_MODIFY\"\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to deploy and test backend code when applicable\n- Use write_text_file tool strictly to save integration_feedback.txt\n- Provide clear, actionable feedback enabling effective refinement\n- Write status marker ([APPROVED] or NEED_MODIFY) at the beginning or end of integration_feedback.txt\n- Do NOT change app.py or templates; only test and report\n\nOutput: integration_feedback.txt\"\"\",\n            \"tools\": [\"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"integration_feedback.txt\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DeveloperRefiner\",\n            \"prompt\": \"\"\"You are a Full-Stack Developer specializing in Python web applications with Flask and frontend templating.\n\nYour goal is to iteratively refine and improve both backend (app.py) and frontend templates (*.html) for the FoodDelivery web application, addressing all feedback provided by the IntegrationTester until the integration_feedback.txt file contains an [APPROVED] status.\n\nTask Details:\n- Read integration_feedback.txt to identify required fixes and improvements\n- Review current app.py and templates/*.html to locate issues\n- Revise backend and frontend code to resolve reported problems and enhance functional correctness\n- Preserve all required UI elements with specified IDs and business logic outlined in user_task_description\n- Output updated app.py and templates/*.html files for next testing cycle\n\n**Refinement Workflow**\n\n1. **Analyze Feedback**\n   - Extract all points labeled as NEED_MODIFY or suggestions for fixes/improvements\n   - Categorize issues by backend or frontend\n\n2. **Code Update**\n   - Modify app.py backend logic accordingly\n   - Update templates to fix UI, IDs, navigation, and display issues\n   - Ensure no regressions and compatibility with remaining specifications\n\n3. **Prepare for Next Test**\n   - Save revised app.py and templates/*.html\n   - Ensure completeness and correctness before next integration test\n\nCRITICAL SUCCESS CRITERIA:\n- Effectively address all feedback items in integration_feedback.txt\n- Maintain consistency with user_task_description features, data flows, and UI elements\n- Use write_text_file tool to output updated files (app.py and templates/*.html)\n- Do NOT produce side effects outside specified files or modify unrelated artifacts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"integration_feedback.txt\", \"source\": \"IntegrationTester\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"IntegrationTester\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Check integration feedback for comprehensive functional coverage, accuracy, completeness, \"\n                \"and verify that identified issues are addressed well.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"integration_feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DeveloperRefiner\",\n            \"reviewer_agent\": \"IntegrationTester\",\n            \"review_criteria\": (\n                \"Verify that refinements in app.py and templates/*.html adequately address all feedback points \"\n                \"and improve overall functional correctness.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"integration_feedback.txt\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce a comprehensive design specification document enabling Backend and Frontend developers to work independently with clear deliverables.

Task Details:
- Read user_task_description from CONTEXT
- Produce design_spec.md with three detailed sections:
  1) Flask routes table (function names, HTTP methods, context variables)
  2) HTML template specifications (exact element IDs, page layouts, navigation mappings)
  3) Data schemas for all text data files (field names, order, format, examples)
- Do NOT include implementation code or frontend/backend code
- Do NOT assume any details beyond user_task_description

**Section 1: Flask Routes Specification**

Create a table listing all routes with columns:
- Route Path (e.g., /dashboard, /restaurants, /menu/<int:restaurant_id>)
- Function Name (snake_case)
- HTTP Method (GET or POST)
- Template file (e.g., dashboard.html)
- Context Variables passed to template with exact names and types
- For dynamic routes, indicate parameter names and types

Requirements:
- Include root route '/' redirecting to dashboard
- Provide context variables needed for rendering each page exactly
- Use consistent function naming aligned with page purposes
- Specify HTTP method(s) for each route clearly

**Section 2: HTML Template Specifications**

For each template, specify:
- File path (templates/{filename}.html)
- Page Title for <title> and <h1>
- All required element IDs with exact casing and element type (div, button, input, etc.)
- Layout overview (brief description)
- Navigation mappings: button/link element IDs linked to Flask route functions using url_for()
- Dynamic element ID patterns (e.g., add-to-cart-button-{item_id}) described with Jinja2 usage

Requirements:
- All element IDs from page design MUST be included exactly
- Navigation IDs must correspond to routes in Section 1
- Template names and page titles must match user_task_description

**Section 3: Data Schemas**

Specify data files in data/ directory with:
- File name
- Field order separated by pipe (|), with exact field names
- Description of each file's purpose
- 2-3 example data rows (from user_task_description)
- Data types for fields (int, float, string, date)

Requirements:
- Use pipe-delimited format consistently
- Field order must match exactly backend parsing requirements
- Example data must be realistic and reflect user data

CRITICAL SUCCESS CRITERIA:
- Backend developer can implement all routes and data loading only from Sections 1 and 3
- Frontend developer can build templates from Section 2 without backend references
- Context variable names are consistent between Sections 1 and 2
- Element IDs and navigation mappings fully match user task specifications
- Data schemas support all data files required in user task description

Use write_text_file tool to save design_spec.md as output."""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend application (app.py) based solely on design specifications.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) from CONTEXT only
- Implement all Flask routes and their handlers as specified, including the root route redirect
- Load and handle data files located in data/ using the exact field orders defined in Section 3
- DO NOT read or assume anything from Section 2 (frontend design) or any template source
- DO NOT introduce functionality beyond the specification

Implementation Requirements:
1. **Flask Application Setup**:
   # Import necessary modules and initialize Flask app
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root Route**:
   - Implement '/' route to redirect to Dashboard page using url_for
   - Example:
   ```python
   @app.route('/')
   def root():
       return redirect(url_for('dashboard'))
   ```

3. **Data Loading**:
   - Load data from text files in data/ directory using pipe-delimited parsing
   - Use exact field names and order from Section 3
   - Example parsing line:
   ```python
   parts = line.strip().split('|')
   record = {
       'field1': parts[0],
       'field2': parts[1],
       # ...
   }
   ```
   - Handle file I/O errors gracefully
   - No header lines in data files

4. **Route Implementation**:
   - Implement ALL routes from Section 1 with exact function names and context variables
   - Use render_template() with template file names from Section 1
   - For POST routes, handle form data with request.form appropriately
   - Validate input data and handle edge cases

5. **Best Practices**:
   - Include `if __name__ == '__main__': app.run(debug=True, port=5000)`
   - Use url_for() for URL generation everywhere
   - Return appropriate HTTP status codes where needed

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Strictly follow Section 1 route names, HTTP methods, and context variables
- Follow field order and formats from Section 3 exactly for all data files
- Do NOT read or use frontend information from Section 2
- Do NOT add features not specified in Sections 1 and 3
- Do NOT send code snippets via chat only; always write to app.py via write_text_file

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement complete frontend HTML templates (*.html) based on detailed design specifications.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) from CONTEXT only
- Implement all HTML templates for the FoodDelivery app with exact page layouts, element IDs, and navigation flow
- Do NOT read or assume anything from Section 1 or 3 (Backend or Data Schemas)
- Do NOT read or modify any backend code (app.py)
- Follow design_spec.md exactly without assumptions or omissions

Implementation Requirements:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ page_title }}</title>
   </head>
   <body>
       <div id="main-container">
           <!-- Content as per design_spec.md Section 2 -->
       </div>
   </body>
   </html>
   ```

2. **File Naming and Location**:
   - Save all templates in the templates/ directory
   - Use filenames as specified (e.g., dashboard.html, restaurants.html)
   - One file per page specification

3. **Element IDs and UI Elements**:
   - Include ALL element IDs EXACTLY as specified (case-sensitive)
   - For dynamic elements (e.g., buttons with IDs including item IDs), use Jinja2 syntax
     - Example: id="view-restaurant-button-{{ restaurant.restaurant_id }}"

4. **Page Titles**:
   - Match page titles exactly as specified in Section 2, in both <title> and top-level <h1> tags

5. **Context Variables and Jinja2 Syntax**:
   - Use context variables as described in specifications
   - Loop over lists: `{% for item in items %}...{% endfor %}`
   - Conditional rendering for optional sections with `{% if condition %}...{% endif %}`

6. **Navigation and URLs**:
   - Implement navigation using Flask's url_for() syntax within templates
   - For static links:
     ```html
     <a href="{{ url_for('function_name') }}">
         <button id="element-id">Button Text</button>
     </a>
     ```
   - For dynamic links:
     ```html
     <a href="{{ url_for('function_name', id=item.id) }}">
         <button id="element-id-{{ item.id }}">Button Text</button>
     </a>
     ```

7. **Forms**:
   - For pages with POST forms, implement proper form tags and inputs
   - Use CSRF tokens if specified (else omit)
   - Use method="POST" and action="{{ url_for('function_name') }}"

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files in templates/
- All element IDs must be present and exactly match specification (case-sensitive)
- Page titles must match exactly both in <title> and <h1>
- Navigation links must use correct url_for() function names
- Do NOT add or remove pages or elements beyond specification
- Do NOT provide code snippets only; always output full files via write_text_file

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "IntegrationTester": {
        "prompt": (
            """You are a Software Test Engineer with expertise in full-stack web application integration and functional testing.

Your goal is to perform thorough integration testing of the combined backend and frontend of the FoodDelivery web app, verifying all user features and writing detailed feedback indicating approval or modification needs.

Task Details:
- Read app.py backend code and all HTML templates from templates/*.html
- Refer to user_task_description for expected functionalities and UI elements
- Test all main user workflows: browsing restaurants, viewing menus, ordering, cart management, checkout, order tracking, and reviews
- Output integration_feedback.txt with comprehensive evaluation and status markers ([APPROVED] or NEED_MODIFY)

**Testing Scope**

- Verify presence and correct operation of UI elements with specified IDs
- Ensure correct data flows between backend and frontend for all pages and user actions
- Validate form inputs, button functions, page navigations, and data persistence
- Check handling of edge cases and error conditions for user actions

**Integration Testing Procedure**

1. **Setup and Launch**
   - Deploy app.py and templates together in test environment
   - Run backend server and load frontend pages

2. **Functional Test Cases**
   - Dashboard: verify featured restaurants, navigation buttons function as expected
   - Restaurant Listing: search, filter, view restaurant menu workflows
   - Menu and Item Details: correct item info display and add-to-cart functionality
   - Shopping Cart: quantity updates, removal, total amount calculation, proceed to checkout
   - Checkout: input validation, placing order, order confirmation
   - Active Orders & Tracking: status filters, tracking details display
   - Reviews: display reviews, filter by rating, navigation to write review

3. **Feedback Writing**
   - For each feature/page, write concise evaluation with any errors or issues found
   - Conclude overall status: write "[APPROVED]" if all tests pass completely, otherwise "NEED_MODIFY"

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to deploy and test backend code when applicable
- Use write_text_file tool strictly to save integration_feedback.txt
- Provide clear, actionable feedback enabling effective refinement
- Write status marker ([APPROVED] or NEED_MODIFY) at the beginning or end of integration_feedback.txt
- Do NOT change app.py or templates; only test and report

Output: integration_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'integration_feedback.txt'}],
    },

    "DeveloperRefiner": {
        "prompt": (
            """You are a Full-Stack Developer specializing in Python web applications with Flask and frontend templating.

Your goal is to iteratively refine and improve both backend (app.py) and frontend templates (*.html) for the FoodDelivery web application, addressing all feedback provided by the IntegrationTester until the integration_feedback.txt file contains an [APPROVED] status.

Task Details:
- Read integration_feedback.txt to identify required fixes and improvements
- Review current app.py and templates/*.html to locate issues
- Revise backend and frontend code to resolve reported problems and enhance functional correctness
- Preserve all required UI elements with specified IDs and business logic outlined in user_task_description
- Output updated app.py and templates/*.html files for next testing cycle

**Refinement Workflow**

1. **Analyze Feedback**
   - Extract all points labeled as NEED_MODIFY or suggestions for fixes/improvements
   - Categorize issues by backend or frontend

2. **Code Update**
   - Modify app.py backend logic accordingly
   - Update templates to fix UI, IDs, navigation, and display issues
   - Ensure no regressions and compatibility with remaining specifications

3. **Prepare for Next Test**
   - Save revised app.py and templates/*.html
   - Ensure completeness and correctness before next integration test

CRITICAL SUCCESS CRITERIA:
- Effectively address all feedback items in integration_feedback.txt
- Maintain consistency with user_task_description features, data flows, and UI elements
- Use write_text_file tool to output updated files (app.py and templates/*.html)
- Do NOT produce side effects outside specified files or modify unrelated artifacts

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'integration_feedback.txt', 'source': 'IntegrationTester'}, {'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Check design_spec.md Section 1 for completeness and correctness of all Flask routes, "
                "including function names, HTTP methods, and context variable details; and Section 3 for accurate data schemas "
                "with correct field order and data types matching user requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Check design_spec.md Section 2 for complete and precise HTML template specifications: "
                "all element IDs, page layouts, and navigation mappings must be clearly defined and match user requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify backend (app.py) correctly implements all Flask routes and data schemas "
                "from design_spec.md Sections 1 and 3, including root route redirect, proper context variables, "
                "and data file handling.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify frontend HTML templates exactly match design_spec.md Section 2 specifications: "
                "all element IDs, navigation, and page titles present and accurate.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'IntegrationTester': [
        ("SystemArchitect", """Check integration feedback for comprehensive functional coverage, accuracy, completeness, "
                "and verify that identified issues are addressed well.""", [{'type': 'text_file', 'name': 'integration_feedback.txt'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'DeveloperRefiner': [
        ("IntegrationTester", """Verify that refinements in app.py and templates/*.html adequately address all feedback points "
                "and improve overall functional correctness.""", [{'type': 'text_file', 'name': 'integration_feedback.txt'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Compound Chaos Controller Setup ====================
import random
from chaos.injectors import ChaosMode

# Compound Chaos: Per-task sampling
COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "prompt_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "io_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "prompt_probability": 0.2,
    "io_probability": 0.2
}

# ChaosMode mapping
MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["prompt_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Agent chaos is sampled with intensity
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

# Prompt/IO separately sampled at 0.2 probability (reset)
all_agents = list(AGENT_PROFILES.keys())
chaos_controller.stress_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["prompt_probability"]]
chaos_controller.io_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["io_probability"]]

# Guarantee at least 1
if not chaos_controller.stress_chaos_targets:
    chaos_controller.stress_chaos_targets = [random.choice(all_agents)]
if not chaos_controller.io_chaos_targets:
    chaos_controller.io_chaos_targets = [random.choice(all_agents)]

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "compound_config": COMPOUND_CONFIG,
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

print(f"Compound Chaos activated: Agent={COMPOUND_CONFIG['agent_intensity']}, Prompt={COMPOUND_CONFIG['prompt_method']}, IO={COMPOUND_CONFIG['io_method']}")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Produce comprehensive design_spec.md including Flask routes, HTML templates, and data schemas based on user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    # Create FrontendDeveloper agent
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py based on Sections 1 and 3 of design_spec.md with all Flask routes, data loading, and business logic"),
        execute(FrontendDeveloper, "Implement all HTML templates (*.html) based on Section 2 of design_spec.md, ensuring exact layouts, element IDs, page titles, and navigation")
    )
# Phase2_End

# Phase3_Start
import asyncio

async def integration_and_testing_phase():
    # Create agents
    IntegrationTester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationTester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    DeveloperRefiner = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DeveloperRefiner",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_ITERATIONS = 3
    for iteration in range(MAX_ITERATIONS):
        if iteration == 0:
            # Initial integration test
            await execute(IntegrationTester, "Deploy app.py and templates; perform full integration testing according to user_task_description; write integration_feedback.txt")
        else:
            # Read the previous feedback to instruct DeveloperRefiner
            try:
                with open("integration_feedback.txt", "r") as f:
                    feedback_content = f.read()
            except FileNotFoundError:
                feedback_content = ""

            # If approval found, stop loop
            if "[APPROVED]" in feedback_content:
                break

            # DeveloperRefiner revises app.py and templates according to feedback
            await execute(DeveloperRefiner, f"Refine app.py and templates based on integration_feedback.txt:\n{feedback_content}")

            # Run integration test again after refinement
            await execute(IntegrationTester, "Deploy app.py and templates; perform full integration testing according to user_task_description; write integration_feedback.txt")

            # Re-check approval status after testing
            try:
                with open("integration_feedback.txt", "r") as f:
                    feedback_content = f.read()
                if "[APPROVED]" in feedback_content:
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
        design_specification_phase()
    ]
    step2 = [
        parallel_implementation_phase()
    ]
    step3 = [
        integration_and_testing_phase()
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
