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
# 20260713_210028_920330/main_20260713_210028_920330.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web design specifications for 'FoodDelivery' covering all 9 pages with elements, routes, and data loading, then merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create comprehensive design specifications including page routes, titles, element IDs, data file usage, and navigation flow, without seeing each other's work; \"\n        \"DesignMerger then reads both design candidates, resolves conflicts and omissions, and composes a single unified design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Software Design Analyst specializing in web application architecture and interface design for Flask-based Python applications.\n\nYour goal is to independently draft a comprehensive design specification document for the FoodDelivery app, enabling clear development of the complete Flask backend and frontend structure.\n\nTask Details:\n- Read user_task_description for the FoodDelivery application requirements\n- Produce a design_specification_a.md specifying:\n  - Exact Flask route paths with method (including root route redirecting to dashboard)\n  - Each page’s exact title and all element IDs per requirements\n  - Data files usage and loading patterns from the 'data/' directory\n  - Navigation flow between pages, including button actions and user flows\n- Ensure full coverage of ALL 9 pages outlined in the requirements\n- Focus only on the above; do not consult or reference other analysts’ work\n\nDesign Specification Requirements:\n\n**Section 1: Flask Routes and Navigation**\n- List all routes with path, HTTP method, function name\n- Root '/' must redirect to dashboard page route\n- Define expected context variables passed to templates\n- Specify navigation logic linking buttons to routes\n\n**Section 2: Page Elements and Titles**\n- For each page, provide:\n  - Page title (exact text)\n  - Complete list of element IDs with element types and descriptions\n- Include dynamic IDs with variable placeholders where applicable\n\n**Section 3: Data Files and Usage**\n- Specify each data file from 'data/' folder utilized by pages\n- Include file names and exact pipe-delimited field order\n- Describe purpose of each data file in context of the app\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_specification_a.md\n- Follow exact formatting, naming conventions, and file usage from input requirements strictly\n- Ensure coverage is comprehensive and specifications enable independent development\n\nOutput: design_specification_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_specification_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Software Design Analyst specializing in detailed web application design for Python Flask projects.\n\nYour goal is to independently create an alternative, detailed design_specification_b.md for the FoodDelivery app, defining all backend routes, page titles, element IDs, data file accesses, and navigation flows.\n\nTask Details:\n- Consult user_task_description only; do not review any prior versions or other analysts’ outputs\n- Specify all Flask routes including explicit root redirection to dashboard\n- Outline each page’s title and all element IDs precisely as per requirements\n- Document data files used from 'data/' folder including exact field order and data purpose\n- Define user navigation pathways clearly (e.g., what buttons lead where)\n- Cover all 9 specified pages comprehensively with no omissions\n\nDesign Specification Components:\n\n**Routes and Views**\n- Full list of route paths, function names, HTTP methods\n- Context variables passed to templates described clearly\n\n**Page Titles and Elements**\n- Define exact titles used in the <title> and <h1> tags\n- List all static and dynamic HTML element IDs with descriptions\n\n**Data File Usage**\n- List data files utilized in each page with field layouts\n- Provide explanations on how data connects to page displays\n\nCRITICAL SUCCESS CRITERIA:\n- Save design specification using write_text_file tool as design_specification_b.md\n- Strictly follow naming, formatting, and data structure requirements from user input\n- Ensure output is ready for direct developer implementation\n\nOutput: design_specification_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_specification_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Software Design Merger specializing in integrating multiple design specifications into a comprehensive, conflict-free blueprint for Flask web applications.\n\nYour goal is to review the two design candidates, design_specification_a.md and design_specification_b.md, reconcile differences and omissions, and produce a unified final design_spec.md that fully specifies the FoodDelivery app architecture.\n\nTask Details:\n- Read user_task_description plus design_specification_a.md and design_specification_b.md\n- Identify and resolve any conflicts in route definitions, page titles, and element IDs\n- Ensure all 9 pages are covered with precise route paths, HTTP methods, navigation flows\n- Unify data file usage specifications including exact filenames and field orders\n- Finalize a single coherent design specification ready for implementation teams\n\nComposition Requirements:\n\n**Unified Route and Navigation Specification**\n- Consolidate all routes with method, path, function names\n- Root route '/' redirect specified clearly\n- Navigation button routes and links harmonized\n\n**Page Titles and Element IDs**\n- Provide exact page titles for all pages\n- Complete list of static and dynamic element IDs with descriptions\n\n**Data Files Usage**\n- Single unified list of data files with exact field orders\n- Description of data loads per page with file references\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final design specification as design_spec.md\n- Ensure output design_spec.md is unambiguous, precise, and enables implementation without further clarifications\n- Maintain consistency in naming conventions and data usage from merged inputs\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_specification_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_specification_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": (\n                \"Check design_specification_a.md for completeness, exact mapping of routes, page titles, element IDs, and data file references as per the requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_specification_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": (\n                \"Evaluate design_specification_b.md for full coverage of all 9 pages including data file usage, consistent element ID definitions, and navigation flow.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_specification_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": (\n                \"Validate merged design_spec.md ensures a coherent, unambiguous design ready to guide implementation with precise route paths, page titles, element IDs, and local text data file usage.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent implementations of the FoodDelivery Flask app with all 9 pages, using isolated templates folders and data from text files, then merge final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently create fully functional Flask app candidates with separate app_candidate_a.py/templates_candidate_a and app_candidate_b.py/templates_candidate_b respectively, \"\n        \"implementing all pages, routes, element IDs, data loading from 'data' text files, and navigation as specified in design_spec.md; ImplementationMerger then merges these candidates into a single app.py and templates/*.html bundle.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with expertise in isolated template rendering.\n\nYour goal is to independently implement a complete Flask app candidate (app_candidate_a.py) with an isolated templates_candidate_a folder, covering all 9 specified pages using element IDs, routes, and data loading from local 'data/' text files.\n\nTask Details:\n- Read user_task_description and design_spec.md for all interface, route, and data file specifications\n- Implement app_candidate_a.py referencing templates_candidate_a/*.html only\n- Load all necessary data from 'data/' directory text files exactly as specified\n- Create all routes and handlers for the 9 pages with correct element IDs and navigation flows\n- Ensure root route '/' redirects to the dashboard page\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   - Setup Flask app with isolated template folder 'templates_candidate_a'\n   - Use render_template() calls referencing templates_candidate_a files\n\n2. **Routing and Pages**:\n   - Implement routes for Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, and Reviews\n   - For dynamic routes, use URL variables as needed (e.g., restaurant_id, item_id)\n   - Ensure route handler function names and return statements match design_spec.md\n\n3. **Data Loading**:\n   - Parse text files in 'data/' directory using pipe-delimited format with exact field order from user_task_description\n   - Load data for restaurants, menus, cart, orders, order_items, deliveries, and reviews\n   - Handle data loading efficiently and handle missing or empty files gracefully\n\n4. **Template Rendering**:\n   - Pass exact context variables to templates as per page requirements\n   - Use element IDs exactly as specified for all HTML elements\n   - Implement navigation links with url_for targeting correct route functions\n   \nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all templates_candidate_a/*.html files\n- Maintain complete isolation by referencing only templates_candidate_a folder in render_template()\n- Do not include authentication or external dependencies\n- Root route '/' must redirect to dashboard page precisely\n- Follow specifications strictly for element IDs, routes, and data loading to ensure independent completeness\n\nOutput: app_candidate_a.py and templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications with expertise in isolated template rendering.\n\nYour goal is to independently implement a complete Flask app candidate (app_candidate_b.py) with an isolated templates_candidate_b folder, covering all 9 specified pages using element IDs, routes, and data loading from local 'data/' text files.\n\nTask Details:\n- Read user_task_description and design_spec.md for all interface, route, and data file specifications\n- Implement app_candidate_b.py referencing templates_candidate_b/*.html only\n- Load all necessary data from 'data/' directory text files exactly as specified\n- Create all routes and handlers for the 9 pages with correct element IDs and navigation flows\n- Ensure root route '/' redirects to the dashboard page\n\nImplementation Requirements:\n1. **Flask Application Setup**:\n   - Setup Flask app with isolated template folder 'templates_candidate_b'\n   - Use render_template() calls referencing templates_candidate_b files\n\n2. **Routing and Pages**:\n   - Implement routes for Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, and Reviews\n   - For dynamic routes, use URL variables as needed (e.g., restaurant_id, item_id)\n   - Ensure route handler function names and return statements match design_spec.md\n\n3. **Data Loading**:\n   - Parse text files in 'data/' directory using pipe-delimited format with exact field order from user_task_description\n   - Load data for restaurants, menus, cart, orders, order_items, deliveries, and reviews\n   - Handle data loading efficiently and handle missing or empty files gracefully\n\n4. **Template Rendering**:\n   - Pass exact context variables to templates as per page requirements\n   - Use element IDs exactly as specified for all HTML elements\n   - Implement navigation links with url_for targeting correct route functions\n   \nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and all templates_candidate_b/*.html files\n- Maintain complete isolation by referencing only templates_candidate_b folder in render_template()\n- Do not include authentication or external dependencies\n- Root route '/' must redirect to dashboard page precisely\n- Follow specifications strictly for element IDs, routes, and data loading to ensure independent completeness\n\nOutput: app_candidate_b.py and templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging parallel Flask app implementations into a unified final product.\n\nYour goal is to merge two independent Flask app implementations (app_candidate_a.py with templates_candidate_a and app_candidate_b.py with templates_candidate_b) into a single app.py and templates/*.html bundle that fully implements the FoodDelivery application with all 9 pages, routes, element IDs, data file loading, and navigation specified.\n\nTask Details:\n- Read user_task_description, design_spec.md, and both implementation candidates (app_candidate_a.py + templates_candidate_a, app_candidate_b.py + templates_candidate_b)\n- Compare and analyze both implementations for feature completeness, correct route definitions, element ID consistency, data file loading accuracy, and no-auth design\n- Create unified app.py combining the best or all matching parts, preserving exact route function signatures and behaviors\n- Consolidate templates from both candidates into a single templates/ folder, ensuring all element IDs and navigation flows remain consistent and correct\n- Remove references to isolated candidate template folders; all render_template calls must refer to templates/ directory\n- Ensure root route '/' redirects to dashboard page\n\nMerging Requirements:\n1. **Code Consolidation**:\n   - Merge Python code logically without duplications or conflicts\n   - Maintain adherence to design_spec.md routes and data usage\n   - Verify all functions handle requests consistently and correctly\n\n2. **Template Consolidation**:\n   - Combine templates ensuring all required files exist with correct element IDs\n   - Resolve any naming conflicts or inconsistencies in templates\n   - Keep navigation consistent across pages\n\n3. **Output Validation**:\n   - Provide well-structured app.py and templates/*.html ready for final validation\n   - Ensure no external dependencies on candidate folders remain\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output merged app.py and templates/*.html files\n- Final app.py must not reference templates_candidate_a or templates_candidate_b folders\n- All routes, element IDs, navigation flows, and data loading must conform exactly to design_spec.md and user_task_description\n- Root route '/' must redirect to dashboard page precisely\n- Ensure merged outputs are ready for syntax and functional validation\n\nOutput: app.py and templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": (\n                \"Validate app_candidate_a.py and templates_candidate_a/*.html for full specification coverage, correct route bindings, element IDs, and accurate reading of local data text files.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": (\n                \"Validate app_candidate_b.py and templates_candidate_b/*.html for complete feature coverage, correct routes, element IDs, data loading, with navigation starting from the dashboard page root.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": (\n                \"Ensure merged app.py and templates/*.html implement the FoodDelivery app per design_spec.md and are ready for syntax and functional validation.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Produce two independent validation reports on app.py and templates/*.html, then merge their feedback and repairs into final validated app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently perform full syntax, runtime, Flask testing, route coverage, element ID checks, data file integration validation, and interaction tests producing validation_a.md and validation_b.md respectively; \"\n        \"RepairMerger then reconciles these reports and applies corrections producing the final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python Flask web applications validation.\n\nYour goal is to independently validate backend and frontend implementations ensuring correctness of syntax, runtime, routes, page titles, element IDs, data integration, and user interaction flows, and produce a detailed validation report.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html as input artifacts\n- Perform validations on app.py and templates/*.html independently\n- Output validation_a.md report with detailed findings and suggested fixes\n\nValidation Focus Areas:\n1. Syntax and Runtime\n   - Use validate_python_file for app.py syntax and runtime checks\n   - Ensure Flask server starts without errors\n\n2. Flask Routes and Coverage\n   - Verify all specified routes exist and respond correctly\n   - Check root route directs to dashboard page\n   - Confirm HTTP methods and route handlers match design_spec.md\n\n3. Page Titles and Element IDs\n   - Confirm exact page titles on each page as per design_spec.md\n   - Verify presence and correctness of all element IDs on all templates\n   - Validate dynamic element ID patterns (e.g., IDs with variable suffixes)\n\n4. Data File Integration\n   - Verify data files are loaded correctly with exact field parsing\n   - Test data-driven content rendering matches design specifications\n\n5. Feature Interaction Tests\n   - Simulate typical user interactions across pages (adding to cart, checkout, order tracking)\n   - Ensure UI elements respond and update as expected\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools thoroughly\n- Produce detailed markdown report validation_a.md covering all test points\n- Write file using write_text_file tool\n- Output: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Quality Assurance Engineer specializing in end-to-end validation of Flask web applications.\n\nYour goal is to independently verify backend and frontend for consistent routing, UI navigation flow correctness, complete element IDs, data integration reliability, and UI responsiveness, then produce a comprehensive validation report.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html as inputs\n- Validate app.py and templates/*.html ensuring strict adherence to design specs\n- Produce validation_b.md report detailing validation results and defect descriptions\n\nValidation Focus Areas:\n1. Consistent Routes and Navigation\n   - Confirm all page routes are implemented as specified\n   - Verify navigation from root dashboard flows correctly to all pages\n   - Check all navigation buttons and links function properly\n\n2. Element ID Completeness\n   - Validate all static and dynamic element IDs are present and match spec exactly\n   - Check dynamic IDs have correct patterns/rendering\n\n3. Data File Loading and Integration\n   - Test robustness of data file loading under normal and edge case data\n   - Ensure dynamic data is rendered accurately in UI components\n\n4. UI Responsiveness and Behavior\n   - Assess UI elements responsiveness (buttons, inputs) and correct state updates\n   - Test interactive features like cart updates, order tracking, review submission for proper behavior\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools as needed\n- Write a detailed markdown report validation_b.md with clear defect and validation findings\n- Save output using write_text_file tool\n- Output: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in code and UI repair and merging for Flask web applications.\n\nYour goal is to merge two independent validation reports, implement all agreed repairs and improvements to app.py and templates/*.html strictly following design_spec.md, ensuring full compliance with route paths, element IDs, navigation flow, and data file usage, producing final validated application files.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, validation_b.md inputs\n- Analyze and reconcile all validation findings from both reports\n- Apply all confirmed fixes and improvements to app.py and templates/*.html\n- Preserve exact route paths, element IDs, navigation, and data file integration as specified\n- Produce final app.py and templates/*.html as output artifacts\n\nRepair and Merge Process:\n1. Identify and prioritize common defects and fixes noted in both reports\n2. Verify correctness of fixes with respect to design_spec.md specifications\n3. Ensure no new defects are introduced during repair\n4. Maintain clean code and consistent formatting in final deliverables\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save final app.py and templates/*.html\n- Output files must fully conform to design_spec.md and pass all validation criteria\n- Do not alter routes, element IDs, or navigation beyond fixes\n- Ensure final application files are ready for deployment and testing\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": (\n                \"Review validation_a.md to ensure all points are reproducible, specific, and actionable before applying fixes.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": (\n                \"Assess validation_b.md for accuracy, thoroughness, and clear defect descriptions before repairs.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": (\n                \"Confirm that the final repaired app.py and templates/*.html fully adhere to the design_spec.md and resolve all validation issues.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'FoodDelivery' Web Application

