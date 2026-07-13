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
# 20260713_210029_431935/main_20260713_210029_431935.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent detailed design specifications for the OnlineAuction web application and merge them into design_spec.md including page layouts, elements, routes, data handling, and user navigation.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create comprehensive design specification documents describing the nine web pages, element IDs, user interactions, Flask routes, data formats, and navigation flows without referencing each other's work; \"\n        \"DesignMerger then reviews both designs with respect to the provided user task and merges them into one consistent design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Design Analyst with expertise in web application UI/UX and backend design for Python Flask frameworks.\n\nYour goal is to develop an exhaustive design specification for the OnlineAuction application that enables implementation teams to build all functional pages independently with precise UI element IDs, page titles, container div structures, user interaction flows, data file structures, and Flask route definitions starting from the Dashboard page.\n\nTask Details:\n- Read the full user_task_description from context to understand all functional requirements.\n- Create design_candidate_a.md specifying each of the nine pages with complete container divs, element IDs (static and dynamic), buttons, and interaction details.\n- Define data file formats, field structures, and how each data file interacts with pages.\n- Specify URL routing and expected user navigation paths explicitly, starting from the Dashboard.\n- Do not access or reference any other agent outputs.\n\n**Design Specification Requirements:**\n\n1. Page Layouts:\n   - For each page, list container div IDs and relevant sub-elements\n   - Include page titles as they appear in view and HTML head\n   - Detail all buttons and inputs with exact IDs\n\n2. User Interactions and Navigation:\n   - Describe navigation buttons and expected route flows among pages\n   - Define button-to-route mappings in Flask routing syntax\n\n3. Data Handling:\n   - For each page, identify required data files and fields accessed or modified\n   - Define data formats precisely with field order and delimiter (pipe |)\n   - Specify any data constraints or relationships used in page logic\n\n4. Flask Routes:\n   - Provide route paths and corresponding expected HTTP methods\n   - Define route parameters if applicable (e.g., auction_id for details pages)\n\nCRITICAL SUCCESS CRITERIA:\n- Use only write_text_file tool to output design_candidate_a.md.\n- Ensure specification is detailed enough to support full independent implementation.\n- Adhere strictly to user_task_description and do not reference other agent outputs.\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Design Specialist with extensive experience in creating detailed UI and backend specifications for Python-based auction platforms.\n\nYour goal is to construct a comprehensive alternative design specification document named design_candidate_b.md for the OnlineAuction app that details all UI element IDs, page flows, navigation buttons, data storage handling, web routes, and interactions starting from the Dashboard page.\n\nTask Details:\n- Analyze the full user_task_description to capture all required features and data structures.\n- Define each page’s layout including container divs, unique element IDs (including dynamic IDs), input fields, and buttons.\n- Specify precise navigation flows between pages and map UI elements to Flask routes.\n- Include detailed descriptions of data file formats, fields, and usage by each component.\n- Provide route structures, HTTP methods, and parameters clearly.\n- Do not consult or incorporate information from design_candidate_a.md or other agent outputs.\n\n**Specification Focus:**\n\n1. UI Element Details:\n   - Exact element IDs with descriptions for each page\n   - Dynamic ID patterns for repeatable elements (e.g., buttons in lists)\n\n2. Navigation and Flows:\n   - Define routes and navigation via buttons/links as Flask URLs\n   - Include page transitions and starting point at Dashboard\n\n3. Data Storage and Access:\n   - Detail data files with field layout and delimiter\n   - Explain data read/write interactions per page\n\n4. Web Routes:\n   - List route URLs with HTTP methods and parameters\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool exclusively to produce design_candidate_b.md.\n- Specification must fully cover implementation needs and match user_task precisely.\n- Avoid referencing any other design documents or agent outputs.\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Integration Specialist skilled in consolidating multiple design documents into a unified and consistent specification for Python Flask auction web applications.\n\nYour goal is to review design_candidate_a.md and design_candidate_b.md thoroughly to assess completeness, consistency, and adherence to the user task, and then merge both into a single coherent and conflict-free design_spec.md that describes the OnlineAuction application’s pages, UI element IDs, route structures, and data file references, ready for implementation.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md fully.\n- Identify overlaps and discrepancies in page elements, routes, data file specifications, and navigation flows.\n- Resolve conflicts in naming conventions, element IDs, and route definitions ensuring consistency.\n- Create a merged design_spec.md document that includes detailed page layouts, UI elements, navigation mappings, data storage formats, and web routing suitable for developers.\n- Ensure merged design is fully aligned with all requirements expressed in user_task_description.\n- Output only final merged specification; do not include secondary notes or drafts.\n\n**Merge Guidelines:**\n\n1. Completeness:\n   - Cover all nine pages with precise container divs, element IDs, buttons, and input fields.\n   - Incorporate all necessary route definitions and parameters.\n\n2. Consistency:\n   - Uniform naming conventions for IDs and routes across all pages.\n   - Unified format for data file schemas with exact field order and delimiter usage.\n\n3. Clarity:\n   - Clear mapping of UI elements to Flask routes and expected HTTP methods.\n   - Explicit navigation paths, starting from the Dashboard page.\n\nCRITICAL SUCCESS CRITERIA:\n- Use write_text_file tool exclusively to output design_spec.md.\n- Final specification must serve as a single source of truth for implementation teams.\n- Avoid contradictions or ambiguous instructions in the merged document.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_a.md fully specifies page elements, routes, data files, and interfaces as per user requirements and independently supports all functional requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Confirm design_candidate_b.md thoroughly covers page designs, data structure, navigation paths, and element IDs without omissions or contradictions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Ensure design_spec.md contains a clear, consistent, and detailed implementation blueprint including routes, templates, data mappings suitable for coding.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two separate full Python Flask web application implementations with templates based on design_spec.md and merge into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently write complete Python Flask app implementations and corresponding templates directories enforcing all routes, page titles, element IDs, and data file handling as per design_spec.md; ImplementationMerger then integrates both implementations, resolves conflicts, and produces the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building full web applications with local text file data management.\n\nYour goal is to independently produce a complete Python Flask application implementation with all required routes, view logic, and data handling, plus HTML templates with exact element IDs and navigation, starting from the Dashboard page.\n\nTask Details:\n- Read user_task_description and design_spec.md for requirements and detailed specifications.\n- Build app_candidate_a.py implementing ALL Flask routes with proper context variables and data file I/O as defined.\n- Create complete templates_candidate_a/*.html with all pages, exact element IDs, page titles, and navigation per design_spec.md.\n- Do NOT refer to or consult ImplementationEngineerB's work or artifacts.\n\nImplementation Requirements:\n1. **Flask Application Structure**:\n   - Set up Flask app with standard imports and configurations.\n   - Implement all routes specified in design_spec.md with precise function names and HTTP methods.\n   - Load/store data from local data/*.txt files exactly per design_spec.md format and field order.\n   - Start app on the Dashboard page (root route '/').\n   - Use render_template for HTML output with correct context variables.\n\n2. **Template Implementation**:\n   - Implement all specified templates in templates_candidate_a/ using exact IDs for elements including dynamic IDs.\n   - Match page titles exactly both in <title> and <h1> tags.\n   - Implement navigation buttons/links with correct url_for(function_name).\n   - Use Jinja2 templating syntax for dynamic contents, loops, and conditionals.\n\n3. **Data File Handling**:\n   - Parse all local text files using pipe-delimited format with no header lines.\n   - Strict adherence to field order and types defined in design_spec.md.\n   - Gracefully handle file I/O errors and missing data cases.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/.\n- Follow design_spec.md exactly for all routes, element IDs, page titles, and data file handling.\n- Do NOT rely on any information or code from ImplementationEngineerB.\n- Provide complete, runnable Flask app with all specified features.\n- Output: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building complete web applications with local text file data management.\n\nYour goal is to independently develop a full Python Flask application implementation with all required routes, data handling, and corresponding HTML templates with correct element IDs and navigation, starting at the Dashboard page.\n\nTask Details:\n- Analyze user_task_description and design_spec.md to gather all requirements and detailed specifications.\n- Implement app_candidate_b.py covering ALL routes and associated logic with precise context variables and file I/O as per design_spec.md.\n- Develop templates_candidate_b/*.html with all pages, ensuring exact element IDs, page titles, and navigation as specified.\n- Operate in complete isolation from ImplementationEngineerA; do not access or consider their artifacts or code.\n\nImplementation Requirements:\n1. **Flask App Setup**:\n   - Initialize Flask app using recommended best practices.\n   - Implement all routes with correct URLs, function names, and HTTP methods from design_spec.md.\n   - Use render_template with accurate context variables for each route.\n   - Start the application at the root '/' dashboard route.\n\n2. **Template Development**:\n   - Create HTML templates in templates_candidate_b/ directory.\n   - Precisely implement all required elements with their unique IDs and dynamic ID patterns.\n   - Ensure page titles match exactly design_spec.md for both <title> and <h1>.\n   - Use Jinja2 templating language features for dynamic data rendering.\n   - Establish correct navigation using url_for() calls matching route function names.\n\n3. **Data Handling**:\n   - Read and write local text files from data/ directory with exact formats and field orders.\n   - Use pipe ‘|’ delimiter and no headers.\n   - Implement error handling for missing or corrupt files gracefully.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and all templates under templates_candidate_b/.\n- Strictly follow design_spec.md regarding all application features, routes, data handling, element IDs, and page titles.\n- Maintain complete independence from ImplementationEngineerA's artifacts or implementation.\n- Deliver a fully functional Flask app with all specified features.\n- Output: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specialized in merging parallel Flask web app implementations and template directories.\n\nYour goal is to consolidate two independent Flask app implementations and their respective HTML template sets into a unified, conflict-free final application, ensuring complete preservation of all features and adherence to design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md for authoritative specifications.\n- Ingest app_candidate_a.py and templates_candidate_a/*.html from ImplementationEngineerA.\n- Ingest app_candidate_b.py and templates_candidate_b/*.html from ImplementationEngineerB.\n- Merge both implementations into a single app.py implementing ALL routes exactly as per design_spec.md:\n  - Resolve any implementation conflicts carefully preserving route names, functionality, and data file handling.\n- Merge both template sets into templates/*.html preserving all element IDs, page titles, navigation flows, and dynamic elements.\n- Ensure resulting application is fully coherent, functional, and strictly conforms to design_spec.md specifications.\n\nIntegration Requirements:\n1. **Code Merging**:\n   - Combine Python codebases, removing duplications and conflicts, unifying data loading and route handlers.\n   - Validate that final app.py supports all functionalities from both candidates without omissions.\n   - Ensure all Flask routes use consistent naming and expected HTTP methods.\n\n2. **Template Consolidation**:\n   - Integrate templates from both candidates, resolving any overlapping or conflicting template files.\n   - Maintain exact element IDs including dynamic patterns.\n   - Preserve all specified page titles and navigational elements matching design_spec.md.\n\n3. **Data Handling Consistency**:\n   - Confirm final data file access matches field order and formats exactly from design_spec.md.\n   - Harmonize any differences in file parsing or writing logic across candidates.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save unified app.py and all templates under templates/ directory.\n- Preserve all features, element IDs, routes, page titles exactly as specified in design_spec.md.\n- Produce a fully integrated, deployable Flask application ready for validation and testing.\n- Output: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Review app_candidate_a.py and templates_candidate_a/*.html to confirm fidelity to design_spec.md, complete routing, page elements, and correct data handling.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Assess app_candidate_b.py and templates_candidate_b/*.html against design_spec.md for completeness and adherence to all required features.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Confirm merged app.py and templates/*.html create a coherent Flask application conforming exactly to the design spec and ready for testing.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Independently validate the Flask app.py and templates/*.html implementations and merge findings to produce final tested and corrected application files.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently run validation checks on app.py and templates/*.html for syntax, route correctness, element ID presence, data operations, and navigation consistency; \"\n        \"RepairMerger then merges their validation reports and applies necessary corrections to produce the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask applications and HTML templating.\n\nYour goal is to perform thorough static and functional validation of the Flask backend and frontend templates to identify issues and suggest improvements.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and templates/*.html from CONTEXT\n- Produce validation_a.md detailing syntax errors, route correctness, element ID existence, and basic functional tests\n- Focus on static code analysis, presence of required routes, and essential UI elements as per design_spec.md\n\nValidation Procedures:\n1. **Static Python Code Checks**:\n   - Use validate_python_file tool to check syntax and runtime errors in app.py\n   - Confirm presence of all Flask routes specified in design_spec.md\n   - Verify function names and HTTP methods for completeness and accuracy\n\n2. **HTML Template Verification**:\n   - Check existence of all required element IDs in templates/*.html as per design_spec.md\n   - Inspect structural correctness of HTML files (no missing tags for critical elements)\n   - Validate that navigation buttons link properly to respective routes\n\n3. **Basic Functional Testing**:\n   - Execute critical Python code snippets for route responses and data loading\n   - Verify that key UI elements correspond to backend data points\n   - Identify inconsistencies or missing elements affecting core functionality\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools for analysis\n- Use write_text_file to output detailed validation_a.md\n- Provide actionable, precise, and reproducible issue descriptions\n- Focus strictly on app.py and templates/*.html correctness per design_spec.md\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in UI and data integration testing for Python Flask web applications.\n\nYour goal is to independently validate data management, UI element enactment, navigation correctness, and compliance with user requirements in frontend and backend implementations.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and templates/*.html from CONTEXT\n- Produce validation_b.md with a comprehensive list of issues and verification results\n- Focus especially on data reading/writing accuracy, UI behavior, and workflow navigation correctness\n\nValidation Procedures:\n1. **Data Operations Validation**:\n   - Verify data loading and saving in app.py follow design_spec.md schemas exactly\n   - Check that displayed data in templates matches backend data sources accurately\n   - Confirm no data inconsistency or mismatches affecting functionality\n\n2. **UI Elements Testing**:\n   - Verify presence and correct functioning of all UI elements described in design_spec.md\n   - Check interactive elements such as buttons and forms operate as intended\n   - Validate filters, dropdowns, and input elements trigger backend logic properly\n\n3. **Navigation and Workflow Checks**:\n   - Confirm navigation buttons in templates direct users to correct routes\n   - Test navigation flow matches user task requirements and page transitions\n   - Identify any broken links or navigation mismatches\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code to verify backend functionality\n- Use write_text_file to save comprehensive validation_b.md report\n- Provide clear, detailed findings related to data integrity, UI functionality, and navigation flow\n- Work independently from ValidationEngineerA to ensure diverse validation perspectives\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specialized in code and UI repair merging for Python Flask applications and HTML templates.\n\nYour goal is to consolidate validation reports from ValidationEngineerA and ValidationEngineerB, apply all necessary fixes to app.py and templates, and produce final production-ready files.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md from CONTEXT\n- Integrate feedback and resolve all defects and issues reported in validation documents\n- Produce updated, fully functional app.py and templates that adhere strictly to design specifications\n\nRepair and Merge Procedures:\n1. **Issue Consolidation**:\n   - Review validation_a.md and validation_b.md for overlapping and unique issues\n   - Prioritize fixes that improve stability, correctness, and user experience\n\n2. **Code and Template Updates**:\n   - Correct syntax errors and remove code defects in app.py\n   - Add, remove, or adjust template elements to match required element IDs and navigation flows\n   - Fix any broken routes, button links, and form handling based on validation insights\n\n3. **Quality Assurance**:\n   - Ensure final app.py runs without syntax or runtime errors\n   - Verify templates render correctly with all required elements and proper navigation\n   - Maintain consistency with user_task_description and design_spec.md requirements\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and all templates/*.html files\n- Ensure all validation issues are comprehensively addressed and closed\n- Preserve original design intent and user requirements exactly\n- Deliver production-ready, error-free backend and frontend files\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Ensure validation_a.md provides actionable and accurate analysis of app.py and templates/*.html functionality and issues before repair.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Validate that validation_b.md thoroughly covers UI, data management, and navigation correctness for app.py and templates/*.html.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify the final app.py and templates/*.html fully resolve validation issues and preserve the original design_spec.md requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'OnlineAuction' Web Application

