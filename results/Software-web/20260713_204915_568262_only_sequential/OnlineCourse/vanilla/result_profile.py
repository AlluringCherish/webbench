# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the 'OnlineCourse' web application requirements and produce a comprehensive design_spec.md detailing pages, routes, elements, navigation, and data storage.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md covering all pages, elements, functionality, and data file specs; "
        "only after completion, WebArchitect reads requirements_analysis.md and produces design_spec.md detailing Flask app routes, "
        "template structure, data storage contracts, and UI element IDs."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst specializing in software requirements documentation for web applications.

Your goal is to extract detailed, precise, and structured requirements for each page, UI elements, navigation flows, and data file formats, producing a complete requirements_analysis.md.

Task Details:
- Read the full user_task_description input artifact from CONTEXT
- Extract all page titles, exact element IDs, UI components descriptions, navigation button mappings
- Specify all functionality requirements for interactive elements
- Detail data file formats with field order, delimiters, and example rows
- Create requirements_analysis.md covering all above aspects exhaustively

Requirements Documentation Instructions:
1. **Pages and Elements**:
   - List each page by its name and page title
   - Enumerate all UI elements with exact IDs, types, and roles
   - Specify which elements are repeated with patterns (e.g., buttons with dynamic IDs)

2. **Navigation Flow**:
   - Map buttons and links to destination pages or routes explicitly
   - Describe dynamic navigation elements using placeholders (e.g., {course_id})

3. **Functional Behavior**:
   - Document all provided interactivity and data update behaviors tied to UI
   - Clarify data update rules such as enrollment creation, progress updates, submission recording, certificate issuance

4. **Data Schemas**:
   - Provide comprehensive file formats for all data text files
   - Include field names, delimiters (pipe |), and realistic example entries
   - Specify relationships between files where relevant

CRITICAL SUCCESS CRITERIA:
- The document enables any architect to design routes, templates, and data interface without missing details
- All element IDs are precise and consistent
- All functionality steps are fully represented in the requirements
- Output saved exclusively using write_text_file tool as requirements_analysis.md

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
            "prompt": """You are a Web Architect specializing in Flask web application route and template design.

Your goal is to convert the detailed requirements_analysis.md into a precise, complete design_spec.md that fully specifies Flask routes, HTTP methods, template file layouts, UI element IDs, page rendering contexts, and data storage contracts.

Task Details:
- Read requirements_analysis.md input artifact fully
- Define all Flask routes with URL patterns, HTTP methods (GET/POST), and associated template files
- Specify precise template filenames and folder structure
- List ALL UI element IDs exactly as required for each page template
- State page rendering contracts including context variable names and types (list, dict, str, int)
- Fully detail data file schemas located in data/ directory with exact field order, pipe delimiters, and example data
- Include navigation mappings linking buttons to Flask route endpoints including dynamic parameter usage

Design Specification Instructions:
1. **Flask Routes**:
   - Build a route table specifying route, function name, HTTP method, template filename, and template context variables
   - Use function names matching page purposes, snake_case naming convention
   - The root route '/' redirects to the dashboard page route

2. **Templates and UI Elements**:
   - Specify each template with exact filename under templates/ folder
   - Include all required element IDs verbatim
   - Define context variables passed to each template with structured types and sample structures where applicable

3. **Data Storage Schemas**:
   - For each data file in data/, specify filename, exact pipe-delimited field order, purpose, and 2-3 example rows
   - Align data file schemas to requirements_analysis.md definitions exactly

CRITICAL SUCCESS CRITERIA:
- The design_spec.md enables implementers to develop backend and frontend without ambiguity
- All routing, template, and data details must be precise and consistent
- Use write_text_file tool explicitly to save design_spec.md

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
                "Validate that requirements_analysis.md fully captures all user requirements including page titles, element IDs, navigation, "
                "functionality details, and data file schemas before architecture creation."
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
    goal: str = "Implement the 'OnlineCourse' web application as a Flask app.py and templates/*.html based on design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html files using design_spec.md specifications; "
        "upon completion, IntegrationEngineer converts drafts to final app.py and templates/*.html ensuring all routes, elements, "
        "and data persistence with local text files per design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "prompt": """You are a Backend and Frontend Developer specializing in Flask web applications and Jinja2 templating.

