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
# 20260713_210029_844454/main_20260713_210029_844454.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs for 'VirtualMuseum' app and merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create design specifications of all seven pages and data storage details following \"\n        \"the user requirements, each saving their design candidate without accessing the other's output; DesignMerger then reads both design \"\n        \"candidates and writes a merged, coherent, complete implementation-ready design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Designer with expertise in comprehensive UI/UX and data architecture for Python web applications.\n\nYour goal is to independently design a complete web application structure for the 'VirtualMuseum' app, producing a design candidate file with all implementation-relevant details.\n\nTask Details:\n- Read user_task_description carefully to understand app requirements.\n- Design all seven pages including routes, exact page titles, element IDs, and navigation flows.\n- Specify data file usage, formats, and key UI components as required.\n- Write your complete design specification into design_candidate_a.md without access to other designs.\n\nDesign Requirements:\n1. Define clear and consistent routes for each page; ensure the root route leads to the Dashboard page.\n2. Specify exact UI element IDs for each page (static and dynamic as applicable).\n3. Map navigation buttons/links to routes with route names for integration.\n4. Detail local data storage files, their formats, and key fields relevant to the app's functionality.\n5. Adhere strictly to user requirements regarding pages, data, and functionality.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output design_candidate_a.md.\n- Provide complete, precise, and unambiguous specifications so downstream developers can implement independently.\n- Focus on delivering a standalone design candidate representing the entire app structure and data details accurately.\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Designer specializing in detailed UI and data design for Python-based museum management applications.\n\nYour goal is to independently create an alternative but complete design specification for the 'VirtualMuseum' app, capturing all required pages, data formats, and navigation flows.\n\nTask Details:\n- Thoroughly analyze user_task_description to capture the scope and requirements.\n- Design every page route with precise page titles, element IDs, and user interface components.\n- Specify navigation button mappings to routes and data files usage with format details.\n- Write your full design candidate into design_candidate_b.md independently, without access to other candidates.\n\nDesign Requirements:\n1. Include consistent naming conventions for routes and UI elements.\n2. Ensure navigation allows starting from the Dashboard and accessing all features.\n3. Clearly specify all data storage files in 'data' directory with field formats and examples.\n4. Cover all seven pages comprehensively with detailed UI and interaction elements.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save your comprehensive design_candidate_b.md.\n- Ensure the design candidate is clear and complete for direct implementation guidance.\n- Maintain independence in design and avoid reliance on other candidates’ outputs.\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Integration Specialist skilled in merging multiple independent web application designs into a single coherent specification.\n\nYour goal is to review design_candidate_a.md and design_candidate_b.md for the 'VirtualMuseum' app, resolve any conflicts, omissions, or inconsistencies, and produce a unified, complete design_spec.md suitable for implementation.\n\nTask Details:\n- Read user_task_description as the authoritative source of requirements.\n- Analyze both design_candidate_a.md and design_candidate_b.md to identify overlaps and gaps.\n- Merge designs ensuring coverage of all seven pages, starting at the Dashboard, with precise page element IDs and navigation flows.\n- Verify data storage designs match the specified pipe-delimited text files and their example data.\n- Produce a merged design_spec.md that provides a consistent, unambiguous implementation contract.\n\nMerging Guidelines:\n1. Harmonize conflicting route naming and UI element IDs to a consistent scheme.\n2. Combine best design components from both candidates to ensure completeness and clarity.\n3. Maintain strict adherence to the data storage formats and examples as per requirements.\n4. Ensure the final design enables independent backend/frontend development without ambiguity.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output a single, comprehensive design_spec.md.\n- The merged specification must fully encompass user requirements and merge candidates without information loss.\n- Provide a document that ImplementationEngineerA can rely on for development without further clarifications.\n- Maintain all exact element IDs, file names, and route patterns from inputs or harmonized consistent variants.\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": (\n                \"Check design_candidate_a.md for completeness, correctness, and adherence to user requirements including all page routes, UI elements, \"\n                \"navigation flow, and data usage details before merging.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": (\n                \"Check design_candidate_b.md for completeness, correctness, and adherence to user requirements including all page routes, UI elements, \"\n                \"navigation flow, and data usage details before merging.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": (\n                \"Verify design_spec.md provides a coherent and complete implementation contract covering all required pages, navigation, element IDs, \"\n                \"and data storage format to guide implementation.\"\n            ),\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Python Flask web app bundles and templates for 'VirtualMuseum' and merge them into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently write complete Flask app bundles with app_candidate_*.py and templates_candidate_*/*.html \"\n        \"for 'VirtualMuseum', strictly following design_spec.md and user requirements, using local text file data storage and navigation starting from Dashboard; \"\n        \"ImplementationMerger then compares and merges both candidates into final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in comprehensive web application implementations.\n\nYour goal is to independently develop a complete Flask web application for the 'VirtualMuseum' project with all seven specified pages, conforming strictly to page titles, element IDs, and navigation flow, using local text file data storage under the data/ directory.\n\nTask Details:\n- Read the user_task_description and design_spec.md comprehensively.\n- Produce app_candidate_a.py implementing all backend routes and logic.\n- Produce all related HTML template files under templates_candidate_a/ matching specified element IDs and page titles.\n- Ensure navigation starts from the Dashboard page and uses button-based navigation.\n- Use proper Flask routing and render_template calls exactly as specified.\n- Do not reference or access ImplementationEngineerB's outputs.\n\nImplementation Requirements:\n1. **Flask Application Structure**:\n   - Setup Flask app with secret key.\n   - All routes must correspond to the seven pages with exact function names and paths.\n   - Implement data loading exclusively from pipe-delimited text files in the data/ folder.\n   - Implement navigation via buttons linking to appropriate routes.\n   - Use render_template() with correct template filenames.\n\n2. **Templates**:\n   - Follow exact page titles for both <title> and <h1> tags.\n   - Include all specified element IDs exactly as provided.\n   - For dynamic element IDs (e.g., view-exhibition-button-{exhibition_id}), use Jinja2 templating syntax.\n\n3. **Data Handling**:\n   - Parse all data files as pipe-delimited without headers.\n   - Ensure field order and names match data formats precisely.\n   - Handle file reading errors safely.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output app_candidate_a.py and all template files under templates_candidate_a/.\n- Adhere strictly to all specifications in the user task and design_spec.\n- Do not add extra routes, pages, or navigation elements.\n- Do not access outputs from other agents.\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer skilled in building full-featured web applications with modular templates.\n\nYour goal is to independently create a fully functional Flask app called 'VirtualMuseum' implementing all seven specified pages, using exact page titles, element IDs, and button-based navigation starting from the Dashboard. Data must be read from local text files under the data/ directory.\n\nTask Details:\n- Analyze user_task_description and design_spec.md thoroughly.\n- Develop app_candidate_b.py implementing the backend with all necessary Flask routes.\n- Implement corresponding templates under templates_candidate_b/ with exact HTML element IDs and titles.\n- Navigation must start from Dashboard and be implemented with buttons directing to proper routes.\n- Do not incorporate or access ImplementationEngineerA's outputs.\n\nImplementation Requirements:\n1. **Backend Implementation**:\n   - Set up Flask application with proper configuration.\n   - All routes must match the user requirements and design spec.\n   - Data loading from pipe-delimited text files, matching exact field order.\n   - Ensure render_template references correct template filenames.\n\n2. **Frontend Templates**:\n   - All template files should implement exact element IDs as specified.\n   - Page titles must be consistent across <title> and <h1> tags.\n   - Use Jinja2 templating syntax for dynamic elements (e.g., button IDs).\n\n3. **Navigation**:\n   - Button-based navigation between pages.\n   - Route names and template names must match design spec exactly.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to write app_candidate_b.py and all templates under templates_candidate_b/.\n- Strictly follow all specifications from the user task and design_spec.\n- Avoid referencing or merging with other implementations before merging phase.\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Specialist experienced in merging parallel Flask web application implementations.\n\nYour goal is to compare, resolve conflicts, and merge two complete Flask web app bundles for the 'VirtualMuseum' project—app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html—into final cohesive app.py and templates/*.html files, fully consistent with the user requirements and design_spec.md.\n\nTask Details:\n- Read user_task_description, design_spec.md, and all candidate implementations from ImplementationEngineerA and ImplementationEngineerB.\n- Identify and reconcile differences in Flask routes, function names, template usage, and navigation flows.\n- Resolve conflicts in templates including element IDs, page titles, and button-based navigation.\n- Ensure merged app.py is a complete, runnable Flask application covering all seven pages.\n- Ensure merged templates/*.html conform exactly to specifications, using consistent element IDs and page titles.\n\nMerge Guidelines:\n1. **Backend**:\n   - Validate all routes from both candidates; include all specified routes only once.\n   - Harmonize data loading and utility functions.\n   - Choose clear and consistent function and variable names.\n   - Ensure root route starts at Dashboard.\n\n2. **Templates**:\n   - Combine templates for identical pages, preserving all required element IDs from both candidates.\n   - Use consistent Jinja2 syntax.\n   - Ensure navigation buttons point correctly to routes.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final merged app.py and templates to templates/ directory.\n- The final merged outputs must be consistent, complete, and ready for further validation.\n- No references or code dependencies on candidate files.\n- Maintain strict adherence to the user requirements and design_spec.\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": (\n                \"Check app_candidate_a.py and templates_candidate_a/*.html for adherence to design_spec.md, exact routes, titles, element IDs, navigation flow, \"\n                \"data file usage, and visibility of requested buttons and messages.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": (\n                \"Check app_candidate_b.py and templates_candidate_b/*.html independently for compliance with design_spec.md and user requirements covering all \"\n                \"pages, exact element details, routing, and local text file data handling.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": (\n                \"Verify that the merged app.py and templates/*.html are a coherent, complete, and feasible Flask web application bundle consistent with design_spec.md \"\n                \"and user requirements, ready for validation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validation reports on app.py and templates/*.html for 'VirtualMuseum' app and merge repair suggestions into final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate app.py and templates/*.html against user requirements including all page routes, UI elements, \"\n        \"navigation flow, and local text file data format correctness, writing validation reports without sharing; RepairMerger reconciles validation reports and applies valid repairs \"\n        \"to produce final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web applications and frontend HTML template validation.\n\nYour goal is to independently validate the correctness, syntax, runtime behavior, and user requirement compliance of the Flask backend (app.py) and all HTML templates (templates/*.html) for a multi-page web application.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and templates/*.html files from CONTEXT\n- Validate ALL seven pages including routes, button presence, page titles, element IDs, navigation flow starting from Dashboard page\n- Ensure local data files conform exactly to pipe-delimited field order and format from design_spec.md\n- Produce a detailed validation report named validation_a.md with identified issues or confirm full compliance\n- Do NOT read or access validation_b.md to maintain independent validation\n\nValidation Requirements:\n1. Syntax & Runtime Checks:\n   - Use validate_python_file tool on app.py for syntax and runtime errors\n   - Spot runtime error possibilities in all route handlers and template rendering\n\n2. Functional Verification:\n   - Confirm presence and correctness of all routes for seven pages as specified\n   - Validate all required button IDs, element IDs, and pages titles per design_spec.md and user requirements\n   - Confirm navigation buttons correctly link to intended pages using specified route functions\n   - Check that root route redirects to Dashboard page\n\n3. Data Storage Validation:\n   - Verify all local text data files use pipe-delimited format as per specifications\n   - Check data file field orders against design_spec.md exactly\n   - Confirm that app.py accesses and processes these data files accordingly\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools as needed for checks\n- Use write_text_file tool to save detailed validation report as validation_a.md\n- Validation report must be thorough, clearly indicate any discrepancies or full compliance\n- Input/output files must be handled exactly as specified, no deviations\n- Do NOT reference or include any contents from validation_b.md\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in verifying backend and frontend implementations of Flask web apps.\n\nYour goal is to independently verify the implementation correctness of app.py and templates/*.html ensuring full alignment with user requirements and design specifications.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and templates/*.html files from CONTEXT\n- Verify all seven pages and their defined UI elements, including buttons and navigation controls starting from Dashboard\n- Confirm page titles exactly match specifications\n- Validate local data file adherence to required formats and correct usage in app.py\n- Produce a comprehensive validation report named validation_b.md describing conformance and discrepancies found\n- Do NOT read or access validation_a.md to maintain independence\n\nVerification Steps:\n1. User Interface and Navigation:\n   - Check all buttons and element IDs exist as per requirements on respective pages\n   - Confirm navigation flow is consistent starting at Dashboard, buttons linking to correct pages\n   - Validate proper page title presence in templates\n\n2. Backend Functionality:\n   - Confirm app.py routes exist and serve expected pages\n   - Validate expected usage of data files as per design_spec.md in backend logic\n\n3. Data Compliance:\n   - Ensure text data files are correctly structured pipe-delimited files matching field orders in design_spec.md\n   - Confirm app.py interacts with data files correctly\n\nCRITICAL SUCCESS CRITERIA:\n- Use validate_python_file and execute_python_code for syntax and runtime validation\n- Write complete detailed validation report as validation_b.md using write_text_file tool\n- Reports must avoid referencing validation_a.md\n- Input and output artifacts must not be modified or extended beyond specifications\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in merging validation feedback and applying repairs to Flask backend and frontend codebases.\n\nYour goal is to analyze independent validation reports from ValidationEngineerA and ValidationEngineerB, consolidate their repair suggestions, and apply necessary corrections to app.py and templates/*.html to fully comply with the design specification and user requirements without regressions.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md from CONTEXT\n- Compare and reconcile repairs suggested in both validation reports\n- Prioritize correctness, completeness, and full functionality adherence\n- Apply all valid fixes to source code files app.py and templates/*.html preserving structural integrity and compliance\n- Produce final corrected app.py and templates/*.html files as output artifacts\n\nRepair Process Guidelines:\n1. Validation Report Analysis:\n   - Extract and unify repair suggestions from validation_a.md and validation_b.md\n   - Identify consistent issues and prioritize critical fixes\n\n2. Implementation of Repairs:\n   - Apply corrections to backend logic, route handling, and data file access in app.py\n   - Fix template HTML to ensure presence of required element IDs, buttons, and page titles per design_spec.md\n   - Test locally to confirm no syntax or runtime regressions\n\n3. Final Output Preparation:\n   - Save updated app.py and all template files exactly as specified\n   - Ensure compatibility with merged design_spec.md and complete user task compliance\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and templates/*.html files\n- Preserve the exact file structure and naming conventions\n- Ensure all fixes maintain alignment with design_spec.md and user requirements\n- Validate no conflicts or regressions introduced during repair merging\n- Produce clean, maintainable, and fully compliant final deliverables\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": (\n                \"Verify validation_a.md for thorough testing coverage, correctness of issue identification, and alignment with user requirements before merging repairs.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": (\n                \"Verify validation_b.md for completeness, accurate issue identification related to UI, navigation, and data files before merging.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": (\n                \"Confirm that the repaired final app.py and templates/*.html remain consistent with the merged design_spec.md and cover all user requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'VirtualMuseum' Web Application

