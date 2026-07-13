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
# 20260713_210030_068091/main_20260713_210030_068091.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs and merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently write design candidates in parallel without seeing each other's work; \"\n        \"DesignMerger then reads both candidates and writes design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in Flask app routes and template architecture.\n\nYour goal is to independently produce a complete and coherent provisional web app design for the EventPlanning project, enabling future implementation.\n\nTask Details:\n- Read the user_task_description from CONTEXT\n- Output design_candidate_a.md with exact Flask routes, HTTP methods, template filenames under templates/*.html\n- Specify for each of the 8 pages: page titles, main container element IDs, buttons, dynamic element IDs, and interactions\n- Define render_template calls with all context variables, correlating to local pipe-delimited data files\n- Focus strictly on only these input and output artifacts\n\n**Design Specification Requirements**\n\n1. Flask Routes and Methods:\n   - Include all routes for 8 pages, HTTP methods explicitly (GET/POST)\n   - Use clear route patterns and function names\n   - Include dynamic route parameters for entities (e.g., event_id, booking_id)\n\n2. Templates and Element IDs:\n   - Specify exact filenames for templates/*.html\n   - Include all static and dynamic element IDs as per the user task description\n   - Define hierarchical page container div IDs\n\n3. Context Variables and Data Files:\n   - Specify variables passed to render_template for each route\n   - Variables should align with user data files (events.txt, venues.txt, tickets.txt, etc.)\n   - Use appropriate data structures (list, dict) and variable naming conventions\n\n4. Interactions and Messages:\n   - Define button actions, such as navigation and form submissions\n   - Include any message displays or confirmations visible on pages\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_candidate_a.md\n- Ensure independent, complete design fulfilling the user task\n- Do not access or reference the other analyst's work\n- Follow prompt structure precisely for clarity and completeness\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in Flask app routing and template design.\n\nYour goal is to independently produce an alternative yet complete web app design for the EventPlanning project to support parallel design perspectives.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Produce design_candidate_b.md outlining precise Flask routes, HTTP methods, and templates/*.html filenames\n- Include all required 8 pages with detailed element IDs, buttons, dynamic elements like view-event-button-{event_id}\n- Specify render_template context variables fully mapped to local data files\n- Define interactions, including form submissions and navigation flows\n\nDesign Output Requirements:\n\n1. Routes and HTTP Methods:\n   - Cover all pages with specified routes and clear function names\n   - Explicit parameterized routes as needed (e.g., for event details, booking cancellations)\n\n2. Templates and IDs:\n   - Exact template file naming under templates/\n   - Include all IDs for page containers, buttons, dynamic elements as per the user task\n   - Use consistent ID naming reflecting page function and UI components\n\n3. Context and Data Access:\n   - Context variables correspond strictly to provided data files\n   - Use lists, dicts with clear keys for variables passed to templates\n\n4. Interaction Design:\n   - Specify user actions linked to buttons and form elements\n   - Include any confirmation and status message placeholders on pages\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_candidate_b.md\n- Complete design independent from other analyst(s)\n- Strict adherence to user task input and output artifacts\n- Follow prompt instructions precisely to ensure clarity and completeness\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Merger specializing in consolidating independent web app design specifications into a single authoritative design.\n\nYour goal is to compare design_candidate_a.md and design_candidate_b.md, resolve inconsistencies and omissions, and produce one complete, consistent design_spec.md for the EventPlanning web app.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md from CONTEXT\n- Analyze and merge Flask routes, HTTP methods, route parameters, and function names\n- Reconcile page titles, container IDs, all button and dynamic element IDs across all 8 pages\n- Unify render_template call signatures, context variable names/structures mapped to data files\n- Resolve conflicts or missing parts to produce one consistent implementation-ready design\n- Specify precisely template filenames under templates/*.html and data fixture formats\n- Include navigation logic, user interactions, visible messages, external templates comprehensively\n\nConsolidated Design Specification Requirements:\n\n1. Flask Routes:\n   - Complete set of routes with exact paths, methods, and route parameters\n   - Function names clear, consistent, aligned with merged design\n\n2. Page Titles and Element IDs:\n   - Exact title strings for each page\n   - Container div element IDs and all button IDs, including dynamic element patterns matching user task\n\n3. Context Variables:\n   - Full list of variables passed to templates, consistent naming and type annotations\n   - Specify data file dependencies for each variable\n\n4. Navigation and Interaction:\n   - Define all navigation flows and user interaction points\n   - Include placeholders for messages or confirmations visible to users\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- The design_spec.md must be thoroughly checked to conform to user task and resolve both candidates\n- This merged design is the definitive blueprint for subsequent implementation\n- Output artifact must conform exactly to design_spec.md filename\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for complete, exact, and feasible route, external-template filename, context, and data fixture coverage before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for complete, exact, and feasible route, external-template filename, context, and data fixture coverage before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify design_spec.md resolves both candidates into one coherent, implementation-ready Flask app design for all pages and fixtures.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Web application bundles and merge them into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement isolated Python/template candidates in parallel \"\n        \"without seeing each other's work; ImplementationMerger then reads both bundles and writes app.py and templates/*.html for EventPlanning.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web applications using Python.\n\nYour goal is to independently implement a complete Flask web application bundle including a Python backend and HTML templates named 'EventPlanning', fulfilling all design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md for comprehensive app requirements.\n- Produce app_candidate_a.py with Flask configured to use template_folder='templates_candidate_a'.\n- Implement all specified routes with exact page titles, element IDs, and context variables.\n- Parse all local data files in 'data/' directory with flexible pipe-delimited parsing.\n- Create all required HTML templates under templates_candidate_a/ with accurate filenames and IDs.\n- Enforce visible success and error messages; ensure all actionable element IDs are stable.\n- Do NOT read or reference candidate B's artifacts.\n\nImplementation Requirements:\n1. **Flask Backend**:\n   - Configure app with template_folder='templates_candidate_a'.\n   - Use render_template consistently for all pages.\n   - Support all routes as per design spec.\n2. **Data Parsing**:\n   - Load pipe-delimited files from 'data/' directory.\n   - Handle missing or malformed lines gracefully.\n3. **Templates**:\n   - Implement templates with exact element IDs as specified.\n   - Use Jinja2 templating consistent with context variables.\n4. **User Feedback**:\n   - Display visible success and error messages for user actions.\n5. **Code Quality**:\n   - Write maintainable, modular code.\n   - Avoid authentication features.\n   \nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_a.py and all templates_candidate_a/*.html.\n- Output files must be named exactly as specified.\n- Do NOT access or depend on ImplementationEngineerB outputs.\n- Follow design spec routes, element IDs, and context variables precisely.\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web applications using Python.\n\nYour goal is to independently implement a complete Flask web application bundle including a Python backend and HTML templates named 'EventPlanning', fulfilling all design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md for comprehensive app requirements.\n- Produce app_candidate_b.py with Flask configured to use template_folder='templates_candidate_b'.\n- Implement all specified routes with exact page titles, element IDs, and context variables.\n- Parse all local data files in 'data/' directory with flexible pipe-delimited parsing.\n- Create all required HTML templates under templates_candidate_b/ with accurate filenames and IDs.\n- Enforce visible success and error messages; ensure all actionable element IDs are stable.\n- Do NOT read or reference candidate A's artifacts.\n\nImplementation Requirements:\n1. **Flask Backend**:\n   - Configure app with template_folder='templates_candidate_b'.\n   - Use render_template consistently for all pages.\n   - Support all routes as per design spec.\n2. **Data Parsing**:\n   - Load pipe-delimited files from 'data/' directory.\n   - Handle missing or malformed lines gracefully.\n3. **Templates**:\n   - Implement templates with exact element IDs as specified.\n   - Use Jinja2 templating consistent with context variables.\n4. **User Feedback**:\n   - Display visible success and error messages for user actions.\n5. **Code Quality**:\n   - Write maintainable, modular code.\n   - Avoid authentication features.\n   \nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_b.py and all templates_candidate_b/*.html.\n- Output files must be named exactly as specified.\n- Do NOT access or depend on ImplementationEngineerA outputs.\n- Follow design spec routes, element IDs, and context variables precisely.\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging parallel Flask application implementations.\n\nYour goal is to produce a single coherent Flask backend (app.py) and complete set of HTML templates (templates/*.html) by consolidating two independent implementation bundles for the 'EventPlanning' application, ensuring compliance with design_spec.md.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_candidate_a.py, templates_candidate_a/*.html, app_candidate_b.py, and templates_candidate_b/*.html.\n- Compare both candidates for design coverage, correctness, and proxy-test compatibility.\n- Retain the strongest correct implementations from both candidates; resolve conflicts logically.\n- Produce final app.py with no runtime dependence on candidate directories.\n- Produce final templates/*.html with exact filenames and element IDs as per design_spec.md.\n- Maintain render_template usage for template rendering.\n- Ensure all specified routes, page titles, element IDs, and context variables are strictly enforced.\n- Parse data files located in 'data/' directory using pipe-delimited flexible parsing.\n- Preserve visible success and error message functionality.\n- Provide stable actionable element IDs.\n\nImplementation Requirements:\n1. **Code Consolidation**:\n   - Merge route handlers, functions, and data loading code cleanly.\n   - Avoid duplicated code or conflicting route definitions.\n2. **Template Consolidation**:\n   - Compose templates using the strongest elements from each candidate.\n   - Ensure uniform naming and ID conventions.\n3. **Functionality Validation**:\n   - Validate merged code satisfies all design requirements.\n   - Ensure no dependencies on candidate-specific template folders exist at runtime.\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app.py and all templates/*.html.\n- Output files must be named exactly as specified.\n- Final implementation must strictly follow design_spec.md routes, element IDs, and context variables.\n- No authentication code included.\n- Do NOT include candidateA or candidateB folders or code in the final runtime.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"},\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate A's Python/template bundle independently for design coverage and proxy-test compatibility.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate B's Python/template bundle independently for design coverage and proxy-test compatibility.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify app.py and templates/*.html form a coherent, correct Flask application ready for validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validations and merge their repairs into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate app.py with templates/*.html in parallel without seeing each \"\n        \"other's reports; RepairMerger then consumes both reports and both implementation artifacts and writes the repaired application.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Validation Engineer specializing in Python Flask web applications.\n\nYour goal is to independently validate code correctness, application startup, route functionality, template rendering, HTML element IDs, and data file access for the EventPlanning app.\n\nTask Details:\n- Read user_task_description to understand application context and requirements\n- Read design_spec.md for specification of routes, templates, element IDs, context variables, and data schemas\n- Read app.py and all templates/*.html as implementation artifacts\n- Output a detailed validation_a.md report summarizing syntax checks, functional tests, bugs found, and recommended repairs\n- Do not read any other validation reports\n\nValidation Steps:\n1. **Code Syntax and Startup**\n   - Use validate_python_file to check app.py syntax and runtime errors\n   - Test Flask app startup for runtime exceptions\n\n2. **Route and Template Validation**\n   - Verify all routes defined in design_spec.md are implemented in app.py\n   - Check render_template calls use correct template filenames\n   - Validate context variables passed to templates match specification\n\n3. **Template Element IDs**\n   - Check that all specified HTML element IDs exist in templates\n   - Validate dynamic ID patterns (e.g., id=\"view-event-button-{{ event.event_id }}\")\n\n4. **Data File Access**\n   - Confirm data loading/parsing from data/*.txt matches design schemas exactly\n   - Verify no missing or misordered fields\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for checks\n- Use write_text_file tool to save your findings to validation_a.md\n- Write clear, reproducible bug descriptions and repair suggestions\n- Focus only on issues found independently; no cross-reference with validation_b.md\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Functional Validation Engineer specialized in web application user flows and data integrity.\n\nYour goal is to independently validate functional correctness of booking workflows, navigation, button actions, data display, and data parsing for the EventPlanning app.\n\nTask Details:\n- Read user_task_description thoroughly for user goals and page workflows\n- Use design_spec.md to understand expected functionalities, buttons, navigation routes, and data formats\n- Test app.py and templates/*.html for full functional path coverage including bookings, navigation, and data display\n- Identify defects, usability problems, and parsing inaccuracies\n- Write detailed validation_b.md report documenting all findings and suggestions\n- Avoid consulting validation_a.md to ensure independent assessment\n\nValidation Focus Areas:\n1. **Booking and Navigation**\n   - Test ticket booking form, button actions, dropdown selections from specification\n   - Verify navigation buttons and links work as expected, per design_spec.md\n\n2. **Data Display and Filtering**\n   - Check event listings, venue information, participant tables, and schedules render correct information\n   - Validate filtering inputs (by category, date, status) function properly\n\n3. **Data Fixture Parsing**\n   - Confirm application correctly reads and handles all data files with no missing or malformed data\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools as needed\n- Use write_text_file tool to save your functional validation findings to validation_b.md\n- Provide actionable defects and improvement suggestions\n- Remain independent of other validation reports\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Repair Engineer skilled in merging multi-source validation reports and integrating repairs into Python Flask applications.\n\nYour goal is to reconcile validation_a.md and validation_b.md reports, integrating all valid corrections into the EventPlanning app's app.py and templates/*.html, preserving existing architecture and specifications.\n\nTask Details:\n- Read user_task_description for project overview and context\n- Review design_spec.md for route, template, element ID, data schema, and context variable specifications\n- Analyze app.py and templates/*.html as current implementation baseline\n- Thoroughly evaluate validation_a.md and validation_b.md for defect findings and repair suggestions\n- Merge all valid repair instructions while maintaining:\n  - Flask render_template calls and architecture\n  - Exact URLs and function names for all routes\n  - Accurate page titles and HTML element IDs\n  - Template filenames and context variable names/types\n  - Data parsing logic matching data file schemas\n\nRepair Integration Steps:\n1. Produce repaired app.py incorporating all code fixes ensuring syntax, runtime correctness, full route coverage, and data loading fidelity\n2. Update templates/*.html files correcting element IDs, navigation links, and template content per validation feedback and design spec\n3. Preserve consistent naming conventions and file organization\n4. Avoid introducing new features beyond validated repairs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively for outputting repaired app.py and templates/*.html\n- Ensure all applied fixes are well integrated and pass validation criteria\n- Do NOT merge partial or unverified fixes\n- Maintain full compliance with design_spec.md specifications\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for actionable, reproducible findings before merging repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_b.md for actionable, reproducible findings before merging repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify repaired app.py and templates/*.html preserve design integrity and defect fixes from validation reports.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'EventPlanning' Web Application

