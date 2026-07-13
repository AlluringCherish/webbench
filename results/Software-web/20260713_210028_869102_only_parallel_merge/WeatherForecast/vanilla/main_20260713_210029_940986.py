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
# 20260713_210029_940986/main_20260713_210029_940986.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent comprehensive Flask web app designs for the WeatherForecast app and merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignerA and DesignerB independently create full route, page titles, element IDs, and data handling specs in design_candidate_a.md \"\n        \"and design_candidate_b.md without reading each other's output; DesignMerger reads both candidates and produces a final merged design_spec.md.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignerA\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in Flask web application design and detailed specifications.\n\nYour goal is to derive a comprehensive design specification for the WeatherForecast app that covers all 8 pages, defining Flask routes, page titles, element IDs including buttons, and data input/output formats using local text files. The design should begin from the Dashboard page.\n\nTask Details:\n- Read user_task_description fully\n- Produce design_candidate_a.md containing all design details with clear route definitions, page titles, element IDs, and data handling specifications\n- Focus on complete coverage of all pages and data files outlined in the user task\n- Output ONLY the design_candidate_a.md artifact as specified\n\nDesign Requirements:\n1. Define Flask routes with URL patterns, HTTP methods, and corresponding page titles\n2. Specify all required HTML element IDs per page with explicit mention of dynamic IDs where applicable\n3. Detail data input and output formats for local text files with exact field orders and example data rows\n4. Structure design_candidate_a.md for easy reference during implementation\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_candidate_a.md\n- Ensure all element IDs from user task are included exactly as provided\n- Routes and page titles must be consistent and comprehensive\n- Data file formats must follow the user task specifications precisely\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignerB\",\n            \"prompt\": \"\"\"You are a Software Designer specializing in Flask web application architecture and integration design.\n\nYour goal is to independently produce a comprehensive alternate design specification for the WeatherForecast app. Include all necessary Flask routes, page titles, element IDs, and integration details specifically for using local text files as the data source. The design should start from the Dashboard page.\n\nTask Details:\n- Read user_task_description completely\n- Generate design_candidate_b.md with detailed Flask routes, page titles, element IDs, and local file data integration specifications\n- Cover all 8 pages and related data files fully and independently from others\n- Output ONLY the design_candidate_b.md artifact as specified\n\nDesign Specifications:\n1. Provide clear route-to-page mappings including URL patterns and HTTP methods\n2. List explicit element IDs per page including dynamic IDs for buttons referencing IDs\n3. Specify the expected structure of data files used for the application with exact field sequencing and example content\n4. Ensure design_candidate_b.md is well-organized for straightforward implementation\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_candidate_b.md\n- Include all required element IDs exactly as per user task\n- Ensure route definitions and page titles are exhaustive and practical\n- Data file formats must match user task details exactly\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Merger specialist experienced in consolidating multiple Flask web app design proposals into a unified implementation-ready specification.\n\nYour goal is to review design_candidate_a.md and design_candidate_b.md, resolve any contradictions, unify page routes, page titles, element IDs, and design details into a single coherent design. Produce the final comprehensive design_spec.md for the WeatherForecast Flask application.\n\nTask Details:\n- Read user_task_description fully along with design_candidate_a.md and design_candidate_b.md as inputs\n- Identify and resolve discrepancies between the two candidate designs\n- Merge routes, page titles, element IDs (including dynamic IDs), and data file specifications confidently and clearly\n- Create final design_spec.md ensuring completeness, consistency, and practical implementability covering all 8 pages and data files\n- Output ONLY the design_spec.md artifact as specified\n\nMerging Guidelines:\n1. Harmonize all Flask route URL patterns and HTTP methods\n2. Standardize page titles and element IDs across pages using exact names from candidates or user_task_description as needed\n3. Integrate data file schemas and example data rows into a single consistent format\n4. Document any conflicts resolved and chosen conventions within design_spec.md for clarity\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save design_spec.md\n- Final design must be fully consistent with user task requirements and incorporate all valid design points from candidate specs\n- Ensure no contradictions or ambiguities remain\n- The merged design_spec.md is final source for implementation teams\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignerA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignerA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for completeness, correctness, and feasibility of routes, page titles, element IDs, and data model before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignerB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md thoroughly for accurate route coverage, Flask app integration, and data file use before merging.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify design_spec.md fully specifies all required app design details and resolves contradictions.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Implement two independent Flask+template app versions for WeatherForecast and merge into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationDevA and ImplementationDevB independently develop complete Flask app bundles with app.py and template files based on \"\n        \"design_spec.md without sharing output; ImplementationMerger compares both and produces final integrated app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationDevA\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications and template integration.\n\nYour goal is to develop a complete WeatherForecast Flask application implementation with isolated template folder and backend Flask app based strictly on design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md fully\n- Develop complete Flask app implementation in app_candidate_a.py\n- Create all HTML templates in templates_candidate_a/ matching specification exactly\n- Use local text files in data/ directory for all data storage as specified\n- Enforce exact page routes, titles, element IDs, buttons, and data handling per design_spec.md\n- Focus only on implementing the specified WeatherForecast features independently\n\nImplementation Requirements:\n1. **Flask App Setup and Routing:**\n   - Implement all routes exactly as specified with correct function names and HTTP methods\n   - Use render_template() with template files from templates_candidate_a/\n   - Redirect root '/' route to dashboard page route\n2. **Data Handling:**\n   - Load and parse data from specified local text files using pipe-delimited format\n   - Match exact field order and data types per design_spec.md data schemas\n3. **Template Implementation:**\n   - Create all HTML templates with exact element IDs and page titles as specified\n   - Use Jinja2 templating syntax for dynamic data rendering\n   - Implement navigation buttons and links with correct route function references\n4. **Project Structure:**\n   - Backend Flask app source: app_candidate_a.py\n   - Templates folder: templates_candidate_a/*.html\n   - Data files used should be from data/ directory as per design_spec.md\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all templates under templates_candidate_a/\n- Exactly follow design_spec.md for routes, titles, element IDs, and data formats\n- No dependencies on other candidate implementations\n- Avoid deviating from specifications or adding unstated features\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationDevB\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications and template integration.\n\nYour goal is to independently create a full WeatherForecast Flask application implementation bundle with backend and templates strictly following design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md fully\n- Implement complete backend Flask app in app_candidate_b.py\n- Develop all HTML templates in templates_candidate_b/ matching design_spec.md accurately\n- Utilize local text files from data/ directory according to specified schemas\n- Adhere strictly to specified routes, element IDs, and page titles per design_spec.md\n- Work independently without referring or sharing with other implementations\n\nImplementation Requirements:\n1. **Flask Backend Implementation:**\n   - Implement all specified routes, functions, and HTTP methods exactly as per design_spec.md\n   - Use render_template() to connect with templates_candidate_b/*.html\n   - Root '/' route must redirect to dashboard\n2. **Data Reads:**\n   - Parse local text data files with exact field order and pipe delimiter as defined\n   - Ensure correct data usage for each app functionality\n3. **Template Development:**\n   - Create HTML templates with required element IDs and page titles exactly matching specifications\n   - Use Jinja2 syntax for dynamic content and navigation\n4. **File Organization:**\n   - Backend file: app_candidate_b.py\n   - Templates folder: templates_candidate_b/*.html\n   - Data files used only from data/ directory following schemas\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and all templates under templates_candidate_b/\n- Follow design_spec.md strictly for all routes, IDs, and page titles\n- No dependencies on other candidate implementations\n- Provide complete implementations covering all specified features\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging and consolidating Flask applications and frontend templates.\n\nYour goal is to compare two independent WeatherForecast Flask application candidates and merge their strongest, most correct features to produce a final integrated Flask backend and frontend templates matching design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md completely\n- Analyze app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html\n- Compare each candidate against design_spec.md for completeness, correctness, feature coverage, and code quality\n- Merge strongest code and template features into single app.py and templates/*.html without dependencies on candidate folders\n- Ensure merged app.py implements all required routes, data handling, and backend logic fully\n- Ensure all templates include correct element IDs, page titles, and navigation per design_spec.md\n- Remove redundant or conflicting code, resolving inconsistencies favoring design_spec.md compliance\n- Produce final deliverables ready for validation and deployment\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and templates/*.html\n- Final implementation must conform exactly to design_spec.md specifications\n- No references to candidate-specific folders or files in final outputs\n- Deliver coherent, maintainable, and fully functional integrated Flask app\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationDevA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationDevA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationDevB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationDevB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationDevA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Check app_candidate_a.py and template files for full compliance with design_spec.md and Flask correctness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationDevB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Verify app_candidate_b.py and templates_candidate_b/*.html fully implement design_spec.md requirements with no missing features.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Ensure merged app.py and templates/*.html form a coherent Flask application ready for validation.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Perform parallel independent validations on app.py and templates, then merge fixes to produce final executable app.py and templates\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidatorA and ValidatorB independently validate app.py and templates/*.html against design_spec.md and functionality requirements, \"\n        \"generate validation reports, then RepairMerger consolidates fixes into final app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidatorA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Python web applications with Flask and HTML frontends.\n\nYour goal is to validate the correctness, syntax, and structural integrity of the backend implementation, ensuring full route coverage and HTML page element accuracy.\n\nTask Details:\n- Read user_task_description for requirements context\n- Read design_spec.md for specification details of routes, templates, and data structures\n- Read app.py and templates/*.html as implementation artifacts to validate\n- Produce validation_a.md detailing syntax checks, route coverage, page contents, and element ID correctness\n\nValidation Requirements:\n1. **Syntax & Startup**:\n   - Validate Python syntax and runtime startup of app.py using validate_python_file tool\n   - Ensure app starts without errors or exceptions\n\n2. **Route Coverage**:\n   - Confirm all routes defined in design_spec.md are implemented in app.py\n   - Ensure root route '/' redirects to dashboard-page\n   - Check HTTP methods and function names match specification\n\n3. **HTML Structure and Elements**:\n   - Verify all required element IDs are present exactly in templates/*.html files\n   - Confirm static and dynamic IDs as specified are correctly implemented\n   - Check page titles and container IDs match specification\n\n4. **Correctness and Consistency**:\n   - Cross-check variable names passed from app.py to templates match design_spec.md\n   - Validate that render_template calls use correct template files\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools to verify app.py\n- Use write_text_file tool to save validation_a.md report\n- Report must detail any syntax errors, missing routes, missing or incorrect element IDs, and inconsistencies\n- Focus strictly on backend code correctness and template structure only; exclude UI interactions and data correctness\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidatorB\",\n            \"prompt\": \"\"\"You are a Quality Assurance Engineer skilled in testing Python Flask web applications and their frontends.\n\nYour goal is to independently validate functional correctness of data reading, UI interactions, button functionalities, and accurate data display.\n\nTask Details:\n- Study user_task_description and design_spec.md for full functional and UI requirements\n- Examine app.py and templates/*.html for implementation of data handling and user interface\n- Validate that data files are read correctly according to schemas\n- Confirm buttons and interactive elements trigger correct backend routes or actions\n- Verify displayed data (weather, forecasts, alerts, air quality) is consistent and correctly formatted\n- Document findings and validations in validation_b.md report\n\nValidation Requirements:\n1. **Data Handling**:\n   - Check data file reading logic in app.py matches design_spec schemas and data formats\n   - Confirm no data omissions or mismatches occur during loading and processing\n\n2. **UI Interaction Verification**:\n   - Validate buttons (static and dynamic) function as specified\n   - Confirm filtering controls, dropdowns, toggles perform expected filtering or state changes\n\n3. **Data Display**:\n   - Ensure that UI elements display correct data from backend context variables\n   - Verify that updates or changes in data are reflected in user interface templates\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code as needed to test data loading and functionality\n- Use write_text_file tool to output validation_b.md\n- Focus strictly on runtime behavior, data correctness, and UI interaction fidelity\n- Do not address syntax or structural backend code errors (covered by ValidatorA)\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging validation reports and applying fixes to web application backend and frontend code.\n\nYour goal is to consolidate ValidatorA's and ValidatorB's findings, and apply all necessary corrections to app.py and templates/*.html files to produce a final, fully functional and specification-compliant version.\n\nTask Details:\n- Read user_task_description and design_spec.md for complete requirements context\n- Read app.py and templates/*.html as the base implementation to correct\n- Read validation_a.md and validation_b.md reports from validators outlining issues and suggested fixes\n- Apply fixes preserving original design and functionality strictly per design_spec.md\n- Correct syntax errors, missing routes, element ID issues, data handling bugs, UI interaction problems\n- Ensure final app.py passes syntax checks and startup validation\n- Ensure final templates/*.html contain all elements and correct dynamic IDs with matching backend variables\n- Deliver final corrected app.py and templates/*.html files\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py and all template files\n- Do not introduce unrelated features or deviate from specification\n- Preserve interface stability and complete functional correctness per reports\n- Validate corrections internally to confirm resolution of all validation issues\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidatorA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidatorB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidatorA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Review validation_a.md for thoroughness, reproducible issues, and actionable fixes.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidatorB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Review validation_b.md for coverage of data handling, UI correctness, and adherence to requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure final merged app.py and templates/*.html fully conform to design_spec.md and fix all validation issues.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'WeatherForecast' Web Application

