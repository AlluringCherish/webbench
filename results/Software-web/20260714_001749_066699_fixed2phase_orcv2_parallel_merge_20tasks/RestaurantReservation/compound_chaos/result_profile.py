# Phase1_Start
def design_specification_phase(
    goal: str = "Create backend and frontend design specifications for the RestaurantReservation web application and merge them into a consistent design_spec.md document",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs Flask backend routes, data models, and file interactions based on the user task; "
        "FrontendDesignArchitect designs HTML templates with exact element IDs and navigations; "
        "DesignMerger reconciles backend and frontend designs into a unified design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "prompt": """You are a System Architect specializing in Flask backend development with expertise in designing RESTful routes, data models, and file-based data interactions for Python web applications.

Your goal is to create a comprehensive backend design specification for the RestaurantReservation app that includes all required Flask routes, data schemas, and exact text file data parsing/writing instructions.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently produce backend_design.md detailing Flask route definitions, data file schemas, and file interaction specifications
- Focus on backend functionality only; do not read or assume frontend_design.md
- Declare all data files and formats for data stored in the local 'data' directory

**Section 1: Flask Route Specifications**
- Specify each route's URL path, HTTP methods, and function name
- Define the expected input parameters, payloads (query, form, JSON), and response types
- Include navigation-related routes and their behaviors linked to pages described in user_task_description
- State expected template filenames for each route if applicable, but exclude frontend layout details

**Section 2: Data File Schemas and Handling**
- Specify the exact schema for each text data file in 'data' directory: filename, delimiter, fields order, and field descriptions
- Include examples of rows with realistic sample data following each schema
- Detail read/write/update/delete operations per data file including locking or concurrency considerations if any
- Ensure all data schemas and operations align strictly with user_task_description data formats and business rules

CRITICAL SUCCESS CRITERIA:
- Output backend_design.md using write_text_file tool
- The artifact must enable backend developers to implement all required Flask routes and data handling independent of frontend_design.md
- Adhere strictly to user_task_description data formats and required application features
- Do not generate or assume any frontend UI elements or templates

Output: backend_design.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "prompt": """You are a System Architect specializing in HTML and Jinja2 template design for Python web applications, focusing on detailed frontend page layouts, element IDs, navigation flows, and dynamic context variables.

Your goal is to create a clear and exact frontend design specification for the RestaurantReservation app that includes all HTML templates, page-specific element IDs, buttons, and navigation flows described by the user task.

Task Details:
- Read the full user_task_description from CONTEXT
- Independently produce frontend_design.md detailing all template file paths, page titles, element IDs with their types, and navigation/link flows between pages
- Provide detailed context variable names and structures needed to render each template based on backend data
- Focus on frontend presentation and navigation only; do not read or assume backend_design.md

**Section 1: Template and Page Specifications**
- List each HTML template file for the nine pages with precise filenames
- Specify the exact page title strings
- For each page, list all element IDs with their HTML tag/type and purpose as described
- Include button IDs with exact action descriptions for page navigation or form submission

**Section 2: Navigation and Context Variables**
- Define the navigation matrix linking all pages via buttons/links by their element IDs
- Specify context variables per template needed for dynamic page rendering as described (e.g., user info, menu items, reservations)
- Ensure all elements and variables strictly adhere to the user_task_description; no external UI details are added

CRITICAL SUCCESS CRITERIA:
- Output frontend_design.md using write_text_file tool
- The artifact must enable frontend developers to implement all HTML templates and navigation flows independent of backend_design.md
- Specify only declared UI elements and navigation given in user_task_description
- Use consistent naming of elements and context variables matching backend contracts is encouraged but not required here

Output: frontend_design.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        },
        {
            "agent_name": "DesignMerger",
            "prompt": """You are a System Architect specializing in integrating backend and frontend design specifications into a coherent, consistent design document for Flask-based Python web applications.

Your goal is to merge backend_design.md and frontend_design.md into a unified design_spec.md for the RestaurantReservation app without introducing any new requirements. Ensure internal consistency and alignment with the user task.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Reconcile backend routes with frontend templates to ensure matching route-to-template mappings
- Align navigation element IDs and button actions between backend route specifications and frontend page flow
- Ensure data schemas referenced in backend_design.md match the context variables used in frontend_design.md
- Produce design_spec.md that clearly separates backend routes, frontend templates, navigation flows, and data schemas

**Section 1: Flask Backend and Data Schemas**
- Include reconciled route listings with HTTP methods, URLs, and linked template filenames
- Confirm all data file schemas and examples are consistent and referenced in frontend sections

**Section 2: Frontend Templates and Navigation**
- Present all frontend template specifications with page titles, element IDs, and navigation mappings
- Validate that all navigation buttons correspond to backend routes and properly linked pages
- Ensure context variables used in templates align with backend data schemas and route outputs

CRITICAL SUCCESS CRITERIA:
- Output design_spec.md using write_text_file tool
- The merged design must enable seamless, error-free backend and frontend implementation
- No additional features beyond input artifacts; the specification must reflect exactly the user task requirements
- Resolve all discrepancies and produce one source of truth for developers

Output: design_spec.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "backend_design.md", "source": "BackendDesignArchitect"},
                {"type": "text_file", "name": "frontend_design.md", "source": "FrontendDesignArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend design completeness and alignment with user requirements",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness and alignment with user requirements",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the backend app.py and frontend templates for RestaurantReservation app based on design_spec.md and integrate them into final deployable artifacts",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py with routes, data handling, business logic from design_spec.md independently; "
        "FrontendDeveloper implements templates/*.html with all exact element IDs and navigation requirements independently; "
        "IntegrationMerger reconciles backend and frontend for interface consistency and produces the final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Backend Developer specializing in Flask web application backend development with Python.

Your goal is to implement the complete backend app.py for the RestaurantReservation application, including all routes, data handling using local text files, and business logic as specified in the design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT to understand all required routes, data schemas, and logic
- Implement data storage and retrieval using local text files with exact formats
- Output app.py implementing all backend functionality independently from frontend templates
- Do not read or assume frontend templates implementations

**Section 1: Flask Backend Implementation**
- Implement Flask routes per design_spec.md with correct HTTP methods and route paths
- Use input validation, error handling, and redirects as required
- Manage data files exactly as specified (users.txt, menu.txt, reservations.txt, waitlist.txt, reviews.txt)
- Use pipe ('|') delimiter and ensure consistent parsing and writing logic

**Section 2: Data Handling and Business Logic**
- Implement CRUD operations on local text files as required by reservations, reviews, waitlist, menus, and user profiles
- Ensure concurrency-safe file read/write logic if applicable
- Implement reservation booking, waitlist management, review submissions, and user profile updates as designed

**Section 3: Implementation Requirements**
- Use standard Flask app structure and idiomatic Python coding
- Include relevant comments using single-quote docstrings in the source code as documentation only
- Implement without incorporating any frontend code or templates

CRITICAL SUCCESS CRITERIA:
- The app.py fully implements backend logic from design_spec.md alone
- Data file interactions strictly follow specified formats and paths
- Use write_text_file tool to output app.py
- Produce only app.py as output artifact; no other files or refinements

Output: app.py""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "agent_name": "FrontendDeveloper",
            "prompt": """You are a Frontend Developer specializing in HTML and Jinja2 template design for Flask web applications.

Your goal is to implement all HTML templates (*.html) for the RestaurantReservation application, including all specified element IDs, page titles, layout, and navigation defined in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT to understand all required templates, page structures, element IDs, and navigation flows
- Implement complete and independent HTML/Jinja2 templates with the exact IDs and elements specified
- Do not read or assume any backend implementation details beyond those in design_spec.md

**Section 1: HTML Template Implementation**
- Create templates for all website pages with exact element IDs as specified
- Conform to naming, structure, and navigation flow requirements from design_spec.md
- Use Jinja2 syntax for dynamic content and context variables as directed

**Section 2: Layout and Navigation**
- Implement navigation buttons and links with correct target routes and IDs
- Ensure user experience matches the described page flows and button behaviors
- Do not implement backend logic; focus on interface, IDs, and template correctness

**Section 3: Implementation Requirements**
- Follow standard Flask/Jinja2 project conventions for template file placement
- Use single-quote docstrings or hash comments if including notes or comments in templates
- Output a complete set of templates/*.html files ready for integration

CRITICAL SUCCESS CRITERIA:
- All templates include the exact element IDs and navigation defined only in design_spec.md
- Use write_text_file tool to output templates/*.html files
- Produce only templates/*.html as output artifacts

Output: templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationMerger",
            "prompt": """You are a Software Integration Engineer specializing in reconciling backend and frontend Flask web application components.

Your goal is to merge and reconcile the implemented backend app.py and frontend templates/*.html for the RestaurantReservation application into final deployable artifacts, correcting only interface inconsistencies.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate consistency between backend routes and frontend navigation elements
- Reconcile any mismatches in route names, context variable names, and template references
- Correct interface inconsistencies while preserving worker implementations' original logic

**Section 1: Backend-Frontend Interface Consistency**
- Ensure that Flask route function names and paths match frontend navigation button targets
- Align context variable names expected by templates with those provided by backend
- Confirm data file usage is consistent across app.py and templates where relevant

**Section 2: Artifact Integration and Refinement**
- Merge adjustments without adding new functionality or requirements
- Maintain clear separation of backend logic and frontend templates
- Document reconciliation decisions using single-quote docstrings or hash comments if applicable

**Section 3: Final Output Requirements**
- Produce final app.py and templates/*.html files ready for deployment
- Use write_text_file tool exclusively for saving final artifacts
- Do not produce additional files or refinement markers beyond declared outputs

CRITICAL SUCCESS CRITERIA:
- Final artifacts are consistent, deployable, and strictly based on input worker outputs and design_spec.md
- Interface inconsistencies corrected only as necessary for integration
- Output only the final app.py and templates/*.html as declared

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"},
                {"type": "text_file", "name": "app.py", "source": "BackendDeveloper"},
                {"type": "text_file", "name": "templates/*.html", "source": "FrontendDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check backend implementation matches design_spec.md and handles all specified data files and routes",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check frontend templates conform to design_spec.md element IDs and navigation requirements",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the complete RestaurantReservation Python Flask web application with specified pages, data storage, and navigation.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design, merging complementary architectural specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce unified backend and frontend design specification document."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel backend and frontend implementation based on design_spec.md and integration into final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Final implementation and integration of backend and frontend components."}
            ]
        }
    ]
): pass
# Orchestrate_End