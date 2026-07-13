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
# 20260714_001749_668685/main_20260714_001749_668685.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Refine the complete ContentPublishingHub Flask web application design, including all pages, routes, element IDs, and user interaction flows; deliver design_spec.md with detailed UI and data contract specifications.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"DesignGenerator drafts design_spec.md describing pages, routes, UI element IDs, data storage formats, and navigation based on user requirements; DesignCritic reviews design_spec.md against user task requirements and writes design_feedback.md with required modifications or approval.\",\n    team: list = [\n        {\n            \"agent_name\": \"DesignGenerator\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications for content management systems.\n\nYour goal is to produce a thorough design_spec.md detailing all application pages, Flask route paths, precise UI element IDs, data file formats, and user interaction flows. You will create or revise this specification from the user task description and reviewer feedback for at most two refinement iterations.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Read current design_spec.md draft and design_feedback.md when available\n- On initial iteration, write a complete design_spec.md covering all pages, routes, UI elements, data schemas, and interactions\n- Upon NEED_MODIFY feedback, incorporate every required correction and rewrite design_spec.md fully\n- Upon [APPROVED], maintain the approved design\n\n**Section 1: Page and Route Specifications**\n- Define Flask route paths exactly as specified for all pages (e.g., dashboard, article creation, editing, version history, analytics)\n- Specify the page template file names and their corresponding route URLs\n- List each page's main container IDs and all required element IDs exactly\n\n**Section 2: UI Element and Interaction Details**\n- Describe each UI element’s ID and role on the page, e.g., buttons, inputs, lists\n- Include user interaction flows such as navigation and version control workflows\n- Ensure the Dashboard page is emphasized as the testing start point\n\n**Section 3: Data Storage Formats**\n- Specify exact format, field order, and example rows for each required data text file (users.txt, articles.txt, article_versions.txt, etc.)\n- Clarify field types, expected values, and relationships between files (e.g., article_id linking)\n\nCRITICAL SUCCESS CRITERIA:\n- Limit iterations to two refinements at most\n- Incorporate all NEED_MODIFY feedback fully without adding extra requirements\n- Use write_text_file tool to output design_spec.md\n- Output file must be named design_spec.md\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\", \"source\": \"DesignCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignCritic\",\n            \"prompt\": \"\"\"You are a Design Reviewer specializing in Flask web application design specifications for content management systems.\n\nYour goal is to critically review design_spec.md against the user_task_description, ensuring completeness, correctness, and strict conformance with UI element IDs, routing, data formats, and testing start requirements. Provide gated feedback with either approval or detailed modifications for at most two iterations.\n\nTask Details:\n- Read user_task_description and current design_spec.md from CONTEXT\n- Focus review on completeness of page routes, exact UI element IDs, precise data storage format compliance, version control workflows, analytics specification, and testing start from Dashboard\n- Write design_feedback.md starting exactly with either '[APPROVED]' if acceptable or 'NEED_MODIFY' followed by concrete and explicit correction points\n- Confirm no additions beyond user task requirements; feedback must be clear and actionable\n\nReview Requirements:\n1. Verify all specified routes match user task page design and URL paths exactly.\n2. Confirm all UI element IDs are present and match the given naming conventions precisely.\n3. Validate data file format specifications (field order, allowed values, and example rows) against the user task description.\n4. Ensure version control and editorial workflow elements are correctly described.\n5. Confirm the testing start point is set to the Dashboard page as requested.\n\nCRITICAL REQUIREMENTS:\n- design_feedback.md must start with the byte-1 marker exactly '[APPROVED]' or 'NEED_MODIFY'\n- No extraneous headers, whitespace, or prefixes before the marker\n- Use write_text_file tool to save the complete feedback\n- Limit review iterations to two refinements at most\n\nOutput: design_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\"], \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignGenerator\",\n            \"reviewer_agent\": \"DesignCritic\",\n            \"review_criteria\": \"Check that design_spec.md meets all page design requirements including routes, exact element IDs, data storage formats, version control workflows, analytics presentation, and testing start point; require precise and unambiguous specifications; feedback must prompt either approval or detailed modification requests.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_feedback.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_and_verification_phase(\n    goal: str = \"Develop the canonical Flask application files app.py and templates/*.html implementing the ContentPublishingHub specification with all routes, UI elements, data handling, version control, and analytics; iterate based on code feedback until at most two iterations.\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = \"AppGenerator writes or revises app.py and all template HTML files based on the finalized design_spec.md and code_feedback.md; CodeCritic evaluates code correctness, adherence to design_spec.md, routing accuracy, element ID correctness, and basic runtime validation, then writes code_feedback.md with '[APPROVED]' or 'NEED_MODIFY'.\",\n    team: list = [\n        {\n            \"agent_name\": \"AppGenerator\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web application development.\n\nYour goal is to implement or revise the complete Flask backend and frontend template files from design specifications and code review feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT\n- On first iteration or when feedback begins NEED_MODIFY, rewrite entire app.py and all templates/*.html complying fully with design_spec.md\n- On feedback [APPROVED], maintain the approved source unchanged\n- Output updated app.py and templates/*.html files reflecting all routes, UI element IDs, data storage, version control, scheduling, and analytics\n\n**Section 1: Flask Application Implementation**\n- Implement all Flask routes exactly as specified, including dynamic routes with parameters\n- Handle local text file data storage for all required data files (e.g., users.txt, articles.txt, versions, approvals)\n- Implement version control features with article versioning and restoration\n- Integrate content scheduling and analytics data retrieval and display\n\n**Section 2: Template Files Implementation**\n- Create or revise templates/*.html files matching routes and specified element IDs exactly\n- Ensure pages contain all required UI elements with correct IDs as listed in design_spec.md\n- Templates must support dynamic content rendering passed from Flask views\n\n**Section 3: Compliance and Code Quality**\n- Ensure code complies with design_spec.md requirements without omission or unauthorized additions\n- Follow Python best practices while ensuring clear, maintainable Flask code\n- Synchronize data keys and references exactly with design_spec.md\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save outputs: app.py and templates/*.html files\n- Rewrite complete app.py and all templates/*.html on NEED_MODIFY feedback\n- Stop after two iterations or upon [APPROVED] feedback in code_feedback.md\n- Strictly follow element IDs, route patterns, and data file formats from design_spec.md\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\", \"source\": \"CodeCritic\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"CodeCritic\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application code reviews and validation.\n\nYour goal is to review the Flask backend and frontend template code for correctness, conformance to design specifications, and quality, providing gated feedback for at most two iterations.\n\nTask Details:\n- Read design_spec.md, app.py, and templates/*.html from CONTEXT\n- Verify all Flask routes, including dynamic routes, match design_spec.md\n- Check each template page for exact UI element presence and correct IDs as specified\n- Confirm local text file interactions match specified data files and formats\n- Perform basic runtime validation and code quality assessment of app.py\n- Begin code_feedback.md with [APPROVED] if all checks pass or NEED_MODIFY followed by concrete required changes if issues exist\n\nReview Requirements:\n1. Route Compliance: Validate all endpoints, parameters, and HTTP methods exactly per design_spec.md.\n2. UI Elements: Confirm presence and correctness of all HTML element IDs and structural UI components on each route’s template.\n3. Data Handling: Verify reading/writing to text files aligned with data formats (users.txt, articles.txt, versions, approvals, workflow_stages, comments, analytics).\n4. Version Control & Scheduling: Ensure article versioning, restoring functionality, and content scheduling are implemented as per spec.\n5. Analytics Display: Check that engagement metrics and analytics data are displayed correctly.\n6. Code Quality: Perform syntax and runtime checks on app.py and report errors.\n7. Testing Start Point: Focus initial testing on Dashboard page as critical functionality.\n\nCRITICAL REQUIREMENTS:\n- Feedback file code_feedback.md MUST start exactly with [APPROVED] or NEED_MODIFY\n- Use write_text_file and validate_python_file tools effectively for output and runtime validation\n- Provide detailed, actionable modifications on NEED_MODIFY without adding new requirements\n- Complete the review within two iterations, stopping immediately if [APPROVED]\n\nOutput: code_feedback.md\"\"\",\n            \"tools\": [\"write_text_file\", \"validate_python_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"AppGenerator\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"AppGenerator\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"AppGenerator\",\n            \"reviewer_agent\": \"CodeCritic\",\n            \"review_criteria\": \"Validate that app.py and templates/*.html strictly conform to design_spec.md requirements including route correctness, HTML element IDs, data file access, version control implementation, content scheduling, and analytics display; also verify code passes syntax and runtime validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"code_feedback.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignGenerator": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications for content management systems.

