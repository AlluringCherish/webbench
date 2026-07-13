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
# 20260713_210029_387941/main_20260713_210029_387941.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent complete design specifications covering all nine NewsPortal pages with exact Flask route names, page titles, element IDs, navigation buttons, and data-handling details; then merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently write comprehensive NewsPortal design specs in Markdown format, specifying Flask routes, page titles, element IDs, navigation button IDs, and local text file data usage. They do not access each other's outputs. \"\n        \"DesignMerger reads both independent design specs and merges them into a single coherent design_spec.md ensuring coverage of all required pages, exact UI details, and data schema usage.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in designing web application specifications using Flask and local text file data storage.\n\nYour goal is to derive a complete design specification for the NewsPortal web application from the user task, producing a design markdown document suitable for full backend/frontend implementation.\n\nTask Details:\n- Read the user_task_description artifact thoroughly to understand all NewsPortal functional requirements and page designs.\n- Produce a comprehensive markdown specification saved as design_candidate_a.md.\n- Specify precise Flask route names and HTTP methods for each of the nine pages.\n- Include exact page titles as required.\n- List all UI element IDs for each page's container and interactive elements as detailed.\n- Specify button element IDs that serve for page navigation with their corresponding route functions.\n- Detail the local text files under the 'data/' directory to be accessed per page, including their exact filenames, field structures, and usage.\n- Focus on completeness and consistency; do not reference or read design_candidate_b.md or any external specifications.\n\n**Flask Routes Specification**\n- Define route URLs and corresponding function names with HTTP verbs (GET/POST).\n- Map each route to its template HTML filename.\n\n**Page UI Elements**\n- For each page, define the container div ID and all element IDs.\n- Specify navigation buttons with their exact IDs and corresponding route functions.\n\n**Data File Usage**\n- Outline how each data file is parsed (filenames, pipe-delimited fields, no headers).\n- Map data files to page usage contexts for rendering content or handling actions.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md\n- Maintain exact element ID naming as in user requirements\n- Include full route and template details to enable independent development\n- Do not merge or compare with other candidate specifications\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in comprehensive web app design specifications focusing on Flask route structures and local text file data integration.\n\nYour goal is to create an independent, alternative, and complete design specification for the NewsPortal web app, ensuring exact UI element IDs, route naming conventions, template structure, and data file handling. Save the design as design_candidate_b.md.\n\nTask Details:\n- Analyze the user_task_description input to capture all NewsPortal pages, UI components, navigation buttons, and data storage formats.\n- Define explicit Flask route paths and HTTP methods for all pages without referencing design_candidate_a.md.\n- Enumerate all container and element IDs per page precisely as described.\n- Detail navigation buttons with target routes using consistent function names.\n- Describe the local 'data/' text files: filenames, pipe-separated field sequences, and their usage by the application.\n- Focus on clarity and precision enabling implementation teams to build the app independently.\n\n**Design Specification Requirements**\n- Flask routes and template filenames must be explicitly aligned with UI navigation.\n- Page titles must match exactly those provided.\n- Include detailed data file schema usage instructions for backend data access.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_candidate_b.md\n- Ensure exact matching of IDs and route names with user requirements\n- Provide comprehensive data file usage to prevent implementation ambiguity\n- Do not access or consider design_candidate_a.md or other agents' outputs\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in merging parallel design specifications into coherent unified documents.\n\nYour goal is to compare two independent design specifications (design_candidate_a.md and design_candidate_b.md) for the NewsPortal web application against the user requirements, identify and resolve conflicts or omissions, and produce a single merged and implementation-ready design_spec.md.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md fully.\n- Check coverage of all nine NewsPortal pages including Flask route names, HTTP methods, page titles, and element IDs.\n- Resolve discrepancies in UI element IDs, navigation button IDs, and route function names to ensure consistency.\n- Produce explicit instructions for text file data handling including filenames, pipe-delimited field order, and usage mapping.\n- Combine specifications into a clear, unambiguous markdown design_spec.md suitable for direct implementation by frontend and backend teams.\n\n**Merging Guidelines**\n- All routes must be well-defined with HTTP methods and template file names.\n- Page titles must match user requirements exactly.\n- Element IDs must be exact and consistent across pages.\n- Navigation button IDs matched with route functions precisely.\n- Data file schemas unified with field orders and example usages included.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save merged specification as design_spec.md\n- Ensure no conflicts remain in route names, UI element IDs, or data schema definitions\n- Maintain completeness and accuracy to cover all implementation needs\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for completeness in specifying Flask route names, page titles, element IDs, navigation button functions, and usage of local text files for data storage.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for completeness and correctness in all UI design details and data handling before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify that design_spec.md is a coherent, complete, and implementation-ready specification covering all required pages, routes, UI elements, and data storage formats.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete NewsPortal Flask application bundles implementing all pages, routes, UI elements, and data handling as per design_spec.md; write app_candidate_{a,b}.py and templates_candidate_{a,b}/*.html; then merge into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement the NewsPortal Flask web app following design_spec.md specifications, creating app_candidate_a.py with templates_candidate_a and app_candidate_b.py with templates_candidate_b respectively. Each uses isolated template folders and does not access each other's outputs. \"\n        \"ImplementationMerger compares both implementations, resolving conflicts and consolidating into app.py and templates/*.html enforcing exact requested routes, page titles, element IDs, template filenames, visible success/error messages, flexible parsing of pipe-delimited local text data files under 'data/', and stable actionable IDs.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications focusing on isolated template folder implementations.\n\nYour goal is to produce a fully functional NewsPortal Flask application bundle consisting of app_candidate_a.py and the complete set of templates_candidate_a/*.html files.\n\nTask Details:\n- Read user_task_description and design_spec.md for complete app requirements and specifications\n- Implement all nine NewsPortal pages with exact adherence to requested routes, page titles, element IDs, and navigation button mappings\n- Read and write local pipe-delimited text files under 'data/' folder as per design_spec.md\n- Use isolated template folder templates_candidate_a without accessing outputs from other implementation teams\n- Produce output artifacts: app_candidate_a.py and templates_candidate_a/*.html\n\nImplementation Requirements:\n1. **Flask App Structure**:\n   - Use app_candidate_a.py as the main Flask app script\n   - Configure Flask to load templates from templates_candidate_a directory\n   - Implement all routes exactly as specified, starting from root redirecting to dashboard\n2. **Data Handling**:\n   - Load and parse text files with pipe-delimited format from 'data/' folder\n   - Flexible parsing: strip whitespace, handle missing optional fields gracefully\n   - Support reading and writing bookmarks and comments as required\n3. **UI and Templates**:\n   - All templates must be located under templates_candidate_a/\n   - Templates must include all IDs exactly as specified (dashboard-page, featured-articles, etc.)\n   - Navigation buttons must link correctly to their endpoints using url_for()\n4. **Stability and Usability**:\n   - Include visible success or error messages for user actions (e.g., bookmarking, commenting)\n   - Use stable and actionable element IDs for dynamic content (view-article-button-{article_id}, remove-bookmark-button-{bookmark_id})\n5. **Coding Standards**:\n   - Follow Python best practices and Flask conventions\n   - Include `if __name__ == '__main__':` block for local development testing\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/\n- DO NOT read or depend on ImplementationEngineerB outputs\n- Follow design_spec.md strictly for routes, templates, element IDs, and data schemas\n- Ensure the application is fully runnable and testable independently\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications focusing on isolated template folder implementations.\n\nYour goal is to produce a fully functional NewsPortal Flask application bundle consisting of app_candidate_b.py and the full suite of templates_candidate_b/*.html files.\n\nTask Details:\n- Read user_task_description and design_spec.md carefully to understand all page, route, UI element, and data handling requirements\n- Implement all nine NewsPortal pages with precise routes, page titles, element IDs, and navigation controls\n- Manage local pipe-delimited text files in 'data/' folder for articles, bookmarks, comments, and trending data\n- Use isolated template folder templates_candidate_b/ with no dependency on other implementation teams\n- Deliver output artifacts: app_candidate_b.py and templates_candidate_b/*.html\n\nImplementation Requirements:\n1. **Flask Application**:\n   - Main app script named app_candidate_b.py\n   - Configure Flask to serve templates from templates_candidate_b directory\n   - Root route redirects to dashboard page per specifications\n2. **Data File Access**:\n   - Implement robust parsing of pipe-delimited text files for all data needs\n   - Support CRUD operations for bookmarks and comments as specified\n   - Handle cases with empty or missing data gracefully without errors\n3. **Templates and UI Elements**:\n   - Templates must exactly include all required IDs and element patterns as specified\n   - Navigation buttons and links must utilize Flask's url_for() with exact endpoint names\n   - Must ensure stable element IDs for dynamically generated content (e.g., view-article-button-{article_id})\n4. **Error Handling and Feedback**:\n   - Provide visible success/error messages for user interactive operations\n   - Maintain usability and accessibility standards in templates and route implementations\n5. **Code Quality**:\n   - Follow best practices in Python Flask coding, including modularity and readability\n   - Include local development run block with debug mode enabled\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool for saving app_candidate_b.py and associated templates under templates_candidate_b/\n- No referencing or reading of ImplementationEngineerA artifacts permitted\n- Strict compliance with design_spec.md for every page, route, element ID, and data file format\n- Application bundle should be independently runnable and fully testable\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Specialist skilled in merging parallel Flask web application implementations into a unified deliverable.\n\nYour goal is to merge two independent NewsPortal Flask app bundles (app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html) into a single cohesive app.py and templates/*.html set exactly conforming to design_spec.md requirements.\n\nTask Details:\n- Read user_task_description and design_spec.md to comprehend full NewsPortal application features and data schemas\n- Review both implementations: app_candidate_a.py with templates_candidate_a/*.html, and app_candidate_b.py with templates_candidate_b/*.html for completeness and adherence\n- Compare routes, page titles, element IDs, navigation buttons, and data file parsing logic across both implementations\n- Resolve conflicts ensuring final app.py and template files strictly follow the specifications, prioritizing correctness, stability, and user experience\n- Normalize template files into templates/ directory with consistent naming and exact IDs\n- Ensure the final app.py handles pipe-delimited local data files flexibly while maintaining robust functionality for all pages, including visible success/error messages and stable actionable element IDs\n- Produce unified outputs: app.py and templates/*.html\n\nMerging Process Requirements:\n1. **Route Consolidation**:\n   - All routes implemented in both candidates must appear with consistent handlers\n   - Harmonize any discrepancies in endpoint naming or route paths, following design_spec.md strictly\n2. **Template Merging**:\n   - Integrate templates from both candidates, resolving inconsistencies in element IDs, structure, and navigation\n   - Retain exact requested element IDs and page titles\n3. **Data Handling**:\n   - Merge data parsing and manipulation code to handle flexible and accurate pipe-delimited file operations\n4. **UI Consistency and Messages**:\n   - Ensure all success and error messages appear clearly with stable, actionable element IDs\n5. **Code Quality and Maintainability**:\n   - Produce clear, readable, and maintainable Flask app.py code\n   - Include comments where necessary to clarify merged logic\n6. **Final Deliverables**:\n   - app.py as the unified Flask app script\n   - Complete templates/*.html directory with all required templates\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save app.py and all templates under templates/\n- Ensure zero references to isolated candidate template folders or candidate app names remain\n- Application bundle must be immediately runnable and fully pass all requirements in design_spec.md\n- Maintain exact requested route paths, element IDs, page titles, and data parsing flexibilities\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Independently verify candidate A's app and templates follow design_spec.md routes, UI element IDs, and data handling accurately.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Independently verify candidate B's app and templates follow design_spec.md details accurately before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Confirm final app.py and templates/*.html form a coherent, runnable Flask application matching design_spec.md fully.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Conduct two independent validations of app.py with templates/*.html, generating detailed validation reports validating correctness of routes, UI elements, data interactions, and then merge repair suggestions into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate the final app.py and templates/*.html for exactness of Flask routes, UI element IDs, navigation correctness, local text file data operations, and visible success/error messages. Each produces a validation report (validation_a.md and validation_b.md). \"\n        \"RepairMerger reconciles both validation reports, applies all necessary repairs to app.py and templates/*.html, producing the final, verified application bundle.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specialized in validating Flask web applications developed with Python.\n\nYour goal is to independently validate correctness and functionality of the Flask backend (app.py) together with all corresponding HTML templates.\n\nTask Details:\n- Read user_task_description and design_spec.md to understand route definitions, UI element IDs, and data file schemas\n- Read app.py and templates/*.html to analyze actual implementation\n- Produce detailed validation report validation_a.md covering observed issues and recommended fixes\n\nValidation Requirements:\n1. **Backend Validation**:\n   - Verify app.py syntax and successful startup\n   - Confirm all Flask routes from design_spec.md exist and respond as expected\n   - Check proper reading/writing from/to local text data files as per schemas\n   - Confirm presence and correctness of success/error messages\n\n2. **Frontend Validation**:\n   - Confirm presence of all UI element IDs specified in design_spec.md and user requirements\n   - Verify navigation correctness between pages and functions\n   - Check dynamic element IDs follow patterns exactly (e.g., view-article-button-{article_id})\n\n3. **Reporting**:\n   - Document each issue clearly with location and description\n   - Specify required repair actions succinctly\n   - Do NOT read or incorporate ValidationEngineerB's outputs\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file tool on app.py for syntax/runtime checks\n- Use execute_python_code tool to run basic behavioral tests if feasible\n- Use write_text_file tool to produce validation_a.md\n- Report only validation_a.md output with no extraneous content\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specialized in comprehensive testing of Python Flask web applications.\n\nYour goal is to independently verify the accuracy of Flask routes, UI element IDs, data file handling, and user interface behaviors in the delivered app.py and templates.\n\nTask Details:\n- Analyze user_task_description and design_spec.md for expected routes, templates element IDs, and data interactions\n- Examine implementation files: app.py and templates/*.html for compliance\n- Produce validation_b.md outlining all findings and repair suggestions\n\nValidation Requirements:\n1. **Route and Backend Checks**:\n   - Confirm all required Flask routes exist with correct methods and handlers\n   - Ensure local text data files are read and written according to design specifications\n   - Test for visible error/success messages on relevant operations\n\n2. **UI Elements and Navigation**:\n   - Verify presence and correctness of all required static and dynamic element IDs\n   - Validate navigation links and buttons match design requirements exactly\n\n3. **Validation Reporting**:\n   - Provide clear, actionable feedback for fixes\n   - Exclude any references to ValidationEngineerA's outputs to maintain independence\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file to confirm code validity of app.py\n- Utilize execute_python_code tool for dynamic validation where appropriate\n- Use write_text_file to output full validation_b.md report\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in code and UI repair integration for Flask applications.\n\nYour goal is to merge independent validation reports from ValidationEngineerA and ValidationEngineerB, apply all valid repair suggestions to app.py and templates/*.html, preserving original application structure and design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md for original requirements and specifications\n- Review validation_a.md and validation_b.md thoroughly to identify all recommended fixes\n- Apply all relevant and valid repairs to app.py and templates/*.html source code\n- Ensure that all Flask routes, UI element IDs, data file handling, and navigation integrity are preserved and corrected as needed\n- Maintain consistent formatting and naming conventions from original implementation\n- Produce final repaired app.py and templates/*.html for deployment\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool for saving repaired source files\n- Do not alter unrelated code sections or add unrequested features\n- Final files must fully comply with design_spec.md and incorporate all repair actions\n- Do not include any validation status markers in output artifacts\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for clear, actionable validation of routes, UI elements, and data file usage before merging repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_b.md for thorough, reproducible validation results aligned with design_spec.md before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify final app.py and templates/*.html correctly incorporate repairs from validations, preserve design_spec.md contract, and are ready for deployment.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'NewsPortal' Web Application

