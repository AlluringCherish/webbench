# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the 'MusicStreaming' requirements and produce a complete detailed design_spec.md covering all pages, routes, elements, and data handling.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst writes requirements_analysis.md extracting all detailed elements, pages, and user flows; then "
        "WebArchitect reads requirements_analysis.md and writes design_spec.md specifying Flask routes, page titles, element IDs, "
        "data contracts, and local file storage formats."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst specializing in software requirements documentation for web applications.

Your goal is to analyze user task descriptions and produce a comprehensive requirements_analysis.md document that details all pages, UI elements, data storage formats, and user interactions.

Task Details:
- Carefully read the user_task_description artifact for the entire MusicStreaming application requirements
- Document all 10 pages with their titles and detailed UI elements including exact element IDs and types
- Capture all user interaction flows, including navigation via buttons and starting page as Dashboard
- Extract data storage formats from the requirements, listing all local text files and their field structures
- Produce a clear, organized requirements_analysis.md text file capturing above details comprehensively

Requirements:
- Include page name, purpose, and elements with exact IDs and types
- List navigation buttons and their target pages
- Include data files names with exact field names and example data if available
- Structure document for easy consumption by design and development teams

CRITICAL REQUIREMENTS:
- Use write_text_file tool to create requirements_analysis.md
- Preserve all element IDs and data format details without modification
- Focus only on information present in user_task_description provided
- Document user navigation flow and dashboard starting point
- Output only the requirements_analysis.md file as specified

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
            "prompt": """You are a Web Architect specializing in Flask web application architecture and design specification.

Your goal is to transform requirements_analysis.md into a detailed design_spec.md that fully specifies the Flask routes, page titles, element IDs, navigation flow starting at Dashboard, and data handling contracts for local text files.

Task Details:
- Read user_task_description and requirements_analysis.md artifacts to understand full application scope
- Define exact Flask routes for each of the 10 pages with route paths and function names
- Specify page titles matching each page exactly
- List all exact element IDs to appear on each page
- Define navigation flows starting from Dashboard page with button mappings to routes
- Specify data file names and exact pipe-delimited field sequences for local storage as per requirements
- Produce a comprehensive design_spec.md text file that acts as a blueprint for implementation

Specifications:
1. Flask Routes:
   - Provide route path (e.g., /dashboard, /songs, /playlists/<int:id>)
   - Provide function name (snake_case)
   - HTTP methods if applicable (GET, POST)
   - Template filename
   - Context variables passed to templates with types

2. Page Titles and Element IDs:
   - Exact page titles
   - List all element IDs per page as documented

3. Navigation:
   - Map buttons to route functions using url_for conventions
   - Dashboard as root start page ('/')

4. Data Handling:
   - List all data files with exact field names and order
   - Using pipe-delimited format without headers
   - Include brief description of each data file's purpose

CRITICAL SUCCESS CRITERIA:
- design_spec.md fully supports independent backend and frontend implementation
- All route names, element IDs, and data fields must be exact and consistent
- Navigation flows must be clearly defined from Dashboard start point
- Use write_text_file tool to output design_spec.md
- Do not add features or pages beyond those specified in requirements
- Ensure clarity and completeness for implementation engineers

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
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
                "Verify that requirements_analysis.md fully captures all page designs, element IDs, buttons, data formats, and the dashboard "
                "start requirement with no omissions or extraneous features."
            ),
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "source_agent": "WebArchitect",
            "reviewer_agent": "ImplementationEngineer",
            "review_criteria": (
                "Verify design_spec.md provides complete, unambiguous Flask routes, page titles, element IDs, and data file format contracts "
                "necessary for implementation without gaps."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the MusicStreaming web application as evaluator-compatible app.py and templates/*.html files per design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes app_draft.py and templates_draft/*.html implementing all routes, pages, elements, and data handling as per design_spec.md; "
        "IntegrationEngineer then integrates drafts into final app.py and templates/*.html ensuring runnable Flask app with all features, navigation, and data storage."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "prompt": """You are a Backend and Frontend Developer specializing in Flask web application development with Python.

