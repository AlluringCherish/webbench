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
# 20260713_210029_475376/main_20260713_210029_475376.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs and merge them into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create complete, detailed Web application design documents specifying \"\n        \"routes, page titles, element IDs, interactions, navigation, and data handling based on the user requirements without knowledge of each other's work. \"\n        \"DesignMerger reviews both design documents and produces a merged, coherent design_spec.md covering the entire OnlineCourse app specification.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Designer with expertise in designing comprehensive specifications for Python-based web applications using local text file data storage.\n\nYour goal is to develop a complete design candidate describing all 9 pages of the OnlineCourse app, detailing route URLs, page titles, element IDs including dynamic buttons, navigation controls, data file utilization, expected user interactions, and constraints such as enrollment status and course progress.\n\nTask Details:\n- Read user_task_description fully to understand app requirements\n- Produce design_candidate_a.md covering all pages, element IDs, navigation, and data interactions\n- Include detailed descriptions of buttons, dynamic IDs, page layout elements, and interaction behaviors\n- Focus exclusively on your own candidate design without referencing other candidates\n\nDesign Specification Requirements:\n1. **Routing and Navigation**\n   - Specify exact route URLs for each page and sub-actions (e.g., enrollments, submissions)\n   - Define navigation flows between pages, relating buttons and dynamic elements\n2. **Page Elements**\n   - List all element IDs per page, including dynamic button patterns with placeholders (e.g., view-course-button-{course_id})\n   - Describe element types (div, button, input, etc.) and their purpose\n3. **Data Handling**\n   - Specify usage of each data file (users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt)\n   - Detail how user interactions update data files (e.g., enrollment creates record, submission writes to submissions.txt)\n4. **User Interactions and Constraints**\n   - Define conditional behaviors like enrollment status disabling enroll button\n   - Describe progress calculations, lesson completion sequences, and certificate generation triggers\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output a complete design_candidate_a.md\n- Ensure all routes, elements, and navigation flows comprehensively cover user task details without omissions\n- Use precise naming consistent with user requirements\n- Do NOT consult other design candidates or user agents\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Designer specialized in alternative design creation for Python web apps using textual data management.\n\nYour goal is to independently create an alternative, comprehensive design candidate describing the full OnlineCourse application including routes, page layouts, element IDs, navigation, sequencing requirements, and data handling details with local text files.\n\nTask Details:\n- Analyze the user_task_description thoroughly for app behavior, data, and UI elements\n- Write design_candidate_b.md describing an alternative design meeting all functional requirements\n- Include detailed route specifications, page element lists with IDs, dynamic button patterns, navigation sequences, and the logic for progress, enrollment, submission, and certificate issuance\n- Do not reference or consult design_candidate_a.md or other designs—maintain design independence\n\nAlternative Design Focus:\n1. **Routes and Page Layout**\n   - Document path URLs and expected page responses\n   - Specify all dynamic and static element IDs per page with usage contexts\n2. **Navigation Interactions**\n   - Describe user flows, button behaviors, and back navigation consistently\n3. **Data Handling and State Management**\n   - Explain how data files are read and updated upon user actions\n   - Detail assignment submission processing and status updates\n4. **Behavioral Constraints**\n   - Include mechanisms for lesson sequencing, progress tracking, and certificate generation conditions\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output complete design_candidate_b.md\n- Cover every specified page, element, and function in detail matching app requirements\n- Ensure naming consistency with the user task but provide an independent design perspective\n- Maintain independence from other design candidates\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [{\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Synthesis Expert specializing in merging parallel design candidates into a final, coherent, and implementable web app specification.\n\nYour goal is to compare and synthesize design_candidate_a.md and design_candidate_b.md, resolving any conflicts or omissions, and produce a merged design_spec.md that fully specifies the OnlineCourse app, including all accurate routes, exact page titles, element IDs (including dynamic buttons), data file usages and formats, navigation flows, progress tracking logic, and enrollment states strictly consistent with the user requirements.\n\nTask Details:\n- Read user_task_description along with design_candidate_a.md and design_candidate_b.md thoroughly\n- Identify and reconcile differences in route definitions, element IDs, navigation, and functional logic\n- Resolve all conflicts to produce a consistent, complete design_spec.md covering the entire application\n- Explicitly include:\n   - All page routes with URL patterns\n   - Exact page titles and element IDs with dynamic ID patterns\n   - Data file interaction specifications including update triggers and field usage\n   - Navigation flows and user interaction constraints (enrollment, progress, submission, certificates)\n- Ensure finalized design aligns fully with user requirements and enables error-free implementation\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final merged design_spec.md\n- Maintain full fidelity and completeness of all required details from both candidate designs\n- Ensure no missing or contradictory information remains\n- Provide a definitive single source of truth for routing, UI elements, navigation, and data handling\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_a.md covers every page route, dynamic element IDs including repeated buttons, data file interactions, and navigation logic as per user requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_b.md covers the app functionality and data flow in detail, matches requirement constraints and includes all specified pages with correct elements and behavior before merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Confirm design_spec.md fully integrates both candidate designs into a consistent, implementable specification with no missing or conflicting details regarding routes, page titles, elements, data files, and required functionality.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent complete Python Flask app implementations and merge them into app.py plus templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement the entire OnlineCourse app as specified in design_spec.md, \"\n        \"including all 9 pages with Flask routes, exact page titles, element IDs, navigation buttons, and data file interactions using local text files. \"\n        \"Each implements fully isolated app_candidate.py and a corresponding templates_candidate folder with HTML files. ImplementationMerger compares both implementations, \"\n        \"resolves conflicts, adopts strongest behaviors, and produces final app.py plus templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in building full-stack web applications with local text file data management.\n\nYour goal is to implement the complete OnlineCourse web application backend and frontend independently based on design_spec.md.\n\nTask Details:\n- Read user_task_description and full design_spec.md for all 9 pages, routes, page titles, element IDs, navigation flows, and data file schema\n- Create isolated backend implementation in app_candidate_a.py implementing ALL Flask routes and logic exactly as specified\n- Create matching HTML templates in templates_candidate_a/ directory following exact element IDs and page structure\n- Handle all data files in data/ folder with exact parsing and updating logic per specifications\n- Focus ONLY on your isolated implementation; do not reference or access other candidates' work\n\nImplementation Requirements:\n1. Flask Backend:\n   - Implement all routes corresponding to the 9 pages in design_spec.md\n   - Enforce page titles exactly as specified (e.g., <title>, <h1>)\n   - Implement enrollment, progress tracking, assignments submission, certificate generation per described functionality\n   - Use local pipe-delimited text files strictly as data storage (users.txt, courses.txt, enrollments.txt, etc.)\n   - Follow data file formats and update logic exactly as documented\n   - Navigation between pages must use proper Flask url_for calls with correct function names\n\n2. Frontend Templates:\n   - Implement templates for all pages in templates_candidate_a/ with given element IDs accurately\n   - Use Jinja2 syntax for dynamic IDs for repeating elements (e.g., view-course-button-{course_id} → id=\"view-course-button-{{ course.course_id }}\")\n   - Include navigation buttons as links or form buttons, matching design requirements exactly\n   - Ensure forms POST to appropriate routes for enrollments, submissions, profile updates\n\n3. UI and Behavior:\n   - Disable enrollment button if already enrolled; show \"Already Enrolled\" text\n   - Calculate progress as specified and update enrollments.txt accordingly\n   - Generate certificates automatically when progress reaches 100%\n   - Maintain lesson completion sequence integrity\n   - Show confirmation messages on assignment submission\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all HTML files under templates_candidate_a/\n- Do not read or incorporate any other candidate's files or code\n- Follow all file and variable naming conventions precisely\n- Ensure full functional completeness and adherence to design_spec.md\n- Focus on your independent implementation only\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Python Flask Developer specializing in full-stack web application development using local text file data stores.\n\nYour goal is to independently implement the entire OnlineCourse Flask application backend and frontend according to design_spec.md.\n\nTask Details:\n- Study user_task_description and comprehensive design_spec.md for ALL pages, routes, UI elements, data files, and logic details\n- Independently write app_candidate_b.py with all routes, backend logic, data reading/writing per specification\n- Independently create templates in templates_candidate_b/ directory following exact element IDs, page titles, and structures\n- Implement full enrollment management, assignment submissions, progress tracking, certificates, and profile management\n- Use data stored in local pipe-delimited text files precisely as outlined\n- Your implementation must be fully isolated; do not consider or depend on ImplementationEngineerA's output\n\nImplementation Guidelines:\n1. Backend:\n   - Implement every Flask route described for the 9 application pages\n   - Use correct function names for Flask routes consistent with design_spec.md\n   - Implement enrollment checks, progress calculations, certificate generation exactly as specified\n   - Perform file I/O with data files correctly handling parsing and updates without headers\n\n2. Templates:\n   - Implement HTML templates using requested element IDs (including dynamic IDs) with Jinja2 templating\n   - Add navigation buttons that link to or post to appropriate routes\n   - Render user and course data dynamically according to specifications\n\n3. Usability:\n   - Disable the enroll button if enrolled; show \"Already Enrolled\"\n   - Use computed progress for display and updating enrollments.txt progress field\n   - Enforce lesson sequence completion before allowing mark complete\n   - Provide confirmation messages on successful submissions\n\nCRITICAL REQUIREMENTS:\n- Save output files using write_text_file tool: app_candidate_b.py and templates_candidate_b/*.html\n- Strictly follow naming conventions and data schema formats\n- Do not integrate or read ImplementationEngineerA's files or code\n- Ensure full correctness, completeness, and adherence to specification independently\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging parallel Python Flask implementations into a unified deployment-ready project.\n\nYour goal is to analyze two fully independent implementations of the OnlineCourse Flask app and combine their strongest, most correct elements into a final app.py and templates directory.\n\nTask Details:\n- Review user_task_description and design_spec.md for project scope and detailed requirements\n- Analyze app_candidate_a.py and app_candidate_b.py backend code; identify identical, conflicting, or complementary route implementations and logic\n- Review templates_candidate_a/*.html and templates_candidate_b/*.html; evaluate element IDs, page titles, navigation flows, and adherence to specification\n- Merge backend logic resolving conflicts by adopting the strongest implementation per route, data handling, error management, correctness, and completeness\n- Merge frontend templates ensuring complete coverage of all element IDs, consistent navigation, and compliance with design_spec.md\n- Ensure merged app.py does not depend on candidate folders or files; fully integrated and runnable\n- Maintain all specified behaviors: enrollment logic, progress tracking, assignment submissions, certificates generation, and profile management\n\nMerging Guidelines:\n1. Backend:\n   - Consolidate routes by selecting best-functioning, fully conformant implementations\n   - Harmonize data file reading/writing with reliable, consistent code\n   - Preserve any error handling improvements and completeness\n\n2. Frontend:\n   - Combine template components to include all required elements and IDs\n   - Use consistent navigation and page titles as per design_spec.md\n   - Remove duplicate or conflicting template elements in merged output\n\n3. Integration:\n   - Final app.py and templates/*.html must form a single coherent Flask application\n   - Outputs must be deployable with no unresolved references or missing elements\n   - Follow Python and Flask best practices for maintainability and clarity\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final merged app.py and templates/*.html\n- Ensure all design_spec.md requirements are fully met and consistent\n- Do not produce candidate-specific outputs; final deliverable forms the common project codebase\n- Verify complete coverage of application features with no contradictions or missing parts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Verify candidate A implements all routes with exact page titles, element IDs, complete data file usage, navigation buttons, and backend functionality per design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate candidate B for compliance with design_spec.md, ensuring all pages, routes, element IDs, and data management features are correctly implemented.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Confirm the merged app.py and templates/*.html form a complete, coherent Flask application with all required features and no contradictory or missing elements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Run two independent validations and merge their suggested fixes into the final app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently perform comprehensive validation testing of the merged app.py and templates/*.html, \"\n        \"including syntax checks, route tests, UI element ID verification, navigation flow correctness, data file operations, and functional behavior. \"\n        \"Each produces a validation report with repair suggestions. RepairMerger consolidates both reports and applies all valid repairs to produce the final tested app.py and templates/*.html.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in validating Python Flask web applications and frontend HTML.\n\nYour goal is to independently validate the merged backend and frontend for correctness, robustness, and adherence to specifications, producing a detailed validation report with suggested fixes.\n\nTask Details:\n- Read app.py and templates/*.html from ImplementationMerger\n- Consult design_spec.md and user_task_description for requirements context\n- Verify syntax correctness and runtime execution of app.py\n- Validate all Flask routes render the correct templates with specified page titles and exact UI element IDs\n- Test all navigation buttons work correctly directing between pages as specified\n- Verify proper read/write operations for data files (users.txt, courses.txt, enrollments.txt, etc.)\n- Generate a comprehensive validation report (validation_a.md) including any defects found and detailed suggested fixes\n\nValidation Requirements:\n1. **Syntax and Runtime Validation**:\n   - Use validate_python_file and execute_python_code tools for app.py\n   - Confirm no syntax or runtime errors occur\n\n2. **Route and Template Verification**:\n   - Check each Flask route existence from design_spec.md Section 1\n   - Confirm routes load correct templates with exact page titles\n   - Validate presence and correctness of all specified element IDs in loaded templates (static and dynamic forms)\n\n3. **Navigation Testing**:\n   - Confirm navigation buttons lead to correct pages per design_spec.md flow\n   - Validate URL and link correctness in templates and redirections in app.py\n\n4. **Data File Interaction Checks**:\n   - Ensure app.py reads and writes all data files accurately per schemas\n   - Validate error handling of missing or malformed data files\n\nCritical Success Criteria:\n- Use validate_python_file and execute_python_code tools for code validation\n- Use write_text_file tool to output detailed validation_a.md report\n- Validation report must include clear suggested fixes with line references if possible\n- Focus strictly on validating given inputs and outputs; avoid implementation beyond validation\n- Observe exact file naming conventions for inputs and output report\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"validation_a.md\"}]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in user interaction and functional behavior testing of Python Flask web applications.\n\nYour goal is to independently test user interaction flows, business logic, and requirement compliance, producing a detailed validation report with repair suggestions.\n\nTask Details:\n- Read app.py and templates/*.html from ImplementationMerger\n- Consult design_spec.md and user_task_description for requirement details\n- Test user interaction flows including course browsing, enrollment, lesson progression, assignment submission, and certificate generation\n- Validate enforcement of sequential lesson completion and accurate progress tracking\n- Confirm assignment submission stores correct data with status update\n- Check automatic certificate generation upon course completion\n- Produce validation_b.md report with detailed repair suggestions for any functional issues or inconsistencies found\n\nFunctional Testing Requirements:\n1. **User Flow Validation**:\n   - Simulate navigation through dashboard, catalog, course details, my courses, learning pages\n   - Verify buttons and links behave correctly as per specifications\n\n2. **Progress and Lesson Completion**:\n   - Confirm progress calculation matches (completed lessons / total lessons) × 100\n   - Validate restriction that lessons must be completed in sequence\n   - Test marking lessons complete updates enrollments.txt properly\n\n3. **Assignment Submission Checks**:\n   - Test submission flow updates submissions.txt with correct status and timestamps\n   - Verify confirmation messages appear on successful submission\n\n4. **Certificate Generation**:\n   - Confirm that reaching 100% progress automatically creates certificate entries in certificates.txt\n   - Validate certificates page displays only completed courses\n\nCritical Success Criteria:\n- Use validate_python_file and execute_python_code tools as needed to simulate and test behaviors\n- Use write_text_file tool to save detailed validation_b.md report with suggested fixes\n- Ensure all tests align strictly with design_spec.md and user_task_description\n- Provide actionable repair advice with specific references where applicable\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [{\"type\": \"text_file\", \"name\": \"validation_b.md\"}]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in integrating multi-source validation feedback and improving Python Flask web applications.\n\nYour goal is to combine two separate validation reports into a single comprehensive repair plan, apply all valid fixes and improvements, and produce the final robust app.py and templates/*.html fully compliant with user requirements.\n\nTask Details:\n- Read validation_a.md and validation_b.md reports from ValidationEngineerA and ValidationEngineerB\n- Read current app.py and templates/*.html from ImplementationMerger\n- Consult design_spec.md and user_task_description to ensure final compliance\n- Merge all distinct suggested repairs and improvements\n- Apply corrections to app.py ensuring no syntax/runtime errors and complete route and data file handling\n- Modify templates/*.html to fix element IDs, navigation, and UI issues based on reports\n- Validate final outputs meet all original functional and UI specifications\n- Produce final app.py and templates/*.html files ready for deployment\n\nIntegration and Repair Guidelines:\n1. **Consolidation Strategy**:\n   - Combine validation suggestions preserving all distinct issues\n   - Resolve conflicts prioritizing correctness and specification adherence\n\n2. **Code Repair**:\n   - Use robust Python best practices for fixes\n   - Ensure all data file schemas are respected and error handling included\n\n3. **Frontend Repair**:\n   - Fix element IDs exactly as specified and navigation links/buttons\n   - Ensure all dynamic IDs use proper template syntax\n\n4. **Verification**:\n   - Confirm no issues remain from validation reports\n   - Maintain all original functionality and UI elements per design specification\n\nCritical Success Criteria:\n- Use write_text_file tool to save repaired app.py and templates/*.html\n- Ensure all fixes pass criteria from both validation reports\n- Final outputs must be robust, error-free, and fully compliant with user_task_description and design_spec.md\n- Do not add new features beyond scope of validation repair\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Assess validation_a.md for completeness of syntax checks, route coverage, UI element ID correctness, and backend data handling tests.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Examine validation_b.md for thoroughness of user flow validation, assignment submission, progress tracking, and certificate generation tests.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Confirm the final app.py and templates/*.html fully incorporate fixes from validation reports and remain faithful to the design_spec.md requirements.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'OnlineCourse' Web Application

