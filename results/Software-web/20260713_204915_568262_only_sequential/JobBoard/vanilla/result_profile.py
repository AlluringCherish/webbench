# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the 'JobBoard' web application requirements and produce a complete design_spec.md covering pages, routes, UI element IDs, and data models.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst reads the user task and writes requirements_analysis.md detailing each page, required routes, page titles, UI element IDs, and the data model. "
        "WebArchitect then reads requirements_analysis.md and converts it into design_spec.md with finalized page architecture, route specifications, template mapping, element IDs, and data file contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Software Requirements Analyst specializing in web application requirements documentation.

Your goal is to analyze the user-provided task description and produce a comprehensive requirements analysis document that details all pages, page titles, UI element IDs, navigation structure, and data storage requirements for the JobBoard web application.

Task Details:
- Read user_task_description in full to extract relevant information
- Identify and document all pages with their exact titles
- Extract and list all UI element IDs for each page
- Outline the navigation flow between pages using button/element IDs
- Summarize data storage requirements including data files, fields, and formats mentioned
- Output requirements_analysis.md capturing all above information clearly and completely

Analysis Requirements:
1. **Pages and Titles**:
   - List each page in the app with exact title as in the user task
   - Include key container element IDs per page

2. **UI Element IDs**:
   - Enumerate all specified UI element IDs for each page accurately
   - Distinguish between static and dynamic element IDs (with variable placeholders)

3. **Navigation Structure**:
   - Map navigational buttons or links to target pages by their button IDs
   - Reflect logical entry points and user flow starting from Dashboard

4. **Data Storage Summary**:
   - List each data file with its name and described format
   - Include fields and example data if available
   - Note relationships or mappings between data files

CRITICAL REQUIREMENTS:
- Use write_text_file tool to output requirements_analysis.md
- Ensure completeness and accuracy matching the user task exactly
- Avoid assumptions beyond the provided user task description

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

Your goal is to create a detailed design specification that converts the requirements_analysis.md into an explicit architecture document containing Flask route endpoints, HTTP methods, exact page titles, template filenames, UI element IDs, navigation flow, and detailed data file schemas. The design must support user navigation starting at the Dashboard page without requiring authentication.

Task Details:
- Read requirements_analysis.md and user_task_description fully
- Define Flask route endpoints with HTTP methods (GET/POST) for all pages and actions
- Specify exact page titles as per requirements
- Map each page to a template filename (templates/{page_name}.html or similar)
- List all UI element IDs as extracted, including dynamic ID patterns
- Specify navigation flow between pages referencing precise button/link IDs
- Define detailed data file schemas with file names, exact field order, data formats (pipe-delimited), and example data rows
- Ensure architecture supports all user task features with no authentication, starting at Dashboard

Design Requirements:
1. **Flask Routes**:
   - Use RESTful GET for pages rendering data
   - Use POST where form submissions occur (e.g., application form)
   - Include dynamic parameters for detail pages (e.g., job_id, company_id, app_id where applicable)

2. **Templates and Page Titles**:
   - Define template filenames tied to pages (snake_case naming recommended)
   - Include exact page titles matching requirements

3. **UI Element IDs**:
   - Enumerate all exact element IDs from requirements_analysis.md
   - Specify format for dynamic IDs with placeholders (e.g., view-job-button-{job_id})