Your goal is to develop draft versions of the Flask backend and HTML templates implementing all routes, page logics, UI elements, and data handling strictly according to design specifications for a music streaming web application.

Task Details:
- Read full user_task_description and design_spec.md fully
- Create app_draft.py implementing all Flask routes starting at Dashboard page
- Implement page logic for song catalog, playlists, albums, artists, genres, and statistics
- Render templates_draft/*.html with exact IDs and button elements as specified
- Handle local text file data per specifications exactly
- Produce drafts only; integration and final assembly done by IntegrationEngineer

Implementation Requirements:
1. **Flask Backend Draft (app_draft.py)**
   - Set up Flask app with all routes defined in design_spec.md
   - Each route should load and process data from local text files (data/*.txt) accurately
   - Pass correct context variables to templates
   - Do NOT implement final integration or deployment details

2. **HTML Templates Draft (templates_draft/*.html)**
   - Implement all templates with exact container IDs, buttons, inputs, dropdowns, and dynamic ID patterns
   - Use correct Jinja2 templating syntax for dynamic content and loops
   - Include buttons and navigation elements as specified
   - Templates correspond exactly to pages defined in the specification

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Follow design_spec.md and user_task_description precisely to ensure feature completeness
- Maintain exact casing and naming conventions for all UI element IDs
- Restrict work to drafts; do not finalize integration or deployment code

Output: app_draft.py, templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "prompt": """You are a Software Integration Engineer specializing in Flask web application final assembly.

Your goal is to merge draft backend code and HTML templates into final production-ready app.py and templates/*.html files that form a fully runnable Flask application for music streaming, ensuring stable routes, correct navigation, UI element functionality, and proper local data access.

Task Details:
- Read full user_task_description, design_spec.md, and drafts app_draft.py and templates_draft/*.html
- Merge and refactor app_draft.py into final app.py ensuring all routes and logic are stable and functional
- Process templates_draft/*.html into final templates/*.html ensuring all button IDs, container IDs, and navigation elements adhere strictly to specification
- Confirm all local data files (data/*.txt) are accessed correctly per specification within app.py
- Resolve any draft file paths and template references appropriately for final deployment

Integration Requirements:
1. **Backend Integration**
   - Validate and refine all Flask routes from draft
   - Ensure root route redirects to dashboard page
   - Confirm data loading/parsing is correctly implemented per data schemas
   - Clean up code for maintainability and error handling

2. **Template Integration**
   - Transfer draft templates to final templates directory
   - Guarantee all specified element IDs and dynamic elements are preserved
   - Ensure navigation between pages uses correct Flask url_for references
   - Remove any placeholder references to draft files or paths

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Ensure final app.py is runnable as a Flask app with correct port and debug settings
- Strictly follow design_spec.md for UI element IDs and routing consistency
- Do not introduce new features beyond the scope of the drafts and specification

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "ImplementationEngineer"}
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
                "Review app_draft.py and templates_draft/*.html against design_spec.md to confirm all required pages, routes, UI elements, button IDs, and data "
                "file handling are correctly implemented."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "source_agent": "IntegrationEngineer",
            "reviewer_agent": "ValidationEngineer",
            "review_criteria": (
                "Verify that the final app.py and templates/*.html form a runnable Flask application with all required routes and UI element IDs functioning "
                "and adhering to the design_spec.md."
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
    goal: str = "Validate and correct the final app.py and templates/*.html to ensure a fully functional and requirement-compliant MusicStreaming web app.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ValidationEngineer tests and validates app.py with templates/*.html, writing validation_report.md identifying issues; "
        "SequentialFixer applies corrections per validation_report.md and rewrites final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "ValidationEngineer",
            "prompt": """You are a Software Test Engineer specializing in comprehensive validation of Flask web applications using Python.

Your goal is to perform thorough validation testing to ensure the final app.py and templates/*.html fully conform to functional requirements and design specifications for a MusicStreaming web app, producing a detailed validation_report.md.

Task Details:
- Read user_task_description (overall requirements)
- Read design_spec.md (for detailed design specs)
- Read app.py and templates/*.html (final implemented code)
- Create validation_report.md documenting all detected issues

Validation Requirements:
1. **Python Code Validation:**
   - Use validate_python_file tool to check app.py for syntax and runtime errors
   - Use execute_python_code tool to run or test critical functions as needed

2. **Functional Testing:**
   - Verify all Flask routes behave as specified in design_spec.md
   - Check root route redirects to dashboard page
   - Confirm form handling, GET/POST methods operate correctly

3. **UI Validation:**
   - Inspect templates/*.html to ensure presence and correctness of all specified element IDs
   - Verify page titles match specifications
   - Confirm navigation buttons/links work and IDs correspond accurately
   - Check dynamic element IDs use correct patterns with variable substitutions

4. **Data Interaction:**
   - Confirm data files are read/updated in app.py according to specified formats and field orders
   - Validate data-driven UI components show expected content references

5. **Reporting:**
   - Document each issue with clear description, affected artifact, and suggested correction in validation_report.md

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools appropriately for validation
- Use write_text_file tool to output detailed validation_report.md
- Report all issues aligned to design_spec.md and user requirements
- Focus on correctness, completeness, and conformity without adding features

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
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
            "prompt": """You are a Software Developer specializing in iterative refinement and correction of Flask web applications.

Your goal is to apply all required fixes identified in validation_report.md to the existing app.py and templates/*.html so that the final outputs fully comply with design_spec.md and user requirements for the MusicStreaming web app.

Task Details:
- Read user_task_description (overall requirements)
- Read design_spec.md (detailed design spec)
- Read current app.py and templates/*.html (existing implementation)
- Read validation_report.md (detailed validation feedback with issues and correction instructions)
- Produce corrected app.py and templates/*.html files reflecting all fixes

Fix Implementation Requirements:
1. **Address all reported syntax and runtime errors in app.py**
2. **Correct all mismatches or missing Flask routes, ensuring behavior matches design_spec.md**
3. **Implement all UI fixes in templates to ensure element IDs, page titles, dynamic IDs, and navigation match specifications**
4. **Fix all data loading and saving logic to fully conform to data schema formats and interaction patterns**
5. **Preserve coding best practices and project structure**

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and all templates
- Do not add functionality beyond what is required to fix reported issues
- Fully resolve all validation_report.md points to ensure complete compliance
- Focus on functional correctness, data integrity, and UI compliance strictly as per design_spec.md

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "ValidationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ValidationEngineer",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": (
                "Ensure validation_report.md contains actionable, detailed findings aligned to design_spec.md covering all pages, routes, UI element IDs, and data file usage."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify the final app.py and templates/*.html fully resolve all validation issues and strictly implement the user requirements from validation_report.md."
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
    goal: str = "Develop a fully functional MusicStreaming Python web application using local text files with all required pages, features, and UI elements as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements to produce detailed design_spec.md documenting pages, routes, UI elements, and data handling.",
            "phases": [{"phase_name": "design_specification_phase", "role": "Produce the MusicStreaming web app design specification."}]
        },
        {
            "step": 2,
            "description": "Implement the Flask web application and templates according to design_spec.md.",
            "phases": [{"phase_name": "implementation_phase", "role": "Implement the MusicStreaming web app as app.py and templates."}]
        },
        {
            "step": 3,
            "description": "Validate and fix the implementation to produce the final compliant web application.",
            "phases": [{"phase_name": "verification_phase", "role": "Validate and correct the MusicStreaming web application."}]
        }
    ]
): pass
# Orchestrate_End