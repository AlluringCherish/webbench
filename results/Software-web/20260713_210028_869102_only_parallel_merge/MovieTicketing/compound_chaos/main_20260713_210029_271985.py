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
# 20260713_210029_271985/main_20260713_210029_271985.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Produce two independent complete web design specifications for MovieTicketing app and merge into design_spec.md\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently produce full design specifications in markdown format covering all 8 pages, \"\n        \"route definitions, exact page titles, element IDs, navigation buttons, data sources, and file organization; DesignMerger reads both \"\n        \"and consolidates a single design_spec.md ensuring full coverage and correctness.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Design Specialist with expertise in creating comprehensive design documents for Python-based web apps.\n\nYour goal is to produce a detailed web app design specification for the MovieTicketing application that fulfills the full user requirements, enabling independent implementation.\n\nTask Details:\n- Read user_task_description to extract all required pages, UI elements, navigation flows, routes, and data file usages\n- Produce design_candidate_a.md including exact route endpoints, page titles, all requested element IDs, and navigation starting from Dashboard as root\n- Include local text file data handling specifications and UI element definitions\n- Do not consult or include information from other design variants\n\n**Specification Requirements:**\n\n1. **Page and Route Definitions**\n   - Define all 8 pages with exact URL route paths (e.g., '/', '/catalog', '/movie/<int:movie_id>')\n   - Specify HTTP verbs (GET/POST) for each route\n   - Include the exact page titles as requested\n\n2. **UI Element Specification**\n   - List all element IDs for each page exactly as specified\n   - Describe element types (Div, Button, Input, Dropdown, Table, etc.)\n   - Specify dynamic ID patterns where applicable (e.g., view-movie-button-{movie_id})\n\n3. **Navigation Flow**\n   - Define navigation buttons and their target routes\n   - Emphasize starting point is the Dashboard page\n   - Include detail on navigation from buttons on each page\n\n4. **Data Source and File Organization**\n   - Specify local text file use and formats per user requirements\n   - Map data files to pages or functionalities that consume them\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md\n- Follow the user requirements strictly without additions\n- Use markdown format with clear headings and subsection structure\n- Ensure all page and element naming matches user task exactly\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Design Specialist expert in detailed, implementation-focused design specifications for Python web apps.\n\nYour goal is to independently produce a high-quality detailed design for the MovieTicketing application emphasizing local text file data handling, exact routes, page titles, element IDs, and navigation starting at the Dashboard page.\n\nTask Details:\n- Read user_task_description thoroughly to identify all required pages, routes, UI elements, and local data files\n- Produce an alternative design document design_candidate_b.md covering the full spec without referencing other designs\n- Emphasize precise file-based data handling in the design\n- Provide exact route paths, HTTP methods, page titles, element IDs, and navigation button behaviors\n\n**Design Focus Areas:**\n\n1. **Route and Page Definitions**\n   - Detail each route path and HTTP method\n   - Specify exact page titles as required\n\n2. **UI Element Details**\n   - Enumerate all element IDs on each page, types, and description\n   - Identify dynamic element IDs with pattern explanations\n\n3. **Navigation Buttons**\n   - Map out navigation flow originating from the Dashboard page\n   - Describe each button target route and expected behavior\n\n4. **Data Files Usage**\n   - Clarify usage of local text files per feature/page\n   - Specify data formats and relationships with UI components\n\nCRITICAL REQUIREMENTS:\n- Save the output exclusively as design_candidate_b.md using write_text_file tool\n- Strict adherence to user task requirements; no assumptions beyond provided data\n- Use markdown format with organized headings and detailed descriptions\n- Exact naming and page title consistency required\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Web Application Design Specialist skilled in consolidating multiple design documents into a single comprehensive specification.\n\nYour goal is to consolidate design_candidate_a.md and design_candidate_b.md into a unified, consistent, and implementation-ready design_spec.md for the MovieTicketing app.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md thoroughly\n- Reconcile and merge differences ensuring no omission of any page, route, element ID, navigation button, or local file usage\n- Ensure the merged design_spec.md includes complete coverage of all 8 pages with exact requested routes, element IDs, navigation, and data source specifications\n- Resolve conflicts by selecting the most complete and accurate elements from both candidates\n- Organize the final document in clear markdown structure optimized for direct implementation\n\n**Merger Guidelines:**\n\n1. **Completeness Check**\n   - Verify all pages are represented with exact route paths and HTTP methods\n   - Confirm all UI elements with their IDs and types are included accurately\n   - Confirm navigation buttons and flows are correct starting from Dashboard page\n\n2. **Consistency Enforcement**\n   - Align naming conventions for IDs, routes, and page titles consistently\n   - Ensure local text file data handling descriptions are complete and coherent\n   - Remove duplications and contradictions carefully\n\n3. **Output Format**\n   - Produce a single markdown file design_spec.md suitable for developers to implement without ambiguity\n   - Use headings and subsections per page, route, UI elements, and data handling\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save merged result as design_spec.md\n- Preserve naming and structural consistency throughout the document\n- Ensure the final spec aligns fully with user requirements\n- Maintain clarity and completeness for independent implementation\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_a.md for thoroughness, route correctness, exact requested page titles, element IDs, and navigational flow.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Check design_candidate_b.md for completeness, local file handling consistency, and adherence to stated page and element requirements.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Verify design_spec.md is comprehensive, unambiguous, and suitable for direct code implementation.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Generate two independent full Flask implementations of MovieTicketing application based on design_spec.md and merge into app.py and templates/*.html\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently write full implementations of the Python Flask app plus all associated \"\n        \"templates, adhering strictly to design_spec.md; ImplementationMerger compares both implementations, resolves conflicts, and produces \"\n        \"final app.py and templates/*.html ready for validation.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python Flask web application development.\n\nYour goal is to develop a complete and fully functional Python Flask application implementing all backend logic and frontend templates according to specification documents, ensuring local data file management and navigation flow starting at Dashboard page.\n\nTask Details:\n- Read user_task_description and design_spec.md thoroughly\n- Produce app_candidate_a.py implementing all Flask routes, data loading/saving from local data/*.txt files as per specification\n- Develop all HTML templates with exact element IDs, navigation links, and page titles matching specification\n- Maintain separation of backend logic and templates while ensuring integration correctness\n- Manage data files in data/ directory using specified pipe-delimited formats\n\nImplementation Requirements:\n1. **Flask Application Structure and Routing:**\n   - Implement all routes specified in design_spec.md with accurate HTTP methods and route names\n   - Ensure root route redirects to Dashboard page as entry point\n2. **Data Handling:**\n   - Load and manage data via reading and writing specified local text files with exact field order and delimiters\n   - Handle missing or malformed data gracefully\n3. **Frontend Templates:**\n   - Implement templates with correct file paths and names under templates_candidate_a/\n   - Include all required element IDs with exact naming and dynamic ID templates for repeated elements\n   - Support navigation flows linking pages using url_for with route function names\n4. **UI and UX:**\n   - Ensure all UI elements correspond to specification including buttons, inputs, dropdowns, and display areas\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_a.py and all template files in templates_candidate_a/\n- Follow specification exactly for route names, element IDs, and data file formats\n- Do not introduce functionality or pages beyond specification\n- Ensure templates and backend integrate properly for a working application\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python Flask web application development.\n\nYour goal is to independently produce a complete Python Flask backend and accompanying frontend templates strictly adhering to design specifications, including all required routes, page components, and local file data handling.\n\nTask Details:\n- Review user_task_description and design_spec.md carefully\n- Implement app_candidate_b.py with all Flask routes and data file operations as defined\n- Create templates_candidate_b/*.html with all UI elements, page titles, and navigation mechanisms matching specification\n- Ensure local data file management in data/ directory using exact schema and delimiters\n- Maintain complete isolation from ImplementationEngineerA's outputs; work independently\n\nDevelopment Guidelines:\n1. **Routing and Backend Logic:**\n   - Include all routes with HTTP methods exactly as specified\n   - Implement data loading and saving from text files per design specs\n2. **Template Implementation:**\n   - Use Jinja2 templating with exact element IDs for static and dynamic content\n   - Replicate navigation flows using url_for calls with correct route names\n3. **Data Integration:**\n   - Use pipe-delimited parsing matching field order from design specifications\n   - Handle errors and edge cases gracefully to prevent crashes\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save app_candidate_b.py and related templates in templates_candidate_b/\n- Adhere strictly to design_spec.md route names, element IDs, and data formats\n- Do not consult or reuse code from other implementation agent\n- Deliver fully functioning Flask app and matched templates for merging\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Engineer specializing in code merging and integration of Python Flask applications.\n\nYour goal is to analyze two independent complete Flask app implementations and corresponding template sets, compare against design_spec.md for correctness, resolve conflicts, and merge into a stable final app.py and templates/*.html bundle.\n\nTask Details:\n- Read user_task_description, design_spec.md, app_candidate_a.py, app_candidate_b.py, templates_candidate_a/*.html, and templates_candidate_b/*.html\n- Identify discrepancies between both implementations and resolve route conflicts, data file handling differences, and UI element mismatches\n- Ensure final merged app.py supports all routes and features exactly as per specification with consistent route names and data access\n- Produce templates/*.html that consolidate both candidates’ UI elements, preserving all required element IDs, page titles, and navigation flows\n- Normalize file structure: app.py at root, templates/*.html in templates/ directory\n\nMerge Guidelines:\n1. **Code Consolidation:**\n   - Reconcile function implementations ensuring comprehensive route coverage without duplication\n   - Retain best coding practices and readability\n2. **Template Unification:**\n   - Merge templates preserving all required elements and dynamic ID patterns\n   - Resolve conflicting element IDs and content by specification precedence\n3. **Data Handling:**\n   - Maintain correct local file access and parsing as per design_spec.md across all modules\n4. **Navigation and Entry Point:**\n   - Confirm root route redirects to Dashboard page post-merge\n   - Verify navigation works seamlessly across all pages\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to output final app.py and all templates/*.html files\n- Ensure outputs conform exactly to design_spec.md requirements and integrate all features from both candidates\n- Deliver production-ready Flask application suitable for validation and deployment\n- Do not include source candidate files in output; only final merged artifacts\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Validate app_candidate_a.py and templates_candidate_a/*.html fully implement design_spec.md with correct routes, titles, elements, and local file usage.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate app_candidate_b.py and templates_candidate_b/*.html for adherence to design_spec.md and functional correctness including navigation starting from Dashboard.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Ensure final app.py and templates/*.html meet design specification and are runnable without errors.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Perform two independent validations of final app.py and templates/*.html and merge repairs into the final deployable application\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate the final merged app.py and templates/*.html by testing route availability, \"\n        \"UI correctness, local data file loading, and interaction flows; RepairMerger consumes reports and implementation artifacts, applies all valid fixes, and \"\n        \"outputs the final verified app.py and templates/*.html for deployment.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask web application validation.\n\nYour goal is to perform thorough validation of Flask backend code and associated HTML templates to ensure proper syntax, route accessibility, UI correctness, and data file handling.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and all templates/*.html from context\n- Validate app.py syntax, Flask application startup, and all specified routes are accessible\n- Verify page titles and all element IDs exist exactly as specified in design_spec.md\n- Confirm local text file data loading correctness and UI navigation starting on Dashboard\n- Output validation_a.md detailing validation results and suggested fixes\n\nValidation Requirements:\n1. **Syntax and Startup Checks**\n   - Use validate_python_file to confirm app.py parses and runs without errors\n   - Confirm Flask app runs and listens on expected port\n\n2. **Route and Navigation Testing**\n   - Test accessibility of all routes defined in design_spec.md\n   - Confirm root route redirects to Dashboard page\n\n3. **UI Verification**\n   - Check that page titles in all templates match design_spec.md exactly\n   - Verify presence and correctness of all element IDs, including dynamic IDs with proper patterns\n\n4. **Data Handling**\n   - Ensure app.py loads all local text file data as per design_spec.md specifications without errors\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools to perform validations\n- Use write_text_file tool to save detailed validation_a.md report\n- Output MUST be saved as validation_a.md with comprehensive and clear findings\n- Focus strictly on ValidationEngineerA scope without suggesting code edits in this phase\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in web user interface and functional flow validation for Flask applications.\n\nYour goal is to independently test the UI and user flows of the application including booking processes, showtime filtering, seat selection, booking history, and theater info displays, ensuring all interface elements and navigation conform exactly to design specifications.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, and all templates/*.html from context\n- Test booking flow correctness: movie selection, showtime filtering, seat selection, booking confirmation\n- Verify booking history presentation including filtering and navigation\n- Confirm theater information page displays correctly with filters and navigation\n- Validate that all UI elements exist with correct IDs, including dynamic elements\n- Confirm navigation buttons properly route back to Dashboard from all relevant pages\n- Output validation_b.md with detailed issues found and suggestions for improvements\n\nValidation Requirements:\n1. **User Flow Testing**\n   - Simulate user interactions for complete booking from Dashboard through confirmation\n   - Verify showtime filtering by theater and date works correctly\n   - Test seat availability display and selection interface\n\n2. **Data Presentation Verification**\n   - Validate booking history page content, filters, and navigation buttons\n   - Check that theater information and filtering displays correct data as per design_spec.md\n\n3. **UI Elements and Navigation**\n   - Verify all element IDs match design_spec.md including dynamic patterns\n   - Confirm that back-to-dashboard buttons navigate correctly without errors\n\nCRITICAL REQUIREMENTS:\n- Use validate_python_file and execute_python_code tools as needed for backend validation supporting UI tests\n- Use write_text_file tool to save detailed validation_b.md report with actionable feedback\n- Output MUST be saved as validation_b.md with clear issue descriptions and improvement recommendations\n- Focus strictly on ValidationEngineerB scope; do not implement fixes here\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask web application maintenance and codebase merging.\n\nYour goal is to aggregate findings from multiple validation reports, reconcile suggested repairs, and update app.py and templates/*.html to fix defects and improve adherence to design specifications, producing the final deployable application.\n\nTask Details:\n- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md from context\n- Analyze all reported issues and suggested fixes from validation reports\n- Update app.py to fix defects related to route handling, data loading, and application stability\n- Modify templates/*.html to correct UI element IDs, page titles, navigation flows, and user interaction components\n- Ensure final implementations fully comply with design_spec.md requirements and pass all validation checks\n- Output the updated and verified app.py and templates/*.html for deployment\n\nRepair and Merge Requirements:\n1. **Consolidated Issue Resolution**\n   - Prioritize fixes based on severity and validation consensus\n   - Avoid introducing new bugs or removing required features\n\n2. **Code and Template Update Best Practices**\n   - Maintain consistent naming conventions and coding style\n   - Update dynamic element IDs and navigation logic to match design spec precisely\n\n3. **Final Validation**\n   - Confirm all fixes are integrated and app functions correctly end-to-end\n   - Prepare codebase for deployment with stable, tested state\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool exclusively to save updated app.py and templates/*.html\n- Do NOT produce validation or review reports; focus solely on merging and repairs\n- Deliverable files MUST be named exactly app.py and templates/*.html\n- Maintain full compliance with design_spec.md element IDs, routes, and data schemas\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Verify validation_a.md for reproducible test results and actionable fixes relating to routes, UI IDs, and local file data.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Confirm validation_b.md contains detailed tests for user flows and UI elements, with clear guidance for corrections.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Validate that final app.py and templates/*.html resolve all reported issues while preserving original design integrity from design_spec.md.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'MovieTicketing' Web Application

