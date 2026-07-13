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
# 20260713_210029_621278/main_20260713_210029_621278.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent complete web design specifications for the RealEstate app and merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create full detailed design specs from the user task in parallel without \"\n        \"access to each other's work; DesignMerger then reviews both specs and merges into a single coherent design_spec.md including \"\n        \"exact Flask routes, page titles, element IDs, template filenames, context variable mappings, data path and format specifications, \"\n        \"and page navigation flow according to the requirements.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in web application design specifications.\n\nYour goal is to create a full independent detailed design specification for a real estate web application that comprehensively captures all 8 user-required pages, their exact Flask routes, page titles, element and button IDs, template filenames, context variable mappings, and data storage formats.\n\nTask Details:\n- Read user_task_description to extract all interface elements, page details, and data file schemas\n- Produce a detailed design candidate specification as design_candidate_a.md\n- Include exact Flask routes for each page and dynamic routes for detail views\n- Specify all page titles, element IDs including dynamic button IDs with patterns, and template filenames\n- Define context variables to be passed to each template, matching page content\n- Specify local text data files with paths, formats, and field order per user data storage definitions\n- Do NOT reference any other analyst’s work; work independently\n\nDesign Specification Requirements:\n1. Flask Routes:\n   - Include route path, function name, HTTP methods\n   - Include dynamic routes with parameters where appropriate (e.g., /property/<int:property_id>)\n2. Page Titles and Templates:\n   - Assign exact titles as per user task\n   - Map each page to a unique template filename (e.g., dashboard.html)\n3. Element IDs:\n   - Include all specified IDs for containers, buttons, inputs, tables, dropdowns, etc.\n   - For dynamic elements, specify ID patterns using {variable} notation\n4. Context Variables:\n   - List all variables passed from route to template\n   - Include data types or data structure descriptions (e.g., list of dicts)\n5. Data File Formats:\n   - Specify file paths under data/\n   - Specify delimiter and exact field order per user task\n   - Include brief descriptions of stored data\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_candidate_a.md\n- Ensure the design spec fully captures user task requirements for independent implementation\n- Maintain clarity and precision: unambiguous route and data definitions\n- Do not mention the parallel analyst or merging process within your output\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in detailed web application design documentation.\n\nYour goal is to independently produce a complete detailed design specification for a real estate web application that covers all 8 pages with precise Flask routing, page titles, element IDs, button IDs, template file mapping, context variables, and data management as defined in the user task.\n\nTask Details:\n- Analyze the user_task_description thoroughly to extract all needed specifications\n- Compile the design candidate as design_candidate_b.md with an alternative perspective\n- Clearly define Flask routes including dynamic parameters for property, inquiry, agent, and location details\n- Assign correct page titles and corresponding template filenames for all pages\n- Document every element and button ID including patterns for dynamic IDs\n- Define variables passed to templates including their types and structures\n- Document data file formats, exact delimiters, and field sequences with explanations\n\nCRITICAL REQUIREMENTS:\n- Save all output precisely using write_text_file tool as design_candidate_b.md\n- Provide a complete and feasible design that covers user requirements exhaustively and could be directly used for implementation\n- Do not reference outputs from any other analyst or mention the merging step\n- Strive for clarity and unambiguous specification\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Software Architect specializing in consolidating parallel design documents into a coherent implementation-ready specification.\n\nYour goal is to review two detailed design candidate specifications for a real estate web app, reconcile any differences or omissions, and produce a unified, precise, and complete design_spec.md that includes full Flask routes, page titles, element IDs, template filenames, context variable mappings, local text data file paths and formats, and page navigation structures according to the user requirements.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md carefully\n- Identify discrepancies, missing elements, or conflicting design choices between the two candidate specs\n- Merge the specs into one seamless design_spec.md adhering strictly to the user task\n- Ensure all 8 pages are fully covered with exact route paths, including dynamic routes\n- Include all specified element IDs and dynamic ID patterns systematically\n- Specify template filenames for all pages uniformly\n- Define context variables per route template mapping with clear data types and structures\n- Explicitly state data storage files location, delimiter, and field order according to user data schemas\n- Ensure navigation paths are consistent and allow full functionality as described in user task\n\nCRITICAL REQUIREMENTS:\n- Output the consolidated design_spec.md using write_text_file tool\n- The merged specification must be implementation-ready with no ambiguity or omissions\n- Retain all relevant details from both candidates while eliminating contradictions\n- Do not invent data not supported by user or candidate inputs\n- Maintain clarity, precision, and usability as the highest priority\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for comprehensive, feasible, and exact representation of all required pages, routes, element IDs, and data file usage before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for comprehensive, feasible, and exact representation of all required pages, routes, element IDs, and data file usage before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete Flask-based RealEstate web app implementations with Python app.py and templates, and merge into final app.py and templates\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement fully functional Python app.py and templates/*.html \"\n        \"based on design_spec.md without access to each other's work; ImplementationMerger then reviews and merges both implementations \"\n        \"into a single coherent final app.py and templates/*.html enforcing exact Flask routes, page titles, element IDs, template filenames, \"\n        \"render_template usage, and data file integration per design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web applications using Python.\n\nYour goal is to implement a complete, fully functional RealEstate web application including app_candidate_a.py and templates_candidate_a/*.html that adheres strictly to the provided design_spec.md and user task requirements.\n\nTask Details:\n- Read user_task_description and design_spec.md carefully.\n- Implement all 8 specified pages with Flask routes, render_templates, and navigation as described.\n- Use local text files for data loading as specified; no authentication needed.\n- Use template folder templates_candidate_a.\n- Output artifacts: app_candidate_a.py and templates_candidate_a/*.html.\n- No access or reference to ImplementationEngineerB's work; work independently.\n\nImplementation Guidelines:\n1. Flask Application Setup:\n   - Initialize Flask app in app_candidate_a.py.\n   - Implement all routes exactly as specified in design_spec.md.\n   - Use render_template with correct template filenames in templates_candidate_a.\n\n2. Data Handling:\n   - Load data from local data/*.txt files respecting exact pipe-delimited schemas.\n   - Gracefully handle file reading errors.\n   - No database usage.\n\n3. Templates:\n   - Create all templates in templates_candidate_a/ with exact element IDs.\n   - Include all buttons, inputs, and navigation elements as specified.\n   - Use Jinja2 syntax to bind context variables precisely.\n\n4. Navigation and Buttons:\n   - Implement navigation buttons to respective routes as per design_spec.md.\n   - Ensure dynamic button IDs and links use correct property or inquiry IDs.\n\nCritical Requirements:\n- Use write_text_file tool to save app_candidate_a.py and all templates in templates_candidate_a/.\n- Follow element IDs, route names, and data file formats exactly as specified.\n- Do not reference or merge code from ImplementationEngineerB.\n- Ensure the app runs correctly with no runtime dependencies on candidate_b files.\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web applications using Python.\n\nYour goal is to implement a complete, fully functional RealEstate web application including app_candidate_b.py and templates_candidate_b/*.html that adheres strictly to the provided design_spec.md and user task requirements.\n\nTask Details:\n- Read user_task_description and design_spec.md carefully.\n- Implement all 8 specified pages with Flask routes, render_templates, and navigation as described.\n- Use local text files for data loading as specified; no authentication needed.\n- Use template folder templates_candidate_b.\n- Output artifacts: app_candidate_b.py and templates_candidate_b/*.html.\n- No access or reference to ImplementationEngineerA's work; work independently.\n\nImplementation Guidelines:\n1. Flask Application Setup:\n   - Initialize Flask app in app_candidate_b.py.\n   - Implement all routes exactly as specified in design_spec.md.\n   - Use render_template with correct template filenames in templates_candidate_b.\n\n2. Data Handling:\n   - Load data from local data/*.txt files respecting exact pipe-delimited schemas.\n   - Gracefully handle file reading errors.\n   - No database usage.\n\n3. Templates:\n   - Create all templates in templates_candidate_b/ with exact element IDs.\n   - Include all buttons, inputs, and navigation elements as specified.\n   - Use Jinja2 syntax to bind context variables precisely.\n\n4. Navigation and Buttons:\n   - Implement navigation buttons to respective routes as per design_spec.md.\n   - Ensure dynamic button IDs and links use correct property or inquiry IDs.\n\nCritical Requirements:\n- Use write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/.\n- Follow element IDs, route names, and data file formats exactly as specified.\n- Do not reference or merge code from ImplementationEngineerA.\n- Ensure the app runs correctly with no runtime dependencies on candidate_a files.\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in merging and integrating multiple Flask web application implementations.\n\nYour goal is to produce a final coherent and fully functional RealEstate Flask application by merging app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html, strictly following design_spec.md without dependencies on candidate-specific directories.\n\nTask Details:\n- Read user_task_description, design_spec.md, and all candidate implementation files.\n- Compare and reconcile differences and omissions between candidate A and candidate B implementations.\n- Ensure final app.py contains complete and consistent Flask routes for all 8 pages.\n- Ensure templates/*.html incorporate all required page titles, element IDs, buttons, and navigation accurately.\n- Enforce exact render_template calls with proper template names (no candidate suffixes).\n- Integrate data loading correctly from local text files as per schemas.\n- Remove all candidate-specific folder dependencies; output final app.py and templates/*.html.\n\nMerge and Validation Guidelines:\n1. Route and Function Consolidation:\n   - Merge all routes from both candidates preserving correctness and completeness.\n   - Resolve conflicting implementations per design_spec.md requirements.\n\n2. Template Merging:\n   - Combine template functionality ensuring all required elements and IDs are present.\n   - Maintain naming consistency: templates/*.html.\n\n3. Data File Handling:\n   - Use correct parsing of data files per design_spec.md.\n   - Handle file I/O gracefully and correctly in final app.py.\n\n4. Code Consistency:\n   - Write clean, readable, and maintainable code.\n   - Avoid duplicate routes or functions.\n   - Ensure navigation buttons point correctly to routes.\n\nCritical Requirements:\n- Use write_text_file tool to save final app.py and templates/*.html.\n- Strictly conform to design_spec.md route names, page titles, element IDs, and data formats.\n- Output files must be runnable with no dependencies on candidate directories.\n- Provide only the final merged artifacts without commentary.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate A's app_candidate_a.py and templates_candidate_a/*.html for adherence to design_spec.md, route correctness, and data file integration.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate B's app_candidate_b.py and templates_candidate_b/*.html for adherence to design_spec.md, route correctness, and data file integration.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validations against final app.py and templates and merge their repair suggestions into a final coherent app.py and templates\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate the final app.py and templates/*.html for syntax, route behavior, \"\n        \"element ID correctness, data file integration, UI rendering, navigation flow, and user requirements compliance without accessing each other's reports; \"\n        \"RepairMerger consumes both validation reports plus implementation artifacts to produce the final repaired app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web application validation.\n\nYour goal is to independently validate the final backend (app.py) and frontend templates (templates/*.html) for correctness, completeness, UI rendering, and adherence to the requirements.\n\nTask Details:\n- Read user_task_description for overall requirements context\n- Read design_spec.md to understand expected routes, element IDs, page titles, and data schemas\n- Validate app.py for syntax correctness, Flask route functionality, and proper data integration with data files\n- Validate templates/*.html for correct element IDs, page titles, navigation links, and UI rendering based on design_spec.md\n- Produce a detailed validation report named validation_a.md outlining all findings and suggested repairs\n\nValidation Checklist:\n1. Syntax Validation:\n   - Use validate_python_file tool to check app.py syntax and runtime errors\n\n2. Route and Data Integration:\n   - Confirm all Flask routes exist as per design_spec.md\n   - Verify route handlers correctly load and utilize data files as specified\n   - Check handling of missing or malformed data gracefully\n\n3. Frontend Validation:\n   - Check presence and correctness of all element IDs in templates\n   - Verify page titles match user requirements exactly\n   - Confirm navigation buttons link correctly to routes\n   - Assess UI rendering consistency and responsiveness\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools as appropriate\n- Use write_text_file tool to produce validation_a.md report\n- Focus exclusively on final app.py and templates/*.html relative to design_spec.md and user requirements\n- Validation report must cover syntax, routes, UI, navigation, and data consistency comprehensively\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Quality Assurance Engineer with expertise in Flask applications and frontend template validation.\n\nYour goal is to independently perform thorough validation of the backend app.py and frontend templates/*.html for functional correctness, UI stability, and compliance with data and user requirements.\n\nTask Details:\n- Analyze user_task_description to understand end-user scenarios and requirements\n- Examine design_spec.md to verify expected page elements, data file usage, and route correctness\n- Validate app.py for route accuracy, data file integration, and error handling\n- Validate templates/*.html for correct element IDs, page titles, navigation flows, and UI presentation\n- Produce a detailed validation report named validation_b.md capturing findings and recommended fixes\n\nValidation Focus Areas:\n1. Syntax and Runtime:\n   - Use validate_python_file on app.py\n   - Test key route behaviors via execute_python_code simulations if applicable\n\n2. Data and Route Consistency:\n   - Confirm app.py routes match design_spec.md specifications\n   - Check integration with data files matches specified field orders and contents\n\n3. Frontend Compliance:\n   - Verify all element IDs are present and correctly named\n   - Confirm page titles and navigation buttons match design requirements\n   - Evaluate frontend rendering stability and usability\n\nCRITICAL REQUIREMENTS:\n- Employ validate_python_file and execute_python_code tools as needed\n- Use write_text_file tool to output validation_b.md\n- Validate final app.py and templates/*.html only, using design_spec.md and user requirements as reference\n- Validation report must be comprehensive, actionable, and focused on defects and remediation\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in merging validation feedback and applying code repairs in Flask web applications.\n\nYour goal is to merge independent validation reports from two validators and reconcile their suggested fixes to produce a final repaired and coherent app.py and templates/*.html set that fully conforms to design and user requirements.\n\nTask Details:\n- Read validation_a.md and validation_b.md carefully, compare and reconcile differing or overlapping repair suggestions\n- Review user_task_description and design_spec.md to ensure all repairs maintain original functional and UI contracts\n- Apply necessary fixes to app.py and templates/*.html from ImplementationMerger to address all validated issues\n- Ensure merged fixes preserve code integrity, readability, and compliance with design specifications\n- Output the final repaired app.py and templates/*.html files\n\nMerger Guidelines:\n1. Prioritize fixes that address critical syntax errors and route/functionality issues first\n2. Harmonize frontend element IDs, navigation links, and page title corrections consistently\n3. Avoid introducing new features or deviating from design requirements\n4. Maintain clear, organized, and maintainable code structure\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save repaired app.py and templates/*.html\n- Preserve all design contracts and specifications precisely\n- Focus corrections strictly on validated issues and suggested remediations\n- Final output must be deployable without syntax errors and fully compliant with user task\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Assess validation_a.md for thoroughness and clearly actionable backend and frontend corrections before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Assess validation_b.md for thoroughness and clearly actionable backend and frontend corrections before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'RealEstate' Web Application

