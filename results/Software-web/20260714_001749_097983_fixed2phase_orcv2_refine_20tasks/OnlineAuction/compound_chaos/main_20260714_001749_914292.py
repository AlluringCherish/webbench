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
# 20260714_001749_914292/main_20260714_001749_914292.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create and refine the full design specification for the OnlineAuction Python Flask web app including detailed page structure and data storage contract; deliver design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator drafts design_spec.md from user_task_description and design_feedback.md; DesignCritic reviews and writes design_feedback.md with [APPROVED] or NEED_MODIFY markers for refinement\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python Flask web application design specifications.\n\nYour goal is to produce and iteratively refine a complete design specification document capturing page layouts, element IDs, navigation flow, and local text file data schemas for the OnlineAuction application.\n\nTask Details:\n- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT\n- Initially create the full design_spec.md covering all required pages and data files\n- On feedback beginning with NEED_MODIFY, apply all required corrections and rewrite the entire design_spec.md\n- Stop refinement after at most two iterations or upon receiving [APPROVED] feedback\n- Output the complete design_spec.md as a text file artifact\n\n**Page Layout Specifications**\n- Define each page with its title and overview\n- Include container div IDs and all specified element IDs with their types and brief descriptions\n- Specify navigation buttons and their target pages where applicable\n\n**Data Storage Contract**\n- Include all local text file data schemas with exact filenames\n- Specify each file's data fields, formats, and provide example records\n- Preserve data field names and formats as declared in user requirements\n\n**Consistency and Scope**\n- Reflect all pages and elements exactly as in user_task_description\n- Do not add authentication or unrequested features\n- Focus on enabling developers to implement the front-end, back-end routing, and data management from the specification\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to write design_spec.md artifact\n- Run a maximum of two Generator/Critic iterations, stopping on [APPROVED]\n- Accurately represent all page and data file specifications from user input\n- Fully incorporate correction requests beginning with NEED_MODIFY without adding new requirements\n- Do not write feedback status markers inside design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Software Design Reviewer specializing in Python Flask web application design review.\n\nYour goal is to critically evaluate design_spec.md against user_task_description and provide gated feedback for at most two iterations.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Verify completeness and accuracy of page layouts, element IDs, navigation flow\n- Verify correctness and consistency of declared local data file schemas including field names and data formats\n- Write feedback in design_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY with clear, itemized corrections\n\nReview Checklist:\n1. Confirm design_spec.md includes all nine required pages with specified page titles and element IDs\n2. Confirm navigation buttons and their target pages match user requirements on all pages\n3. Validate data storage schemas for all declared text files, field names, data formats, and examples are consistent with user_task_description\n4. Ensure no unrequested features like authentication or additional pages are introduced\n5. Ensure naming conventions and element IDs are consistent across pages\n6. Provide actionable feedback if issues found, else approve design_spec.md\n\nCRITICAL REQUIREMENTS:\n- Write the first bytes of design_feedback.md exactly as [APPROVED] or NEED_MODIFY\n- No extra prefix, heading, or whitespace before the status marker\n- Use write_text_file tool to output design_feedback.md\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Ensure the design_spec.md fully covers all required pages, element IDs, navigation links, and data storage files per user requirements; provide constructive feedback to achieve final approval\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Develop and iteratively refine the OnlineAuction Flask web app source code including app.py and templates/*.html with full functionality and correct element IDs; generate code_feedback.md with validation\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or revises app.py and templates/*.html using design_spec.md and code_feedback.md; CodeCritic evaluates functionality, correctness, completeness, element IDs, and data file integration then writes code_feedback.md starting with [APPROVED] or NEED_MODIFY\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specialized in building web applications with backend and frontend integration.\n\nYour goal is to implement and iteratively refine the complete OnlineAuction Flask backend (app.py) and frontend templates (*.html) according to the design specifications and feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On the first iteration, implement full app.py and templates/*.html based on design_spec.md\n- On NEED_MODIFY feedback, apply all corrections and rewrite the entire app.py and templates/*.html accordingly\n- On [APPROVED] feedback, preserve the approved implementation\n- Output complete app.py and all templates/*.html files in the designated folders\n\n**Section 1: Flask Backend Implementation**\n- Implement Flask routes for all specified pages: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status\n- Integrate data loading and saving from local text files in the 'data' directory as specified (auctions.txt, categories.txt, bids.txt, winners.txt, bid_history.txt, items.txt, trending.txt)\n- Ensure data consistency and correct file format handling for all operations (viewing, placing bids, filtering)\n- Provide handlers for navigation and filtering as per design_spec.md\n\n**Section 2: Frontend Templates (*.html)**\n- Implement HTML templates with the exact required page titles and element IDs listed in the design specification\n- Each template must contain the specified container elements, buttons, inputs, dropdowns, tables, and display areas exactly matching IDs (e.g., dashboard-page, featured-auctions, bids-table, place-bid-page, etc.)\n- Bind frontend elements correctly with backend context data for dynamic content rendering\n- Keep the UI navigation consistent with buttons leading to the corresponding Flask routes\n\n**Section 3: Iterative Refinement and Feedback Usage**\n- At feedback NEED_MODIFY, comprehensively identify and fix issues across backend and frontend code\n- Validate all element IDs, navigation routes, and data file interactions per feedback\n- Do not introduce extra functionalities beyond the design_spec.md and USER_TASK scope\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output completed app.py and templates/*.html files\n- Maintain exact element IDs, page titles, and data file integration as specified\n- Stop after two iterations or immediately upon receiving [APPROVED] feedback in code_feedback.md\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer with expertise in Python Flask application validation and front-end verification.\n\nYour goal is to perform comprehensive review and validation of app.py and templates/*.html against design_spec.md, ensuring full compliance, correct element IDs, navigation, and data integration; provide feedback limited to [APPROVED] or NEED_MODIFY for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Validate completeness and correctness of all required Flask routes and backend functionality\n- Verify all page titles, container elements, buttons, inputs, dropdowns, tables, and IDs exactly as specified in design_spec.md\n- Check integration of all local text data files for correct access, parsing, and writing operations\n- Ensure navigation flows correctly among all defined pages\n- Write feedback in code_feedback.md starting exactly with [APPROVED] if fully compliant or NEED_MODIFY followed by detailed, actionable corrections\n\nValidation Checklist:\n1. Confirm all 9 pages (Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status) exist with correct Flask routes\n2. Confirm every specified element ID is present in the related HTML template exactly as defined\n3. Confirm all data file interactions respect specified formats and fields in the USER_TASK and design_spec.md\n4. Confirm navigation buttons and links function correctly to corresponding routes\n5. Identify missing or inconsistent features, broken IDs, or data handling errors clearly in feedback\n\nCRITICAL REQUIREMENTS:\n- Feedback artifact code_feedback.md MUST begin exactly with [APPROVED] or NEED_MODIFY on byte 1\n- Use write_text_file tool to save complete feedback file\n- Use validate_python_file tool to check app.py syntax and runtime, report errors\n- Feedback must be precise, actionable, and strictly reference design_spec.md compliance\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Gate the conformity of app.py and templates/*.html to the design_spec.md and data storage schemes; verify that all required pages and element IDs exist and function correctly; ensure no regression or functionality gaps\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a Software Architect specializing in Python Flask web application design specifications.