## 1. Objective
Develop a comprehensive web application named 'NewsPortal' using Python, with data managed through local text files. The application enables users to browse news articles by category, read detailed articles, bookmark favorites, view comments, and track trending articles. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'NewsPortal' application is Python.

## 3. Page Design

The 'NewsPortal' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: News Portal
- **Overview**: The main hub displaying featured articles, trending news, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-articles** - Type: Div - Display of featured article recommendations.
  - **ID: browse-articles-button** - Type: Button - Button to navigate to article catalog page.
  - **ID: view-bookmarks-button** - Type: Button - Button to navigate to bookmarks page.
  - **ID: trending-articles-button** - Type: Button - Button to navigate to trending articles page.

### 2. Article Catalog Page
- **Page Title**: Article Catalog
- **Overview**: A page displaying all available articles with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search articles by title, author, or keywords.
  - **ID: category-filter** - Type: Dropdown - Dropdown to filter by category (Technology, Sports, Business, Health, Entertainment, etc.).
  - **ID: articles-grid** - Type: Div - Grid displaying article cards with thumbnail, title, author, and date.
  - **ID: view-article-button-{article_id}** - Type: Button - Button to view article details (each article card has this).

### 3. Article Details Page
- **Page Title**: Article Details
- **Overview**: A page displaying detailed information about a specific article.
- **Elements**:
  - **ID: article-details-page** - Type: Div - Container for the article details page.
  - **ID: article-title** - Type: H1 - Display article title.
  - **ID: article-author** - Type: Div - Display article author.
  - **ID: article-date** - Type: Div - Display article publication date.
  - **ID: bookmark-button** - Type: Button - Button to bookmark the article.
  - **ID: article-content** - Type: Div - Section displaying the full article content.

