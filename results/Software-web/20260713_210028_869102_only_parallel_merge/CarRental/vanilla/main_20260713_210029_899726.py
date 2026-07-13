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
# 20260713_210029_899726/main_20260713_210029_899726.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent design candidates detailing all Flask routes, page elements, and navigation per the CarRental requirements, then merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAgentA and DesignAgentB independently generate comprehensive Flask web app design documents including routes, \"\n        \"page titles, element IDs, data storage and handling strategies, and navigation. DesignMerger then consolidates both \"\n        \"design candidates into a single unified design_spec.md file that ensures compatibility and full coverage of requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAgentA\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in designing Flask web applications.\n\nYour goal is to draft a complete Flask application design candidate covering all specified pages with full route definitions, exact page titles, element IDs, navigation actions, and data file interaction strategies within the 'data/' directory, along with UI/UX details as per the CarRental requirements.\n\nTask Details:\n- Read the user_task_description to understand all CarRental requirements\n- Produce design_candidate_a.md documenting all nine pages, including:\n  - Flask route paths and methods\n  - Exact page titles matching requirements\n  - All HTML element IDs per page (static and dynamic)\n  - Button actions, navigation links, and expected user flows\n  - Data storage strategy with reading and writing to specified text files under 'data/'\n  - UI/UX considerations consistent with the app's purpose and usability\n\nDesign Document Requirements:\n1. **Routes and Views**:\n   - Define route URL paths for each page, using RESTful conventions\n   - Assign meaningful function names in snake_case\n   - Specify HTTP methods (GET, POST) per route\n\n2. **Page Elements**:\n   - List all required element IDs per page exactly as in specifications\n   - Detail dynamic IDs with variable placeholders (e.g., view-details-button-{vehicle_id})\n\n3. **Navigation and Actions**:\n   - Describe button/link navigation targets using Flask url_for function names\n   - Specify user interaction flows (e.g., from booking page to insurance options)\n\n4. **Data Handling**:\n   - Map each data file to its usage context (reading, writing)\n   - Use pipe-delimited formats as specified in the task\n   - Include protocols for data validation and error handling\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save the output as design_candidate_a.md\n- Ensure all design details conform strictly to the CarRental requirements\n- Do NOT refer to or incorporate design_candidate_b.md content\n- Output filename must be exactly design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAgentB\",\n            \"prompt\": \"\"\"You are a Software Architect specialized in Flask web application design.\n\nYour goal is to independently create a comprehensive Flask web app design candidate covering all CarRental requirements, including precise route definitions, exact HTML element IDs, data storage interactions with local text files, and navigation schemas.\n\nTask Details:\n- Parse user_task_description thoroughly for full requirements comprehension\n- Write design_candidate_b.md including:\n  - All route paths and HTTP methods for the nine specified pages\n  - Exact matching page titles and container element IDs\n  - Specific dynamic element ID patterns for buttons and inputs (e.g., select-insurance-{insurance_id})\n  - User interaction sequences and navigation link mappings using Flask url_for\n  - Data file usage with detailed read/write formats and locations under 'data/'\n\nDesign Document Expectations:\n1. **Flask Routes**:\n   - Define all URLs and corresponding view function names clearly and consistently\n   - Specify GET or POST usage appropriately\n\n2. **Page Structure**:\n   - Enumerate all element IDs, with explanations when needed\n   - Capture both static and dynamic IDs precisely\n\n3. **Navigation Actions**:\n   - Map each button or interactive element to target routes\n   - Illustrate navigation flow through the app\n\n4. **Data File Handling**:\n   - Detail how each data file is accessed and updated\n   - Emphasize pipe-delimited format adherence and data integrity checks\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to write design_candidate_b.md\n- Do NOT access or incorporate content from design_candidate_a.md\n- Provide standalone design addressing the entire CarRental spec\n- Name output file exactly design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Software Architect with expertise in consolidating multiple design documents into a unified specification for Flask applications.\n\nYour goal is to review design_candidate_a.md and design_candidate_b.md, identify and resolve any conflicts or omissions, and produce a final merged design_spec.md that encompasses all Flask routes, page elements, button actions, navigation links, template structures, and data file read/write protocols required for the CarRental application.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md fully\n- Analyze overlap and discrepancies in:\n  - Flask route definitions, URL paths, methods, and function names\n  - Page titles and all element IDs, ensuring full coverage of all required pages\n  - Navigation flows, button/link actions, and user journey consistency\n  - Data storage handling for all specified text files, formats, and access methods\n- Merge content preserving all unique elements and reconciling differences to maintain completeness and clarity\n- Structure design_spec.md logically and clearly for implementation teams\n\nMerged Design Requirements:\n1. **Unified Flask Routes**:\n   - Comprehensive route list with consistent naming conventions and HTTP methods\n2. **Page Elements and Templates**:\n   - Inclusive enumeration of all element IDs (static and dynamic)\n   - Navigation mappings with Flask url_for references intact\n3. **Data File Access**:\n   - Clear protocols for reading and writing with pipe-delimited format adherence\n   - Illustrate which routes/pages interact with which files\n4. **Consistency and Clarity**:\n   - Avoid redundancies and contradictions\n   - Ensure final document is ready for direct implementation\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save merged output as design_spec.md\n- Output must be comprehensive and consistent, addressing all user_task_description requirements\n- Resolve conflicts and fill gaps present in source candidates\n- File name must exactly be design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAgentA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAgentB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAgentA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for complete route, page title, element ID coverage, navigation accuracy, and data file interaction strategies.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAgentB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for comprehensive Flask app design including all required pages, UI elements, and data access details.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify that the merged design_spec.md is coherent, fully detailed, and ready for precise implementation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete Python Flask app implementations with templates based on design_spec.md, then merge into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently create full Flask app implementations, including app.py and templates/*, \"\n        \"enforcing all routes, page titles, element IDs, buttons, and data file usage as per design_spec.md without seeing each other's work. \"\n        \"ImplementationMerger consolidates both implementations into final app.py and templates/*.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building web applications with data file integration.\n\nYour goal is to independently implement a fully functional Flask app including app.py and all required HTML templates.\n\nTask Details:\n- Read user_task_description and design_spec.md from DesignMerger\n- Implement app_candidate_a.py with all Flask routes, no-auth access, and flexible parsing of data files under data/\n- Create all page templates in templates_candidate_a/ with correct page titles, element IDs, buttons, and visible user messages\n- Do NOT access or refer to ImplementationEngineerB outputs or code\n\nImplementation Guidelines:\n1. **Flask Application**\n   - Follow design_spec.md specifications strictly for route paths, function names, HTTP methods, and template rendering.\n   - Implement routes for dashboard, vehicle search, vehicle details, booking, insurance selection, rental history, reservations management, special requests, and locations pages.\n   - Use flexible yet precise parsing of pipe-delimited data files from the data/ directory.\n   - Handle file I/O gracefully and maintain direct no-auth access to all pages.\n\n2. **Templates**\n   - Create all HTML templates in templates_candidate_a/ directory matching design_spec.md element IDs exactly.\n   - Include page titles in both <title> and <h1> tags.\n   - Use Jinja2 templating syntax for dynamic content rendering.\n   - Ensure buttons and interactive elements have stable actionable IDs per spec.\n\n3. **General**\n   - Provide visible messages and UI statuses as required by the spec.\n   - Follow best practices for Flask app structure and template organization.\n   - Avoid referencing or reading any artifacts or outputs from ImplementationEngineerB.\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_a.py and all templates under templates_candidate_a/\n- Follow design_spec.md strictly for routes, IDs, and file data handling\n- Ensure all pages are accessible without authentication\n- Output filenames: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specialized in developing web applications with a focus on UI fidelity and data integration.\n\nYour goal is to produce an independent, complete Flask app implementation including app_candidate_b.py and all required HTML templates.\n\nTask Details:\n- Read user_task_description and design_spec.md from DesignMerger\n- Implement app_candidate_b.py implementing all required Flask routes strictly according to the specification, including no-auth direct access\n- Create all templates in templates_candidate_b/ with exact page titles, element IDs, buttons, and UI behaviors described in design_spec.md\n- Do NOT refer to or read ImplementationEngineerA's code or templates\n\nImplementation Guidelines:\n1. **Flask Backend**\n   - Strictly follow routes, parameter handling, data file parsing, and template rendering rules as stated in design_spec.md.\n   - Ensure robustness in reading and processing local data files in data/ directory.\n   - Enforce all navigation and interactive features with stable actionable IDs.\n\n2. **Frontend Templates**\n   - Develop templates using Jinja2 syntax with exact IDs as per design_spec.md under templates_candidate_b/\n   - Include page titles consistently in <title> and <h1> tags\n   - Ensure all user interactions like booking, insurance selection, reservations management, and special requests work via visible UI elements with proper IDs.\n\n3. **General**\n   - Provide clear UI feedback and status messages on pages.\n   - Maintain separation from any outputs or knowledge of ImplementationEngineerA's work.\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/\n- Follow design_spec.md for precise routing, templates, element IDs, and data handling\n- Ensure all routes are accessible with no authentication\n- Output filenames: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\", \"execute_python_code\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging independent Flask application implementations.\n\nYour goal is to consolidate two independent Flask app implementations into a single final app.py and unified templates/*.html that fully conform to design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md from DesignMerger\n- Compare and merge app_candidate_a.py and app_candidate_b.py into one complete, conflict-free app.py\n- Compare and merge templates_candidate_a/*.html and templates_candidate_b/*.html, resolving conflicts and preserving strongest correct features into templates/*.html\n- Ensure all routes, page titles, element IDs, buttons, and complete data file handling are correctly preserved and unified\n- Maintain direct no-auth URLs and visible status messages as per spec\n\nMerging Guidelines:\n1. **Backend Merge**\n   - Identify route implementations, data loading, and business logic in both candidates.\n   - Resolve conflicts by selecting the best or most complete code per route and data handling.\n   - Ensure the merged app.py matches design_spec.md requirements fully.\n\n2. **Templates Merge**\n   - For each template, compare both versions closely.\n   - Keep exact element IDs as per design_spec.md.\n   - Retain all interactive elements, page titles in <title> and <h1>, and UI feedback.\n   - Synthesize best structures and styles, resolving conflicts carefully.\n\n3. **Validation Preparation**\n   - Prepare merged outputs so they can be validated against design_spec.md.\n   - Ensure no merged outputs contain remnants of candidate identifiers or conflicting IDs.\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save final app.py and templates/*.html\n- Final outputs must fully comply with design_spec.md on routes, UI, data file usage, and no-auth access\n- Preserve and consolidate all visible user messages and statuses\n- Output filenames: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate A for correct implementation of Flask routes, element IDs, no-auth access, and data file handling per design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess candidate B's implementation for feature completeness, route correctness, template fidelity, and data storage integration.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify merged app.py and templates/*.html conform fully with design_spec.md and are ready for testing and validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Conduct two independent validations producing validation reports, then merge repair suggestions to produce final tested app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently verify app.py and templates/*.html for syntax correctness, startup behavior, route accessibility, \"\n        \"HTML element presence and correctness, data file interactions, and UI response correctness. They produce validation_a.md and validation_b.md respectively. \"\n        \"RepairMerger merges both validation reports and applies corrections to generate the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web applications and frontend HTML validation.\n\nYour goal is to independently validate correctness of backend and frontend components, producing a detailed validation report.\n\nTask Details:\n- Read input artifacts: app.py, all template files (templates/*.html), design_spec.md, and user task description\n- Verify syntax correctness of app.py (compile and runtime)\n- Check Flask app startup and all route accessibility matches design_spec.md specifications\n- Validate presence and correctness of ALL required element IDs and buttons in templates\n- Verify correct reading/writing of data files under data/ as per design_spec.md\n- Confirm visible messaging and no-auth direct access functionality as specified\n- Produce validation_a.md report detailing findings\n\nValidation Steps:\n1. **Python Code Validation**\n   - Use validate_python_file tool to check syntax and runtime of app.py\n   - Report any errors or exceptions in validation_a.md\n\n2. **Flask App Behavior**\n   - Use execute_python_code tool to start Flask app (in test mode)\n   - Check accessibility of all routes defined in design_spec.md\n   - Confirm root route redirects correctly\n   - Test POST routes if any from design_spec.md\n\n3. **Frontend Templates Validation**\n   - Parse templates/*.html for presence of all required element IDs per design_spec.md\n   - Verify buttons, inputs, radio buttons, checkboxes, dropdowns appear as specified\n   - Check correct labeling and structural correctness\n\n4. **Data File Interaction**\n   - Verify app.py properly reads/writes data files in data/ directory\n   - Confirm field parsing matches design_spec.md schemas\n   - Validate no data corruption or incorrect access in interactions\n\n5. **UI Behavior and Messaging**\n   - Confirm UI visibility of success/error messages on actions\n   - Validate navigation buttons function as expected without authentication blocking\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file to check app.py\n- Use execute_python_code for runtime validations\n- Use write_text_file to output validation_a.md with detailed, structured report\n- Focus ONLY on provided input artifacts\n- Report ALL errors or inconsistencies clearly for repair\n- Do NOT write or modify any source code or templates\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer with expertise in end-to-end validation of Flask-based web applications including backend and frontend correctness.\n\nYour goal is to independently perform comprehensive validation of backend and frontend artifacts, producing a factual validation report.\n\nTask Details:\n- Read input artifacts: app.py, all templates (*.html), design_spec.md, and user task description\n- Validate functional correctness of all routes and their compliance with design_spec.md\n- Verify all element IDs in templates are accurate and correctly implemented\n- Check proper access and manipulation of data files under data/ directory\n- Confirm visibility and content of success and error messages in UI flows\n- Assess overall UI behavior matching the design and user requirements\n- Produce validation_b.md report with detailed validation results\n\nValidation Steps:\n1. **Flask Backend Validation**\n   - Check that app.py routes exist as specified and respond correctly (use execute_python_code)\n   - Validate input handling and output data formats\n   - Confirm correct use of design_spec.md field orders for data parsing\n\n2. **Frontend Template Checks**\n   - Verify that templates contain all required UI elements including dynamic IDs and buttons\n   - Confirm that navigation controls link appropriately as per design_spec.md\n   - Check form elements for correct names and types, especially radio buttons and checkboxes\n\n3. **Data File Access Validation**\n   - Confirm app.py reads/writes all required files with correct formats\n   - Validate no unauthorized access or missing file handling\n\n4. **User Interface Behavior**\n   - Evaluate visibility and accuracy of status messages on user actions (e.g., booking confirmation)\n   - Check appropriateness of UI flows without authentication\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file for static checks of app.py\n- Use execute_python_code to test live responses and route behavior\n- Use write_text_file to output validation_b.md\n- Base all conclusions strictly on input artifacts\n- Clearly identify any functional deviations or UI inconsistencies\n- Do NOT modify any source files or write code\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer with expertise in merging validation feedback and applying fixes to Flask applications and HTML templates.\n\nYour goal is to analyze two independent validation reports, reconcile needed repairs, and produce final, clean, fully functional and specification-compliant app.py and templates.\n\nTask Details:\n- Read validation_a.md and validation_b.md validation reports\n- Analyze discrepancies and compile comprehensive repair and correction list\n- Apply all fixes to app.py and templates/*.html to conform fully to design_spec.md\n- Ensure final app.py and templates/*.html pass all validation criteria from both reports\n- Produce final corrected app.py and templates/*.html files for deployment\n\nImplementation Steps:\n1. **Validation Analysis**\n   - Compare validation_a.md and validation_b.md for overlapping and unique issues\n   - Prioritize fixes based on criticality and specification compliance\n\n2. **Code and Template Corrections**\n   - Fix syntax errors, route definitions, data file handling in app.py\n   - Correct missing or incorrect element IDs, buttons, forms in templates\n   - Preserve original functionality and design intent\n\n3. **Verification**\n   - Confirm corrections align to design_spec.md fully\n   - Prepare clean, tested final artifacts ready for release\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save corrected app.py and all template files\n- Follow repair suggestions strictly from validation reports\n- Maintain format and naming conventions from original implementation\n- Deliver final artifacts that meet all design_spec.md requirements\n- Do NOT produce any additional report files or analysis text\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for detailed verification of routes, element IDs, file I/O, and UI, flagging actionable errors or omissions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Ensure validation_b.md provides thorough factual testing results for all requested functionalities and UI elements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html implement all design_spec.md features reliably, resolving identified validation issues.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'CarRental' Web Application

