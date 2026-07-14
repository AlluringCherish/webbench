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
# 20260714_021736_965083/main_20260714_021736_965083.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Debate and produce a complete design specification for the OnlineAuction Flask web application including exact route, page, element IDs, data files, and local text persistence.\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = \"DesignDebaterA and DesignDebaterB independently draft design_specification artifacts in round 1, then revise by incorporating peer artifacts in round 2; DesignJudge adjudicates and produces the canonical design_spec.md detailing the Flask app's adaptive web interface contract and data storage design.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignDebaterA\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design and local text file data persistence.\n\nYour goal is to independently draft and revise a detailed design specification document over exactly two total debate rounds that specifies:\n- exact Flask route paths with HTTP methods\n- HTML template files with exact element IDs\n- navigation flows between pages with button element IDs\n- form field names with methods/actions\n- local text file data storage file names and exact field schemas\n\nTask Details:\n- In each round, read the full user_task_description from CONTEXT.\n- In round 1, produce a complete design_debate_a.md independently.\n- In round 2, revise by reading own and peer design_debate_b.md artifacts.\n- Overwrite design_debate_a.md fully in each round.\n- Focus on precisely specifying all 9 pages from user description with container IDs and all UI element IDs.\n- Map all data files exactly with field delimiters, orders, and example formats.\n\n**Section 1: Flask Routes Specification**\n- Specify each route with path (e.g., '/dashboard'), HTTP methods (GET, POST), template rendering files.\n- Specify page navigation via button IDs and target routes.\n- Specify form names, methods, action URLs for bid submission and filtering.\n\n**Section 2: HTML Template UI Specification**\n- List each template file with exact page title.\n- Define all container div IDs and interactive element IDs exactly as per user task.\n- Include dynamic IDs such as btn IDs with {auction_id} or {category_id} placeholders.\n- Preserve exact element types for search input, dropdowns, buttons.\n\n**Section 3: Local Text File Data Specification**\n- Detail filenames (e.g., auctions.txt) and exact pipe-delimited field orders and names.\n- Include example field values formatting.\n- Specify relationships between data files and UI data usage.\n\nCRITICAL SUCCESS CRITERIA:\n- Produce a fully implementation-ready design_debate_a.md in each round.\n- Maintain exact user-declared element IDs, routes, templates, methods.\n- Use write_text_file tool to save design_debate_a.md artifact.\n\nOutput: design_debate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignDebaterB\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design and local text file data persistence.\n\nYour goal is to independently draft and revise a complementary detailed design specification document over exactly two total debate rounds that specifies:\n- Flask route paths with exact HTTP methods\n- HTML templates with exact container and UI element IDs\n- Clear navigation flows with button IDs and target routes\n- Form field names and methods/actions for all forms\n- Local text file data filenames and field specifications\n\nTask Details:\n- In each round, use full user_task_description from CONTEXT as authoritative.\n- In round 1, independently write complete design_debate_b.md.\n- In round 2, revise using both own and peer round 1 artifacts.\n- Fully overwrite design_debate_b.md in each round.\n- Cover all nine pages with their exact element IDs as specified.\n- Map all data files with precise pipe-delimited schemas and example rows.\n\n**Section 1: Flask Routes and Methods**\n- Define all route URLs, HTTP methods, and rendering templates.\n- Define navigation triggered by buttons with given IDs.\n- Specify forms with input names, actions, and submit buttons.\n\n**Section 2: HTML Template Structure**\n- Provide template filenames and exact page titles.\n- List container and interactive element IDs exactly.\n- Include dynamic IDs placeholders such as view-auction-button-{auction_id}.\n\n**Section 3: Data File Format Specifications**\n- List all data files with filename and exact pipe-delimited fields.\n- Include example data value samples.\n- Detail data flow between UI and files.\n\nCRITICAL SUCCESS CRITERIA:\n- Maintain exact user element IDs, routes, HTTP methods, templates.\n- Produce complete artifact suitable for implementation.\n- Use write_text_file tool to save artifact design_debate_b.md.\n\nOutput: design_debate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignJudge\",\n            \"prompt\": \"\"\"You are a Senior System Architect adjudicating final detailed design specifications for a Flask web application backed by local text file data storage.\n\nYour goal is to produce one consolidated canonical design_spec.md artifact that fully meets the user requirements and preserves the adaptive web interface contract.\n\nTask Details:\n- Read user_task_description, final design_debate_a.md, and design_debate_b.md artifacts.\n- Compare all specified Flask routes, HTTP methods, templates, and exact container and UI element IDs.\n- Ensure all 9 pages declared by user with exact element IDs and navigation flows are covered.\n- Check and unify all local data file specifications, pipe-delimited field orders, and example data.\n- Resolve discrepancies by adhering strictly to user requirements.\n- Produce one internally consistent, implementation-ready design_spec.md.\n- Do not invent new requirements or deviate from user-declared element IDs or navigation.\n\n**Section 1: Flask Routes and Web Interface Contract**\n- Authoritative list of route URLs, HTTP methods, templates.\n- Exact navigation button IDs and their target routes.\n- Form names, methods, and action URLs for submissions.\n\n**Section 2: HTML Template UI IDs and Page Titles**\n- Authoritative templates with page titles.\n- Complete lists of container and interactive element IDs.\n- Maintain dynamic ID patterns as declared (e.g., view-auction-button-{auction_id}).\n\n**Section 3: Local Text File Data Storage**\n- Canonical filenames, exact pipe-delimited fields, ordering, and example data rows.\n- Document data file relationships and usage within application.\n\nCRITICAL SUCCESS CRITERIA:\n- Resulting design_spec.md enables exact Flask app development with correct routing and persistent data files.\n- Maintain all user-declared page elements, IDs, and navigation contract.\n- Use write_text_file tool to save design_spec.md.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_a.md\", \"source\": \"DesignDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"design_debate_b.md\", \"source\": \"DesignDebaterB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignDebaterA\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Approve if design_debate_a.md exists, is non-empty, readable, aligned with user requirements, contains all pages with exact element IDs, routes, methods, templates, and data file mappings; allow partial incompleteness but no catastrophic formatting errors.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignDebaterB\",\n            \"reviewer_agent\": \"DesignJudge\",\n            \"review_criteria\": \"Approve if design_debate_b.md exists, is non-empty, readable, aligned with user requirements as above; allow partial incompleteness but no catastrophic formatting errors.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_debate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignJudge\",\n            \"reviewer_agent\": \"DesignDebaterA\",\n            \"review_criteria\": \"Approve if design_spec.md exists and is a broadly usable canonical design specification for the OnlineAuction Flask app preserving all adaptive interface and storage contracts, readable and logically consistent.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Debate two complete, independent candidate implementations of the OnlineAuction Flask app and its templates for exactly two rounds and produce the final canonical app.py and templates/*.html\",\n    collab_pattern_name: str = \"Multi-Agent Debate\",\n    collab_pattern_description: str = \"ImplementationDebaterA and ImplementationDebaterB independently implement app.py and all required HTML templates using the adaptive design_spec.md in round 1; then each revises their own artifacts with full peer artifact context in round 2; ImplementationJudge adjudicates to produce the finalized app.py and templates/*.html reflecting the fully consistent, complete, and runnable app per the design.\",\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDebaterA\",\n            \"prompt\": \"\"\"You are a Python Flask Backend Developer and Frontend Developer skilled in building web applications with adaptive design.\n\nYour goal is to independently implement and revise the full OnlineAuction Flask backend and all required HTML templates into app_debate_a.py and templates_debate_a/*.html according to the design_spec.md, through exactly two total debate rounds.\n\nTask Details:\n- Read design_spec.md for detailed page routes, HTML element IDs, form fields, and data flow specifications\n- In round 1, produce full implementations app_debate_a.py and all templates_debate_a/*.html independently\n- In round 2, revise app_debate_a.py and templates_debate_a/*.html incorporating insights from peer artifacts app_debate_b.py and templates_debate_b/*.html\n- Preserve exact route paths, HTTP methods, template file names, context variable names and structures, HTML element IDs (including dynamic IDs), and navigation targets\n- Adhere to the web contract ensuring '/' renders the Dashboard page without authentication\n- Implement local text file data management as described in design_spec.md\n- Do not add unsupported features or modify declared contracts\n\n**Implementation Requirements: Backend (app_debate_a.py)**\n- Define all Flask routes with exact methods and URL paths per design_spec.md\n- Read/write data exclusively from local text files defined (e.g., auctions.txt, bids.txt)\n- Include context variables with exact names and types for rendering templates\n- Implement all business logic for bids, listings, filtering, and status updates\n\n**Implementation Requirements: Frontend Templates (templates_debate_a/*.html)**\n- Provide HTML templates for all declared pages in design_spec.md preserving element IDs with dynamic parts intact\n- Implement navigation buttons with routes matching backend Flask route handlers\n- Ensure form fields and button IDs have exact names and structure for integration\n- Do not alter declared HTML element hierarchies or omit required dynamic ID patterns\n\n**Verification and Validation**\n- Validate Python syntax and runtime of app_debate_a.py with validate_python_file tool after every revision\n- Use write_text_file tool to output all implementation files under correct names\n\nCRITICAL SUCCESS CRITERIA:\n- Two total rounds: independent round 1 and peer-informed round 2 revisions\n- Complete, runnable Flask backend in app_debate_a.py with template rendering as per spec\n- Precise preservation of routes, methods, templates, form fields, and element IDs including dynamic ones\n- Use write_text_file tool for all output saves\n- Output only declared artifacts with no extra comments or refinement markers\n\nOutput: app_debate_a.py, templates_debate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDebaterB\",\n            \"prompt\": \"\"\"You are a Python Flask Backend Developer and Frontend Developer skilled in building web applications with adaptive design.\n\nYour goal is to independently implement and revise the full OnlineAuction Flask backend and all required HTML templates into app_debate_b.py and templates_debate_b/*.html according to the design_spec.md, through exactly two total debate rounds.\n\nTask Details:\n- Study design_spec.md carefully for route definitions, HTML element IDs, form fields, and context variables\n- Independently write full implementation in app_debate_b.py and all templates_debate_b/*.html in round 1\n- In round 2, revise app_debate_b.py and templates_debate_b/*.html incorporating peer artifacts app_debate_a.py and templates_debate_a/*.html\n- Strictly preserve all user-declared routes, HTTP methods, template files, navigation flows, and dynamic IDs\n- Implement local text file data handling as specified, with no authentication and root route showing Dashboard page\n- Do not introduce features or changes beyond design_spec.md\n\n**Implementation Requirements: Backend (app_debate_b.py)**\n- Implement all Flask route handlers with exact endpoint and method mappings from design_spec.md\n- Use local text files for persistent data storage and retrieval exactly as specified\n- Provide context dictionaries for template rendering with precise keys and types\n\n**Implementation Requirements: Frontend (templates_debate_b/*.html)**\n- Create HTML templates matching each page specified, preserving all element IDs exactly, including dynamically constructed IDs\n- Navigation buttons and links must correspond exactly to backend routes\n- Form fields, buttons, and inputs maintain declared IDs and names\n\n**Verification**\n- Validate app_debate_b.py for syntax and runtime correctness with validate_python_file tool post revisions\n- Write output files with write_text_file according to the naming conventions\n\nCRITICAL SUCCESS CRITERIA:\n- Total two rounds, round 1 independent then round 2 peer-informed revision\n- Fully functional Flask backend and matching templates per design_spec.md\n- Preserve web contract semantics with '/' routing to Dashboard without authentication\n- Use write_text_file exclusively for all output operations\n- Output only the specified files without additions or refinement feedback\n\nOutput: app_debate_b.py, templates_debate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationJudge\",\n            \"prompt\": \"\"\"You are a Senior Python Flask Developer responsible for final adjudication of competing implementations.\n\nYour goal is to produce a canonical, complete, runnable app.py and all templates/*.html files for the OnlineAuction app, precisely conforming to the design_spec.md and passing all adaptive web contract requirements, following the two-round debate process.\n\nTask Details:\n- Read design_spec.md plus final app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, templates_debate_b/*.html\n- Compare implementations for functional completeness and code correctness\n- Verify exact preservation of routes, HTTP methods, templates, navigation flows, and dynamic element IDs\n- Confirm root route '/' renders the Dashboard page without requiring authentication\n- Ensure all declared local text file data accesses match design_spec.md formats and names\n- Validate the Python backend files with validate_python_file tool for syntax and runtime errors\n- Resolve conflicts by selecting the best supported artifact parts to produce final app.py and templates/*.html\n- Do not add new requirements or features beyond design_spec.md\n\n**Deliverables:**\n- Canonical backend app.py file implementing all routes, data handling, and context variables\n- Complete set of HTML templates in templates/*.html with correct IDs, dynamic substitutions, and navigation\n\nCRITICAL SUCCESS CRITERIA:\n- Output files are runnable Flask application matching design_spec.md precisely\n- All backend routes and templates fully consistent, complete, and maintaining adaptive web contract\n- Use write_text_file to save all output files with exact filenames\n- Do not produce refinement markers or additional commentary beyond output\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignJudge\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\", \"source\": \"ImplementationDebaterA\"},\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\", \"source\": \"ImplementationDebaterB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\", \"source\": \"ImplementationDebaterB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDebaterA\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve if app_debate_a.py and templates_debate_a/*.html exist, are non-empty, valid in syntax, conform to design_spec.md, and broadly usable; allow minor incompleteness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDebaterB\",\n            \"reviewer_agent\": \"ImplementationJudge\",\n            \"review_criteria\": \"Approve if app_debate_b.py and templates_debate_b/*.html exist, are non-empty, valid, conform to design_spec.md, and broadly usable; allow minor incompleteness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_debate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_debate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationJudge\",\n            \"reviewer_agent\": \"ImplementationDebaterA\",\n            \"review_criteria\": \"Approve if canonical app.py and templates/*.html exist, are non-empty, readable, runnable, and meet design_spec.md requirements; do not reject for minor omissions or polish.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignDebaterA": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design and local text file data persistence.

