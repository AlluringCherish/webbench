# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the OnlineAuction requirements and produce a complete design_spec.md covering Flask routes, templates, page titles, element IDs, and data file usage.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md with detailed tracing of all UI elements, data files, and user flows; then WebArchitect reads requirements_analysis.md "
        "and writes design_spec.md defining Flask routes, template filenames, page titles, element IDs, data handling contracts for text files, and navigation flow including the Dashboard as start page."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Business Analyst specializing in detailed requirements analysis for web applications.

Your goal is to thoroughly analyze the OnlineAuction user requirements to produce a comprehensive requirements_analysis.md that captures every UI element, page, navigation flow, and data file interaction.

Task Details:
- Read the full user_task_description input artifact
- Trace all pages and extract exact page titles, external template filenames, element IDs, action buttons, search and filter options
- Identify all referenced data files and their usage contexts
- Produce one detailed Markdown file requirements_analysis.md capturing these

Analysis Requirements:
1. For each page:
   - List the exact template filename and page-to-template mapping
   - Extract and list the exact page title string
   - Enumerate all element IDs with their element types and descriptions
   - Note all buttons, inputs, search/filter elements, including dynamic IDs with patterns
2. Document data file usage and mapping to UI elements if any
3. Capture navigation flows, especially buttons linking pages, and highlight Dashboard as the start page
4. Present findings in a clear, organized Markdown document

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save requirements_analysis.md
- File must be human-readable with clear sections for each page and data file
- Provide comprehensive coverage of ALL UI elements and data relations described in user input

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

Your goal is to convert detailed requirements analysis into a precise design_spec.md that fully specifies Flask routes, HTTP methods, page titles, element IDs, navigation, context variables, and data file handling conventions.

Task Details:
- Read user_task_description and requirements_analysis.md inputs
- Create design_spec.md defining:
   - Flask route paths and HTTP methods for each user page, ensuring the root route '/' redirects to the Dashboard page
   - Exact template filenames for all pages
   - Precise page titles and all element IDs per page
   - Navigation mappings with routing function names and URLs
   - Context variables passed to templates aligning with UI elements and data files
   - Data file handling contracts for auctions.txt, bids.txt, categories.txt, winners.txt, bid_history.txt, items.txt, trending.txt including field order and usage

Specification Requirements:
1. Flask Routes:
   - For each page, define the route path, HTTP method(s), route function name (lowercase_with_underscores), and associated template filename
2. Templates:
   - List all element IDs required in each page template along with descriptions
3. Navigation:
   - Specify navigation actions with exact url_for() function calls
4. Data Files:
   - For each data file, specify path and exact pipe-delimited fields with order, usage, and examples
5. Enforce Dashboard page as the start/root page with route '/' redirecting there

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save design_spec.md
- All route function names, template names, element IDs, and context variables must match user requirements precisely
- Provide complete and unambiguous design details enabling backend and frontend parallel implementation without ambiguity

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
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
                "Verify requirements_analysis.md includes all pages, exact element IDs, navigation paths, data file references, and UI elements as specified in user requirements."
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
    goal: str = "Implement the OnlineAuction web application with Flask app.py and templates/*.html files adhering to design_spec.md and using local text file data.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html according to design_spec.md, configuring routes, page titles, element IDs, UI interactions, and data parsing from text files; then IntegrationEngineer integrates drafts into final app.py and templates/*.html optimized for Flask rendering and stable functionality."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "prompt": """You are a Backend Developer and Frontend Developer skilled in Flask web development and HTML templating.

Your goal is to draft a complete Flask backend script (app_draft.py) and corresponding HTML templates (templates_draft/*.html) based strictly on the provided design specification.

Task Details:
- Read user_task_description and design_spec.md carefully to ensure full coverage
- Produce app_draft.py implementing all Flask routes with required HTTP methods
- Implement data loading and parsing logic from local text files exactly as specified
- Create all templates_draft/*.html files with exact element IDs, page titles, navigation buttons, forms, and content display per design_spec.md
- Focus solely on drafting versions; do not finalize or refactor for production

Backend Implementation Guidelines:
1. Define Flask app with necessary imports and configuration
2. Implement each route handling GET/POST as specified with correct function names
3. Load and parse text data files with exact field order and no header lines
4. Map parsed data to context variables passed to templates faithfully
5. Handle errors gracefully and ensure app draft runs without syntax errors

Frontend Implementation Guidelines:
1. For each HTML template, include all specified page titles in <title> and <h1> tags
2. Use exact element IDs as specified (including dynamic IDs with Jinja2 syntax)
3. Implement navigation buttons and links directing to correct Flask routes
4. Implement forms with proper method and input field IDs matching design_spec.md
5. Use Jinja2 templating to iterate over data and conditionally display elements

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save app_draft.py and all templates_draft/*.html files
- Follow design_spec.md exactly on routing, IDs, page titles, and data fields
- Ensure data parsing strictly matches file formats in the specification
- Do not finalize or optimize beyond a clean working draft stage

Output: app_draft.py, templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "prompt": """You are a Software Integration Engineer specializing in Flask web applications and frontend-backend integration.

