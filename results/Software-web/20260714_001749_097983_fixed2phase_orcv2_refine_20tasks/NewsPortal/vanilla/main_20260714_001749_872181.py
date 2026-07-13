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
# 20260714_001749_872181/main_20260714_001749_872181.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the comprehensive design specification for the NewsPortal Flask web application including all 9 page designs, element IDs, navigation flow, and local text data storage formats; deliver design_spec.md and gated design_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator produces design_spec.md describing UI pages with element IDs, navigation, and data storage contract; DesignCritic reviews design_spec.md and produces design_feedback.md starting with [APPROVED] or NEED_MODIFY.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python Flask web applications.\n\nYour goal is to generate or revise a complete design specification for the NewsPortal Flask app, focusing on detailed page templates with exact element IDs, navigation routes starting from the Dashboard, and local text file data management formats.\n\nTask Details:\n- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT\n- On initial iteration, create full design_spec.md covering all 9 pages, element IDs, navigation, and data storage format\n- On feedback NEED_MODIFY, incorporate all corrections and overwrite design_spec.md\n- Stop after approval or at most two iterations\n\n**Section 1: Flask Page Templates**\n- Specify 9 page templates with exact page titles and element IDs as outlined in user_task_description\n- Include container divs, buttons, inputs, dropdowns with correct IDs and types\n- Ensure the Dashboard page is the starting point of navigation\n\n**Section 2: Navigation Flow**\n- Describe Flask route mappings and navigation logic between pages\n- Ensure direct accessibility per user requirements, no authentication\n- Include back to dashboard and page-to-page navigations consistently\n\n**Section 3: Local Text File Data Management**\n- Define file names and data formats for articles.txt, categories.txt, bookmarks.txt, comments.txt, and trending.txt\n- Specify field orders and data delimiters precisely per examples\n- Clarify reading and writing methods for these local data files\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output design_spec.md\n- Retain exact artifact name 'design_spec.md'\n- Implement at most two refinement iterations, obey NEED_MODIFY feedback fully\n- Avoid adding requirements beyond user_task_description\n- Include detailed UI element IDs and data storage formats as given\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Software Design Reviewer specializing in Flask web application specifications.\n\nYour goal is to critically review design_spec.md for completeness, conformance to user requirements, and fidelity of element IDs, navigation routes, and data storage design; then write gated design_feedback.md with [APPROVED] or NEED_MODIFY markers.\n\nTask Details:\n- Read user_task_description and design_spec.md from CONTEXT\n- Verify all 9 pages are fully specified, including exact element IDs per requirements\n- Confirm navigation flows start at Dashboard and cover all page-to-page routes\n- Check data storage files, formats, field orders, delimiters match examples exactly\n- Write [APPROVED] if design meets all criteria; otherwise write NEED_MODIFY plus specific corrections\n- Conduct at most two review iterations, gating Generator output accordingly\n\nReview Checklist:\n1. Are all pages named and titled per the user task with correct element IDs?\n2. Is navigation flow thorough, accessible, and starting from Dashboard page?\n3. Are local text data files specified with correct names, formats, and fields?\n4. Are no extraneous features or requirements introduced beyond user specification?\n5. Does feedback begin exactly with [APPROVED] or NEED_MODIFY on byte 1 of design_feedback.md?\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save complete design_feedback.md\n- Begin feedback artifact with precise [APPROVED] or NEED_MODIFY marker without preceding spaces or lines\n- Provide detailed corrections if NEED_MODIFY is given\n- Limit to two total review loops maximum\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Ensure design_spec.md accurately represents all 9 required pages with exact element IDs, provides clear navigation starting from dashboard page, and specifies local text file data format per user requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Iteratively develop and refine the NewsPortal Flask application code base with all 9 page templates, exact element IDs, local text file data handling, and navigation; deliver final app.py and templates/*.html and gated code_feedback.md\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or revises app.py and each templates/*.html file implementing the design_spec.md and incorporating code_feedback.md; CodeCritic reviews all code files for functional correctness, element ID compliance, data access reliability, and navigation, returning code_feedback.md starting with [APPROVED] or NEED_MODIFY.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building web applications using local text file data storage.\n\nYour goal is to implement or revise the complete NewsPortal Flask application including app.py and all nine HTML templates with exact page element IDs and local text file management, incorporating code critic feedback for up to two iteration cycles.\n\nTask Details:\n- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration, implement full app.py and all templates/*.html per design_spec.md requirements\n- On subsequent iteration with feedback starting NEED_MODIFY, apply all indicated corrections and rewrite complete app.py and templates/*.html\n- On feedback [APPROVED], preserve final approved code and templates\n\n**Section 1: Flask app.py Implementation**\n- Implement routes for all nine pages with correct route paths and navigation starting at dashboard\n- Handle local text file reading/writing for articles, categories, bookmarks, comments, trending data exactly as specified\n- Maintain data file formats and field usage strictly as per design_spec.md\n- Implement bookmark, comment, search, trending filtering, and pagination logic if applicable\n\n**Section 2: Templates/*.html Implementation**\n- Create or revise nine HTML templates each corresponding to specified pages with exact element IDs from design_spec.md\n- Use standard Flask Jinja2 templating for dynamic content insertion consistent with app.py context variables\n- Include all buttons, dropdowns, inputs, divs, and controls as required with specified IDs for consistent frontend behavior\n\n**Section 3: Integration and Consistency**\n- Ensure all template element IDs exactly match those defined in design_spec.md for correct frontend identification\n- Guarantee Flask routes and page navigation logically flow as described, especially starting from dashboard\n- Do not add features outside design_spec.md scope; strictly focus on required pages and functionality\n\nCRITICAL REQUIREMENTS:\n- Run at most two refinement iterations guided by code_feedback.md marker ([APPROVED]/NEED_MODIFY)\n- MUST use write_text_file tool to save outputs: app.py and templates/*.html files\n- Output complete app.py and all templates/*.html files in each revision cycle\n- Maintain exact element IDs and file data access specifications exactly as in design_spec.md\n- Preserve application start route as dashboard page\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application code review and quality assurance.\n\nYour goal is to conduct detailed code and template review of app.py and templates/*.html for the NewsPortal app and provide gated feedback for up to two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Review correctness of Flask route implementations for all nine pages including routing starting at dashboard\n- Verify exact match of all page element IDs against design_spec.md specifications\n- Validate local text file reading and writing handling for articles, categories, bookmarks, comments, and trending data complies with specified formats\n- Check navigation flows between pages as per requirements and consistency with design_spec.md\n- Identify missing features, incorrect implementations, or deviations, but do not add extra functionalities\n\nReview Criteria:\n1. Confirm presence and correctness of all nine pages and their route handlers\n2. Confirm all HTML templates have exact element IDs as specified in design_spec.md\n3. Validate code correctly loads, writes, and updates local data files in stated formats\n4. Verify navigation between pages works as expected starting from dashboard\n5. Ensure code and templates do not introduce requirements beyond design_spec.md\n\nCRITICAL REQUIREMENTS:\n- Feedback file code_feedback.md MUST begin with exact marker [APPROVED] or NEED_MODIFY\n- Use write_text_file tool to save complete feedback report\n- Limit review iterations to two and halt immediately upon approval\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Validate that all 9 pages and their exact element IDs exist, local text file data reading/writing is correctly integrated, and navigation begins from the dashboard page; ensure adherence to design_spec.md without adding functionalities.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'NewsPortal' Web Application