## 1. Objective
Develop a comprehensive web application named 'WeatherForecast' using Python, with data managed through local text files. The application enables users to view current weather conditions, check weekly forecasts, search for locations, receive weather alerts, and monitor air quality. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'WeatherForecast' application is Python.

## 3. Page Design

The 'WeatherForecast' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Weather Dashboard
- **Overview**: The main hub displaying current weather, quick location access, and navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: current-weather-summary** - Type: Div - Display of current weather conditions for default location.
  - **ID: search-location-button** - Type: Button - Button to navigate to location search page.
  - **ID: view-forecast-button** - Type: Button - Button to navigate to weekly forecast page.
  - **ID: view-alerts-button** - Type: Button - Button to navigate to weather alerts page.

### 2. Current Weather Page
- **Page Title**: Current Weather
- **Overview**: A page displaying detailed current weather conditions for selected location.
- **Elements**:
  - **ID: current-weather-page** - Type: Div - Container for the current weather page.
  - **ID: location-name** - Type: H1 - Display location name.
  - **ID: temperature-display** - Type: Div - Display current temperature.
  - **ID: weather-condition** - Type: Div - Display weather condition (sunny, rainy, cloudy, etc.).
  - **ID: humidity-info** - Type: Div - Display humidity percentage.
  - **ID: wind-speed-info** - Type: Div - Display wind speed.