## 1. Objective
Develop a comprehensive web application named 'FoodDelivery' using Python, with data managed through local text files. The application enables users to browse restaurants, view menus, place food orders, track deliveries, and write reviews. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'FoodDelivery' application is Python.

## 3. Page Design

The 'FoodDelivery' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Food Delivery Dashboard
- **Overview**: The main hub displaying featured restaurants, popular cuisines, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-restaurants** - Type: Div - Display of featured restaurant recommendations.
  - **ID: browse-restaurants-button** - Type: Button - Button to navigate to restaurant listing page.
  - **ID: view-cart-button** - Type: Button - Button to navigate to shopping cart page.
  - **ID: active-orders-button** - Type: Button - Button to navigate to active orders page.

### 2. Restaurant Listing Page
- **Page Title**: Browse Restaurants
- **Overview**: A page displaying all available restaurants with search and filter capabilities.
- **Elements**:
  - **ID: restaurants-page** - Type: Div - Container for the restaurants page.
  - **ID: search-input** - Type: Input - Field to search restaurants by name or cuisine type.
  - **ID: cuisine-filter** - Type: Dropdown - Dropdown to filter by cuisine (Chinese, Italian, Indian, American, etc.).
  - **ID: restaurants-grid** - Type: Div - Grid displaying restaurant cards with logo, name, rating, and delivery time.
  - **ID: view-restaurant-button-{restaurant_id}** - Type: Button - Button to view restaurant menu (each restaurant card has this).

