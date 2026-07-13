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
# 20260713_210029_184691/main_20260713_210029_184691.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent detailed design specifications for GymMembership web app and merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently craft complete detailed design documents describing Flask routes, page titles, element IDs, \"\n        \"navigation, data flow with local text files, and UI elements reflecting user requirements; DesignMerger merges both documents into a single \"\n        \"coherent design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web applications design.\n\nYour goal is to create a comprehensive Flask app design based on user requirements focusing on route definitions, page titles, element IDs, button actions, template filenames, data file formats, and layout. This design will enable implementation without authentication and with dashboard as the start page.\n\nTask Details:\n- Read user_task_description fully for context\n- Produce a complete design_candidate_a.md describing Flask routes, pages, element IDs, button actions, template files, and local text file data formats\n- Follow user requirements ensuring all pages and UI elements are included with proper naming and navigation\n- Define data file schema and access patterns corresponding to local text files from requirements\n\nDesign Specifications:\n1. Flask Routes and Pages\n   - Define all route paths starting with dashboard as root or main entry\n   - Specify route functions, HTTP methods, and corresponding templates\n   - Include direct no-auth access to all pages\n\n2. UI Element IDs and Buttons\n   - Enumerate all element IDs as per user requirements for each page\n   - Define actions for buttons and navigation links clearly with target routes\n\n3. Data Files and Schemas\n   - Define local text file formats found in data directory (filename, field order, delimiters)\n   - Describe data loading and handling to support UI views and interactions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save detailed design in design_candidate_a.md\n- Ensure design is complete and consistent with user requirements and data files\n- Maintain precise element IDs, route names, and file schemas for implementation\n- Focus on independent design document enabling downstream implementation\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Architect expert in Flask web application design.\n\nYour goal is to independently create a complete Flask app design specifying route paths, page titles, element IDs, navigation mechanics, data handling from local text files, and UI layout consistent with the user task, starting from the dashboard page.\n\nTask Details:\n- Refer to user_task_description fully for reference\n- Produce comprehensive design_candidate_b.md specifying all routes, page titles, navigation button IDs and behaviors, template usage, and data file integration\n- Consider no-auth user access and dashboard as start page\n- Ensure UI components and data connections fully reflect user project requirements\n\nDesign Requirements:\n1. Route and Navigation Design\n   - Identify all Flask route paths and their corresponding page titles and template files\n   - Specify all navigation buttons, element IDs and their related route actions clearly\n\n2. UI Elements and Layout\n   - List all required element IDs for each page and their roles\n   - Include dynamic element IDs where applicable (e.g., buttons with {id} variables)\n\n3. Data File Integration\n   - Specify reading and interpretation of local text files for backend data serving\n   - Define file formats, field order, and expected usage in UI rendering\n\nCRITICAL REQUIREMENTS:\n- Save all detailed design into design_candidate_b.md using write_text_file\n- The design must be fully aligned with user requirements and local data storage conventions\n- Output must enable downstream independent implementation and integration\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Integrator skilled in merging and reconciling software design documents.\n\nYour goal is to merge and reconcile two independent design candidates into a single unified and coherent design_spec.md. This specification must be implementation-ready, defining all Flask routes, page titles, element IDs, button actions, local text file schemas and access patterns, dashboard start page, and no-auth direct navigation consistent with user requirements.\n\nTask Details:\n- Read user_task_description plus design_candidate_a.md and design_candidate_b.md\n- Identify and resolve conflicts, inconsistencies or omissions in both designs\n- Produce a unified design_spec.md that combines best elements and ensures completeness and clarity\n- Confirm all pages, route paths, UI elements, button behaviors, and data file descriptions are covered thoroughly\n- Maintain dashboard as start page and no-auth access everywhere\n\nMerging Instructions:\n1. Aggregate all Flask routes ensuring unique paths and correct HTTP methods\n2. Consolidate element IDs including dynamic patterns for buttons and controls\n3. Harmonize data file schemas and define exact access patterns for each file\n4. Provide a clear, implementation-focused document suitable for both backend and frontend engineering\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final design_spec.md\n- Ensure no conflicts remain and specification aligns perfectly with user requirements\n- Format specification for clear readability and actionable implementation guidance\n- Output only design_spec.md as specified\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for completeness, accuracy of Flask routes, pages, element IDs, button actions, and data file integration.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for completeness, accuracy of Flask routes, pages, element IDs, button actions, and data file integration.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Validate that design_spec.md is an accurate, coherent, and complete specification ready for implementation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement two independent complete GymMembership Flask app bundles and merge into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement Flask web apps including app.py and templates under isolated directories, \"\n        \"enforcing routes, page titles, element IDs, button behavior, data storage in local text files with correct I/O formats and access, no-auth navigation, \"\n        \"and dashboard as start page; ImplementationMerger merges both into a final app.py and unified templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application development with local text file data storage.\n\nYour goal is to independently implement a complete Flask web application bundle including the app logic and HTML templates, strictly following design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md provided in CONTEXT\n- Output a fully functional Flask application named app_candidate_a.py\n- Implement all required pages, routes, element IDs, button functionalities as specified\n- Use data files located under 'data/' directory with correct pipe-delimited I/O formats\n- Produce all HTML templates under templates_candidate_a/ directory with exact element IDs\n- Ensure the app starts at the Dashboard page and uses no authentication/navigation barriers\n\nImplementation Instructions:\n1. **App Structure and Routing**:\n   - Implement Flask routes exactly as per specifications for all nine pages\n   - Root URL ('/') must serve the dashboard page\n   - Use render_template() for HTML rendering with correct template names from templates_candidate_a\n2. **Data Integration**:\n   - Load and write data exclusively using the specified data text files\n   - Follow exact field orders and formats for reading and writing\n3. **Templates**:\n   - Implement all HTML templates as per specification with exact element IDs\n   - Include all buttons, dropdowns, tables, inputs, and forms as required\n4. **No Authentication**:\n   - Ensure all pages are accessible without login or authorization\n   - Maintain smooth navigation between pages with the provided buttons\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app_candidate_a.py and all templates_candidate_a/*.html files\n- Ensure strict compliance with design_spec.md for routes, data file formats, element IDs, page titles\n- Dashboard page must be the app's root/start page\n- Maintain clean, readable, and executable Flask code ready for merging with another implementation\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application development and local data file integration.\n\nYour goal is to independently implement a complete Flask web application package covering all required pages, routes, and template files as per specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md in CONTEXT\n- Build a fully working Flask application named app_candidate_b.py\n- Implement all routes and pages with correct HTML templates named and placed in templates_candidate_b/\n- Use the specified local data files in 'data/' directory with precise parsing and writing rules\n- The dashboard page must be set as the root route '/'\n- Ensure no authentication mechanisms are implemented; all pages accessible directly\n\nImplementation Guidance:\n1. **Routing and Navigation**:\n   - Implement exact Flask routes for the nine specified pages\n   - Root '/' must route to Dashboard page\n   - Use render_template for serving templates from templates_candidate_b folder\n2. **Data File Handling**:\n   - Read/write pipe-delimited files according to field order and types\n   - Implement robust file handlers for data persistence\n3. **Templates Implementation**:\n   - Create all templates as per spec with exact element IDs, buttons, and inputs\n   - Follow naming conventions exactly for template filenames\n4. **No-Auth Access**:\n   - All pages are openly accessible without login or restrictions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app_candidate_b.py and templates_candidate_b/*.html\n- Adhere strictly to design_spec.md for routing, page titles, element IDs, and data access\n- Dashboard page is root entry point of the app\n- Provide clean, maintainable, and functional Flask code ready for merging\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specialized in merging Flask web application implementations.\n\nYour goal is to merge two independently developed Flask app implementations into a final unified stable system including app.py and templates/*.html.\n\nTask Details:\n- Analyze user_task_description and design_spec.md from CONTEXT\n- Review app_candidate_a.py and templates_candidate_a/*.html from ImplementationEngineerA\n- Review app_candidate_b.py and templates_candidate_b/*.html from ImplementationEngineerB\n- Resolve any conflicts in routes, data file handling, templates, and element IDs\n- Synthesize a coherent final Flask app.py implementing all required routes and logic\n- Consolidate and unify templates into templates/*.html with correct element IDs and page titles\n- Ensure the app uses render_template correctly and reads/writes data files under 'data/' folder\n- Confirm no authentication required and root route ('/') serves the dashboard page\n- Prepare the merged app.py and templates/*.html ready for validation and deployment\n\nMerging Instructions:\n1. **Route and Function Integration**:\n   - Identify overlapping and complementary routes\n   - Merge code maintaining route correctness and data integrity\n2. **Template Consolidation**:\n   - Combine template files into a single coherent set\n   - Maintain consistent element IDs and page layout per spec\n3. **Data File Access Consistency**:\n   - Ensure all data I/O uses the specified pipe-delimited 'data/' files precisely\n4. **No Auth and Navigation**:\n   - Preserve open access without login barriers\n   - Dashboard is start page and root URL\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save merged app.py and all templates/*.html files\n- The merged system must fully comply with design_spec.md and user_task_description\n- Final output must be clean, maintainable, and functionally complete for the GymMembership app\n- Ensure no duplicate or conflicting routes or templates remain\n- Dashboard page must be served at root URL '/'\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess app_candidate_a.py and templates_candidate_a for completeness, code correctness, and adherence to design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess app_candidate_b.py and templates_candidate_b for completeness, code correctness, and adherence to design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Confirm that the merged app.py and templates/*.html fully implement design_spec.md and are ready for validation testing.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validations on the merged GymMembership Flask app and merge fixes into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate app.py and templates/*.html through syntax checks, route tests, data handling validation, \"\n        \"and UI element confirmations; RepairMerger reconciles results, applies necessary fixes, and writes a final polished app.py and templates/*.html bundle.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web application validation.\n\nYour goal is to perform comprehensive validation of the GymMembership app backend and frontend for correctness and completeness to produce a detailed validation report.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and all HTML templates (*.html)\n- Validate app.py for syntax correctness and verify all Flask routes exist for each page described\n- Confirm presence of all required HTML element IDs and buttons per design specification\n- Verify correct parsing and usage of all local data files stored under 'data/' directory\n- Ensure the Dashboard page is configured as the start page\n- Output detailed validation report as validation_a.md\n\nValidation Requirements:\n1. Syntax Checks:\n   - Run syntax validation on app.py, report any errors/warnings\n2. Route Validations:\n   - Confirm each of the nine pages has a corresponding route function\n   - Check correct HTTP methods and templates used\n3. UI Element Verifications:\n   - Confirm presence of all specified element IDs (static and dynamic)\n   - Verify button IDs and link navigations correspond to design spec\n4. Data File Usages:\n   - Ensure data files are loaded correctly with proper field mappings\n   - Confirm data-driven outputs in templates reflect data source structures\n5. Application Start-Up:\n   - Verify root route '/' redirects to the Dashboard page\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file tool for syntax checking of app.py\n- Use execute_python_code for runtime route tests if needed\n- Use write_text_file tool to output validation_a.md\n- Reports must be clear, itemized, referencing design_spec.md contracts\n- Focus only on validation; do not fix code or templates here\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in end-to-end functional testing of Python Flask web applications.\n\nYour goal is to independently verify that the GymMembership app fully implements required functionalities, data integration, and UI compliance producing a structured validation report.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and HTML templates (*.html)\n- Test coverage of all required functionalities for user flows: membership plans, classes, trainers, bookings, workouts\n- Validate correct integration of local text-based data files with app and templates\n- Confirm UI elements presence, correctness of element IDs, and no authentication flows exist\n- Verify the Dashboard page is the first page users see on navigation\n- Output comprehensive validation report as validation_b.md\n\nTesting Scope:\n1. Functional Completeness:\n   - Check all user-facing pages and features listed in the user requirements\n   - Verify form submissions and data display workflows\n2. Data Integration:\n   - Confirm correctness of data loaded from files (memberships.txt, classes.txt, etc.)\n   - Spot discrepancies or missing data usage in templates or routes\n3. UI and UX Compliance:\n   - Validate presence and correctness of specified element IDs and buttons\n   - Ensure navigation flows per design spec\n4. Security / Flow Checks:\n   - Confirm absence of authentication or login requirement flows\n5. Start Page Verification:\n   - Ensure Dashboard is the landing page route\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file for backend syntax checks\n- Use execute_python_code for integration and runtime tests\n- Use write_text_file tool to output validation_b.md report\n- Do not perform any code or template modifications here\n- Outputs must be thorough, referencing user requirements and design_spec.md\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Full Stack Developer specializing in Python Flask application maintenance and integration.\n\nYour goal is to analyze independent validation reports, reconcile discrepancies, fix all identified errors, and produce a final fully functional GymMembership app.py and templates/*.html set that comply fully with user requirements and design specifications.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md\n- Analyze both validation reports for errors, inconsistencies, and omissions\n- Apply necessary corrections and bug fixes in app.py and templates/*.html\n- Ensure full adherence to design_spec.md contracts on routing, data usage, and UI elements\n- Confirm error-free syntax and runtime correctness of Flask app and templates\n- Produce polished final app.py and templates/*.html ready for deployment\n\nImplementation Guidelines:\n1. Code Corrections:\n   - Fix any syntax issues and routing errors in app.py\n   - Ensure data loading matches specified pipe-delimited formats and data fields exactly\n   - Validate route functions correspond one-to-one with pages from design spec\n2. Template Adjustments:\n   - Add missing element IDs or buttons per design_spec.md\n   - Correct dynamic IDs and navigation links for full functionality\n3. Consistency Checks:\n   - Ensure design_spec.md constraints are preserved; no deviations\n   - All validation issues from both reports must be resolved\n4. Final Testing:\n   - Confirm app.py passes validation tools without errors\n   - Validate templates render correctly matching specification\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and templates/*.html files\n- No new features or design changes; focus solely on corrections and adherence\n- Output must be a clean and maintainable code base matching user requirements\n- Maintain explicit data schema usage compliance as specified\n- Do not omit any fixes reported in validation_a.md or validation_b.md\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Evaluate validation_a.md for actionable errors and completeness before merging corrections.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Evaluate validation_b.md for actionable errors and completeness before merging corrections.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html preserve design_spec.md and fully meet all validated requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'GymMembership' Web Application

