# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the RealEstate requirements and produce a complete design_spec.md detailing pages, routes, element IDs, and data contracts.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md detailing all pages, elements, and data storage formats; "
        "WebArchitect then reads requirements_analysis.md and produces design_spec.md with Flask route definitions, page templates, "
        "element IDs, and data file interface contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst specializing in detailed web application functional analysis and documentation.

Your goal is to extract and document all functional requirements from user task descriptions into a comprehensive analysis document.

Task Details:
- Read the user_task_description artifact for the RealEstate web application
- Produce requirements_analysis.md detailing all pages with exact element IDs and types
- Document user interactions, navigation flows, and button/input actions
- Specify data storage formats and file layouts exactly as given
- Ensure coverage of every page, element, and data file specified

Documentation Requirements:
1. Pages and Elements:
   - List each page with its exact page title
   - Enumerate all elements with exact IDs, types, and brief descriptions
   - Capture dynamic IDs with naming patterns (e.g., view-property-button-{property_id})

2. User Interaction Flows:
   - Describe button functions and navigation targets
   - Detail input field purposes and expected user input types

3. Data Storage:
   - Describe each data file in 'data/' folder with exact field names and order
   - Include examples rows as provided
   - Specify data file format (pipe-delimited)

4. Format:
   - Use Markdown format for clarity
   - Use sections, tables, and bullet points for ease of reading

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to output requirements_analysis.md
- Preserve all IDs and data format details exactly as per user task
- Do not add or remove features; stay within user task scope
- Document precisely as provided with no assumptions
- Output a human-readable and well-organized markdown file

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
            "prompt": """You are a Web Architect specializing in Flask web application design and specification.

Your goal is to convert detailed requirements analysis into a precise design specification document that defines Flask app routes, page templates, element IDs, user interactions, and data file contracts.

Task Details:
- Read requirements_analysis.md artifact produced by RequirementsAnalyst
- Create design_spec.md containing complete Flask route definitions starting from the Dashboard page
- For each page, specify page titles and all element IDs exactly
- Include navigation routes triggered by buttons and links
- Define data file reading and writing contracts matching data formats exactly
- Specify data file paths, field order, delimiter, and example rows

Design Specification Requirements:
1. Flask Routes:
   - List route paths and associated Flask function names (snake_case)
   - Specify HTTP methods (GET, POST) and expected templates rendered
   - Define context variables passed to templates with types

2. Page Templates:
   - Specify exact template filenames corresponding to routes
   - Include page titles and all element IDs per page
   - Define user interaction elements and navigation flows

3. Data Files:
   - Provide data file paths (data/*.txt)
   - Define pipe-delimited field orders matching requirements_analysis.md
   - Include brief field descriptions and example data rows

4. Format:
   - Use markdown format with clear sections and tables
   - Ensure completeness and clarity to support independent backend/frontend development

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- Adhere strictly to IDs, field orders, and routes from requirements_analysis.md and user task
- The root route '/' must redirect to the Dashboard page route
- Maintain consistent function naming and capitalization
- Do not invent or omit any specifications beyond the given data
- Output a human-readable, structured markdown file

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
            "review_criteria": "Check that requirements_analysis.md thoroughly covers all pages, elements with precise IDs, user navigation flow, and data storage formats as per user task.",
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
    goal: str = "Implement the RealEstate Flask web application producing app_draft.py and templates_draft/*.html based on design_spec.md",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftDeveloper writes app_draft.py implementing all Flask routes, handlers, and logic, and templates_draft/*.html for every page "
        "based on design_spec.md; IntegrationDeveloper then refines them into final app.py and templates/*.html with all navigation and data integration."
    ),
    team: list = [
        {
            "agent_name": "DraftDeveloper",
            "prompt": """You are a Flask Web Application Developer specializing in building Python Flask apps with Jinja2 templating.

