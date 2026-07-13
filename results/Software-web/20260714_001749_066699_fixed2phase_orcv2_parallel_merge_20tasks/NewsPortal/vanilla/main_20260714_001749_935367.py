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
# 20260714_001749_935367/main_20260714_001749_935367.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create backend and frontend design specifications for the NewsPortal application and merge them into a complete design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDesignArchitect and FrontendDesignArchitect work independently to create backend route and data schema \"\n        \"specifications and frontend page templates with element IDs and navigation. DesignMerger receives backend_design.md \"\n        \"and frontend_design.md and produces a reconciled, internally consistent design_spec.md covering all pages, elements, \"\n        \"and data requirements without introducing new features.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask backend development with expertise in text file data management for web applications.\n\nYour goal is to specify the backend Flask routes, data file schemas, and data handling required for the NewsPortal application.\n\nTask Details:\n- Read user_task_description from CONTEXT for backend requirements\n- Independently create backend_design.md specifying Flask routes, HTTP methods, and data file schemas for articles, categories, bookmarks, comments, and trending data\n- Define the endpoints to support all described pages and features including browsing, reading, bookmarking, commenting, and trending\n- Do not read or rely on frontend_design.md outputs\n\n**Section 1: Flask Routes Specification**\n- Define route paths and supported HTTP methods for each NewsPortal page and action\n- Specify route functions with expected inputs, outputs, and navigation flow\n- Detail interactions with local text files (reading/writing) for each route\n- Include routes for browsing articles by category, viewing details, bookmarking, comments management, trending data retrieval, and search\n\n**Section 2: Data File Schemas**\n- Specify exact data file formats for articles.txt, categories.txt, bookmarks.txt, comments.txt, and trending.txt with field names, delimiters, and validations\n- Include example data lines demonstrating formatting\n- Define any data manipulation rules and constraints for reads and writes\n\n**Section 3: Operational Notes**\n- Clarify no authentication involved; all data actions are open\n- Ensure data handling aligns with local text files stored in the 'data' directory\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper can implement all necessary Flask routes and data logic solely from backend_design.md\n- Precise and complete route-to-file mappings and data schemas appear without dependence on frontend details\n- Must use write_text_file tool to output backend_design.md\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"backend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a System Architect with expertise in frontend web design focusing on HTML templates, page layout, and UI element specification.\n\nYour goal is to design the complete set of HTML page templates with precise element IDs, layout details, navigation, and interactive buttons for the NewsPortal web application.\n\nTask Details:\n- Read user_task_description from CONTEXT for frontend requirements\n- Independently produce frontend_design.md specifying all nine NewsPortal pages, their exact element IDs, element types, page titles, and user interface navigation flow\n- Define buttons, dropdowns, input fields, and lists with IDs and their intended interactive behavior\n- Do not read or rely on backend_design.md outputs\n\n**Section 1: Page Template Specifications**\n- Specify each page as a template with exact filename/path and page title\n- List all container divs, UI elements (buttons, inputs, dropdowns, lists) with precise IDs and types per specification\n- Cover pages: Dashboard, Article Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results\n\n**Section 2: Navigation and Interaction**\n- Map button IDs to navigation or action targets (e.g., view article details, add bookmark)\n- Define dropdowns and input fields purpose and interaction context\n- Ensure back-to-dashboard buttons and filters are clearly described\n\n**Section 3: Layout and Usability Notes**\n- Include any relevant layout grouping or accessibility notes to support smooth UI implementation\n- Emphasize clarity in element roles and data binding placeholders\n\nCRITICAL SUCCESS CRITERIA:\n- FrontendDeveloper can implement all templates (*.html) exactly from frontend_design.md\n- All element IDs and interactive controls comply strictly with user_task_description\n- Must use write_text_file tool to output frontend_design.md\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"frontend_design.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect skilled at integrating backend and frontend specifications into a single, consistent application design document.\n\nYour goal is to merge backend_design.md and frontend_design.md into one coherent design_spec.md that satisfies all user requirements for the NewsPortal application without adding features.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Verify completeness and consistency of backend routes and data schemas against frontend page elements and navigation\n- Reconcile route names, endpoint inputs/outputs, and template references for uniformity\n- Ensure all specified pages, elements, and data files are covered without omissions or contradictions\n\n**Section 1: Consolidated Flask Routes and Data Schemas**\n- Integrate backend routes with frontend navigation expectations\n- Harmonize data file usage descriptions with UI element bindings\n\n**Section 2: Unified Frontend Template Specifications**\n- Confirm all element IDs from frontend_design.md are referenced consistently in backend routes where applicable\n- Aggregate page template definitions matching backend endpoints\n\n**Section 3: Consistency and Coverage Checks**\n- Ensure no new features beyond input specifications are introduced\n- Validate completeness of all nine pages, all data files, and user interactions\n- Highlight and resolve any mismatches or gaps found\n\nCRITICAL SUCCESS CRITERIA:\n- BackendDeveloper and FrontendDeveloper can implement full application from design_spec.md\n- All interface contract aspects match across backend and frontend\n- Must use write_text_file tool to output design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify backend route and data design completeness and correctness before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify frontend template and element ID accuracy before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement backend app.py and frontend templates based on design_spec.md and integrate them into a complete runnable NewsPortal application bundle\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py with routes, data handling, and logic per design_spec.md. FrontendDeveloper creates HTML templates/*.html \"\n        \"with exact element IDs, layouts, and navigation from design_spec.md. IntegrationMerger reconciles app.py and templates/*.html ensuring interface \"\n        \"compliance and writes final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications and local text file data management in Python.\n\nYour goal is to implement a complete Flask backend application (app.py) including all routes, data file operations, and server-side logic based strictly on the design_spec.md artifact.\n\nTask Details:\n- Read design_spec.md from CONTEXT fully to derive required Flask routes, data schemas, and business logic.\n- Produce app.py implementing the specified backend routes and logic, including reading and writing to the declared local text data files.\n- Focus on backend code only; do not generate frontend templates or merge with other components.\n\n**Section 1: Flask Routes Implementation**\n- Implement all Flask route functions with route decorators as specified.\n- Ensure routes handle HTTP methods, request arguments, and return appropriate render_template calls or redirects.\n- Include route logic to read, write, and update the exact text files as per declared schemas in design_spec.md.\n\n**Section 2: Data Handling and File Operations**\n- Explicitly implement parsing, querying, updating, and saving of data in local text files (e.g., articles.txt, categories.txt, bookmarks.txt, comments.txt, trending.txt).\n- Follow the file formats and field orders exactly as described.\n- Handle edge cases gracefully (e.g., missing entries, empty files).\n\n**Section 3: Application Structure and Code Quality**\n- Organize app.py with necessary imports, Flask app initialization, helper functions for file I/O, and route handlers.\n- Include appropriate comments and docstrings using single-quote triple quotes only for any code explanations.\n- Avoid frontend layout or template details; backend must only control data and route flow.\n\nCRITICAL SUCCESS CRITERIA:\n- Use the write_text_file tool to output a single file named app.py.\n- Backend routes and data handling must strictly conform to design_spec.md.\n- Produce a standalone app.py suitable to be integrated with separate frontend templates.\n- Do not include any sibling artifact contents or refinement markers.\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"app.py\"}]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 template creation for Flask web applications.\n\nYour goal is to implement all frontend HTML templates (*.html) with exact element IDs, page structures, and navigation flows based exclusively on the design_spec.md artifact.\n\nTask Details:\n- Read the full design_spec.md from CONTEXT to extract all template specifications and element details.\n- Produce the complete set of templates/*.html files implementing all pages, element IDs, buttons, inputs, and navigation as specified.\n- Templates must reflect the precise layouts, container divs, buttons, and dynamic content placeholders with Jinja2 syntax where needed.\n\n**Section 1: Template Structure and Naming**\n- Create a separate HTML template file for each distinct page defined in design_spec.md.\n- Use the exact element IDs and types (div, button, input, textarea, dropdown, etc.) as declared.\n- Include page titles and layout structure consistent with the design_spec.md descriptions.\n\n**Section 2: Jinja2 Dynamic Content and Context Variables**\n- Incorporate Jinja2 syntax for rendering context variables passed from backend routes.\n- Support iteration over collections for listings (e.g., articles list, comments list).\n- Implement navigation links or buttons using proper Flask URL endpoints as per design_spec.md.\n\n**Section 3: Template Completeness and Usability**\n- Ensure all specified user interface elements are present and functional in template markup.\n- Use semantic HTML5 elements where appropriate.\n- Do not include any backend Python logic; strictly frontend templates.\n\nCRITICAL SUCCESS CRITERIA:\n- Use the write_text_file tool to output all templates/*.html files.\n- Templates must be fully consistent and implement all elements from design_spec.md, including exact IDs and navigation.\n- Do not read sibling outputs or produce backend code.\n- No refinement markers allowed; output only declared files.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"templates/*.html\"}]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Flask web application integration and quality assurance.\n\nYour goal is to merge and verify the backend implementation (app.py) and frontend templates (templates/*.html) ensuring full compliance with the design_spec.md into a final deployable NewsPortal application bundle.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT.\n- Verify that backend app.py routes match the expected routes and data handling specified in design_spec.md.\n- Verify that frontend templates contain all element IDs, page layouts, and navigation structures as per design_spec.md.\n- Check consistency between backend route templates rendered and the frontend template filenames.\n- Resolve any interface discrepancies or missing elements by adapting the final outputs (without adding new feature requirements).\n- Produce final app.py and templates/*.html files that are fully consistent, functional, and integratable.\n\n**Section 1: Backend-Frontend Interface Consistency**\n- Cross-check route handler template names with actual templates filenames.\n- Validate presence of all critical element IDs in templates referenced by backend context.\n- Ensure navigation buttons and links in templates correspond to backend routes.\n\n**Section 2: Compliance and Completeness Verification**\n- Confirm backend file operations conform to declared data schemas with correct file names.\n- Confirm templates implement all pages and UI elements declared in design_spec.md.\n- Identify and reconcile any inconsistencies between backend and frontend implementations.\n\n**Section 3: Final Output Preparation**\n- Integrate all validated components into final app.py and templates/*.html artifacts.\n- Prepare files ready for deployment without additional refinement rounds.\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to output final app.py and templates/*.html.\n- Output only the declared artifacts without refinement feedback.\n- Final files must be fully consistent and runnable as a unified NewsPortal application bundle.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check backend app.py implementation conformance with design_spec.md including routes and data handling.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Check frontend templates/*.html conform to design_spec.md including exact element IDs and navigation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask backend development with expertise in text file data management for web applications.

