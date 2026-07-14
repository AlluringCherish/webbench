# Phase1_Start
def design_specification_phase(
    goal: str = "Debate the adaptive Web design contract for the OnlineLibrary app for exactly two total rounds and produce a unified design_spec.md document.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "DesignDebaterA and DesignDebaterB independently draft design artifacts for the OnlineLibrary app in round 1, revise from each other's drafts in round 2, then DesignJudge adjudicates and synthesizes the final design_spec.md incorporating the user requirements and exact page routes, elements, and file data formats.",
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "prompt": """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and improve a detailed design_debate_a.md for the OnlineLibrary application through exactly two total debate rounds.

Task Details:
- Read user_task_description each round focusing on the 'OnlineLibrary' web app requirements
- In round 1, independently write a complete design_debate_a.md covering Flask routes, HTTP methods, templates, page navigation flows, element IDs, and local text file data handling
- In round 2, read previous design_debate_a.md and peer design_debate_b.md; update your design_debate_a.md incorporating valid peer improvements only
- Overwrite the entire design_debate_a.md artifact every round

**Section 1: Flask Routes Specification**
- Precisely specify all route paths, HTTP methods, corresponding template files, and required context variables for each of the ten pages declared by the user
- Ensure routes preserve all user-declared page names and enable the Dashboard as the default entry '/'
- Specify navigation targets and transitions exactly as per user page design
- Maintain correct mapping of page element IDs and dynamic IDs for repeated elements (e.g., buttons with {book_id})

**Section 2: HTML Template and Page Elements**
- Document template file names and page titles exactly as stated by the user
- List all UI element IDs and their types per page, preserving dynamic IDs formatting
- Specify interactions like buttons and forms with exact field names and methods when relevant

**Section 3: Data Persistence and Local Text Files**
- Specify data files used per functionality, respecting the exact file names and formats given
- Map how Flask routes access and update the local text files in the 'data' directory
- Include data format schemas and delimiters as per specification with no deviations

CRITICAL SUCCESS CRITERIA:
- Implement two total debate rounds: independent round 1 and one peer-informed round 2
- Produce a comprehensive, implementation-ready design_debate_a.md each round
- Keep all user-declared routes, methods, element IDs, navigation flows, and local text data schemas exact
- Use write_text_file tool to output design_debate_a.md

Output: design_debate_a.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_debate_a.md"}
            ]
        },
        {
            "agent_name": "DesignDebaterB",
            "prompt": """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and improve a comprehensive design_debate_b.md for the OnlineLibrary application through exactly two total debate rounds.

Task Details:
- Read user_task_description each round with attention to adaptive Flask route contracts and page element IDs
- In round 1, independently write a complete design_debate_b.md that defines exact Flask route contracts, page context variables, local text file data integration, and dynamic element ID usage
- In round 2, revise design_debate_b.md based on review of own and peer designs (design_debate_a.md) keeping conformance to user requirements and the adaptive web contract
- Overwrite the entire design_debate_b.md artifact every round

**Section 1: Flask Route Contracts**
- Specify all user-declared routes with HTTP methods, templates, expected context variables, and form definitions
- Preserve the exact page routes, including dynamic parameters such as {book_id}, {borrow_id}, etc.
- Ensure default route '/' renders or redirects to Dashboard page

**Section 2: Context Variables and Page Navigation**
- Define all context variables passed to templates, including dynamic data from local files
- List client-side element IDs, including dynamically generated IDs, exactly as declared
- Specify navigation flows between pages using button or link element IDs

**Section 3: Local Text Data Integration**
- Describe reading and writing of local text files with the exact filenames and schema
- Ensure correct data mapping between route handlers and local file persistence
- Maintain use of 'data' directory and '|' delimiter text formats without alteration

CRITICAL SUCCESS CRITERIA:
- Perform exactly two total rounds: initial independent and one peer-informed revision
- Provide complete design_debate_b.md in each round, strictly following the adaptive web design contract
- Use write_text_file tool for saving design_debate_b.md

Output: design_debate_b.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_debate_b.md"}
            ]
        },
        {
            "agent_name": "DesignJudge",
            "prompt": """You are a Senior System Architect adjudicating two competing Flask web application designs for the OnlineLibrary app.

Your goal is to write a single authoritative design_spec.md document merging the final artifacts from both debaters after exactly two debate rounds, respecting the user requirements strictly.

Task Details:
- Read user_task_description, final design_debate_a.md, and design_debate_b.md 
- Compare all Flask routes, templates, page element IDs, context variables, navigation flows, and local text file interactions
- Resolve conflicts or differences strictly based on the user requirements document, preserving declared routes, HTTP methods, element IDs including dynamic ones, and data formats
- Write a full and internally consistent canonical design_spec.md that supports implementation without omitted routes or overlooked data handling

**Section 1: Flask Routes and Methods**
- Enumerate all user-declared page routes, HTTP methods, and associated templates
- Prescribe exact function names, URL parameters, and expected context variables
- Ensure '/' serves or redirects to the Dashboard page precisely

**Section 2: HTML Template Specifications and Elements**
- Specify all page template files, titles, and element IDs with exact naming (including dynamic )
- Detail navigation flows between pages with exact button IDs for links or actions

**Section 3: Local Text Data Files and Formats**
- Describe the local text files used (filenames, directories, delimiter '|', field schemas)
- Confirm how the web app reads from and writes to these files per user functionality
- Maintain the data directory organization without adding files or altering schema

CRITICAL SUCCESS CRITERIA:
- Final design_spec.md must be complete, internally consistent, and fulfill the user's original detailed requirements
- Preserve every declared page, route, element ID, HTTP method, field name, navigation path, and file format
- Use write_text_file tool to save design_spec.md

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignDebaterA",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Verify design_debate_a.md exists, is non-empty, coherent, follows requirements format, contains Flask route specs for all user-declared pages including element IDs and data persistence.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Check design_debate_b.md exists, is relevant, readable, specifies adaptive web contract conformance including exact routes, forms, and page element IDs.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Confirm design_spec.md exists, is non-empty, correct, complete with the final canonical web design definition meeting user requirements as specified.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate full Python Flask implementation of OnlineLibrary with all defined routes, templates, local text data management, and UI elements for exactly two total rounds and produce final app.py and templates/*.html artifacts.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "ImplementationDebaterA and ImplementationDebaterB independently develop candidate app.py and templates sets from design_spec.md in round 1, each revises their versions with peer insights in round 2, then ImplementationJudge combines and adjudicates the final complete app.py and HTML templates without adding features.",
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "prompt": """You are a Python Flask Developer specialized in full-stack web application implementation focusing on backend logic, frontend templates, and local text file data handling.

Your goal is to create and revise a complete Flask app.py and a full set of HTML templates implementing all specified routes, UI elements, page titles, precise HTML element IDs (including dynamic IDs), navigation flows, and local text file data management as defined for the OnlineLibrary application.

Task Details:
- Read design_spec.md fully each round for precise route, template, and data requirements
- Produce or update app_debate_a.py and templates_debate_a/*.html implementing all defined pages and behaviors
- Preserve all exact user-declared route paths, HTTP methods, template file names, context variables, HTML element IDs (static and dynamic), form actions/methods, and navigation targets
- In round 2, use app_debate_b.py and templates_debate_b/*.html peer artifacts to improve and correct your implementation
- Use local text files as specified for data loading and persistence under ‘data’ directory using pipe delimiter

**Section 1: Flask Application Implementation Requirements**
- Implement all Flask routes matching the declared URLs in design_spec.md, including the root route `/` rendering or redirecting to Dashboard page
- Ensure GET and POST methods as specified, preserving exact form field names and submission behaviors
- Handle data read/write exclusively via local text files as per given formats, parsing pipe-delimited records accurately
- Incorporate borrowing logic, reservation management, reviews, payments, and user profile edits respecting data integrity and specified UI flows

**Section 2: HTML Template Implementation Guidelines**
- Implement all templates with file names and folder structure reflecting templates_debate_a/*.html
- Ensure page titles and precise HTML element IDs exactly match the specification including dynamic IDs like `view-book-button-{book_id}`
- Maintain consistent navigation buttons with exact target routes and element IDs
- Preserve form element names, methods, and actions as declared, supporting all user inputs for searches, reviews, profile updates, borrow confirmations, and payments

**Section 3: Revision and Consistency Rules**
- In round 2, analyze provided peer app_debate_b.py and templates_debate_b/*.html to identify discrepancies or missed requirements
- Correct your own candidate app_debate_a.py and templates_debate_a/*.html accordingly without adding unrequested features
- Ensure consistent data usage, route implementations, and UI element presence between your artifacts and peer artifacts

CRITICAL REQUIREMENTS:
- MUST use write_text_file tool for saving the complete app_debate_a.py and every template file in templates_debate_a/
- Strictly adhere to all user-specified route paths, HTTP methods, template names, context variables, HTML element IDs (including dynamic), form field names, and local text file data formats
- Implement exact navigation flows, including `/` rendering or redirecting to Dashboard page
- Produce output files only: app_debate_a.py and templates_debate_a/*.html, no additional outputs or refinement markers

Output: app_debate_a.py and templates_debate_a/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "agent_name": "ImplementationDebaterB",
            "prompt": """You are a Python Flask Developer specializing in implementing comprehensive web applications with full backend and frontend integration, optimized for local text file data persistence.

Your goal is to develop and revise an independent Flask app_debate_b.py along with a complete set of templates_debate_b/*.html implementing all Functionalities, routes, and UI interfaces for OnlineLibrary as specified.

Task Details:
- Fully absorb design_spec.md input to understand all required routes, context variables, element IDs, and data handling
- Independently build or update app_debate_b.py and templates_debate_b/*.html incorporating all pages, UI components, and local file data management
- Maintain exact matching of user-declared route paths, HTTP methods, HTML element IDs (including dynamic IDs), form field names, navigation targets, and data file operations
- In round 2, consult app_debate_a.py and templates_debate_a/*.html for peer input to enhance completeness and correctness
- Employ pipe-delimited local text files as the sole data source/sink within the ‘data’ directory, applying correct parsing and writing

**Section 1: Flask Backend Implementation**
- Realize all Flask routes per specification, providing exact GET/POST method behaviors, including root `/` that must load or redirect to Dashboard
- Implement borrow, return, reservation, review, profile, and payment endpoints accurately reading/writing the designated text files
- Ensure code clarity and maintain consistent variable naming aligned with design_spec.md

**Section 2: HTML Frontend Template Implementation**
- Deliver all templates according to the declared filenames under templates_debate_b/
- All elements must have the precise HTML IDs specified; for dynamic IDs such as `return-book-button-{borrow_id}`, generate as required
- Include all navigation and buttons as specified with their exact IDs and targets
- Preserve form characteristics including method, action, field names for all input controls

**Section 3: Peer Review Integration**
- For the revision round, analyze the peer app_debate_a.py and templates_debate_a/*.html to identify deficiencies or missing elements
- Improve your candidate outputs accordingly without introducing non-specified features
- Maintain strict compliance with user declarations across all artifacts and rounds

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output app_debate_b.py and templates_debate_b/*.html files
- Do not deviate from explicit user requirements including routes, element IDs, and data formats
- Root route `/` must render or redirect to Dashboard page precisely as specified
- Only produce declared output files; avoid extraneous commentary or refinement markers

Output: app_debate_b.py and templates_debate_b/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "agent_name": "ImplementationJudge",
            "prompt": """You are a Senior Python Flask Developer and Integrator responsible for adjudicating two competing implementations into a final canonical online library web application.

Your goal is to synthesize, reconcile, and write a comprehensive, fully functional app.py and complete set of templates/*.html consistent strictly with design_spec.md, app_debate_a.py, app_debate_b.py, and their respective template sets, without adding additional features.

Task Details:
- Read design_spec.md for authoritative requirements and context including all routes, templates, UI elements, and local text file data formats
- Consume final round outputs: app_debate_a.py and templates_debate_a/*.html plus app_debate_b.py and templates_debate_b/*.html
- Compare and merge Flask routes, application logic, and template HTML elements ensuring correctness and completeness
- Resolve any conflicting implementations in favor of user declared specifications with no enhancements
- Produce one canonical app.py implementing all required features with exact route paths, HTTP methods, data handling, and navigation flows
- Produce canonical templates/*.html files with precise element IDs, dynamic IDs, page titles, and form structures matching spec

**Section 1: Integration and Consistency Verification**
- Validate all routes, methods, and navigation flows present in both candidates and conforming to design_spec.md
- Ensure all local data file operations align to declared file formats and file paths under 'data' directory
- Confirm every UI element ID and dynamic ID matches the authoritative page design, preserving user expectations

**Section 2: Canonical Artifact Generation**
- Deliver a single app.py and a set of templates/*.html files representing the authoritative implementation
- Ensure root path `/` renders or redirects to the Dashboard page exactly
- Use write_text_file tool to save all outputs cleanly without auxiliary commentary or extra files

CRITICAL SUCCESS CRITERIA:
- Final artifacts fully implement all pages, routes, UI elements, and data handling per user specification and design_spec.md
- No new features or requirements are introduced beyond user directives
- All file names, IDs, methods, and navigation targets are exactly as specified
- Outputs are ready for functional deployment as a Flask application

Output: app.py and templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationDebaterA",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve candidate app_debate_a.py and templates_debate_a/*.html presence, readability, adherence to design_spec.md, and absence of catastrophic errors; no full completion required.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve candidate app_debate_b.py and templates_debate_b/*.html presence, accuracy, conformity to design_spec.md, and no catastrophic mistakes; no full completion required.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Confirm final app.py and templates/*.html exist, are readable, fully implement design_spec.md with no feature additions, and are broadly usable as a Flask application.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Create the OnlineLibrary Python Flask Web application fully implementing the specified pages, local text file data management, and adaptive fixed Web interface contract.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design phase: debate and adjudicate the adaptive Web design contract for OnlineLibrary.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Adaptively design the OnlineLibrary Flask web application architecture and interface."}
            ]
        },
        {
            "step": 2,
            "description": "Implementation phase: debate and adjudicate the full Python Flask app and templates implementation.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and verify the complete OnlineLibrary app and templates per design specification."}
            ]
        }
    ]
): pass
# Orchestrate_End