## 1. Objective
Develop a comprehensive web application named 'MovieTicketing' using Python, with data managed through local text files. The application enables users to browse movies, view showtimes, select seats, book tickets, view booking history, and manage theater information. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'MovieTicketing' application is Python.

## 3. Page Design

The 'MovieTicketing' web application will consist of the following eight pages:

### 1. Dashboard Page
- **Page Title**: Movie Ticketing Dashboard
- **Overview**: The main hub displaying featured movies, upcoming releases, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-movies** - Type: Div - Display of featured movie recommendations.
  - **ID: browse-movies-button** - Type: Button - Button to navigate to movie catalog page.
  - **ID: view-bookings-button** - Type: Button - Button to navigate to booking history page.
  - **ID: showtimes-button** - Type: Button - Button to navigate to showtimes page.

### 2. Movie Catalog Page
- **Page Title**: Movie Catalog
- **Overview**: A page displaying all available movies with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search movies by title or genre.
  - **ID: genre-filter** - Type: Dropdown - Dropdown to filter by genre (Action, Comedy, Drama, Horror, etc.).
  - **ID: movies-grid** - Type: Div - Grid displaying movie cards with poster, title, rating, and duration.
  - **ID: view-movie-button-{movie_id}** - Type: Button - Button to view movie details (each movie card has this).

