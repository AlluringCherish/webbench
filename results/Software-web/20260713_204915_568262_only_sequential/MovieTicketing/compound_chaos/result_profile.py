# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze user requirements and produce a comprehensive design_spec.md detailing pages, routes, elements, and data files.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst produces requirements_analysis.md based on the user task description; "
        "WebArchitect then reads requirements_analysis.md to generate design_spec.md specifying Flask routes, page titles, element IDs, "
        "data storage formats, and flexible parsing contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Business Analyst specializing in software requirements elicitation and documentation.

Your goal is to analyze the user's task description to identify and trace all user-visible pages, UI elements, data entities, and storage requirements, and produce a detailed requirements analysis document.

Task Details:
- Read user_task_description artifact thoroughly to extract all pages, elements, and data specifications
- Produce requirements_analysis.md with exact tracing of each page's purpose, elements with IDs and types, and data file formats
- Ensure complete coverage of the eight specified web pages and six data files as described by the user
- Include precise descriptions of UI elements and their functionalities

Documentation Requirements:
1. Pages and UI Elements:
   - List each page with its title and overview
   - Enumerate all element IDs per page with type (Div, Button, Input, etc.) and role
   - Include dynamic element ID patterns (e.g., view-movie-button-{movie_id})

2. Data Entities and Storage:
   - List each data file by filename with field names and order
   - Provide examples illustrating data content format
   - Note parsing constraints such as delimiter usage and no header lines

3. Navigation and Functional Flow:
   - Detail navigation flows between pages via buttons and links
   - Specify filters and dropdown options where applicable

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output the requirements_analysis.md file
- Preserve exact input artifact content structure and terminology
- Provide clear, concise, and comprehensive tracing suitable for technical translation by WebArchitect

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
            "prompt": """You are a Web Architect specializing in Flask web application design and specification.

Your goal is to convert the detailed requirements analysis into a comprehensive design specification document that defines all Flask routes, HTTP methods, page titles, element IDs, navigation flows, and data parsing contracts for text files.

Task Details:
- Read requirements_analysis.md and user_task_description artifacts
- Produce design_spec.md that specifies:
  - Flask routes with URL patterns, function names, HTTP methods (GET/POST)
  - Page titles and exact page container element IDs
  - All UI element IDs with types for each page, including dynamic formats
  - Navigation mappings between pages via buttons and links using url_for functions
  - Data file contracts specifying filenames, field order, delimiters, and example data
- Ensure parsing contracts are detailed and reflect flexible but exact requirements from the data files
- Define a complete contract for all six specified data files with field names and examples

Design Specification Requirements:
1. Flask Routes Specification:
   - List all routes by URL pattern and function name (snake_case)
   - Specify method (GET or POST) per route
   - Specify template file to render per route
   - Include context variables and their types passed to templates

2. Page and Element Specification:
   - Exactly specify page container IDs and page titles
   - List all element IDs per page with element types (Div, Button, Input, Dropdown, Table, etc.)
   - Specify patterns for dynamic element IDs with placeholders

3. Navigation Flow:
   - Map all navigation buttons to corresponding routes via url_for
   - Include static and dynamic navigations (with parameters)

4. Data Parsing Contracts:
   - For each data file, specify:
     - Filename and path (data/)
     - Exact field order using pipe '|' delimiter
     - Data description
     - 2-3 realistic example rows from user data
   - Note absence of header lines and parsing approach

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Follow user task definitions strictly without assumptions
- Ensure consistency of element IDs between navigation and pages
- Provide clear and unambiguous specifications for backend developers

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
            "review_criteria": (
                "Verify requirements_analysis.md contains complete and accurate tracing of all user-visible pages, elements, "
                "and data storage requirements before architecture proceeds."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the MovieTicketing Flask web application with exact requested routes, templates, and data handling.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes app_draft.py and all templates_draft/*.html from design_spec.md; "
        "IntegrationEngineer then refines these drafts into final app.py and templates/*.html enforcing exact routes, element IDs, and data parsing."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "prompt": """You are a Flask web developer specializing in Python web applications.