### 3. Weekly Forecast Page
- **Page Title**: Weekly Forecast
- **Overview**: A page displaying weather forecast for the next 7 days.
- **Elements**:
  - **ID: forecast-page** - Type: Div - Container for the forecast page.
  - **ID: forecast-table** - Type: Table - Table displaying daily forecasts with date, high temp, low temp, and condition.
  - **ID: location-filter** - Type: Dropdown - Dropdown to filter forecast by location.
  - **ID: forecast-list** - Type: Div - Grid displaying forecast cards for each day.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 4. Location Search Page
- **Page Title**: Search Locations
- **Overview**: A page for users to search and select different locations.
- **Elements**:
  - **ID: search-page** - Type: Div - Container for the search page.
  - **ID: location-search-input** - Type: Input - Field to search locations by city name or coordinates.
  - **ID: search-results** - Type: Div - List of search results displaying matching locations.
  - **ID: select-location-button-{location_id}** - Type: Button - Button to select a location (each result has this).
  - **ID: saved-locations-list** - Type: Div - Display of previously saved locations.

### 5. Weather Alerts Page
- **Page Title**: Weather Alerts
- **Overview**: A page displaying active weather alerts and warnings for selected locations.
- **Elements**:
  - **ID: alerts-page** - Type: Div - Container for the alerts page.
  - **ID: alerts-list** - Type: Div - List of all active weather alerts with severity, description, and location.
  - **ID: severity-filter** - Type: Dropdown - Dropdown to filter alerts by severity (All, Critical, High, Medium, Low).
  - **ID: location-filter-alerts** - Type: Dropdown - Dropdown to filter alerts by location.
  - **ID: acknowledge-alert-button-{alert_id}** - Type: Button - Button to acknowledge an alert (each alert has this).