## 1. Objective
Develop a comprehensive web application named 'CarRental' using Python, with data managed through local text files. The application enables users to search vehicles, book rentals, manage reservations, view rental history, and select insurance options. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'CarRental' application is Python.

## 3. Page Design

The 'CarRental' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Car Rental Dashboard
- **Overview**: The main hub displaying featured vehicles, current promotions, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-vehicles** - Type: Div - Display of featured vehicle recommendations.
  - **ID: search-vehicles-button** - Type: Button - Button to navigate to vehicle search page.
  - **ID: my-reservations-button** - Type: Button - Button to navigate to reservations page.
  - **ID: promotions-section** - Type: Div - Display of current promotions and offers.

### 2. Vehicle Search Page
- **Page Title**: Search Vehicles
- **Overview**: A page displaying all available vehicles with search and filter capabilities.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-filter** - Type: Dropdown - Dropdown to filter by pickup location.
  - **ID: vehicle-type-filter** - Type: Dropdown - Dropdown to filter by vehicle type (Economy, Compact, Sedan, SUV, Luxury).
  - **ID: date-range-input** - Type: Input - Field to select rental date range.
  - **ID: vehicles-grid** - Type: Div - Grid displaying vehicle cards with image, model, price per day.
  - **ID: view-details-button-{vehicle_id}** - Type: Button - Button to view vehicle details (each vehicle card has this).

