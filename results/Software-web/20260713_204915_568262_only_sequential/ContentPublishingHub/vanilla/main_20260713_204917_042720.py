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
# 20260713_204917_042720/main_20260713_204917_042720.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Analyze user requirements and produce a comprehensive design_spec.md detailing Flask routes, page elements, data formats, and application features.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"RequirementsAnalyst first creates requirements_analysis.md outlining all page routes, elements, and data storage needs; \"\n        \"then WebArchitect reads this and produces design_spec.md with detailed Flask route and page element specifications, data format contracts, and feature descriptions.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"RequirementsAnalyst\",\n            \"prompt\": \"\"\"You are a Requirements Analyst specializing in detailed web application requirement extraction.\n\nYour goal is to produce an exhaustive requirements_analysis.md document capturing all page routes, page names, UI element IDs, page purposes, and local data storage format specifications from the user task description.\n\nTask Details:\n- Read the full user_task_description input artifact\n- Extract all pages with their route paths, page names, and purposes\n- Enumerate all HTML element IDs per page as specified in the description\n- Document all local data storage files with formats, field orders, and sample data from user task\n- Preserve exact naming conventions and data formats without modifications or assumptions\n- Output requirements_analysis.md as a comprehensive, clear specification\n\nProcedure:\n1. Parse user_task_description systematically for each page and data file section\n2. Summarize each page route, purpose, and list all element IDs exactly\n3. For data storage, list each file name, exact pipe-delimited field order, field descriptions, and example data rows\n4. Structure requirements_analysis.md for readability and completeness emphasizing traceability to user input\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save requirements_analysis.md\n- Include no assumptions or additions beyond user task content\n- Maintain exact field orders and element ID names\n- Ensure end deliverable supports downstream design specification generation\n\nOutput: requirements_analysis.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"WebArchitect\",\n            \"prompt\": \"\"\"You are a Web Architect specialized in Flask web application design and specification drafting.\n\nYour goal is to convert the detailed requirements_analysis.md document into a precise design_spec.md that rigorously specifies Flask routes, their associated HTML template filenames, exact UI element IDs per page for frontend development and automated testing, detailed data storage file schemas, button behaviors, and overall application flow.\n\nTask Details:\n- Read user_task_description and requirements_analysis.md input artifacts\n- Specify all Flask routes including route paths and expected HTTP methods\n- Map each route to its HTML template filename matching the pages specified\n- Enumerate exact HTML element IDs per page as extracted for frontend use and testing\n- Specify all data storage text files with exact pipe-delimited field order and field definitions\n- Detail button functionalities and key application flow points based on requirements\n- Organize design_spec.md for clear reference by both backend and frontend teams\n- Maintain full consistency with all user requirements and requirements_analysis.md content\n\nSpecification Sections:\n1. Flask Routes Specification\n   - List route path, HTTP method(s), Flask function names, and associated template files\n2. HTML Template Details\n   - For each page specify HTML template file (e.g., dashboard.html)\n   - List all element IDs exactly, grouped by page section\n3. Data Storage Format Contracts\n   - For each data file, list file name, exact pipe-delimited field order, field descriptions, and examples\n4. Application Flow and Button Behavior\n   - Specify behaviors of critical buttons like Create, Save, Restore, Back, etc.\n   - Include navigation flow between pages where relevant\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_spec.md file\n- Ensure all naming matches requirements_analysis.md exactly\n- Provide complete and unambiguous specifications for backend and frontend implementation\n- Support automated UI testing through exhaustive element ID enumeration\n- Do not introduce features or changes not supported by user inputs or requirements_analysis.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\", \"source\": \"RequirementsAnalyst\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"RequirementsAnalyst\",\n            \"reviewer_agent\": \"WebArchitect\",\n            \"review_criteria\": (\n                \"Verify that requirements_analysis.md exhaustively enumerates all pages, routes, element IDs, data formats, and system features \"\n                \"matching user input without omissions or alterations.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"requirements_analysis.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"WebArchitect\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Validate design_spec.md for thorough Flask route coverage, exact external template filenames, correct and complete element IDs, \"\n                \"precise data storage formats, and conformity to user task requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Develop a Flask web application codebase including app.py and all required templates/*.html files strictly according to design_spec.md.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"DraftEngineer writes app_draft.py and all templates_draft/*.html files enforcing all routes, element IDs, page structures, and data handling as per design_spec.md; \"\n        \"then IntegrationEngineer refines and integrates the draft into final app.py and final templates/*.html files fully operational and matching design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DraftEngineer\",\n            \"prompt\": \"\"\"You are a Flask Developer specializing in rapid prototyping of backend and frontend code for content management systems.\n\nYour goal is to create a complete draft Flask application (app_draft.py) implementing all routes, data interactions, and UI elements specified in the design specification document. Concurrently, develop matching draft HTML templates in the templates_draft directory using exact element IDs and page layouts.\n\nTask Details:\n- Read user_task_description and design_spec.md thoroughly before implementation\n- Generate app_draft.py implementing ALL routes and data handling per design_spec.md\n- Create templates_draft/*.html files with exact element IDs, page structures, and content placeholders as specified\n- Use render_template with folder set to templates_draft for all routes\n- Respect data file formats and field orders when reading data in app_draft.py\n- Draft artifacts are separate from final production code and templates\n\nImplementation Guidelines:\n1. **Flask Routes and App Structure**\n   - Implement each route exactly as specified (paths, methods, variable parameters)\n   - Implement data loading from text files in 'data/' directory with correct parsing\n   - Use Python string splitting on pipe delimiter '|' matching field order exactly\n   - Handle all CRUD operations or interactions defined\n2. **Template Development**\n   - Produce templates with the exact element IDs listed (e.g., dashboard-page, create-article-button)\n   - Include placeholders for dynamic content using Jinja2 syntax\n   - Ensure navigation and buttons are present with correct IDs\n3. **Render Templates**\n   - In app_draft.py, set render_template calls to use templates from 'templates_draft'\n   - Pass correct context variables to templates as specified in design_spec.md\n4. **Error Handling**\n   - Include minimal handling for missing or empty data files\n   - Do not implement advanced features or polish; focus on completeness and structure\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files\n- All element IDs and page layouts must match design_spec.md exactly\n- Route paths and methods must exactly follow design_spec.md\n- Data loading must strictly follow specified file formats and field orders\n- Maintain draft code isolation: do NOT mix final templates or app.py paths\n- Code snippets or templates written only via write_text_file; no inline partial code outputs\n\nOutput: app_draft.py, templates_draft/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"IntegrationEngineer\",\n            \"prompt\": \"\"\"You are a Flask Developer specializing in final integration and production-grade web application development.\n\nYour goal is to integrate the draft Flask application (app_draft.py) and draft HTML templates (templates_draft/*.html) into a polished, fully functional final app.py and templates/*.html set. The final application must fully realize all features, routes, UI elements, and data interactions per design_spec.md and run properly without draft dependencies.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html for thorough understanding\n- Refactor and combine draft code to produce final app.py implementing all routes with render_template using templates/ folder\n- Convert all template references to the final templates directory (templates/*.html)\n- Ensure correctness of all route paths, variable handling, and HTTP methods as specified\n- Confirm all element IDs and page contents exactly match design_spec.md requirements\n- Optimize data file access and parsing consistency with design_spec.md formats\n- Ensure final app.py is runnable with Flask without errors and matches specification fully\n\nIntegration and Refinement Guidelines:\n1. **Finalize Routes and App.py**\n   - Remove draft prefixes or references (templates_draft)\n   - Conduct overall code cleanup, avoiding functionality loss\n2. **Finalize Templates**\n   - Move or recreate templates from templates_draft to templates directory\n   - Verify all pages have complete elements and IDs as specified\n   - Confirm correct Jinja2 syntax and placeholders for dynamic data\n3. **Testing and Validation**\n   - Confirm Flask app runs and serves all routes defined in design_spec.md\n   - Validate all UI elements present with correct IDs and structures\n   - Validate data loading and display correctness per data file definitions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and all templates/*.html files\n- All routes, element IDs, page structures, and data handling must strictly follow design_spec.md\n- No draft folders or draft references remain in output\n- Final app.py must be runnable by Flask with no errors\n- Output only final versions via write_text_file\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\", \"source\": \"DraftEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\", \"source\": \"DraftEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DraftEngineer\",\n            \"reviewer_agent\": \"IntegrationEngineer\",\n            \"review_criteria\": \"Check app_draft.py and templates_draft/*.html fully implement all design_spec.md requirements and page elements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app_draft.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_draft/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"IntegrationEngineer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": \"Verify that final app.py and templates/*.html fully realize design_spec.md, are runnable, and expose all specified routes and elements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Comprehensively validate the final Flask app.py and templates/*.html for functional correctness, exact route availability, element presence, and runtime stability; fix issues and produce a validated final version.\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"WebValidator tests app.py and templates/*.html producing validation_report.md with findings; \"\n        \"SequentialFixer then applies these findings to finalize app.py and templates/*.html resolving all reported issues.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"WebValidator\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in testing Flask web applications.\n\nYour goal is to comprehensively validate the Flask backend and frontend templates to ensure functional correctness, exact route presence, UI element presence, and runtime stability, producing a detailed validation report.\n\nTask Details:\n- Read user_task_description and design_spec.md for requirements and expected routes/pages\n- Read current app.py and templates/*.html implementations to test\n- Produce validation_report.md documenting detected defects and successful tests related to routes, Flask syntax, and UI components\n\nValidation Requirements:\n1. **Backend Validation**:\n   - Perform syntax and import checks on app.py using validate_python_file tool\n   - Attempt to start Flask server and perform runtime validation\n   - Verify all routes from design_spec.md exist and respond properly, including /dashboard and all specified dynamic routes\n   - Confirm correct HTTP methods and route parameters\n\n2. **Frontend Validation**:\n   - Check templates/*.html for presence of all required element IDs exactly as specified (e.g., dashboard-page, create-article-button)\n   - Verify buttons, inputs, dropdowns, and other UI components exist and are correctly named\n   - Validate connectivity between routes and templates\n\n3. **Reporting**:\n   - Record all validation findings in validation_report.md with clear descriptions, exact location of issues, and severity\n   - Include pass/fail status for each route and UI element checked\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for backend testing\n- Use write_text_file tool to save validation_report.md\n- Provide clear, reproducible issue reports for SequentialFixer\n- Focus on the exact route list and element IDs from design_spec.md and user task description\n\nOutput: validation_report.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"SequentialFixer\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in iterative refinement and bug fixing of Flask web applications.\n\nYour goal is to apply all actionable corrections from validation_report.md to the Flask backend (app.py) and frontend templates (*.html) to produce fully conformant and validated final deliverables.\n\nTask Details:\n- Read user_task_description and design_spec.md for understanding original requirements\n- Read current app.py and templates/*.html for existing implementation status\n- Carefully analyze validation_report.md for detailed issues to address\n- Update app.py and templates/*.html strictly following design_spec.md and user task specifications\n- Focus on fixing route presence, HTTP methods, element IDs, UI components, and runtime issues until all reported problems are resolved\n\nFixing Guidelines:\n1. **Backend Corrections**:\n   - Address syntax errors, runtime crashes, and missing routes as reported\n   - Ensure all routes defined in design_spec.md exist with correct function names and methods\n   - Verify data loading and processing matches specifications\n\n2. **Frontend Corrections**:\n   - Add or correct missing element IDs, buttons, inputs, and other UI elements exactly as specified\n   - Maintain naming consistency and template structure per design_spec.md\n   - Fix navigation links, forms, and dynamic content rendering where applicable\n\n3. **Validation Compliance**:\n   - Cross-check all fixes adhere strictly to design_spec.md and user requirements\n   - Prepare updated app.py and templates/*.html for subsequent validation round or final delivery\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and all templates\n- Maintain strict conformity with design_spec.md element IDs and route specifications\n- Resolve all issues reported in validation_report.md thoroughly\n- Deliver production-ready final code without extraneous changes\n- Do not omit fixing any reported critical or major defects\n\nOutputs: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"WebArchitect\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"IntegrationEngineer\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\", \"source\": \"WebValidator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"WebValidator\",\n            \"reviewer_agent\": \"SequentialFixer\",\n            \"review_criteria\": (\n                \"Check validation_report.md correctly identifies missing elements, route issues, and runtime errors with clear, reproducible instructions.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SequentialFixer\",\n            \"reviewer_agent\": \"RequirementsAnalyst\",\n            \"review_criteria\": (\n                \"Verify the final app.py and templates/*.html incorporate all fixes and fully conform to the original user task and design_spec.md.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_report.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
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
            """You are a Requirements Analyst specializing in detailed web application requirement extraction.

Your goal is to produce an exhaustive requirements_analysis.md document capturing all page routes, page names, UI element IDs, page purposes, and local data storage format specifications from the user task description.

Task Details:
- Read the full user_task_description input artifact
- Extract all pages with their route paths, page names, and purposes
- Enumerate all HTML element IDs per page as specified in the description
- Document all local data storage files with formats, field orders, and sample data from user task
- Preserve exact naming conventions and data formats without modifications or assumptions
- Output requirements_analysis.md as a comprehensive, clear specification

Procedure:
1. Parse user_task_description systematically for each page and data file section
2. Summarize each page route, purpose, and list all element IDs exactly
3. For data storage, list each file name, exact pipe-delimited field order, field descriptions, and example data rows
4. Structure requirements_analysis.md for readability and completeness emphasizing traceability to user input

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save requirements_analysis.md
- Include no assumptions or additions beyond user task content
- Maintain exact field orders and element ID names
- Ensure end deliverable supports downstream design specification generation

Output: requirements_analysis.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'requirements_analysis.md'}],

    },

    "WebArchitect": {
        "prompt": (
            """You are a Web Architect specialized in Flask web application design and specification drafting.

