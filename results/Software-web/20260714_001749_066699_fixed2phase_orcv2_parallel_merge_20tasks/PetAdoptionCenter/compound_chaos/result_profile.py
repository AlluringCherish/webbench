# Phase1_Start
def design_specification_phase(
    goal: str = "Design comprehensive backend routes and frontend HTML templates reflecting all pages and specified element IDs; produce merged design specification document.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect defines the Flask routes, data handling flows, and input/output data schemas for all specified pages and data files;"
        "FrontendDesignArchitect specifies HTML templates, with correct element IDs, page layouts, and navigation for all application pages;"
        "DesignMerger reviews and merges backend_design.md and frontend_design.md into a single, consistent design_spec.md ensuring coherence and compliance to the user requirements."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "prompt": """You are a System Architect specializing in backend Flask web application design and local text file data management.

Your goal is to design the backend architecture addressing all user requirements by defining Flask routes, data handling, and input/output data schemas for all specified application pages and local text files independently.

Task Details:
- Read user_task_description from CONTEXT
- Produce backend_design.md without referencing frontend_design.md
- Define all Flask routes with required parameters and HTTP methods
- Specify detailed data read/write schemas matching local text files for users, pets, applications, favorites, messages, adoption history, and shelters
- Outline backend logic flows for all ten application pages including data interactions and route handlers

**Section 1: Flask Routes Specification**
- Enumerate route paths, allowed HTTP methods, and route parameters
- Define route purposes linked to each application page and data operation
- Include routes for listing, detail, creation, updating, and navigation actions

**Section 2: Data Interaction and Schema Definition**
- Specify file-based data formats, field order, delimiters, and example entries referencing all required data files in the 'data' directory
- Detail data reading and writing operations per route
- Confirm local text-file management including concurrency assumptions and error handling

**Section 3: Backend Logic and Workflow**
- Describe backend logic per route: input processing, validation, data updates, state changes, and response generation
- Define session or user state considerations if applicable

CRITICAL SUCCESS CRITERIA:
- backend_design.md must fully enable implementation of backend app.py
- Routes and data schemas must cover all user task requirements independently
- Use write_text_file tool exclusively for outputting backend_design.md
- Do not rely on or read sibling frontend_design.md artifact

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
            "prompt": """You are a System Architect specializing in frontend HTML template design with detailed element ID and navigation planning.

Your goal is to create comprehensive HTML templates layout, specifying exact element IDs, page structure, navigation flows, and data-binding placeholders for all pages independently.

Task Details:
- Read user_task_description from CONTEXT
- Produce frontend_design.md independently without reading backend_design.md
- Define precise HTML template names and page titles for all ten specified pages
- Specify all required element IDs matching the user task elements described for each page
- Include navigation flows between pages via buttons and links identified by element IDs
- Outline placeholders for dynamic data binding and UI behavior from backend context

**Section 1: HTML Template Structure and IDs**
- For each page, list template filename, page title, and container elements with their exact IDs and element types
- Include buttons, inputs, dropdowns, textareas, tables, and grids with specified IDs

**Section 2: Navigation and Interaction Flow**
- Map all navigation triggers (buttons, links) to target pages using element IDs
- Detail form submission buttons and UI controls referencing backend interaction points

**Section 3: Data Binding Placeholders**
- Specify dynamic context variables or placeholders to be rendered per template element
- Ensure consistency with backend data models without assuming backend_design.md

CRITICAL SUCCESS CRITERIA:
- frontend_design.md fully supports implementation of all templates in templates/*.html
- All required IDs, page titles, and navigation described in user task must be included
- Use write_text_file tool exclusively for outputting frontend_design.md
- Do not reference or depend on backend_design.md

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
            "prompt": """You are a System Architect specializing in merging backend and frontend web application designs into a coherent specification document.

Your goal is to consolidate backend_design.md and frontend_design.md into one consistent and complete design_spec.md, ensuring coverage of all functionalities, UI elements, and data flows as per user requirements without adding or omitting any features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Analyze and reconcile route definitions with UI templates and navigation flows
- Check consistency of route parameters with frontend data-binding placeholders and element usage
- Merge backend route, data schema, and logic descriptions with frontend template and navigation specifications
- Resolve conflicting or divergent details with strict adherence to user task inputs only
- Assemble a final design_spec.md document organized with Sections for Backend Routes, Data Schemas, Frontend Templates, and Navigation

**Section 1: Comprehensive Backend Routes and Data Schemas**
- Present reconciled, coherent route list from backend_design.md
- Include full data file schemas and examples integrated with backend logic

**Section 2: Detailed Frontend Template Specifications**
- Present finalized template filenames, page titles, element IDs, and UI components from frontend_design.md

**Section 3: Cross-Artifact Consistency Checks and Navigation Mappings**
- Ensure navigation flows and UI interactions are consistent with backend routes
- Confirm matching field names and parameters between backend and frontend

CRITICAL SUCCESS CRITERIA:
- design_spec.md supports seamless backend and frontend implementation
- No new requirements beyond input artifacts are introduced
- Use write_text_file tool exclusively for outputting design_spec.md

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
            "review_criteria": "Verify backend design covers all routes, data storage schema, and specifications as per user requirements.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design matches element IDs, page layouts, and navigation requirements.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend Flask app.py and frontend HTML templates in parallel from design_spec.md, then merge and integrate them into a consistent working web application.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements the Flask app.py file with routes, logic, and data file management strictly following design_spec.md;"
        "FrontendDeveloper creates all required HTML templates with correct element IDs and structures as specified in design_spec.md;"
        "IntegrationMerger reconciles the backend and frontend components, resolves interface mismatches, and produces integrated app.py and templates/*.html ensuring functional consistency."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Backend Developer specializing in Flask web applications using Python.

Your goal is to implement the complete backend Flask application (app.py) including all routes, data file interactions, form handling, and business logic strictly according to the design specifications.

Task Details:
- Read design_spec.md artifact from CONTEXT for route, data structure, and application logic specifications.
- Produce app.py implementing all Flask routes, handlers, and local text file data management as specified.
- Focus only on backend functionality: routing, data reading/writing, application logic, and form processing.
- Do NOT read or depend on frontend artifacts from siblings.

**Implementation Requirements:**
- Implement all routes as specified with proper HTTP methods (GET/POST).
- Handle local data files under the 'data' directory for users, pets, applications, favorites, messages, etc.
- Implement all form inputs, validation, submission logic, and status updates.
- Use Flask features for route decorators, request parsing, session or context as needed.
- Maintain modular code organization within app.py using functions or classes.
- Follow the data formats and examples provided in design_spec.md strictly.
- Include code comments using single-quote docstrings for clarity.
- Ensure exception handling around file access and user inputs.

CRITICAL SUCCESS CRITERIA:
- app.py must be fully functional and runnable as a Flask application.
- The implementation strictly follows design_spec.md routes and data schemas.
- Use write_text_file tool to output app.py only.
- Do not produce any files other than app.py.

Output: app.py""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [{"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}],
            "output_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "agent_name": "FrontendDeveloper",
            "prompt": """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to create all HTML templates with correct element IDs, page layouts, and navigation patterns as defined in design_spec.md.

Task Details:
- Read design_spec.md artifact from CONTEXT for templates structure, page titles, element IDs, and navigation flows.
- Produce all required HTML template files under templates/ directory (*.html) implementing layouts for all pages.
- Focus only on frontend artifacts: HTML structure, element IDs, navigation buttons, and integration placeholders.
- Do NOT read or depend on backend code artifacts from siblings.

**Template Specification Requirements:**
- Create one HTML file per page: Dashboard, Pet Listings, Pet Details, Add Pet, Adoption Application, My Applications, Favorites, Messages, User Profile, Admin Panel.
- Use element IDs exactly as specified, including buttons, inputs, divs, and other UI elements.
- Structure pages for a consistent user experience with correct titles and navigation elements.
- Use Jinja2 templating syntax for dynamic content placeholders but no actual data logic.
- Include comments using single-quote docstrings formatting where appropriate.
- Ensure navigation buttons link to correct routes based on design_spec.md.

CRITICAL SUCCESS CRITERIA:
- templates/*.html are complete and fully compliant with design_spec.md.
- Files are independent of backend implementation details.
- Use write_text_file tool to output templates/*.html only.
- Do not produce any files other than templates/*.html.

Output: templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [{"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}],
            "output_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        },
        {
            "agent_name": "IntegrationMerger",
            "prompt": """You are a Software Integration Specialist with expertise in combining Flask backend and HTML frontend components into a coherent web application.

Your goal is to merge and integrate the app.py backend implementation and all HTML templates to ensure consistent interfaces, resolve mismatches, and produce a fully functional PetAdoptionCenter web application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html artifacts from CONTEXT.
- Perform reconciliation to resolve remaining interface mismatches between backend routes and frontend navigation.
- Correct minor inconsistencies in route URLs, form action endpoints, element IDs, or variable references.
- Ensure outputs conform strictly to design_spec.md specifications.
- Produce final version of app.py and templates/*.html for deployment.

**Integration and Consistency Checks:**
- Verify all app.py routes are referenced correctly by HTML form actions and navigation links.
- Confirm all element IDs in templates are consistent with backend route handlers and context variables.
- Validate that all forms submit to correct backend endpoints.
- Ensure navigation flows allow returning to Dashboard or other pages as described.
- Keep code style consistent and add comments using single-quote docstrings.

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html are fully consistent and deployable together.
- No feature is added or removed beyond design_spec.md scope.
- Use write_text_file tool to save final app.py and all templates/*.html.
- Write ONLY the specified output artifacts.

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
            "review_criteria": "Check app.py conforms precisely to design_spec.md routes, data access, and requirements.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check HTML templates conform completely to design_spec.md element IDs, structure, and navigation.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'PetAdoptionCenter' Python Flask web application with all specified pages, elements, and local text file data management as detailed in user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel comprehensive design of backend architecture and frontend templates followed by merged design specification creation.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Merged backend and frontend design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend followed by integration merging into final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Merged implementation of backend Flask app and frontend HTML templates."}
            ]
        }
    ]
): pass
# Orchestrate_End