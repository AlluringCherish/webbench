import asyncio
import sys
import os
import time
import asyncio
from typing import List, Dict, Any
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from essential_modules import build_resilient_agent, execute, aggregate_task_metrics
from chaos import ChaosController

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Create a comprehensive design specification document for OnlineAuction covering Flask routes, HTML templates, and data schemas for parallel backend and frontend development\",\n    collab_pattern_name: str = \"Sequential Flow\",\n    collab_pattern_description: str = (\n        \"SystemArchitect drafts design_spec.md including (1) Flask routes with function names, HTTP methods and context variables, \"\n        \"(2) HTML templates detailing element IDs and navigation url_for functions, \"\n        \"and (3) data schemas specifying all required data files, fields, and formats.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"SystemArchitect\",\n            \"prompt\": \"\"\"You are a System Architect specializing in Flask web application design specifications.\n\nYour goal is to produce a comprehensive design specification document enabling Backend and Frontend teams to implement the OnlineAuction application independently and in parallel.\n\nTask Details:\n- Read user_task_description from CONTEXT\n- Create design_spec.md with three main sections tailored for independent parallel development:\n  Section 1: Flask backend routes specification\n  Section 2: Frontend HTML templates with exact element IDs and navigation\n  Section 3: Data file schemas with field definitions and formats\n- Preserve all input artifact details exactly, including page titles and element IDs\n- Do NOT assume or add functionality beyond specified requirements\n\n**Section 1: Flask Routes Specification (Backend)**\n\nDefine a detailed route table with columns:\n- Route Path (e.g., /dashboard, /auction/<int:auction_id>)\n- Function Name (flask function, lowercase with underscores)\n- HTTP Method (GET or POST)\n- Template to render\n- Context Variables passed to template with precise type annotations (str, int, float, list, dict)\n  For list of dict, specify structure fully\n\nRequirements:\n- Include root route '/' redirecting to dashboard page\n- Function names and route paths must be consistent and descriptive\n- Include routes for all pages: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Categories, Winners, Trending Auctions, Auction Status\n\n**Section 2: HTML Templates Specification (Frontend)**\n\nFor each page, specify:\n- Template filename and directory path (e.g., templates/dashboard.html)\n- Page title for <title> and <h1>\n- All required element IDs with exact casing and element types\n- Specify dynamic element IDs using Jinja2 templating patterns (e.g., id=\"view-auction-button-{{ auction.auction_id }}\")\n- Navigation mapping of buttons/links to flask routes using url_for with correct function names\n- Context variables available in each template with full structures\n\nRequirements:\n- All element IDs from user requirements must be present exactly as specified\n- Navigation functions must match Section 1 function names\n- Page titles must exactly match user task descriptions\n\n**Section 3: Data File Schemas (Backend)**\n\nFor each data file listed in user task, specify:\n- Path (data/{filename}.txt)\n- File format: pipe-delimited (|), no header line\n- Exact field order and field names for parsing\n- Description of the file’s purpose\n- Include 2-3 example data rows matching user-provided examples\n\nRequirements:\n- Field order and delimiters must match exactly for backend parsing\n- File format adherence is mandatory for data consistency\n- All fields must be clearly defined and named as per user task\n\nCRITICAL SUCCESS CRITERIA:\n- Backend developers can implement all Flask routes with data handling using only Sections 1 and 3\n- Frontend developers can implement all HTML templates with correct IDs and navigation using only Section 2\n- No overlap or dependency between backend and frontend implementation details beyond specification\n- All element IDs and page titles exactly match user requirements\n- Use write_text_file tool to output design_spec.md\n- Do NOT provide code or details beyond specification document content\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 1 and 3 completeness: all Flask routes with HTTP methods and context variables correctly defined, \"\n                \"all data schema definitions complete with correct field and file formats as per requirements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"SystemArchitect\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Verify design_spec.md Section 2 accuracy: all HTML templates defined with exact required element IDs, \"\n                \"navigation mappings using correct url_for functions, and page titles correctly specified.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase2": "def parallel_implementation_phase(\n    goal: str = \"Independently implement backend logic and frontend templates based on the design specification to realize OnlineAuction functionalities\",\n    collab_pattern_name: str = \"Parallel Flow\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper implements app.py containing Flask routes and data management per design_spec.md Sections 1+3; \"\n        \"FrontendDeveloper implements all HTML template files per design_spec.md Section 2.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloper\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Flask web applications.\n\nYour goal is to implement the complete Flask backend of the OnlineAuction application based on the design specification, delivering a fully functional app.py.\n\nTask Details:\n- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) ONLY from CONTEXT\n- Implement all Flask routes with correct HTTP methods, function names, and context variables exactly as specified\n- Manage data file interactions using the exact field orders and pipe-delimited formats from Section 3\n- Do NOT read or consider frontend template details from Section 2\n- Do NOT add functionality not specified in design_spec.md\n\nImplementation Requirements:\n1. **Flask App Setup**\n   ```python\n   from flask import Flask, render_template, redirect, url_for, request\n   app = Flask(__name__)\n   app.config['SECRET_KEY'] = 'dev-secret-key'\n   ```\n\n2. **Root Route**\n   - Implement '/' route to redirect to Dashboard page route\n   - Use `return redirect(url_for('dashboard'))` or appropriate route name from Section 1\n\n3. **Data Handling**\n   - Load and save data from data/*.txt files using pipe-delimited parsing\n   - Parse lines with: `parts = line.strip().split('|')`\n   - Match exact field order and names from Section 3 for each data file\n   - Implement CRUD and data retrieval as required by route logic\n   - Handle missing or empty files gracefully without crashing\n\n4. **Route Implementation**\n   - Implement all routes as per Section 1 route table with corresponding function names and templates\n   - Pass all required context variables to templates with correct names and data types\n   - For POST routes, handle form data with `request.form`\n   - Return rendered templates using `render_template()` with exact template filenames\n\n5. **Best Practices**\n   - Use `if __name__ == '__main__':` block to run app with debug=True on port 5000\n   - Use `url_for()` for all redirects and URL generation\n   - Validate inputs minimally to avoid runtime errors\n   - Do NOT provide code snippets in chat responses only; always write the full app.py using write_text_file tool\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app.py\n- Respect exact function names and variable names as per design_spec.md Section 1\n- Parse data files exactly according to the schemas in Section 3 (field order and pipe delimiters)\n- Do NOT implement or modify templates or frontend behavior\n- Do NOT add features beyond design_spec.md\n- Ensure the root route redirects properly to the Dashboard page\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloper\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.\n\nYour goal is to create all HTML template files for the OnlineAuction application implementing the full page layouts, element IDs, navigation, and UI details from the design specification.\n\nTask Details:\n- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT\n- Implement all HTML template files (*.html) as specified, including exact page titles and element IDs\n- Implement navigation links and buttons using `url_for()` functions exactly as specified\n- Do NOT reference or implement backend logic or routes beyond those in Section 2\n- Do NOT add templates or elements not specified in design_spec.md\n\nImplementation Requirements:\n1. **Template Structure**\n   ```html\n   <!DOCTYPE html>\n   <html lang=\"en\">\n   <head>\n       <meta charset=\"UTF-8\">\n       <title>{{ Page Title from design_spec.md }}</title>\n   </head>\n   <body>\n       <div id=\"main-container-id\">\n           <h1>{{ Page Title from design_spec.md }}</h1>\n           <!-- Main content with exact element IDs -->\n       </div>\n   </body>\n   </html>\n   ```\n\n2. **Element IDs**\n   - Include all required element IDs exactly as specified (case-sensitive)\n   - For dynamic IDs use Jinja2 templating syntax, e.g., `id=\"view-auction-button-{{ auction.auction_id }}\"`\n\n3. **Navigation**\n   - Use exact `url_for()` function names and parameters for all links and buttons\n   - For static links:\n     ```html\n     <a href=\"{{ url_for('function_name') }}\"><button id=\"element-id\">Text</button></a>\n     ```\n   - For dynamic links:\n     ```html\n     <a href=\"{{ url_for('function_name', id=item.id) }}\"><button id=\"element-id-{{ item.id }}\">Text</button></a>\n     ```\n\n4. **Variables and Control Flow**\n   - Use variables and loops as specified in Section 2 to render dynamic content\n   - Use conditionals to render content conditionally if specified\n\n5. **Forms**\n   - Implement forms for POST routes exactly with correct `method=\"POST\"` and field names as specified\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save all template files in templates/ directory\n- All element IDs must match exactly with design_spec.md Section 2\n- Page titles must match exactly in both <title> and <h1> tags\n- Navigation function names and parameters must exactly match design_spec.md Section 2\n- Do NOT modify backend code or data file handling\n- Do NOT add templates not described in design_spec.md\n- Do NOT provide code snippets in chat only; always write full template files using write_text_file\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"SystemArchitect\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Confirm app.py correctly implements all Flask routes specified, with correct HTTP methods, context variables, \"\n                \"data file handling, and that the root route redirects to the Dashboard page.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloper\",\n            \"reviewer_agent\": \"SystemArchitect\",\n            \"review_criteria\": (\n                \"Confirm all HTML templates fully implement design_spec.md specifications including all element IDs, page titles, \"\n                \"and navigation using url_for functions correctly.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def testing_and_validation_phase(\n    goal: str = \"Perform comprehensive testing and validation of the OnlineAuction backend and frontend code to ensure functional correctness and alignment with requirements\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"Tester conducts testing on app.py and templates/*.html with feedback provided iteratively to BackendDeveloper and FrontendDeveloper for corrections until approval.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendTester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in testing Python backend applications.\n\nYour goal is to thoroughly test the backend implementation of the OnlineAuction web application, ensuring that all Flask routes, data handling, and business logic function correctly and comply with the requirements.\n\nTask Details:\n- Read app.py from CONTEXT input\n- Verify all defined Flask routes correspond to requirements in the OnlineAuction project (Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status)\n- Validate data loading, parsing, and manipulation according to data file formats\n- Test business logic for handling bids, auctions status, filtering, and navigation accuracy\n- Do NOT review frontend templates or UI elements\n- Produce backend_test_report.txt detailing tests performed, results, and coverage\n- Write backend_feedback.txt with clear [APPROVED] status if all tests pass or NEED_MODIFY instructions if issues found\n\nTesting Strategy:\n1. Route and Endpoint Validation:\n   - Confirm presence of all required routes with correct HTTP methods\n   - Check proper rendering or redirecting behavior\n2. Data Handling:\n   - Test file reading from data/*.txt with correct parsing and field orders\n   - Validate data integrity and error handling\n3. Business Logic:\n   - Test bid placement and updates to current bids\n   - Verify filtering and sorting functionalities\n   - Check status updates and correctness of auction states\n4. Error and Edge Cases:\n   - Confirm graceful handling of invalid inputs or missing data\n   - Ensure no crashes or unhandled exceptions\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool to run app.py and test routes dynamically\n- Use write_text_file tool to output backend_test_report.txt and backend_feedback.txt\n- Feedback file must include clear status markers: \"[APPROVED]\" if all criteria met, else \"NEED_MODIFY\"\n- Test coverage must include all routes and critical business logic as per project requirements\n- Do NOT generate code or modify app.py here\n\nOutput: backend_test_report.txt, backend_feedback.txt\"\"\",\n            \"tools\": [\"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_test_report.txt\"},\n                {\"type\": \"text_file\", \"name\": \"backend_feedback.txt\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendTester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in frontend web UI and template validation.\n\nYour goal is to conduct comprehensive testing of the OnlineAuction frontend HTML templates to ensure correct UI structure, required element presence, navigation flows, and accurate template rendering consistent with project requirements.\n\nTask Details:\n- Read templates/*.html from CONTEXT input\n- Verify all required pages and templates are implemented: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status\n- Check all element IDs specified for each page are present with correct casing and HTML element types\n- Validate navigation buttons and links function logically (e.g., back-to-dashboard buttons navigate correctly)\n- Confirm usage of consistent template variables and control flows (loops, conditionals) as appropriate\n- Do NOT review backend code or application logic\n- Generate frontend_test_report.txt detailing UI and template correctness, issues found, and coverage\n- Write frontend_feedback.txt with clear [APPROVED] if UI meets all criteria or NEED_MODIFY with actionable feedback if not\n\nTesting Strategy:\n1. Element Presence:\n   - Check for all static and dynamic element IDs per page specification\n2. Navigation:\n   - Verify buttons and links lead to expected pages/routes\n3. Template Rendering:\n   - Confirm proper use of Jinja2 constructs for loops and conditionals over context data\n4. UI Consistency:\n   - Validate that page titles and key headings match requirements\n5. Error Handling:\n   - Ensure templates handle empty or missing data gracefully\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output frontend_test_report.txt and frontend_feedback.txt\n- Feedback file must include status markers: \"[APPROVED]\" if all validation passes, else \"NEED_MODIFY\"\n- Do NOT modify or generate any backend code\n- Do NOT rely on assumptions about missing elements – strictly check based on provided templates and project specs\n\nOutput: frontend_test_report.txt, frontend_feedback.txt\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloper\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_test_report.txt\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_feedback.txt\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendTester\",\n            \"reviewer_agent\": \"BackendDeveloper\",\n            \"review_criteria\": (\n                \"Evaluate backend_test_report.txt for completeness of route and logic testing, and provide actionable feedback in backend_feedback.txt.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_test_report.txt\"},\n                {\"type\": \"text_file\", \"name\": \"backend_feedback.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendTester\",\n            \"reviewer_agent\": \"FrontendDeveloper\",\n            \"review_criteria\": (\n                \"Assess frontend_test_report.txt on UI and template correctness, and provide detailed frontend_feedback.txt for improvements.\"\n            ),\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_test_report.txt\"},\n                {\"type\": \"text_file\", \"name\": \"frontend_feedback.txt\"}\n            ]\n        }\n    ]\n): pass",
    "phase4": "def refinement_loop_phase(\n    goal: str = \"Iteratively refine backend and frontend implementations based on tester feedback until both pass approval criteria\",\n    collab_pattern_name: str = \"Refinement Loop\",\n    collab_pattern_description: str = (\n        \"BackendDeveloper and FrontendDeveloper iteratively fix issues found by BackendTester and FrontendTester respectively; \"\n        \"testers provide iterative feedback through their feedback files until they write '[APPROVED]', signaling acceptance.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"BackendDeveloperRefiner\",\n            \"prompt\": \"\"\"You are a Backend Developer specializing in Python Flask web applications.\n\nYour goal is to iteratively refine and improve the backend implementation (app.py) based on detailed feedback from backend tests.\n\nTask Details:\n- Read backend_feedback.txt from CONTEXT to identify issues and improvement suggestions\n- Update app.py to address all issues and improve functionality based on feedback\n- Maintain existing backend functionality for OnlineAuction using local text file data\n- Do NOT modify frontend templates or unrelated files\n\nRefinement Instructions:\n1. Analyze all feedback entries carefully, focusing on error messages, missing features, and incorrect data handling.\n2. Implement fixes and adjustments in app.py without introducing new features beyond the scope.\n3. Ensure data loading/parsing from data/*.txt files respects specified formats and field orders.\n4. Test locally before submission to confirm fixes align with feedback points.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated app.py\n- Do NOT override feedback files or frontend code\n- Refinement iteration continues until backend_feedback.txt contains '[APPROVED]'\n- Preserve code readability and comments where applicable\n\nOutput: app.py\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_feedback.txt\", \"source\": \"BackendTester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"}\n            ]\n        },\n        {\n            \"agent_name\": \"BackendTester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in backend testing for Python Flask applications.\n\nYour goal is to rigorously retest the backend implementation (app.py) after refinements and provide detailed feedback with a clear approval status.\n\nTask Details:\n- Read app.py from CONTEXT and execute its functionality\n- Perform comprehensive tests verifying all backend requirements of OnlineAuction:\n  - Data loading correctness from data/*.txt files\n  - Correct implementation of all Flask routes and their outputs\n  - Accurate business logic for auctions, bids, categories, winners, trending, and status pages\n  - Edge cases and error handling\n- Write backend_feedback.txt detailing any failures, bugs, or improvement suggestions\n- If all tests pass, write \"[APPROVED]\" as sole content of backend_feedback.txt\n- Otherwise write \"NEED_MODIFY\" and detailed feedback\n\nTesting Instructions:\n1. Execute app.py using execute_python_code tool with appropriate timeout\n2. Automate input/output validation scenarios matching user task specification\n3. Document all discrepancies and missing features precisely\n\nCRITICAL REQUIREMENTS:\n- Use execute_python_code tool for execution tests\n- Use write_text_file tool to save comprehensive backend_feedback.txt\n- Feedback file must contain either \"[APPROVED]\" or \"NEED_MODIFY\" status marker\n- Feedback is the gating mechanism for backend refinement loop continuation\n\nOutput: backend_feedback.txt\"\"\",\n            \"tools\": [\"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"BackendDeveloperRefiner\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_feedback.txt\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendDeveloperRefiner\",\n            \"prompt\": \"\"\"You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask web applications.\n\nYour goal is to iteratively update and refine frontend templates (*.html) based on detailed feedback from frontend tests.\n\nTask Details:\n- Read frontend_feedback.txt from CONTEXT containing UI and template issues\n- Update all relevant templates in templates/*.html to fix bugs and improve compliance with specifications\n- Maintain consistency with OnlineAuction UI element IDs, page titles, and content structure\n- Do NOT modify backend Python code or other unrelated files\n\nRefinement Instructions:\n1. Carefully analyze frontend_feedback.txt for all indicated issues including missing elements, incorrect IDs, or navigation problems.\n2. Modify template files to resolve issues without adding new, unspecified features.\n3. Ensure all required element IDs and page titles exactly match specifications in user task.\n4. Include proper Jinja2 syntax and maintain clean, valid HTML structure.\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save updated templates/*.html files\n- Repeat refinement cycles until frontend_feedback.txt contains \"[APPROVED]\"\n- Do NOT alter backend code or feedback files directly\n\nOutput: templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_feedback.txt\", \"source\": \"FrontendTester\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"FrontendTester\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in frontend testing of HTML/Jinja2 templates for Flask web applications.\n\nYour goal is to retest frontend templates (*.html) after refinements and produce detailed, actionable feedback including a clear approval status.\n\nTask Details:\n- Read templates/*.html files from CONTEXT and verify their correctness against OnlineAuction UI requirements:\n  - Presence and correctness of all element IDs as specified\n  - Accurate page titles matching specifications\n  - Proper navigation button links and actions\n  - Correct data binding via Jinja2 syntax for dynamic content\n  - UI responsiveness and basic usability checks\n- Write frontend_feedback.txt detailing found issues or improvements\n- If all templates meet requirements fully, write only \"[APPROVED]\" in frontend_feedback.txt\n- Otherwise write \"NEED_MODIFY\" plus detailed feedback\n\nTesting Instructions:\n1. Manually or automatically parse templates/*.html to validate element IDs and structure\n2. Test navigation links for correctness and dynamic content placeholders\n3. Document any missing or incorrect element IDs or contents clearly\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output frontend_feedback.txt\n- Feedback file must contain either \"[APPROVED]\" or \"NEED_MODIFY\" status marker\n- Feedback is mandatory for frontend refinement loop control\n\nOutput: frontend_feedback.txt\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"FrontendDeveloperRefiner\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_feedback.txt\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"BackendDeveloperRefiner\",\n            \"reviewer_agent\": \"BackendTester\",\n            \"review_criteria\": \"Ensure backend refinements address issues and improve test results based on backend_feedback.txt\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"backend_feedback.txt\"}\n            ]\n        },\n        {\n            \"source_agent\": \"FrontendDeveloperRefiner\",\n            \"reviewer_agent\": \"FrontendTester\",\n            \"review_criteria\": \"Ensure frontend refinements resolve UI and template issues identified previously as documented in frontend_feedback.txt\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"frontend_feedback.txt\"}\n            ]\n        }\n    ]\n): pass",
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
    "SystemArchitect": {
        "prompt": (
            """You are a System Architect specializing in Flask web application design specifications.

Your goal is to produce a comprehensive design specification document enabling Backend and Frontend teams to implement the OnlineAuction application independently and in parallel.

Task Details:
- Read user_task_description from CONTEXT
- Create design_spec.md with three main sections tailored for independent parallel development:
  Section 1: Flask backend routes specification
  Section 2: Frontend HTML templates with exact element IDs and navigation
  Section 3: Data file schemas with field definitions and formats
- Preserve all input artifact details exactly, including page titles and element IDs
- Do NOT assume or add functionality beyond specified requirements

**Section 1: Flask Routes Specification (Backend)**

Define a detailed route table with columns:
- Route Path (e.g., /dashboard, /auction/<int:auction_id>)
- Function Name (flask function, lowercase with underscores)
- HTTP Method (GET or POST)
- Template to render
- Context Variables passed to template with precise type annotations (str, int, float, list, dict)
  For list of dict, specify structure fully

Requirements:
- Include root route '/' redirecting to dashboard page
- Function names and route paths must be consistent and descriptive
- Include routes for all pages: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Categories, Winners, Trending Auctions, Auction Status

**Section 2: HTML Templates Specification (Frontend)**

For each page, specify:
- Template filename and directory path (e.g., templates/dashboard.html)
- Page title for <title> and <h1>
- All required element IDs with exact casing and element types
- Specify dynamic element IDs using Jinja2 templating patterns (e.g., id="view-auction-button-{{ auction.auction_id }}")
- Navigation mapping of buttons/links to flask routes using url_for with correct function names
- Context variables available in each template with full structures

Requirements:
- All element IDs from user requirements must be present exactly as specified
- Navigation functions must match Section 1 function names
- Page titles must exactly match user task descriptions

**Section 3: Data File Schemas (Backend)**

For each data file listed in user task, specify:
- Path (data/{filename}.txt)
- File format: pipe-delimited (|), no header line
- Exact field order and field names for parsing
- Description of the file’s purpose
- Include 2-3 example data rows matching user-provided examples

Requirements:
- Field order and delimiters must match exactly for backend parsing
- File format adherence is mandatory for data consistency
- All fields must be clearly defined and named as per user task

CRITICAL SUCCESS CRITERIA:
- Backend developers can implement all Flask routes with data handling using only Sections 1 and 3
- Frontend developers can implement all HTML templates with correct IDs and navigation using only Section 2
- No overlap or dependency between backend and frontend implementation details beyond specification
- All element IDs and page titles exactly match user requirements
- Use write_text_file tool to output design_spec.md
- Do NOT provide code or details beyond specification document content

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],
    },

    "BackendDeveloper": {
        "prompt": (
            """You are a Backend Developer specializing in Flask web applications.

Your goal is to implement the complete Flask backend of the OnlineAuction application based on the design specification, delivering a fully functional app.py.

Task Details:
- Read design_spec.md Sections 1 (Flask Routes) and 3 (Data Schemas) ONLY from CONTEXT
- Implement all Flask routes with correct HTTP methods, function names, and context variables exactly as specified
- Manage data file interactions using the exact field orders and pipe-delimited formats from Section 3
- Do NOT read or consider frontend template details from Section 2
- Do NOT add functionality not specified in design_spec.md

Implementation Requirements:
1. **Flask App Setup**
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Root Route**
   - Implement '/' route to redirect to Dashboard page route
   - Use `return redirect(url_for('dashboard'))` or appropriate route name from Section 1

3. **Data Handling**
   - Load and save data from data/*.txt files using pipe-delimited parsing
   - Parse lines with: `parts = line.strip().split('|')`
   - Match exact field order and names from Section 3 for each data file
   - Implement CRUD and data retrieval as required by route logic
   - Handle missing or empty files gracefully without crashing

4. **Route Implementation**
   - Implement all routes as per Section 1 route table with corresponding function names and templates
   - Pass all required context variables to templates with correct names and data types
   - For POST routes, handle form data with `request.form`
   - Return rendered templates using `render_template()` with exact template filenames

5. **Best Practices**
   - Use `if __name__ == '__main__':` block to run app with debug=True on port 5000
   - Use `url_for()` for all redirects and URL generation
   - Validate inputs minimally to avoid runtime errors
   - Do NOT provide code snippets in chat responses only; always write the full app.py using write_text_file tool

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py
- Respect exact function names and variable names as per design_spec.md Section 1
- Parse data files exactly according to the schemas in Section 3 (field order and pipe delimiters)
- Do NOT implement or modify templates or frontend behavior
- Do NOT add features beyond design_spec.md
- Ensure the root route redirects properly to the Dashboard page

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "FrontendDeveloper": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to create all HTML template files for the OnlineAuction application implementing the full page layouts, element IDs, navigation, and UI details from the design specification.

Task Details:
- Read design_spec.md Section 2 (HTML Templates) ONLY from CONTEXT
- Implement all HTML template files (*.html) as specified, including exact page titles and element IDs
- Implement navigation links and buttons using `url_for()` functions exactly as specified
- Do NOT reference or implement backend logic or routes beyond those in Section 2
- Do NOT add templates or elements not specified in design_spec.md

Implementation Requirements:
1. **Template Structure**
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ Page Title from design_spec.md }}</title>
   </head>
   <body>
       <div id="main-container-id">
           <h1>{{ Page Title from design_spec.md }}</h1>
           <!-- Main content with exact element IDs -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs**
   - Include all required element IDs exactly as specified (case-sensitive)
   - For dynamic IDs use Jinja2 templating syntax, e.g., `id="view-auction-button-{{ auction.auction_id }}"`

3. **Navigation**
   - Use exact `url_for()` function names and parameters for all links and buttons
   - For static links:
     ```html
     <a href="{{ url_for('function_name') }}"><button id="element-id">Text</button></a>
     ```
   - For dynamic links:
     ```html
     <a href="{{ url_for('function_name', id=item.id) }}"><button id="element-id-{{ item.id }}">Text</button></a>
     ```

4. **Variables and Control Flow**
   - Use variables and loops as specified in Section 2 to render dynamic content
   - Use conditionals to render content conditionally if specified

5. **Forms**
   - Implement forms for POST routes exactly with correct `method="POST"` and field names as specified

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all template files in templates/ directory
- All element IDs must match exactly with design_spec.md Section 2
- Page titles must match exactly in both <title> and <h1> tags
- Navigation function names and parameters must exactly match design_spec.md Section 2
- Do NOT modify backend code or data file handling
- Do NOT add templates not described in design_spec.md
- Do NOT provide code snippets in chat only; always write full template files using write_text_file

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'design_spec.md', 'source': 'SystemArchitect'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "BackendTester": {
        "prompt": (
            """You are a Software Test Engineer specializing in testing Python backend applications.

Your goal is to thoroughly test the backend implementation of the OnlineAuction web application, ensuring that all Flask routes, data handling, and business logic function correctly and comply with the requirements.

Task Details:
- Read app.py from CONTEXT input
- Verify all defined Flask routes correspond to requirements in the OnlineAuction project (Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status)
- Validate data loading, parsing, and manipulation according to data file formats
- Test business logic for handling bids, auctions status, filtering, and navigation accuracy
- Do NOT review frontend templates or UI elements
- Produce backend_test_report.txt detailing tests performed, results, and coverage
- Write backend_feedback.txt with clear [APPROVED] status if all tests pass or NEED_MODIFY instructions if issues found

Testing Strategy:
1. Route and Endpoint Validation:
   - Confirm presence of all required routes with correct HTTP methods
   - Check proper rendering or redirecting behavior
2. Data Handling:
   - Test file reading from data/*.txt with correct parsing and field orders
   - Validate data integrity and error handling
3. Business Logic:
   - Test bid placement and updates to current bids
   - Verify filtering and sorting functionalities
   - Check status updates and correctness of auction states
4. Error and Edge Cases:
   - Confirm graceful handling of invalid inputs or missing data
   - Ensure no crashes or unhandled exceptions

CRITICAL REQUIREMENTS:
- Use execute_python_code tool to run app.py and test routes dynamically
- Use write_text_file tool to output backend_test_report.txt and backend_feedback.txt
- Feedback file must include clear status markers: "[APPROVED]" if all criteria met, else "NEED_MODIFY"
- Test coverage must include all routes and critical business logic as per project requirements
- Do NOT generate code or modify app.py here

Output: backend_test_report.txt, backend_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_test_report.txt'}, {'type': 'text_file', 'name': 'backend_feedback.txt'}],
    },

    "FrontendTester": {
        "prompt": (
            """You are a Software Test Engineer specializing in frontend web UI and template validation.

Your goal is to conduct comprehensive testing of the OnlineAuction frontend HTML templates to ensure correct UI structure, required element presence, navigation flows, and accurate template rendering consistent with project requirements.

Task Details:
- Read templates/*.html from CONTEXT input
- Verify all required pages and templates are implemented: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status
- Check all element IDs specified for each page are present with correct casing and HTML element types
- Validate navigation buttons and links function logically (e.g., back-to-dashboard buttons navigate correctly)
- Confirm usage of consistent template variables and control flows (loops, conditionals) as appropriate
- Do NOT review backend code or application logic
- Generate frontend_test_report.txt detailing UI and template correctness, issues found, and coverage
- Write frontend_feedback.txt with clear [APPROVED] if UI meets all criteria or NEED_MODIFY with actionable feedback if not

Testing Strategy:
1. Element Presence:
   - Check for all static and dynamic element IDs per page specification
2. Navigation:
   - Verify buttons and links lead to expected pages/routes
3. Template Rendering:
   - Confirm proper use of Jinja2 constructs for loops and conditionals over context data
4. UI Consistency:
   - Validate that page titles and key headings match requirements
5. Error Handling:
   - Ensure templates handle empty or missing data gracefully

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output frontend_test_report.txt and frontend_feedback.txt
- Feedback file must include status markers: "[APPROVED]" if all validation passes, else "NEED_MODIFY"
- Do NOT modify or generate any backend code
- Do NOT rely on assumptions about missing elements – strictly check based on provided templates and project specs

Output: frontend_test_report.txt, frontend_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloper'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_test_report.txt'}, {'type': 'text_file', 'name': 'frontend_feedback.txt'}],
    },

    "BackendDeveloperRefiner": {
        "prompt": (
            """You are a Backend Developer specializing in Python Flask web applications.

Your goal is to iteratively refine and improve the backend implementation (app.py) based on detailed feedback from backend tests.

Task Details:
- Read backend_feedback.txt from CONTEXT to identify issues and improvement suggestions
- Update app.py to address all issues and improve functionality based on feedback
- Maintain existing backend functionality for OnlineAuction using local text file data
- Do NOT modify frontend templates or unrelated files

Refinement Instructions:
1. Analyze all feedback entries carefully, focusing on error messages, missing features, and incorrect data handling.
2. Implement fixes and adjustments in app.py without introducing new features beyond the scope.
3. Ensure data loading/parsing from data/*.txt files respects specified formats and field orders.
4. Test locally before submission to confirm fixes align with feedback points.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py
- Do NOT override feedback files or frontend code
- Refinement iteration continues until backend_feedback.txt contains '[APPROVED]'
- Preserve code readability and comments where applicable

Output: app.py"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'backend_feedback.txt', 'source': 'BackendTester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}],
    },

    "BackendTester": {
        "prompt": (
            """You are a Software Test Engineer specializing in backend testing for Python Flask applications.

Your goal is to rigorously retest the backend implementation (app.py) after refinements and provide detailed feedback with a clear approval status.

Task Details:
- Read app.py from CONTEXT and execute its functionality
- Perform comprehensive tests verifying all backend requirements of OnlineAuction:
  - Data loading correctness from data/*.txt files
  - Correct implementation of all Flask routes and their outputs
  - Accurate business logic for auctions, bids, categories, winners, trending, and status pages
  - Edge cases and error handling
- Write backend_feedback.txt detailing any failures, bugs, or improvement suggestions
- If all tests pass, write "[APPROVED]" as sole content of backend_feedback.txt
- Otherwise write "NEED_MODIFY" and detailed feedback

Testing Instructions:
1. Execute app.py using execute_python_code tool with appropriate timeout
2. Automate input/output validation scenarios matching user task specification
3. Document all discrepancies and missing features precisely

CRITICAL REQUIREMENTS:
- Use execute_python_code tool for execution tests
- Use write_text_file tool to save comprehensive backend_feedback.txt
- Feedback file must contain either "[APPROVED]" or "NEED_MODIFY" status marker
- Feedback is the gating mechanism for backend refinement loop continuation

Output: backend_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'BackendDeveloperRefiner'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'backend_feedback.txt'}],
    },

    "FrontendDeveloperRefiner": {
        "prompt": (
            """You are a Frontend Developer specializing in HTML/Jinja2 templating for Flask web applications.

Your goal is to iteratively update and refine frontend templates (*.html) based on detailed feedback from frontend tests.

Task Details:
- Read frontend_feedback.txt from CONTEXT containing UI and template issues
- Update all relevant templates in templates/*.html to fix bugs and improve compliance with specifications
- Maintain consistency with OnlineAuction UI element IDs, page titles, and content structure
- Do NOT modify backend Python code or other unrelated files

Refinement Instructions:
1. Carefully analyze frontend_feedback.txt for all indicated issues including missing elements, incorrect IDs, or navigation problems.
2. Modify template files to resolve issues without adding new, unspecified features.
3. Ensure all required element IDs and page titles exactly match specifications in user task.
4. Include proper Jinja2 syntax and maintain clean, valid HTML structure.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated templates/*.html files
- Repeat refinement cycles until frontend_feedback.txt contains "[APPROVED]"
- Do NOT alter backend code or feedback files directly

Output: templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'frontend_feedback.txt', 'source': 'FrontendTester'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'templates/*.html'}],
    },

    "FrontendTester": {
        "prompt": (
            """You are a Software Test Engineer specializing in frontend testing of HTML/Jinja2 templates for Flask web applications.

Your goal is to retest frontend templates (*.html) after refinements and produce detailed, actionable feedback including a clear approval status.

Task Details:
- Read templates/*.html files from CONTEXT and verify their correctness against OnlineAuction UI requirements:
  - Presence and correctness of all element IDs as specified
  - Accurate page titles matching specifications
  - Proper navigation button links and actions
  - Correct data binding via Jinja2 syntax for dynamic content
  - UI responsiveness and basic usability checks
- Write frontend_feedback.txt detailing found issues or improvements
- If all templates meet requirements fully, write only "[APPROVED]" in frontend_feedback.txt
- Otherwise write "NEED_MODIFY" plus detailed feedback

Testing Instructions:
1. Manually or automatically parse templates/*.html to validate element IDs and structure
2. Test navigation links for correctness and dynamic content placeholders
3. Document any missing or incorrect element IDs or contents clearly

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output frontend_feedback.txt
- Feedback file must contain either "[APPROVED]" or "NEED_MODIFY" status marker
- Feedback is mandatory for frontend refinement loop control

Output: frontend_feedback.txt"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'templates/*.html', 'source': 'FrontendDeveloperRefiner'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'frontend_feedback.txt'}],
    }

}

REVIEW_PROFILES = {
    'SystemArchitect': [
        ("BackendDeveloper", """Verify design_spec.md Section 1 and 3 completeness: all Flask routes with HTTP methods and context variables correctly defined, "
                "all data schema definitions complete with correct field and file formats as per requirements.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}]),
        ("FrontendDeveloper", """Verify design_spec.md Section 2 accuracy: all HTML templates defined with exact required element IDs, "
                "navigation mappings using correct url_for functions, and page titles correctly specified.""", [{'type': 'user', 'name': 'user_task_description'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'BackendDeveloper': [
        ("SystemArchitect", """Confirm app.py correctly implements all Flask routes specified, with correct HTTP methods, context variables, "
                "data file handling, and that the root route redirects to the Dashboard page.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}])
    ],

    'FrontendDeveloper': [
        ("SystemArchitect", """Confirm all HTML templates fully implement design_spec.md specifications including all element IDs, page titles, "
                "and navigation using url_for functions correctly.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'BackendTester': [
        ("BackendDeveloper", """Evaluate backend_test_report.txt for completeness of route and logic testing, and provide actionable feedback in backend_feedback.txt.""", [{'type': 'text_file', 'name': 'backend_test_report.txt'}, {'type': 'text_file', 'name': 'backend_feedback.txt'}])
    ],

    'FrontendTester': [
        ("FrontendDeveloper", """Assess frontend_test_report.txt on UI and template correctness, and provide detailed frontend_feedback.txt for improvements.""", [{'type': 'text_file', 'name': 'frontend_test_report.txt'}, {'type': 'text_file', 'name': 'frontend_feedback.txt'}])
    ],

    'BackendDeveloperRefiner': [
        ("BackendTester", """Ensure backend refinements address issues and improve test results based on backend_feedback.txt""", [{'type': 'text_file', 'name': 'backend_feedback.txt'}])
    ],

    'FrontendDeveloperRefiner': [
        ("FrontendTester", """Ensure frontend refinements resolve UI and template issues identified previously as documented in frontend_feedback.txt""", [{'type': 'text_file', 'name': 'frontend_feedback.txt'}])
    ]

}




# ==================== Compound Chaos Controller Setup ====================
import random
from chaos.injectors import ChaosMode

# Compound Chaos: Per-task sampling
COMPOUND_CONFIG = {
    "agent_intensity": random.choice([0.2, 0.3, 0.4, 0.5, 0.6]),
    "prompt_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "io_method": random.choice(["WORD_SHUFFLE", "WORD_DELETION", "WORD_REPLACEMENT"]),
    "prompt_probability": 0.2,
    "io_probability": 0.2
}

# ChaosMode mapping
MODE_MAP = {
    "WORD_SHUFFLE": ChaosMode.WORD_SHUFFLE,
    "WORD_DELETION": ChaosMode.WORD_DELETION,
    "WORD_REPLACEMENT": ChaosMode.WORD_REPLACEMENT,
}

chaos_controller = ChaosController(
    agent_chaos_enabled=True,
    stress_chaos_enabled=True,
    stress_chaos_mode=MODE_MAP[COMPOUND_CONFIG["prompt_method"]],
    io_chaos_enabled=True,
    io_chaos_mode=MODE_MAP[COMPOUND_CONFIG["io_method"]],
    target_agent_names=list(AGENT_PROFILES.keys())
)

# Agent chaos is sampled with intensity
chaos_controller.start_experiment(
    running_agents=list(AGENT_PROFILES.keys()),
    agent_profiles=AGENT_PROFILES,
    probability=COMPOUND_CONFIG["agent_intensity"]
)

# Prompt/IO separately sampled at 0.2 probability (reset)
all_agents = list(AGENT_PROFILES.keys())
chaos_controller.stress_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["prompt_probability"]]
chaos_controller.io_chaos_targets = [a for a in all_agents if random.random() < COMPOUND_CONFIG["io_probability"]]

# Guarantee at least 1
if not chaos_controller.stress_chaos_targets:
    chaos_controller.stress_chaos_targets = [random.choice(all_agents)]
if not chaos_controller.io_chaos_targets:
    chaos_controller.io_chaos_targets = [random.choice(all_agents)]

# Save chaos configuration to file for debugging
from datetime import datetime
import json

chaos_config_data = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "scenario": "compound_chaos",
    "compound_config": COMPOUND_CONFIG,
    "enabled_chaos_types": {
        "agent_chaos": chaos_controller.agent_chaos.enabled,
        "stress_chaos": chaos_controller.stress_chaos.enabled,
        "io_chaos": chaos_controller.io_chaos.enabled
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

print(f"Compound Chaos activated: Agent={COMPOUND_CONFIG['agent_intensity']}, Prompt={COMPOUND_CONFIG['prompt_method']}, IO={COMPOUND_CONFIG['io_method']}")
print(f"Chaos configuration saved to: chaos_config.json")
# ================================================================

# Orchestration Functions
async def design_specification_phase():
    # Create SystemArchitect agent
    SystemArchitect = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute SystemArchitect to create design_spec.md
    await execute(SystemArchitect, "Draft comprehensive design_spec.md covering Flask routes, HTML templates, and data schemas according to user_task_description")
# Phase1_End

# Phase2_Start
import asyncio

async def parallel_implementation_phase():
    # Create BackendDeveloper agent
    BackendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Create FrontendDeveloper agent
    FrontendDeveloper = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute both agents in parallel
    await asyncio.gather(
        execute(BackendDeveloper, "Implement app.py with all Flask routes and data management per design_spec.md Sections 1 and 3"),
        execute(FrontendDeveloper, "Implement all HTML template files per design_spec.md Section 2")
    )
# Phase2_End

# Phase3_Start
import asyncio

async def testing_and_validation_phase():
    # Create BackendTester agent
    BackendTester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendTester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    # Create FrontendTester agent
    FrontendTester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendTester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Execute both testers in parallel as per Refinement Loop pattern
    await asyncio.gather(
        execute(BackendTester, "Test app.py backend routes and business logic; write backend_test_report.txt and backend_feedback.txt"),
        execute(FrontendTester, "Validate templates/*.html UI elements, navigation, and rendering; write frontend_test_report.txt and frontend_feedback.txt")
    )
# Phase3_End

# Phase4_Start

async def refinement_loop_phase():
    # Create agents
    BackendDeveloperRefiner = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendDeveloperRefiner",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    BackendTester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="BackendTester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloperRefiner = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendDeveloperRefiner",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendTester = build_resilient_agent(
        chaos_controller=chaos_controller,
        agent_name="FrontendTester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase4"],
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_LOOPS = 5
    for iteration in range(MAX_LOOPS):
        # Backend refinement and testing
        if iteration == 0:
            # First iteration may not have feedback file, so message excludes it
            await execute(BackendDeveloperRefiner, "Refine and improve backend implementation based on backend_feedback.txt if available")
        else:
            try:
                with open("backend_feedback.txt", "r") as f_bf:
                    backend_feedback_content = f_bf.read()
                await execute(BackendDeveloperRefiner, f"Refine backend app.py based on the following feedback:\n{backend_feedback_content}")
            except FileNotFoundError:
                # No feedback file, still proceed normally
                await execute(BackendDeveloperRefiner, "Refine and improve backend implementation based on latest feedback")

        await execute(BackendTester, "Retest backend app.py and generate backend_feedback.txt")

        try:
            with open("backend_feedback.txt", "r") as f_bf:
                backend_feedback_content = f_bf.read()
            if "[APPROVED]" in backend_feedback_content:
                backend_approved = True
            else:
                backend_approved = False
        except FileNotFoundError:
            backend_approved = False

        # Frontend refinement and testing
        if iteration == 0:
            # First iteration may not have feedback file
            await execute(FrontendDeveloperRefiner, "Refine and improve frontend templates based on frontend_feedback.txt if available")
        else:
            try:
                with open("frontend_feedback.txt", "r") as f_ff:
                    frontend_feedback_content = f_ff.read()
                await execute(FrontendDeveloperRefiner, f"Refine frontend templates based on the following feedback:\n{frontend_feedback_content}")
            except FileNotFoundError:
                await execute(FrontendDeveloperRefiner, "Refine and improve frontend templates based on latest feedback")

        await execute(FrontendTester, "Retest frontend templates and generate frontend_feedback.txt")

        try:
            with open("frontend_feedback.txt", "r") as f_ff:
                frontend_feedback_content = f_ff.read()
            if "[APPROVED]" in frontend_feedback_content:
                frontend_approved = True
            else:
                frontend_approved = False
        except FileNotFoundError:
            frontend_approved = False

        # Check if both backend and frontend approved
        if backend_approved and frontend_approved:
            break
# Phase4_End

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
        parallel_implementation_phase()
    ]
    step3 = [
        testing_and_validation_phase()
    ]
    step4 = [
        refinement_loop_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)
    await asyncio.gather(*step4)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)

    # Save metrics to JSON
    task_metrics = aggregate_task_metrics(CONTEXT)
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
        print(f"\n  Received signal {signum}, saving metrics before exit...")
        try:
            task_metrics = aggregate_task_metrics(CONTEXT)
            metrics_path = Path("metrics.json")
            with open(metrics_path, "w") as f:
                json.dump(task_metrics, f, indent=2)
            print(f"Metrics saved to: {metrics_path.resolve()}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGTERM, save_metrics_on_signal)
    signal.signal(signal.SIGINT, save_metrics_on_signal)

    # Open log file for real-time stdout/stderr capture
    log_file = open("execution_log.txt", "w", encoding="utf-8")

    # Write header
    log_file.write("=== Execution Log ===\n")
    log_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("\n=== OUTPUT ===\n")
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

        # Write summary
        log_file.write(f"\n\n=== Summary ===\n")
        log_file.write(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.close()