### 3. Movie Details Page
- **Page Title**: Movie Details
- **Overview**: A page displaying detailed information about a specific movie.
- **Elements**:
  - **ID: movie-details-page** - Type: Div - Container for the movie details page.
  - **ID: movie-title** - Type: H1 - Display movie title.
  - **ID: movie-director** - Type: Div - Display movie director.
  - **ID: movie-rating** - Type: Div - Display movie rating.
  - **ID: movie-description** - Type: Div - Display movie description.
  - **ID: select-showtime-button** - Type: Button - Button to proceed to showtime selection.

### 4. Showtime Selection Page
- **Page Title**: Select Showtime
- **Overview**: A page displaying available showtimes for the selected movie in different theaters.
- **Elements**:
  - **ID: showtime-page** - Type: Div - Container for the showtime page.
  - **ID: showtimes-list** - Type: Div - List of available showtimes with date, time, theater, and price.
  - **ID: theater-filter** - Type: Dropdown - Dropdown to filter showtimes by theater.
  - **ID: date-filter** - Type: Input - Field to filter showtimes by date.
  - **ID: select-showtime-button-{showtime_id}** - Type: Button - Button to select a specific showtime.

### 5. Seat Selection Page
- **Page Title**: Select Seats
- **Overview**: A page for users to select seats from an interactive seat map.
- **Elements**:
  - **ID: seat-selection-page** - Type: Div - Container for the seat selection page.
  - **ID: seat-map** - Type: Div - Interactive seat map showing available and booked seats.
  - **ID: selected-seats-display** - Type: Div - Display of currently selected seats.
  - **ID: seat-{row}{col}** - Type: Button - Individual seat button (e.g., seat-A1, seat-B3).
  - **ID: proceed-booking-button** - Type: Button - Button to proceed to booking confirmation.

