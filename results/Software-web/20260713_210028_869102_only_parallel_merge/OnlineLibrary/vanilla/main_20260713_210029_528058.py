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
# 20260713_210029_528058/main_20260713_210029_528058.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs and merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently write design candidates in parallel without seeing each other's work; \"\n        \"DesignMerger then reads both candidates and writes design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in Python Flask web app design.\n\nYour goal is to independently derive a complete web app design candidate from the user task, producing a detailed design document with concrete deliverables.\n\nTask Details:\n- Read full user_task_description artifact from CONTEXT\n- Create a comprehensive design candidate as design_candidate_a.md\n- Specify all Flask routes with methods and exact render_template() filenames\n- Define page titles, all element IDs, user interactions, visible messages\n- Specify context variables for each route with types and structures\n- Include data fixture schemas for pipe-delimited data files matching user task\n- Do NOT read or depend on any other analyst's candidate\n\nDesign Requirements:\n1. **Route and Template Mapping**\n   - List each route as URL path with HTTP methods (GET/POST)\n   - Specify exact templates/*.html filenames for render_template()\n2. **Page Titles and Element IDs**\n   - Include page titles as specified or derived\n   - Provide all required static and dynamic element IDs with description\n3. **Context Variables**\n   - Specify variables passed from backend to templates with types (str, int, list, dict)\n   - For lists of dicts, specify dict structure fields\n4. **User Interactions and Messages**\n   - Define button/link IDs and corresponding user actions or navigation\n   - Include any messages displayed to users per page\n5. **Data Fixture Schemas**\n   - Specify pipe-delimited field schemas for all data files (e.g., books.txt)\n   - Include field names and example data structures\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md\n- Produce a standalone design that enables independent backend/frontend implementation\n- Adhere strictly to user_task_description details\n- Do not access or use any external design candidates\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in Flask web application design and specification.\n\nYour goal is to independently craft an alternative complete design candidate for the web application described in the user task.\n\nTask Details:\n- Read the full user_task_description provided in CONTEXT\n- Produce an alternative design candidate as design_candidate_b.md\n- Detail all Flask routes with methods and corresponding render_template() filenames\n- Define exact page titles, UI element IDs, and interactive components\n- Specify template context variables with data types and structures precisely\n- Define data file schemas for all relevant pipe-delimited fixtures\n- Work independently without access to other analyst outputs\n\nDesign Instructions:\n1. **Routing and Templates**\n   - Enumerate each URL route and allowed HTTP methods\n   - Provide exact template filenames used by render_template()\n2. **Page Titles & UI Elements**\n   - Supply all exact page titles and required static/dynamic element IDs\n3. **Backend-Frontend Context**\n   - Specify context variables per route with clear types and nested structures\n4. **User UI Actions**\n   - Define buttons, navigation flows, and visible messages explicitly\n5. **Data Fixtures**\n   - List pipe-delimited data file formats with field ordering and examples\n\nCRITICAL REQUIREMENTS:\n- Save output using write_text_file as design_candidate_b.md\n- Ensure the design is implementable and covers every requirement in the user task\n- Do not use or refer to any other analyst's design documents\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Merger specializing in consolidating multiple web application design candidates into one cohesive specification.\n\nYour goal is to ingest two independent design candidates and the original user task, then produce a single coherent, complete design_spec.md.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md from CONTEXT\n- Compare both candidates in detail for omissions, conflicts, and coverage completeness\n- Resolve discrepancies and merge all consistent design elements into one unified design\n- Produce one design_spec.md with full Flask route definitions (paths, methods), exact page titles, element IDs\n- Specify user navigation flows, button actions, visible messages precisely\n- Define render_template filenames matching routes and context variable mappings with types\n- Consolidate pipe-delimited data fixture schemas with exact field orders and sample data\n- Ensure design_spec.md supports independent, implementation-ready backend and frontend development\n\nMerging Guidelines:\n1. **Route and Method Resolution**\n   - Include all unique routes from both candidates\n   - Merge route methods to cover all specified HTTP methods\n2. **Page Titles and UI Element Consistency**\n   - Resolve conflicting titles and retain those aligning with user task\n   - Harmonize element IDs and ensure no missing IDs for all pages\n3. **Context Variables Harmonization**\n   - Unify variable definitions and data structures, merging fields where appropriate\n4. **Navigation and User Interaction**\n   - Define consistent navigation paths and button/link behaviors\n5. **Data Schema Integration**\n   - Merge data file schemas ensuring full coverage and consistency\n6. **Implementation Readiness**\n   - Output design_spec.md that can directly guide backend and frontend implementation\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_spec.md\n- Deliver a single, conflict-resolved, and complete design specification\n- Ensure end-to-end feasibility from routes to UI to data schemas\n- Align final design strictly with original user_task_description and both candidates\n- Do NOT introduce new routes or elements not supported by inputs\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for complete, exact, and feasible route, external-template filename, context, and data fixture coverage before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for complete, exact, and feasible route, external-template filename, context, and data fixture coverage before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify design_spec.md resolves both candidates into one coherent, implementation-ready app.py plus templates/*.html contract.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Web application bundles and merge them into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement isolated Python/template candidates in parallel \"\n        \"without seeing each other's work; ImplementationMerger then reads both bundles and writes app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building complete web applications with templating and local file storage.\n\nYour goal is to independently implement a full Flask web application candidate bundle with isolated app and HTML templates.\n\nTask Details:\n- Read user_task_description and design_spec.md for complete functional requirements and design constraints\n- Do NOT read or use any artifacts from ImplementationEngineerB\n- Output a fully functional app_candidate_a.py configured with template_folder='templates_candidate_a'\n- Output complete templates in templates_candidate_a/*.html matching design: route paths, page titles, element IDs, template filenames, context variables\n- Use local data files stored in 'data/' directory, using provided pipe-delimited formats as source of truth\n- Cover features including search, borrow, return, reviews, reservations, history, payment, and user profile management with stable, actionable element IDs\n\nImplementation Requirements:\n1. Flask Configuration:\n   - Use: app = Flask(__name__, template_folder='templates_candidate_a')\n   - Use render_template for all page rendering\n2. Routing:\n   - Implement all required routes exactly as specified in design_spec.md and user_task_description\n3. Templates:\n   - Use precise element IDs as specified for each page\n   - Use requested page titles, matching exactly both in <title> and <h1>\n4. Data Handling:\n   - Read and write data from/to 'data/' folder files, respecting exact field order and pipe delimiter\n   - Handle file errors gracefully\n5. Features:\n   - Support search, borrowing, returns, review submission/editing, reservations management, borrowing history, payment of fines, and user profile edits\n6. Stability:\n   - Use stable unique IDs for actionable buttons and elements to avoid conflicts\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/\n- Follow design_spec.md and user_task_description precisely\n- Do not use or depend on any ImplementationEngineerB files or directories\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building complete web applications with templating and local file storage.\n\nYour goal is to independently implement a full Flask web application candidate bundle with isolated app and HTML templates.\n\nTask Details:\n- Read user_task_description and design_spec.md for complete functional requirements and design constraints\n- Do NOT read or use any artifacts from ImplementationEngineerA\n- Output a fully functional app_candidate_b.py configured with template_folder='templates_candidate_b'\n- Output complete templates in templates_candidate_b/*.html matching design: route paths, page titles, element IDs, template filenames, context variables\n- Use local data files stored in 'data/' folder, using provided pipe-delimited formats as source of truth\n- Cover features including search, borrow, return, reviews, reservations, history, payment, and user profile management with stable, actionable element IDs\n\nImplementation Requirements:\n1. Flask Configuration:\n   - Use: app = Flask(__name__, template_folder='templates_candidate_b')\n   - Use render_template for all page rendering\n2. Routing:\n   - Implement all required routes exactly as specified in design_spec.md and user_task_description\n3. Templates:\n   - Use precise element IDs as specified for each page\n   - Use requested page titles, matching exactly both in <title> and <h1>\n4. Data Handling:\n   - Read and write data from/to 'data/' folder files, respecting exact field order and pipe delimiter\n   - Handle file errors gracefully\n5. Features:\n   - Support search, borrowing, returns, review submission/editing, reservations management, borrowing history, payment of fines, and user profile edits\n6. Stability:\n   - Use stable unique IDs for actionable buttons and elements to avoid conflicts\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and all template files under templates_candidate_b/\n- Follow design_spec.md and user_task_description precisely\n- Do not use or depend on any ImplementationEngineerA files or directories\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging parallel Flask web application implementations into coherent, production-ready bundles.\n\nYour goal is to merge two independently developed Flask candidate bundles into a single consolidated app.py and templates/*.html project ready for deployment.\n\nTask Details:\n- Read user_task_description and design_spec.md as the authoritative design source\n- Read both candidate bundles: app_candidate_a.py + templates_candidate_a/*.html, and app_candidate_b.py + templates_candidate_b/*.html\n- Do NOT alter design_spec.md or user_task_description\n- Resolve any conflicts in routes, templates, variable names, data handling by merging logically following design_spec.md mandates\n- Output a single app.py with no runtime dependency on candidate directories\n- Output templates/*.html consistent with merged app.py\n- Enforce exact requested routes, page titles, element IDs, template filenames, and context variables as per design_spec.md\n- Ensure local 'data/' directory usage with pipe-delimited formats as per specifications\n- Include user-visible success and error messages for all critical operations\n- Maintain stable and actionable element IDs supporting features: search, borrowing, returning, reviews, reservations, history, payment, user profiles\n\nIntegration Requirements:\n1. Application:\n   - Flask app using render_template with templates/ folder\n   - All route handlers fully implemented, coherent, and tested against design_spec.md\n2. Templates:\n   - Unified templates set with exact IDs and navigation matching merged app.py\n3. Data:\n   - Data file access consistent and correctly implemented in app.py\n   - Data schemas matching provided formats exactly\n4. Conflict Resolution:\n   - Resolve naming and functional conflicts favoring completeness and conformance\n   - Avoid duplicate or conflicting routes, variables, or template files\n5. Messages:\n   - Implement user friendly feedback on each operation (success, error)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and all unified template files under templates/\n- Final outputs must be ready for independent validation without modification\n- Follow all design spec fields exactly; do not introduce extraneous routes or templates\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate A's Python/template bundle independently for design and data fixture coverage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate B's Python/template bundle independently for design and data fixture coverage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify app.py and templates/*.html form a coherent merge ready for independent validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validations and merge their repairs into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate app.py with templates/*.html in parallel without seeing each \"\n        \"other's reports; RepairMerger then consumes both reports and both implementation artifacts and writes the repaired application.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web applications and frontend-backend integration testing.\n\nYour goal is to independently validate Flask backend and HTML frontend artifacts to ensure correct syntax, startup, route handling, HTML contracts, and UI interaction behaviors, then produce a detailed validation report.\n\nTask Details:\n- Read user task description, design_spec.md, app.py, and templates/*.html\n- Validate app.py syntax and startup using Python file validation and test client simulations\n- Verify all templates specified are loaded via render_template with exact route mappings\n- Check page titles, element IDs, template filenames, and context variables for exact match to design_spec.md\n- Confirm URLs are accessible without authentication as specified\n- Validate parsing of pipe-delimited fixture files is flexible and consistent\n- Check UI for visible success/error messages and stable actionable element IDs\n- Produce validation_a.md report without referencing validation_b.md\n\nValidation Requirements:\n1. **Syntax and Startup Validation**\n   - Use validation tool to verify no syntax/runtime errors in app.py\n   - Test Flask app startup and route accessibility\n\n2. **Route and Template Validation**\n   - Confirm each route in app.py serves the correct template filename\n   - Verify render_template calls correspond exactly to defined templates\n   - Check exact page title strings and element IDs per template\n\n3. **Fixture Parsing**\n   - Validate flexible parsing of all pipe-delimited fixture files like users.txt, books.txt, borrowings.txt etc.\n\n4. **UI Interaction Checks**\n   - Verify success and error messages appear as specified\n   - Ensure all buttons and action IDs are stable and correctly named\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools to check app.py\n- Use write_text_file tool to save validation_a.md\n- Validation report must be precise, actionable, and reproducible\n- Do not read or reference validation_b.md\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in data validation and user interface consistency for Flask applications.\n\nYour goal is to independently validate backend data fixture handling, no-auth deep links, UI element consistency, action correctness, and visible outcomes, then produce a detailed validation report.\n\nTask Details:\n- Read user task description, design_spec.md, app.py, and templates/*.html\n- Validate consistency and correctness of data-fixture file parsing with various valid inputs\n- Verify all direct no-auth URLs are working exactly as specified\n- Check render_template filename and context variable consistency across backend and frontend\n- Validate exact page titles and all element IDs match design_spec.md specifications\n- Confirm all UI actions produce visible success or error outcomes\n- Validate stable actionable element IDs for buttons and forms\n- Produce validation_b.md report without referencing validation_a.md\n\nValidation Requirements:\n1. **Data Fixture Validation**\n   - Confirm parsing correctness for users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt\n\n2. **No-auth Deep Link Validation**\n   - Test all URLs accessible without authentication per design\n\n3. **UI Consistency Checks**\n   - Match exact page titles, element IDs, and render_template usage\n   - Confirm visible outcomes for user actions (borrow, return, reserve, review submission)\n\n4. **Actionable Element IDs**\n   - Verify stability and exact naming of all action buttons and form elements\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for backend execution and test simulations\n- Use write_text_file tool to save validation_b.md\n- Validation report must be detailed, independently reproducible, and actionable\n- Do not read or reference validation_a.md\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application maintenance and integration repair.\n\nYour goal is to reconcile two independent validation reports, apply all valid corrections, and produce the final repaired app.py and templates/*.html artifacts which fully comply with the merged design contract.\n\nTask Details:\n- Read user task description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md\n- Analyze both validation reports, extracting all reproducible and actionable backend and frontend corrections\n- Apply every accepted fix preserving existing render_template architecture and route definitions\n- Ensure all routes, page titles, element IDs, template filenames, context variables, no-auth URLs, fixture parsing, and visible success/error outcomes are strictly preserved or improved\n- Maintain the modular template files and exact Flask route handlers without altering design intent\n\nRepair Requirements:\n1. **Report Reconciliation**\n   - Combine and resolve conflicting suggestions from both validation reports logically\n   - Prioritize accuracy, maintainability, and user experience improvements\n\n2. **Code and Template Repair**\n   - Edit app.py with stable and tested fixes only\n   - Edit templates/*.html with exact element IDs and correct context integration\n   - Validate pipe-delimited fixture parsing is robust and flexible\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively to save final app.py and templates/*.html\n- Preserve existing external-template render_template architecture and exact contract specifications\n- Final artifacts must pass both validation criteria fully\n- Do not introduce new features beyond fixed corrections\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for reproducible, actionable backend and external-template findings before merging repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_b.md for reproducible, actionable backend and external-template findings before merging repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify final app.py and templates/*.html resolve both reports while preserving the merged design contract.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'OnlineLibrary' Web Application