## 1. Objective
Develop a comprehensive web application named 'VirtualMuseum' using Python, with data managed through local text files. The application enables museums to manage virtual exhibitions, curate artifact collections, provide audio guides, sell visitor tickets, and host virtual events. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'VirtualMuseum' application is Python.

## 3. Page Design

The 'VirtualMuseum' web application will consist of the following seven pages:

### 1. Dashboard Page
- **Page Title**: Museum Dashboard
- **Overview**: The main hub displaying overview of exhibitions, artifacts, and navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: exhibition-summary** - Type: Div - Summary showing total exhibitions, active exhibitions count.
  - **ID: artifact-catalog-button** - Type: Button - Button to navigate to artifact catalog page.
  - **ID: exhibitions-button** - Type: Button - Button to navigate to exhibitions page.
  - **ID: visitor-tickets-button** - Type: Button - Button to navigate to visitor tickets page.
  - **ID: virtual-events-button** - Type: Button - Button to navigate to virtual events page.
  - **ID: audio-guides-button** - Type: Button - Button to navigate to audio guides page.

### 2. Artifact Catalog Page
- **Page Title**: Artifact Catalog
- **Overview**: A page displaying all artifacts with search and filter capabilities.
- **Elements**:
  - **ID: artifact-catalog-page** - Type: Div - Container for the artifact catalog page.
  - **ID: artifact-table** - Type: Table - Table displaying artifacts with ID, name, period, origin, exhibition, and actions.
  - **ID: search-artifact** - Type: Input - Field to search artifacts by name or ID.
  - **ID: apply-artifact-filter** - Type: Button - Button to apply filters.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Exhibitions Page