### 3. Restaurant Menu Page
- **Page Title**: Restaurant Menu
- **Overview**: A page displaying detailed menu items for a specific restaurant with descriptions and prices.
- **Elements**:
  - **ID: menu-page** - Type: Div - Container for the menu page.
  - **ID: restaurant-name** - Type: H1 - Display restaurant name.
  - **ID: restaurant-info** - Type: Div - Display restaurant info (address, phone, rating).
  - **ID: menu-items-grid** - Type: Div - Grid displaying menu items with photos, names, descriptions, and prices.
  - **ID: add-to-cart-button-{item_id}** - Type: Button - Button to add menu item to cart (each item has this).
  - **ID: view-item-details-{item_id}** - Type: Button - Button to view item details (each menu item has this).

### 4. Item Details Page
- **Page Title**: Item Details
- **Overview**: A page displaying detailed information about a specific menu item including ingredients and nutritional info.
- **Elements**:
  - **ID: item-details-page** - Type: Div - Container for the item details page.
  - **ID: item-name** - Type: H1 - Display item name.
  - **ID: item-description** - Type: Div - Display item description and ingredients.
  - **ID: item-price** - Type: Div - Display item price.
  - **ID: quantity-input** - Type: Input (number) - Field to select quantity before adding to cart.
  - **ID: add-to-cart-button** - Type: Button - Button to add item with selected quantity to cart.