### 6. Air Quality Page
- **Page Title**: Air Quality Index
- **Overview**: A page displaying air quality information and pollution levels for locations.
- **Elements**:
  - **ID: air-quality-page** - Type: Div - Container for the air quality page.
  - **ID: aqi-display** - Type: Div - Display air quality index value (0-500).
  - **ID: aqi-description** - Type: Div - Display air quality description (Good, Moderate, Unhealthy, etc.).
  - **ID: pollution-details** - Type: Table - Table showing PM2.5, PM10, NO2, and other pollutants.
  - **ID: location-aqi-filter** - Type: Dropdown - Dropdown to filter by location.
  - **ID: health-recommendation** - Type: Div - Display health recommendations based on air quality.

### 7. Saved Locations Page
- **Page Title**: Saved Locations
- **Overview**: A page displaying all saved locations with quick weather access.
- **Elements**:
  - **ID: saved-locations-page** - Type: Div - Container for the saved locations page.
  - **ID: locations-table** - Type: Table - Table displaying saved locations with current temp and weather condition.
  - **ID: view-location-weather-{location_id}** - Type: Button - Button to view weather for a location (each location has this).
  - **ID: remove-location-button-{location_id}** - Type: Button - Button to remove saved location (each location has this).
  - **ID: add-new-location-button** - Type: Button - Button to add new location.

### 8. Settings Page
- **Page Title**: Settings
- **Overview**: A page for users to configure temperature units, notification preferences, and default location.
- **Elements**:
  - **ID: settings-page** - Type: Div - Container for the settings page.
  - **ID: temperature-unit-select** - Type: Dropdown - Dropdown to select temperature unit (Celsius, Fahrenheit, Kelvin).
  - **ID: default-location-select** - Type: Dropdown - Dropdown to set default location.
  - **ID: alert-notifications-toggle** - Type: Checkbox - Toggle to enable/disable alert notifications.
  - **ID: save-settings-button** - Type: Button - Button to save settings changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'WeatherForecast' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Current Weather Data
- **File Name**: `current_weather.txt`
- **Data Format**:
  ```
  location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
  ```
- **Example Data**:
  ```
  1|New York|72|Sunny|65|10|2025-01-20 14:30
  2|London|55|Rainy|80|15|2025-01-20 14:30
  3|Tokyo|45|Cloudy|72|8|2025-01-20 14:30
  ```