## 1. Objective
Develop a comprehensive web application named 'RealEstate' using Python, with data managed through local text files. The application enables users to browse property listings, search by location and price, view property details, submit inquiries, and manage favorite properties. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'RealEstate' application is Python.

## 3. Page Design

The 'RealEstate' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Real Estate Dashboard
- **Overview**: The main hub displaying featured properties, recent listings, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-properties** - Type: Div - Display of featured property recommendations.
  - **ID: browse-properties-button** - Type: Button - Button to navigate to property search page.
  - **ID: my-inquiries-button** - Type: Button - Button to navigate to inquiries page.
  - **ID: my-favorites-button** - Type: Button - Button to navigate to favorites page.

### 2. Property Search Page
- **Page Title**: Property Search
- **Overview**: A page displaying all available properties with advanced search and filter capabilities.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-input** - Type: Input - Field to search properties by location/city.
  - **ID: price-range-min** - Type: Input (number) - Field to set minimum price filter.
  - **ID: price-range-max** - Type: Input (number) - Field to set maximum price filter.
  - **ID: property-type-filter** - Type: Dropdown - Dropdown to filter by property type (House, Apartment, Condo, Land).
  - **ID: properties-grid** - Type: Div - Grid displaying property cards with image, location, price, and beds/baths.
  - **ID: view-property-button-{property_id}** - Type: Button - Button to view property details (each property card has this).

