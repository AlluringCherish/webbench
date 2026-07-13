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
# 20260713_210029_750350/main_20260713_210029_750350.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent complete Flask web application design specifications describing all 7 pages with exact routes, page titles, element IDs, navigation, and data fixtures; then merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently produce full design_spec candidates in parallel without access to each other's work; \"\n        \"DesignMerger compares both candidates and merges the best combined design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web applications.\n\nYour goal is to independently produce a complete design specification for a Flask web application covering all 7 pages, starting at Dashboard, enabling clear implementation of routes, UI, navigation, and data fixtures.\n\nTask Details:\n- Read the full user_task_description artifact for comprehensive understanding\n- Create design_candidate_a.md specifying all Flask routes for the 7 pages\n- Detail exact page titles and every UI element ID as described in the requirements\n- Specify navigation button mappings between pages with exact IDs and target routes\n- Define data fixture file formats with field order and example rows as per user task\n- Focus solely on the single candidate output artifact design_candidate_a.md without reading others\n\nSpecification Requirements:\n**Routes and Pages:**\n- Specify route URLs for each page, starting at the dashboard page '/'\n- Include route function names for clarity and consistency\n\n**Page Elements:**\n- For each page, list all UI element IDs exactly matching requirements\n- Identify static and dynamic element IDs, including patterns like control-device-button-{device_id}\n\n**Navigation:**\n- Map navigation buttons by their element IDs to corresponding route functions\n- Ensure navigational consistency across all pages\n\n**Data Fixtures:**\n- For each data file (users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt):\n  - Specify file path and pipe-delimited field order exactly\n  - Provide 2-3 sample data rows from requirements to illustrate format\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_candidate_a.md\n- Preserve exact names and spellings of all element IDs and page titles\n- Ensure all navigation mappings are clear and consistent\n- Provide comprehensive and realistic data fixture specifications\n- Do NOT read or incorporate any candidate B outputs or their artifacts\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in Flask web application design.\n\nYour goal is to independently create a comprehensive Flask app design covering all 7 pages, including explicit route definitions, exact page titles, all UI element IDs, navigation button mappings, and local data fixture references.\n\nTask Details:\n- Use the full user_task_description as input context\n- Produce an alternative full design specification named design_candidate_b.md\n- Define explicit Flask routes for each page, beginning with the dashboard at '/'\n- Include detailed and exact page titles for every page as listed in requirements\n- List all element IDs including dynamic buttons like control-device-button-{device_id}\n- Define navigation with button IDs linked to route functions uniformly\n- Specify fixture file names and their usage per feature section clearly\n\nCRITICAL REQUIREMENTS:\n- Output must be saved using write_text_file as design_candidate_b.md\n- Preserve all exact element IDs, page titles, and navigation mappings from the user description\n- Do NOT access or integrate design_candidate_a.md content\n- Provide complete and clear fixture file mapping consistent with user task's data storage section\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Software Architect specialized in consolidating design specifications for Flask web applications.\n\nYour goal is to compare two independently produced design candidates (design_candidate_a.md, design_candidate_b.md) and merge them into a single, coherent, and conflict-resolved design_spec.md covering all 7 pages with precise routes, page titles, element IDs, navigation mappings, and data fixture file usage.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md comprehensively\n- Identify and resolve any conflicts or omissions between both candidates\n- Produce a merged design_spec.md that:\n  - Defines exact Flask routes for all seven pages, starting at '/'\n  - Includes consistent and accurate page titles as per requirements\n  - Lists all UI element IDs exactly as specified, including dynamic patterns like control-device-button-{device_id}\n  - Maps all navigation buttons to their corresponding routes with correct element IDs\n  - Consolidates data fixture file paths, formats, field orders, and example rows clearly\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively for outputting design_spec.md\n- Ensure merged specification is complete and consistent for implementation\n- Maintain exact naming, casing, and field order from source materials\n- Deliver final output suitable for direct use by implementation engineers\n- Do NOT alter original file naming conventions or lose detail in merge\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for comprehensive coverage of all pages, clear element ID definitions, correct data fixture references, and navigation alignment with user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for completeness, accuracy of element IDs, navigation, and fixture consistency before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify that design_spec.md resolves all conflicts and defines exact routes, element IDs, page titles, navigation, and fixture usage for implementation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete Flask application bundles with app_candidate_x.py and templates_candidate_x/*.html enforcing routes, page titles, element IDs, navigation, local data fixture reading, and starting at dashboard page; then merge bundles into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently build full Flask app candidates (Python and templates) in parallel, \"\n        \"then ImplementationMerger integrates the best features and corrects conflicts into the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with expertise in building full-stack web apps using local text data storage.\n\nYour goal is to implement a full Flask application bundle including app_candidate_a.py and all required HTML templates under templates_candidate_a/, fully meeting the design specifications for SmartHomeManager.\n\nTask Details:\n- Read design_spec.md and user_task_description for comprehensive requirements\n- Implement all 7 specified pages and navigation starting from the dashboard page\n- Use Flask render_template to load templates from templates_candidate_a/\n- Read all necessary local data files from 'data/' folder with pipe-delimited parsing exactly as specified\n- Use exact requested element IDs and page titles for each page, strictly follow design and structure\n- Produce outputs: app_candidate_a.py and templates_candidate_a/*.html\n\nImplementation Requirements:\n1. **Flask Application Setup and Routing**\n   - Define all routes for the 7 pages according to design_spec.md\n   - Implement root route '/' to serve the dashboard page\n   - Use function names consistent with page purposes, lowercase with underscores\n   - Utilize render_template with templates_candidate_a/ paths matching page templates\n2. **Local Data Handling**\n   - Implement robust parsing of local text files in 'data/' directory with pipe '|' delimiter\n   - Follow exact field order and field names for users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt\n   - Handle missing or empty files gracefully with appropriate defaults (empty lists/dicts)\n3. **HTML Template Development**\n   - Create templates_candidate_a/*.html files with exact element IDs as specified\n   - Page titles must match exactly (e.g., \"Smart Home Dashboard\", \"My Devices\", etc.)\n   - Include all specified input fields, buttons, tables, and other elements with proper IDs\n4. **Navigation and Controls**\n   - Implement navigation buttons linking between pages as specified (e.g., device-list-button → device list page)\n   - Use Flask url_for functions for navigation in templates\n5. **Output Artifacts**\n   - Save final Flask app code as app_candidate_a.py using write_text_file\n   - Save all HTML templates under templates_candidate_a/ with exact file names and element IDs using write_text_file\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save all output files (app_candidate_a.py and templates_candidate_a/*.html)\n- MUST parse all data files strictly with pipe delimiter and exact field order from design_spec.md\n- MUST enforce all exact element IDs and page titles from design_spec.md (no deviations)\n- MUST implement full routing starting at '/' for dashboard page, consistent with user requirements\n- Output filenames: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications and templating, with a focus on adhering strictly to design specifications and local data-driven dynamic content.\n\nYour goal is to create an alternative complete implementation of the SmartHomeManager Flask app, producing app_candidate_b.py and HTML templates under templates_candidate_b/, fully complying with design_spec.md and user task requirements.\n\nTask Details:\n- Use design_spec.md and user_task_description as sole sources for implementation\n- Implement all 7 defined pages and enable navigation starting from the dashboard home page\n- Templates must reside in templates_candidate_b/ directory; use Flask render_template accordingly\n- Read local text data fixtures from the 'data/' directory with exact pipe-delimited parsing rules\n- Maintain exact element IDs and page titles for all pages as specified, no deviations allowed\n- Output two artifacts: app_candidate_b.py and templates_candidate_b/*.html files\n\nImplementation Requirements:\n1. **Full Flask Routing and Views**\n   - Define routes named consistently with page functions as per design_spec.md\n   - Ensure root '/' route delivers the dashboard view\n   - Implement all page handlers rendering templates_candidate_b/*.html templates\n2. **Data Loading from Local Files**\n   - Parse all required data files (users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt) with pipe delimiter\n   - Respect exact data field order and types, create appropriate data structures for template rendering\n   - Handle file read errors and missing data sensibly\n3. **HTML Templates**\n   - Create all required HTML template files in templates_candidate_b/ with required element IDs for inputs, buttons, tables, and display elements\n   - Titles on each page must exactly match the design spec requirements\n4. **Navigation and UI Controls**\n   - Implement navigation buttons and links as specified, use url_for for all routes in templates\n   - Include dynamic elements with proper Jinja2 syntax where applicable\n5. **Deliverables**\n   - Save implemented Flask application code as app_candidate_b.py via write_text_file\n   - Save all HTML templates under templates_candidate_b/ directory exactly named with specified elements\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_b.py and templates_candidate_b/*.html\n- MUST adhere strictly to the pipe-delimited data parsing and exact data field ordering\n- MUST implement all element IDs and page titles exactly as specified in design_spec.md\n- Application must start at dashboard page root route '/'\n- Do not read or depend on ImplementationEngineerA outputs\n- Output filenames: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Python Flask applications and front-end template consolidation.\n\nYour goal is to integrate candidate implementations app_candidate_a.py and app_candidate_b.py along with respective templates_candidate_a/*.html and templates_candidate_b/*.html into a final unified Flask app named app.py and templates/*.html fully complying with design_spec.md.\n\nTask Details:\n- Ingest design_spec.md, both sets of candidate implementations, and user_task_description\n- Merge route definitions from both candidates to form a complete, conflict-free app.py\n- Consolidate and harmonize HTML templates combining best features and enforcing exact element IDs and page titles\n- Ensure all navigation starts from dashboard page at root '/'\n- Ensure all local text data files in 'data/' folder are parsed using pipe-delimited format exactly as specified\n- Remove dependencies on candidate-specific template directories; templates/*.html must be self-contained and consistent\n- Validate usage of all navigation buttons, routes, data loading, and template content against design_spec.md\n\nImplementation Requirements:\n1. **App.py Merge**\n   - Analyze app_candidate_a.py and app_candidate_b.py for route implementations and data handling\n   - Resolve conflicts by selecting best practice implementations or merging logic as needed\n   - Maintain consistent function names for all routes as per design_spec.md\n2. **Templates Consolidation**\n   - Combine templates from templates_candidate_a/ and templates_candidate_b/\n   - Ensure all templates have exact element IDs as required without duplication or inconsistency\n   - Synchronize page titles exactly as specified\n3. **Data File Parsing**\n   - Unified data reading logic respecting pipe-delimited formats with exact field definitions from design_spec.md\n   - Ensure error handling and default data states are robust and unified\n4. **Navigation Integrity**\n   - Confirm all navigation buttons and links function correctly and use Flask's url_for system\n5. **Final Output**\n   - Save integrated Flask app as app.py\n   - Save consolidated HTML templates under templates/*.html\n   - Use write_text_file tool for all final outputs\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app.py and templates/*.html\n- Final outputs MUST fully comply with routes, page titles, element IDs, navigation flows, and local data fixture reading per design_spec.md\n- No references or dependencies on candidate-specific template folders should remain\n- Focus on merging correctness, consistency, and completeness\n- Output filenames: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess candidate A for compliance with design_spec.md regarding routes, element IDs, template structure, and local data file reads.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate B for correctness, completeness per design_spec.md, appropriate data file parsing, and Flask template usage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify final merged app.py and templates/*.html align strictly with design_spec.md and implement requested features with Python and Flask best practices.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two parallel independent validation passes producing validation_a.md and validation_b.md verifying correctness of app.py and templates/*.html; merge their repair suggestions into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate correctness, route accuracy, template IDs, navigation, local data access, and \"\n        \"functionality based on design_spec.md and run reports; RepairMerger consolidates reports to produce final corrected app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python backend and HTML template validation for Flask web applications.\n\nYour goal is to validate the syntax, route implementation, and template correctness of the backend and frontend codebases, producing a detailed validation report with repair suggestions.\n\nTask Details:\n- Read app.py and templates/*.html source files from ImplementationMerger\n- Consult design_spec.md for expected route definitions, page structures, and element IDs\n- Use user_task_description for overall context on page and data requirements\n- Produce validation_a.md including syntax checks, verification of all 7 pages with exact element IDs, route validation, and data parsing correctness\n\nValidation Requirements:\n1. **Syntax Validation**:\n   - Use validate_python_file tool to confirm app.py syntax and runtime correctness\n   - Report any syntax or runtime errors with line references\n\n2. **Route and Template Validation**:\n   - Verify the existence of all specified 7 pages with the exact required element IDs\n   - Confirm route handlers in app.py align with design_spec.md route paths and HTTP methods\n   - Ensure templates/*.html contain all required elements and IDs as per design_spec.md\n   - Validate local text file data parsing and field order matching design_spec.md data files\n\n3. **Report Content**:\n   - Document any missing routes, template elements, or mismatched IDs\n   - Provide actionable repair suggestions for every detected issue, referencing design_spec.md sections and line numbers if applicable\n   - Organize report in markdown with clear headings for each validation category\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file tool for syntax checking\n- Use execute_python_code tool for dynamic validations if needed\n- Use write_text_file tool to save validation_a.md\n- Report all issues specifically and provide clear repair instructions\n- Do not modify source code, only write validation report\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Quality Assurance Engineer specializing in full-stack verification of Flask applications and HTML/Jinja2 templates.\n\nYour goal is to independently verify the functional correctness and integration compliance of app.py and templates/*.html against design specifications, providing a detailed validation report with repair recommendations.\n\nTask Details:\n- Read app.py and templates/*.html from ImplementationMerger\n- Reference design_spec.md to verify presence of all required element IDs, page content, and data fixture handling\n- Use user_task_description to understand the SmartHomeManager application domain and expected workflows\n- Produce validation_b.md outlining tests of rendering correctness, route accessibility, data handling, and integration, giving clear repair recommendations\n\nVerification Checklist:\n1. **Rendering and Elements**:\n   - Confirm templates render without errors and include all design_spec.md specified element IDs and structure\n   - Validate dynamic elements like buttons with variable IDs follow correct patterns\n\n2. **Route Accessibility**:\n   - Verify all routes defined in app.py respond correctly and render corresponding pages\n   - Test navigation flows including buttons/link navigation among all 7 pages\n\n3. **Data Handling**:\n   - Check that data from local text files is loaded with correct field order and usage in both backend and frontend\n   - Analyze fixture handling for devices, automation rules, energy logs, and activity logs\n\n4. **Report Structure**:\n   - Document all found mismatches or missing features\n   - Provide detailed repair steps tied to design_spec.md references and source files\n   - Format report in markdown with clear sections\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for testing\n- Use write_text_file to save validation_b.md\n- Focus on independent verification from ValidationEngineerA report\n- Provide actionable and clear repair guidelines\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in consolidating validation reports and merging repair changes into final backend and frontend code.\n\nYour goal is to combine validation reports validation_a.md and validation_b.md, reconcile overlapping and conflicting repair suggestions, and produce final corrected app.py and templates/*.html implementing all design_spec.md requirements flawlessly.\n\nTask Details:\n- Read validation_a.md and validation_b.md to identify all repair instructions and overlapping issues\n- Read current app.py and templates/*.html from ImplementationMerger\n- Reference design_spec.md for full specifications on routes, templates, element IDs, data file formats, and page navigation\n- Use user_task_description for full context on SmartHomeManager functionality and data requirements\n- Produce updated and corrected app.py fully conformant to design_spec.md\n- Produce updated and corrected templates/*.html fully conformant to design_spec.md\n\nMerging Requirements:\n1. **Repair Prioritization**:\n   - Analyze both validation reports to merge fixes avoiding duplication\n   - Resolve conflicts by cross-checking design_spec.md and user_task_description\n\n2. **Code Update**:\n   - Implement all agreed fixes in app.py ensuring route correctness, data loading accuracy, and error-free execution\n   - Update templates/*.html files to include all missing or corrected element IDs and navigation controls\n\n3. **Output Deliverables**:\n   - Final app.py file with all accumulated corrections applied\n   - Final templates/*.html files with complete and correct markup and IDs\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html\n- Do not modify design_spec.md or validation reports\n- Ensure final outputs fully satisfy design_spec.md and pass all validation criteria\n- Maintain clean, readable code and templates with consistent naming conventions\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Confirm validation_a.md details precise and reproducible test results, repair suggestions aligned with design_spec.md that can be implemented.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"validation_a.md\"}]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Confirm validation_b.md provides thorough review results with actionable repair instructions coherent with validation_a.md findings.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"validation_b.md\"}]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure the final merged app.py and templates/*.html preserve the complete merged design_spec.md, resolve reported issues, and implement all requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'SmartHomeManager' Web Application

