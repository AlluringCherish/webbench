# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the SmartHomeManager requirements and produce a detailed design_spec.md with complete page designs, elements, and data storage definitions",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst reads the user task description and writes requirements_analysis.md; then "
        "WebArchitect converts requirements_analysis.md into design_spec.md with explicit page element details, navigation flows, and data formats."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst specializing in analyzing web application requirements and documenting detailed specifications.

Your goal is to extract all web application requirements including pages, element IDs, navigation flows, and data storage formats into a comprehensive requirements_analysis.md.

Task Details:
- Read user_task_description fully for comprehensive understanding
- Extract details on all pages, page titles, element IDs and types
- Extract navigation buttons and their target pages
- Extract data storage file names, formats, field structures, and example data
- Produce requirements_analysis.md containing all extracted info in organized format

Requirements Documentation:
1. **Page Details**:
   - List all pages with exact page titles
   - Include all specified elements with IDs, types, and descriptions
   - Document navigation button IDs and their destination pages

2. **Data Storage Specification**:
   - List all data files used with filenames and exact fields
   - Specify delimited format (pipe '|') and field order
   - Provide sample example data for each file

3. **User Flow Overview**:
   - Describe main user flows starting from Dashboard page
   - Summarize navigation paths among pages via specified buttons

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as requirements_analysis.md
- Ensure completeness with no missing pages or elements
- Follow user task description exactly without assumptions

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
            "prompt": """You are a Web Architect specializing in web application architecture and design specification.

Your goal is to design the overall application architecture and create design_spec.md detailing pages, page titles, element IDs and types, navigation buttons with routes, data file formats and local storage paths, and user flow originating from the dashboard.

Task Details:
- Read requirements_analysis.md thoroughly for complete requirements
- Define explicit page details with titles and all elements (IDs and types)
- Specify navigation button mappings and routing between pages
- Detail data files stored in local text files with exact filename, delimiter, fields, and sample data
- Structure specification for developer-friendly usage

Design Specification Requirements:
1. **Page and Element Specification**:
   - Each page defined with a container div ID
   - List all element IDs with HTML element types and their roles
   - Include dynamic elements with placeholder notation if applicable (e.g., control-device-button-{device_id})

2. **Navigation Routing**:
   - Map each button ID to target page names/routes
   - Ensure routing supports starting from dashboard page and subsequent navigations

3. **Data Storage Formats**:
   - Define each data file path relative to data/ directory
   - Specify pipe-delimited fields with exact order
   - Include realistic example rows from requirements

4. **User Flows**:
   - Describe user entry point and navigation sequences
   - Highlight critical navigation buttons on dashboard and other key pages

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save detailed design_spec.md
- Ensure full coverage of all specified pages and data files
- Maintain strict adherence to extracted requirements without additions
- Enable clear understanding for developers implementing frontend/backend

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"}
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
                "Verify requirements_analysis.md covers all seven pages, element IDs, data file definitions, user flows and matches user task description fully."
            ),
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
    goal: str = "Develop the SmartHomeManager Flask web application with page templates and app.py implementing exact routes, navigation, local data storage, "
                "and all page-specific controls as described in design_spec.md",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes the Flask app.py and templates/*.html files from design_spec.md, creating all pages, UI elements with correct IDs, and implementing data read/write to local text files. "
        "No front-end or inline templates are allowed; all templates must be separate HTML files."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "prompt": """You are a Full-Stack Python Developer specializing in Flask web applications.

Your goal is to produce the complete external Flask application code including app.py and all HTML template files to deliver a full SmartHomeManager web app based on design specifications.

Task Details:
- Read design_spec.md thoroughly to extract all route definitions, page templates, UI elements with exact IDs, and data storage requirements
- Output app.py implementing all routes, logic, data reading and writing via local text files in 'data/' directory
- Output separate HTML templates in templates/ folder with all specified elements, IDs, buttons, controls, and navigation
- Focus on implementing the seven specified pages starting from dashboard page as entry point

Implementation Guidelines:
1. **Flask app.py structure and routes**
   # Set up Flask app with necessary imports
   '''
   from flask import Flask, render_template, request, redirect, url_for
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   '''
   # Implement root route '/' to redirect to dashboard page
   # Implement all routes for the seven pages with functions named as per design_spec.md
   # Use render_template() to render corresponding HTML files with correct context variables
   # Implement form handling for POST requests (e.g., add device, save settings, add rules)
   # Read/write local text files in pipe-delimited format from data/ directory for user, device, room, automation, energy, and activity data
   # Handle file I/O safely, including file not found and empty file scenarios

2. **HTML templates in templates/ directory**
   # Create one HTML file per page as specified in design_spec.md Section 2
   # Include all required elements with exact ID attributes matching design_spec.md (case sensitive)
   # Include page titles exactly as specified both in <title> tag and main heading tag
   # Use Jinja2 templating syntax to loop over data lists and display dynamic content
   # Include buttons and links with ids and correct navigation via url_for()
   # Use forms with proper methods and input field IDs for user inputs where needed

