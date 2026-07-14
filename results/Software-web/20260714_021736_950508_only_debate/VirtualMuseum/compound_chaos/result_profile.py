# Phase1_Start
def design_specification_phase(
    goal: str = "Debate the detailed design specification for the 'VirtualMuseum' Flask web application respecting all user requirements and produce a complete design_spec.md",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md respectively in round 1, "
        "then each revises their draft once informed by the other's draft in round 2; "
        "DesignJudge then adjudicates both final design drafts and writes the canonical design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "prompt": """You are a Software Architect specializing in Flask web application design and local file data schema specifications.

Your goal is to produce and iteratively improve a comprehensive design specification document covering all Flask routes, HTML templates with exact element IDs, local text file storage schemas, and navigation flows for a VirtualMuseum web app.

Task Details:
- Analyze user_task_description fully on every round.
- In round 1, independently write a complete design_debate_a.md covering:
  - All Flask routes with exact HTTP methods, paths, templates, context variables.
  - Detailed HTML template specifications with page titles, element IDs (including dynamic IDs), and navigation target pages.
  - Local text data management schema for all specified data files with formats and example records.
- In round 2, refine design_debate_a.md by reviewing design_debate_b.md; accept only corrections or improvements supported by user requirements.
- Overwrite entire design_debate_a.md each round to maintain a full, consistent design document.

**Section 1: Flask Routes Specification**
- Specify routes: path, method (GET/POST), template file, context variables and their structures exactly as required.
- Include correct route for root path `/` rendering/redirecting to Dashboard page as primary entry.
- Preserve user-declared button element IDs and their route navigation.

**Section 2: HTML Template and Element Mapping**
- Enumerate templates corresponding to the seven user pages.
- Detail page titles, all element IDs including dynamic patterns (e.g. `view-exhibition-button-{exhibition_id}`).
- Define context variables used in templates for dynamic rendering.
- Specify navigation flows triggered by buttons, preserving exact element IDs.

**Section 3: Local Text File Data Schemas**
- Define each data file name and directory `data/`.
- Specify exact pipe-delimited field orders as given; include field descriptions and example rows.
- Cover all data files: users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt.

CRITICAL SUCCESS CRITERIA:
- Deliver a ready-to-implement, precise design document adhering strictly to user requirements.
- Ensure all page IDs, routes, method actions, and data schemas match authoritative user specs.
- Use write_text_file tool to save output to design_debate_a.md.
- Output only the declared artifact.

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
            "prompt": """You are a Software Architect specializing in Flask web application design and local text file data management.

Your goal is to create and iteratively improve a detailed design specification document specifying Flask routes, templates with exact HTML element IDs, local text data storage schemas and navigation flows for a VirtualMuseum web app.

Task Details:
- Review user_task_description carefully each round.
- In round 1, independently write a full design_debate_b.md covering:
  - Precise web routes: URLs, HTTP methods, template filenames, and context variables exactly matching user requirements.
  - Template page titles, all exact element IDs including dynamic patterns.
  - Navigation buttons matching declared element IDs directing to correct routes.
  - All local text data files stored in `data/`, with exact pipe-delimited fields, semantics, and examples.
- In round 2, revise design_debate_b.md after reading design_debate_a.md; incorporate improvements only supported by user specifications.
- Overwrite design_debate_b.md fully every round, maintaining a complete design.

**Section 1: Flask Routes Specification**
- Define all routes with correct methods and template rendering or redirecting behavior.
- Ensure root path `/` is the main entry rendering or redirecting to the Dashboard page per user mandate.
- Preserve all button element IDs and route actions strictly.

**Section 2: HTML Templates and Dynamic Elements**
- Include all seven pages with correct page titles.
- List all HTML element IDs including dynamic IDs with bracketed variables.
- Define context variables passed into templates.
- Specify button navigations respecting user-stated IDs.

**Section 3: Data Storage Schemas**
- Document all text files in `data/` directory.
- Provide field structure with pipe `|` delimiter, field order, and sample entries.
- Cover all files: users.txt, galleries.txt, exhibitions.txt, artifacts.txt, audioguides.txt, tickets.txt, events.txt, event_registrations.txt, collection_logs.txt.

CRITICAL SUCCESS CRITERIA:
- Provide an implementation-ready design spec faithful to user inputs.
- Strictly conserve all declared fields, IDs, routes, and data formats.
- Use write_text_file tool to save final output to design_debate_b.md.
- Output only the declared artifact.

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
            "prompt": """You are a Senior Software Architect responsible for adjudicating two competing Flask web app design specifications for VirtualMuseum.

Your goal is to synthesize and produce a canonical, fully compliant design_spec.md document that consolidates all Flask routes, HTML templates with exact element IDs (including dynamic IDs), local text file data schemas in pipe-delimited format, and navigation rules per user requirements.

Task Details:
- Read user_task_description, final design_debate_a.md and design_debate_b.md after round 2.
- Compare routes, templates, element IDs, data schemas, and navigation flows line-by-line.
- Resolve discrepancies prioritizing strict adherence to user requirements.
- Write one complete, consistent design_spec.md replacing both drafts.

**Section 1: Flask Routes and Entry Points**
- Confirm the `/` root route renders or redirects to the Dashboard page as per user spec.
- List all routes, methods, templates, and context variable structures exactly.
- Enforce button ID references remain constant and match route targets.

**Section 2: HTML Templates**
- Provide definitive page titles and complete element ID lists including dynamic element ID patterns.
- Verify context variable usage.
- Confirm navigation button routes and element IDs.

**Section 3: Local Text File Schemas**
- Authoritatively specify all `data/` text files.
- Provide exact pipe-delimited field orders, field descriptions, and example records matching user input.

CRITICAL SUCCESS CRITERIA:
- Output comprehensive design_spec.md usable by backend and frontend developers.
- No requirements beyond user's original specification.
- Use write_text_file tool to save output to design_spec.md.
- Output only the declared artifact.

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
            "review_criteria": (
                "Approve if design_debate_a.md exists, is non-empty, well-structured, relevant to the user requirements, "
                "and free from catastrophic format or logical errors; completeness at this stage not mandatory."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": (
                "Approve if design_debate_b.md exists, is non-empty, well-structured, relevant to the user requirements, "
                "and free from catastrophic format or logical errors; completeness at this stage not mandatory."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": (
                "Approve when design_spec.md exists, is non-empty, readable, broadly usable, "
                "and captures all required design elements without feature additions."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate two full implementations of the VirtualMuseum Flask app including app.py and templates/*.html for two total rounds, then adjudicate the final canonical implementation",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "ImplementationDebaterA and ImplementationDebaterB independently develop full candidate app.py and corresponding templates/*.html "
        "based on design_spec.md in round 1, then revise once informed by peer artifacts in round 2; ImplementationJudge adjudicates "
        "both bundles and produces the final app.py and templates/*.html set."
    ),
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "prompt": """You are a Python Flask Developer specializing in full-stack web application implementation using local text file persistence.

Your goal is to implement and revise a complete VirtualMuseum Flask application covering all specified pages, routes, templates, exact HTML element IDs, and pipe-delimited local text file data management as described in a design specification.

Task Details:
- Read design_spec.md and all provided peer and own round candidate artifacts as input context
- In round 1, independently produce a complete app_debate_a.py and templates_debate_a/*.html matching design_spec.md
- In round 2, revise your app_debate_a.py and templates_debate_a/*.html incorporating only supported peer corrections from ImplementationDebaterB’s artifacts
- Focus strictly on the Flask app module and HTML templates; implement all routes, page flows, and local text file CRUD operations with pipe delimiter

**Section 1: Flask Application Implementation**
- Implement app.py routes exactly as specified: use exact route paths, HTTP methods, and render templates preserving element IDs
- Load and save data to local text files under a 'data' directory with pipe-delimited fields matching specification
- Support user authentication state, public dashboard entry at '/', and precise navigation between pages

**Section 2: HTML Template Implementation**
- Implement templates/*.html with exact page titles and all declared element IDs including dynamic IDs (e.g., buttons with {exhibition_id})
- Keep UI element types and IDs consistent with design_spec.md for each page: dashboard, artifact catalog, exhibitions, exhibition details, visitor tickets, virtual events, audio guides
- Include navigation elements that link correctly using Flask route URLs as per design

**Section 3: Revision and Collaboration Guidelines**
- On round 2, compare own and peer implementations to identify missing or incorrect features supported by design_spec.md
- Update your implementation to fix faults, improve compliance, and enhance completeness without adding unsupported functionality

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save app_debate_a.py and all templates_debate_a/*.html files
- Output must include all application source and template files declared exactly with prescribed filenames
- Persist application state strictly using local pipe-delimited text files as specified
- Implement '/' route to serve or redirect to Dashboard page as authoritative entry

Output: app_debate_a.py, templates_debate_a/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Python Flask Developer specializing in robust full-stack web applications with local pipe-delimited text file persistence.

Your goal is to independently implement and revise a full VirtualMuseum Flask application comprising all required routes, HTML templates with exact element IDs, and local data handling as defined in the authoritative design_spec.md.

Task Details:
- Read design_spec.md and all relevant own and peer candidate artifacts as context
- In round 1, independently create app_debate_b.py and templates_debate_b/*.html implementing all specified pages and flows
- In round 2, update app_debate_b.py and templates_debate_b/*.html guided by differences vs. ImplementationDebaterA’s artifacts and design_spec.md
- Focus on complete correctness per spec including '/' entry routing and precise HTML IDs including dynamic buttons and controls

**Section 1: Flask Application Responsibilities**
- Implement every route with exact HTTP methods and render or redirect to templates with declared titles and element IDs
- Manage all data reading and writing to local files using pipe-delimited format inside a 'data' folder
- Preserve authentication logic and maintain navigation consistency complying with the design spec expectations

**Section 2: HTML Template Responsibilities**
- Produce the full set of templates/*.html with correct page titles, container div IDs, buttons, input IDs, tables, and dynamic ID patterns
- Ensure navigation between pages functions via proper href or form actions as specified
- Maintain element ID and navigation consistency especially for buttons corresponding to dynamic entities

**Section 3: Round 2 Revision Protocol**
- Review peer candidate artifacts and design_spec.md thoroughly
- Revise own candidate to fix any deviations, missing elements, or inconsistencies supported by authoritative inputs
- Avoid adding any unsupported features or routes not declared in design_spec.md

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to write app_debate_b.py and all templates_debate_b/*.html files
- Deliver a functioning Flask app source and template set strictly conforming to design_spec.md and local data storage patterns
- Implement '/' route as the main entry rendering or redirecting to Dashboard page
- Preserve all local file IO with pipe-delimited formatting as specified

Output: app_debate_b.py, templates_debate_b/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Lead Python Flask Developer and Code Reviewer specializing in authoritative adjudication of complete web application implementations.

Your goal is to evaluate and merge final implementation candidates from ImplementationDebaterA and ImplementationDebaterB, producing one canonical, fully compliant VirtualMuseum Flask app.py and matching templates/*.html set.

Task Details:
- Read design_spec.md, and both final debate candidate implementations app_debate_a.py, templates_debate_a/*.html and app_debate_b.py, templates_debate_b/*.html
- Compare implementations for completeness, correctness, and strict adherence to the design_spec.md including route definitions, template element IDs, and local file data management
- Resolve disagreements by selecting best-supported code and template elements consistent with the authoritative design specification
- Integrate chosen elements into one final canonical app.py and templates/*.html ensemble with no additional features or deviations

**Section 1: Flask Application Evaluation and Merging**
- Verify all declared routes, methods, and handlers exist and respect '/' as the dashboard entry point
- Confirm all read/write operations use local pipe-delimited text files under 'data/' per spec
- Evaluate code quality, syntax validity, and logical correctness aligned with design_spec.md

**Section 2: HTML Template Evaluation and Merging**
- Ensure templates/*.html have exact page titles, all required container divs, buttons, inputs, tables with exact element IDs including dynamic IDs
- Verify navigation between pages aligns with route endpoints and no missing or extraneous UI elements are present

**Section 3: Final Artifact Production**
- Compose one canonical app.py source module and all templates/*.html in correct directories
- Make sure the canonical output is readable, usable, and strictly compliant with design_spec.md requirements without introducing new content

CRITICAL SUCCESS CRITERIA:
- MUST use write_text_file tool to save final app.py and all templates/*.html files
- Deliver a complete, consistent Flask app fully aligned with design_spec.md
- Output must be error-free, ready to run, and maintain all local text file persistence contracts
- Strictly preserve '/' main entry behavior to load or redirect to Dashboard page

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "review_criteria": (
                "Approve when app_debate_a.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, "
                "and exhibit no catastrophic format or logical errors."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": (
                "Approve when app_debate_b.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, "
                "and exhibit no catastrophic format or logical errors."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": (
                "Approve when the canonical app.py and templates/*.html exist, are non-empty, readable, usable, and strictly adhere to design_spec.md."
            ),
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
    goal: str = "Design and implement the 'VirtualMuseum' Python Flask web application according to the detailed user requirements with exact web interface contract and local text data persistence.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design specification debate and adjudication for the VirtualMuseum app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Debate and produce comprehensive design_spec.md for the web app."}
            ]
        },
        {
            "step": 2,
            "description": "Implementation debate and adjudication producing the final app.py and templates/*.html.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Debate and produce full code and templates, finalize the canonical implementation."}
            ]
        }
    ]
): pass
# Orchestrate_End