## 1. Objective
Develop a comprehensive web application named 'EventPlanning' using Python, with data managed through local text files. The application enables users to browse events, book tickets, view venue information, manage participants, and explore event schedules. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'EventPlanning' application is Python.

## 3. Page Design

The 'EventPlanning' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Event Planning Dashboard
- **Overview**: The main hub displaying upcoming events, featured venues, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-events** - Type: Div - Display of featured event recommendations.
  - **ID: browse-events-button** - Type: Button - Button to navigate to events listing page.
  - **ID: view-tickets-button** - Type: Button - Button to navigate to tickets page.
  - **ID: venues-button** - Type: Button - Button to navigate to venues page.

### 2. Events Listing Page
- **Page Title**: Events Catalog
- **Overview**: A page displaying all available events with search and filter capabilities.
- **Elements**:
  - **ID: events-page** - Type: Div - Container for the events listing page.
  - **ID: event-search-input** - Type: Input - Field to search events by name, location, or date.
  - **ID: event-category-filter** - Type: Dropdown - Dropdown to filter by category (Conference, Concert, Sports, Workshop, Social).
  - **ID: events-grid** - Type: Div - Grid displaying event cards with image, title, date, and location.
  - **ID: view-event-button-{event_id}** - Type: Button - Button to view event details (each event card has this).