Your goal is to produce and iteratively refine a complete design specification document capturing page layouts, element IDs, navigation flow, and local text file data schemas for the OnlineAuction application.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- Initially create the full design_spec.md covering all required pages and data files
- On feedback beginning with NEED_MODIFY, apply all required corrections and rewrite the entire design_spec.md
- Stop refinement after at most two iterations or upon receiving [APPROVED] feedback
- Output the complete design_spec.md as a text file artifact

**Page Layout Specifications**
- Define each page with its title and overview
- Include container div IDs and all specified element IDs with their types and brief descriptions
- Specify navigation buttons and their target pages where applicable

**Data Storage Contract**
- Include all local text file data schemas with exact filenames
- Specify each file's data fields, formats, and provide example records
- Preserve data field names and formats as declared in user requirements

**Consistency and Scope**
- Reflect all pages and elements exactly as in user_task_description
- Do not add authentication or unrequested features
- Focus on enabling developers to implement the front-end, back-end routing, and data management from the specification

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to write design_spec.md artifact
- Run a maximum of two Generator/Critic iterations, stopping on [APPROVED]
- Accurately represent all page and data file specifications from user input
- Fully incorporate correction requests beginning with NEED_MODIFY without adding new requirements
- Do not write feedback status markers inside design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Software Design Reviewer specializing in Python Flask web application design review.

Your goal is to critically evaluate design_spec.md against user_task_description and provide gated feedback for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify completeness and accuracy of page layouts, element IDs, navigation flow
- Verify correctness and consistency of declared local data file schemas including field names and data formats
- Write feedback in design_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY with clear, itemized corrections

Review Checklist:
1. Confirm design_spec.md includes all nine required pages with specified page titles and element IDs
2. Confirm navigation buttons and their target pages match user requirements on all pages
3. Validate data storage schemas for all declared text files, field names, data formats, and examples are consistent with user_task_description
4. Ensure no unrequested features like authentication or additional pages are introduced
5. Ensure naming conventions and element IDs are consistent across pages
6. Provide actionable feedback if issues found, else approve design_spec.md

CRITICAL REQUIREMENTS:
- Write the first bytes of design_feedback.md exactly as [APPROVED] or NEED_MODIFY
- No extra prefix, heading, or whitespace before the status marker
- Use write_text_file tool to output design_feedback.md

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specialized in building web applications with backend and frontend integration.