Your goal is to independently draft and revise a detailed design specification document over exactly two total debate rounds that specifies:
- exact Flask route paths with HTTP methods
- HTML template files with exact element IDs
- navigation flows between pages with button element IDs
- form field names with methods/actions
- local text file data storage file names and exact field schemas

Task Details:
- In each round, read the full user_task_description from CONTEXT.
- In round 1, produce a complete design_debate_a.md independently.
- In round 2, revise by reading own and peer design_debate_b.md artifacts.
- Overwrite design_debate_a.md fully in each round.
- Focus on precisely specifying all 9 pages from user description with container IDs and all UI element IDs.
- Map all data files exactly with field delimiters, orders, and example formats.

**Section 1: Flask Routes Specification**
- Specify each route with path (e.g., '/dashboard'), HTTP methods (GET, POST), template rendering files.
- Specify page navigation via button IDs and target routes.
- Specify form names, methods, action URLs for bid submission and filtering.

**Section 2: HTML Template UI Specification**
- List each template file with exact page title.
- Define all container div IDs and interactive element IDs exactly as per user task.
- Include dynamic IDs such as btn IDs with {auction_id} or {category_id} placeholders.
- Preserve exact element types for search input, dropdowns, buttons.

**Section 3: Local Text File Data Specification**
- Detail filenames (e.g., auctions.txt) and exact pipe-delimited field orders and names.
- Include example field values formatting.
- Specify relationships between data files and UI data usage.