Your goal is to specify the backend Flask routes, data file schemas, and data handling required for the NewsPortal application.

Task Details:
- Read user_task_description from CONTEXT for backend requirements
- Independently create backend_design.md specifying Flask routes, HTTP methods, and data file schemas for articles, categories, bookmarks, comments, and trending data
- Define the endpoints to support all described pages and features including browsing, reading, bookmarking, commenting, and trending
- Do not read or rely on frontend_design.md outputs

**Section 1: Flask Routes Specification**
- Define route paths and supported HTTP methods for each NewsPortal page and action
- Specify route functions with expected inputs, outputs, and navigation flow
- Detail interactions with local text files (reading/writing) for each route
- Include routes for browsing articles by category, viewing details, bookmarking, comments management, trending data retrieval, and search

**Section 2: Data File Schemas**
- Specify exact data file formats for articles.txt, categories.txt, bookmarks.txt, comments.txt, and trending.txt with field names, delimiters, and validations
- Include example data lines demonstrating formatting
- Define any data manipulation rules and constraints for reads and writes

**Section 3: Operational Notes**
- Clarify no authentication involved; all data actions are open
- Ensure data handling aligns with local text files stored in the 'data' directory

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement all necessary Flask routes and data logic solely from backend_design.md
- Precise and complete route-to-file mappings and data schemas appear without dependence on frontend details
- Must use write_text_file tool to output backend_design.md

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a System Architect with expertise in frontend web design focusing on HTML templates, page layout, and UI element specification.