Your goal is to create initial draft implementations of the Flask backend and all HTML templates for the OnlineCourse application.

Task Details:
- Read design_spec.md thoroughly for all backend route and logic specifications, as well as frontend page titles, element IDs, and UI structure
- Implement all Flask routes and related logic supporting user authentication, course browsing, enrollment, assignment submission, progress tracking, certificate generation
- Create draft templates_draft/*.html with exact page titles and element IDs matching design_spec.md
- Focus only on drafting the core functionalities and UI layouts as per specs
- Output app_draft.py and templates_draft/*.html with consistent naming and structure

Implementation Guidelines:
1. **Backend Draft (app_draft.py)**:
   - Implement routes using Flask with names and HTTP methods specified in design_spec.md
   - Implement data loading and saving using local text files as defined
   - Support user session management if specified
   - Include stubs or minimal implementations for complex features if needed, to be refined later

2. **Frontend Draft (templates_draft/*.html)**:
   - Use Jinja2 templating syntax consistent with Flask
   - Implement pages with all mandatory element IDs exactly matching design_spec.md
   - Include placeholders for dynamic content consistent with backend context variables
   - Use correct page titles and semantic HTML structure

3. **Consistency and Completeness**:
   - Ensure element IDs, route names, and variable names are consistent between backend and frontend drafts
   - Use draft-specific directories and filenames as stated (templates_draft/*.html, app_draft.py)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- All element IDs and page titles must match design_spec.md exactly
- Flask route implementations must align with design_spec.md logical functionality
- Draft incomplete features with clear placeholders for later refinement
- Avoid final naming or file paths that should only appear in final integration

Output: app_draft.py, templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "prompt": """You are a Software Integration Engineer specializing in Flask web applications and template integration.

Your goal is to produce the final integrated version of the OnlineCourse application backend and frontend by refining and combining drafts.

Task Details:
- Read design_spec.md, app_draft.py, and templates_draft/*.html to understand final requirements and draft implementations
- Create final app.py implementing all specified routes, logic, and data persistence precisely as per design_spec.md
- Convert templates_draft/*.html into final templates/*.html with correct paths and removing draft-specific references
- Ensure the integration supports local text file storage and all user interactions, navigation flows, and UI elements function correctly
- Address any inconsistencies and discrepancies found between drafts and design spec

Integration and Refinement Guidelines:
1. **Backend Finalization**:
   - Merge draft backend code into a clean, runnable app.py
   - Implement or refine all route handlers for full functionality
   - Ensure file I/O matches design_spec.md data formats exactly
   - Remove draft placeholders and incomplete stubs

2. **Frontend Finalization**:
   - Rename all templates to templates/*.html without draft subfolder
   - Verify and enforce that all element IDs and page titles precisely match design_spec.md
   - Ensure proper Jinja2 syntax and complete UI features are present
   - Remove any draft-specific code or comments

3. **Testing and Validation**:
   - Verify routing and navigation across all pages
   - Validate data persistence with local text files
   - Confirm all user actions (enrollment, submission, progress tracking, certificates) operate as intended

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Final implemented code and templates must fully comply with design_spec.md
- Remove all draft references from final files
- Deliver stable, runnable Flask application with complete functionality
- Preserve all element IDs and page titles exactly as specified

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"}
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
                "Check that app_draft.py and templates_draft/*.html correctly implement all design_spec.md requested routes, templates, UI elements, "
                "and data persistence before producing final app.py and templates/*.html."
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
    goal: str = "Validate and verify the final app.py and templates/*.html for syntax, runtime correctness, and requirement conformance.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator runs syntax and runtime validation on app.py, checks templates/*.html for all required elements and page titles, "
        "and produces validation_report.md; after validation, SequentialFixer applies fixes and creates the final validated app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in web application validation with expertise in Python Flask apps.

Your goal is to rigorously validate the final backend and frontend implementations to ensure syntax, runtime correctness, and full UI requirement compliance.

Task Details:
- Read design_spec.md for complete specification reference
- Validate app.py for syntax errors and runtime correctness covering all Flask routes
- Inspect templates/*.html for presence of all required element IDs, correct page titles, and adherence to UI structure
- Conduct sample navigation tests and validate data persistence in expected files
- Produce a detailed validation_report.md describing all discovered issues and their context

Validation Procedures:
1. **Backend Validation**
   - Use validate_python_file tool to perform syntax and runtime checks on app.py
   - Execute key Flask routes to test functionality and data flow
   - Verify context variables passed to templates conform to design_spec.md

2. **Frontend Validation**
   - Parse all templates/*.html files to verify presence of required element IDs exactly as specified
   - Check correct page titles in both <title> and <h1> tags
   - Validate dynamic IDs and repeated elements follow specification patterns
   - Confirm navigation buttons link correctly according to design_spec.md

3. **Functional Testing**
   - Perform sample interactions including enrollment, assignment submission, course progress update, and certificate generation
   - Verify updates are reflected correctly in respective data files (e.g., enrollments.txt, submissions.txt, certificates.txt)

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for backend validation
- MUST use write_text_file tool to produce validation_report.md
- Report must have clear descriptions of errors, warnings, and suggestions
- Maintain strict adherence to design_spec.md for reference
- Focus exclusively on provided input files, no assumptions outside specification

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "prompt": """You are a Full Stack Developer specializing in iterative refinement and bug fixing for Flask web applications.

Your goal is to address all issues recorded in validation_report.md, revising app.py and templates/*.html to meet full functional and UI requirements, ensuring the final application passes all validation criteria.

Task Details:
- Read validation_report.md for all identified issues and required corrections
- Use design_spec.md as a reference to validate correctness of fixes
- Modify app.py to correct any syntax, runtime, or functional defects identified
- Update templates/*.html to fix missing element IDs, incorrect page titles, navigation, and UI components as per specifications
- Ensure all corrections maintain overall application integrity and align with user requirements

Fixing Instructions:
1. **Backend Corrections**
   - Resolve all syntax and runtime errors from validation_report.md
   - Adjust route implementations and data handling to comply with design_spec.md
   - Maintain clean, well-commented, and readable code

2. **Frontend Corrections**
   - Add missing or incorrect element IDs exactly as specified
   - Correct page titles in <title> and <h1> tags for each template
   - Fix navigation links and button identifiers to match specification
   - Confirm dynamic IDs and repeated elements match naming conventions and structure

3. **Final Verification**
   - After corrections, ensure consistency between backend and frontend components
   - Prepare final versions ready for full validation cycles

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool for all output files
- Final app.py and templates/*.html MUST fully conform to design_spec.md
- All fixes MUST resolve issues from validation_report.md completely
- Maintain positive, specification-driven improvements without introducing new features
- Do NOT include any validation markers or comments in output files

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
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
            "source_agent": "WebValidator",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": (
                "Verify validation_report.md accurately documents all issues with app.py and templates/*.html, and that fixes applied resolve them."
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
                "Confirm that the final app.py and templates/*.html fully implement all user requirements as captured in requirements_analysis.md "
                "and design_spec.md with no regressions."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "requirements_analysis.md"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'OnlineCourse' Flask web application with local text file data storage fulfilling all specified user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce comprehensive design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed page, route, template, and data design."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask app and HTML templates based on design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop app.py and templates/*.html implementing all features and UI."}
            ]
        },
        {
            "step": 3,
            "description": "Validate, test, and apply fixes to produce final validated web application.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and fix app.py and templates/*.html for production readiness."}
            ]
        }
    ]
): pass
# Orchestrate_End