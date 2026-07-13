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
# 20260713_210029_788505/main_20260713_210029_788505.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs for the TravelPlanner app including all page routes, titles, element IDs, and features, then merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently produce complete design candidates detailing Flask routes, page titles, element IDs, \"\n        \"navigation buttons, data file usage, and interactions for all 10 specified pages of TravelPlanner in parallel without reading each other's output. \"\n        \"DesignMerger then reads both design candidates and writes one merged design_spec.md capturing a coherent, exact, and implementation-ready specification.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Designer specializing in detailed UI/UX and route design for Flask web applications.\n\nYour goal is to create a complete and detailed design candidate for the TravelPlanner app covering all 10 specified pages, including all Flask routes, page titles, \nelement IDs, button actions, navigation, and data file usage. The design must start the site at the Dashboard page and enforce no authentication requirements.\n\nTask Details:\n- Read user_task_description fully to understand page requirements and data storage formats\n- Produce design_candidate_a.md describing all pages, routes, element IDs, button/function mappings, and data file access\n- Focus on covering EVERY specified element ID and interaction detailed in the user task\n- Ensure clear route paths that map to the specified pages and include dynamic route parameters where needed\n\nDesign Requirements:\n1. **Page Routes and Titles**\n   - List all Flask route paths and corresponding page titles precisely\n   - Root route ('/') must load or redirect to the Dashboard page\n2. **Element IDs and Navigation**\n   - For each page, specify all static and dynamic element IDs (e.g., view-destination-button-{dest_id})\n   - Define button actions and navigation link mappings linking to route functions\n3. **Data File Usage**\n   - Specify which data files (e.g., destinations.txt) each page accesses and how data is displayed or manipulated\n4. **No Authentication**\n   - Confirm no login/authentication routes or mechanisms are included\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md\n- Provide consistent and clear names for routes and buttons\n- Cover the entire scope of the user task thoroughly without omissions\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Designer specializing in full-stack design specifications for Flask-based projects.\n\nYour goal is to independently produce an alternative complete design candidate for TravelPlanner app, detailing Flask route definitions, all page titles, element IDs, \nnavigation elements, and data storage methods ensuring every specified page and interface control is covered exactly as per the user task.\n\nTask Details:\n- Thoroughly analyze user_task_description for the 10 pages, associated UI controls, and data storage requirements\n- Write design_candidate_b.md with alternative but complete definitions of routes, page titles, element IDs, button and link mappings\n- Detail data file usage per page, specifying how data is consumed or updated\n- Ensure the site starts on Dashboard route and has no authentication elements\n\nDesign Requirements:\n1. **Complete Route List**\n   - Include all URL endpoints, dynamic segments, and corresponding pages\n2. **UI Elements**\n   - Enumerate all element IDs per page, distinguishing static and dynamic elements\n   - Define button/link functions clearly and precisely\n3. **Data Access Specification**\n   - Map each page to the relevant data files used (e.g., itineraries.txt for the itinerary page)\n4. **Authentication Exclusion**\n   - Explicitly note that no authentication or user sessions are required\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_b.md\n- Ensure alternative design fulfills all data and UI requirements without missing details\n- Be consistent and exact in naming and structure to facilitate merging\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a System Architect specializing in consolidating multiple design specifications into a single coherent implementation-ready specification.\n\nYour goal is to merge design_candidate_a.md and design_candidate_b.md into a unified design_spec.md that contains consistent, conflict-free Flask routes, page titles, \nelement IDs, button actions, data file accesses, and overall site behavior for the TravelPlanner app as described by the user task and candidate inputs.\n\nTask Details:\n- Read user_task_description along with design_candidate_a.md and design_candidate_b.md\n- Identify and resolve conflicts in route definitions, element ID naming, button/link actions, and data file usage\n- Ensure coverage of all 10 pages and all UI components described in the user task\n- The root route must load the Dashboard page; no authentication is to be included\n- Create a clear, concise, and implementable design_spec.md document containing:\n  - Complete route list with paths and handlers\n  - Page titles exactly as specified\n  - Complete element ID list per page (static and dynamic)\n  - Button/link mappings to routes or functions\n  - Data file usage per page with access details\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_spec.md\n- Produce a clean, well-structured, and fully integrated single design spec document\n- Maintain naming consistency and logical organization to facilitate direct implementation\n- Ensure no information loss from either candidate unless justified by conflict resolution\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_a.md covers all 10 pages with detailed routes, element IDs, buttons, data file integration, and no authentication.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_b.md completeness and correctness covering all required pages, UI elements, and data access details.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Ensure design_spec.md is consistent, conflict-free and contains an exact, implementation-ready specification for all pages and features.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete TravelPlanner web app implementations with Flask Python backend and templates, then merge into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement the full TravelPlanner Flask web app with app_candidate_*.py and templates_candidate_*/.html in isolation based on design_spec.md. \"\n        \"Each enforces routing, page titles, element IDs, data file interaction per specification, and no authentication. ImplementationMerger then compares both and writes merged app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.\n\nYour goal is to independently implement a complete TravelPlanner Flask web application, ensuring all routes, page titles, UI element IDs, navigation buttons, and local text file data handling conform to the design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md provided by DesignMerger\n- Produce a full Flask backend named app_candidate_a.py with all specified routes starting at Dashboard\n- Create all HTML templates in templates_candidate_a/ with precise element IDs and page titles\n- Use data files from the 'data' folder exactly as specified in design_spec.md for all features\n- No authentication should be implemented; the app is fully accessible\n\nImplementation Requirements:\n1. **Flask App Setup and Routing**:\n   - Implement all Flask routes from the specification with correct function names and HTTP methods\n   - Ensure route '/' redirects to the Dashboard page\n   - Use Flask's render_template to render corresponding HTML templates\n2. **Template and UI Elements**:\n   - Create HTML templates with exact required element IDs (static and dynamic)\n   - Implement navigation buttons with correct url_for references matching routes\n   - Include all page titles exactly as specified for <title> and <h1>\n3. **Data Handling**:\n   - Load and parse data from text files in 'data/' folder using pipe-delimited format and specified field orders\n   - Handle data for destinations, itineraries, hotels, flights, packages, trips, and bookings\n4. **General**:\n   - Follow best practices for Flask and Jinja2 templating\n   - Handle errors gracefully and maintain consistent naming and structure\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all templates_candidate_a/*.html\n- Adhere strictly to design_spec.md for all routes, UI elements, and data usage\n- No features outside specification, no authentication\n- Ensure output filenames and directory structures match requirements exactly\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.\n\nYour goal is to independently implement a complete TravelPlanner Flask web application, ensuring all routes, page titles, UI element IDs, navigation buttons, and local text file data handling strictly follow the design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md provided by DesignMerger\n- Produce a full Flask backend named app_candidate_b.py with all specified routes starting at Dashboard\n- Create all HTML templates in templates_candidate_b/ with exact element IDs and page titles as specified\n- Use 'data' directory text files exactly as specified for all application data\n- No authentication implemented; all functionality is publicly accessible\n\nImplementation Requirements:\n1. **Flask Backend**:\n   - Implement all Flask routes with method correctness and route names per specification\n   - Ensure root route redirects to Dashboard\n   - Use render_template with exact template names and context variables\n2. **Frontend Templates**:\n   - Generate templates with all required static and dynamic element IDs precisely as specified\n   - Implement navigation buttons consistent with routing functions\n   - Maintain exact page titles for SEO and UI consistency\n3. **Data Access**:\n   - Load and parse all required data from specified text files with correct pipe-delimited fields\n4. **Best Practices**:\n   - Write clean, maintainable Flask and Jinja2 code paying attention to structure and naming\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and all templates_candidate_b/*.html\n- Strictly follow design_spec.md for routes, templates, data handling, and UI elements\n- Avoid features not present in design_spec.md; no authentication\n- Output exactly as requested with correct filenames and folder structure\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging Flask backend code and frontend templates.\n\nYour goal is to compare two independently implemented TravelPlanner Flask app versions and their HTML templates, resolve all differences, and produce a single, consistent, feature-complete final app.py and set of templates.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_candidate_a.py, templates_candidate_a/*.html, app_candidate_b.py, and templates_candidate_b/*.html\n- Identify discrepancies between the two candidate implementations in routes, UI element IDs, page titles, data file usage, and navigation\n- Select correct, complete, and consistent code and templates per design_spec.md for merging\n- Produce final merged app.py with all routes correctly implemented and using specified data files without authentication\n- Create final set of templates/*.html matching exact UI specifications and navigation buttons as per design_spec.md\n\nMerging Guidelines:\n1. **Backend Code**:\n   - Resolve conflicts by prioritizing correctness, completeness, and adherence to specification\n   - Maintain consistent naming conventions and route implementations\n2. **Frontend Templates**:\n   - Ensure all element IDs (static and dynamic) from specification are present exactly\n   - Page titles and button navigations must match specification exactly\n3. **Data Handling**:\n   - Verify data file loading integrity matches specification and is consistent across features\n4. **General**:\n   - Final outputs must run seamlessly together fulfilling all user requirements and specification details\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save merged app.py and templates/*.html files\n- Strictly enforce design_spec.md for routes, page titles, element IDs, data usage, and navigation\n- Produce clean, maintainable, and fully functional merged outputs\n- Output file names and directory structures MUST be exactly app.py and templates/*.html\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate code and templates for correctness, completeness, Flask route fidelity, and adherence to design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate alternative candidate for full feature coverage, accurate templates, and data file management as per design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Confirm merged app.py and templates/*.html exactly implement design_spec.md and are ready for thorough validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Independently validate the merged TravelPlanner app through two validation reports and merge corrections into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate app.py and templates/*.html for syntax, runtime, route correctness, template rendering, data access, and UI element adherence. \"\n        \"Each produces a validation report. RepairMerger then consumes both validation reports and original merged app to produce a repaired final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask application backend and frontend integration validation.\n\nYour goal is to thoroughly validate the merged backend and frontend implementation to ensure correctness, stability, and conformance to specification, producing a detailed validation report.\n\nTask Details:\n- Read user_task_description, design_spec.md, merged app.py, and templates/*.html\n- Verify Python syntax correctness and runtime Flask startup with app.py\n- Check all Flask routes exist as specified with correct HTTP methods\n- Confirm all page titles and HTML element IDs per design_spec.md exist in templates\n- Validate integration with data files loading and usage in app.py\n- Validate navigation correctness and absence of authentication flows\n- Produce validation_a.md with issues found and improvement suggestions\n\nValidation Requirements:\n**Syntax and Runtime Checks**\n- Use validate_python_file tool on app.py to check syntax and runtime errors\n- Confirm Flask app runs, routes register, and no startup exceptions\n\n**Route and Context Variables Checks**\n- Verify all routes declared in design_spec.md exist in app.py\n- Verify route handlers pass required context variables matching specification\n\n**Template and UI Element Checks**\n- Read templates/*.html to confirm all element IDs from design_spec.md appear exactly\n- Confirm page titles in <title> and <h1> tags match specification\n\n**Data Integration Checks**\n- Confirm app.py reads, parses, and uses data files as specified\n- Verify no data loading errors or missing fields handling\n\n**Navigation Checks**\n- Confirm all navigation buttons/links point to correct routes using url_for\n- Confirm no authentication or user session logic exists\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for automated checks\n- Use write_text_file tool to save validation_a.md report with clear sectioned feedback\n- Focus only on specified files and requirements, avoid speculative checks\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in user interaction and frontend-backend integration validation for Flask web applications.\n\nYour goal is to independently validate user-facing interactions, UI element presence, data handling, and compliance with design requirements, producing a comprehensive validation report.\n\nTask Details:\n- Read user_task_description, design_spec.md, merged app.py, and templates/*.html\n- Perform user interaction validations covering route handling and template rendering\n- Verify data files integration and usage in app.py and displayed information in templates\n- Check UI elements per design_spec.md: element IDs, buttons, inputs, dropdowns exactly as specified\n- Confirm absence of authentication flows and direct access to all features\n- Produce validation_b.md detailing test results, UI checks, and data integration validation\n\nValidation Requirements:\n**Interaction and UI Validations**\n- Test all specified routes for expected HTTP methods and returned content\n- Verify templates render content dynamically per data sources\n- Confirm presence and correct behavior of all UI elements by ID\n\n**Data Handling Validations**\n- Confirm data loaded in app.py from text files reflects correctly in rendered pages\n- Validate filters, search inputs, and buttons correspond to UI design\n\n**Compliance Checks**\n- Ensure testing aligns strictly with design_spec.md requirements\n- Document any discrepancies in UI, data, or routes clearly\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code for backend sanity checks\n- Use write_text_file tool to save validation_b.md report with actionable details\n- Focus on user experience, UI elements, and data correctness only\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in software repair and integration for Flask web applications.\n\nYour goal is to merge and apply corrections based on two independent validation reports into a final repaired backend and frontend implementation that fully comply with the design specification.\n\nTask Details:\n- Read user_task_description, design_spec.md, merged original app.py and templates/*.html\n- Read validation reports validation_a.md and validation_b.md\n- Analyze validation feedback for syntax, runtime, route completeness, UI, and data integration issues\n- Apply necessary code fixes to app.py preserving Flask routes, data file integration, and application logic\n- Revise templates/*.html to correct UI element IDs, page titles, navigation, and data rendering\n- Ensure repaired app.py and templates/*.html fully conform to design_spec.md specifications\n\nImplementation Requirements:\n- Maintain all Flask route handlers and data loading per design_spec.md\n- Ensure UI element IDs and structure precisely match specification\n- Avoid introducing new features or removing valid functionality\n- Keep code clean, maintainable, and consistent\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final repaired app.py and templates/*.html files\n- Thoroughly address all validation report points without altering design spec compliance\n- Deliver final artifacts ready for deployment and user testing\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for actionable, detailed correctness and completeness of syntactic and runtime checks with recommended fixes.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Confirm validation_b.md provides thorough UI and data interaction testing results and aligns with design_spec.md requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure final repaired app.py and templates/*.html fully implement the design_spec.md requirements and address issues raised by both validation reports.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'TravelPlanner' Web Application