## 1. Objective
Develop a comprehensive web application named 'NewsPortal' using Python, with data managed through local text files. The application enables users to browse news articles by category, read detailed articles, bookmark favorites, view comments, and track trending articles. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'NewsPortal' application is Python.

## 3. Page Design

The 'NewsPortal' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: News Portal
- **Overview**: The main hub displaying featured articles, trending news, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-articles** - Type: Div - Display of featured article recommendations.
  - **ID: browse-articles-button** - Type: Button - Button to navigate to article catalog page.
  - **ID: view-bookmarks-button** - Type: Button - Button to navigate to bookmarks page.
  - **ID: trending-articles-button** - Type: Button - Button to navigate to trending articles page.

### 2. Article Catalog Page
- **Page Title**: Article Catalog
- **Overview**: A page displaying all available articles with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search articles by title, author, or keywords.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Technology, Sports, Business, Health, Entertainment, etc.).
  - **ID: articles-grid** - Type: Div - Grid displaying article cards with thumbnail, title, author, and date.
  - **ID: view-article-button-{article_id}** - Type: Button - Button to view article details (each article card has this).

### 3. Article Details Page
- **Page Title**: Article Details
- **Overview**: A page displaying detailed information about a specific article.
- **Elements**:
  - **ID: article-details-page** - Type: Div - Container for the article details page.
  - **ID: article-title** - Type: H1 - Display article title.
  - **ID: article-author** - Type: Div - Display article author.
  - **ID: article-date** - Type: Div - Display article publication date.
  - **ID: bookmark-button** - Type: Button - Button to bookmark the article.
  - **ID: article-content** - Type: Div - Section displaying the full article content.