### 3. Property Details Page
- **Page Title**: Property Details
- **Overview**: A page displaying detailed information about a specific property.
- **Elements**:
  - **ID: property-details-page** - Type: Div - Container for the property details page.
  - **ID: property-address** - Type: H1 - Display property address.
  - **ID: property-price** - Type: Div - Display property price.
  - **ID: property-description** - Type: Div - Display property description.
  - **ID: property-features** - Type: Div - Display property features (beds, baths, square footage).
  - **ID: add-to-favorites-button** - Type: Button - Button to add property to favorites.
  - **ID: submit-inquiry-button** - Type: Button - Button to submit inquiry for property.

### 4. Property Inquiry Page
- **Page Title**: Submit Property Inquiry
- **Overview**: A page for users to submit inquiries for properties they are interested in.
- **Elements**:
  - **ID: inquiry-page** - Type: Div - Container for the inquiry page.
  - **ID: select-property** - Type: Dropdown - Dropdown to select property for inquiry.
  - **ID: inquiry-name** - Type: Input - Field to input customer name.
  - **ID: inquiry-email** - Type: Input (email) - Field to input customer email.
  - **ID: inquiry-phone** - Type: Input (tel) - Field to input customer phone.
  - **ID: inquiry-message** - Type: Textarea - Field to write inquiry message.
  - **ID: submit-inquiry-button** - Type: Button - Button to submit inquiry.

