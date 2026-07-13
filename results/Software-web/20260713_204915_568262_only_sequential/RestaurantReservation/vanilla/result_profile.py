# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the RestaurantReservation requirements and produce design_spec.md detailing Flask routes, page structure, element IDs, and data management using local text files.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md capturing all page elements, navigation, and user stories; "
        "then WebArchitect reads requirements_analysis.md and produces design_spec.md covering Flask app routing, template filenames and locations, "
        "exact page titles, element IDs, form inputs, data file access, and user flow ensuring dashboard as the root page."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst with expertise in web application UI/UX and data workflow analysis.

Your goal is to extract and document detailed requirements for all user-visible pages, including UI elements, user actions, data interactions, and navigation flows, producing a structured requirements_analysis.md file.

Task Details:
- Analyze user_task_description for all pages and elements, including page titles, element IDs, and user actions
- Document user workflows, navigation paths, and interactions in requirements_analysis.md
- Capture data file schemas, including exact field names and formats
- Include comprehensive descriptions and examples for clarity and exhaustiveness

Instructions:
1. Identify and list all pages with their page titles and container IDs
2. Enumerate all UI elements per page with exact element IDs, types, and descriptions
3. Describe user actions such as button clicks, form submissions, and dynamic interactions
4. Detail navigation flows linking buttons to target pages or actions
5. Describe and list data files used by the app with formats and examples

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md
- Follow markdown formatting for clarity and structure
- Preserve exact element ID names and data schema field orders
- Ensure completeness to enable downstream architecture design without omissions

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
            "prompt": """You are a Web Architect specializing in Flask web application design and architecture.

Your goal is to design a detailed Flask web app architecture document (design_spec.md) based on requirements_analysis.md that facilitates independent backend and frontend development.

Task Details:
- Read requirements_analysis.md thoroughly and consult user_task_description as needed
- Define all Flask routes mapping URLs to functions and templates, ensuring root route '/' leads to Dashboard
- Specify template filenames and locations under templates/ directory for all pages
- Document exact page titles and container element IDs for each page template
- Detail all interactive elements: buttons (with target routes), form inputs (with names, types), and expected form actions
- Specify data file accesses including exact file names in data/ directory, with pipe-delimited field schemas
- Capture user navigation flows and interactions clearly to support frontend and backend implementation

Architecture Specifications:
1. **Flask Routes:**
   - Route path (e.g., /dashboard, /menu, /dish/<int:dish_id>)
   - Function name (lowercase with underscores)
   - HTTP method (GET or POST)
   - Template filename (templates/{template_name}.html)
   - Context variables passed to template

2. **Templates:**
   - File path in templates/
   - Page title in <title> and <h1>
   - Main container element ID
   - All button and input element IDs with descriptions

3. **Forms:**
   - Input fields with names and types
   - Submit buttons with action routes

4. **Data Files:**
   - Filename in data/
   - Pipe-delimited field order and meaning
   - Usage context per route or feature

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Ensure consistency and exact matching of all element IDs, filenames, route names, and data schemas
- Root route '/' must redirect or render Dashboard page
- Provide complete architecture spanning backend routing and frontend structure
- Design must allow independent backend and frontend development without ambiguity

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
                "Verify requirements_analysis.md fully captures every user-visible page, exact element IDs, data file formats, navigation paths, "
                "and user functionality needed before architecture design."
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
    goal: str = "Implement the RestaurantReservation Flask application including app.py and templates/*.html files according to design_spec.md and requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes initial app_draft.py and all templates_draft/*.html with correct routing, page content, element IDs, forms, and data "
        "handling per design_spec.md. IntegrationEngineer then finalizes app.py and templates/*.html for deployment by replacing draft paths and closing gaps."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "prompt": """You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.