## 1. Objective
Develop a comprehensive web application named 'OnlineCourse' using Python, with data managed through local text files. The application enables users to browse and enroll in courses, submit assignments, track progress, and receive certificates. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'OnlineCourse' application is Python.

## 3. Page Design

The 'OnlineCourse' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Learning Dashboard
- **Overview**: Main hub displaying enrolled courses and progress.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying user's name.
  - **ID: enrolled-courses** - Type: Div - Display of currently enrolled courses.
  - **ID: browse-courses-button** - Type: Button - Navigate to course catalog.
  - **ID: my-courses-button** - Type: Button - Navigate to my courses page.

### 2. Course Catalog Page
- **Page Title**: Available Courses
- **Overview**: Browse all available courses.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search courses.
  - **ID: course-grid** - Type: Div - Grid display of course cards.
  - **ID: view-course-button-{course_id}** - Type: Button - View course details. (반복 요소)
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

### 3. Course Details Page
- **Page Title**: Course Details
- **Overview**: Detailed information about a course including syllabus and enrollment option.
- **Elements**:
  - **ID: course-details-page** - Type: Div - Container for the course details page.
  - **ID: course-title** - Type: H1 - Display of course title.
  - **ID: course-description** - Type: Div - Full description of course content.
  - **ID: enroll-button** - Type: Button - Button to enroll in the course.
  - **ID: back-to-catalog** - Type: Button - Button to navigate back to course catalog.