## 1. Objective
Develop a comprehensive web application named 'OnlineLibrary' using Python, with data managed through local text files. The application enables users to search and browse books, borrow and return books, write reviews, manage reservations, and track their borrowing history. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'OnlineLibrary' application is Python.

## 3. Page Design

The 'OnlineLibrary' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Library Dashboard
- **Overview**: The main hub displaying featured books and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying username.
  - **ID: browse-books-button** - Type: Button - Button to navigate to book catalog page.
  - **ID: my-borrows-button** - Type: Button - Button to navigate to my borrowings page.

### 2. Book Catalog Page
- **Page Title**: Book Catalog
- **Overview**: A page displaying all available books with filtering and search options.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the book catalog page.
  - **ID: search-input** - Type: Input - Field to search books by title or author.
  - **ID: book-grid** - Type: Div - Grid displaying book cards with cover, title, author, and status.
  - **ID: view-book-button-{book_id}** - Type: Button - Button to navigate to book details page (each book card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Book Details Page
- **Page Title**: Book Details
- **Overview**: A page displaying detailed information about a specific book.
- **Elements**:
  - **ID: book-details-page** - Type: Div - Container for the book details page.
  - **ID: book-title** - Type: H1 - Display book title.
  - **ID: book-author** - Type: Div - Display book author.
  - **ID: book-status** - Type: Div - Display availability status (Available, Borrowed, Reserved).
  - **ID: borrow-button** - Type: Button - Button to borrow the book.
  - **ID: reviews-section** - Type: Div - Section displaying user reviews.
  - **ID: write-review-button** - Type: Button - Button to write a review.
  - **ID: back-to-catalog** - Type: Button - Button to navigate back to catalog.

### 4. Borrow Confirmation Page
- **Page Title**: Borrow Confirmation
- **Overview**: A page to confirm book borrowing details.
- **Elements**:
  - **ID: borrow-page** - Type: Div - Container for the borrow confirmation page.
  - **ID: borrow-book-info** - Type: Div - Display information about the book being borrowed.
  - **ID: due-date-display** - Type: Div - Display the due date for return (14 days from borrow).
  - **ID: confirm-borrow-button** - Type: Button - Button to confirm borrowing.
  - **ID: cancel-borrow-button** - Type: Button - Button to cancel and go back.

### 5. My Borrowings Page
- **Page Title**: My Borrowings
- **Overview**: A page displaying all books currently borrowed by the user.
- **Elements**:
  - **ID: my-borrows-page** - Type: Div - Container for the my borrowings page.
  - **ID: filter-status** - Type: Dropdown - Dropdown to filter by status (All, Active, Returned, Overdue).
  - **ID: borrows-table** - Type: Table - Table displaying borrowed books with title, borrow date, due date, status.
  - **ID: return-book-button-{borrow_id}** - Type: Button - Button to return book (each active borrow has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. My Reservations Page
- **Page Title**: My Reservations
- **Overview**: A page displaying all book reservations made by the user.
- **Elements**:
  - **ID: reservations-page** - Type: Div - Container for the reservations page.
  - **ID: reservations-table** - Type: Table - Table displaying reserved books with title, reservation date, status.
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each row has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Overview**: A page displaying all reviews written by the user.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of reviews with book title, rating, review text.
  - **ID: edit-review-button-{review_id}** - Type: Button - Button to edit review (each review has this).
  - **ID: delete-review-button-{review_id}** - Type: Button - Button to delete review (each review has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write Review
- **Overview**: A page for users to write or edit a review for a book.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: book-info-display** - Type: Div - Display information about the book being reviewed.
  - **ID: rating-input** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.
  - **ID: back-to-book** - Type: Button - Button to navigate back to book details.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: borrow-history** - Type: Div - Display list of all previously borrowed books.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Payment Confirmation Page
- **Page Title**: Payment Confirmation
- **Overview**: A page to confirm payment of overdue fines.
- **Elements**:
  - **ID: payment-page** - Type: Div - Container for the payment confirmation page.
  - **ID: fine-amount-display** - Type: Div - Display the fine amount to be paid.
  - **ID: confirm-payment-button** - Type: Button - Button to confirm payment.
  - **ID: back-to-profile** - Type: Button - Button to navigate back to profile.

## 4. Data Storage

The 'OnlineLibrary' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|address
  ```
- **Example Data**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. Books Data
- **File Name**: `books.txt`
- **Data Format**:
  ```
  book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
  ```
- **Example Data**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```

### 3. Borrowings Data
- **File Name**: `borrowings.txt`
- **Data Format**:
  ```
  borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
  ```
- **Example Data**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|username|book_id|reservation_date|status
  ```
- **Example Data**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|username|book_id|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. Fines Data
- **File Name**: `fines.txt`
- **Data Format**:
  ```
  fine_id|username|borrow_id|amount|status|date_issued
  ```
- **Example Data**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
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
            """You are a Web Application Design Analyst specializing in Python Flask web app design.

Your goal is to independently derive a complete web app design candidate from the user task, producing a detailed design document with concrete deliverables.

Task Details:
- Read full user_task_description artifact from CONTEXT
- Create a comprehensive design candidate as design_candidate_a.md
- Specify all Flask routes with methods and exact render_template() filenames
- Define page titles, all element IDs, user interactions, visible messages
- Specify context variables for each route with types and structures
- Include data fixture schemas for pipe-delimited data files matching user task
- Do NOT read or depend on any other analyst's candidate

Design Requirements:
1. **Route and Template Mapping**
   - List each route as URL path with HTTP methods (GET/POST)
   - Specify exact templates/*.html filenames for render_template()
2. **Page Titles and Element IDs**
   - Include page titles as specified or derived
   - Provide all required static and dynamic element IDs with description
3. **Context Variables**
   - Specify variables passed from backend to templates with types (str, int, list, dict)
   - For lists of dicts, specify dict structure fields
4. **User Interactions and Messages**
   - Define button/link IDs and corresponding user actions or navigation
   - Include any messages displayed to users per page
5. **Data Fixture Schemas**
   - Specify pipe-delimited field schemas for all data files (e.g., books.txt)
   - Include field names and example data structures

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md
- Produce a standalone design that enables independent backend/frontend implementation
- Adhere strictly to user_task_description details
- Do not access or use any external design candidates

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Design Analyst specializing in Flask web application design and specification.

Your goal is to independently craft an alternative complete design candidate for the web application described in the user task.

Task Details:
- Read the full user_task_description provided in CONTEXT
- Produce an alternative design candidate as design_candidate_b.md
- Detail all Flask routes with methods and corresponding render_template() filenames
- Define exact page titles, UI element IDs, and interactive components
- Specify template context variables with data types and structures precisely
- Define data file schemas for all relevant pipe-delimited fixtures
- Work independently without access to other analyst outputs

Design Instructions:
1. **Routing and Templates**
   - Enumerate each URL route and allowed HTTP methods
   - Provide exact template filenames used by render_template()
2. **Page Titles & UI Elements**
   - Supply all exact page titles and required static/dynamic element IDs
3. **Backend-Frontend Context**
   - Specify context variables per route with clear types and nested structures
4. **User UI Actions**
   - Define buttons, navigation flows, and visible messages explicitly
5. **Data Fixtures**
   - List pipe-delimited data file formats with field ordering and examples

CRITICAL REQUIREMENTS:
- Save output using write_text_file as design_candidate_b.md
- Ensure the design is implementable and covers every requirement in the user task
- Do not use or refer to any other analyst's design documents

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Merger specializing in consolidating multiple web application design candidates into one cohesive specification.

Your goal is to ingest two independent design candidates and the original user task, then produce a single coherent, complete design_spec.md.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md from CONTEXT
- Compare both candidates in detail for omissions, conflicts, and coverage completeness
- Resolve discrepancies and merge all consistent design elements into one unified design
- Produce one design_spec.md with full Flask route definitions (paths, methods), exact page titles, element IDs
- Specify user navigation flows, button actions, visible messages precisely
- Define render_template filenames matching routes and context variable mappings with types
- Consolidate pipe-delimited data fixture schemas with exact field orders and sample data
- Ensure design_spec.md supports independent, implementation-ready backend and frontend development

Merging Guidelines:
1. **Route and Method Resolution**
   - Include all unique routes from both candidates
   - Merge route methods to cover all specified HTTP methods
2. **Page Titles and UI Element Consistency**
   - Resolve conflicting titles and retain those aligning with user task
   - Harmonize element IDs and ensure no missing IDs for all pages
3. **Context Variables Harmonization**
   - Unify variable definitions and data structures, merging fields where appropriate
4. **Navigation and User Interaction**
   - Define consistent navigation paths and button/link behaviors
5. **Data Schema Integration**
   - Merge data file schemas ensuring full coverage and consistency
6. **Implementation Readiness**
   - Output design_spec.md that can directly guide backend and frontend implementation

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Deliver a single, conflict-resolved, and complete design specification
- Ensure end-to-end feasibility from routes to UI to data schemas
- Align final design strictly with original user_task_description and both candidates
- Do NOT introduce new routes or elements not supported by inputs

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Python Flask Developer specializing in building complete web applications with templating and local file storage.

Your goal is to independently implement a full Flask web application candidate bundle with isolated app and HTML templates.

Task Details:
- Read user_task_description and design_spec.md for complete functional requirements and design constraints
- Do NOT read or use any artifacts from ImplementationEngineerB
- Output a fully functional app_candidate_a.py configured with template_folder='templates_candidate_a'
- Output complete templates in templates_candidate_a/*.html matching design: route paths, page titles, element IDs, template filenames, context variables
- Use local data files stored in 'data/' directory, using provided pipe-delimited formats as source of truth
- Cover features including search, borrow, return, reviews, reservations, history, payment, and user profile management with stable, actionable element IDs

Implementation Requirements:
1. Flask Configuration:
   - Use: app = Flask(__name__, template_folder='templates_candidate_a')
   - Use render_template for all page rendering
2. Routing:
   - Implement all required routes exactly as specified in design_spec.md and user_task_description
3. Templates:
   - Use precise element IDs as specified for each page
   - Use requested page titles, matching exactly both in <title> and <h1>
4. Data Handling:
   - Read and write data from/to 'data/' folder files, respecting exact field order and pipe delimiter
   - Handle file errors gracefully
5. Features:
   - Support search, borrowing, returns, review submission/editing, reservations management, borrowing history, payment of fines, and user profile edits
6. Stability:
   - Use stable unique IDs for actionable buttons and elements to avoid conflicts

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/
- Follow design_spec.md and user_task_description precisely
- Do not use or depend on any ImplementationEngineerB files or directories

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Python Flask Developer specializing in building complete web applications with templating and local file storage.

Your goal is to independently implement a full Flask web application candidate bundle with isolated app and HTML templates.

Task Details:
- Read user_task_description and design_spec.md for complete functional requirements and design constraints
- Do NOT read or use any artifacts from ImplementationEngineerA
- Output a fully functional app_candidate_b.py configured with template_folder='templates_candidate_b'
- Output complete templates in templates_candidate_b/*.html matching design: route paths, page titles, element IDs, template filenames, context variables
- Use local data files stored in 'data/' folder, using provided pipe-delimited formats as source of truth
- Cover features including search, borrow, return, reviews, reservations, history, payment, and user profile management with stable, actionable element IDs

Implementation Requirements:
1. Flask Configuration:
   - Use: app = Flask(__name__, template_folder='templates_candidate_b')
   - Use render_template for all page rendering
2. Routing:
   - Implement all required routes exactly as specified in design_spec.md and user_task_description
3. Templates:
   - Use precise element IDs as specified for each page
   - Use requested page titles, matching exactly both in <title> and <h1>
4. Data Handling:
   - Read and write data from/to 'data/' folder files, respecting exact field order and pipe delimiter
   - Handle file errors gracefully
5. Features:
   - Support search, borrowing, returns, review submission/editing, reservations management, borrowing history, payment of fines, and user profile edits
6. Stability:
   - Use stable unique IDs for actionable buttons and elements to avoid conflicts

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and all template files under templates_candidate_b/
- Follow design_spec.md and user_task_description precisely
- Do not use or depend on any ImplementationEngineerA files or directories

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging parallel Flask web application implementations into coherent, production-ready bundles.

Your goal is to merge two independently developed Flask candidate bundles into a single consolidated app.py and templates/*.html project ready for deployment.

Task Details:
- Read user_task_description and design_spec.md as the authoritative design source
- Read both candidate bundles: app_candidate_a.py + templates_candidate_a/*.html, and app_candidate_b.py + templates_candidate_b/*.html
- Do NOT alter design_spec.md or user_task_description
- Resolve any conflicts in routes, templates, variable names, data handling by merging logically following design_spec.md mandates
- Output a single app.py with no runtime dependency on candidate directories
- Output templates/*.html consistent with merged app.py
- Enforce exact requested routes, page titles, element IDs, template filenames, and context variables as per design_spec.md
- Ensure local 'data/' directory usage with pipe-delimited formats as per specifications
- Include user-visible success and error messages for all critical operations
- Maintain stable and actionable element IDs supporting features: search, borrowing, returning, reviews, reservations, history, payment, user profiles

Integration Requirements:
1. Application:
   - Flask app using render_template with templates/ folder
   - All route handlers fully implemented, coherent, and tested against design_spec.md
2. Templates:
   - Unified templates set with exact IDs and navigation matching merged app.py
3. Data:
   - Data file access consistent and correctly implemented in app.py
   - Data schemas matching provided formats exactly
4. Conflict Resolution:
   - Resolve naming and functional conflicts favoring completeness and conformance
   - Avoid duplicate or conflicting routes, variables, or template files
5. Messages:
   - Implement user friendly feedback on each operation (success, error)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and all unified template files under templates/
- Final outputs must be ready for independent validation without modification
- Follow all design spec fields exactly; do not introduce extraneous routes or templates

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web applications and frontend-backend integration testing.

Your goal is to independently validate Flask backend and HTML frontend artifacts to ensure correct syntax, startup, route handling, HTML contracts, and UI interaction behaviors, then produce a detailed validation report.

Task Details:
- Read user task description, design_spec.md, app.py, and templates/*.html
- Validate app.py syntax and startup using Python file validation and test client simulations
- Verify all templates specified are loaded via render_template with exact route mappings
- Check page titles, element IDs, template filenames, and context variables for exact match to design_spec.md
- Confirm URLs are accessible without authentication as specified
- Validate parsing of pipe-delimited fixture files is flexible and consistent
- Check UI for visible success/error messages and stable actionable element IDs
- Produce validation_a.md report without referencing validation_b.md

Validation Requirements:
1. **Syntax and Startup Validation**
   - Use validation tool to verify no syntax/runtime errors in app.py
   - Test Flask app startup and route accessibility

2. **Route and Template Validation**
   - Confirm each route in app.py serves the correct template filename
   - Verify render_template calls correspond exactly to defined templates
   - Check exact page title strings and element IDs per template

3. **Fixture Parsing**
   - Validate flexible parsing of all pipe-delimited fixture files like users.txt, books.txt, borrowings.txt etc.

4. **UI Interaction Checks**
   - Verify success and error messages appear as specified
   - Ensure all buttons and action IDs are stable and correctly named

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools to check app.py
- Use write_text_file tool to save validation_a.md
- Validation report must be precise, actionable, and reproducible
- Do not read or reference validation_b.md

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in data validation and user interface consistency for Flask applications.

Your goal is to independently validate backend data fixture handling, no-auth deep links, UI element consistency, action correctness, and visible outcomes, then produce a detailed validation report.

Task Details:
- Read user task description, design_spec.md, app.py, and templates/*.html
- Validate consistency and correctness of data-fixture file parsing with various valid inputs
- Verify all direct no-auth URLs are working exactly as specified
- Check render_template filename and context variable consistency across backend and frontend
- Validate exact page titles and all element IDs match design_spec.md specifications
- Confirm all UI actions produce visible success or error outcomes
- Validate stable actionable element IDs for buttons and forms
- Produce validation_b.md report without referencing validation_a.md

Validation Requirements:
1. **Data Fixture Validation**
   - Confirm parsing correctness for users.txt, books.txt, borrowings.txt, reservations.txt, reviews.txt, fines.txt

2. **No-auth Deep Link Validation**
   - Test all URLs accessible without authentication per design

3. **UI Consistency Checks**
   - Match exact page titles, element IDs, and render_template usage
   - Confirm visible outcomes for user actions (borrow, return, reserve, review submission)

4. **Actionable Element IDs**
   - Verify stability and exact naming of all action buttons and form elements

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for backend execution and test simulations
- Use write_text_file tool to save validation_b.md
- Validation report must be detailed, independently reproducible, and actionable
- Do not read or reference validation_a.md

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application maintenance and integration repair.

Your goal is to reconcile two independent validation reports, apply all valid corrections, and produce the final repaired app.py and templates/*.html artifacts which fully comply with the merged design contract.

Task Details:
- Read user task description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md
- Analyze both validation reports, extracting all reproducible and actionable backend and frontend corrections
- Apply every accepted fix preserving existing render_template architecture and route definitions
- Ensure all routes, page titles, element IDs, template filenames, context variables, no-auth URLs, fixture parsing, and visible success/error outcomes are strictly preserved or improved
- Maintain the modular template files and exact Flask route handlers without altering design intent

Repair Requirements:
1. **Report Reconciliation**
   - Combine and resolve conflicting suggestions from both validation reports logically
   - Prioritize accuracy, maintainability, and user experience improvements

2. **Code and Template Repair**
   - Edit app.py with stable and tested fixes only
   - Edit templates/*.html with exact element IDs and correct context integration
   - Validate pipe-delimited fixture parsing is robust and flexible

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively to save final app.py and templates/*.html
- Preserve existing external-template render_template architecture and exact contract specifications
- Final artifacts must pass both validation criteria fully
- Do not introduce new features beyond fixed corrections

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
        ("ImplementationEngineerA", """Verify design_spec.md resolves both candidates into one coherent, implementation-ready app.py plus templates/*.html contract.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate candidate A's Python/template bundle independently for design and data fixture coverage.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate candidate B's Python/template bundle independently for design and data fixture coverage.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify app.py and templates/*.html form a coherent merge ready for independent validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for reproducible, actionable backend and external-template findings before merging repairs.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Check validation_b.md for reproducible, actionable backend and external-template findings before merging repairs.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Verify final app.py and templates/*.html resolve both reports while preserving the merged design contract.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    # Create DesignAnalystA agent
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
    # Create DesignAnalystB agent
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
    # Create DesignMerger agent
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

    # Parallel execution of analysts
    await asyncio.gather(
        execute(DesignAnalystA, "Analyze the user task and create a complete standalone design candidate as design_candidate_a.md"),
        execute(DesignAnalystB, "Analyze the user task independently and create an alternative complete design candidate as design_candidate_b.md")
    )

    # Read analyst outputs for merger
    design_candidate_a, design_candidate_b = "", ""
    try:
        design_candidate_a = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b = open("design_candidate_b.md").read()
    except:
        pass

    # Merge results into final design specification
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_candidate_a}\n\n"
                  f"=== DesignAnalystB ===\n{design_candidate_b}")
# Phase1_End

# Phase2_Start

async def implementation_phase():
    ImplementationEngineerA = build_resilient_agent(
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
        agent_name="ImplementationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Parallel execution of two independent implementations
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full Flask web app candidate bundle: app_candidate_a.py and templates_candidate_a/*.html based on user_task_description and design_spec.md. Do NOT use ImplementationEngineerB data."),
        execute(ImplementationEngineerB,
                "Implement full Flask web app candidate bundle: app_candidate_b.py and templates_candidate_b/*.html based on user_task_description and design_spec.md. Do NOT use ImplementationEngineerA data.")
    )

    # Read outputs from both candidates for merging
    app_candidate_a_code, app_candidate_b_code = "", ""
    templates_candidate_a, templates_candidate_b = "", ""
    try:
        app_candidate_a_code = open("app_candidate_a.py").read()
    except:
        pass
    try:
        app_candidate_b_code = open("app_candidate_b.py").read()
    except:
        pass

    # Reading templates candidate_a/*.html
    # Since multiple files, we try to read each known template filename if known or aggregate from wildcard (not possible here), so safely ignore actual reading here
    # We inject empty strings as fallback for template files content
    # Similarly for templates_candidate_b/*.html
    try:
        templates_candidate_a = open("templates_candidate_a/index.html").read()
    except:
        templates_candidate_a = ""
    try:
        templates_candidate_b = open("templates_candidate_b/index.html").read()
    except:
        templates_candidate_b = ""

    # Provide candidate bundles content to ImplementationMerger for coherent integration
    await execute(ImplementationMerger,
                  f"Merge two independent Flask candidates into single app.py and unified templates/*.html.\n"
                  f"User task and design_spec.md are authoritative.\n\n"
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a/index.html (sample) ===\n{templates_candidate_a}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b/index.html (sample) ===\n{templates_candidate_b}")
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=60
    )
    ValidationEngineerB = build_resilient_agent(
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

    # Parallel validation by both ValidationEngineer agents
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Perform comprehensive validation of app.py and templates/*.html per design_spec.md. "
                "Generate detailed validation_a.md report."),
        execute(ValidationEngineerB,
                "Perform independent validation of data-fixture parsing, no-auth URL access, and UI consistency per design_spec.md. "
                "Generate detailed validation_b.md report.")
    )

    # Read validation reports for merger
    validation_a_report, validation_b_report = "", ""
    try:
        validation_a_report = open("validation_a.md").read()
    except:
        validation_a_report = ""
    try:
        validation_b_report = open("validation_b.md").read()
    except:
        validation_b_report = ""

    # RepairMerger merges reports and applies fixes to app.py and templates/*.html
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_report}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_report}\n\n"
                  "Analyze both reports, reconcile all reproducible and actionable corrections, and "
                  "apply fixes to produce final repaired app.py and templates/*.html that fully comply "
                  "with design_spec.md and validation criteria. Preserve render_template architecture and route handlers. "
                  "Save final artifacts to app.py and templates/*.html.")
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