## 1. Objective
Develop a comprehensive web application named 'SmartHomeManager' using Python, with data managed through local text files. The application enables users to manage smart home devices, control them remotely, set automation rules, and monitor energy consumption. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'SmartHomeManager' application is Python.

## 3. Page Design

The 'SmartHomeManager' web application will consist of the following seven pages:

### 1. Dashboard Page
- **Page Title**: Smart Home Dashboard
- **Overview**: The main hub displaying overview of all devices, quick controls, and navigation to all functionality.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: device-summary** - Type: Div - Summary showing total devices, active devices, and offline devices count.
  - **ID: device-list-button** - Type: Button - Button to navigate to device list page.
  - **ID: add-device-button** - Type: Button - Button to navigate to add device page.
  - **ID: automation-button** - Type: Button - Button to navigate to automation rules page.
  - **ID: energy-button** - Type: Button - Button to navigate to energy report page.
  - **ID: activity-button** - Type: Button - Button to navigate to activity logs page.
  - **ID: room-list** - Type: Div - List of all rooms with device counts, displayed as a dashboard section.

### 2. Device List Page
- **Page Title**: My Devices
- **Overview**: A page displaying all registered smart devices with their status and quick controls.
- **Elements**:
  - **ID: device-list-page** - Type: Div - Container for the device list page.
  - **ID: device-table** - Type: Table - Table displaying all devices with name, type, room, status, and actions.
  - **ID: control-device-button-{device_id}** - Type: Button - Button to navigate to device control page (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Add Device Page
- **Page Title**: Add New Device
- **Overview**: A page for users to register a new smart device.
- **Elements**:
  - **ID: add-device-page** - Type: Div - Container for the add device page.
  - **ID: device-name** - Type: Input - Field to input device name.
  - **ID: device-type** - Type: Dropdown - Dropdown to select device type (Light, Thermostat, Camera, Lock, Sensor, Appliance).
  - **ID: device-room** - Type: Dropdown - Dropdown to select room (Living Room, Bedroom, Kitchen, Bathroom, Garage).
  - **ID: submit-device-button** - Type: Button - Button to submit the new device.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Device Control Page
- **Page Title**: Device Control
- **Overview**: A page for controlling a specific device with detailed settings.
- **Elements**:
  - **ID: device-control-page** - Type: Div - Container for the device control page.
  - **ID: device-name-display** - Type: H2 - Display device name.
  - **ID: device-status-display** - Type: Div - Display current device status (Online/Offline).
  - **ID: power-toggle** - Type: Button - Button to toggle device power on/off.
  - **ID: save-settings-button** - Type: Button - Button to save device settings.
  - **ID: back-to-devices** - Type: Button - Button to navigate back to device list.

### 5. Automation Rules Page
- **Page Title**: Automation Rules
- **Overview**: A page for creating and managing automation rules for devices.
- **Elements**:
  - **ID: automation-page** - Type: Div - Container for the automation rules page.
  - **ID: rules-table** - Type: Table - Table displaying all automation rules with name, trigger, action, and status.
  - **ID: rule-name** - Type: Input - Field to input rule name.
  - **ID: trigger-type** - Type: Dropdown - Dropdown to select trigger type (Time, Motion, Temperature).
  - **ID: trigger-value** - Type: Input - Field to input trigger value (e.g., time or threshold).
  - **ID: action-device** - Type: Dropdown - Dropdown to select target device.
  - **ID: action-type** - Type: Dropdown - Dropdown to select action type (Turn On, Turn Off, Set Brightness, Set Temperature).
  - **ID: add-rule-button** - Type: Button - Button to add new automation rule.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Energy Report Page
- **Page Title**: Energy Report
- **Overview**: A page displaying energy consumption data and statistics for all devices.
- **Elements**:
  - **ID: energy-page** - Type: Div - Container for the energy report page.
  - **ID: energy-summary** - Type: Div - Summary showing total energy consumption and cost estimate.
  - **ID: energy-table** - Type: Table - Table displaying energy consumption per device with date and kWh.
  - **ID: date-filter** - Type: Input (date) - Field to filter energy data by date.
  - **ID: apply-filter-button** - Type: Button - Button to apply date filter.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Activity Logs Page
- **Page Title**: Activity Logs
- **Overview**: A page displaying all device activity logs and system events.
- **Elements**:
  - **ID: activity-page** - Type: Div - Container for the activity logs page.
  - **ID: activity-table** - Type: Table - Table displaying activity logs with timestamp, device, action, and details.
  - **ID: search-activity** - Type: Input - Field to search activity logs.
  - **ID: apply-search-button** - Type: Button - Button to apply search filter.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'SmartHomeManager' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email
  ```
- **Example Data**:
  ```
  john_doe|john@example.com
  jane_smith|jane@example.com
  ```

### 2. Device Data
- **File Name**: `devices.txt`
- **Data Format**:
  ```
  username|device_id|device_name|device_type|room|brand|model|status|power|brightness|temperature|mode|schedule_time
  ```
- **Example Data**:
  ```
  john_doe|1|Living Room Light|Light|Living Room|Philips|Hue|Online|on|75|||Auto|
  john_doe|2|Bedroom Thermostat|Thermostat|Bedroom|Nest|Learning|Online|on||72|Auto|22:00
  jane_smith|3|Kitchen Camera|Camera|Kitchen|Ring|Indoor|Online|on||||Manual|
  ```

### 3. Room Data
- **File Name**: `rooms.txt`
- **Data Format**:
  ```
  username|room_id|room_name
  ```
- **Example Data**:
  ```
  john_doe|1|Living Room
  john_doe|2|Bedroom
  john_doe|3|Kitchen
  jane_smith|1|Living Room
  ```

### 4. Automation Rules Data
- **File Name**: `automation_rules.txt`
- **Data Format**:
  ```
  username|rule_id|rule_name|trigger_type|trigger_value|action_device_id|action_type|action_value|enabled
  ```
- **Example Data**:
  ```
  john_doe|1|Morning Lights|Time|07:00|1|Turn On||true
  john_doe|2|Night Mode|Time|22:00|1|Set Brightness|20|true
  jane_smith|1|Motion Alert|Motion|detected|3|Turn On||true
  ```

### 5. Energy Consumption Logs
- **File Name**: `energy_logs.txt`
- **Data Format**:
  ```
  username|device_id|date|consumption_kwh
  ```
- **Example Data**:
  ```
  john_doe|1|2024-11-01|0.5
  john_doe|2|2024-11-01|2.3
  john_doe|1|2024-11-02|0.6
  jane_smith|3|2024-11-01|0.2
  ```

### 6. Activity Logs
- **File Name**: `activity_logs.txt`
- **Data Format**:
  ```
  username|timestamp|device_id|action|details
  ```
- **Example Data**:
  ```
  john_doe|2024-11-01 07:00:00|1|Power On|Automation triggered: Morning Lights
  john_doe|2024-11-01 08:30:00|2|Settings Changed|Temperature set to 72
  jane_smith|2024-11-01 09:15:00|3|Power On|Manual control
  ```

All files will be saved in the `data` directory to ensure organization and easy access. The format uses a pipe (`|`) delimiter for better readability and parsing. Different types of data will be isolated to ensure efficient data management and retrieval.
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
            """You are a Software Architect specializing in Flask web applications.

Your goal is to independently produce a complete design specification for a Flask web application covering all 7 pages, starting at Dashboard, enabling clear implementation of routes, UI, navigation, and data fixtures.

Task Details:
- Read the full user_task_description artifact for comprehensive understanding
- Create design_candidate_a.md specifying all Flask routes for the 7 pages
- Detail exact page titles and every UI element ID as described in the requirements
- Specify navigation button mappings between pages with exact IDs and target routes
- Define data fixture file formats with field order and example rows as per user task
- Focus solely on the single candidate output artifact design_candidate_a.md without reading others

Specification Requirements:
**Routes and Pages:**
- Specify route URLs for each page, starting at the dashboard page '/'
- Include route function names for clarity and consistency

**Page Elements:**
- For each page, list all UI element IDs exactly matching requirements
- Identify static and dynamic element IDs, including patterns like control-device-button-{device_id}

**Navigation:**
- Map navigation buttons by their element IDs to corresponding route functions
- Ensure navigational consistency across all pages

**Data Fixtures:**
- For each data file (users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt):
  - Specify file path and pipe-delimited field order exactly
  - Provide 2-3 sample data rows from requirements to illustrate format

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_candidate_a.md
- Preserve exact names and spellings of all element IDs and page titles
- Ensure all navigation mappings are clear and consistent
- Provide comprehensive and realistic data fixture specifications
- Do NOT read or incorporate any candidate B outputs or their artifacts

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Architect specializing in Flask web application design.

Your goal is to independently create a comprehensive Flask app design covering all 7 pages, including explicit route definitions, exact page titles, all UI element IDs, navigation button mappings, and local data fixture references.

Task Details:
- Use the full user_task_description as input context
- Produce an alternative full design specification named design_candidate_b.md
- Define explicit Flask routes for each page, beginning with the dashboard at '/'
- Include detailed and exact page titles for every page as listed in requirements
- List all element IDs including dynamic buttons like control-device-button-{device_id}
- Define navigation with button IDs linked to route functions uniformly
- Specify fixture file names and their usage per feature section clearly

CRITICAL REQUIREMENTS:
- Output must be saved using write_text_file as design_candidate_b.md
- Preserve all exact element IDs, page titles, and navigation mappings from the user description
- Do NOT access or integrate design_candidate_a.md content
- Provide complete and clear fixture file mapping consistent with user task's data storage section

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Software Architect specialized in consolidating design specifications for Flask web applications.

Your goal is to compare two independently produced design candidates (design_candidate_a.md, design_candidate_b.md) and merge them into a single, coherent, and conflict-resolved design_spec.md covering all 7 pages with precise routes, page titles, element IDs, navigation mappings, and data fixture file usage.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md comprehensively
- Identify and resolve any conflicts or omissions between both candidates
- Produce a merged design_spec.md that:
  - Defines exact Flask routes for all seven pages, starting at '/'
  - Includes consistent and accurate page titles as per requirements
  - Lists all UI element IDs exactly as specified, including dynamic patterns like control-device-button-{device_id}
  - Maps all navigation buttons to their corresponding routes with correct element IDs
  - Consolidates data fixture file paths, formats, field orders, and example rows clearly

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively for outputting design_spec.md
- Ensure merged specification is complete and consistent for implementation
- Maintain exact naming, casing, and field order from source materials
- Deliver final output suitable for direct use by implementation engineers
- Do NOT alter original file naming conventions or lose detail in merge

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with expertise in building full-stack web apps using local text data storage.

Your goal is to implement a full Flask application bundle including app_candidate_a.py and all required HTML templates under templates_candidate_a/, fully meeting the design specifications for SmartHomeManager.

Task Details:
- Read design_spec.md and user_task_description for comprehensive requirements
- Implement all 7 specified pages and navigation starting from the dashboard page
- Use Flask render_template to load templates from templates_candidate_a/
- Read all necessary local data files from 'data/' folder with pipe-delimited parsing exactly as specified
- Use exact requested element IDs and page titles for each page, strictly follow design and structure
- Produce outputs: app_candidate_a.py and templates_candidate_a/*.html

Implementation Requirements:
1. **Flask Application Setup and Routing**
   - Define all routes for the 7 pages according to design_spec.md
   - Implement root route '/' to serve the dashboard page
   - Use function names consistent with page purposes, lowercase with underscores
   - Utilize render_template with templates_candidate_a/ paths matching page templates
2. **Local Data Handling**
   - Implement robust parsing of local text files in 'data/' directory with pipe '|' delimiter
   - Follow exact field order and field names for users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt
   - Handle missing or empty files gracefully with appropriate defaults (empty lists/dicts)
3. **HTML Template Development**
   - Create templates_candidate_a/*.html files with exact element IDs as specified
   - Page titles must match exactly (e.g., "Smart Home Dashboard", "My Devices", etc.)
   - Include all specified input fields, buttons, tables, and other elements with proper IDs
4. **Navigation and Controls**
   - Implement navigation buttons linking between pages as specified (e.g., device-list-button → device list page)
   - Use Flask url_for functions for navigation in templates
5. **Output Artifacts**
   - Save final Flask app code as app_candidate_a.py using write_text_file
   - Save all HTML templates under templates_candidate_a/ with exact file names and element IDs using write_text_file

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save all output files (app_candidate_a.py and templates_candidate_a/*.html)
- MUST parse all data files strictly with pipe delimiter and exact field order from design_spec.md
- MUST enforce all exact element IDs and page titles from design_spec.md (no deviations)
- MUST implement full routing starting at '/' for dashboard page, consistent with user requirements
- Output filenames: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications and templating, with a focus on adhering strictly to design specifications and local data-driven dynamic content.

Your goal is to create an alternative complete implementation of the SmartHomeManager Flask app, producing app_candidate_b.py and HTML templates under templates_candidate_b/, fully complying with design_spec.md and user task requirements.

Task Details:
- Use design_spec.md and user_task_description as sole sources for implementation
- Implement all 7 defined pages and enable navigation starting from the dashboard home page
- Templates must reside in templates_candidate_b/ directory; use Flask render_template accordingly
- Read local text data fixtures from the 'data/' directory with exact pipe-delimited parsing rules
- Maintain exact element IDs and page titles for all pages as specified, no deviations allowed
- Output two artifacts: app_candidate_b.py and templates_candidate_b/*.html files

Implementation Requirements:
1. **Full Flask Routing and Views**
   - Define routes named consistently with page functions as per design_spec.md
   - Ensure root '/' route delivers the dashboard view
   - Implement all page handlers rendering templates_candidate_b/*.html templates
2. **Data Loading from Local Files**
   - Parse all required data files (users.txt, devices.txt, rooms.txt, automation_rules.txt, energy_logs.txt, activity_logs.txt) with pipe delimiter
   - Respect exact data field order and types, create appropriate data structures for template rendering
   - Handle file read errors and missing data sensibly
3. **HTML Templates**
   - Create all required HTML template files in templates_candidate_b/ with required element IDs for inputs, buttons, tables, and display elements
   - Titles on each page must exactly match the design spec requirements
4. **Navigation and UI Controls**
   - Implement navigation buttons and links as specified, use url_for for all routes in templates
   - Include dynamic elements with proper Jinja2 syntax where applicable
5. **Deliverables**
   - Save implemented Flask application code as app_candidate_b.py via write_text_file
   - Save all HTML templates under templates_candidate_b/ directory exactly named with specified elements

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_b.py and templates_candidate_b/*.html
- MUST adhere strictly to the pipe-delimited data parsing and exact data field ordering
- MUST implement all element IDs and page titles exactly as specified in design_spec.md
- Application must start at dashboard page root route '/'
- Do not read or depend on ImplementationEngineerA outputs
- Output filenames: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Python Flask applications and front-end template consolidation.

Your goal is to integrate candidate implementations app_candidate_a.py and app_candidate_b.py along with respective templates_candidate_a/*.html and templates_candidate_b/*.html into a final unified Flask app named app.py and templates/*.html fully complying with design_spec.md.

Task Details:
- Ingest design_spec.md, both sets of candidate implementations, and user_task_description
- Merge route definitions from both candidates to form a complete, conflict-free app.py
- Consolidate and harmonize HTML templates combining best features and enforcing exact element IDs and page titles
- Ensure all navigation starts from dashboard page at root '/'
- Ensure all local text data files in 'data/' folder are parsed using pipe-delimited format exactly as specified
- Remove dependencies on candidate-specific template directories; templates/*.html must be self-contained and consistent
- Validate usage of all navigation buttons, routes, data loading, and template content against design_spec.md

Implementation Requirements:
1. **App.py Merge**
   - Analyze app_candidate_a.py and app_candidate_b.py for route implementations and data handling
   - Resolve conflicts by selecting best practice implementations or merging logic as needed
   - Maintain consistent function names for all routes as per design_spec.md
2. **Templates Consolidation**
   - Combine templates from templates_candidate_a/ and templates_candidate_b/
   - Ensure all templates have exact element IDs as required without duplication or inconsistency
   - Synchronize page titles exactly as specified
3. **Data File Parsing**
   - Unified data reading logic respecting pipe-delimited formats with exact field definitions from design_spec.md
   - Ensure error handling and default data states are robust and unified
4. **Navigation Integrity**
   - Confirm all navigation buttons and links function correctly and use Flask's url_for system
5. **Final Output**
   - Save integrated Flask app as app.py
   - Save consolidated HTML templates under templates/*.html
   - Use write_text_file tool for all final outputs

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app.py and templates/*.html
- Final outputs MUST fully comply with routes, page titles, element IDs, navigation flows, and local data fixture reading per design_spec.md
- No references or dependencies on candidate-specific template folders should remain
- Focus on merging correctness, consistency, and completeness
- Output filenames: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python backend and HTML template validation for Flask web applications.

Your goal is to validate the syntax, route implementation, and template correctness of the backend and frontend codebases, producing a detailed validation report with repair suggestions.

Task Details:
- Read app.py and templates/*.html source files from ImplementationMerger
- Consult design_spec.md for expected route definitions, page structures, and element IDs
- Use user_task_description for overall context on page and data requirements
- Produce validation_a.md including syntax checks, verification of all 7 pages with exact element IDs, route validation, and data parsing correctness

Validation Requirements:
1. **Syntax Validation**:
   - Use validate_python_file tool to confirm app.py syntax and runtime correctness
   - Report any syntax or runtime errors with line references

2. **Route and Template Validation**:
   - Verify the existence of all specified 7 pages with the exact required element IDs
   - Confirm route handlers in app.py align with design_spec.md route paths and HTTP methods
   - Ensure templates/*.html contain all required elements and IDs as per design_spec.md
   - Validate local text file data parsing and field order matching design_spec.md data files

3. **Report Content**:
   - Document any missing routes, template elements, or mismatched IDs
   - Provide actionable repair suggestions for every detected issue, referencing design_spec.md sections and line numbers if applicable
   - Organize report in markdown with clear headings for each validation category

CRITICAL REQUIREMENTS:
- Use validate_python_file tool for syntax checking
- Use execute_python_code tool for dynamic validations if needed
- Use write_text_file tool to save validation_a.md
- Report all issues specifically and provide clear repair instructions
- Do not modify source code, only write validation report

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Quality Assurance Engineer specializing in full-stack verification of Flask applications and HTML/Jinja2 templates.

Your goal is to independently verify the functional correctness and integration compliance of app.py and templates/*.html against design specifications, providing a detailed validation report with repair recommendations.

Task Details:
- Read app.py and templates/*.html from ImplementationMerger
- Reference design_spec.md to verify presence of all required element IDs, page content, and data fixture handling
- Use user_task_description to understand the SmartHomeManager application domain and expected workflows
- Produce validation_b.md outlining tests of rendering correctness, route accessibility, data handling, and integration, giving clear repair recommendations

Verification Checklist:
1. **Rendering and Elements**:
   - Confirm templates render without errors and include all design_spec.md specified element IDs and structure
   - Validate dynamic elements like buttons with variable IDs follow correct patterns

2. **Route Accessibility**:
   - Verify all routes defined in app.py respond correctly and render corresponding pages
   - Test navigation flows including buttons/link navigation among all 7 pages

3. **Data Handling**:
   - Check that data from local text files is loaded with correct field order and usage in both backend and frontend
   - Analyze fixture handling for devices, automation rules, energy logs, and activity logs

4. **Report Structure**:
   - Document all found mismatches or missing features
   - Provide detailed repair steps tied to design_spec.md references and source files
   - Format report in markdown with clear sections

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for testing
- Use write_text_file to save validation_b.md
- Focus on independent verification from ValidationEngineerA report
- Provide actionable and clear repair guidelines

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in consolidating validation reports and merging repair changes into final backend and frontend code.

Your goal is to combine validation reports validation_a.md and validation_b.md, reconcile overlapping and conflicting repair suggestions, and produce final corrected app.py and templates/*.html implementing all design_spec.md requirements flawlessly.

Task Details:
- Read validation_a.md and validation_b.md to identify all repair instructions and overlapping issues
- Read current app.py and templates/*.html from ImplementationMerger
- Reference design_spec.md for full specifications on routes, templates, element IDs, data file formats, and page navigation
- Use user_task_description for full context on SmartHomeManager functionality and data requirements
- Produce updated and corrected app.py fully conformant to design_spec.md
- Produce updated and corrected templates/*.html fully conformant to design_spec.md

Merging Requirements:
1. **Repair Prioritization**:
   - Analyze both validation reports to merge fixes avoiding duplication
   - Resolve conflicts by cross-checking design_spec.md and user_task_description

2. **Code Update**:
   - Implement all agreed fixes in app.py ensuring route correctness, data loading accuracy, and error-free execution
   - Update templates/*.html files to include all missing or corrected element IDs and navigation controls

3. **Output Deliverables**:
   - Final app.py file with all accumulated corrections applied
   - Final templates/*.html files with complete and correct markup and IDs

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html
- Do not modify design_spec.md or validation reports
- Ensure final outputs fully satisfy design_spec.md and pass all validation criteria
- Maintain clean, readable code and templates with consistent naming conventions

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
        ("DesignMerger", """Check design_candidate_a.md for comprehensive coverage of all pages, clear element ID definitions, correct data fixture references, and navigation alignment with user requirements.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for completeness, accuracy of element IDs, navigation, and fixture consistency before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify that design_spec.md resolves all conflicts and defines exact routes, element IDs, page titles, navigation, and fixture usage for implementation.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Assess candidate A for compliance with design_spec.md regarding routes, element IDs, template structure, and local data file reads.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate candidate B for correctness, completeness per design_spec.md, appropriate data file parsing, and Flask template usage.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify final merged app.py and templates/*.html align strictly with design_spec.md and implement requested features with Python and Flask best practices.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Confirm validation_a.md details precise and reproducible test results, repair suggestions aligned with design_spec.md that can be implemented.""", [{'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Confirm validation_b.md provides thorough review results with actionable repair instructions coherent with validation_a.md findings.""", [{'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Ensure the final merged app.py and templates/*.html preserve the complete merged design_spec.md, resolve reported issues, and implement all requirements.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
    # Create agents
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

    # Parallel generation of design candidates by DesignAnalystA and DesignAnalystB
    await asyncio.gather(
        execute(DesignAnalystA, "Produce complete Flask web app design specification for all 7 pages and output design_candidate_a.md"),
        execute(DesignAnalystB, "Produce complete Flask web app design specification alternative for all 7 pages and output design_candidate_b.md")
    )

    # Read outputs of both candidates for merger
    design_candidate_a_content, design_candidate_b_content = "", ""
    try:
        design_candidate_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge design candidates into unified design_spec.md
    await execute(DesignMerger,
                  f"=== DesignCandidateA ===\n{design_candidate_a_content}\n\n"
                  f"=== DesignCandidateB ===\n{design_candidate_b_content}")
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
        recovery_time=50
    )

    # Parallel execution of candidate implementations
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full Flask app and templates in templates_candidate_a/ based on design_spec.md and user_task_description. "
                "Save outputs: app_candidate_a.py and templates_candidate_a/*.html."),
        execute(ImplementationEngineerB,
                "Implement full Flask app and templates in templates_candidate_b/ based on design_spec.md and user_task_description. "
                "Save outputs: app_candidate_b.py and templates_candidate_b/*.html.")
    )

    # Read outputs from candidates for merging
    app_candidate_a_code, app_candidate_b_code = "", ""
    templates_candidate_a, templates_candidate_b = "", ""
    try:
        app_candidate_a_code = open("app_candidate_a.py", "r").read()
    except Exception:
        pass
    try:
        app_candidate_b_code = open("app_candidate_b.py", "r").read()
    except Exception:
        pass
    try:
        templates_candidate_a = open("templates_candidate_a/index.html").read()
    except Exception:
        # Fallback reading or empty if missing
        templates_candidate_a = ""
    try:
        templates_candidate_b = open("templates_candidate_b/index.html").read()
    except Exception:
        templates_candidate_b = ""

    # Merge candidate implementations into final app.py and templates/*.html
    await execute(ImplementationMerger,
                  f"=== design_spec.md ===\n"
                  f"{CONTEXT.get('design_spec.md', [{'content': ''}])[-1]['content'] if CONTEXT.get('design_spec.md') else ''}\n\n"
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a/index.html sample ===\n{templates_candidate_a}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b/index.html sample ===\n{templates_candidate_b}\n\n"
                  f"=== user_task_description ===\n"
                  f"{CONTEXT.get('user_task_description', [{'content': ''}])[-1]['content'] if CONTEXT.get('user_task_description') else ''}\n\n"
                  f"Integrate and merge the above candidates into a final, unified Flask app.py and templates/*.html files "
                  f"fully complying with design_spec.md, enforcing exact element IDs, page titles, navigation routes as required.")
# Phase2_End

# Phase3_Start

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

    # Parallel validation by two independent engineers
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate app.py and templates/*.html syntax, routes, element IDs, navigation, and data parsing "
                "against design_spec.md and user_task_description. Produce validation_a.md."),
        execute(ValidationEngineerB,
                "Independently verify rendering correctness, route accessibility, data handling, and integration "
                "based on app.py, templates/*.html, design_spec.md, and user_task_description. Produce validation_b.md.")
    )

    # Read validation reports for merger
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # Merge validation reports and produce final corrected app.py and templates/*.html
    await execute(RepairMerger,
                  f"=== validation_a.md ===\n{validation_a_content}\n\n"
                  f"=== validation_b.md ===\n{validation_b_content}")
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