## 1. Objective
Develop a comprehensive web application named 'OnlineAuction' using Python, with data managed through local text files. The application enables users to browse auction items, place bids, track bid history, view winning items, and explore categories. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'OnlineAuction' application is Python.

## 3. Page Design

The 'OnlineAuction' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Auction Dashboard
- **Overview**: The main hub displaying featured auction items, trending auctions, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-auctions** - Type: Div - Display of featured auction items.
  - **ID: browse-auctions-button** - Type: Button - Button to navigate to auction catalog page.
  - **ID: view-bids-button** - Type: Button - Button to navigate to bid history page.
  - **ID: trending-auctions-button** - Type: Button - Button to navigate to trending auctions page.

### 2. Auction Catalog Page
- **Page Title**: Auction Catalog
- **Overview**: A page displaying all available auction items with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search auctions by item name, description, or item ID.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Electronics, Collectibles, Furniture, Art, Other).
  - **ID: auctions-grid** - Type: Div - Grid displaying auction cards with item image, title, current bid, and time remaining.
  - **ID: view-auction-button-{auction_id}** - Type: Button - Button to view auction details (each auction card has this).

### 3. Auction Details Page
- **Page Title**: Auction Details
- **Overview**: A page displaying detailed information about a specific auction item.
- **Elements**:
  - **ID: auction-details-page** - Type: Div - Container for the auction details page.
  - **ID: auction-title** - Type: H1 - Display auction item title.
  - **ID: auction-description** - Type: Div - Display item description.
  - **ID: current-bid** - Type: Div - Display current highest bid amount.
  - **ID: place-bid-button** - Type: Button - Button to place a new bid.
  - **ID: bid-history** - Type: Div - Section displaying bid history with bidder names and amounts.