Your goal is to develop a draft Flask application and all required HTML templates implementing the specifications for a movie ticketing system.

Task Details:
- Read design_spec.md and user_task_description thoroughly
- Produce a draft Flask app named app_draft.py including routes for all 8 pages
- Create draft HTML templates under templates_draft/ with correct page titles and all specified element IDs
- Implement navigation buttons as specified to enable page transitions starting from Dashboard
- Parse local text-based data files as described, ensuring data fields and formats align with design spec and user task

Implementation Requirements:
1. **Flask App Structure**:
   - Use Flask routing and view functions
   - Define routes matching all 8 pages and their functionalities
   - Ensure the '/' route redirects to Dashboard page route
   - Use render_template() referencing templates in templates_draft/

2. **Data Handling**:
   - Load and parse text data files locally with exact field orders and pipe-delimited format
   - Handle files: movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt
   - Prepare data as dicts or lists for passing to templates

3. **Templates Drafts**:
   - Place template files in templates_draft/ directory
   - Implement specified element IDs exactly as per user task page design
   - Include page titles matching specified titles in <title> and <h1> tags
   - Include navigation buttons with IDs to transition between pages
   - Implement dynamic IDs using Jinja2 where applicable (e.g., view-movie-button-{movie_id})

4. **Routing and Navigation**:
   - Ensure all navigation buttons and links use url_for() pointing to correct Flask route functions
   - Navigation must start from Dashboard page on app launch

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to output app_draft.py and all templates in templates_draft/
- Maintain exact element ID naming and page titles as per user task
- Follow data file formats exactly for loading and parsing
- The draft app and templates must be functional but can allow placeholder content where required

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
            "prompt": """You are a Python Flask integration specialist experienced in refining draft web applications.

Your goal is to refine the draft Flask app and HTML templates into final production-ready code that strictly conforms to all route specifications, element IDs, and data parsing rules for the movie ticketing system.

Task Details:
- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description
- Produce finalized app.py implementing all routes starting from Dashboard page with exact route behaviors
- Refine templates/*.html from templates_draft/ enforcing exact element IDs and layout consistency
- Ensure stable, robust parsing of all local text-based data files as specified (movies.txt, theaters.txt, showtimes.txt, seats.txt, bookings.txt, genres.txt)
- Enforce all navigation buttons and links correspond to correct Flask routes

Refinement Requirements:
1. **Routing**:
   - Confirm '/' route redirects accurately to Dashboard route
   - Validate that all endpoints precisely match design_spec.md definitions
   - Ensure HTTP methods and route parameters are correctly handled

2. **Templates**:
   - Adopt all element IDs exactly as specified without deviation
   - Maintain accurate page titles in <title> and <h1>
   - Fix any draft template inconsistencies in layout or element presence

3. **Data Handling**:
   - Confirm data files are parsed with correct delimiter and exact field orders
   - Include error handling for file reading
   - Data passed to templates must match design specification exactly

4. **Final Integration**:
   - Test navigation flows start from Dashboard with all buttons functional
   - Ensure no placeholder content remains; all pages fully implement their data presentation

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to output final app.py and all templates in templates/
- Strictly maintain all element IDs and route names as defined
- Data parsing must be robust and conform exactly to file schemas
- Final code and templates must be complete and production-ready

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "ImplementationEngineer"},
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
            "source_agent": "ImplementationEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Review app_draft.py and templates_draft/*.html to ensure full compliance with design_spec.md, including correct routes, "
                "element IDs, and local file data handling."
            ),
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
    goal: str = "Validate the completed app.py and templates/*.html for correctness, completeness, and runnability.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator runs syntax and runtime validation on app.py and templates/*.html, producing validation_report.md; "
        "SequentialFixer then applies fixes and writes final artifacts."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in Flask web application validation and verification.

Your goal is to thoroughly validate the app.py and HTML templates, ensuring correctness in syntax, runtime stability, route handling, and compliance with the design specification. Deliver a detailed validation_report.md documenting all findings.

Task Details:
- Read design_spec.md, app.py, templates/*.html, and user_task_description from CONTEXT
- Validate app.py for Python syntax and runtime errors using tools
- Validate templates/*.html for correct structure, element IDs, and content matching design_spec.md
- Verify all Flask routes exist and handle requests as specified in design_spec.md
- Check stable interaction with data files (file paths, parsing, field orders)
- Produce validation_report.md with all validation results and issues found

Validation Requirements:
1. **Syntax Validation**:
   - Use validate_python_file tool on app.py
   - Identify any syntax or runtime errors preventing app start

2. **Runtime Testing**:
   - Use execute_python_code tool to run app.py minimally to detect runtime exceptions on start

3. **Design Compliance**:
   - Confirm routes in app.py match design_spec.md Section 1 (function names, decorators)
   - Confirm context variables passed to templates correspond exactly to design_spec.md
   - Validate templates/*.html contain all required element IDs and match design_spec.md Section 2 content and structure
   - Check page titles and navigation mappings are accurate

4. **Data File Handling**:
   - Check file paths and loading logic in app.py match design_spec.md Section 3
   - Verify data parsing uses correct field order, no headers assumed unless specified

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for code verification
- Use write_text_file tool to output validation_report.md documenting all findings with examples
- Provide clear, actionable comments for any issues discovered
- Focus strictly on inputs given; do not extend beyond specified artifacts

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
            "prompt": """You are a Software Engineer specializing in automated code correction and integration for Flask web applications.