Your goal is to develop an initial draft of the complete Flask backend (app_draft.py) with all routes starting from '/' as Dashboard, and draft all corresponding HTML templates under templates_draft/*.html with full page content, element IDs, and form handling as per specifications.

Task Details:
- Read design_spec.md and user_task_description comprehensively
- Input artifacts: design_spec.md, user_task_description
- Output artifacts: app_draft.py implementing all Flask routes and logic; templates_draft/*.html with all required pages and element IDs
- Focus on correct routing, page titles, element IDs, and reading/writing pipe-delimited data files exactly as specified

Implementation Requirements:
1. **Flask Backend (app_draft.py)**
   - Implement all routes listed, starting with '/' route rendering Dashboard page
   - Use Flask render_template() referencing templates in templates_draft/
   - Read and write data from/to data/*.txt files using pipe-delimited parsing matching exact field order
   - Handle GET and POST methods for forms (reservation, reviews, profile update)
   - Implement data management for users, menu, reservations, waitlist, reviews as per data formats
   - Use clear function names consistent with page purposes
   - Provide route handlers for all specified pages without omissions

2. **Frontend Templates (templates_draft/*.html)**
   - Create Jinja2 HTML templates for each specified page inside templates_draft/
   - Include all specified element IDs exactly as required
   - Include page titles matching design_spec.md / user_task_description exactly (e.g., 'Restaurant Dashboard')
   - Implement navigation elements linking using url_for() with correct endpoint names
   - Implement forms with correct input element IDs, names, and methods matching backend route handlers
   - Use proper Jinja2 looping and conditionals for dynamic content rendering (e.g., menu items, reservations list)
   - For dynamic element IDs (e.g., view-dish-button-{dish_id}), use Jinja2 syntax: id="view-dish-button-{{ dish.dish_id }}"

3. **Data Handling**
   - Use file paths exactly as 'data/filename.txt' for all data files
   - Parse and output pipe-delimited records without header lines
   - Handle any missing or empty data gracefully in templates and routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Template files must be saved individually inside templates_draft/ directory
- All element IDs and page titles must strictly match specifications without deviation
- Data file handling must adhere exactly to field orders and formats described
- Implement only what is specified in design_spec.md and user_task_description (no extra features)
- Ensure '/' route renders Dashboard page properly

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
            "prompt": """You are a Software Integration Engineer specializing in Flask web application deployment preparation.

Your goal is to refine initial draft implementations by converting app_draft.py and templates_draft/*.html into final app.py and templates/*.html files, ensuring all routes, template references, and data file paths conform perfectly to production standards.

Task Details:
- Read design_spec.md, app_draft.py, templates_draft/*.html, and user_task_description
- Input artifacts: design_spec.md, app_draft.py, templates_draft/*.html, user_task_description
- Output artifacts: finalized app.py, templates/*.html for deployment
- Focus on removing draft paths, correcting template folder references, and enforcing '/' route as Dashboard
- Ensure all data file paths exactly match 'data/*.txt' with no deviations
- Confirm all page titles and element IDs match specifications perfectly
- Close gaps or inconsistencies found in draft implementation without adding new features

Refinement Requirements:
1. **Backend Refinement (app.py)**
   - Replace all 'templates_draft/' references with 'templates/'
   - Verify '/' route serves dashboard page
   - Validate all routes and functions correspond exactly to design_spec.md
   - Confirm data file path usage is consistent and correct
   - Eliminate any draft-specific paths, variables, or temporary code

2. **Frontend Templates (templates/*.html)**
   - Rename and move all draft HTML templates to templates/ directory
   - Ensure element IDs and page titles strictly follow design_spec.md and user_task_description
   - Verify all navigation endpoints using url_for() correspond to final route names
   - Clean any draft placeholders or annotations present in draft templates

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- All filenames and paths must be exact with no residual draft references
- Do not add or remove pages or functionality beyond specifications
- Ensure final codebase is ready for deployment with consistent naming and routing

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
            "review_criteria": (
                "Ensure app_draft.py and templates_draft/*.html implement all routes, elements, and data management from design_spec.md with accurate page titles and element IDs."
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
    goal: str = "Validate the final app.py and templates/*.html for correctness, compliance with requirements, and seamless functionality.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator performs syntax and runtime checks on app.py, ensures templates/*.html render correctly, tests route accessibility, and verifies UI elements, IDs, "
        "startup behavior, and data handling per design_spec.md. SequentialFixer applies corrections from validation_report.md and produces the final corrected application files."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in Python Flask web application validation.

Your goal is to thoroughly validate backend and frontend code to ensure compliance with specifications and flawless runtime behavior.

Task Details:
- Read input files app.py and all templates/*.html from IntegrationEngineer
- Refer to design_spec.md for expected routes, UI element IDs, and data handling rules
- Read user_task_description for overall project context and requirements
- Produce validation_report.md detailing all issues, defects, and actionable improvement suggestions

Validation Focus:
1. **Python Code Validation**
   - Perform syntax and runtime checks on app.py using validate_python_file tool
   - Confirm Flask app startup without errors
   - Verify all Flask routes are implemented per design_spec.md
   - Test route accessibility and expected HTTP methods

2. **Template Rendering Validation**
   - Render each template and verify presence of all specified element IDs exactly
   - Confirm dynamic ID patterns and static IDs are correct
   - Check Jinja2 template syntax and variable usage compliance

3. **Data Handling Verification**
   - Verify data read/write operations for all local text files match design_spec.md schemas
   - Confirm correct parsing, field order, and data loading logic
   - Check handling of file I/O errors and empty data cases

4. **Functional Behavior Testing**
   - Validate UI navigations and button actions route to correct pages
   - Confirm startup page is Dashboard
   - Check form handling behavior for POST routes
   - Validate waitlist and reservations management according to requirements

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for all code checks
- Summarize all findings clearly in validation_report.md with recommendations
- Provide precise, actionable feedback without code fixes
- Use write_text_file tool to save validation_report.md

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "prompt": """You are a Software Developer specializing in Python Flask web application bug fixing and refinement.

Your goal is to implement all corrections from validation reports to deliver a fully functional and requirements-compliant final application.

Task Details:
- Read validation_report.md summarizing detected issues and recommendations
- Read current versions of app.py and all templates/*.html from IntegrationEngineer
- Refer to design_spec.md and user_task_description for correct behavior and requirement confirmation
- Apply fixes and improvements in app.py and templates to resolve all functional, UI, and data handling defects
- Ensure stable route handling, accurate data processing, and exact UI element ID compliance
- Maintain all original functionality and structure outside of necessary fixes

Fix Implementation Requirements:
1. **Bug Fixes**
   - Correct Python syntax and runtime errors in app.py
   - Fix route and HTTP method inconsistencies
   - Repair data parsing and file I/O handling problems

2. **UI and Template Corrections**
   - Add or correct missing or incorrect element IDs in all templates
   - Fix Jinja2 syntax errors and data binding issues
   - Ensure navigation buttons route correctly

3. **Quality Assurance**
   - Confirm application starts at Dashboard page
   - Verify all specified workflows and features operate as intended
   - Maintain consistent naming and formatting standards

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html
- Apply all fixes as specified without introducing new features
- Maintain clean, readable, and well-organized code
- Submit only the corrected final files as output

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
            "review_criteria": "Ensure validation_report.md clearly identifies all functional, UI, and data handling defects with actionable recommendations.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "WebArchitect",
            "review_criteria": (
                "Verify the final app.py and templates/*.html fully resolve all issues reported in validation_report.md and strictly match design_spec.md and requirements."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a full-featured, requirements-compliant Flask RestaurantReservation web application with local file data storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce detailed web app design specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce comprehensive design spec for Flask web app."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and HTML templates based on the design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Create initial and final Flask app.py and templates with required UI and data handling."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the Flask application and templates ensuring full compliance and correctness.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate, report issues, and apply fixes to finalize application code and templates."}
            ]
        }
    ]
): pass
# Orchestrate_End