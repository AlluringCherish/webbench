# Phase1_Start
def design_specification_phase(
    goal: str = "Debate and finalize a comprehensive adaptive design_spec.md for the TravelPlanner Flask web application with exact page routes, method contracts, element IDs, and data storage formats.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "DesignDebaterA and DesignDebaterB independently draft their candidate design_spec.md documents in round 1 based on user requirements, "
        "then each revises their documents in round 2 by incorporating or rebutting peer artifacts. DesignJudge adjudicates and synthesizes the final "
        "design_spec.md reflecting the adaptive Web Contract and user requirements."
    ),
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "prompt": """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and revise a complete design_spec.md for the TravelPlanner web app through exactly two debate rounds.

Task Details:
- Read the entire user_task_description in every round for design context
- In round 1, independently draft design_debate_a.md covering Flask route mappings, HTTP methods, template files, and exact element IDs for all TravelPlanner pages
- In round 2, revise design_debate_a.md by reading the input design_debate_a.md and peer design_debate_b.md, integrating valid peer improvements or rebuttals
- Output a complete, implementation-ready design_debate_a.md after each round

**Section 1: Flask Routes and HTTP Methods**
- Specify each route path exactly as in the User Task
- Define the HTTP methods allowed (GET, POST, etc.) with correct forms and actions
- Explicitly mark the route for root '/' as entry rendering Dashboard page

**Section 2: Template Files and HTML Elements**
- List precise template filenames per page
- Define all element IDs including dynamic IDs exactly as declared (e.g., view-destination-button-{dest_id})
- Describe page titles and navigation button routes

**Section 3: Data Storage File Formats**
- Specify all local text file names and exact data formats with field order, delimiters, and example rows
- Do not invent data files beyond user specification

CRITICAL SUCCESS CRITERIA:
- Must strictly preserve all user-declared routes, methods, template names, and element IDs
- Produce a design document fully consistent with user requirements and peer feedback after round 2
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
            "prompt": """You are a Software Architect specializing in Flask web application design specifications.

Your goal is to produce and refine a comprehensive design_spec.md for the TravelPlanner app in exactly two debate rounds.

Task Details:
- Thoroughly review user_task_description in every round to understand the app workflow
- Independently write design_debate_b.md in round 1 focusing on route definitions, data persistence behavior, template filenames, and exact HTML element IDs for all pages
- In round 2, read the round 1 artifact and the peer's final design_debate_a.md, revising your design_debate_b.md to address peer points supported by user requirements
- Overwrite and submit the complete design_debate_b.md after each round

**Section 1: Route and URL Structure**
- Define exact route paths and navigation targets, including root '/' redirecting or rendering Dashboard page
- Specify HTTP methods and form action attributes exactly as required

**Section 2: Template and HTML Element Details**
- Provide exact template filenames as used in the application
- Enumerate all HTML element IDs including dynamic patterns like view-package-details-button-{pkg_id}
- Maintain exact consistency of element IDs and navigation button targets

**Section 3: Local Text Data Persistence**
- Define all data files used with exact file names and delineate their content schema with fields and delimiters
- Describe the reading and writing behavior tied to each data file without adding unsupported files

