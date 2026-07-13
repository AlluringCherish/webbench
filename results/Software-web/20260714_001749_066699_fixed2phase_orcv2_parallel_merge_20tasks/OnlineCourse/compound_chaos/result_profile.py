# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend designs for the 'OnlineCourse' app and produce a merged design specification document.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect specifies Flask routes, data schema, and business logic from the user task description; "
        "FrontendDesignArchitect specifies HTML templates, element IDs, UI structure, and navigation. "
        "DesignMerger reconciles backend_design.md and frontend_design.md into a consistent design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "prompt": """You are a System Architect specializing in Flask backend development and data schema design for Python web applications.

Your goal is to design and specify the backend routes, data file schemas, enrollment and progress tracking logic, and API contracts necessary to implement the 'OnlineCourse' web application.

Task Details:
- Read user_task_description from CONTEXT for all backend requirements including pages, functionalities, and data storage
- Produce backend_design.md independently describing all Flask routes, HTTP methods, expected inputs, outputs, and business logic
- Define exact text file schemas (fields, delimiters, formats, examples) for users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, and certificates.txt
- Specify logic for enrollment management, progress calculation, assignment submissions, and certificate generation
- Do not access or rely on frontend_design.md outputs

**Section 1: Flask Routes Specification**
- List each Flask route with path, HTTP methods, expected request parameters, response format, and behavior
- Include routes for all nine pages and their interactive features (e.g., enrollment, progress update, submissions)
- Define redirects, login/session assumptions (if any), and error handling

**Section 2: Data File Schemas**
- Specify each data file path and exact pipe '|' delimited fields with data types and descriptions
- Provide example data rows for each file matching the requirements document
- Include enrollment progress tracking and status fields with format details

**Section 3: Business Logic and API Contracts**
- Describe enrollment logic: creation, initial progress zero, date recording
- Detail progress update rules: lessons completion sequence, progress percentage calculation
- Outline submission and grading data flow
- Describe certificate generation criteria and data update procedures

CRITICAL SUCCESS CRITERIA:
- Output is complete and independently sufficient backend_design.md
- All route and data schema elements strictly derived from user_task_description
- Use write_text_file tool strictly to save backend_design.md
- Do not read or assume frontend_design.md details
- Output artifacts: backend_design.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [{"type": "user", "name": "user_task_description", "source": "User"}],
            "output_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "prompt": """You are a System Architect specializing in HTML and frontend template design for Python web applications.

Your goal is to design the complete frontend HTML templates, element IDs, UI layouts, and navigation flows for the nine pages of the 'OnlineCourse' web application according to the requirements.

Task Details:
- Read user_task_description from CONTEXT for complete frontend page designs, UI elements, and navigation details
- Independently produce frontend_design.md describing the HTML template structure, element IDs, page titles, and navigation flow
- Specify exact element IDs (including repeated elements with parameters) and types for all buttons, divs, inputs, and other controls per page requirements
- Map navigation links and button actions to the corresponding pages and user flows
- Exclude backend routing, data schema, and business logic details—focus solely on frontend templates
- Do not access or rely on backend_design.md outputs

**Section 1: HTML Template Structure**
- For each of the nine pages, specify the template filename and page title exactly as given
- List all element IDs with element type and purpose
- Specify the layout hierarchy and any repeated elements using parameterized IDs (e.g., view-course-button-{course_id})

**Section 2: Navigation and UI Behavior**
- Define navigation buttons and their target pages
- Describe UI state changes such as button enabling/disabling based on user status (enrolled/not enrolled)
- Specify location of dynamic content placeholders or template variables for course info, assignments, progress, and certificates