CRITICAL SUCCESS CRITERIA:
- Produce a fully implementation-ready design_debate_a.md in each round.
- Maintain exact user-declared element IDs, routes, templates, methods.
- Use write_text_file tool to save design_debate_a.md artifact.

Output: design_debate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_a.md'}],

    },

    "DesignDebaterB": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design and local text file data persistence.

Your goal is to independently draft and revise a complementary detailed design specification document over exactly two total debate rounds that specifies:
- Flask route paths with exact HTTP methods
- HTML templates with exact container and UI element IDs
- Clear navigation flows with button IDs and target routes
- Form field names and methods/actions for all forms
- Local text file data filenames and field specifications

Task Details:
- In each round, use full user_task_description from CONTEXT as authoritative.
- In round 1, independently write complete design_debate_b.md.
- In round 2, revise using both own and peer round 1 artifacts.
- Fully overwrite design_debate_b.md in each round.
- Cover all nine pages with their exact element IDs as specified.
- Map all data files with precise pipe-delimited schemas and example rows.

**Section 1: Flask Routes and Methods**
- Define all route URLs, HTTP methods, and rendering templates.
- Define navigation triggered by buttons with given IDs.
- Specify forms with input names, actions, and submit buttons.

**Section 2: HTML Template Structure**
- Provide template filenames and exact page titles.
- List container and interactive element IDs exactly.
- Include dynamic IDs placeholders such as view-auction-button-{auction_id}.