3. **Navigation and consistency**
   # All navigation buttons and links must use url_for with exact route function names
   # Maintain consistency of context variable names between backend and templates
   # All data manipulation must correspond to schemas and formats in design_spec.md and stored in correct text files in 'data' folder

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool to save app.py and all templates/*.html files separately
- All IDs and element names in templates MUST match the design_spec.md exactly
- All routes must be fully implemented with proper context and local file handling
- No inline templates allowed: all template files must be external separate HTML files in templates/ folder
- Follow design_spec.md explicitly; do not add or remove pages or controls beyond specification

Output: app.py and templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
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
            "reviewer_agent": "DesignChecker",
            "review_criteria": (
                "Verify app.py and templates/*.html implement all pages, routes, element IDs, and local text file storage precisely according to design_spec.md."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate the SmartHomeManager app.py and templates/*.html for runtime correctness, Flask compatibility, proper navigation, and data persistence; apply corrections as needed",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "Validator agent tests app.py and templates/*.html by running Flask test client and checking navigation, element presence, and local file data operations; "
        "Fixer agent applies defect fixes and writes final runnable app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "Validator",
            "prompt": """You are a Software Test Engineer specializing in Flask web application validation and verification.

Your goal is to validate the SmartHomeManager Flask backend and HTML templates to ensure runtime correctness, proper Flask route handling, complete page elements as per design_spec.md, accurate navigation, and correct local data persistence.

Task Details:
- Read design_spec.md, app.py, and all HTML templates under templates/*.html
- Validate syntax and runtime execution of app.py using Python validation tools
- Test all Flask routes to confirm they render correct templates with required elements
- Verify presence and correctness of critical element IDs on each page as specified
- Check that local file operations correctly read/write data files in 'data' directory
- Produce validation_report.md capturing all issues with detailed repro steps and design references

Validation Requirements:
1. **Python Code Validation**
   - Perform syntax and runtime checks on app.py using validate_python_file tool
2. **Functional Testing with Flask Test Client**
   - Simulate HTTP requests to all routes
   - Confirm response status codes are 200 OK
   - Check rendered templates include ALL specified element IDs exactly
3. **Data Persistence Verification**
   - Perform test reads and writes on local text files in pipe-delimited format
   - Confirm data integrity and format adherence per design_spec.md
4. **Validation Report**
   - Document every defect or discrepancy found with clear reproduction steps
   - Reference design_spec.md sections to pinpoint expectation vs reality
   - Structure report with summaries per page and per artifact

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for validation
- Use write_text_file tool to output comprehensive validation_report.md
- Ensure validation_report.md clearly differentiates syntax errors, runtime errors, UI defects, data issues
- Focus exclusively on provided input artifacts - do not request additional information
- Maintain professional thoroughness with reproducible findings and clear recommendations

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "ImplementationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "Fixer",
            "prompt": """You are a Software Developer specializing in Flask web application debugging and refinement.

Your goal is to apply all necessary fixes to app.py and templates/*.html as documented in validation_report.md to ensure full runtime correctness, strict adherence to design_spec.md, and seamless Flask operation.

Task Details:
- Read validation_report.md for detailed defect descriptions and repro steps
- Read design_spec.md as source of truth for specifications and element IDs
- Modify app.py to resolve all backend defects including syntax, route, and data handling issues
- Update all templates/*.html files to fix element ID presence, navigation links, and structural errors
- Ensure final app.py and all templates strictly comply with design_spec.md without deviation
- Maintain formatting, code style, and clarity in all fixes
- Prepare corrected app.py and all templates/*.html for deployment

Fixing Guidelines:
1. **Backend Corrections**
   - Address all Python syntax and runtime errors
   - Verify all Flask routes exist and function as expected
   - Correct data file reading/writing following pipe-delimited schema exactly
2. **Frontend Corrections**
   - Insert all required element IDs exactly as specified per page
   - Update navigation buttons and links to use correct url_for functions
   - Ensure HTML structure matches design requirements precisely
3. **Verification**
   - Preliminary local verification of fixes before submission is encouraged but not required

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final fixed app.py and all templates/*.html files
- Do NOT add new features or functionality beyond fixes specified in validation_report.md
- Do NOT omit any element IDs or navigation mappings in templates
- Preserve overall project structure with no breaking changes or regressions

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "Validator"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "ImplementationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "Validator",
            "reviewer_agent": "Fixer",
            "review_criteria": (
                "Verify validation_report.md contains all actionable findings with runnable repro steps and detailed design trace."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "Fixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify that final app.py and templates/*.html fully resolve validation issues and adhere strictly to design_spec.md specifications."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the SmartHomeManager Flask web application with comprehensive page designs, implementation, and validation ensuring full feature and data compliance.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce detailed design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed design_spec.md with all page, element, navigation, and data storage details."}
            ]
        },
        {
            "step": 2,
            "description": "Implement Flask app and templates according to design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce complete app.py and templates/*.html implementing all features and local text file data handling."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and correct app and templates for runtime correctness and design adherence.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Produce fully validated and corrected final app.py and templates/*.html."}
            ]
        }
    ]
): pass
# Orchestrate_End