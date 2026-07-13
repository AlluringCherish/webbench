# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze 'WeatherForecast' app requirements and produce a detailed design_spec.md covering all pages, elements, routes, and data fixtures.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md capturing all user-visible features, page titles, UI elements with IDs, "
        "route mappings, and data file usage; then WebArchitect reads it and produces design_spec.md, specifying Flask application architecture, "
        "template filenames and layouts, route methods, context variables, and data file interaction."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Business Analyst specializing in requirements tracing for web applications.

Your goal is to produce a detailed requirements_analysis.md that comprehensively captures all user-visible features, UI element IDs, page titles, routes, and data files expected.

Task Details:
- Read user_task_description fully
- Extract and document every UI page with its page title and all elements IDs as specified
- Identify and list all user-accessible routes and navigation mappings based on pages and buttons
- List expected data files with their formats and example usage as described
- Output a clear, organized markdown file requirements_analysis.md reflecting full user requirements

Instructions:
1. Systematically scan each page section and collect:
   - Page Title
   - All element IDs and their types (button, div, input, dropdown, etc.)
   - Navigation buttons and their linked pages/routes
2. Record routes derived from navigation buttons and pages
3. Summarize all data files, their fields, formats, and example rows
4. Organize requirements_analysis.md into sections: Pages & Elements, Routes, Data Files

Critical Requirements:
- Use write_text_file tool to save output as requirements_analysis.md
- Preserve exact element IDs and page titles as in the user input
- Provide concise and unambiguous mappings
- Focus only on information explicitly given in user_task_description

Output: requirements_analysis.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "agent_name": "WebArchitect",
            "prompt": """You are a Web Architect specializing in Flask web application design and architecture.

Your goal is to produce a detailed design_spec.md that specifies Flask routes, HTTP methods, template file names and layout, exact element IDs, context variables, and data file interactions per user feature.

Task Details:
- Read requirements_analysis.md fully
- Define complete Flask route table: route paths, function names, HTTP methods (GET/POST)
- Specify template filenames under templates/ with required HTML element IDs per page
- Enumerate context variables passed to each template with types and structures
- Describe data file reading/loading logic aligned to user features and design
- Output a comprehensive design_spec.md covering application architecture for both backend and frontend teams

Instructions:
1. Draft route specification mapping each page and button navigation to Flask URL routes and methods
2. Detail template files naming conventions and layout including required element IDs exactly
3. Specify context variables for each template reflecting data to display (e.g. dicts, lists, primitives)
4. Document data file usage: filenames, field formats, parsing order, and integration points
5. Organize design_spec.md into:
   - Flask Routes and Methods
   - Template Files, Element IDs, Context Variables
   - Data File Interaction and Parsing Schemas

Critical Requirements:
- Use write_text_file tool to save output as design_spec.md
- Maintain exact element ID names and page titles from requirements_analysis.md
- Define function names consistent with routes and templates naming conventions
- Ensure clarity to enable independent backend and frontend developments based on this spec

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "RequirementsAnalyst",
            "reviewer_agent": "WebArchitect",
            "review_criteria": (
                "Verify requirements_analysis.md covers all user-visible pages, exact element IDs, page titles, navigation paths, and required data files "
                "before architecture begins."
            ),
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the 'WeatherForecast' Flask application as app_draft.py and templates/*.html drafts according to design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer develops app_draft.py with all routes and logic plus templates_draft/*.html files for each page based on design_spec.md; "
        "then IntegrationEngineer integrates drafts into final app.py and templates/*.html with correct render_template calls and local data file usage."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "prompt": """You are a Backend Developer and Frontend Developer specializing in Flask web applications and HTML templating.

Your goal is to create draft implementations of the Flask backend and HTML views using the given design specifications to form a foundation for final integration.

