# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications for 'BookstoreOnline' and merge them into one consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs the Flask routes and data schemas, including local text file formats and data handling requirements. "
        "FrontendDesignArchitect designs the HTML templates, element IDs, navigation, and page structure as per the specifications. "
        "DesignMerger consolidates backend_design.md and frontend_design.md ensuring consistency with the user task and outputs design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "prompt": """You are a System Architect specializing in Flask backend development and data schema design for Python applications using local text file storage.

Your goal is to produce the backend design specification covering all Flask routes, local text data file formats, and backend logic needed for the 'BookstoreOnline' user requirements.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md
- Specify all Flask routes with methods, route paths, expected request parameters, and response templates
- Specify all data schemas for local text files (books.txt, categories.txt, cart.txt, orders.txt, order_items.txt, reviews.txt, bestsellers.txt) including exact file names, delimiter '|', field order, data types, and example rows
- Do not read or rely on frontend_design.md

**Section 1: Flask Routes Specification**
- Define route URL patterns, HTTP methods, function names, and associated template filenames
- Detail context variables passed to templates, form data received, and actions performed (e.g., add to cart, checkout, submit review)
- Include routes for all nine pages (Dashboard, Book Catalog, Book Details, Shopping Cart, Checkout, Order History, Reviews, Write Review, Bestsellers)
- Include navigation routes between pages and button action handling

**Section 2: Text File Data Schemas**
- For each data file, describe file name, exact delimiter, column names with data types, and constraints
- Provide sample data rows matching user examples for clarity
- Include data manipulation considerations (e.g., updating stock, cart contents, order status)

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement the entire Flask backend using backend_design.md alone
- Routes and data schemas strictly align with user_task_description and local text file storage approach
- Must use write_text_file tool to output backend_design.md
- Output only the declared artifact backend_design.md without refinement markers

Output: backend_design.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [{"type": "user", "name": "user_task_description", "source": "User"}],
            "output_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "prompt": """You are a System Architect specializing in HTML/Jinja2 template design and user interface structure for Python web applications.

Your goal is to produce the frontend design specification covering all HTML templates, exact element IDs, page structure, and navigation flows to implement the 'BookstoreOnline' web UI.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md
- Specify all HTML templates for the nine pages detailed in user_task_description
- Define exact element IDs, element types (div, button, table, input, dropdown, textarea, etc.), and page titles
- Specify navigation flows between pages triggered by buttons and links
- Include lists/grids/tables structure, context variables used in templates, and dynamic elements such as book lists, cart items, reviews, and bestsellers
- Do not read or rely on backend_design.md

**Section 1: HTML Template Specifications**
- Specify each template file name and page title
- List every element ID with its HTML tag type and description reflecting user_task_description
- Define dynamic content placeholders (e.g., book cards, reviews list) and how data from context variables maps to layout
- Map buttons and navigation controls to their target pages or actions

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement all templates from frontend_design.md alone
- Element IDs, page titles, and navigation flow are fully consistent with user_task_description
- Must use write_text_file tool to output frontend_design.md
- Output only the declared artifact frontend_design.md without refinement markers

