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
# 20260714_001749_976611/main_20260714_001749_976611.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create complementary backend and frontend designs for the OnlineAuction web app and merge into one consistent design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect specifies Flask routes, data models from auctions, bids, winners, and items, and data management logic into backend_design.md. \"\n        \"FrontendDesignArchitect defines HTML templates with exact element IDs and page structures for the 9 application pages into frontend_design.md. \"\n        \"DesignMerger consumes backend_design.md and frontend_design.md plus the user task description to reconcile and write a coherent design_spec.md without deviation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with expertise in designing backend routes and data management using local text files.\n\nYour goal is to specify the backend design for the OnlineAuction application, including Flask route architecture, data file handling, data schemas, and management logic, independently of frontend specifications.\n\nTask Details:\n- Read user_task_description from CONTEXT.\n- Produce backend_design.md detailing all backend routes, logic, and text-based data file schemas.\n- Focus exclusively on backend artifacts without reading frontend_design.md.\n\n**Section 1: Flask Routes and Backend Logic**\n- Specify all Flask routes: URL paths, HTTP methods, controller logic, and related templates (template filenames only).\n- Detail the handling of auctions, bids, winners, trending data, and category-related routes.\n- Include logic for data read/write operations targeting the defined local text files.\n- Cover special routes for filtering, sorting, and navigation for each page's required backend.\n\n**Section 2: Data File Schemas and Access**\n- For each text data file (e.g., auctions.txt, categories.txt, bids.txt, winners.txt, bid_history.txt, items.txt, trending.txt):\n  - Define exact file path relative to a 'data' directory.\n  - Specify delimiter, field names, types, and descriptions matching user_task_description.\n  - Provide example rows illustrating the format.\n- Include data validation and concurrency considerations in design if applicable.\n\n**Section 3: Data Management and Business Logic**\n- Describe logic for placing bids, updating current bids, recording winners.\n- Define data retrieval processes for dashboards, trending auctions, category browsing, and bid history.\n- Ensure data consistency strategies for concurrent accesses or updates.\n- Provide summaries sufficient for implementation without referencing frontend designs.\n\nCRITICAL SUCCESS CRITERIA:\n- Output backend_design.md suitable for backend developers to implement Flask app.py.\n- Use write_text_file tool for artifact creation.\n- Include no references or assumptions about frontend_design.md.\n- Follow all user task requirements precisely.\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications, with expertise in crafting page layouts and element structures.\n\nYour goal is to define all frontend design specifications for the OnlineAuction app, including exact HTML template structures, element IDs, and navigation flows for the nine required web pages.\n\nTask Details:\n- Read user_task_description from CONTEXT.\n- Independently author frontend_design.md containing detailed template specifications.\n- Define all structural elements, IDs, navigation buttons, forms, and page layouts for each specified page.\n- Do not depend on backend_design.md.\n\n**Section 1: HTML Template Structure**\n- Specify paths and filenames of all templates (*.html).\n- For each of the nine pages, define:\n  - Page title exact text.\n  - Container elements with their element IDs and types.\n  - Key interactive elements including buttons, inputs, tables, dropdowns, with exact element IDs.\n  - Page sections and containers hierarchy for layout clarity.\n- Provide details on context variables required for dynamic content rendering.\n\n**Section 2: Navigation and Interaction**\n- Map buttons and navigation elements to their corresponding page transitions.\n- Define consistent naming conventions for element IDs and form fields per page.\n- Specify any client-side behaviors necessary for proper page functionality (e.g., filters, sorts).\n\n**Section 3: Styling and Accessibility Notes** (if applicable)\n- Include essential notes on element roles and accessibility attributes.\n- Highlight structural considerations for responsiveness or adaptive layouts.\n\nCRITICAL SUCCESS CRITERIA:\n- Output frontend_design.md that frontend developers can use to implement templates/*.html.\n- Use write_text_file tool to save output.\n- Adhere strictly to element IDs, page titles, and interaction flows as per user task.\n- Avoid any backend-specific details or assumptions.\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in integration and reconciliation of complementary backend and frontend design specifications into a cohesive and consistent design contract.\n\nYour goal is to merge backend_design.md and frontend_design.md into one unified design_spec.md, ensuring internal consistency and full compliance with the OnlineAuction user requirements without adding or omitting details.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT.\n- Thoroughly analyze backend and frontend artifacts to identify potential inconsistencies or gaps.\n- Reconcile backend routes, data schemas, and logic with frontend templates, element IDs, and navigation flows.\n- Preserve all data fields, routes, template names, and element IDs as declared.\n- Clearly organize design_spec.md into sections: Backend Routes & Data, Frontend Templates & Elements, and Data Schemas & Integration Notes.\n\n**Section 1: Backend Integration**\n- Validate all backend routes are referenced correctly in frontend navigation.\n- Confirm route methods, parameters, and data management align with interface requirements.\n- Ensure backend data schemas fully support frontend dynamic content needs.\n\n**Section 2: Frontend Integration**\n- Verify all frontend pages specify elements and IDs as required.\n- Confirm navigation flows correspond to backend routes.\n- Maintain consistency in naming conventions between backend and frontend.\n\n**Section 3: Overall Consistency and Completeness**\n- No new requirements or features beyond user_task_description.\n- All bidirectional dependencies are properly documented.\n- Provide summary notes on any adaptations or required developer clarifications.\n\nCRITICAL SUCCESS CRITERIA:\n- Output design_spec.md consolidating backend_design.md and frontend_design.md into one source of truth.\n- Use write_text_file tool exclusively.\n- Maintain integrity of all input artifact data without divergence.\n- Ensure output fully satisfies the user task.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check backend design completeness and correctness against user task and compatibility with frontend design.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend design adherence to user requirements and backend design integration feasibility.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend logic and frontend templates in parallel from design_spec.md, then integrate into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with routing, data loading, and business logic per design_spec.md. \"\n        \"FrontendDeveloper implements all HTML templates for 9 pages with specified element IDs and navigation per design_spec.md. \"\n        \"IntegrationMerger integrates app.py and frontend templates ensuring interface correctness and produces the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with Python.\n\nYour goal is to implement a complete Flask backend application including all required routes, business logic, and data file management according to the provided design specifications.\n\nTask Details:\n- Read design_spec.md from CONTEXT as the only input artifact\n- Independently implement app.py covering auctions, bids, winners, categories, trending data, and file I/O per design_spec.md\n- Produce the full backend app.py as output artifact without accessing any sibling agent outputs\n\n**Implementation Requirements:**\n- Define Flask routes corresponding to all pages and features described in design_spec.md\n- Implement business logic for auction browsing, bidding, bid history, winners, categories, trending auctions, and auction status\n- Use local text files in 'data' directory for persistent storage with proper parsing and writing according to data schemas\n- Handle all route methods (GET, POST) and data validation\n- Include error handling and input sanitation as needed\n- Follow any naming conventions and route paths exactly specified in design_spec.md\n\n**Code Template:**\n''' \nfrom flask import Flask, render_template, request, redirect, url_for\n# Additional imports\napp = Flask(__name__)\n\n# Route definitions corresponding to design_spec.md pages\n# Functions implementing data loading and business logic\n# Data read/write using local text files as per design_spec.md format\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n'''\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save the complete app.py file\n- Implement exactly the routes and logic specified in design_spec.md\n- Do not read or depend on frontend templates or sibling outputs\n- Focus solely on backend implementation from design_spec.md\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for web applications.\n\nYour goal is to develop all HTML templates for the nine specified pages with exact element IDs, layout, and navigation per the design specifications.\n\nTask Details:\n- Read design_spec.md from CONTEXT as the only input artifact\n- Independently create templates/*.html files for all required pages\n- Use exact element IDs and structure defined in design_spec.md\n- Generate well-structured, semantic HTML with Jinja2 variable placeholders as needed\n- Do not access backend code or sibling agent outputs\n\n**Implementation Requirements:**\n- Create one HTML template file per page described in design_spec.md (total nine pages)\n- Assign exact IDs to elements as specified (buttons, div containers, inputs, tables, etc.)\n- Include navigation elements linking pages per design_spec.md requirements\n- Apply consistent page titles and headers\n- Use Jinja2 syntax for dynamic content placeholders consistent with backend design\n\n**Example Code Snippet:**\n''' \n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <title>{{ page_title }}</title>\n</head>\n<body>\n    <div id=\"dashboard-page\">\n        <!-- Featured auctions section -->\n        <!-- Buttons with IDs like browse-auctions-button -->\n    </div>\n</body>\n</html>\n'''\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output all templates as templates/*.html\n- Follow design_spec.md strictly for element IDs and page structure\n- Templates are independently complete without backend code access\n- Do not read backend code or sibling outputs\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integrator specializing in Flask backend and frontend template integration.\n\nYour goal is to merge and reconcile the backend app.py and frontend templates into a consistent, executable application bundle.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify that Flask route handlers in app.py match template files and element IDs in templates/*.html\n- Identify and correct interface mismatches such as route names, template references, and context variables\n- Produce final merged app.py and templates/*.html artifacts that are ready for deployment\n- Do not modify design_spec.md or add new requirements\n\n**Integration and Validation Steps:**\n- Validate that all route endpoints in app.py have corresponding HTML templates with correct element IDs\n- Ensure navigation links in templates point to Flask routes in app.py accurately\n- Check that data placeholders in templates match context variables passed by app.py\n- Fix any discrepancies in filenames, variable names, or routing logic without altering design intent\n- Confirm file I/O and data handling remains consistent with design_spec.md\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output finalized app.py and templates/*.html\n- Integration covers all features specified in design_spec.md\n- Outputs are coherent and runnable as a single Flask application\n- Do not alter design_spec.md or add features beyond input artifacts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify backend implementation matches route, data handling, and business logic in design_spec.md precisely.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify frontend templates conform to design_spec.md element IDs, layout, and navigation requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'OnlineAuction' Web Application

