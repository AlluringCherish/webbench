# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the GymMembership requirements and produce a detailed design_spec.md outlining pages, elements, navigation, and data formats.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md detailing all pages, elements, and data storage; "
        "then WebArchitect reads requirements_analysis.md and produces design_spec.md defining Flask routes, templates, page IDs, "
        "navigation flows, data file use, and context variable contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst specializing in comprehensive web application requirements gathering.

Your goal is to produce a thorough requirements_analysis.md document enumerating all pages, UI elements with their IDs, navigation flows, and local data file specifications based on user-provided task descriptions.

Task Details:
- Read user_task_description to identify all pages and their intended functions
- Extract all UI elements with exact IDs per page
- Detail navigation buttons and their target pages
- Specify data storage files with exact fields and formats as provided
- Generate requirements_analysis.md including above details for architect use

Requirements Documentation:
1. **Page and Element Enumeration**
   - List each page by name and exact title
   - For each page, detail all UI elements with their element IDs and types
2. **Navigation Mapping**
   - Specify all navigation buttons/links with source and destination pages
3. **Data Storage Specification**
   - Detail each data file: filename, field names and order, data format (pipe-delimited)
   - Include sample data as examples

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save requirements_analysis.md
- Preserve exact element IDs and data field orders from user requirements
- Ensure clarity and completeness for WebArchitect's usage
- No assumptions beyond given user_task_description

Output: requirements_analysis.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "agent_name": "WebArchitect",
            "prompt": """You are a Web Architect specializing in Flask web application design specifications.

Your goal is to create a detailed design_spec.md document for the GymMembership Flask app, transforming requirements_analysis.md into comprehensive route-to-template mappings, page element IDs, navigation flows, data file formats, and context variable contracts suitable for independent backend and frontend development.

Task Details:
- Read requirements_analysis.md thoroughly and user_task_description for complete context
- Produce design_spec.md including:
  - Flask routes table mapping URLs to templates and handler function names
  - Exact element IDs per page as defined in requirements_analysis.md
  - Navigation mappings with button IDs directing to Flask routes
  - Data file usage details: reading and writing methods, exact field order
  - Context variable structures passed from routes to templates

Design Specification Structure:
1. **Flask Routes**
   - Define all routes starting with root '/' redirecting to Dashboard
   - Include function names, HTTP methods, template files, and context variables with types
2. **HTML Templates**
   - Specify each template file under templates/, page titles, and all required element IDs with types
   - Map navigation buttons to route functions with url_for calls
3. **Data File Schemas**
   - Specify data files under data/, pipe-delimited fields with exact orders and example data
   - Clarify data loading and saving format expected in backend

Consistency and Conventions:
- Function names in snake_case matching page purposes
- Context variable names consistent between routes and templates
- Navigation flows must use exact button IDs and route names from specifications

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Preserve all element IDs and data field orders exactly as in requirements_analysis.md
- Ensure routes, templates, and data schemas enable independent backend/frontend implementations
- Include sufficient detail to avoid ambiguities
- Root route '/' must redirect to 'dashboard' route
- Do NOT add features or pages not specified in requirements_analysis.md or user_task_description

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "RequirementsAnalyst",
            "reviewer_agent": "WebArchitect",
            "review_criteria": "Verify that requirements_analysis.md captures every page, element ID, navigation button, and data file structure exactly as requested without omissions.",
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the GymMembership Flask application as app_draft.py and templates_draft/*.html consistent with design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html following design_spec.md, implementing exact routes,"
        "page titles, element IDs, local text-file data access, and navigation flows; IntegrationEngineer then refines these into final app.py and "
        "templates/*.html, removing draft artifacts and ensuring readiness for validation."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "prompt": """You are a Backend and Frontend Developer specializing in Flask web application draft implementations.

Your goal is to write the Flask application draft (app_draft.py) and all related HTML templates in the templates_draft/ directory, strictly following design_spec.md.