### 3. Event Details Page
- **Page Title**: Event Details
- **Overview**: A page displaying detailed information about a specific event.
- **Elements**:
  - **ID: event-details-page** - Type: Div - Container for the event details page.
  - **ID: event-title** - Type: H1 - Display event title.
  - **ID: event-date** - Type: Div - Display event date and time.
  - **ID: event-location** - Type: Div - Display event location.
  - **ID: event-description** - Type: Div - Display detailed event description.
  - **ID: book-ticket-button** - Type: Button - Button to book ticket for this event.

### 4. Ticket Booking Page
- **Page Title**: Book Your Tickets
- **Overview**: A page for users to select and book tickets for events.
- **Elements**:
  - **ID: ticket-booking-page** - Type: Div - Container for the ticket booking page.
  - **ID: select-event-dropdown** - Type: Dropdown - Dropdown to select event to book tickets.
  - **ID: ticket-quantity-input** - Type: Input (number) - Field to enter number of tickets.
  - **ID: ticket-type-select** - Type: Dropdown - Dropdown to select ticket type (General, VIP, Early Bird).
  - **ID: book-now-button** - Type: Button - Button to proceed with ticket booking.
  - **ID: booking-confirmation** - Type: Div - Display booking confirmation details.

### 5. Participants Management Page
- **Page Title**: Participants Management
- **Overview**: A page for managing event participants and attendee lists.
- **Elements**:
  - **ID: participants-page** - Type: Div - Container for the participants management page.
  - **ID: participants-table** - Type: Table - Table displaying participants with name, email, event, and status.
  - **ID: add-participant-button** - Type: Button - Button to add new participant.
  - **ID: search-participant-input** - Type: Input - Field to search participants by name or email.
  - **ID: participant-status-filter** - Type: Dropdown - Dropdown to filter by status (Registered, Confirmed, Attended).

