# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications capturing all required Flask routes, data interaction patterns, and HTML template structures with element IDs, then merge into a single consistent design_spec.md document.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs detailed Flask route endpoints, data schemas, "
        "and file interaction patterns producing backend_design.md. FrontendDesignArchitect "
        "defines HTML templates, element IDs, UI components, navigation, and filtering mechanisms "
        "producing frontend_design.md. DesignMerger consolidates these two documents into a "
        "unified design_spec.md ensuring consistency and completeness without adding new features."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "prompt": """You are a System Architect specializing in Python Flask backend development with local text file database interaction.

Your goal is to specify the backend design including Flask routes, data access logic, and data schemas reflecting the MusicStreaming application requirements.

Task Details:
- Read user_task_description from CONTEXT
- Independently create backend_design.md specifying all Flask endpoints, request methods, and data interaction patterns
- Utilize the specified local text data files: songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt
- Exclude any dependency or assumptions on frontend_design.md

**Section 1: Flask Route Specifications**
- Define each route path, HTTP method(s), expected request parameters, and response data structure
- Include routes for searching songs, managing playlists, browsing albums, exploring artists, filtering genres, and statistics pages
- Specify JSON structures or context variables passed to templates where applicable

**Section 2: Data File Schemas and Access**
- Describe the exact parsing logic and schema for each local text file based on column definitions and delimiters
- Detail how data is read, filtered, and aggregated from these files in the backend
- Cover data models representing songs, artists, albums, genres, playlists, and playlist songs with example data rows

**Section 3: API and Integration Details**
- Define APIs for add/remove songs in playlists, play counts updates, and navigation handling
- Describe any necessary query parameters for filtering and sorting on the backend

CRITICAL SUCCESS CRITERIA:
- BackendDeveloper can implement functional Flask routes and data access from backend_design.md alone
- Data file schemas are accurate and directly correspond to user_task_description examples
- Use write_text_file tool to output backend_design.md

Output: backend_design.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ],
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "prompt": """You are a System Architect specializing in HTML and Jinja2 template design for Python web applications.

Your goal is to specify frontend HTML templates with detailed element IDs and UI structure for all MusicStreaming web pages as described.

Task Details:
- Read user_task_description from CONTEXT
- Independently create frontend_design.md detailing all required HTML template files and their element IDs
- Cover each of the ten specified pages: Dashboard, Song Catalog, Song Details, Playlists, Playlist Details, Create Playlist, Album Browse, Album Details, Artist Profiles, and Genre Exploration
- Specify UI components such as buttons, input fields, dropdowns, grids, tables, and navigation widgets
- Do not depend on backend_design.md

**Section 1: HTML Templates Overview**
- For each page, specify template filenames and page titles
- List element IDs with their HTML element types and roles
- Define navigation button actions and filtering UI elements

**Section 2: UI Components and Interactions**
- Detail how search inputs, dropdown filters, and buttons interact within templates
- Include dynamic elements needing context variables and loops (e.g., song cards, playlist grids)
- Provide exact ID conventions for controls like add-to-playlist and remove-song buttons with placeholders

CRITICAL SUCCESS CRITERIA:
- FrontendDeveloper can implement all templates and UI elements from frontend_design.md alone
- Element IDs and page structures comply strictly with user_task_description
- Use write_text_file tool to output frontend_design.md