Task Details:
- Read design_spec.md and user_task_description from CONTEXT
- Implement all Flask routes as specified in design_spec.md with exact function names
- Use local plaintext data files (data/*.txt) as specified for data loading and saving
- Implement HTML templates with all specified element IDs and page titles exactly
- Ensure the root route '/' redirects or serves the Dashboard page as specified
- Output app_draft.py and templates_draft/*.html files reflecting draft status but with full functionality

Implementation Guidelines:
1. Flask App Draft:
   - Set up Flask app with required routes, handlers, and data file accesses
   - Follow design_spec.md for precise route paths, HTTP methods, and context variables
   - Use Python standard file I/O for reading/writing pipe-delimited text files
   - Implement form handling for POST routes
   - Maintain dashboard as root route

2. HTML Templates Draft:
   - Create full-featured HTML templates in templates_draft/ directory
   - Use exact element IDs and page titles from design_spec.md
   - Use Jinja2 templating syntax for context variables and loops
   - Implement navigation buttons linking to Flask routes exactly
   - Include draft indicators in filenames or comments to distinguish draft status

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app_draft.py and all templates in templates_draft/
- Must not add or omit routes or elements beyond design_spec.md specifications
- Ensure data file reading/parsing matches design_spec.md field order exactly
- Root route '/' must serve or redirect to Dashboard
- Templates must include all specified element IDs exactly as per design_spec.md

Output: app_draft.py, templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "prompt": """You are a Software Integration Engineer specializing in finalizing Flask web applications.

Your goal is to convert the draft Flask app (app_draft.py) and draft templates (templates_draft/*.html) into finalized, polished versions (app.py, templates/*.html) fully compliant with design_spec.md.

Task Details:
- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description from CONTEXT
- Remove draft-specific artifacts, comments, or placeholders from code and templates
- Refine and polish app.py and templates to match exact UI element IDs, route implementations, and page titles
- Ensure data file access and parsing strictly follow design_spec.md schemas and formats
- Enforce root Dashboard page as root route '/' with correct navigation
- Produce clean, production-ready code and templates suitable for validation and deployment

Refinement Guidelines:
1. Flask App Finalization:
   - Clean up draft artifacts and comments
   - Verify all routes exist and use exact function names as per design_spec.md
   - Confirm data file reading/writing matches specified field orders
   - Optimize code readability and maintain functionality

2. HTML Templates Finalization:
   - Remove draft indicators, placeholders, and comments
   - Verify all element IDs exist exactly as specified
   - Confirm page titles and navigation links match design_spec.md exactly
   - Ensure Jinja2 templating conforms to Flask usage standards

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save finalized app.py and templates/*.html
- Ensure full compliance with design_spec.md UI element IDs, route names, and page titles
- Maintain root route '/' as Dashboard page with correct navigation
- Do not add functionality beyond design_spec.md requirements
- Output must be clean and ready for validation testing

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DraftEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": "Check accuracy of app_draft.py and templates_draft/*.html against design_spec.md for route correctness, element IDs, data file handling, and navigation.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate and fix the final Flask application producing a fully runnable app.py and templates/*.html that meet all requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator validates the final app.py and templates/*.html for runtime errors, route availability, data file accesses, and UI element presence, "
        "then SequentialFixer applies corrections based on validation_report.md ensuring full functionality and compliance."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in validating Flask web applications.

Your goal is to ensure the final Flask app.py and templates/*.html are fully functional, error-free, and meet all specified user requirements.

Task Details:
- Read design_spec.md, app.py, templates/*.html, and user_task_description from context
- Produce a comprehensive validation_report.md detailing syntax/runtime errors, route existence, and UI element presence
- Focus on runtime correctness of Flask app, availability of all required routes, and required UI elements on all pages

Validation Objectives:
1. **Syntax and Runtime Validation**:
   - Use validate_python_file and execute_python_code tools to check app.py syntax and runtime
   - Report detailed errors with file lines and messages

2. **Route Verification**:
   - Confirm all Flask routes from design_spec.md exist in app.py
   - Test routes respond with status code 200 or appropriate redirects
   - Verify root (/) route redirects to dashboard page

3. **Template Content Verification**:
   - Parse templates/*.html to ensure all requested HTML pages exist
   - Verify all required element IDs are present on their corresponding pages
   - Check that navigation elements and buttons match the specifications

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for all code checks
- Use write_text_file tool to save detailed validation_report.md
- Clearly state all detected issues and improvement suggestions
- Validation report MUST enable SequentialFixer to accurately locate and fix problems

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "prompt": """You are a Backend Developer specializing in Flask applications and frontend HTML templating.

Your goal is to analyze validation_report.md and produce corrected app.py and templates/*.html that fully comply with GymMembership requirements and fix all identified issues.

Task Details:
- Read validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description from context
- Implement fixes to app.py to resolve all runtime, routing, and data file access issues
- Update templates/*.html to add missing UI elements, fix incorrect IDs, and correct navigation flows
- Ensure the final outputs are fully functional and consistent with all design specifications and user requirements

Fix Implementation Guidelines:
1. **Code Corrections**:
   - Use write_text_file tool to save revised app.py
   - Focus on fixing syntax, runtime errors, and missing or incorrect routes
   - Verify data file accesses follow design_spec.md schema exactly

2. **Template Updates**:
   - Use write_text_file tool to save corrected templates/*.html files individually
   - Include all required element IDs and correct page titles
   - Match navigation and dynamic element naming as per design_spec.md

3. **Consistency and Completeness**:
   - Maintain naming consistency with design_spec.md and user requirements
   - Ensure root route redirects to dashboard page
   - Do not add functionality beyond original specifications

CRITICAL REQUIREMENTS:
- Use write_text_file tool exclusively for output files
- Preserve exact naming, ID conventions, and file structures per original design_spec.md
- Deliver fully runnable Flask app with complete UI as per requirements

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "WebValidator",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": "Ensure validation_report.md identifies all runtime, routing, and UI element inconsistencies for repair.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm that fixed app.py and templates/*.html fully implement the original user requirements and design specifications.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a complete GymMembership Python Flask application managing all specified pages and local text file storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce detailed design specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce a detailed design_spec.md covering all app design aspects."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the GymMembership app draft and finalize source and templates.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce a complete Flask app.py and templates as per design_spec.md."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the final Flask app producing a fully functional GymMembership application.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Deliver a validated and corrected runnable Flask app with templates."}
            ]
        }
    ]
): pass
# Orchestrate_End