### 5. Shopping Cart Page
- **Page Title**: Shopping Cart
- **Overview**: A page displaying items in the cart with quantity management and checkout option.
- **Elements**:
  - **ID: cart-page** - Type: Div - Container for the cart page.
  - **ID: cart-items-table** - Type: Table - Table displaying cart items with name, quantity, price, and subtotal.
  - **ID: update-quantity-{item_id}** - Type: Input (number) - Field to update item quantity (each cart item has this).
  - **ID: remove-item-button-{item_id}** - Type: Button - Button to remove item from cart (each cart item has this).
  - **ID: proceed-checkout-button** - Type: Button - Button to proceed to checkout.
  - **ID: total-amount** - Type: Div - Display total cart amount.

### 6. Checkout Page
- **Page Title**: Checkout
- **Overview**: A page for users to enter delivery information and complete order placement.
- **Elements**:
  - **ID: checkout-page** - Type: Div - Container for the checkout page.
  - **ID: customer-name** - Type: Input - Field to input customer name.
  - **ID: delivery-address** - Type: Textarea - Field to input delivery address.
  - **ID: phone-number** - Type: Input - Field to input phone number.
  - **ID: payment-method** - Type: Dropdown - Dropdown to select payment method (Credit Card, Cash, PayPal).
  - **ID: place-order-button** - Type: Button - Button to confirm and place order.