### 3. Vehicle Details Page
- **Page Title**: Vehicle Details
- **Overview**: A page displaying detailed information about a specific vehicle.
- **Elements**:
  - **ID: vehicle-details-page** - Type: Div - Container for the vehicle details page.
  - **ID: vehicle-name** - Type: H1 - Display vehicle name and model.
  - **ID: vehicle-specs** - Type: Div - Display vehicle specifications (engine, seats, transmission).
  - **ID: daily-rate** - Type: Div - Display daily rental rate.
  - **ID: book-now-button** - Type: Button - Button to book this vehicle.
  - **ID: vehicle-reviews** - Type: Div - Section displaying customer reviews.

### 4. Booking Page
- **Page Title**: Book Your Rental
- **Overview**: A page for users to complete rental booking with dates and location selection.
- **Elements**:
  - **ID: booking-page** - Type: Div - Container for the booking page.
  - **ID: pickup-location** - Type: Dropdown - Dropdown to select pickup location.
  - **ID: dropoff-location** - Type: Dropdown - Dropdown to select dropoff location.
  - **ID: pickup-date** - Type: Input - Field to select pickup date.
  - **ID: dropoff-date** - Type: Input - Field to select dropoff date.
  - **ID: calculate-price-button** - Type: Button - Button to calculate total rental price.
  - **ID: total-price** - Type: Div - Display calculated total price.
  - **ID: proceed-to-insurance-button** - Type: Button - Button to proceed to insurance options.