## 1. Objective
Develop a comprehensive web application named 'GymMembership' using Python, with data managed through local text files. The application enables users to browse membership plans, view class schedules, explore trainer profiles, book personal training sessions, and track workout records. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'GymMembership' application is Python.

## 3. Page Design

The 'GymMembership' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Gym Membership Dashboard
- **Overview**: The main hub displaying member highlights, featured classes, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: member-welcome** - Type: Div - Welcome section with member status information.
  - **ID: browse-membership-button** - Type: Button - Button to navigate to membership plans page.
  - **ID: view-schedule-button** - Type: Button - Button to navigate to class schedule page.
  - **ID: book-trainer-button** - Type: Button - Button to navigate to personal training booking page.

### 2. Membership Plans Page
- **Page Title**: Membership Plans
- **Overview**: A page displaying all available membership plans with details and pricing.
- **Elements**:
  - **ID: membership-page** - Type: Div - Container for the membership plans page.
  - **ID: plan-filter** - Type: Dropdown - Dropdown to filter by membership type (Basic, Premium, Elite).
  - **ID: plans-grid** - Type: Div - Grid displaying membership plan cards with name, price, and features.
  - **ID: view-details-button-{plan_id}** - Type: Button - Button to view plan details (each plan card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Plan Details Page
- **Page Title**: Plan Details
- **Overview**: A page displaying comprehensive information about a specific membership plan.
- **Elements**:
  - **ID: plan-details-page** - Type: Div - Container for the plan details page.
  - **ID: plan-title** - Type: H1 - Display plan name.
  - **ID: plan-price** - Type: Div - Display plan price and billing cycle.
  - **ID: plan-features** - Type: Div - Display all features included in the plan.
  - **ID: enroll-plan-button** - Type: Button - Button to enroll in the plan.
  - **ID: plan-reviews** - Type: Div - Section displaying member reviews of the plan.

### 4. Class Schedule Page
- **Page Title**: Class Schedule
- **Overview**: A page displaying fitness classes with time, duration, trainer, and capacity information.
- **Elements**:
  - **ID: schedule-page** - Type: Div - Container for the schedule page.
  - **ID: schedule-search** - Type: Input - Field to search classes by name or trainer.
  - **ID: schedule-filter** - Type: Dropdown - Dropdown to filter by class type (Yoga, CrossFit, Pilates, Boxing, etc.).
  - **ID: classes-grid** - Type: Div - Grid displaying class cards with schedule and instructor.
  - **ID: enroll-class-button-{class_id}** - Type: Button - Button to enroll in class (each class card has this).

### 5. Trainer Profiles Page
- **Page Title**: Trainer Profiles
- **Overview**: A page displaying all available trainers with expertise, certifications, and specialties.
- **Elements**:
  - **ID: trainers-page** - Type: Div - Container for the trainers page.
  - **ID: trainer-search** - Type: Input - Field to search trainers by name or specialty.
  - **ID: specialty-filter** - Type: Dropdown - Dropdown to filter by specialty (Strength, Cardio, Flexibility, Weight Loss).
  - **ID: trainers-grid** - Type: Div - Grid displaying trainer cards with photo, name, and expertise.
  - **ID: view-trainer-button-{trainer_id}** - Type: Button - Button to view trainer profile (each trainer card has this).

### 6. Trainer Detail Page
- **Page Title**: Trainer Profile
- **Overview**: A page displaying detailed information about a specific trainer.
- **Elements**:
  - **ID: trainer-detail-page** - Type: Div - Container for the trainer detail page.
  - **ID: trainer-name** - Type: H1 - Display trainer name.
  - **ID: trainer-bio** - Type: Div - Display trainer biography and experience.
  - **ID: trainer-certifications** - Type: Div - Display trainer certifications.
  - **ID: book-session-button** - Type: Button - Button to book a session with this trainer.
  - **ID: trainer-reviews** - Type: Div - Section displaying reviews from clients.

### 7. PT Booking Page
- **Page Title**: Book Personal Training
- **Overview**: A page for users to schedule personal training sessions with trainers.
- **Elements**:
  - **ID: booking-page** - Type: Div - Container for the booking page.
  - **ID: select-trainer** - Type: Dropdown - Dropdown to select trainer.
  - **ID: session-date** - Type: Input (date) - Field to select session date.
  - **ID: session-time** - Type: Dropdown - Dropdown to select session time slot.
  - **ID: session-duration** - Type: Dropdown - Dropdown to select session duration (30, 60, 90 minutes).
  - **ID: confirm-booking-button** - Type: Button - Button to confirm booking.

### 8. Workout Records Page
- **Page Title**: My Workout Records
- **Overview**: A page displaying user's personal workout history and progress tracking.
- **Elements**:
  - **ID: workouts-page** - Type: Div - Container for the workouts page.
  - **ID: workouts-table** - Type: Table - Table displaying workout history with date, type, duration, and calories burned.
  - **ID: filter-by-type** - Type: Dropdown - Dropdown to filter workouts by type (Class, PT Session, Personal).
  - **ID: log-workout-button** - Type: Button - Button to log a new workout.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Log Workout Page
- **Page Title**: Log Workout
- **Overview**: A page for users to record their workout sessions and progress.
- **Elements**:
  - **ID: log-workout-page** - Type: Div - Container for the log workout page.
  - **ID: workout-type** - Type: Dropdown - Dropdown to select workout type (Cardio, Strength, Flexibility, Sports).
  - **ID: workout-duration** - Type: Input (number) - Field to input workout duration in minutes.
  - **ID: calories-burned** - Type: Input (number) - Field to input estimated calories burned.
  - **ID: workout-notes** - Type: Textarea - Field to add notes about the workout.
  - **ID: submit-workout-button** - Type: Button - Button to submit workout record.

## 4. Data Storage

The 'GymMembership' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Memberships Data
- **File Name**: `memberships.txt`
- **Data Format**:
  ```
  membership_id|plan_name|price|billing_cycle|features|max_classes
  ```
- **Example Data**:
  ```
  1|Basic|29.99|monthly|Gym access, 2 classes per week|8
  2|Premium|59.99|monthly|Gym access, 5 classes per week, 2 PT sessions|20
  3|Elite|99.99|monthly|Unlimited gym access, unlimited classes, 4 PT sessions, nutrition coaching|unlimited
  ```

### 2. Classes Data
- **File Name**: `classes.txt`
- **Data Format**:
  ```
  class_id|class_name|trainer_id|class_type|schedule_day|schedule_time|capacity|duration
  ```
- **Example Data**:
  ```
  1|Morning Yoga|1|Yoga|Monday|06:00|20|60
  2|CrossFit Bootcamp|2|CrossFit|Tuesday|18:00|15|45
  3|Pilates Core|3|Pilates|Wednesday|10:00|18|50
  ```

### 3. Trainers Data
- **File Name**: `trainers.txt`
- **Data Format**:
  ```
  trainer_id|name|specialty|certifications|experience_years|bio
  ```
- **Example Data**:
  ```
  1|Sarah Johnson|Yoga & Flexibility|Certified Yoga Instructor, CPR|8|Expert in mind-body wellness and injury prevention
  2|Mike Thompson|Strength & Conditioning|NASM-CPT, CrossFit Level 2|10|Specializes in powerlifting and functional fitness
  3|Emma Davis|Pilates|Pilates Method Alliance Certified|6|Focus on core strength and postural alignment
  ```

### 4. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|member_name|trainer_id|booking_date|booking_time|duration_minutes|status
  ```
- **Example Data**:
  ```
  1|John Doe|1|2025-01-20|10:00|60|Confirmed
  2|Jane Smith|2|2025-01-21|14:00|45|Confirmed
  3|Alex Johnson|3|2025-01-22|16:00|60|Pending
  ```

### 5. Workouts Data
- **File Name**: `workouts.txt`
- **Data Format**:
  ```
  workout_id|member_name|workout_type|workout_date|duration_minutes|calories_burned|notes
  ```
- **Example Data**:
  ```
  1|John Doe|Cardio|2025-01-15|45|350|Morning run on treadmill
  2|Jane Smith|Strength|2025-01-16|60|420|Upper body weight training with trainer
  3|Alex Johnson|Class|2025-01-17|50|380|CrossFit Bootcamp session
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
            """You are a Software Architect specializing in Flask web applications design.

Your goal is to create a comprehensive Flask app design based on user requirements focusing on route definitions, page titles, element IDs, button actions, template filenames, data file formats, and layout. This design will enable implementation without authentication and with dashboard as the start page.

Task Details:
- Read user_task_description fully for context
- Produce a complete design_candidate_a.md describing Flask routes, pages, element IDs, button actions, template files, and local text file data formats
- Follow user requirements ensuring all pages and UI elements are included with proper naming and navigation
- Define data file schema and access patterns corresponding to local text files from requirements

Design Specifications:
1. Flask Routes and Pages
   - Define all route paths starting with dashboard as root or main entry
   - Specify route functions, HTTP methods, and corresponding templates
   - Include direct no-auth access to all pages

2. UI Element IDs and Buttons
   - Enumerate all element IDs as per user requirements for each page
   - Define actions for buttons and navigation links clearly with target routes

3. Data Files and Schemas
   - Define local text file formats found in data directory (filename, field order, delimiters)
   - Describe data loading and handling to support UI views and interactions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save detailed design in design_candidate_a.md
- Ensure design is complete and consistent with user requirements and data files
- Maintain precise element IDs, route names, and file schemas for implementation
- Focus on independent design document enabling downstream implementation

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Architect expert in Flask web application design.

Your goal is to independently create a complete Flask app design specifying route paths, page titles, element IDs, navigation mechanics, data handling from local text files, and UI layout consistent with the user task, starting from the dashboard page.

Task Details:
- Refer to user_task_description fully for reference
- Produce comprehensive design_candidate_b.md specifying all routes, page titles, navigation button IDs and behaviors, template usage, and data file integration
- Consider no-auth user access and dashboard as start page
- Ensure UI components and data connections fully reflect user project requirements

Design Requirements:
1. Route and Navigation Design
   - Identify all Flask route paths and their corresponding page titles and template files
   - Specify all navigation buttons, element IDs and their related route actions clearly

2. UI Elements and Layout
   - List all required element IDs for each page and their roles
   - Include dynamic element IDs where applicable (e.g., buttons with {id} variables)

3. Data File Integration
   - Specify reading and interpretation of local text files for backend data serving
   - Define file formats, field order, and expected usage in UI rendering

CRITICAL REQUIREMENTS:
- Save all detailed design into design_candidate_b.md using write_text_file
- The design must be fully aligned with user requirements and local data storage conventions
- Output must enable downstream independent implementation and integration

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Integrator skilled in merging and reconciling software design documents.

Your goal is to merge and reconcile two independent design candidates into a single unified and coherent design_spec.md. This specification must be implementation-ready, defining all Flask routes, page titles, element IDs, button actions, local text file schemas and access patterns, dashboard start page, and no-auth direct navigation consistent with user requirements.

Task Details:
- Read user_task_description plus design_candidate_a.md and design_candidate_b.md
- Identify and resolve conflicts, inconsistencies or omissions in both designs
- Produce a unified design_spec.md that combines best elements and ensures completeness and clarity
- Confirm all pages, route paths, UI elements, button behaviors, and data file descriptions are covered thoroughly
- Maintain dashboard as start page and no-auth access everywhere

Merging Instructions:
1. Aggregate all Flask routes ensuring unique paths and correct HTTP methods
2. Consolidate element IDs including dynamic patterns for buttons and controls
3. Harmonize data file schemas and define exact access patterns for each file
4. Provide a clear, implementation-focused document suitable for both backend and frontend engineering

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final design_spec.md
- Ensure no conflicts remain and specification aligns perfectly with user requirements
- Format specification for clear readability and actionable implementation guidance
- Output only design_spec.md as specified

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application development with local text file data storage.

Your goal is to independently implement a complete Flask web application bundle including the app logic and HTML templates, strictly following design specifications.

Task Details:
- Read user_task_description and design_spec.md provided in CONTEXT
- Output a fully functional Flask application named app_candidate_a.py
- Implement all required pages, routes, element IDs, button functionalities as specified
- Use data files located under 'data/' directory with correct pipe-delimited I/O formats
- Produce all HTML templates under templates_candidate_a/ directory with exact element IDs
- Ensure the app starts at the Dashboard page and uses no authentication/navigation barriers

Implementation Instructions:
1. **App Structure and Routing**:
   - Implement Flask routes exactly as per specifications for all nine pages
   - Root URL ('/') must serve the dashboard page
   - Use render_template() for HTML rendering with correct template names from templates_candidate_a
2. **Data Integration**:
   - Load and write data exclusively using the specified data text files
   - Follow exact field orders and formats for reading and writing
3. **Templates**:
   - Implement all HTML templates as per specification with exact element IDs
   - Include all buttons, dropdowns, tables, inputs, and forms as required
4. **No Authentication**:
   - Ensure all pages are accessible without login or authorization
   - Maintain smooth navigation between pages with the provided buttons

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app_candidate_a.py and all templates_candidate_a/*.html files
- Ensure strict compliance with design_spec.md for routes, data file formats, element IDs, page titles
- Dashboard page must be the app's root/start page
- Maintain clean, readable, and executable Flask code ready for merging with another implementation

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application development and local data file integration.

Your goal is to independently implement a complete Flask web application package covering all required pages, routes, and template files as per specifications.

Task Details:
- Read user_task_description and design_spec.md in CONTEXT
- Build a fully working Flask application named app_candidate_b.py
- Implement all routes and pages with correct HTML templates named and placed in templates_candidate_b/
- Use the specified local data files in 'data/' directory with precise parsing and writing rules
- The dashboard page must be set as the root route '/'
- Ensure no authentication mechanisms are implemented; all pages accessible directly

Implementation Guidance:
1. **Routing and Navigation**:
   - Implement exact Flask routes for the nine specified pages
   - Root '/' must route to Dashboard page
   - Use render_template for serving templates from templates_candidate_b folder
2. **Data File Handling**:
   - Read/write pipe-delimited files according to field order and types
   - Implement robust file handlers for data persistence
3. **Templates Implementation**:
   - Create all templates as per spec with exact element IDs, buttons, and inputs
   - Follow naming conventions exactly for template filenames
4. **No-Auth Access**:
   - All pages are openly accessible without login or restrictions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app_candidate_b.py and templates_candidate_b/*.html
- Adhere strictly to design_spec.md for routing, page titles, element IDs, and data access
- Dashboard page is root entry point of the app
- Provide clean, maintainable, and functional Flask code ready for merging

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specialized in merging Flask web application implementations.

Your goal is to merge two independently developed Flask app implementations into a final unified stable system including app.py and templates/*.html.

Task Details:
- Analyze user_task_description and design_spec.md from CONTEXT
- Review app_candidate_a.py and templates_candidate_a/*.html from ImplementationEngineerA
- Review app_candidate_b.py and templates_candidate_b/*.html from ImplementationEngineerB
- Resolve any conflicts in routes, data file handling, templates, and element IDs
- Synthesize a coherent final Flask app.py implementing all required routes and logic
- Consolidate and unify templates into templates/*.html with correct element IDs and page titles
- Ensure the app uses render_template correctly and reads/writes data files under 'data/' folder
- Confirm no authentication required and root route ('/') serves the dashboard page
- Prepare the merged app.py and templates/*.html ready for validation and deployment

Merging Instructions:
1. **Route and Function Integration**:
   - Identify overlapping and complementary routes
   - Merge code maintaining route correctness and data integrity
2. **Template Consolidation**:
   - Combine template files into a single coherent set
   - Maintain consistent element IDs and page layout per spec
3. **Data File Access Consistency**:
   - Ensure all data I/O uses the specified pipe-delimited 'data/' files precisely
4. **No Auth and Navigation**:
   - Preserve open access without login barriers
   - Dashboard is start page and root URL

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save merged app.py and all templates/*.html files
- The merged system must fully comply with design_spec.md and user_task_description
- Final output must be clean, maintainable, and functionally complete for the GymMembership app
- Ensure no duplicate or conflicting routes or templates remain
- Dashboard page must be served at root URL '/'

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web application validation.

Your goal is to perform comprehensive validation of the GymMembership app backend and frontend for correctness and completeness to produce a detailed validation report.

Task Details:
- Read user_task_description, design_spec.md, app.py, and all HTML templates (*.html)
- Validate app.py for syntax correctness and verify all Flask routes exist for each page described
- Confirm presence of all required HTML element IDs and buttons per design specification
- Verify correct parsing and usage of all local data files stored under 'data/' directory
- Ensure the Dashboard page is configured as the start page
- Output detailed validation report as validation_a.md

Validation Requirements:
1. Syntax Checks:
   - Run syntax validation on app.py, report any errors/warnings
2. Route Validations:
   - Confirm each of the nine pages has a corresponding route function
   - Check correct HTTP methods and templates used
3. UI Element Verifications:
   - Confirm presence of all specified element IDs (static and dynamic)
   - Verify button IDs and link navigations correspond to design spec
4. Data File Usages:
   - Ensure data files are loaded correctly with proper field mappings
   - Confirm data-driven outputs in templates reflect data source structures
5. Application Start-Up:
   - Verify root route '/' redirects to the Dashboard page

CRITICAL REQUIREMENTS:
- Use validate_python_file tool for syntax checking of app.py
- Use execute_python_code for runtime route tests if needed
- Use write_text_file tool to output validation_a.md
- Reports must be clear, itemized, referencing design_spec.md contracts
- Focus only on validation; do not fix code or templates here

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in end-to-end functional testing of Python Flask web applications.

Your goal is to independently verify that the GymMembership app fully implements required functionalities, data integration, and UI compliance producing a structured validation report.

Task Details:
- Read user_task_description, design_spec.md, app.py, and HTML templates (*.html)
- Test coverage of all required functionalities for user flows: membership plans, classes, trainers, bookings, workouts
- Validate correct integration of local text-based data files with app and templates
- Confirm UI elements presence, correctness of element IDs, and no authentication flows exist
- Verify the Dashboard page is the first page users see on navigation
- Output comprehensive validation report as validation_b.md

Testing Scope:
1. Functional Completeness:
   - Check all user-facing pages and features listed in the user requirements
   - Verify form submissions and data display workflows
2. Data Integration:
   - Confirm correctness of data loaded from files (memberships.txt, classes.txt, etc.)
   - Spot discrepancies or missing data usage in templates or routes
3. UI and UX Compliance:
   - Validate presence and correctness of specified element IDs and buttons
   - Ensure navigation flows per design spec
4. Security / Flow Checks:
   - Confirm absence of authentication or login requirement flows
5. Start Page Verification:
   - Ensure Dashboard is the landing page route

CRITICAL REQUIREMENTS:
- Use validate_python_file for backend syntax checks
- Use execute_python_code for integration and runtime tests
- Use write_text_file tool to output validation_b.md report
- Do not perform any code or template modifications here
- Outputs must be thorough, referencing user requirements and design_spec.md

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Full Stack Developer specializing in Python Flask application maintenance and integration.

Your goal is to analyze independent validation reports, reconcile discrepancies, fix all identified errors, and produce a final fully functional GymMembership app.py and templates/*.html set that comply fully with user requirements and design specifications.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md
- Analyze both validation reports for errors, inconsistencies, and omissions
- Apply necessary corrections and bug fixes in app.py and templates/*.html
- Ensure full adherence to design_spec.md contracts on routing, data usage, and UI elements
- Confirm error-free syntax and runtime correctness of Flask app and templates
- Produce polished final app.py and templates/*.html ready for deployment

Implementation Guidelines:
1. Code Corrections:
   - Fix any syntax issues and routing errors in app.py
   - Ensure data loading matches specified pipe-delimited formats and data fields exactly
   - Validate route functions correspond one-to-one with pages from design spec
2. Template Adjustments:
   - Add missing element IDs or buttons per design_spec.md
   - Correct dynamic IDs and navigation links for full functionality
3. Consistency Checks:
   - Ensure design_spec.md constraints are preserved; no deviations
   - All validation issues from both reports must be resolved
4. Final Testing:
   - Confirm app.py passes validation tools without errors
   - Validate templates render correctly matching specification

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and templates/*.html files
- No new features or design changes; focus solely on corrections and adherence
- Output must be a clean and maintainable code base matching user requirements
- Maintain explicit data schema usage compliance as specified
- Do not omit any fixes reported in validation_a.md or validation_b.md

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
        ("DesignMerger", """Check design_candidate_a.md for completeness, accuracy of Flask routes, pages, element IDs, button actions, and data file integration.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for completeness, accuracy of Flask routes, pages, element IDs, button actions, and data file integration.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Validate that design_spec.md is an accurate, coherent, and complete specification ready for implementation.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Assess app_candidate_a.py and templates_candidate_a for completeness, code correctness, and adherence to design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Assess app_candidate_b.py and templates_candidate_b for completeness, code correctness, and adherence to design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Confirm that the merged app.py and templates/*.html fully implement design_spec.md and are ready for validation testing.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Evaluate validation_a.md for actionable errors and completeness before merging corrections.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Evaluate validation_b.md for actionable errors and completeness before merging corrections.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm final app.py and templates/*.html preserve design_spec.md and fully meet all validated requirements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
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

    # Parallel design creation
    await asyncio.gather(
        execute(DesignAnalystA, "Create comprehensive design_candidate_a.md describing Flask routes, UI elements, data files per user requirements."),
        execute(DesignAnalystB, "Create comprehensive design_candidate_b.md describing Flask routes, titles, navigation, UI and data files per user requirements.")
    )

    # Read design candidates for merging
    design_candidate_a, design_candidate_b = "", ""
    try:
        design_candidate_a = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b = open("design_candidate_b.md").read()
    except:
        pass

    # Merge design candidates into final design_spec.md
    await execute(DesignMerger,
                  f"User task description is available in CONTEXT.\n\n"
                  f"=== Design Candidate A ===\n{design_candidate_a}\n\n"
                  f"=== Design Candidate B ===\n{design_candidate_b}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    ImplementationEngineerA = build_resilient_agent(
        agent_name="ImplementationEngineerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
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
        timeout_threshold=280,
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
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel implementation by Engineer A and Engineer B
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete Flask app as app_candidate_a.py and templates_candidate_a/*.html "
                "based on user_task_description and design_spec.md, enforcing all specs, dashboard as root."),
        execute(ImplementationEngineerB,
                "Implement complete Flask app as app_candidate_b.py and templates_candidate_b/*.html "
                "based on user_task_description and design_spec.md, enforcing all specs, dashboard as root.")
    )

    # Read outputs from both candidates for merging
    candidate_a_py, candidate_b_py = "", ""
    candidate_a_templates, candidate_b_templates = "", ""
    try:
        candidate_a_py = open("app_candidate_a.py").read()
    except:
        pass
    try:
        candidate_b_py = open("app_candidate_b.py").read()
    except:
        pass
    # Templates are multiple files, reading content of the directories as string is assumed unavailable.
    # Instead, pass the directory names or indication for injection to the merger.

    # For merger, inject the code contents of both app_candidate_*.py plus indication of templates
    merger_message = (
        f"Implementation merges two Flask apps:\n"
        f"=== app_candidate_a.py ===\n{candidate_a_py}\n\n"
        f"=== app_candidate_b.py ===\n{candidate_b_py}\n\n"
        f"Templates directories: templates_candidate_a/*.html and templates_candidate_b/*.html"
    )

    await execute(ImplementationMerger, merger_message)
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
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=60
    )

    # Parallel independent validation by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate GymMembership app.py and templates/*.html for syntax, route completeness, "
                "UI element presence, data handling, and start page correctness. Output validation_a.md."),
        execute(ValidationEngineerB,
                "Conduct comprehensive functional testing of GymMembership app.py and templates/*.html "
                "for user flows, data integration, UI compliance, security check (no auth), and start page. "
                "Output validation_b.md.")
    )

    # Read validation reports for RepairMerger
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # RepairMerger reconciles validation reports and produces final app.py and templates/*.html
    await execute(
        RepairMerger,
        f"Analyze validation reports and apply all fixes to app.py and templates/*.html. "
        f"Ensure strict compliance with design_spec.md and user requirements. "
        f"Output polished final app.py and templates/*.html.\n\n"
        f"=== ValidationEngineerA Report ===\n{validation_a_content}\n\n"
        f"=== ValidationEngineerB Report ===\n{validation_b_content}"
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
