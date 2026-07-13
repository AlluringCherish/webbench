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
# 20260713_210029_979428/main_20260713_210029_979428.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs specifying all routes, titles, element IDs, page content, and navigation for the BookstoreOnline app, merged into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently produce full designs including detailed route and page element specifications \"\n        \"covering all nine pages and their specified elements without viewing each other's output; \"\n        \"DesignMerger reads both design candidates and synthesizes a merged, consistent design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Design Analyst specializing in Python-based Flask web applications.\n\nYour goal is to independently create a complete candidate Web design for BookstoreOnline, covering all nine user-specified pages and elements with route definitions, page titles, element IDs, and UI descriptions.\n\nTask Details:\n- Read user_task_description for full application requirements\n- Output a detailed design candidate document with routes, page titles, UI element IDs, button functions, and descriptions\n- Create design_candidate_a.md capturing a full, consistent set of specifications for implementation\n- Do NOT read or consider any other design candidate files\n\nDesign Requirements:\n1. **Route Definitions:**\n   - Include all URL routes for the nine pages, with method indications (GET/POST)\n   - Specify route function names following lower_snake_case convention\n\n2. **Page Titles and Layout:**\n   - Ensure each page has exact page titles as per requirements\n   - Specify container IDs and key UI element IDs for each page as listed\n   - Include descriptions of main UI features and their relationships\n\n3. **Navigation:**\n   - Define navigation buttons and their target routes clearly\n   - Use concrete function names for routing references\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md\n- Provide a standalone, exhaustive design candidate covering all pages and UI elements exactly\n- Do not reference or depend on any other design candidate outputs\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Design Analyst specializing in Python-based Flask web applications.\n\nYour goal is to independently create an alternative yet complete candidate Web design for BookstoreOnline, covering all nine specified pages and UI elements with full route definitions, page titles, element IDs, and UI descriptions.\n\nTask Details:\n- Read user_task_description for complete app requirements\n- Produce a distinct but comprehensive design candidate covering routes, titles, element IDs, and UI layout\n- Save output as design_candidate_b.md\n- Do NOT read or consider any other design candidate files\n\nDesign Requirements:\n1. **Complete Route List:**\n   - Provide all page URL routes with HTTP methods and function names per Flask conventions\n   - Use unique but consistent function naming in snake_case\n\n2. **UI Element Specification:**\n   - Specify all container IDs, button IDs, input IDs exactly as required\n   - Detail the layout and interactivity of each page so it is fully understood for implementation\n\n3. **Page Titles and Navigation:**\n   - Accurately specify page titles, including those for nested or dynamic pages\n   - Include clear mappings of navigation buttons to route functions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_b.md\n- Deliver a fully detailed and implementable design candidate without reliance on others\n- Complete coverage of all elements and routes is mandatory\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Web Design Merger specializing in synthesizing multiple design candidates into a single coherent Flask web application design.\n\nYour goal is to merge design_candidate_a.md and design_candidate_b.md with the user task to produce a unified, conflict-resolved, implementation-ready design_spec.md for BookstoreOnline.\n\nTask Details:\n- Read user_task_description for full context on BookstoreOnline requirements\n- Compare design_candidate_a.md and design_candidate_b.md thoroughly\n- Resolve conflicts, duplicates, and omissions to create a consistent complete design\n- Specify all Flask routes with exact function names, HTTP methods, and URLs\n- Include all page titles, container and UI element IDs exactly as required\n- Provide clear navigation mappings and UI layout details\n- Reference local data files as needed to highlight integration points\n- Output a single authoritative design_spec.md representing the merged design\n\nMerging Guidelines:\n1. **Conflict Resolution:**\n   - Prefer completeness, accuracy, and adherence to user task\n   - Combine complementary details\n   - Resolve naming conflicts by standardizing on lowercase_with_underscores\n\n2. **Completeness Check:**\n   - Ensure all nine pages and all specified UI elements are present\n   - Verify navigation buttons and routes enable full app flow from dashboard start page\n\n3. **Consistency:**\n   - Standardize element and function naming conventions\n   - Ensure no contradictory instructions or missing elements remain\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the merged design_spec.md\n- Provide a consistent, detailed Flask app design ready for direct implementation\n- Ensure flawless alignment with user task and input candidates\n- No references to partial inputs or unresolved conflicts remain\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_a.md for complete and exact coverage of all pages, routes, element IDs, and UI requirements as per the user task before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_b.md for complete and exact coverage of all pages, routes, element IDs, and UI requirements as per the user task before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify design_spec.md fully resolves and unifies design candidates into a coherent, detailed implementation contract.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Flask app bundles including app.py and isolated templates/*.html directories, and merge them into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently build full Flask applications with app.py and templates directory \"\n        \"implementing all specified routes, pages, element IDs, data file reading/writing, and navigation per design_spec.md; \"\n        \"ImplementationMerger reads both complete candidate bundles and merges them into a single coherent app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web applications with expertise in isolated template management.\n\nYour goal is to independently implement a complete Flask application for BookstoreOnline, including app.py and an isolated templates directory, fully compliant with design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md fully\n- Implement app_candidate_a.py and all templates in templates_candidate_a/*.html\n- Ensure full route coverage matching design_spec.md\n- Implement all page titles, element IDs exactly as specified\n- Access and modify data using specified text files under data/ directory\n- Provide visible success/error messages for UI interactions\n- Support direct no-auth access for all features\n- Isolate all template files within templates_candidate_a directory\n\nImplementation Requirements:\n1. **Flask Structure**:\n   - Setup Flask app with isolated template folder (templates_candidate_a)\n   - Use render_template with templates_candidate_a directory paths\n   - Define all routes with exact function names and HTTP methods per design_spec.md\n\n2. **Data Handling**:\n   - Read/write from/to specified data/*.txt files using pipe-delimited format\n   - Match field orders exactly as specified in design_spec.md data schemas\n   - Handle file I/O errors gracefully with user-friendly messages\n\n3. **UI Elements**:\n   - Implement all UI element IDs exactly as specified (static and dynamic)\n   - Use Jinja2 templating syntax for dynamic IDs and content rendering\n   - Ensure buttons, inputs, tables have full functionality as per requirements\n\n4. **Navigation and Forms**:\n   - Implement navigation flows using url_for with precise route names\n   - Handle all form POST requests with validation and state updates\n   - Maintain session-independent logic (no authentication)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all templates in templates_candidate_a/\n- Do NOT mix templates with other candidates\n- Follow design_spec.md strictly in routes, element IDs, and data access\n- Provide clear, visible UI feedback success/error messages\n- Ensure all app.py code runs without syntax or runtime errors\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web applications with expertise in isolated template management.\n\nYour goal is to independently implement a complete Flask application for BookstoreOnline, including app.py and an isolated templates directory, fully compliant with design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md fully\n- Implement app_candidate_b.py and all templates in templates_candidate_b/*.html\n- Ensure full route coverage matching design_spec.md\n- Implement all page titles, element IDs exactly as specified\n- Access and modify data using specified text files under data/ directory\n- Provide visible success/error messages for UI interactions\n- Support direct no-auth access for all features\n- Isolate all template files within templates_candidate_b directory\n\nImplementation Requirements:\n1. **Flask Structure**:\n   - Setup Flask app with isolated template folder (templates_candidate_b)\n   - Use render_template with templates_candidate_b directory paths\n   - Define all routes with exact function names and HTTP methods per design_spec.md\n\n2. **Data Handling**:\n   - Read/write from/to specified data/*.txt files using pipe-delimited format\n   - Match field orders exactly as specified in design_spec.md data schemas\n   - Handle file I/O errors gracefully with user-friendly messages\n\n3. **UI Elements**:\n   - Implement all UI element IDs exactly as specified (static and dynamic)\n   - Use Jinja2 templating syntax for dynamic IDs and content rendering\n   - Ensure buttons, inputs, tables have full functionality as per requirements\n\n4. **Navigation and Forms**:\n   - Implement navigation flows using url_for with precise route names\n   - Handle all form POST requests with validation and state updates\n   - Maintain session-independent logic (no authentication)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/\n- Do NOT mix templates with other candidates\n- Follow design_spec.md strictly in routes, element IDs, and data access\n- Provide clear, visible UI feedback success/error messages\n- Ensure all app.py code runs without syntax or runtime errors\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging parallel Flask application implementations with isolated template directories.\n\nYour goal is to merge two independently developed Flask app bundles (app_candidate_a.py, templates_candidate_a/*.html and app_candidate_b.py, templates_candidate_b/*.html) into a single coherent final Flask application (app.py and templates/*.html), fully compliant with design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md\n- Read both candidate bundles (app_candidate_a.py, templates_candidate_a/*.html and app_candidate_b.py, templates_candidate_b/*.html)\n- Evaluate route coverage, correctness, and data file usage in both app_candidate_*.py files\n- Compare UI element implementation and template completeness between candidates\n- Resolve conflicts by selecting strongest features and correcting code for consistency and completeness\n- Merge isolated template directories into single templates/ directory with no dependency on candidate directories\n- Ensure final app.py follows Flask best practices, exact function names, and route specifications\n- Preserve all specified UI element IDs, page titles, navigation flows, and visible success/error messages\n- Ensure data file access complies exactly with design_spec.md schemas and field orders\n- Remove isolated template directory references; use standard templates/ folder\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and all templates/*.html in templates/ directory\n- Ensure final merged app.py passes syntax and runtime validations\n- Verify exact route and element ID compliance with design_spec.md\n- Provide clear and consistent UI feedback messages\n- The merged application must run standalone without reliance on candidate directories\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate app_candidate_a.py and templates_candidate_a/*.html for completeness, route correctness, data file usage, and UI element compliance before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate app_candidate_b.py and templates_candidate_b/*.html for completeness, route correctness, data file usage, and UI element compliance before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify merged app.py and templates/*.html fully respect the design_spec.md and are correct for all specified functionalities.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validation checks on app.py and templates, then merge repair suggestions into final app.py and templates\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently perform thorough validation on app.py and templates/*.html including \"\n        \"syntax, runtime, route functionality, UI elements, data file integration, and overall compliance with design_spec.md saved as \"\n        \"validation_a.md and validation_b.md respectively; RepairMerger then merges these reports and applies corrections to produce \"\n        \"the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask applications validation and quality assurance.\n\nYour goal is to independently validate the syntax correctness, startup behavior, Flask route coverage through test client, template rendering, and UI element presence of the web application according to the design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md to understand requirements\n- Use app.py and templates/*.html as implementation artifacts for validation\n- Produce a detailed validation report in validation_a.md covering syntax, runtime, routes, data file I/O, and UI elements verification\n- Focus on compliance with design_spec.md and runtime correctness without altering source\n\nValidation Steps:\n1. **Syntax and Startup Validation**:\n   - Use validate_python_file tool to check syntax and runtime of app.py\n   - Ensure Flask app starts without errors\n\n2. **Route and Template Coverage**:\n   - Use Flask test client to send requests to all routes specified in design_spec.md\n   - Verify HTTP status codes and template rendering success\n   - Confirm all required UI elements exist according to element IDs in design_spec.md\n\n3. **Data Files Integration Check**:\n   - Verify that all specified data files are correctly read and written during route handling\n   - Validate data loading/parsing respects field order in design_spec.md schemas\n\n4. **UI Element Presence and Consistency**:\n   - Confirm presence of dynamic and static element IDs in rendered pages as per design_spec.md\n   - Validate button and input element behaviors correspond to UI specs\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for validation tasks\n- Use write_text_file tool to save comprehensive validation report as validation_a.md\n- Focus on actionable, precise feedback for repair agent\n- Do NOT modify source code artifacts; output is validation report only\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in business logic and user interface functional validation for Flask web apps.\n\nYour goal is to independently validate business logic correctness, data file handling, UI element functionality, error message display, and route stability of the web application against design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md for requirements and expected behaviors\n- Use app.py and templates/*.html as implementation references\n- Run extensive test cases covering data read/write consistency, UI workflows, error handling, and route responsiveness\n- Produce a detailed validation report in validation_b.md with findings and suggestions\n\nValidation Workflow:\n1. **Business Logic Verification**:\n   - Check data handling matches schemas and usage in design_spec.md\n   - Test shopping cart, checkout, review submission, and order tracking functionalities for correctness\n\n2. **UI Element Functionality Testing**:\n   - Validate input controls (quantity updates, filters, submission buttons) behave as expected\n   - Confirm error or informational messages appear correctly for invalid inputs or failures\n\n3. **Route Stability and Performance**:\n   - Test each route under normal and edge conditions ensuring no crashes or errors\n   - Verify all dynamic elements (e.g., view-book-button-{book_id}) render and function properly\n\n4. **Data File Handling Validation**:\n   - Confirm data files (books.txt, cart.txt, orders.txt, etc.) are accessed and updated correctly\n   - Check for race conditions, concurrency issues, or data loss scenarios\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools as necessary\n- Use write_text_file tool to produce comprehensive validation report as validation_b.md\n- Provide clear, actionable feedback for RepairMerger, no source code changes here\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging validation feedback and applying repairs to Flask web application code and templates.\n\nYour goal is to analyze validation_a.md and validation_b.md reports, merge repair suggestions, reconcile contradictions, and update app.py and templates/*.html accordingly while preserving full compliance with design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md to maintain feature and compliance integrity\n- Read existing app.py, templates/*.html implementations and both validation reports\n- Merge and reconcile all repair suggestions into a consistent update plan\n- Apply corrections to app.py and templates/*.html preserving all original design_spec.md requirements\n- Produce updated app.py and templates/*.html reflecting all merged repairs\n\nRepair and Merge Process:\n1. **Validation Report Analysis**:\n   - Extract actionable repair items from both validation_a.md and validation_b.md\n   - Identify overlaps and conflicts, resolve with design_spec.md as source of truth\n\n2. **Code and Template Updates**:\n   - Edit app.py for bug fixes, route corrections, data handling improvements, and logic fixes\n   - Update templates/*.html to fix UI element presence, dynamic element rendering, and form actions per specs\n\n3. **Compliance Verification**:\n   - Ensure no introduced violation of design_spec.md specs in final outputs\n   - Verify format, structure, and naming conventions strictly follow original spec\n\n4. **Final Output**:\n   - Save corrected app.py and templates/*.html to designated output artifacts\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively for output saving\n- Maintain strict design_spec.md compliance throughout updates\n- Preserve all intended functionalities and element IDs\n- Provide bug-free, maintainable, and clean code and templates\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for correctness and actionable feedback that can improve app.py and templates/*.html.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_b.md for correctness and actionable feedback that can improve app.py and templates/*.html.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify the final app.py and templates/*.html preserve design_spec.md compliance and integrate all required fixes faithfully.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'BookstoreOnline' Web Application