Your goal is to design the complete set of HTML page templates with precise element IDs, layout details, navigation, and interactive buttons for the NewsPortal web application.

Task Details:
- Read user_task_description from CONTEXT for frontend requirements
- Independently produce frontend_design.md specifying all nine NewsPortal pages, their exact element IDs, element types, page titles, and user interface navigation flow
- Define buttons, dropdowns, input fields, and lists with IDs and their intended interactive behavior
- Do not read or rely on backend_design.md outputs

**Section 1: Page Template Specifications**
- Specify each page as a template with exact filename/path and page title
- List all container divs, UI elements (buttons, inputs, dropdowns, lists) with precise IDs and types per specification
- Cover pages: Dashboard, Article Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results

**Section 2: Navigation and Interaction**
- Map button IDs to navigation or action targets (e.g., view article details, add bookmark)
- Define dropdowns and input fields purpose and interaction context
- Ensure back-to-dashboard buttons and filters are clearly described

**Section 3: Layout and Usability Notes**
- Include any relevant layout grouping or accessibility notes to support smooth UI implementation
- Emphasize clarity in element roles and data binding placeholders

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement all templates (*.html) exactly from frontend_design.md
- All element IDs and interactive controls comply strictly with user_task_description
- Must use write_text_file tool to output frontend_design.md

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect skilled at integrating backend and frontend specifications into a single, consistent application design document.