## 1. Objective
Develop a comprehensive web application named 'TravelPlanner' using Python, with data managed through local text files. The application enables users to browse destinations, plan itineraries, search accommodations, book flights, view travel packages, and manage trip details. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'TravelPlanner' application is Python.

## 3. Page Design

The 'TravelPlanner' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Travel Planner Dashboard
- **Overview**: The main hub displaying featured destinations, upcoming trips, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-destinations** - Type: Div - Display of featured travel destinations.
  - **ID: upcoming-trips** - Type: Div - Display of upcoming planned trips.
  - **ID: browse-destinations-button** - Type: Button - Button to navigate to destinations page.
  - **ID: plan-itinerary-button** - Type: Button - Button to navigate to itinerary planning page.

### 2. Destinations Page
- **Page Title**: Travel Destinations
- **Overview**: A page displaying all available travel destinations with search and filter capabilities.
- **Elements**:
  - **ID: destinations-page** - Type: Div - Container for the destinations page.
  - **ID: search-destination** - Type: Input - Field to search destinations by name or country.
  - **ID: region-filter** - Type: Dropdown - Dropdown to filter by region (Asia, Europe, Americas, Africa, Oceania).
  - **ID: destinations-grid** - Type: Div - Grid displaying destination cards with image, name, and country.
  - **ID: view-destination-button-{dest_id}** - Type: Button - Button to view destination details (each destination card has this).