### 5. Insurance Options Page
- **Page Title**: Select Insurance Coverage
- **Overview**: A page for users to select insurance coverage for their rental.
- **Elements**:
  - **ID: insurance-page** - Type: Div - Container for the insurance page.
  - **ID: insurance-options** - Type: Div - Display of available insurance plans.
  - **ID: select-insurance-{insurance_id}** - Type: Radio - Radio button to select insurance plan (each plan has this).
  - **ID: insurance-description** - Type: Div - Display description of selected insurance plan.
  - **ID: insurance-price** - Type: Div - Display insurance price.
  - **ID: confirm-booking-button** - Type: Button - Button to confirm booking with insurance selection.

### 6. Rental History Page
- **Page Title**: Rental History
- **Overview**: A page displaying all previous rentals with details and status information.
- **Elements**:
  - **ID: history-page** - Type: Div - Container for the rental history page.
  - **ID: rentals-table** - Type: Table - Table displaying rentals with ID, vehicle, dates, location, and status.
  - **ID: view-rental-details-{rental_id}** - Type: Button - Button to view rental details (each rental has this).
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Active, Completed, Cancelled).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Reservation Management Page
- **Page Title**: My Reservations
- **Overview**: A page displaying current and upcoming reservations with management options.
- **Elements**:
  - **ID: reservations-page** - Type: Div - Container for the reservations page.
  - **ID: reservations-list** - Type: Div - List of all reservations with vehicle, dates, and status.
  - **ID: modify-reservation-button-{reservation_id}** - Type: Button - Button to modify reservation (each reservation has this).
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each reservation has this).
  - **ID: sort-by-date-button** - Type: Button - Button to sort reservations by date.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Special Requests Page
- **Page Title**: Special Requests
- **Overview**: A page for users to add special requests to their rental booking.
- **Elements**:
  - **ID: requests-page** - Type: Div - Container for the special requests page.
  - **ID: select-reservation** - Type: Dropdown - Dropdown to select reservation to add requests to.
  - **ID: driver-assistance-checkbox** - Type: Checkbox - Checkbox for driver assistance request.
  - **ID: gps-option-checkbox** - Type: Checkbox - Checkbox for GPS option.
  - **ID: child-seat-quantity** - Type: Input - Field to specify number of child seats needed.
  - **ID: special-notes** - Type: Textarea - Field to enter special notes and requests.
  - **ID: submit-requests-button** - Type: Button - Button to submit special requests.