4. **Data File Contracts**:
   - For each data file, specify path data/{filename}.txt
   - List fields in exact order pipe-delimited
   - Describe contents briefly
   - Provide 2-3 example entries matching user data samples

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Ensure full traceability between requirements_analysis.md and design_spec.md
- Follow user requirements precisely; no assumptions beyond spec
- Use consistent naming conventions for routes, templates, UI IDs
- Support direct navigation from Dashboard with no authentication requirement

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"},
                {"type": "user", "name": "user_task_description", "source": "User"}
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
            "review_criteria": "Verify requirements_analysis.md covers all pages, UI element IDs, and data storage requirements as specified in the user task with no omissions.",
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
    goal: str = "Implement the 'JobBoard' web application as a Flask app.py and corresponding templates/*.html files based on design_spec.md and user requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer develops app_draft.py and draft templates/*.html files implementing all pages, routes, UIs, and data file handling as specified. "
        "IntegrationEngineer then refines and integrates drafts into a final app.py and templates/*.html set that fully comply with the design_spec.md and run as a cohesive Flask web app with dashboard as the start page."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "prompt": """You are a Backend and Frontend Developer specializing in Flask web applications with template drafting.

Your goal is to draft a Flask application (app_draft.py) and corresponding HTML template drafts implementing all required pages, UI element IDs, navigation buttons, and data interactions with local text files.

Task Details:
- Read design_spec.md and user_task_description fully to understand all pages, routes, UIs, and data storage formats.
- Create app_draft.py implementing Flask routes and handlers covering all pages and features.
- Draft ALL HTML templates (*.html) for all pages with correct UI element IDs as specified in user requirements.
- Use render_template calls referencing templates in a 'templates_draft/' directory.
- Manage local data files for all specified entities (jobs, companies, applications, resumes, categories, job_categories).
- Focus on implementing page navigation and data loading/presentation as drafts for subsequent refinement.
- Output app_draft.py and templates draft files under templates_draft/ folder.

Flask Implementation Guidelines:
1. Define Flask app with standard setup and SECRET_KEY.
2. For each route, implement GET handlers rendering templates with appropriate context variables derived from data files.
3. Include placeholders or simple forms for POST routes (e.g., application submission).
4. Load data from pipe-delimited local text files in the data/ directory using prescribed field orders.
5. Use clear function names matching page purposes and route URLs consistent with design_spec.md.
6. Use render_template with template filenames located under templates_draft/.

Template Drafting Guidelines:
1. Create basic HTML structure for each template including DOCTYPE, <html>, <head> with page title, and <body>.
2. Include all required UI elements with exact IDs as specified in the user requirements.
3. Use Jinja2 syntax to loop over data items and display context variables as per design_spec.md.
4. Implement navigation buttons as links or forms referencing correct routes.
5. Mark dynamic IDs using Jinja2 template expressions (e.g., id="view-job-button-{{ job.job_id }}").

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all template files under templates_draft/.
- All element IDs MUST match exactly those specified in user requirements.
- Do NOT implement final polishing or optimization - this is a working draft for later refinement.
- Ensure all local data file formats and field orders comply strictly with specifications.
- Flask app MUST start with dashboard page route as root ('/') redirect or render.

Output: app_draft.py, templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "prompt": """You are a Full Stack Flask Developer specializing in integrating and refining Flask app drafts and templates.

