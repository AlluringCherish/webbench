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
# 20260713_210029_226499/main_20260713_210029_226499.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent detailed Web app design specs and merge into design_spec.md covering all specified pages, routes, elements, and data files.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently generate full design specifications including Flask routes, page titles, element-IDs, interactions, \"\n        \"data file usage and formats without viewing each other's outputs. DesignMerger then reviews both specs, resolves conflicts and omissions, \"\n        \"and produces a single unified design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in comprehensive specification creation for Flask-based job board applications.\n\nYour goal is to produce a complete design specification that covers all 9 pages specified in the user requirements, including Flask routes, template filenames, page titles, element IDs, input/output controls, user navigation starting from the Dashboard page, and data read/write interactions with local text files.\n\nTask Details:\n- Read the full user_task_description artifact.\n- Produce a detailed design specification saved as design_candidate_a.md.\n- Include all required Flask routes with method details, mapping to template files.\n- Specify exact element IDs for each page including dynamic IDs with patterns.\n- Detail page titles exactly as specified.\n- Describe user navigation flows starting at the Dashboard page.\n- Document data file usage, read/write operations, and field formats based on provided data storage specs.\n\nSpecification Requirements:\n1. **Flask Routes and Templates:**\n   - Provide route paths, HTTP methods, and the template file each renders.\n   - Define context variables passed to templates precisely.\n\n2. **Page Elements and Layout:**\n   - List all element IDs per page with descriptions and types (e.g., div, button, input).\n   - Specify dynamic element ID patterns using {variable} syntax.\n\n3. **Navigation Flow:**\n   - Map user interaction from buttons and links to respective routes.\n   - Start navigation explicitly from the Dashboard page.\n\n4. **Data File Integration:**\n   - For each data file, specify path (data/*.txt), format with exact field order, read/write usage per route or page.\n   - Use pipe-delimited '|' format consistently.\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to save the output as design_candidate_a.md.\n- Follow all user task specifications precisely without omissions.\n- Ensure the specification enables independent implementation of frontend and backend.\n- Do not cross-reference any other design candidates or outputs.\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst with expertise in Flask applications, focused on independent comprehensive design specification production.\n\nYour goal is to independently create an alternative detailed design specification that fully addresses all 9 pages from the user requirements, including Flask routes, template filenames, element IDs, user interactions, navigation flow, and data file formats and usage, without viewing or referencing DesignAnalystA's work.\n\nTask Details:\n- Analyze the entire user_task_description provided.\n- Produce a detailed design specification saved as design_candidate_b.md.\n- Include all necessary Flask routes aligned to template filenames.\n- Specify exact element IDs including those with dynamic variables.\n- Clearly define page titles and their usage.\n- Lay out navigation workflows consistent with provided specifications.\n- Specify data read and write operations with exact data file formats and paths.\n\nSpecification Details:\n1. **Routes and Templates:**\n   - List all routes with HTTP methods and linked templates.\n   - Define the context variables for each route.\n\n2. **Page Elements:**\n   - List element IDs and their types, including dynamic IDs with {parameter} patterns.\n   - Ensure elements align with user interface requirements.\n\n3. **User Navigation:**\n   - Explicitly start navigation from Dashboard.\n   - Map buttons and links to their respective routes.\n\n4. **Data Files:**\n   - Document all relevant data files with fields, format, read/write usage.\n   - Follow pipe '|' delimited format precisely.\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to output the specification as design_candidate_b.md.\n- Follow user requirements fully with no omissions.\n- Ensure the spec enables separate frontend and backend development.\n- Do not consult or use DesignAnalystA’s data or outputs.\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Integration Specialist expert in unifying multiple web application design specifications into a consistent master specification.\n\nYour goal is to review design_candidate_a.md and design_candidate_b.md along with the original user_task_description to identify any omissions, conflicts, or inconsistencies, then synthesize and produce a single detailed design_spec.md covering all Flask routes, page titles, element IDs, template filenames, navigation workflows, all page elements, and data file interfaces required to fully implement the JobBoard application.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md artifacts.\n- Compare and analyze both candidate specifications for completeness and consistency.\n- Resolve conflicts or omissions by applying user requirements as the source of truth.\n- Produce a unified, precise design specification document saved as design_spec.md.\n- Ensure specification enables complete backend and frontend implementation without ambiguity.\n\nSpecification Requirements:\n1. **Unified Flask Routes:**\n   - Comprehensive list of route paths, HTTP methods, template filenames.\n   - Complete context variable listings per route.\n\n2. **Consolidated Page Elements:**\n   - Complete element ID lists per page with types and descriptions.\n   - Include all dynamic IDs with {variable} patterns.\n\n3. **Navigation Flow:**\n   - Clear navigation mappings between all pages starting at Dashboard.\n   - Button/link-to-route mappings.\n\n4. **Data File Specifications:**\n   - Confirm data file usage, field orders, formats per user data storage specs.\n   - Include read/write access details.\n\nCRITICAL REQUIREMENTS:\n- Use the write_text_file tool to save output as design_spec.md.\n- Specification must precisely reflect the user requirements with merged inputs.\n- Ensure no design elements, routes, or data file details are omitted.\n- Enable frontend and backend teams to work independently without confusion.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for complete page coverage, specified element IDs, data file usage, and adherence to requirements before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for comprehensive details and no omissions before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify design_spec.md covers all required pages, routes, elements, and data file contracts clearly and precisely for implementation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete JobBoard application implementations (app.py plus templates) and merge into final app.py and templates.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently develop full Python Flask app and templates implementing all design_spec.md \"\n        \"requirements. Each candidate uses isolated template folders and writes app_candidate_*.py and templates_candidate_*/.html files. \"\n        \"ImplementationMerger then reviews both candidate bundles, reconciles differences and conflicts, and produces final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python Flask web applications.\n\nYour goal is to implement a complete, standalone Flask JobBoard application as app_candidate_a.py, along with all required HTML templates saved in the templates_candidate_a directory, following the provided specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md fully to ensure all functional requirements are understood.\n- Implement all Flask routes with correct URL patterns, HTTP methods, and render associated templates.\n- Create templates containing all required element IDs, page titles, and UI elements exactly as specified.\n- Use local data files in the data/ directory for all application data interactions.\n- Isolate your implementation: do NOT read or rely on artifacts from other candidates.\n- Output app_candidate_a.py and templates_candidate_a/*.html files matching the design.\n\nImplementation Guidelines:\n1. Flask Application:\n   - Use standard Flask structure with render_template for HTML pages.\n   - Follow routing and view function conventions strictly.\n   - Read data files using precise pipe-delimited field orders as specified.\n   - Handle form submissions for application submissions and resume uploads.\n\n2. Templates:\n   - Implement Jinja2 templates supporting all UI elements with exact IDs.\n   - Ensure dynamic elements use Jinja2 syntax for variable interpolation and loops.\n   - Match page titles and navigation buttons precisely.\n\n3. Data Handling:\n   - Load and parse data files from data/ directory accurately.\n   - Use data to populate templates dynamically where applicable.\n\nCRITICAL REQUIREMENTS:\n- Use only the write_text_file tool to save your output files.\n- Ensure output filenames are app_candidate_a.py and templates_candidate_a/*.html.\n- Follow the user_task_description and design_spec.md exactly for routes, elements, and data.\n- Do NOT read or incorporate any files from other candidate implementations.\n- Your implementation must work independently and meet all specifications fully.\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python Flask web applications.\n\nYour goal is to develop a fully functional, alternative Flask JobBoard application implementation named app_candidate_b.py, along with all required HTML templates saved in the templates_candidate_b directory, adhering strictly to the specifications.\n\nTask Details:\n- Review the user_task_description and design_spec.md completely to understand all necessary routes, UI elements, data files, and page behaviors.\n- Build all Flask routes to handle requests, return appropriate templates, and process user input as detailed.\n- Design templates with exact element IDs, page titles, dynamic content rendering with Jinja2 as specified.\n- Utilize local data files under the data/ folder for backend data interactions.\n- Work in isolation from other ImplementationEngineer agents; no sharing or reading of other candidate files is allowed.\n- Deliver app_candidate_b.py and templates_candidate_b/*.html outputs based fully on specifications.\n\nImplementation Guidelines:\n1. Flask Backend:\n   - Setup Flask app with all specified routes and data loading logic.\n   - Implement HTML rendering using render_template with correctly named templates.\n   - Handle user form inputs such as application submission and resume upload properly.\n\n2. Template Implementation:\n   - Ensure all UI elements have the exact IDs and structures from the specifications.\n   - Use Jinja2 syntax for loops, conditions, and variable interpolation for dynamic content.\n   - Maintain consistency in page titles and navigation.\n\n3. Data File Processing:\n   - Precisely parse the pipe-delimited data files following the provided field order.\n   - Load and integrate data into pages as required.\n\nCRITICAL REQUIREMENTS:\n- Employ only the write_text_file tool to save your output files.\n- Generate output files named app_candidate_b.py and templates_candidate_b/*.html.\n- Strictly follow user_task_description and design_spec.md for all routes, elements, and data usage.\n- Your implementation must be complete, independent, and comply fully with the specs.\n- No cross-candidate reading or dependence.\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in Python Flask web applications.\n\nYour goal is to merge two independently developed JobBoard Flask application implementations (app_candidate_a.py and app_candidate_b.py, including their templates), resolving conflicts and consolidating features into a single coherent, fully compliant final app.py and templates/*.html suite.\n\nTask Details:\n- Review user_task_description and design_spec.md to understand all requirements, UI element IDs, routing, and data handling.\n- Analyze both candidate implementation sets (app_candidate_a.py, templates_candidate_a/*.html and app_candidate_b.py, templates_candidate_b/*.html).\n- Identify conflicts or discrepancies in route implementations, template element IDs, page titles, and data file usage.\n- Resolve conflicts by selecting the best implementation details or harmonizing both.\n- Produce a unified Flask application (app.py) that fully meets all design_spec.md specs and uses consistent templates in templates/*.html.\n- Ensure the final app.py handles all local data files correctly and supports all UI navigation and functionalities without errors.\n- Maintain strict adherence to specifications for all routes, UI elements, and data interactions.\n\nMerging Guidelines:\n1. Review Differences:\n   - Compare route handlers, function names, and HTTP methods in both app_candidate files.\n   - Examine templates for completeness, element ID consistency, page title accuracy, and dynamic content rendering.\n\n2. Conflict Resolution:\n   - Choose consistent naming and structure.\n   - Integrate best practices from both implementations.\n   - Confirm no missing routes or UI elements.\n\n3. Final Implementation:\n   - Write clean, coherent single app.py file.\n   - Consolidate templates into templates/ directory with all required HTML files.\n   - Maintain exact element IDs, page titles, and navigation workflow.\n\nCRITICAL REQUIREMENTS:\n- Use only the write_text_file tool to output final app.py and templates/*.html.\n- Output filenames must be app.py and templates/*.html.\n- Final implementation must be runnable Flask application fully conforming to design_spec.md and user_task_description.\n- Ensure local data files are handled correctly and data-driven features function as specified.\n- Deliver a clean, integrated codebase without references to candidate-specific artifacts.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Validate app_candidate_a.py and templates_candidate_a for complete adherence to design_spec.md including routes, element IDs, and data file interactions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Validate app_candidate_b.py and templates_candidate_b against design_spec.md requirements for correctness and completeness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Check final app.py and templates/*.html form a complete and runnable Flask app meeting design_spec.md requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Conduct two independent validation reports of app.py and templates, merge fixes and produce the final JobBoard application code bundles.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate syntax, run-time behavior, route coverage, UI element presence, \"\n        \"and data file interfacing for correctness. Each produces a validation report. RepairMerger reviews reports and produces the final \"\n        \"corrected and fully compliant app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask applications and front-end validation.\n\nYour goal is to perform thorough validation of the backend app.py and frontend templates for correct syntax, runtime behavior, route coverage, UI elements, and data file handling, culminating in a detailed validation report.\n\nTask Details:\n- Read user_task_description and design_spec.md fully\n- Analyze app.py and all templates/*.html from ImplementationMerger\n- Validate syntax and runtime start-up success of app.py\n- Validate presence and correctness of all requested Flask routes and templates\n- Verify page titles and required element IDs as per design_spec.md\n- Check integration and correct processing of all local text data files\n- Produce detailed validation_a.md report enumerating findings and issues\n\nValidation Activities:\n1. **Syntax and Runtime Validation**\n   - Use validate_python_file tool on app.py to ensure syntax and runtime pass\n   - Run app.py without errors, report failures if any\n\n2. **Route and UI Element Validation**\n   - Confirm all routes specified in design_spec.md exist and respond correctly\n   - Check all page titles match design specifications exactly\n   - Verify all required element IDs exist in the rendered HTML templates\n   - Check navigation flows and button actions per design_spec.md\n\n3. **Data Integration Validation**\n   - Verify app.py correctly loads and utilizes local text data files as specified\n   - Confirm updates or data manipulations follow design schema and field order\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for thorough validation\n- Use write_text_file tool to write the validation_a.md report\n- Validation report must be detailed, cover all points above, and provide actionable notes\n- Maintain strict adherence to design_spec.md and user_task_description\n- Do not modify code or templates; output only the validation report\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer with expertise in validating Flask backends and Jinja2 frontends.\n\nYour goal is to independently verify correctness of the backend app.py and frontend templates with focus on all required routes, exact element IDs, navigation flows, and data file integration, producing a comprehensive validation report.\n\nTask Details:\n- Read user_task_description and design_spec.md completely\n- Examine app.py and templates/*.html from ImplementationMerger\n- Validate Python file syntax and runtime correctness thoroughly\n- Validate that all required routes defined in design_spec.md exist and function properly\n- Check that all UI element IDs exactly match specification in design_spec.md\n- Verify navigation flows and link correctness across pages\n- Confirm correct integration and usage of all defined local text data files\n- Produce validation_b.md with complete findings and functional validation details\n\nValidation Steps:\n1. **Syntax and Runtime Verification**\n   - Use validate_python_file on app.py to confirm syntax and runtime pass\n   - Execute necessary code snippets to test route behavior where feasible\n\n2. **Route and UI Compliance**\n   - Ensure every route in design_spec.md is implemented in app.py\n   - Confirm all required HTML element IDs present in templates with exact casing\n   - Validate presence of expected page titles on each page as per design_spec.md\n   - Test navigation elements for correct linking and expected behavior\n\n3. **Data File Usage Validation**\n   - Analyze code for correct reading, parsing, and usage of local text data files\n   - Check conformity to data file field orders and formats as specified\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file, execute_python_code, and write_text_file tools accordingly\n- Produce validation_b.md report detailing all checks and identified issues\n- Follow design_spec.md and user_task_description strictly\n- No code changes; only report generation\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in code repair and integration for Flask web applications.\n\nYour goal is to consolidate two independent validation reports, apply all necessary fixes and improvements to app.py and templates/*.html, ensuring full compliance with requirements and design_spec.md, and deliver final correct JobBoard code bundles.\n\nTask Details:\n- Read user_task_description and design_spec.md for context and requirements\n- Analyze original app.py and templates from ImplementationMerger\n- Carefully study validation_a.md and validation_b.md reports for detailed findings and corrections needed\n- Apply all necessary code and template repairs to fix syntax, runtime, route coverage, UI elements, navigation, and data file handling issues identified\n- Preserve original design and feature intent as specified in design_spec.md and user_task_description\n- Ensure final app.py runs without error and passes all validation criteria\n- Ensure all templates/*.html contain correct elements, IDs, titles, and navigation flows\n\nRepair and Merge Guidelines:\n1. **Issue Consolidation**\n   - Aggregate all findings from both validation reports without omission\n   - Prioritize fixes impacting correctness and compliance\n\n2. **Code Repair**\n   - Correct syntax or runtime errors in app.py\n   - Add missing or fix incorrect routes as required\n   - Align data file parsing and usage with design_spec.md schemas\n\n3. **Template Repair**\n   - Add or correct element IDs as per specification strictly\n   - Correct page titles and navigation elements\n   - Ensure consistent naming and functionality of dynamic elements\n\n4. **Finalization**\n   - Verify corrected app.py passes syntax and runtime checks\n   - Confirm templates render as expected with all required features\n   - Prepare final deliverable code bundles ready for deployment\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively to write final corrected app.py and templates/*.html\n- Strictly adhere to design_spec.md and user_task_description specifications\n- Do NOT introduce new features or unrelated code changes\n- Output final corrected app.py and templates/*.html files as specified artifacts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Review validation_a.md for actionable detailed findings to enable effective repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Evaluate validation_b.md for completeness and detailed validation of all functional and UI requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html accurately implement all requirements and preserve design_spec.md intent after repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'JobBoard' Web Application