Output: frontend_design.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ],
        },
        {
            "agent_name": "DesignMerger",
            "prompt": """You are a System Architect specializing in integrating backend and frontend design specifications for Flask web applications.

Your goal is to merge backend_design.md and frontend_design.md into a unified, consistent design_spec.md without introducing new features beyond the user task.

Task Details:
- Read user_task_description, backend_design.md, and frontend_design.md from CONTEXT
- Verify completeness and resolve any inconsistencies between backend routes, data schemas, and frontend template elements
- Ensure naming conventions, element IDs, and route parameters align perfectly across designs
- Consolidate all information into one canonical design_spec.md document

**Section 1: Consistency Verification**
- Cross-check that every frontend element requiring backend data has matching route/context variable definitions
- Confirm all backend routes are supported by corresponding frontend templates or UI components

**Section 2: Unified Design Specification**
- Integrate backend routes, data schemas, and frontend templates with element IDs into coherent sections
- Maintain clear separation with consistent formatting consistent for developer consumption

CRITICAL SUCCESS CRITERIA:
- Resulting design_spec.md enables developers to implement both backend Flask routes and frontend HTML templates with no contradictions
- The artifact references ONLY declared input artifacts; no extra requirements added
- Use write_text_file tool to output design_spec.md

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
            ],
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend design completeness and correctness per user task and local file data handling.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness and correctness of HTML element IDs and page structures.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the backend app.py and frontend templates/*.html based on design_spec.md and merge into a complete functional Python Flask app with HTML templates.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements Flask app.py with routes, data loading, and processing per design_spec.md. "
        "FrontendDeveloper implements all HTML templates with specified element IDs and UI features concurrently. "
        "IntegrationMerger reconciles app.py and templates/*.html ensuring interface consistency and writes the final "
        "app.py and all templates."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Python backend developer specializing in Flask web applications.

Your goal is to implement a complete Flask backend application as specified in design_spec.md, focusing on data handling using local text files, request routing, and business logic for the MusicStreaming app.

Task Details:
- Read design_spec.md from CONTEXT for all backend route specifications, data schemas, and functional requirements.
- Produce a fully functional app.py implementing Flask routes, data loading from text files, search operations, playlist management, filtering, and statistics.
- Do not incorporate frontend template details other than render and context variable usage as specified.
- Write app.py independently without reading frontend templates.

**Implementation Requirements:**
- Implement data loading functions to read all specified text files (songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, playlist_songs.txt) with correct parsing per schema.
- Define Flask routes with route paths, HTTP methods, and handlers as documented in design_spec.md.
- Include logic for search (songs, albums, artists), filtering (genres), playlist CRUD operations, album and artist detail retrieval, and statistics computations.
- Render templates with correct context dictionaries matching design_spec.md variable contracts.

**Code Quality and Structure:**
- Use concise, modular functions with clear single-quote docstring documentation.
- Handle errors gracefully, especially file I/O and data integrity issues.
- Maintain code readability with consistent style and commenting.

CRITICAL SUCCESS CRITERIA:
- app.py must comply fully with design_spec.md requirements for routes, data access, and processing.
- Must use write_text_file tool to save app.py.
- Output only the declared artifact app.py without extraneous notes.

Output: app.py""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ],
        },
        {
            "agent_name": "FrontendDeveloper",
            "prompt": """You are a frontend developer specializing in HTML and Jinja2 templating for Flask applications.

Your goal is to implement all HTML templates (*.html) for the MusicStreaming app using element IDs, page structures, and navigation flows as specified in design_spec.md.

Task Details:
- Read design_spec.md from CONTEXT to extract frontend template specifications including page layouts, element IDs, and UI components.
- Independently create all required templates under templates/*.html with correct element IDs and content placeholders.
- Ensure navigation buttons, links, and data bindings match design_spec.md specifications.
- Do not read or depend on backend code files.

**Template Implementation Guidelines:**
- Follow the exact page titles and element IDs as defined.
- Use Jinja2 syntax for dynamic content rendering consistent with context variables described in design_spec.md.
- Include page containers, buttons, inputs, grids, tables, and other UI elements with proper semantic HTML structures.
- Maintain consistent style and accessibility where applicable.

**Navigation and Interaction:**
- Implement all buttons with designated IDs linked to appropriate routes or JavaScript hooks per design_spec.md.
- Ensure forms, dropdowns, and search inputs are properly named and integrated.

CRITICAL SUCCESS CRITERIA:
- All templates must fully conform to design_spec.md UI requirements and element ID mappings.
- Must use write_text_file tool to write templates/*.html files.
- Output only the declared artifact templates/*.html, no additional files or commentary.

Output: templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ],
        },
        {
            "agent_name": "IntegrationMerger",
            "prompt": """You are a software integration engineer specializing in merging Flask backend and frontend templates for web applications.

Your goal is to consolidate and reconcile the backend app.py and frontend templates/*.html into a consistent, functional MusicStreaming app aligned with design_spec.md.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Verify that all routes in app.py have corresponding templates with matching element IDs and navigation controls.
- Detect and correct interface inconsistencies between backend context variables and frontend template placeholders.
- Adjust only integration-related issues without altering core logic or UI specifications.
- Produce the final app.py and templates/*.html artifacts fully aligned and ready for deployment.

**Integration Tasks:**
- Confirm all page routes defined in design_spec.md are implemented in app.py and referenced by templates.
- Ensure element IDs in templates correspond to context variables rendered by app.py routes.
- Verify that navigation buttons and links work correctly between pages as defined.
- Correct any mismatches in naming, missing elements, or broken bindings.

**Quality Assurance:**
- Adhere strictly to design_spec.md requirements without adding new features.
- Provide clear consistency in naming conventions and data flow between backend and frontend.
- Maintain proper formatting and code comments only where necessary for integration clarity.

CRITICAL SUCCESS CRITERIA:
- Final app.py and templates/*.html fully conform to design_spec.md and pass backend-frontend integration validation.
- Use write_text_file tool to output final app.py and all templates/*.html.
- Output only declared artifacts app.py and templates/*.html.

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
            ],
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify backend implementation correctness and conformance to design_spec.md.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend template correctness and conformance to design_spec.md.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop complete Python Flask 'MusicStreaming' web application with frontend templates and backend app.py per user requirements and local text data management.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design specification and merged design.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce merged backend and frontend design specification."
                }
            ],
        },
        {
            "step": 2,
            "description": "Parallel backend and frontend implementation and integration merge.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce merged backend app.py and frontend templates/*.html implementation."
                }
            ],
        }
    ]
): pass
# Orchestrate_End