### 3. Destination Details Page
- **Page Title**: Destination Details
- **Overview**: A page displaying detailed information about a specific destination.
- **Elements**:
  - **ID: destination-details-page** - Type: Div - Container for the destination details page.
  - **ID: destination-name** - Type: H1 - Display destination name.
  - **ID: destination-country** - Type: Div - Display destination country.
  - **ID: destination-description** - Type: Div - Display detailed description of the destination.
  - **ID: add-to-trip-button** - Type: Button - Button to add destination to trip.
  - **ID: destination-attractions** - Type: Div - Section displaying main attractions and activities.

### 4. Itinerary Planning Page
- **Page Title**: Plan Your Itinerary
- **Overview**: A page for users to create and manage travel itineraries with activities and schedules.
- **Elements**:
  - **ID: itinerary-page** - Type: Div - Container for the itinerary page.
  - **ID: itinerary-name-input** - Type: Input - Field to enter itinerary name.
  - **ID: start-date-input** - Type: Input (date) - Field to select trip start date.
  - **ID: end-date-input** - Type: Input (date) - Field to select trip end date.
  - **ID: add-activity-button** - Type: Button - Button to add activity to itinerary.
  - **ID: itinerary-list** - Type: Div - Display list of created itineraries with edit/delete options.

### 5. Accommodations Page
- **Page Title**: Search Accommodations
- **Overview**: A page for searching and browsing hotel options with filters and pricing.
- **Elements**:
  - **ID: accommodations-page** - Type: Div - Container for the accommodations page.
  - **ID: destination-input** - Type: Input - Field to enter destination city for hotels.
  - **ID: check-in-date** - Type: Input (date) - Field to select check-in date.
  - **ID: check-out-date** - Type: Input (date) - Field to select check-out date.
  - **ID: price-filter** - Type: Dropdown - Dropdown to filter hotels by price range (Budget, Mid-range, Luxury).
  - **ID: hotels-list** - Type: Div - List of available hotels with name, rating, price, and amenities.

