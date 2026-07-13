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
# 20260714_001749_343642/main_20260714_001749_343642.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Design the backend data model, Flask routes, and frontend HTML templates with element IDs and page navigation for the ContentPublishingHub application; produce backend_design.md, frontend_design.md, and design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDesignArchitect and FrontendDesignArchitect work independently to produce backend_design.md and frontend_design.md respectively based on the user task description; DesignMerger consolidates these into a single consistent design_spec.md document.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Python Flask backend web applications.\n\nYour goal is to design the complete backend architecture for the ContentPublishingHub application, producing a detailed backend_design.md artifact.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create backend_design.md outlining all Flask routes, data models, and business logic\n- Cover content management, version control, approval workflows, scheduling, and analytics as described\n- Do not rely on or read frontend_design.md or sibling outputs\n\n**Section 1: Flask Routes Design**\n- Specify each route path, HTTP methods, and route handler responsibilities\n- Define route names matching user task page requirements (e.g., /dashboard, /article/create)\n- Include parameterized routes with argument names (e.g., article_id)\n\n**Section 2: Data Models and File Schemas**\n- Define the exact data format for each text data file (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt)\n- Specify field names, data types, delimiters, order, and field descriptions\n- Provide example records for each schema using data from user task\n- Describe relationships linking models (e.g., article_id references, version tracking)\n\n**Section 3: Business Logic and Functional Requirements**\n- Detail logic for content version control, approval status handling, scheduling, and analytics calculations\n- Describe any backend state changes triggered by routes or data updates\n- Avoid assumptions beyond user task requirements\n\nCRITICAL SUCCESS CRITERIA:\n- Output backend_design.md can be directly implemented to produce the backend Flask app\n- All relevant specifications must stem solely from the user task description\n- Use write_text_file tool to save backend_design.md only\n\nOutput: backend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDesignArchitect\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in frontend web design using HTML and Flask template technologies.\n\nYour goal is to create detailed frontend_design.md specifying HTML templates for ContentPublishingHub pages with element IDs and navigation flows.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Independently create frontend_design.md describing all HTML templates, element IDs, and navigation controls\n- Cover all pages: dashboard, article creation/editing, version history, lists, calendar, and analytics as specified \n- Do not read or assume backend_design.md or sibling outputs\n\n**Section 1: Template and Page Specifications**\n- For each page, specify template filename and exact page-level container element IDs\n- List all important HTML element IDs with their purpose and element types (buttons, inputs, tables, etc.)\n- Include all form controls, buttons, filters, and navigation elements with identifiers\n\n**Section 2: Context Variables and Data Bindings**\n- Define context variables expected from backend for each template\n- Specify data structures and types for dynamic content rendering\n\n**Section 3: Navigation and Inter-Page Links**\n- Define navigation buttons and controls routing users between pages\n- Specify consistency of element IDs used for navigation flows\n\nCRITICAL SUCCESS CRITERIA:\n- frontend_design.md supports implementation of templates/*.html with correct element IDs and navigation\n- All specifications derive solely from the user task description\n- Use write_text_file tool to write frontend_design.md only\n\nOutput: frontend_design.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in synthesizing backend and frontend architecture designs for Flask web applications.\n\nYour goal is to merge backend_design.md and frontend_design.md into a single consistent design_spec.md that fully meets user requirements without adding features.\n\nTask Details:\n- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT\n- Combine backend and frontend specifications into one coherent document design_spec.md\n- Ensure consistency between route definitions, data models, and frontend context variables\n- Resolve any naming conflicts and unify navigation elements and page structures\n- Do not introduce new features or requirements beyond inputs\n\n**Section 1: Consolidated Flask Routes and Backend Design**\n- Preserve all routes, parameters, and business logic details from backend_design.md\n- Reconcile with frontend navigation flows and template context requirements\n\n**Section 2: Combined Frontend Templates Specification**\n- Preserve all template names, element IDs, and context variables from frontend_design.md\n- Ensure alignment with backend routes and data model definitions\n\n**Section 3: Data Models and Integration**\n- Unify data schema definitions with references from both backend and frontend\n- List all artifacts’ links and maintain data integrity constraints\n\nCRITICAL SUCCESS CRITERIA:\n- design_spec.md supports both backend implementation (app.py) and frontend templates/*.html implementation\n- No additional features outside user task description are added\n- Use write_text_file tool to save only design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\", \"source\": \"BackendDesignArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\", \"source\": \"FrontendDesignArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check backend_design.md for completeness and clarity in covering routes, data models, and business logic.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_design.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDesignArchitect\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Validate frontend_design.md to ensure all page templates, element IDs, and navigation are specified as per user requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_design.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Implement the backend Flask application and frontend templates from design_spec.md, and integrate them into a working ContentPublishingHub application; produce app.py and templates/*.html with fidelity to design\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = \"BackendDeveloper and FrontendDeveloper independently implement app.py and HTML templates respectively from design_spec.md; IntegrationMerger reconciles their outputs ensuring interface conformity and produces the final app.py and templates/*.html.\",\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask web applications.\n\nYour goal is to implement the backend Flask application including complete route handling, data management, version control, approvals, content scheduling, and analytics, as specified fully in design_spec.md.\n\nTask Details:\n- Read design_spec.md from CONTEXT, use it as the sole source of requirements\n- Independently implement all Flask routes, data file interactions, and business logic\n- Output a single app.py implementing the entire backend functionality\n- Do not read or rely on any sibling agent outputs\n\n**Implementation Requirements:**\n- Implement all routes accurately with correct HTTP methods and route parameters\n- Manage local text file storage for users, articles, versions, approvals, workflow stages, comments, and analytics data\n- Include handlers for version tracking, editorial comments, content scheduling, and analytics computations\n- Use the Flask framework with clear modular route functions and error handling\n\n**Data Management:**\n- Use specified text data formats and files under 'data' directory for persistence\n- Implement parsing, reading, writing, and updating of text files conforming exactly to the design_spec.md data schema\n- Ensure concurrency safety and data integrity in file operations\n\n**Code Formatting and Structure:**\n- Use Python 3 best practices and PEP8 style guidelines\n- Include necessary imports, app initialization, and run configuration\n- Add concise function-level comments using single-quote docstrings only\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to output app.py\n- Output app.py must be complete and runnable independently\n- Follow design_spec.md exactly without adding or omitting routes or data handling\n- Do not read or assume frontend implementation artifacts\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask applications.\n\nYour goal is to implement all frontend HTML templates as specified in design_spec.md with precise page structure, element IDs, navigation, and content placeholders.\n\nTask Details:\n- Read design_spec.md from CONTEXT only\n- Independently create all required templates with correct filenames in templates/*.html\n- Use exact element IDs and structure described in the page designs\n- Do not read or depend on backend implementation artifacts\n\n**Template Implementation Instructions:**\n- Implement each page’s HTML with Flask/Jinja2 templating syntax for dynamic content\n- Provide all specified IDs for page containers, inputs, buttons, tables, and navigation controls\n- Include proper links, forms, buttons, and sections as described for each page\n- Ensure consistent and semantic markup following web standards\n\n**Navigation and Page Structure:**\n- Implement navigation elements as described to enable workflow between pages\n- Include placeholders for dynamic variables matching backend context variables as implied by design_spec.md\n- Use reusable components or layout inheritance only if reflected in design_spec.md\n\n**Code Style:**\n- Use indentation and HTML5 semantic tags appropriately\n- Comment code with hash (#) style comments for sections as needed\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to output templates/*.html files\n- Templates must exactly match the element IDs and structures given in design_spec.md\n- Templates must be independently complete without backend assumptions\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in full-stack Flask web applications.\n\nYour goal is to combine and reconcile the backend app.py and frontend templates/*.html implementations into a consistent fully integrated ContentPublishingHub application ready for deployment.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify route definitions, context variables, and UI element IDs match across backend and frontend\n- Resolve any inconsistencies in routing paths, variable naming, and template rendering\n- Produce a reconciled final version of app.py and the complete templates/*.html set\n\n**Integration Validation:**\n- Ensure Flask routes in app.py correspond to templates rendered and UI elements specified\n- Verify that context data passed by backend matches template variables and element expectations\n- Check all navigation and form submission paths are consistent in both codebases\n- Remove duplication or mismatch errors, preserving design_spec.md requirements only\n\n**Output Artifacts:**\n- Write the consolidated, tested, and consistent backend code to app.py\n- Write the merged and verified frontend templates to templates/*.html\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to save final app.py and templates/*.html\n- No additional requirements or modifications outside design_spec.md permitted\n- Outputs must be deployable and fully synchronized backend-frontend codebases\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify app.py implementation conforms to design_spec.md including correct route handling and local file data management.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"IntegrationMerger\",\n            \"review_criteria\": \"Verify templates/*.html align with design_spec.md including presence of all required element IDs and page navigation structure.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "BackendDesignArchitect": {
        "prompt": (
            """You are a Software Architect specializing in Python Flask backend web applications.

Your goal is to design the complete backend architecture for the ContentPublishingHub application, producing a detailed backend_design.md artifact.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md outlining all Flask routes, data models, and business logic
- Cover content management, version control, approval workflows, scheduling, and analytics as described
- Do not rely on or read frontend_design.md or sibling outputs

**Section 1: Flask Routes Design**
- Specify each route path, HTTP methods, and route handler responsibilities
- Define route names matching user task page requirements (e.g., /dashboard, /article/create)
- Include parameterized routes with argument names (e.g., article_id)

**Section 2: Data Models and File Schemas**
- Define the exact data format for each text data file (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt)
- Specify field names, data types, delimiters, order, and field descriptions
- Provide example records for each schema using data from user task
- Describe relationships linking models (e.g., article_id references, version tracking)

**Section 3: Business Logic and Functional Requirements**
- Detail logic for content version control, approval status handling, scheduling, and analytics calculations
- Describe any backend state changes triggered by routes or data updates
- Avoid assumptions beyond user task requirements

CRITICAL SUCCESS CRITERIA:
- Output backend_design.md can be directly implemented to produce the backend Flask app
- All relevant specifications must stem solely from the user task description
- Use write_text_file tool to save backend_design.md only

Output: backend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_design.md'}],

    },

    "FrontendDesignArchitect": {
        "prompt": (
            """You are a Software Architect specializing in frontend web design using HTML and Flask template technologies.

Your goal is to create detailed frontend_design.md specifying HTML templates for ContentPublishingHub pages with element IDs and navigation flows.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md describing all HTML templates, element IDs, and navigation controls
- Cover all pages: dashboard, article creation/editing, version history, lists, calendar, and analytics as specified 
- Do not read or assume backend_design.md or sibling outputs

**Section 1: Template and Page Specifications**
- For each page, specify template filename and exact page-level container element IDs
- List all important HTML element IDs with their purpose and element types (buttons, inputs, tables, etc.)
- Include all form controls, buttons, filters, and navigation elements with identifiers

**Section 2: Context Variables and Data Bindings**
- Define context variables expected from backend for each template
- Specify data structures and types for dynamic content rendering

**Section 3: Navigation and Inter-Page Links**
- Define navigation buttons and controls routing users between pages
- Specify consistency of element IDs used for navigation flows

CRITICAL SUCCESS CRITERIA:
- frontend_design.md supports implementation of templates/*.html with correct element IDs and navigation
- All specifications derive solely from the user task description
- Use write_text_file tool to write frontend_design.md only

Output: frontend_design.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_design.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Software Architect specializing in synthesizing backend and frontend architecture designs for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into a single consistent design_spec.md that fully meets user requirements without adding features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Combine backend and frontend specifications into one coherent document design_spec.md
- Ensure consistency between route definitions, data models, and frontend context variables
- Resolve any naming conflicts and unify navigation elements and page structures
- Do not introduce new features or requirements beyond inputs

**Section 1: Consolidated Flask Routes and Backend Design**
- Preserve all routes, parameters, and business logic details from backend_design.md
- Reconcile with frontend navigation flows and template context requirements

**Section 2: Combined Frontend Templates Specification**
- Preserve all template names, element IDs, and context variables from frontend_design.md
- Ensure alignment with backend routes and data model definitions

**Section 3: Data Models and Integration**
- Unify data schema definitions with references from both backend and frontend
- List all artifacts’ links and maintain data integrity constraints

CRITICAL SUCCESS CRITERIA:
- design_spec.md supports both backend implementation (app.py) and frontend templates/*.html implementation
- No additional features outside user task description are added
- Use write_text_file tool to save only design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'backend_design.md', 'source': 'BackendDesignArchitect'}, {'type': 'text_file', 'name': 'frontend_design.md', 'source': 'FrontendDesignArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Python Flask web applications.

Your goal is to implement the backend Flask application including complete route handling, data management, version control, approvals, content scheduling, and analytics, as specified fully in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT, use it as the sole source of requirements
- Independently implement all Flask routes, data file interactions, and business logic
- Output a single app.py implementing the entire backend functionality
- Do not read or rely on any sibling agent outputs

**Implementation Requirements:**
- Implement all routes accurately with correct HTTP methods and route parameters
- Manage local text file storage for users, articles, versions, approvals, workflow stages, comments, and analytics data
- Include handlers for version tracking, editorial comments, content scheduling, and analytics computations
- Use the Flask framework with clear modular route functions and error handling

**Data Management:**
- Use specified text data formats and files under 'data' directory for persistence
- Implement parsing, reading, writing, and updating of text files conforming exactly to the design_spec.md data schema
- Ensure concurrency safety and data integrity in file operations

**Code Formatting and Structure:**
- Use Python 3 best practices and PEP8 style guidelines
- Include necessary imports, app initialization, and run configuration
- Add concise function-level comments using single-quote docstrings only

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output app.py
- Output app.py must be complete and runnable independently
- Follow design_spec.md exactly without adding or omitting routes or data handling
- Do not read or assume frontend implementation artifacts

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],

    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask applications.

Your goal is to implement all frontend HTML templates as specified in design_spec.md with precise page structure, element IDs, navigation, and content placeholders.

Task Details:
- Read design_spec.md from CONTEXT only
- Independently create all required templates with correct filenames in templates/*.html
- Use exact element IDs and structure described in the page designs
- Do not read or depend on backend implementation artifacts

**Template Implementation Instructions:**
- Implement each page’s HTML with Flask/Jinja2 templating syntax for dynamic content
- Provide all specified IDs for page containers, inputs, buttons, tables, and navigation controls
- Include proper links, forms, buttons, and sections as described for each page
- Ensure consistent and semantic markup following web standards

**Navigation and Page Structure:**
- Implement navigation elements as described to enable workflow between pages
- Include placeholders for dynamic variables matching backend context variables as implied by design_spec.md
- Use reusable components or layout inheritance only if reflected in design_spec.md

**Code Style:**
- Use indentation and HTML5 semantic tags appropriately
- Comment code with hash (#) style comments for sections as needed

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output templates/*.html files
- Templates must exactly match the element IDs and structures given in design_spec.md
- Templates must be independently complete without backend assumptions

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "IntegrationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in full-stack Flask web applications.

Your goal is to combine and reconcile the backend app.py and frontend templates/*.html implementations into a consistent fully integrated ContentPublishingHub application ready for deployment.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify route definitions, context variables, and UI element IDs match across backend and frontend
- Resolve any inconsistencies in routing paths, variable naming, and template rendering
- Produce a reconciled final version of app.py and the complete templates/*.html set

**Integration Validation:**
- Ensure Flask routes in app.py correspond to templates rendered and UI elements specified
- Verify that context data passed by backend matches template variables and element expectations
- Check all navigation and form submission paths are consistent in both codebases
- Remove duplication or mismatch errors, preserving design_spec.md requirements only

**Output Artifacts:**
- Write the consolidated, tested, and consistent backend code to app.py
- Write the merged and verified frontend templates to templates/*.html

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save final app.py and templates/*.html
- No additional requirements or modifications outside design_spec.md permitted
- Outputs must be deployable and fully synchronized backend-frontend codebases

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
        ("DesignMerger", """Check backend_design.md for completeness and clarity in covering routes, data models, and business logic.""", [{'type': 'text_file', 'name': 'backend_design.md'}])
    ],

    'FrontendDesignArchitect': [
        ("DesignMerger", """Validate frontend_design.md to ensure all page templates, element IDs, and navigation are specified as per user requirements.""", [{'type': 'text_file', 'name': 'frontend_design.md'}])
    ],

    'BackendDeveloper': [
        ("IntegrationMerger", """Verify app.py implementation conforms to design_spec.md including correct route handling and local file data management.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'FrontendDeveloper': [
        ("IntegrationMerger", """Verify templates/*.html align with design_spec.md including presence of all required element IDs and page navigation structure.""", [{'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
    BackendDesignArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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
        chaos_controller=chaos_controller,
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

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Design complete backend architecture and output backend_design.md"),
        execute(FrontendDesignArchitect, "Design complete frontend specification and output frontend_design.md")
    )

    # Read backend_design.md and frontend_design.md for merger
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

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into a consistent design_spec.md.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )
    IntegrationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=40
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper implementations
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement the complete backend app.py with all Flask routes, data management, version control, approvals, content scheduling, and analytics as specified in design_spec.md."
        ),
        execute(
            FrontendDeveloper,
            "Implement all frontend templates in templates/*.html with exact page structure, element IDs, navigation, and dynamic placeholders as specified in design_spec.md."
        )
    )

    # Read latest backend and frontend outputs for integration
    backend_code = ""
    frontend_templates_content = ""
    try:
        backend_code = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Run IntegrationMerger to reconcile backend and frontend outputs with design_spec.md
    await execute(
        IntegrationMerger,
        "Combine and reconcile backend app.py and frontend templates/*.html ensuring consistency with design_spec.md.\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== backend app.py ===\n{backend_code}\n\n"
        f"=== frontend templates ==={frontend_templates_content}"
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
