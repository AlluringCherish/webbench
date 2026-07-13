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
# 20260713_210029_568692/main_20260713_210029_568692.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs for PetAdoptionCenter and merge them into design_spec.md covering all 10 pages with element IDs, routes, data files, and interactions.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create full page/component designs, route mappings, and data interactions \"\n        \"from the user task. Each writes a design candidate markdown without reading the other's output. \"\n        \"DesignMerger reads both candidates, resolves conflicts, and produces the final design_spec.md covering all pages, elements, \"\n        \"route endpoints, data file usage, and interaction details to support implementation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Designer specializing in creating comprehensive design documents for Python Flask apps.\n\nYour goal is to independently create a complete web design candidate covering all pages and components of the PetAdoptionCenter application.\n\nTask Details:\n- Read the full user_task_description from CONTEXT\n- Produce design_candidate_a.md describing all 10 pages with page titles and URL routes starting from Dashboard\n- Include detailed element IDs for each page as specified in the user requirements\n- Specify user navigation flows via button/link interactions between pages\n- Document data file usage with expected CRUD operations on pets, users, applications, favorites, messages, shelters, and adoption history\n- Include communication flows such as messaging between users and shelters\n- Do not access or reference any other candidate outputs\n- Output a self-contained design candidate markdown file for review\n\nDesign Requirements:\n1. **Page Routes and Titles**\n   - List each page with URL route path (e.g., /dashboard, /pets, /pet/<id>)\n   - Provide exact page titles as specified\n\n2. **Element IDs and Structure**\n   - For each page, list all element IDs exactly as given (divs, buttons, inputs, tables, etc.)\n   - Specify element types (Div, Button, Input, Dropdown, etc.)\n\n3. **Navigation and User Interactions**\n   - Map navigation buttons to target routes or page states\n   - Describe user flow for multi-step interactions (e.g., adoption application submission)\n\n4. **Data File Usage and CRUD Operations**\n   - Specify which data files each page reads or writes\n   - Describe expected create, read, update, delete actions per data source\n\n5. **Communication Flows**\n   - Include message sending and receiving formats between users and shelters\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_candidate_a.md with full detailed design candidate\n- Strictly separate from DesignAnalystB's output; do not integrate or merge here\n- Follow user_task_description exactly for all element IDs and pages\n- Provide clear and unambiguous navigation and data interaction specifications\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Designer with expertise in user experience and system design for Flask-based apps.\n\nYour goal is to independently create an alternative full web design candidate for the PetAdoptionCenter.\n\nTask Details:\n- Fully analyze the user_task_description from CONTEXT\n- Write design_candidate_b.md covering all 10 pages with explicit URL route specifications starting at Dashboard\n- List each UI element’s ID with exact types and functions as per requirements\n- Describe data file interactions including reading, writing, and expected form processing flows\n- Provide detailed user action paths and navigation scenarios (e.g., from pet listings to adoption)\n- Suggest form validation and processing flow for application and message forms\n- Produce a comprehensive markdown design candidate without reviewing DesignAnalystA’s work\n\nDesign Requirements:\n1. **Page Routes and Navigation**\n   - Define URL route patterns and link destinations for all key navigation elements\n\n2. **Element IDs and Page Composition**\n   - List all required element IDs with their HTML element types clearly indicated\n   - Assign responsibilities for buttons, inputs, dropdowns, and other controls\n\n3. **Data Management and Form Processing**\n   - Outline expected CRUD operations on each data file\n   - Suggest detailed form submission workflows including validation points\n\n4. **User Interaction and Messaging**\n   - Define conversation management and message send/receive cycles\n   - Describe UI state changes during multi-step interactions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to produce design_candidate_b.md file\n- Maintain full independence from DesignAnalystA outputs\n- Adhere strictly to user requirements for completeness and clarity\n- Ensure all navigation paths and user interactions are clearly defined\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Systems Integration Specialist skilled in consolidating multiple design documents into a unified specification for implementation.\n\nYour goal is to merge two independent design candidates into a single coherent, comprehensive design_spec.md for PetAdoptionCenter.\n\nTask Details:\n- Read design_candidate_a.md and design_candidate_b.md fully from CONTEXT\n- Compare both for coverage, consistency, and feasibility across all 10 pages and all features\n- Resolve discrepancies in element IDs, routes, data file usages, and interaction flows\n- Produce a single design_spec.md that integrates the best elements from both candidates\n- Ensure completeness of routes starting from Dashboard, exact element IDs, data interaction schemes, and navigation mappings\n- Highlight any assumptions made when resolving conflicts\n- Output a clear, actionable, and unambiguous specification ready for implementation by developers\n\nMerging Requirements:\n1. **Page and Route Consistency**\n   - Use canonical, consistent URL routes and page titles for all pages\n\n2. **Element IDs and UI Components**\n   - Confirm all element IDs appear exactly once per page as required\n   - Resolve any naming conflicts or omissions\n\n3. **Data File Access and CRUD**\n   - Align data usage with user task data files\n   - Ensure all expected data actions (read/write/update/delete) are addressed\n\n4. **User Navigation and Interaction Flows**\n   - Consolidate navigation paths ensuring smooth user experience\n   - Include communication flows for messaging\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final design_spec.md\n- Deliver a single design document suitable for direct use by backend and frontend developers\n- Maintain full traceability to user_task_description and input candidate designs\n- Provide explicit page routes, element IDs, data file schema usage, and interaction descriptions\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_a.md covers all 10 pages, with correct element IDs, navigation, and data file CRUD operations based on user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_b.md provides a full alternative design with elements, routes, and data management aligned with user task.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Ensure design_spec.md is comprehensive, consistent, and fully actionable for implementation of Python Flask app with specified data stores and UI elements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Python Flask application bundles and template sets, and merge them into app.py and templates/*.html.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement complete app.py and templates/*.html sets \"\n        \"based on design_spec.md without accessing each other's output. ImplementationMerger then compares both candidates, resolves conflicts, \"\n        \"and creates the final polished app.py and templates/*.html supporting all user functionality, routes, elements, and data persistence.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in full-stack web application development.\n\nYour goal is to independently implement a complete Flask application and accompanying HTML templates based on provided design specifications.\n\nTask Details:\n- Read design_spec.md and user_task_description from CONTEXT\n- Implement full Flask app including all required routes and logic for PetAdoptionCenter\n- Create all templates under templates_candidate_a/ directory with exact element IDs and page titles\n- Handle data persistence using local pipe-delimited text files under data/ directory as per specifications\n- Provide visible success/error messages and maintain specified navigation flow\n\nImplementation Requirements:\n1. **Flask Application**:\n   - Implement all routes with starting page as Dashboard\n   - Support all 10 pages with specified page titles and element IDs\n   - Handle form submissions with validation and data file updates\n   - Read/write data exclusively from/to specified data/*.txt files\n   - Implement navigation buttons with correct IDs and route links\n\n2. **Templates**:\n   - Save templates in templates_candidate_a/ directory\n   - Use exact element IDs as specified in design_spec.md page design\n   - Match page titles both in <title> and visible headers\n   - Include forms, buttons, tables, grids as per specifications\n   - Support dynamic data display from Flask context\n\n3. **Data Management**:\n   - Load and save data in pipe-delimited text files (data/*.txt)\n   - Ensure data field order and types match specifications\n   - Handle missing or empty data gracefully\n   - Implement CRUD operations for pets, applications, favorites, messages, users as required\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/\n- Follow exactly element IDs, page titles, route patterns, and data schema instructions\n- Ensure all specified user functionality is implemented independently\n- DO NOT read or refer to candidate B outputs\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer experienced in creating complete web applications with templating and data persistence.\n\nYour goal is to independently develop a full Flask application and matching HTML templates adhering strictly to the design specification.\n\nTask Details:\n- Read design_spec.md and user_task_description from CONTEXT\n- Fully implement Flask app.py covering all required routes and business logic for PetAdoptionCenter\n- Create templates in templates_candidate_b/ directory using exact element IDs and page titles\n- Manage data through local pipe-delimited text files located in data/ folder\n- Implement user interface interactions, form handling, navigation, and data updates with clarity\n\nImplementation Guidelines:\n1. **Flask Backend**:\n   - Implement starting dashboard route and all other endpoints as specified\n   - Form processing must validate input and update data files accordingly\n   - Manage data consistency and error handling robustly\n   - Use the exact element IDs and button IDs for UI controls\n\n2. **Frontend Templates**:\n   - Place all templates under templates_candidate_b/\n   - Ensure pages display dynamic data consistent with backend context\n   - Maintain consistency of element IDs and page titles across all pages\n   - Build forms, tables, grids, and buttons as per design\n\n3. **Data Handling**:\n   - Parse and save all data files with pipe ('|') delimiter complying with field order\n   - Handle additions, edits, deletions for pets, applications, favorites, messages, and users\n   - Ensure data read/write is safe and synchronized\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool for all source code and template outputs\n- Adhere strictly to design_spec.md and user_task_description details\n- Produce independent, full implementation unrelated to candidate A\n- Deliver app_candidate_b.py and templates_candidate_b/*.html set as outputs\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in code and template merging for Python Flask applications.\n\nYour goal is to merge two independently developed Flask apps and template sets into a single coherent application meeting all user requirements.\n\nTask Details:\n- Read design_spec.md, both candidate app.py files and template sets from CONTEXT\n- Compare coverage of routes, element IDs, data file usage, and implemented features between candidate A and B\n- Identify conflicts, missing features, or inconsistencies in code and templates\n- Merge code to create final app.py implementing all requested pages, routes, and data I/O handling\n- Harmonize templates into templates/ directory ensuring all element IDs, page titles, buttons, and dynamic views are included and consistent\n- Ensure smooth, robust navigation flow and visible form success/error messages\n- Preserve data persistence with exact reading/writing of local pipe-delimited text files as specified\n\nMerging Process:\n1. **Comparison**:\n   - Map routes and templates from both candidates to find full coverage and discrepancies\n   - Verify element IDs, page titles, and button IDs for correctness and completeness\n\n2. **Conflict Resolution**:\n   - For code conflicts, choose the most complete and robust solution or combine approaches\n   - For template conflicts, merge UI elements and ensure no duplication or missing elements\n   - Ensure consistent naming and function implementations throughout\n\n3. **Final Assembly**:\n   - Compose final app.py with all routes and features fully integrated\n   - Assemble unified templates directory with fully compliant templates/*.html\n   - Test logical coherence of navigation and data operations\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file to output final app.py and templates/*.html files\n- Confirm all functionalities from user_task_description are fully supported\n- Ensure all UI element IDs and page titles are exact matches as specified\n- Validate robust data file I/O and error handling\n- Produce deliverables ready for deployment without further integration\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Review app_candidate_a.py and templates_candidate_a/*.html for full feature coverage, exact routes, element IDs, and text file data handling.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Review app_candidate_b.py and templates_candidate_b/*.html for completeness, correct route handling, UI IDs, and data file operations.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify merged app.py and templates/*.html are implementation-ready with consistent routing, data file usage, and UI elements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validations of app.py and templates/*.html, merge their repair suggestions, and produce the final working PetAdoptionCenter app bundle.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently test the final app.py and templates/*.html for syntax correctness, \"\n        \"route coverage, UI elements including exact element IDs, data persistence with local text files, and user flows. Each writes \"\n        \"a validation report. RepairMerger integrates both validation reports and applies necessary corrections to produce the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask application validation.\n\nYour goal is to independently validate the backend Python application (app.py) and frontend templates (*.html) to ensure full syntactic correctness, route coverage, UI element presence, and proper data interaction according to specifications.\n\nTask Details:\n- Read app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT\n- Validate syntax of app.py using validate_python_file tool\n- Run route and functional tests via execute_python_code to confirm all 10 pages load with correct titles and exact element IDs\n- Verify local data files under data/ directory read/write operations match design_spec.md schemas and usage\n- Produce comprehensive validation_a.md report describing all findings, errors, and suggestions\n\nValidation Requirements:\n1. Syntax and Runtime:\n   - Use validate_python_file tool on app.py; confirm syntax and runtime pass\n2. Route Testing:\n   - Programmatically test each route renders appropriate template with exact titles\n3. UI Elements:\n   - Check presence of all required element IDs on each page exactly as specified in requirements\n4. Data Persistence:\n   - Confirm app.py reads/writes all local data files correctly per design_spec.md formats\n   - Verify coverage and correctness of data handling\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use validate_python_file and execute_python_code tools for validation\n- Must write detailed validation_a.md as text file\n- Report must include page-wise test results, syntax status, and data file compliance\n- Focus only on: app.py, templates/*.html, design_spec.md, user task inputs\n- No fixes or code changes; pure validation only\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in end-to-end user interaction and UI validation for Flask applications.\n\nYour goal is to independently validate the complete web application functionality including user interactions, forms, navigation, data persistence, and UI element correctness.\n\nTask Details:\n- Read app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT\n- Validate syntax correctness of app.py with validate_python_file\n- Manually simulate or programmatically test all user interactions:\n  - Form submissions, button clicks, and navigation back to dashboard for all 10 pages\n  - Confirmation of exact element IDs on each page as per specifications\n- Check accuracy of data saved and retrieved from local text files against user data format specifications\n- Validate visible success and error messages in UI on user actions\n- Write detailed validation_b.md report with issues, observations, and test evidence\n\nValidation Requirements:\n1. Backend Syntax:\n   - Use validate_python_file tool to confirm no syntax/runtime errors in app.py\n2. UI and Interaction:\n   - Verify all element IDs exactly match requirements\n   - Confirm all navigation buttons link correctly and return to dashboard where specified\n3. Data Persistence:\n   - Check data integrity in local files aligns with user data format definitions\n4. Messaging:\n   - Validate UI shows appropriate feedback messages on user actions\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use validate_python_file and write_text_file tools\n- Produce comprehensive validation_b.md describing all issues and confirmations\n- Focus exclusively on user interaction accuracy and UI elements\n- No direct code modification, only validation reporting\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in code integration and repair for Flask web applications.\n\nYour goal is to consolidate the validation reports from two independent engineers, apply necessary corrections to backend app.py and frontend templates/*.html, and produce the final executable PetAdoptionCenter application bundle fully compliant with design specifications.\n\nTask Details:\n- Read validation_a.md, validation_b.md, app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT\n- Integrate findings from both validation reports to identify overlapping and unique issues\n- Correct syntax errors, route handling, UI element IDs, data file interactions, and user interface problems as documented\n- Preserve all exact route names, page element IDs, data file schemas, and UI behaviors as per design_spec.md\n- Produce final corrected app.py and templates/*.html output artifacts ready for deployment\n\nRepair and Integration Requirements:\n1. Issue Consolidation:\n   - Merge validation issues, prioritize fixes encompassing both reports\n2. Code Corrections:\n   - Fix Python syntax and runtime errors in app.py\n   - Update templates to add missing or correct element IDs and UI features\n3. Data Handling:\n   - Ensure all read/write operations on local text files follow design_spec.md formats exactly\n4. UI Consistency:\n   - Validate all buttons, forms, and navigation links function correctly\n5. Maintainability:\n   - Keep code readable, modular, and documented\n   - Do NOT arbitrarily add features not referenced in design_spec.md or validation reports\n\nCRITICAL SUCCESS CRITERIA:\n- MUST use write_text_file tool to output corrected app.py and templates/*.html\n- Preserve exact naming conventions and element IDs as specified\n- All known validation issues from both reports must be addressed and resolved\n- Deliver deployable final code bundle for PetAdoptionCenter app\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for detailed, actionable issues with app.py and templates/*.html before merging corrections.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_b.md for consistent, reproducible issues and verification of UI elements and data persistency before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html fully implement design_spec.md and have all validation issues resolved.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'PetAdoptionCenter' Web Application