CRITICAL SUCCESS CRITERIA:
- Output is a complete frontend_design.md describing all UI templates and navigation flows
- All element IDs and pages strictly derived from user_task_description
- Use write_text_file tool strictly to save frontend_design.md
- Do not read or assume backend_design.md details
- Output artifacts: frontend_design.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [{"type": "user", "name": "user_task_description", "source": "User"}],
            "output_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        },
        {
            "agent_name": "DesignMerger",
            "prompt": """You are a System Architect specializing in synthesizing backend and frontend design specifications into coherent unified documentation for Flask web applications.

Your goal is to combine backend_design.md and frontend_design.md with the user_task_description into one consistent design_spec.md that reconciles all routes, data schemas, UI templates, element IDs, and navigation flows without adding new requirements.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Validate completeness and consistency between backend routes and frontend templates for the nine pages
- Ensure all route context variables and UI element IDs are aligned and naming consistent
- Integrate backend data schemas with frontend UI data placeholders coherently
- Preserve all backend and frontend sections and reconcile any conflicts or overlap strictly within original requirements

**Section 1: Integrated Flask Routes and API Contracts**
- Combine backend routes and endpoint specifications ensuring alignment with frontend navigation and UI actions
- Document consistent input/output formats and parameters referenced in frontend templates

**Section 2: Combined HTML Template Specifications**
- Present all frontend templates with exact element IDs as per frontend_design.md
- Ensure navigation flow matches backend routing and business logic
- Clarify dynamic UI components tied to backend data schemas

**Section 3: Data Schemas and Business Logic Summary**
- Present unified data file schemas and examples from backend_design.md
- Ensure descriptions match frontend data usage and UI display

CRITICAL SUCCESS CRITERIA:
- Output is a single design_spec.md artifact fully consistent with inputs
- Backend and frontend designs are fully reconciled without information loss or conflict
- Use write_text_file tool strictly to save design_spec.md
- Output artifact: design_spec.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "backend_design.md", "source": "BackendDesignArchitect"},
                {"type": "text_file", "name": "frontend_design.md", "source": "FrontendDesignArchitect"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend routes, data schemas, and logic completeness for 'OnlineCourse' against requirements.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Validate frontend templates, element IDs, and navigation flow for accuracy and completeness.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend code artifacts from design_spec.md and integrate them into a consistent final web application.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py backend logic independently from design_spec.md; "
        "FrontendDeveloper implements templates/*.html frontend UI independently using design_spec.md; "
        "IntegrationMerger integrates and reconciles backend and frontend artifacts into final app.py and templates/*.html ensuring interface consistency."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Backend Developer specializing in Flask web applications with local text-file data handling.

Your goal is to implement the complete Flask backend app.py based on design_spec.md independently of the frontend implementation.

Task Details:
- Read design_spec.md from CONTEXT
- Implement all Flask routes, business logic, data file handling, enrollment, progress tracking, certificate generation
- Produce a fully functional app.py covering all declared routes and data operations, reflecting the user task requirements
- Do not read or assume templates/*.html sibling outputs

**Implementation Requirements:**
- Implement Flask route handlers exactly as specified, with correct HTTP methods and route paths
- Handle all file operations on data/*.txt files using the specified formats for users, courses, enrollments, assignments, submissions, certificates
- Manage user enrollment creation with initial progress and dates, update progress on lesson completion, and generate certificates at 100% progress
- Provide error handling for data consistency and access

**Code Style and Integration:**
- Use Python with Flask idioms and standard libraries only
- Include comments using hash (#) style and use triple single-quotes (''') for any code documentation
- Maintain clear separation of route logic, file I/O, and business rules in the code structure

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output app.py
- Implementation strictly follows design_spec.md specifications and data formats from user task
- Do not write any output other than app.py and do not use sibling outputs

Output: app.py""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "agent_name": "FrontendDeveloper",
            "prompt": """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement all required HTML templates (*.html) independently, following the design_spec.md without dependence on backend code specifics.

Task Details:
- Read design_spec.md from CONTEXT
- Implement templates/*.html with full page structures, element IDs, buttons, inputs, tables, and navigation flows
- Ensure each template corresponds to a page defined in design_spec.md, with correct page titles and required repeated element IDs as indicated
- Do not read or assume app.py backend code sibling outputs

**Implementation Requirements:**
- Implement Jinja2-compatible HTML templates with consistent file naming and structure as per design_spec.md
- Include all specified element IDs exactly, with appropriate element types (div, h1, button, input, textarea, table)
- Ensure navigation buttons and links correspond to the declared routes and produce correct user navigation flow
- Use semantic HTML and organize layout clearly for all nine pages described in user task documentation

**Code Style and Integration:**
- Use consistent indentation, escaping, and Jinja2 syntax as needed
- Include brief comments via HTML or Jinja2 comments as appropriate for clarity

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output templates/*.html files
- Implementation strictly follows design_spec.md frontend specifications and page details from user task
- Do not write any output other than templates/*.html and do not use sibling outputs

Output: templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        },
        {
            "agent_name": "IntegrationMerger",
            "prompt": """You are a Software Integration Engineer specializing in Flask backend and frontend template consolidation.

Your goal is to merge and reconcile backend app.py and frontend templates/*.html artifacts into a consistent final deployment-ready web application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Identify and resolve any interface mismatches between backend routes, expected templates, and frontend navigation elements
- Ensure data flows, route handlers, and template element IDs align perfectly and navigation structures function coherently
- Produce reconciled final app.py and templates/*.html outputs that satisfy user requirements and are mutually consistent

**Integration Process:**
- Compare route declarations and handlers in app.py with template files referencing those routes
- Verify all buttons and navigation links in templates correspond to valid backend routes
- Correct any naming or interface mismatches without adding new features or removing declared functionality
- Ensure adherence to design_spec.md as the source of truth and no additional requirements are introduced

**Validation and Consistency Checks:**
- Validate that app.py runs without syntax errors and handles declared routes as expected
- Validate templates render correctly with required element IDs and navigation paths
- Preserve all user task and design_spec.md data format and UI element constraints

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool exclusively to output final app.py and templates/*.html
- Final artifacts are fully consistent, deployable, and reflect user task specifications without deviation
- Do not produce or modify any other artifacts beyond declared outputs

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
            "review_criteria": "Check backend app.py for correct route implementations, data file management, and business logic conformity.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates/*.html adhere to design_spec.md including all element IDs and navigation correctness.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a complete Python Flask web application 'OnlineCourse' with local text file data storage, multiple interactive pages, and full backend/frontend integration based on the user requirements document.",
    workflow: list = [
        {
            "step": 1,
            "description": "Create backend and frontend design specifications and merge into a unified design document.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Merged comprehensive backend and frontend design for OnlineCourse."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend code independently from design; merge and reconcile into final deployable artifacts.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Final integrated backend and frontend implementation for OnlineCourse."
                }
            ]
        }
    ]
): pass
# Orchestrate_End