Your goal is to merge backend_design.md and frontend_design.md into one coherent design_spec.md that satisfies all user requirements for the NewsPortal application without adding features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Verify completeness and consistency of backend routes and data schemas against frontend page elements and navigation
- Reconcile route names, endpoint inputs/outputs, and template references for uniformity
- Ensure all specified pages, elements, and data files are covered without omissions or contradictions

**Section 1: Consolidated Flask Routes and Data Schemas**
- Integrate backend routes with frontend navigation expectations
- Harmonize data file usage descriptions with UI element bindings

**Section 2: Unified Frontend Template Specifications**
- Confirm all element IDs from frontend_design.md are referenced consistently in backend routes where applicable
- Aggregate page template definitions matching backend endpoints

**Section 3: Consistency and Coverage Checks**
- Ensure no new features beyond input specifications are introduced
- Validate completeness of all nine pages, all data files, and user interactions
- Highlight and resolve any mismatches or gaps found

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper and FrontendDeveloper can implement full application from design_spec.md
- All interface contract aspects match across backend and frontend
- Must use write_text_file tool to output design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications and local text file data management in Python.

Your goal is to implement a complete Flask backend application (app.py) including all routes, data file operations, and server-side logic based strictly on the design_spec.md artifact.

Task Details:
- Read design_spec.md from CONTEXT fully to derive required Flask routes, data schemas, and business logic.
- Produce app.py implementing the specified backend routes and logic, including reading and writing to the declared local text data files.
- Focus on backend code only; do not generate frontend templates or merge with other components.

**Section 1: Flask Routes Implementation**
- Implement all Flask route functions with route decorators as specified.
- Ensure routes handle HTTP methods, request arguments, and return appropriate render_template calls or redirects.
- Include route logic to read, write, and update the exact text files as per declared schemas in design_spec.md.

**Section 2: Data Handling and File Operations**
- Explicitly implement parsing, querying, updating, and saving of data in local text files (e.g., articles.txt, categories.txt, bookmarks.txt, comments.txt, trending.txt).
- Follow the file formats and field orders exactly as described.
- Handle edge cases gracefully (e.g., missing entries, empty files).

**Section 3: Application Structure and Code Quality**
- Organize app.py with necessary imports, Flask app initialization, helper functions for file I/O, and route handlers.
- Include appropriate comments and docstrings using single-quote triple quotes only for any code explanations.
- Avoid frontend layout or template details; backend must only control data and route flow.

CRITICAL SUCCESS CRITERIA:
- Use the write_text_file tool to output a single file named app.py.
- Backend routes and data handling must strictly conform to design_spec.md.
- Produce a standalone app.py suitable to be integrated with separate frontend templates.
- Do not include any sibling artifact contents or refinement markers.

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 template creation for Flask web applications.

Your goal is to implement all frontend HTML templates (*.html) with exact element IDs, page structures, and navigation flows based exclusively on the design_spec.md artifact.

