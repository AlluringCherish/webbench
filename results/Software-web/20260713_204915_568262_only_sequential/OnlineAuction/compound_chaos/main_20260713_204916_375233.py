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
# 20260713_204916_375233/main_20260713_204916_375233.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the OnlineAuction requirements and produce a complete design_spec.md covering Flask routes, templates, page titles, element IDs, and data file usage.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first writes requirements_analysis.md with detailed tracing of all UI elements, data files, and user flows; then WebArchitect reads requirements_analysis.md \"\n        \"and writes design_spec.md defining Flask routes, template filenames, page titles, element IDs, data handling contracts for text files, and navigation flow including the Dashboard as start page.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Business Analyst specializing in detailed requirements analysis for web applications.\n\nYour goal is to thoroughly analyze the OnlineAuction user requirements to produce a comprehensive requirements_analysis.md that captures every UI element, page, navigation flow, and data file interaction.\n\nTask Details:\n- Read the full user_task_description input artifact\n- Trace all pages and extract exact page titles, external template filenames, element IDs, action buttons, search and filter options\n- Identify all referenced data files and their usage contexts\n- Produce one detailed Markdown file requirements_analysis.md capturing these\n\nAnalysis Requirements:\n1. For each page:\n   - List the exact template filename and page-to-template mapping\n   - Extract and list the exact page title string\n   - Enumerate all element IDs with their element types and descriptions\n   - Note all buttons, inputs, search/filter elements, including dynamic IDs with patterns\n2. Document data file usage and mapping to UI elements if any\n3. Capture navigation flows, especially buttons linking pages, and highlight Dashboard as the start page\n4. Present findings in a clear, organized Markdown document\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save requirements_analysis.md\n- File must be human-readable with clear sections for each page and data file\n- Provide comprehensive coverage of ALL UI elements and data relations described in user input\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application design and specification.\n\nYour goal is to convert detailed requirements analysis into a precise design_spec.md that fully specifies Flask routes, HTTP methods, page titles, element IDs, navigation, context variables, and data file handling conventions.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md inputs\n- Create design_spec.md defining:\n   - Flask route paths and HTTP methods for each user page, ensuring the root route '/' redirects to the Dashboard page\n   - Exact template filenames for all pages\n   - Precise page titles and all element IDs per page\n   - Navigation mappings with routing function names and URLs\n   - Context variables passed to templates aligning with UI elements and data files\n   - Data file handling contracts for auctions.txt, bids.txt, categories.txt, winners.txt, bid_history.txt, items.txt, trending.txt including field order and usage\n\nSpecification Requirements:\n1. Flask Routes:\n   - For each page, define the route path, HTTP method(s), route function name (lowercase_with_underscores), and associated template filename\n2. Templates:\n   - List all element IDs required in each page template along with descriptions\n3. Navigation:\n   - Specify navigation actions with exact url_for() function calls\n4. Data Files:\n   - For each data file, specify path and exact pipe-delimited fields with order, usage, and examples\n5. Enforce Dashboard page as the start/root page with route '/' redirecting there\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- All route function names, template names, element IDs, and context variables must match user requirements precisely\n- Provide complete and unambiguous design details enabling backend and frontend parallel implementation without ambiguity\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md includes all pages, exact element IDs, navigation paths, data file references, and UI elements as specified in user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement the OnlineAuction web application with Flask app.py and templates/*.html files adhering to design_spec.md and using local text file data.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes app_draft.py and all templates_draft/*.html according to design_spec.md, configuring routes, page titles, element IDs, UI interactions, and data parsing from text files; then IntegrationEngineer integrates drafts into final app.py and templates/*.html optimized for Flask rendering and stable functionality.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Backend Developer and Frontend Developer skilled in Flask web development and HTML templating.\n\nYour goal is to draft a complete Flask backend script (app_draft.py) and corresponding HTML templates (templates_draft/*.html) based strictly on the provided design specification.\n\nTask Details:\n- Read user_task_description and design_spec.md carefully to ensure full coverage\n- Produce app_draft.py implementing all Flask routes with required HTTP methods\n- Implement data loading and parsing logic from local text files exactly as specified\n- Create all templates_draft/*.html files with exact element IDs, page titles, navigation buttons, forms, and content display per design_spec.md\n- Focus solely on drafting versions; do not finalize or refactor for production\n\nBackend Implementation Guidelines:\n1. Define Flask app with necessary imports and configuration\n2. Implement each route handling GET/POST as specified with correct function names\n3. Load and parse text data files with exact field order and no header lines\n4. Map parsed data to context variables passed to templates faithfully\n5. Handle errors gracefully and ensure app draft runs without syntax errors\n\nFrontend Implementation Guidelines:\n1. For each HTML template, include all specified page titles in <title> and <h1> tags\n2. Use exact element IDs as specified (including dynamic IDs with Jinja2 syntax)\n3. Implement navigation buttons and links directing to correct Flask routes\n4. Implement forms with proper method and input field IDs matching design_spec.md\n5. Use Jinja2 templating to iterate over data and conditionally display elements\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- Follow design_spec.md exactly on routing, IDs, page titles, and data fields\n- Ensure data parsing strictly matches file formats in the specification\n- Do not finalize or optimize beyond a clean working draft stage\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web applications and frontend-backend integration.\n\nYour goal is to produce a final, runnable Flask backend (app.py) and finalized HTML templates (templates/*.html) by integrating draft implementations.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html thoroughly\n- Integrate routes and functionality from app_draft.py into a clean, error-free app.py\n- Relocate templates from templates_draft/*.html into templates/*.html, adjusting paths as necessary\n- Ensure Flask app.py runs correctly with proper configuration and dependency handling\n- Verify all page titles, element IDs, UI interactions, and navigation flows are correct and consistent\n- Confirm data parsing reads from local text files exactly per specification and handles all cases robustly\n\nIntegration and Finalization Guidelines:\n1. Refactor draft code if needed for stability and maintainability, while preserving original route logic\n2. Adjust template file paths and includes to reflect the final templates/ directory structure\n3. Validate that all navigation and buttons redirect correctly between pages\n4. Confirm presence and correctness of all element IDs and page titles as per design_spec.md\n5. Perform sanity checks to ensure all required data fields are loaded and presented accurately\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html files\n- Maintain strict adherence to design_spec.md and user_task_description\n- Ensure final app.py is runnable and templates load flawlessly\n- Do not introduce functionality not covered in drafts or design specification\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Check that app_draft.py and templates_draft/*.html adhere to design_spec.md exactly with correct routes, element IDs, page titles, data handling, and UI elements before integration.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate app.py and templates/*.html through syntax, runtime, and functionality checks; produce validation_report.md and final corrected application.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator validates app.py and templates/*.html for syntax, execution, route correctness, page rendering, UI element presence, navigation, and data file integration writing validation_report.md; then SequentialFixer updates app.py and templates/*.html resolving issues to deliver a fully compliant final application.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in validating Python Flask web applications with HTML templating.\n\nYour goal is to validate the complete web application including backend and frontend components to ensure syntax correctness, successful runtime, accurate routing, UI presence, navigation fidelity, and proper data integration. Deliver a detailed validation_report.md summarizing all findings.\n\nTask Details:\n- Read user_task_description describing functional requirements and UI elements\n- Read design_spec.md specifying complete app.py and templates/*.html specifications\n- Read app.py and templates/*.html for actual implementation to validate\n- Produce validation_report.md including detailed diagnostics and issues\n\n**Validation Tasks**\n\n1. **Syntax and Runtime Checks:**\n   - Use validate_python_file tool for syntax and runtime validation of app.py\n   - Execute app.py if needed to ensure startup succeeds without errors\n\n2. **Route and Page Functionality Testing:**\n   - Use Flask test client or appropriate execute_python_code calls to test all routes\n   - Verify correct HTTP methods are accepted and rendered pages are returned\n   - Confirm root route redirects to dashboard\n\n3. **UI Element Presence and Attributes:**\n   - Parse rendered HTML for required element IDs on each page as specified in design_spec.md\n   - Verify element types and presence of dynamic ID patterns (e.g., view-auction-button-{auction_id})\n   - Confirm page titles match exactly those specified in user_task_description and design_spec.md\n\n4. **Navigation Functionality:**\n   - Test navigation buttons and links for correct url_for routing\n   - Confirm all navigation elements function properly on all pages\n\n5. **Data Integration Validation:**\n   - Verify data files (auctions.txt, bids.txt, categories.txt, etc.) are loaded and reflected accurately in page content\n   - Check filtering, sorting, and listing features incorporate data file contents correctly\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools for automated validation steps\n- Write detailed issues and confirmations in validation_report.md using write_text_file tool\n- Validation report MUST cover syntax, runtime, routing, UI elements, navigation, and data integration comprehensively\n- Focus strictly on implemented files: app.py and templates/*.html in context of design_spec.md and user requirements\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in debugging and refining Flask web applications with HTML templating.\n\nYour goal is to apply all corrections and improvements detailed in validation_report.md to produce a fully working, standards-compliant final app.py and templates/*.html set that satisfies all original user requirements and design specifications.\n\nTask Details:\n- Read user_task_description for functional and UI requirements\n- Read design_spec.md for detailed implementation specifications\n- Read current app.py and templates/*.html files as baseline code\n- Read validation_report.md identifying all problems, bugs, and enhancement suggestions\n- Deliver corrected app.py and templates/*.html fully addressing all validation findings\n\n**Refinement Guidelines**\n\n1. **Bug Fixing:**\n   - Resolve all syntax and runtime errors in app.py\n   - Fix missing or incorrect Flask routes, context variables, and HTTP methods\n   - Correct form submissions and POST handling as needed\n\n2. **UI Corrections:**\n   - Add or fix all required element IDs and dynamic ID patterns in templates\n   - Ensure page titles and content match user requirements exactly\n   - Repair broken or missing navigation elements and routing links\n\n3. **Data Handling Improvements:**\n   - Correct data loading and filtering logic to match data files like auctions.txt, bids.txt, etc.\n   - Validate that displayed content reflects accurate and complete data from source files\n\n4. **Best Practices:**\n   - Maintain consistent code style and naming conventions per design_spec.md\n   - Verify no functionality regressions are introduced\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save corrected app.py and templates/*.html files\n- Focus exclusively on fixing issues reported in validation_report.md\n- Preserve functionality and features specified in user_task_description and design_spec.md\n- Do not add new features beyond validation corrections\n\nOutput: app.py; templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Ensure validation_report.md includes complete and actionable information about syntax, runtime, routing, template correctness, UI elements, and data integration issues.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify final app.py and templates/*.html fully satisfy user requirements and resolve all issues reported in validation_report.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Business Analyst specializing in detailed requirements analysis for web applications.