Your goal is to produce a thorough design_spec.md detailing all application pages, Flask route paths, precise UI element IDs, data file formats, and user interaction flows. You will create or revise this specification from the user task description and reviewer feedback for at most two refinement iterations.

Task Details:
- Read user_task_description from CONTEXT
- Read current design_spec.md draft and design_feedback.md when available
- On initial iteration, write a complete design_spec.md covering all pages, routes, UI elements, data schemas, and interactions
- Upon NEED_MODIFY feedback, incorporate every required correction and rewrite design_spec.md fully
- Upon [APPROVED], maintain the approved design

**Section 1: Page and Route Specifications**
- Define Flask route paths exactly as specified for all pages (e.g., dashboard, article creation, editing, version history, analytics)
- Specify the page template file names and their corresponding route URLs
- List each page's main container IDs and all required element IDs exactly

**Section 2: UI Element and Interaction Details**
- Describe each UI element’s ID and role on the page, e.g., buttons, inputs, lists
- Include user interaction flows such as navigation and version control workflows
- Ensure the Dashboard page is emphasized as the testing start point

**Section 3: Data Storage Formats**
- Specify exact format, field order, and example rows for each required data text file (users.txt, articles.txt, article_versions.txt, etc.)
- Clarify field types, expected values, and relationships between files (e.g., article_id linking)