### 4. Place Bid Page
- **Page Title**: Place Bid
- **Overview**: A page for users to enter bid information for an auction item.
- **Elements**:
  - **ID: place-bid-page** - Type: Div - Container for the place bid page.
  - **ID: bidder-name** - Type: Input - Field to input bidder name.
  - **ID: bid-amount** - Type: Input - Field to input bid amount.
  - **ID: auction-name** - Type: Div - Display the auction item name.
  - **ID: minimum-bid** - Type: Div - Display minimum acceptable bid amount.
  - **ID: submit-bid-button** - Type: Button - Button to submit the bid.

### 5. Bid History Page
- **Page Title**: Bid History
- **Overview**: A page displaying all bids placed by users with detailed information.
- **Elements**:
  - **ID: bid-history-page** - Type: Div - Container for the bid history page.
  - **ID: bids-table** - Type: Table - Table displaying bids with bid ID, auction name, bidder, amount, and timestamp.
  - **ID: filter-by-auction** - Type: Dropdown - Dropdown to filter bids by auction.
  - **ID: sort-by-amount** - Type: Button - Button to sort bids by amount.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Auction Categories Page
- **Page Title**: Auction Categories
- **Overview**: A page displaying all auction categories with brief descriptions.
- **Elements**:
  - **ID: categories-page** - Type: Div - Container for the categories page.
  - **ID: categories-list** - Type: Div - List of categories with descriptions and item counts.
  - **ID: category-card-{category_id}** - Type: Div - Card for each category with name and count.
  - **ID: view-category-button-{category_id}** - Type: Button - Button to view items in category (each category card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Winners Page
- **Page Title**: Winning Items
- **Overview**: A page displaying all auction items won by users with winner information.
- **Elements**:
  - **ID: winners-page** - Type: Div - Container for the winners page.
  - **ID: winners-list** - Type: Div - List of winning items with item name, winner, and winning bid amount.
  - **ID: winner-card-{auction_id}** - Type: Div - Card for each winning item.
  - **ID: filter-by-winner** - Type: Input - Input field to filter winners by name.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Trending Auctions Page
- **Page Title**: Trending Auctions
- **Overview**: A page displaying the most popular and active auction items ranked by bid activity.
- **Elements**:
  - **ID: trending-page** - Type: Div - Container for the trending auctions page.
  - **ID: trending-list** - Type: Div - Ranked list of trending auctions with rank, title, current bid, and bid count.
  - **ID: time-range-filter** - Type: Dropdown - Dropdown to filter by time range (Last 24 Hours, This Week, All Time).
  - **ID: view-auction-button-{auction_id}** - Type: Button - Button to view auction details (each trending item has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Auction Status Page
- **Page Title**: Auction Status
- **Overview**: A page displaying the status of all active, closed, and upcoming auctions.
- **Elements**:
  - **ID: status-page** - Type: Div - Container for the auction status page.
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Active, Closed, Upcoming).
  - **ID: status-table** - Type: Table - Table displaying auctions with name, status, time remaining, and current bid.
  - **ID: refresh-status-button** - Type: Button - Button to refresh auction statuses.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'OnlineAuction' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Auctions Data
- **File Name**: `auctions.txt`
- **Data Format**:
  ```
  auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
  ```
- **Example Data**:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description|item_count
  ```
- **Example Data**:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. Bids Data
- **File Name**: `bids.txt`
- **Data Format**:
  ```
  bid_id|auction_id|bidder_name|bid_amount|bid_timestamp
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. Winners Data
- **File Name**: `winners.txt`
- **Data Format**:
  ```
  winner_id|auction_id|item_name|winner_name|winning_bid|win_date
  ```
- **Example Data**:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. Bid History Data
- **File Name**: `bid_history.txt`
- **Data Format**:
  ```
  history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp
  ```
- **Example Data**:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. Items Data
- **File Name**: `items.txt`
- **Data Format**:
  ```
  item_id|auction_id|item_name|starting_price|category|condition|seller_name
  ```
- **Example Data**:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. Trending Data
- **File Name**: `trending.txt`
- **Data Format**:
  ```
  auction_id|item_name|bid_count|current_bid|trending_rank|time_period
  ```
- **Example Data**:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
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
            """You are a Software Design Analyst with expertise in web application UI/UX and backend design for Python Flask frameworks.

Your goal is to develop an exhaustive design specification for the OnlineAuction application that enables implementation teams to build all functional pages independently with precise UI element IDs, page titles, container div structures, user interaction flows, data file structures, and Flask route definitions starting from the Dashboard page.

Task Details:
- Read the full user_task_description from context to understand all functional requirements.
- Create design_candidate_a.md specifying each of the nine pages with complete container divs, element IDs (static and dynamic), buttons, and interaction details.
- Define data file formats, field structures, and how each data file interacts with pages.
- Specify URL routing and expected user navigation paths explicitly, starting from the Dashboard.
- Do not access or reference any other agent outputs.

**Design Specification Requirements:**

1. Page Layouts:
   - For each page, list container div IDs and relevant sub-elements
   - Include page titles as they appear in view and HTML head
   - Detail all buttons and inputs with exact IDs

2. User Interactions and Navigation:
   - Describe navigation buttons and expected route flows among pages
   - Define button-to-route mappings in Flask routing syntax

3. Data Handling:
   - For each page, identify required data files and fields accessed or modified
   - Define data formats precisely with field order and delimiter (pipe |)
   - Specify any data constraints or relationships used in page logic

4. Flask Routes:
   - Provide route paths and corresponding expected HTTP methods
   - Define route parameters if applicable (e.g., auction_id for details pages)

CRITICAL SUCCESS CRITERIA:
- Use only write_text_file tool to output design_candidate_a.md.
- Ensure specification is detailed enough to support full independent implementation.
- Adhere strictly to user_task_description and do not reference other agent outputs.

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Design Specialist with extensive experience in creating detailed UI and backend specifications for Python-based auction platforms.

Your goal is to construct a comprehensive alternative design specification document named design_candidate_b.md for the OnlineAuction app that details all UI element IDs, page flows, navigation buttons, data storage handling, web routes, and interactions starting from the Dashboard page.

Task Details:
- Analyze the full user_task_description to capture all required features and data structures.
- Define each page’s layout including container divs, unique element IDs (including dynamic IDs), input fields, and buttons.
- Specify precise navigation flows between pages and map UI elements to Flask routes.
- Include detailed descriptions of data file formats, fields, and usage by each component.
- Provide route structures, HTTP methods, and parameters clearly.
- Do not consult or incorporate information from design_candidate_a.md or other agent outputs.

**Specification Focus:**

1. UI Element Details:
   - Exact element IDs with descriptions for each page
   - Dynamic ID patterns for repeatable elements (e.g., buttons in lists)

2. Navigation and Flows:
   - Define routes and navigation via buttons/links as Flask URLs
   - Include page transitions and starting point at Dashboard

3. Data Storage and Access:
   - Detail data files with field layout and delimiter
   - Explain data read/write interactions per page

4. Web Routes:
   - List route URLs with HTTP methods and parameters

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to produce design_candidate_b.md.
- Specification must fully cover implementation needs and match user_task precisely.
- Avoid referencing any other design documents or agent outputs.

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Integration Specialist skilled in consolidating multiple design documents into a unified and consistent specification for Python Flask auction web applications.

Your goal is to review design_candidate_a.md and design_candidate_b.md thoroughly to assess completeness, consistency, and adherence to the user task, and then merge both into a single coherent and conflict-free design_spec.md that describes the OnlineAuction application’s pages, UI element IDs, route structures, and data file references, ready for implementation.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md fully.
- Identify overlaps and discrepancies in page elements, routes, data file specifications, and navigation flows.
- Resolve conflicts in naming conventions, element IDs, and route definitions ensuring consistency.
- Create a merged design_spec.md document that includes detailed page layouts, UI elements, navigation mappings, data storage formats, and web routing suitable for developers.
- Ensure merged design is fully aligned with all requirements expressed in user_task_description.
- Output only final merged specification; do not include secondary notes or drafts.

**Merge Guidelines:**

1. Completeness:
   - Cover all nine pages with precise container divs, element IDs, buttons, and input fields.
   - Incorporate all necessary route definitions and parameters.

2. Consistency:
   - Uniform naming conventions for IDs and routes across all pages.
   - Unified format for data file schemas with exact field order and delimiter usage.

3. Clarity:
   - Clear mapping of UI elements to Flask routes and expected HTTP methods.
   - Explicit navigation paths, starting from the Dashboard page.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output design_spec.md.
- Final specification must serve as a single source of truth for implementation teams.
- Avoid contradictions or ambiguous instructions in the merged document.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Python Flask Developer specializing in building full web applications with local text file data management.

Your goal is to independently produce a complete Python Flask application implementation with all required routes, view logic, and data handling, plus HTML templates with exact element IDs and navigation, starting from the Dashboard page.

Task Details:
- Read user_task_description and design_spec.md for requirements and detailed specifications.
- Build app_candidate_a.py implementing ALL Flask routes with proper context variables and data file I/O as defined.
- Create complete templates_candidate_a/*.html with all pages, exact element IDs, page titles, and navigation per design_spec.md.
- Do NOT refer to or consult ImplementationEngineerB's work or artifacts.

Implementation Requirements:
1. **Flask Application Structure**:
   - Set up Flask app with standard imports and configurations.
   - Implement all routes specified in design_spec.md with precise function names and HTTP methods.
   - Load/store data from local data/*.txt files exactly per design_spec.md format and field order.
   - Start app on the Dashboard page (root route '/').
   - Use render_template for HTML output with correct context variables.

2. **Template Implementation**:
   - Implement all specified templates in templates_candidate_a/ using exact IDs for elements including dynamic IDs.
   - Match page titles exactly both in <title> and <h1> tags.
   - Implement navigation buttons/links with correct url_for(function_name).
   - Use Jinja2 templating syntax for dynamic contents, loops, and conditionals.

3. **Data File Handling**:
   - Parse all local text files using pipe-delimited format with no header lines.
   - Strict adherence to field order and types defined in design_spec.md.
   - Gracefully handle file I/O errors and missing data cases.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/.
- Follow design_spec.md exactly for all routes, element IDs, page titles, and data file handling.
- Do NOT rely on any information or code from ImplementationEngineerB.
- Provide complete, runnable Flask app with all specified features.
- Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Python Flask Developer specializing in building complete web applications with local text file data management.

Your goal is to independently develop a full Python Flask application implementation with all required routes, data handling, and corresponding HTML templates with correct element IDs and navigation, starting at the Dashboard page.

Task Details:
- Analyze user_task_description and design_spec.md to gather all requirements and detailed specifications.
- Implement app_candidate_b.py covering ALL routes and associated logic with precise context variables and file I/O as per design_spec.md.
- Develop templates_candidate_b/*.html with all pages, ensuring exact element IDs, page titles, and navigation as specified.
- Operate in complete isolation from ImplementationEngineerA; do not access or consider their artifacts or code.

Implementation Requirements:
1. **Flask App Setup**:
   - Initialize Flask app using recommended best practices.
   - Implement all routes with correct URLs, function names, and HTTP methods from design_spec.md.
   - Use render_template with accurate context variables for each route.
   - Start the application at the root '/' dashboard route.

2. **Template Development**:
   - Create HTML templates in templates_candidate_b/ directory.
   - Precisely implement all required elements with their unique IDs and dynamic ID patterns.
   - Ensure page titles match exactly design_spec.md for both <title> and <h1>.
   - Use Jinja2 templating language features for dynamic data rendering.
   - Establish correct navigation using url_for() calls matching route function names.

3. **Data Handling**:
   - Read and write local text files from data/ directory with exact formats and field orders.
   - Use pipe ‘|’ delimiter and no headers.
   - Implement error handling for missing or corrupt files gracefully.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and all templates under templates_candidate_b/.
- Strictly follow design_spec.md regarding all application features, routes, data handling, element IDs, and page titles.
- Maintain complete independence from ImplementationEngineerA's artifacts or implementation.
- Deliver a fully functional Flask app with all specified features.
- Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specialized in merging parallel Flask web app implementations and template directories.

Your goal is to consolidate two independent Flask app implementations and their respective HTML template sets into a unified, conflict-free final application, ensuring complete preservation of all features and adherence to design_spec.md.

Task Details:
- Read user_task_description and design_spec.md for authoritative specifications.
- Ingest app_candidate_a.py and templates_candidate_a/*.html from ImplementationEngineerA.
- Ingest app_candidate_b.py and templates_candidate_b/*.html from ImplementationEngineerB.
- Merge both implementations into a single app.py implementing ALL routes exactly as per design_spec.md:
  - Resolve any implementation conflicts carefully preserving route names, functionality, and data file handling.
- Merge both template sets into templates/*.html preserving all element IDs, page titles, navigation flows, and dynamic elements.
- Ensure resulting application is fully coherent, functional, and strictly conforms to design_spec.md specifications.

Integration Requirements:
1. **Code Merging**:
   - Combine Python codebases, removing duplications and conflicts, unifying data loading and route handlers.
   - Validate that final app.py supports all functionalities from both candidates without omissions.
   - Ensure all Flask routes use consistent naming and expected HTTP methods.

2. **Template Consolidation**:
   - Integrate templates from both candidates, resolving any overlapping or conflicting template files.
   - Maintain exact element IDs including dynamic patterns.
   - Preserve all specified page titles and navigational elements matching design_spec.md.

3. **Data Handling Consistency**:
   - Confirm final data file access matches field order and formats exactly from design_spec.md.
   - Harmonize any differences in file parsing or writing logic across candidates.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save unified app.py and all templates under templates/ directory.
- Preserve all features, element IDs, routes, page titles exactly as specified in design_spec.md.
- Produce a fully integrated, deployable Flask application ready for validation and testing.
- Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask applications and HTML templating.

Your goal is to perform thorough static and functional validation of the Flask backend and frontend templates to identify issues and suggest improvements.

Task Details:
- Read user_task_description, design_spec.md, app.py, and templates/*.html from CONTEXT
- Produce validation_a.md detailing syntax errors, route correctness, element ID existence, and basic functional tests
- Focus on static code analysis, presence of required routes, and essential UI elements as per design_spec.md

Validation Procedures:
1. **Static Python Code Checks**:
   - Use validate_python_file tool to check syntax and runtime errors in app.py
   - Confirm presence of all Flask routes specified in design_spec.md
   - Verify function names and HTTP methods for completeness and accuracy

2. **HTML Template Verification**:
   - Check existence of all required element IDs in templates/*.html as per design_spec.md
   - Inspect structural correctness of HTML files (no missing tags for critical elements)
   - Validate that navigation buttons link properly to respective routes

3. **Basic Functional Testing**:
   - Execute critical Python code snippets for route responses and data loading
   - Verify that key UI elements correspond to backend data points
   - Identify inconsistencies or missing elements affecting core functionality

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for analysis
- Use write_text_file to output detailed validation_a.md
- Provide actionable, precise, and reproducible issue descriptions
- Focus strictly on app.py and templates/*.html correctness per design_spec.md

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in UI and data integration testing for Python Flask web applications.

Your goal is to independently validate data management, UI element enactment, navigation correctness, and compliance with user requirements in frontend and backend implementations.

Task Details:
- Read user_task_description, design_spec.md, app.py, and templates/*.html from CONTEXT
- Produce validation_b.md with a comprehensive list of issues and verification results
- Focus especially on data reading/writing accuracy, UI behavior, and workflow navigation correctness

Validation Procedures:
1. **Data Operations Validation**:
   - Verify data loading and saving in app.py follow design_spec.md schemas exactly
   - Check that displayed data in templates matches backend data sources accurately
   - Confirm no data inconsistency or mismatches affecting functionality

2. **UI Elements Testing**:
   - Verify presence and correct functioning of all UI elements described in design_spec.md
   - Check interactive elements such as buttons and forms operate as intended
   - Validate filters, dropdowns, and input elements trigger backend logic properly

3. **Navigation and Workflow Checks**:
   - Confirm navigation buttons in templates direct users to correct routes
   - Test navigation flow matches user task requirements and page transitions
   - Identify any broken links or navigation mismatches

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code to verify backend functionality
- Use write_text_file to save comprehensive validation_b.md report
- Provide clear, detailed findings related to data integrity, UI functionality, and navigation flow
- Work independently from ValidationEngineerA to ensure diverse validation perspectives

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Engineer specialized in code and UI repair merging for Python Flask applications and HTML templates.

Your goal is to consolidate validation reports from ValidationEngineerA and ValidationEngineerB, apply all necessary fixes to app.py and templates, and produce final production-ready files.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md from CONTEXT
- Integrate feedback and resolve all defects and issues reported in validation documents
- Produce updated, fully functional app.py and templates that adhere strictly to design specifications

Repair and Merge Procedures:
1. **Issue Consolidation**:
   - Review validation_a.md and validation_b.md for overlapping and unique issues
   - Prioritize fixes that improve stability, correctness, and user experience

2. **Code and Template Updates**:
   - Correct syntax errors and remove code defects in app.py
   - Add, remove, or adjust template elements to match required element IDs and navigation flows
   - Fix any broken routes, button links, and form handling based on validation insights

3. **Quality Assurance**:
   - Ensure final app.py runs without syntax or runtime errors
   - Verify templates render correctly with all required elements and proper navigation
   - Maintain consistency with user_task_description and design_spec.md requirements

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all templates/*.html files
- Ensure all validation issues are comprehensively addressed and closed
- Preserve original design intent and user requirements exactly
- Deliver production-ready, error-free backend and frontend files

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
        ("DesignMerger", """Verify design_candidate_a.md fully specifies page elements, routes, data files, and interfaces as per user requirements and independently supports all functional requirements.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Confirm design_candidate_b.md thoroughly covers page designs, data structure, navigation paths, and element IDs without omissions or contradictions.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Ensure design_spec.md contains a clear, consistent, and detailed implementation blueprint including routes, templates, data mappings suitable for coding.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Review app_candidate_a.py and templates_candidate_a/*.html to confirm fidelity to design_spec.md, complete routing, page elements, and correct data handling.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Assess app_candidate_b.py and templates_candidate_b/*.html against design_spec.md for completeness and adherence to all required features.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Confirm merged app.py and templates/*.html create a coherent Flask application conforming exactly to the design spec and ready for testing.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Ensure validation_a.md provides actionable and accurate analysis of app.py and templates/*.html functionality and issues before repair.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Validate that validation_b.md thoroughly covers UI, data management, and navigation correctness for app.py and templates/*.html.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Verify the final app.py and templates/*.html fully resolve validation issues and preserve the original design_spec.md requirements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=60
    )

    # Parallel execution: DesignAnalystA and DesignAnalystB create independent design docs
    await asyncio.gather(
        execute(DesignAnalystA, "Create exhaustive design_candidate_a.md specifying all nine pages with layouts, element IDs, data handling, and routes as per user_task_description"),
        execute(DesignAnalystB, "Create complete design_candidate_b.md detailing page layouts, UI element IDs, navigation flows, data formats, and route structures as per user_task_description")
    )

    # Read outputs for DesignMerger
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

    # Merge both design specs into single coherent design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_candidate_a}\n\n=== DesignAnalystB ===\n{design_candidate_b}")
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
        timeout_threshold=320,
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
        timeout_threshold=320,
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
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=30
    )

    # Run ImplementationEngineerA and ImplementationEngineerB in parallel
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Build complete Flask app as app_candidate_a.py with all routes, data handling, and templates in templates_candidate_a/*.html per design_spec.md."),
        execute(ImplementationEngineerB,
                "Build complete Flask app as app_candidate_b.py with all routes, data handling, and templates in templates_candidate_b/*.html per design_spec.md.")
    )

    # Read outputs from both implementation engineers for merging
    app_a_code, app_b_code = "", ""
    templates_a_content, templates_b_content = "", ""
    try:
        app_a_code = open("app_candidate_a.py").read()
    except:
        pass
    try:
        app_b_code = open("app_candidate_b.py").read()
    except:
        pass
    try: 
        # For templates, reading multiple files might be complex; 
        # here we can read all files under each templates_candidate_X directory if available.
        # Since direct reading of multiple files is not possible here, pass empty or partial content.
        # Placeholder for content reading:
        templates_a_content = ""  # Real code would aggregate all app_candidate_a template files content
    except:
        pass
    try:
        templates_b_content = ""  # Similarly for ImplementationEngineerB templates
    except:
        pass

    # Execute merging with all collected code and templates content
    await execute(ImplementationMerger,
                  f"Merge the following code and templates into final app.py and templates/*.html strictly following design_spec.md.\n\n"
                  f"=== app_candidate_a.py ===\n{app_a_code}\n\n"
                  f"=== templates_candidate_a contents ===\n{templates_a_content}\n\n"
                  f"=== app_candidate_b.py ===\n{app_b_code}\n\n"
                  f"=== templates_candidate_b contents ===\n{templates_b_content}")
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

    # Read file contents for injection
    user_task_description = ""
    design_spec = ""
    app_py = ""
    templates_all = ""

    try:
        entries = CONTEXT.get("user_task_description", [])
        user_task_description = entries[-1]["content"] if entries else ""
    except:
        user_task_description = ""

    try:
        design_entries = CONTEXT.get("design_spec.md", [])
        design_spec = design_entries[-1]["content"] if design_entries else ""
    except:
        design_spec = ""

    try:
        app_entries = CONTEXT.get("app.py", [])
        app_py = app_entries[-1]["content"] if app_entries else ""
    except:
        app_py = ""

    # For templates/*.html, we aggregate all templates content separated by file names if possible
    templates_entries = CONTEXT.get("templates/*.html", [])
    # Assume each entry's content is single template file content, concatenate
    templates_all = "\n\n".join(entry.get("content", "") for entry in templates_entries)

    # Parallel validation by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(
            ValidationEngineerA,
            f"User task description:\n{user_task_description}\n\n"
            f"Design spec:\n{design_spec}\n\n"
            f"App.py:\n{app_py}\n\n"
            f"Templates:\n{templates_all}\n\n"
            "Perform static and functional validation, "
            "output detailed validation_a.md with syntax errors, route checks, element ID verification, and basic functional tests."
        ),
        execute(
            ValidationEngineerB,
            f"User task description:\n{user_task_description}\n\n"
            f"Design spec:\n{design_spec}\n\n"
            f"App.py:\n{app_py}\n\n"
            f"Templates:\n{templates_all}\n\n"
            "Perform data operation validation, UI element tests, navigation flow verification, "
            "output comprehensive validation_b.md report detailing data integrity, UI functionality, and navigation correctness."
        )
    )

    # Read validation results for RepairMerger injection
    validation_a = ""
    validation_b = ""
    try:
        validation_a = open("validation_a.md").read()
    except:
        validation_a = ""
    try:
        validation_b = open("validation_b.md").read()
    except:
        validation_b = ""

    # RepairMerger merges validation results and produces final corrected app.py and templates/*.html
    await execute(
        RepairMerger,
        f"User task description:\n{user_task_description}\n\n"
        f"Design spec:\n{design_spec}\n\n"
        f"App.py:\n{app_py}\n\n"
        f"Templates:\n{templates_all}\n\n"
        f"Validation A report:\n{validation_a}\n\n"
        f"Validation B report:\n{validation_b}\n\n"
        "Consolidate issues, apply all necessary fixes, and output final production-ready app.py and templates/*.html files."
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