### 2. Forecasts Data
- **File Name**: `forecasts.txt`
- **Data Format**:
  ```
  forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
  ```
- **Example Data**:
  ```
  1|1|2025-01-21|75|60|Sunny|0|60
  2|1|2025-01-22|68|55|Cloudy|10|70
  3|2|2025-01-21|58|48|Rainy|80|85
  ```

### 3. Locations Data
- **File Name**: `locations.txt`
- **Data Format**:
  ```
  location_id|location_name|latitude|longitude|country|timezone
  ```
- **Example Data**:
  ```
  1|New York|40.7128|-74.0060|USA|EST
  2|London|51.5074|-0.1278|UK|GMT
  3|Tokyo|35.6762|139.6503|Japan|JST
  ```

### 4. Weather Alerts Data
- **File Name**: `alerts.txt`
- **Data Format**:
  ```
  alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
  ```
- **Example Data**:
  ```
  1|1|Thunderstorm|High|Severe thunderstorm warning in effect until 8 PM|2025-01-20 14:00|2025-01-20 20:00|0
  2|2|Fog|Medium|Dense fog advisory in effect until noon tomorrow|2025-01-20 06:00|2025-01-21 12:00|0
  3|1|Wind|Medium|High wind advisory with gusts up to 45 mph|2025-01-20 15:00|2025-01-21 09:00|1
  ```

### 5. Air Quality Data
- **File Name**: `air_quality.txt`
- **Data Format**:
  ```
  aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
  ```
- **Example Data**:
  ```
  1|1|45|12.5|35|28|55|2025-01-20 14:30
  2|2|67|22.3|48|42|78|2025-01-20 14:30
  3|3|120|68.5|95|65|110|2025-01-20 14:30
  ```

### 6. Saved Locations Data
- **File Name**: `saved_locations.txt`
- **Data Format**:
  ```
  saved_id|user_id|location_id|location_name|is_default
  ```