### 5. My Inquiries Page
- **Page Title**: My Inquiries
- **Overview**: A page displaying all submitted inquiries and their status.
- **Elements**:
  - **ID: inquiries-page** - Type: Div - Container for the inquiries page.
  - **ID: inquiries-table** - Type: Table - Table displaying inquiries with property, date, status, and contact info.
  - **ID: inquiry-status-filter** - Type: Dropdown - Dropdown to filter by status (All, Pending, Contacted, Resolved).
  - **ID: delete-inquiry-button-{inquiry_id}** - Type: Button - Button to delete inquiry (each inquiry has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. My Favorites Page
- **Page Title**: My Favorite Properties
- **Overview**: A page displaying all properties added to favorites.
- **Elements**:
  - **ID: favorites-page** - Type: Div - Container for the favorites page.
  - **ID: favorites-list** - Type: Div - List of all favorite properties with address, price, and action buttons.
  - **ID: remove-from-favorites-button-{property_id}** - Type: Button - Button to remove property from favorites (each property has this).
  - **ID: view-property-button-{property_id}** - Type: Button - Button to view property details (each property has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Agent Directory Page
- **Page Title**: Real Estate Agents
- **Overview**: A page displaying all real estate agents and their contact information.
- **Elements**:
  - **ID: agents-page** - Type: Div - Container for the agents page.
  - **ID: agents-list** - Type: Div - List of all agents with photo, name, specialization, and contact info.
  - **ID: agent-search** - Type: Input - Field to search agents by name.
  - **ID: contact-agent-button-{agent_id}** - Type: Button - Button to contact agent (each agent has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Locations Page
- **Page Title**: Featured Locations
- **Overview**: A page displaying popular locations with property count and details.
- **Elements**:
  - **ID: locations-page** - Type: Div - Container for the locations page.
  - **ID: locations-list** - Type: Div - List of all locations with name, property count, and average price.
  - **ID: view-location-button-{location_id}** - Type: Button - Button to view properties in location (each location has this).
  - **ID: location-sort** - Type: Dropdown - Dropdown to sort locations (By Name, By Properties Count, By Average Price).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'RealEstate' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Properties Data
- **File Name**: `properties.txt`
- **Data Format**:
  ```
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
  ```
- **Example Data**:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|location_name|region|average_price|property_count|description
  ```
- **Example Data**:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. Property Inquiries Data
- **File Name**: `inquiries.txt`
- **Data Format**:
  ```
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
  ```
- **Example Data**:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. Favorite Properties Data
- **File Name**: `favorites.txt`
- **Data Format**:
  ```
  favorite_id|property_id|added_date
  ```
- **Example Data**:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. Real Estate Agents Data
- **File Name**: `agents.txt`
- **Data Format**:
  ```
  agent_id|agent_name|specialization|email|phone|properties_sold
  ```
- **Example Data**:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
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
            """You are a Software Designer specializing in web application design specifications.

Your goal is to create a full independent detailed design specification for a real estate web application that comprehensively captures all 8 user-required pages, their exact Flask routes, page titles, element and button IDs, template filenames, context variable mappings, and data storage formats.

Task Details:
- Read user_task_description to extract all interface elements, page details, and data file schemas
- Produce a detailed design candidate specification as design_candidate_a.md
- Include exact Flask routes for each page and dynamic routes for detail views
- Specify all page titles, element IDs including dynamic button IDs with patterns, and template filenames
- Define context variables to be passed to each template, matching page content
- Specify local text data files with paths, formats, and field order per user data storage definitions
- Do NOT reference any other analyst’s work; work independently

Design Specification Requirements:
1. Flask Routes:
   - Include route path, function name, HTTP methods
   - Include dynamic routes with parameters where appropriate (e.g., /property/<int:property_id>)
2. Page Titles and Templates:
   - Assign exact titles as per user task
   - Map each page to a unique template filename (e.g., dashboard.html)
3. Element IDs:
   - Include all specified IDs for containers, buttons, inputs, tables, dropdowns, etc.
   - For dynamic elements, specify ID patterns using {variable} notation
4. Context Variables:
   - List all variables passed from route to template
   - Include data types or data structure descriptions (e.g., list of dicts)
5. Data File Formats:
   - Specify file paths under data/
   - Specify delimiter and exact field order per user task
   - Include brief descriptions of stored data

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_candidate_a.md
- Ensure the design spec fully captures user task requirements for independent implementation
- Maintain clarity and precision: unambiguous route and data definitions
- Do not mention the parallel analyst or merging process within your output

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Designer specializing in detailed web application design documentation.

Your goal is to independently produce a complete detailed design specification for a real estate web application that covers all 8 pages with precise Flask routing, page titles, element IDs, button IDs, template file mapping, context variables, and data management as defined in the user task.

Task Details:
- Analyze the user_task_description thoroughly to extract all needed specifications
- Compile the design candidate as design_candidate_b.md with an alternative perspective
- Clearly define Flask routes including dynamic parameters for property, inquiry, agent, and location details
- Assign correct page titles and corresponding template filenames for all pages
- Document every element and button ID including patterns for dynamic IDs
- Define variables passed to templates including their types and structures
- Document data file formats, exact delimiters, and field sequences with explanations

CRITICAL REQUIREMENTS:
- Save all output precisely using write_text_file tool as design_candidate_b.md
- Provide a complete and feasible design that covers user requirements exhaustively and could be directly used for implementation
- Do not reference outputs from any other analyst or mention the merging step
- Strive for clarity and unambiguous specification

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Software Architect specializing in consolidating parallel design documents into a coherent implementation-ready specification.

Your goal is to review two detailed design candidate specifications for a real estate web app, reconcile any differences or omissions, and produce a unified, precise, and complete design_spec.md that includes full Flask routes, page titles, element IDs, template filenames, context variable mappings, local text data file paths and formats, and page navigation structures according to the user requirements.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md carefully
- Identify discrepancies, missing elements, or conflicting design choices between the two candidate specs
- Merge the specs into one seamless design_spec.md adhering strictly to the user task
- Ensure all 8 pages are fully covered with exact route paths, including dynamic routes
- Include all specified element IDs and dynamic ID patterns systematically
- Specify template filenames for all pages uniformly
- Define context variables per route template mapping with clear data types and structures
- Explicitly state data storage files location, delimiter, and field order according to user data schemas
- Ensure navigation paths are consistent and allow full functionality as described in user task

CRITICAL REQUIREMENTS:
- Output the consolidated design_spec.md using write_text_file tool
- The merged specification must be implementation-ready with no ambiguity or omissions
- Retain all relevant details from both candidates while eliminating contradictions
- Do not invent data not supported by user or candidate inputs
- Maintain clarity, precision, and usability as the highest priority

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Software Developer specializing in Flask web applications using Python.

Your goal is to implement a complete, fully functional RealEstate web application including app_candidate_a.py and templates_candidate_a/*.html that adheres strictly to the provided design_spec.md and user task requirements.

Task Details:
- Read user_task_description and design_spec.md carefully.
- Implement all 8 specified pages with Flask routes, render_templates, and navigation as described.
- Use local text files for data loading as specified; no authentication needed.
- Use template folder templates_candidate_a.
- Output artifacts: app_candidate_a.py and templates_candidate_a/*.html.
- No access or reference to ImplementationEngineerB's work; work independently.

Implementation Guidelines:
1. Flask Application Setup:
   - Initialize Flask app in app_candidate_a.py.
   - Implement all routes exactly as specified in design_spec.md.
   - Use render_template with correct template filenames in templates_candidate_a.

2. Data Handling:
   - Load data from local data/*.txt files respecting exact pipe-delimited schemas.
   - Gracefully handle file reading errors.
   - No database usage.

3. Templates:
   - Create all templates in templates_candidate_a/ with exact element IDs.
   - Include all buttons, inputs, and navigation elements as specified.
   - Use Jinja2 syntax to bind context variables precisely.

4. Navigation and Buttons:
   - Implement navigation buttons to respective routes as per design_spec.md.
   - Ensure dynamic button IDs and links use correct property or inquiry IDs.

Critical Requirements:
- Use write_text_file tool to save app_candidate_a.py and all templates in templates_candidate_a/.
- Follow element IDs, route names, and data file formats exactly as specified.
- Do not reference or merge code from ImplementationEngineerB.
- Ensure the app runs correctly with no runtime dependencies on candidate_b files.

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Flask web applications using Python.

Your goal is to implement a complete, fully functional RealEstate web application including app_candidate_b.py and templates_candidate_b/*.html that adheres strictly to the provided design_spec.md and user task requirements.

Task Details:
- Read user_task_description and design_spec.md carefully.
- Implement all 8 specified pages with Flask routes, render_templates, and navigation as described.
- Use local text files for data loading as specified; no authentication needed.
- Use template folder templates_candidate_b.
- Output artifacts: app_candidate_b.py and templates_candidate_b/*.html.
- No access or reference to ImplementationEngineerA's work; work independently.

Implementation Guidelines:
1. Flask Application Setup:
   - Initialize Flask app in app_candidate_b.py.
   - Implement all routes exactly as specified in design_spec.md.
   - Use render_template with correct template filenames in templates_candidate_b.

2. Data Handling:
   - Load data from local data/*.txt files respecting exact pipe-delimited schemas.
   - Gracefully handle file reading errors.
   - No database usage.

3. Templates:
   - Create all templates in templates_candidate_b/ with exact element IDs.
   - Include all buttons, inputs, and navigation elements as specified.
   - Use Jinja2 syntax to bind context variables precisely.

4. Navigation and Buttons:
   - Implement navigation buttons to respective routes as per design_spec.md.
   - Ensure dynamic button IDs and links use correct property or inquiry IDs.

Critical Requirements:
- Use write_text_file tool to save app_candidate_b.py and all templates in templates_candidate_b/.
- Follow element IDs, route names, and data file formats exactly as specified.
- Do not reference or merge code from ImplementationEngineerA.
- Ensure the app runs correctly with no runtime dependencies on candidate_a files.

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Engineer specializing in merging and integrating multiple Flask web application implementations.

Your goal is to produce a final coherent and fully functional RealEstate Flask application by merging app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html, strictly following design_spec.md without dependencies on candidate-specific directories.

Task Details:
- Read user_task_description, design_spec.md, and all candidate implementation files.
- Compare and reconcile differences and omissions between candidate A and candidate B implementations.
- Ensure final app.py contains complete and consistent Flask routes for all 8 pages.
- Ensure templates/*.html incorporate all required page titles, element IDs, buttons, and navigation accurately.
- Enforce exact render_template calls with proper template names (no candidate suffixes).
- Integrate data loading correctly from local text files as per schemas.
- Remove all candidate-specific folder dependencies; output final app.py and templates/*.html.

Merge and Validation Guidelines:
1. Route and Function Consolidation:
   - Merge all routes from both candidates preserving correctness and completeness.
   - Resolve conflicting implementations per design_spec.md requirements.

2. Template Merging:
   - Combine template functionality ensuring all required elements and IDs are present.
   - Maintain naming consistency: templates/*.html.

3. Data File Handling:
   - Use correct parsing of data files per design_spec.md.
   - Handle file I/O gracefully and correctly in final app.py.

4. Code Consistency:
   - Write clean, readable, and maintainable code.
   - Avoid duplicate routes or functions.
   - Ensure navigation buttons point correctly to routes.

Critical Requirements:
- Use write_text_file tool to save final app.py and templates/*.html.
- Strictly conform to design_spec.md route names, page titles, element IDs, and data formats.
- Output files must be runnable with no dependencies on candidate directories.
- Provide only the final merged artifacts without commentary.

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

Your goal is to independently validate the final backend (app.py) and frontend templates (templates/*.html) for correctness, completeness, UI rendering, and adherence to the requirements.

Task Details:
- Read user_task_description for overall requirements context
- Read design_spec.md to understand expected routes, element IDs, page titles, and data schemas
- Validate app.py for syntax correctness, Flask route functionality, and proper data integration with data files
- Validate templates/*.html for correct element IDs, page titles, navigation links, and UI rendering based on design_spec.md
- Produce a detailed validation report named validation_a.md outlining all findings and suggested repairs

Validation Checklist:
1. Syntax Validation:
   - Use validate_python_file tool to check app.py syntax and runtime errors

2. Route and Data Integration:
   - Confirm all Flask routes exist as per design_spec.md
   - Verify route handlers correctly load and utilize data files as specified
   - Check handling of missing or malformed data gracefully

3. Frontend Validation:
   - Check presence and correctness of all element IDs in templates
   - Verify page titles match user requirements exactly
   - Confirm navigation buttons link correctly to routes
   - Assess UI rendering consistency and responsiveness

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools as appropriate
- Use write_text_file tool to produce validation_a.md report
- Focus exclusively on final app.py and templates/*.html relative to design_spec.md and user requirements
- Validation report must cover syntax, routes, UI, navigation, and data consistency comprehensively

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Quality Assurance Engineer with expertise in Flask applications and frontend template validation.

Your goal is to independently perform thorough validation of the backend app.py and frontend templates/*.html for functional correctness, UI stability, and compliance with data and user requirements.

Task Details:
- Analyze user_task_description to understand end-user scenarios and requirements
- Examine design_spec.md to verify expected page elements, data file usage, and route correctness
- Validate app.py for route accuracy, data file integration, and error handling
- Validate templates/*.html for correct element IDs, page titles, navigation flows, and UI presentation
- Produce a detailed validation report named validation_b.md capturing findings and recommended fixes

Validation Focus Areas:
1. Syntax and Runtime:
   - Use validate_python_file on app.py
   - Test key route behaviors via execute_python_code simulations if applicable

2. Data and Route Consistency:
   - Confirm app.py routes match design_spec.md specifications
   - Check integration with data files matches specified field orders and contents

3. Frontend Compliance:
   - Verify all element IDs are present and correctly named
   - Confirm page titles and navigation buttons match design requirements
   - Evaluate frontend rendering stability and usability

CRITICAL REQUIREMENTS:
- Employ validate_python_file and execute_python_code tools as needed
- Use write_text_file tool to output validation_b.md
- Validate final app.py and templates/*.html only, using design_spec.md and user requirements as reference
- Validation report must be comprehensive, actionable, and focused on defects and remediation

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Engineer specializing in merging validation feedback and applying code repairs in Flask web applications.

Your goal is to merge independent validation reports from two validators and reconcile their suggested fixes to produce a final repaired and coherent app.py and templates/*.html set that fully conforms to design and user requirements.

Task Details:
- Read validation_a.md and validation_b.md carefully, compare and reconcile differing or overlapping repair suggestions
- Review user_task_description and design_spec.md to ensure all repairs maintain original functional and UI contracts
- Apply necessary fixes to app.py and templates/*.html from ImplementationMerger to address all validated issues
- Ensure merged fixes preserve code integrity, readability, and compliance with design specifications
- Output the final repaired app.py and templates/*.html files

Merger Guidelines:
1. Prioritize fixes that address critical syntax errors and route/functionality issues first
2. Harmonize frontend element IDs, navigation links, and page title corrections consistently
3. Avoid introducing new features or deviating from design requirements
4. Maintain clear, organized, and maintainable code structure

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save repaired app.py and templates/*.html
- Preserve all design contracts and specifications precisely
- Focus corrections strictly on validated issues and suggested remediations
- Final output must be deployable without syntax errors and fully compliant with user task

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
        ("DesignMerger", """Check design_candidate_a.md for comprehensive, feasible, and exact representation of all required pages, routes, element IDs, and data file usage before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for comprehensive, feasible, and exact representation of all required pages, routes, element IDs, and data file usage before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate candidate A's app_candidate_a.py and templates_candidate_a/*.html for adherence to design_spec.md, route correctness, and data file integration.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate candidate B's app_candidate_b.py and templates_candidate_b/*.html for adherence to design_spec.md, route correctness, and data file integration.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Assess validation_a.md for thoroughness and clearly actionable backend and frontend corrections before merging.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Assess validation_b.md for thoroughness and clearly actionable backend and frontend corrections before merging.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
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

    # Parallel execution for design candidates by DesignAnalystA and DesignAnalystB
    await asyncio.gather(
        execute(DesignAnalystA, "Create full detailed design specification for real estate app with all routes, page titles, element IDs, template filenames, context variables, and data file formats. Save as design_candidate_a.md."),
        execute(DesignAnalystB, "Independently produce complete detailed design specification for real estate app covering all pages, routes, element IDs, template files, context variables, and data formats. Save as design_candidate_b.md.")
    )

    # Read design candidate files for merger agent input
    design_candidate_a_content, design_candidate_b_content = "", ""
    try:
        design_candidate_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge design candidates into final design_spec.md
    await execute(DesignMerger,
                  f"User task description is available.\n"
                  f"=== Design Candidate A ===\n{design_candidate_a_content}\n\n"
                  f"=== Design Candidate B ===\n{design_candidate_b_content}\n\n"
                  f"Merge these into a single coherent, unambiguous, and complete design_spec.md that includes all required Flask routes, page titles, element IDs, template filenames, context variable mappings, data file formats, and navigation according to the user requirements.")
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

    # Read candidate A implementation files
    app_a_code, templates_a = "", ""
    try:
        app_a_code = open("app_candidate_a.py").read()
    except:
        pass
    try:
        templates_a = _read_text_artifacts("templates_candidate_a/*.html")
    except:
        pass

    # Read candidate B implementation files
    app_b_code, templates_b = "", ""
    try:
        app_b_code = open("app_candidate_b.py").read()
    except:
        pass
    try:
        templates_b = _read_text_artifacts("templates_candidate_b/*.html")
    except:
        pass

    # Parallel execution for candidate A and B implementations
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete Flask app_candidate_a.py and templates_candidate_a/*.html based on user_task_description and design_spec.md."),
        execute(ImplementationEngineerB,
                "Implement complete Flask app_candidate_b.py and templates_candidate_b/*.html based on user_task_description and design_spec.md.")
    )

    # After both implementations, merge results
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{app_a_code}\n\n"
                  f"=== templates_candidate_a/*.html ===\n{templates_a}\n\n"
                  f"=== app_candidate_b.py ===\n{app_b_code}\n\n"
                  f"=== templates_candidate_b/*.html ===\n{templates_b}\n\n"
                  "Merge the above into final coherent app.py and templates/*.html strictly following design_spec.md. "
                  "Remove candidate directory dependencies.")
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
        timeout_threshold=420,
        failure_threshold=1,
        recovery_time=45
    )

    # Parallel validation of app.py and templates
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate final app.py and templates/*.html for syntax, route correctness, data integration, UI, navigation, and compliance. "
                "Produce validation_a.md with detailed findings and suggested repairs."),
        execute(ValidationEngineerB,
                "Independently validate final app.py and templates/*.html for syntax, route accuracy, data file integration, frontend element IDs, page titles, navigation, and UI rendering. "
                "Write detailed validation_b.md report with actionable repair suggestions.")
    )

    # Read validations reports for RepairMerger input
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md", "r").read()
    except Exception:
        pass
    try:
        validation_b_content = open("validation_b.md", "r").read()
    except Exception:
        pass

    # RepairMerger merges reports and applies fixes to produce final app.py and templates/*.html
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_content}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_content}\n\n"
                  "Using user_task_description, design_spec.md, and ImplementationMerger's app.py and templates/*.html, merge validation reports, reconcile fixes, "
                  "and produce final repaired app.py and templates/*.html outputs with all issues addressed and full compliance.")
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