- **Functionality**:
  - Enroll button creates entry in enrollments.txt with 0% initial progress
  - If already enrolled, button shows "Already Enrolled" and is disabled
  - Enrollment date is recorded as current date

### 4. My Courses Page
- **Page Title**: My Courses
- **Overview**: Display enrolled courses and progress.
- **Elements**:
  - **ID: my-courses-page** - Type: Div - Container for the my courses page.
  - **ID: courses-list** - Type: Div - List of enrolled courses with progress.
  - **ID: continue-learning-button-{course_id}** - Type: Button - Continue learning a course. (반복 요소)
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

### 5. Course Learning Page
- **Page Title**: Course Learning
- **Overview**: View course content and lessons with progress tracking.
- **Elements**:
  - **ID: learning-page** - Type: Div - Container for the course learning page.
  - **ID: lessons-list** - Type: Div - List of all lessons in the course.
  - **ID: lesson-content** - Type: Div - Display of current lesson materials.
  - **ID: mark-complete-button** - Type: Button - Button to mark current lesson as completed.
  - **ID: back-to-my-courses** - Type: Button - Button to navigate back to enrolled courses.
- **Functionality**:
  - Progress is calculated as (completed lessons / total lessons) × 100
  - Marking lesson complete updates enrollments.txt progress field
  - Course completion (100% progress) automatically generates certificate
  - Lessons must be completed in sequence