## 1. Objective
Develop a comprehensive web application named 'JobBoard' using Python, with data managed through local text files. The application enables users to browse job postings, submit resumes, track applications, view company profiles, and manage job applications. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'JobBoard' application is Python.

## 3. Page Design

The 'JobBoard' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Job Board Dashboard
- **Overview**: The main hub displaying featured job postings, latest opportunities, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-jobs** - Type: Div - Display of featured job recommendations.
  - **ID: browse-jobs-button** - Type: Button - Button to navigate to job listings page.
  - **ID: my-applications-button** - Type: Button - Button to navigate to applications tracking page.
  - **ID: companies-button** - Type: Button - Button to navigate to companies directory page.

### 2. Job Listings Page
- **Page Title**: Job Listings
- **Overview**: A page displaying all available job postings with search and filter capabilities.
- **Elements**:
  - **ID: listings-page** - Type: Div - Container for the listings page.
  - **ID: search-input** - Type: Input - Field to search jobs by title, company, or location.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by job category (Technology, Finance, Healthcare, etc.).
  - **ID: location-filter** - Type: Dropdown - Dropdown to filter by location (Remote, On-site, Hybrid).
  - **ID: jobs-grid** - Type: Div - Grid displaying job cards with title, company, location, and salary range.
  - **ID: view-job-button-{job_id}** - Type: Button - Button to view job details (each job card has this).