### 9. Locations Page
- **Page Title**: Pickup and Dropoff Locations
- **Overview**: A page displaying all available rental pickup and dropoff locations with details.
- **Elements**:
  - **ID: locations-page** - Type: Div - Container for the locations page.
  - **ID: locations-list** - Type: Div - List of all rental locations with address and hours.
  - **ID: location-detail-button-{location_id}** - Type: Button - Button to view location details (each location has this).
  - **ID: hours-filter** - Type: Dropdown - Dropdown to filter by operating hours (24/7, Business Hours, Weekend).
  - **ID: search-location-input** - Type: Input - Field to search locations by city or name.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'CarRental' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Vehicles Data
- **File Name**: `vehicles.txt`
- **Data Format**:
  ```
  vehicle_id|make|model|vehicle_type|daily_rate|seats|transmission|fuel_type|status
  ```
- **Example Data**:
  ```
  1|Toyota|Camry|Sedan|55.00|5|Automatic|Petrol|Available
  2|Honda|CR-V|SUV|75.00|7|Automatic|Petrol|Available
  3|BMW|X5|Luxury|150.00|5|Automatic|Diesel|Available
  ```

### 2. Customers Data
- **File Name**: `customers.txt`
- **Data Format**:
  ```
  customer_id|name|email|phone|driver_license|license_expiry
  ```
- **Example Data**:
  ```
  1|Alice Johnson|alice@example.com|555-0101|D1234567|2026-06-15
  2|Bob Williams|bob@example.com|555-0102|D2345678|2027-03-20
  ```

### 3. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|city|address|phone|hours|available_vehicles
  ```
- **Example Data**:
  ```
  1|New York|123 Main St, NYC|555-1000|24/7|12
  2|Los Angeles|456 Oak Ave, LA|555-2000|09:00-18:00|8
  ```

### 4. Rentals Data
- **File Name**: `rentals.txt`
- **Data Format**:
  ```
  rental_id|vehicle_id|customer_id|pickup_date|dropoff_date|pickup_location|dropoff_location|total_price|status
  ```
- **Example Data**:
  ```
  1|1|1|2025-02-01|2025-02-05|New York|Los Angeles|275.00|Completed
  2|2|2|2025-02-10|2025-02-12|Los Angeles|New York|150.00|Active
  ```

### 5. Insurance Data
- **File Name**: `insurance.txt`
- **Data Format**:
  ```
  insurance_id|plan_name|description|daily_cost|coverage_limit|deductible
  ```
- **Example Data**:
  ```
  1|Basic Coverage|Liability only, min coverage|5.00|50000|1000
  2|Standard Coverage|Collision and theft protection|12.00|250000|500
  3|Premium Coverage|Full comprehensive protection|18.00|Unlimited|0
  ```

### 6. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|rental_id|vehicle_id|customer_id|status|insurance_id|special_requests
  ```