### 6. Transportation Page
- **Page Title**: Book Flights
- **Overview**: A page for searching and booking flights with departure and arrival options.
- **Elements**:
  - **ID: transportation-page** - Type: Div - Container for the transportation page.
  - **ID: departure-city** - Type: Input - Field to enter departure city.
  - **ID: arrival-city** - Type: Input - Field to enter arrival city.
  - **ID: departure-date** - Type: Input (date) - Field to select departure date.
  - **ID: flight-class-filter** - Type: Dropdown - Dropdown to filter by flight class (Economy, Business, First Class).
  - **ID: available-flights** - Type: Div - List of available flights with airlines, times, and prices.

### 7. Travel Packages Page
- **Page Title**: Travel Packages
- **Overview**: A page displaying pre-designed travel packages with complete trip information.
- **Elements**:
  - **ID: packages-page** - Type: Div - Container for the packages page.
  - **ID: packages-grid** - Type: Div - Grid displaying travel package cards with destination, duration, and price.
  - **ID: duration-filter** - Type: Dropdown - Dropdown to filter packages by duration (3-5 days, 7-10 days, 14+ days).
  - **ID: view-package-details-button-{pkg_id}** - Type: Button - Button to view package details (each package has this).
  - **ID: book-package-button-{pkg_id}** - Type: Button - Button to book selected package (each package has this).

### 8. Trip Management Page
- **Page Title**: My Trips
- **Overview**: A page displaying all created trips with options to view, edit, or delete them.
- **Elements**:
  - **ID: trips-page** - Type: Div - Container for the trips page.
  - **ID: trips-table** - Type: Table - Table displaying all trips with destination, dates, and status.
  - **ID: view-trip-details-button-{trip_id}** - Type: Button - Button to view trip details (each trip has this).
  - **ID: edit-trip-button-{trip_id}** - Type: Button - Button to edit trip (each trip has this).
  - **ID: delete-trip-button-{trip_id}** - Type: Button - Button to delete trip (each trip has this).

### 9. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Overview**: A page displaying booking confirmation details with reservation information.
- **Elements**:
  - **ID: confirmation-page** - Type: Div - Container for the confirmation page.
  - **ID: confirmation-number** - Type: Div - Display confirmation/booking number.
  - **ID: booking-details** - Type: Div - Display detailed booking information (dates, amounts, locations).
  - **ID: download-itinerary-button** - Type: Button - Button to download trip itinerary as PDF.
  - **ID: share-trip-button** - Type: Button - Button to share trip details.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 10. Travel Recommendations Page
- **Page Title**: Travel Recommendations
- **Overview**: A page displaying personalized travel recommendations and trending destinations.
- **Elements**:
  - **ID: recommendations-page** - Type: Div - Container for the recommendations page.
  - **ID: trending-destinations** - Type: Div - Display trending destinations ranked by popularity.
  - **ID: recommendation-season-filter** - Type: Dropdown - Dropdown to filter by travel season (Spring, Summer, Fall, Winter).
  - **ID: budget-filter** - Type: Dropdown - Dropdown to filter by budget range (Low, Medium, High).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'TravelPlanner' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Destinations Data