- **Page Title**: Exhibitions
- **Overview**: A page displaying all exhibitions with details and status.
- **Elements**:
  - **ID: exhibitions-page** - Type: Div - Container for the exhibitions page.
  - **ID: exhibition-list** - Type: Table - Table displaying all exhibitions with title, type, dates, gallery, and status.
  - **ID: filter-exhibition-type** - Type: Dropdown - Dropdown to filter by exhibition type (Permanent, Temporary, Virtual).
  - **ID: apply-exhibition-filter** - Type: Button - Button to apply exhibition filter.
  - **ID: view-exhibition-button-{exhibition_id}** - Type: Button - Button to view exhibition details (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Exhibition Details Page
- **Page Title**: Exhibition Details
- **Overview**: A detailed view of a specific exhibition with its artifacts.
- **Elements**:
  - **ID: exhibition-details-page** - Type: Div - Container for the exhibition details page.
  - **ID: exhibition-title** - Type: H1 - Title of the exhibition.
  - **ID: exhibition-description** - Type: Div - Description of the exhibition.
  - **ID: exhibition-dates** - Type: Div - Start and end dates of the exhibition.
  - **ID: exhibition-artifacts** - Type: Table - Table displaying artifacts in this exhibition.
  - **ID: back-to-exhibitions** - Type: Button - Button to navigate back to exhibitions list.

### 5. Visitor Tickets Page
- **Page Title**: Visitor Tickets
- **Overview**: A page for visitors to purchase tickets and view ticket sales.
- **Elements**:
  - **ID: visitor-tickets-page** - Type: Div - Container for the visitor tickets page.
  - **ID: ticket-type** - Type: Dropdown - Dropdown to select ticket type (Standard, Student, Senior, Family, VIP).
  - **ID: number-of-tickets** - Type: Input (number) - Field to input number of tickets.
  - **ID: purchase-ticket-button** - Type: Button - Button to purchase tickets.
  - **ID: my-tickets-table** - Type: Table - Table displaying user's purchased tickets.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Virtual Events Page
- **Page Title**: Virtual Events
- **Overview**: A page to view and manage virtual museum events like webinars and artist talks.
- **Elements**:
  - **ID: virtual-events-page** - Type: Div - Container for the virtual events page.
  - **ID: event-list** - Type: Table - Table displaying all events with title, date, time, type, and registration status.
  - **ID: register-event-button-{event_id}** - Type: Button - Button to register for an event (each row has this button).
  - **ID: cancel-registration-button-{registration_id}** - Type: Button - Button to cancel registration (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. Audio Guides Page
- **Page Title**: Audio Guides
- **Overview**: A page to browse and access audio guides for exhibits.
- **Elements**:
  - **ID: audio-guides-page** - Type: Div - Container for the audio guides page.
  - **ID: audio-guide-list** - Type: Table - Table displaying all audio guides with exhibit number, title, language, and duration.
  - **ID: filter-language** - Type: Dropdown - Dropdown to filter by language (English, Spanish, French).
  - **ID: apply-language-filter** - Type: Button - Button to apply language filter.
  - **ID: play-guide-button-{guide_id}** - Type: Button - Button to play audio guide (each row has this button).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'VirtualMuseum' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Authentication Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username
  ```
- **Example Data**:
  ```
  curator_john
  visitor_mary
  curator_sarah
  ```

### 2. Gallery Data
- **File Name**: `galleries.txt`
- **Data Format**:
  ```
  gallery_id|gallery_name|floor|capacity|theme|status
  ```
- **Example Data**:
  ```
  1|Ancient Civilizations Hall|1|50|Ancient|Open
  2|Modern Art Wing|2|30|Modern|Open
  3|Science Discovery Center|3|40|Science|Renovation
  ```

### 3. Exhibition Data
- **File Name**: `exhibitions.txt`
- **Data Format**:
  ```
  exhibition_id|title|description|gallery_id|exhibition_type|start_date|end_date|curator_name|created_by
  ```
- **Example Data**:
  ```
  1|Egyptian Treasures|Ancient artifacts from Egypt|1|Permanent|2024-01-01|2025-12-31|Dr. Smith|curator_john
  2|Pop Art Revolution|Contemporary pop art collection|2|Temporary|2024-11-01|2024-12-31|Lisa Chen|curator_sarah
  3|Virtual Space Exploration|Online space exhibition|2|Virtual|2024-10-01|2025-03-31|Mark Johnson|curator_john
  ```

### 4. Artifact Data
- **File Name**: `artifacts.txt`
- **Data Format**:
  ```
  artifact_id|artifact_name|period|origin|description|exhibition_id|storage_location|acquisition_date|added_by
  ```
- **Example Data**:
  ```
  1|Golden Mask of Tutankhamun|Ancient|Egypt|Famous golden funeral mask|1|A-101|2020-05-15|curator_john
  2|Warhol Soup Cans|Contemporary|USA|Iconic pop art piece|2|B-205|2023-08-20|curator_sarah
  3|Roman Amphora|Ancient|Italy|Ancient storage vessel|1|A-103|2019-11-10|curator_john
  ```

### 5. Audio Guide Data
- **File Name**: `audioguides.txt`
- **Data Format**:
  ```
  guide_id|exhibit_number|title|language|duration|script|narrator|created_by
  ```
- **Example Data**:
  ```
  1|101|Introduction to Egyptian Art|English|5|Welcome to the Egyptian exhibition...|James Brown|curator_john
  2|101|Introducción al Arte Egipcio|Spanish|5|Bienvenido a la exhibición egipcia...|Maria Garcia|curator_john
  3|205|Pop Art Explained|English|7|Pop art emerged in the 1950s...|Sarah Williams|curator_sarah
  ```

### 6. Ticket Data
- **File Name**: `tickets.txt`
- **Data Format**:
  ```
  ticket_id|username|ticket_type|visit_date|visit_time|number_of_tickets|price|visitor_name|visitor_email|purchase_date
  ```
- **Example Data**:
  ```
  1|visitor_mary|Standard|2024-11-25|11:00 AM|2|30|Mary Johnson|mary@email.com|2024-11-20
  2|visitor_mary|VIP|2024-12-01|1:00 PM|1|50|Mary Johnson|mary@email.com|2024-11-20
  3|visitor_tom|Student|2024-11-22|9:00 AM|1|10|Tom Lee|tom@email.com|2024-11-18
  ```

### 7. Virtual Event Data
- **File Name**: `events.txt`
- **Data Format**:
  ```
  event_id|title|date|time|event_type|speaker|capacity|description|created_by
  ```
- **Example Data**:
  ```
  1|Ancient Egypt Webinar|2024-12-05|2:00 PM|Webinar|Dr. Smith|100|Deep dive into Egyptian culture|curator_john
  2|Meet the Artist: Pop Art|2024-11-30|6:00 PM|Artist Talk|Andy Williams|50|Discussion with contemporary artist|curator_sarah
  3|Virtual Museum Tour|2024-12-10|10:00 AM|Virtual Tour|Lisa Chen|200|Guided tour of entire museum|curator_john
  ```

### 8. Event Registration Data
- **File Name**: `event_registrations.txt`
- **Data Format**:
  ```
  registration_id|event_id|username|registration_date
  ```
- **Example Data**:
  ```
  1|1|visitor_mary|2024-11-20
  2|2|visitor_mary|2024-11-21
  3|1|visitor_tom|2024-11-19
  ```

### 9. Collection Log Data
- **File Name**: `collection_logs.txt`
- **Data Format**:
  ```
  log_id|artifact_id|activity_type|date|notes|condition|curator
  ```
- **Example Data**:
  ```
  1|1|Inspection|2024-11-15|Routine quarterly inspection|Excellent|curator_john
  2|1|Cleaning|2024-11-16|Professional cleaning performed|Excellent|curator_john
  3|2|Photography|2024-10-20|High-resolution images taken|Good|curator_sarah
  4|3|Restoration|2024-09-10|Minor crack repair completed|Good|curator_john
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
            """You are a Web Application Designer with expertise in comprehensive UI/UX and data architecture for Python web applications.

Your goal is to independently design a complete web application structure for the 'VirtualMuseum' app, producing a design candidate file with all implementation-relevant details.

Task Details:
- Read user_task_description carefully to understand app requirements.
- Design all seven pages including routes, exact page titles, element IDs, and navigation flows.
- Specify data file usage, formats, and key UI components as required.
- Write your complete design specification into design_candidate_a.md without access to other designs.

Design Requirements:
1. Define clear and consistent routes for each page; ensure the root route leads to the Dashboard page.
2. Specify exact UI element IDs for each page (static and dynamic as applicable).
3. Map navigation buttons/links to routes with route names for integration.
4. Detail local data storage files, their formats, and key fields relevant to the app's functionality.
5. Adhere strictly to user requirements regarding pages, data, and functionality.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output design_candidate_a.md.
- Provide complete, precise, and unambiguous specifications so downstream developers can implement independently.
- Focus on delivering a standalone design candidate representing the entire app structure and data details accurately.

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Designer specializing in detailed UI and data design for Python-based museum management applications.

Your goal is to independently create an alternative but complete design specification for the 'VirtualMuseum' app, capturing all required pages, data formats, and navigation flows.

Task Details:
- Thoroughly analyze user_task_description to capture the scope and requirements.
- Design every page route with precise page titles, element IDs, and user interface components.
- Specify navigation button mappings to routes and data files usage with format details.
- Write your full design candidate into design_candidate_b.md independently, without access to other candidates.

Design Requirements:
1. Include consistent naming conventions for routes and UI elements.
2. Ensure navigation allows starting from the Dashboard and accessing all features.
3. Clearly specify all data storage files in 'data' directory with field formats and examples.
4. Cover all seven pages comprehensively with detailed UI and interaction elements.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save your comprehensive design_candidate_b.md.
- Ensure the design candidate is clear and complete for direct implementation guidance.
- Maintain independence in design and avoid reliance on other candidates’ outputs.

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Integration Specialist skilled in merging multiple independent web application designs into a single coherent specification.

Your goal is to review design_candidate_a.md and design_candidate_b.md for the 'VirtualMuseum' app, resolve any conflicts, omissions, or inconsistencies, and produce a unified, complete design_spec.md suitable for implementation.

Task Details:
- Read user_task_description as the authoritative source of requirements.
- Analyze both design_candidate_a.md and design_candidate_b.md to identify overlaps and gaps.
- Merge designs ensuring coverage of all seven pages, starting at the Dashboard, with precise page element IDs and navigation flows.
- Verify data storage designs match the specified pipe-delimited text files and their example data.
- Produce a merged design_spec.md that provides a consistent, unambiguous implementation contract.

Merging Guidelines:
1. Harmonize conflicting route naming and UI element IDs to a consistent scheme.
2. Combine best design components from both candidates to ensure completeness and clarity.
3. Maintain strict adherence to the data storage formats and examples as per requirements.
4. Ensure the final design enables independent backend/frontend development without ambiguity.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output a single, comprehensive design_spec.md.
- The merged specification must fully encompass user requirements and merge candidates without information loss.
- Provide a document that ImplementationEngineerA can rely on for development without further clarifications.
- Maintain all exact element IDs, file names, and route patterns from inputs or harmonized consistent variants.

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Python Flask Developer specializing in comprehensive web application implementations.

Your goal is to independently develop a complete Flask web application for the 'VirtualMuseum' project with all seven specified pages, conforming strictly to page titles, element IDs, and navigation flow, using local text file data storage under the data/ directory.

Task Details:
- Read the user_task_description and design_spec.md comprehensively.
- Produce app_candidate_a.py implementing all backend routes and logic.
- Produce all related HTML template files under templates_candidate_a/ matching specified element IDs and page titles.
- Ensure navigation starts from the Dashboard page and uses button-based navigation.
- Use proper Flask routing and render_template calls exactly as specified.
- Do not reference or access ImplementationEngineerB's outputs.

Implementation Requirements:
1. **Flask Application Structure**:
   - Setup Flask app with secret key.
   - All routes must correspond to the seven pages with exact function names and paths.
   - Implement data loading exclusively from pipe-delimited text files in the data/ folder.
   - Implement navigation via buttons linking to appropriate routes.
   - Use render_template() with correct template filenames.

2. **Templates**:
   - Follow exact page titles for both <title> and <h1> tags.
   - Include all specified element IDs exactly as provided.
   - For dynamic element IDs (e.g., view-exhibition-button-{exhibition_id}), use Jinja2 templating syntax.

3. **Data Handling**:
   - Parse all data files as pipe-delimited without headers.
   - Ensure field order and names match data formats precisely.
   - Handle file reading errors safely.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app_candidate_a.py and all template files under templates_candidate_a/.
- Adhere strictly to all specifications in the user task and design_spec.
- Do not add extra routes, pages, or navigation elements.
- Do not access outputs from other agents.

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Python Flask Developer skilled in building full-featured web applications with modular templates.

Your goal is to independently create a fully functional Flask app called 'VirtualMuseum' implementing all seven specified pages, using exact page titles, element IDs, and button-based navigation starting from the Dashboard. Data must be read from local text files under the data/ directory.

Task Details:
- Analyze user_task_description and design_spec.md thoroughly.
- Develop app_candidate_b.py implementing the backend with all necessary Flask routes.
- Implement corresponding templates under templates_candidate_b/ with exact HTML element IDs and titles.
- Navigation must start from Dashboard and be implemented with buttons directing to proper routes.
- Do not incorporate or access ImplementationEngineerA's outputs.

Implementation Requirements:
1. **Backend Implementation**:
   - Set up Flask application with proper configuration.
   - All routes must match the user requirements and design spec.
   - Data loading from pipe-delimited text files, matching exact field order.
   - Ensure render_template references correct template filenames.

2. **Frontend Templates**:
   - All template files should implement exact element IDs as specified.
   - Page titles must be consistent across <title> and <h1> tags.
   - Use Jinja2 templating syntax for dynamic elements (e.g., button IDs).

3. **Navigation**:
   - Button-based navigation between pages.
   - Route names and template names must match design spec exactly.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to write app_candidate_b.py and all templates under templates_candidate_b/.
- Strictly follow all specifications from the user task and design_spec.
- Avoid referencing or merging with other implementations before merging phase.

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Specialist experienced in merging parallel Flask web application implementations.

Your goal is to compare, resolve conflicts, and merge two complete Flask web app bundles for the 'VirtualMuseum' project—app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html—into final cohesive app.py and templates/*.html files, fully consistent with the user requirements and design_spec.md.

Task Details:
- Read user_task_description, design_spec.md, and all candidate implementations from ImplementationEngineerA and ImplementationEngineerB.
- Identify and reconcile differences in Flask routes, function names, template usage, and navigation flows.
- Resolve conflicts in templates including element IDs, page titles, and button-based navigation.
- Ensure merged app.py is a complete, runnable Flask application covering all seven pages.
- Ensure merged templates/*.html conform exactly to specifications, using consistent element IDs and page titles.

Merge Guidelines:
1. **Backend**:
   - Validate all routes from both candidates; include all specified routes only once.
   - Harmonize data loading and utility functions.
   - Choose clear and consistent function and variable names.
   - Ensure root route starts at Dashboard.

2. **Templates**:
   - Combine templates for identical pages, preserving all required element IDs from both candidates.
   - Use consistent Jinja2 syntax.
   - Ensure navigation buttons point correctly to routes.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final merged app.py and templates to templates/ directory.
- The final merged outputs must be consistent, complete, and ready for further validation.
- No references or code dependencies on candidate files.
- Maintain strict adherence to the user requirements and design_spec.

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web applications and frontend HTML template validation.

Your goal is to independently validate the correctness, syntax, runtime behavior, and user requirement compliance of the Flask backend (app.py) and all HTML templates (templates/*.html) for a multi-page web application.

Task Details:
- Read user_task_description, design_spec.md, app.py, and templates/*.html files from CONTEXT
- Validate ALL seven pages including routes, button presence, page titles, element IDs, navigation flow starting from Dashboard page
- Ensure local data files conform exactly to pipe-delimited field order and format from design_spec.md
- Produce a detailed validation report named validation_a.md with identified issues or confirm full compliance
- Do NOT read or access validation_b.md to maintain independent validation

Validation Requirements:
1. Syntax & Runtime Checks:
   - Use validate_python_file tool on app.py for syntax and runtime errors
   - Spot runtime error possibilities in all route handlers and template rendering

2. Functional Verification:
   - Confirm presence and correctness of all routes for seven pages as specified
   - Validate all required button IDs, element IDs, and pages titles per design_spec.md and user requirements
   - Confirm navigation buttons correctly link to intended pages using specified route functions
   - Check that root route redirects to Dashboard page

3. Data Storage Validation:
   - Verify all local text data files use pipe-delimited format as per specifications
   - Check data file field orders against design_spec.md exactly
   - Confirm that app.py accesses and processes these data files accordingly

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools as needed for checks
- Use write_text_file tool to save detailed validation report as validation_a.md
- Validation report must be thorough, clearly indicate any discrepancies or full compliance
- Input/output files must be handled exactly as specified, no deviations
- Do NOT reference or include any contents from validation_b.md

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in verifying backend and frontend implementations of Flask web apps.

Your goal is to independently verify the implementation correctness of app.py and templates/*.html ensuring full alignment with user requirements and design specifications.

Task Details:
- Read user_task_description, design_spec.md, app.py, and templates/*.html files from CONTEXT
- Verify all seven pages and their defined UI elements, including buttons and navigation controls starting from Dashboard
- Confirm page titles exactly match specifications
- Validate local data file adherence to required formats and correct usage in app.py
- Produce a comprehensive validation report named validation_b.md describing conformance and discrepancies found
- Do NOT read or access validation_a.md to maintain independence

Verification Steps:
1. User Interface and Navigation:
   - Check all buttons and element IDs exist as per requirements on respective pages
   - Confirm navigation flow is consistent starting at Dashboard, buttons linking to correct pages
   - Validate proper page title presence in templates

2. Backend Functionality:
   - Confirm app.py routes exist and serve expected pages
   - Validate expected usage of data files as per design_spec.md in backend logic

3. Data Compliance:
   - Ensure text data files are correctly structured pipe-delimited files matching field orders in design_spec.md
   - Confirm app.py interacts with data files correctly

CRITICAL SUCCESS CRITERIA:
- Use validate_python_file and execute_python_code for syntax and runtime validation
- Write complete detailed validation report as validation_b.md using write_text_file tool
- Reports must avoid referencing validation_a.md
- Input and output artifacts must not be modified or extended beyond specifications

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in merging validation feedback and applying repairs to Flask backend and frontend codebases.

Your goal is to analyze independent validation reports from ValidationEngineerA and ValidationEngineerB, consolidate their repair suggestions, and apply necessary corrections to app.py and templates/*.html to fully comply with the design specification and user requirements without regressions.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md from CONTEXT
- Compare and reconcile repairs suggested in both validation reports
- Prioritize correctness, completeness, and full functionality adherence
- Apply all valid fixes to source code files app.py and templates/*.html preserving structural integrity and compliance
- Produce final corrected app.py and templates/*.html files as output artifacts

Repair Process Guidelines:
1. Validation Report Analysis:
   - Extract and unify repair suggestions from validation_a.md and validation_b.md
   - Identify consistent issues and prioritize critical fixes

2. Implementation of Repairs:
   - Apply corrections to backend logic, route handling, and data file access in app.py
   - Fix template HTML to ensure presence of required element IDs, buttons, and page titles per design_spec.md
   - Test locally to confirm no syntax or runtime regressions

3. Final Output Preparation:
   - Save updated app.py and all template files exactly as specified
   - Ensure compatibility with merged design_spec.md and complete user task compliance

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and templates/*.html files
- Preserve the exact file structure and naming conventions
- Ensure all fixes maintain alignment with design_spec.md and user requirements
- Validate no conflicts or regressions introduced during repair merging
- Produce clean, maintainable, and fully compliant final deliverables

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
        ("DesignMerger", """Check design_candidate_a.md for completeness, correctness, and adherence to user requirements including all page routes, UI elements, "
                "navigation flow, and data usage details before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for completeness, correctness, and adherence to user requirements including all page routes, UI elements, "
                "navigation flow, and data usage details before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify design_spec.md provides a coherent and complete implementation contract covering all required pages, navigation, element IDs, "
                "and data storage format to guide implementation.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Check app_candidate_a.py and templates_candidate_a/*.html for adherence to design_spec.md, exact routes, titles, element IDs, navigation flow, "
                "data file usage, and visibility of requested buttons and messages.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Check app_candidate_b.py and templates_candidate_b/*.html independently for compliance with design_spec.md and user requirements covering all "
                "pages, exact element details, routing, and local text file data handling.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify that the merged app.py and templates/*.html are a coherent, complete, and feasible Flask web application bundle consistent with design_spec.md "
                "and user requirements, ready for validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Verify validation_a.md for thorough testing coverage, correctness of issue identification, and alignment with user requirements before merging repairs.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Verify validation_b.md for completeness, accurate issue identification related to UI, navigation, and data files before merging.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm that the repaired final app.py and templates/*.html remain consistent with the merged design_spec.md and cover all user requirements.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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

    # Parallel design candidate creation
    await asyncio.gather(
        execute(DesignAnalystA, "Create complete design candidate for VirtualMuseum app, output design_candidate_a.md"),
        execute(DesignAnalystB, "Create complete alternative design candidate for VirtualMuseum app, output design_candidate_b.md")
    )

    # Read both design candidates for merging
    design_candidate_a, design_candidate_b = "", ""
    try: design_candidate_a = open("design_candidate_a.md").read()
    except: pass
    try: design_candidate_b = open("design_candidate_b.md").read()
    except: pass

    # Merge design candidates into coherent design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA Candidate ===\n{design_candidate_a}\n\n"
                  f"=== DesignAnalystB Candidate ===\n{design_candidate_b}")
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

    # Parallel implementations by EngineerA and EngineerB
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Develop complete 'VirtualMuseum' Flask app as app_candidate_a.py and templates under templates_candidate_a/ "
                "following design_spec.md and user requirements strictly, no referencing EngineerB."),
        execute(ImplementationEngineerB,
                "Develop complete 'VirtualMuseum' Flask app as app_candidate_b.py and templates under templates_candidate_b/ "
                "following design_spec.md and user requirements strictly, no referencing EngineerA.")
    )

    # Read candidate outputs for merging
    candidate_a_app, candidate_b_app = "", ""
    candidate_a_templates, candidate_b_templates = "", ""
    try:
        candidate_a_app = open("app_candidate_a.py").read()
    except:
        pass
    try:
        candidate_b_app = open("app_candidate_b.py").read()
    except:
        pass
    # Template directories' merging content would be read inside the agent, so just placeholder here
    # But we need to try reading at least one representative file or note empty,
    # since filenames are wildcard, we skip direct reading here, rely on merging agent textual inputs.

    # Merge both candidates into final app.py and templates
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{candidate_a_app}\n\n"
                  f"=== app_candidate_b.py ===\n{candidate_b_app}\n\n"
                  f"=== templates_candidate_a content ===\n"
                  f"(Read templates_candidate_a/*.html files contents and include here accordingly - placeholder)\n\n"
                  f"=== templates_candidate_b content ===\n"
                  f"(Read templates_candidate_b/*.html files contents and include here accordingly - placeholder)")
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    # Build agents
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
        timeout_threshold=450,
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
                "Independently validate app.py and templates/*.html for correctness, syntax, runtime, compliance with user requirements. "
                "Produce validation_a.md with detailed issues or confirmation of full compliance."),
        execute(ValidationEngineerB,
                "Independently validate app.py and templates/*.html for correctness, syntax, runtime, compliance with user requirements. "
                "Produce validation_b.md with detailed issues or confirmation of full compliance.")
    )

    # Read validation reports for merger
    val_a_content, val_b_content = "", ""
    try:
        val_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        val_b_content = open("validation_b.md").read()
    except:
        pass

    # RepairMerger reconciles validation reports and applies repairs
    await execute(
        RepairMerger,
        f"Consolidate and merge repair suggestions from validation_a.md and validation_b.md, "
        f"apply necessary corrections to app.py and templates/*.html to produce final compliant outputs. "
        f"Validation reports content:\n"
        f"=== validation_a.md ===\n{val_a_content}\n\n"
        f"=== validation_b.md ===\n{val_b_content}"
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