Your goal is to produce a final, runnable Flask backend (app.py) and finalized HTML templates (templates/*.html) by integrating draft implementations.

Task Details:
- Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html thoroughly
- Integrate routes and functionality from app_draft.py into a clean, error-free app.py
- Relocate templates from templates_draft/*.html into templates/*.html, adjusting paths as necessary
- Ensure Flask app.py runs correctly with proper configuration and dependency handling
- Verify all page titles, element IDs, UI interactions, and navigation flows are correct and consistent
- Confirm data parsing reads from local text files exactly per specification and handles all cases robustly

Integration and Finalization Guidelines:
1. Refactor draft code if needed for stability and maintainability, while preserving original route logic
2. Adjust template file paths and includes to reflect the final templates/ directory structure
3. Validate that all navigation and buttons redirect correctly between pages
4. Confirm presence and correctness of all element IDs and page titles as per design_spec.md
5. Perform sanity checks to ensure all required data fields are loaded and presented accurately

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and templates/*.html files
- Maintain strict adherence to design_spec.md and user_task_description
- Ensure final app.py is runnable and templates load flawlessly
- Do not introduce functionality not covered in drafts or design specification

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
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
                "Check that app_draft.py and templates_draft/*.html adhere to design_spec.md exactly with correct routes, element IDs, page titles, data handling, and UI elements before integration."
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
    goal: str = "Validate app.py and templates/*.html through syntax, runtime, and functionality checks; produce validation_report.md and final corrected application.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator validates app.py and templates/*.html for syntax, execution, route correctness, page rendering, UI element presence, navigation, and data file integration writing validation_report.md; then SequentialFixer updates app.py and templates/*.html resolving issues to deliver a fully compliant final application."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "prompt": """You are a Software Test Engineer specializing in validating Python Flask web applications with HTML templating.

Your goal is to validate the complete web application including backend and frontend components to ensure syntax correctness, successful runtime, accurate routing, UI presence, navigation fidelity, and proper data integration. Deliver a detailed validation_report.md summarizing all findings.

Task Details:
- Read user_task_description describing functional requirements and UI elements
- Read design_spec.md specifying complete app.py and templates/*.html specifications
- Read app.py and templates/*.html for actual implementation to validate
- Produce validation_report.md including detailed diagnostics and issues

**Validation Tasks**

1. **Syntax and Runtime Checks:**
   - Use validate_python_file tool for syntax and runtime validation of app.py
   - Execute app.py if needed to ensure startup succeeds without errors

2. **Route and Page Functionality Testing:**
   - Use Flask test client or appropriate execute_python_code calls to test all routes
   - Verify correct HTTP methods are accepted and rendered pages are returned
   - Confirm root route redirects to dashboard

3. **UI Element Presence and Attributes:**
   - Parse rendered HTML for required element IDs on each page as specified in design_spec.md
   - Verify element types and presence of dynamic ID patterns (e.g., view-auction-button-{auction_id})
   - Confirm page titles match exactly those specified in user_task_description and design_spec.md

4. **Navigation Functionality:**
   - Test navigation buttons and links for correct url_for routing
   - Confirm all navigation elements function properly on all pages

5. **Data Integration Validation:**
   - Verify data files (auctions.txt, bids.txt, categories.txt, etc.) are loaded and reflected accurately in page content
   - Check filtering, sorting, and listing features incorporate data file contents correctly

CRITICAL REQUIREMENTS:
- MUST use validate_python_file and execute_python_code tools for automated validation steps
- Write detailed issues and confirmations in validation_report.md using write_text_file tool
- Validation report MUST cover syntax, runtime, routing, UI elements, navigation, and data integration comprehensively
- Focus strictly on implemented files: app.py and templates/*.html in context of design_spec.md and user requirements

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
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
            "prompt": """You are a Software Developer specializing in debugging and refining Flask web applications with HTML templating.

Your goal is to apply all corrections and improvements detailed in validation_report.md to produce a fully working, standards-compliant final app.py and templates/*.html set that satisfies all original user requirements and design specifications.

Task Details:
- Read user_task_description for functional and UI requirements
- Read design_spec.md for detailed implementation specifications
- Read current app.py and templates/*.html files as baseline code
- Read validation_report.md identifying all problems, bugs, and enhancement suggestions
- Deliver corrected app.py and templates/*.html fully addressing all validation findings

**Refinement Guidelines**

1. **Bug Fixing:**
   - Resolve all syntax and runtime errors in app.py
   - Fix missing or incorrect Flask routes, context variables, and HTTP methods
   - Correct form submissions and POST handling as needed

2. **UI Corrections:**
   - Add or fix all required element IDs and dynamic ID patterns in templates
   - Ensure page titles and content match user requirements exactly
   - Repair broken or missing navigation elements and routing links

3. **Data Handling Improvements:**
   - Correct data loading and filtering logic to match data files like auctions.txt, bids.txt, etc.
   - Validate that displayed content reflects accurate and complete data from source files

4. **Best Practices:**
   - Maintain consistent code style and naming conventions per design_spec.md
   - Verify no functionality regressions are introduced

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save corrected app.py and templates/*.html files
- Focus exclusively on fixing issues reported in validation_report.md
- Preserve functionality and features specified in user_task_description and design_spec.md
- Do not add new features beyond validation corrections

Output: app.py; templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"}
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
                "Ensure validation_report.md includes complete and actionable information about syntax, runtime, routing, template correctness, UI elements, and data integration issues."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify final app.py and templates/*.html fully satisfy user requirements and resolve all issues reported in validation_report.md."
            ),
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
    goal: str = "Complete the 'OnlineAuction' Python web application per requirements with validated, fully functional Flask app.py and templates.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and create design specification for the OnlineAuction application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the detailed design specification including Flask routes, templates, and data handling."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the OnlineAuction application with Flask and Jinja2 templates using local text file data, as per design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop app.py and templates implementing the full required functionality and UI."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the final OnlineAuction application ensuring correctness, usability, and compliance.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and refine the final Flask application producing a fully compliant final product."}
            ]
        }
    ]
): pass
# Orchestrate_End