CRITICAL SUCCESS CRITERIA:
- Preserve all user-specified exact routes, methods, templates, and element IDs without deviation
- Produce a clear, consistent, and complete design after two rounds integrating pertinent peer corrections
- Use write_text_file tool to save output as design_debate_b.md

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
            "prompt": """You are a Senior System Architect adjudicating two competing design specifications for a Flask web application.

Your goal is to produce a final canonical design_spec.md fully aligned to the TravelPlanner user requirements and the adaptive Web Contract after the two debate rounds.

Task Details:
- Carefully read user_task_description, final design_debate_a.md, and final design_debate_b.md
- Compare every route, method, template, and element ID across both final debater artifacts
- Validate complete coverage of all pages and local text data files as per user requirements
- Resolve any conflicts by strictly adhering to user specifications and preserving exact route paths, HTTP methods, template file names, and element IDs
- Compile a consistent, authoritative design_spec.md without introducing new requirements or deviations

**Section 1: Routes and Methods**
- Verify root '/' route renders or redirects to Dashboard page exactly
- Confirm all declared routes, methods, and form actions are specified verbatim

**Section 2: Template Filenames and HTML Elements**
- Include all template filenames and exact HTML element IDs per page including dynamic ID patterns
- Ensure navigation button targets and page titles are exactly aligned

**Section 3: Data File Formats and Persistence**
- Synthesize precise data file names, formats, field orders, delimiters, and example data from both candidates
- Confirm local text file data persistence matches user description exactly

CRITICAL SUCCESS CRITERIA:
- Output a comprehensive, exact design_spec.md suitable for implementation directly from this canonical design
- Use write_text_file tool to save design_spec.md
- Ensure all user requirements are met with perfect data integrity, no omitted elements or routes, and no added properties

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
            "review_criteria": "Approve if design_debate_a.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_b.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Approve if design_spec.md exists, is non-empty, broadly usable, well-structured, and sufficient for implementation without minor omissions.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate complete implementation bundles of app.py and templates/*.html for the TravelPlanner Flask application with exact adaptive web contract compliance and local text data management, then finalize canonical artifacts.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "ImplementationDebaterA and ImplementationDebaterB independently create complete app.py source and all required HTML templates in separate directories in round 1, "
        "revise once from peer artifacts in round 2, and ImplementationJudge adjudicates and combines them into canonical app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "prompt": """You are a Backend Web Developer specializing in Flask applications with local text file data management.

Your goal is to implement a complete Flask backend along with all frontend HTML templates, strictly following the adaptive Web interface contract and the design_spec.md reference, producing full application bundles independently and then revising with peer feedback.