- **Example Data**:
  ```
  1|1|1|New York|1
  2|1|2|London|0
  3|2|3|Tokyo|1
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
    "DesignerA": {
        "prompt": (
            """You are a Software Designer specializing in Flask web application design and detailed specifications.

Your goal is to derive a comprehensive design specification for the WeatherForecast app that covers all 8 pages, defining Flask routes, page titles, element IDs including buttons, and data input/output formats using local text files. The design should begin from the Dashboard page.

Task Details:
- Read user_task_description fully
- Produce design_candidate_a.md containing all design details with clear route definitions, page titles, element IDs, and data handling specifications
- Focus on complete coverage of all pages and data files outlined in the user task
- Output ONLY the design_candidate_a.md artifact as specified

Design Requirements:
1. Define Flask routes with URL patterns, HTTP methods, and corresponding page titles
2. Specify all required HTML element IDs per page with explicit mention of dynamic IDs where applicable
3. Detail data input and output formats for local text files with exact field orders and example data rows
4. Structure design_candidate_a.md for easy reference during implementation

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_candidate_a.md
- Ensure all element IDs from user task are included exactly as provided
- Routes and page titles must be consistent and comprehensive
- Data file formats must follow the user task specifications precisely

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignerB": {
        "prompt": (
            """You are a Software Designer specializing in Flask web application architecture and integration design.

Your goal is to independently produce a comprehensive alternate design specification for the WeatherForecast app. Include all necessary Flask routes, page titles, element IDs, and integration details specifically for using local text files as the data source. The design should start from the Dashboard page.

Task Details:
- Read user_task_description completely
- Generate design_candidate_b.md with detailed Flask routes, page titles, element IDs, and local file data integration specifications
- Cover all 8 pages and related data files fully and independently from others
- Output ONLY the design_candidate_b.md artifact as specified

Design Specifications:
1. Provide clear route-to-page mappings including URL patterns and HTTP methods
2. List explicit element IDs per page including dynamic IDs for buttons referencing IDs
3. Specify the expected structure of data files used for the application with exact field sequencing and example content
4. Ensure design_candidate_b.md is well-organized for straightforward implementation

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_candidate_b.md
- Include all required element IDs exactly as per user task
- Ensure route definitions and page titles are exhaustive and practical
- Data file formats must match user task details exactly

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Merger specialist experienced in consolidating multiple Flask web app design proposals into a unified implementation-ready specification.

Your goal is to review design_candidate_a.md and design_candidate_b.md, resolve any contradictions, unify page routes, page titles, element IDs, and design details into a single coherent design. Produce the final comprehensive design_spec.md for the WeatherForecast Flask application.

Task Details:
- Read user_task_description fully along with design_candidate_a.md and design_candidate_b.md as inputs
- Identify and resolve discrepancies between the two candidate designs
- Merge routes, page titles, element IDs (including dynamic IDs), and data file specifications confidently and clearly
- Create final design_spec.md ensuring completeness, consistency, and practical implementability covering all 8 pages and data files
- Output ONLY the design_spec.md artifact as specified

Merging Guidelines:
1. Harmonize all Flask route URL patterns and HTTP methods
2. Standardize page titles and element IDs across pages using exact names from candidates or user_task_description as needed
3. Integrate data file schemas and example data rows into a single consistent format
4. Document any conflicts resolved and chosen conventions within design_spec.md for clarity

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Final design must be fully consistent with user task requirements and incorporate all valid design points from candidate specs
- Ensure no contradictions or ambiguities remain
- The merged design_spec.md is final source for implementation teams

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignerA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationDevA": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications and template integration.

Your goal is to develop a complete WeatherForecast Flask application implementation with isolated template folder and backend Flask app based strictly on design specifications.

Task Details:
- Read user_task_description and design_spec.md fully
- Develop complete Flask app implementation in app_candidate_a.py
- Create all HTML templates in templates_candidate_a/ matching specification exactly
- Use local text files in data/ directory for all data storage as specified
- Enforce exact page routes, titles, element IDs, buttons, and data handling per design_spec.md
- Focus only on implementing the specified WeatherForecast features independently

Implementation Requirements:
1. **Flask App Setup and Routing:**
   - Implement all routes exactly as specified with correct function names and HTTP methods
   - Use render_template() with template files from templates_candidate_a/
   - Redirect root '/' route to dashboard page route
2. **Data Handling:**
   - Load and parse data from specified local text files using pipe-delimited format
   - Match exact field order and data types per design_spec.md data schemas
3. **Template Implementation:**
   - Create all HTML templates with exact element IDs and page titles as specified
   - Use Jinja2 templating syntax for dynamic data rendering
   - Implement navigation buttons and links with correct route function references
4. **Project Structure:**
   - Backend Flask app source: app_candidate_a.py
   - Templates folder: templates_candidate_a/*.html
   - Data files used should be from data/ directory as per design_spec.md

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all templates under templates_candidate_a/
- Exactly follow design_spec.md for routes, titles, element IDs, and data formats
- No dependencies on other candidate implementations
- Avoid deviating from specifications or adding unstated features

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationDevB": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications and template integration.

Your goal is to independently create a full WeatherForecast Flask application implementation bundle with backend and templates strictly following design specifications.

Task Details:
- Read user_task_description and design_spec.md fully
- Implement complete backend Flask app in app_candidate_b.py
- Develop all HTML templates in templates_candidate_b/ matching design_spec.md accurately
- Utilize local text files from data/ directory according to specified schemas
- Adhere strictly to specified routes, element IDs, and page titles per design_spec.md
- Work independently without referring or sharing with other implementations

Implementation Requirements:
1. **Flask Backend Implementation:**
   - Implement all specified routes, functions, and HTTP methods exactly as per design_spec.md
   - Use render_template() to connect with templates_candidate_b/*.html
   - Root '/' route must redirect to dashboard
2. **Data Reads:**
   - Parse local text data files with exact field order and pipe delimiter as defined
   - Ensure correct data usage for each app functionality
3. **Template Development:**
   - Create HTML templates with required element IDs and page titles exactly matching specifications
   - Use Jinja2 syntax for dynamic content and navigation
4. **File Organization:**
   - Backend file: app_candidate_b.py
   - Templates folder: templates_candidate_b/*.html
   - Data files used only from data/ directory following schemas

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and all templates under templates_candidate_b/
- Follow design_spec.md strictly for all routes, IDs, and page titles
- No dependencies on other candidate implementations
- Provide complete implementations covering all specified features

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging and consolidating Flask applications and frontend templates.

Your goal is to compare two independent WeatherForecast Flask application candidates and merge their strongest, most correct features to produce a final integrated Flask backend and frontend templates matching design specifications.

Task Details:
- Read user_task_description and design_spec.md completely
- Analyze app_candidate_a.py with templates_candidate_a/*.html and app_candidate_b.py with templates_candidate_b/*.html
- Compare each candidate against design_spec.md for completeness, correctness, feature coverage, and code quality
- Merge strongest code and template features into single app.py and templates/*.html without dependencies on candidate folders
- Ensure merged app.py implements all required routes, data handling, and backend logic fully
- Ensure all templates include correct element IDs, page titles, and navigation per design_spec.md
- Remove redundant or conflicting code, resolving inconsistencies favoring design_spec.md compliance
- Produce final deliverables ready for validation and deployment

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and templates/*.html
- Final implementation must conform exactly to design_spec.md specifications
- No references to candidate-specific folders or files in final outputs
- Deliver coherent, maintainable, and fully functional integrated Flask app

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationDevA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationDevA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationDevB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationDevB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidatorA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Python web applications with Flask and HTML frontends.

Your goal is to validate the correctness, syntax, and structural integrity of the backend implementation, ensuring full route coverage and HTML page element accuracy.

Task Details:
- Read user_task_description for requirements context
- Read design_spec.md for specification details of routes, templates, and data structures
- Read app.py and templates/*.html as implementation artifacts to validate
- Produce validation_a.md detailing syntax checks, route coverage, page contents, and element ID correctness

Validation Requirements:
1. **Syntax & Startup**:
   - Validate Python syntax and runtime startup of app.py using validate_python_file tool
   - Ensure app starts without errors or exceptions

2. **Route Coverage**:
   - Confirm all routes defined in design_spec.md are implemented in app.py
   - Ensure root route '/' redirects to dashboard-page
   - Check HTTP methods and function names match specification

3. **HTML Structure and Elements**:
   - Verify all required element IDs are present exactly in templates/*.html files
   - Confirm static and dynamic IDs as specified are correctly implemented
   - Check page titles and container IDs match specification

4. **Correctness and Consistency**:
   - Cross-check variable names passed from app.py to templates match design_spec.md
   - Validate that render_template calls use correct template files

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools to verify app.py
- Use write_text_file tool to save validation_a.md report
- Report must detail any syntax errors, missing routes, missing or incorrect element IDs, and inconsistencies
- Focus strictly on backend code correctness and template structure only; exclude UI interactions and data correctness

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidatorB": {
        "prompt": (
            """You are a Quality Assurance Engineer skilled in testing Python Flask web applications and their frontends.

Your goal is to independently validate functional correctness of data reading, UI interactions, button functionalities, and accurate data display.

Task Details:
- Study user_task_description and design_spec.md for full functional and UI requirements
- Examine app.py and templates/*.html for implementation of data handling and user interface
- Validate that data files are read correctly according to schemas
- Confirm buttons and interactive elements trigger correct backend routes or actions
- Verify displayed data (weather, forecasts, alerts, air quality) is consistent and correctly formatted
- Document findings and validations in validation_b.md report

Validation Requirements:
1. **Data Handling**:
   - Check data file reading logic in app.py matches design_spec schemas and data formats
   - Confirm no data omissions or mismatches occur during loading and processing

2. **UI Interaction Verification**:
   - Validate buttons (static and dynamic) function as specified
   - Confirm filtering controls, dropdowns, toggles perform expected filtering or state changes

3. **Data Display**:
   - Ensure that UI elements display correct data from backend context variables
   - Verify that updates or changes in data are reflected in user interface templates

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code as needed to test data loading and functionality
- Use write_text_file tool to output validation_b.md
- Focus strictly on runtime behavior, data correctness, and UI interaction fidelity
- Do not address syntax or structural backend code errors (covered by ValidatorA)

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging validation reports and applying fixes to web application backend and frontend code.

Your goal is to consolidate ValidatorA's and ValidatorB's findings, and apply all necessary corrections to app.py and templates/*.html files to produce a final, fully functional and specification-compliant version.

Task Details:
- Read user_task_description and design_spec.md for complete requirements context
- Read app.py and templates/*.html as the base implementation to correct
- Read validation_a.md and validation_b.md reports from validators outlining issues and suggested fixes
- Apply fixes preserving original design and functionality strictly per design_spec.md
- Correct syntax errors, missing routes, element ID issues, data handling bugs, UI interaction problems
- Ensure final app.py passes syntax checks and startup validation
- Ensure final templates/*.html contain all elements and correct dynamic IDs with matching backend variables
- Deliver final corrected app.py and templates/*.html files

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all template files
- Do not introduce unrelated features or deviate from specification
- Preserve interface stability and complete functional correctness per reports
- Validate corrections internally to confirm resolution of all validation issues

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'validation_a.md', 'source': 'ValidatorA'}, {'type': 'text_file', 'name': 'validation_b.md', 'source': 'ValidatorB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    }

}

REVIEW_PROFILES = {
    'DesignerA': [
        ("DesignMerger", """Check design_candidate_a.md for completeness, correctness, and feasibility of routes, page titles, element IDs, and data model before merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignerB': [
        ("DesignMerger", """Check design_candidate_b.md thoroughly for accurate route coverage, Flask app integration, and data file use before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify design_spec.md fully specifies all required app design details and resolves contradictions.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationDevA': [
        ("ImplementationMerger", """Check app_candidate_a.py and template files for full compliance with design_spec.md and Flask correctness.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationDevB': [
        ("ImplementationMerger", """Verify app_candidate_b.py and templates_candidate_b/*.html fully implement design_spec.md requirements with no missing features.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Ensure merged app.py and templates/*.html form a coherent Flask application ready for validation.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidatorA': [
        ("RepairMerger", """Review validation_a.md for thoroughness, reproducible issues, and actionable fixes.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidatorB': [
        ("RepairMerger", """Review validation_b.md for coverage of data handling, UI correctness, and adherence to requirements.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Ensure final merged app.py and templates/*.html fully conform to design_spec.md and fix all validation issues.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignerA = build_resilient_agent(
        agent_name="DesignerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    DesignerB = build_resilient_agent(
        agent_name="DesignerB",
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

    # Parallel design generation by DesignerA and DesignerB
    await asyncio.gather(
        execute(DesignerA, "Create design_candidate_a.md for full Flask routes, page titles, element IDs, and data file specs for WeatherForecast app."),
        execute(DesignerB, "Create design_candidate_b.md with independent full Flask routes, page titles, element IDs, and data file specs for WeatherForecast app.")
    )

    # Read design_candidate_a.md and design_candidate_b.md outputs for merging
    design_candidate_a_content, design_candidate_b_content = "", ""
    try:
        design_candidate_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_candidate_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge the two design candidates into final design_spec.md
    await execute(DesignMerger,
                  f"=== Design Candidate A ===\n{design_candidate_a_content}\n\n"
                  f"=== Design Candidate B ===\n{design_candidate_b_content}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    ImplementationDevA = build_resilient_agent(
        agent_name="ImplementationDevA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationDevB = build_resilient_agent(
        agent_name="ImplementationDevB",
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
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel development by ImplementationDevA and ImplementationDevB
    await asyncio.gather(
        execute(ImplementationDevA,
                "Develop complete Flask app implementation as app_candidate_a.py and templates in templates_candidate_a/, "
                "following design_spec.md and user_task_description precisely."),
        execute(ImplementationDevB,
                "Develop complete Flask app implementation as app_candidate_b.py and templates in templates_candidate_b/, "
                "following design_spec.md and user_task_description precisely.")
    )

    # Read candidate outputs for merger input injection
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
        # For templates, read all candidate_a templates content as a single string
        import os, glob
        templates_candidate_a_files = glob.glob("templates_candidate_a/*.html")
        templates_candidate_a_content = ""
        for file_path in templates_candidate_a_files:
            try:
                with open(file_path, "r") as f:
                    templates_candidate_a_content += f"=== {os.path.basename(file_path)} ===\n" + f.read() + "\n\n"
            except:
                continue
    except:
        pass
    try:
        # Similarly for candidate_b templates
        templates_candidate_b_files = glob.glob("templates_candidate_b/*.html")
        templates_candidate_b_content = ""
        for file_path in templates_candidate_b_files:
            try:
                with open(file_path, "r") as f:
                    templates_candidate_b_content += f"=== {os.path.basename(file_path)} ===\n" + f.read() + "\n\n"
            except:
                continue
    except:
        pass

    # Execute ImplementationMerger to merge candidates into final app.py and templates/*.html
    await execute(ImplementationMerger,
                  f"Analyze and merge the following independent WeatherForecast Flask app candidates into a final integrated app.py and templates/*.html as per design_spec.md.\n\n"
                  f"=== app_candidate_a.py ===\n{app_candidate_a_code}\n\n"
                  f"=== templates_candidate_a ===\n{templates_candidate_a_content}\n\n"
                  f"=== app_candidate_b.py ===\n{app_candidate_b_code}\n\n"
                  f"=== templates_candidate_b ===\n{templates_candidate_b_content}")
# Phase2_End

# Phase3_Start

async def verification_phase():
    ValidatorA = build_resilient_agent(
        agent_name="ValidatorA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=60
    )
    ValidatorB = build_resilient_agent(
        agent_name="ValidatorB",
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

    # Parallel validation
    await asyncio.gather(
        execute(ValidatorA,
                "Validate app.py syntax, runtime startup, route coverage, and correctness of HTML structure including element IDs, page titles, and template usage. "
                "Produce detailed validation_a.md report."),
        execute(ValidatorB,
                "Validate functional correctness of data reading, UI interactions, button functionalities, and data display in app.py and templates/*.html. "
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

    # Merge fixes based on validator reports
    await execute(RepairMerger,
                  f"Based on validation reports, apply all necessary fixes to app.py and templates/*.html to produce final fully functional version. "
                  f"Maintain full specification compliance and correctness.\n\n"
                  f"=== ValidationA Report ===\n{validation_a_report}\n\n"
                  f"=== ValidationB Report ===\n{validation_b_report}")
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