Your goal is to integrate and refine app_draft.py and templates_draft/*.html into a final cohesive Flask application (app.py) and templates set (*.html) fully compliant with design_spec.md and user requirements.

Task Details:
- Read design_spec.md, user_task_description, app_draft.py, and all templates_draft/*.html files.
- Produce final app.py with fully integrated Flask routes and handlers removing any draft dependencies.
- Refine templates from templates_draft/*.html to templates/*.html ensuring all pages, UI element IDs, navigation, and data presentation strictly comply with specifications.
- Ensure all routes, page titles, element IDs, and local data file handling precisely match the design_spec.md requirements.
- The Flask app MUST start at the Dashboard page with root route '/' redirecting or rendering it.
- Refine and fix any inconsistencies, missing features, or errors present in drafts.

Integration and Refinement Guidelines:
1. Merge route handlers ensuring no draft placeholders remain.
2. Use render_template referencing templates/ directory without draft suffix.
3. Implement form submission handling and any POST routes required.
4. Validate local data reading/parsing according to data file schemas.
5. Preserve all UI element IDs exactly as specified.
6. Confirm page titles and navigation links precisely follow specifications.
7. Ensure app.py runs as a cohesive Flask app supporting all user workflows.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app.py and all final template files under templates/.
- Do not alter or add new routes beyond design_spec.md and drafts.
- Maintain exact element ID naming and page titles as specified.
- Remove any draft references from code and templates.
- Focus on integration completeness and correctness as defined.
- Provide clean, runnable final Flask app without draft artifacts.

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"},
                {"type": "user", "name": "user_task_description", "source": "User"}
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
            "review_criteria": "Check that app_draft.py and templates_draft/*.html conform to design_spec.md and user requirements before producing the final integration.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate and finalize the 'JobBoard' Flask application by testing app.py and templates/*.html, then apply fixes to produce the final application.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator inspects and tests the integrated app.py and templates/*.html for syntax correctness, compliance with design_spec.md, route availability, UI element presence (element IDs), data handling, and navigation. "
        "SequentialFixer applies all corrections based on validation_report.md to produce the final runnable Flask application with complete requirement coverage."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in Flask web application validation and quality assurance.

Your goal is to validate the complete integrated Flask application to ensure syntax correctness, adherence to the design specification, route availability, UI element presence, data handling accuracy, and correct navigation behavior, producing a detailed validation report.

Task Details:
- Read input artifacts: app.py, all HTML templates in templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Produce output artifact: validation_report.md with comprehensive test and validation findings
- Focus on confirming the presence of all routes, UI element IDs, local data handling per data schemas, and Dashboard as the start page

Validation Requirements:
1. **Syntax Validation**:
   - Check Python syntax and runtime errors in app.py using validate_python_file tool
   - Confirm HTML syntax correctness in templates/*.html (visual/manual checks or parsing)

2. **Route Validation**:
   - Verify all routes defined in design_spec.md exist in app.py
   - Confirm root route '/' redirects to Dashboard page

3. **UI Elements Validation**:
   - Check presence of ALL element IDs in each HTML template as specified in design_spec.md
   - Verify dynamic IDs (e.g., view-job-button-{job_id}) appear correctly with placeholders or Jinja2 syntax

4. **Data Handling Validation**:
   - Validate app.py data loading from specified local text files complies with design_spec.md data schemas
   - Confirm proper parsing format and field order usage

5. **Navigation and Functionality**:
   - Confirm all navigation buttons and links correctly point to appropriate routes with correct identifiers
   - Check form inputs and submission buttons exist as per specification

CRITICAL REQUIREMENTS:
- Use validate_python_file tool to check app.py
- Use execute_python_code tool to assist any calculations or runtime checks
- Use write_text_file tool to save the detailed validation_report.md
- Format validation_report.md clearly with sections for syntax, routes, UI elements, data handling, navigation findings
- Focus validation on inputs specified only (app.py, templates/*.html, design_spec.md, user task)
- Do NOT modify any input files
- Provide detailed, actionable findings for SequentialFixer to apply

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "prompt": """You are a Full-Stack Developer with expertise in debugging and refining Flask web applications.

Your goal is to apply all corrections stated in the validation_report.md to the existing app.py and templates/*.html files, ensuring full compliance with design_spec.md and complete coverage of user requirements, producing final production-ready Flask application files.

Task Details:
- Read input artifacts: validation_report.md, app.py, templates/*.html, design_spec.md, and user_task_description from CONTEXT
- Output corrected app.py and templates/*.html files reflecting all required fixes
- Scope is limited to fixing issues in app.py and templates only per validation_report.md findings for syntax, routes, UI elements, data handling, and navigation

Fixing Instructions:
1. **Syntax and Runtime Fixes**:
   - Correct all Python syntax and runtime errors in app.py identified by WebValidator
   - Fix any broken HTML markup or missing critical structure in templates

2. **Route and Navigation Fixes**:
   - Ensure all Flask routes match those in design_spec.md precisely
   - Confirm that root route '/' redirects to dashboard page
   - Correct navigation links and buttons to use proper Flask url_for functions and IDs

3. **UI Elements and Template Fixes**:
   - Add or correct missing UI elements with exact IDs as specified
   - Fix dynamic element ID templating with correct Jinja2 syntax
   - Maintain consistent element naming and structure

4. **Data Handling Fixes**:
   - Adjust data loading, parsing, and usage in app.py to match data schema specifications exactly
   - Fix file reading logic, field order, and error handling as needed

5. **Testing and Verification**:
   - Ensure completed fixes resolve all validation issues
   - Preserve or enhance all features required by user specification
   - Deliver clean, maintainable, and runnable Flask app.py and templates

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save all fixed app.py and templates/*.html files
- Deliver final code that passes all syntax validations and meets design_spec.md requirements fully
- Do NOT introduce new features beyond fixing validation issues
- Preserve all user requirements and original design integrity
- Provide outputs in correct file names as input except for corrected content only

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
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
            "review_criteria": "Verify validation_report.md covers all critical syntax, route, UI element ID errors, and data handling issues thoroughly.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm the final app.py and templates/*.html completely address all validation issues while preserving full user requirement coverage.",
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
    goal: str = "Build a comprehensive 'JobBoard' Python Flask web application per user requirements with local text file data storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and create complete design specification for the JobBoard app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the Web design specification including pages, routes, UI elements, and data models."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and templates according to the design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Write draft and final Flask app.py and templates with all specified features and data file handling."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the implementation to produce a fully compliant and functional final web application.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Test, validate, and apply fixes to finalize the Flask web application."}
            ]
        }
    ]
): pass
# Orchestrate_End