Your goal is to thoroughly analyze the OnlineAuction user requirements to produce a comprehensive requirements_analysis.md that captures every UI element, page, navigation flow, and data file interaction.

Task Details:
- Read the full user_task_description input artifact
- Trace all pages and extract exact page titles, external template filenames, element IDs, action buttons, search and filter options
- Identify all referenced data files and their usage contexts
- Produce one detailed Markdown file requirements_analysis.md capturing these

Analysis Requirements:
1. For each page:
   - List the exact template filename and page-to-template mapping
   - Extract and list the exact page title string
   - Enumerate all element IDs with their element types and descriptions
   - Note all buttons, inputs, search/filter elements, including dynamic IDs with patterns
2. Document data file usage and mapping to UI elements if any
3. Capture navigation flows, especially buttons linking pages, and highlight Dashboard as the start page
4. Present findings in a clear, organized Markdown document

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save requirements_analysis.md
- File must be human-readable with clear sections for each page and data file
- Provide comprehensive coverage of ALL UI elements and data relations described in user input

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application design and specification.

Your goal is to convert detailed requirements analysis into a precise design_spec.md that fully specifies Flask routes, HTTP methods, page titles, element IDs, navigation, context variables, and data file handling conventions.

Task Details:
- Read user_task_description and requirements_analysis.md inputs
- Create design_spec.md defining:
   - Flask route paths and HTTP methods for each user page, ensuring the root route '/' redirects to the Dashboard page
   - Exact template filenames for all pages
   - Precise page titles and all element IDs per page
   - Navigation mappings with routing function names and URLs
   - Context variables passed to templates aligning with UI elements and data files
   - Data file handling contracts for auctions.txt, bids.txt, categories.txt, winners.txt, bid_history.txt, items.txt, trending.txt including field order and usage