Task Details:
- Read design_spec.md fully for all Flask routes, page element IDs, layout, and navigation requirements
- Implement app_draft.py with all Flask routes, logic placeholders for data access only (no real data loading)
- Create templates_draft/*.html files with exact page element IDs, buttons, inputs, and layouts as specified
- Use placeholder content and comments in draft code for file I/O and dynamic data rendering
- Output draft backend as app_draft.py and draft frontend templates in templates_draft/*.html

Implementation Instructions:
1. Flask Backend Draft:
   - Implement Flask routes exactly as specified (route paths, function names, HTTP methods)
   - For dynamic routes, use route parameters as in design spec
   - Include placeholder comments for data reading from text files (e.g., # TODO: Load current_weather.txt)
   - Use render_template with template names from templates_draft directory
   - Include route navigations but omit actual data logic (stub function bodies allowed)

2. HTML Templates Draft:
   - Create one HTML file per page as specified
   - Include all required element IDs exactly as listed (divs, buttons, inputs, tables, etc.)
   - Use minimal placeholder content or dummy text for areas requiring dynamic data
   - Structure content and layout according to design spec overview and page elements
   - Use static references to buttons and links for navigation controls only

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Ensure all element IDs match design_spec.md exactly (case sensitive, including dynamic ID patterns)
- Draft code must not include actual data file reading or integration logic
- Do not finalize code for deployment—focus on structure and placeholders only

Output: app_draft.py, templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "prompt": """You are a Backend Developer and Frontend Developer specializing in Flask applications with local data integration.

Your goal is to build the final production-ready Flask backend and HTML templates by integrating data file reads and completing the draft implementations.

Task Details:
- Read design_spec.md for reference on routes, element IDs, context variables, and navigation mappings
- Read app_draft.py and templates_draft/*.html as draft starting points
- Convert app_draft.py into fully functional app.py, implementing data file reading from the 'data' directory
- Adjust render_template calls to use templates/*.html
- Complete all routes with correct data loading from local text files using exact field orders
- Convert each templates_draft/*.html to templates/*.html, preserving all element IDs and adding dynamic content placeholders accordingly
- Ensure all navigation and UI elements conform exactly to design_spec.md specifications

Implementation Instructions:
1. Backend Integration:
   - Implement file I/O to read data from text files located in 'data' directory, parsing with pipe-delimited format
   - Load all required data into appropriate structures to pass as context variables to templates
   - Use exact function and route names and HTTP methods as per design_spec.md
   - Use render_template with final templates/*.html paths
   - Handle edge cases such as missing files or empty data gracefully

2. Frontend Integration:
   - For each draft template, create a corresponding final template with dynamic placeholders using Jinja2 syntax
   - Replace static placeholders with loops, conditionals, and variable insertions to reflect live data
   - Preserve all element IDs exactly as specified (static and dynamic patterns)
   - Ensure navigation buttons and links use url_for() with correct route names and parameters

3. Quality:
   - Ensure consistent naming and data usage across backend and frontend
   - Confirm that all dynamic UI elements correspond correctly to data provided by backend routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Preserve all element IDs with case sensitivity and pattern accuracy
- Data file parsing must match design_spec.md exact field orders for all data files
- All render_template calls must refer to templates/*.html, not drafts
- Ensure full feature completion as per design_spec.md
- Avoid leaving stub placeholders—fully implement data retrieval and rendering for all routes

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DraftEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Ensure the draft app_draft.py and templates_draft/*.html correctly implement all routes and UI elements as per design_spec.md before integration."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate final app.py and templates/*.html to ensure correct functionality, route coverage, UI elements, and data integration.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator conducts thorough syntax, runtime, and functional validation on app.py and templates/*.html producing validation_report.md; "
        "SequentialFixer applies all fixes identified and writes final corrected app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in web application validation and quality assurance.

Your goal is to thoroughly validate the final backend and frontend implementation for correctness, covering syntax, runtime, route coverage, UI elements, and data integration. Your deliverable is a detailed validation_report.md.

Task Details:
- Read design_spec.md to understand expected routes, templates, element IDs, and data schemas
- Validate app.py for Python syntax and runtime errors, ensuring it starts and runs correctly
- Validate templates/*.html for presence of all specified element IDs and correct template rendering
- Check that all routes defined in design_spec.md are implemented in app.py and render correct templates
- Verify data files are used according to defined schemas and loaded correctly in the backend
- Produce comprehensive validation_report.md describing findings with error traces and test results

Validation Requirements:
1. Syntax and Runtime Validation:
   - Use validate_python_file tool for app.py syntax and runtime checks
   - Use execute_python_code to attempt starting the Flask app or test key functions (simulate requests)

2. Route and Template Coverage:
   - Verify each route in design_spec.md Section 1 is implemented and renders correct template
   - Confirm all HTML templates contain required element IDs exactly as specified

3. Data Integration:
   - Check usage and correctness of data files as per design_spec.md Section 3
   - Confirm that field parsing matches specified schemas with exact field order

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools for validations
- Use write_text_file tool to output detailed validation_report.md
- Validation report must clearly state all errors, warnings, and passes
- Focus strictly on artifacts: app.py, templates/*.html, and design_spec.md
- Provide actionable, descriptive feedback suitable for fixing in next phase

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "prompt": """You are a Software Developer specializing in sequential bug fixing and compliance enforcement for web applications.

Your goal is to apply all corrections from validation_report.md to produce the final versions of app.py and templates/*.html fully compliant with design_spec.md and user requirements.

Task Details:
- Read validation_report.md for all identified issues and suggested fixes
- Review current app.py and templates/*.html implementations
- Update app.py and templates/*.html to fix all backend and frontend issues:
  - Correct syntax and runtime errors
  - Ensure full route coverage and correct template rendering
  - Fix missing or incorrect UI element IDs
  - Align data loading and usage with design_spec.md schemas
- Produce final corrected app.py and templates/*.html ready for deployment

Fixing Guidelines:
1. Prioritize critical errors affecting app startup or core functionality
2. Address all missing or mismatched element IDs in templates
3. Ensure all fixes conform strictly to design_spec.md specifications without adding extra features
4. Maintain code quality, readability, and consistency

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and all templates/*.html files
- Fully resolve all validation_report.md issues without omissions
- Maintain artifact filename conventions exactly as provided
- Do not modify unrelated code or templates beyond necessary fixes
- Deliver production-ready, error-free backend and frontend codebase

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "WebValidator",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": (
                "Verify validation_report.md contains exhaustive test coverage results, error traces, and actionable fixes for both backend and frontend."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Confirm that the final app.py and templates/*.html address all validation issues and fully implement all user requirements "
                "from requirements_analysis.md."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a Flask 'WeatherForecast' web application with local text file data storage according to detailed requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce comprehensive design specification for the Flask app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed design_spec.md specifying app architecture and UI."}
            ]
        },
        {
            "step": 2,
            "description": "Implement draft Flask application and templates based on the design specification, then integrate into final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop app_draft.py, templates_draft/*.html and integrate into final app.py and templates/*.html."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the final application to ensure full correctness and requirement coverage.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and correct final app.py and templates/*.html with feedback-driven refinements."}
            ]
        }
    ]
): pass
# Orchestrate_End