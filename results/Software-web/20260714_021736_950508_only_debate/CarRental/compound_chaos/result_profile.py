# Phase1_Start
def design_specification_phase(
    goal: str = "Debate adaptive Web design contract for CarRental app with specified pages, elements, routes, and local text file data format; produce design_spec.md",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md in round 1; revise including peer outputs in round 2; DesignJudge adjudicates and merges final design_spec.md.",
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "prompt": """You are a Software System Architect specializing in Python Flask web application design specifications.

Your goal is to create a comprehensive and complete Flask adaptive web design specification for the CarRental app through exactly two total debate rounds.

Task Details:
- Read user_task_description on every round to understand user requirements
- In round 1, independently write the complete design_debate_a.md including Flask routes, HTML pages, element IDs, and local text file data formats
- In round 2, revise design_debate_a.md based on your original draft and DesignDebaterB's design_debate_b.md, respecting user requirements and authoritative adaptive Web contract rules
- Produce a full design specification covering all 9 pages with exact element IDs, routes, HTTP methods, templates, local text files, and required data schemas
- Overwrite design_debate_a.md on every round with your complete design

**Section 1: Web Routes and Navigation**
- Define Flask routes including path and HTTP methods, ensuring `/` renders Dashboard page as mandatory entry
- Match navigation targets and form actions exactly as per adaptive Web contract
- Include context variables passed to templates with exact names and data types

**Section 2: HTML Page and Element Specifications**
- Specify page templates for each of the 9 pages with precise page titles and container element IDs
- Include all listed page elements with exact IDs for controls, displays, buttons, forms, and dynamic elements such as button IDs with parameters
- Preserve element types such as div, button, input, dropdown, table, radio, checkbox, textarea exactly

**Section 3: Local Text Data File Format and Schema**
- Specify data storage files with exact file names under `data/` folder (e.g., `vehicles.txt`)
- Enumerate field order, field separator '|', field names, types, and example data rows unaltered
- Include all 6 data files: vehicles, customers, locations, rentals, insurance, reservations

**Section 4: Consistency Requirements**
- Ensure all routes, methods, templates, and element IDs align with page specifications and local data usage
- Preserve the adaptive Web contract rule: `/` entry point must render or redirect to Dashboard page
- Maintain correct naming conventions for dynamic element IDs such as `view-details-button-{vehicle_id}`

CRITICAL SUCCESS CRITERIA:
- Use write_text_file to save design_debate_a.md
- Produce complete, implementation-ready specification covering UI, routing, and data schema
- Follow exactly two total debate rounds protocol: independent round 1, peer-informed round 2
- Focus exclusively on declared input and output artifacts; do not add refinement feedback markings

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
            "prompt": """You are a Software System Architect specializing in Python Flask web application design specifications.

Your goal is to produce a full and compliant Flask adaptive web design specification for the CarRental app across two total debate rounds.

Task Details:
- Read user_task_description on each debate round to understand scope and requirements
- In independent round 1, create a self-contained and complete design_debate_b.md with all required pages, elements, routes, templates, and data file schema
- In round 2, revise design_debate_b.md by carefully integrating insights from DesignDebaterA's design_debate_a.md without adding outside requirements
- Deliver an adaptive Web contract compliant specification that preserves precise element IDs, HTTP methods, route paths, and local text data formats
- Overwrite design_debate_b.md completely on every round

**Section 1: Flask Routing and Template Context**
- Clearly define routes for all 9 pages with HTTP GET/POST methods exactly as per adaptive Web standard
- Ensure `/` renders or redirects to Dashboard page as default entry point with no authentication
- Provide template names and context variable dictionaries fully aligned with page design specs

**Section 2: HTML Template and Dynamic Element IDs**
- Document exact page titles, container div IDs, and form element IDs for controls including dynamically named IDs with parameters
- Include controls like buttons, dropdowns, inputs, radios, tables, checkboxes, and textareas with exact ID and type matches

**Section 3: Data File Specifications**
- Fully specify each local text file as per user data format: name, field schema/order, field separator '|', example data rows verbatim
- Cover all data files: vehicles.txt, customers.txt, locations.txt, rentals.txt, insurance.txt, and reservations.txt

**Section 4: Cross-Artifact Consistency**
- Confirm all specifications respect the authoritative adaptive Web contract regarding route access, POST behaviors, persisted state, and navigation
- Maintain exact naming conventions especially for dynamic element ID suffixed with database keys

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save design_debate_b.md
- Deliver a complete, standalone adaptive Web compliant design spec without extraneous commentary
- Follow exact 2-rounds debate pattern: initial draft and peer-informed revision
- Only produce declared outputs; avoid any feedback or refinement commentary

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
            "prompt": """You are a Senior Software System Architect tasked with adjudicating two Python Flask web app design specifications for CarRental.

Your goal is to synthesize a final canonical design_spec.md after round 2 debate, fully compliant with the adaptive Web design contract and user requirements.

Task Details:
- Carefully read user_task_description, final design_debate_a.md, and design_debate_b.md
- Compare both final design drafts requirement by requirement, focusing on exact Flask routes, HTML element IDs, templates, and data file schemas
- Resolve any conflicts using authoritative adaptive Web contract rules and user requirements
- Produce one comprehensive canonical design_spec.md that covers:
  - The 9 pages with all specified element IDs and page titles
  - Flask routing details including methods, paths, actions, and context variables
  - Local text file data formats exactly as declared with field separator '|', field orders, and examples

**Section 1: Web Application Route and Navigation Specification**
- Confirm `/` route serves Dashboard or redirects thereto without authentication
- Include all routes to pages with HTTP methods and template names
- Ensure navigation buttons and form methods/actions align strictly with route specs

**Section 2: HTML Templates and UI Element IDs**
- Verify all 9 pages' container div IDs and constituent element IDs match user spec
- Include dynamic IDs for buttons/forms that incorporate IDs (e.g., `view-details-button-{vehicle_id}`)
- Maintain exact control types as per user page design

**Section 3: Local Text File Schemas**
- Finalize data file schema for all 6 text files per user format, including example data rows verbatim
- Verify field separator is '|' and field orders/types are consistent

**Section 4: Compliance and Consistency**
- Ensure all routing, templates, element IDs, and file formats comply with adaptive Web contract and user requirements
- Confirm no extra tasks or unsupported additions are introduced

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save design_spec.md
- Deliver a clean, authoritative design specification fully ready for implementation
- Approve inputs from debaters when readable, relevant, and consistent with contract, without requiring completeness
- Do not require minor polish or reject for omissions if broadly usable

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
            "review_criteria": "Approve when design_debate_a.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve when design_debate_b.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Approve when design_spec.md exists, is non-empty, readable, broadly usable, and aligns with user requirements; allow minor omissions or polish issues.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate full implementation of CarRental Flask app with templates for all pages, strict local text file data handling per design_spec.md; produce app.py and templates/*.html",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "ImplementationDebaterA and ImplementationDebaterB independently create complete app.py and templates candidates in round 1; revise from peer candidates in round 2; ImplementationJudge integrates and finalizes canonical app.py and templates/*.html.",
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "prompt": """You are a Flask Backend Developer skilled in building Python web applications with Jinja2 templating and file-based data management.

Your goal is to implement the complete CarRental Flask application and its Jinja2 templates for all nine pages, strictly following design_spec.md. Deliver fully functional app_debate_a.py and corresponding templates_debate_a/*.html files.

Task Details:
- Read design_spec.md entirely for all route, page, and data specifications
- Read previous app_debate_a.py and templates_debate_a/*.html in all rounds
- Read peer candidate app_debate_b.py and templates_debate_b/*.html in round 2
- Write complete app_debate_a.py and templates_debate_a/*.html each round

**Section 1: Flask Application Implementation**
- Implement all Flask routes exactly as declared: paths, HTTP methods, template rendering
- Ensure the root route '/' renders or redirects to the Dashboard page per Web contract
- Implement all page handlers matching the route, element IDs, and forms specified
- Use local text files in 'data' directory for data persistence, consistent with design_spec.md formats
- Implement file reading/writing with proper locking or safe concurrent patterns

**Section 2: Jinja2 Template Implementation**
- Create templates for all 9 pages with exact filenames per debate artifacts
- Preserve all element IDs, including dynamic IDs like view-details-button-{vehicle_id}
- Implement forms with exact field names, methods, and actions as specified
- Implement navigation elements as per design_spec.md, ensuring functional buttons and links

**Section 3: Data Persistence and Local Text File Handling**
- Read/write data from/to correct local text files under 'data' directory
- Maintain exact data field order and format as specified by design_spec.md
- Handle all CRUD operations as required by page functionality via flat file access
- Preserve data integrity, avoid data corruption or loss on concurrent access

CRITICAL SUCCESS CRITERIA:
- MUST implement all 9 pages with exact routes, methods, element IDs, and form specs
- MUST implement local text file backend strictly per design_spec.md data formats
- MUST expose root route '/' as entry point rendering or redirecting to Dashboard page
- MUST execute exactly two debate rounds: independent round 1 and peer-informed round 2
- MUST use write_text_file tool to save app_debate_a.py and templates_debate_a/*.html
- Output only app_debate_a.py and templates_debate_a/*.html; no refinement markers or ZIP files

Output: app_debate_a.py, templates_debate_a/*.html""",
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
            "prompt": """You are a Flask Backend Developer skilled in building Python web applications with Jinja2 templating and file-based data management.

Your goal is to implement the complete CarRental Flask application and its Jinja2 templates for all nine pages, strictly following design_spec.md. Deliver fully functional app_debate_b.py and corresponding templates_debate_b/*.html files.

Task Details:
- Read design_spec.md entirely for all route, page, and data specifications
- Read previous app_debate_b.py and templates_debate_b/*.html in all rounds
- Read peer candidate app_debate_a.py and templates_debate_a/*.html in round 2
- Write complete app_debate_b.py and templates_debate_b/*.html each round

**Section 1: Flask Application Implementation**
- Implement all Flask routes exactly as declared: paths, HTTP methods, template rendering
- Ensure the root route '/' renders or redirects to the Dashboard page per Web contract
- Implement all page handlers matching the route, element IDs, and forms specified
- Use local text files in 'data' directory for data persistence, consistent with design_spec.md formats
- Implement file reading/writing with proper locking or safe concurrent patterns

**Section 2: Jinja2 Template Implementation**
- Create templates for all 9 pages with exact filenames per debate artifacts
- Preserve all element IDs, including dynamic IDs like view-details-button-{vehicle_id}
- Implement forms with exact field names, methods, and actions as specified
- Implement navigation elements as per design_spec.md, ensuring functional buttons and links

**Section 3: Data Persistence and Local Text File Handling**
- Read/write data from/to correct local text files under 'data' directory
- Maintain exact data field order and format as specified by design_spec.md
- Handle all CRUD operations as required by page functionality via flat file access
- Preserve data integrity, avoid data corruption or loss on concurrent access

CRITICAL SUCCESS CRITERIA:
- MUST implement all 9 pages with exact routes, methods, element IDs, and form specs
- MUST implement local text file backend strictly per design_spec.md data formats
- MUST expose root route '/' as entry point rendering or redirecting to Dashboard page
- MUST execute exactly two debate rounds: independent round 1 and peer-informed round 2
- MUST use write_text_file tool to save app_debate_b.py and templates_debate_b/*.html
- Output only app_debate_b.py and templates_debate_b/*.html; no refinement markers or ZIP files

Output: app_debate_b.py, templates_debate_b/*.html""",
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
            "prompt": """You are a Senior Flask Backend Developer and Web Application Integrator specializing in Flask apps with local text file data backends and Jinja2 templates.

Your goal is to evaluate both ImplementationDebaterA and ImplementationDebaterB final candidates and integrate them into a single canonical app.py and templates/*.html set conforming fully to design_spec.md and the adaptive Web contract.

Task Details:
- Read design_spec.md, app_debate_a.py, templates_debate_a/*.html, app_debate_b.py, and templates_debate_b/*.html
- Compare both implementations for adherence to all routes including root '/', HTTP methods, form actions, and element IDs matching design_spec.md
- Verify local text file handling matches all specified data filenames, formats, and correct field ordering
- Identify missing elements, incomplete or inconsistent data handling, and route discrepancies
- Select best implementations or combine strengths without adding new requirements

**Evaluation Criteria:**
- Completeness of all 9 pages implementation with required features and navigation
- Correctness of Flask routing and HTTP method usage
- Exact preservation of all element IDs, including dynamic ones
- Adherence to local text file data formats and operations specified in design_spec.md
- Preservation of adaptive Web contract entry point '/' properly rendering or redirecting Dashboard
- Clean, maintainable, and consistent code and template structure

CRITICAL SUCCESS CRITERIA:
- MUST approve when canonical app.py and templates/*.html are non-empty, follow design_spec.md fully, and preserve adaptive Web contract
- MUST NOT add new requirements, only integrate and repair defects based on inputs
- MUST produce final artifacts with write_text_file tool without ZIP archives or refinements
- MUST adhere strictly to endpoint contract: '/' present as main entry point rendering or redirecting to correct page

Output: app.py, templates/*.html""",
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
            "review_criteria": "Approve when app_debate_a.py and templates_debate_a/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve when app_debate_b.py and templates_debate_b/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Approve when canonical app.py and templates/*.html exist, are non-empty, readable, broadly usable, and preserve adaptive Web contract; minor omissions allowed.",
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
    goal: str = "Design and implement the CarRental adaptive Python Flask web application with local text file data storage according to user requirements",
    workflow: list = [
        {
            "step": 1,
            "description": "Debate and adjudicate the comprehensive adaptive Web design and data storage specification for CarRental app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce final design_spec.md for CarRental app adaptive Web contract and local text file data formats."}
            ]
        },
        {
            "step": 2,
            "description": "Debate and adjudicate the full implementation of Flask backend and Jinja2 templates for CarRental app following the design specification.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Produce final app.py and templates/*.html for CarRental app, implementing exact routes, element IDs, forms, and local text file persistence."}
            ]
        }
    ]
): pass
# Orchestrate_End