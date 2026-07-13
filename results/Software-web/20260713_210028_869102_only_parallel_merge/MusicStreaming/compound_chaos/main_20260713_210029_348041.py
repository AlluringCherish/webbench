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
# 20260713_210029_348041/main_20260713_210029_348041.py

# Phase_info dictionary containing complete def blocks for failover context
Phase_info = {
    "phase1": "def design_specification_phase(\n    goal: str = \"Generate two independent Web designs for MusicStreaming app and merge them into design_spec.md covering all requested pages, elements, routes, and data management features.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"DesignAnalystA and DesignAnalystB independently create comprehensive design specifications each covering user interface, page structure, \"\n        \"route mappings, page titles, element IDs, buttons, and data interaction using local text files; DesignMerger then reviews both designs to produce \"\n        \"a unified, implementation-ready design_spec.md ensuring all user requirements are fully covered.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"DesignAnalystA\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in Flask web application UI and data interaction design.\n\nYour goal is to create a complete, detailed standalone design specification for the MusicStreaming application that enables implementation teams to build frontend and backend independently.\n\nTask Details:\n- Read user_task_description fully for the MusicStreaming app features and data storage\n- Produce design_candidate_a.md covering all 10 pages with exact Flask routes, page titles, element IDs, button interactions, navigation flows, and local text file data access patterns\n- Include all user-visible UI components, route mappings starting from the Dashboard page\n- Focus on precise element IDs and clear data management contracts\n\nSpecification Requirements:\n1. Flask Routes:\n   - Define all routes with URL patterns and HTTP methods\n   - Specify which template each route renders\n   - Include navigation flow by defining which buttons lead to which routes\n\n2. Page Details:\n   - For each page, specify page titles and list all element IDs with types and purposes\n   - Describe button behavior and user interactions clearly\n\n3. Data Files Usage:\n   - For each page or feature accessing data, specify the relevant local text files and fields used\n   - Describe how data is read and utilized in the UI (e.g., filtering, sorting, displaying counts)\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_a.md\n- Ensure the specification is self-contained, coherent, and fully covers all user requirements independently of any other design\n- Maintain consistent naming conventions and exact ID spellings as provided in user_task_description\n- Do not refer to or incorporate other analysts' work\n\nOutput: design_candidate_a.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignAnalystB\",\n            \"prompt\": \"\"\"You are a Web Application Design Analyst specializing in UI design consistency, navigation, and local file data management for Flask apps.\n\nYour goal is to produce an alternative complete design specification for the MusicStreaming application that fully covers all pages, UI elements, navigation routes, and data handling with an emphasis on stable element IDs and flexible filtering/sorting capabilities.\n\nTask Details:\n- Read user_task_description thoroughly to understand all 10 required pages, user interactions, and data files\n- Write design_candidate_b.md specifying Flask routes, page titles, stable and reusable element IDs, buttons, navigation flows, and data access using local text files\n- Highlight flexible UI mechanisms such as sorting dropdowns and genre filters with exact IDs\n- Avoid referencing or integration with any other analyst's designs\n\nSpecification Details:\n1. URL Routing and Navigation:\n   - List all Flask routes and HTTP methods\n   - Map buttons and clickable elements to exact Flask functions or endpoints\n\n2. UI Components and Element IDs:\n   - For each page, describe all element IDs, their types, and roles\n   - Emphasize stable ID usage compatible with dynamic elements like add-to-playlist-button-{song_id}\n\n3. Data Interaction:\n   - Define how local text files are used for data storage, access, and filtering\n   - Specify data-driven UI features, dropdown filters, sorting, and dynamic content handling\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_candidate_b.md\n- Ensure full coverage of user needs with stable and consistent element IDs and clearly mapped navigation routes\n- Independent and comprehensive specification with no referencing to other analysts' outputs\n\nOutput: design_candidate_b.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"DesignMerger\",\n            \"prompt\": \"\"\"You are a Design Merger specializing in consolidating and reconciling multiple web UI and backend design specifications into a single unified document.\n\nYour goal is to merge design_candidate_a.md and design_candidate_b.md into a coherent, implementable design_spec.md that fully satisfies all MusicStreaming user requirements, covering 10 pages with complete UI components, navigation routes starting from the Dashboard, and local text file data handling.\n\nTask Details:\n- Read user_task_description, design_candidate_a.md, and design_candidate_b.md completely\n- Identify overlaps, inconsistencies, and gaps; reconcile them into a single unified design specification\n- Ensure all requested pages are fully incorporated with exact element IDs, route mappings, button behaviors, and data management contracts\n- Maintain consistency in naming, stable element IDs, full navigation flow beginning at Dashboard\n- Output a comprehensive design_spec.md ready to guide implementation teams independently\n\nMerge Requirements:\n1. Full coverage of all pages with all required elements and UI components\n2. Complete Flask route table with URL patterns, HTTP methods, templates, and navigation link mappings\n3. Detailed data file usage descriptions for all relevant features and pages\n4. Resolve any contradictions between candidate specs, preferring completeness and clarity\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool to save output as design_spec.md\n- Result must be clear, unambiguous, and fully aligned with the user task details\n- No omissions of required pages or features\n- Ensure exact matching of element IDs and route names throughout\n- Produce a single authoritative source of truth for subsequent implementation\n\nOutput: design_spec.md\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_a.md\", \"source\": \"DesignAnalystA\"},\n                {\"type\": \"text_file\", \"name\": \"design_candidate_b.md\", \"source\": \"DesignAnalystB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"DesignAnalystA\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure design_candidate_a.md contains full and correct page routes, element IDs, and data access contracts for merging.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_a.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignAnalystB\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Verify design_candidate_b.md completeness and feasibility covering all required UI features and local file data handling.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_candidate_b.md\"}]\n        },\n        {\n            \"source_agent\": \"DesignMerger\",\n            \"reviewer_agent\": \"ImplementationEngineerA\",\n            \"review_criteria\": \"Check design_spec.md for clarity, completeness, and readiness to guide Python Flask app implementation with local text files.\",\n            \"review_artifacts\": [{\"type\": \"text_file\", \"name\": \"design_spec.md\"}]\n        }\n    ]\n): pass",
    "phase2": "def implementation_phase(\n    goal: str = \"Produce two independent complete Python Flask app implementations and corresponding templates with data handling from local text files, then merge into final app.py and templates/*.html.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ImplementationEngineerA and ImplementationEngineerB independently implement Python Flask app bundles including app.py and templates/*.html \"\n        \"that satisfy design_spec.md requirements with local text file storage for data; ImplementationMerger then integrates both to produce final app.py \"\n        \"and templates/*.html ensuring proxy-test compatibility, stable routes, element IDs, and reliable file-based data parsing.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ImplementationEngineerA\",\n            \"prompt\": \"\"\"You are a Backend and Frontend Developer specializing in Python Flask applications with local text file data handling.\n\nYour goal is to implement a standalone, fully functional Python Flask app and corresponding HTML templates for the MusicStreaming application based on design specifications.\n\nTask Details:\n- Read the user_task_description and design_spec.md fully\n- Produce app_candidate_a.py implementing all required Flask routes, data parsing from local text files as specified\n- Implement templates_candidate_a/*.html with correct page titles, element IDs, UI elements, search/filter features, playlist management, and navigation flows\n- Focus on no-auth functionality and stable route handling as per design_spec.md\n\nImplementation Instructions:\n1. Flask Application:\n   - Setup app.py with Flask, route handlers, and local file reading/parsing of songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt with exact field order\n   - Implement all routes for dashboard, songs catalog, song details, playlists, albums, artists, genres pages with data passed to templates accordingly\n\n2. Templates:\n   - For each page, implement HTML templates ensuring:\n     - Exact element IDs as specified in design_spec.md page design\n     - Use Jinja2 templating syntax for dynamic content rendering\n     - Implement buttons and inputs with correct IDs and behaviors (e.g., add-to-playlist-button-{song_id})\n     - Implement search/filter elements and playlist creation/management UI\n\n3. Data Handling:\n   - Parse local text files with pipe-delimited format (|) without headers\n   - Convert fields to appropriate data types when necessary (int, str, date)\n   - Handle missing or empty data gracefully\n\n4. Output:\n   - Save Flask app code to app_candidate_a.py using write_text_file\n   - Save templates to templates_candidate_a/*.html files using write_text_file, one file per page\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool for all output files\n- Maintain exact route names, function names, element IDs, and UI flow as per design_spec.md\n- Ensure no authentication is required; all pages accessible directly\n- Follow design_spec.md strictly for data formats and page elements\n- Do not overlap with ImplementationEngineerB's code or templates\n\nOutput: app_candidate_a.py, templates_candidate_a/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Python Flask web applications and Jinja2 templating with local file data management.\n\nYour goal is to build an alternative fully functional Python Flask app and corresponding HTML templates for MusicStreaming according to design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md carefully to understand all requirements\n- Independently implement app_candidate_b.py with all Flask routes, handling local text files for data storage and retrieval as specified\n- Create templates_candidate_b/*.html with complete UI components, page titles, element IDs, and navigation flows consistent with design_spec.md\n- Maintain no-authentication access and support all features: song search, playlists, albums, artists, genres, statistics\n\nImplementation Instructions:\n1. Backend Implementation:\n   - Accurately parse pipe-delimited data files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt)\n   - Implement routing and data passing matching design specifications exactly\n   - Use clear, distinct function and route names to avoid overlap with EngineerA\n\n2. Frontend Templates:\n   - Implement templates with all required static and dynamic element IDs\n   - Use Jinja2 template language for looping over lists and displaying dynamic content\n   - Include filter inputs and buttons with correct IDs for interactivity\n\n3. Data Consistency:\n   - Convert data fields into appropriate types as needed\n   - Handle empty or missing data gracefully without errors\n\n4. Output:\n   - Save Flask application code to app_candidate_b.py\n   - Save HTML templates to templates_candidate_b/*.html, one file per page, all using write_text_file\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file to save all output files\n- Ensure all page routes, UI element IDs, and data parsing follow design_spec.md precisely\n- Independently developed code and templates with no code overlap with ImplementationEngineerA\n- Provide fully functional no-auth Flask app and templates satisfying all user features\n\nOutput: app_candidate_b.py, templates_candidate_b/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ImplementationMerger\",\n            \"prompt\": \"\"\"You are a Software Integration Engineer specializing in merging multiple Python Flask app implementations and HTML template sets into a single coherent application.\n\nYour goal is to merge app_candidate_a.py and app_candidate_b.py plus their respective template sets into one final app.py and templates/*.html for the MusicStreaming app, ensuring full compliance with design_spec.md.\n\nTask Details:\n- Read user_task_description and design_spec.md thoroughly\n- Analyze app_candidate_a.py and templates_candidate_a/*.html and app_candidate_b.py and templates_candidate_b/*.html inputs\n- Resolve any conflicting routes, function names, and UI elements to produce unified, stable route handling and UI\n- Unify data parsing from local text files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt) ensuring correct field ordering and robust error handling\n- Merge templates to create templates/*.html preserving all required element IDs, page titles, navigation, and UI features without duplication or conflict\n- Ensure final app.py and templates/*.html are stable, proxy-test compatible, and fully functional with no authentication required\n- Document any significant merged design decisions in comments\n\nImplementation Instructions:\n1. Code Integration:\n   - Harmonize route handlers from both candidate apps; prefer best implementations or combine logically\n   - Unify data loading functions for all data files with consistent parsing and typing\n   - Maintain consistent function naming and route paths per design_spec.md; refactor as needed for clarity and stability\n\n2. Template Consolidation:\n   - Identify common templates and merge UI components, preserving critical element IDs\n   - Ensure dynamic IDs (e.g., add-to-playlist-button-{song_id}) function correctly with Jinja2 syntax\n   - Remove duplicates and unify layout and navigation flows\n\n3. Testing and Validation:\n   - Verify all routes respond as expected with correct data passing\n   - Validate UI elements exist with correct IDs per design_spec.md\n   - Confirm no authentication flow is required and site is accessible from dashboard onward\n   - Ensure app.py and templates pass proxy-based test harness without errors\n\n4. Output:\n   - Save merged Flask app code as app.py using write_text_file\n   - Save merged templates/*.html, one file per page, using write_text_file\n\nCRITICAL REQUIREMENTS:\n- Use write_text_file tool for all output files\n- Deliver fully working, integrated Flask application and templates that meet or exceed design_spec.md requirements\n- Maintain all element IDs as in design_spec.md exactly\n- Ensure robust, stable file-based data parsing for all text data sources\n- Produce single app.py and templates/*.html ready for deployment and proxy testing\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\", \"source\": \"ImplementationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\", \"source\": \"ImplementationEngineerB\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\", \"source\": \"ImplementationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ImplementationEngineerA\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Evaluate app_candidate_a.py and templates_candidate_a/*.html for compliance with design_spec.md and proxy-test readiness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_a.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_a/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationEngineerB\",\n            \"reviewer_agent\": \"ImplementationMerger\",\n            \"review_criteria\": \"Check app_candidate_b.py and templates_candidate_b/*.html independently for feature completeness and code correctness.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app_candidate_b.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates_candidate_b/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ImplementationMerger\",\n            \"reviewer_agent\": \"ValidationEngineerA\",\n            \"review_criteria\": \"Verify merged app.py and templates/*.html are a coherent, functional Flask app fully compatible with design_spec.md and web tests.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
    "phase3": "def verification_phase(\n    goal: str = \"Conduct two independent validations of final app.py and templates/*.html and merge validated repairs into a final robust Flask app bundle.\",\n    collab_pattern_name: str = \"Parallel + Merger\",\n    collab_pattern_description: str = (\n        \"ValidationEngineerA and ValidationEngineerB independently validate the final merged app.py and templates/*.html by testing functionality, \"\n        \"syntax, route accuracy, UI element presence, local file data interaction, and proxy-test compatibility; RepairMerger then reconciles validation \"\n        \"reports and applies necessary fixes to deliver the final stable application.\"\n    ),\n    team: list = [\n        {\n            \"agent_name\": \"ValidationEngineerA\",\n            \"prompt\": \"\"\"You are a Software Test Engineer specializing in Flask applications and web UI validation.\n\nYour goal is to independently validate the final Flask backend code (app.py) and all HTML templates (templates/*.html) ensuring syntax correctness, proper route functionality, accurate UI element IDs, and precise local text file data integration consistent with the MusicStreaming design.\n\nTask Details:\n- Read user_task_description for overall MusicStreaming requirements\n- Read design_spec.md for detailed functional specifications\n- Validate app.py syntax, route definitions, request handling, and data file interactions\n- Validate all templates/*.html for required element IDs presence and correct structure\n- Produce a comprehensive validation report detailing all functional checks, errors, and observations\n\nValidation Requirements:\n1. **Backend Code Validation:**\n   - Use validate_python_file tool to confirm syntax and runtime correctness of app.py\n   - Test all Flask routes defined in design_spec.md for correct responses and context\n   - Verify data loading/parsing from local text files matches design_spec field order and types\n\n2. **Frontend Template Validation:**\n   - Check presence of all required element IDs specified in design_spec.md across templates\n   - Confirm templates render context variables correctly with no missing data\n   - Validate UI elements for buttons, inputs, and navigation correspond exactly to specs\n\n3. **Functional Testing:**\n   - Test main user flows such as searching songs, creating playlists, browsing albums/artists, filtering genres\n   - Confirm edge cases such as empty playlists, non-existing songs handled gracefully\n   - Verify interaction between frontend and backend is consistent and error-free\n\nCRITICAL REQUIREMENTS:\n- MUST use validate_python_file and execute_python_code tools to verify backend\n- MUST use write_text_file tool to save detailed validation report as validation_a.md\n- Validation report must cover all pages and routes comprehensively\n- Focus exclusively on validating provided app.py and templates/*.html against design_spec.md without implementing changes\n\nOutput: validation_a.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"ValidationEngineerB\",\n            \"prompt\": \"\"\"You are a Software Test Engineer with expertise in Flask web applications and user interface validation.\n\nYour goal is to independently perform comprehensive validation of the final Flask backend (app.py) and frontend HTML templates (templates/*.html) ensuring complete feature coverage, correct local text file data operations, search and filter functionalities, and UI stability aligned with the MusicStreaming application requirements.\n\nTask Details:\n- Read user_task_description for full functional context\n- Read design_spec.md to understand detailed expected behaviors\n- Validate app.py for correct implementation of all features and data handling\n- Validate templates/*.html for required UI elements, navigation, and dynamic content rendering\n- Produce a detailed validation report stating test coverage, bugs, and suggestions named validation_b.md\n\nValidation Requirements:\n1. **Backend Validation:**\n   - Confirm all CRUD-like operations on playlists, songs, albums, and artists work as specified\n   - Validate local data files are accessed and parsed properly with correct field sequences\n   - Use validate_python_file and execute_python_code to verify code robustness and runtime behavior\n\n2. **Frontend Validation:**\n   - Check for presence and correctness of all UI elements, including buttons with dynamic IDs\n   - Ensure search inputs, dropdown filters, and navigations function properly in templates\n   - Verify pages load correct content per user actions and data context\n\n3. **End-to-End Feature Testing:**\n   - Test key user stories: searching and adding songs, managing playlists, browsing albums/artists, genre exploration\n   - Confirm error handling and UI feedback for edge scenarios\n   - Evaluate UI stability and consistent styling across all pages\n\nCRITICAL REQUIREMENTS:\n- MUST utilize validate_python_file and execute_python_code tools for backend validation\n- MUST write the validation report to validation_b.md using write_text_file tool\n- The report must comprehensively cover all app features, UI elements, and data interactions\n- Concentrate on validating provided code and templates, do NOT apply fixes or changes\n\nOutput: validation_b.md\"\"\",\n            \"tools\": [\"validate_python_file\", \"execute_python_code\", \"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"}\n            ]\n        },\n        {\n            \"agent_name\": \"RepairMerger\",\n            \"prompt\": \"\"\"You are a Software Developer specializing in Flask applications and frontend-backend integration.\n\nYour goal is to evaluate independent validation reports (validation_a.md and validation_b.md), identify required corrections, apply appropriate fixes to the Flask backend (app.py) and the frontend templates (templates/*.html), and produce the final polished MusicStreaming web application fully compliant with the verified design specifications.\n\nTask Details:\n- Read user_task_description and design_spec.md for overall requirements and detailed specs\n- Analyze validation_a.md and validation_b.md to extract all reported issues and suggested fixes\n- Apply necessary code repairs and template modifications to app.py and templates/*.html\n- Ensure the final app.py and templates are fully functional, error free, and consistent with design_spec.md\n- Deliver the refined backend and frontend code ready for deployment or final delivery\n\nRepair and Integration Guidelines:\n1. **Bug Fixing:**\n   - Correct all syntax errors, route inaccuracies, and data handling bugs in app.py\n   - Fix any missing or incorrect UI element IDs, navigations, and content rendering in templates\n2. **Consistency and Compliance:**\n   - Ensure all function names, route handlers, and context variables strictly match design_spec.md\n   - Confirm templates comply precisely with element ID naming conventions and page titles\n3. **Code and Template Quality:**\n   - Maintain readable, clean, and maintainable code and markup style\n   - Do not introduce new features or functionality beyond validated fixes\n\nCRITICAL REQUIREMENTS:\n- MUST use write_text_file tool to save the corrected app.py and all templates/*.html\n- Focus exclusively on applying fixes identified in validation reports; no feature additions\n- Final deliverables must pass all previous validations and align 100% with design_spec.md\n- Ensure file naming and directory structures are preserved exactly as provided\n\nOutput: app.py, templates/*.html\"\"\",\n            \"tools\": [\"write_text_file\"],\n            \"llm_model\": \"gpt-4.1-mini\",\n            \"input_artifacts\": [\n                {\"type\": \"user\", \"name\": \"user_task_description\", \"source\": \"User\"},\n                {\"type\": \"text_file\", \"name\": \"design_spec.md\", \"source\": \"DesignMerger\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\", \"source\": \"ImplementationMerger\"},\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\", \"source\": \"ValidationEngineerA\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\", \"source\": \"ValidationEngineerB\"}\n            ],\n            \"output_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ],\n    review_policy: list = [\n        {\n            \"source_agent\": \"ValidationEngineerA\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Check validation_a.md for detailed functional correctness and any implementation issues before merging repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"ValidationEngineerB\",\n            \"reviewer_agent\": \"RepairMerger\",\n            \"review_criteria\": \"Review validation_b.md for completeness of testing and verify all reported issues are addressed in repairs.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        },\n        {\n            \"source_agent\": \"RepairMerger\",\n            \"reviewer_agent\": \"DesignMerger\",\n            \"review_criteria\": \"Ensure final app.py and templates/*.html fully satisfy the design_spec.md and incorporate all fixes from validations.\",\n            \"review_artifacts\": [\n                {\"type\": \"text_file\", \"name\": \"validation_a.md\"},\n                {\"type\": \"text_file\", \"name\": \"validation_b.md\"},\n                {\"type\": \"text_file\", \"name\": \"app.py\"},\n                {\"type\": \"text_file\", \"name\": \"templates/*.html\"}\n            ]\n        }\n    ]\n): pass",
}

