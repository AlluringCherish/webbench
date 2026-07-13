import asyncio
import sys
import os
import time
import asyncio
import glob
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import essential_modules
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics


def _read_text_artifacts(pattern: str) -> str:
    """Read all matching UTF-8 text artifacts in stable order."""
    sections = []
    for filename in sorted(glob.glob(pattern)):
        path = Path(filename)
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="replace")
            sections.append(f"===== {path.as_posix()} =====\n{content}")
    return "\n\n".join(sections)
from chaos import ChaosController
# 20260713_210029_706258/main_20260713_210029_706258.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent design specifications for RestaurantReservation web app pages and features, then merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA produces a detailed design candidate describing route structure, page elements with exact IDs, titles, and navigation for the required 9 pages; \"\n        \"DesignAnalystB independently produces an alternative but complete design candidate covering the same scope with possibly different UI/UX and structures; \"\n        \"DesignMerger then consolidates these two designs into a single coherent design_spec.md covering Flask routes, page titles, element IDs, data interactions, navigation flows, and file structures under templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in Flask web application design specifications.\n\nYour goal is to create a complete and exact Flask web application design candidate covering all 9 specified pages with detailed route structures, precise page titles, container and element IDs, navigation controls, and data interaction structures.\n\nTask Details:\n- Read user_task_description from CONTEXT.\n- Produce a full design candidate in Markdown format named design_candidate_a.md.\n- Include all specified pages with exact element IDs, page titles, and route paths.\n- Specify template filenames for render_template() calls.\n- Ensure the Dashboard page is the root route ('/') and starting point.\n- Focus on completeness, accuracy, and adherence to user requirements.\n\n**Design Requirements:**\n\n1. **Page Routes and Templates**\n   - Define Flask route paths for each page.\n   - Assign template file names under templates/ directory.\n   - Map each route to its template using render_template().\n\n2. **Page Titles and Container Elements**\n   - Specify exact page titles matching user requirements.\n   - Define container div IDs and all other element IDs exactly as specified.\n   - Include dynamic element IDs with placeholder notation (e.g., view-dish-button-{dish_id}).\n\n3. **Navigation Controls**\n   - Specify buttons or links with IDs and their target routes.\n   - Map navigation flows consistent with the requirements.\n   - Include back buttons or dashboard navigation elements explicitly.\n\n4. **Data Interaction**\n   - Identify data fields relevant to each page for backend interface.\n   - Specify any parameters required in routes (e.g., dish_id in dish details).\n   - Ensure all user input controls have corresponding IDs as specified.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md.\n- Follow exact casing and naming for all element IDs.\n- Maintain clear and organized Markdown formatting.\n- Include all 9 pages fully and accurately.\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in Flask web application design specifications.\n\nYour goal is to independently produce an alternative, complete Flask web application design candidate for the same 9 pages, covering all required routes, exact page titles, element IDs, and navigation, potentially differing in UI/UX or structure.\n\nTask Details:\n- Read user_task_description from CONTEXT.\n- Produce a complete alternative design candidate in Markdown named design_candidate_b.md.\n- Ensure all pages are covered with exact element IDs and page titles matching requirements.\n- Specify Flask route paths with template mapping via render_template().\n- Begin from Dashboard as root page.\n- Focus on independent design, completeness, and correctness.\n\n**Design Tasks:**\n\n1. **Routes and Templates**\n   - Define routes for all 9 pages with specific paths.\n   - Specify template filenames clearly.\n   - Map routes to templates using standard Flask calls.\n\n2. **Page Structure and Elements**\n   - List container and dynamic element IDs exactly.\n   - Include page titles consistent with the user task.\n   - Detail navigation buttons with related link targets.\n\n3. **Navigation and User Interaction**\n   - Define button IDs and their navigation actions.\n   - Use back-to-dashboard and other navigation controls precisely.\n   - Account for dynamic buttons with placeholders for IDs.\n\n4. **Data Parameters and Inputs**\n   - Specify parameters needed for details pages (like dish_id).\n   - Include form elements and input IDs including dropdowns, inputs, and buttons.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save as design_candidate_b.md.\n- Ensure all naming conventions and IDs match the requirements exactly.\n- Maintain clear Markdown formatting with consistent structure.\n- Cover all pages fully.\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Merger specializing in integrating multiple design candidates into one comprehensive and coherent Flask web application specification.\n\nYour goal is to compare design_candidate_a.md and design_candidate_b.md against the user requirements, resolve conflicts, omissions, and inconsistencies, and produce a merged, final design_spec.md that comprehensively covers:\n\n- Flask route definitions and paths for all 9 pages.\n- Exact page titles and container and element IDs.\n- Template file organization under templates/*.html.\n- Navigation flows including buttons, links, back navigation, and dashboard entry.\n- Data interface contracts including input controls, route parameters, and data display IDs.\n\nTask Details:\n- Read user_task_description plus design_candidate_a.md and design_candidate_b.md from CONTEXT.\n- Analyze both design candidates in detail.\n- Resolve any conflicting route paths, element IDs or page titles based on completeness and fidelity to requirements.\n- Merge both designs into a unified design_spec.md with clear sections:\n  - Routes and Templates\n  - Page Titles and Elements\n  - Navigation Flows\n  - Data Interfaces\n- Ensure consistency of naming and structure.\n- Maintain fidelity to user specifications with no omissions.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save merged output as design_spec.md.\n- Follow exact naming conventions and casing for all elements.\n- Provide a thoroughly integrated Markdown document usable as a single source of truth.\n- Cover all pages and features as specified.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for completeness, page coverage, exact element, ID correctness, route feasibility, and consistency with requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for completeness, page coverage, exact element, ID correctness, route feasibility, and consistency with requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete Flask implementations with templates following design_spec.md, merge them into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently write complete Flask app implementations including app_candidate_*.py and candidate isolated templates directories with templates/*.html files as per design_spec.md. \"\n        \"Each implementation must enforce all required route handlers, exact page titles, element IDs, navigation buttons, data processing and local file management as specified. \"\n        \"ImplementationMerger then reads both implementations, resolves conflicts, and produces the final app.py plus a unified templates/ directory with all templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications for restaurant reservation systems.\n\nYour goal is to implement a full Flask application with all required pages, routes, data processing from local text files, and stable, actionable element IDs, isolating templates into a dedicated directory.\n\nTask Details:\n- Read user_task_description and design_spec.md fully for requirements and specifications\n- Produce app_candidate_a.py implementing ALL Flask routes and business logic\n- Isolate and implement all HTML templates in templates_candidate_a/*.html matching exact page titles and element IDs\n- Use local data files in data/ directory for users, menu, reservations, waitlist, and reviews\n- Implement exact navigation buttons with route handling as specified\n\nImplementation Requirements:\n1. **App Structure:**\n   - Use Flask app with standard setup and run statements\n   - Implement root route '/' redirecting to dashboard page\n   - Follow exact function names and route paths from design_spec.md and user_task_description\n\n2. **Data Handling:**\n   - Load from data/*.txt pipe-delimited files\n   - Parse each line carefully with exact field order and create dicts for use in templates\n   - Implement CRUD operations as required for reservations, reviews, waitlist, profile updates\n\n3. **Templates:**\n   - Implement all templates under templates_candidate_a/\n   - Match all specified element IDs (dashboard-page, welcome-message, make-reservation-button, etc.)\n   - Use Jinja2 templating for dynamic elements and loops\n   - Ensure page titles match exactly those specified in requirement document\n\n4. **Navigation:**\n   - Implement all navigation buttons and links with url_for to correct route names\n   - Use redirect for post submissions to appropriate pages\n\nCRITICAL REQUIREMENTS:\n- MUST utilize write_text_file tool to save app_candidate_a.py and all templates in templates_candidate_a/\n- Follow exact routes, naming conventions, and page elements from design_spec.md and user_task_description\n- Do NOT deviate from specified element IDs or route names\n- All data file field orders and parsing must be exact\n- Isolate templates strictly in templates_candidate_a/ directory for integration later\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications for restaurant reservation systems.\n\nYour goal is to implement a full Flask application with all required pages, routes, data processing from local text files, and stable, actionable element IDs, isolating templates into a dedicated directory.\n\nTask Details:\n- Read user_task_description and design_spec.md fully for requirements and specifications\n- Produce app_candidate_b.py implementing ALL Flask routes and business logic\n- Isolate and implement all HTML templates in templates_candidate_b/*.html matching exact page titles and element IDs\n- Use local data files in data/ directory for users, menu, reservations, waitlist, and reviews\n- Implement exact navigation buttons with route handling as specified\n\nImplementation Requirements:\n1. **App Structure:**\n   - Use Flask app with standard setup and run statements\n   - Implement root route '/' redirecting to dashboard page\n   - Follow exact function names and route paths from design_spec.md and user_task_description\n\n2. **Data Handling:**\n   - Load from data/*.txt pipe-delimited files\n   - Parse each line carefully with exact field order and create dicts for use in templates\n   - Implement CRUD operations as required for reservations, reviews, waitlist, profile updates\n\n3. **Templates:**\n   - Implement all templates under templates_candidate_b/\n   - Match all specified element IDs (dashboard-page, welcome-message, make-reservation-button, etc.)\n   - Use Jinja2 templating for dynamic elements and loops\n   - Ensure page titles match exactly those specified in requirement document\n\n4. **Navigation:**\n   - Implement all navigation buttons and links with url_for to correct route names\n   - Use redirect for post submissions to appropriate pages\n\nCRITICAL REQUIREMENTS:\n- MUST utilize write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/\n- Follow exact routes, naming conventions, and page elements from design_spec.md and user_task_description\n- Do NOT deviate from specified element IDs or route names\n- All data file field orders and parsing must be exact\n- Isolate templates strictly in templates_candidate_b/ directory for integration later\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Backend Developer and Integration Specialist with expertise in Flask web applications.\n\nYour goal is to comprehensively compare and merge two independent Flask application implementations and their isolated templates directories into a single unified Flask app and templates directory according to design_spec.md.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_candidate_a.py, app_candidate_b.py, and all templates in templates_candidate_a/ and templates_candidate_b/\n- Merge all Flask routes, handlers, and business logic from both app_candidate_*.py files into one complete app.py\n- Consolidate all templates into a unified templates/ directory, resolving naming conflicts and preserving all required element IDs and page titles\n- Ensure all routes and URLs conform exactly to design_spec.md and user_task_description\n- Maintain data file access and consistent local file management\n- Ensure the final app.py and templates/*.html are fully compatible and ready for deployment behind a web proxy\n\nMerging Guidelines:\n1. Consolidate routes by matching identical endpoints and unify handler logic; choose best implementation to avoid duplication\n2. Carefully merge template files ensuring all required element IDs and dynamic content exist without conflict\n3. Preserve exact filenames and locations as specified for final output (app.py, templates/*.html)\n4. Validate that no required route, page title, or element ID is missing after merging\n5. Maintain code quality and readability; eliminate redundant code\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to output final app.py and all templates into templates/\n- Final implementation must exactly match all page titles, routes, element IDs, and navigation buttons specified in design_spec.md and user_task_description\n- Ensure merged application is fully functional and consistent\n- Do NOT add or remove functional features beyond design specification\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate app_candidate_a.py and isolated templates for completeness, route alignment, code quality, and faithful adherence to design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate app_candidate_b.py and isolated templates for completeness, route alignment, code quality, and faithful adherence to design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Conduct two independent validation passes and merge their repair suggestions into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate the final app.py and templates/*.html including syntax, runtime, route correctness, UI element presence, data interaction correctness with local text files, and user navigation. They produce validation reports validation_a.md and validation_b.md respectively. \"\n        \"RepairMerger then reviews both reports, applies valid fixes or improvements, and produces the final approved app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in comprehensive validation of Python Flask web applications.\n\nYour goal is to perform a thorough independent validation of the web application source code and templates ensuring syntactic correctness, runtime stability, and full compliance with design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md for context and expected features\n- Validate app.py source code and templates/*.html files for compliance, correctness, and completeness per design_spec.md\n- Produce a detailed validation report validation_a.md capturing all findings and actionable recommendations\n\nValidation Scope:\n- Syntax and runtime validation of app.py using code validation tools\n- Confirm existence and correctness of all Flask routes as per design_spec.md\n- Validate page titles and presence of all required element IDs in templates\n- Check data file interactions for correct reading/writing with local text files under /data directory\n- Verify user navigation flows and URL stability without authentication\n\nValidation Steps:\n1. Run syntax and runtime checks on app.py using validate_python_file tool\n2. Manually inspect or programmatically parse app.py and HTML templates for route and element verification\n3. Compare actual implementation against design_spec.md page titles, element IDs, and route definitions\n4. Test data interaction points ensuring correct file usage and formats aligned with design_spec.md\n5. Verify that no authentication requirements exist and URLs behave consistently across flows\n\nCRITICAL SUCCESS CRITERIA:\n- Use validate_python_file and execute_python_code to confirm code correctness\n- Write detailed validation findings with clear, reproducible issues in validation_a.md\n- Report must cover all aspects described in Task Details and Validation Scope\n- Use write_text_file tool to save validation_a.md\n- Output file: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"validation_a.md\"}]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in user flow validation and data persistence testing for Python Flask web applications.\n\nYour goal is to independently validate critical user workflows and data handling processes ensuring seamless reservation, waitlist, review, and profile management functionality.\n\nTask Details:\n- Read user_task_description and design_spec.md for relevant feature descriptions and data schemas\n- Validate app.py and templates/*.html focusing on reservation workflows, waitlist correctness, review submissions, and data persistence in text files\n- Produce a detailed validation report validation_b.md with findings, issues, and suggested fixes\n\nValidation Scope:\n- Test user reservation flow including making, viewing, and cancelling reservations\n- Verify waitlist functionality including joining, position tracking, status updates\n- Confirm review writing, listing, and storage behaves per design with correct data file updates\n- Inspect profile update and dashboard navigation flows\n- Ensure data file reads/writes conform to defined formats and fields in design_spec.md\n\nValidation Steps:\n1. Inspect code and templates to confirm forms, inputs, and navigation for user workflows\n2. Analyze data file interactions for accuracy and robustness during user actions\n3. Validate feedback correctness and data consistency after simulated user scenarios\n4. Document discovered issues with steps to reproduce and suggested remediation\n\nCRITICAL SUCCESS CRITERIA:\n- Use validate_python_file and execute_python_code as needed for runtime validation\n- Write clear, concise, actionable validation report validation_b.md\n- Focus on user experience, data durability, and workflow integrity across features\n- Use write_text_file tool to save validation_b.md\n- Output file: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"validation_b.md\"}]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in code merging and application stability enhancement for Python Flask web applications.\n\nYour goal is to merge independent validation reports, apply necessary corrections or improvements to app.py and templates/*.html, ensure compliance with design specifications, and produce the final production-ready codebases.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md\n- Analyze validation reports for findings and recommended fixes or improvements\n- Apply all valid and relevant fixes to app.py and templates/*.html ensuring full compliance with design_spec.md\n- Confirm no regressions by adhering to design specs in final versions\n- Produce final verified app.py and templates/*.html ready for deployment\n\nMerging and Repair Process:\n1. Combine and reconcile findings from validation_a.md and validation_b.md\n2. Prioritize fixes that improve correctness, consistency, and feature completeness\n3. Update code and templates accordingly, keeping original structure unless fixes require enhancements\n4. Thoroughly check alignment with design_spec.md after applying fixes\n5. Prepare final clean and stable versions of app.py and templates/*.html\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool to save corrected app.py and all updated templates/*.html files\n- Ensure final outputs fully conform to design_spec.md specifications\n- Do NOT introduce new features beyond validation fixes\n- Maintain overall code quality and readability\n- Output files: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Validate validation_a.md for clear, actionable, and reproducible findings and recommendations aligned with design_spec.md before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Validate validation_b.md for clear, actionable, and reproducible findings and recommendations aligned with design_spec.md before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'RestaurantReservation' Web Application