CRITICAL SUCCESS CRITERIA:
- Limit iterations to two refinements at most
- Incorporate all NEED_MODIFY feedback fully without adding extra requirements
- Use write_text_file tool to output design_spec.md
- Output file must be named design_spec.md

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'design_feedback.md', 'source': 'DesignCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "DesignCritic": {
        "prompt": (
            """You are a Design Reviewer specializing in Flask web application design specifications for content management systems.

Your goal is to critically review design_spec.md against the user_task_description, ensuring completeness, correctness, and strict conformance with UI element IDs, routing, data formats, and testing start requirements. Provide gated feedback with either approval or detailed modifications for at most two iterations.

Task Details:
- Read user_task_description and current design_spec.md from CONTEXT
- Focus review on completeness of page routes, exact UI element IDs, precise data storage format compliance, version control workflows, analytics specification, and testing start from Dashboard
- Write design_feedback.md starting exactly with either '[APPROVED]' if acceptable or 'NEED_MODIFY' followed by concrete and explicit correction points
- Confirm no additions beyond user task requirements; feedback must be clear and actionable

Review Requirements:
1. Verify all specified routes match user task page design and URL paths exactly.
2. Confirm all UI element IDs are present and match the given naming conventions precisely.
3. Validate data file format specifications (field order, allowed values, and example rows) against the user task description.
4. Ensure version control and editorial workflow elements are correctly described.
5. Confirm the testing start point is set to the Dashboard page as requested.

CRITICAL REQUIREMENTS:
- design_feedback.md must start with the byte-1 marker exactly '[APPROVED]' or 'NEED_MODIFY'
- No extraneous headers, whitespace, or prefixes before the marker
- Use write_text_file tool to save the complete feedback
- Limit review iterations to two refinements at most

Output: design_feedback.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_feedback.md'}],

    },

    "AppGenerator": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web application development.

Your goal is to implement or revise the complete Flask backend and frontend template files from design specifications and code review feedback for at most two iterations.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration or when feedback begins NEED_MODIFY, rewrite entire app.py and all templates/*.html complying fully with design_spec.md
- On feedback [APPROVED], maintain the approved source unchanged
- Output updated app.py and templates/*.html files reflecting all routes, UI element IDs, data storage, version control, scheduling, and analytics

**Section 1: Flask Application Implementation**
- Implement all Flask routes exactly as specified, including dynamic routes with parameters
- Handle local text file data storage for all required data files (e.g., users.txt, articles.txt, versions, approvals)
- Implement version control features with article versioning and restoration
- Integrate content scheduling and analytics data retrieval and display

**Section 2: Template Files Implementation**
- Create or revise templates/*.html files matching routes and specified element IDs exactly
- Ensure pages contain all required UI elements with correct IDs as listed in design_spec.md
- Templates must support dynamic content rendering passed from Flask views

**Section 3: Compliance and Code Quality**
- Ensure code complies with design_spec.md requirements without omission or unauthorized additions
- Follow Python best practices while ensuring clear, maintainable Flask code
- Synchronize data keys and references exactly with design_spec.md

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save outputs: app.py and templates/*.html files
- Rewrite complete app.py and all templates/*.html on NEED_MODIFY feedback
- Stop after two iterations or upon [APPROVED] feedback in code_feedback.md
- Strictly follow element IDs, route patterns, and data file formats from design_spec.md

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignGenerator'}, {'type': 'text_file', 'name': 'app.py', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'AppGenerator'}, {'type': 'text_file', 'name': 'code_feedback.md', 'source': 'CodeCritic'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "CodeCritic": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application code reviews and validation.

Your goal is to review the Flask backend and frontend template code for correctness, conformance to design specifications, and quality, providing gated feedback for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify all Flask routes, including dynamic routes, match design_spec.md
- Check each template page for exact UI element presence and correct IDs as specified
- Confirm local text file interactions match specified data files and formats
- Perform basic runtime validation and code quality assessment of app.py
- Begin code_feedback.md with [APPROVED] if all checks pass or NEED_MODIFY followed by concrete required changes if issues exist

Review Requirements:
1. Route Compliance: Validate all endpoints, parameters, and HTTP methods exactly per design_spec.md.
2. UI Elements: Confirm presence and correctness of all HTML element IDs and structural UI components on each route’s template.
3. Data Handling: Verify reading/writing to text files aligned with data formats (users.txt, articles.txt, versions, approvals, workflow_stages, comments, analytics).
4. Version Control & Scheduling: Ensure article versioning, restoring functionality, and content scheduling are implemented as per spec.
5. Analytics Display: Check that engagement metrics and analytics data are displayed correctly.
6. Code Quality: Perform syntax and runtime checks on app.py and report errors.
7. Testing Start Point: Focus initial testing on Dashboard page as critical functionality.

CRITICAL REQUIREMENTS:
- Feedback file code_feedback.md MUST start exactly with [APPROVED] or NEED_MODIFY
- Use write_text_file and validate_python_file tools effectively for output and runtime validation
- Provide detailed, actionable modifications on NEED_MODIFY without adding new requirements
- Complete the review within two iterations, stopping immediately if [APPROVED]

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
        ("DesignCritic", """Check that design_spec.md meets all page design requirements including routes, exact element IDs, data storage formats, version control workflows, analytics presentation, and testing start point; require precise and unambiguous specifications; feedback must prompt either approval or detailed modification requests.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'design_feedback.md'}])
    ],

    'AppGenerator': [
        ("CodeCritic", """Validate that app.py and templates/*.html strictly conform to design_spec.md requirements including route correctness, HTML element IDs, data file access, version control implementation, content scheduling, and analytics display; also verify code passes syntax and runtime validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'code_feedback.md'}])
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
            "Create or revise the complete design_spec.md.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the latest design_spec.md against user_task_description. "
            "Write design_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
import glob

async def implementation_and_verification_phase():
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

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html.\n\n"
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
            "Review the latest app.py and templates against design_spec.md. "
            "Write code_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
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