user_task = """
# Requirements Document for 'MusicStreaming' Web Application

## 1. Objective
Develop a comprehensive web application named 'MusicStreaming' using Python, with data managed through local text files. The application enables users to search for songs, create and manage playlists, browse albums, explore artist profiles, filter by genres, and view song/artist statistics. No authentication required - all features are directly accessible. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'MusicStreaming' application is Python.

## 3. Page Design

The 'MusicStreaming' web application will consist of the following ten pages:

### 1. Dashboard Page
- **Page Title**: Music Streaming Dashboard
- **Overview**: The main hub displaying featured songs, trending artists, and quick navigation to all functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: featured-songs** - Type: Div - Display of featured song recommendations.
  - **ID: browse-songs-button** - Type: Button - Button to navigate to song catalog page.
  - **ID: my-playlists-button** - Type: Button - Button to navigate to my playlists page.
  - **ID: trending-artists-button** - Type: Button - Button to navigate to trending artists page.

### 2. Song Catalog Page
- **Page Title**: Song Catalog
- **Overview**: A page displaying all available songs with search and filter capabilities.
- **Elements**:
  - **ID: catalog-page** - Type: Div - Container for the catalog page.
  - **ID: search-input** - Type: Input - Field to search songs by title, artist, or album.
  - **ID: genre-filter** - Type: Dropdown - Dropdown to filter by genre (Pop, Rock, Hip-Hop, Jazz, Classical, etc.).
  - **ID: songs-grid** - Type: Div - Grid displaying song cards with cover art, title, artist, and duration.
  - **ID: add-to-playlist-button-{song_id}** - Type: Button - Button to add song to playlist (each song card has this).

### 3. Song Details Page
- **Page Title**: Song Details
- **Overview**: A page displaying detailed information about a specific song.
- **Elements**:
  - **ID: song-details-page** - Type: Div - Container for the song details page.
  - **ID: song-title** - Type: H1 - Display song title.
  - **ID: artist-name** - Type: Div - Display artist name with link to artist profile.
  - **ID: album-name** - Type: Div - Display album name.
  - **ID: duration-display** - Type: Div - Display song duration.
  - **ID: play-button** - Type: Button - Button to play the song.

### 4. Playlist Page
- **Page Title**: My Playlists
- **Overview**: A page displaying all user-created playlists.
- **Elements**:
  - **ID: playlists-page** - Type: Div - Container for the playlists page.
  - **ID: playlists-grid** - Type: Div - Grid displaying playlist cards with cover, title, and song count.
  - **ID: create-playlist-button** - Type: Button - Button to create a new playlist.
  - **ID: view-playlist-button-{playlist_id}** - Type: Button - Button to view playlist details (each playlist has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. Playlist Details Page
- **Page Title**: Playlist Details
- **Overview**: A page displaying songs in a specific playlist with management options.
- **Elements**:
  - **ID: playlist-details-page** - Type: Div - Container for the playlist details page.
  - **ID: playlist-title** - Type: H1 - Display playlist title.
  - **ID: playlist-description** - Type: Div - Display playlist description.
  - **ID: songs-in-playlist** - Type: Table - Table displaying songs with title, artist, duration, and remove option.
  - **ID: remove-song-button-{song_id}** - Type: Button - Button to remove song from playlist (each song has this).
  - **ID: delete-playlist-button** - Type: Button - Button to delete the entire playlist.

### 6. Create Playlist Page
- **Page Title**: Create New Playlist
- **Overview**: A page for users to create a new playlist with title and description.
- **Elements**:
  - **ID: create-playlist-page** - Type: Div - Container for the create playlist page.
  - **ID: playlist-name-input** - Type: Input - Field to input playlist name.
  - **ID: playlist-description-input** - Type: Textarea - Field to input playlist description.
  - **ID: save-playlist-button** - Type: Button - Button to save and create the new playlist.
  - **ID: cancel-create-button** - Type: Button - Button to cancel and go back.

### 7. Album Browse Page
- **Page Title**: Albums
- **Overview**: A page displaying all available albums with browsing and filtering options.
- **Elements**:
  - **ID: albums-page** - Type: Div - Container for the albums page.
  - **ID: albums-grid** - Type: Div - Grid displaying album cards with cover art, title, artist, and year.
  - **ID: search-albums** - Type: Input - Field to search albums by title or artist.
  - **ID: sort-albums** - Type: Dropdown - Dropdown to sort albums (By Title, By Artist, By Year).
  - **ID: view-album-button-{album_id}** - Type: Button - Button to view album details (each album has this).

### 8. Album Details Page
- **Page Title**: Album Details
- **Overview**: A page displaying all songs in a specific album.
- **Elements**:
  - **ID: album-details-page** - Type: Div - Container for the album details page.
  - **ID: album-title** - Type: H1 - Display album title.
  - **ID: album-artist** - Type: Div - Display album artist.
  - **ID: album-year** - Type: Div - Display album release year.
  - **ID: album-songs-list** - Type: Div - List of songs in the album.
  - **ID: add-album-to-playlist-button** - Type: Button - Button to add all songs from album to playlist.

### 9. Artist Profile Page
- **Page Title**: Artist Profiles
- **Overview**: A page displaying all artists and their information.
- **Elements**:
  - **ID: artists-page** - Type: Div - Container for the artists page.
  - **ID: artists-grid** - Type: Div - Grid displaying artist cards with photo, name, and genre.
  - **ID: search-artists** - Type: Input - Field to search artists by name.
  - **ID: artists-sort** - Type: Dropdown - Dropdown to sort artists (By Name, By Genre).
  - **ID: view-artist-button-{artist_id}** - Type: Button - Button to view artist profile (each artist has this).

### 10. Genre Exploration Page
- **Page Title**: Genre Exploration
- **Overview**: A page for exploring music by genres with featured songs and artists per genre.
- **Elements**:
  - **ID: genres-page** - Type: Div - Container for the genres page.
  - **ID: genres-list** - Type: Div - List of all available genres.
  - **ID: select-genre** - Type: Dropdown - Dropdown to select and view a specific genre.
  - **ID: genre-songs** - Type: Div - Display songs for selected genre.
  - **ID: genre-artists** - Type: Div - Display artists for selected genre.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'MusicStreaming' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. Songs Data
- **File Name**: `songs.txt`
- **Data Format**:
  ```
  song_id|title|artist_id|album_id|genre|duration|release_date|play_count
  ```
- **Example Data**:
  ```
  1|Bohemian Rhapsody|1|1|Rock|354|1975-10-31|2500000
  2|Blinding Lights|2|2|Synth-Pop|200|2019-11-29|3800000
  3|Shape of You|3|3|Pop|233|2017-01-06|4200000
  ```

### 2. Artists Data
- **File Name**: `artists.txt`
- **Data Format**:
  ```
  artist_id|name|genre|country|formation_year
  ```
- **Example Data**:
  ```
  1|Queen|Rock|United Kingdom|1970
  2|The Weeknd|Synth-Pop|Canada|2010
  3|Ed Sheeran|Pop|United Kingdom|2005
  ```

### 3. Albums Data
- **File Name**: `albums.txt`
- **Data Format**:
  ```
  album_id|title|artist_id|release_year|total_songs|genre
  ```
- **Example Data**:
  ```
  1|A Night at the Opera|1|1975|11|Rock
  2|After Hours|2|2019|14|Synth-Pop
  3|Divide|3|2017|12|Pop
  ```

### 4. Genres Data
- **File Name**: `genres.txt`
- **Data Format**:
  ```
  genre_id|genre_name|description
  ```
- **Example Data**:
  ```
  1|Rock|Guitar-driven music with strong beats and vocals
  2|Pop|Catchy mainstream music with broad appeal
  3|Hip-Hop|Rhythmic music with rap vocals and beat production
  ```

### 5. Playlists Data
- **File Name**: `playlists.txt`
- **Data Format**:
  ```
  playlist_id|title|description|creation_date|total_songs
  ```
- **Example Data**:
  ```
  1|Workout Mix|High energy songs for the gym|2025-01-15|25
  2|Chill Vibes|Relaxing music for study|2025-01-16|18
  3|Party Hits|Latest party tracks|2025-01-17|32
  ```

### 6. Playlist Songs Data
- **File Name**: `playlist_songs.txt`
- **Data Format**:
  ```
  playlist_song_id|playlist_id|song_id|added_date
  ```
- **Example Data**:
  ```
  1|1|2|2025-01-15
  2|1|3|2025-01-15
  3|2|1|2025-01-16
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
            """You are a Web Application Design Analyst specializing in Flask web application UI and data interaction design.

