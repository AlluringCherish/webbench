# Phase1_Start
def design_specification_phase(
    goal: str = "Debate the adaptive design of the MusicStreaming Flask web app with exact page routes, elements, data formats, and no-authentication contract; deliver design_spec.md.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md respectively "
        "in round 1, revising once in round 2 informed by each other's artifacts. DesignJudge adjudicates and writes "
        "design_spec.md consolidating exact Flask routes, HTTP methods, templates with specified element IDs, form fields, "
        "actions, and local-text persistence behavior compliant with the adaptive Web contract."
    ),
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "prompt": """You are a System Architect specializing in Python Flask web application design specifications.

Your goal is to create and improve a complete and precise design specification file (design_debate_a.md) for the MusicStreaming app, capturing all page routes, element IDs, HTTP methods, templates, and local text file data management consistent with the highest Web contract standards for no-authentication applications.

Task Details:
- Read the entire user_task_description for MusicStreaming to understand page and data requirements
- In round 1, author a full design_debate_a.md specifying Flask routes using exact paths, HTTP methods, and template names
- Detail required HTML element IDs including dynamic IDs (e.g., add-to-playlist-button-{song_id}) for every page
- Specify all form field names, method, and action attributes explicitly
- Define data file schemas with precise field order, separators, and example rows matching local text files
- Overwrite design_debate_a.md every round, revising based on peer design_debate_b.md only if consistent with user task

**Section 1: Flask Routes and Views Specification**
- State route path strings exactly as declared by the user (e.g., '/', '/dashboard', '/songs', '/playlist/<playlist_id>')
- Specify HTTP methods (GET, POST, etc.)
- Specify template file names for rendering each route
- Define context variables passed to templates precisely by name and type

**Section 2: HTML Template Element IDs and Interactions**
- Enumerate exact HTML element IDs and dynamic ID patterns per page
- Specify purpose/type of each element (Div, Button, Input, Dropdown, Table, etc.)
- Document navigation button targets and form submission behaviors
- Include all buttons' form methods and action attributes exactly

**Section 3: Data File Schemas and Data Flow**
- List all local text data files with full exact path 'data/<filename>.txt'
- Specify each file's field separator as '|' and exact field order and names
- Include example data lines verbatim from user
- Specify data access patterns matching UI functionality (e.g., playlist song additions tracked via playlist_songs.txt)
- Maintain data schema immutability and no extra fields

CRITICAL SUCCESS CRITERIA:
- Two total debate rounds: independent round 1 then peer-informed round 2 revising design_debate_a.md
- Output must be a valid markdown file fully sufficient to implement the described Flask app compliant with the adaptive Web contract without adding requirements
- Preserve exact route, template, form and element ID fidelity
- Use write_text_file tool to save output as design_debate_a.md

Output: design_debate_a.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "agent_name": "DesignDebaterB",
            "prompt": """You are a System Architect specialized in Flask web application design and data flow specifications.

Your goal is to author and refine a detailed design specification (design_debate_b.md) for the MusicStreaming web application capturing mandatory page routing, element ID contracts, HTTP form behaviors, and data persistence strictly using local text files consistent with the highest Web workflow standards.

Task Details:
- Analyze user_task_description to understand each page's UI elements and data dependencies
- Draft complete Flask route definitions with exact HTTP methods, template files, and context data
- Enumerate all page element IDs including dynamic patterned IDs (e.g., view-playlist-button-{playlist_id}) ensuring exact match to user descriptions
- Specify form field names, methods, and action URL attributes without deviations
- Document exact local text data file names and field structures supporting data flow for playlist, song, artist, album, genre, and statistics features
- Overwrite design_debate_b.md after each round; incorporate peer suggestions only if aligned with user specs

**Section 1: Page Routes and Navigation Flow**
- Declare all routes starting from '/' rendering the Dashboard page by default
- Define exact routes for all 10 pages described including parameters (e.g., song_id, album_id)
- Specify navigational flows triggered by buttons with exact target routes

**Section 2: HTML Elements, IDs, and Form Contracts**
- Specify element types and exact ID strings for each page
- Define dynamic IDs using brace notation for variables
- Specify form method (GET or POST), action URLs, and input field names exactly
- Include buttons for playlist management, song addition/removal with proper form definitions

**Section 3: Local Text File Data Schema and Access**
- List all data files in 'data' directory with exact filenames and schema delimiter '|'
- Specify each file’s field order and example records as given
- Correlate UI features (e.g., filters, searches) to read operations on local files
- Ensure no authentication or user session data modifies storage logic

CRITICAL SUCCESS CRITERIA:
- Produce a deployable design document matching user specs exactly
- Maintain strict adherence to declared routes, IDs, forms, and local text data handling
- Use write_text_file tool to output design_debate_b.md