Your goal is to apply necessary corrections from the provided validation_report.md to finalize app.py and templates/*.html, ensuring the entire MovieTicketing application fully meets all user requirements and design specifications.

Task Details:
- Read validation_report.md, design_spec.md, app.py, templates/*.html, and user_task_description from CONTEXT
- Identify all issues flagged in validation_report.md
- Correct app.py syntax, runtime, route handling, and data file usage errors
- Fix templates/*.html defects including missing element IDs, incorrect content, navigation, and title mismatches
- Maintain full compliance with design_spec.md and user_task_description
- Deliver corrected artifact files: app.py and templates/*.html

Correction Requirements:
1. **Code Corrections**:
   - Fix all syntax and runtime errors preventing proper app operation
   - Ensure routes correspond exactly with design_spec.md Section 1 specifications
   - Verify all context variables are consistent and complete

2. **Template Corrections**:
   - Add or fix missing element IDs and ensure exact naming
   - Adjust page titles and navigation buttons as per design_spec.md Section 2
   - Preserve Jinja2 templating where applicable and test for rendering readiness

3. **Data Handling**:
   - Confirm data file loads parse fields in exact order as design_spec.md Section 3
   - Do not introduce new features beyond fixing reported issues

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html
- Fully resolve all issues reported in validation_report.md with traceability to requirements
- Maintain original artifact file names and formats exactly
- Focus exclusively on artifacts listed; do not generate unrelated files

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
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
            "review_criteria": (
                "Ensure that validation_report.md accurately identifies syntax, runtime, and design compliance issues."
            ),
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
            "review_criteria": (
                "Verify that final app.py and templates/*.html fully resolve all issues from validation_report.md while maintaining full "
                "traceability to user requirements."
            ),
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
    goal: str = "Develop and deliver a Python Flask-based MovieTicketing web application handling local text file data storage as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce the design specification for the application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the detailed design specification document."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask app and HTML templates according to design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop the application code and templates from the design specification."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the application to ensure correctness and completeness.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Perform validation and final fixes to produce a runnable MovieTicketing app."}
            ]
        }
    ]
): pass
# Orchestrate_End