## 1. Objective
Develop a comprehensive web application named 'BookstoreOnline' using Python, with data managed through local text files. The application enables users to browse books, add items to cart, checkout, write reviews, and track order history. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'BookstoreOnline' application is Python.

## 3. Page Design

The 'BookstoreOnline' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Bookstore Dashboard
- **Overview**: The main hub displaying featured books, bestsellers, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-books** - Type: Div - Display of featured book recommendations.
  - **ID: browse-catalog-button** - Type: Button - Button to navigate to book catalog page.
  - **ID: view-cart-button** - Type: Button - Button to navigate to shopping cart page.
  - **ID: bestsellers-button** - Type: Button - Button to navigate to bestsellers page.

### 2. Book Catalog Page
- **Page Title**: Book Catalog
- **Overview**: A page displaying all available books with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search books by title, author, or ISBN.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Fiction, Non-Fiction, Science, History, etc.).
  - **ID: books-grid** - Type: Div - Grid displaying book cards with cover, title, author, and price.
  - **ID: view-book-button-{book_id}** - Type: Button - Button to view book details (each book card has this).

### 3. Book Details Page
- **Page Title**: Book Details
- **Overview**: A page displaying detailed information about a specific book.
- **Elements**:
  - **ID: book-details-page** - Type: Div - Container for the book details page.
  - **ID: book-title** - Type: H1 - Display book title.
  - **ID: book-author** - Type: Div - Display book author.
  - **ID: book-price** - Type: Div - Display book price.
  - **ID: add-to-cart-button** - Type: Button - Button to add book to shopping cart.
  - **ID: book-reviews** - Type: Div - Section displaying customer reviews.