**Section 3: Data File Format Specifications**
- List all data files with filename and exact pipe-delimited fields.
- Include example data value samples.
- Detail data flow between UI and files.

CRITICAL SUCCESS CRITERIA:
- Maintain exact user element IDs, routes, HTTP methods, templates.
- Produce complete artifact suitable for implementation.
- Use write_text_file tool to save artifact design_debate_b.md.

Output: design_debate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_debate_b.md'}],

    },

    "DesignJudge": {
        "prompt": (
            """You are a Senior System Architect adjudicating final detailed design specifications for a Flask web application backed by local text file data storage.

Your goal is to produce one consolidated canonical design_spec.md artifact that fully meets the user requirements and preserves the adaptive web interface contract.

Task Details:
- Read user_task_description, final design_debate_a.md, and design_debate_b.md artifacts.
- Compare all specified Flask routes, HTTP methods, templates, and exact container and UI element IDs.
- Ensure all 9 pages declared by user with exact element IDs and navigation flows are covered.
- Check and unify all local data file specifications, pipe-delimited field orders, and example data.
- Resolve discrepancies by adhering strictly to user requirements.
- Produce one internally consistent, implementation-ready design_spec.md.
- Do not invent new requirements or deviate from user-declared element IDs or navigation.

**Section 1: Flask Routes and Web Interface Contract**
- Authoritative list of route URLs, HTTP methods, templates.
- Exact navigation button IDs and their target routes.
- Form names, methods, and action URLs for submissions.

**Section 2: HTML Template UI IDs and Page Titles**
- Authoritative templates with page titles.
- Complete lists of container and interactive element IDs.
- Maintain dynamic ID patterns as declared (e.g., view-auction-button-{auction_id}).

**Section 3: Local Text File Data Storage**
- Canonical filenames, exact pipe-delimited fields, ordering, and example data rows.
- Document data file relationships and usage within application.

CRITICAL SUCCESS CRITERIA:
- Resulting design_spec.md enables exact Flask app development with correct routing and persistent data files.
- Maintain all user-declared page elements, IDs, and navigation contract.
- Use write_text_file tool to save design_spec.md.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_debate_a.md', 'source': 'DesignDebaterA'}, {'type': 'text_file', 'name': 'design_debate_b.md', 'source': 'DesignDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDebaterA": {
        "prompt": (
            """You are a Python Flask Backend Developer and Frontend Developer skilled in building web applications with adaptive design.

Your goal is to independently implement and revise the full OnlineAuction Flask backend and all required HTML templates into app_debate_a.py and templates_debate_a/*.html according to the design_spec.md, through exactly two total debate rounds.

Task Details:
- Read design_spec.md for detailed page routes, HTML element IDs, form fields, and data flow specifications
- In round 1, produce full implementations app_debate_a.py and all templates_debate_a/*.html independently
- In round 2, revise app_debate_a.py and templates_debate_a/*.html incorporating insights from peer artifacts app_debate_b.py and templates_debate_b/*.html
- Preserve exact route paths, HTTP methods, template file names, context variable names and structures, HTML element IDs (including dynamic IDs), and navigation targets
- Adhere to the web contract ensuring '/' renders the Dashboard page without authentication
- Implement local text file data management as described in design_spec.md
- Do not add unsupported features or modify declared contracts

**Implementation Requirements: Backend (app_debate_a.py)**
- Define all Flask routes with exact methods and URL paths per design_spec.md
- Read/write data exclusively from local text files defined (e.g., auctions.txt, bids.txt)
- Include context variables with exact names and types for rendering templates
- Implement all business logic for bids, listings, filtering, and status updates

**Implementation Requirements: Frontend Templates (templates_debate_a/*.html)**
- Provide HTML templates for all declared pages in design_spec.md preserving element IDs with dynamic parts intact
- Implement navigation buttons with routes matching backend Flask route handlers
- Ensure form fields and button IDs have exact names and structure for integration
- Do not alter declared HTML element hierarchies or omit required dynamic ID patterns

**Verification and Validation**
- Validate Python syntax and runtime of app_debate_a.py with validate_python_file tool after every revision
- Use write_text_file tool to output all implementation files under correct names

CRITICAL SUCCESS CRITERIA:
- Two total rounds: independent round 1 and peer-informed round 2 revisions
- Complete, runnable Flask backend in app_debate_a.py with template rendering as per spec
- Precise preservation of routes, methods, templates, form fields, and element IDs including dynamic ones
- Use write_text_file tool for all output saves
- Output only declared artifacts with no extra comments or refinement markers

Output: app_debate_a.py, templates_debate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}],

    },

    "ImplementationDebaterB": {
        "prompt": (
            """You are a Python Flask Backend Developer and Frontend Developer skilled in building web applications with adaptive design.

Your goal is to independently implement and revise the full OnlineAuction Flask backend and all required HTML templates into app_debate_b.py and templates_debate_b/*.html according to the design_spec.md, through exactly two total debate rounds.

Task Details:
- Study design_spec.md carefully for route definitions, HTML element IDs, form fields, and context variables
- Independently write full implementation in app_debate_b.py and all templates_debate_b/*.html in round 1
- In round 2, revise app_debate_b.py and templates_debate_b/*.html incorporating peer artifacts app_debate_a.py and templates_debate_a/*.html
- Strictly preserve all user-declared routes, HTTP methods, template files, navigation flows, and dynamic IDs
- Implement local text file data handling as specified, with no authentication and root route showing Dashboard page
- Do not introduce features or changes beyond design_spec.md

**Implementation Requirements: Backend (app_debate_b.py)**
- Implement all Flask route handlers with exact endpoint and method mappings from design_spec.md
- Use local text files for persistent data storage and retrieval exactly as specified
- Provide context dictionaries for template rendering with precise keys and types

**Implementation Requirements: Frontend (templates_debate_b/*.html)**
- Create HTML templates matching each page specified, preserving all element IDs exactly, including dynamically constructed IDs
- Navigation buttons and links must correspond exactly to backend routes
- Form fields, buttons, and inputs maintain declared IDs and names

**Verification**
- Validate app_debate_b.py for syntax and runtime correctness with validate_python_file tool post revisions
- Write output files with write_text_file according to the naming conventions

CRITICAL SUCCESS CRITERIA:
- Total two rounds, round 1 independent then round 2 peer-informed revision
- Fully functional Flask backend and matching templates per design_spec.md
- Preserve web contract semantics with '/' routing to Dashboard without authentication
- Use write_text_file exclusively for all output operations
- Output only the specified files without additions or refinement feedback

Output: app_debate_b.py, templates_debate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}],

    },

    "ImplementationJudge": {
        "prompt": (
            """You are a Senior Python Flask Developer responsible for final adjudication of competing implementations.

Your goal is to produce a canonical, complete, runnable app.py and all templates/*.html files for the OnlineAuction app, precisely conforming to the design_spec.md and passing all adaptive web contract requirements, following the two-round debate process.

Task Details:
- Read design_spec.md plus final app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, templates_debate_b/*.html
- Compare implementations for functional completeness and code correctness
- Verify exact preservation of routes, HTTP methods, templates, navigation flows, and dynamic element IDs
- Confirm root route '/' renders the Dashboard page without requiring authentication
- Ensure all declared local text file data accesses match design_spec.md formats and names
- Validate the Python backend files with validate_python_file tool for syntax and runtime errors
- Resolve conflicts by selecting the best supported artifact parts to produce final app.py and templates/*.html
- Do not add new requirements or features beyond design_spec.md

**Deliverables:**
- Canonical backend app.py file implementing all routes, data handling, and context variables
- Complete set of HTML templates in templates/*.html with correct IDs, dynamic substitutions, and navigation

CRITICAL SUCCESS CRITERIA:
- Output files are runnable Flask application matching design_spec.md precisely
- All backend routes and templates fully consistent, complete, and maintaining adaptive web contract
- Use write_text_file to save all output files with exact filenames
- Do not produce refinement markers or additional commentary beyond output

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignJudge'}, {'type': 'text_file', 'name': 'app_debate_a.py', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html', 'source': 'ImplementationDebaterA'}, {'type': 'text_file', 'name': 'app_debate_b.py', 'source': 'ImplementationDebaterB'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html', 'source': 'ImplementationDebaterB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignDebaterA': [
        ("DesignJudge", """Approve if design_debate_a.md exists, is non-empty, readable, aligned with user requirements, contains all pages with exact element IDs, routes, methods, templates, and data file mappings; allow partial incompleteness but no catastrophic formatting errors.""", [{'type': 'text_file', 'name': 'design_debate_a.md'}])
    ],

    'DesignDebaterB': [
        ("DesignJudge", """Approve if design_debate_b.md exists, is non-empty, readable, aligned with user requirements as above; allow partial incompleteness but no catastrophic formatting errors.""", [{'type': 'text_file', 'name': 'design_debate_b.md'}])
    ],

    'DesignJudge': [
        ("DesignDebaterA", """Approve if design_spec.md exists and is a broadly usable canonical design specification for the OnlineAuction Flask app preserving all adaptive interface and storage contracts, readable and logically consistent.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDebaterA': [
        ("ImplementationJudge", """Approve if app_debate_a.py and templates_debate_a/*.html exist, are non-empty, valid in syntax, conform to design_spec.md, and broadly usable; allow minor incompleteness.""", [{'type': 'text_file', 'name': 'app_debate_a.py'}, {'type': 'text_file', 'name': 'templates_debate_a/*.html'}])
    ],

    'ImplementationDebaterB': [
        ("ImplementationJudge", """Approve if app_debate_b.py and templates_debate_b/*.html exist, are non-empty, valid, conform to design_spec.md, and broadly usable; allow minor incompleteness.""", [{'type': 'text_file', 'name': 'app_debate_b.py'}, {'type': 'text_file', 'name': 'templates_debate_b/*.html'}])
    ],

    'ImplementationJudge': [
        ("ImplementationDebaterA", """Approve if canonical app.py and templates/*.html exist, are non-empty, readable, runnable, and meet design_spec.md requirements; do not reject for minor omissions or polish.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    DesignDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    DesignDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    DesignJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial drafts, 2=peer-informed revisions)
    for round_num in range(1, 3):
        design_a_content = ""
        design_b_content = ""

        if round_num > 1:
            try:
                design_a_content = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a_content = ""
            try:
                design_b_content = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b_content = ""

        if round_num == 1:
            msg_a = "(No peer artifact yet; first round initial independent draft.)"
            msg_b = "(No peer artifact yet; first round initial independent draft.)"
        else:
            msg_a = f"Round 2 peer revision: read your own design_debate_a.md and peer design_debate_b.md artifacts to revise and fully overwrite design_debate_a.md.\n\nPeer DesignDebaterB content:\n{design_b_content}"
            msg_b = f"Round 2 peer revision: read your own design_debate_b.md and peer design_debate_a.md artifacts to revise and fully overwrite design_debate_b.md.\n\nPeer DesignDebaterA content:\n{design_a_content}"

        # Run both debaters in parallel each round
        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After 2 rounds, read final debater artifacts for adjudication
    final_design_a = ""
    final_design_b = ""
    try:
        final_design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_a = ""
    try:
        final_design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_b = ""

    # Run the DesignJudge to adjudicate and produce canonical design_spec.md
    await execute(
        DesignJudge,
        "Adjudicate the complete final round 2 design_debate_a.md and design_debate_b.md, "
        "compare and unify Flask routes, HTTP methods, templates, element IDs, navigation flows, "
        "data file schemas, and local text persistence. Produce one consistent, implementation-ready design_spec.md.\n\n"
        "=== Final DesignDebaterA ===\n" + final_design_a + "\n\n=== Final DesignDebaterB ===\n" + final_design_b
    )
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

    ImplementationDebaterA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationDebaterB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationJudge = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        app_a_content = ""
        templates_a_content = ""
        app_b_content = ""
        templates_b_content = ""

        if round_num > 1:
            try:
                app_a_content = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                app_a_content = ""
            for template_path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    templates_a_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

            try:
                app_b_content = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                app_b_content = ""
            for template_path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    templates_b_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

        if round_num == 1:
            msg_a = "Round 1 of 2: independently implement full app_debate_a.py and templates_debate_a/*.html based on design_spec.md."
            msg_b = "Round 1 of 2: independently implement full app_debate_b.py and templates_debate_b/*.html based on design_spec.md."
        else:
            msg_a = (
                "Round 2 of 2: revise app_debate_a.py and templates_debate_a/*.html "
                "incorporating peer artifacts below.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b_content + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + templates_b_content
            )
            msg_b = (
                "Round 2 of 2: revise app_debate_b.py and templates_debate_b/*.html "
                "incorporating peer artifacts below.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a_content + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + templates_a_content
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b),
        )

    # After debate rounds, ImplementationJudge adjudicates final canonical app.py and templates/*.html
    app_a_content = ""
    templates_a_content = ""
    app_b_content = ""
    templates_b_content = ""

    try:
        app_a_content = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        app_a_content = ""
    for template_path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    try:
        app_b_content = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        app_b_content = ""
    for template_path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    await execute(
        ImplementationJudge,
        "Adjudicate the two final round-2 candidate implementations and write canonical app.py and templates/*.html files.\n\n"
        "=== Candidate A ===\n" + app_a_content + "\n\n" + templates_a_content + "\n\n"
        "=== Candidate B ===\n" + app_b_content + "\n\n" + templates_b_content,
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
