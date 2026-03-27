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
    "phase1": "def design_specification_phase(\n    goal: str = \"Create comprehensive design specification enabling independent backend/frontend development for NewsPortal, including Flask routes, HTML templates, and data schemas\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect produces design_spec.md with detailed Flask Routes, HTML Templates, and Data Schema definitions \"\n        \"based on user requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to create comprehensive design specifications for the NewsPortal application that enable Backend and Frontend developers to work independently without dependencies.\n\nTask Details:\n- Read user_task_description from CONTEXT to understand application features and page designs\n- Produce design_spec.md with three key sections: Flask Routes, HTML Templates, and Data Schemas\n- Include ALL necessary information for independent backend and frontend development\n- Preserve exact page element IDs, context variable names/types, and data schema field orders\n- DO NOT assume or add features beyond user requirements\n\n**Section 1: Flask Routes Specification**\n\nCreate a detailed table listing:\n- Route Path and URL pattern (e.g., \"/\", \"/articles/<int:article_id>\")\n- Flask function name (lowercase, underscore separated)\n- HTTP method (GET or POST)\n- Template file to render\n- Context variables passed to templates with explicit types (list, dict, str, int, float)\n- Note any form data expected in POST routes\n\nMust include:\n- Root route '/' redirecting to dashboard page\n- All pages described in user requirements\n- Consistent and descriptive function names aligned with page purposes\n\n**Section 2: HTML Template Specifications**\n\nFor each page template, specify:\n- File path as templates/{template_name}.html\n- Page title for <title> and <h1> tags matching user specification\n- Complete list of element IDs with element types and brief descriptions\n- Context variables available in template including structure of dicts/lists\n- Navigation mappings correlating buttons/links to Flask routes using url_for()\n  - Static and dynamic element ID patterns must be preserved exactly\n- Use Jinja2 templating conventions for dynamic content and loops\n\n**Section 3: Data File Schemas**\n\nFor each data file:\n- File path as data/{filename}.txt\n- Pipe-delimited format (|)\n- Exact field order and names matching user data specification\n- Description of the data content\n- 2-3 realistic example data rows from user examples\n\nRequirements:\n- No header row in files\n- Field order is critical for backend parsing\n- Maintain field naming consistency across all sections\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developers can implement full Flask app.py with only Sections 1 and 3\n- Frontend developers can implement full HTML templates with only Section 2\n- No cross-team assumptions or dependency on source code besides specification\n- Element IDs, function names, and context variables are consistent across all sections\n- Use write_text_file tool to save design_spec.md exactly\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Review design_spec.md for completeness and accuracy of Flask Routes section and Data Schemas section relevant to backend implementation: \"\n                \"correctness of routes, HTTP methods, context variables, and data file schemas.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Review design_spec.md for completeness and accuracy of HTML Templates section: all specified page layouts, element IDs, context variables, and navigation mappings.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Implement backend and frontend in parallel based on design_spec.md for NewsPortal application\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py based on Flask Routes and Data Schemas from design_spec.md. \"\n        \"FrontendDeveloper implements templates/*.html based on HTML Templates section from design_spec.md. \"\n        \"Both agents work independently.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement the complete Flask backend for the NewsPortal application based on the backend sections of the design_spec.md specification document.\n\nTask Details:\n- Read design_spec.md backend sections ONLY (Flask Routes and Data Schemas)\n- Implement all Flask routes defined in the specification with correct HTTP methods and context variables\n- Manage data persistence exclusively via local text files as specified\n- Ensure the root route redirects to the dashboard page\n- Do NOT read or implement any frontend templates or unrelated design sections\n\nImplementation Requirements:\n1. **Flask App Initialization**:\n   # Initialize Flask app with necessary imports\n   '''python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   '''\n\n2. **Root Route**:\n   - Implement '/' route to redirect to dashboard page\n   - Use 'redirect(url_for(...))' for redirection\n\n3. **Data Handling**:\n   - Load and save data from/to local files in 'data/' directory\n   - Parse files with pipe-delimited format (|)\n   - Adhere strictly to field order as specified in data schemas\n   - Gracefully handle file I/O errors and missing data cases\n\n4. **Route Implementations**:\n   - Implement all routes with exact function names from design_spec.md\n   - Use render_template with exact template filenames specified\n   - Pass all context variables as specified with correct types\n   - For POST routes, handle form data processing with request.form\n\n5. **Best Practices**:\n   - Include '__main__' block for app execution\n   - Use url_for() consistently for internal routes\n   - Do not add features beyond the specification\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to write 'app.py'\n- Do NOT include frontend code or templates\n- Ensure perfect matching of function names and context variables from specification\n- Follow file formats and data parsing rules precisely as per data schemas\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to create all HTML template files for the NewsPortal application based on the frontend section of design_spec.md.\n\nTask Details:\n- Read only the HTML Templates section of design_spec.md\n- Implement all specified templates (*.html) with exact page layouts and UI element IDs\n- Include correct page titles as specified\n- Implement navigation using url_for() with exact function names from the spec\n- Do NOT read or implement backend code or data schemas\n- Do NOT add any UI elements or pages not documented in the specification\n\nImplementation Requirements:\n1. **Template File Structure**:\n   '''html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ page_title }}</title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1>{{ page_title }}</h1>\n           <!-- Page content here -->\n       </div>\n   </body>\n   </html>\n   '''\n\n2. **Element IDs**:\n   - Use all element IDs exactly as specified (case-sensitive)\n   - For dynamic elements with variable IDs (e.g., view-article-button-{article_id}), use Jinja2 syntax:\n     id=\"view-article-button-{{ article.article_id }}\"\n\n3. **Navigation Links**:\n   - Use url_for() with exact function names for all navigation buttons and links\n   - For dynamic links including parameters, use Jinja2 variable syntax in url_for calls\n\n4. **Form Elements**:\n   - For pages with forms (e.g., Write Comment), implement form tags with method and action attributes per specification\n   - Use appropriate input types and button IDs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all required template files inside 'templates/' directory\n- Do NOT modify backend or data files\n- Do NOT include any client-side scripting unless specified\n- All element IDs and page titles must be exact matches to spec\n- Navigation must exactly match design_spec.md instructions\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify app.py correctly implements all Flask routes specified in design_spec.md including correct context variables, HTTP methods, and proper file I/O \"\n                \"for data persistence, and ensures the root route redirects to the dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify all HTML templates implement all page layout and UI element ID requirements from design_spec.md, including navigation with correct url_for usage and page titles.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def integration_testing_phase(\n    goal: str = \"Perform integration and functional testing of NewsPortal's backend and frontend to ensure complete feature functionality\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"Tester runs functional tests on combined app.py and templates, reports issues in feedback.txt. \"\n        \"BackendDeveloper fixes backend defects, FrontendDeveloper fixes frontend defects based on feedback. \"\n        \"Loop continues until Tester writes '[APPROVED]' in feedback.txt.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"Tester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in full-stack web application integration and functional testing.\n\nYour goal is to design and execute comprehensive end-to-end integration tests ensuring the NewsPortal application functions correctly as a whole.\n\nTask Details:\n- Read input artifacts: app.py and all templates/*.html from CONTEXT\n- Read feedback.txt from previous test cycles for context\n- Create and run tests covering ALL NewsPortal features as described in user task\n- Write feedback.txt with detailed bug reports or \"[APPROVED]\" if tests pass fully\n- Do NOT modify app.py or templates yourself\n\nTesting Requirements:\n1. **Test Coverage**:\n   - Verify navigation flows between all nine pages (Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results)\n   - Validate display of data from data/*.txt files (articles, categories, bookmarks, comments, trending)\n   - Check dynamic behaviors: buttons working, filtering, sorting, bookmarking, comment submission\n   - Confirm content rendering matches design: element IDs, page titles, context variables\n   - Test data integration: bookmarking persists, comments listed and added correctly, trending filters work\n\n2. **Test Execution**:\n   - Use execute_python_code tool to run app.py in a controlled environment\n   - Simulate user interactions programmatically or describe test steps clearly\n\n3. **Bug Reporting**:\n   - For any failures, write clear reproduction steps, expected vs actual results, and affected components\n   - Write \"NEED_MODIFY\" status and details if issues are detected\n   - Write \"[APPROVED]\" only if all tests pass with no defects\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file to generate/update feedback.txt\n- Include exact status markers: \"[APPROVED]\" or \"NEED_MODIFY\"\n- Feedback file drives phase termination upon \"[APPROVED]\"\n- Use execute_python_code for running backend tests and scripts\n- Do NOT fix code or templates yourself\n- Ensure all feedback is clear and actionable\n\nOutput: feedback.txt\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        },\n        {\n            \"agent_name\": \"BackendDeveloper_Fix\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web application development and debugging.\n\nYour goal is to fix backend defects identified by the Tester to ensure NewsPortal backend works correctly and integrates seamlessly with frontend.\n\nTask Details:\n- Read input artifacts: current app.py and Tester-generated feedback.txt\n- Identify and fix all backend issues reported in feedback.txt related to app.py\n- Maintain existing functionality; do NOT alter frontend files or templates\n- Update app.py with fixes ensuring full compliance with NewsPortal feature specifications\n- Do not introduce new features or change UI behavior\n\nImplementation Instructions:\n1. Analyze feedback.txt carefully to locate backend defects\n2. Focus on data handling, route implementation, data loading from data/*.txt, context variables passed to templates\n3. Fix bugs preventing correct data display, functionality (e.g., bookmarks, comments, trending filters)\n4. Test locally before submission to ensure issues are resolved\n5. Follow existing project coding style and conventions strictly\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file to save fixed app.py\n- Do NOT fix frontend or templates\n- Do NOT add or remove features beyond reported fixes\n- Ensure app.py runs without errors after fixes\n- Provide only updated app.py; no inline explanations or commentary\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper_Fix\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to fix frontend defects reported by the Tester to ensure that all NewsPortal templates render correctly and meet all UI and interaction requirements.\n\nTask Details:\n- Read input artifacts: current templates/*.html files and Tester-generated feedback.txt\n- Identify and fix all frontend issues reported in feedback.txt related to template files\n- Preserve backend code and business logic; do NOT modify app.py\n- Correct element IDs, content rendering, Jinja2 syntax, and navigation links as needed\n- Maintain consistency with NewsPortal page design and interaction specifications\n\nImplementation Instructions:\n1. Analyze feedback.txt systematically to find reported frontend defects\n2. Fix issues like missing or incorrect element IDs, broken navigation buttons, improper context variable usage\n3. Validate template syntax for errors or inconsistencies\n4. Ensure all updated templates pass display and interaction expectations\n5. Use consistent formatting and naming conventions already used\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file to save updated templates/*.html files\n- Do NOT modify backend code (app.py)\n- Do NOT add new pages or features beyond fixing reported issues\n- Deliver only fixed template files; no explanations or comments in output\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\", \"source\": \"Tester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"BackendDeveloper_Fix\",\n            \"review_criteria\": (\n                \"Check that all backend issues in feedback.txt are addressed with fixes applied correctly in app.py.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"Tester\",\n            \"reviewer_agent\": \"FrontendDeveloper_Fix\",\n            \"review_criteria\": (\n                \"Check that all frontend issues in feedback.txt are addressed with fixes applied correctly in templates/*.html.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"feedback.txt\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create comprehensive design specifications for the NewsPortal application that enable Backend and Frontend developers to work independently without dependencies.

Task Details:
- Read user_task_description from CONTEXT to understand application features and page designs
- Produce design_spec.md with three key sections: Flask Routes, HTML Templates, and Data Schemas
- Include ALL necessary information for independent backend and frontend development
- Preserve exact page element IDs, context variable names/types, and data schema field orders
- DO NOT assume or add features beyond user requirements

**Section 1: Flask Routes Specification**

Create a detailed table listing:
- Route Path and URL pattern (e.g., "/", "/articles/<int:article_id>")
- Flask function name (lowercase, underscore separated)
- HTTP method (GET or POST)
- Template file to render
- Context variables passed to templates with explicit types (list, dict, str, int, float)
- Note any form data expected in POST routes

Must include:
- Root route '/' redirecting to dashboard page
- All pages described in user requirements
- Consistent and descriptive function names aligned with page purposes

**Section 2: HTML Template Specifications**

For each page template, specify:
- File path as templates/{template_name}.html
- Page title for <title> and <h1> tags matching user specification
- Complete list of element IDs with element types and brief descriptions
- Context variables available in template including structure of dicts/lists
- Navigation mappings correlating buttons/links to Flask routes using url_for()
  - Static and dynamic element ID patterns must be preserved exactly
- Use Jinja2 templating conventions for dynamic content and loops

**Section 3: Data File Schemas**

For each data file:
- File path as data/{filename}.txt
- Pipe-delimited format (|)
- Exact field order and names matching user data specification
- Description of the data content
- 2-3 realistic example data rows from user examples

Requirements:
- No header row in files
- Field order is critical for backend parsing
- Maintain field naming consistency across all sections

CRITICAL SUCCESS CRITERIA:
- Backend developers can implement full Flask app.py with only Sections 1 and 3
- Frontend developers can implement full HTML templates with only Section 2
- No cross-team assumptions or dependency on source code besides specification
- Element IDs, function names, and context variables are consistent across all sections
- Use write_text_file tool to save design_spec.md exactly

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement the complete Flask backend for the NewsPortal application based on the backend sections of the design_spec.md specification document.

Task Details:
- Read design_spec.md backend sections ONLY (Flask Routes and Data Schemas)
- Implement all Flask routes defined in the specification with correct HTTP methods and context variables
- Manage data persistence exclusively via local text files as specified
- Ensure the root route redirects to the dashboard page
- Do NOT read or implement any frontend templates or unrelated design sections

Implementation Requirements:
1. **Flask App Initialization**:
   # Initialize Flask app with necessary imports
   '''python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   '''

2. **Root Route**:
   - Implement '/' route to redirect to dashboard page
   - Use 'redirect(url_for(...))' for redirection

3. **Data Handling**:
   - Load and save data from/to local files in 'data/' directory
   - Parse files with pipe-delimited format (|)
   - Adhere strictly to field order as specified in data schemas
   - Gracefully handle file I/O errors and missing data cases

4. **Route Implementations**:
   - Implement all routes with exact function names from design_spec.md
   - Use render_template with exact template filenames specified
   - Pass all context variables as specified with correct types
   - For POST routes, handle form data processing with request.form

5. **Best Practices**:
   - Include '__main__' block for app execution
   - Use url_for() consistently for internal routes
   - Do not add features beyond the specification

CRITICAL REQUIREMENTS:
- Use write_text_file tool to write 'app.py'
- Do NOT include frontend code or templates
- Ensure perfect matching of function names and context variables from specification
- Follow file formats and data parsing rules precisely as per data schemas

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

Your goal is to create all HTML template files for the NewsPortal application based on the frontend section of design_spec.md.

Task Details:
- Read only the HTML Templates section of design_spec.md
- Implement all specified templates (*.html) with exact page layouts and UI element IDs
- Include correct page titles as specified
- Implement navigation using url_for() with exact function names from the spec
- Do NOT read or implement backend code or data schemas
- Do NOT add any UI elements or pages not documented in the specification

Implementation Requirements:
1. **Template File Structure**:
   '''html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ page_title }}</title>
   </head>
   <body>
       <div id="main-container-id">
           <h1>{{ page_title }}</h1>
           <!-- Page content here -->
       </div>
   </body>
   </html>
   '''

2. **Element IDs**:
   - Use all element IDs exactly as specified (case-sensitive)
   - For dynamic elements with variable IDs (e.g., view-article-button-{article_id}), use Jinja2 syntax:
     id="view-article-button-{{ article.article_id }}"

3. **Navigation Links**:
   - Use url_for() with exact function names for all navigation buttons and links
   - For dynamic links including parameters, use Jinja2 variable syntax in url_for calls

4. **Form Elements**:
   - For pages with forms (e.g., Write Comment), implement form tags with method and action attributes per specification
   - Use appropriate input types and button IDs

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all required template files inside 'templates/' directory
- Do NOT modify backend or data files
- Do NOT include any client-side scripting unless specified
- All element IDs and page titles must be exact matches to spec
- Navigation must exactly match design_spec.md instructions

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "Tester": {
        "prompt": (
            """You are a Software Test Engineer specializing in full-stack web application integration and functional testing.

Your goal is to design and execute comprehensive end-to-end integration tests ensuring the NewsPortal application functions correctly as a whole.

Task Details:
- Read input artifacts: app.py and all templates/*.html from CONTEXT
- Read feedback.txt from previous test cycles for context
- Create and run tests covering ALL NewsPortal features as described in user task
- Write feedback.txt with detailed bug reports or "[APPROVED]" if tests pass fully
- Do NOT modify app.py or templates yourself

Testing Requirements:
1. **Test Coverage**:
   - Verify navigation flows between all nine pages (Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results)
   - Validate display of data from data/*.txt files (articles, categories, bookmarks, comments, trending)
   - Check dynamic behaviors: buttons working, filtering, sorting, bookmarking, comment submission
   - Confirm content rendering matches design: element IDs, page titles, context variables
   - Test data integration: bookmarking persists, comments listed and added correctly, trending filters work

2. **Test Execution**:
   - Use execute_python_code tool to run app.py in a controlled environment
   - Simulate user interactions programmatically or describe test steps clearly

3. **Bug Reporting**:
   - For any failures, write clear reproduction steps, expected vs actual results, and affected components
   - Write "NEED_MODIFY" status and details if issues are detected
   - Write "[APPROVED]" only if all tests pass with no defects

CRITICAL REQUIREMENTS:
- Use write_text_file to generate/update feedback.txt
- Include exact status markers: "[APPROVED]" or "NEED_MODIFY"
- Feedback file drives phase termination upon "[APPROVED]"
- Use execute_python_code for running backend tests and scripts
- Do NOT fix code or templates yourself
- Ensure all feedback is clear and actionable

Output: feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'feedback.txt', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'feedback.txt'}],
    },

    "BackendDeveloper_Fix": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web application development and debugging.

Your goal is to fix backend defects identified by the Tester to ensure NewsPortal backend works correctly and integrates seamlessly with frontend.

Task Details:
- Read input artifacts: current app.py and Tester-generated feedback.txt
- Identify and fix all backend issues reported in feedback.txt related to app.py
- Maintain existing functionality; do NOT alter frontend files or templates
- Update app.py with fixes ensuring full compliance with NewsPortal feature specifications
- Do not introduce new features or change UI behavior

Implementation Instructions:
1. Analyze feedback.txt carefully to locate backend defects
2. Focus on data handling, route implementation, data loading from data/*.txt, context variables passed to templates
3. Fix bugs preventing correct data display, functionality (e.g., bookmarks, comments, trending filters)
4. Test locally before submission to ensure issues are resolved
5. Follow existing project coding style and conventions strictly

CRITICAL REQUIREMENTS:
- Use write_text_file to save fixed app.py
- Do NOT fix frontend or templates
- Do NOT add or remove features beyond reported fixes
- Ensure app.py runs without errors after fixes
- Provide only updated app.py; no inline explanations or commentary

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'feedback.txt', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper_Fix": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to fix frontend defects reported by the Tester to ensure that all NewsPortal templates render correctly and meet all UI and interaction requirements.

Task Details:
- Read input artifacts: current templates/*.html files and Tester-generated feedback.txt
- Identify and fix all frontend issues reported in feedback.txt related to template files
- Preserve backend code and business logic; do NOT modify app.py
- Correct element IDs, content rendering, Jinja2 syntax, and navigation links as needed
- Maintain consistency with NewsPortal page design and interaction specifications

Implementation Instructions:
1. Analyze feedback.txt systematically to find reported frontend defects
2. Fix issues like missing or incorrect element IDs, broken navigation buttons, improper context variable usage
3. Validate template syntax for errors or inconsistencies
4. Ensure all updated templates pass display and interaction expectations
5. Use consistent formatting and naming conventions already used

CRITICAL REQUIREMENTS:
- Use write_text_file to save updated templates/*.html files
- Do NOT modify backend code (app.py)
- Do NOT add new pages or features beyond fixing reported issues
- Deliver only fixed template files; no explanations or comments in output

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'feedback.txt', 'source': 'Tester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Review design_spec.md for completeness and accuracy of Flask Routes section and Data Schemas section relevant to backend implementation: "
                "correctness of routes, HTTP methods, context variables, and data file schemas.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Review design_spec.md for completeness and accuracy of HTML Templates section: all specified page layouts, element IDs, context variables, and navigation mappings.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify app.py correctly implements all Flask routes specified in design_spec.md including correct context variables, HTTP methods, and proper file I/O "
                "for data persistence, and ensures the root route redirects to the dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify all HTML templates implement all page layout and UI element ID requirements from design_spec.md, including navigation with correct url_for usage and page titles.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'Tester': [
        ("BackendDeveloper_Fix", """Check that all backend issues in feedback.txt are addressed with fixes applied correctly in app.py.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'feedback.txt'}]),
        ("FrontendDeveloper_Fix", """Check that all frontend issues in feedback.txt are addressed with fixes applied correctly in templates/*.html.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'feedback.txt'}])
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
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect to produce design_spec.md with detailed Flask routes, HTML templates, and data schemas
    await execute(SystemArchitect, "Create design_spec.md with Flask Routes, HTML Templates, and Data Schemas based on user_task_description in CONTEXT")
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
        timeout_threshold=180,
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
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement Flask backend app.py based on backend sections of design_spec.md"),
        execute(FrontendDeveloper, "Implement all HTML templates based on HTML Templates section of design_spec.md")
    )
# Phase2_End

# Phase3_Start
import asyncio

async def integration_testing_phase():
    # Create agents
    Tester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=200,
        failure_threshold=1,
        recovery_time=40
    )
    BackendDeveloper_Fix = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper_Fix",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloper_Fix = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper_Fix",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 5
    for iteration in range(MAX_LOOPS):
        # Execute Tester to run integration tests and produce feedback.txt
        if iteration == 0:
            await execute(Tester, "Run full integration and functional tests on NewsPortal app.py and templates")
        else:
            # Read previous feedback.txt and include it for context
            try:
                with open("feedback.txt", "r") as f:
                    feedback_content = f.read()
            except FileNotFoundError:
                feedback_content = ""
            await execute(Tester, f"Re-run tests with latest fixes considering previous feedback:\n{feedback_content}")

        # Read feedback after Tester run
        try:
            with open("feedback.txt", "r") as f:
                feedback_content = f.read()
        except FileNotFoundError:
            # No feedback file means failure or unexpected error; stop looping
            break

        # Check if approval achieved
        if "[APPROVED]" in feedback_content:
            break

        # Parallel fix by BackendDeveloper_Fix and FrontendDeveloper_Fix based on feedback
        await asyncio.gather(
            execute(BackendDeveloper_Fix, "Fix all backend issues reported in feedback.txt and update app.py"),
            execute(FrontendDeveloper_Fix, "Fix all frontend template issues reported in feedback.txt and update templates")
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
        parallel_implementation_phase()
    ]
    step3 = [
        integration_testing_phase()
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