## 1. Objective
Develop a comprehensive web application named 'OnlineAuction' using Python, with data managed through local text files. The application enables users to browse auction items, place bids, track bid history, view winning items, and explore categories. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'OnlineAuction' application is Python.

## 3. Page Design

The 'OnlineAuction' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Auction Dashboard
- **Overview**: The main hub displaying featured auction items, trending auctions, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-auctions** - Type: Div - Display of featured auction items.
  - **ID: browse-auctions-button** - Type: Button - Button to navigate to auction catalog page.
  - **ID: view-bids-button** - Type: Button - Button to navigate to bid history page.
  - **ID: trending-auctions-button** - Type: Button - Button to navigate to trending auctions page.

### 2. Auction Catalog Page
- **Page Title**: Auction Catalog
- **Overview**: A page displaying all available auction items with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search auctions by item name, description, or item ID.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Electronics, Collectibles, Furniture, Art, Other).
  - **ID: auctions-grid** - Type: Div - Grid displaying auction cards with item image, title, current bid, and time remaining.
  - **ID: view-auction-button-{auction_id}** - Type: Button - Button to view auction details (each auction card has this).

### 3. Auction Details Page
- **Page Title**: Auction Details
- **Overview**: A page displaying detailed information about a specific auction item.
- **Elements**:
  - **ID: auction-details-page** - Type: Div - Container for the auction details page.
  - **ID: auction-title** - Type: H1 - Display auction item title.
  - **ID: auction-description** - Type: Div - Display item description.
  - **ID: current-bid** - Type: Div - Display current highest bid amount.
  - **ID: place-bid-button** - Type: Button - Button to place a new bid.
  - **ID: bid-history** - Type: Div - Section displaying bid history with bidder names and amounts.