## 1. Objective
Develop a comprehensive web application named 'PetAdoptionCenter' using Python, with data managed through local text files. The application enables users to browse available pets for adoption, submit adoption applications, manage favorites, and communicate with shelters. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'PetAdoptionCenter' application is Python.

## 3. Page Design

The 'PetAdoptionCenter' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Pet Adoption Dashboard
- **Overview**: The main hub displaying featured pets, recent activities, and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-pets** - Type: Div - Display of featured pets available for adoption (limit 5).
  - **ID: browse-pets-button** - Type: Button - Button to navigate to pet listings page.
  - **ID: back-to-dashboard** - Type: Button - Button to refresh dashboard.

### 2. Pet Listings Page
- **Page Title**: Available Pets
- **Overview**: A page displaying all available pets with filtering and search options.
- **Elements**:
  - **ID: pet-listings-page** - Type: Div - Container for the pet listings page.
  - **ID: search-input** - Type: Input - Field to search pets by name.
  - **ID: filter-species** - Type: Dropdown - Dropdown to filter by species (All, Dog, Cat, Bird, Rabbit, Other).
  - **ID: pet-grid** - Type: Div - Grid displaying pet cards with photo, name, species, and age.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Pet Details Page
- **Page Title**: Pet Details
- **Overview**: A page displaying detailed information about a specific pet.
- **Elements**:
  - **ID: pet-details-page** - Type: Div - Container for the pet details page.
  - **ID: pet-name** - Type: H1 - Display pet name.
  - **ID: pet-species** - Type: Div - Display pet species.
  - **ID: pet-description** - Type: Div - Display detailed description about the pet.
  - **ID: adopt-button** - Type: Button - Button to start adoption application process.
  - **ID: back-to-listings** - Type: Button - Button to navigate back to pet listings.