Task Details:
- Read the full design_spec.md from CONTEXT to extract all template specifications and element details.
- Produce the complete set of templates/*.html files implementing all pages, element IDs, buttons, inputs, and navigation as specified.
- Templates must reflect the precise layouts, container divs, buttons, and dynamic content placeholders with Jinja2 syntax where needed.

**Section 1: Template Structure and Naming**
- Create a separate HTML template file for each distinct page defined in design_spec.md.
- Use the exact element IDs and types (div, button, input, textarea, dropdown, etc.) as declared.
- Include page titles and layout structure consistent with the design_spec.md descriptions.

**Section 2: Jinja2 Dynamic Content and Context Variables**
- Incorporate Jinja2 syntax for rendering context variables passed from backend routes.
- Support iteration over collections for listings (e.g., articles list, comments list).
- Implement navigation links or buttons using proper Flask URL endpoints as per design_spec.md.

**Section 3: Template Completeness and Usability**
- Ensure all specified user interface elements are present and functional in template markup.
- Use semantic HTML5 elements where appropriate.
- Do not include any backend Python logic; strictly frontend templates.

CRITICAL SUCCESS CRITERIA:
- Use the write_text_file tool to output all templates/*.html files.
- Templates must be fully consistent and implement all elements from design_spec.md, including exact IDs and navigation.
- Do not read sibling outputs or produce backend code.
- No refinement markers allowed; output only declared files.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Flask web application integration and quality assurance.

Your goal is to merge and verify the backend implementation (app.py) and frontend templates (templates/*.html) ensuring full compliance with the design_spec.md into a final deployable NewsPortal application bundle.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Verify that backend app.py routes match the expected routes and data handling specified in design_spec.md.
- Verify that frontend templates contain all element IDs, page layouts, and navigation structures as per design_spec.md.
- Check consistency between backend route templates rendered and the frontend template filenames.
- Resolve any interface discrepancies or missing elements by adapting the final outputs (without adding new feature requirements).
- Produce final app.py and templates/*.html files that are fully consistent, functional, and integratable.

**Section 1: Backend-Frontend Interface Consistency**
- Cross-check route handler template names with actual templates filenames.
- Validate presence of all critical element IDs in templates referenced by backend context.
- Ensure navigation buttons and links in templates correspond to backend routes.

**Section 2: Compliance and Completeness Verification**
- Confirm backend file operations conform to declared data schemas with correct file names.
- Confirm templates implement all pages and UI elements declared in design_spec.md.
- Identify and reconcile any inconsistencies between backend and frontend implementations.

**Section 3: Final Output Preparation**
- Integrate all validated components into final app.py and templates/*.html artifacts.
- Prepare files ready for deployment without additional refinement rounds.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output final app.py and templates/*.html.
- Output only the declared artifacts without refinement feedback.
- Final files must be fully consistent and runnable as a unified NewsPortal application bundle.

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
        ("DesignMerger", """Verify backend route and data design completeness and correctness before merging.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Verify frontend template and element ID accuracy before merging.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Check backend app.py implementation conformance with design_spec.md including routes and data handling.""", [{'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Check frontend templates/*.html conform to design_spec.md including exact element IDs and navigation.""", [{'type': 'text_file', 'name': 'templates/*.html'}])
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
        recovery_time=30
    )

    # Parallel execution: Backend and Frontend Design Architects work independently
    await asyncio.gather(
        execute(BackendDesignArchitect,
                "Create backend_design.md specifying Flask routes for NewsPortal, HTTP methods, and data file schemas for all relevant entities. Output backend_design.md."),
        execute(FrontendDesignArchitect,
                "Create frontend_design.md specifying NewsPortal HTML page templates with all element IDs, types, page titles, navigation flows, and interactive elements. Output frontend_design.md.")
    )

    # Read outputs for DesignMerger
    backend_design_content = ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass

    frontend_design_content = ""
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend designs into a unified design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into design_spec.md for NewsPortal.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
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
        failure_threshold=2,
        recovery_time=50
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=50
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete app.py backend based on design_spec.md from DesignMerger including all Flask routes, data handling, and server-side logic strictly conforming to design_spec.md."),
        execute(FrontendDeveloper,
                "Implement all frontend HTML templates (*.html) based on design_spec.md from DesignMerger including exact element IDs, page layouts, Jinja2 syntax, and navigation.")
    )

    # Read BackendDeveloper output app.py
    backend_app_py = ""
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            backend_app_py = f.read()
    except FileNotFoundError:
        backend_app_py = ""

    # Read FrontendDeveloper output templates/*.html
    frontend_templates_content = ""
    for template_file in sorted(glob.glob("templates/*.html")):
        try:
            with open(template_file, "r", encoding="utf-8") as f:
                frontend_templates_content += f"\n=== {template_file} ===\n" + f.read()
        except OSError:
            pass

    # IntegrationMerger verifies and reconciles final outputs
    await execute(
        IntegrationMerger,
        f"Verify and merge backend app.py and frontend templates from DesignMerger.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== Backend app.py ===\n{backend_app_py}\n\n"
        f"=== Frontend Templates ===\n{frontend_templates_content}\n\n"
        "Produce final consistent app.py and templates/*.html artifacts ready for deployment."
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
