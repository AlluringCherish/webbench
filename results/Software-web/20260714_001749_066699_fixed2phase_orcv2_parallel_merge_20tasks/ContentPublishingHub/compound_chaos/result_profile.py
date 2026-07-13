# Phase1_Start
def design_specification_phase(
    goal: str = "Design the backend data model, Flask routes, and frontend HTML templates with element IDs and page navigation for the ContentPublishingHub application; produce backend_design.md, frontend_design.md, and design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDesignArchitect and FrontendDesignArchitect work independently to produce backend_design.md and frontend_design.md respectively based on the user task description; DesignMerger consolidates these into a single consistent design_spec.md document.",
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "prompt": """You are a Software Architect specializing in Python Flask backend web applications.

Your goal is to design the complete backend architecture for the ContentPublishingHub application, producing a detailed backend_design.md artifact.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md outlining all Flask routes, data models, and business logic
- Cover content management, version control, approval workflows, scheduling, and analytics as described
- Do not rely on or read frontend_design.md or sibling outputs

**Section 1: Flask Routes Design**
- Specify each route path, HTTP methods, and route handler responsibilities
- Define route names matching user task page requirements (e.g., /dashboard, /article/create)
- Include parameterized routes with argument names (e.g., article_id)

**Section 2: Data Models and File Schemas**
- Define the exact data format for each text data file (users.txt, articles.txt, article_versions.txt, approvals.txt, workflow_stages.txt, comments.txt, analytics.txt)
- Specify field names, data types, delimiters, order, and field descriptions
- Provide example records for each schema using data from user task
- Describe relationships linking models (e.g., article_id references, version tracking)

**Section 3: Business Logic and Functional Requirements**
- Detail logic for content version control, approval status handling, scheduling, and analytics calculations
- Describe any backend state changes triggered by routes or data updates
- Avoid assumptions beyond user task requirements

CRITICAL SUCCESS CRITERIA:
- Output backend_design.md can be directly implemented to produce the backend Flask app
- All relevant specifications must stem solely from the user task description
- Use write_text_file tool to save backend_design.md only

Output: backend_design.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "prompt": """You are a Software Architect specializing in frontend web design using HTML and Flask template technologies.

Your goal is to create detailed frontend_design.md specifying HTML templates for ContentPublishingHub pages with element IDs and navigation flows.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md describing all HTML templates, element IDs, and navigation controls
- Cover all pages: dashboard, article creation/editing, version history, lists, calendar, and analytics as specified 
- Do not read or assume backend_design.md or sibling outputs

**Section 1: Template and Page Specifications**
- For each page, specify template filename and exact page-level container element IDs
- List all important HTML element IDs with their purpose and element types (buttons, inputs, tables, etc.)
- Include all form controls, buttons, filters, and navigation elements with identifiers

**Section 2: Context Variables and Data Bindings**
- Define context variables expected from backend for each template
- Specify data structures and types for dynamic content rendering

**Section 3: Navigation and Inter-Page Links**
- Define navigation buttons and controls routing users between pages
- Specify consistency of element IDs used for navigation flows

CRITICAL SUCCESS CRITERIA:
- frontend_design.md supports implementation of templates/*.html with correct element IDs and navigation
- All specifications derive solely from the user task description
- Use write_text_file tool to write frontend_design.md only

Output: frontend_design.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        },
        {
            "agent_name": "DesignMerger",
            "prompt": """You are a Software Architect specializing in synthesizing backend and frontend architecture designs for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into a single consistent design_spec.md that fully meets user requirements without adding features.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Combine backend and frontend specifications into one coherent document design_spec.md
- Ensure consistency between route definitions, data models, and frontend context variables
- Resolve any naming conflicts and unify navigation elements and page structures
- Do not introduce new features or requirements beyond inputs

**Section 1: Consolidated Flask Routes and Backend Design**
- Preserve all routes, parameters, and business logic details from backend_design.md
- Reconcile with frontend navigation flows and template context requirements

**Section 2: Combined Frontend Templates Specification**
- Preserve all template names, element IDs, and context variables from frontend_design.md
- Ensure alignment with backend routes and data model definitions

**Section 3: Data Models and Integration**
- Unify data schema definitions with references from both backend and frontend
- List all artifacts’ links and maintain data integrity constraints

CRITICAL SUCCESS CRITERIA:
- design_spec.md supports both backend implementation (app.py) and frontend templates/*.html implementation
- No additional features outside user task description are added
- Use write_text_file tool to save only design_spec.md

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Check backend_design.md for completeness and clarity in covering routes, data models, and business logic.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Validate frontend_design.md to ensure all page templates, element IDs, and navigation are specified as per user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the backend Flask application and frontend templates from design_spec.md, and integrate them into a working ContentPublishingHub application; produce app.py and templates/*.html with fidelity to design",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDeveloper and FrontendDeveloper independently implement app.py and HTML templates respectively from design_spec.md; IntegrationMerger reconciles their outputs ensuring interface conformity and produces the final app.py and templates/*.html.",
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Backend Developer specializing in Python Flask web applications.

Your goal is to implement the backend Flask application including complete route handling, data management, version control, approvals, content scheduling, and analytics, as specified fully in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT, use it as the sole source of requirements
- Independently implement all Flask routes, data file interactions, and business logic
- Output a single app.py implementing the entire backend functionality
- Do not read or rely on any sibling agent outputs

**Implementation Requirements:**
- Implement all routes accurately with correct HTTP methods and route parameters
- Manage local text file storage for users, articles, versions, approvals, workflow stages, comments, and analytics data
- Include handlers for version tracking, editorial comments, content scheduling, and analytics computations
- Use the Flask framework with clear modular route functions and error handling

**Data Management:**
- Use specified text data formats and files under 'data' directory for persistence
- Implement parsing, reading, writing, and updating of text files conforming exactly to the design_spec.md data schema
- Ensure concurrency safety and data integrity in file operations

**Code Formatting and Structure:**
- Use Python 3 best practices and PEP8 style guidelines
- Include necessary imports, app initialization, and run configuration
- Add concise function-level comments using single-quote docstrings only

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output app.py
- Output app.py must be complete and runnable independently
- Follow design_spec.md exactly without adding or omitting routes or data handling
- Do not read or assume frontend implementation artifacts

Output: app.py""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "agent_name": "FrontendDeveloper",
            "prompt": """You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask applications.

Your goal is to implement all frontend HTML templates as specified in design_spec.md with precise page structure, element IDs, navigation, and content placeholders.

Task Details:
- Read design_spec.md from CONTEXT only
- Independently create all required templates with correct filenames in templates/*.html
- Use exact element IDs and structure described in the page designs
- Do not read or depend on backend implementation artifacts

**Template Implementation Instructions:**
- Implement each page’s HTML with Flask/Jinja2 templating syntax for dynamic content
- Provide all specified IDs for page containers, inputs, buttons, tables, and navigation controls
- Include proper links, forms, buttons, and sections as described for each page
- Ensure consistent and semantic markup following web standards

**Navigation and Page Structure:**
- Implement navigation elements as described to enable workflow between pages
- Include placeholders for dynamic variables matching backend context variables as implied by design_spec.md
- Use reusable components or layout inheritance only if reflected in design_spec.md

**Code Style:**
- Use indentation and HTML5 semantic tags appropriately
- Comment code with hash (#) style comments for sections as needed

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to output templates/*.html files
- Templates must exactly match the element IDs and structures given in design_spec.md
- Templates must be independently complete without backend assumptions

Output: templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationMerger",
            "prompt": """You are a Software Integration Engineer specializing in full-stack Flask web applications.

Your goal is to combine and reconcile the backend app.py and frontend templates/*.html implementations into a consistent fully integrated ContentPublishingHub application ready for deployment.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify route definitions, context variables, and UI element IDs match across backend and frontend
- Resolve any inconsistencies in routing paths, variable naming, and template rendering
- Produce a reconciled final version of app.py and the complete templates/*.html set

**Integration Validation:**
- Ensure Flask routes in app.py correspond to templates rendered and UI elements specified
- Verify that context data passed by backend matches template variables and element expectations
- Check all navigation and form submission paths are consistent in both codebases
- Remove duplication or mismatch errors, preserving design_spec.md requirements only

**Output Artifacts:**
- Write the consolidated, tested, and consistent backend code to app.py
- Write the merged and verified frontend templates to templates/*.html

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save final app.py and templates/*.html
- No additional requirements or modifications outside design_spec.md permitted
- Outputs must be deployable and fully synchronized backend-frontend codebases

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Verify app.py implementation conforms to design_spec.md including correct route handling and local file data management.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify templates/*.html align with design_spec.md including presence of all required element IDs and page navigation structure.",
            "review_artifacts": [
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Build a comprehensive ContentPublishingHub Flask web application with version control, analytics, and scheduling as per the provided specification",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design and merger.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce merged design_spec.md encapsulating backend and frontend architecture."
                }
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend with final integration.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce final integrated app.py and templates/*.html that implement the design specification."
                }
            ]
        }
    ]
): pass
# Orchestrate_End