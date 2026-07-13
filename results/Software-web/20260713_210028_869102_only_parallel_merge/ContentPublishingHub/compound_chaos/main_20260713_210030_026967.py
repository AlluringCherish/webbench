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
# 20260713_210030_026967/main_20260713_210030_026967.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs for ContentPublishingHub covering all pages and elements, and merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create complete detailed design candidates, including all routes, page titles, \"\n        \"element IDs, UI elements, data storage formats, and interactions from the user task without access to each other's work; \"\n        \"DesignMerger then reviews both candidates and writes design_spec.md consolidating all features and ensuring no omissions.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in comprehensive web application design specifications for Flask-based projects.\n\nYour goal is to produce a comprehensive design candidate for the ContentPublishingHub web app that includes all pages specified in the user task, with exact routes, page titles, element IDs, and UI elements. Additionally, specify data storage formats, Flask template mappings, and detailed user interactions and editor workflows.\n\nTask Details:\n- Read full user_task_description from context\n- Produce design_candidate_a.md including complete details on pages, routes, UI elements, element IDs, and data file formats\n- Describe Flask template names and mappings for all pages\n- Include descriptions of user workflows, version control, content scheduling, and editorial interactions\n\nDesign Specification Requirements:\n1. Pages and Routing\n   - List each page with exact Flask route paths\n   - Specify template filenames (e.g., dashboard.html)\n   - Provide page container element IDs and all critical UI element IDs\n\n2. UI Element Details\n   - Include all interactive elements like buttons, inputs, dropdowns with exact ids\n   - Describe content displayed in each section/element relevant to user task\n\n3. Data Storage Format\n   - Specify text file names and exact pipe-delimited field orders\n   - Provide field descriptions and example data\n\n4. User Workflows\n   - Define workflows for creating, editing, saving, versioning articles\n   - Editorial approval process and comment interactions\n   - Content publishing and analytics overview\n\nCRITICAL REQUIREMENTS:\n- Use only write_text_file tool to produce design_candidate_a.md\n- Ensure coverage is complete and matches user task specifics exactly\n- Do not merge or combine designs with any external sources; work independently\n- Output file: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in detailed web application design for Flask frameworks.\n\nYour goal is to independently produce an alternative detailed design candidate for the ContentPublishingHub web application. This design must cover all pages, route specifications, UI element IDs, data storage arrangement, Flask template and route designs, and user workflows.\n\nTask Details:\n- Read full user_task_description from context\n- Produce design_candidate_b.md with complete page-by-page specifications\n- Define all Flask routes and map to HTML templates explicitly\n- Include full UI element IDs and their types for all interactive components\n- Specify data storage text files with field formats and example data\n- Document content versioning, editorial comments, approval workflow, content scheduling, and analytics access\n\nCRITICAL REQUIREMENTS:\n- Use only write_text_file tool to save design_candidate_b.md\n- Work independently without referencing any other design candidate\n- Ensure full completeness and accuracy per the user task description\n- Output file: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Integrator specializing in consolidating comprehensive web app design documents for Flask applications.\n\nYour goal is to review, reconcile, and merge two independent design candidates—design_candidate_a.md and design_candidate_b.md—into a final unified design_spec.md for the ContentPublishingHub web app. The merged specification must describe Flask routes, exact page titles, element IDs, templates, data file formats, and interaction workflows covering all specified pages and features.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md from context\n- Compare both design candidates against the user task for completeness and consistency\n- Resolve any conflicts or omissions, merging the best and most complete aspects\n- Produce a comprehensive final design_spec.md covering:\n  * Flask routes with exact route paths and methods\n  * HTML templates corresponding to routes\n  * All page container IDs and UI element IDs exactly as required\n  * Data storage formats: text file names, pipe-delimited fields, descriptions, examples\n  * Key user interactions, editorial workflows, version control, content scheduling, analytics access\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output the final design_spec.md\n- Ensure no omissions or contradictions remain from input candidates\n- All final element IDs, route paths, and data formats must match user task or best candidate specifications\n- Output must enable independent development of backend and frontend without ambiguity\n- Output file: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_a.md covers all user task requirements fully including routes, pages, UI elements, data formats, and workflows before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_b.md covers all user task requirements fully including routes, pages, UI elements, data formats, and workflows before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Flask web application bundles for ContentPublishingHub and merge into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement full Flask web app candidates (app_candidate_*.py and \"\n        \"templates_candidate_*/*.html) adhering strictly to design_spec.md; ImplementationMerger then compares both candidates and writes final \"\n        \"app.py and templates/*.html enforcing all routes, page titles, element IDs, data storage, and UI contracts.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend Flask Developer specializing in building full-stack web applications using Flask framework.\n\nYour goal is to independently develop a complete Flask web application candidate with isolated template directory 'templates_candidate_a' for ContentPublishingHub.\n\nTask Details:\n- Read design_spec.md and user_task_description for understanding UI, routes, data formats, and requirements\n- Produce app_candidate_a.py implementing all routes with correct Flask render_template calls using 'templates_candidate_a' directory\n- Implement all page containers with specified IDs, buttons, inputs, and UI elements exactly as per design_spec.md\n- Flexibly parse all data/*.txt files respecting field orders and formats described\n- Provide visible user success and error messages for relevant actions\n- Output app_candidate_a.py and all HTML template files in templates_candidate_a directory\n\nImplementation Guidelines:\n1. Flask App Structure:\n   - Use Flask best practices: create app, configure secret key, route definitions\n   - Use render_template specifying the isolated template folder 'templates_candidate_a'\n   - Implement error handling and success message flashing with clear UI indications\n\n2. Route Handlers:\n   - Implement each route defined in design_spec.md with precise URL patterns, methods, and context variables\n   - Ensure routes serve the correct template files with expected page container IDs and UI elements\n   - Implement form handling for POST requests where applicable, with validation and user feedback\n\n3. Data Handling:\n   - Parse data files from 'data/' directory with pipe-delimited format; do NOT assume headers\n   - Map data file fields exactly as specified without adding/removing fields\n   - Gracefully handle missing or malformed data\n\n4. Templates Implementation:\n   - Build complete HTML templates with all required element IDs, buttons, inputs per design_spec.md spec\n   - Use Jinja2 syntax to render dynamic content and loops\n   - Maintain isolated templates in 'templates_candidate_a' directory only\n\nCRITICAL REQUIREMENTS:\n- Use ONLY write_text_file tool to save output source code and templates\n- Do NOT refer to or depend on templates from other candidates\n- Must implement all UI contracts: element IDs, page containers, buttons, inputs as specified\n- Provide visible success and error messages where relevant\n- Maintain consistent data parsing and usage throughout\n- Follow code organization and naming conventions consistent with Flask best practices\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Backend Flask Developer specializing in building full-stack web applications using Flask framework.\n\nYour goal is to independently develop a complete Flask web application candidate with isolated template directory 'templates_candidate_b' for ContentPublishingHub.\n\nTask Details:\n- Read design_spec.md and user_task_description for understanding UI, routes, data formats, and requirements\n- Produce app_candidate_b.py implementing all routes with correct Flask render_template calls using 'templates_candidate_b' directory\n- Implement all page containers with specified IDs, buttons, inputs, and UI elements exactly as per design_spec.md\n- Flexibly parse all data/*.txt files respecting field orders and formats described\n- Provide visible user success and error messages for relevant actions\n- Output app_candidate_b.py and all HTML template files in templates_candidate_b directory\n\nImplementation Guidelines:\n1. Flask App Structure:\n   - Use Flask best practices: create app, configure secret key, route definitions\n   - Use render_template specifying the isolated template folder 'templates_candidate_b'\n   - Implement error handling and success message flashing with clear UI indications\n\n2. Route Handlers:\n   - Implement each route defined in design_spec.md with precise URL patterns, methods, and context variables\n   - Ensure routes serve the correct template files with expected page container IDs and UI elements\n   - Implement form handling for POST requests where applicable, with validation and user feedback\n\n3. Data Handling:\n   - Parse data files from 'data/' directory with pipe-delimited format; do NOT assume headers\n   - Map data file fields exactly as specified without adding/removing fields\n   - Gracefully handle missing or malformed data\n\n4. Templates Implementation:\n   - Build complete HTML templates with all required element IDs, buttons, inputs per design_spec.md spec\n   - Use Jinja2 syntax to render dynamic content and loops\n   - Maintain isolated templates in 'templates_candidate_b' directory only\n\nCRITICAL REQUIREMENTS:\n- Use ONLY write_text_file tool to save output source code and templates\n- Do NOT refer to or depend on templates from other candidates\n- Must implement all UI contracts: element IDs, page containers, buttons, inputs as specified\n- Provide visible success and error messages where relevant\n- Maintain consistent data parsing and usage throughout\n- Follow code organization and naming conventions consistent with Flask best practices\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integrator specializing in Flask web application merging and standardization.\n\nYour goal is to evaluate two full Flask web app candidates and their template bundles for ContentPublishingHub, resolve discrepancies, and merge them into a single final app.py and templates/*.html bundle with no dependency on candidate template directories.\n\nTask Details:\n- Read design_spec.md to understand all required routes, page containers, element IDs, UI elements, data file formats, and UI contracts\n- Compare app_candidate_a.py and app_candidate_b.py plus their respective templates_candidate_a/*.html and templates_candidate_b/*.html to find differences and inconsistencies\n- Resolve conflicts to enforce strict compliance with design_spec.md on:\n  - All Flask routes, URL patterns, HTTP methods, and context variables\n  - Template filenames, page titles, element IDs, buttons, inputs, and layout structures\n  - Data file parsing matching exact field orders and handling per design_spec.md\n  - Visible user success and error messages consistency and correctness\n  - Proper usage of Flask render_template referring to unified templates/*.html directory\n\nMerge Procedure:\n1. Source Code Integration:\n   - Merge Python source files app_candidate_a.py and app_candidate_b.py ensuring no duplicate routes or conflicting implementations\n   - Preserve best implementation details from both candidates ensuring full feature coverage\n   - Adjust render_template calls to use unified templates directory (templates/)\n   - Maintain consistent code style and structure\n\n2. Template Integration:\n   - Merge HTML templates from both candidate directories into a unified templates/ folder\n   - Ensure all required element IDs, page container IDs, buttons, inputs are present and correct as per design_spec.md\n   - Resolve conflicting template content by selecting the most complete and standards-compliant version\n   - Ensure Jinja2 templating syntax correctness and consistent variable usage\n\n3. Validation:\n   - Validate that the merged app.py and templates/*.html fully comply with design_spec.md requirements\n   - Confirm all routes exist and functionally map to correct templates and data\n   - Confirm data file parsing accuracy and handling in merged app.py\n   - Confirm visible messages display properly on UI actions\n\nCRITICAL REQUIREMENTS:\n- Use ONLY write_text_file tool to save final app.py and templates/*.html files\n- Final merged output must have NO runtime dependence on candidate template directories\n- All element IDs, routes, UI elements must strictly comply with design_spec.md\n- Ensure merged artifacts are fully functional and ready for deployment\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess app_candidate_a.py and templates_candidate_a/*.html for full feature implementation and design_spec.md compliance independently of candidate B.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess app_candidate_b.py and templates_candidate_b/*.html for full feature implementation and design_spec.md compliance independently of candidate A.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Generate two independent validation reports for ContentPublishingHub's app.py and templates, and merge their repairs into final app.py and templates\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate app.py and templates/*.html for syntax, route access, UI elements, \"\n        \"data file parsing, and specified workflows starting from the Dashboard page; RepairMerger then merges their findings and writes final \"\n        \"corrected app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in validation of Flask web applications and frontend templates.\n\nYour goal is to independently validate the backend (app.py) and frontend templates for correctness, syntax, and runtime behavior, producing a detailed validation report.\n\nTask Details:\n- Read app.py and all templates/*.html files from ImplementationMerger\n- Read design_spec.md for official specifications and user_task_description for context\n- Produce validation_a.md summarizing results of validation and testing\n\nValidation Requirements:\n1. **Syntax and Runtime Checks**:\n   - Use validate_python_file tool on app.py to confirm syntax and runtime correctness\n   - Perform route tests starting with /dashboard to confirm accessibility and correct HTTP methods\n\n2. **Frontend Validation**:\n   - Check all templates for presence of exact required element IDs as per design_spec.md\n   - Verify correct usage of Flask render_template with proper context variables passed\n\n3. **Functional Testing**:\n   - Validate data file parsing from 'data' directory matches specified schemas and field orders\n   - Test user workflows through UI starting at /dashboard, including navigation and visible success/error messages\n   - Ensure the presence and stability of UI elements like buttons, feeds, and stats sections\n\n4. **Report Composition**:\n   - Document all tests performed, pass/fail results, and any defects found\n   - Provide actionable repair suggestions for defects and inconsistencies\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools to perform validations\n- Save results only via write_text_file as validation_a.md\n- Follow design_spec.md and user_task_description strictly, do not infer beyond specifications\n- Do not modify any code or templates; only validate and report\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in thorough compliance validation for Flask backend and frontend templates.\n\nYour goal is to comprehensively validate the application implementation against all user requirements, focusing on multi-page access, UI stability, data handling, and workflow correctness.\n\nTask Details:\n- Read app.py and templates/*.html files from ImplementationMerger\n- Consult design_spec.md and user_task_description for detailed requirements\n- Produce validation_b.md detailing validation findings\n\nValidation Requirements:\n1. **Functionality Testing**:\n   - Test application routes starting at /dashboard, verifying route existence and correct HTTP method handling\n   - Evaluate full user workflows across multiple pages, including article creation, editing, version history, and analytics\n\n2. **UI Elements & Stability**:\n   - Confirm all specified element IDs are present and stable on respective pages as per design_spec.md\n   - Validate visible feedback for success/error messages during user interactions\n\n3. **Data File Handling**:\n   - Test data file parsing from all specified text files (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt)\n   - Verify field order, parsing robustness, and correct data utilization in app.py\n\n4. **Report Composition**:\n   - Clearly document all tests, issues found, and recommended corrections\n   - Emphasize compliance with user workflows and data requirements\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code extensively for syntax and dynamic validations\n- Save complete validation results to validation_b.md using write_text_file only\n- Strictly follow design_spec.md and user_task_description without assumption or extension\n- Do not alter any source files, only perform validation and reporting\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in code repair and merging for Flask web applications.\n\nYour goal is to consolidate independent validation reports, reconcile defects, and produce corrected, fully compliant final implementations of app.py and frontend templates.\n\nTask Details:\n- Read validation_a.md and validation_b.md for defect details from ValidationEngineerA and ValidationEngineerB\n- Review current app.py and templates/*.html from ImplementationMerger alongside design_spec.md and user_task_description\n- Identify discrepancies and repair defects related to:\n  - Flask routes and render_template correctness\n  - Exact presence and naming of element IDs in templates\n  - Data file parsing according to specified field orders and formats\n  - Visible success/error message functionality\n  - Workflow adherence starting from the Dashboard page\n\nRepair and Merging Process:\n1. **Defect Reconciliation**:\n   - Combine and prioritize defects reported by both validation engineers\n   - Resolve contradictions and avoid regression of fixed issues\n\n2. **Code & Template Repair**:\n   - Apply corrections ensuring compliance with design_spec.md and user_task_description\n   - Maintain original design architecture, route structure, and data schema formats\n\n3. **Output Producing**:\n   - Save corrected app.py and all templates/*.html via write_text_file\n   - Ensure no additional features beyond specifications are added\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file exclusively to save final corrected app.py and templates/*.html\n- Carefully validate merge of validation results before applying fixes\n- Preserve all specified routes, element IDs, data parsing logic, and visible feedback behavior\n- Do not introduce unrelated changes or remove any required behaviors\n- Deliver final corrected artifacts meeting 100% compliance with the user task\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for accurate, reproducible, and actionable validation results covering syntax, routes, UI elements, and workflows.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_b.md for comprehensive validation across all required functionalities, including data file parsing and visible messages.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
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
    "DesignAnalystA": {
        "prompt": (
            """You are a Software Designer specializing in comprehensive web application design specifications for Flask-based projects.

Your goal is to produce a comprehensive design candidate for the ContentPublishingHub web app that includes all pages specified in the user task, with exact routes, page titles, element IDs, and UI elements. Additionally, specify data storage formats, Flask template mappings, and detailed user interactions and editor workflows.

Task Details:
- Read full user_task_description from context
- Produce design_candidate_a.md including complete details on pages, routes, UI elements, element IDs, and data file formats
- Describe Flask template names and mappings for all pages
- Include descriptions of user workflows, version control, content scheduling, and editorial interactions

Design Specification Requirements:
1. Pages and Routing
   - List each page with exact Flask route paths
   - Specify template filenames (e.g., dashboard.html)
   - Provide page container element IDs and all critical UI element IDs

2. UI Element Details
   - Include all interactive elements like buttons, inputs, dropdowns with exact ids
   - Describe content displayed in each section/element relevant to user task

3. Data Storage Format
   - Specify text file names and exact pipe-delimited field orders
   - Provide field descriptions and example data

4. User Workflows
   - Define workflows for creating, editing, saving, versioning articles
   - Editorial approval process and comment interactions
   - Content publishing and analytics overview

CRITICAL REQUIREMENTS:
- Use only write_text_file tool to produce design_candidate_a.md
- Ensure coverage is complete and matches user task specifics exactly
- Do not merge or combine designs with any external sources; work independently
- Output file: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Designer specializing in detailed web application design for Flask frameworks.

Your goal is to independently produce an alternative detailed design candidate for the ContentPublishingHub web application. This design must cover all pages, route specifications, UI element IDs, data storage arrangement, Flask template and route designs, and user workflows.

Task Details:
- Read full user_task_description from context
- Produce design_candidate_b.md with complete page-by-page specifications
- Define all Flask routes and map to HTML templates explicitly
- Include full UI element IDs and their types for all interactive components
- Specify data storage text files with field formats and example data
- Document content versioning, editorial comments, approval workflow, content scheduling, and analytics access

CRITICAL REQUIREMENTS:
- Use only write_text_file tool to save design_candidate_b.md
- Work independently without referencing any other design candidate
- Ensure full completeness and accuracy per the user task description
- Output file: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Integrator specializing in consolidating comprehensive web app design documents for Flask applications.

Your goal is to review, reconcile, and merge two independent design candidates—design_candidate_a.md and design_candidate_b.md—into a final unified design_spec.md for the ContentPublishingHub web app. The merged specification must describe Flask routes, exact page titles, element IDs, templates, data file formats, and interaction workflows covering all specified pages and features.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md from context
- Compare both design candidates against the user task for completeness and consistency
- Resolve any conflicts or omissions, merging the best and most complete aspects
- Produce a comprehensive final design_spec.md covering:
  * Flask routes with exact route paths and methods
  * HTML templates corresponding to routes
  * All page container IDs and UI element IDs exactly as required
  * Data storage formats: text file names, pipe-delimited fields, descriptions, examples
  * Key user interactions, editorial workflows, version control, content scheduling, analytics access

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output the final design_spec.md
- Ensure no omissions or contradictions remain from input candidates
- All final element IDs, route paths, and data formats must match user task or best candidate specifications
- Output must enable independent development of backend and frontend without ambiguity
- Output file: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend Flask Developer specializing in building full-stack web applications using Flask framework.

Your goal is to independently develop a complete Flask web application candidate with isolated template directory 'templates_candidate_a' for ContentPublishingHub.

Task Details:
- Read design_spec.md and user_task_description for understanding UI, routes, data formats, and requirements
- Produce app_candidate_a.py implementing all routes with correct Flask render_template calls using 'templates_candidate_a' directory
- Implement all page containers with specified IDs, buttons, inputs, and UI elements exactly as per design_spec.md
- Flexibly parse all data/*.txt files respecting field orders and formats described
- Provide visible user success and error messages for relevant actions
- Output app_candidate_a.py and all HTML template files in templates_candidate_a directory

Implementation Guidelines:
1. Flask App Structure:
   - Use Flask best practices: create app, configure secret key, route definitions
   - Use render_template specifying the isolated template folder 'templates_candidate_a'
   - Implement error handling and success message flashing with clear UI indications

2. Route Handlers:
   - Implement each route defined in design_spec.md with precise URL patterns, methods, and context variables
   - Ensure routes serve the correct template files with expected page container IDs and UI elements
   - Implement form handling for POST requests where applicable, with validation and user feedback

3. Data Handling:
   - Parse data files from 'data/' directory with pipe-delimited format; do NOT assume headers
   - Map data file fields exactly as specified without adding/removing fields
   - Gracefully handle missing or malformed data

4. Templates Implementation:
   - Build complete HTML templates with all required element IDs, buttons, inputs per design_spec.md spec
   - Use Jinja2 syntax to render dynamic content and loops
   - Maintain isolated templates in 'templates_candidate_a' directory only

CRITICAL REQUIREMENTS:
- Use ONLY write_text_file tool to save output source code and templates
- Do NOT refer to or depend on templates from other candidates
- Must implement all UI contracts: element IDs, page containers, buttons, inputs as specified
- Provide visible success and error messages where relevant
- Maintain consistent data parsing and usage throughout
- Follow code organization and naming conventions consistent with Flask best practices

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Backend Flask Developer specializing in building full-stack web applications using Flask framework.

Your goal is to independently develop a complete Flask web application candidate with isolated template directory 'templates_candidate_b' for ContentPublishingHub.

Task Details:
- Read design_spec.md and user_task_description for understanding UI, routes, data formats, and requirements
- Produce app_candidate_b.py implementing all routes with correct Flask render_template calls using 'templates_candidate_b' directory
- Implement all page containers with specified IDs, buttons, inputs, and UI elements exactly as per design_spec.md
- Flexibly parse all data/*.txt files respecting field orders and formats described
- Provide visible user success and error messages for relevant actions
- Output app_candidate_b.py and all HTML template files in templates_candidate_b directory

Implementation Guidelines:
1. Flask App Structure:
   - Use Flask best practices: create app, configure secret key, route definitions
   - Use render_template specifying the isolated template folder 'templates_candidate_b'
   - Implement error handling and success message flashing with clear UI indications

2. Route Handlers:
   - Implement each route defined in design_spec.md with precise URL patterns, methods, and context variables
   - Ensure routes serve the correct template files with expected page container IDs and UI elements
   - Implement form handling for POST requests where applicable, with validation and user feedback

3. Data Handling:
   - Parse data files from 'data/' directory with pipe-delimited format; do NOT assume headers
   - Map data file fields exactly as specified without adding/removing fields
   - Gracefully handle missing or malformed data

4. Templates Implementation:
   - Build complete HTML templates with all required element IDs, buttons, inputs per design_spec.md spec
   - Use Jinja2 syntax to render dynamic content and loops
   - Maintain isolated templates in 'templates_candidate_b' directory only

CRITICAL REQUIREMENTS:
- Use ONLY write_text_file tool to save output source code and templates
- Do NOT refer to or depend on templates from other candidates
- Must implement all UI contracts: element IDs, page containers, buttons, inputs as specified
- Provide visible success and error messages where relevant
- Maintain consistent data parsing and usage throughout
- Follow code organization and naming conventions consistent with Flask best practices

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integrator specializing in Flask web application merging and standardization.

Your goal is to evaluate two full Flask web app candidates and their template bundles for ContentPublishingHub, resolve discrepancies, and merge them into a single final app.py and templates/*.html bundle with no dependency on candidate template directories.

Task Details:
- Read design_spec.md to understand all required routes, page containers, element IDs, UI elements, data file formats, and UI contracts
- Compare app_candidate_a.py and app_candidate_b.py plus their respective templates_candidate_a/*.html and templates_candidate_b/*.html to find differences and inconsistencies
- Resolve conflicts to enforce strict compliance with design_spec.md on:
  - All Flask routes, URL patterns, HTTP methods, and context variables
  - Template filenames, page titles, element IDs, buttons, inputs, and layout structures
  - Data file parsing matching exact field orders and handling per design_spec.md
  - Visible user success and error messages consistency and correctness
  - Proper usage of Flask render_template referring to unified templates/*.html directory

Merge Procedure:
1. Source Code Integration:
   - Merge Python source files app_candidate_a.py and app_candidate_b.py ensuring no duplicate routes or conflicting implementations
   - Preserve best implementation details from both candidates ensuring full feature coverage
   - Adjust render_template calls to use unified templates directory (templates/)
   - Maintain consistent code style and structure

2. Template Integration:
   - Merge HTML templates from both candidate directories into a unified templates/ folder
   - Ensure all required element IDs, page container IDs, buttons, inputs are present and correct as per design_spec.md
   - Resolve conflicting template content by selecting the most complete and standards-compliant version
   - Ensure Jinja2 templating syntax correctness and consistent variable usage

3. Validation:
   - Validate that the merged app.py and templates/*.html fully comply with design_spec.md requirements
   - Confirm all routes exist and functionally map to correct templates and data
   - Confirm data file parsing accuracy and handling in merged app.py
   - Confirm visible messages display properly on UI actions

CRITICAL REQUIREMENTS:
- Use ONLY write_text_file tool to save final app.py and templates/*.html files
- Final merged output must have NO runtime dependence on candidate template directories
- All element IDs, routes, UI elements must strictly comply with design_spec.md
- Ensure merged artifacts are fully functional and ready for deployment

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in validation of Flask web applications and frontend templates.

Your goal is to independently validate the backend (app.py) and frontend templates for correctness, syntax, and runtime behavior, producing a detailed validation report.

Task Details:
- Read app.py and all templates/*.html files from ImplementationMerger
- Read design_spec.md for official specifications and user_task_description for context
- Produce validation_a.md summarizing results of validation and testing

Validation Requirements:
1. **Syntax and Runtime Checks**:
   - Use validate_python_file tool on app.py to confirm syntax and runtime correctness
   - Perform route tests starting with /dashboard to confirm accessibility and correct HTTP methods

2. **Frontend Validation**:
   - Check all templates for presence of exact required element IDs as per design_spec.md
   - Verify correct usage of Flask render_template with proper context variables passed

3. **Functional Testing**:
   - Validate data file parsing from 'data' directory matches specified schemas and field orders
   - Test user workflows through UI starting at /dashboard, including navigation and visible success/error messages
   - Ensure the presence and stability of UI elements like buttons, feeds, and stats sections

4. **Report Composition**:
   - Document all tests performed, pass/fail results, and any defects found
   - Provide actionable repair suggestions for defects and inconsistencies

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools to perform validations
- Save results only via write_text_file as validation_a.md
- Follow design_spec.md and user_task_description strictly, do not infer beyond specifications
- Do not modify any code or templates; only validate and report

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in thorough compliance validation for Flask backend and frontend templates.

Your goal is to comprehensively validate the application implementation against all user requirements, focusing on multi-page access, UI stability, data handling, and workflow correctness.

Task Details:
- Read app.py and templates/*.html files from ImplementationMerger
- Consult design_spec.md and user_task_description for detailed requirements
- Produce validation_b.md detailing validation findings

Validation Requirements:
1. **Functionality Testing**:
   - Test application routes starting at /dashboard, verifying route existence and correct HTTP method handling
   - Evaluate full user workflows across multiple pages, including article creation, editing, version history, and analytics

2. **UI Elements & Stability**:
   - Confirm all specified element IDs are present and stable on respective pages as per design_spec.md
   - Validate visible feedback for success/error messages during user interactions

3. **Data File Handling**:
   - Test data file parsing from all specified text files (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt)
   - Verify field order, parsing robustness, and correct data utilization in app.py

4. **Report Composition**:
   - Clearly document all tests, issues found, and recommended corrections
   - Emphasize compliance with user workflows and data requirements

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code extensively for syntax and dynamic validations
- Save complete validation results to validation_b.md using write_text_file only
- Strictly follow design_spec.md and user_task_description without assumption or extension
- Do not alter any source files, only perform validation and reporting

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in code repair and merging for Flask web applications.

Your goal is to consolidate independent validation reports, reconcile defects, and produce corrected, fully compliant final implementations of app.py and frontend templates.

Task Details:
- Read validation_a.md and validation_b.md for defect details from ValidationEngineerA and ValidationEngineerB
- Review current app.py and templates/*.html from ImplementationMerger alongside design_spec.md and user_task_description
- Identify discrepancies and repair defects related to:
  - Flask routes and render_template correctness
  - Exact presence and naming of element IDs in templates
  - Data file parsing according to specified field orders and formats
  - Visible success/error message functionality
  - Workflow adherence starting from the Dashboard page

Repair and Merging Process:
1. **Defect Reconciliation**:
   - Combine and prioritize defects reported by both validation engineers
   - Resolve contradictions and avoid regression of fixed issues

2. **Code & Template Repair**:
   - Apply corrections ensuring compliance with design_spec.md and user_task_description
   - Maintain original design architecture, route structure, and data schema formats

3. **Output Producing**:
   - Save corrected app.py and all templates/*.html via write_text_file
   - Ensure no additional features beyond specifications are added

CRITICAL REQUIREMENTS:
- Use write_text_file exclusively to save final corrected app.py and templates/*.html
- Carefully validate merge of validation results before applying fixes
- Preserve all specified routes, element IDs, data parsing logic, and visible feedback behavior
- Do not introduce unrelated changes or remove any required behaviors
- Deliver final corrected artifacts meeting 100% compliance with the user task

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_a.md', 'source': 'ValidationEngineerA'}, {'type': 'text_file', 'name': 'validation_b.md', 'source': 'ValidationEngineerB'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignAnalystA': [
        ("DesignMerger", """Verify design_candidate_a.md covers all user task requirements fully including routes, pages, UI elements, data formats, and workflows before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Verify design_candidate_b.md covers all user task requirements fully including routes, pages, UI elements, data formats, and workflows before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Assess app_candidate_a.py and templates_candidate_a/*.html for full feature implementation and design_spec.md compliance independently of candidate B.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Assess app_candidate_b.py and templates_candidate_b/*.html for full feature implementation and design_spec.md compliance independently of candidate A.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for accurate, reproducible, and actionable validation results covering syntax, routes, UI elements, and workflows.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Check validation_b.md for comprehensive validation across all required functionalities, including data file parsing and visible messages.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
    DesignAnalystA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignAnalystA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    DesignAnalystB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignAnalystB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    DesignMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=200,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel generation of design candidates
    await asyncio.gather(
        execute(DesignAnalystA, "Generate complete design_candidate_a.md with full pages, routes, UI elements, element IDs, data formats, and user workflows for ContentPublishingHub."),
        execute(DesignAnalystB, "Generate complete design_candidate_b.md with full pages, route specifications, UI elements, element IDs, data storage formats, Flask template mappings, and detailed workflows for ContentPublishingHub.")
    )

    # Read design candidates for merger
    design_candidate_a_content, design_candidate_b_content = "", ""
    try:
        design_candidate_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge designs into final design_spec.md
    await execute(DesignMerger,
                  f"=== DesignCandidateA ===\n{design_candidate_a_content}\n\n"
                  f"=== DesignCandidateB ===\n{design_candidate_b_content}\n"
                  "Merge both independent designs into a comprehensive, complete, and consistent design_spec.md that covers Flask routes, templates, element IDs, data formats, and user workflows exactly matching user task requirements.")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    ImplementationEngineerA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationEngineerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationEngineerB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationEngineerB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ImplementationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel implementation by ImplementationEngineerA and ImplementationEngineerB
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full Flask app candidate app_candidate_a.py and templates_candidate_a/*.html based on design_spec.md and user_task_description. "
                "Use isolated templates_candidate_a directory, implement all UI contracts, routes, and data parsing. Provide visible messages."),
        execute(ImplementationEngineerB,
                "Implement full Flask app candidate app_candidate_b.py and templates_candidate_b/*.html based on design_spec.md and user_task_description. "
                "Use isolated templates_candidate_b directory, implement all UI contracts, routes, and data parsing. Provide visible messages.")
    )

    # Read candidate source code and template contents for merger
    app_candidate_a_code, app_candidate_b_code = "", ""
    templates_candidate_a_files, templates_candidate_b_files = "", ""
    try:
        app_candidate_a_code = open("app_candidate_a.py").read()
    except Exception:
        pass
    try:
        app_candidate_b_code = open("app_candidate_b.py").read()
    except Exception:
        pass
    # For templates, read all candidate templates content as a single string for injection
    try:
        import glob
        files_a = glob.glob("templates_candidate_a/*.html")
        content_a = []
        for f in files_a:
            try:
                content_a.append(f"=== {f} ===\n" + open(f).read())
            except Exception:
                pass
        templates_candidate_a_files = "\n\n".join(content_a)
    except Exception:
        templates_candidate_a_files = ""
    try:
        files_b = glob.glob("templates_candidate_b/*.html")
        content_b = []
        for f in files_b:
            try:
                content_b.append(f"=== {f} ===\n" + open(f).read())
            except Exception:
                pass
        templates_candidate_b_files = "\n\n".join(content_b)
    except Exception:
        templates_candidate_b_files = ""

    # Execute merger agent with all collected inputs
    await execute(ImplementationMerger,
                  f"Merge two full Flask app candidates into final app.py and templates/*.html strictly adhering to design_spec.md.\n"
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a ===\n{templates_candidate_a_files}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b ===\n{templates_candidate_b_files}\n\n"
                  f"Use user_task_description and design_spec.md for guidance and correctness. Output final app.py and templates/*.html.")
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    # Create agents
    ValidationEngineerA = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ValidationEngineerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    ValidationEngineerB = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="ValidationEngineerB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    RepairMerger = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="RepairMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel validations by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate app.py and templates/*.html from ImplementationMerger for syntax, route access, UI elements, data parsing, "
                "and workflows starting from /dashboard. Save report to validation_a.md."),
        execute(ValidationEngineerB,
                "Comprehensively validate app.py and templates/*.html from ImplementationMerger for functionality, UI stability, data handling, "
                "and workflow correctness. Save report to validation_b.md.")
    )

    # Read validation reports
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # Execute RepairMerger to merge validation reports and produce corrected app.py and templates
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_content}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_content}\n"
                  "Review both validation reports and merge findings to repair and produce final compliant app.py and templates/*.html. "
                  "Ensure no features beyond specifications are added, preserving all required functionality and compliance.")
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
