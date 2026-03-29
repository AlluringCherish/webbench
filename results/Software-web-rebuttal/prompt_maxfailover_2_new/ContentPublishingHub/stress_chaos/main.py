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
    "phase1": "def requirements_analysis_phase(\n    goal: str = \"Analyze content publishing system requirements and produce a detailed design specification document\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst reads the user task description and creates design_spec.md covering \"\n        \"Flask routes, HTML templates structure with element IDs, and data schema specifications.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Software Requirements Analyst specializing in comprehensive design specifications for Flask web applications.\n\nYour goal is to analyze detailed user requirements to produce a thorough design specification document enabling separate backend and frontend development. The deliverable is design_spec.md containing complete Flask routes, HTML template structures with element IDs, and precise data schema definitions.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Create design_spec.md describing all required Flask routes with methods, URL patterns, and context variables\n- Specify HTML template structures for all pages, including exact element IDs as per requirements\n- Detail data file schemas with exact field order, format, and example data from provided specifications\n- Do NOT assume unprovided requirements or modify input/output artifact definitions\n\n**Section 1: Flask Routes Specification**\n\n- List all required routes (e.g., /dashboard, /article/create, /article/<article_id>/edit)\n- Specify HTTP methods (GET, POST) for each route\n- Define function names clearly and consistently (lowercase with underscores)\n- Specify template names rendered per route\n- Detail context variables passed to templates with their types and structures\n\n**Section 2: HTML Template Structure**\n\n- For each HTML template file (e.g., dashboard.html), specify:\n  - Page container element with exact id\n  - All required element IDs exactly as specified in the requirements\n  - Button IDs, input fields, dropdowns, tables, grids as appropriate\n- Define the expected page layout and navigation elements (buttons linking to routes)\n- Ensure element IDs and names match the backend context variables where applicable\n\n**Section 3: Data File Schemas**\n\n- For each data file (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt):\n  - Specify exact pipe-delimited field order\n  - Describe each field’s meaning and data type\n  - Provide example data rows as given\n  - Clarify any enumerations or status codes used (e.g., article status values)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_spec.md\n- design_spec.md must enable backend and frontend developers to implement their parts independently without ambiguity\n- Follow exactly the input and output artifact definitions without additions or omissions\n- Do NOT include implementation code or application logic, only design specification\n- Ensure all elements and data schemas included match the user task and phase descriptions precisely\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Review design_spec.md for completeness of backend routes and data schema coverage \"\n                \"including all CRUD operations, versioning, approvals, comments, analytics, and navigation routes.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"FrontendDesigner\",\n            \"review_criteria\": (\n                \"Review design_spec.md for completeness and correctness of frontend templates \"\n                \"including element IDs, page layout, buttons, navigational links, and user interactions.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def architecture_design_phase(\n    goal: str = \"Create detailed architectural design document guiding backend and frontend implementation\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect generates architecture.md based on design_spec.md including \"\n        \"Flask app structure, data access layers, routing logic, version control design, \"\n        \"and integration points with frontend templates.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in backend architecture design for Flask web applications.\n\nYour goal is to develop a detailed architectural design document that guides both backend and frontend implementation teams.\n\nTask Details:\n- Read design_spec.md from CONTEXT to understand application requirements and page designs\n- Create architecture.md detailing backend system design, Flask app modules, data flow, routing logic, and API endpoints\n- Specify version control mechanisms and explain integration points with frontend templates\n- Do NOT implement code or frontend templates; focus strictly on architecture documentation\n\n**Section 1: Backend System Design**\n\n- Describe Flask application structure with modules and packages\n- Define responsibilities of each module (routing, data access, business logic, version control)\n- Explain how data files (data/*.txt) will be accessed and managed\n- Detail data flow between components and layers\n\n**Section 2: Routing and API Endpoints**\n\n- List all Flask routes derived from design_spec.md pages with method types (GET/POST)\n- Map routes to controller functions and expected input/output\n- Include patterns for dynamic routes (e.g., article_id parameters)\n- Clarify handling of user sessions and authentication considerations if any\n\n**Section 3: Version Control Design**\n\n- Define architecture for article versioning and approval workflow\n- Specify how version history, approvals, and comments relate to articles and versions\n- Explain storage interaction with article_versions.txt, approvals.txt, comments.txt\n\n**Section 4: Frontend Integration Points**\n\n- Describe how backend passes data and context variables to frontend templates\n- Specify endpoint responses to support frontend page rendering\n- Highlight areas requiring close coordination with frontend design (e.g., data structures expected)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save architecture.md\n- Follow input schema and artifact naming conventions precisely\n- Do NOT include implementation code or frontend markup\n- Ensure document enables independent backend/frontend implementation based on architecture.md alone\n\nOutput: architecture.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"architecture.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Validate architecture.md aligns with design_spec.md requirements and covers all functional areas adequately.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"architecture.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDesigner\",\n            \"review_criteria\": (\n                \"Check architecture.md for completeness on integration points with frontend and usability concerns.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"architecture.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def parallel_implementation_phase(\n    goal: str = \"Independently implement backend and frontend components based on architecture documentation\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements Flask backend code app.py for data models, routes, version control, approvals, comments, and analytics. \"\n        \"FrontendDeveloper builds templates/*.html with specified element IDs, navigation, buttons, and page layouts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement a complete Flask backend application with routing, data handling, version control, approvals, comments, and analytics following the architecture documentation.\n\nTask Details:\n- Read architecture.md fully from CONTEXT; extract all Flask routes, data models, and logic for version control, approvals, comments, and analytics\n- Implement Flask app.py with all routes and their associated handlers, including data loading and saving based on specified text file schemas\n- Implement versioning logic for articles and article_versions, approval workflow, user comments, and analytics aggregation\n- Output is a single app.py file implementing full backend functionality\n- Do NOT implement frontend templates or UI layout; focus strictly on Flask backend logic and API\n\nImplementation Requirements:\n1. **Flask App Setup**:\n   # Initialize Flask app, configure secret keys, and prepare routes\n2. **Routes Implementation**:\n   # Implement all specified routes with correct HTTP methods and URL patterns\n   # Examples: /dashboard, /article/create, /article/<article_id>/edit, /article/<article_id>/versions, /articles/mine, /articles/published, /calendar, /article/<article_id>/analytics\n3. **Data Loading and Persistence**:\n   # Parse all data files from data/*.txt using exact pipe-delimited schemas and field orders from architecture.md\n   # Use robust file handling and error checking\n4. **Version Control Logic**:\n   # Manage article_versions with version numbers, saving new versions, retrieving version history\n5. **Approvals and Comments**:\n   # Track approvals from multiple approvers with statuses and comments\n   # Manage editorial comments linked to article versions\n6. **Analytics Data Handling**:\n   # Aggregate and present metrics such as views, unique visitors, average time on article, and shares\n7. **Root and Redirect Routes**:\n   # Implement root route '/' redirecting to '/dashboard'\n8. **Coding Best Practices**:\n   # Use Flask idioms, separate concerns, write clear and maintainable code\n   # Use request.form for POST data, render_template for responses\n   # Handle missing or invalid data gracefully\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Use execute_python_code tool for local testing as needed\n- Match all routes and data parsing exactly per architecture.md specification\n- Functions and variable names should be consistent and descriptive\n- Do NOT implement frontend templates or UI code in this file\n- Do NOT add features beyond specification in architecture.md\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"architecture.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to implement the complete set of HTML templates for the ContentPublishingHub application, strictly following the architecture documentation for element IDs, buttons, navigation, and page layouts.\n\nTask Details:\n- Read architecture.md fully from CONTEXT; extract page designs, element IDs, route URLs, and navigation specifications\n- Implement all HTML templates corresponding to each page (dashboard, create_article, edit_article, version_history, my_articles, published_articles, content_calendar, article_analytics)\n- Ensure all element IDs specified are present exactly as named\n- Incorporate navigation buttons and links matching the specified route paths\n- Output HTML templates saved under templates/ directory with specified filenames (e.g., dashboard.html, create_article.html, etc.)\n- Do NOT implement backend logic or Flask routes; focus fully on frontend templates, layout, and elements\n\nImplementation Requirements:\n1. **Template Structure**:\n   # Use standard HTML5 and Jinja2 syntax\n   # Include <title> and <h1> tags with descriptive page titles\n2. **Element IDs and Layout**:\n   # Implement all required element IDs exactly as specified, case-sensitive\n   # Maintain page container ids such as dashboard-page, create-article-page, etc.\n3. **Navigation**:\n   # Use Jinja2 url_for() with route function names for links and buttons\n   # Create navigation buttons to move between pages as specified (e.g., back to dashboard)\n4. **Forms and Inputs**:\n   # Include form elements for inputs and buttons with required IDs (e.g., article-title, article-content)\n   # Use method and action attributes correctly for POST/GET routes as needed\n5. **Dynamic Content**:\n   # Use Jinja2 templating for content lists, tables, and dynamic sections (e.g., list of articles, version comparisons)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files in templates/ folder\n- Do NOT implement any backend Python code or route handlers\n- Do NOT change or omit any specified element IDs or page layout details\n- Ensure buttons and links use exact route paths as defined\n- Save templates separately by page: dashboard.html, create_article.html, edit_article.html, etc.\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"architecture.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify that app.py implements all Flask routes, data models, versioning logic, approvals, comments, \"\n                \"and analytics per architecture.md specification. Validate root route redirects to dashboard.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"architecture.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Verify templates/*.html implement all element IDs, navigation, buttons, and page structure \"\n                \"as specified in architecture.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"architecture.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase4": "def testing_and_refinement_phase(\n    goal: str = \"Iteratively test and refine backend and frontend implementation until approval\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"TestingAgent executes test cases against app.py and templates/*.html starting from dashboard page. \"\n        \"Reports feedback and defects in feedback_testing.txt. \"\n        \"Developers fix issues and resubmit until TestingAgent writes [APPROVED] in feedback_testing.txt.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationImprover\",\n            \"prompt\": \"\"\"You are a Full-Stack Developer specializing in Flask web applications, experienced in both backend and frontend refinement.\n\nYour goal is to fix bugs and iteratively refine the Flask backend (app.py) and frontend templates (templates/*.html) based on tester feedback, until the system meets all quality standards.\n\nTask Details:\n- Read current app.py and templates/*.html from CONTEXT to understand existing implementation\n- Carefully review feedback_testing.txt for defect reports and suggested improvements\n- Update app.py and templates/*.html to fix all bugs and issues mentioned\n- Do NOT modify artifacts unrelated to reported issues\n- Prepare updated app.py and all modified templates/*.html for output\n\n**Backend Improvements:**\n- Ensure all Flask routes function correctly and match expected behavior for all pages starting from /dashboard\n- Address any data loading, routing, or rendering errors identified by TestingAgent\n- Confirm backend correctly handles article management, version control, scheduling, and analytics logic\n\n**Frontend Improvements:**\n- Correct HTML structure, element IDs, and navigation flow as specified\n- Fix display, interaction, or templating bugs in templates/*.html\n- Maintain exact ID names and page layouts consistent with specifications\n\n**Collaboration and Iteration:**\n- Incorporate feedback fully before resubmission\n- Use execute_python_code tool to test snippets locally if needed before saving\n- Repeat updates based on new feedback_testing.txt until final approval is achieved\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and all template files\n- Preserve exact filenames for all templates (templates/*.html)\n- Do NOT introduce new features or changes beyond feedback scope\n- Strictly follow feedback_testing.txt defect details\n- Output only updated app.py and templates/*.html files\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"feedback_testing.txt\", \"source\": \"TestingAgent\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"TestingAgent\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in end-to-end functional testing of Flask web applications.\n\nYour goal is to conduct comprehensive functional testing of the backend (app.py) and frontend templates (templates/*.html) starting at the /dashboard page, and write detailed testing feedback with approval status to feedback_testing.txt.\n\nTask Details:\n- Read current app.py and templates/*.html source code from CONTEXT\n- Execute functional tests covering all pages and routes starting from /dashboard\n- Validate correct rendering of page elements, navigation flows, and backend data interactions\n- Test content management features including create, edit, version history, approvals, scheduling, and analytics\n- Identify any functional defects, UI issues, or inconsistencies with specification\n- Write detailed defect reports and suggestions into feedback_testing.txt\n- Mark feedback_testing.txt with \"[APPROVED]\" ONLY if no defects remain; otherwise write \"NEED_MODIFY\"\n\n**Testing Scope:**\n- Start testing from /dashboard, verify presence of all required elements with correct IDs\n- Test all article workflows: creation, editing, versioning, approval, publishing, filtering\n- Test content calendar, user analytics, and backend data consistency\n- Verify links, buttons, dropdowns, and form submissions behave as expected\n- Confirm page titles and element IDs match specification exactly\n\n**Feedback File Format:**\n- List each defect with clear description and reproduction steps if applicable\n- Provide actionable suggestions aligned with specification\n- End file with one of the status markers: [APPROVED] or NEED_MODIFY\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to run backend tests or scripts as needed\n- Use write_text_file tool to output comprehensive feedback_testing.txt\n- Do NOT mark approval until all defects are verified fixed\n- Feedback must be clear and precise to guide ImplementationImprover\n\nOutput: feedback_testing.txt\"\"\",\n            \"tools\": [\"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback_testing.txt\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationImprover\",\n            \"reviewer_agent\": \"TestingAgent\",\n            \"review_criteria\": (\n                \"TestingAgent verifies fixes in app.py and templates/*.html effectively resolve reported defects.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"feedback_testing.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"TestingAgent\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Validate testing feedback and approval status accurately reflects system quality and readiness.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"feedback_testing.txt\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# ContentPublishingHub Web Application Specification

## Objective
Build a comprehensive content management system with version control, content scheduling, and analytics. The system supports collaborative content creation with version history tracking, editorial comments, and content analytics. Testing should start from the Dashboard page.

## Language
Python (Flask framework recommended)

## Page Design

### 1. Dashboard Page (`dashboard.html`)
**Route:** `/dashboard`
**Purpose:** Main landing page showing content overview and navigation
**Elements:**
- Page container (id: `dashboard-page`)
- Welcome message with username (id: `welcome-message`)
- Quick stats section (id: `quick-stats`)
- Create Article button (id: `create-article-button`)
- Recent activity feed (id: `recent-activity`)

### 2. Create Article Page (`create_article.html`)
**Route:** `/article/create`
**Purpose:** Editor for creating new articles
**Elements:**
- Page container (id: `create-article-page`)
- Article title input (id: `article-title`)
- Content editor textarea (id: `article-content`)
- Save as Draft button (id: `save-draft-button`)
- Cancel button (id: `cancel-button`)

### 3. Edit Article Page (`edit_article.html`)
**Route:** `/article/<article_id>/edit`
**Purpose:** Edit existing article with version tracking
**Elements:**
- Page container (id: `edit-article-page`)
- Article title input (id: `edit-article-title`)
- Content editor textarea (id: `edit-article-content`)
- Save New Version button (id: `save-version-button`)
- Cancel button (id: `cancel-edit`)

### 4. Article Version History Page (`version_history.html`)
**Route:** `/article/<article_id>/versions`
**Purpose:** View all versions and restore previous versions
**Elements:**
- Page container (id: `version-history-page`)
- Versions list (id: `versions-list`)
- Version comparison section (id: `version-comparison`)
- Restore button (id: `restore-version-1`)
- Back to Edit button (id: `back-to-edit-history`)

### 5. My Articles Page (`my_articles.html`)
**Route:** `/articles/mine`
**Purpose:** List user's articles with filters
**Elements:**
- Page container (id: `my-articles-page`)
- Filter by status dropdown (id: `filter-article-status`)
- Articles table (id: `articles-table`)
- Create New Article button (id: `create-new-article`)
- Back to Dashboard button (id: `back-to-dashboard`)

### 6. Published Articles Page (`published_articles.html`)
**Route:** `/articles/published`
**Purpose:** Public-facing content library
**Elements:**
- Page container (id: `published-articles-page`)
- Filter by category dropdown (id: `filter-published-category`)
- Articles grid (id: `published-articles-grid`)
- Sort by dropdown (id: `sort-published`)
- Back to Dashboard button (id: `back-to-dashboard-published`)

### 7. Content Calendar Page (`content_calendar.html`)
**Route:** `/calendar`
**Purpose:** Scheduled publications timeline view
**Elements:**
- Page container (id: `calendar-page`)
- Calendar view selector (id: `calendar-view`)
- Calendar grid (id: `calendar-grid`)
- Schedule button (id: `schedule-button`)
- Back to Dashboard button (id: `back-to-dashboard-calendar`)

### 8. Article Analytics Page (`article_analytics.html`)
**Route:** `/article/<article_id>/analytics`
**Purpose:** View engagement metrics for published article
**Elements:**
- Page container (id: `analytics-page`)
- Analytics overview (id: `analytics-overview`)
- Total views (id: `analytics-total-views`)
- Unique visitors (id: `analytics-unique-visitors`)
- Back to Article button (id: `back-to-article-analytics`)

## Data Storage

The 'ContentPublishingHub' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. users.txt
Format: `username|email|fullname|created_date`
Example:
```
john|john@example.com|John Doe|2024-01-15
alice|alice@example.com|Alice Smith|2024-01-16
bob|bob@example.com|Bob Johnson|2024-01-17
admin|admin@example.com|Admin User|2024-01-10
```

### 2. articles.txt
Format: `article_id|title|author|category|status|tags|featured_image|meta_description|created_date|publish_date`
Example:
```
1|Introduction to Flask|john|tutorial|published|python,flask,web|/img/flask.jpg|Learn Flask basics|2024-01-20|2024-01-22 10:00:00
2|Company Quarterly Update|alice|announcement|approved|company,news||Q1 results|2024-01-23|2024-01-25 09:00:00
3|New Product Launch|john|press_release|draft|product,launch|/img/product.jpg|Exciting new release|2024-01-24|
```
status: draft, pending_review, under_review, approved, published, rejected, archived
category: news, blog, tutorial, announcement, press_release

### 3. article_versions.txt
Format: `version_id|article_id|version_number|content|author|created_date|change_summary`
Example:
```
1|1|1|Flask is a micro web framework...|john|2024-01-20 14:30:00|Initial draft
2|1|2|Flask is a lightweight web framework...|john|2024-01-21 09:15:00|Improved introduction
3|2|1|We are pleased to announce...|alice|2024-01-23 11:00:00|Initial version
```

### 4. approvals.txt
Format: `approval_id|article_id|version_id|approver|status|comments|timestamp`
Example:
```
1|1|2|alice|approved|Looks good, well written|2024-01-21 10:30:00
2|1|2|bob|approved|Ready for publication|2024-01-21 15:00:00
3|3|1|alice|rejected|Needs more details in section 2|2024-01-24 14:00:00
```
status: approved, rejected, revision_requested

### 5. workflow_stages.txt
Format: `stage_id|category|stage_name|stage_order|is_required`
Example:
```
1|tutorial|Editor Review|1|yes
2|tutorial|Publisher Approval|2|yes
3|news|Editor Review|1|yes
4|announcement|Editor Review|1|yes
5|announcement|Publisher Approval|2|yes
```

### 6. comments.txt
Format: `comment_id|article_id|version_id|user|comment_text|timestamp`
Example:
```
1|1|1|alice|Great start! Consider adding more examples.|2024-01-20 16:00:00
2|1|2|bob|The flow is much better now.|2024-01-21 11:00:00
3|3|1|alice|Section 2 needs expansion - add metrics.|2024-01-24 13:45:00
```

### 7. analytics.txt
Format: `analytics_id|article_id|date|views|unique_visitors|avg_time_seconds|shares`
Example:
```
1|1|2024-01-22|150|120|245|12
2|1|2024-01-23|230|180|210|18
3|1|2024-01-24|180|140|220|15
4|2|2024-01-25|95|75|180|8
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
            """You are a Software Requirements Analyst specializing in comprehensive design specifications for Flask web applications.

Your goal is to analyze detailed user requirements to produce a thorough design specification document enabling separate backend and frontend development. The deliverable is design_spec.md containing complete Flask routes, HTML template structures with element IDs, and precise data schema definitions.

Task Details:
- Read the full user_task_description from CONTEXT
- Create design_spec.md describing all required Flask routes with methods, URL patterns, and context variables
- Specify HTML template structures for all pages, including exact element IDs as per requirements
- Detail data file schemas with exact field order, format, and example data from provided specifications
- Do NOT assume unprovided requirements or modify input/output artifact definitions

**Section 1: Flask Routes Specification**

- List all required routes (e.g., /dashboard, /article/create, /article/<article_id>/edit)
- Specify HTTP methods (GET, POST) for each route
- Define function names clearly and consistently (lowercase with underscores)
- Specify template names rendered per route
- Detail context variables passed to templates with their types and structures

**Section 2: HTML Template Structure**

- For each HTML template file (e.g., dashboard.html), specify:
  - Page container element with exact id
  - All required element IDs exactly as specified in the requirements
  - Button IDs, input fields, dropdowns, tables, grids as appropriate
- Define the expected page layout and navigation elements (buttons linking to routes)
- Ensure element IDs and names match the backend context variables where applicable

**Section 3: Data File Schemas**

- For each data file (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt):
  - Specify exact pipe-delimited field order
  - Describe each field’s meaning and data type
  - Provide example data rows as given
  - Clarify any enumerations or status codes used (e.g., article status values)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_spec.md
- design_spec.md must enable backend and frontend developers to implement their parts independently without ambiguity
- Follow exactly the input and output artifact definitions without additions or omissions
- Do NOT include implementation code or application logic, only design specification
- Ensure all elements and data schemas included match the user task and phase descriptions precisely

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in backend architecture design for Flask web applications.

Your goal is to develop a detailed architectural design document that guides both backend and frontend implementation teams.

Task Details:
- Read design_spec.md from CONTEXT to understand application requirements and page designs
- Create architecture.md detailing backend system design, Flask app modules, data flow, routing logic, and API endpoints
- Specify version control mechanisms and explain integration points with frontend templates
- Do NOT implement code or frontend templates; focus strictly on architecture documentation

**Section 1: Backend System Design**

- Describe Flask application structure with modules and packages
- Define responsibilities of each module (routing, data access, business logic, version control)
- Explain how data files (data/*.txt) will be accessed and managed
- Detail data flow between components and layers

**Section 2: Routing and API Endpoints**

- List all Flask routes derived from design_spec.md pages with method types (GET/POST)
- Map routes to controller functions and expected input/output
- Include patterns for dynamic routes (e.g., article_id parameters)
- Clarify handling of user sessions and authentication considerations if any

**Section 3: Version Control Design**

- Define architecture for article versioning and approval workflow
- Specify how version history, approvals, and comments relate to articles and versions
- Explain storage interaction with article_versions.txt, approvals.txt, comments.txt

**Section 4: Frontend Integration Points**

- Describe how backend passes data and context variables to frontend templates
- Specify endpoint responses to support frontend page rendering
- Highlight areas requiring close coordination with frontend design (e.g., data structures expected)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save architecture.md
- Follow input schema and artifact naming conventions precisely
- Do NOT include implementation code or frontend markup
- Ensure document enables independent backend/frontend implementation based on architecture.md alone

Output: architecture.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'architecture.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend application with routing, data handling, version control, approvals, comments, and analytics following the architecture documentation.

Task Details:
- Read architecture.md fully from CONTEXT; extract all Flask routes, data models, and logic for version control, approvals, comments, and analytics
- Implement Flask app.py with all routes and their associated handlers, including data loading and saving based on specified text file schemas
- Implement versioning logic for articles and article_versions, approval workflow, user comments, and analytics aggregation
- Output is a single app.py file implementing full backend functionality
- Do NOT implement frontend templates or UI layout; focus strictly on Flask backend logic and API

Implementation Requirements:
1. **Flask App Setup**:
   # Initialize Flask app, configure secret keys, and prepare routes
2. **Routes Implementation**:
   # Implement all specified routes with correct HTTP methods and URL patterns
   # Examples: /dashboard, /article/create, /article/<article_id>/edit, /article/<article_id>/versions, /articles/mine, /articles/published, /calendar, /article/<article_id>/analytics
3. **Data Loading and Persistence**:
   # Parse all data files from data/*.txt using exact pipe-delimited schemas and field orders from architecture.md
   # Use robust file handling and error checking
4. **Version Control Logic**:
   # Manage article_versions with version numbers, saving new versions, retrieving version history
5. **Approvals and Comments**:
   # Track approvals from multiple approvers with statuses and comments
   # Manage editorial comments linked to article versions
6. **Analytics Data Handling**:
   # Aggregate and present metrics such as views, unique visitors, average time on article, and shares
7. **Root and Redirect Routes**:
   # Implement root route '/' redirecting to '/dashboard'
8. **Coding Best Practices**:
   # Use Flask idioms, separate concerns, write clear and maintainable code
   # Use request.form for POST data, render_template for responses
   # Handle missing or invalid data gracefully

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Use execute_python_code tool for local testing as needed
- Match all routes and data parsing exactly per architecture.md specification
- Functions and variable names should be consistent and descriptive
- Do NOT implement frontend templates or UI code in this file
- Do NOT add features beyond specification in architecture.md

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'architecture.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to implement the complete set of HTML templates for the ContentPublishingHub application, strictly following the architecture documentation for element IDs, buttons, navigation, and page layouts.

Task Details:
- Read architecture.md fully from CONTEXT; extract page designs, element IDs, route URLs, and navigation specifications
- Implement all HTML templates corresponding to each page (dashboard, create_article, edit_article, version_history, my_articles, published_articles, content_calendar, article_analytics)
- Ensure all element IDs specified are present exactly as named
- Incorporate navigation buttons and links matching the specified route paths
- Output HTML templates saved under templates/ directory with specified filenames (e.g., dashboard.html, create_article.html, etc.)
- Do NOT implement backend logic or Flask routes; focus fully on frontend templates, layout, and elements

Implementation Requirements:
1. **Template Structure**:
   # Use standard HTML5 and Jinja2 syntax
   # Include <title> and <h1> tags with descriptive page titles
2. **Element IDs and Layout**:
   # Implement all required element IDs exactly as specified, case-sensitive
   # Maintain page container ids such as dashboard-page, create-article-page, etc.
3. **Navigation**:
   # Use Jinja2 url_for() with route function names for links and buttons
   # Create navigation buttons to move between pages as specified (e.g., back to dashboard)
4. **Forms and Inputs**:
   # Include form elements for inputs and buttons with required IDs (e.g., article-title, article-content)
   # Use method and action attributes correctly for POST/GET routes as needed
5. **Dynamic Content**:
   # Use Jinja2 templating for content lists, tables, and dynamic sections (e.g., list of articles, version comparisons)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files in templates/ folder
- Do NOT implement any backend Python code or route handlers
- Do NOT change or omit any specified element IDs or page layout details
- Ensure buttons and links use exact route paths as defined
- Save templates separately by page: dashboard.html, create_article.html, edit_article.html, etc.

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'architecture.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "ImplementationImprover": {
        "prompt": (
            """You are a Full-Stack Developer specializing in Flask web applications, experienced in both backend and frontend refinement.

Your goal is to fix bugs and iteratively refine the Flask backend (app.py) and frontend templates (templates/*.html) based on tester feedback, until the system meets all quality standards.

Task Details:
- Read current app.py and templates/*.html from CONTEXT to understand existing implementation
- Carefully review feedback_testing.txt for defect reports and suggested improvements
- Update app.py and templates/*.html to fix all bugs and issues mentioned
- Do NOT modify artifacts unrelated to reported issues
- Prepare updated app.py and all modified templates/*.html for output

**Backend Improvements:**
- Ensure all Flask routes function correctly and match expected behavior for all pages starting from /dashboard
- Address any data loading, routing, or rendering errors identified by TestingAgent
- Confirm backend correctly handles article management, version control, scheduling, and analytics logic

**Frontend Improvements:**
- Correct HTML structure, element IDs, and navigation flow as specified
- Fix display, interaction, or templating bugs in templates/*.html
- Maintain exact ID names and page layouts consistent with specifications

**Collaboration and Iteration:**
- Incorporate feedback fully before resubmission
- Use execute_python_code tool to test snippets locally if needed before saving
- Repeat updates based on new feedback_testing.txt until final approval is achieved

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all template files
- Preserve exact filenames for all templates (templates/*.html)
- Do NOT introduce new features or changes beyond feedback scope
- Strictly follow feedback_testing.txt defect details
- Output only updated app.py and templates/*.html files

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}, {'type': 'text_file', 'name': 'feedback_testing.txt', 'source': 'TestingAgent'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "TestingAgent": {
        "prompt": (
            """You are a Software Test Engineer specializing in end-to-end functional testing of Flask web applications.

Your goal is to conduct comprehensive functional testing of the backend (app.py) and frontend templates (templates/*.html) starting at the /dashboard page, and write detailed testing feedback with approval status to feedback_testing.txt.

Task Details:
- Read current app.py and templates/*.html source code from CONTEXT
- Execute functional tests covering all pages and routes starting from /dashboard
- Validate correct rendering of page elements, navigation flows, and backend data interactions
- Test content management features including create, edit, version history, approvals, scheduling, and analytics
- Identify any functional defects, UI issues, or inconsistencies with specification
- Write detailed defect reports and suggestions into feedback_testing.txt
- Mark feedback_testing.txt with "[APPROVED]" ONLY if no defects remain; otherwise write "NEED_MODIFY"

**Testing Scope:**
- Start testing from /dashboard, verify presence of all required elements with correct IDs
- Test all article workflows: creation, editing, versioning, approval, publishing, filtering
- Test content calendar, user analytics, and backend data consistency
- Verify links, buttons, dropdowns, and form submissions behave as expected
- Confirm page titles and element IDs match specification exactly

**Feedback File Format:**
- List each defect with clear description and reproduction steps if applicable
- Provide actionable suggestions aligned with specification
- End file with one of the status markers: [APPROVED] or NEED_MODIFY

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to run backend tests or scripts as needed
- Use write_text_file tool to output comprehensive feedback_testing.txt
- Do NOT mark approval until all defects are verified fixed
- Feedback must be clear and precise to guide ImplementationImprover

Output: feedback_testing.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'feedback_testing.txt'}],
    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("SystemArchitect", """Review design_spec.md for completeness of backend routes and data schema coverage "
                "including all CRUD operations, versioning, approvals, comments, analytics, and navigation routes.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDesigner", """Review design_spec.md for completeness and correctness of frontend templates "
                "including element IDs, page layout, buttons, navigational links, and user interactions.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'SystemArchitect': [
        ("RequirementsAnalyst", """Validate architecture.md aligns with design_spec.md requirements and covers all functional areas adequately.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'architecture.md'}]),
        ("FrontendDesigner", """Check architecture.md for completeness on integration points with frontend and usability concerns.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'architecture.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Verify that app.py implements all Flask routes, data models, versioning logic, approvals, comments, "
                "and analytics per architecture.md specification. Validate root route redirects to dashboard.""", [{'type': 'text_file', 'name': 'architecture.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Verify templates/*.html implement all element IDs, navigation, buttons, and page structure "
                "as specified in architecture.md.""", [{'type': 'text_file', 'name': 'architecture.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ImplementationImprover': [
        ("TestingAgent", """TestingAgent verifies fixes in app.py and templates/*.html effectively resolve reported defects.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'feedback_testing.txt'}])
    ],

    'TestingAgent': [
        ("SystemArchitect", """Validate testing feedback and approval status accurately reflects system quality and readiness.""", [{'type': 'text_file', 'name': 'feedback_testing.txt'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}




# ==================== Chaos Controller Setup ====================
chaos_controller = ChaosController(
    agent_chaos_enabled=False,
    stress_chaos_enabled=True,
    io_chaos_enabled=False,
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Start chaos experiment with 20% probability
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=0.2
)

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "stress_chaos",
    "probability": 0.2,
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

print(f"Chaos scenario 'stress_chaos' activated with 20% probability")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def requirements_analysis_phase():
    # Create RequirementsAnalyst agent
    RequirementsAnalyst = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute RequirementsAnalyst
    await execute(RequirementsAnalyst, "Analyze user requirements and create design_spec.md with Flask routes, HTML templates with element IDs, and data schema specifications")
# Phase1_End

# Phase2_Start

async def architecture_design_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=150,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute SystemArchitect
    await execute(SystemArchitect, "Generate architecture.md based on design_spec.md including backend design, routing, version control, and frontend integration points")
# Phase2_End

# Phase3_Start
import asyncio

async def parallel_implementation_phase():
    # Create BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=200,
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
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=160,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute the two agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement Flask backend app.py with routing, data models, version control, approvals, comments, and analytics per architecture.md"),
        execute(FrontendDeveloper, "Implement all HTML templates with specified element IDs, navigation, and layouts per architecture.md")
    )
# Phase3_End

# Phase4_Start

async def testing_and_refinement_phase():
    # Create agents
    ImplementationImprover = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationImprover",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    TestingAgent = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="TestingAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=180,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 4
    for iteration in range(MAX_LOOPS):
        # Execute TestingAgent to produce feedback_testing.txt
        await execute(TestingAgent, "Conduct comprehensive functional tests starting at /dashboard and write detailed feedback_testing.txt")

        # Read feedback_testing.txt and check for approval
        try:
            with open("feedback_testing.txt", "r") as f:
                feedback_content = f.read()
            if "[APPROVED]" in feedback_content:
                break
        except FileNotFoundError:
            # If missing feedback, continue to next iteration
            pass

        # Execute ImplementationImprover to fix defects reported in feedback_testing.txt
        await execute(ImplementationImprover, "Fix defects and issues reported in feedback_testing.txt and update app.py and templates/*.html accordingly")
# Phase4_End

# Orchestrate_Start

async def orchestrate():
    """Execute the complete multi-agent workflow in steps."""
    import time
    import json
    from pathlib import Path
    from essential_modules import aggregate_task_metrics
    orchestrate_start_time = time.time()

    step1 = [
        requirements_analysis_phase()
    ]
    step2 = [
        architecture_design_phase()
    ]
    step3 = [
        parallel_implementation_phase()
    ]
    step4 = [
        testing_and_refinement_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)
    await asyncio.gather(*step4)

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