### 6. My Assignments Page
- **Page Title**: My Assignments
- **Overview**: View and submit assignments.
- **Elements**:
  - **ID: assignments-page** - Type: Div - Container for assignments page.
  - **ID: assignments-table** - Type: Table - Table displaying all assignments.
  - **ID: submit-assignment-button-{assignment_id}** - Type: Button - Submit a pending assignment. (반복 요소)
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

### 7. Submit Assignment Page
- **Page Title**: Submit Assignment
- **Overview**: Submit assignment work with text responses.
- **Elements**:
  - **ID: submit-page** - Type: Div - Container for the assignment submission page.
  - **ID: assignment-info** - Type: Div - Display of assignment title and description.
  - **ID: submission-text** - Type: Textarea - Field to input text response.
  - **ID: submit-button** - Type: Button - Button to submit the assignment.
  - **ID: back-to-assignments** - Type: Button - Button to navigate back to assignments list.
- **Functionality**:
  - Submission creates entry in submissions.txt with status "Submitted"
  - Submit date is recorded for late submission tracking
  - Confirmation message displays after successful submission

### 8. Certificates Page
- **Page Title**: My Certificates
- **Overview**: View earned course completion certificates.
- **Elements**:
  - **ID: certificates-page** - Type: Div - Container for the certificates page.
  - **ID: certificates-grid** - Type: Div - Grid display of certificate cards.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.
- **Functionality**:
  - Certificates are automatically generated when course progress reaches 100%
  - Certificate entry is added to certificates.txt with current date
  - Only completed courses appear in the grid

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: View and edit profile.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for profile page.
  - **ID: profile-email** - Type: Input - Email input field.
  - **ID: profile-fullname** - Type: Input - Full name input field.
  - **ID: update-profile-button** - Type: Button - Save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Navigate back to dashboard.

## 4. Data Storage