### 4. Bookmarks Page
- **Page Title**: My Bookmarks
- **Overview**: A page displaying all bookmarked articles with removal and reading options.
- **Elements**:
  - **ID: bookmarks-page** - Type: Div - Container for the bookmarks page.
  - **ID: bookmarks-list** - Type: Div - List displaying all bookmarked articles with title and date.
  - **ID: remove-bookmark-button-{bookmark_id}** - Type: Button - Button to remove bookmark (each bookmark has this).
  - **ID: read-bookmark-button-{bookmark_id}** - Type: Button - Button to read bookmarked article (each bookmark has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Comments Page
- **Page Title**: Article Comments
- **Overview**: A page displaying all comments on articles and allowing users to write new comments.
- **Elements**:
  - **ID: comments-page** - Type: Div - Container for the comments page.
  - **ID: comments-list** - Type: Div - List of all comments with article title, commenter name, and comment text.
  - **ID: write-comment-button** - Type: Button - Button to navigate to write comment page.
  - **ID: filter-by-article** - Type: Dropdown - Dropdown to filter comments by article.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Write Comment Page
- **Page Title**: Write a Comment
- **Overview**: A page for users to write comments on articles.
- **Elements**:
  - **ID: write-comment-page** - Type: Div - Container for the write comment page.
  - **ID: select-article** - Type: Dropdown - Dropdown to select article to comment on.
  - **ID: commenter-name** - Type: Input - Field to input commenter name.
  - **ID: comment-text** - Type: Textarea - Field to write comment text.
  - **ID: submit-comment-button** - Type: Button - Button to submit comment.

### 7. Trending Articles Page
- **Page Title**: Trending Articles
- **Overview**: A page displaying top trending articles ranked by views and engagement.
- **Elements**:
  - **ID: trending-page** - Type: Div - Container for the trending articles page.
  - **ID: trending-list** - Type: Div - Ranked list of trending articles with rank, title, category, and view count.
  - **ID: time-period-filter** - Type: Dropdown - Dropdown to filter by time period (Today, This Week, This Month).
  - **ID: view-article-button-{article_id}** - Type: Button - Button to view article details (each trending article has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Category Page
- **Page Title**: Category Articles
- **Overview**: A page displaying articles from a specific category.
- **Elements**:
  - **ID: category-page** - Type: Div - Container for the category page.
  - **ID: category-title** - Type: H1 - Display the category name.
  - **ID: category-articles** - Type: Div - List of articles in the selected category.
  - **ID: sort-by-date** - Type: Button - Button to sort articles by date.
  - **ID: sort-by-popularity** - Type: Button - Button to sort articles by popularity.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Search Results Page
- **Page Title**: Search Results
- **Overview**: A page displaying search results based on user query.
- **Elements**:
  - **ID: search-results-page** - Type: Div - Container for the search results page.
  - **ID: search-query-display** - Type: Div - Display the search query performed.
  - **ID: results-list** - Type: Div - List of search results with article title and excerpt.
  - **ID: no-results-message** - Type: Div - Message displayed when no results found.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'NewsPortal' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Articles Data
- **File Name**: `articles.txt`
- **Data Format**:
  ```
  article_id|title|author|category|content|date|views
  ```
- **Example Data**:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- **File Name**: `bookmarks.txt`
- **Data Format**:
  ```
  bookmark_id|article_id|article_title|bookmarked_date
  ```
- **Example Data**:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- **File Name**: `comments.txt`
- **Data Format**:
  ```
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
  ```
- **Example Data**:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- **File Name**: `trending.txt`
- **Data Format**:
  ```
  article_id|article_title|category|view_count|period
  ```
- **Example Data**:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
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
            """You are a Software Architect specializing in Python Flask web applications.

Your goal is to generate or revise a complete design specification for the NewsPortal Flask app, focusing on detailed page templates with exact element IDs, navigation routes starting from the Dashboard, and local text file data management formats.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- On initial iteration, create full design_spec.md covering all 9 pages, element IDs, navigation, and data storage format
- On feedback NEED_MODIFY, incorporate all corrections and overwrite design_spec.md
- Stop after approval or at most two iterations

**Section 1: Flask Page Templates**
- Specify 9 page templates with exact page titles and element IDs as outlined in user_task_description
- Include container divs, buttons, inputs, dropdowns with correct IDs and types
- Ensure the Dashboard page is the starting point of navigation

**Section 2: Navigation Flow**
- Describe Flask route mappings and navigation logic between pages
- Ensure direct accessibility per user requirements, no authentication
- Include back to dashboard and page-to-page navigations consistently

**Section 3: Local Text File Data Management**
- Define file names and data formats for articles.txt, categories.txt, bookmarks.txt, comments.txt, and trending.txt
- Specify field orders and data delimiters precisely per examples
- Clarify reading and writing methods for these local data files

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output design_spec.md
- Retain exact artifact name 'design_spec.md'
- Implement at most two refinement iterations, obey NEED_MODIFY feedback fully
- Avoid adding requirements beyond user_task_description
- Include detailed UI element IDs and data storage formats as given

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Software Design Reviewer specializing in Flask web application specifications.

Your goal is to critically review design_spec.md for completeness, conformance to user requirements, and fidelity of element IDs, navigation routes, and data storage design; then write gated design_feedback.md with [APPROVED] or NEED_MODIFY markers.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify all 9 pages are fully specified, including exact element IDs per requirements
- Confirm navigation flows start at Dashboard and cover all page-to-page routes
- Check data storage files, formats, field orders, delimiters match examples exactly
- Write [APPROVED] if design meets all criteria; otherwise write NEED_MODIFY plus specific corrections
- Conduct at most two review iterations, gating Generator output accordingly

Review Checklist:
1. Are all pages named and titled per the user task with correct element IDs?
2. Is navigation flow thorough, accessible, and starting from Dashboard page?
3. Are local text data files specified with correct names, formats, and fields?
4. Are no extraneous features or requirements introduced beyond user specification?
5. Does feedback begin exactly with [APPROVED] or NEED_MODIFY on byte 1 of design_feedback.md?

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save complete design_feedback.md
- Begin feedback artifact with precise [APPROVED] or NEED_MODIFY marker without preceding spaces or lines
- Provide detailed corrections if NEED_MODIFY is given
- Limit to two total review loops maximum

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Python Flask Developer specializing in building web applications using local text file data storage.

Your goal is to implement or revise the complete NewsPortal Flask application including app.py and all nine HTML templates with exact page element IDs and local text file management, incorporating code critic feedback for up to two iteration cycles.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, implement full app.py and all templates/*.html per design_spec.md requirements
- On subsequent iteration with feedback starting NEED_MODIFY, apply all indicated corrections and rewrite complete app.py and templates/*.html
- On feedback [APPROVED], preserve final approved code and templates

**Section 1: Flask app.py Implementation**
- Implement routes for all nine pages with correct route paths and navigation starting at dashboard
- Handle local text file reading/writing for articles, categories, bookmarks, comments, trending data exactly as specified
- Maintain data file formats and field usage strictly as per design_spec.md
- Implement bookmark, comment, search, trending filtering, and pagination logic if applicable

**Section 2: Templates/*.html Implementation**
- Create or revise nine HTML templates each corresponding to specified pages with exact element IDs from design_spec.md
- Use standard Flask Jinja2 templating for dynamic content insertion consistent with app.py context variables
- Include all buttons, dropdowns, inputs, divs, and controls as required with specified IDs for consistent frontend behavior

**Section 3: Integration and Consistency**
- Ensure all template element IDs exactly match those defined in design_spec.md for correct frontend identification
- Guarantee Flask routes and page navigation logically flow as described, especially starting from dashboard
- Do not add features outside design_spec.md scope; strictly focus on required pages and functionality

CRITICAL REQUIREMENTS:
- Run at most two refinement iterations guided by code_feedback.md marker ([APPROVED]/NEED_MODIFY)
- MUST use write_text_file tool to save outputs: app.py and templates/*.html files
- Output complete app.py and all templates/*.html files in each revision cycle
- Maintain exact element IDs and file data access specifications exactly as in design_spec.md
- Preserve application start route as dashboard page

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application code review and quality assurance.

Your goal is to conduct detailed code and template review of app.py and templates/*.html for the NewsPortal app and provide gated feedback for up to two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Review correctness of Flask route implementations for all nine pages including routing starting at dashboard
- Verify exact match of all page element IDs against design_spec.md specifications
- Validate local text file reading and writing handling for articles, categories, bookmarks, comments, and trending data complies with specified formats
- Check navigation flows between pages as per requirements and consistency with design_spec.md
- Identify missing features, incorrect implementations, or deviations, but do not add extra functionalities

Review Criteria:
1. Confirm presence and correctness of all nine pages and their route handlers
2. Confirm all HTML templates have exact element IDs as specified in design_spec.md
3. Validate code correctly loads, writes, and updates local data files in stated formats
4. Verify navigation between pages works as expected starting from dashboard
5. Ensure code and templates do not introduce requirements beyond design_spec.md

CRITICAL REQUIREMENTS:
- Feedback file code_feedback.md MUST begin with exact marker [APPROVED] or NEED_MODIFY
- Use write_text_file tool to save complete feedback report
- Limit review iterations to two and halt immediately upon approval

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
        ("DesignCritic", """Ensure design_spec.md accurately represents all 9 required pages with exact element IDs, provides clear navigation starting from dashboard page, and specifies local text file data format per user requirements.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Validate that all 9 pages and their exact element IDs exist, local text file data reading/writing is correctly integrated, and navigation begins from the dashboard page; ensure adherence to design_spec.md without adding functionalities.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    DesignCritic = build_resilient_agent(
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
            "Generate or revise the complete design_spec.md for the NewsPortal Flask app including all 9 pages, element IDs, navigation starting from Dashboard, and local text file data formats.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md against user_task_description, checking for completeness of all pages with exact element IDs, navigation starting at Dashboard, and correct local text file data formats.\n"
            "Write design_feedback.md starting exactly with [APPROVED] or NEED_MODIFY and include detailed corrections if needed.\n\n"
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
import asyncio
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
            "Create or revise the complete app.py and templates/*.html implementing design_spec.md "
            "and incorporating code_feedback.md.\n\n"
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
            "Review the latest app.py and templates/*.html against design_spec.md to ensure correctness.\n"
            "Provide code_feedback.md starting exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