### 4. Shopping Cart Page
- **Page Title**: Shopping Cart
- **Overview**: A page displaying items in the cart with quantity management and checkout option.
- **Elements**:
  - **ID: cart-page** - Type: Div - Container for the cart page.
  - **ID: cart-items-table** - Type: Table - Table displaying cart items with title, quantity, price, and subtotal.
  - **ID: update-quantity-{item_id}** - Type: Input (number) - Field to update item quantity (each cart item has this).
  - **ID: remove-item-button-{item_id}** - Type: Button - Button to remove item from cart (each cart item has this).
  - **ID: proceed-checkout-button** - Type: Button - Button to proceed to checkout.
  - **ID: total-amount** - Type: Div - Display total cart amount.

### 5. Checkout Page
- **Page Title**: Checkout
- **Overview**: A page for users to enter shipping information and complete purchase.
- **Elements**:
  - **ID: checkout-page** - Type: Div - Container for the checkout page.
  - **ID: customer-name** - Type: Input - Field to input customer name.
  - **ID: shipping-address** - Type: Textarea - Field to input shipping address.
  - **ID: payment-method** - Type: Dropdown - Dropdown to select payment method (Credit Card, PayPal, Bank Transfer).
  - **ID: place-order-button** - Type: Button - Button to confirm and place order.