### 4. Place Bid Page
- **Page Title**: Place Bid
- **Overview**: A page for users to enter bid information for an auction item.
- **Elements**:
  - **ID: place-bid-page** - Type: Div - Container for the place bid page.
  - **ID: bidder-name** - Type: Input - Field to input bidder name.
  - **ID: bid-amount** - Type: Input - Field to input bid amount.
  - **ID: auction-name** - Type: Div - Display the auction item name.
  - **ID: minimum-bid** - Type: Div - Display minimum acceptable bid amount.
  - **ID: submit-bid-button** - Type: Button - Button to submit the bid.

### 5. Bid History Page
- **Page Title**: Bid History
- **Overview**: A page displaying all bids placed by users with detailed information.
- **Elements**:
  - **ID: bid-history-page** - Type: Div - Container for the bid history page.
  - **ID: bids-table** - Type: Table - Table displaying bids with bid ID, auction name, bidder, amount, and timestamp.
  - **ID: filter-by-auction** - Type: Dropdown - Dropdown to filter bids by auction.
  - **ID: sort-by-amount** - Type: Button - Button to sort bids by amount.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Auction Categories Page
- **Page Title**: Auction Categories
- **Overview**: A page displaying all auction categories with brief descriptions.
- **Elements**:
  - **ID: categories-page** - Type: Div - Container for the categories page.
  - **ID: categories-list** - Type: Div - List of categories with descriptions and item counts.
  - **ID: category-card-{category_id}** - Type: Div - Card for each category with name and count.
  - **ID: view-category-button-{category_id}** - Type: Button - Button to view items in category (each category card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Winners Page
- **Page Title**: Winning Items
- **Overview**: A page displaying all auction items won by users with winner information.
- **Elements**:
  - **ID: winners-page** - Type: Div - Container for the winners page.
  - **ID: winners-list** - Type: Div - List of winning items with item name, winner, and winning bid amount.
  - **ID: winner-card-{auction_id}** - Type: Div - Card for each winning item.
  - **ID: filter-by-winner** - Type: Input - Input field to filter winners by name.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Trending Auctions Page
- **Page Title**: Trending Auctions
- **Overview**: A page displaying the most popular and active auction items ranked by bid activity.
- **Elements**:
  - **ID: trending-page** - Type: Div - Container for the trending auctions page.
  - **ID: trending-list** - Type: Div - Ranked list of trending auctions with rank, title, current bid, and bid count.
  - **ID: time-range-filter** - Type: Dropdown - Dropdown to filter by time range (Last 24 Hours, This Week, All Time).
  - **ID: view-auction-button-{auction_id}** - Type: Button - Button to view auction details (each trending item has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Auction Status Page
- **Page Title**: Auction Status
- **Overview**: A page displaying the status of all active, closed, and upcoming auctions.
- **Elements**:
  - **ID: status-page** - Type: Div - Container for the auction status page.
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Active, Closed, Upcoming).
  - **ID: status-table** - Type: Table - Table displaying auctions with name, status, time remaining, and current bid.
  - **ID: refresh-status-button** - Type: Button - Button to refresh auction statuses.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'OnlineAuction' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Auctions Data
- **File Name**: `auctions.txt`
- **Data Format**:
  ```
  auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
  ```
- **Example Data**:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description|item_count
  ```
- **Example Data**:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. Bids Data
- **File Name**: `bids.txt`
- **Data Format**:
  ```
  bid_id|auction_id|bidder_name|bid_amount|bid_timestamp
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. Winners Data
- **File Name**: `winners.txt`
- **Data Format**:
  ```
  winner_id|auction_id|item_name|winner_name|winning_bid|win_date
  ```
- **Example Data**:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. Bid History Data
- **File Name**: `bid_history.txt`
- **Data Format**:
  ```
  history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp
  ```
- **Example Data**:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. Items Data
- **File Name**: `items.txt`
- **Data Format**:
  ```
  item_id|auction_id|item_name|starting_price|category|condition|seller_name
  ```
- **Example Data**:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. Trending Data
- **File Name**: `trending.txt`
- **Data Format**:
  ```
  auction_id|item_name|bid_count|current_bid|trending_rank|time_period
  ```
- **Example Data**:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
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
            """You are a Backend Developer specializing in Flask web applications with expertise in designing backend routes and data management using local text files.

Your goal is to specify the backend design for the OnlineAuction application, including Flask route architecture, data file handling, data schemas, and management logic, independently of frontend specifications.

Task Details:
- Read user_task_description from CONTEXT.
- Produce backend_design.md detailing all backend routes, logic, and text-based data file schemas.
- Focus exclusively on backend artifacts without reading frontend_design.md.

**Section 1: Flask Routes and Backend Logic**
- Specify all Flask routes: URL paths, HTTP methods, controller logic, and related templates (template filenames only).
- Detail the handling of auctions, bids, winners, trending data, and category-related routes.
- Include logic for data read/write operations targeting the defined local text files.
- Cover special routes for filtering, sorting, and navigation for each page's required backend.

**Section 2: Data File Schemas and Access**
- For each text data file (e.g., auctions.txt, categories.txt, bids.txt, winners.txt, bid_history.txt, items.txt, trending.txt):
  - Define exact file path relative to a 'data' directory.
  - Specify delimiter, field names, types, and descriptions matching user_task_description.
  - Provide example rows illustrating the format.
- Include data validation and concurrency considerations in design if applicable.

**Section 3: Data Management and Business Logic**
- Describe logic for placing bids, updating current bids, recording winners.
- Define data retrieval processes for dashboards, trending auctions, category browsing, and bid history.
- Ensure data consistency strategies for concurrent accesses or updates.
- Provide summaries sufficient for implementation without referencing frontend designs.

CRITICAL SUCCESS CRITERIA:
- Output backend_design.md suitable for backend developers to implement Flask app.py.
- Use write_text_file tool for artifact creation.
- Include no references or assumptions about frontend_design.md.
- Follow all user task requirements precisely.

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications, with expertise in crafting page layouts and element structures.

Your goal is to define all frontend design specifications for the OnlineAuction app, including exact HTML template structures, element IDs, and navigation flows for the nine required web pages.

Task Details:
- Read user_task_description from CONTEXT.
- Independently author frontend_design.md containing detailed template specifications.
- Define all structural elements, IDs, navigation buttons, forms, and page layouts for each specified page.
- Do not depend on backend_design.md.

**Section 1: HTML Template Structure**
- Specify paths and filenames of all templates (*.html).
- For each of the nine pages, define:
  - Page title exact text.
  - Container elements with their element IDs and types.
  - Key interactive elements including buttons, inputs, tables, dropdowns, with exact element IDs.
  - Page sections and containers hierarchy for layout clarity.
- Provide details on context variables required for dynamic content rendering.

**Section 2: Navigation and Interaction**
- Map buttons and navigation elements to their corresponding page transitions.
- Define consistent naming conventions for element IDs and form fields per page.
- Specify any client-side behaviors necessary for proper page functionality (e.g., filters, sorts).

**Section 3: Styling and Accessibility Notes** (if applicable)
- Include essential notes on element roles and accessibility attributes.
- Highlight structural considerations for responsiveness or adaptive layouts.

CRITICAL SUCCESS CRITERIA:
- Output frontend_design.md that frontend developers can use to implement templates/*.html.
- Use write_text_file tool to save output.
- Adhere strictly to element IDs, page titles, and interaction flows as per user task.
- Avoid any backend-specific details or assumptions.

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in integration and reconciliation of complementary backend and frontend design specifications into a cohesive and consistent design contract.

Your goal is to merge backend_design.md and frontend_design.md into one unified design_spec.md, ensuring internal consistency and full compliance with the OnlineAuction user requirements without adding or omitting details.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT.
- Thoroughly analyze backend and frontend artifacts to identify potential inconsistencies or gaps.
- Reconcile backend routes, data schemas, and logic with frontend templates, element IDs, and navigation flows.
- Preserve all data fields, routes, template names, and element IDs as declared.
- Clearly organize design_spec.md into sections: Backend Routes & Data, Frontend Templates & Elements, and Data Schemas & Integration Notes.

**Section 1: Backend Integration**
- Validate all backend routes are referenced correctly in frontend navigation.
- Confirm route methods, parameters, and data management align with interface requirements.
- Ensure backend data schemas fully support frontend dynamic content needs.

**Section 2: Frontend Integration**
- Verify all frontend pages specify elements and IDs as required.
- Confirm navigation flows correspond to backend routes.
- Maintain consistency in naming conventions between backend and frontend.

**Section 3: Overall Consistency and Completeness**
- No new requirements or features beyond user_task_description.
- All bidirectional dependencies are properly documented.
- Provide summary notes on any adaptations or required developer clarifications.

CRITICAL SUCCESS CRITERIA:
- Output design_spec.md consolidating backend_design.md and frontend_design.md into one source of truth.
- Use write_text_file tool exclusively.
- Maintain integrity of all input artifact data without divergence.
- Ensure output fully satisfies the user task.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with Python.

Your goal is to implement a complete Flask backend application including all required routes, business logic, and data file management according to the provided design specifications.

Task Details:
- Read design_spec.md from CONTEXT as the only input artifact
- Independently implement app.py covering auctions, bids, winners, categories, trending data, and file I/O per design_spec.md
- Produce the full backend app.py as output artifact without accessing any sibling agent outputs

**Implementation Requirements:**
- Define Flask routes corresponding to all pages and features described in design_spec.md
- Implement business logic for auction browsing, bidding, bid history, winners, categories, trending auctions, and auction status
- Use local text files in 'data' directory for persistent storage with proper parsing and writing according to data schemas
- Handle all route methods (GET, POST) and data validation
- Include error handling and input sanitation as needed
- Follow any naming conventions and route paths exactly specified in design_spec.md

**Code Template:**
''' 
from flask import Flask, render_template, request, redirect, url_for
# Additional imports
app = Flask(__name__)

# Route definitions corresponding to design_spec.md pages
# Functions implementing data loading and business logic
# Data read/write using local text files as per design_spec.md format

if __name__ == "__main__":
    app.run(debug=True)
'''

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save the complete app.py file
- Implement exactly the routes and logic specified in design_spec.md
- Do not read or depend on frontend templates or sibling outputs
- Focus solely on backend implementation from design_spec.md

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for web applications.

Your goal is to develop all HTML templates for the nine specified pages with exact element IDs, layout, and navigation per the design specifications.

Task Details:
- Read design_spec.md from CONTEXT as the only input artifact
- Independently create templates/*.html files for all required pages
- Use exact element IDs and structure defined in design_spec.md
- Generate well-structured, semantic HTML with Jinja2 variable placeholders as needed
- Do not access backend code or sibling agent outputs

**Implementation Requirements:**
- Create one HTML template file per page described in design_spec.md (total nine pages)
- Assign exact IDs to elements as specified (buttons, div containers, inputs, tables, etc.)
- Include navigation elements linking pages per design_spec.md requirements
- Apply consistent page titles and headers
- Use Jinja2 syntax for dynamic content placeholders consistent with backend design

**Example Code Snippet:**
''' 
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <div id="dashboard-page">
        <!-- Featured auctions section -->
        <!-- Buttons with IDs like browse-auctions-button -->
    </div>
</body>
</html>
'''

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output all templates as templates/*.html
- Follow design_spec.md strictly for element IDs and page structure
- Templates are independently complete without backend code access
- Do not read backend code or sibling outputs

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integrator specializing in Flask backend and frontend template integration.

Your goal is to merge and reconcile the backend app.py and frontend templates into a consistent, executable application bundle.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify that Flask route handlers in app.py match template files and element IDs in templates/*.html
- Identify and correct interface mismatches such as route names, template references, and context variables
- Produce final merged app.py and templates/*.html artifacts that are ready for deployment
- Do not modify design_spec.md or add new requirements

**Integration and Validation Steps:**
- Validate that all route endpoints in app.py have corresponding HTML templates with correct element IDs
- Ensure navigation links in templates point to Flask routes in app.py accurately
- Check that data placeholders in templates match context variables passed by app.py
- Fix any discrepancies in filenames, variable names, or routing logic without altering design intent
- Confirm file I/O and data handling remains consistent with design_spec.md

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output finalized app.py and templates/*.html
- Integration covers all features specified in design_spec.md
- Outputs are coherent and runnable as a single Flask application
- Do not alter design_spec.md or add features beyond input artifacts

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
        ("DesignMerger", """Check backend design completeness and correctness against user task and compatibility with frontend design.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend design adherence to user requirements and backend design integration feasibility.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify backend implementation matches route, data handling, and business logic in design_spec.md precisely.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify frontend templates conform to design_spec.md element IDs, layout, and navigation requirements.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
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
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of backend and frontend design architecture
    await asyncio.gather(
        execute(BackendDesignArchitect,
                "Read user_task_description and produce backend_design.md detailing Flask routes, backend logic, data file schemas, "
                "data management for auctions, bids, winners, items, trending and category routes."),
        execute(FrontendDesignArchitect,
                "Read user_task_description and produce frontend_design.md detailing all HTML templates, element IDs, page structures, "
                "navigation flows for nine application pages.")
    )

    # Read backend and frontend design outputs for merging
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

    # Merge backend and frontend designs into unified design_spec.md
    await execute(DesignMerger,
                  f"Merge backend_design.md and frontend_design.md with strict consistency and adherence to user_task_description.\n\n"
                  f"=== Backend Design ===\n{backend_design_content}\n\n"
                  f"=== Frontend Design ===\n{frontend_design_content}")
# Phase1_End

# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of backend and frontend implementation
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement the complete Flask backend app.py based on design_spec.md from CONTEXT. "
                "Include all routing, business logic, and data management per specifications."),
        execute(FrontendDeveloper,
                "Implement nine HTML template files in templates/*.html with exact element IDs and navigation strictly following design_spec.md from CONTEXT.")
    )

    # Read outputs from BackendDeveloper and FrontendDeveloper
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Execute IntegrationMerger to merge backend and frontend into final output
    await execute(
        IntegrationMerger,
        "Integrate and reconcile backend app.py and frontend templates from design_spec.md, app.py, and templates/*.html. "
        "Ensure all Flask routes match HTML templates and element IDs, fix interface mismatches, and produce final app.py and templates/*.html.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
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