Your goal is to convert the detailed requirements_analysis.md document into a precise design_spec.md that rigorously specifies Flask routes, their associated HTML template filenames, exact UI element IDs per page for frontend development and automated testing, detailed data storage file schemas, button behaviors, and overall application flow.

Task Details:
- Read user_task_description and requirements_analysis.md input artifacts
- Specify all Flask routes including route paths and expected HTTP methods
- Map each route to its HTML template filename matching the pages specified
- Enumerate exact HTML element IDs per page as extracted for frontend use and testing
- Specify all data storage text files with exact pipe-delimited field order and field definitions
- Detail button functionalities and key application flow points based on requirements
- Organize design_spec.md for clear reference by both backend and frontend teams
- Maintain full consistency with all user requirements and requirements_analysis.md content

Specification Sections:
1. Flask Routes Specification
   - List route path, HTTP method(s), Flask function names, and associated template files
2. HTML Template Details
   - For each page specify HTML template file (e.g., dashboard.html)
   - List all element IDs exactly, grouped by page section
3. Data Storage Format Contracts
   - For each data file, list file name, exact pipe-delimited field order, field descriptions, and examples
4. Application Flow and Button Behavior
   - Specify behaviors of critical buttons like Create, Save, Restore, Back, etc.
   - Include navigation flow between pages where relevant

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_spec.md file
- Ensure all naming matches requirements_analysis.md exactly
- Provide complete and unambiguous specifications for backend and frontend implementation
- Support automated UI testing through exhaustive element ID enumeration
- Do not introduce features or changes not supported by user inputs or requirements_analysis.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'requirements_analysis.md', 'source': 'RequirementsAnalyst'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DraftEngineer": {
        "prompt": (
            """You are a Flask Developer specializing in rapid prototyping of backend and frontend code for content management systems.

Your goal is to create a complete draft Flask application (app_draft.py) implementing all routes, data interactions, and UI elements specified in the design specification document. Concurrently, develop matching draft HTML templates in the templates_draft directory using exact element IDs and page layouts.

Task Details:
- Read user_task_description and design_spec.md thoroughly before implementation
- Generate app_draft.py implementing ALL routes and data handling per design_spec.md
- Create templates_draft/*.html files with exact element IDs, page structures, and content placeholders as specified
- Use render_template with folder set to templates_draft for all routes
- Respect data file formats and field orders when reading data in app_draft.py
- Draft artifacts are separate from final production code and templates

Implementation Guidelines:
1. **Flask Routes and App Structure**
   - Implement each route exactly as specified (paths, methods, variable parameters)
   - Implement data loading from text files in 'data/' directory with correct parsing
   - Use Python string splitting on pipe delimiter '|' matching field order exactly
   - Handle all CRUD operations or interactions defined
2. **Template Development**
   - Produce templates with the exact element IDs listed (e.g., dashboard-page, create-article-button)
   - Include placeholders for dynamic content using Jinja2 syntax
   - Ensure navigation and buttons are present with correct IDs
3. **Render Templates**
   - In app_draft.py, set render_template calls to use templates from 'templates_draft'
   - Pass correct context variables to templates as specified in design_spec.md
4. **Error Handling**
   - Include minimal handling for missing or empty data files
   - Do not implement advanced features or polish; focus on completeness and structure

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- All element IDs and page layouts must match design_spec.md exactly
- Route paths and methods must exactly follow design_spec.md
- Data loading must strictly follow specified file formats and field orders
- Maintain draft code isolation: do NOT mix final templates or app.py paths
- Code snippets or templates written only via write_text_file; no inline partial code outputs

Output: app_draft.py, templates_draft/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}],

    },

    "IntegrationEngineer": {
        "prompt": (
            """You are a Flask Developer specializing in final integration and production-grade web application development.

Your goal is to integrate the draft Flask application (app_draft.py) and draft HTML templates (templates_draft/*.html) into a polished, fully functional final app.py and templates/*.html set. The final application must fully realize all features, routes, UI elements, and data interactions per design_spec.md and run properly without draft dependencies.

Task Details:
- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html for thorough understanding
- Refactor and combine draft code to produce final app.py implementing all routes with render_template using templates/ folder
- Convert all template references to the final templates directory (templates/*.html)
- Ensure correctness of all route paths, variable handling, and HTTP methods as specified
- Confirm all element IDs and page contents exactly match design_spec.md requirements
- Optimize data file access and parsing consistency with design_spec.md formats
- Ensure final app.py is runnable with Flask without errors and matches specification fully

Integration and Refinement Guidelines:
1. **Finalize Routes and App.py**
   - Remove draft prefixes or references (templates_draft)
   - Conduct overall code cleanup, avoiding functionality loss
2. **Finalize Templates**
   - Move or recreate templates from templates_draft to templates directory
   - Verify all pages have complete elements and IDs as specified
   - Confirm correct Jinja2 syntax and placeholders for dynamic data
3. **Testing and Validation**
   - Confirm Flask app runs and serves all routes defined in design_spec.md
   - Validate all UI elements present with correct IDs and structures
   - Validate data loading and display correctness per data file definitions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and all templates/*.html files
- All routes, element IDs, page structures, and data handling must strictly follow design_spec.md
- No draft folders or draft references remain in output
- Final app.py must be runnable by Flask with no errors
- Output only final versions via write_text_file

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app_draft.py', 'source': 'DraftEngineer'}, {'type': 'text_file', 'name': 'templates_draft/*.html', 'source': 'DraftEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "WebValidator": {
        "prompt": (
            """You are a Software Test Engineer specializing in testing Flask web applications.

Your goal is to comprehensively validate the Flask backend and frontend templates to ensure functional correctness, exact route presence, UI element presence, and runtime stability, producing a detailed validation report.

Task Details:
- Read user_task_description and design_spec.md for requirements and expected routes/pages
- Read current app.py and templates/*.html implementations to test
- Produce validation_report.md documenting detected defects and successful tests related to routes, Flask syntax, and UI components

Validation Requirements:
1. **Backend Validation**:
   - Perform syntax and import checks on app.py using validate_python_file tool
   - Attempt to start Flask server and perform runtime validation
   - Verify all routes from design_spec.md exist and respond properly, including /dashboard and all specified dynamic routes
   - Confirm correct HTTP methods and route parameters

2. **Frontend Validation**:
   - Check templates/*.html for presence of all required element IDs exactly as specified (e.g., dashboard-page, create-article-button)
   - Verify buttons, inputs, dropdowns, and other UI components exist and are correctly named
   - Validate connectivity between routes and templates

3. **Reporting**:
   - Record all validation findings in validation_report.md with clear descriptions, exact location of issues, and severity
   - Include pass/fail status for each route and UI element checked

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for backend testing
- Use write_text_file tool to save validation_report.md
- Provide clear, reproducible issue reports for SequentialFixer
- Focus on the exact route list and element IDs from design_spec.md and user task description

Output: validation_report.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_report.md'}],

    },

    "SequentialFixer": {
        "prompt": (
            """You are a Software Developer specializing in iterative refinement and bug fixing of Flask web applications.

Your goal is to apply all actionable corrections from validation_report.md to the Flask backend (app.py) and frontend templates (*.html) to produce fully conformant and validated final deliverables.

Task Details:
- Read user_task_description and design_spec.md for understanding original requirements
- Read current app.py and templates/*.html for existing implementation status
- Carefully analyze validation_report.md for detailed issues to address
- Update app.py and templates/*.html strictly following design_spec.md and user task specifications
- Focus on fixing route presence, HTTP methods, element IDs, UI components, and runtime issues until all reported problems are resolved

Fixing Guidelines:
1. **Backend Corrections**:
   - Address syntax errors, runtime crashes, and missing routes as reported
   - Ensure all routes defined in design_spec.md exist with correct function names and methods
   - Verify data loading and processing matches specifications

2. **Frontend Corrections**:
   - Add or correct missing element IDs, buttons, inputs, and other UI elements exactly as specified
   - Maintain naming consistency and template structure per design_spec.md
   - Fix navigation links, forms, and dynamic content rendering where applicable

3. **Validation Compliance**:
   - Cross-check all fixes adhere strictly to design_spec.md and user requirements
   - Prepare updated app.py and templates/*.html for subsequent validation round or final delivery

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all templates
- Maintain strict conformity with design_spec.md element IDs and route specifications
- Resolve all issues reported in validation_report.md thoroughly
- Deliver production-ready final code without extraneous changes
- Do not omit fixing any reported critical or major defects

Outputs: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'WebArchitect'}, {'type': 'text_file', 'name': 'app.py', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'IntegrationEngineer'}, {'type': 'text_file', 'name': 'validation_report.md', 'source': 'WebValidator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'RequirementsAnalyst': [
        ("WebArchitect", """Verify that requirements_analysis.md exhaustively enumerates all pages, routes, element IDs, data formats, and system features "
                "matching user input without omissions or alterations.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'requirements_analysis.md'}])
    ],

    'WebArchitect': [
        ("RequirementsAnalyst", """Validate design_spec.md for thorough Flask route coverage, exact external template filenames, correct and complete element IDs, "
                "precise data storage formats, and conformity to user task requirements.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'DraftEngineer': [
        ("IntegrationEngineer", """Check app_draft.py and templates_draft/*.html fully implement all design_spec.md requirements and page elements.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app_draft.py'}, {'type': 'text_file', 'name': 'templates_draft/*.html'}])
    ],

    'IntegrationEngineer': [
        ("RequirementsAnalyst", """Verify that final app.py and templates/*.html fully realize design_spec.md, are runnable, and expose all specified routes and elements.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'WebValidator': [
        ("SequentialFixer", """Check validation_report.md correctly identifies missing elements, route issues, and runtime errors with clear, reproducible instructions.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_report.md'}])
    ],

    'SequentialFixer': [
        ("RequirementsAnalyst", """Verify the final app.py and templates/*.html incorporate all fixes and fully conform to the original user task and design_spec.md.""", [{'type': 'text_file', 'name': 'validation_report.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Create agents
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=30
    )

    # Sequential execution
    await execute(RequirementsAnalyst,
                  "Read user_task_description and produce requirements_analysis.md capturing all page routes, element IDs, page purposes, and local data storage formats without assumptions.")

    # Read requirements_analysis.md for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md. Convert the requirements_analysis.md content into design_spec.md specifying Flask routes, HTML templates with exact element IDs, data storage file schema, button behaviors, and application flow. Maintain full consistency and naming exactness.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Create agents
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: DraftEngineer first, then IntegrationEngineer
    await execute(DraftEngineer,
                  "Create complete app_draft.py implementing all routes and data handling per design_spec.md. "
                  "Create all templates_draft/*.html with exact element IDs, page layouts, and placeholders. Use render_template with templates_draft folder.")

    # Read draft files content to inject for IntegrationEngineer
    app_draft_code = ""
    templates_draft_content = ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    # Attempt to read all templates_draft/*.html files - simplistic approach: read at least one or multiple files if needed
    # For orchestration, we provide only aggregated content string representing templates draft.
    # This can be improved with explicit names if known.
    import glob
    templates_files = []
    try:
        templates_files = glob.glob("templates_draft/*.html")
    except:
        templates_files = []

    templates_content_accum = ""
    for t_file in templates_files:
        try:
            t_content = open(t_file).read()
            templates_content_accum += f"=== {t_file} ===\n{t_content}\n\n"
        except:
            continue
    templates_draft_content = templates_content_accum

    await execute(IntegrationEngineer,
                  f"Integrate draft into final app.py and templates/*.html per design_spec.md. "
                  f"Refactor routes to use templates folder, verify all element IDs and page structures strictly follow design_spec.md. "
                  f"Ensure final app.py is runnable without draft references.\n\n"
                  f"=== app_draft.py content ===\n{app_draft_code}\n\n"
                  f"=== templates_draft content ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=420,
        failure_threshold=1,
        recovery_time=40
    )

    # Run WebValidator to produce validation_report.md
    await execute(WebValidator,
                  "Validate backend app.py using validate_python_file and execute_python_code tools. "
                  "Check all routes from design_spec.md including /dashboard and dynamic routes, HTTP methods, and runtime stability. "
                  "Validate frontend templates/*.html for presence of all required element IDs and UI components as specified in design_spec.md and user task description. "
                  "Produce detailed validation_report.md with pass/fail for routes and UI elements.")

    # Read validation_report.md content for injection
    validation_report = ""
    try:
        validation_report = open("validation_report.md", "r").read()
    except Exception:
        validation_report = ""

    # Run SequentialFixer to fix all issues based on validation_report.md
    await execute(SequentialFixer,
                  "Apply all fixes to app.py and templates/*.html based on the following validation_report.md. "
                  "Ensure full conformance with design_spec.md and user task requirements, resolving all reported functional, route, and UI element issues.\n"
                  f"=== validation_report.md ===\n{validation_report}")
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