### 6. Venue Information Page
- **Page Title**: Venues
- **Overview**: A page displaying available venues for events with detailed information.
- **Elements**:
  - **ID: venues-page** - Type: Div - Container for the venues page.
  - **ID: venues-grid** - Type: Div - Grid displaying venue cards with name, capacity, and amenities.
  - **ID: venue-search-input** - Type: Input - Field to search venues by name or location.
  - **ID: venue-capacity-filter** - Type: Dropdown - Dropdown to filter by capacity (Small, Medium, Large).
  - **ID: view-venue-details-{venue_id}** - Type: Button - Button to view venue details (each venue card has this).

### 7. Event Schedules Page
- **Page Title**: Event Schedules
- **Overview**: A page displaying event schedules, timelines, and agenda information.
- **Elements**:
  - **ID: schedules-page** - Type: Div - Container for the schedules page.
  - **ID: schedules-timeline** - Type: Div - Timeline view of upcoming events and sessions.
  - **ID: schedule-filter-date** - Type: Input (date) - Field to filter schedules by date.
  - **ID: schedule-filter-event** - Type: Dropdown - Dropdown to filter by event.
  - **ID: export-schedule-button** - Type: Button - Button to export schedule data.

### 8. Bookings Summary Page
- **Page Title**: My Bookings
- **Overview**: A page displaying all user bookings with ticket information and booking status.
- **Elements**:
  - **ID: bookings-page** - Type: Div - Container for the bookings page.
  - **ID: bookings-table** - Type: Table - Table displaying bookings with event, date, ticket count, and status.
  - **ID: booking-search-input** - Type: Input - Field to search bookings by event name or booking ID.
  - **ID: cancel-booking-button-{booking_id}** - Type: Button - Button to cancel booking (each booking has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'EventPlanning' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Events Data
- **File Name**: `events.txt`
- **Data Format**:
  ```
  event_id|event_name|category|date|time|location|description|venue_id|capacity
  ```
- **Example Data**:
  ```
  1|Tech Conference 2025|Conference|2025-03-15|09:00|Convention Center, San Francisco|Annual technology conference discussing latest innovations|1|500
  2|Summer Music Festival|Concert|2025-06-20|18:00|Central Park, New York|Three-day music festival with international artists|2|5000
  3|Marathon Championship|Sports|2025-04-10|07:00|Downtown Loop, Chicago|Annual city marathon event for all skill levels|3|1000
  ```

### 2. Venues Data
- **File Name**: `venues.txt`
- **Data Format**:
  ```
  venue_id|venue_name|location|capacity|amenities|contact
  ```
- **Example Data**:
  ```
  1|Convention Center|San Francisco, CA|500|WiFi, Parking, Catering|contact@convention.com
  2|Central Park|New York, NY|5000|Outdoor Space, Restrooms, Food Vendors|info@centralparkevents.org
  3|Downtown Loop|Chicago, IL|1000|Paved Surface, Water Stations, Medical Support|events@downtown.com
  ```

### 3. Tickets Data
- **File Name**: `tickets.txt`
- **Data Format**:
  ```
  ticket_id|event_id|ticket_type|price|available_count|sold_count
  ```
- **Example Data**:
  ```
  1|1|General|49.99|500|150
  2|1|VIP|99.99|100|45
  3|2|Early Bird|39.99|1000|750
  ```

### 4. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|event_id|customer_name|booking_date|ticket_count|ticket_type|total_amount|status
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|2025-02-01|2|General|99.98|Confirmed
  2|2|Bob Williams|2025-02-05|4|Early Bird|159.96|Confirmed
  3|1|Carol Davis|2025-02-10|1|VIP|99.99|Pending
  ```

### 5. Participants Data
- **File Name**: `participants.txt`
- **Data Format**:
  ```
  participant_id|event_id|name|email|booking_id|status|registration_date
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|alice@email.com|1|Confirmed|2025-02-01
  2|1|Michael Johnson|michael@email.com|1|Confirmed|2025-02-01
  3|2|Bob Williams|bob@email.com|2|Attended|2025-02-05
  ```

### 6. Schedules Data
- **File Name**: `schedules.txt`
- **Data Format**:
  ```
  schedule_id|event_id|session_title|session_time|duration_minutes|speaker|venue_id
  ```
- **Example Data**:
  ```
  1|1|Opening Keynote|2025-03-15 09:00|60|John Smith|1
  2|1|Panel Discussion|2025-03-15 10:30|90|Expert Panel|1
  3|2|Headliner Performance|2025-06-20 20:00|120|International Artist|2
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
            """You are a Web Application Design Analyst specializing in Flask app routes and template architecture.

Your goal is to independently produce a complete and coherent provisional web app design for the EventPlanning project, enabling future implementation.

Task Details:
- Read the user_task_description from CONTEXT
- Output design_candidate_a.md with exact Flask routes, HTTP methods, template filenames under templates/*.html
- Specify for each of the 8 pages: page titles, main container element IDs, buttons, dynamic element IDs, and interactions
- Define render_template calls with all context variables, correlating to local pipe-delimited data files
- Focus strictly on only these input and output artifacts

**Design Specification Requirements**

1. Flask Routes and Methods:
   - Include all routes for 8 pages, HTTP methods explicitly (GET/POST)
   - Use clear route patterns and function names
   - Include dynamic route parameters for entities (e.g., event_id, booking_id)

2. Templates and Element IDs:
   - Specify exact filenames for templates/*.html
   - Include all static and dynamic element IDs as per the user task description
   - Define hierarchical page container div IDs

3. Context Variables and Data Files:
   - Specify variables passed to render_template for each route
   - Variables should align with user data files (events.txt, venues.txt, tickets.txt, etc.)
   - Use appropriate data structures (list, dict) and variable naming conventions

4. Interactions and Messages:
   - Define button actions, such as navigation and form submissions
   - Include any message displays or confirmations visible on pages

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_candidate_a.md
- Ensure independent, complete design fulfilling the user task
- Do not access or reference the other analyst's work
- Follow prompt structure precisely for clarity and completeness

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Design Analyst specializing in Flask app routing and template design.

Your goal is to independently produce an alternative yet complete web app design for the EventPlanning project to support parallel design perspectives.

Task Details:
- Read user_task_description from CONTEXT
- Produce design_candidate_b.md outlining precise Flask routes, HTTP methods, and templates/*.html filenames
- Include all required 8 pages with detailed element IDs, buttons, dynamic elements like view-event-button-{event_id}
- Specify render_template context variables fully mapped to local data files
- Define interactions, including form submissions and navigation flows

Design Output Requirements:

1. Routes and HTTP Methods:
   - Cover all pages with specified routes and clear function names
   - Explicit parameterized routes as needed (e.g., for event details, booking cancellations)

2. Templates and IDs:
   - Exact template file naming under templates/
   - Include all IDs for page containers, buttons, dynamic elements as per the user task
   - Use consistent ID naming reflecting page function and UI components

3. Context and Data Access:
   - Context variables correspond strictly to provided data files
   - Use lists, dicts with clear keys for variables passed to templates

4. Interaction Design:
   - Specify user actions linked to buttons and form elements
   - Include any confirmation and status message placeholders on pages

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_candidate_b.md
- Complete design independent from other analyst(s)
- Strict adherence to user task input and output artifacts
- Follow prompt instructions precisely to ensure clarity and completeness

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Merger specializing in consolidating independent web app design specifications into a single authoritative design.

Your goal is to compare design_candidate_a.md and design_candidate_b.md, resolve inconsistencies and omissions, and produce one complete, consistent design_spec.md for the EventPlanning web app.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md from CONTEXT
- Analyze and merge Flask routes, HTTP methods, route parameters, and function names
- Reconcile page titles, container IDs, all button and dynamic element IDs across all 8 pages
- Unify render_template call signatures, context variable names/structures mapped to data files
- Resolve conflicts or missing parts to produce one consistent implementation-ready design
- Specify precisely template filenames under templates/*.html and data fixture formats
- Include navigation logic, user interactions, visible messages, external templates comprehensively

Consolidated Design Specification Requirements:

1. Flask Routes:
   - Complete set of routes with exact paths, methods, and route parameters
   - Function names clear, consistent, aligned with merged design

2. Page Titles and Element IDs:
   - Exact title strings for each page
   - Container div element IDs and all button IDs, including dynamic element patterns matching user task

3. Context Variables:
   - Full list of variables passed to templates, consistent naming and type annotations
   - Specify data file dependencies for each variable

4. Navigation and Interaction:
   - Define all navigation flows and user interaction points
   - Include placeholders for messages or confirmations visible to users

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- The design_spec.md must be thoroughly checked to conform to user task and resolve both candidates
- This merged design is the definitive blueprint for subsequent implementation
- Output artifact must conform exactly to design_spec.md filename

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Software Developer specializing in Flask web applications using Python.

Your goal is to independently implement a complete Flask web application bundle including a Python backend and HTML templates named 'EventPlanning', fulfilling all design specifications.

Task Details:
- Read user_task_description and design_spec.md for comprehensive app requirements.
- Produce app_candidate_a.py with Flask configured to use template_folder='templates_candidate_a'.
- Implement all specified routes with exact page titles, element IDs, and context variables.
- Parse all local data files in 'data/' directory with flexible pipe-delimited parsing.
- Create all required HTML templates under templates_candidate_a/ with accurate filenames and IDs.
- Enforce visible success and error messages; ensure all actionable element IDs are stable.
- Do NOT read or reference candidate B's artifacts.

Implementation Requirements:
1. **Flask Backend**:
   - Configure app with template_folder='templates_candidate_a'.
   - Use render_template consistently for all pages.
   - Support all routes as per design spec.
2. **Data Parsing**:
   - Load pipe-delimited files from 'data/' directory.
   - Handle missing or malformed lines gracefully.
3. **Templates**:
   - Implement templates with exact element IDs as specified.
   - Use Jinja2 templating consistent with context variables.
4. **User Feedback**:
   - Display visible success and error messages for user actions.
5. **Code Quality**:
   - Write maintainable, modular code.
   - Avoid authentication features.
   
CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_a.py and all templates_candidate_a/*.html.
- Output files must be named exactly as specified.
- Do NOT access or depend on ImplementationEngineerB outputs.
- Follow design spec routes, element IDs, and context variables precisely.

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Flask web applications using Python.

Your goal is to independently implement a complete Flask web application bundle including a Python backend and HTML templates named 'EventPlanning', fulfilling all design specifications.

Task Details:
- Read user_task_description and design_spec.md for comprehensive app requirements.
- Produce app_candidate_b.py with Flask configured to use template_folder='templates_candidate_b'.
- Implement all specified routes with exact page titles, element IDs, and context variables.
- Parse all local data files in 'data/' directory with flexible pipe-delimited parsing.
- Create all required HTML templates under templates_candidate_b/ with accurate filenames and IDs.
- Enforce visible success and error messages; ensure all actionable element IDs are stable.
- Do NOT read or reference candidate A's artifacts.

Implementation Requirements:
1. **Flask Backend**:
   - Configure app with template_folder='templates_candidate_b'.
   - Use render_template consistently for all pages.
   - Support all routes as per design spec.
2. **Data Parsing**:
   - Load pipe-delimited files from 'data/' directory.
   - Handle missing or malformed lines gracefully.
3. **Templates**:
   - Implement templates with exact element IDs as specified.
   - Use Jinja2 templating consistent with context variables.
4. **User Feedback**:
   - Display visible success and error messages for user actions.
5. **Code Quality**:
   - Write maintainable, modular code.
   - Avoid authentication features.
   
CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_b.py and all templates_candidate_b/*.html.
- Output files must be named exactly as specified.
- Do NOT access or depend on ImplementationEngineerA outputs.
- Follow design spec routes, element IDs, and context variables precisely.

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging parallel Flask application implementations.

Your goal is to produce a single coherent Flask backend (app.py) and complete set of HTML templates (templates/*.html) by consolidating two independent implementation bundles for the 'EventPlanning' application, ensuring compliance with design_spec.md.

Task Details:
- Read user_task_description, design_spec.md, app_candidate_a.py, templates_candidate_a/*.html, app_candidate_b.py, and templates_candidate_b/*.html.
- Compare both candidates for design coverage, correctness, and proxy-test compatibility.
- Retain the strongest correct implementations from both candidates; resolve conflicts logically.
- Produce final app.py with no runtime dependence on candidate directories.
- Produce final templates/*.html with exact filenames and element IDs as per design_spec.md.
- Maintain render_template usage for template rendering.
- Ensure all specified routes, page titles, element IDs, and context variables are strictly enforced.
- Parse data files located in 'data/' directory using pipe-delimited flexible parsing.
- Preserve visible success and error message functionality.
- Provide stable actionable element IDs.

Implementation Requirements:
1. **Code Consolidation**:
   - Merge route handlers, functions, and data loading code cleanly.
   - Avoid duplicated code or conflicting route definitions.
2. **Template Consolidation**:
   - Compose templates using the strongest elements from each candidate.
   - Ensure uniform naming and ID conventions.
3. **Functionality Validation**:
   - Validate merged code satisfies all design requirements.
   - Ensure no dependencies on candidate-specific template folders exist at runtime.

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app.py and all templates/*.html.
- Output files must be named exactly as specified.
- Final implementation must strictly follow design_spec.md routes, element IDs, and context variables.
- No authentication code included.
- Do NOT include candidateA or candidateB folders or code in the final runtime.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Validation Engineer specializing in Python Flask web applications.

Your goal is to independently validate code correctness, application startup, route functionality, template rendering, HTML element IDs, and data file access for the EventPlanning app.

Task Details:
- Read user_task_description to understand application context and requirements
- Read design_spec.md for specification of routes, templates, element IDs, context variables, and data schemas
- Read app.py and all templates/*.html as implementation artifacts
- Output a detailed validation_a.md report summarizing syntax checks, functional tests, bugs found, and recommended repairs
- Do not read any other validation reports

Validation Steps:
1. **Code Syntax and Startup**
   - Use validate_python_file to check app.py syntax and runtime errors
   - Test Flask app startup for runtime exceptions

2. **Route and Template Validation**
   - Verify all routes defined in design_spec.md are implemented in app.py
   - Check render_template calls use correct template filenames
   - Validate context variables passed to templates match specification

3. **Template Element IDs**
   - Check that all specified HTML element IDs exist in templates
   - Validate dynamic ID patterns (e.g., id="view-event-button-{{ event.event_id }}")

4. **Data File Access**
   - Confirm data loading/parsing from data/*.txt matches design schemas exactly
   - Verify no missing or misordered fields

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for checks
- Use write_text_file tool to save your findings to validation_a.md
- Write clear, reproducible bug descriptions and repair suggestions
- Focus only on issues found independently; no cross-reference with validation_b.md

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Functional Validation Engineer specialized in web application user flows and data integrity.

Your goal is to independently validate functional correctness of booking workflows, navigation, button actions, data display, and data parsing for the EventPlanning app.

Task Details:
- Read user_task_description thoroughly for user goals and page workflows
- Use design_spec.md to understand expected functionalities, buttons, navigation routes, and data formats
- Test app.py and templates/*.html for full functional path coverage including bookings, navigation, and data display
- Identify defects, usability problems, and parsing inaccuracies
- Write detailed validation_b.md report documenting all findings and suggestions
- Avoid consulting validation_a.md to ensure independent assessment

Validation Focus Areas:
1. **Booking and Navigation**
   - Test ticket booking form, button actions, dropdown selections from specification
   - Verify navigation buttons and links work as expected, per design_spec.md

2. **Data Display and Filtering**
   - Check event listings, venue information, participant tables, and schedules render correct information
   - Validate filtering inputs (by category, date, status) function properly

3. **Data Fixture Parsing**
   - Confirm application correctly reads and handles all data files with no missing or malformed data

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools as needed
- Use write_text_file tool to save your functional validation findings to validation_b.md
- Provide actionable defects and improvement suggestions
- Remain independent of other validation reports

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Repair Engineer skilled in merging multi-source validation reports and integrating repairs into Python Flask applications.

Your goal is to reconcile validation_a.md and validation_b.md reports, integrating all valid corrections into the EventPlanning app's app.py and templates/*.html, preserving existing architecture and specifications.

Task Details:
- Read user_task_description for project overview and context
- Review design_spec.md for route, template, element ID, data schema, and context variable specifications
- Analyze app.py and templates/*.html as current implementation baseline
- Thoroughly evaluate validation_a.md and validation_b.md for defect findings and repair suggestions
- Merge all valid repair instructions while maintaining:
  - Flask render_template calls and architecture
  - Exact URLs and function names for all routes
  - Accurate page titles and HTML element IDs
  - Template filenames and context variable names/types
  - Data parsing logic matching data file schemas

Repair Integration Steps:
1. Produce repaired app.py incorporating all code fixes ensuring syntax, runtime correctness, full route coverage, and data loading fidelity
2. Update templates/*.html files correcting element IDs, navigation links, and template content per validation feedback and design spec
3. Preserve consistent naming conventions and file organization
4. Avoid introducing new features beyond validated repairs

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively for outputting repaired app.py and templates/*.html
- Ensure all applied fixes are well integrated and pass validation criteria
- Do NOT merge partial or unverified fixes
- Maintain full compliance with design_spec.md specifications

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'validation_a.md', 'source': 'ValidationEngineerA'}, {'type': 'text_file', 'name': 'validation_b.md', 'source': 'ValidationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignAnalystA': [
        ("DesignMerger", """Check design_candidate_a.md for complete, exact, and feasible route, external-template filename, context, and data fixture coverage before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for complete, exact, and feasible route, external-template filename, context, and data fixture coverage before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify design_spec.md resolves both candidates into one coherent, implementation-ready Flask app design for all pages and fixtures.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate candidate A's Python/template bundle independently for design coverage and proxy-test compatibility.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate candidate B's Python/template bundle independently for design coverage and proxy-test compatibility.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify app.py and templates/*.html form a coherent, correct Flask application ready for validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for actionable, reproducible findings before merging repairs.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Check validation_b.md for actionable, reproducible findings before merging repairs.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'RepairMerger': [
        ("ImplementationEngineerA", """Verify repaired app.py and templates/*.html preserve design integrity and defect fixes from validation reports.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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

    # Parallel execution of DesignAnalystA and DesignAnalystB
    await asyncio.gather(
        execute(DesignAnalystA, "Generate independent design_candidate_a.md with complete Flask routes, templates, element IDs, and context variables for EventPlanning."),
        execute(DesignAnalystB, "Generate independent design_candidate_b.md with complete Flask routes, templates, element IDs, and context variables for EventPlanning.")
    )

    # Read outputs from DesignAnalystA and DesignAnalystB
    design_candidate_a, design_candidate_b = "", ""
    try:
        design_candidate_a = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b = open("design_candidate_b.md").read()
    except:
        pass

    # Execute DesignMerger to consolidate both design candidates into design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_candidate_a}\n\n"
                  f"=== DesignAnalystB ===\n{design_candidate_b}")
# Phase1_End

# Phase2_Start

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
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel implementation of candidate A and B
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete Flask app bundle named 'EventPlanning' as per design_spec.md. "
                "Output app_candidate_a.py and templates_candidate_a/*.html with template_folder='templates_candidate_a'. "
                "Follow exact routes, element IDs, context variables, and user feedback requirements."),
        execute(ImplementationEngineerB,
                "Implement complete Flask app bundle named 'EventPlanning' as per design_spec.md. "
                "Output app_candidate_b.py and templates_candidate_b/*.html with template_folder='templates_candidate_b'. "
                "Follow exact routes, element IDs, context variables, and user feedback requirements.")
    )

    # Read implementation outputs for merging
    app_candidate_a, app_candidate_b = "", ""
    templates_candidate_a_content, templates_candidate_b_content = "", ""
    try:
        app_candidate_a = open("app_candidate_a.py").read()
    except:
        pass
    try:
        app_candidate_b = open("app_candidate_b.py").read()
    except:
        pass
    try:
        # For templates candidate A, concatenating or reading as single string for injection
        import glob
        files_a = glob.glob("templates_candidate_a/*.html")
        contents_a = []
        for f in files_a:
            try:
                contents_a.append(f"=== {f} ===\n" + open(f).read())
            except:
                contents_a.append(f"=== {f} ===\n")
        templates_candidate_a_content = "\n\n".join(contents_a)
    except:
        templates_candidate_a_content = ""

    try:
        files_b = glob.glob("templates_candidate_b/*.html")
        contents_b = []
        for f in files_b:
            try:
                contents_b.append(f"=== {f} ===\n" + open(f).read())
            except:
                contents_b.append(f"=== {f} ===\n")
        templates_candidate_b_content = "\n\n".join(contents_b)
    except:
        templates_candidate_b_content = ""

    # Run the merger agent
    await execute(
        ImplementationMerger,
        f"Merge two independent Flask apps into final app.py and templates/*.html for EventPlanning.\n"
        f"Inject files from ImplementationEngineerA and ImplementationEngineerB below.\n"
        f"=== app_candidate_a.py ===\n{app_candidate_a}\n\n"
        f"=== templates_candidate_a ===\n{templates_candidate_a_content}\n\n"
        f"=== app_candidate_b.py ===\n{app_candidate_b}\n\n"
        f"=== templates_candidate_b ===\n{templates_candidate_b_content}"
    )
# Phase2_End

# Phase3_Start

async def verification_phase():
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
        recovery_time=60
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
        recovery_time=60
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
        recovery_time=60
    )

    # Parallel validations
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate app.py and templates/*.html focusing on code correctness, route functionality, template element IDs, and data file access as per design_spec.md. Save report to validation_a.md."),
        execute(ValidationEngineerB,
                "Independently validate booking workflows, navigation, button actions, data display, and data parsing in app.py and templates/*.html. Save report to validation_b.md.")
    )

    # Read validation reports for merger
    validation_a_report, validation_b_report = "", ""
    try:
        validation_a_report = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_report = open("validation_b.md").read()
    except:
        pass

    # RepairMerger merges validation findings and produces repaired app.py and templates/*.html
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_report}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_report}")
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