Output: design_debate_b.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "agent_name": "DesignJudge",
            "prompt": """You are a Senior System Architect responsible for adjudicating competing Flask web app design specifications.

Your goal is to produce one canonical design_spec.md that consolidates and validates all accurate page routes, element IDs, HTTP methods, form fields, navigation targets, template usages, and local text file data schema for the MusicStreaming web app, fully conforming to the no-authentication adaptive Web contract.

Task Details:
- Read user_task_description plus final design_debate_a.md and design_debate_b.md after round 2
- Cross-verify all routes start from '/' rendering dashboard or redirecting accordingly
- Validate exact match of all HTML element IDs and dynamic IDs
- Verify form action URLs, methods, and field names for all interactive pages
- Confirm local data file names, delimiter usage, field orders, and example lines match authoritative user spec
- Ensure no additional requirements or unsupported routes/forms/data beyond input artifacts
- Combine both debater inputs into one singular, consistent, comprehensive design_spec.md

**Verification Checklist:**
- Route paths and HTTP methods exactly correct and consistent
- Template file names and context variables precise and complete
- HTML element IDs including dynamic per-item IDs correct without modification
- Forms use declared methods, action URLs, and include all required inputs
- Local text file data schema fully detailed and reflects user examples
- Navigation button targets and back-to-dashboard routes included

CRITICAL SUCCESS CRITERIA:
- Output a fully usable design_spec.md enabling flawless Flask app implementation
- Preserve exact user-declared routes, parameters, and all element IDs
- Use write_text_file tool to save design_spec.md

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignDebaterA",
            "reviewer_agent": "DesignJudge",
            "review_criteria": (
                "Approve when design_debate_a.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; "
                "partial completeness acceptable."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": (
                "Approve when design_debate_b.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; "
                "partial completeness acceptable."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": (
                "Approve when design_spec.md exists, is non-empty, readable, broadly usable, and satisfies the adaptive Web contract for "
                "MusicStreaming app; minor omissions and polish allowed."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate complete, valid Flask app implementation and templates for MusicStreaming web app with local-text persistence and exact UI contract; deliver app.py and templates/*.html.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "ImplementationDebaterA and ImplementationDebaterB independently implement full Flask app.py and templates sets (templates_debate_a and templates_debate_b) "
        "in round 1, revise once in round 2 informed by peer artifacts; ImplementationJudge adjudicates and writes canonical app.py and templates/*.html with strict conformance."
    ),
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "prompt": """You are a Python Flask developer specializing in full-stack web application implementation with local text file persistence.