## 1. Objective
Develop a comprehensive web application named 'RestaurantReservation' using Python, with data managed through local text files. The application enables users to browse restaurant menus, make table reservations, write reviews, check waitlist status, and manage their dining history. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'RestaurantReservation' application is Python.

## 3. Page Design

The 'RestaurantReservation' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Restaurant Dashboard
- **Overview**: The main hub displaying featured dishes, upcoming reservations, and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying username.
  - **ID: make-reservation-button** - Type: Button - Button to navigate to reservation page.
  - **ID: view-menu-button** - Type: Button - Button to navigate to menu page.
  - **ID: back-to-dashboard** - Type: Button - Button to refresh dashboard.
  - **ID: my-reservations-button** - Type: Button - Button to navigate to my reservations page.
  - **ID: my-reviews-button** - Type: Button - Button to navigate to my reviews page.
  - **ID: waitlist-button** - Type: Button - Button to navigate to waitlist page.
  - **ID: profile-button** - Type: Button - Button to navigate to user profile page.

### 2. Menu Page
- **Page Title**: Restaurant Menu
- **Overview**: A page displaying the restaurant menu with categories and filtering.
- **Elements**:
  - **ID: menu-page** - Type: Div - Container for the menu page.
  - **ID: menu-grid** - Type: Div - Grid displaying dish cards with image, name, price, description.
  - **ID: view-dish-button-{dish_id}** - Type: Button - Button to view dish details (each card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Dish Details Page
- **Page Title**: Dish Details
- **Overview**: A page displaying detailed information about a specific dish.
- **Elements**:
  - **ID: dish-details-page** - Type: Div - Container for the dish details page.
  - **ID: dish-name** - Type: H1 - Display dish name.
  - **ID: dish-price** - Type: Div - Display dish price.
  - **ID: back-to-menu** - Type: Button - Button to navigate back to menu.

### 4. Make Reservation Page
- **Page Title**: Make Reservation
- **Overview**: A page for users to make a table reservation.
- **Elements**:
  - **ID: reservation-page** - Type: Div - Container for the reservation page.
  - **ID: guest-name** - Type: Input - Field to input guest name.
  - **ID: party-size** - Type: Dropdown - Dropdown to select party size (1-10).
  - **ID: reservation-date** - Type: Input (date) - Field to select reservation date.
  - **ID: submit-reservation-button** - Type: Button - Button to submit reservation.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. My Reservations Page
- **Page Title**: My Reservations
- **Overview**: A page displaying all reservations made by the user.
- **Elements**:
  - **ID: my-reservations-page** - Type: Div - Container for the my reservations page.
  - **ID: reservations-table** - Type: Table - Table displaying reservations with date, time, party size, status.
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each upcoming reservation has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Waitlist Page
- **Page Title**: Waitlist
- **Overview**: A page for users to join the waitlist and check their position.
- **Elements**:
  - **ID: waitlist-page** - Type: Div - Container for the waitlist page.
  - **ID: waitlist-party-size** - Type: Dropdown - Dropdown to select party size.
  - **ID: join-waitlist-button** - Type: Button - Button to join waitlist.
  - **ID: user-position** - Type: Div - Display user's current position in waitlist.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Overview**: A page displaying all reviews written by the user.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of reviews with dish name, rating, review text.
  - **ID: write-new-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write Review
- **Overview**: A page for users to write a review for a dish.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: select-dish** - Type: Dropdown - Dropdown to select dish to review.
  - **ID: rating-input** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.
  - **ID: back-to-reviews** - Type: Button - Button to navigate back to my reviews.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'RestaurantReservation' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|full_name
  ```
- **Example Data**:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. Menu Items Data
- **File Name**: `menu.txt`
- **Data Format**:
  ```
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
  ```
- **Example Data**:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
  ```
- **Example Data**:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. Waitlist Data
- **File Name**: `waitlist.txt`
- **Data Format**:
  ```
  waitlist_id|username|party_size|join_time|status
  ```
- **Example Data**:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|username|dish_id|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

All files will be saved in the `data` directory to ensure organization and easy access. The format uses a pipe (`|`) delimiter for better readability and parsing.
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
            """You are a Software Designer specializing in Flask web application design specifications.

Your goal is to create a complete and exact Flask web application design candidate covering all 9 specified pages with detailed route structures, precise page titles, container and element IDs, navigation controls, and data interaction structures.

Task Details:
- Read user_task_description from CONTEXT.
- Produce a full design candidate in Markdown format named design_candidate_a.md.
- Include all specified pages with exact element IDs, page titles, and route paths.
- Specify template filenames for render_template() calls.
- Ensure the Dashboard page is the root route ('/') and starting point.
- Focus on completeness, accuracy, and adherence to user requirements.

**Design Requirements:**

1. **Page Routes and Templates**
   - Define Flask route paths for each page.
   - Assign template file names under templates/ directory.
   - Map each route to its template using render_template().

2. **Page Titles and Container Elements**
   - Specify exact page titles matching user requirements.
   - Define container div IDs and all other element IDs exactly as specified.
   - Include dynamic element IDs with placeholder notation (e.g., view-dish-button-{dish_id}).

3. **Navigation Controls**
   - Specify buttons or links with IDs and their target routes.
   - Map navigation flows consistent with the requirements.
   - Include back buttons or dashboard navigation elements explicitly.

4. **Data Interaction**
   - Identify data fields relevant to each page for backend interface.
   - Specify any parameters required in routes (e.g., dish_id in dish details).
   - Ensure all user input controls have corresponding IDs as specified.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md.
- Follow exact casing and naming for all element IDs.
- Maintain clear and organized Markdown formatting.
- Include all 9 pages fully and accurately.

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Designer specializing in Flask web application design specifications.

Your goal is to independently produce an alternative, complete Flask web application design candidate for the same 9 pages, covering all required routes, exact page titles, element IDs, and navigation, potentially differing in UI/UX or structure.

Task Details:
- Read user_task_description from CONTEXT.
- Produce a complete alternative design candidate in Markdown named design_candidate_b.md.
- Ensure all pages are covered with exact element IDs and page titles matching requirements.
- Specify Flask route paths with template mapping via render_template().
- Begin from Dashboard as root page.
- Focus on independent design, completeness, and correctness.

**Design Tasks:**

1. **Routes and Templates**
   - Define routes for all 9 pages with specific paths.
   - Specify template filenames clearly.
   - Map routes to templates using standard Flask calls.

2. **Page Structure and Elements**
   - List container and dynamic element IDs exactly.
   - Include page titles consistent with the user task.
   - Detail navigation buttons with related link targets.

3. **Navigation and User Interaction**
   - Define button IDs and their navigation actions.
   - Use back-to-dashboard and other navigation controls precisely.
   - Account for dynamic buttons with placeholders for IDs.

4. **Data Parameters and Inputs**
   - Specify parameters needed for details pages (like dish_id).
   - Include form elements and input IDs including dropdowns, inputs, and buttons.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save as design_candidate_b.md.
- Ensure all naming conventions and IDs match the requirements exactly.
- Maintain clear Markdown formatting with consistent structure.
- Cover all pages fully.

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Merger specializing in integrating multiple design candidates into one comprehensive and coherent Flask web application specification.

Your goal is to compare design_candidate_a.md and design_candidate_b.md against the user requirements, resolve conflicts, omissions, and inconsistencies, and produce a merged, final design_spec.md that comprehensively covers:

- Flask route definitions and paths for all 9 pages.
- Exact page titles and container and element IDs.
- Template file organization under templates/*.html.
- Navigation flows including buttons, links, back navigation, and dashboard entry.
- Data interface contracts including input controls, route parameters, and data display IDs.

Task Details:
- Read user_task_description plus design_candidate_a.md and design_candidate_b.md from CONTEXT.
- Analyze both design candidates in detail.
- Resolve any conflicting route paths, element IDs or page titles based on completeness and fidelity to requirements.
- Merge both designs into a unified design_spec.md with clear sections:
  - Routes and Templates
  - Page Titles and Elements
  - Navigation Flows
  - Data Interfaces
- Ensure consistency of naming and structure.
- Maintain fidelity to user specifications with no omissions.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save merged output as design_spec.md.
- Follow exact naming conventions and casing for all elements.
- Provide a thoroughly integrated Markdown document usable as a single source of truth.
- Cover all pages and features as specified.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications for restaurant reservation systems.

Your goal is to implement a full Flask application with all required pages, routes, data processing from local text files, and stable, actionable element IDs, isolating templates into a dedicated directory.

Task Details:
- Read user_task_description and design_spec.md fully for requirements and specifications
- Produce app_candidate_a.py implementing ALL Flask routes and business logic
- Isolate and implement all HTML templates in templates_candidate_a/*.html matching exact page titles and element IDs
- Use local data files in data/ directory for users, menu, reservations, waitlist, and reviews
- Implement exact navigation buttons with route handling as specified

Implementation Requirements:
1. **App Structure:**
   - Use Flask app with standard setup and run statements
   - Implement root route '/' redirecting to dashboard page
   - Follow exact function names and route paths from design_spec.md and user_task_description

2. **Data Handling:**
   - Load from data/*.txt pipe-delimited files
   - Parse each line carefully with exact field order and create dicts for use in templates
   - Implement CRUD operations as required for reservations, reviews, waitlist, profile updates

3. **Templates:**
   - Implement all templates under templates_candidate_a/
   - Match all specified element IDs (dashboard-page, welcome-message, make-reservation-button, etc.)
   - Use Jinja2 templating for dynamic elements and loops
   - Ensure page titles match exactly those specified in requirement document

4. **Navigation:**
   - Implement all navigation buttons and links with url_for to correct route names
   - Use redirect for post submissions to appropriate pages

CRITICAL REQUIREMENTS:
- MUST utilize write_text_file tool to save app_candidate_a.py and all templates in templates_candidate_a/
- Follow exact routes, naming conventions, and page elements from design_spec.md and user_task_description
- Do NOT deviate from specified element IDs or route names
- All data file field orders and parsing must be exact
- Isolate templates strictly in templates_candidate_a/ directory for integration later

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications for restaurant reservation systems.

Your goal is to implement a full Flask application with all required pages, routes, data processing from local text files, and stable, actionable element IDs, isolating templates into a dedicated directory.

Task Details:
- Read user_task_description and design_spec.md fully for requirements and specifications
- Produce app_candidate_b.py implementing ALL Flask routes and business logic
- Isolate and implement all HTML templates in templates_candidate_b/*.html matching exact page titles and element IDs
- Use local data files in data/ directory for users, menu, reservations, waitlist, and reviews
- Implement exact navigation buttons with route handling as specified

Implementation Requirements:
1. **App Structure:**
   - Use Flask app with standard setup and run statements
   - Implement root route '/' redirecting to dashboard page
   - Follow exact function names and route paths from design_spec.md and user_task_description

2. **Data Handling:**
   - Load from data/*.txt pipe-delimited files
   - Parse each line carefully with exact field order and create dicts for use in templates
   - Implement CRUD operations as required for reservations, reviews, waitlist, profile updates

3. **Templates:**
   - Implement all templates under templates_candidate_b/
   - Match all specified element IDs (dashboard-page, welcome-message, make-reservation-button, etc.)
   - Use Jinja2 templating for dynamic elements and loops
   - Ensure page titles match exactly those specified in requirement document

4. **Navigation:**
   - Implement all navigation buttons and links with url_for to correct route names
   - Use redirect for post submissions to appropriate pages

CRITICAL REQUIREMENTS:
- MUST utilize write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/
- Follow exact routes, naming conventions, and page elements from design_spec.md and user_task_description
- Do NOT deviate from specified element IDs or route names
- All data file field orders and parsing must be exact
- Isolate templates strictly in templates_candidate_b/ directory for integration later

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Backend Developer and Integration Specialist with expertise in Flask web applications.

Your goal is to comprehensively compare and merge two independent Flask application implementations and their isolated templates directories into a single unified Flask app and templates directory according to design_spec.md.

Task Details:
- Read user_task_description, design_spec.md, app_candidate_a.py, app_candidate_b.py, and all templates in templates_candidate_a/ and templates_candidate_b/
- Merge all Flask routes, handlers, and business logic from both app_candidate_*.py files into one complete app.py
- Consolidate all templates into a unified templates/ directory, resolving naming conflicts and preserving all required element IDs and page titles
- Ensure all routes and URLs conform exactly to design_spec.md and user_task_description
- Maintain data file access and consistent local file management
- Ensure the final app.py and templates/*.html are fully compatible and ready for deployment behind a web proxy

Merging Guidelines:
1. Consolidate routes by matching identical endpoints and unify handler logic; choose best implementation to avoid duplication
2. Carefully merge template files ensuring all required element IDs and dynamic content exist without conflict
3. Preserve exact filenames and locations as specified for final output (app.py, templates/*.html)
4. Validate that no required route, page title, or element ID is missing after merging
5. Maintain code quality and readability; eliminate redundant code

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to output final app.py and all templates into templates/
- Final implementation must exactly match all page titles, routes, element IDs, and navigation buttons specified in design_spec.md and user_task_description
- Ensure merged application is fully functional and consistent
- Do NOT add or remove functional features beyond design specification

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in comprehensive validation of Python Flask web applications.

Your goal is to perform a thorough independent validation of the web application source code and templates ensuring syntactic correctness, runtime stability, and full compliance with design specifications.

Task Details:
- Read user_task_description and design_spec.md for context and expected features
- Validate app.py source code and templates/*.html files for compliance, correctness, and completeness per design_spec.md
- Produce a detailed validation report validation_a.md capturing all findings and actionable recommendations

Validation Scope:
- Syntax and runtime validation of app.py using code validation tools
- Confirm existence and correctness of all Flask routes as per design_spec.md
- Validate page titles and presence of all required element IDs in templates
- Check data file interactions for correct reading/writing with local text files under /data directory
- Verify user navigation flows and URL stability without authentication

Validation Steps:
1. Run syntax and runtime checks on app.py using validate_python_file tool
2. Manually inspect or programmatically parse app.py and HTML templates for route and element verification
3. Compare actual implementation against design_spec.md page titles, element IDs, and route definitions
4. Test data interaction points ensuring correct file usage and formats aligned with design_spec.md
5. Verify that no authentication requirements exist and URLs behave consistently across flows

CRITICAL SUCCESS CRITERIA:
- Use validate_python_file and execute_python_code to confirm code correctness
- Write detailed validation findings with clear, reproducible issues in validation_a.md
- Report must cover all aspects described in Task Details and Validation Scope
- Use write_text_file tool to save validation_a.md
- Output file: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in user flow validation and data persistence testing for Python Flask web applications.

Your goal is to independently validate critical user workflows and data handling processes ensuring seamless reservation, waitlist, review, and profile management functionality.

Task Details:
- Read user_task_description and design_spec.md for relevant feature descriptions and data schemas
- Validate app.py and templates/*.html focusing on reservation workflows, waitlist correctness, review submissions, and data persistence in text files
- Produce a detailed validation report validation_b.md with findings, issues, and suggested fixes

Validation Scope:
- Test user reservation flow including making, viewing, and cancelling reservations
- Verify waitlist functionality including joining, position tracking, status updates
- Confirm review writing, listing, and storage behaves per design with correct data file updates
- Inspect profile update and dashboard navigation flows
- Ensure data file reads/writes conform to defined formats and fields in design_spec.md

Validation Steps:
1. Inspect code and templates to confirm forms, inputs, and navigation for user workflows
2. Analyze data file interactions for accuracy and robustness during user actions
3. Validate feedback correctness and data consistency after simulated user scenarios
4. Document discovered issues with steps to reproduce and suggested remediation

CRITICAL SUCCESS CRITERIA:
- Use validate_python_file and execute_python_code as needed for runtime validation
- Write clear, concise, actionable validation report validation_b.md
- Focus on user experience, data durability, and workflow integrity across features
- Use write_text_file tool to save validation_b.md
- Output file: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in code merging and application stability enhancement for Python Flask web applications.

Your goal is to merge independent validation reports, apply necessary corrections or improvements to app.py and templates/*.html, ensure compliance with design specifications, and produce the final production-ready codebases.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md
- Analyze validation reports for findings and recommended fixes or improvements
- Apply all valid and relevant fixes to app.py and templates/*.html ensuring full compliance with design_spec.md
- Confirm no regressions by adhering to design specs in final versions
- Produce final verified app.py and templates/*.html ready for deployment

Merging and Repair Process:
1. Combine and reconcile findings from validation_a.md and validation_b.md
2. Prioritize fixes that improve correctness, consistency, and feature completeness
3. Update code and templates accordingly, keeping original structure unless fixes require enhancements
4. Thoroughly check alignment with design_spec.md after applying fixes
5. Prepare final clean and stable versions of app.py and templates/*.html

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save corrected app.py and all updated templates/*.html files
- Ensure final outputs fully conform to design_spec.md specifications
- Do NOT introduce new features beyond validation fixes
- Maintain overall code quality and readability
- Output files: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'validation_a.md', 'source': 'ValidationEngineerA'}, {'type': 'text_file', 'name': 'validation_b.md', 'source': 'ValidationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignAnalystA': [
        ("DesignMerger", """Check design_candidate_a.md for completeness, page coverage, exact element, ID correctness, route feasibility, and consistency with requirements.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for completeness, page coverage, exact element, ID correctness, route feasibility, and consistency with requirements.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate app_candidate_a.py and isolated templates for completeness, route alignment, code quality, and faithful adherence to design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate app_candidate_b.py and isolated templates for completeness, route alignment, code quality, and faithful adherence to design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Validate validation_a.md for clear, actionable, and reproducible findings and recommendations aligned with design_spec.md before merging.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Validate validation_b.md for clear, actionable, and reproducible findings and recommendations aligned with design_spec.md before merging.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
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

    # Parallel execution for design candidates
    await asyncio.gather(
        execute(DesignAnalystA, "Produce detailed design candidate for 9 pages as design_candidate_a.md with exact routes, element IDs, page titles, navigation."),
        execute(DesignAnalystB, "Produce alternative complete design candidate for same 9 pages as design_candidate_b.md with exact routes, element IDs, page titles, navigation.")
    )

    # Read design candidates for merger
    candidate_a_content, candidate_b_content = "", ""
    try:
        candidate_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        candidate_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge the two designs into final design_spec.md
    await execute(DesignMerger,
                  f"=== Design Candidate A ===\n{candidate_a_content}\n\n=== Design Candidate B ===\n{candidate_b_content}")
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

    # Parallel implementation by EngineerA and EngineerB
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full Flask app as app_candidate_a.py and templates under templates_candidate_a/ "
                "based on user_task_description and design_spec.md."),
        execute(ImplementationEngineerB,
                "Implement full Flask app as app_candidate_b.py and templates under templates_candidate_b/ "
                "based on user_task_description and design_spec.md.")
    )

    # Read partial implementation outputs for merger
    app_candidate_a_code, app_candidate_b_code = "", ""
    templates_candidate_a_content, templates_candidate_b_content = "", ""
    try:
        app_candidate_a_code = open("app_candidate_a.py").read()
    except:
        pass
    try:
        app_candidate_b_code = open("app_candidate_b.py").read()
    except:
        pass
    try:
        templates_candidate_a_content = _read_text_artifacts("templates_candidate_a/*.html")
    except:
        pass
    try:
        templates_candidate_b_content = _read_text_artifacts("templates_candidate_b/*.html")
    except:
        pass

    # Merge implementations into final app.py and templates/
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a ===\n{templates_candidate_a_content}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b ===\n{templates_candidate_b_content}")
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
        recovery_time=45
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
        recovery_time=45
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

    # Parallel validation passes by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Perform comprehensive validation of app.py and templates/*.html including syntax, runtime, route correctness, UI elements, data interactions, and navigation. Write detailed validation report validation_a.md."),
        execute(ValidationEngineerB,
                "Independently validate user workflows, data persistence, and feature correctness in app.py and templates/*.html. Write detailed validation report validation_b.md.")
    )

    # Read validation reports for merger
    validation_a_content = ""
    validation_b_content = ""
    try:
        validation_a_content = open("validation_a.md").read()
    except Exception:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except Exception:
        pass

    # RepairMerger merges reports and applies fixes to produce final approved app.py and templates
    await execute(RepairMerger,
                  f"Analyze validation reports validation_a.md and validation_b.md, reconcile findings, apply valid fixes to app.py and templates/*.html. Produce final approved app.py and templates/*.html files.\n\n"
                  f"=== validation_a.md ===\n{validation_a_content}\n\n"
                  f"=== validation_b.md ===\n{validation_b_content}\n")
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