### 6. Booking Confirmation Page
- **Page Title**: Booking Confirmation
- **Overview**: A page for users to review booking details and complete the purchase.
- **Elements**:
  - **ID: confirmation-page** - Type: Div - Container for the confirmation page.
  - **ID: booking-summary** - Type: Div - Summary of booking details (movie, showtime, seats, total).
  - **ID: customer-name** - Type: Input - Field to input customer name.
  - **ID: customer-email** - Type: Input - Field to input customer email.
  - **ID: confirm-booking-button** - Type: Button - Button to confirm and complete booking.

### 7. Booking History Page
- **Page Title**: Booking History
- **Overview**: A page displaying all previous bookings with ticket information.
- **Elements**:
  - **ID: bookings-page** - Type: Div - Container for the bookings page.
  - **ID: bookings-table** - Type: Table - Table displaying bookings with booking ID, movie, date, seats, and status.
  - **ID: view-booking-button-{booking_id}** - Type: Button - Button to view booking details (each booking has this).
  - **ID: status-filter** - Type: Dropdown - Dropdown to filter by status (All, Confirmed, Cancelled, Completed).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Theater Information Page
- **Page Title**: Theater Information
- **Overview**: A page displaying information about theaters and their facilities.
- **Elements**:
  - **ID: theater-page** - Type: Div - Container for the theater page.
  - **ID: theaters-list** - Type: Div - List of all theaters with location, screens, and facilities.
  - **ID: theater-location-filter** - Type: Dropdown - Dropdown to filter theaters by location.
  - **ID: facilities-display** - Type: Div - Display of theater facilities and amenities.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'MovieTicketing' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Movies Data