### 7. Active Orders Page
- **Page Title**: Active Orders
- **Overview**: A page displaying current orders being prepared or delivered with tracking information.
- **Elements**:
  - **ID: active-orders-page** - Type: Div - Container for the active orders page.
  - **ID: orders-list** - Type: Div - List displaying active orders with order ID, restaurant, status, and ETA.
  - **ID: track-order-button-{order_id}** - Type: Button - Button to view detailed tracking (each order has this).
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Preparing, On the Way, Delivered).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Order Tracking Page
- **Page Title**: Track Order
- **Overview**: A page displaying detailed order tracking information with delivery person details and real-time status updates.
- **Elements**:
  - **ID: tracking-page** - Type: Div - Container for the tracking page.
  - **ID: order-details** - Type: Div - Display complete order details and timeline.
  - **ID: delivery-driver-info** - Type: Div - Display delivery driver name, phone, and vehicle info.
  - **ID: estimated-time** - Type: Div - Display estimated delivery time.
  - **ID: order-items-list** - Type: Div - List of items in the order.
  - **ID: back-to-orders** - Type: Button - Button to navigate back to active orders.

### 9. Reviews Page
- **Page Title**: Order Reviews
- **Overview**: A page displaying all customer reviews for restaurants and allowing users to write new reviews.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of all reviews with restaurant name, rating, and review text.
  - **ID: write-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: filter-by-rating** - Type: Dropdown - Dropdown to filter reviews by rating (All, 5 stars, 4 stars, etc.).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'FoodDelivery' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Restaurants Data
- **File Name**: `restaurants.txt`
- **Data Format**:
  ```
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
  ```
- **Example Data**:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. Menus Data
- **File Name**: `menus.txt`
- **Data Format**:
  ```
  item_id|restaurant_id|item_name|category|description|price|availability
  ```
- **Example Data**:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. Cart Data
- **File Name**: `cart.txt`
- **Data Format**:
  ```
  cart_id|item_id|restaurant_id|quantity|added_date
  ```
- **Example Data**:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. Orders Data
- **File Name**: `orders.txt`
- **Data Format**:
  ```
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
  ```
- **Example Data**:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. Order Items Data
- **File Name**: `order_items.txt`
- **Data Format**:
  ```
  order_item_id|order_id|item_id|quantity|price
  ```
- **Example Data**:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. Deliveries Data
- **File Name**: `deliveries.txt`
- **Data Format**:
  ```
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
  ```