Task Details:
- Read design_spec.md and both your own and peer's app.py and templates artifact sets for each round.
- Independently draft entire app_debate_a.py and all templates_debate_a/*.html in round 1.
- Revise app_debate_a.py and templates_debate_a/*.html after peer-informed round 2 incorporating supported corrections.
- Output exact element IDs, page titles, route paths, HTTP methods, form actions, and local text file data handling per design_spec.md.
- Ensure the root route (/) renders or redirects to the Dashboard page without authentication.
- Preserve local text file read/write consistency with declared data file formats and names.

**Implementation Requirements: Backend (app.py)**
- Use Flask framework routes and views.
- Implement data handling using local text files under 'data' directory with correct parsing and updates.
- Implement all declared pages and routes with exact context variables.
- Maintain precise HTTP methods and form action URLs.
- Handle data validation and error conditions gracefully.

**Implementation Requirements: Frontend Templates**
- Create all HTML templates under templates_debate_a/ with exact filenames and element IDs as specified.
- Templates must include the declared distinct elements like div IDs, input names, button IDs, dropdowns referencing design_spec.md exactly.
- Navigation buttons trigger Flask routes as declared.
- Include form fields with declared names and methods enforcing contract.

**Coding and Collaboration**
- Use 'write_text_file' tool to save all source files.
- Use 'validate_python_file' tool to ensure syntax and runtime correctness for app_debate_a.py.
- Retain full completeness and reject unsupported peer additions during revision round.

CRITICAL REQUIREMENTS:
- MUST write and update app_debate_a.py and templates_debate_a/*.html only.
- MUST preserve all exact element IDs, routes, methods, and local data format handling.
- MUST follow the adaptive Web contract preserving '/' as dashboard entry point.
- Use only declared outputs; do not add refinement markers or extra files.

Output: app_debate_a.py, templates_debate_a/*.html""",
            "tools": ["write_text_file", "validate_python_file"],
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
            "prompt": """You are a Backend Web Developer specializing in Flask applications with local text file data management.

Your goal is to independently implement a full Flask backend and related frontend HTML templates based on design_spec.md with adherence to the adaptive Web interface contract, then revise your implementation after peer review.

Task Details:
- In each round, read the user design_spec.md plus your own and your peer's app.py and templates artifacts.
- In round 1, author a full app_debate_b.py and templates_debate_b/*.html independently.
- In round 2, revise app_debate_b.py and templates_debate_b/*.html incorporating peer-informed corrections consistent with design_spec.md.
- Follow all declared page routes, HTTP methods, form actions, element IDs, navigation, and local text data management exactly.
- Ensure '/' route serves or redirects to Dashboard page as per web contract.
- Maintain strict data handling from text files with exact formats given.

**Implementation Requirements: Backend (app.py)**
- Flask routes for all pages and features with precise context variables.
- Read and write all text data files under 'data' directory conforming to the provided schemas.
- Handle all forms with correct POST/GET methods and data validation.

**Implementation Requirements: Frontend Templates**
- Full HTML templates in templates_debate_b/ directory with exact element IDs, input names, and buttons per design_spec.md.
- Implement navigation consistent with backend routes and contract.
- Include buttons and inputs with exact names, IDs, and dropdown options.

**Collaboration and Tool Usage**
- Use write_text_file tool to save code and templates.
- Use validate_python_file tool to verify Python source syntax and runtime.
- Preserve contract validation and no unsupported additions after peer review.

CRITICAL REQUIREMENTS:
- Output app_debate_b.py and templates_debate_b/*.html with exact contract adherence.
- Must maintain exact element IDs, route names, and local file data handling.
- Root '/' must provide dashboard page as entry point without authentication.
- Produce only declared output artifacts with no extraneous files or feedback.

Output: app_debate_b.py, templates_debate_b/*.html""",
            "tools": ["write_text_file", "validate_python_file"],
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
            "prompt": """You are a Senior Backend Web Developer and Code Reviewer specializing in Flask applications with local text file data management and UI contract compliance.

Your goal is to evaluate and merge two complete implementations of the TravelPlanner Flask application, selecting and producing one canonical app.py and set of templates/*.html that conform fully to design_spec.md and the adaptive Web contract.

Task Details:
- Read design_spec.md plus final versions of app_debate_a.py, app_debate_b.py, templates_debate_a/*.html, and templates_debate_b/*.html.
- Compare both implementations feature-by-feature, route-by-route, and template-by-template for exact contract adherence.
- Verify all routes, HTTP methods, template usages, and context variables match design_spec.md precisely.
- Ensure exactly one root route '/' serves or redirects to Dashboard page without authentication.
- Check all element IDs, dynamic IDs, input names, and button IDs in templates for exact compliance.
- Validate local data file reads and writes strictly follow declared formats.
- Use validate_python_file tool to confirm syntax and runtime of candidate app.py files.
- Produce merged canonical app.py and templates/*.html, choosing best contract-conforming parts from both debates.
- Output complete, ready-to-deploy Flask backend and template files with no additions beyond authoritative inputs.

**Review Criteria**
- Syntax correctness and runtime pass of canonical app.py.
- Precise adaptive Web contract compliance for routing and front-end elements.
- Local text file data handling consistent with provided formats.
- No unsupported features or missing essential routes or data handling.
- Preserved root route '/' as Dashboard entry with no authentication.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output canonical app.py and templates/*.html.
- Validate the final app.py with validate_python_file for syntax and runtime.
- Deliver only the declared canonical artifacts.
- Do not add new requirements or refinement markers.

Output: app.py, templates/*.html""",
            "tools": ["write_text_file", "validate_python_file"],
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
            "review_criteria": "Approve if app_debate_a.py and templates_debate_a/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve if app_debate_b.py and templates_debate_b/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Approve if app.py and templates/*.html exist as canonical deliverables, are readable, well-structured, and suitable for deployment with no blocking issues.",
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
    goal: str = "Develop a complete TravelPlanner Flask web app with local text data storage according to user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design phase: debate and finalize detailed adaptive design specification.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Debate and adjudicate the adaptive design specification for TravelPlanner."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implementation phase: debate, revise, and adjudicate the full Flask app and templates implementations.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Debate and adjudicate complete TravelPlanner app.py and templates/*.html implementation."
                }
            ]
        }
    ]
): pass
# Orchestrate_End