- **File Name**: `destinations.txt`
- **Data Format**:
  ```
  dest_id|name|country|region|description|attractions|climate
  ```
- **Example Data**:
  ```
  1|Paris|France|Europe|City of lights and romance with world-class museums|Eiffel Tower, Louvre Museum, Notre-Dame|Temperate
  2|Tokyo|Japan|Asia|Modern metropolis blending tradition and innovation|Senso-ji Temple, Shibuya Crossing, Meiji Shrine|Temperate
  3|Rio de Janeiro|Brazil|Americas|Vibrant beach city with iconic landmarks|Christ the Redeemer, Copacabana Beach, Sugarloaf Mountain|Tropical
  ```

### 2. Itineraries Data
- **File Name**: `itineraries.txt`
- **Data Format**:
  ```
  itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
  ```
- **Example Data**:
  ```
  1|Paris Spring Break|Paris|2025-03-20|2025-03-27|Museum tours, River cruise, Cafe hopping|Planned
  2|Tokyo Adventure|Tokyo|2025-05-01|2025-05-14|Temple visits, Anime district tour, Cooking class|In Progress
  3|Rio Beach Trip|Rio de Janeiro|2025-07-15|2025-07-22|Beach days, Hiking, Night clubs|Planned
  ```

### 3. Hotels Data
- **File Name**: `hotels.txt`
- **Data Format**:
  ```
  hotel_id|name|city|rating|price_per_night|amenities|category
  ```
- **Example Data**:
  ```
  1|Ritz Paris|Paris|5.0|450.00|WiFi, Spa, Restaurant, Pool|Luxury
  2|Hotel Shibuya|Tokyo|4.5|120.00|WiFi, Cafe, Business Center|Mid-range
  3|Copacabana Beach Hotel|Rio de Janeiro|4.0|95.00|Beach access, Restaurant, WiFi|Mid-range
  ```

### 4. Flights Data
- **File Name**: `flights.txt`
- **Data Format**:
  ```
  flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
  ```
- **Example Data**:
  ```
  1|Air France|New York|Paris|10:00|22:30|850.00|Economy|7 hours 30 minutes
  2|JAL|Los Angeles|Tokyo|14:30|15:20 next day|920.00|Business|11 hours 50 minutes
  3|Latam|Miami|Rio de Janeiro|18:00|23:45|380.00|Economy|5 hours 45 minutes
  ```

### 5. Travel Packages Data
- **File Name**: `packages.txt`
- **Data Format**:
  ```
  package_id|package_name|destination|duration_days|price|included_items|difficulty_level
  ```
- **Example Data**:
  ```
  1|Paris Classic Tour|Paris|5|1500.00|Hotel, Flights, Guided tours, Meals|Easy
  2|Tokyo Experience|Tokyo|10|2200.00|Hotel, Flights, Activities, Cultural events|Moderate
  3|Rio Adventure|Rio de Janeiro|7|1800.00|Hotel, Flights, Beach activities, Mountain hiking|Moderate
  ```

### 6. Trips Data
- **File Name**: `trips.txt`
- **Data Format**:
  ```
  trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
  ```
- **Example Data**:
  ```
  1|Summer Vacation 2025|Paris|2025-06-01|2025-06-15|3000.00|Booked|2025-01-10
  2|Winter Holiday|Tokyo|2025-12-15|2025-12-30|4500.00|Planned|2025-01-11
  3|Beach Getaway|Rio de Janeiro|2025-07-01|2025-07-08|2000.00|Pending|2025-01-12
  ```

