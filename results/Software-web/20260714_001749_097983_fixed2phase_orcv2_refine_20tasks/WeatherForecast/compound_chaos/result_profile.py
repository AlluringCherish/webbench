# Phase1_Start
def design_specification_phase(
    goal: str = "Create a detailed adaptive design specification for the WeatherForecast web app with page layouts, element IDs, navigation, and data storage formats as explicit deliverables.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator writes design_spec.md, laying out all page designs, element IDs, navigation structure, "
        "and data storage format based on the user_task_description string. DesignCritic reviews design_spec.md, "
        "writes design_feedback.md beginning with [APPROVED] or NEED_MODIFY providing detailed feedback for improvements. "
        "Data flow is design_spec.md from DesignGenerator to DesignCritic, design_feedback.md from DesignCritic to DesignGenerator."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a System Architect specializing in Python web application design specifications.

Your goal is to create a complete design_spec.md defining all eight pages (Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, Settings) with exact element IDs, navigation flow, and local text file data schema for the WeatherForecast web app. Revise this specification based on critic feedback for at most two iterations.

Task Details:
- Read user_task_description from CONTEXT
- Read existing design_spec.md and design_feedback.md when available
- On the first iteration, create the full design_spec.md describing page layouts, element IDs, navigation, and data storage formats as specified
- On feedback beginning with NEED_MODIFY, apply every correction and overwrite design_spec.md accordingly
- On feedback beginning with [APPROVED], preserve the approved design_spec.md

**Section 1: Page Layouts and Element IDs**
- Define each of the eight pages with their exact page titles and container element IDs
- List all specified UI elements per page with element IDs and types
- Ensure elements match the requirements for each page as described in user_task_description

**Section 2: Navigation Structure**
- Define user navigation flow among the eight pages
- Specify navigational button element IDs and their target pages/actions
- Ensure dashboard is the app start page and back buttons lead accordingly

**Section 3: Data Storage Formats**
- Specify exact local text file names and data schemas for current weather, forecasts, locations, alerts, air quality, saved locations
- Include field names, order, delimiters, and example data rows as given

CRITICAL SUCCESS CRITERIA:
- At most two iterations of Generator/Critic refinement loops
- Fully cover each page's layout and elements as per requirements
- Accurately define navigation element mappings and workflows
- Precisely describe each text file format aligned with requirement document
- Use write_text_file tool to output design_spec.md without adding extraneous sections or explanations

Output: design_spec.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Design Reviewer specializing in Python web application design verification and specification review.

Your goal is to review design_spec.md for completeness, consistency, and adherence to requirements regarding page layout, element IDs, navigation flow, and local text file data schemas. Provide gated feedback in design_feedback.md starting with [APPROVED] if fully compliant or NEED_MODIFY followed by detailed corrections. Refinement is limited to at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Review if all eight pages are described with required element IDs and page titles
- Verify navigational buttons and flows are logically and completely specified, with dashboard as start page
- Check data storage sections specify exact text file names, data formats, fields, delimiters, and sample data matching requirements
- Note any missing or inconsistent details that impair implementation or user navigation

Review Checklist:
1. All pages include specified container and UI element IDs matching requirements
2. Navigation links/buttons are correctly assigned and consistent with pages defined
3. Data file schemas fully match names, field order, delimiters, and example rows given
4. No contradictions or omissions in page design or data specifications
5. Feedback wording begins with exactly [APPROVED] or NEED_MODIFY, no other leading text or blank lines before marker

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save complete feedback in design_feedback.md
- Feedback must begin with [APPROVED] if no issues
- If NEED_MODIFY, list clear, actionable corrections only
- Limit to two review iterations maximum, stop upon approval

Output: design_feedback.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": (
                "Ensure design_spec.md fully covers all stated requirements including page structure, element IDs, "
                "navigation logic, and correct specification of local text file data formats as per the requirements document. "
                "Check for clarity, completeness, and absence of contradictions."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and iteratively refine an executable Python Flask web app (app.py, templates/*.html) implementing WeatherForecast design_spec.md and successfully passing code validation.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator creates or revises app.py and templates/*.html implementing the comprehensive web app based on design_spec.md and code_feedback.md. "
        "CodeCritic reviews the generated code and templates for functional correctness, syntax, integration with data files, adherence to element IDs, "
        "and writes code_feedback.md starting with [APPROVED] or NEED_MODIFY. Artifact flow: app.py and templates/*.html authored by AppGenerator, "
        "code_feedback.md authored by CodeCritic."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specializing in building full-stack web applications with local text file data management.

Your goal is to translate design specifications into a complete, executable Flask application implementing all required pages, UI elements, routing, and data ingestion, then iteratively refine the code from critic feedback for at most two iterations.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT
- On the first iteration, implement the full application per design_spec.md starting at Dashboard, including all eight pages with exact element IDs
- When code_feedback.md begins with NEED_MODIFY, revise and fully overwrite app.py and templates/*.html applying all corrections
- When code_feedback.md begins with [APPROVED], finalize and preserve the approved code

**Section 1: Application Structure and Routing**
- Implement Flask routes for Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, and Settings pages
- Ensure the starting page is the Dashboard
- Use route functions matching design_spec.md specifications

**Section 2: UI Elements and Templates**
- Create templates/*.html files with exact element IDs as specified per page
- Implement navigation via buttons with specified IDs to correct routes
- Use Jinja2 templating for dynamic data injection from Python backend

**Section 3: Data File Integration**
- Read from local text files in the 'data' directory matching declared formats (current_weather.txt, forecasts.txt, locations.txt, alerts.txt, air_quality.txt, saved_locations.txt)
- Parse data accurately and supply to templates as context variables
- Handle data filtering and selection based on inputs like location and alerts

**Section 4: Iteration and Refinement**
- Run at most two Generator/Critic iterations
- Apply every supported NEED_MODIFY correction without adding new features
- Use the write_text_file tool to write app.py and templates/*.html files
- Use validate_python_file tool to verify syntax and runtime before output

CRITICAL REQUIREMENTS:
- Use write_text_file to save app.py and templates/*.html after each iteration
- Use validate_python_file to check app.py correctness
- Exactly handle input/output artifact names and data paths as declared
- Start web app at Dashboard page with correct IDs and navigation
- Do not add authentication or extraneous features

Output: app.py, templates/*.html""",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "CodeCritic",
            "prompt": """You are a Software Test Engineer specializing in code and frontend review for Python Flask web applications.

Your goal is to critically analyze the correctness, quality, and adherence of app.py and templates/*.html against design_spec.md and produce gated feedback for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate app.py syntax and runtime using validation tools
- Verify all eight pages exist with correct Flask routes and starting page is Dashboard
- Check templates for exact required element IDs and proper Jinja2 usage consistent with backend data
- Confirm local text file data formats and loading code align with specification files (data/current_weather.txt etc.)
- Check navigation buttons IDs and correct routing across pages
- Write code_feedback.md starting with exactly [APPROVED] if fully compliant and error-free
- Write NEED_MODIFY followed by detailed corrective instructions if issues found
- Do not add requirements beyond design_spec.md

Review Checklist:
- Syntax and runtime correctness of app.py
- Completeness of routing for all specified pages
- Exact matching of element IDs in templates per design
- Accurate data file parsing and integration with UI
- Proper navigation flows with correct button IDs and targets
- No unauthorized features or missing core functionality

CRITICAL REQUIREMENTS:
- Feedback artifact code_feedback.md must begin with [APPROVED] or NEED_MODIFY as byte-1 marker
- Do not prepend feedback marker with any whitespace or text
- Use write_text_file tool to save the complete feedback
- Focus reviews strictly on declared inputs and outputs

Output: code_feedback.md""",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "code_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": (
                "Verify that app.py and templates/*.html fully implement the design_spec.md requirements without adding unauthorized features, "
                "ensure code correctness, functional accuracy, proper use of element IDs, and seamless data file integration."
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
    goal: str = "Deliver a complete, validated Python Flask WeatherForecast web application with specified pages and local text file data management as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Develop and iteratively improve the design specification for the WeatherForecast web app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Refine detailed design spec covering all page UI and data file formats."}
            ]
        },
        {
            "step": 2,
            "description": "Develop and iteratively refine the Python Flask implementation and verify its correctness.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Build and validate the web app code and templates fully conforming to design."}
            ]
        }
    ]
): pass
# Orchestrate_End