Specification Requirements:
1. Flask Routes:
   - For each page, define the route path, HTTP method(s), route function name (lowercase_with_underscores), and associated template filename
2. Templates:
   - List all element IDs required in each page template along with descriptions
3. Navigation:
   - Specify navigation actions with exact url_for() function calls
4. Data Files:
   - For each data file, specify path and exact pipe-delimited fields with order, usage, and examples
5. Enforce Dashboard page as the start/root page with route '/' redirecting there

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- All route function names, template names, element IDs, and context variables must match user requirements precisely
- Provide complete and unambiguous design details enabling backend and frontend parallel implementation without ambiguity

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Backend Developer and Frontend Developer skilled in Flask web development and HTML templating.

Your goal is to draft a complete Flask backend script (app_draft.py) and corresponding HTML templates (templates_draft/*.html) based strictly on the provided design specification.

Task Details:
- Read user_task_description and design_spec.md carefully to ensure full coverage
- Produce app_draft.py implementing all Flask routes with required HTTP methods
- Implement data loading and parsing logic from local text files exactly as specified
- Create all templates_draft/*.html files with exact element IDs, page titles, navigation buttons, forms, and content display per design_spec.md
- Focus solely on drafting versions; do not finalize or refactor for production

Backend Implementation Guidelines:
1. Define Flask app with necessary imports and configuration
2. Implement each route handling GET/POST as specified with correct function names
3. Load and parse text data files with exact field order and no header lines
4. Map parsed data to context variables passed to templates faithfully
5. Handle errors gracefully and ensure app draft runs without syntax errors

Frontend Implementation Guidelines:
1. For each HTML template, include all specified page titles in <title> and <h1> tags
2. Use exact element IDs as specified (including dynamic IDs with Jinja2 syntax)
3. Implement navigation buttons and links directing to correct Flask routes
4. Implement forms with proper method and input field IDs matching design_spec.md
5. Use Jinja2 templating to iterate over data and conditionally display elements

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Follow design_spec.md exactly on routing, IDs, page titles, and data fields
- Ensure data parsing strictly matches file formats in the specification
- Do not finalize or optimize beyond a clean working draft stage

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web applications and frontend-backend integration.

Your goal is to produce a final, runnable Flask backend (app.py) and finalized HTML templates (templates/*.html) by integrating draft implementations.

Task Details:
- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html thoroughly
- Integrate routes and functionality from app_draft.py into a clean, error-free app.py
- Relocate templates from templates_draft/*.html into templates/*.html, adjusting paths as necessary
- Ensure Flask app.py runs correctly with proper configuration and dependency handling
- Verify all page titles, element IDs, UI interactions, and navigation flows are correct and consistent
- Confirm data parsing reads from local text files exactly per specification and handles all cases robustly

Integration and Finalization Guidelines:
1. Refactor draft code if needed for stability and maintainability, while preserving original route logic
2. Adjust template file paths and includes to reflect the final templates/ directory structure
3. Validate that all navigation and buttons redirect correctly between pages
4. Confirm presence and correctness of all element IDs and page titles as per design_spec.md
5. Perform sanity checks to ensure all required data fields are loaded and presented accurately

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Maintain strict adherence to design_spec.md and user_task_description
- Ensure final app.py is runnable and templates load flawlessly
- Do not introduce functionality not covered in drafts or design specification

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in validating Python Flask web applications with HTML templating.

Your goal is to validate the complete web application including backend and frontend components to ensure syntax correctness, successful runtime, accurate routing, UI presence, navigation fidelity, and proper data integration. Deliver a detailed validation_report.md summarizing all findings.

Task Details:
- Read user_task_description describing functional requirements and UI elements
- Read design_spec.md specifying complete app.py and templates/*.html specifications
- Read app.py and templates/*.html for actual implementation to validate
- Produce validation_report.md including detailed diagnostics and issues

**Validation Tasks**

1. **Syntax and Runtime Checks:**
   - Use validate_python_file tool for syntax and runtime validation of app.py
   - Execute app.py if needed to ensure startup succeeds without errors

2. **Route and Page Functionality Testing:**
   - Use Flask test client or appropriate execute_python_code calls to test all routes
   - Verify correct HTTP methods are accepted and rendered pages are returned
   - Confirm root route redirects to dashboard

3. **UI Element Presence and Attributes:**
   - Parse rendered HTML for required element IDs on each page as specified in design_spec.md
   - Verify element types and presence of dynamic ID patterns (e.g., view-auction-button-{auction_id})
   - Confirm page titles match exactly those specified in user_task_description and design_spec.md

4. **Navigation Functionality:**
   - Test navigation buttons and links for correct url_for routing
   - Confirm all navigation elements function properly on all pages

5. **Data Integration Validation:**
   - Verify data files (auctions.txt, bids.txt, categories.txt, etc.) are loaded and reflected accurately in page content
   - Check filtering, sorting, and listing features incorporate data file contents correctly

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for automated validation steps
- Write detailed issues and confirmations in validation_report.md using write_text_file tool
- Validation report MUST cover syntax, runtime, routing, UI elements, navigation, and data integration comprehensively
- Focus strictly on implemented files: app.py and templates/*.html in context of design_spec.md and user requirements

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in debugging and refining Flask web applications with HTML templating.

Your goal is to apply all corrections and improvements detailed in validation_report.md to produce a fully working, standards-compliant final app.py and templates/*.html set that satisfies all original user requirements and design specifications.

Task Details:
- Read user_task_description for functional and UI requirements
- Read design_spec.md for detailed implementation specifications
- Read current app.py and templates/*.html files as baseline code
- Read validation_report.md identifying all problems, bugs, and enhancement suggestions
- Deliver corrected app.py and templates/*.html fully addressing all validation findings

**Refinement Guidelines**

1. **Bug Fixing:**
   - Resolve all syntax and runtime errors in app.py
   - Fix missing or incorrect Flask routes, context variables, and HTTP methods
   - Correct form submissions and POST handling as needed

2. **UI Corrections:**
   - Add or fix all required element IDs and dynamic ID patterns in templates
   - Ensure page titles and content match user requirements exactly
   - Repair broken or missing navigation elements and routing links

3. **Data Handling Improvements:**
   - Correct data loading and filtering logic to match data files like auctions.txt, bids.txt, etc.
   - Validate that displayed content reflects accurate and complete data from source files

4. **Best Practices:**
   - Maintain consistent code style and naming conventions per design_spec.md
   - Verify no functionality regressions are introduced

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html files
- Focus exclusively on fixing issues reported in validation_report.md
- Preserve functionality and features specified in user_task_description and design_spec.md
- Do not add new features beyond validation corrections

Output: app.py; templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md includes all pages, exact element IDs, navigation paths, data file references, and UI elements as specified in user requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Check that app_draft.py and templates_draft/*.html adhere to design_spec.md exactly with correct routes, element IDs, page titles, data handling, and UI elements before integration.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Ensure validation_report.md includes complete and actionable information about syntax, runtime, routing, template correctness, UI elements, and data integration issues.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify final app.py and templates/*.html fully satisfy user requirements and resolve all issues reported in validation_report.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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

    # Sequential execution: RequirementsAnalyst then WebArchitect
    await execute(RequirementsAnalyst, "Analyze user_task_description and produce detailed requirements_analysis.md capturing all UI elements, pages, templates, element IDs, buttons, filters, data files, and navigation flows including Dashboard as start page.")
    
    # Read requirements_analysis.md content for WebArchitect input injection
    requirements_analysis_md = ""
    try:
        requirements_analysis_md = open("requirements_analysis.md").read()
    except Exception:
        pass

    await execute(WebArchitect, f"Based on user_task_description and the following requirements_analysis.md content, produce a detailed design_spec.md specifying Flask routes, HTTP methods, route function names, template filenames, page titles, element IDs, navigation mappings, context variables, and data file handling contracts including start page redirect to Dashboard.\n\n=== requirements_analysis.md ===\n{requirements_analysis_md}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=350,
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential execution: DraftEngineer first, then IntegrationEngineer
    await execute(DraftEngineer,
                  "Draft app_draft.py implementing all Flask routes with correct HTTP methods and data loading from text files. "
                  "Draft all templates_draft/*.html with exact element IDs, page titles, navigation buttons, forms and content per design_spec.md.")
    
    # Reading the outputs of drafts for injection
    app_draft_code = ""
    templates_draft_code = ""
    try:
        app_draft_code = open("app_draft.py").read()
    except Exception:
        pass
    try:
        # As templates_draft/*.html is a glob pattern, injection here will be generic.
        # In practice, multiple files would be read; here just try to read one or leave empty.
        # We inject all drafts content read from templates_draft/*.html files, but here simplified.
        templates_draft_code = open("templates_draft/index.html").read()
    except Exception:
        pass

    await execute(IntegrationEngineer,
                  f"Integrate draft implementations by reading app_draft.py and templates_draft/*.html. "
                  f"Produce final app.py and templates/*.html files, ensuring adherence to design_spec.md and runnable Flask app.\n\n"
                  f"=== app_draft.py ===\n{app_draft_code}\n\n=== templates_draft examples ===\n{templates_draft_code}")
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
        failure_threshold=1,
        recovery_time=45
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
        failure_threshold=1,
        recovery_time=45
    )

    # Sequential execution of validation and fixing
    await execute(WebValidator,
                  "Validate app.py and all templates/*.html with syntax, runtime, routing, UI element presence, navigation, and data integration. "
                  "Write detailed validation_report.md.")

    # Read validation report content to inject into fixer
    validation_report_content = ""
    try:
        with open("validation_report.md", "r") as f:
            validation_report_content = f.read()
    except FileNotFoundError:
        validation_report_content = ""

    await execute(SequentialFixer,
                  "Apply all corrections in validation_report.md to app.py and templates/*.html. "
                  "Produce corrected final app.py and templates/*.html."

                  f"\n=== Validation Report ===\n{validation_report_content}")
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