### 7. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
  ```
- **Example Data**:
  ```
  1|1|Hotel|2025-01-10|750.00|CONF001|Confirmed
  2|2|Flight|2025-01-11|1840.00|CONF002|Confirmed
  3|3|Package|2025-01-12|1800.00|CONF003|Pending
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
            """You are a Web Application Designer specializing in detailed UI/UX and route design for Flask web applications.

Your goal is to create a complete and detailed design candidate for the TravelPlanner app covering all 10 specified pages, including all Flask routes, page titles, 
element IDs, button actions, navigation, and data file usage. The design must start the site at the Dashboard page and enforce no authentication requirements.

Task Details:
- Read user_task_description fully to understand page requirements and data storage formats
- Produce design_candidate_a.md describing all pages, routes, element IDs, button/function mappings, and data file access
- Focus on covering EVERY specified element ID and interaction detailed in the user task
- Ensure clear route paths that map to the specified pages and include dynamic route parameters where needed

Design Requirements:
1. **Page Routes and Titles**
   - List all Flask route paths and corresponding page titles precisely
   - Root route ('/') must load or redirect to the Dashboard page
2. **Element IDs and Navigation**
   - For each page, specify all static and dynamic element IDs (e.g., view-destination-button-{dest_id})
   - Define button actions and navigation link mappings linking to route functions
3. **Data File Usage**
   - Specify which data files (e.g., destinations.txt) each page accesses and how data is displayed or manipulated
4. **No Authentication**
   - Confirm no login/authentication routes or mechanisms are included

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md
- Provide consistent and clear names for routes and buttons
- Cover the entire scope of the user task thoroughly without omissions

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Designer specializing in full-stack design specifications for Flask-based projects.

Your goal is to independently produce an alternative complete design candidate for TravelPlanner app, detailing Flask route definitions, all page titles, element IDs, 
navigation elements, and data storage methods ensuring every specified page and interface control is covered exactly as per the user task.

Task Details:
- Thoroughly analyze user_task_description for the 10 pages, associated UI controls, and data storage requirements
- Write design_candidate_b.md with alternative but complete definitions of routes, page titles, element IDs, button and link mappings
- Detail data file usage per page, specifying how data is consumed or updated
- Ensure the site starts on Dashboard route and has no authentication elements

Design Requirements:
1. **Complete Route List**
   - Include all URL endpoints, dynamic segments, and corresponding pages
2. **UI Elements**
   - Enumerate all element IDs per page, distinguishing static and dynamic elements
   - Define button/link functions clearly and precisely
3. **Data Access Specification**
   - Map each page to the relevant data files used (e.g., itineraries.txt for the itinerary page)
4. **Authentication Exclusion**
   - Explicitly note that no authentication or user sessions are required

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_b.md
- Ensure alternative design fulfills all data and UI requirements without missing details
- Be consistent and exact in naming and structure to facilitate merging

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a System Architect specializing in consolidating multiple design specifications into a single coherent implementation-ready specification.

Your goal is to merge design_candidate_a.md and design_candidate_b.md into a unified design_spec.md that contains consistent, conflict-free Flask routes, page titles, 
element IDs, button actions, data file accesses, and overall site behavior for the TravelPlanner app as described by the user task and candidate inputs.

Task Details:
- Read user_task_description along with design_candidate_a.md and design_candidate_b.md
- Identify and resolve conflicts in route definitions, element ID naming, button/link actions, and data file usage
- Ensure coverage of all 10 pages and all UI components described in the user task
- The root route must load the Dashboard page; no authentication is to be included
- Create a clear, concise, and implementable design_spec.md document containing:
  - Complete route list with paths and handlers
  - Page titles exactly as specified
  - Complete element ID list per page (static and dynamic)
  - Button/link mappings to routes or functions
  - Data file usage per page with access details

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Produce a clean, well-structured, and fully integrated single design spec document
- Maintain naming consistency and logical organization to facilitate direct implementation
- Ensure no information loss from either candidate unless justified by conflict resolution

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.

Your goal is to independently implement a complete TravelPlanner Flask web application, ensuring all routes, page titles, UI element IDs, navigation buttons, and local text file data handling conform to the design specifications.

Task Details:
- Read user_task_description and design_spec.md provided by DesignMerger
- Produce a full Flask backend named app_candidate_a.py with all specified routes starting at Dashboard
- Create all HTML templates in templates_candidate_a/ with precise element IDs and page titles
- Use data files from the 'data' folder exactly as specified in design_spec.md for all features
- No authentication should be implemented; the app is fully accessible

Implementation Requirements:
1. **Flask App Setup and Routing**:
   - Implement all Flask routes from the specification with correct function names and HTTP methods
   - Ensure route '/' redirects to the Dashboard page
   - Use Flask's render_template to render corresponding HTML templates
2. **Template and UI Elements**:
   - Create HTML templates with exact required element IDs (static and dynamic)
   - Implement navigation buttons with correct url_for references matching routes
   - Include all page titles exactly as specified for <title> and <h1>
3. **Data Handling**:
   - Load and parse data from text files in 'data/' folder using pipe-delimited format and specified field orders
   - Handle data for destinations, itineraries, hotels, flights, packages, trips, and bookings
4. **General**:
   - Follow best practices for Flask and Jinja2 templating
   - Handle errors gracefully and maintain consistent naming and structure

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all templates_candidate_a/*.html
- Adhere strictly to design_spec.md for all routes, UI elements, and data usage
- No features outside specification, no authentication
- Ensure output filenames and directory structures match requirements exactly

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.

Your goal is to independently implement a complete TravelPlanner Flask web application, ensuring all routes, page titles, UI element IDs, navigation buttons, and local text file data handling strictly follow the design specifications.

Task Details:
- Read user_task_description and design_spec.md provided by DesignMerger
- Produce a full Flask backend named app_candidate_b.py with all specified routes starting at Dashboard
- Create all HTML templates in templates_candidate_b/ with exact element IDs and page titles as specified
- Use 'data' directory text files exactly as specified for all application data
- No authentication implemented; all functionality is publicly accessible

Implementation Requirements:
1. **Flask Backend**:
   - Implement all Flask routes with method correctness and route names per specification
   - Ensure root route redirects to Dashboard
   - Use render_template with exact template names and context variables
2. **Frontend Templates**:
   - Generate templates with all required static and dynamic element IDs precisely as specified
   - Implement navigation buttons consistent with routing functions
   - Maintain exact page titles for SEO and UI consistency
3. **Data Access**:
   - Load and parse all required data from specified text files with correct pipe-delimited fields
4. **Best Practices**:
   - Write clean, maintainable Flask and Jinja2 code paying attention to structure and naming

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and all templates_candidate_b/*.html
- Strictly follow design_spec.md for routes, templates, data handling, and UI elements
- Avoid features not present in design_spec.md; no authentication
- Output exactly as requested with correct filenames and folder structure

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging Flask backend code and frontend templates.

Your goal is to compare two independently implemented TravelPlanner Flask app versions and their HTML templates, resolve all differences, and produce a single, consistent, feature-complete final app.py and set of templates.

Task Details:
- Read user_task_description, design_spec.md, app_candidate_a.py, templates_candidate_a/*.html, app_candidate_b.py, and templates_candidate_b/*.html
- Identify discrepancies between the two candidate implementations in routes, UI element IDs, page titles, data file usage, and navigation
- Select correct, complete, and consistent code and templates per design_spec.md for merging
- Produce final merged app.py with all routes correctly implemented and using specified data files without authentication
- Create final set of templates/*.html matching exact UI specifications and navigation buttons as per design_spec.md

Merging Guidelines:
1. **Backend Code**:
   - Resolve conflicts by prioritizing correctness, completeness, and adherence to specification
   - Maintain consistent naming conventions and route implementations
2. **Frontend Templates**:
   - Ensure all element IDs (static and dynamic) from specification are present exactly
   - Page titles and button navigations must match specification exactly
3. **Data Handling**:
   - Verify data file loading integrity matches specification and is consistent across features
4. **General**:
   - Final outputs must run seamlessly together fulfilling all user requirements and specification details

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save merged app.py and templates/*.html files
- Strictly enforce design_spec.md for routes, page titles, element IDs, data usage, and navigation
- Produce clean, maintainable, and fully functional merged outputs
- Output file names and directory structures MUST be exactly app.py and templates/*.html

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask application backend and frontend integration validation.

Your goal is to thoroughly validate the merged backend and frontend implementation to ensure correctness, stability, and conformance to specification, producing a detailed validation report.

Task Details:
- Read user_task_description, design_spec.md, merged app.py, and templates/*.html
- Verify Python syntax correctness and runtime Flask startup with app.py
- Check all Flask routes exist as specified with correct HTTP methods
- Confirm all page titles and HTML element IDs per design_spec.md exist in templates
- Validate integration with data files loading and usage in app.py
- Validate navigation correctness and absence of authentication flows
- Produce validation_a.md with issues found and improvement suggestions

Validation Requirements:
**Syntax and Runtime Checks**
- Use validate_python_file tool on app.py to check syntax and runtime errors
- Confirm Flask app runs, routes register, and no startup exceptions

**Route and Context Variables Checks**
- Verify all routes declared in design_spec.md exist in app.py
- Verify route handlers pass required context variables matching specification

**Template and UI Element Checks**
- Read templates/*.html to confirm all element IDs from design_spec.md appear exactly
- Confirm page titles in <title> and <h1> tags match specification

**Data Integration Checks**
- Confirm app.py reads, parses, and uses data files as specified
- Verify no data loading errors or missing fields handling

**Navigation Checks**
- Confirm all navigation buttons/links point to correct routes using url_for
- Confirm no authentication or user session logic exists

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for automated checks
- Use write_text_file tool to save validation_a.md report with clear sectioned feedback
- Focus only on specified files and requirements, avoid speculative checks

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in user interaction and frontend-backend integration validation for Flask web applications.

Your goal is to independently validate user-facing interactions, UI element presence, data handling, and compliance with design requirements, producing a comprehensive validation report.

Task Details:
- Read user_task_description, design_spec.md, merged app.py, and templates/*.html
- Perform user interaction validations covering route handling and template rendering
- Verify data files integration and usage in app.py and displayed information in templates
- Check UI elements per design_spec.md: element IDs, buttons, inputs, dropdowns exactly as specified
- Confirm absence of authentication flows and direct access to all features
- Produce validation_b.md detailing test results, UI checks, and data integration validation

Validation Requirements:
**Interaction and UI Validations**
- Test all specified routes for expected HTTP methods and returned content
- Verify templates render content dynamically per data sources
- Confirm presence and correct behavior of all UI elements by ID

**Data Handling Validations**
- Confirm data loaded in app.py from text files reflects correctly in rendered pages
- Validate filters, search inputs, and buttons correspond to UI design

**Compliance Checks**
- Ensure testing aligns strictly with design_spec.md requirements
- Document any discrepancies in UI, data, or routes clearly

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code for backend sanity checks
- Use write_text_file tool to save validation_b.md report with actionable details
- Focus on user experience, UI elements, and data correctness only

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Engineer specializing in software repair and integration for Flask web applications.

Your goal is to merge and apply corrections based on two independent validation reports into a final repaired backend and frontend implementation that fully comply with the design specification.

Task Details:
- Read user_task_description, design_spec.md, merged original app.py and templates/*.html
- Read validation reports validation_a.md and validation_b.md
- Analyze validation feedback for syntax, runtime, route completeness, UI, and data integration issues
- Apply necessary code fixes to app.py preserving Flask routes, data file integration, and application logic
- Revise templates/*.html to correct UI element IDs, page titles, navigation, and data rendering
- Ensure repaired app.py and templates/*.html fully conform to design_spec.md specifications

Implementation Requirements:
- Maintain all Flask route handlers and data loading per design_spec.md
- Ensure UI element IDs and structure precisely match specification
- Avoid introducing new features or removing valid functionality
- Keep code clean, maintainable, and consistent

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final repaired app.py and templates/*.html files
- Thoroughly address all validation report points without altering design spec compliance
- Deliver final artifacts ready for deployment and user testing

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
        ("DesignMerger", """Verify design_candidate_a.md covers all 10 pages with detailed routes, element IDs, buttons, data file integration, and no authentication.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Verify design_candidate_b.md completeness and correctness covering all required pages, UI elements, and data access details.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Ensure design_spec.md is consistent, conflict-free and contains an exact, implementation-ready specification for all pages and features.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate code and templates for correctness, completeness, Flask route fidelity, and adherence to design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate alternative candidate for full feature coverage, accurate templates, and data file management as per design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Confirm merged app.py and templates/*.html exactly implement design_spec.md and are ready for thorough validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for actionable, detailed correctness and completeness of syntactic and runtime checks with recommended fixes.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Confirm validation_b.md provides thorough UI and data interaction testing results and aligns with design_spec.md requirements.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Ensure final repaired app.py and templates/*.html fully implement the design_spec.md requirements and address issues raised by both validation reports.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        execute(DesignAnalystA, "Create complete design candidate for TravelPlanner with all 10 pages, Flask routes, element IDs, navigation buttons, and data file usage. Save as design_candidate_a.md."),
        execute(DesignAnalystB, "Create an alternative complete design candidate for TravelPlanner with all 10 pages, routes, UI elements, navigation, and data file usage. Save as design_candidate_b.md.")
    )

    # Read outputs of design candidates
    design_candidate_a = ""
    design_candidate_b = ""
    try:
        design_candidate_a = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b = open("design_candidate_b.md").read()
    except:
        pass

    # Execute DesignMerger to produce the unified design_spec.md
    await execute(DesignMerger,
                  f"Merge design_candidate_a.md and design_candidate_b.md into a single coherent design_spec.md for TravelPlanner app, resolving conflicts, ensuring coverage of all 10 pages, routes, element IDs, navigation, and data files. Root route must load Dashboard with no authentication.\n\n"
                  f"=== design_candidate_a.md ===\n{design_candidate_a}\n\n"
                  f"=== design_candidate_b.md ===\n{design_candidate_b}")
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
        recovery_time=45
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
        recovery_time=45
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

    # Run ImplementationEngineerA and ImplementationEngineerB in parallel
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete TravelPlanner Flask app as app_candidate_a.py; create templates_candidate_a/*.html with exact routes, element IDs, page titles, and data handling per design_spec.md."),
        execute(ImplementationEngineerB,
                "Implement complete TravelPlanner Flask app as app_candidate_b.py; create templates_candidate_b/*.html with exact routes, element IDs, page titles, and data handling per design_spec.md.")
    )

    # Read outputs from both implementation agents
    candidate_a_code, candidate_b_code = "", ""
    candidate_a_templates, candidate_b_templates = "", ""
    try:
        candidate_a_code = open("app_candidate_a.py").read()
    except: 
        pass
    try:
        candidate_b_code = open("app_candidate_b.py").read()
    except: 
        pass
    try:
        # Reading content of all template files from templates_candidate_a/ (assuming concatenated or single file for injection)
        # If multiple files, they should be concatenated here for context passing.
        from glob import glob
        paths_a = glob("templates_candidate_a/*.html")
        candidate_a_templates = ""
        for p in paths_a:
            try:
                candidate_a_templates += f"\n=== {p} ===\n" + open(p).read()
            except:
                pass
    except:
        candidate_a_templates = ""
    try:
        paths_b = glob("templates_candidate_b/*.html")
        candidate_b_templates = ""
        for p in paths_b:
            try:
                candidate_b_templates += f"\n=== {p} ===\n" + open(p).read()
            except:
                pass
    except:
        candidate_b_templates = ""

    # Merge results with ImplementationMerger
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{candidate_a_code}\n\n"
                  f"=== templates_candidate_a/*.html ===\n{candidate_a_templates}\n\n"
                  f"=== app_candidate_b.py ===\n{candidate_b_code}\n\n"
                  f"=== templates_candidate_b/*.html ===\n{candidate_b_templates}")
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
        timeout_threshold=450,
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
        timeout_threshold=450,
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
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel validation by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate app.py and templates/*.html for syntax, runtime, routes, context variables, UI elements adherence, and data integration. Produce validation_a.md."),
        execute(ValidationEngineerB,
                "Validate user interactions, UI elements, data handling, and compliance with design_spec.md in app.py and templates/*.html. Produce validation_b.md.")
    )

    # Read validation reports content to inject for RepairMerger
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # RepairMerger merges fixes based on validation reports and original merged artifacts
    await execute(RepairMerger,
                  f"Apply corrections to app.py and templates/*.html based on validation reports.\n\n"
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