Your goal is to implement and iteratively refine the complete OnlineAuction Flask backend (app.py) and frontend templates (*.html) according to the design specifications and feedback for at most two iterations.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On the first iteration, implement full app.py and templates/*.html based on design_spec.md
- On NEED_MODIFY feedback, apply all corrections and rewrite the entire app.py and templates/*.html accordingly
- On [APPROVED] feedback, preserve the approved implementation
- Output complete app.py and all templates/*.html files in the designated folders

**Section 1: Flask Backend Implementation**
- Implement Flask routes for all specified pages: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status
- Integrate data loading and saving from local text files in the 'data' directory as specified (auctions.txt, categories.txt, bids.txt, winners.txt, bid_history.txt, items.txt, trending.txt)
- Ensure data consistency and correct file format handling for all operations (viewing, placing bids, filtering)
- Provide handlers for navigation and filtering as per design_spec.md

**Section 2: Frontend Templates (*.html)**
- Implement HTML templates with the exact required page titles and element IDs listed in the design specification
- Each template must contain the specified container elements, buttons, inputs, dropdowns, tables, and display areas exactly matching IDs (e.g., dashboard-page, featured-auctions, bids-table, place-bid-page, etc.)
- Bind frontend elements correctly with backend context data for dynamic content rendering
- Keep the UI navigation consistent with buttons leading to the corresponding Flask routes

**Section 3: Iterative Refinement and Feedback Usage**
- At feedback NEED_MODIFY, comprehensively identify and fix issues across backend and frontend code
- Validate all element IDs, navigation routes, and data file interactions per feedback
- Do not introduce extra functionalities beyond the design_spec.md and USER_TASK scope

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output completed app.py and templates/*.html files
- Maintain exact element IDs, page titles, and data file integration as specified
- Stop after two iterations or immediately upon receiving [APPROVED] feedback in code_feedback.md

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer with expertise in Python Flask application validation and front-end verification.

Your goal is to perform comprehensive review and validation of app.py and templates/*.html against design_spec.md, ensuring full compliance, correct element IDs, navigation, and data integration; provide feedback limited to [APPROVED] or NEED_MODIFY for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate completeness and correctness of all required Flask routes and backend functionality
- Verify all page titles, container elements, buttons, inputs, dropdowns, tables, and IDs exactly as specified in design_spec.md
- Check integration of all local text data files for correct access, parsing, and writing operations
- Ensure navigation flows correctly among all defined pages
- Write feedback in code_feedback.md starting exactly with [APPROVED] if fully compliant or NEED_MODIFY followed by detailed, actionable corrections

Validation Checklist:
1. Confirm all 9 pages (Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status) exist with correct Flask routes
2. Confirm every specified element ID is present in the related HTML template exactly as defined
3. Confirm all data file interactions respect specified formats and fields in the USER_TASK and design_spec.md
4. Confirm navigation buttons and links function correctly to corresponding routes
5. Identify missing or inconsistent features, broken IDs, or data handling errors clearly in feedback

CRITICAL REQUIREMENTS:
- Feedback artifact code_feedback.md MUST begin exactly with [APPROVED] or NEED_MODIFY on byte 1
- Use write_text_file tool to save complete feedback file
- Use validate_python_file tool to check app.py syntax and runtime, report errors
- Feedback must be precise, actionable, and strictly reference design_spec.md compliance

Output: code_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'validate_python_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'code_feedback.md'}],

    }

}

REVIEW_PROFILES = {
    'DesignGenerator': [
        ("DesignCritic", """Ensure the design_spec.md fully covers all required pages, element IDs, navigation links, and data storage files per user requirements; provide constructive feedback to achieve final approval""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Gate the conformity of app.py and templates/*.html to the design_spec.md and data storage schemes; verify that all required pages and element IDs exist and function correctly; ensure no regression or functionality gaps""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        design_spec_content = ""
        design_feedback_content = ""
        try:
            design_spec_content = open("design_spec.md").read()
        except FileNotFoundError:
            pass
        if iteration > 0:
            try:
                design_feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            DesignGenerator,
            "Produce or revise the full design_spec.md.\n\n"
            f"=== Current design_spec.md ===\n{design_spec_content}\n\n"
            f"=== Received design_feedback.md ===\n{design_feedback_content}"
        )

        try:
            design_spec_content = open("design_spec.md").read()
        except FileNotFoundError:
            design_spec_content = ""

        await execute(
            DesignCritic,
            "Review the complete design_spec.md against user_task_description and provide feedback starting with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== design_spec.md to review ===\n{design_spec_content}"
        )

        try:
            design_feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            design_feedback_content = ""

        if design_feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start

async def implementation_and_verification_phase():
    import glob

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

        # AppGenerator execution: create or revise full app.py and templates based on design_spec.md and feedback
        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html according to design_spec.md and code_feedback.md.\n\n"
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

        # CodeCritic execution: review app.py and templates thoroughly, write code_feedback.md with [APPROVED] or NEED_MODIFY
        await execute(
            CodeCritic,
            "Review the latest app.py and templates/*.html against design_spec.md.\n"
            "Check backend routes, frontend element IDs, page titles, navigation, and data file integration.\n"
            "Write code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY with actionable corrections.\n\n"
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