Your goal is to create a complete, detailed standalone design specification for the MusicStreaming application that enables implementation teams to build frontend and backend independently.

Task Details:
- Read user_task_description fully for the MusicStreaming app features and data storage
- Produce design_candidate_a.md covering all 10 pages with exact Flask routes, page titles, element IDs, button interactions, navigation flows, and local text file data access patterns
- Include all user-visible UI components, route mappings starting from the Dashboard page
- Focus on precise element IDs and clear data management contracts

Specification Requirements:
1. Flask Routes:
   - Define all routes with URL patterns and HTTP methods
   - Specify which template each route renders
   - Include navigation flow by defining which buttons lead to which routes

2. Page Details:
   - For each page, specify page titles and list all element IDs with types and purposes
   - Describe button behavior and user interactions clearly

3. Data Files Usage:
   - For each page or feature accessing data, specify the relevant local text files and fields used
   - Describe how data is read and utilized in the UI (e.g., filtering, sorting, displaying counts)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_a.md
- Ensure the specification is self-contained, coherent, and fully covers all user requirements independently of any other design
- Maintain consistent naming conventions and exact ID spellings as provided in user_task_description
- Do not refer to or incorporate other analysts' work

Output: design_candidate_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_a.md'}],

    },

    "DesignAnalystB": {
        "prompt": (
            """You are a Web Application Design Analyst specializing in UI design consistency, navigation, and local file data management for Flask apps.

Your goal is to produce an alternative complete design specification for the MusicStreaming application that fully covers all pages, UI elements, navigation routes, and data handling with an emphasis on stable element IDs and flexible filtering/sorting capabilities.

Task Details:
- Read user_task_description thoroughly to understand all 10 required pages, user interactions, and data files
- Write design_candidate_b.md specifying Flask routes, page titles, stable and reusable element IDs, buttons, navigation flows, and data access using local text files
- Highlight flexible UI mechanisms such as sorting dropdowns and genre filters with exact IDs
- Avoid referencing or integration with any other analyst's designs

Specification Details:
1. URL Routing and Navigation:
   - List all Flask routes and HTTP methods
   - Map buttons and clickable elements to exact Flask functions or endpoints

2. UI Components and Element IDs:
   - For each page, describe all element IDs, their types, and roles
   - Emphasize stable ID usage compatible with dynamic elements like add-to-playlist-button-{song_id}

3. Data Interaction:
   - Define how local text files are used for data storage, access, and filtering
   - Specify data-driven UI features, dropdown filters, sorting, and dynamic content handling

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_candidate_b.md
- Ensure full coverage of user needs with stable and consistent element IDs and clearly mapped navigation routes
- Independent and comprehensive specification with no referencing to other analysts' outputs

Output: design_candidate_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_candidate_b.md'}],

    },

    "DesignMerger": {
        "prompt": (
            """You are a Design Merger specializing in consolidating and reconciling multiple web UI and backend design specifications into a single unified document.

Your goal is to merge design_candidate_a.md and design_candidate_b.md into a coherent, implementable design_spec.md that fully satisfies all MusicStreaming user requirements, covering 10 pages with complete UI components, navigation routes starting from the Dashboard, and local text file data handling.

Task Details:
- Read user_task_description, design_candidate_a.md, and design_candidate_b.md completely
- Identify overlaps, inconsistencies, and gaps; reconcile them into a single unified design specification
- Ensure all requested pages are fully incorporated with exact element IDs, route mappings, button behaviors, and data management contracts
- Maintain consistency in naming, stable element IDs, full navigation flow beginning at Dashboard
- Output a comprehensive design_spec.md ready to guide implementation teams independently

Merge Requirements:
1. Full coverage of all pages with all required elements and UI components
2. Complete Flask route table with URL patterns, HTTP methods, templates, and navigation link mappings
3. Detailed data file usage descriptions for all relevant features and pages
4. Resolve any contradictions between candidate specs, preferring completeness and clarity

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Result must be clear, unambiguous, and fully aligned with the user task details
- No omissions of required pages or features
- Ensure exact matching of element IDs and route names throughout
- Produce a single authoritative source of truth for subsequent implementation

Output: design_spec.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_candidate_a.md', 'source': 'DesignAnalystA'}, {'type': 'text_file', 'name': 'design_candidate_b.md', 'source': 'DesignAnalystB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'design_spec.md'}],

    },

    "ImplementationEngineerA": {
        "prompt": (
            """You are a Backend and Frontend Developer specializing in Python Flask applications with local text file data handling.

Your goal is to implement a standalone, fully functional Python Flask app and corresponding HTML templates for the MusicStreaming application based on design specifications.

Task Details:
- Read the user_task_description and design_spec.md fully
- Produce app_candidate_a.py implementing all required Flask routes, data parsing from local text files as specified
- Implement templates_candidate_a/*.html with correct page titles, element IDs, UI elements, search/filter features, playlist management, and navigation flows
- Focus on no-auth functionality and stable route handling as per design_spec.md

Implementation Instructions:
1. Flask Application:
   - Setup app.py with Flask, route handlers, and local file reading/parsing of songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt with exact field order
   - Implement all routes for dashboard, songs catalog, song details, playlists, albums, artists, genres pages with data passed to templates accordingly

2. Templates:
   - For each page, implement HTML templates ensuring:
     - Exact element IDs as specified in design_spec.md page design
     - Use Jinja2 templating syntax for dynamic content rendering
     - Implement buttons and inputs with correct IDs and behaviors (e.g., add-to-playlist-button-{song_id})
     - Implement search/filter elements and playlist creation/management UI

3. Data Handling:
   - Parse local text files with pipe-delimited format (|) without headers
   - Convert fields to appropriate data types when necessary (int, str, date)
   - Handle missing or empty data gracefully

4. Output:
   - Save Flask app code to app_candidate_a.py using write_text_file
   - Save templates to templates_candidate_a/*.html files using write_text_file, one file per page

CRITICAL REQUIREMENTS:
- Use write_text_file tool for all output files
- Maintain exact route names, function names, element IDs, and UI flow as per design_spec.md
- Ensure no authentication is required; all pages accessible directly
- Follow design_spec.md strictly for data formats and page elements
- Do not overlap with ImplementationEngineerB's code or templates

Output: app_candidate_a.py, templates_candidate_a/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}],

    },

    "ImplementationEngineerB": {
        "prompt": (
            """You are a Software Developer specializing in Python Flask web applications and Jinja2 templating with local file data management.

Your goal is to build an alternative fully functional Python Flask app and corresponding HTML templates for MusicStreaming according to design specifications.

Task Details:
- Read user_task_description and design_spec.md carefully to understand all requirements
- Independently implement app_candidate_b.py with all Flask routes, handling local text files for data storage and retrieval as specified
- Create templates_candidate_b/*.html with complete UI components, page titles, element IDs, and navigation flows consistent with design_spec.md
- Maintain no-authentication access and support all features: song search, playlists, albums, artists, genres, statistics

Implementation Instructions:
1. Backend Implementation:
   - Accurately parse pipe-delimited data files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt)
   - Implement routing and data passing matching design specifications exactly
   - Use clear, distinct function and route names to avoid overlap with EngineerA

2. Frontend Templates:
   - Implement templates with all required static and dynamic element IDs
   - Use Jinja2 template language for looping over lists and displaying dynamic content
   - Include filter inputs and buttons with correct IDs for interactivity

3. Data Consistency:
   - Convert data fields into appropriate types as needed
   - Handle empty or missing data gracefully without errors

4. Output:
   - Save Flask application code to app_candidate_b.py
   - Save HTML templates to templates_candidate_b/*.html, one file per page, all using write_text_file

CRITICAL REQUIREMENTS:
- Use write_text_file to save all output files
- Ensure all page routes, UI element IDs, and data parsing follow design_spec.md precisely
- Independently developed code and templates with no code overlap with ImplementationEngineerA
- Provide fully functional no-auth Flask app and templates satisfying all user features

Output: app_candidate_b.py, templates_candidate_b/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}],

    },

    "ImplementationMerger": {
        "prompt": (
            """You are a Software Integration Engineer specializing in merging multiple Python Flask app implementations and HTML template sets into a single coherent application.

Your goal is to merge app_candidate_a.py and app_candidate_b.py plus their respective template sets into one final app.py and templates/*.html for the MusicStreaming app, ensuring full compliance with design_spec.md.

Task Details:
- Read user_task_description and design_spec.md thoroughly
- Analyze app_candidate_a.py and templates_candidate_a/*.html and app_candidate_b.py and templates_candidate_b/*.html inputs
- Resolve any conflicting routes, function names, and UI elements to produce unified, stable route handling and UI
- Unify data parsing from local text files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt) ensuring correct field ordering and robust error handling
- Merge templates to create templates/*.html preserving all required element IDs, page titles, navigation, and UI features without duplication or conflict
- Ensure final app.py and templates/*.html are stable, proxy-test compatible, and fully functional with no authentication required
- Document any significant merged design decisions in comments

Implementation Instructions:
1. Code Integration:
   - Harmonize route handlers from both candidate apps; prefer best implementations or combine logically
   - Unify data loading functions for all data files with consistent parsing and typing
   - Maintain consistent function naming and route paths per design_spec.md; refactor as needed for clarity and stability

2. Template Consolidation:
   - Identify common templates and merge UI components, preserving critical element IDs
   - Ensure dynamic IDs (e.g., add-to-playlist-button-{song_id}) function correctly with Jinja2 syntax
   - Remove duplicates and unify layout and navigation flows

3. Testing and Validation:
   - Verify all routes respond as expected with correct data passing
   - Validate UI elements exist with correct IDs per design_spec.md
   - Confirm no authentication flow is required and site is accessible from dashboard onward
   - Ensure app.py and templates pass proxy-based test harness without errors

4. Output:
   - Save merged Flask app code as app.py using write_text_file
   - Save merged templates/*.html, one file per page, using write_text_file

CRITICAL REQUIREMENTS:
- Use write_text_file tool for all output files
- Deliver fully working, integrated Flask application and templates that meet or exceed design_spec.md requirements
- Maintain all element IDs as in design_spec.md exactly
- Ensure robust, stable file-based data parsing for all text data sources
- Produce single app.py and templates/*.html ready for deployment and proxy testing

Output: app.py, templates/*.html"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app_candidate_a.py', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html', 'source': 'ImplementationEngineerA'}, {'type': 'text_file', 'name': 'app_candidate_b.py', 'source': 'ImplementationEngineerB'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html', 'source': 'ImplementationEngineerB'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}],

    },

    "ValidationEngineerA": {
        "prompt": (
            """You are a Software Test Engineer specializing in Flask applications and web UI validation.

Your goal is to independently validate the final Flask backend code (app.py) and all HTML templates (templates/*.html) ensuring syntax correctness, proper route functionality, accurate UI element IDs, and precise local text file data integration consistent with the MusicStreaming design.

Task Details:
- Read user_task_description for overall MusicStreaming requirements
- Read design_spec.md for detailed functional specifications
- Validate app.py syntax, route definitions, request handling, and data file interactions
- Validate all templates/*.html for required element IDs presence and correct structure
- Produce a comprehensive validation report detailing all functional checks, errors, and observations

Validation Requirements:
1. **Backend Code Validation:**
   - Use validate_python_file tool to confirm syntax and runtime correctness of app.py
   - Test all Flask routes defined in design_spec.md for correct responses and context
   - Verify data loading/parsing from local text files matches design_spec field order and types

2. **Frontend Template Validation:**
   - Check presence of all required element IDs specified in design_spec.md across templates
   - Confirm templates render context variables correctly with no missing data
   - Validate UI elements for buttons, inputs, and navigation correspond exactly to specs

3. **Functional Testing:**
   - Test main user flows such as searching songs, creating playlists, browsing albums/artists, filtering genres
   - Confirm edge cases such as empty playlists, non-existing songs handled gracefully
   - Verify interaction between frontend and backend is consistent and error-free

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools to verify backend
- MUST use write_text_file tool to save detailed validation report as validation_a.md
- Validation report must cover all pages and routes comprehensively
- Focus exclusively on validating provided app.py and templates/*.html against design_spec.md without implementing changes

Output: validation_a.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_a.md'}],

    },

    "ValidationEngineerB": {
        "prompt": (
            """You are a Software Test Engineer with expertise in Flask web applications and user interface validation.

Your goal is to independently perform comprehensive validation of the final Flask backend (app.py) and frontend HTML templates (templates/*.html) ensuring complete feature coverage, correct local text file data operations, search and filter functionalities, and UI stability aligned with the MusicStreaming application requirements.

Task Details:
- Read user_task_description for full functional context
- Read design_spec.md to understand detailed expected behaviors
- Validate app.py for correct implementation of all features and data handling
- Validate templates/*.html for required UI elements, navigation, and dynamic content rendering
- Produce a detailed validation report stating test coverage, bugs, and suggestions named validation_b.md

Validation Requirements:
1. **Backend Validation:**
   - Confirm all CRUD-like operations on playlists, songs, albums, and artists work as specified
   - Validate local data files are accessed and parsed properly with correct field sequences
   - Use validate_python_file and execute_python_code to verify code robustness and runtime behavior

2. **Frontend Validation:**
   - Check for presence and correctness of all UI elements, including buttons with dynamic IDs
   - Ensure search inputs, dropdown filters, and navigations function properly in templates
   - Verify pages load correct content per user actions and data context

3. **End-to-End Feature Testing:**
   - Test key user stories: searching and adding songs, managing playlists, browsing albums/artists, genre exploration
   - Confirm error handling and UI feedback for edge scenarios
   - Evaluate UI stability and consistent styling across all pages

CRITICAL REQUIREMENTS:
- MUST utilize validate_python_file and execute_python_code tools for backend validation
- MUST write the validation report to validation_b.md using write_text_file tool
- The report must comprehensively cover all app features, UI elements, and data interactions
- Concentrate on validating provided code and templates, do NOT apply fixes or changes

Output: validation_b.md"""
        ),
        "model": "gpt-4.1-mini",
        "tools": ['validate_python_file', 'execute_python_code', 'write_text_file'],
        "input_artifacts": [{'type': 'user', 'name': 'user_task_description', 'source': 'User'}, {'type': 'text_file', 'name': 'design_spec.md', 'source': 'DesignMerger'}, {'type': 'text_file', 'name': 'app.py', 'source': 'ImplementationMerger'}, {'type': 'text_file', 'name': 'templates/*.html', 'source': 'ImplementationMerger'}],
        "output_artifacts": [{'type': 'text_file', 'name': 'validation_b.md'}],

    },

    "RepairMerger": {
        "prompt": (
            """You are a Software Developer specializing in Flask applications and frontend-backend integration.

Your goal is to evaluate independent validation reports (validation_a.md and validation_b.md), identify required corrections, apply appropriate fixes to the Flask backend (app.py) and the frontend templates (templates/*.html), and produce the final polished MusicStreaming web application fully compliant with the verified design specifications.

Task Details:
- Read user_task_description and design_spec.md for overall requirements and detailed specs
- Analyze validation_a.md and validation_b.md to extract all reported issues and suggested fixes
- Apply necessary code repairs and template modifications to app.py and templates/*.html
- Ensure the final app.py and templates are fully functional, error free, and consistent with design_spec.md
- Deliver the refined backend and frontend code ready for deployment or final delivery

Repair and Integration Guidelines:
1. **Bug Fixing:**
   - Correct all syntax errors, route inaccuracies, and data handling bugs in app.py
   - Fix any missing or incorrect UI element IDs, navigations, and content rendering in templates
2. **Consistency and Compliance:**
   - Ensure all function names, route handlers, and context variables strictly match design_spec.md
   - Confirm templates comply precisely with element ID naming conventions and page titles
3. **Code and Template Quality:**
   - Maintain readable, clean, and maintainable code and markup style
   - Do not introduce new features or functionality beyond validated fixes

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save the corrected app.py and all templates/*.html
- Focus exclusively on applying fixes identified in validation reports; no feature additions
- Final deliverables must pass all previous validations and align 100% with design_spec.md
- Ensure file naming and directory structures are preserved exactly as provided

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
        ("DesignMerger", """Ensure design_candidate_a.md contains full and correct page routes, element IDs, and data access contracts for merging.""", [{'type': 'text_file', 'name': 'design_candidate_a.md'}])
    ],

    'DesignAnalystB': [
        ("DesignMerger", """Verify design_candidate_b.md completeness and feasibility covering all required UI features and local file data handling.""", [{'type': 'text_file', 'name': 'design_candidate_b.md'}])
    ],

    'DesignMerger': [
        ("ImplementationEngineerA", """Check design_spec.md for clarity, completeness, and readiness to guide Python Flask app implementation with local text files.""", [{'type': 'text_file', 'name': 'design_spec.md'}])
    ],

    'ImplementationEngineerA': [
        ("ImplementationMerger", """Evaluate app_candidate_a.py and templates_candidate_a/*.html for compliance with design_spec.md and proxy-test readiness.""", [{'type': 'text_file', 'name': 'app_candidate_a.py'}, {'type': 'text_file', 'name': 'templates_candidate_a/*.html'}])
    ],

    'ImplementationEngineerB': [
        ("ImplementationMerger", """Check app_candidate_b.py and templates_candidate_b/*.html independently for feature completeness and code correctness.""", [{'type': 'text_file', 'name': 'app_candidate_b.py'}, {'type': 'text_file', 'name': 'templates_candidate_b/*.html'}])
    ],

    'ImplementationMerger': [
        ("ValidationEngineerA", """Verify merged app.py and templates/*.html are a coherent, functional Flask app fully compatible with design_spec.md and web tests.""", [{'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerA': [
        ("RepairMerger", """Check validation_a.md for detailed functional correctness and any implementation issues before merging repairs.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'ValidationEngineerB': [
        ("RepairMerger", """Review validation_b.md for completeness of testing and verify all reported issues are addressed in repairs.""", [{'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
    ],

    'RepairMerger': [
        ("DesignMerger", """Ensure final app.py and templates/*.html fully satisfy the design_spec.md and incorporate all fixes from validations.""", [{'type': 'text_file', 'name': 'validation_a.md'}, {'type': 'text_file', 'name': 'validation_b.md'}, {'type': 'text_file', 'name': 'app.py'}, {'type': 'text_file', 'name': 'templates/*.html'}])
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

    # Parallel design creation
    await asyncio.gather(
        execute(DesignAnalystA, "Create a complete, detailed standalone design specification for the MusicStreaming app. Save as design_candidate_a.md"),
        execute(DesignAnalystB, "Produce an alternative full design specification for the MusicStreaming app emphasizing stable IDs and flexible UI. Save as design_candidate_b.md")
    )

    # Read outputs of both analysts
    design_a_content, design_b_content = "", ""
    try:
        design_a_content = open("design_candidate_a.md").read()
    except:
        pass
    try:
        design_b_content = open("design_candidate_b.md").read()
    except:
        pass

    # Merge the two design specifications into one unified design_spec.md
    await execute(DesignMerger,
                  f"=== DesignAnalystA Output ===\n{design_a_content}\n\n=== DesignAnalystB Output ===\n{design_b_content}\n")
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

    # Parallel implementations by EngineerA and EngineerB
    await asyncio.gather(
        execute(
            ImplementationEngineerA,
            "Implement standalone Python Flask app and templates (app_candidate_a.py, templates_candidate_a/*.html) "
            "based on user_task_description and design_spec.md. Include data parsing from local text files, all routes, "
            "correct element IDs, and no-auth functionality."
        ),
        execute(
            ImplementationEngineerB,
            "Independently implement Python Flask app and templates (app_candidate_b.py, templates_candidate_b/*.html) "
            "fully satisfying user_task_description and design_spec.md with local text file data handling and stable no-auth routes."
        )
    )

    # Read outputs from EngineerA and EngineerB for merging
    app_a_code, app_b_code = "", ""
    templates_a, templates_b = "", ""
    try:
        app_a_code = open("app_candidate_a.py").read()
    except Exception:
        pass
    try:
        app_b_code = open("app_candidate_b.py").read()
    except Exception:
        pass
    try:
        # reading templates_candidate_a/*.html as a concatenated string for injection
        import glob
        files_a = glob.glob("templates_candidate_a/*.html")
        templates_a = ""
        for f in files_a:
            try:
                templates_a += f"=== {f} ===\n" + open(f).read() + "\n\n"
            except Exception:
                continue
    except Exception:
        templates_a = ""
    try:
        # reading templates_candidate_b/*.html as a concatenated string for injection
        import glob
        files_b = glob.glob("templates_candidate_b/*.html")
        templates_b = ""
        for f in files_b:
            try:
                templates_b += f"=== {f} ===\n" + open(f).read() + "\n\n"
            except Exception:
                continue
    except Exception:
        templates_b = ""

    # Merge implementations into final app.py and templates/*.html
    await execute(
        ImplementationMerger,
        f"Merge app_candidate_a.py and app_candidate_b.py along with templates_candidate_a/*.html and templates_candidate_b/*.html "
        f"to produce final app.py and templates/*.html. Ensure stable routes, correct element IDs, robust file parsing, "
        f"and full compliance with design_spec.md and user_task_description.\n\n"
        f"=== app_candidate_a.py ===\n{app_a_code}\n\n"
        f"=== app_candidate_b.py ===\n{app_b_code}\n\n"
        f"=== templates_candidate_a.html files ===\n{templates_a}\n\n"
        f"=== templates_candidate_b.html files ===\n{templates_b}"
    )
# Phase2_End

# Phase3_Start

async def verification_phase():
    # Declare agents
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
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=60
    )

    # Parallel validation by ValidationEngineerA and ValidationEngineerB
    await asyncio.gather(
        execute(ValidationEngineerA,
                "Validate final app.py and templates/*.html using validate_python_file and execute_python_code tools. "
                "Check syntax, routes, UI element IDs, data file access, and produce comprehensive validation report named validation_a.md."),
        execute(ValidationEngineerB,
                "Perform full validation of final app.py and templates/*.html for correct features, data handling, UI elements, "
                "navigation, and end-to-end testing. Use validate_python_file and execute_python_code. Write detailed report to validation_b.md.")
    )

    # Read outputs from validation reports for RepairMerger
    validation_a_content, validation_b_content = "", ""
    try:
        validation_a_content = open("validation_a.md").read()
    except:
        pass
    try:
        validation_b_content = open("validation_b.md").read()
    except:
        pass

    # RepairMerger merges validation results and applies fixes producing final app and templates
    await execute(RepairMerger,
                  f"=== ValidationEngineerA Report ===\n{validation_a_content}\n\n"
                  f"=== ValidationEngineerB Report ===\n{validation_b_content}\n\n"
                  "Analyze these reports, identify all necessary fixes for app.py and templates/*.html, "
                  "apply corrections to produce final robust and compliant Flask application outputs.")
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