### 3. Job Details Page
- **Page Title**: Job Details
- **Overview**: A page displaying detailed information about a specific job posting.
- **Elements**:
  - **ID: job-details-page** - Type: Div - Container for the job details page.
  - **ID: job-title** - Type: H1 - Display job title.
  - **ID: company-name** - Type: Div - Display company name.
  - **ID: job-description** - Type: Div - Display full job description and requirements.
  - **ID: salary-range** - Type: Div - Display salary range.
  - **ID: apply-now-button** - Type: Button - Button to apply for the job.

### 4. Application Form Page
- **Page Title**: Submit Application
- **Overview**: A page for users to submit job applications with resume and cover letter.
- **Elements**:
  - **ID: application-form-page** - Type: Div - Container for the application form page.
  - **ID: applicant-name** - Type: Input - Field to input applicant name.
  - **ID: applicant-email** - Type: Input - Field to input applicant email.
  - **ID: resume-upload** - Type: File Input - Field to upload resume file.
  - **ID: cover-letter** - Type: Textarea - Field to enter cover letter text.
  - **ID: submit-application-button** - Type: Button - Button to submit application.

### 5. Application Tracking Page
- **Page Title**: My Applications
- **Overview**: A page displaying all submitted applications with status tracking.
- **Elements**:
  - **ID: tracking-page** - Type: Div - Container for the tracking page.
  - **ID: applications-table** - Type: Table - Table displaying applications with job title, company, status, and date applied.
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Applied, Under Review, Interview, Rejected).
  - **ID: view-application-button-{app_id}** - Type: Button - Button to view application details (each application has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Companies Directory Page
- **Page Title**: Company Directory
- **Overview**: A page displaying all registered companies with their profiles and available jobs.
- **Elements**:
  - **ID: companies-page** - Type: Div - Container for the companies page.
  - **ID: companies-list** - Type: Div - List of company cards with company name, industry, and employee count.
  - **ID: search-company-input** - Type: Input - Field to search companies by name or industry.
  - **ID: view-company-button-{company_id}** - Type: Button - Button to view company profile (each company card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Company Profile Page
- **Page Title**: Company Profile
- **Overview**: A page displaying detailed information about a specific company.
- **Elements**:
  - **ID: company-profile-page** - Type: Div - Container for the company profile page.
  - **ID: company-info** - Type: Div - Display company name, industry, location, and description.
  - **ID: company-jobs** - Type: Div - Display all open jobs from this company.
  - **ID: jobs-list** - Type: Div - List of jobs with titles and status indicators.
  - **ID: view-job-button-{job_id}** - Type: Button - Button to view job details from company profile.
  - **ID: back-to-companies** - Type: Button - Button to go back to companies directory.

### 8. Resume Management Page
- **Page Title**: My Resumes
- **Overview**: A page for users to upload and manage multiple resumes.
- **Elements**:
  - **ID: resume-page** - Type: Div - Container for the resume page.
  - **ID: resumes-list** - Type: Div - List of uploaded resumes with upload date.
  - **ID: upload-resume-button** - Type: Button - Button to upload a new resume.
  - **ID: resume-file-input** - Type: File Input - Hidden file input for resume upload.
  - **ID: delete-resume-button-{resume_id}** - Type: Button - Button to delete a resume (each resume has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Search Results Page
- **Page Title**: Search Results
- **Overview**: A page displaying search results for jobs and companies.
- **Elements**:
  - **ID: search-results-page** - Type: Div - Container for the search results page.
  - **ID: search-query-display** - Type: Div - Display the search query entered.
  - **ID: results-tabs** - Type: Div - Tabs to switch between job results and company results.
  - **ID: job-results** - Type: Div - Display search results for jobs.
  - **ID: company-results** - Type: Div - Display search results for companies.
  - **ID: no-results-message** - Type: Div - Display when no results are found.

## 4. Data Storage

The 'JobBoard' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Jobs Data
- **File Name**: `jobs.txt`
- **Data Format**:
  ```
  job_id|title|company_id|location|salary_min|salary_max|category|description|posted_date
  ```
- **Example Data**:
  ```
  1|Senior Python Developer|1|Remote|80000|120000|Technology|Experienced Python developer for web applications|2025-01-15
  2|Data Analyst|2|New York, NY|60000|85000|Finance|Analyze financial data and create reports|2025-01-16
  3|Healthcare Administrator|3|Los Angeles, CA|50000|70000|Healthcare|Manage hospital operations and patient records|2025-01-14
  ```

### 2. Companies Data
- **File Name**: `companies.txt`
- **Data Format**:
  ```
  company_id|company_name|industry|location|employee_count|description
  ```
- **Example Data**:
  ```
  1|TechCorp|Technology|San Francisco, CA|500|Leading software solutions provider
  2|FinanceHub|Finance|New York, NY|300|Innovative financial services company
  3|MediCare|Healthcare|Los Angeles, CA|200|Premier healthcare management organization
  ```

### 3. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Technology|Software, IT, and tech-related positions
  2|Finance|Banking, accounting, and finance positions
  3|Healthcare|Medical and healthcare industry positions
  ```

### 4. Applications Data
- **File Name**: `applications.txt`
- **Data Format**:
  ```
  application_id|job_id|applicant_name|applicant_email|status|applied_date|resume_id
  ```
- **Example Data**:
  ```
  1|1|John Doe|john@email.com|Under Review|2025-01-17|1
  2|2|Jane Smith|jane@email.com|Applied|2025-01-16|2
  3|3|Robert Johnson|robert@email.com|Interview|2025-01-15|3
  ```

### 5. Resumes Data
- **File Name**: `resumes.txt`
- **Data Format**:
  ```
  resume_id|applicant_name|applicant_email|filename|upload_date|summary
  ```
- **Example Data**:
  ```
  1|John Doe|john@email.com|john_resume.pdf|2025-01-17|Senior developer with 8 years experience
  2|Jane Smith|jane@email.com|jane_resume.pdf|2025-01-16|Data analyst with financial background
  3|Robert Johnson|robert@email.com|robert_resume.pdf|2025-01-15|Healthcare administrator with 5 years experience
  ```

### 6. Job Categories Mapping Data
- **File Name**: `job_categories.txt`
- **Data Format**:
  ```
  mapping_id|job_id|category_id
  ```
- **Example Data**:
  ```
  1|1|1
  2|2|2
  3|3|3
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
            """You are a Web Application Design Analyst specializing in comprehensive specification creation for Flask-based job board applications.

Your goal is to produce a complete design specification that covers all 9 pages specified in the user requirements, including Flask routes, template filenames, page titles, element IDs, input/output controls, user navigation starting from the Dashboard page, and data read/write interactions with local text files.

Task Details:
- Read the full user_task_description artifact.
- Produce a detailed design specification saved as design_candidate_a.md.
- Include all required Flask routes with method details, mapping to template files.
- Specify exact element IDs for each page including dynamic IDs with patterns.
- Detail page titles exactly as specified.
- Describe user navigation flows starting at the Dashboard page.
- Document data file usage, read/write operations, and field formats based on provided data storage specs.

Specification Requirements:
1. **Flask Routes and Templates:**
   - Provide route paths, HTTP methods, and the template file each renders.
   - Define context variables passed to templates precisely.

2. **Page Elements and Layout:**
   - List all element IDs per page with descriptions and types (e.g., div, button, input).
   - Specify dynamic element ID patterns using {variable} syntax.

3. **Navigation Flow:**
   - Map user interaction from buttons and links to respective routes.
   - Start navigation explicitly from the Dashboard page.

4. **Data File Integration:**
   - For each data file, specify path (data/*.txt), format with exact field order, read/write usage per route or page.
   - Use pipe-delimited '|' format consistently.

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to save the output as design_candidate_a.md.
- Follow all user task specifications precisely without omissions.
- Ensure the specification enables independent implementation of frontend and backend.
- Do not cross-reference any other design candidates or outputs.

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Design Analyst with expertise in Flask applications, focused on independent comprehensive design specification production.

Your goal is to independently create an alternative detailed design specification that fully addresses all 9 pages from the user requirements, including Flask routes, template filenames, element IDs, user interactions, navigation flow, and data file formats and usage, without viewing or referencing DesignAnalystA's work.

Task Details:
- Analyze the entire user_task_description provided.
- Produce a detailed design specification saved as design_candidate_b.md.
- Include all necessary Flask routes aligned to template filenames.
- Specify exact element IDs including those with dynamic variables.
- Clearly define page titles and their usage.
- Lay out navigation workflows consistent with provided specifications.
- Specify data read and write operations with exact data file formats and paths.

Specification Details:
1. **Routes and Templates:**
   - List all routes with HTTP methods and linked templates.
   - Define the context variables for each route.

2. **Page Elements:**
   - List element IDs and their types, including dynamic IDs with {parameter} patterns.
   - Ensure elements align with user interface requirements.

3. **User Navigation:**
   - Explicitly start navigation from Dashboard.
   - Map buttons and links to their respective routes.

4. **Data Files:**
   - Document all relevant data files with fields, format, read/write usage.
   - Follow pipe '|' delimited format precisely.

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to output the specification as design_candidate_b.md.
- Follow user requirements fully with no omissions.
- Ensure the spec enables separate frontend and backend development.
- Do not consult or use DesignAnalystA’s data or outputs.

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Integration Specialist expert in unifying multiple web application design specifications into a consistent master specification.

Your goal is to review design_candidate_a.md and design_candidate_b.md along with the original user_task_description to identify any omissions, conflicts, or inconsistencies, then synthesize and produce a single detailed design_spec.md covering all Flask routes, page titles, element IDs, template filenames, navigation workflows, all page elements, and data file interfaces required to fully implement the JobBoard application.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md artifacts.
- Compare and analyze both candidate specifications for completeness and consistency.
- Resolve conflicts or omissions by applying user requirements as the source of truth.
- Produce a unified, precise design specification document saved as design_spec.md.
- Ensure specification enables complete backend and frontend implementation without ambiguity.

Specification Requirements:
1. **Unified Flask Routes:**
   - Comprehensive list of route paths, HTTP methods, template filenames.
   - Complete context variable listings per route.

2. **Consolidated Page Elements:**
   - Complete element ID lists per page with types and descriptions.
   - Include all dynamic IDs with {variable} patterns.

3. **Navigation Flow:**
   - Clear navigation mappings between all pages starting at Dashboard.
   - Button/link-to-route mappings.

4. **Data File Specifications:**
   - Confirm data file usage, field orders, formats per user data storage specs.
   - Include read/write access details.

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to save output as design_spec.md.
- Specification must precisely reflect the user requirements with merged inputs.
- Ensure no design elements, routes, or data file details are omitted.
- Enable frontend and backend teams to work independently without confusion.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Software Developer specializing in Python Flask web applications.

Your goal is to implement a complete, standalone Flask JobBoard application as app_candidate_a.py, along with all required HTML templates saved in the templates_candidate_a directory, following the provided specifications.

Task Details:
- Read user_task_description and design_spec.md fully to ensure all functional requirements are understood.
- Implement all Flask routes with correct URL patterns, HTTP methods, and render associated templates.
- Create templates containing all required element IDs, page titles, and UI elements exactly as specified.
- Use local data files in the data/ directory for all application data interactions.
- Isolate your implementation: do NOT read or rely on artifacts from other candidates.
- Output app_candidate_a.py and templates_candidate_a/*.html files matching the design.

Implementation Guidelines:
1. Flask Application:
   - Use standard Flask structure with render_template for HTML pages.
   - Follow routing and view function conventions strictly.
   - Read data files using precise pipe-delimited field orders as specified.
   - Handle form submissions for application submissions and resume uploads.

2. Templates:
   - Implement Jinja2 templates supporting all UI elements with exact IDs.
   - Ensure dynamic elements use Jinja2 syntax for variable interpolation and loops.
   - Match page titles and navigation buttons precisely.

3. Data Handling:
   - Load and parse data files from data/ directory accurately.
   - Use data to populate templates dynamically where applicable.

CRITICAL REQUIREMENTS:
- Use only the write_text_file tool to save your output files.
- Ensure output filenames are app_candidate_a.py and templates_candidate_a/*.html.
- Follow the user_task_description and design_spec.md exactly for routes, elements, and data.
- Do NOT read or incorporate any files from other candidate implementations.
- Your implementation must work independently and meet all specifications fully.

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Python Flask web applications.

Your goal is to develop a fully functional, alternative Flask JobBoard application implementation named app_candidate_b.py, along with all required HTML templates saved in the templates_candidate_b directory, adhering strictly to the specifications.

Task Details:
- Review the user_task_description and design_spec.md completely to understand all necessary routes, UI elements, data files, and page behaviors.
- Build all Flask routes to handle requests, return appropriate templates, and process user input as detailed.
- Design templates with exact element IDs, page titles, dynamic content rendering with Jinja2 as specified.
- Utilize local data files under the data/ folder for backend data interactions.
- Work in isolation from other ImplementationEngineer agents; no sharing or reading of other candidate files is allowed.
- Deliver app_candidate_b.py and templates_candidate_b/*.html outputs based fully on specifications.

Implementation Guidelines:
1. Flask Backend:
   - Setup Flask app with all specified routes and data loading logic.
   - Implement HTML rendering using render_template with correctly named templates.
   - Handle user form inputs such as application submission and resume upload properly.

2. Template Implementation:
   - Ensure all UI elements have the exact IDs and structures from the specifications.
   - Use Jinja2 syntax for loops, conditions, and variable interpolation for dynamic content.
   - Maintain consistency in page titles and navigation.

3. Data File Processing:
   - Precisely parse the pipe-delimited data files following the provided field order.
   - Load and integrate data into pages as required.

CRITICAL REQUIREMENTS:
- Employ only the write_text_file tool to save your output files.
- Generate output files named app_candidate_b.py and templates_candidate_b/*.html.
- Strictly follow user_task_description and design_spec.md for all routes, elements, and data usage.
- Your implementation must be complete, independent, and comply fully with the specs.
- No cross-candidate reading or dependence.

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in Python Flask web applications.

Your goal is to merge two independently developed JobBoard Flask application implementations (app_candidate_a.py and app_candidate_b.py, including their templates), resolving conflicts and consolidating features into a single coherent, fully compliant final app.py and templates/*.html suite.

Task Details:
- Review user_task_description and design_spec.md to understand all requirements, UI element IDs, routing, and data handling.
- Analyze both candidate implementation sets (app_candidate_a.py, templates_candidate_a/*.html and app_candidate_b.py, templates_candidate_b/*.html).
- Identify conflicts or discrepancies in route implementations, template element IDs, page titles, and data file usage.
- Resolve conflicts by selecting the best implementation details or harmonizing both.
- Produce a unified Flask application (app.py) that fully meets all design_spec.md specs and uses consistent templates in templates/*.html.
- Ensure the final app.py handles all local data files correctly and supports all UI navigation and functionalities without errors.
- Maintain strict adherence to specifications for all routes, UI elements, and data interactions.

Merging Guidelines:
1. Review Differences:
   - Compare route handlers, function names, and HTTP methods in both app_candidate files.
   - Examine templates for completeness, element ID consistency, page title accuracy, and dynamic content rendering.

2. Conflict Resolution:
   - Choose consistent naming and structure.
   - Integrate best practices from both implementations.
   - Confirm no missing routes or UI elements.

3. Final Implementation:
   - Write clean, coherent single app.py file.
   - Consolidate templates into templates/ directory with all required HTML files.
   - Maintain exact element IDs, page titles, and navigation workflow.

CRITICAL REQUIREMENTS:
- Use only the write_text_file tool to output final app.py and templates/*.html.
- Output filenames must be app.py and templates/*.html.
- Final implementation must be runnable Flask application fully conforming to design_spec.md and user_task_description.
- Ensure local data files are handled correctly and data-driven features function as specified.
- Deliver a clean, integrated codebase without references to candidate-specific artifacts.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask applications and front-end validation.

Your goal is to perform thorough validation of the backend app.py and frontend templates for correct syntax, runtime behavior, route coverage, UI elements, and data file handling, culminating in a detailed validation report.

Task Details:
- Read user_task_description and design_spec.md fully
- Analyze app.py and all templates/*.html from ImplementationMerger
- Validate syntax and runtime start-up success of app.py
- Validate presence and correctness of all requested Flask routes and templates
- Verify page titles and required element IDs as per design_spec.md
- Check integration and correct processing of all local text data files
- Produce detailed validation_a.md report enumerating findings and issues

Validation Activities:
1. **Syntax and Runtime Validation**
   - Use validate_python_file tool on app.py to ensure syntax and runtime pass
   - Run app.py without errors, report failures if any

2. **Route and UI Element Validation**
   - Confirm all routes specified in design_spec.md exist and respond correctly
   - Check all page titles match design specifications exactly
   - Verify all required element IDs exist in the rendered HTML templates
   - Check navigation flows and button actions per design_spec.md

3. **Data Integration Validation**
   - Verify app.py correctly loads and utilizes local text data files as specified
   - Confirm updates or data manipulations follow design schema and field order

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for thorough validation
- Use write_text_file tool to write the validation_a.md report
- Validation report must be detailed, cover all points above, and provide actionable notes
- Maintain strict adherence to design_spec.md and user_task_description
- Do not modify code or templates; output only the validation report

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer with expertise in validating Flask backends and Jinja2 frontends.

Your goal is to independently verify correctness of the backend app.py and frontend templates with focus on all required routes, exact element IDs, navigation flows, and data file integration, producing a comprehensive validation report.

Task Details:
- Read user_task_description and design_spec.md completely
- Examine app.py and templates/*.html from ImplementationMerger
- Validate Python file syntax and runtime correctness thoroughly
- Validate that all required routes defined in design_spec.md exist and function properly
- Check that all UI element IDs exactly match specification in design_spec.md
- Verify navigation flows and link correctness across pages
- Confirm correct integration and usage of all defined local text data files
- Produce validation_b.md with complete findings and functional validation details

Validation Steps:
1. **Syntax and Runtime Verification**
   - Use validate_python_file on app.py to confirm syntax and runtime pass
   - Execute necessary code snippets to test route behavior where feasible

2. **Route and UI Compliance**
   - Ensure every route in design_spec.md is implemented in app.py
   - Confirm all required HTML element IDs present in templates with exact casing
   - Validate presence of expected page titles on each page as per design_spec.md
   - Test navigation elements for correct linking and expected behavior

3. **Data File Usage Validation**
   - Analyze code for correct reading, parsing, and usage of local text data files
   - Check conformity to data file field orders and formats as specified

CRITICAL REQUIREMENTS:
- Use validate_python_file, execute_python_code, and write_text_file tools accordingly
- Produce validation_b.md report detailing all checks and identified issues
- Follow design_spec.md and user_task_description strictly
- No code changes; only report generation

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in code repair and integration for Flask web applications.

Your goal is to consolidate two independent validation reports, apply all necessary fixes and improvements to app.py and templates/*.html, ensuring full compliance with requirements and design_spec.md, and deliver final correct JobBoard code bundles.

Task Details:
- Read user_task_description and design_spec.md for context and requirements
- Analyze original app.py and templates from ImplementationMerger
- Carefully study validation_a.md and validation_b.md reports for detailed findings and corrections needed
- Apply all necessary code and template repairs to fix syntax, runtime, route coverage, UI elements, navigation, and data file handling issues identified
- Preserve original design and feature intent as specified in design_spec.md and user_task_description
- Ensure final app.py runs without error and passes all validation criteria
- Ensure all templates/*.html contain correct elements, IDs, titles, and navigation flows

Repair and Merge Guidelines:
1. **Issue Consolidation**
   - Aggregate all findings from both validation reports without omission
   - Prioritize fixes impacting correctness and compliance

2. **Code Repair**
   - Correct syntax or runtime errors in app.py
   - Add missing or fix incorrect routes as required
   - Align data file parsing and usage with design_spec.md schemas

3. **Template Repair**
   - Add or correct element IDs as per specification strictly
   - Correct page titles and navigation elements
   - Ensure consistent naming and functionality of dynamic elements

4. **Finalization**
   - Verify corrected app.py passes syntax and runtime checks
   - Confirm templates render as expected with all required features
   - Prepare final deliverable code bundles ready for deployment

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively to write final corrected app.py and templates/*.html
- Strictly adhere to design_spec.md and user_task_description specifications
- Do NOT introduce new features or unrelated code changes
- Output final corrected app.py and templates/*.html files as specified artifacts

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
        ("DesignMerger", """Check design_candidate_a.md for complete page coverage, specified element IDs, data file usage, and adherence to requirements before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for comprehensive details and no omissions before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify design_spec.md covers all required pages, routes, elements, and data file contracts clearly and precisely for implementation.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Validate app_candidate_a.py and templates_candidate_a for complete adherence to design_spec.md including routes, element IDs, and data file interactions.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Validate app_candidate_b.py and templates_candidate_b against design_spec.md requirements for correctness and completeness.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Check final app.py and templates/*.html form a complete and runnable Flask app meeting design_spec.md requirements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Review validation_a.md for actionable detailed findings to enable effective repairs.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Evaluate validation_b.md for completeness and detailed validation of all functional and UI requirements.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm final app.py and templates/*.html accurately implement all requirements and preserve design_spec.md intent after repairs.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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

    # Parallel generation by DesignAnalystA and DesignAnalystB
    await asyncio.gather(
        execute(DesignAnalystA, "Produce complete design specification and save as design_candidate_a.md"),
        execute(DesignAnalystB, "Produce complete design specification and save as design_candidate_b.md")
    )

    # Read outputs of DesignAnalystA and DesignAnalystB
    design_a_content, design_b_content = "", ""
    try:
        design_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge specifications by DesignMerger
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_a_content}\n\n"
                  f"=== DesignAnalystB ===\n{design_b_content}\n")
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel implementation by Engineer A and B
    await asyncio.gather(
        execute(
            ImplementationEngineerA,
            "Implement full Flask JobBoard app as app_candidate_a.py with templates in templates_candidate_a/*.html. "
            "Follow design_spec.md and user_task_description strictly, isolate from other candidates."
        ),
        execute(
            ImplementationEngineerB,
            "Implement full Flask JobBoard app as app_candidate_b.py with templates in templates_candidate_b/*.html. "
            "Follow design_spec.md and user_task_description strictly, isolate from other candidates."
        )
    )

    # Read outputs from both candidates for merging
    app_a_code, app_b_code = "", ""
    templates_a_content, templates_b_content = "", ""
    try:
        app_a_code = open("app_candidate_a.py").read()
    except Exception:
        pass
    try:
        app_b_code = open("app_candidate_b.py").read()
    except Exception:
        pass
    # For templates, reading all files is complex; inject placeholder strings
    try:
        templates_a_content = open("templates_candidate_a/template_list.txt").read()
    except Exception:
        templates_a_content = ""
    try:
        templates_b_content = open("templates_candidate_b/template_list.txt").read()
    except Exception:
        templates_b_content = ""

    # Merge implementations into final app.py and templates/*.html
    await execute(
        ImplementationMerger,
        f"Merge independent implementations into final app.py and templates/*.html. "
        f"User requirements and design_spec.md apply. "
        f"=== app_candidate_a.py ===\n{app_a_code}\n\n"
        f"=== app_candidate_b.py ===\n{app_b_code}\n\n"
        f"=== templates_candidate_a content summary ===\n{templates_a_content}\n\n"
        f"=== templates_candidate_b content summary ===\n{templates_b_content}"
    )
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
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=60
    )

    # Parallel validation by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate backend app.py and frontend templates/*.html thoroughly for syntax, runtime, route coverage, UI elements, "
                "and data file integration. Produce detailed validation_a.md report."),
        execute(ValidationEngineerB,
                "Independently validate backend app.py and templates/*.html for syntax, runtime, route coverage, exact element IDs, "
                "navigation flows, and data file usage. Produce detailed validation_b.md report.")
    )

    # Read validation reports for merger
    validation_a_report, validation_b_report = "", ""
    try: validation_a_report = open("validation_a.md").read()
    except: pass
    try: validation_b_report = open("validation_b.md").read()
    except: pass

    # RepairMerger reviews validation reports and produces final corrected app.py and templates/*.html
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
