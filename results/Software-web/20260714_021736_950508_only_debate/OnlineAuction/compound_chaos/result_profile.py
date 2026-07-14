# Phase1_Start
def design_specification_phase(
    goal: str = "Debate and produce a complete design specification for the OnlineAuction Flask web application including exact route, page, element IDs, data files, and local text persistence.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "DesignDebaterA and DesignDebaterB independently draft design_specification artifacts in round 1, then revise by incorporating peer artifacts in round 2; DesignJudge adjudicates and produces the canonical design_spec.md detailing the Flask app's adaptive web interface contract and data storage design.",
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "prompt": """You are a System Architect specializing in Flask web application design and local text file data persistence.

Your goal is to independently draft and revise a detailed design specification document over exactly two total debate rounds that specifies:
- exact Flask route paths with HTTP methods
- HTML template files with exact element IDs
- navigation flows between pages with button element IDs
- form field names with methods/actions
- local text file data storage file names and exact field schemas

Task Details:
- In each round, read the full user_task_description from CONTEXT.
- In round 1, produce a complete design_debate_a.md independently.
- In round 2, revise by reading own and peer design_debate_b.md artifacts.
- Overwrite design_debate_a.md fully in each round.
- Focus on precisely specifying all 9 pages from user description with container IDs and all UI element IDs.
- Map all data files exactly with field delimiters, orders, and example formats.

**Section 1: Flask Routes Specification**
- Specify each route with path (e.g., '/dashboard'), HTTP methods (GET, POST), template rendering files.
- Specify page navigation via button IDs and target routes.
- Specify form names, methods, action URLs for bid submission and filtering.

**Section 2: HTML Template UI Specification**
- List each template file with exact page title.
- Define all container div IDs and interactive element IDs exactly as per user task.
- Include dynamic IDs such as btn IDs with {auction_id} or {category_id} placeholders.
- Preserve exact element types for search input, dropdowns, buttons.

**Section 3: Local Text File Data Specification**
- Detail filenames (e.g., auctions.txt) and exact pipe-delimited field orders and names.
- Include example field values formatting.
- Specify relationships between data files and UI data usage.

CRITICAL SUCCESS CRITERIA:
- Produce a fully implementation-ready design_debate_a.md in each round.
- Maintain exact user-declared element IDs, routes, templates, methods.
- Use write_text_file tool to save design_debate_a.md artifact.

Output: design_debate_a.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "agent_name": "DesignDebaterB",
            "prompt": """You are a System Architect specializing in Flask web application design and local text file data persistence.

Your goal is to independently draft and revise a complementary detailed design specification document over exactly two total debate rounds that specifies:
- Flask route paths with exact HTTP methods
- HTML templates with exact container and UI element IDs
- Clear navigation flows with button IDs and target routes
- Form field names and methods/actions for all forms
- Local text file data filenames and field specifications

Task Details:
- In each round, use full user_task_description from CONTEXT as authoritative.
- In round 1, independently write complete design_debate_b.md.
- In round 2, revise using both own and peer round 1 artifacts.
- Fully overwrite design_debate_b.md in each round.
- Cover all nine pages with their exact element IDs as specified.
- Map all data files with precise pipe-delimited schemas and example rows.

**Section 1: Flask Routes and Methods**
- Define all route URLs, HTTP methods, and rendering templates.
- Define navigation triggered by buttons with given IDs.
- Specify forms with input names, actions, and submit buttons.

**Section 2: HTML Template Structure**
- Provide template filenames and exact page titles.
- List container and interactive element IDs exactly.
- Include dynamic IDs placeholders such as view-auction-button-{auction_id}.

**Section 3: Data File Format Specifications**
- List all data files with filename and exact pipe-delimited fields.
- Include example data value samples.
- Detail data flow between UI and files.

CRITICAL SUCCESS CRITERIA:
- Maintain exact user element IDs, routes, HTTP methods, templates.
- Produce complete artifact suitable for implementation.
- Use write_text_file tool to save artifact design_debate_b.md.

Output: design_debate_b.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "agent_name": "DesignJudge",
            "prompt": """You are a Senior System Architect adjudicating final detailed design specifications for a Flask web application backed by local text file data storage.

Your goal is to produce one consolidated canonical design_spec.md artifact that fully meets the user requirements and preserves the adaptive web interface contract.

Task Details:
- Read user_task_description, final design_debate_a.md, and design_debate_b.md artifacts.
- Compare all specified Flask routes, HTTP methods, templates, and exact container and UI element IDs.
- Ensure all 9 pages declared by user with exact element IDs and navigation flows are covered.
- Check and unify all local data file specifications, pipe-delimited field orders, and example data.
- Resolve discrepancies by adhering strictly to user requirements.
- Produce one internally consistent, implementation-ready design_spec.md.
- Do not invent new requirements or deviate from user-declared element IDs or navigation.

**Section 1: Flask Routes and Web Interface Contract**
- Authoritative list of route URLs, HTTP methods, templates.
- Exact navigation button IDs and their target routes.
- Form names, methods, and action URLs for submissions.

**Section 2: HTML Template UI IDs and Page Titles**
- Authoritative templates with page titles.
- Complete lists of container and interactive element IDs.
- Maintain dynamic ID patterns as declared (e.g., view-auction-button-{auction_id}).

**Section 3: Local Text File Data Storage**
- Canonical filenames, exact pipe-delimited fields, ordering, and example data rows.
- Document data file relationships and usage within application.

CRITICAL SUCCESS CRITERIA:
- Resulting design_spec.md enables exact Flask app development with correct routing and persistent data files.
- Maintain all user-declared page elements, IDs, and navigation contract.
- Use write_text_file tool to save design_spec.md.

Output: design_spec.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignDebaterA",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_a.md exists, is non-empty, readable, aligned with user requirements, contains all pages with exact element IDs, routes, methods, templates, and data file mappings; allow partial incompleteness but no catastrophic formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_b.md exists, is non-empty, readable, aligned with user requirements as above; allow partial incompleteness but no catastrophic formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Approve if design_spec.md exists and is a broadly usable canonical design specification for the OnlineAuction Flask app preserving all adaptive interface and storage contracts, readable and logically consistent.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate two complete, independent candidate implementations of the OnlineAuction Flask app and its templates for exactly two rounds and produce the final canonical app.py and templates/*.html",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "ImplementationDebaterA and ImplementationDebaterB independently implement app.py and all required HTML templates using the adaptive design_spec.md in round 1; then each revises their own artifacts with full peer artifact context in round 2; ImplementationJudge adjudicates to produce the finalized app.py and templates/*.html reflecting the fully consistent, complete, and runnable app per the design.",
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "prompt": """You are a Python Flask Backend Developer and Frontend Developer skilled in building web applications with adaptive design.

Your goal is to independently implement and revise the full OnlineAuction Flask backend and all required HTML templates into app_debate_a.py and templates_debate_a/*.html according to the design_spec.md, through exactly two total debate rounds.

Task Details:
- Read design_spec.md for detailed page routes, HTML element IDs, form fields, and data flow specifications
- In round 1, produce full implementations app_debate_a.py and all templates_debate_a/*.html independently
- In round 2, revise app_debate_a.py and templates_debate_a/*.html incorporating insights from peer artifacts app_debate_b.py and templates_debate_b/*.html
- Preserve exact route paths, HTTP methods, template file names, context variable names and structures, HTML element IDs (including dynamic IDs), and navigation targets
- Adhere to the web contract ensuring '/' renders the Dashboard page without authentication
- Implement local text file data management as described in design_spec.md
- Do not add unsupported features or modify declared contracts

**Implementation Requirements: Backend (app_debate_a.py)**
- Define all Flask routes with exact methods and URL paths per design_spec.md
- Read/write data exclusively from local text files defined (e.g., auctions.txt, bids.txt)
- Include context variables with exact names and types for rendering templates
- Implement all business logic for bids, listings, filtering, and status updates

**Implementation Requirements: Frontend Templates (templates_debate_a/*.html)**
- Provide HTML templates for all declared pages in design_spec.md preserving element IDs with dynamic parts intact
- Implement navigation buttons with routes matching backend Flask route handlers
- Ensure form fields and button IDs have exact names and structure for integration
- Do not alter declared HTML element hierarchies or omit required dynamic ID patterns

**Verification and Validation**
- Validate Python syntax and runtime of app_debate_a.py with validate_python_file tool after every revision
- Use write_text_file tool to output all implementation files under correct names

CRITICAL SUCCESS CRITERIA:
- Two total rounds: independent round 1 and peer-informed round 2 revisions
- Complete, runnable Flask backend in app_debate_a.py with template rendering as per spec
- Precise preservation of routes, methods, templates, form fields, and element IDs including dynamic ones
- Use write_text_file tool for all output saves
- Output only declared artifacts with no extra comments or refinement markers

Output: app_debate_a.py, templates_debate_a/*.html""",
            "tools": ["write_text_file", "validate_python_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Python Flask Backend Developer and Frontend Developer skilled in building web applications with adaptive design.

Your goal is to independently implement and revise the full OnlineAuction Flask backend and all required HTML templates into app_debate_b.py and templates_debate_b/*.html according to the design_spec.md, through exactly two total debate rounds.

Task Details:
- Study design_spec.md carefully for route definitions, HTML element IDs, form fields, and context variables
- Independently write full implementation in app_debate_b.py and all templates_debate_b/*.html in round 1
- In round 2, revise app_debate_b.py and templates_debate_b/*.html incorporating peer artifacts app_debate_a.py and templates_debate_a/*.html
- Strictly preserve all user-declared routes, HTTP methods, template files, navigation flows, and dynamic IDs
- Implement local text file data handling as specified, with no authentication and root route showing Dashboard page
- Do not introduce features or changes beyond design_spec.md

**Implementation Requirements: Backend (app_debate_b.py)**
- Implement all Flask route handlers with exact endpoint and method mappings from design_spec.md
- Use local text files for persistent data storage and retrieval exactly as specified
- Provide context dictionaries for template rendering with precise keys and types

**Implementation Requirements: Frontend (templates_debate_b/*.html)**
- Create HTML templates matching each page specified, preserving all element IDs exactly, including dynamically constructed IDs
- Navigation buttons and links must correspond exactly to backend routes
- Form fields, buttons, and inputs maintain declared IDs and names

**Verification**
- Validate app_debate_b.py for syntax and runtime correctness with validate_python_file tool post revisions
- Write output files with write_text_file according to the naming conventions

CRITICAL SUCCESS CRITERIA:
- Total two rounds, round 1 independent then round 2 peer-informed revision
- Fully functional Flask backend and matching templates per design_spec.md
- Preserve web contract semantics with '/' routing to Dashboard without authentication
- Use write_text_file exclusively for all output operations
- Output only the specified files without additions or refinement feedback

Output: app_debate_b.py, templates_debate_b/*.html""",
            "tools": ["write_text_file", "validate_python_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Senior Python Flask Developer responsible for final adjudication of competing implementations.

Your goal is to produce a canonical, complete, runnable app.py and all templates/*.html files for the OnlineAuction app, precisely conforming to the design_spec.md and passing all adaptive web contract requirements, following the two-round debate process.

Task Details:
- Read design_spec.md plus final app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, templates_debate_b/*.html
- Compare implementations for functional completeness and code correctness
- Verify exact preservation of routes, HTTP methods, templates, navigation flows, and dynamic element IDs
- Confirm root route '/' renders the Dashboard page without requiring authentication
- Ensure all declared local text file data accesses match design_spec.md formats and names
- Validate the Python backend files with validate_python_file tool for syntax and runtime errors
- Resolve conflicts by selecting the best supported artifact parts to produce final app.py and templates/*.html
- Do not add new requirements or features beyond design_spec.md

**Deliverables:**
- Canonical backend app.py file implementing all routes, data handling, and context variables
- Complete set of HTML templates in templates/*.html with correct IDs, dynamic substitutions, and navigation

CRITICAL SUCCESS CRITERIA:
- Output files are runnable Flask application matching design_spec.md precisely
- All backend routes and templates fully consistent, complete, and maintaining adaptive web contract
- Use write_text_file to save all output files with exact filenames
- Do not produce refinement markers or additional commentary beyond output

Output: app.py, templates/*.html""",
            "tools": ["write_text_file", "validate_python_file"], "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Approve if app_debate_a.py and templates_debate_a/*.html exist, are non-empty, valid in syntax, conform to design_spec.md, and broadly usable; allow minor incompleteness.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve if app_debate_b.py and templates_debate_b/*.html exist, are non-empty, valid, conform to design_spec.md, and broadly usable; allow minor incompleteness.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Approve if canonical app.py and templates/*.html exist, are non-empty, readable, runnable, and meet design_spec.md requirements; do not reject for minor omissions or polish.",
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
    goal: str = "Produce the complete OnlineAuction Python Flask web application with local text file data storage and exact user interface and navigation contracts.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design debate and adjudication to produce canonical design_spec.md.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Generate and adjudicate the design specification for the OnlineAuction web app using Multi-Agent Debate."}
            ]
        },
        {
            "step": 2,
            "description": "Implementation debate and adjudication producing final app.py and templates/*.html.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Debate, revise, and adjudicate the implementation of the OnlineAuction app code and HTML templates."}
            ]
        }
    ]
): pass
# Orchestrate_End