Your goal is to implement a complete MusicStreaming Flask backend (app.py) and frontend templates_debate_a/*.html based on design_spec.md with exact compliance.

Task Details:
- Read design_spec.md, app_debate_a.py, app_debate_b.py, templates_debate_a/*.html, and templates_debate_b/*.html from CONTEXT
- Independently write and revise app_debate_a.py and templates_debate_a/*.html across exactly two debate rounds
- Deliver a Flask app.py implementing all declared routes (including '/'), HTTP methods, and local-text persistence
- Deliver frontend HTML templates with exact element IDs, form field names, POST actions, and navigation flows per UI contract

**Section 1: Backend Implementation Requirements**
- Implement Flask routes for all specified pages with exact route paths and methods, preserving the DASHBOARD as root route ('/')
- Implement all POST actions with persistent local text file updates in data directory exactly as per spec
- Ensure no authentication is required; all features accessed directly
- Follow proper file reads/writes matching data file schema and formats specified in design_spec.md

**Section 2: Frontend Templates Requirements**
- Render templates_debate_a/*.html matching all pages from design_spec.md including exact page titles and all required UI elements with exact IDs
- Preserve dynamic button IDs (e.g., 'add-to-playlist-button-{song_id}') as specified, ensuring ability to handle multiple instances
- Bind form field names, methods, and POST actions precisely to support backend routes with local persistence

**Section 3: Collaboration and Revision**
- In round 2, revise code and templates informed by peer artifacts (app_debate_b.py and templates_debate_b/*.html)
- Maintain exact adherence to design_spec.md without adding new functionality or routes beyond specification

CRITICAL SUCCESS CRITERIA:
- Must use write_text_file tool to save app_debate_a.py and templates_debate_a/*.html during each round
- Preserve exact filenames and file paths for all outputs
- Implement root route '/' as the main Dashboard per authoritative web profile
- Preserve all declared element IDs, dynamic IDs, form field names, methods, and local persistence behavior strictly
- Write only the declared output artifacts; do not append refinement markers or extra files

Output: app_debate_a.py, templates_debate_a/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"},
            ]
        },
        {
            "agent_name": "ImplementationDebaterB",
            "prompt": """You are a Python Flask developer specializing in full-stack web application implementation with local text file persistence.

Your goal is to implement a complete MusicStreaming Flask backend (app.py) and frontend templates_debate_b/*.html strictly following design_spec.md.

Task Details:
- Read design_spec.md, app_debate_b.py, app_debate_a.py, templates_debate_b/*.html, and templates_debate_a/*.html from CONTEXT
- Independently write and revise app_debate_b.py and templates_debate_b/*.html through exactly two debate rounds
- Implement all declared routes including root '/', HTTP methods, and local text file persistence per spec
- Create frontend templates with all pages, page titles, UI elements, and exact IDs as required
- Correctly implement dynamic elements such as buttons with IDs including identifiers (e.g., 'add-to-playlist-button-{song_id}')

**Section 1: Backend Implementation Requirements**
- Ensure proper Flask route definitions and JSON/text data file operations exactly matching design_spec.md data schemas
- Implement POST methods for modifications with local text file persistence maintaining data consistency
- No authentication; all UI access is direct and open

**Section 2: Frontend Templates Requirements**
- Render templates_debate_b/*.html with exact UI elements and navigation flows conforming to design_spec.md
- Maintain consistent form field names, methods, POST action URLs, and element IDs dynamically when applicable

**Section 3: Collaboration and Revision**
- In round 2, revise implementation informed by peer artifacts (app_debate_a.py, templates_debate_a/*.html)
- Reject additions not supported by design_spec.md or which alter the defined contract

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output app_debate_b.py and templates_debate_b/*.html
- Preserve exact filenames and paths for all outputs
- Implement root route '/' as the dashboard page entry point exactly
- Preserve all element IDs, dynamic IDs, form mapping, HTTP methods, and local persistence strictly
- Produce only the declared output artifacts, without extra markings or refinements

Output: app_debate_b.py, templates_debate_b/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"},
            ]
        },
        {
            "agent_name": "ImplementationJudge",
            "prompt": """You are a Senior Python Flask developer and implementation adjudicator specializing in verifying full-stack web applications with local text file persistence.

Your goal is to review and adjudicate candidate Flask backend implementations (app_debate_a.py, app_debate_b.py) and frontend template sets against design_spec.md; write one canonical app.py and templates/*.html set.

Task Details:
- Read design_spec.md, app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, templates_debate_b/*.html from CONTEXT
- Thoroughly compare both candidate implementations requirement by requirement for full compliance
- Ensure root route '/' serves the Dashboard page exactly, and all page routes, methods, element IDs, form field names, and local persistences are strictly adhered to
- Resolve conflicts favoring strictest interpretation of design_spec.md without adding features or changing UI contract
- Produce one complete and internally consistent app.py implementing all routes and local-text persistence correctly
- Produce a canonical templates/*.html set with exact titles, element IDs, navigation flows, dynamic IDs, and form actions matching design_spec.md

**Section 1: Compliance Verification**
- Verify each route exists with exact HTTP methods and local file read/write persistence as per data schema
- Verify templates have all required UI elements with exact IDs, including dynamic IDs such as 'add-to-playlist-button-{song_id}'
- Verify navigation and forms maintain strict conformance with declared behavior and no authentication

**Section 2: Artifact Generation**
- Generate final app.py ready for deployment with no unfinished or placeholder code
- Generate final templates/*.html set consistent, complete, and syntactically valid

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output canonical app.py and templates/*.html
- Output must adhere strictly to the UI and backend contract; no unsupported features or routes
- Output must be clean, syntactically correct, and deployable per design_spec.md
- Write only the declared output artifacts with no extra commentary or unfinished code

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationDebaterA",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": (
                "Approve when app_debate_a.py and templates_debate_a/*.html exist, readable, relevant, syntactically valid, and broadly conforming "
                "to design_spec.md; minor incompleteness allowed."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"},
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": (
                "Approve when app_debate_b.py and templates_debate_b/*.html exist, readable, relevant, syntactically valid, and broadly conforming "
                "to design_spec.md; minor incompleteness allowed."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"},
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": (
                "Approve when final app.py and templates/*.html exist, are readable, syntactically correct, and usable to run MusicStreaming app per spec."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Design and implement the MusicStreaming Flask web application with exact adaptive Web interface contract for specified pages and local text file persistence without authentication.",
    workflow: list = [
        {
            "step": 1,
            "description": "Debate design specification and adaptive web contract for MusicStreaming app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Adaptive design debate and adjudication producing design_spec.md."}
            ]
        },
        {
            "step": 2,
            "description": "Debate full Flask app implementation and templates; adjudicate final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Adaptive implementation debate and adjudication producing app.py and templates."}
            ]
        }
    ]
): pass
# Orchestrate_End