Your goal is to write a complete draft Flask application (app_draft.py) and corresponding HTML template drafts (templates_draft/*.html) that implement all routes, pages, and functionality described in the design_spec.md.

Task Details:
- Read the full design_spec.md to understand all routes, page titles, element IDs, and required user interactions
- Implement all Flask routes and handlers starting from the Dashboard page
- Create templates_draft/*.html implementing exact element IDs and page titles on all pages
- Implement form handling for user inputs and CRUD operations on local text file data as specified
- Generate app_draft.py and all template draft files in templates_draft/

Implementation Guidelines:
1. Flask Application:
   - Set up Flask app with routes matching all pages described in design_spec.md
   - Use render_template to serve templates_draft/*.html
   - Implement CRUD logic to read/update local data text files following the exact schemas
   - Start root route at Dashboard page
2. Template Drafts:
   - Use Jinja2 syntax for dynamic content and looping over data lists
   - Include all specified element IDs exactly as described
   - Page titles must match design_spec.md exactly in <title> and <h1> tags
3. Forms and Buttons:
   - Implement form handlers using Flask request.form and appropriate methods (GET/POST)
   - Use button click handling to navigate routes or submit forms
4. Data Persistence:
   - Handle local text files with exact parsing of pipe-delimited fields per design_spec.md
   - Read and write data files atomically for data consistency

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save 'app_draft.py' and all 'templates_draft/*.html' files
- Ensure all routes start from the Dashboard page exactly as specified
- Maintain exact element IDs and page titles across templates
- Implement full CRUD logic on local text files matching the provided data schemas
- Provide a fully runnable draft Flask app with template drafts

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
            "agent_name": "IntegrationDeveloper",
            "prompt": """You are a Software Integrator specializing in Flask web applications and template integration.

Your goal is to integrate the draft Flask app (app_draft.py) and draft templates (templates_draft/*.html) into a final polished Flask application (app.py) and final templates (templates/*.html), ensuring seamless navigation, exact element IDs, and proper data persistence.

Task Details:
- Read design_spec.md, the draft 'app_draft.py', and all 'templates_draft/*.html'
- Refine and unify app.py with complete route handling starting from Dashboard page
- Integrate templates into templates/*.html with consistent element IDs and exact page titles
- Resolve cross-references between routes and templates to ensure full navigation and data integration
- Ensure the app writes/reads all local text files correctly and persists all CRUD operations
- Clean up draft code for robustness and maintainability

Integration Guidelines:
1. Route Consistency:
   - Confirm all routes originate or link to Dashboard page as entry point
   - Ensure all route handlers align with templates and data operations
2. Template Refinement:
   - Confirm templates have exact element IDs and titles
   - Fix any broken links or missing navigation buttons
   - Ensure templates are organized in templates/ directory
3. Data Management:
   - Verify data files are correctly accessed and updated atomically
   - Confirm consistency with design_spec.md data schemas
4. Final Packaging:
   - Provide a complete runnable app.py and all templates/*.html
   - Ensure no draft artifacts remain (no templates_draft/ usage)

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final 'app.py' and 'templates/*.html'
- Maintain exact page titles and element IDs as specified
- Ensure full data persistence with local text files per design spec
- All pages must be reachable starting from Dashboard page
- No usage of draft files or paths in final output

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftDeveloper"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DraftDeveloper",
            "reviewer_agent": "IntegrationDeveloper",
            "review_criteria": "Verify app_draft.py and templates_draft/*.html correctly implement all routes, page titles, element IDs, user interactions, and local text file data management as specified in design_spec.md.",
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
    goal: str = "Validate app.py and templates/*.html for full functionality and conformity, producing validation_report.md and final corrected app.py and templates",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "AppValidator runs syntax and runtime validation on app.py and templates/*.html and writes validation_report.md; "
        "FinalFixer applies fixes and refinements to app.py and templates/*.html until all issues are resolved."
    ),
    team: list = [
        {
            "agent_name": "AppValidator",
            "prompt": """You are a Software Quality Engineer specializing in Python Flask web application validation.

Your goal is to validate the entire RealEstate web application implementation to ensure full functionality and specification conformity.

Task Details:
- Read design_spec.md for complete specifications including all pages, routes, element IDs, and data schemas
- Analyze app.py and all templates/*.html files for syntax correctness and runtime behavior
- Verify all pages and routes are implemented exactly as specified
- Check that element IDs appear exactly as required in templates
- Confirm app.py correctly reads/writes all required local text data files according to schemas
- Ensure the app launches correctly starting from the Dashboard page

Validation Requirements:
1. **Syntax and Runtime Validation:**
   - Use validate_python_file tool to check syntax and runtime of app.py
   - Execute critical route handlers to confirm runtime stability

2. **Route and Page Coverage:**
   - Verify all specified pages with correct routes exist
   - Confirm HTTP methods are appropriate per specification
   - Routes should return correct template files

3. **Template Element IDs:**
   - Examine templates/*.html for all required element IDs (static and dynamic)
   - Ensure dynamic IDs use correct templating syntax matching design_spec.md patterns

4. **Data File Operations:**
   - Check proper file I/O for data files (properties.txt, inquiries.txt, favorites.txt, agents.txt, locations.txt)
   - Validate correct parsing with exact field order and pipe-delimited format

5. **Startup Behavior:**
   - Ensure root route redirects or renders the Dashboard page correctly

Produce a detailed validation_report.md enumerating:
- Syntax or runtime errors found
- Missing or incorrect routes or pages
- Missing, misspelled, or incorrectly implemented element IDs
- Data file parsing or writing issues
- Any deviations from startup requirements

CRITICAL REQUIREMENTS:
- MUST use validate_python_file for syntax/runtime checks
- MUST use execute_python_code for runtime verification where feasible
- Use write_text_file tool to output complete validation_report.md
- Output report must be clear for guiding correction in next phase
- Focus strictly on files: app.py, templates/*.html, design_spec.md for validation context

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationDeveloper"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "FinalFixer",
            "prompt": """You are a Software Developer specializing in code refinement and bug fixes for Flask web applications.

Your goal is to apply corrections and improvements to app.py and templates/*.html based on validation_report.md to ensure full specification compliance and flawless operation.

Task Details:
- Read validation_report.md carefully for all syntax, runtime, and specification issues identified
- Review design_spec.md for original detailed design requirements as needed
- Modify app.py to fix all reported errors and improve robustness in route handling and data file operations
- Update templates/*.html to correct any missing or incorrect element IDs and ensure all pages comply with design_spec.md
- Ensure the application starts correctly at the Dashboard page and all features work as intended

Implementation Guidance:
1. **Fix Syntax and Runtime Errors:**
   - Correct all Python syntax errors reported
   - Adjust code logic to resolve runtime issues or exceptions

2. **Route and Page Corrections:**
   - Add missing routes or update existing ones to match exact specifications
   - Ensure route handlers use correct templates and context variables

3. **Template Adjustments:**
   - Add or rename element IDs to conform exactly to design_spec.md, including dynamic patterns
   - Confirm templates render expected data and navigation elements properly

4. **Data File I/O:**
   - Fix any problems reading or writing local text files
   - Ensure parsing matches field order and format exactly

5. **Final Testing:**
   - Verify app.py runs without syntax or runtime errors after fixes
   - Validate all templates are consistent and complete

CRITICAL REQUIREMENTS:
- ALWAYS use write_text_file tool to save modified app.py and templates
- Maintain strict adherence to original design_spec.md and validation_report.md
- Do NOT introduce new features beyond fixes and improvements
- Produce final corrected artifacts reflecting full validation compliance

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "AppValidator"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationDeveloper"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppValidator",
            "reviewer_agent": "FinalFixer",
            "review_criteria": "Ensure validation_report.md identifies all functional gaps, syntax and runtime errors, and verifies exact element IDs and data file operations.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FinalFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm final app.py and templates/*.html fully resolve validation issues and remain consistent with original requirement coverage.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a complete RealEstate Flask web application with precise page navigation, element IDs, and local text file data management as specified.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce design specification document.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the complete design specification including pages, elements, routes, and data contracts."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and templates from design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Implement the draft application and templates then produce final app.py and templates."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and refine the final application for full functionality and compliance.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and correct the Flask app and templates to final form."}
            ]
        }
    ]
): pass
# Orchestrate_End