### 4. Add Pet Page
- **Page Title**: Add New Pet
- **Overview**: A page for shelter administrators to add new pets for adoption.
- **Elements**:
  - **ID: add-pet-page** - Type: Div - Container for the add pet page.
  - **ID: pet-name-input** - Type: Input - Field to input pet name.
  - **ID: pet-species-input** - Type: Dropdown - Dropdown to select species (Dog, Cat, Bird, Rabbit, Other).
  - **ID: pet-breed-input** - Type: Input - Field to input breed.
  - **ID: pet-age-input** - Type: Input - Field to input age (e.g., "2 years").
  - **ID: pet-gender-input** - Type: Dropdown - Dropdown to select gender (Male, Female).
  - **ID: pet-size-input** - Type: Dropdown - Dropdown to select size (Small, Medium, Large).
  - **ID: pet-description-input** - Type: Textarea - Field to input detailed description.
  - **ID: submit-pet-button** - Type: Button - Button to submit new pet listing.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Adoption Application Page
- **Page Title**: Adoption Application
- **Overview**: A page for users to submit adoption applications.
- **Elements**:
  - **ID: application-page** - Type: Div - Container for the application page.
  - **ID: applicant-name** - Type: Input - Field to input applicant's full name.
  - **ID: applicant-phone** - Type: Input - Field to input phone number.
  - **ID: housing-type** - Type: Dropdown - Dropdown to select housing type (House, Apartment, Condo, Other).
  - **ID: reason** - Type: Textarea - Field to explain why they want to adopt this pet.
  - **ID: submit-application-button** - Type: Button - Button to submit application.
  - **ID: back-to-pet** - Type: Button - Button to navigate back to pet details.