The 'OnlineCourse' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**: `username|email|fullname`
- **Example Data**:
  ```
  john|john@student.com|John Student
  alice|alice@instructor.com|Alice Professor
  jane|jane@student.com|Jane Learner
  ```

### 2. Courses Data
- **File Name**: `courses.txt`
- **Data Format**: `course_id|title|description|category|level|duration|status`
- **Example Data**:
  ```
  1|Python Programming|Learn Python from scratch|Programming|Beginner|40 hours|Active
  2|Web Development|Build modern websites|Web|Intermediate|60 hours|Active
  3|Data Science|Introduction to data analysis|Data|Advanced|80 hours|Active
  ```

### 3. Enrollments Data
- **File Name**: `enrollments.txt`
- **Data Format**: `enrollment_id|username|course_id|enrollment_date|progress|status`
- **Example Data**:
  ```
  1|john|1|2024-11-01|75|In Progress
  2|jane|1|2024-10-15|100|Completed
  3|john|2|2024-11-10|25|In Progress
  ```

### 4. Assignments Data
- **File Name**: `assignments.txt`
- **Data Format**: `assignment_id|course_id|title|description|due_date|max_points`
- **Example Data**:
  ```
  1|1|Python Basics Quiz|Complete the quiz on variables and data types|2024-12-01|100
  2|1|Final Project|Build a calculator application|2024-12-15|200
  ```

### 5. Submissions Data
- **File Name**: `submissions.txt`
- **Data Format**: `submission_id|assignment_id|username|submission_text|submit_date|grade|feedback`
- **Example Data**:
  ```
  1|1|john|My answers are...|2024-11-25|85|Good work!
  2|2|jane|Here is my project...|2024-11-20|95|Excellent!
  ```