- **File Name**: `movies.txt`
- **Data Format**:
  ```
  movie_id|title|director|genre|rating|duration|description|release_date
  ```
- **Example Data**:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### 2. Theaters Data
- **File Name**: `theaters.txt`
- **Data Format**:
  ```
  theater_id|theater_name|location|city|screens|facilities
  ```
- **Example Data**:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### 3. Showtimes Data
- **File Name**: `showtimes.txt`
- **Data Format**:
  ```
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
  ```
- **Example Data**:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### 4. Seats Data
- **File Name**: `seats.txt`
- **Data Format**:
  ```
  seat_id|theater_id|screen_id|row|column|seat_type|status
  ```
- **Example Data**:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### 5. Bookings Data
- **File Name**: `bookings.txt`
- **Data Format**:
  ```
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
  ```
- **Example Data**:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### 6. Genres Data
- **File Name**: `genres.txt`
- **Data Format**:
  ```
  genre_id|genre_name|description
  ```
- **Example Data**:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
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
            """You are a Web Application Design Specialist with expertise in creating comprehensive design documents for Python-based web apps.

Your goal is to produce a detailed web app design specification for the MovieTicketing application that fulfills the full user requirements, enabling independent implementation.

Task Details:
- Read user_task_description to extract all required pages, UI elements, navigation flows, routes, and data file usages
- Produce design_candidate_a.md including exact route endpoints, page titles, all requested element IDs, and navigation starting from Dashboard as root
- Include local text file data handling specifications and UI element definitions
- Do not consult or include information from other design variants

**Specification Requirements:**

1. **Page and Route Definitions**
   - Define all 8 pages with exact URL route paths (e.g., '/', '/catalog', '/movie/<int:movie_id>')
   - Specify HTTP verbs (GET/POST) for each route
   - Include the exact page titles as requested

2. **UI Element Specification**
   - List all element IDs for each page exactly as specified
   - Describe element types (Div, Button, Input, Dropdown, Table, etc.)
   - Specify dynamic ID patterns where applicable (e.g., view-movie-button-{movie_id})

3. **Navigation Flow**
   - Define navigation buttons and their target routes
   - Emphasize starting point is the Dashboard page
   - Include detail on navigation from buttons on each page

4. **Data Source and File Organization**
   - Specify local text file use and formats per user requirements
   - Map data files to pages or functionalities that consume them

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md
- Follow the user requirements strictly without additions
- Use markdown format with clear headings and subsection structure
- Ensure all page and element naming matches user task exactly

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Design Specialist expert in detailed, implementation-focused design specifications for Python web apps.

Your goal is to independently produce a high-quality detailed design for the MovieTicketing application emphasizing local text file data handling, exact routes, page titles, element IDs, and navigation starting at the Dashboard page.

Task Details:
- Read user_task_description thoroughly to identify all required pages, routes, UI elements, and local data files
- Produce an alternative design document design_candidate_b.md covering the full spec without referencing other designs
- Emphasize precise file-based data handling in the design
- Provide exact route paths, HTTP methods, page titles, element IDs, and navigation button behaviors

**Design Focus Areas:**

1. **Route and Page Definitions**
   - Detail each route path and HTTP method
   - Specify exact page titles as required

2. **UI Element Details**
   - Enumerate all element IDs on each page, types, and description
   - Identify dynamic element IDs with pattern explanations

3. **Navigation Buttons**
   - Map out navigation flow originating from the Dashboard page
   - Describe each button target route and expected behavior

4. **Data Files Usage**
   - Clarify usage of local text files per feature/page
   - Specify data formats and relationships with UI components

CRITICAL REQUIREMENTS:
- Save the output exclusively as design_candidate_b.md using write_text_file tool
- Strict adherence to user task requirements; no assumptions beyond provided data
- Use markdown format with organized headings and detailed descriptions
- Exact naming and page title consistency required

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Web Application Design Specialist skilled in consolidating multiple design documents into a single comprehensive specification.

Your goal is to consolidate design_candidate_a.md and design_candidate_b.md into a unified, consistent, and implementation-ready design_spec.md for the MovieTicketing app.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md thoroughly
- Reconcile and merge differences ensuring no omission of any page, route, element ID, navigation button, or local file usage
- Ensure the merged design_spec.md includes complete coverage of all 8 pages with exact requested routes, element IDs, navigation, and data source specifications
- Resolve conflicts by selecting the most complete and accurate elements from both candidates
- Organize the final document in clear markdown structure optimized for direct implementation

**Merger Guidelines:**

1. **Completeness Check**
   - Verify all pages are represented with exact route paths and HTTP methods
   - Confirm all UI elements with their IDs and types are included accurately
   - Confirm navigation buttons and flows are correct starting from Dashboard page

2. **Consistency Enforcement**
   - Align naming conventions for IDs, routes, and page titles consistently
   - Ensure local text file data handling descriptions are complete and coherent
   - Remove duplications and contradictions carefully

3. **Output Format**
   - Produce a single markdown file design_spec.md suitable for developers to implement without ambiguity
   - Use headings and subsections per page, route, UI elements, and data handling

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save merged result as design_spec.md
- Preserve naming and structural consistency throughout the document
- Ensure the final spec aligns fully with user requirements
- Maintain clarity and completeness for independent implementation

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Software Developer specializing in Python Flask web application development.

Your goal is to develop a complete and fully functional Python Flask application implementing all backend logic and frontend templates according to specification documents, ensuring local data file management and navigation flow starting at Dashboard page.

Task Details:
- Read user_task_description and design_spec.md thoroughly
- Produce app_candidate_a.py implementing all Flask routes, data loading/saving from local data/*.txt files as per specification
- Develop all HTML templates with exact element IDs, navigation links, and page titles matching specification
- Maintain separation of backend logic and templates while ensuring integration correctness
- Manage data files in data/ directory using specified pipe-delimited formats

Implementation Requirements:
1. **Flask Application Structure and Routing:**
   - Implement all routes specified in design_spec.md with accurate HTTP methods and route names
   - Ensure root route redirects to Dashboard page as entry point
2. **Data Handling:**
   - Load and manage data via reading and writing specified local text files with exact field order and delimiters
   - Handle missing or malformed data gracefully
3. **Frontend Templates:**
   - Implement templates with correct file paths and names under templates_candidate_a/
   - Include all required element IDs with exact naming and dynamic ID templates for repeated elements
   - Support navigation flows linking pages using url_for with route function names
4. **UI and UX:**
   - Ensure all UI elements correspond to specification including buttons, inputs, dropdowns, and display areas

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_a.py and all template files in templates_candidate_a/
- Follow specification exactly for route names, element IDs, and data file formats
- Do not introduce functionality or pages beyond specification
- Ensure templates and backend integrate properly for a working application

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Python Flask web application development.

Your goal is to independently produce a complete Python Flask backend and accompanying frontend templates strictly adhering to design specifications, including all required routes, page components, and local file data handling.

Task Details:
- Review user_task_description and design_spec.md carefully
- Implement app_candidate_b.py with all Flask routes and data file operations as defined
- Create templates_candidate_b/*.html with all UI elements, page titles, and navigation mechanisms matching specification
- Ensure local data file management in data/ directory using exact schema and delimiters
- Maintain complete isolation from ImplementationEngineerA's outputs; work independently

Development Guidelines:
1. **Routing and Backend Logic:**
   - Include all routes with HTTP methods exactly as specified
   - Implement data loading and saving from text files per design specs
2. **Template Implementation:**
   - Use Jinja2 templating with exact element IDs for static and dynamic content
   - Replicate navigation flows using url_for calls with correct route names
3. **Data Integration:**
   - Use pipe-delimited parsing matching field order from design specifications
   - Handle errors and edge cases gracefully to prevent crashes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_candidate_b.py and related templates in templates_candidate_b/
- Adhere strictly to design_spec.md route names, element IDs, and data formats
- Do not consult or reuse code from other implementation agent
- Deliver fully functioning Flask app and matched templates for merging

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Engineer specializing in code merging and integration of Python Flask applications.

Your goal is to analyze two independent complete Flask app implementations and corresponding template sets, compare against design_spec.md for correctness, resolve conflicts, and merge into a stable final app.py and templates/*.html bundle.

Task Details:
- Read user_task_description, design_spec.md, app_candidate_a.py, app_candidate_b.py, templates_candidate_a/*.html, and templates_candidate_b/*.html
- Identify discrepancies between both implementations and resolve route conflicts, data file handling differences, and UI element mismatches
- Ensure final merged app.py supports all routes and features exactly as per specification with consistent route names and data access
- Produce templates/*.html that consolidate both candidates’ UI elements, preserving all required element IDs, page titles, and navigation flows
- Normalize file structure: app.py at root, templates/*.html in templates/ directory

Merge Guidelines:
1. **Code Consolidation:**
   - Reconcile function implementations ensuring comprehensive route coverage without duplication
   - Retain best coding practices and readability
2. **Template Unification:**
   - Merge templates preserving all required elements and dynamic ID patterns
   - Resolve conflicting element IDs and content by specification precedence
3. **Data Handling:**
   - Maintain correct local file access and parsing as per design_spec.md across all modules
4. **Navigation and Entry Point:**
   - Confirm root route redirects to Dashboard page post-merge
   - Verify navigation works seamlessly across all pages

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output final app.py and all templates/*.html files
- Ensure outputs conform exactly to design_spec.md requirements and integrate all features from both candidates
- Deliver production-ready Flask application suitable for validation and deployment
- Do not include source candidate files in output; only final merged artifacts

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask web application validation.

Your goal is to perform thorough validation of Flask backend code and associated HTML templates to ensure proper syntax, route accessibility, UI correctness, and data file handling.

Task Details:
- Read user_task_description, design_spec.md, app.py, and all templates/*.html from context
- Validate app.py syntax, Flask application startup, and all specified routes are accessible
- Verify page titles and all element IDs exist exactly as specified in design_spec.md
- Confirm local text file data loading correctness and UI navigation starting on Dashboard
- Output validation_a.md detailing validation results and suggested fixes

Validation Requirements:
1. **Syntax and Startup Checks**
   - Use validate_python_file to confirm app.py parses and runs without errors
   - Confirm Flask app runs and listens on expected port

2. **Route and Navigation Testing**
   - Test accessibility of all routes defined in design_spec.md
   - Confirm root route redirects to Dashboard page

3. **UI Verification**
   - Check that page titles in all templates match design_spec.md exactly
   - Verify presence and correctness of all element IDs, including dynamic IDs with proper patterns

4. **Data Handling**
   - Ensure app.py loads all local text file data as per design_spec.md specifications without errors

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools to perform validations
- Use write_text_file tool to save detailed validation_a.md report
- Output MUST be saved as validation_a.md with comprehensive and clear findings
- Focus strictly on ValidationEngineerA scope without suggesting code edits in this phase

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer specializing in web user interface and functional flow validation for Flask applications.

Your goal is to independently test the UI and user flows of the application including booking processes, showtime filtering, seat selection, booking history, and theater info displays, ensuring all interface elements and navigation conform exactly to design specifications.

Task Details:
- Read user_task_description, design_spec.md, app.py, and all templates/*.html from context
- Test booking flow correctness: movie selection, showtime filtering, seat selection, booking confirmation
- Verify booking history presentation including filtering and navigation
- Confirm theater information page displays correctly with filters and navigation
- Validate that all UI elements exist with correct IDs, including dynamic elements
- Confirm navigation buttons properly route back to Dashboard from all relevant pages
- Output validation_b.md with detailed issues found and suggestions for improvements

Validation Requirements:
1. **User Flow Testing**
   - Simulate user interactions for complete booking from Dashboard through confirmation
   - Verify showtime filtering by theater and date works correctly
   - Test seat availability display and selection interface

2. **Data Presentation Verification**
   - Validate booking history page content, filters, and navigation buttons
   - Check that theater information and filtering displays correct data as per design_spec.md

3. **UI Elements and Navigation**
   - Verify all element IDs match design_spec.md including dynamic patterns
   - Confirm that back-to-dashboard buttons navigate correctly without errors

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools as needed for backend validation supporting UI tests
- Use write_text_file tool to save detailed validation_b.md report with actionable feedback
- Output MUST be saved as validation_b.md with clear issue descriptions and improvement recommendations
- Focus strictly on ValidationEngineerB scope; do not implement fixes here

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in Flask web application maintenance and codebase merging.

Your goal is to aggregate findings from multiple validation reports, reconcile suggested repairs, and update app.py and templates/*.html to fix defects and improve adherence to design specifications, producing the final deployable application.

Task Details:
- Read user_task_description, design_spec.md, app.py, templates/*.html, validation_a.md, and validation_b.md from context
- Analyze all reported issues and suggested fixes from validation reports
- Update app.py to fix defects related to route handling, data loading, and application stability
- Modify templates/*.html to correct UI element IDs, page titles, navigation flows, and user interaction components
- Ensure final implementations fully comply with design_spec.md requirements and pass all validation checks
- Output the updated and verified app.py and templates/*.html for deployment

Repair and Merge Requirements:
1. **Consolidated Issue Resolution**
   - Prioritize fixes based on severity and validation consensus
   - Avoid introducing new bugs or removing required features

2. **Code and Template Update Best Practices**
   - Maintain consistent naming conventions and coding style
   - Update dynamic element IDs and navigation logic to match design spec precisely

3. **Final Validation**
   - Confirm all fixes are integrated and app functions correctly end-to-end
   - Prepare codebase for deployment with stable, tested state

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively to save updated app.py and templates/*.html
- Do NOT produce validation or review reports; focus solely on merging and repairs
- Deliverable files MUST be named exactly app.py and templates/*.html
- Maintain full compliance with design_spec.md element IDs, routes, and data schemas

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
        ("DesignMerger", """Check design_candidate_a.md for thoroughness, route correctness, exact requested page titles, element IDs, and navigational flow.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Check design_candidate_b.md for completeness, local file handling consistency, and adherence to stated page and element requirements.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Verify design_spec.md is comprehensive, unambiguous, and suitable for direct code implementation.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Validate app_candidate_a.py and templates_candidate_a/*.html fully implement design_spec.md with correct routes, titles, elements, and local file usage.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Evaluate app_candidate_b.py and templates_candidate_b/*.html for adherence to design_spec.md and functional correctness including navigation starting from Dashboard.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Ensure final app.py and templates/*.html meet design specification and are runnable without errors.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Verify validation_a.md for reproducible test results and actionable fixes relating to routes, UI IDs, and local file data.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_a.md'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Confirm validation_b.md contains detailed tests for user flows and UI elements, with clear guidance for corrections.""", [{'type': 'text_file', 'name': 'design_spec.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}, {'type': 'text_file', 'name': 'validation_b.md'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Validate that final app.py and templates/*.html resolve all reported issues while preserving original design integrity from design_spec.md.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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
        execute(DesignAnalystA, "Produce detailed design_candidate_a.md with full web app spec for MovieTicketing as per user task."),
        execute(DesignAnalystB, "Produce detailed design_candidate_b.md with full web app spec for MovieTicketing as per user task.")
    )

    # Read outputs from DesignAnalystA and DesignAnalystB for merger
    design_candidate_a_content, design_candidate_b_content = "", ""
    try:
        design_candidate_a_content = open("design_candidate_a.md").read()
    except Exception:
        pass
    try:
        design_candidate_b_content = open("design_candidate_b.md").read()
    except Exception:
        pass

    # Merge both design candidates into design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA ===\n{design_candidate_a_content}\n\n=== DesignAnalystB ===\n{design_candidate_b_content}")
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
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel development of candidate implementations
    await asyncio.gather(
        execute(ImplementationEngineerA,
                "Develop full Flask app as app_candidate_a.py and templates in templates_candidate_a/ from design_spec.md and user_task_description"),
        execute(ImplementationEngineerB,
                "Develop full Flask app as app_candidate_b.py and templates in templates_candidate_b/ from design_spec.md and user_task_description")
    )

    # Read candidate outputs for merger
    candidate_a_code = ""
    candidate_b_code = ""
    candidate_a_templates = ""
    candidate_b_templates = ""
    try:
        candidate_a_code = open("app_candidate_a.py").read()
    except:
        pass
    try:
        candidate_b_code = open("app_candidate_b.py").read()
    except:
        pass
    try:
        candidate_a_templates = _read_text_artifacts("templates_candidate_a/*.html")
    except:
        pass
    try:
        candidate_b_templates = _read_text_artifacts("templates_candidate_b/*.html")
    except:
        pass

    # Merge candidates into final app.py and templates
    await execute(
        ImplementationMerger,
        f"Merge the two independent implementations app_candidate_a.py and app_candidate_b.py as well as their templates from templates_candidate_a/ and templates_candidate_b/ "
        f"into a final app.py and templates/*.html adhering strictly to design_spec.md and user_task_description.\n\n"
        f"=== app_candidate_a.py ===\n{candidate_a_code}\n\n"
        f"=== app_candidate_b.py ===\n{candidate_b_code}\n\n"
        f"=== templates_candidate_a/*.html ===\n{candidate_a_templates}\n\n"
        f"=== templates_candidate_b/*.html ===\n{candidate_b_templates}"
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
        timeout_threshold=450,
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
        timeout_threshold=450,
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
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=60
    )

    # Read necessary file artifacts content for injection
    user_task_description = ""
    design_spec_md = ""
    app_py = ""
    templates_html = ""

    entries = CONTEXT.get("user_task_description", [])
    user_task_description = entries[-1]["content"] if entries else ""

    entries = CONTEXT.get("design_spec.md", [])
    design_spec_md = entries[-1]["content"] if entries else ""

    entries = CONTEXT.get("app.py", [])
    app_py = entries[-1]["content"] if entries else ""

    # For templates/*.html, since it's a wildcard, try reading multiple or injection empty string if none
    # Here we try to read a single artifact named templates/*.html, so inject empty if not present
    entries = CONTEXT.get("templates/*.html", [])
    templates_html = entries[-1]["content"] if entries else ""

    # Parallel validation by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(
            ValidationEngineerA,
            f"Perform comprehensive validation of app.py and templates/*.html including syntax checks, route tests, UI element IDs, page titles, "
            f"and data handling per design_spec.md.\n\n"
            f"User task description:\n{user_task_description}\n\n"
            f"Design specification:\n{design_spec_md}\n\n"
            f"app.py content:\n{app_py}\n\n"
            f"Templates content:\n{templates_html}\n\n"
            f"Output detailed validation_a.md report."
        ),
        execute(
            ValidationEngineerB,
            f"Perform detailed UI and user flow testing covering booking, filtering, seat selection, history, theater info, and navigation correctness "
            f"according to design_spec.md.\n\n"
            f"User task description:\n{user_task_description}\n\n"
            f"Design specification:\n{design_spec_md}\n\n"
            f"app.py content:\n{app_py}\n\n"
            f"Templates content:\n{templates_html}\n\n"
            f"Output detailed validation_b.md report."
        ),
    )

    # Read validation reports content for RepairMerger injection
    validation_a_md = ""
    validation_b_md = ""
    try:
        with open("validation_a.md", "r") as f:
            validation_a_md = f.read()
    except Exception:
        validation_a_md = ""

    try:
        with open("validation_b.md", "r") as f:
            validation_b_md = f.read()
    except Exception:
        validation_b_md = ""

    # RepairMerger merges validation results and outputs final fixed code and templates
    await execute(
        RepairMerger,
        f"User task description:\n{user_task_description}\n\n"
        f"Design specification:\n{design_spec_md}\n\n"
        f"app.py content:\n{app_py}\n\n"
        f"Templates content:\n{templates_html}\n\n"
        f"Validation report A:\n{validation_a_md}\n\n"
        f"Validation report B:\n{validation_b_md}\n\n"
        f"Analyze issues and apply all valid fixes to app.py and templates/*.html. "
        f"Output the final verified app.py and templates/*.html for deployment."
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