- **Example Data**:
  ```
  1|1|1|1|Confirmed|2|Driver assistance requested
  2|2|2|2|Active|1|GPS and child seat needed
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
    "DesignAgentA": {
        "prompt": (
            """You are a Software Architect specializing in designing Flask web applications.

Your goal is to draft a complete Flask application design candidate covering all specified pages with full route definitions, exact page titles, element IDs, navigation actions, and data file interaction strategies within the 'data/' directory, along with UI/UX details as per the CarRental requirements.

Task Details:
- Read the user_task_description to understand all CarRental requirements
- Produce design_candidate_a.md documenting all nine pages, including:
  - Flask route paths and methods
  - Exact page titles matching requirements
  - All HTML element IDs per page (static and dynamic)
  - Button actions, navigation links, and expected user flows
  - Data storage strategy with reading and writing to specified text files under 'data/'
  - UI/UX considerations consistent with the app's purpose and usability

Design Document Requirements:
1. **Routes and Views**:
   - Define route URL paths for each page, using RESTful conventions
   - Assign meaningful function names in snake_case
   - Specify HTTP methods (GET, POST) per route

2. **Page Elements**:
   - List all required element IDs per page exactly as in specifications
   - Detail dynamic IDs with variable placeholders (e.g., view-details-button-{vehicle_id})

3. **Navigation and Actions**:
   - Describe button/link navigation targets using Flask url_for function names
   - Specify user interaction flows (e.g., from booking page to insurance options)

4. **Data Handling**:
   - Map each data file to its usage context (reading, writing)
   - Use pipe-delimited formats as specified in the task
   - Include protocols for data validation and error handling

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save the output as design_candidate_a.md
- Ensure all design details conform strictly to the CarRental requirements
- Do NOT refer to or incorporate design_candidate_b.md content
- Output filename must be exactly design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAgentB": {
        "prompt": (
            """You are a Software Architect specialized in Flask web application design.

Your goal is to independently create a comprehensive Flask web app design candidate covering all CarRental requirements, including precise route definitions, exact HTML element IDs, data storage interactions with local text files, and navigation schemas.

Task Details:
- Parse user_task_description thoroughly for full requirements comprehension
- Write design_candidate_b.md including:
  - All route paths and HTTP methods for the nine specified pages
  - Exact matching page titles and container element IDs
  - Specific dynamic element ID patterns for buttons and inputs (e.g., select-insurance-{insurance_id})
  - User interaction sequences and navigation link mappings using Flask url_for
  - Data file usage with detailed read/write formats and locations under 'data/'

Design Document Expectations:
1. **Flask Routes**:
   - Define all URLs and corresponding view function names clearly and consistently
   - Specify GET or POST usage appropriately

2. **Page Structure**:
   - Enumerate all element IDs, with explanations when needed
   - Capture both static and dynamic IDs precisely

3. **Navigation Actions**:
   - Map each button or interactive element to target routes
   - Illustrate navigation flow through the app

4. **Data File Handling**:
   - Detail how each data file is accessed and updated
   - Emphasize pipe-delimited format adherence and data integrity checks

CRITICAL REQUIREMENTS:
- Use write_text_file tool to write design_candidate_b.md
- Do NOT access or incorporate content from design_candidate_a.md
- Provide standalone design addressing the entire CarRental spec
- Name output file exactly design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Software Architect with expertise in consolidating multiple design documents into a unified specification for Flask applications.

Your goal is to review design_candidate_a.md and design_candidate_b.md, identify and resolve any conflicts or omissions, and produce a final merged design_spec.md that encompasses all Flask routes, page elements, button actions, navigation links, template structures, and data file read/write protocols required for the CarRental application.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md fully
- Analyze overlap and discrepancies in:
  - Flask route definitions, URL paths, methods, and function names
  - Page titles and all element IDs, ensuring full coverage of all required pages
  - Navigation flows, button/link actions, and user journey consistency
  - Data storage handling for all specified text files, formats, and access methods
- Merge content preserving all unique elements and reconciling differences to maintain completeness and clarity
- Structure design_spec.md logically and clearly for implementation teams

Merged Design Requirements:
1. **Unified Flask Routes**:
   - Comprehensive route list with consistent naming conventions and HTTP methods
2. **Page Elements and Templates**:
   - Inclusive enumeration of all element IDs (static and dynamic)
   - Navigation mappings with Flask url_for references intact
3. **Data File Access**:
   - Clear protocols for reading and writing with pipe-delimited format adherence
   - Illustrate which routes/pages interact with which files
4. **Consistency and Clarity**:
   - Avoid redundancies and contradictions
   - Ensure final document is ready for direct implementation

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save merged output as design_spec.md
- Output must be comprehensive and consistent, addressing all user_task_description requirements
- Resolve conflicts and fill gaps present in source candidates
- File name must exactly be design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAgentA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAgentB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Python Flask Developer specializing in building web applications with data file integration.

Your goal is to independently implement a fully functional Flask app including app.py and all required HTML templates.

Task Details:
- Read user_task_description and design_spec.md from DesignMerger
- Implement app_candidate_a.py with all Flask routes, no-auth access, and flexible parsing of data files under data/
- Create all page templates in templates_candidate_a/ with correct page titles, element IDs, buttons, and visible user messages
- Do NOT access or refer to ImplementationEngineerB outputs or code

Implementation Guidelines:
1. **Flask Application**
   - Follow design_spec.md specifications strictly for route paths, function names, HTTP methods, and template rendering.
   - Implement routes for dashboard, vehicle search, vehicle details, booking, insurance selection, rental history, reservations management, special requests, and locations pages.
   - Use flexible yet precise parsing of pipe-delimited data files from the data/ directory.
   - Handle file I/O gracefully and maintain direct no-auth access to all pages.

2. **Templates**
   - Create all HTML templates in templates_candidate_a/ directory matching design_spec.md element IDs exactly.
   - Include page titles in both <title> and <h1> tags.
   - Use Jinja2 templating syntax for dynamic content rendering.
   - Ensure buttons and interactive elements have stable actionable IDs per spec.

3. **General**
   - Provide visible messages and UI statuses as required by the spec.
   - Follow best practices for Flask app structure and template organization.
   - Avoid referencing or reading any artifacts or outputs from ImplementationEngineerB.

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_a.py and all templates under templates_candidate_a/
- Follow design_spec.md strictly for routes, IDs, and file data handling
- Ensure all pages are accessible without authentication
- Output filenames: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Python Flask Developer specialized in developing web applications with a focus on UI fidelity and data integration.

Your goal is to produce an independent, complete Flask app implementation including app_candidate_b.py and all required HTML templates.

Task Details:
- Read user_task_description and design_spec.md from DesignMerger
- Implement app_candidate_b.py implementing all required Flask routes strictly according to the specification, including no-auth direct access
- Create all templates in templates_candidate_b/ with exact page titles, element IDs, buttons, and UI behaviors described in design_spec.md
- Do NOT refer to or read ImplementationEngineerA's code or templates

Implementation Guidelines:
1. **Flask Backend**
   - Strictly follow routes, parameter handling, data file parsing, and template rendering rules as stated in design_spec.md.
   - Ensure robustness in reading and processing local data files in data/ directory.
   - Enforce all navigation and interactive features with stable actionable IDs.

2. **Frontend Templates**
   - Develop templates using Jinja2 syntax with exact IDs as per design_spec.md under templates_candidate_b/
   - Include page titles consistently in <title> and <h1> tags
   - Ensure all user interactions like booking, insurance selection, reservations management, and special requests work via visible UI elements with proper IDs.

3. **General**
   - Provide clear UI feedback and status messages on pages.
   - Maintain separation from any outputs or knowledge of ImplementationEngineerA's work.

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/
- Follow design_spec.md for precise routing, templates, element IDs, and data handling
- Ensure all routes are accessible with no authentication
- Output filenames: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file', 'execute_python_code'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging independent Flask application implementations.

Your goal is to consolidate two independent Flask app implementations into a single final app.py and unified templates/*.html that fully conform to design_spec.md.

Task Details:
- Read user_task_description and design_spec.md from DesignMerger
- Compare and merge app_candidate_a.py and app_candidate_b.py into one complete, conflict-free app.py
- Compare and merge templates_candidate_a/*.html and templates_candidate_b/*.html, resolving conflicts and preserving strongest correct features into templates/*.html
- Ensure all routes, page titles, element IDs, buttons, and complete data file handling are correctly preserved and unified
- Maintain direct no-auth URLs and visible status messages as per spec

Merging Guidelines:
1. **Backend Merge**
   - Identify route implementations, data loading, and business logic in both candidates.
   - Resolve conflicts by selecting the best or most complete code per route and data handling.
   - Ensure the merged app.py matches design_spec.md requirements fully.

2. **Templates Merge**
   - For each template, compare both versions closely.
   - Keep exact element IDs as per design_spec.md.
   - Retain all interactive elements, page titles in <title> and <h1>, and UI feedback.
   - Synthesize best structures and styles, resolving conflicts carefully.

3. **Validation Preparation**
   - Prepare merged outputs so they can be validated against design_spec.md.
   - Ensure no merged outputs contain remnants of candidate identifiers or conflicting IDs.

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save final app.py and templates/*.html
- Final outputs must fully comply with design_spec.md on routes, UI, data file usage, and no-auth access
- Preserve and consolidate all visible user messages and statuses
- Output filenames: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web applications and frontend HTML validation.

Your goal is to independently validate correctness of backend and frontend components, producing a detailed validation report.

Task Details:
- Read input artifacts: app.py, all template files (templates/*.html), design_spec.md, and user task description
- Verify syntax correctness of app.py (compile and runtime)
- Check Flask app startup and all route accessibility matches design_spec.md specifications
- Validate presence and correctness of ALL required element IDs and buttons in templates
- Verify correct reading/writing of data files under data/ as per design_spec.md
- Confirm visible messaging and no-auth direct access functionality as specified
- Produce validation_a.md report detailing findings

Validation Steps:
1. **Python Code Validation**
   - Use validate_python_file tool to check syntax and runtime of app.py
   - Report any errors or exceptions in validation_a.md

2. **Flask App Behavior**
   - Use execute_python_code tool to start Flask app (in test mode)
   - Check accessibility of all routes defined in design_spec.md
   - Confirm root route redirects correctly
   - Test POST routes if any from design_spec.md

3. **Frontend Templates Validation**
   - Parse templates/*.html for presence of all required element IDs per design_spec.md
   - Verify buttons, inputs, radio buttons, checkboxes, dropdowns appear as specified
   - Check correct labeling and structural correctness

4. **Data File Interaction**
   - Verify app.py properly reads/writes data files in data/ directory
   - Confirm field parsing matches design_spec.md schemas
   - Validate no data corruption or incorrect access in interactions

5. **UI Behavior and Messaging**
   - Confirm UI visibility of success/error messages on actions
   - Validate navigation buttons function as expected without authentication blocking

CRITICAL REQUIREMENTS:
- Use validate_python_file to check app.py
- Use execute_python_code for runtime validations
- Use write_text_file to output validation_a.md with detailed, structured report
- Focus ONLY on provided input artifacts
- Report ALL errors or inconsistencies clearly for repair
- Do NOT write or modify any source code or templates

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer with expertise in end-to-end validation of Flask-based web applications including backend and frontend correctness.

Your goal is to independently perform comprehensive validation of backend and frontend artifacts, producing a factual validation report.

Task Details:
- Read input artifacts: app.py, all templates (*.html), design_spec.md, and user task description
- Validate functional correctness of all routes and their compliance with design_spec.md
- Verify all element IDs in templates are accurate and correctly implemented
- Check proper access and manipulation of data files under data/ directory
- Confirm visibility and content of success and error messages in UI flows
- Assess overall UI behavior matching the design and user requirements
- Produce validation_b.md report with detailed validation results

Validation Steps:
1. **Flask Backend Validation**
   - Check that app.py routes exist as specified and respond correctly (use execute_python_code)
   - Validate input handling and output data formats
   - Confirm correct use of design_spec.md field orders for data parsing

2. **Frontend Template Checks**
   - Verify that templates contain all required UI elements including dynamic IDs and buttons
   - Confirm that navigation controls link appropriately as per design_spec.md
   - Check form elements for correct names and types, especially radio buttons and checkboxes

3. **Data File Access Validation**
   - Confirm app.py reads/writes all required files with correct formats
   - Validate no unauthorized access or missing file handling

4. **User Interface Behavior**
   - Evaluate visibility and accuracy of status messages on user actions (e.g., booking confirmation)
   - Check appropriateness of UI flows without authentication

CRITICAL REQUIREMENTS:
- Use validate_python_file for static checks of app.py
- Use execute_python_code to test live responses and route behavior
- Use write_text_file to output validation_b.md
- Base all conclusions strictly on input artifacts
- Clearly identify any functional deviations or UI inconsistencies
- Do NOT modify any source files or write code

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Integration Engineer with expertise in merging validation feedback and applying fixes to Flask applications and HTML templates.

Your goal is to analyze two independent validation reports, reconcile needed repairs, and produce final, clean, fully functional and specification-compliant app.py and templates.

Task Details:
- Read validation_a.md and validation_b.md validation reports
- Analyze discrepancies and compile comprehensive repair and correction list
- Apply all fixes to app.py and templates/*.html to conform fully to design_spec.md
- Ensure final app.py and templates/*.html pass all validation criteria from both reports
- Produce final corrected app.py and templates/*.html files for deployment

Implementation Steps:
1. **Validation Analysis**
   - Compare validation_a.md and validation_b.md for overlapping and unique issues
   - Prioritize fixes based on criticality and specification compliance

2. **Code and Template Corrections**
   - Fix syntax errors, route definitions, data file handling in app.py
   - Correct missing or incorrect element IDs, buttons, forms in templates
   - Preserve original functionality and design intent

3. **Verification**
   - Confirm corrections align to design_spec.md fully
   - Prepare clean, tested final artifacts ready for release

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and all template files
- Follow repair suggestions strictly from validation reports
- Maintain format and naming conventions from original implementation
- Deliver final artifacts that meet all design_spec.md requirements
- Do NOT produce any additional report files or analysis text

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'validation_a.md', 'source': 'ValidationEngineerA'}, {'type': 'text_file', 'name': 'validation_b.md', 'source': 'ValidationEngineerB'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignAgentA': [
        ("DesignMerger", """Check design_candidate_a.md for complete route, page title, element ID coverage, navigation accuracy, and data file interaction strategies.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAgentB': [
        ("DesignMerger", """Check design_candidate_b.md for comprehensive Flask app design including all required pages, UI elements, and data access details.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify that the merged design_spec.md is coherent, fully detailed, and ready for precise implementation.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate candidate A for correct implementation of Flask routes, element IDs, no-auth access, and data file handling per design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Assess candidate B's implementation for feature completeness, route correctness, template fidelity, and data storage integration.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify merged app.py and templates/*.html conform fully with design_spec.md and are ready for testing and validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for detailed verification of routes, element IDs, file I/O, and UI, flagging actionable errors or omissions.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Ensure validation_b.md provides thorough factual testing results for all requested functionalities and UI elements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm final app.py and templates/*.html implement all design_spec.md features reliably, resolving identified validation issues.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignAgentA = build_resilient_agent(
        agent_name="DesignAgentA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    DesignAgentB = build_resilient_agent(
        agent_name="DesignAgentB",
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

    # Parallel generation of design candidates
    await asyncio.gather(
        execute(DesignAgentA,
                "Analyze user_task_description and produce design_candidate_a.md with complete Flask routes, page titles, "
                "element IDs, navigation details, and data storage strategy per CarRental requirements."),
        execute(DesignAgentB,
                "Analyze user_task_description and produce design_candidate_b.md with complete Flask routes, page titles, "
                "element IDs, navigation details, and data storage strategy independently per CarRental requirements.")
    )

    # Read design candidate contents for merger
    design_a_content, design_b_content = "", ""
    try:
        design_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge design candidates into unified design_spec.md
    await execute(
        DesignMerger,
        f"User requirements:\n"
        f"{CONTEXT.get('user_task_description', [{'content': ''}])[-1]['content']}\n\n"
        f"=== Design Candidate A ===\n{design_a_content}\n\n"
        f"=== Design Candidate B ===\n{design_b_content}",
    )
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
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel implementation of candidates A and B
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full Flask app in app_candidate_a.py "
                "with all routes and templates in templates_candidate_a/ per design_spec.md, no reference to ImplementationEngineerB."),
        execute(ImplementationEngineerB,
                "Implement full Flask app in app_candidate_b.py "
                "with all routes and templates in templates_candidate_b/ per design_spec.md, no reference to ImplementationEngineerA.")
    )

    # Read candidate outputs for merging
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
    # For templates, read as a bulk string as no specific filenames or counts are given
    try:
        # Here we read all templates_candidate_a/*.html files content concatenated
        import glob
        templates_a_files = glob.glob("templates_candidate_a/*.html")
        templates_candidate_a_content = "\n\n".join(open(f).read() for f in templates_a_files) if templates_a_files else ""
    except:
        templates_candidate_a_content = ""
    try:
        templates_b_files = glob.glob("templates_candidate_b/*.html")
        templates_candidate_b_content = "\n\n".join(open(f).read() for f in templates_b_files) if templates_b_files else ""
    except:
        templates_candidate_b_content = ""

    # Merge candidate implementations
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a.html ===\n{templates_candidate_a_content}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b.html ===\n{templates_candidate_b_content}\n")
# Phase2_End

# Phase3_Start

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
        recovery_time=60
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

    # Parallel validation by two engineers
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate app.py and templates/*.html with design_spec.md and user_task_description. "
                "Use validate_python_file and execute_python_code tools. "
                "Produce detailed validation_a.md report."),
        execute(ValidationEngineerB,
                "Validate app.py and templates/*.html with design_spec.md and user_task_description. "
                "Use validate_python_file and execute_python_code tools. "
                "Produce detailed validation_b.md report.")
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

    # RepairMerger applies fixes based on both validation reports producing final app.py and templates
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_report}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_report}\n\n"
                  "Analyze both reports, apply all necessary fixes to app.py and templates/*.html, "
                  "ensure full compliance with design_spec.md, "
                  "and output final corrected app.py and templates/*.html.")
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
