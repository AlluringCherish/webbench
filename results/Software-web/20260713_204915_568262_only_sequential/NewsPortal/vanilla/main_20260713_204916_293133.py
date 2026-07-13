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
# 20260713_204916_293133/main_20260713_204916_293133.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze the NewsPortal requirements document and produce a complete design_spec.md specifying Flask routes, pages, elements, data contracts, and navigation flows.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first creates requirements_analysis.md tracing every requested page, route, element ID, data file format, navigation path, and feature; \"\n        \"then WebArchitect consumes that to produce design_spec.md detailing Flask route methods, exact page titles, element IDs, directory layout, and data contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in web application requirements documentation.\n\nYour goal is to analyze the NewsPortal user task input and produce a comprehensive requirements_analysis.md tracing every required page, route, element ID, data file format with examples, page-to-template mappings, navigation flows, and key features like bookmarks, comments, and trending articles.\n\nTask Details:\n- Read complete user_task_description artifact from CONTEXT.\n- Create requirements_analysis.md documenting all 9 pages: Dashboard, Article Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending Articles, Category, Search Results.\n- Trace all route paths and HTTP methods implied by navigation and functionalities.\n- List exact element IDs on each page with type and description.\n- Outline data file formats with sample records for articles, categories, bookmarks, comments, trending.\n- Detail navigation buttons and links mapping between pages and key user flows.\n- Highlight bookmark, comment posting, trending tracking functionality.\n\nInstructions:\n1. Analyze user_task_description for structural and functional requirements.\n2. Organize requirements_analysis.md into sections by page and data files.\n3. For each page, list all element IDs exactly as specified.\n4. For each data file, specify exact field order, pipe-delimited format, and example data usage.\n5. Define inter-page navigation paths and button/element mappings.\n6. Provide clear, structured documentation to enable precise design specification downstream.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output requirements_analysis.md.\n- Preserve exact element IDs as specified, maintain data format details accurately.\n- Focus on full coverage of all pages, routes, data contracts, and navigation flows.\n- Generate clear, organized documentation suitable for consumption by WebArchitect.\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specializing in Flask web application architectures.\n\nYour goal is to create a detailed design_spec.md that defines the complete Flask app architecture for NewsPortal, including comprehensive route listings, HTTP methods, exact page titles, all element IDs per page, templates directory structure, data file parsing rules and contracts for articles, categories, bookmarks, comments, and trending data, and UI navigation flows.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md artifacts from CONTEXT.\n- Produce design_spec.md listing ALL Flask routes with URL paths, HTTP method (GET/POST), function names (snake_case), and corresponding template filenames.\n- Specify exact page titles for each route template.\n- Enumerate all exact element IDs on each page as in requirements_analysis.md.\n- Define data file parsing details: file names, pipe-separated fields in exact order, field meanings, and example data for articles.txt, categories.txt, bookmarks.txt, comments.txt, trending.txt.\n- Document UI navigation button/link mappings with source element IDs and target routes.\n- Structure specification to facilitate downstream implementation of backend, frontend, and data loading.\n\nImplementation Instructions:\n1. Layout design_spec.md in clear sections: Flask Routes, Page Titles & Elements, Data Schema, Navigation Flows.\n2. Flask Routes Section should list every route including parameterized URLs (e.g., /articles/<int:article_id>).\n3. Data Schema Section must specify exact field order for each .txt file and sample data rows.\n4. Navigation Flows should map buttons (by element ID) to Flask route functions/actions.\n5. Consistency rules: Function names must be snake_case and descriptive; Template names consistent with page names (e.g. dashboard.html).\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_spec.md.\n- Ensure all page titles and element IDs exactly match input specifications.\n- Design document must be self-sufficient for developers to implement without further clarifications.\n- Maintain precise field order and pipe-delimited format for data schemas.\n- Fully cover all pages, routes, navigation, and data contracts outlined by requirements_analysis.md.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify requirements_analysis.md includes all page elements, exact requested element IDs, all data file formats with examples, and detailed navigation flows.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"WebArchitect\",\n            \"reviewer_agent\": \"ImplementationEngineer\",\n            \"review_criteria\": (\n                \"Ensure design_spec.md fully implements all requirements from requirements_analysis.md, including precise Flask routes, template names, data file parsing contracts, \"\n                \"page titles, element IDs, and correct navigation button actions.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement NewsPortal as a Flask application with exact Flask routes, app.py, and templates/*.html files according to design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineer writes a complete app.py with all routes and logic per design_spec.md; TemplateDesigner writes all templates/*.html files with exact element IDs and content structure; \"\n        \"IntegrationEngineer integrates app.py and templates ensuring no draft paths remain and all features function as specified.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineer\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications and local text data processing.\n\nYour goal is to implement a complete Flask backend (app.py) with all routes and logic as specified in the design specification, focusing on data loading from local text files and handling user interactions such as browsing articles, reading details, bookmarking, commenting, trending articles, and filtering.\n\nTask Details:\n- Read design_spec.md from WebArchitect and extract all route specifications, HTTP methods, and data schema details\n- Implement app.py with complete Flask routes handling logic for all pages: Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results\n- Load data exclusively from data/*.txt files using exact field orders and parsing rules as specified\n- Do NOT implement frontend templates or modify template files\n- Output a fully functional app.py that supports all specified features and navigation\n\nImplementation Requirements:\n1. **Flask Setup & Routing**\n   - Set up Flask app with appropriate configurations\n   - Define all routes with exact function names and HTTP methods from design_spec.md\n   - Implement redirects and route parameters as specified\n\n2. **Data Loading & Parsing**\n   - Read local text files from data/ directory using pipe-delimited parsing\n   - Parse each file according to exact field order given in design_spec.md\n   - Create data structures (lists/dictionaries) for use in routes\n\n3. **Route Logic**\n   - Implement data filtering, searching, sorting, and pagination as needed based on query parameters\n   - Handle bookmarking and comment submission logic, updating in-memory or storage as specified\n   - Pass precise context variables to templates matching design_spec.md exactly\n\n4. **Error Handling**\n   - Handle file read errors gracefully\n   - Handle missing data or invalid route parameters\n\n5. **Flask Best Practices**\n   - Use render_template() correctly with exact template file names\n   - Use url_for() for redirects and links internally\n   - Include main entry point with debug mode for local testing\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the final app.py\n- Ensure all Flask routes and context variables strictly follow design_spec.md\n- Load data strictly according to data file formats and field orders\n- Do NOT include any UI/HTML code in this agent's output\n- Do NOT introduce features beyond design_spec.md scope\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"TemplateDesigner\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.\n\nYour goal is to create complete, fully functional HTML templates under the templates/ directory with exact element IDs and page structures as specified in the design specification, ensuring all pages are correctly represented including Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, and Search Results pages.\n\nTask Details:\n- Read design_spec.md from WebArchitect, focusing on the HTML template section including exact element IDs and page content requirements\n- Implement all HTML files for the specified pages with the exact file naming conventions and directory structure\n- Use Jinja2 syntax to represent dynamic content with context variables matching design_spec.md\n- Include all required elements with exact IDs (case-sensitive)\n- Do NOT implement backend logic, routes, or data loading—focus solely on templates\n- Ensure navigation buttons and links have correct href attributes using url_for() calls as specified\n\nImplementation Requirements:\n1. **Template Structure**\n   - Create valid HTML5 documents with proper structure: doctype, head with <title>, body with container divs\n   - Include <h1> tags with page titles matching design_spec.md exactly\n\n2. **Element IDs & Content**\n   - Use exact IDs for all static and dynamic elements as specified\n   - For dynamic elements with IDs containing variables (e.g., view-article-button-{article_id}), implement with Jinja2 variable interpolation\n\n3. **Context Variables & Jinja2 Syntax**\n   - Use Jinja2 templating to loop over collections, display variables, and conditionally render sections as needed\n   - Match variable naming exactly as specified to ensure consistency with backend\n\n4. **Navigation & Links**\n   - Implement all navigation buttons and links with url_for() calls exactly as specified\n   - Use form tags and buttons for POST routes where necessary\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all templates as separate files under templates/ directory\n- All element IDs must be exact matches (case-sensitive)\n- Page titles in <title> and <h1> must exactly match design_spec.md\n- Navigation must use url_for() with correct endpoints and parameters\n- Do NOT include backend code or data processing in templates\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in integrating Flask backend and frontend templates into a cohesive web application.\n\nYour goal is to integrate the backend app.py and all frontend template files into a working NewsPortal application, resolving all draft placeholders, ensuring correct render_template usage, data parsing from text files, and validating that all navigation elements correctly route to their destinations.\n\nTask Details:\n- Read design_spec.md, the completed app.py from ImplementationEngineer, and templates/*.html from TemplateDesigner\n- Remove any draft, placeholder, or temporary references in app.py and templates\n- Ensure render_template calls in app.py reference the correct template filenames exactly\n- Verify that data loading and parsing logic in app.py complies with design_spec.md data schemas\n- Check navigation buttons and links in templates use proper Flask url_for endpoints consistent with app.py routes\n- Integrate error handling for missing pages or data gracefully\n- Prepare finalized app.py and templates/*.html files that form a complete, runnable Flask application matching design_spec.md\n\nIntegration Requirements:\n1. **Code Cleanup**\n   - Remove comments or code snippets indicating incomplete or draft status\n   - Check for consistency and completeness between backend and frontend\n\n2. **Navigation Validation**\n   - Test that all internal redirects and URL generations correspond to actual routes\n   - Verify all buttons and links use exact IDs and href attributes as specified\n\n3. **Data Parsing Consistency**\n   - Confirm data files are parsed correctly and no mismatch in field orders or names\n   - Ensure context variables passed to templates are in sync\n\n4. **Finalization**\n   - Output finalized app.py and all template files in templates/ directory, ready for deployment\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save finalized app.py and all template files\n- Maintain exact filenames and folder paths for all outputs\n- Ensure no draft or placeholder references remain\n- Output must comply with design_spec.md fully to pass validation\n- Do NOT alter template content beyond integration fixes and navigation correctness\n- Do NOT add new features or change file formats\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"TemplateDesigner\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Verify app.py implements all routes and data loading exactly as design_spec.md requires, especially handling data files, navigation buttons, and page responses.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"TemplateDesigner\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": (\n                \"Verify all templates/*.html contain every required element with exact IDs, page titles, and structure, and that navigation buttons and links match design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"IntegrationEngineer\",\n            \"reviewer_agent\": \"WebValidator\",\n            \"review_criteria\": (\n                \"Assess the integrated app.py and templates/*.html form a runnable Flask web app adhering to design_spec.md and requirements_analysis.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Validate the NewsPortal Flask application for correctness, completeness, and usability, then produce validation_report.md with actionable fixes.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator runs full Flask application verification, checking route correctness, page rendering, data loading, navigation, and UI completeness; \"\n        \"SequentialFixer then applies fixes from validation_report.md to finalize app.py and templates.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Web Validator expert specializing in Flask web application quality assurance and functional validation.\n\nYour goal is to validate the complete Flask web application, ensuring correctness, completeness, and usability across all features and pages. Produce a detailed validation_report.md with actionable findings and improvement suggestions.\n\nTask Details:\n- Read design_spec.md, app.py, and all templates (*.html)\n- Verify all Flask routes exist, function, and match design_spec.md specifications\n- Check data file reading in app.py matches design_spec data schemas and field orders\n- Validate all page templates have exact element IDs as specified, including dynamic ID patterns\n- Confirm navigation buttons correctly link to intended routes as per design_spec.md\n- Assess that the app displays expected content for representative pages (dashboard, article details, bookmarks, comments, trending, etc.)\n- Do not modify code; produce a clear report of issues and fixes\n\nValidation Requirements:\n\n**1. Flask Application Verification**\n- Use validate_python_file tool on app.py for syntax/runtime errors\n- Execute key Flask routes using execute_python_code to verify responses & context variables\n- Confirm all routes from design_spec.md exist and handle GET/POST methods properly\n\n**2. Template and UI Checks**\n- For each HTML template, verify presence of ALL required static and dynamic element IDs exactly as specified\n- Ensure navigation buttons link correctly via url_for() routes matching Flask app.py endpoints\n- Confirm page titles match exactly design_spec.md requirements\n\n**3. Data Loading Validation**\n- Check that app.py reads data from all specified data files (articles.txt, categories.txt, bookmarks.txt, comments.txt, trending.txt)\n- Verify parsing follows correct pipe-delimited format and field order as defined in design_spec.md\n\nReport Requirements:\n- Create validation_report.md explaining all detected issues with detailed descriptions\n- Provide exact fix instructions (file, location, expected/correct content)\n- Include severity levels: Critical, Major, Minor\n- Summarize overall compliance and readiness status\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for app.py checks\n- Use write_text_file tool to output validation_report.md\n- Provide clear, actionable feedback for SequentialFixer to implement\n- Do NOT modify any source files yourself\n- Keep report organized and easy to follow\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Sequential Fixer specializing in debugging and refining Flask web applications and their frontend templates.\n\nYour goal is to apply all corrections from validation_report.md to fully fix and finalize app.py and all templates (*.html), ensuring the application meets design specifications and user requirements exactly.\n\nTask Details:\n- Read design_spec.md, app.py, templates/*.html, and validation_report.md\n- Identify all reported issues and instructions in validation_report.md\n- Modify app.py and HTML templates to fix syntax errors, route issues, data loading errors, element ID mismatches, navigation links, and content inaccuracies\n- Ensure all fixes strictly follow design_spec.md specifications and required data formats\n- Preserve app functionality and UI/UX consistency\n\nImplementation Requirements:\n\n1. **Code Fixes**\n- Correct any syntax or runtime errors in app.py identified by validation_report.md\n- Ensure all Flask routes exist and implementation matches specification for parameters, methods, templates, and context variables\n- Fix data loading logic for all data files; parsing must strictly use pipe-delimited format and specified field orders\n\n2. **Template Corrections**\n- Add or correct all missing or incorrect element IDs, including dynamic IDs with proper Jinja2 syntax\n- Fix navigation button hrefs to use correct url_for() functions matching app.py routes\n- Update page titles and UI elements to exactly match design_spec.md\n\n3. **Quality Assurance**\n- Review each modification to avoid regressions or new issues\n- Maintain coding and templating best practices for readability and maintainability\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the fixed app.py and templates/*.html files\n- Do NOT add features beyond those specified in design_spec.md\n- Each fix must be traceable to specific validation report instructions\n- Deliver a fully functional, standards-compliant Flask app and frontend\n- Avoid modifying files not listed as input/output artifacts\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Verify validation_report.md comprehensively covers route correctness, data file parsing, element IDs, navigation, and includes clear fix instructions.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Validate that the finalized app.py and templates/*.html fully resolve all validation issues and meet user requirements completely.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
    "RequirementsAnalyst": {
        "prompt": (
            """You are a Requirements Analyst specializing in web application requirements documentation.

Your goal is to analyze the NewsPortal user task input and produce a comprehensive requirements_analysis.md tracing every required page, route, element ID, data file format with examples, page-to-template mappings, navigation flows, and key features like bookmarks, comments, and trending articles.

Task Details:
- Read complete user_task_description artifact from CONTEXT.
- Create requirements_analysis.md documenting all 9 pages: Dashboard, Article Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending Articles, Category, Search Results.
- Trace all route paths and HTTP methods implied by navigation and functionalities.
- List exact element IDs on each page with type and description.
- Outline data file formats with sample records for articles, categories, bookmarks, comments, trending.
- Detail navigation buttons and links mapping between pages and key user flows.
- Highlight bookmark, comment posting, trending tracking functionality.

Instructions:
1. Analyze user_task_description for structural and functional requirements.
2. Organize requirements_analysis.md into sections by page and data files.
3. For each page, list all element IDs exactly as specified.
4. For each data file, specify exact field order, pipe-delimited format, and example data usage.
5. Define inter-page navigation paths and button/element mappings.
6. Provide clear, structured documentation to enable precise design specification downstream.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md.
- Preserve exact element IDs as specified, maintain data format details accurately.
- Focus on full coverage of all pages, routes, data contracts, and navigation flows.
- Generate clear, organized documentation suitable for consumption by WebArchitect.

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specializing in Flask web application architectures.

Your goal is to create a detailed design_spec.md that defines the complete Flask app architecture for NewsPortal, including comprehensive route listings, HTTP methods, exact page titles, all element IDs per page, templates directory structure, data file parsing rules and contracts for articles, categories, bookmarks, comments, and trending data, and UI navigation flows.

Task Details:
- Read user_task_description and requirements_analysis.md artifacts from CONTEXT.
- Produce design_spec.md listing ALL Flask routes with URL paths, HTTP method (GET/POST), function names (snake_case), and corresponding template filenames.
- Specify exact page titles for each route template.
- Enumerate all exact element IDs on each page as in requirements_analysis.md.
- Define data file parsing details: file names, pipe-separated fields in exact order, field meanings, and example data for articles.txt, categories.txt, bookmarks.txt, comments.txt, trending.txt.
- Document UI navigation button/link mappings with source element IDs and target routes.
- Structure specification to facilitate downstream implementation of backend, frontend, and data loading.

Implementation Instructions:
1. Layout design_spec.md in clear sections: Flask Routes, Page Titles & Elements, Data Schema, Navigation Flows.
2. Flask Routes Section should list every route including parameterized URLs (e.g., /articles/<int:article_id>).
3. Data Schema Section must specify exact field order for each .txt file and sample data rows.
4. Navigation Flows should map buttons (by element ID) to Flask route functions/actions.
5. Consistency rules: Function names must be snake_case and descriptive; Template names consistent with page names (e.g. dashboard.html).

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_spec.md.
- Ensure all page titles and element IDs exactly match input specifications.
- Design document must be self-sufficient for developers to implement without further clarifications.
- Maintain precise field order and pipe-delimited format for data schemas.
- Fully cover all pages, routes, navigation, and data contracts outlined by requirements_analysis.md.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineer": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications and local text data processing.

Your goal is to implement a complete Flask backend (app.py) with all routes and logic as specified in the design specification, focusing on data loading from local text files and handling user interactions such as browsing articles, reading details, bookmarking, commenting, trending articles, and filtering.

Task Details:
- Read design_spec.md from WebArchitect and extract all route specifications, HTTP methods, and data schema details
- Implement app.py with complete Flask routes handling logic for all pages: Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results
- Load data exclusively from data/*.txt files using exact field orders and parsing rules as specified
- Do NOT implement frontend templates or modify template files
- Output a fully functional app.py that supports all specified features and navigation

Implementation Requirements:
1. **Flask Setup & Routing**
   - Set up Flask app with appropriate configurations
   - Define all routes with exact function names and HTTP methods from design_spec.md
   - Implement redirects and route parameters as specified

2. **Data Loading & Parsing**
   - Read local text files from data/ directory using pipe-delimited parsing
   - Parse each file according to exact field order given in design_spec.md
   - Create data structures (lists/dictionaries) for use in routes

3. **Route Logic**
   - Implement data filtering, searching, sorting, and pagination as needed based on query parameters
   - Handle bookmarking and comment submission logic, updating in-memory or storage as specified
   - Pass precise context variables to templates matching design_spec.md exactly

4. **Error Handling**
   - Handle file read errors gracefully
   - Handle missing data or invalid route parameters

5. **Flask Best Practices**
   - Use render_template() correctly with exact template file names
   - Use url_for() for redirects and links internally
   - Include main entry point with debug mode for local testing

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the final app.py
- Ensure all Flask routes and context variables strictly follow design_spec.md
- Load data strictly according to data file formats and field orders
- Do NOT include any UI/HTML code in this agent's output
- Do NOT introduce features beyond design_spec.md scope

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "TemplateDesigner": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to create complete, fully functional HTML templates under the templates/ directory with exact element IDs and page structures as specified in the design specification, ensuring all pages are correctly represented including Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, and Search Results pages.

Task Details:
- Read design_spec.md from WebArchitect, focusing on the HTML template section including exact element IDs and page content requirements
- Implement all HTML files for the specified pages with the exact file naming conventions and directory structure
- Use Jinja2 syntax to represent dynamic content with context variables matching design_spec.md
- Include all required elements with exact IDs (case-sensitive)
- Do NOT implement backend logic, routes, or data loading—focus solely on templates
- Ensure navigation buttons and links have correct href attributes using url_for() calls as specified

Implementation Requirements:
1. **Template Structure**
   - Create valid HTML5 documents with proper structure: doctype, head with <title>, body with container divs
   - Include <h1> tags with page titles matching design_spec.md exactly

2. **Element IDs & Content**
   - Use exact IDs for all static and dynamic elements as specified
   - For dynamic elements with IDs containing variables (e.g., view-article-button-{article_id}), implement with Jinja2 variable interpolation

3. **Context Variables & Jinja2 Syntax**
   - Use Jinja2 templating to loop over collections, display variables, and conditionally render sections as needed
   - Match variable naming exactly as specified to ensure consistency with backend

4. **Navigation & Links**
   - Implement all navigation buttons and links with url_for() calls exactly as specified
   - Use form tags and buttons for POST routes where necessary

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all templates as separate files under templates/ directory
- All element IDs must be exact matches (case-sensitive)
- Page titles in <title> and <h1> must exactly match design_spec.md
- Navigation must use url_for() with correct endpoints and parameters
- Do NOT include backend code or data processing in templates

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Software Integration Engineer specializing in integrating Flask backend and frontend templates into a cohesive web application.

Your goal is to integrate the backend app.py and all frontend template files into a working NewsPortal application, resolving all draft placeholders, ensuring correct render_template usage, data parsing from text files, and validating that all navigation elements correctly route to their destinations.

Task Details:
- Read design_spec.md, the completed app.py from ImplementationEngineer, and templates/*.html from TemplateDesigner
- Remove any draft, placeholder, or temporary references in app.py and templates
- Ensure render_template calls in app.py reference the correct template filenames exactly
- Verify that data loading and parsing logic in app.py complies with design_spec.md data schemas
- Check navigation buttons and links in templates use proper Flask url_for endpoints consistent with app.py routes
- Integrate error handling for missing pages or data gracefully
- Prepare finalized app.py and templates/*.html files that form a complete, runnable Flask application matching design_spec.md

Integration Requirements:
1. **Code Cleanup**
   - Remove comments or code snippets indicating incomplete or draft status
   - Check for consistency and completeness between backend and frontend

2. **Navigation Validation**
   - Test that all internal redirects and URL generations correspond to actual routes
   - Verify all buttons and links use exact IDs and href attributes as specified

3. **Data Parsing Consistency**
   - Confirm data files are parsed correctly and no mismatch in field orders or names
   - Ensure context variables passed to templates are in sync

4. **Finalization**
   - Output finalized app.py and all template files in templates/ directory, ready for deployment

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save finalized app.py and all template files
- Maintain exact filenames and folder paths for all outputs
- Ensure no draft or placeholder references remain
- Output must comply with design_spec.md fully to pass validation
- Do NOT alter template content beyond integration fixes and navigation correctness
- Do NOT add new features or change file formats

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'TemplateDesigner'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Web Validator expert specializing in Flask web application quality assurance and functional validation.

Your goal is to validate the complete Flask web application, ensuring correctness, completeness, and usability across all features and pages. Produce a detailed validation_report.md with actionable findings and improvement suggestions.

Task Details:
- Read design_spec.md, app.py, and all templates (*.html)
- Verify all Flask routes exist, function, and match design_spec.md specifications
- Check data file reading in app.py matches design_spec data schemas and field orders
- Validate all page templates have exact element IDs as specified, including dynamic ID patterns
- Confirm navigation buttons correctly link to intended routes as per design_spec.md
- Assess that the app displays expected content for representative pages (dashboard, article details, bookmarks, comments, trending, etc.)
- Do not modify code; produce a clear report of issues and fixes

Validation Requirements:

**1. Flask Application Verification**
- Use validate_python_file tool on app.py for syntax/runtime errors
- Execute key Flask routes using execute_python_code to verify responses & context variables
- Confirm all routes from design_spec.md exist and handle GET/POST methods properly

**2. Template and UI Checks**
- For each HTML template, verify presence of ALL required static and dynamic element IDs exactly as specified
- Ensure navigation buttons link correctly via url_for() routes matching Flask app.py endpoints
- Confirm page titles match exactly design_spec.md requirements

**3. Data Loading Validation**
- Check that app.py reads data from all specified data files (articles.txt, categories.txt, bookmarks.txt, comments.txt, trending.txt)
- Verify parsing follows correct pipe-delimited format and field order as defined in design_spec.md

Report Requirements:
- Create validation_report.md explaining all detected issues with detailed descriptions
- Provide exact fix instructions (file, location, expected/correct content)
- Include severity levels: Critical, Major, Minor
- Summarize overall compliance and readiness status

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for app.py checks
- Use write_text_file tool to output validation_report.md
- Provide clear, actionable feedback for SequentialFixer to implement
- Do NOT modify any source files yourself
- Keep report organized and easy to follow

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Sequential Fixer specializing in debugging and refining Flask web applications and their frontend templates.

Your goal is to apply all corrections from validation_report.md to fully fix and finalize app.py and all templates (*.html), ensuring the application meets design specifications and user requirements exactly.

Task Details:
- Read design_spec.md, app.py, templates/*.html, and validation_report.md
- Identify all reported issues and instructions in validation_report.md
- Modify app.py and HTML templates to fix syntax errors, route issues, data loading errors, element ID mismatches, navigation links, and content inaccuracies
- Ensure all fixes strictly follow design_spec.md specifications and required data formats
- Preserve app functionality and UI/UX consistency

Implementation Requirements:

1. **Code Fixes**
- Correct any syntax or runtime errors in app.py identified by validation_report.md
- Ensure all Flask routes exist and implementation matches specification for parameters, methods, templates, and context variables
- Fix data loading logic for all data files; parsing must strictly use pipe-delimited format and specified field orders

2. **Template Corrections**
- Add or correct all missing or incorrect element IDs, including dynamic IDs with proper Jinja2 syntax
- Fix navigation button hrefs to use correct url_for() functions matching app.py routes
- Update page titles and UI elements to exactly match design_spec.md

3. **Quality Assurance**
- Review each modification to avoid regressions or new issues
- Maintain coding and templating best practices for readability and maintainability

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the fixed app.py and templates/*.html files
- Do NOT add features beyond those specified in design_spec.md
- Each fix must be traceable to specific validation report instructions
- Deliver a fully functional, standards-compliant Flask app and frontend
- Avoid modifying files not listed as input/output artifacts

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify requirements_analysis.md includes all page elements, exact requested element IDs, all data file formats with examples, and detailed navigation flows.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'WebArchitect': [
        ("ImplementationEngineer", """Ensure design_spec.md fully implements all requirements from requirements_analysis.md, including precise Flask routes, template names, data file parsing contracts, "
                "page titles, element IDs, and correct navigation button actions.""", [{'type': 'text_file', 'name': 'requirements_analysis.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineer': [
        ("IntegrationEngineer", """Verify app.py implements all routes and data loading exactly as design_spec.md requires, especially handling data files, navigation buttons, and page responses.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'TemplateDesigner': [
        ("IntegrationEngineer", """Verify all templates/*.html contain every required element with exact IDs, page titles, and structure, and that navigation buttons and links match design_spec.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'IntegrationEngineer': [
        ("WebValidator", """Assess the integrated app.py and templates/*.html form a runnable Flask web app adhering to design_spec.md and requirements_analysis.md.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Verify validation_report.md comprehensively covers route correctness, data file parsing, element IDs, navigation, and includes clear fix instructions.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Validate that the finalized app.py and templates/*.html fully resolve all validation issues and meet user requirements completely.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Create agents RequirementsAnalyst and WebArchitect
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution flow
    # Step 1: RequirementsAnalyst creates requirements_analysis.md from user_task_description
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md tracing all pages, routes, element IDs, data file formats with example data, navigation flows, bookmarks, comments, trending features.")

    # Step 2: WebArchitect creates design_spec.md using user_task_description and requirements_analysis.md
    # Read requirements_analysis.md content for injection
    req_analysis_content = ""
    try:
        req_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    user_task_desc = ""
    entries = CONTEXT.get("user_task_description", [])
    if entries:
        user_task_desc = entries[-1]["content"]

    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md to produce design_spec.md with complete Flask routes (paths, methods, function names), exact page titles, element IDs per page, data file parsing contracts with field orders and examples, and UI navigation mappings.\n\n=== requirements_analysis.md ===\n{req_analysis_content}\n\n=== user_task_description ===\n{user_task_desc}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Create agents with parameters for Phase 2
    ImplementationEngineer = build_resilient_agent(
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    TemplateDesigner = build_resilient_agent(
        agent_name="TemplateDesigner",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=50
    )

    # Read input artifact content for injection
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except Exception:
        pass
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    try:
        # For templates/*.html, assume merged or empty string for injection
        import glob
        templates_files = glob.glob("templates/*.html")
        all_templates_content = []
        for file_path in templates_files:
            try:
                content = open(file_path).read()
                all_templates_content.append(f"=== {file_path} ===\n{content}\n")
            except Exception:
                pass
        templates_content = "\n".join(all_templates_content)
    except Exception:
        pass

    # Sequential execution based on Sequential Flow
    # 1. ImplementationEngineer creates app.py
    # 2. TemplateDesigner creates templates/*.html
    # 3. IntegrationEngineer integrates and finalizes app.py and templates/*.html

    await execute(ImplementationEngineer,
                  "Implement complete app.py with all Flask routes and logic strictly following design_spec.md. "
                  "Use design_spec.md content for reference.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}")

    await execute(TemplateDesigner,
                  "Implement all HTML templates (*.html) with exact element IDs and content structure per design_spec.md.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}")

    await execute(IntegrationEngineer,
                  "Integrate app.py and templates/*.html files, removing any draft or placeholder references. "
                  "Ensure render_template calls and navigation buttons/links use correct routes and file names. "
                  "Validate data loading and context variable consistency with design_spec.md.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Build WebValidator agent
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )

    # Build SequentialFixer agent
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=45
    )

    # Read files for injection
    design_spec_md = ""
    app_py = ""
    templates_html = ""
    validation_report_md = ""

    try:
        design_spec_md = open("design_spec.md").read()
    except:
        pass

    try:
        app_py = open("app.py").read()
    except:
        pass

    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_list = []
        for tpl_file in template_files:
            try:
                content = open(tpl_file).read()
                templates_list.append(f"=== {tpl_file} ===\n{content}\n")
            except:
                templates_list.append(f"=== {tpl_file} ===\n[Unable to read]\n")
        templates_html = "\n".join(templates_list)
    except:
        pass

    # Step 1: WebValidator runs full Flask app validation
    await execute(WebValidator,
                  f"Validate the Flask app as per specifications.\n"
                  f"=== design_spec.md ===\n{design_spec_md}\n\n"
                  f"=== app.py ===\n{app_py}\n\n"
                  f"=== templates/*.html ===\n{templates_html}\n\n"
                  "Use validate_python_file on app.py, execute key Flask routes with execute_python_code, check routes, templates, element IDs, navigation, and data loading.\n"
                  "Output validation_report.md.")

    # Read validation_report.md to inject into SequentialFixer
    try:
        validation_report_md = open("validation_report.md").read()
    except:
        pass

    # Step 2: SequentialFixer applies all fixes based on validation_report.md
    await execute(SequentialFixer,
                  f"Apply all fixes as detailed in validation_report.md to app.py and templates/*.html.\n"
                  f"=== design_spec.md ===\n{design_spec_md}\n\n"
                  f"=== app.py ===\n{app_py}\n\n"
                  f"=== templates/*.html ===\n{templates_html}\n\n"
                  f"=== validation_report.md ===\n{validation_report_md}\n\n"
                  "Produce corrected app.py and templates/*.html.")
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