### 6. My Applications Page
- **Page Title**: My Applications
- **Overview**: A page displaying all adoption applications submitted by the user.
- **Elements**:
  - **ID: my-applications-page** - Type: Div - Container for the my applications page.
  - **ID: filter-status** - Type: Dropdown - Dropdown to filter by status (All, Pending, Approved, Rejected).
  - **ID: applications-table** - Type: Table - Table displaying applications with pet name, date, status, and actions.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Favorites Page
- **Page Title**: My Favorites
- **Overview**: A page displaying all pets the user has saved as favorites.
- **Elements**:
  - **ID: favorites-page** - Type: Div - Container for the favorites page.
  - **ID: favorites-grid** - Type: Div - Grid displaying favorite pet cards.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Messages Page
- **Page Title**: Messages
- **Overview**: A page for users to view and send messages to shelters.
- **Elements**:
  - **ID: messages-page** - Type: Div - Container for the messages page.
  - **ID: conversation-list** - Type: Div - List of message conversations.
  - **ID: message-input** - Type: Textarea - Field to compose new message.
  - **ID: send-message-button** - Type: Button - Button to send message.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Admin Panel Page
- **Page Title**: Admin Panel
- **Overview**: A page for administrators to manage applications and pets.
- **Elements**:
  - **ID: admin-panel-page** - Type: Div - Container for the admin panel page.
  - **ID: pending-applications** - Type: Div - List of pending adoption applications.
  - **ID: all-pets-list** - Type: Div - List of all pets with edit/delete options.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'PetAdoptionCenter' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|address
  ```
- **Example Data**:
  ```
  john_doe|john@example.com|555-1234|123 Main St, City
  admin_user|admin@shelter.com|555-0000|456 Shelter Ave
  jane_smith|jane@example.com|555-5678|789 Oak Rd, Town
  ```

### 2. Pet Data
- **File Name**: `pets.txt`
- **Data Format**:
  ```
  pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
  ```
- **Example Data**:
  ```
  1|Buddy|Dog|Golden Retriever|3 years|Male|Large|Friendly and energetic dog who loves to play fetch.|1|Available|2024-10-15
  2|Whiskers|Cat|Siamese|2 years|Female|Small|Calm and affectionate cat, great with children.|1|Pending|2024-10-20
  3|Charlie|Dog|Beagle|5 years|Male|Medium|Gentle senior dog looking for a quiet home.|2|Available|2024-11-01
  ```

### 3. Adoption Applications Data
- **File Name**: `applications.txt`
- **Data Format**:
  ```
  application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
  ```
- **Example Data**:
  ```
  1|john_doe|1|John Doe|555-1234|123 Main St|House|Yes|One cat|5 years with dogs|Looking for a companion for hiking|Pending|2024-11-10
  2|jane_smith|2|Jane Smith|555-5678|789 Oak Rd|Apartment|No|None|First time pet owner|Always wanted a cat|Approved|2024-11-05
  ```

### 4. Favorites Data
- **File Name**: `favorites.txt`
- **Data Format**:
  ```
  username|pet_id|date_added
  ```
- **Example Data**:
  ```
  john_doe|1|2024-11-01
  john_doe|3|2024-11-05
  jane_smith|2|2024-10-25
  ```

### 5. Messages Data
- **File Name**: `messages.txt`
- **Data Format**:
  ```
  message_id|sender_username|recipient_username|subject|content|timestamp|is_read
  ```
- **Example Data**:
  ```
  1|john_doe|admin_user|Question about Buddy|Is Buddy good with other dogs?|2024-11-10 14:30:00|true
  2|admin_user|john_doe|Re: Question about Buddy|Yes, Buddy is great with other dogs!|2024-11-10 15:00:00|false
  ```

### 6. Adoption History Data
- **File Name**: `adoption_history.txt`
- **Data Format**:
  ```
  history_id|username|pet_id|pet_name|adoption_date|shelter_id
  ```
- **Example Data**:
  ```
  1|jane_smith|2|Whiskers|2024-11-15|1
  ```

### 7. Shelters Data
- **File Name**: `shelters.txt`
- **Data Format**:
  ```
  shelter_id|name|address|phone|email
  ```
- **Example Data**:
  ```
  1|Happy Paws Shelter|100 Shelter Lane, City|555-1000|contact@happypaws.com
  2|Second Chance Animals|200 Rescue Road, Town|555-2000|info@secondchance.org
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
            """You are a Web Application Designer specializing in creating comprehensive design documents for Python Flask apps.

Your goal is to independently create a complete web design candidate covering all pages and components of the PetAdoptionCenter application.

Task Details:
- Read the full user_task_description from CONTEXT
- Produce design_candidate_a.md describing all 10 pages with page titles and URL routes starting from Dashboard
- Include detailed element IDs for each page as specified in the user requirements
- Specify user navigation flows via button/link interactions between pages
- Document data file usage with expected CRUD operations on pets, users, applications, favorites, messages, shelters, and adoption history
- Include communication flows such as messaging between users and shelters
- Do not access or reference any other candidate outputs
- Output a self-contained design candidate markdown file for review

Design Requirements:
1. **Page Routes and Titles**
   - List each page with URL route path (e.g., /dashboard, /pets, /pet/<id>)
   - Provide exact page titles as specified

2. **Element IDs and Structure**
   - For each page, list all element IDs exactly as given (divs, buttons, inputs, tables, etc.)
   - Specify element types (Div, Button, Input, Dropdown, etc.)

3. **Navigation and User Interactions**
   - Map navigation buttons to target routes or page states
   - Describe user flow for multi-step interactions (e.g., adoption application submission)

4. **Data File Usage and CRUD Operations**
   - Specify which data files each page reads or writes
   - Describe expected create, read, update, delete actions per data source

5. **Communication Flows**
   - Include message sending and receiving formats between users and shelters

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_candidate_a.md with full detailed design candidate
- Strictly separate from DesignAnalystB's output; do not integrate or merge here
- Follow user_task_description exactly for all element IDs and pages
- Provide clear and unambiguous navigation and data interaction specifications

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Designer with expertise in user experience and system design for Flask-based apps.

Your goal is to independently create an alternative full web design candidate for the PetAdoptionCenter.

Task Details:
- Fully analyze the user_task_description from CONTEXT
- Write design_candidate_b.md covering all 10 pages with explicit URL route specifications starting at Dashboard
- List each UI element’s ID with exact types and functions as per requirements
- Describe data file interactions including reading, writing, and expected form processing flows
- Provide detailed user action paths and navigation scenarios (e.g., from pet listings to adoption)
- Suggest form validation and processing flow for application and message forms
- Produce a comprehensive markdown design candidate without reviewing DesignAnalystA’s work

Design Requirements:
1. **Page Routes and Navigation**
   - Define URL route patterns and link destinations for all key navigation elements

2. **Element IDs and Page Composition**
   - List all required element IDs with their HTML element types clearly indicated
   - Assign responsibilities for buttons, inputs, dropdowns, and other controls

3. **Data Management and Form Processing**
   - Outline expected CRUD operations on each data file
   - Suggest detailed form submission workflows including validation points

4. **User Interaction and Messaging**
   - Define conversation management and message send/receive cycles
   - Describe UI state changes during multi-step interactions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to produce design_candidate_b.md file
- Maintain full independence from DesignAnalystA outputs
- Adhere strictly to user requirements for completeness and clarity
- Ensure all navigation paths and user interactions are clearly defined

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Systems Integration Specialist skilled in consolidating multiple design documents into a unified specification for implementation.

Your goal is to merge two independent design candidates into a single coherent, comprehensive design_spec.md for PetAdoptionCenter.

Task Details:
- Read design_candidate_a.md and design_candidate_b.md fully from CONTEXT
- Compare both for coverage, consistency, and feasibility across all 10 pages and all features
- Resolve discrepancies in element IDs, routes, data file usages, and interaction flows
- Produce a single design_spec.md that integrates the best elements from both candidates
- Ensure completeness of routes starting from Dashboard, exact element IDs, data interaction schemes, and navigation mappings
- Highlight any assumptions made when resolving conflicts
- Output a clear, actionable, and unambiguous specification ready for implementation by developers

Merging Requirements:
1. **Page and Route Consistency**
   - Use canonical, consistent URL routes and page titles for all pages

2. **Element IDs and UI Components**
   - Confirm all element IDs appear exactly once per page as required
   - Resolve any naming conflicts or omissions

3. **Data File Access and CRUD**
   - Align data usage with user task data files
   - Ensure all expected data actions (read/write/update/delete) are addressed

4. **User Navigation and Interaction Flows**
   - Consolidate navigation paths ensuring smooth user experience
   - Include communication flows for messaging

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final design_spec.md
- Deliver a single design document suitable for direct use by backend and frontend developers
- Maintain full traceability to user_task_description and input candidate designs
- Provide explicit page routes, element IDs, data file schema usage, and interaction descriptions

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Python Flask Developer specializing in full-stack web application development.

Your goal is to independently implement a complete Flask application and accompanying HTML templates based on provided design specifications.

Task Details:
- Read design_spec.md and user_task_description from CONTEXT
- Implement full Flask app including all required routes and logic for PetAdoptionCenter
- Create all templates under templates_candidate_a/ directory with exact element IDs and page titles
- Handle data persistence using local pipe-delimited text files under data/ directory as per specifications
- Provide visible success/error messages and maintain specified navigation flow

Implementation Requirements:
1. **Flask Application**:
   - Implement all routes with starting page as Dashboard
   - Support all 10 pages with specified page titles and element IDs
   - Handle form submissions with validation and data file updates
   - Read/write data exclusively from/to specified data/*.txt files
   - Implement navigation buttons with correct IDs and route links

2. **Templates**:
   - Save templates in templates_candidate_a/ directory
   - Use exact element IDs as specified in design_spec.md page design
   - Match page titles both in <title> and visible headers
   - Include forms, buttons, tables, grids as per specifications
   - Support dynamic data display from Flask context

3. **Data Management**:
   - Load and save data in pipe-delimited text files (data/*.txt)
   - Ensure data field order and types match specifications
   - Handle missing or empty data gracefully
   - Implement CRUD operations for pets, applications, favorites, messages, users as required

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/
- Follow exactly element IDs, page titles, route patterns, and data schema instructions
- Ensure all specified user functionality is implemented independently
- DO NOT read or refer to candidate B outputs

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Python Flask Developer experienced in creating complete web applications with templating and data persistence.

Your goal is to independently develop a full Flask application and matching HTML templates adhering strictly to the design specification.

Task Details:
- Read design_spec.md and user_task_description from CONTEXT
- Fully implement Flask app.py covering all required routes and business logic for PetAdoptionCenter
- Create templates in templates_candidate_b/ directory using exact element IDs and page titles
- Manage data through local pipe-delimited text files located in data/ folder
- Implement user interface interactions, form handling, navigation, and data updates with clarity

Implementation Guidelines:
1. **Flask Backend**:
   - Implement starting dashboard route and all other endpoints as specified
   - Form processing must validate input and update data files accordingly
   - Manage data consistency and error handling robustly
   - Use the exact element IDs and button IDs for UI controls

2. **Frontend Templates**:
   - Place all templates under templates_candidate_b/
   - Ensure pages display dynamic data consistent with backend context
   - Maintain consistency of element IDs and page titles across all pages
   - Build forms, tables, grids, and buttons as per design

3. **Data Handling**:
   - Parse and save all data files with pipe ('|') delimiter complying with field order
   - Handle additions, edits, deletions for pets, applications, favorites, messages, and users
   - Ensure data read/write is safe and synchronized

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool for all source code and template outputs
- Adhere strictly to design_spec.md and user_task_description details
- Produce independent, full implementation unrelated to candidate A
- Deliver app_candidate_b.py and templates_candidate_b/*.html set as outputs

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Engineer specializing in code and template merging for Python Flask applications.

Your goal is to merge two independently developed Flask apps and template sets into a single coherent application meeting all user requirements.

Task Details:
- Read design_spec.md, both candidate app.py files and template sets from CONTEXT
- Compare coverage of routes, element IDs, data file usage, and implemented features between candidate A and B
- Identify conflicts, missing features, or inconsistencies in code and templates
- Merge code to create final app.py implementing all requested pages, routes, and data I/O handling
- Harmonize templates into templates/ directory ensuring all element IDs, page titles, buttons, and dynamic views are included and consistent
- Ensure smooth, robust navigation flow and visible form success/error messages
- Preserve data persistence with exact reading/writing of local pipe-delimited text files as specified

Merging Process:
1. **Comparison**:
   - Map routes and templates from both candidates to find full coverage and discrepancies
   - Verify element IDs, page titles, and button IDs for correctness and completeness

2. **Conflict Resolution**:
   - For code conflicts, choose the most complete and robust solution or combine approaches
   - For template conflicts, merge UI elements and ensure no duplication or missing elements
   - Ensure consistent naming and function implementations throughout

3. **Final Assembly**:
   - Compose final app.py with all routes and features fully integrated
   - Assemble unified templates directory with fully compliant templates/*.html
   - Test logical coherence of navigation and data operations

CRITICAL REQUIREMENTS:
- Use write_text_file to output final app.py and templates/*.html files
- Confirm all functionalities from user_task_description are fully supported
- Ensure all UI element IDs and page titles are exact matches as specified
- Validate robust data file I/O and error handling
- Produce deliverables ready for deployment without further integration

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask application validation.

Your goal is to independently validate the backend Python application (app.py) and frontend templates (*.html) to ensure full syntactic correctness, route coverage, UI element presence, and proper data interaction according to specifications.

Task Details:
- Read app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Validate syntax of app.py using validate_python_file tool
- Run route and functional tests via execute_python_code to confirm all 10 pages load with correct titles and exact element IDs
- Verify local data files under data/ directory read/write operations match design_spec.md schemas and usage
- Produce comprehensive validation_a.md report describing all findings, errors, and suggestions

Validation Requirements:
1. Syntax and Runtime:
   - Use validate_python_file tool on app.py; confirm syntax and runtime pass
2. Route Testing:
   - Programmatically test each route renders appropriate template with exact titles
3. UI Elements:
   - Check presence of all required element IDs on each page exactly as specified in requirements
4. Data Persistence:
   - Confirm app.py reads/writes all local data files correctly per design_spec.md formats
   - Verify coverage and correctness of data handling

CRITICAL SUCCESS CRITERIA:
- MUST use validate_python_file and execute_python_code tools for validation
- Must write detailed validation_a.md as text file
- Report must include page-wise test results, syntax status, and data file compliance
- Focus only on: app.py, templates/*.html, design_spec.md, user task inputs
- No fixes or code changes; pure validation only

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in end-to-end user interaction and UI validation for Flask applications.

Your goal is to independently validate the complete web application functionality including user interactions, forms, navigation, data persistence, and UI element correctness.

Task Details:
- Read app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Validate syntax correctness of app.py with validate_python_file
- Manually simulate or programmatically test all user interactions:
  - Form submissions, button clicks, and navigation back to dashboard for all 10 pages
  - Confirmation of exact element IDs on each page as per specifications
- Check accuracy of data saved and retrieved from local text files against user data format specifications
- Validate visible success and error messages in UI on user actions
- Write detailed validation_b.md report with issues, observations, and test evidence

Validation Requirements:
1. Backend Syntax:
   - Use validate_python_file tool to confirm no syntax/runtime errors in app.py
2. UI and Interaction:
   - Verify all element IDs exactly match requirements
   - Confirm all navigation buttons link correctly and return to dashboard where specified
3. Data Persistence:
   - Check data integrity in local files aligns with user data format definitions
4. Messaging:
   - Validate UI shows appropriate feedback messages on user actions

CRITICAL SUCCESS CRITERIA:
- MUST use validate_python_file and write_text_file tools
- Produce comprehensive validation_b.md describing all issues and confirmations
- Focus exclusively on user interaction accuracy and UI elements
- No direct code modification, only validation reporting

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Engineer specializing in code integration and repair for Flask web applications.

Your goal is to consolidate the validation reports from two independent engineers, apply necessary corrections to backend app.py and frontend templates/*.html, and produce the final executable PetAdoptionCenter application bundle fully compliant with design specifications.

Task Details:
- Read validation_a.md, validation_b.md, app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Integrate findings from both validation reports to identify overlapping and unique issues
- Correct syntax errors, route handling, UI element IDs, data file interactions, and user interface problems as documented
- Preserve all exact route names, page element IDs, data file schemas, and UI behaviors as per design_spec.md
- Produce final corrected app.py and templates/*.html output artifacts ready for deployment

Repair and Integration Requirements:
1. Issue Consolidation:
   - Merge validation issues, prioritize fixes encompassing both reports
2. Code Corrections:
   - Fix Python syntax and runtime errors in app.py
   - Update templates to add missing or correct element IDs and UI features
3. Data Handling:
   - Ensure all read/write operations on local text files follow design_spec.md formats exactly
4. UI Consistency:
   - Validate all buttons, forms, and navigation links function correctly
5. Maintainability:
   - Keep code readable, modular, and documented
   - Do NOT arbitrarily add features not referenced in design_spec.md or validation reports

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output corrected app.py and templates/*.html
- Preserve exact naming conventions and element IDs as specified
- All known validation issues from both reports must be addressed and resolved
- Deliver deployable final code bundle for PetAdoptionCenter app

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
        ("DesignMerger", """Verify design_candidate_a.md covers all 10 pages, with correct element IDs, navigation, and data file CRUD operations based on user requirements.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Verify design_candidate_b.md provides a full alternative design with elements, routes, and data management aligned with user task.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Ensure design_spec.md is comprehensive, consistent, and fully actionable for implementation of Python Flask app with specified data stores and UI elements.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Review app_candidate_a.py and templates_candidate_a/*.html for full feature coverage, exact routes, element IDs, and text file data handling.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Review app_candidate_b.py and templates_candidate_b/*.html for completeness, correct route handling, UI IDs, and data file operations.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify merged app.py and templates/*.html are implementation-ready with consistent routing, data file usage, and UI elements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for detailed, actionable issues with app.py and templates/*.html before merging corrections.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Check validation_b.md for consistent, reproducible issues and verification of UI elements and data persistency before merging.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm final app.py and templates/*.html fully implement design_spec.md and have all validation issues resolved.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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

    # Parallel execution of Design Analysts A and B
    await asyncio.gather(
        execute(DesignAnalystA,
                "Generate design_candidate_a.md with detailed PetAdoptionCenter design covering all 10 pages, element IDs, routes, data file usage, navigation flows, and communications based on user_task_description."),
        execute(DesignAnalystB,
                "Generate design_candidate_b.md with alternative comprehensive PetAdoptionCenter design including page routes, element IDs, user interactions, data management, and messaging workflows based on user_task_description.")
    )

    # Read design candidate outputs for merger
    design_a_content, design_b_content = "", ""
    try:
        design_a_content = open("design_candidate_a.md").read()
    except Exception:
        pass
    try:
        design_b_content = open("design_candidate_b.md").read()
    except Exception:
        pass

    # Merge design candidates into final design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA Candidate ===\n"
                  f"{design_a_content}\n\n"
                  f"=== DesignAnalystB Candidate ===\n"
                  f"{design_b_content}")
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
        timeout_threshold=300,
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
        timeout_threshold=300,
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
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel implementation by candidates A and B
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full Flask app and templates in templates_candidate_a/ based on design_spec.md and user_task_description. "
                "Output app_candidate_a.py and templates_candidate_a/*.html."),
        execute(ImplementationEngineerB,
                "Implement full Flask app and templates in templates_candidate_b/ based on design_spec.md and user_task_description. "
                "Output app_candidate_b.py and templates_candidate_b/*.html.")
    )

    # Read outputs from candidates for merging
    app_candidate_a_content, app_candidate_b_content = "", ""
    templates_candidate_a_content, templates_candidate_b_content = "", ""
    try:
        app_candidate_a_content = open("app_candidate_a.py").read()
    except:
        pass
    try:
        app_candidate_b_content = open("app_candidate_b.py").read()
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

    # Merge outputs into final app.py and templates/*.html
    await execute(ImplementationMerger,
                  f"=== Design Specification ===\n{CONTEXT.get('design_spec.md', [{}])[-1].get('content', '')}\n\n"
                  f"=== Candidate A app.py ===\n{app_candidate_a_content}\n\n"
                  f"=== Candidate A templates ===\n{templates_candidate_a_content}\n\n"
                  f"=== Candidate B app.py ===\n{app_candidate_b_content}\n\n"
                  f"=== Candidate B templates ===\n{templates_candidate_b_content}\n\n"
                  f"Proceed to merge candidates into final app.py and templates/*.html meeting all user requirements.")
# Phase2_End

# Phase3_Start
import asyncio

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

    # Read artifacts content for injection
    app_py_content, templates_content, design_spec_content, user_task_desc = "", "", "", ""
    try:
        app_py_content = open("app.py").read()
    except:
        pass
    try:
        # For templates/*.html, read all template files and concatenate content for injection
        import glob
        templates_files = glob.glob("templates/*.html")
        templates_content = ""
        for f in templates_files:
            try:
                templates_content += f"=== {f} ===\n" + open(f).read() + "\n\n"
            except:
                continue
    except:
        pass
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    try:
        entries = CONTEXT.get("user_task_description", [])
        user_task_desc = entries[-1]["content"] if entries else ""
    except:
        pass

    # Parallel validation executions
    await asyncio.gather(
        execute(ValidationEngineerA,
                f"Validate app.py and templates/*.html for syntax, route coverage, UI elements, "
                f"and data file correctness using validate_python_file and execute_python_code tools.\n\n"
                f"=== app.py ===\n{app_py_content}\n\n"
                f"=== templates/*.html ===\n{templates_content}\n\n"
                f"=== design_spec.md ===\n{design_spec_content}\n\n"
                f"User task description:\n{user_task_desc}"),
        execute(ValidationEngineerB,
                f"Validate backend syntax and UI/UX including user interaction accuracy, element IDs, navigation, data persistence, "
                f"and messaging based on app.py, templates/*.html, design_spec.md.\n\n"
                f"=== app.py ===\n{app_py_content}\n\n"
                f"=== templates/*.html ===\n{templates_content}\n\n"
                f"=== design_spec.md ===\n{design_spec_content}\n\n"
                f"User task description:\n{user_task_desc}")
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

    # Execute RepairMerger agent with all inputs and merged validation reports
    await execute(RepairMerger,
                  f"Merge the validation reports from two engineers and fix all issues in app.py and templates/*.html accordingly.\n\n"
                  f"=== validation_a.md ===\n{validation_a_content}\n\n"
                  f"=== validation_b.md ===\n{validation_b_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"User task description:\n{user_task_desc}")
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