### 4. Bookmarks Page
- **Page Title**: My Bookmarks
- **Overview**: A page displaying all bookmarked articles with removal and reading options.
- **Elements**:
  - **ID: bookmarks-page** - Type: Div - Container for the bookmarks page.
  - **ID: bookmarks-list** - Type: Div - List displaying all bookmarked articles with title and date.
  - **ID: remove-bookmark-button-{bookmark_id}** - Type: Button - Button to remove bookmark (each bookmark has this).
  - **ID: read-bookmark-button-{bookmark_id}** - Type: Button - Button to read bookmarked article (each bookmark has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Comments Page
- **Page Title**: Article Comments
- **Overview**: A page displaying all comments on articles and allowing users to write new comments.
- **Elements**:
  - **ID: comments-page** - Type: Div - Container for the comments page.
  - **ID: comments-list** - Type: Div - List of all comments with article title, commenter name, and comment text.
  - **ID: write-comment-button** - Type: Button - Button to navigate to write comment page.
  - **ID: filter-by-article** - Type: Dropdown - Dropdown to filter comments by article.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Write Comment Page
- **Page Title**: Write a Comment
- **Overview**: A page for users to write comments on articles.
- **Elements**:
  - **ID: write-comment-page** - Type: Div - Container for the write comment page.
  - **ID: select-article** - Type: Dropdown - Dropdown to select article to comment on.
  - **ID: commenter-name** - Type: Input - Field to input commenter name.
  - **ID: comment-text** - Type: Textarea - Field to write comment text.
  - **ID: submit-comment-button** - Type: Button - Button to submit comment.

### 7. Trending Articles Page
- **Page Title**: Trending Articles
- **Overview**: A page displaying top trending articles ranked by views and engagement.
- **Elements**:
  - **ID: trending-page** - Type: Div - Container for the trending articles page.
  - **ID: trending-list** - Type: Div - Ranked list of trending articles with rank, title, category, and view count.
  - **ID: time-period-filter** - Type: Dropdown - Dropdown to filter by time period (Today, This Week, This Month).
  - **ID: view-article-button-{article_id}** - Type: Button - Button to view article details (each trending article has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Category Page
- **Page Title**: Category Articles
- **Overview**: A page displaying articles from a specific category.
- **Elements**:
  - **ID: category-page** - Type: Div - Container for the category page.
  - **ID: category-title** - Type: H1 - Display the category name.
  - **ID: category-articles** - Type: Div - List of articles in the selected category.
  - **ID: sort-by-date** - Type: Button - Button to sort articles by date.
  - **ID: sort-by-popularity** - Type: Button - Button to sort articles by popularity.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 9. Search Results Page
- **Page Title**: Search Results
- **Overview**: A page displaying search results based on user query.
- **Elements**:
  - **ID: search-results-page** - Type: Div - Container for the search results page.
  - **ID: search-query-display** - Type: Div - Display the search query performed.
  - **ID: results-list** - Type: Div - List of search results with article title and excerpt.
  - **ID: no-results-message** - Type: Div - Message displayed when no results found.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'NewsPortal' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Articles Data
- **File Name**: `articles.txt`
- **Data Format**:
  ```
  article_id|title|author|category|content|date|views
  ```
- **Example Data**:
  ```
  1|Breaking: New Technology Breakthrough|John Smith|Technology|Revolutionary advancement in quantum computing announced today|2025-01-20|5432
  2|Sports: Championship Victory|Sarah Johnson|Sports|Team wins the national championship with a thrilling final match|2025-01-19|3210
  3|Business: Market Trends Analysis|Michael Chen|Business|Expert analysis of current market conditions and forecasts|2025-01-18|2891
  ```

### 2. Categories Data
- **File Name**: `categories.txt`
- **Data Format**:
  ```
  category_id|category_name|description
  ```
- **Example Data**:
  ```
  1|Technology|Latest tech news and innovations
  2|Sports|Sports news and event coverage
  3|Business|Business and finance news
  ```

### 3. Bookmarks Data
- **File Name**: `bookmarks.txt`
- **Data Format**:
  ```
  bookmark_id|article_id|article_title|bookmarked_date
  ```
- **Example Data**:
  ```
  1|1|Breaking: New Technology Breakthrough|2025-01-20
  2|3|Business: Market Trends Analysis|2025-01-18
  ```

### 4. Comments Data
- **File Name**: `comments.txt`
- **Data Format**:
  ```
  comment_id|article_id|article_title|commenter_name|comment_text|comment_date
  ```
- **Example Data**:
  ```
  1|1|Breaking: New Technology Breakthrough|Alice Davis|Fascinating development!|2025-01-20
  2|2|Sports: Championship Victory|Robert Wilson|Amazing performance by the team!|2025-01-19
  ```

### 5. Trending Data
- **File Name**: `trending.txt`
- **Data Format**:
  ```
  article_id|article_title|category|view_count|period
  ```
- **Example Data**:
  ```
  1|Breaking: New Technology Breakthrough|Technology|5432|This Week
  2|Sports: Championship Victory|Sports|3210|This Week
  3|Business: Market Trends Analysis|Business|2891|This Month
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
            """You are a Software Architect specializing in designing web application specifications using Flask and local text file data storage.

Your goal is to derive a complete design specification for the NewsPortal web application from the user task, producing a design markdown document suitable for full backend/frontend implementation.

Task Details:
- Read the user_task_description artifact thoroughly to understand all NewsPortal functional requirements and page designs.
- Produce a comprehensive markdown specification saved as design_candidate_a.md.
- Specify precise Flask route names and HTTP methods for each of the nine pages.
- Include exact page titles as required.
- List all UI element IDs for each page's container and interactive elements as detailed.
- Specify button element IDs that serve for page navigation with their corresponding route functions.
- Detail the local text files under the 'data/' directory to be accessed per page, including their exact filenames, field structures, and usage.
- Focus on completeness and consistency; do not reference or read design_candidate_b.md or any external specifications.

**Flask Routes Specification**
- Define route URLs and corresponding function names with HTTP verbs (GET/POST).
- Map each route to its template HTML filename.

**Page UI Elements**
- For each page, define the container div ID and all element IDs.
- Specify navigation buttons with their exact IDs and corresponding route functions.

**Data File Usage**
- Outline how each data file is parsed (filenames, pipe-delimited fields, no headers).
- Map data files to page usage contexts for rendering content or handling actions.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md
- Maintain exact element ID naming as in user requirements
- Include full route and template details to enable independent development
- Do not merge or compare with other candidate specifications

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Architect specializing in comprehensive web app design specifications focusing on Flask route structures and local text file data integration.

Your goal is to create an independent, alternative, and complete design specification for the NewsPortal web app, ensuring exact UI element IDs, route naming conventions, template structure, and data file handling. Save the design as design_candidate_b.md.

Task Details:
- Analyze the user_task_description input to capture all NewsPortal pages, UI components, navigation buttons, and data storage formats.
- Define explicit Flask route paths and HTTP methods for all pages without referencing design_candidate_a.md.
- Enumerate all container and element IDs per page precisely as described.
- Detail navigation buttons with target routes using consistent function names.
- Describe the local 'data/' text files: filenames, pipe-separated field sequences, and their usage by the application.
- Focus on clarity and precision enabling implementation teams to build the app independently.

**Design Specification Requirements**
- Flask routes and template filenames must be explicitly aligned with UI navigation.
- Page titles must match exactly those provided.
- Include detailed data file schema usage instructions for backend data access.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_candidate_b.md
- Ensure exact matching of IDs and route names with user requirements
- Provide comprehensive data file usage to prevent implementation ambiguity
- Do not access or consider design_candidate_a.md or other agents' outputs

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Software Architect specializing in merging parallel design specifications into coherent unified documents.

Your goal is to compare two independent design specifications (design_candidate_a.md and design_candidate_b.md) for the NewsPortal web application against the user requirements, identify and resolve conflicts or omissions, and produce a single merged and implementation-ready design_spec.md.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md fully.
- Check coverage of all nine NewsPortal pages including Flask route names, HTTP methods, page titles, and element IDs.
- Resolve discrepancies in UI element IDs, navigation button IDs, and route function names to ensure consistency.
- Produce explicit instructions for text file data handling including filenames, pipe-delimited field order, and usage mapping.
- Combine specifications into a clear, unambiguous markdown design_spec.md suitable for direct implementation by frontend and backend teams.

**Merging Guidelines**
- All routes must be well-defined with HTTP methods and template file names.
- Page titles must match user requirements exactly.
- Element IDs must be exact and consistent across pages.
- Navigation button IDs matched with route functions precisely.
- Data file schemas unified with field orders and example usages included.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save merged specification as design_spec.md
- Ensure no conflicts remain in route names, UI element IDs, or data schema definitions
- Maintain completeness and accuracy to cover all implementation needs

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications focusing on isolated template folder implementations.

Your goal is to produce a fully functional NewsPortal Flask application bundle consisting of app_candidate_a.py and the complete set of templates_candidate_a/*.html files.

Task Details:
- Read user_task_description and design_spec.md for complete app requirements and specifications
- Implement all nine NewsPortal pages with exact adherence to requested routes, page titles, element IDs, and navigation button mappings
- Read and write local pipe-delimited text files under 'data/' folder as per design_spec.md
- Use isolated template folder templates_candidate_a without accessing outputs from other implementation teams
- Produce output artifacts: app_candidate_a.py and templates_candidate_a/*.html

Implementation Requirements:
1. **Flask App Structure**:
   - Use app_candidate_a.py as the main Flask app script
   - Configure Flask to load templates from templates_candidate_a directory
   - Implement all routes exactly as specified, starting from root redirecting to dashboard
2. **Data Handling**:
   - Load and parse text files with pipe-delimited format from 'data/' folder
   - Flexible parsing: strip whitespace, handle missing optional fields gracefully
   - Support reading and writing bookmarks and comments as required
3. **UI and Templates**:
   - All templates must be located under templates_candidate_a/
   - Templates must include all IDs exactly as specified (dashboard-page, featured-articles, etc.)
   - Navigation buttons must link correctly to their endpoints using url_for()
4. **Stability and Usability**:
   - Include visible success or error messages for user actions (e.g., bookmarking, commenting)
   - Use stable and actionable element IDs for dynamic content (view-article-button-{article_id}, remove-bookmark-button-{bookmark_id})
5. **Coding Standards**:
   - Follow Python best practices and Flask conventions
   - Include `if __name__ == '__main__':` block for local development testing

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_candidate_a.py and all template files under templates_candidate_a/
- DO NOT read or depend on ImplementationEngineerB outputs
- Follow design_spec.md strictly for routes, templates, element IDs, and data schemas
- Ensure the application is fully runnable and testable independently

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications focusing on isolated template folder implementations.

Your goal is to produce a fully functional NewsPortal Flask application bundle consisting of app_candidate_b.py and the full suite of templates_candidate_b/*.html files.

Task Details:
- Read user_task_description and design_spec.md carefully to understand all page, route, UI element, and data handling requirements
- Implement all nine NewsPortal pages with precise routes, page titles, element IDs, and navigation controls
- Manage local pipe-delimited text files in 'data/' folder for articles, bookmarks, comments, and trending data
- Use isolated template folder templates_candidate_b/ with no dependency on other implementation teams
- Deliver output artifacts: app_candidate_b.py and templates_candidate_b/*.html

Implementation Requirements:
1. **Flask Application**:
   - Main app script named app_candidate_b.py
   - Configure Flask to serve templates from templates_candidate_b directory
   - Root route redirects to dashboard page per specifications
2. **Data File Access**:
   - Implement robust parsing of pipe-delimited text files for all data needs
   - Support CRUD operations for bookmarks and comments as specified
   - Handle cases with empty or missing data gracefully without errors
3. **Templates and UI Elements**:
   - Templates must exactly include all required IDs and element patterns as specified
   - Navigation buttons and links must utilize Flask's url_for() with exact endpoint names
   - Must ensure stable element IDs for dynamically generated content (e.g., view-article-button-{article_id})
4. **Error Handling and Feedback**:
   - Provide visible success/error messages for user interactive operations
   - Maintain usability and accessibility standards in templates and route implementations
5. **Code Quality**:
   - Follow best practices in Python Flask coding, including modularity and readability
   - Include local development run block with debug mode enabled

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool for saving app_candidate_b.py and associated templates under templates_candidate_b/
- No referencing or reading of ImplementationEngineerA artifacts permitted
- Strict compliance with design_spec.md for every page, route, element ID, and data file format
- Application bundle should be independently runnable and fully testable

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Specialist skilled in merging parallel Flask web application implementations into a unified deliverable.

Your goal is to merge two independent NewsPortal Flask app bundles (app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html) into a single cohesive app.py and templates/*.html set exactly conforming to design_spec.md requirements.

Task Details:
- Read user_task_description and design_spec.md to comprehend full NewsPortal application features and data schemas
- Review both implementations: app_candidate_a.py with templates_candidate_a/*.html, and app_candidate_b.py with templates_candidate_b/*.html for completeness and adherence
- Compare routes, page titles, element IDs, navigation buttons, and data file parsing logic across both implementations
- Resolve conflicts ensuring final app.py and template files strictly follow the specifications, prioritizing correctness, stability, and user experience
- Normalize template files into templates/ directory with consistent naming and exact IDs
- Ensure the final app.py handles pipe-delimited local data files flexibly while maintaining robust functionality for all pages, including visible success/error messages and stable actionable element IDs
- Produce unified outputs: app.py and templates/*.html

Merging Process Requirements:
1. **Route Consolidation**:
   - All routes implemented in both candidates must appear with consistent handlers
   - Harmonize any discrepancies in endpoint naming or route paths, following design_spec.md strictly
2. **Template Merging**:
   - Integrate templates from both candidates, resolving inconsistencies in element IDs, structure, and navigation
   - Retain exact requested element IDs and page titles
3. **Data Handling**:
   - Merge data parsing and manipulation code to handle flexible and accurate pipe-delimited file operations
4. **UI Consistency and Messages**:
   - Ensure all success and error messages appear clearly with stable, actionable element IDs
5. **Code Quality and Maintainability**:
   - Produce clear, readable, and maintainable Flask app.py code
   - Include comments where necessary to clarify merged logic
6. **Final Deliverables**:
   - app.py as the unified Flask app script
   - Complete templates/*.html directory with all required templates

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app.py and all templates under templates/
- Ensure zero references to isolated candidate template folders or candidate app names remain
- Application bundle must be immediately runnable and fully pass all requirements in design_spec.md
- Maintain exact requested route paths, element IDs, page titles, and data parsing flexibilities

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specialized in validating Flask web applications developed with Python.

Your goal is to independently validate correctness and functionality of the Flask backend (app.py) together with all corresponding HTML templates.

Task Details:
- Read user_task_description and design_spec.md to understand route definitions, UI element IDs, and data file schemas
- Read app.py and templates/*.html to analyze actual implementation
- Produce detailed validation report validation_a.md covering observed issues and recommended fixes

Validation Requirements:
1. **Backend Validation**:
   - Verify app.py syntax and successful startup
   - Confirm all Flask routes from design_spec.md exist and respond as expected
   - Check proper reading/writing from/to local text data files as per schemas
   - Confirm presence and correctness of success/error messages

2. **Frontend Validation**:
   - Confirm presence of all UI element IDs specified in design_spec.md and user requirements
   - Verify navigation correctness between pages and functions
   - Check dynamic element IDs follow patterns exactly (e.g., view-article-button-{article_id})

3. **Reporting**:
   - Document each issue clearly with location and description
   - Specify required repair actions succinctly
   - Do NOT read or incorporate ValidationEngineerB's outputs

CRITICAL REQUIREMENTS:
- Use validate_python_file tool on app.py for syntax/runtime checks
- Use execute_python_code tool to run basic behavioral tests if feasible
- Use write_text_file tool to produce validation_a.md
- Report only validation_a.md output with no extraneous content

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specialized in comprehensive testing of Python Flask web applications.

Your goal is to independently verify the accuracy of Flask routes, UI element IDs, data file handling, and user interface behaviors in the delivered app.py and templates.

Task Details:
- Analyze user_task_description and design_spec.md for expected routes, templates element IDs, and data interactions
- Examine implementation files: app.py and templates/*.html for compliance
- Produce validation_b.md outlining all findings and repair suggestions

Validation Requirements:
1. **Route and Backend Checks**:
   - Confirm all required Flask routes exist with correct methods and handlers
   - Ensure local text data files are read and written according to design specifications
   - Test for visible error/success messages on relevant operations

2. **UI Elements and Navigation**:
   - Verify presence and correctness of all required static and dynamic element IDs
   - Validate navigation links and buttons match design requirements exactly

3. **Validation Reporting**:
   - Provide clear, actionable feedback for fixes
   - Exclude any references to ValidationEngineerA's outputs to maintain independence

CRITICAL REQUIREMENTS:
- Use validate_python_file to confirm code validity of app.py
- Utilize execute_python_code tool for dynamic validation where appropriate
- Use write_text_file to output full validation_b.md report

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in code and UI repair integration for Flask applications.

Your goal is to merge independent validation reports from ValidationEngineerA and ValidationEngineerB, apply all valid repair suggestions to app.py and templates/*.html, preserving original application structure and design specifications.

Task Details:
- Read user_task_description and design_spec.md for original requirements and specifications
- Review validation_a.md and validation_b.md thoroughly to identify all recommended fixes
- Apply all relevant and valid repairs to app.py and templates/*.html source code
- Ensure that all Flask routes, UI element IDs, data file handling, and navigation integrity are preserved and corrected as needed
- Maintain consistent formatting and naming conventions from original implementation
- Produce final repaired app.py and templates/*.html for deployment

CRITICAL REQUIREMENTS:
- Use write_text_file tool for saving repaired source files
- Do not alter unrelated code sections or add unrequested features
- Final files must fully comply with design_spec.md and incorporate all repair actions
- Do not include any validation status markers in output artifacts

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'validation_a.md', 'source': 'ValidationEngineerA'}, {'type': 'text_file', 'name': 'validation_b.md', 'source': 'ValidationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignAnalystA': [
        ("DesignMerger", """Check design_candidate_a.md for completeness in specifying Flask route names, page titles, element IDs, navigation button functions, and usage of local text files for data storage.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for completeness and correctness in all UI design details and data handling before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify that design_spec.md is a coherent, complete, and implementation-ready specification covering all required pages, routes, UI elements, and data storage formats.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Independently verify candidate A's app and templates follow design_spec.md routes, UI element IDs, and data handling accurately.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Independently verify candidate B's app and templates follow design_spec.md details accurately before merging.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Confirm final app.py and templates/*.html form a coherent, runnable Flask application matching design_spec.md fully.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for clear, actionable validation of routes, UI elements, and data file usage before merging repairs.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Check validation_b.md for thorough, reproducible validation results aligned with design_spec.md before merging.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Verify final app.py and templates/*.html correctly incorporate repairs from validations, preserve design_spec.md contract, and are ready for deployment.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel execution of DesignAnalystA and DesignAnalystB
    await asyncio.gather(
        execute(DesignAnalystA, "Analyze user_task_description and produce comprehensive NewsPortal design spec in design_candidate_a.md with exact Flask routes, page titles, UI element IDs, navigation buttons, and data file usage."),
        execute(DesignAnalystB, "Analyze user_task_description and produce independent design_candidate_b.md with complete NewsPortal design spec including Flask routes, exact UI element IDs, page titles, navigation, and data file handling.")
    )

    # Read outputs from DesignAnalystA and DesignAnalystB for merger
    design_candidate_a_content, design_candidate_b_content = "", ""
    try:
        design_candidate_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Execute DesignMerger to merge both design candidates into design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_candidate_a_content}\n\n=== DesignAnalystB ===\n{design_candidate_b_content}\n\n"
                  "Read both independent design specs and user_task_description, then merge into a single coherent design_spec.md covering all nine NewsPortal pages with consistent Flask route names, exact UI element IDs, navigation, and local text file data handling.")
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
        timeout_threshold=280,
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
        timeout_threshold=280,
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
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel implementation by both engineers
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement full NewsPortal Flask app as app_candidate_a.py with all routes, templates, and data handling as per design_spec.md. "
                "Use templates_candidate_a/ for HTML files with exact IDs and navigation."),
        execute(ImplementationEngineerB,
                "Implement full NewsPortal Flask app as app_candidate_b.py with all routes, templates, and data handling as per design_spec.md. "
                "Use templates_candidate_b/ for HTML files with exact IDs and navigation.")
    )

    # Read output files from both implementations to provide input for merger
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
        # Read all templates_candidate_a/*.html content as a single string for injection
        # For simplicity, treat as one artifact string
        templates_candidate_a_content = open("templates_candidate_a/index.html").read()
    except:
        pass
    try:
        # Similarly for candidate_b templates
        templates_candidate_b_content = open("templates_candidate_b/index.html").read()
    except:
        pass

    # Provide merger with all inputs for comparison and merging
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a (excerpt) ===\n{templates_candidate_a_content}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b (excerpt) ===\n{templates_candidate_b_content}\n\n"
                  "Merge into unified app.py and templates/*.html with exact routes, element IDs, page titles, data handling, and messages as per design_spec.md.")
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=50
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
        recovery_time=50
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

    # Execute validations in parallel
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate app.py and templates/*.html for correctness of routes, UI elements, navigation, data interactions, and success/error messages. "
                "Produce detailed validation report validation_a.md."),
        execute(ValidationEngineerB,
                "Independently verify app.py and templates/*.html for route existence, UI element IDs, data file handling, and UI behaviors. "
                "Produce validation_b.md with thorough findings and repair suggestions.")
    )

    # Read validation reports
    validation_a_output, validation_b_output = "", ""
    try:
        validation_a_output = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_output = open("validation_b.md").read()
    except:
        pass

    # Execute repair merger
    await execute(RepairMerger,
                  f"Merge validation_a.md and validation_b.md repair suggestions. "
                  f"Apply all valid repairs to app.py and templates/*.html preserving original structure and design specs. "
                  f"Output final repaired app.py and templates/*.html.\n\n"
                  f"=== ValidationEngineerA Report ===\n{validation_a_output}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_output}")
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