### 6. Certificates Data
- **File Name**: `certificates.txt`
- **Data Format**: `certificate_id|username|course_id|issue_date`
- **Example Data**:
  ```
  1|jane|1|2024-11-22
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
            """You are a Web Application Designer with expertise in designing comprehensive specifications for Python-based web applications using local text file data storage.

Your goal is to develop a complete design candidate describing all 9 pages of the OnlineCourse app, detailing route URLs, page titles, element IDs including dynamic buttons, navigation controls, data file utilization, expected user interactions, and constraints such as enrollment status and course progress.

Task Details:
- Read user_task_description fully to understand app requirements
- Produce design_candidate_a.md covering all pages, element IDs, navigation, and data interactions
- Include detailed descriptions of buttons, dynamic IDs, page layout elements, and interaction behaviors
- Focus exclusively on your own candidate design without referencing other candidates

Design Specification Requirements:
1. **Routing and Navigation**
   - Specify exact route URLs for each page and sub-actions (e.g., enrollments, submissions)
   - Define navigation flows between pages, relating buttons and dynamic elements
2. **Page Elements**
   - List all element IDs per page, including dynamic button patterns with placeholders (e.g., view-course-button-{course_id})
   - Describe element types (div, button, input, etc.) and their purpose
3. **Data Handling**
   - Specify usage of each data file (users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt)
   - Detail how user interactions update data files (e.g., enrollment creates record, submission writes to submissions.txt)
4. **User Interactions and Constraints**
   - Define conditional behaviors like enrollment status disabling enroll button
   - Describe progress calculations, lesson completion sequences, and certificate generation triggers

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output a complete design_candidate_a.md
- Ensure all routes, elements, and navigation flows comprehensively cover user task details without omissions
- Use precise naming consistent with user requirements
- Do NOT consult other design candidates or user agents

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Designer specialized in alternative design creation for Python web apps using textual data management.

Your goal is to independently create an alternative, comprehensive design candidate describing the full OnlineCourse application including routes, page layouts, element IDs, navigation, sequencing requirements, and data handling details with local text files.

Task Details:
- Analyze the user_task_description thoroughly for app behavior, data, and UI elements
- Write design_candidate_b.md describing an alternative design meeting all functional requirements
- Include detailed route specifications, page element lists with IDs, dynamic button patterns, navigation sequences, and the logic for progress, enrollment, submission, and certificate issuance
- Do not reference or consult design_candidate_a.md or other designs—maintain design independence

Alternative Design Focus:
1. **Routes and Page Layout**
   - Document path URLs and expected page responses
   - Specify all dynamic and static element IDs per page with usage contexts
2. **Navigation Interactions**
   - Describe user flows, button behaviors, and back navigation consistently
3. **Data Handling and State Management**
   - Explain how data files are read and updated upon user actions
   - Detail assignment submission processing and status updates
4. **Behavioral Constraints**
   - Include mechanisms for lesson sequencing, progress tracking, and certificate generation conditions

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output complete design_candidate_b.md
- Cover every specified page, element, and function in detail matching app requirements
- Ensure naming consistency with the user task but provide an independent design perspective
- Maintain independence from other design candidates

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Synthesis Expert specializing in merging parallel design candidates into a final, coherent, and implementable web app specification.

Your goal is to compare and synthesize design_candidate_a.md and design_candidate_b.md, resolving any conflicts or omissions, and produce a merged design_spec.md that fully specifies the OnlineCourse app, including all accurate routes, exact page titles, element IDs (including dynamic buttons), data file usages and formats, navigation flows, progress tracking logic, and enrollment states strictly consistent with the user requirements.

Task Details:
- Read user_task_description along with design_candidate_a.md and design_candidate_b.md thoroughly
- Identify and reconcile differences in route definitions, element IDs, navigation, and functional logic
- Resolve all conflicts to produce a consistent, complete design_spec.md covering the entire application
- Explicitly include:
   - All page routes with URL patterns
   - Exact page titles and element IDs with dynamic ID patterns
   - Data file interaction specifications including update triggers and field usage
   - Navigation flows and user interaction constraints (enrollment, progress, submission, certificates)
- Ensure finalized design aligns fully with user requirements and enables error-free implementation

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final merged design_spec.md
- Maintain full fidelity and completeness of all required details from both candidate designs
- Ensure no missing or contradictory information remains
- Provide a definitive single source of truth for routing, UI elements, navigation, and data handling

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Python Flask Developer specializing in building full-stack web applications with local text file data management.

Your goal is to implement the complete OnlineCourse web application backend and frontend independently based on design_spec.md.

Task Details:
- Read user_task_description and full design_spec.md for all 9 pages, routes, page titles, element IDs, navigation flows, and data file schema
- Create isolated backend implementation in app_candidate_a.py implementing ALL Flask routes and logic exactly as specified
- Create matching HTML templates in templates_candidate_a/ directory following exact element IDs and page structure
- Handle all data files in data/ folder with exact parsing and updating logic per specifications
- Focus ONLY on your isolated implementation; do not reference or access other candidates' work

Implementation Requirements:
1. Flask Backend:
   - Implement all routes corresponding to the 9 pages in design_spec.md
   - Enforce page titles exactly as specified (e.g., <title>, <h1>)
   - Implement enrollment, progress tracking, assignments submission, certificate generation per described functionality
   - Use local pipe-delimited text files strictly as data storage (users.txt, courses.txt, enrollments.txt, etc.)
   - Follow data file formats and update logic exactly as documented
   - Navigation between pages must use proper Flask url_for calls with correct function names

2. Frontend Templates:
   - Implement templates for all pages in templates_candidate_a/ with given element IDs accurately
   - Use Jinja2 syntax for dynamic IDs for repeating elements (e.g., view-course-button-{course_id} → id="view-course-button-{{ course.course_id }}")
   - Include navigation buttons as links or form buttons, matching design requirements exactly
   - Ensure forms POST to appropriate routes for enrollments, submissions, profile updates

3. UI and Behavior:
   - Disable enrollment button if already enrolled; show "Already Enrolled" text
   - Calculate progress as specified and update enrollments.txt accordingly
   - Generate certificates automatically when progress reaches 100%
   - Maintain lesson completion sequence integrity
   - Show confirmation messages on assignment submission

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all HTML files under templates_candidate_a/
- Do not read or incorporate any other candidate's files or code
- Follow all file and variable naming conventions precisely
- Ensure full functional completeness and adherence to design_spec.md
- Focus on your independent implementation only

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Python Flask Developer specializing in full-stack web application development using local text file data stores.

Your goal is to independently implement the entire OnlineCourse Flask application backend and frontend according to design_spec.md.

Task Details:
- Study user_task_description and comprehensive design_spec.md for ALL pages, routes, UI elements, data files, and logic details
- Independently write app_candidate_b.py with all routes, backend logic, data reading/writing per specification
- Independently create templates in templates_candidate_b/ directory following exact element IDs, page titles, and structures
- Implement full enrollment management, assignment submissions, progress tracking, certificates, and profile management
- Use data stored in local pipe-delimited text files precisely as outlined
- Your implementation must be fully isolated; do not consider or depend on ImplementationEngineerA's output

Implementation Guidelines:
1. Backend:
   - Implement every Flask route described for the 9 application pages
   - Use correct function names for Flask routes consistent with design_spec.md
   - Implement enrollment checks, progress calculations, certificate generation exactly as specified
   - Perform file I/O with data files correctly handling parsing and updates without headers

2. Templates:
   - Implement HTML templates using requested element IDs (including dynamic IDs) with Jinja2 templating
   - Add navigation buttons that link to or post to appropriate routes
   - Render user and course data dynamically according to specifications

3. Usability:
   - Disable the enroll button if enrolled; show "Already Enrolled"
   - Use computed progress for display and updating enrollments.txt progress field
   - Enforce lesson sequence completion before allowing mark complete
   - Provide confirmation messages on successful submissions

CRITICAL REQUIREMENTS:
- Save output files using write_text_file tool: app_candidate_b.py and templates_candidate_b/*.html
- Strictly follow naming conventions and data schema formats
- Do not integrate or read ImplementationEngineerA's files or code
- Ensure full correctness, completeness, and adherence to specification independently

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging parallel Python Flask implementations into a unified deployment-ready project.

Your goal is to analyze two fully independent implementations of the OnlineCourse Flask app and combine their strongest, most correct elements into a final app.py and templates directory.

Task Details:
- Review user_task_description and design_spec.md for project scope and detailed requirements
- Analyze app_candidate_a.py and app_candidate_b.py backend code; identify identical, conflicting, or complementary route implementations and logic
- Review templates_candidate_a/*.html and templates_candidate_b/*.html; evaluate element IDs, page titles, navigation flows, and adherence to specification
- Merge backend logic resolving conflicts by adopting the strongest implementation per route, data handling, error management, correctness, and completeness
- Merge frontend templates ensuring complete coverage of all element IDs, consistent navigation, and compliance with design_spec.md
- Ensure merged app.py does not depend on candidate folders or files; fully integrated and runnable
- Maintain all specified behaviors: enrollment logic, progress tracking, assignment submissions, certificates generation, and profile management

Merging Guidelines:
1. Backend:
   - Consolidate routes by selecting best-functioning, fully conformant implementations
   - Harmonize data file reading/writing with reliable, consistent code
   - Preserve any error handling improvements and completeness

2. Frontend:
   - Combine template components to include all required elements and IDs
   - Use consistent navigation and page titles as per design_spec.md
   - Remove duplicate or conflicting template elements in merged output

3. Integration:
   - Final app.py and templates/*.html must form a single coherent Flask application
   - Outputs must be deployable with no unresolved references or missing elements
   - Follow Python and Flask best practices for maintainability and clarity

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final merged app.py and templates/*.html
- Ensure all design_spec.md requirements are fully met and consistent
- Do not produce candidate-specific outputs; final deliverable forms the common project codebase
- Verify complete coverage of application features with no contradictions or missing parts

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in validating Python Flask web applications and frontend HTML.

Your goal is to independently validate the merged backend and frontend for correctness, robustness, and adherence to specifications, producing a detailed validation report with suggested fixes.

Task Details:
- Read app.py and templates/*.html from ImplementationMerger
- Consult design_spec.md and user_task_description for requirements context
- Verify syntax correctness and runtime execution of app.py
- Validate all Flask routes render the correct templates with specified page titles and exact UI element IDs
- Test all navigation buttons work correctly directing between pages as specified
- Verify proper read/write operations for data files (users.txt, courses.txt, enrollments.txt, etc.)
- Generate a comprehensive validation report (validation_a.md) including any defects found and detailed suggested fixes

Validation Requirements:
1. **Syntax and Runtime Validation**:
   - Use validate_python_file and execute_python_code tools for app.py
   - Confirm no syntax or runtime errors occur

2. **Route and Template Verification**:
   - Check each Flask route existence from design_spec.md Section 1
   - Confirm routes load correct templates with exact page titles
   - Validate presence and correctness of all specified element IDs in loaded templates (static and dynamic forms)

3. **Navigation Testing**:
   - Confirm navigation buttons lead to correct pages per design_spec.md flow
   - Validate URL and link correctness in templates and redirections in app.py

4. **Data File Interaction Checks**:
   - Ensure app.py reads and writes all data files accurately per schemas
   - Validate error handling of missing or malformed data files

Critical Success Criteria:
- Use validate_python_file and execute_python_code tools for code validation
- Use write_text_file tool to output detailed validation_a.md report
- Validation report must include clear suggested fixes with line references if possible
- Focus strictly on validating given inputs and outputs; avoid implementation beyond validation
- Observe exact file naming conventions for inputs and output report

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in user interaction and functional behavior testing of Python Flask web applications.

Your goal is to independently test user interaction flows, business logic, and requirement compliance, producing a detailed validation report with repair suggestions.

Task Details:
- Read app.py and templates/*.html from ImplementationMerger
- Consult design_spec.md and user_task_description for requirement details
- Test user interaction flows including course browsing, enrollment, lesson progression, assignment submission, and certificate generation
- Validate enforcement of sequential lesson completion and accurate progress tracking
- Confirm assignment submission stores correct data with status update
- Check automatic certificate generation upon course completion
- Produce validation_b.md report with detailed repair suggestions for any functional issues or inconsistencies found

Functional Testing Requirements:
1. **User Flow Validation**:
   - Simulate navigation through dashboard, catalog, course details, my courses, learning pages
   - Verify buttons and links behave correctly as per specifications

2. **Progress and Lesson Completion**:
   - Confirm progress calculation matches (completed lessons / total lessons) × 100
   - Validate restriction that lessons must be completed in sequence
   - Test marking lessons complete updates enrollments.txt properly

3. **Assignment Submission Checks**:
   - Test submission flow updates submissions.txt with correct status and timestamps
   - Verify confirmation messages appear on successful submission

4. **Certificate Generation**:
   - Confirm that reaching 100% progress automatically creates certificate entries in certificates.txt
   - Validate certificates page displays only completed courses

Critical Success Criteria:
- Use validate_python_file and execute_python_code tools as needed to simulate and test behaviors
- Use write_text_file tool to save detailed validation_b.md report with suggested fixes
- Ensure all tests align strictly with design_spec.md and user_task_description
- Provide actionable repair advice with specific references where applicable

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in integrating multi-source validation feedback and improving Python Flask web applications.

Your goal is to combine two separate validation reports into a single comprehensive repair plan, apply all valid fixes and improvements, and produce the final robust app.py and templates/*.html fully compliant with user requirements.

Task Details:
- Read validation_a.md and validation_b.md reports from ValidationEngineerA and ValidationEngineerB
- Read current app.py and templates/*.html from ImplementationMerger
- Consult design_spec.md and user_task_description to ensure final compliance
- Merge all distinct suggested repairs and improvements
- Apply corrections to app.py ensuring no syntax/runtime errors and complete route and data file handling
- Modify templates/*.html to fix element IDs, navigation, and UI issues based on reports
- Validate final outputs meet all original functional and UI specifications
- Produce final app.py and templates/*.html files ready for deployment

Integration and Repair Guidelines:
1. **Consolidation Strategy**:
   - Combine validation suggestions preserving all distinct issues
   - Resolve conflicts prioritizing correctness and specification adherence

2. **Code Repair**:
   - Use robust Python best practices for fixes
   - Ensure all data file schemas are respected and error handling included

3. **Frontend Repair**:
   - Fix element IDs exactly as specified and navigation links/buttons
   - Ensure all dynamic IDs use proper template syntax

4. **Verification**:
   - Confirm no issues remain from validation reports
   - Maintain all original functionality and UI elements per design specification

Critical Success Criteria:
- Use write_text_file tool to save repaired app.py and templates/*.html
- Ensure all fixes pass criteria from both validation reports
- Final outputs must be robust, error-free, and fully compliant with user_task_description and design_spec.md
- Do not add new features beyond scope of validation repair

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
        ("DesignMerger", """Verify design_candidate_a.md covers every page route, dynamic element IDs including repeated buttons, data file interactions, and navigation logic as per user requirements.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Verify design_candidate_b.md covers the app functionality and data flow in detail, matches requirement constraints and includes all specified pages with correct elements and behavior before merging.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Confirm design_spec.md fully integrates both candidate designs into a consistent, implementable specification with no missing or conflicting details regarding routes, page titles, elements, data files, and required functionality.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Verify candidate A implements all routes with exact page titles, element IDs, complete data file usage, navigation buttons, and backend functionality per design_spec.md.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate candidate B for compliance with design_spec.md, ensuring all pages, routes, element IDs, and data management features are correctly implemented.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Confirm the merged app.py and templates/*.html form a complete, coherent Flask application with all required features and no contradictory or missing elements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Assess validation_a.md for completeness of syntax checks, route coverage, UI element ID correctness, and backend data handling tests.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Examine validation_b.md for thoroughness of user flow validation, assignment submission, progress tracking, and certificate generation tests.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Confirm the final app.py and templates/*.html fully incorporate fixes from validation reports and remain faithful to the design_spec.md requirements.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'design_spec.md'}])
    ]

}



# Orchestration Functions
async def design_specification_phase():
    DesignAnalystA = build_resilient_agent(
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

    # Parallel execution of DesignAnalystA and DesignAnalystB to create independent design candidates
    await asyncio.gather(
        execute(DesignAnalystA, "Create design_candidate_a.md: complete design of all 9 pages including routes, element IDs, navigation, data handling, and interactions."),
        execute(DesignAnalystB, "Create design_candidate_b.md: alternative comprehensive design of all app pages, routes, elements, navigation, data management, and interaction logic.")
    )

    # Read outputs for merger
    design_a_output, design_b_output = "", ""
    try:
        design_a_output = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_b_output = open("design_candidate_b.md").read()
    except:
        pass

    # Merge designs into final design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_a_output}\n\n=== DesignAnalystB ===\n{design_b_output}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    ImplementationEngineerA = build_resilient_agent(
        agent_name="ImplementationEngineerA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=60
    )
    ImplementationEngineerB = build_resilient_agent(
        agent_name="ImplementationEngineerB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=60
    )
    ImplementationMerger = build_resilient_agent(
        agent_name="ImplementationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=380,
        failure_threshold=1,
        recovery_time=45
    )

    # Parallel execution for independent implementations
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Implement complete OnlineCourse app independently. "
                "Create app_candidate_a.py and templates_candidate_a/*.html with all 9 pages' Flask routes, exact page titles, element IDs, navigation, and data file usage as specified."),
        execute(ImplementationEngineerB,
                "Implement entire OnlineCourse Flask app independently. "
                "Write app_candidate_b.py and templates_candidate_b/*.html following all specifications for backend, frontend, data management, enrollment, progress tracking, and UI elements.")
    )

    # Read the two candidate backends and template files for merging
    app_candidate_a_code, app_candidate_b_code = "", ""
    templates_candidate_a_html, templates_candidate_b_html = "", ""
    try:
        app_candidate_a_code = open("app_candidate_a.py").read()
    except:
        pass
    try:
        app_candidate_b_code = open("app_candidate_b.py").read()
    except:
        pass
    try:
        # Reading templates_candidate_a/*.html content as single string for injection (concatenate all files)
        import glob
        candidate_a_files = glob.glob("templates_candidate_a/*.html")
        candidate_a_contents = []
        for file in candidate_a_files:
            try:
                candidate_a_contents.append(open(file).read())
            except:
                pass
        templates_candidate_a_html = "\n\n".join(candidate_a_contents)
    except:
        pass
    try:
        # Reading templates_candidate_b/*.html content as single string for injection
        import glob
        candidate_b_files = glob.glob("templates_candidate_b/*.html")
        candidate_b_contents = []
        for file in candidate_b_files:
            try:
                candidate_b_contents.append(open(file).read())
            except:
                pass
        templates_candidate_b_html = "\n\n".join(candidate_b_contents)
    except:
        pass

    # Execute merge phase with all inputs
    await execute(ImplementationMerger,
                  f"Merge two independent OnlineCourse app implementations.\n"
                  f"User task and design_spec.md included.\n"
                  f"\n=== app_candidate_a.py ===\n{app_candidate_a_code}\n"
                  f"\n=== templates_candidate_a/*.html ===\n{templates_candidate_a_html}\n"
                  f"\n=== app_candidate_b.py ===\n{app_candidate_b_code}\n"
                  f"\n=== templates_candidate_b/*.html ===\n{templates_candidate_b_html}\n"
                  "Produce unified final app.py and templates/*.html with full integration, conflict resolution, best codes combined, and full functional completeness following design_spec.md.")
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    # Create agents
    ValidationEngineerA = build_resilient_agent(
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

    # Read file artifacts for injection before RepairMerger execution
    app_py_content = ""
    templates_content = ""
    design_spec_content = ""
    user_task_description = ""

    try:
        app_py_content = open("app.py").read()
    except:
        pass
    try:
        import glob
        template_files = glob.glob("templates/*.html")
        templates_aggregate = []
        for tpl_file in template_files:
            try:
                content = open(tpl_file).read()
                templates_aggregate.append(f"=== {tpl_file} ===\n{content}\n")
            except:
                pass
        templates_content = "\n".join(templates_aggregate)
    except:
        pass
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    try:
        entries = CONTEXT.get("user_task_description", [])
        user_task_description = entries[-1]["content"] if entries else ""
    except:
        pass

    # Parallel validation execution
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate backend and frontend functionality independently, produce validation_a.md report."),
        execute(ValidationEngineerB,
                "Independently test user flows, progress tracking, assignment and certificate behavior, produce validation_b.md report.")
    )

    # Read validation reports for RepairMerger input injection
    validation_a_content = ""
    validation_b_content = ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # RepairMerger execution with injected contents
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_content}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_content}\n\n"
                  f"=== Current app.py ===\n{app_py_content}\n\n"
                  f"=== Current Templates ===\n{templates_content}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== User Task Description ===\n{user_task_description}")
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