### 6. Order History Page
- **Page Title**: Order History
- **Overview**: A page displaying all previous orders with tracking information.
- **Elements**:
  - **ID: orders-page** - Type: Div - Container for the orders page.
  - **ID: orders-table** - Type: Table - Table displaying orders with order ID, date, total amount, and status.
  - **ID: view-order-button-{order_id}** - Type: Button - Button to view order details (each order has this).
  - **ID: order-status-filter** - Type: Dropdown - Dropdown to filter by status (All, Pending, Shipped, Delivered).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Reviews Page
- **Page Title**: Customer Reviews
- **Overview**: A page displaying all customer reviews and allowing users to write new reviews.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of all reviews with book title, rating, and review text.
  - **ID: write-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: filter-by-rating** - Type: Dropdown - Dropdown to filter reviews by rating (All, 5 stars, 4 stars, etc.).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write a Review
- **Overview**: A page for users to write reviews for purchased books.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: select-book** - Type: Dropdown - Dropdown to select book to review.
  - **ID: rating-select** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.

### 9. Bestsellers Page
- **Page Title**: Bestsellers
- **Overview**: A page displaying top-selling books ranked by sales.
- **Elements**:
  - **ID: bestsellers-page** - Type: Div - Container for the bestsellers page.
  - **ID: bestsellers-list** - Type: Div - Ranked list of bestselling books with rank, title, author, and sales count.
  - **ID: time-period-filter** - Type: Dropdown - Dropdown to filter by time period (This Week, This Month, All Time).
  - **ID: view-book-button-{book_id}** - Type: Button - Button to view book details (each bestseller has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'BookstoreOnline' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Books Data
- **File Name**: `books.txt`
- **Data Format**:
  ```
  book_id|title|author|isbn|category|price|stock|description
  ```
- **Example Data**:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File Name**: `cart.txt`
- **Data Format**:
  ```
  cart_id|book_id|quantity|added_date
  ```
- **Example Data**:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File Name**: `orders.txt`
- **Data Format**:
  ```
  order_id|customer_name|order_date|total_amount|status|shipping_address
  ```
- **Example Data**:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File Name**: `order_items.txt`
- **Data Format**:
  ```
  order_item_id|order_id|book_id|quantity|price
  ```
- **Example Data**:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|book_id|customer_name|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File Name**: `bestsellers.txt`
- **Data Format**:
  ```
  book_id|sales_count|period
  ```
- **Example Data**:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
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
            """You are a Web Design Analyst specializing in Python-based Flask web applications.

Your goal is to independently create a complete candidate Web design for BookstoreOnline, covering all nine user-specified pages and elements with route definitions, page titles, element IDs, and UI descriptions.

Task Details:
- Read user_task_description for full application requirements
- Output a detailed design candidate document with routes, page titles, UI element IDs, button functions, and descriptions
- Create design_candidate_a.md capturing a full, consistent set of specifications for implementation
- Do NOT read or consider any other design candidate files

Design Requirements:
1. **Route Definitions:**
   - Include all URL routes for the nine pages, with method indications (GET/POST)
   - Specify route function names following lower_snake_case convention

2. **Page Titles and Layout:**
   - Ensure each page has exact page titles as per requirements
   - Specify container IDs and key UI element IDs for each page as listed
   - Include descriptions of main UI features and their relationships

3. **Navigation:**
   - Define navigation buttons and their target routes clearly
   - Use concrete function names for routing references

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md
- Provide a standalone, exhaustive design candidate covering all pages and UI elements exactly
- Do not reference or depend on any other design candidate outputs

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Design Analyst specializing in Python-based Flask web applications.

Your goal is to independently create an alternative yet complete candidate Web design for BookstoreOnline, covering all nine specified pages and UI elements with full route definitions, page titles, element IDs, and UI descriptions.

Task Details:
- Read user_task_description for complete app requirements
- Produce a distinct but comprehensive design candidate covering routes, titles, element IDs, and UI layout
- Save output as design_candidate_b.md
- Do NOT read or consider any other design candidate files

Design Requirements:
1. **Complete Route List:**
   - Provide all page URL routes with HTTP methods and function names per Flask conventions
   - Use unique but consistent function naming in snake_case

2. **UI Element Specification:**
   - Specify all container IDs, button IDs, input IDs exactly as required
   - Detail the layout and interactivity of each page so it is fully understood for implementation

3. **Page Titles and Navigation:**
   - Accurately specify page titles, including those for nested or dynamic pages
   - Include clear mappings of navigation buttons to route functions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_b.md
- Deliver a fully detailed and implementable design candidate without reliance on others
- Complete coverage of all elements and routes is mandatory

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Web Design Merger specializing in synthesizing multiple design candidates into a single coherent Flask web application design.

Your goal is to merge design_candidate_a.md and design_candidate_b.md with the user task to produce a unified, conflict-resolved, implementation-ready design_spec.md for BookstoreOnline.

Task Details:
- Read user_task_description for full context on BookstoreOnline requirements
- Compare design_candidate_a.md and design_candidate_b.md thoroughly
- Resolve conflicts, duplicates, and omissions to create a consistent complete design
- Specify all Flask routes with exact function names, HTTP methods, and URLs
- Include all page titles, container and UI element IDs exactly as required
- Provide clear navigation mappings and UI layout details
- Reference local data files as needed to highlight integration points
- Output a single authoritative design_spec.md representing the merged design

Merging Guidelines:
1. **Conflict Resolution:**
   - Prefer completeness, accuracy, and adherence to user task
   - Combine complementary details
   - Resolve naming conflicts by standardizing on lowercase_with_underscores

2. **Completeness Check:**
   - Ensure all nine pages and all specified UI elements are present
   - Verify navigation buttons and routes enable full app flow from dashboard start page

3. **Consistency:**
   - Standardize element and function naming conventions
   - Ensure no contradictory instructions or missing elements remain

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the merged design_spec.md
- Provide a consistent, detailed Flask app design ready for direct implementation
- Ensure flawless alignment with user task and input candidates
- No references to partial inputs or unresolved conflicts remain

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Software Developer specializing in Flask web applications with expertise in isolated template management.

Your goal is to independently implement a complete Flask application for BookstoreOnline, including app.py and an isolated templates directory, fully compliant with design_spec.md.

Task Details:
- Read user_task_description and design_spec.md fully
- Implement app_candidate_a.py and all templates in templates_candidate_a/*.html
- Ensure full route coverage matching design_spec.md
- Implement all page titles, element IDs exactly as specified
- Access and modify data using specified text files under data/ directory
- Provide visible success/error messages for UI interactions
- Support direct no-auth access for all features
- Isolate all template files within templates_candidate_a directory

Implementation Requirements:
1. **Flask Structure**:
   - Setup Flask app with isolated template folder (templates_candidate_a)
   - Use render_template with templates_candidate_a directory paths
   - Define all routes with exact function names and HTTP methods per design_spec.md

2. **Data Handling**:
   - Read/write from/to specified data/*.txt files using pipe-delimited format
   - Match field orders exactly as specified in design_spec.md data schemas
   - Handle file I/O errors gracefully with user-friendly messages

3. **UI Elements**:
   - Implement all UI element IDs exactly as specified (static and dynamic)
   - Use Jinja2 templating syntax for dynamic IDs and content rendering
   - Ensure buttons, inputs, tables have full functionality as per requirements

4. **Navigation and Forms**:
   - Implement navigation flows using url_for with precise route names
   - Handle all form POST requests with validation and state updates
   - Maintain session-independent logic (no authentication)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all templates in templates_candidate_a/
- Do NOT mix templates with other candidates
- Follow design_spec.md strictly in routes, element IDs, and data access
- Provide clear, visible UI feedback success/error messages
- Ensure all app.py code runs without syntax or runtime errors

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Flask web applications with expertise in isolated template management.

Your goal is to independently implement a complete Flask application for BookstoreOnline, including app.py and an isolated templates directory, fully compliant with design_spec.md.

Task Details:
- Read user_task_description and design_spec.md fully
- Implement app_candidate_b.py and all templates in templates_candidate_b/*.html
- Ensure full route coverage matching design_spec.md
- Implement all page titles, element IDs exactly as specified
- Access and modify data using specified text files under data/ directory
- Provide visible success/error messages for UI interactions
- Support direct no-auth access for all features
- Isolate all template files within templates_candidate_b directory

Implementation Requirements:
1. **Flask Structure**:
   - Setup Flask app with isolated template folder (templates_candidate_b)
   - Use render_template with templates_candidate_b directory paths
   - Define all routes with exact function names and HTTP methods per design_spec.md

2. **Data Handling**:
   - Read/write from/to specified data/*.txt files using pipe-delimited format
   - Match field orders exactly as specified in design_spec.md data schemas
   - Handle file I/O errors gracefully with user-friendly messages

3. **UI Elements**:
   - Implement all UI element IDs exactly as specified (static and dynamic)
   - Use Jinja2 templating syntax for dynamic IDs and content rendering
   - Ensure buttons, inputs, tables have full functionality as per requirements

4. **Navigation and Forms**:
   - Implement navigation flows using url_for with precise route names
   - Handle all form POST requests with validation and state updates
   - Maintain session-independent logic (no authentication)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/
- Do NOT mix templates with other candidates
- Follow design_spec.md strictly in routes, element IDs, and data access
- Provide clear, visible UI feedback success/error messages
- Ensure all app.py code runs without syntax or runtime errors

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging parallel Flask application implementations with isolated template directories.

Your goal is to merge two independently developed Flask app bundles (app_candidate_a.py, templates_candidate_a/*.html and app_candidate_b.py, templates_candidate_b/*.html) into a single coherent final Flask application (app.py and templates/*.html), fully compliant with design_spec.md.

Task Details:
- Read user_task_description and design_spec.md
- Read both candidate bundles (app_candidate_a.py, templates_candidate_a/*.html and app_candidate_b.py, templates_candidate_b/*.html)
- Evaluate route coverage, correctness, and data file usage in both app_candidate_*.py files
- Compare UI element implementation and template completeness between candidates
- Resolve conflicts by selecting strongest features and correcting code for consistency and completeness
- Merge isolated template directories into single templates/ directory with no dependency on candidate directories
- Ensure final app.py follows Flask best practices, exact function names, and route specifications
- Preserve all specified UI element IDs, page titles, navigation flows, and visible success/error messages
- Ensure data file access complies exactly with design_spec.md schemas and field orders
- Remove isolated template directory references; use standard templates/ folder

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and all templates/*.html in templates/ directory
- Ensure final merged app.py passes syntax and runtime validations
- Verify exact route and element ID compliance with design_spec.md
- Provide clear and consistent UI feedback messages
- The merged application must run standalone without reliance on candidate directories

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask applications validation and quality assurance.

Your goal is to independently validate the syntax correctness, startup behavior, Flask route coverage through test client, template rendering, and UI element presence of the web application according to the design specifications.

Task Details:
- Read user_task_description and design_spec.md to understand requirements
- Use app.py and templates/*.html as implementation artifacts for validation
- Produce a detailed validation report in validation_a.md covering syntax, runtime, routes, data file I/O, and UI elements verification
- Focus on compliance with design_spec.md and runtime correctness without altering source

Validation Steps:
1. **Syntax and Startup Validation**:
   - Use validate_python_file tool to check syntax and runtime of app.py
   - Ensure Flask app starts without errors

2. **Route and Template Coverage**:
   - Use Flask test client to send requests to all routes specified in design_spec.md
   - Verify HTTP status codes and template rendering success
   - Confirm all required UI elements exist according to element IDs in design_spec.md

3. **Data Files Integration Check**:
   - Verify that all specified data files are correctly read and written during route handling
   - Validate data loading/parsing respects field order in design_spec.md schemas

4. **UI Element Presence and Consistency**:
   - Confirm presence of dynamic and static element IDs in rendered pages as per design_spec.md
   - Validate button and input element behaviors correspond to UI specs

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for validation tasks
- Use write_text_file tool to save comprehensive validation report as validation_a.md
- Focus on actionable, precise feedback for repair agent
- Do NOT modify source code artifacts; output is validation report only

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in business logic and user interface functional validation for Flask web apps.

Your goal is to independently validate business logic correctness, data file handling, UI element functionality, error message display, and route stability of the web application against design specifications.

Task Details:
- Read user_task_description and design_spec.md for requirements and expected behaviors
- Use app.py and templates/*.html as implementation references
- Run extensive test cases covering data read/write consistency, UI workflows, error handling, and route responsiveness
- Produce a detailed validation report in validation_b.md with findings and suggestions

Validation Workflow:
1. **Business Logic Verification**:
   - Check data handling matches schemas and usage in design_spec.md
   - Test shopping cart, checkout, review submission, and order tracking functionalities for correctness

2. **UI Element Functionality Testing**:
   - Validate input controls (quantity updates, filters, submission buttons) behave as expected
   - Confirm error or informational messages appear correctly for invalid inputs or failures

3. **Route Stability and Performance**:
   - Test each route under normal and edge conditions ensuring no crashes or errors
   - Verify all dynamic elements (e.g., view-book-button-{book_id}) render and function properly

4. **Data File Handling Validation**:
   - Confirm data files (books.txt, cart.txt, orders.txt, etc.) are accessed and updated correctly
   - Check for race conditions, concurrency issues, or data loss scenarios

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools as necessary
- Use write_text_file tool to produce comprehensive validation report as validation_b.md
- Provide clear, actionable feedback for RepairMerger, no source code changes here

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging validation feedback and applying repairs to Flask web application code and templates.

Your goal is to analyze validation_a.md and validation_b.md reports, merge repair suggestions, reconcile contradictions, and update app.py and templates/*.html accordingly while preserving full compliance with design_spec.md.

Task Details:
- Read user_task_description and design_spec.md to maintain feature and compliance integrity
- Read existing app.py, templates/*.html implementations and both validation reports
- Merge and reconcile all repair suggestions into a consistent update plan
- Apply corrections to app.py and templates/*.html preserving all original design_spec.md requirements
- Produce updated app.py and templates/*.html reflecting all merged repairs

Repair and Merge Process:
1. **Validation Report Analysis**:
   - Extract actionable repair items from both validation_a.md and validation_b.md
   - Identify overlaps and conflicts, resolve with design_spec.md as source of truth

2. **Code and Template Updates**:
   - Edit app.py for bug fixes, route corrections, data handling improvements, and logic fixes
   - Update templates/*.html to fix UI element presence, dynamic element rendering, and form actions per specs

3. **Compliance Verification**:
   - Ensure no introduced violation of design_spec.md specs in final outputs
   - Verify format, structure, and naming conventions strictly follow original spec

4. **Final Output**:
   - Save corrected app.py and templates/*.html to designated output artifacts

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively for output saving
- Maintain strict design_spec.md compliance throughout updates
- Preserve all intended functionalities and element IDs
- Provide bug-free, maintainable, and clean code and templates

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
        ("DesignMerger", """Verify design_candidate_a.md for complete and exact coverage of all pages, routes, element IDs, and UI requirements as per the user task before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Verify design_candidate_b.md for complete and exact coverage of all pages, routes, element IDs, and UI requirements as per the user task before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify design_spec.md fully resolves and unifies design candidates into a coherent, detailed implementation contract.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate app_candidate_a.py and templates_candidate_a/*.html for completeness, route correctness, data file usage, and UI element compliance before merging.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate app_candidate_b.py and templates_candidate_b/*.html for completeness, route correctness, data file usage, and UI element compliance before merging.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify merged app.py and templates/*.html fully respect the design_spec.md and are correct for all specified functionalities.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for correctness and actionable feedback that can improve app.py and templates/*.html.""", [{'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Check validation_b.md for correctness and actionable feedback that can improve app.py and templates/*.html.""", [{'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Verify the final app.py and templates/*.html preserve design_spec.md compliance and integrate all required fixes faithfully.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Build agents with defined parameters
    DesignAnalystA = build_resilient_agent(
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
        execute(DesignAnalystA, "Create a complete independent design candidate for BookstoreOnline and save as design_candidate_a.md"),
        execute(DesignAnalystB, "Create a complete independent design candidate for BookstoreOnline and save as design_candidate_b.md")
    )

    # Read outputs from analysts for merging
    design_candidate_a = ""
    design_candidate_b = ""
    try: design_candidate_a = open("design_candidate_a.md").read()
    except: pass
    try: design_candidate_b = open("design_candidate_b.md").read()
    except: pass

    # Merge the two design candidates into a final design_spec.md
    await execute(DesignMerger,
                  f"=== DesignCandidateA ===\n{design_candidate_a}\n\n=== DesignCandidateB ===\n{design_candidate_b}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    # Define agents
    ImplementationEngineerA = build_resilient_agent(
        agent_name="ImplementationEngineerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=60
    )
    ImplementationEngineerB = build_resilient_agent(
        agent_name="ImplementationEngineerB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=60
    )
    ImplementationMerger = build_resilient_agent(
        agent_name="ImplementationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=60
    )

    # Parallel execution for candidates
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete Flask app_candidate_a.py and templates_candidate_a/*.html "
                "based on user_task_description and design_spec.md. Follow all route, element ID, and data file specs precisely. "
                "Include UI success/error messages and support no-auth access."),
        execute(ImplementationEngineerB,
                "Implement complete Flask app_candidate_b.py and templates_candidate_b/*.html "
                "based on user_task_description and design_spec.md. Follow all route, element ID, and data file specs precisely. "
                "Include UI success/error messages and support no-auth access.")
    )

    # Read candidate outputs for merging
    candidate_a_app, candidate_b_app = "", ""
    candidate_a_templates, candidate_b_templates = "", ""
    try:
        candidate_a_app = open("app_candidate_a.py").read()
    except Exception:
        pass
    try:
        candidate_b_app = open("app_candidate_b.py").read()
    except Exception:
        pass
    try:
        candidate_a_templates = _read_text_artifacts("templates_candidate_a/*.html")
    except Exception:
        pass
    try:
        candidate_b_templates = _read_text_artifacts("templates_candidate_b/*.html")
    except Exception:
        pass

    # Merge candidate bundles into final app.py and templates/
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{candidate_a_app}\n\n"
                  f"=== templates_candidate_a/*.html ===\n{candidate_a_templates}\n\n"
                  f"=== app_candidate_b.py ===\n{candidate_b_app}\n\n"
                  f"=== templates_candidate_b/*.html ===\n{candidate_b_templates}\n\n"
                  "Merge both independent Flask app bundles into a single coherent final app.py and templates/*.html directory. "
                  "Resolve conflicts, unify routes, template usage, UI elements, and data handling as per design_spec.md. "
                  "Remove isolated template directory references, use standard templates/ folder. "
                  "Ensure final app.py and templates are complete, consistent, and runnable standalone."
                  )
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    ValidationEngineerA = build_resilient_agent(
        agent_name="ValidationEngineerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45,
    )
    ValidationEngineerB = build_resilient_agent(
        agent_name="ValidationEngineerB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45,
    )
    RepairMerger = build_resilient_agent(
        agent_name="RepairMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40,
    )

    # Read file artifacts for injection
    user_task_description = ""
    design_spec_md = ""
    app_py = ""
    templates_html = ""
    try: user_task_description = CONTEXT.get("user_task_description", [])[-1]["content"]
    except: pass
    try: design_spec_md = open("design_spec.md").read()
    except: pass
    try: app_py = open("app.py").read()
    except: pass
    try:
        import glob
        template_files = glob.glob("templates/*.html")
        templates_list = []
        for tf in template_files:
            try:
                templates_list.append(f"=== {tf} ===\n" + open(tf).read())
            except:
                continue
        templates_html = "\n\n".join(templates_list)
    except:
        templates_html = ""

    # Run ValidationEngineerA and ValidationEngineerB in parallel
    await asyncio.gather(
        execute(
            ValidationEngineerA,
            f"Validate Flask app and templates for syntax, startup, route coverage, template rendering, UI elements, and data integration.\n\n"
            f"User Task Description:\n{user_task_description}\n\n"
            f"Design Specification:\n{design_spec_md}\n\n"
            f"App.py implementation:\n{app_py}\n\n"
            f"Templates:\n{templates_html}\n\n"
            f"Output a detailed report as validation_a.md"
        ),
        execute(
            ValidationEngineerB,
            f"Validate business logic, data handling, UI functionality, error message display, and route stability.\n\n"
            f"User Task Description:\n{user_task_description}\n\n"
            f"Design Specification:\n{design_spec_md}\n\n"
            f"App.py implementation:\n{app_py}\n\n"
            f"Templates:\n{templates_html}\n\n"
            f"Output a detailed report as validation_b.md"
        ),
    )

    # Read validation reports for RepairMerger input
    validation_a_md = ""
    validation_b_md = ""
    try: validation_a_md = open("validation_a.md").read()
    except: pass
    try: validation_b_md = open("validation_b.md").read()
    except: pass

    # Run RepairMerger to merge reports and apply repair fixes to app.py and templates/*.html
    await execute(
        RepairMerger,
        f"Merge and reconcile validation reports from ValidationEngineerA and ValidationEngineerB below, "
        f"and apply the necessary fixes to update app.py and templates/*.html while maintaining full compliance with design_spec.md.\n\n"
        f"User Task Description:\n{user_task_description}\n\n"
        f"Design Specification:\n{design_spec_md}\n\n"
        f"Existing App.py:\n{app_py}\n\n"
        f"Existing Templates:\n{templates_html}\n\n"
        f"ValidationEngineerA report:\n{validation_a_md}\n\n"
        f"ValidationEngineerB report:\n{validation_b_md}"
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