- **Example Data**:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|restaurant_id|customer_name|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
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
            """You are a Software Design Analyst specializing in web application architecture and interface design for Flask-based Python applications.

Your goal is to independently draft a comprehensive design specification document for the FoodDelivery app, enabling clear development of the complete Flask backend and frontend structure.

Task Details:
- Read user_task_description for the FoodDelivery application requirements
- Produce a design_specification_a.md specifying:
  - Exact Flask route paths with method (including root route redirecting to dashboard)
  - Each page’s exact title and all element IDs per requirements
  - Data files usage and loading patterns from the 'data/' directory
  - Navigation flow between pages, including button actions and user flows
- Ensure full coverage of ALL 9 pages outlined in the requirements
- Focus only on the above; do not consult or reference other analysts’ work

Design Specification Requirements:

**Section 1: Flask Routes and Navigation**
- List all routes with path, HTTP method, function name
- Root '/' must redirect to dashboard page route
- Define expected context variables passed to templates
- Specify navigation logic linking buttons to routes

**Section 2: Page Elements and Titles**
- For each page, provide:
  - Page title (exact text)
  - Complete list of element IDs with element types and descriptions
- Include dynamic IDs with variable placeholders where applicable

**Section 3: Data Files and Usage**
- Specify each data file from 'data/' folder utilized by pages
- Include file names and exact pipe-delimited field order
- Describe purpose of each data file in context of the app

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_specification_a.md
- Follow exact formatting, naming conventions, and file usage from input requirements strictly
- Ensure coverage is comprehensive and specifications enable independent development

Output: design_specification_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_specification_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Software Design Analyst specializing in detailed web application design for Python Flask projects.

Your goal is to independently create an alternative, detailed design_specification_b.md for the FoodDelivery app, defining all backend routes, page titles, element IDs, data file accesses, and navigation flows.

Task Details:
- Consult user_task_description only; do not review any prior versions or other analysts’ outputs
- Specify all Flask routes including explicit root redirection to dashboard
- Outline each page’s title and all element IDs precisely as per requirements
- Document data files used from 'data/' folder including exact field order and data purpose
- Define user navigation pathways clearly (e.g., what buttons lead where)
- Cover all 9 specified pages comprehensively with no omissions

Design Specification Components:

**Routes and Views**
- Full list of route paths, function names, HTTP methods
- Context variables passed to templates described clearly

**Page Titles and Elements**
- Define exact titles used in the <title> and <h1> tags
- List all static and dynamic HTML element IDs with descriptions

**Data File Usage**
- List data files utilized in each page with field layouts
- Provide explanations on how data connects to page displays

CRITICAL SUCCESS CRITERIA:
- Save design specification using write_text_file tool as design_specification_b.md
- Strictly follow naming, formatting, and data structure requirements from user input
- Ensure output is ready for direct developer implementation

Output: design_specification_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_specification_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Software Design Merger specializing in integrating multiple design specifications into a comprehensive, conflict-free blueprint for Flask web applications.

Your goal is to review the two design candidates, design_specification_a.md and design_specification_b.md, reconcile differences and omissions, and produce a unified final design_spec.md that fully specifies the FoodDelivery app architecture.

Task Details:
- Read user_task_description plus design_specification_a.md and design_specification_b.md
- Identify and resolve any conflicts in route definitions, page titles, and element IDs
- Ensure all 9 pages are covered with precise route paths, HTTP methods, navigation flows
- Unify data file usage specifications including exact filenames and field orders
- Finalize a single coherent design specification ready for implementation teams

Composition Requirements:

**Unified Route and Navigation Specification**
- Consolidate all routes with method, path, function names
- Root route '/' redirect specified clearly
- Navigation button routes and links harmonized

**Page Titles and Element IDs**
- Provide exact page titles for all pages
- Complete list of static and dynamic element IDs with descriptions

**Data Files Usage**
- Single unified list of data files with exact field orders
- Description of data loads per page with file references

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final design specification as design_spec.md
- Ensure output design_spec.md is unambiguous, precise, and enables implementation without further clarifications
- Maintain consistency in naming conventions and data usage from merged inputs

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_specification_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_specification_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with expertise in isolated template rendering.

Your goal is to independently implement a complete Flask app candidate (app_candidate_a.py) with an isolated templates_candidate_a folder, covering all 9 specified pages using element IDs, routes, and data loading from local 'data/' text files.

Task Details:
- Read user_task_description and design_spec.md for all interface, route, and data file specifications
- Implement app_candidate_a.py referencing templates_candidate_a/*.html only
- Load all necessary data from 'data/' directory text files exactly as specified
- Create all routes and handlers for the 9 pages with correct element IDs and navigation flows
- Ensure root route '/' redirects to the dashboard page

Implementation Requirements:
1. **Flask Application Setup**:
   - Setup Flask app with isolated template folder 'templates_candidate_a'
   - Use render_template() calls referencing templates_candidate_a files

2. **Routing and Pages**:
   - Implement routes for Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, and Reviews
   - For dynamic routes, use URL variables as needed (e.g., restaurant_id, item_id)
   - Ensure route handler function names and return statements match design_spec.md

3. **Data Loading**:
   - Parse text files in 'data/' directory using pipe-delimited format with exact field order from user_task_description
   - Load data for restaurants, menus, cart, orders, order_items, deliveries, and reviews
   - Handle data loading efficiently and handle missing or empty files gracefully

4. **Template Rendering**:
   - Pass exact context variables to templates as per page requirements
   - Use element IDs exactly as specified for all HTML elements
   - Implement navigation links with url_for targeting correct route functions
   
CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all templates_candidate_a/*.html files
- Maintain complete isolation by referencing only templates_candidate_a folder in render_template()
- Do not include authentication or external dependencies
- Root route '/' must redirect to dashboard page precisely
- Follow specifications strictly for element IDs, routes, and data loading to ensure independent completeness

Output: app_candidate_a.py and templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications with expertise in isolated template rendering.

Your goal is to independently implement a complete Flask app candidate (app_candidate_b.py) with an isolated templates_candidate_b folder, covering all 9 specified pages using element IDs, routes, and data loading from local 'data/' text files.

Task Details:
- Read user_task_description and design_spec.md for all interface, route, and data file specifications
- Implement app_candidate_b.py referencing templates_candidate_b/*.html only
- Load all necessary data from 'data/' directory text files exactly as specified
- Create all routes and handlers for the 9 pages with correct element IDs and navigation flows
- Ensure root route '/' redirects to the dashboard page

Implementation Requirements:
1. **Flask Application Setup**:
   - Setup Flask app with isolated template folder 'templates_candidate_b'
   - Use render_template() calls referencing templates_candidate_b files

2. **Routing and Pages**:
   - Implement routes for Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, and Reviews
   - For dynamic routes, use URL variables as needed (e.g., restaurant_id, item_id)
   - Ensure route handler function names and return statements match design_spec.md

3. **Data Loading**:
   - Parse text files in 'data/' directory using pipe-delimited format with exact field order from user_task_description
   - Load data for restaurants, menus, cart, orders, order_items, deliveries, and reviews
   - Handle data loading efficiently and handle missing or empty files gracefully

4. **Template Rendering**:
   - Pass exact context variables to templates as per page requirements
   - Use element IDs exactly as specified for all HTML elements
   - Implement navigation links with url_for targeting correct route functions
   
CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and all templates_candidate_b/*.html files
- Maintain complete isolation by referencing only templates_candidate_b folder in render_template()
- Do not include authentication or external dependencies
- Root route '/' must redirect to dashboard page precisely
- Follow specifications strictly for element IDs, routes, and data loading to ensure independent completeness

Output: app_candidate_b.py and templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging parallel Flask app implementations into a unified final product.

Your goal is to merge two independent Flask app implementations (app_candidate_a.py with templates_candidate_a and app_candidate_b.py with templates_candidate_b) into a single app.py and templates/*.html bundle that fully implements the FoodDelivery application with all 9 pages, routes, element IDs, data file loading, and navigation specified.

Task Details:
- Read user_task_description, design_spec.md, and both implementation candidates (app_candidate_a.py + templates_candidate_a, app_candidate_b.py + templates_candidate_b)
- Compare and analyze both implementations for feature completeness, correct route definitions, element ID consistency, data file loading accuracy, and no-auth design
- Create unified app.py combining the best or all matching parts, preserving exact route function signatures and behaviors
- Consolidate templates from both candidates into a single templates/ folder, ensuring all element IDs and navigation flows remain consistent and correct
- Remove references to isolated candidate template folders; all render_template calls must refer to templates/ directory
- Ensure root route '/' redirects to dashboard page

Merging Requirements:
1. **Code Consolidation**:
   - Merge Python code logically without duplications or conflicts
   - Maintain adherence to design_spec.md routes and data usage
   - Verify all functions handle requests consistently and correctly

2. **Template Consolidation**:
   - Combine templates ensuring all required files exist with correct element IDs
   - Resolve any naming conflicts or inconsistencies in templates
   - Keep navigation consistent across pages

3. **Output Validation**:
   - Provide well-structured app.py and templates/*.html ready for final validation
   - Ensure no external dependencies on candidate folders remain

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output merged app.py and templates/*.html files
- Final app.py must not reference templates_candidate_a or templates_candidate_b folders
- All routes, element IDs, navigation flows, and data loading must conform exactly to design_spec.md and user_task_description
- Root route '/' must redirect to dashboard page precisely
- Ensure merged outputs are ready for syntax and functional validation

Output: app.py and templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python Flask web applications validation.

Your goal is to independently validate backend and frontend implementations ensuring correctness of syntax, runtime, routes, page titles, element IDs, data integration, and user interaction flows, and produce a detailed validation report.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html as input artifacts
- Perform validations on app.py and templates/*.html independently
- Output validation_a.md report with detailed findings and suggested fixes

Validation Focus Areas:
1. Syntax and Runtime
   - Use validate_python_file for app.py syntax and runtime checks
   - Ensure Flask server starts without errors

2. Flask Routes and Coverage
   - Verify all specified routes exist and respond correctly
   - Check root route directs to dashboard page
   - Confirm HTTP methods and route handlers match design_spec.md

3. Page Titles and Element IDs
   - Confirm exact page titles on each page as per design_spec.md
   - Verify presence and correctness of all element IDs on all templates
   - Validate dynamic element ID patterns (e.g., IDs with variable suffixes)

4. Data File Integration
   - Verify data files are loaded correctly with exact field parsing
   - Test data-driven content rendering matches design specifications

5. Feature Interaction Tests
   - Simulate typical user interactions across pages (adding to cart, checkout, order tracking)
   - Ensure UI elements respond and update as expected

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools thoroughly
- Produce detailed markdown report validation_a.md covering all test points
- Write file using write_text_file tool
- Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Quality Assurance Engineer specializing in end-to-end validation of Flask web applications.

Your goal is to independently verify backend and frontend for consistent routing, UI navigation flow correctness, complete element IDs, data integration reliability, and UI responsiveness, then produce a comprehensive validation report.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html as inputs
- Validate app.py and templates/*.html ensuring strict adherence to design specs
- Produce validation_b.md report detailing validation results and defect descriptions

Validation Focus Areas:
1. Consistent Routes and Navigation
   - Confirm all page routes are implemented as specified
   - Verify navigation from root dashboard flows correctly to all pages
   - Check all navigation buttons and links function properly

2. Element ID Completeness
   - Validate all static and dynamic element IDs are present and match spec exactly
   - Check dynamic IDs have correct patterns/rendering

3. Data File Loading and Integration
   - Test robustness of data file loading under normal and edge case data
   - Ensure dynamic data is rendered accurately in UI components

4. UI Responsiveness and Behavior
   - Assess UI elements responsiveness (buttons, inputs) and correct state updates
   - Test interactive features like cart updates, order tracking, review submission for proper behavior

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools as needed
- Write a detailed markdown report validation_b.md with clear defect and validation findings
- Save output using write_text_file tool
- Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Engineer specializing in code and UI repair and merging for Flask web applications.

Your goal is to merge two independent validation reports, implement all agreed repairs and improvements to app.py and templates/*.html strictly following design_spec.md, ensuring full compliance with route paths, element IDs, navigation flow, and data file usage, producing final validated application files.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, validation_b.md inputs
- Analyze and reconcile all validation findings from both reports
- Apply all confirmed fixes and improvements to app.py and templates/*.html
- Preserve exact route paths, element IDs, navigation, and data file integration as specified
- Produce final app.py and templates/*.html as output artifacts

Repair and Merge Process:
1. Identify and prioritize common defects and fixes noted in both reports
2. Verify correctness of fixes with respect to design_spec.md specifications
3. Ensure no new defects are introduced during repair
4. Maintain clean code and consistent formatting in final deliverables

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html
- Output files must fully conform to design_spec.md and pass all validation criteria
- Do not alter routes, element IDs, or navigation beyond fixes
- Ensure final application files are ready for deployment and testing

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
        ("DesignMerger", """Check design_specification_a.md for completeness, exact mapping of routes, page titles, element IDs, and data file references as per the requirements.""", [{'type': 'text_file', 'name': 'design_specification_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Evaluate design_specification_b.md for full coverage of all 9 pages including data file usage, consistent element ID definitions, and navigation flow.""", [{'type': 'text_file', 'name': 'design_specification_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Validate merged design_spec.md ensures a coherent, unambiguous design ready to guide implementation with precise route paths, page titles, element IDs, and local text data file usage.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Validate app_candidate_a.py and templates_candidate_a/*.html for full specification coverage, correct route bindings, element IDs, and accurate reading of local data text files.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Validate app_candidate_b.py and templates_candidate_b/*.html for complete feature coverage, correct routes, element IDs, data loading, with navigation starting from the dashboard page root.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Ensure merged app.py and templates/*.html implement the FoodDelivery app per design_spec.md and are ready for syntax and functional validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Review validation_a.md to ensure all points are reproducible, specific, and actionable before applying fixes.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Assess validation_b.md for accuracy, thoroughness, and clear defect descriptions before repairs.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm that the final repaired app.py and templates/*.html fully adhere to the design_spec.md and resolve all validation issues.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
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

    # Parallel creation of design specifications
    await asyncio.gather(
        execute(DesignAnalystA, "Create design_specification_a.md with comprehensive Flask routes, page titles, element IDs, data file usage, and navigation flow for all 9 pages."),
        execute(DesignAnalystB, "Create design_specification_b.md detailing all Flask routes, page titles, element IDs, data file usage, and navigation pathways for all 9 pages.")
    )

    # Read outputs from DesignAnalysts for merging
    design_spec_a, design_spec_b = "", ""
    try:
        design_spec_a = open("design_specification_a.md").read()
    except:
        pass
    try:
        design_spec_b = open("design_specification_b.md").read()
    except:
        pass

    # Merge design specifications
    await execute(DesignMerger,
                  f"=== Design Specification A ===\n{design_spec_a}\n\n"
                  f"=== Design Specification B ===\n{design_spec_b}")
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

    # Parallel execution of ImplementationEngineerA and ImplementationEngineerB
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete Flask app candidate app_candidate_a.py with templates_candidate_a/*.html, "
                "loading from data text files and ensuring full route and element ID coverage per design_spec.md."),
        execute(ImplementationEngineerB,
                "Implement complete Flask app candidate app_candidate_b.py with templates_candidate_b/*.html, "
                "loading from data text files and ensuring full route and element ID coverage per design_spec.md.")
    )

    # Read outputs from both candidates for merging
    candidate_a_app, candidate_b_app = "", ""
    candidate_a_templates, candidate_b_templates = "", ""
    try:
        candidate_a_app = open("app_candidate_a.py").read()
    except Exception:
        pass
    try:
        candidate_b_app = open("app_candidate_b.py").read()
    except Exception:
        pass
    try:
        candidate_a_templates = _read_text_artifacts("templates_candidate_a/*.html")
    except Exception:
        pass
    try:
        candidate_b_templates = _read_text_artifacts("templates_candidate_b/*.html")
    except Exception:
        pass

    # Execute ImplementationMerger to unify both candidates into final app.py and templates/*.html
    await execute(ImplementationMerger,
                  f"=== app_candidate_a.py ===\n{candidate_a_app}\n\n"
                  f"=== templates_candidate_a/*.html ===\n{candidate_a_templates}\n\n"
                  f"=== app_candidate_b.py ===\n{candidate_b_app}\n\n"
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
        recovery_time=45
    )

    # Parallel validation execution
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Perform independent validation of app.py and templates/*.html including syntax, runtime, route coverage, element IDs, data integration, and interaction tests. Produce detailed validation_a.md."),
        execute(ValidationEngineerB,
                "Independently verify backend and frontend implementations for route consistency, UI navigation flow, element ID completeness, data loading, and UI responsiveness. Produce detailed validation_b.md.")
    )

    # Read validation reports
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # Repair and merge based on validation reports
    await execute(RepairMerger,
                  f"Merge validation reports validation_a.md and validation_b.md, analyze all issues, and apply necessary fixes to app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md, preserve routes, element IDs, and navigation. Output final validated app.py and templates/*.html.\n\n"
                  f"=== ValidationEngineerA Report ===\n{validation_a_content}\n\n=== ValidationEngineerB Report ===\n{validation_b_content}")
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