Output: frontend_design.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [{"type": "user", "name": "user_task_description", "source": "User"}],
            "output_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        },
        {
            "agent_name": "DesignMerger",
            "prompt": """You are a System Architect specializing in web application specification integration and consistency validation.

Your goal is to merge backend_design.md and frontend_design.md into one cohesive design_spec.md that fully satisfies the 'BookstoreOnline' user requirements without contradictions or omissions.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Independently reconcile backend and frontend specifications ensuring alignment on routes, templates, element IDs, navigation, and data schemas
- Validate completeness of all nine pages and their functionalities as specified by user_task_description
- Produce a consolidated design_spec.md including backend Flask routes, data schemas, frontend templates, element IDs, and navigation maps

**Section 1: Backend and Frontend Consistency Checks**
- Cross-check route URLs with template file names and frontend navigation targets
- Ensure element IDs referenced in backend context variables exist in frontend templates
- Resolve any naming discrepancies in routing, context variable usage, or data files

**Section 2: Comprehensive Design Specification**
- Combine all backend and frontend details into one unified specification document
- Organize sections clearly: Flask routes, local text file data schemas, HTML templates, element IDs, and navigation flows
- Highlight how data flows between backend and frontend using local text files as persistent store

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper and FrontendDeveloper can implement their parts directly from design_spec.md
- The consolidated artifact contains no conflicting specifications or missing requirements
- Must use write_text_file tool to output design_spec.md
- Output only the declared artifact design_spec.md without refinement markers

Output: design_spec.md""",
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
            "review_criteria": "Ensure backend design completeness and alignment with user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Ensure frontend design completeness and alignment with user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend artifacts from design_spec.md in parallel and integrate them into a consistent 'BookstoreOnline' application",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py using backend specifications from design_spec.md including data management from local text files. "
        "FrontendDeveloper implements all HTML templates (*.html) including all required pages and element IDs. "
        "IntegrationMerger reconciles app.py and templates/*.html ensuring interface consistency and produces final deployable app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Backend Developer specializing in Python Flask applications with local text file data management.

Your goal is to implement the complete Flask backend app.py based exclusively on backend specifications from design_spec.md, managing all data operations on local text files as declared.

Task Details:
- Read design_spec.md from CONTEXT
- Independently implement app.py with Flask routes and data file handling as specified
- Produce app.py implementing all backend logic including CRUD, data parsing, and business rules per design_spec.md
- Do not read or use any frontend templates or outputs

**Implementation Requirements: Flask Backend**
- Implement each route with correct URL, HTTP methods, and handlers as defined
- Implement reading from and writing to designated text files (e.g., books.txt, cart.txt, orders.txt) per specified schema
- Handle all user actions: browsing books, cart management, checkout, reviews, and order history without authentication
- Use consistent variable and function names per design_spec.md conventions
- Implement data parsing with correct field delimiters and types from text files
- Return JSON or render templates endpoints as appropriate (render_template calls match frontend expectations)

**Code Structure and Standards:**
- Use single-quoted docstrings for any inline documentation or code comments
- Follow Flask best practices for route definition, error handling, and modularity
- Include writing to 'data' directory files with proper file locking or atomic writes if needed
- No external databases or persistent storage outside specified text files permitted

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save app.py output
- Implement only declared routes and data interactions as per design_spec.md
- Generated app.py is complete, self-contained, and ready for integration with frontend templates
- Do not use or produce any files beyond app.py

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
            "prompt": """You are a Frontend Developer specializing in HTML and Jinja2 template development for Flask applications.

Your goal is to fully implement all frontend HTML templates (*.html) for the 'BookstoreOnline' application, strictly following the structure, element IDs, and navigation requirements specified in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT
- Independently create all templates/*.html reflecting the nine pages described
- Include all specified page titles, container divs, buttons, inputs, tables, dropdowns, and navigation elements exactly as named
- Implement Jinja2 templating syntax where dynamic data rendering is implied
- Do not read, validate, or assume any backend implementations beyond design_spec.md

**Template Implementation Guidelines:**
- Preserve exact ID attributes for all elements like dashboard-page, featured-books, search-input, cart-items-table, etc.
- Include navigation controls between pages as specified (e.g., buttons linking dashboard to catalog, back-to-dashboard buttons)
- Structure tables for cart, orders, and reviews with appropriate columns and placeholders for dynamic content
- Implement forms for order checkout and write review pages with correct input types and IDs
- Follow HTML5 standards and keep templates modular and readable

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save template files in templates/*.html
- Templates completely reflect design_spec.md page and element requirements without deviation
- Do not use or write any files beyond the declared templates
- Generated frontend is ready to integrate seamlessly with backend app.py

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
            "prompt": """You are a Software Integration Specialist skilled in merging Flask backend and Jinja2 frontend templates.

Your goal is to review and merge the independently implemented app.py backend and templates/*.html frontend outputs to ensure full consistency, correctness, and readiness for production deployment of the 'BookstoreOnline' application.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate that app.py routes match template filenames, element IDs, and navigation flows in templates
- Ensure data variable names passed from backend to frontend templates are consistent and correctly referenced
- Detect and resolve interface discrepancies between backend endpoints and frontend template expectations
- Produce final integrated and consistent app.py and templates/*.html artifacts ready for deployment

**Integration and Consistency Checks:**
- Verify all route URLs in app.py exist as links or forms in frontend templates
- Check that all template variables rendered are set or passed correctly from app.py
- Confirm all input elements, buttons, and forms in templates correspond to backend handlers managing data files
- Harmonize any naming conflicts or missing elements found between backend and frontend
- Ensure no additional features or requirements beyond design_spec.md are introduced

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output final app.py and templates/*.html
- Output artifacts overwrite prior worker versions with fully reconciled content
- Focus only on inputs from declared artifacts, no external assumptions
- Provide integrated deliverables that enable seamless Flask app execution with complete UI

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
            "review_criteria": "Validate backend implementation against design_spec.md and integration interface.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Validate frontend HTML templates against design_spec.md and integration interface.",
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
    goal: str = "Develop the 'BookstoreOnline' Python Flask web application with complete backend and frontend, integrated and verified",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel complementary design of backend and frontend specifications and merging into design_spec.md.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce a merged backend and frontend design specification"
                }
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend from design_spec.md and integration into final app.py and templates/*.html.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce final integrated backend and frontend code"
                }
            ]
        }
    ]
): pass
# Orchestrate_End